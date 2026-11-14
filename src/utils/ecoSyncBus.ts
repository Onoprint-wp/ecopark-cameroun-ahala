// ============================================================================
// BACKOFFICE <-> FRONTEND REAL-TIME SYNC BUS, RBAC STORE GUARDS & CLOUD MAPPER
// (src/utils/ecoSyncBus.ts)
// ============================================================================

import type {
  AuthenticatedUser,
  CitizenReport,
  EcoParkRole,
  EcoPass,
  ExperienceType,
  MobilityMode,
  ParkTelemetry,
  Trail,
} from '../types/ecosystem.ts';
import {
  AUTH_STORAGE_KEYS,
  canCheckInPasses,
  canManageParkOperations,
  isStaffRole,
  isSupabaseCloudConfigured,
} from './ecoAuth.ts';

export const SYNC_CHANNEL_NAME = 'eco_park_ahala_v2_bus';

export const SHARED_DOMAIN_KEYS = new Set<string>([
  'eco_park_ahala_v2_trails',
  'eco_park_ahala_v2_telemetry',
  'eco_park_ahala_v2_passes',
  'eco_park_ahala_v2_reports',
]);

export const TAB_LOCAL_UI_KEYS = new Set<string>([
  'eco_park_ahala_v2_active_view',
  'eco_park_ahala_v2_selected_trail',
  'eco_park_ahala_v2_selected_species',
  'eco_park_ahala_v2_active_pass_id',
  'eco_park_ahala_v2_drawer_open',
  'eco_park_ahala_v2_session_unlocked_passes',
]);

/**
 * Returns true strictly for shared domain state (Trails, Telemetry, Passes, Reports)
 * and false for tab-local UI state (ActiveView, SelectedTrail, Drawer, SessionPass),
 * preventing cross-tab navigation hijacking between /exploitation and visitor tabs.
 */
export function isCrossTabSyncedKey(storageKey: string): boolean {
  if (TAB_LOCAL_UI_KEYS.has(storageKey)) return false;
  return SHARED_DOMAIN_KEYS.has(storageKey);
}

export type SyncDomain = 'trails' | 'telemetry' | 'passes' | 'reports' | 'reset';

export interface SyncMeta {
  tabId: string;
  transport: 'broadcast_storage' | 'supabase_hybrid';
  lastSyncedAt: string | null;
  lastDomain: SyncDomain | 'init';
  lastActorRole: EcoParkRole | null;
  publishedCount: number;
  receivedCount: number;
}

export interface SyncEnvelope {
  id: string;
  senderTabId: string;
  domain: SyncDomain;
  timestamp: string;
  actorRole: EcoParkRole;
  trails?: Trail[];
  telemetry?: ParkTelemetry;
  passes?: EcoPass[];
  reports?: CitizenReport[];
}

export interface EcoSyncBusHandle {
  tabId: string;
  publish: (payload: Omit<SyncEnvelope, 'id' | 'senderTabId' | 'timestamp'>) => SyncEnvelope;
  close: () => void;
}

export function generateTabInstanceId(): string {
  const rand = Math.random().toString(36).slice(2, 10);
  return `tab-${Date.now().toString(36)}-${rand}`;
}

/**
 * Creates a real-time BroadcastChannel bus for sub-20ms synchronization between
 * Backoffice (/exploitation) and Frontend tabs, ignoring self-echoes and duplicates.
 */
export function createEcoSyncBus(
  tabId: string,
  onReceive: (envelope: SyncEnvelope) => void,
  channelName: string = SYNC_CHANNEL_NAME
): EcoSyncBusHandle {
  let channel: BroadcastChannel | null = null;
  const seenIds = new Set<string>();

  if (typeof BroadcastChannel !== 'undefined') {
    try {
      channel = new BroadcastChannel(channelName);
      channel.onmessage = (event: MessageEvent<SyncEnvelope>) => {
        const env = event?.data;
        if (!env || typeof env !== 'object' || typeof env.id !== 'string') return;
        if (env.senderTabId === tabId) return;
        if (seenIds.has(env.id)) return;
        seenIds.add(env.id);
        if (seenIds.size > 200) {
          const oldest = seenIds.values().next().value;
          if (oldest) seenIds.delete(oldest);
        }
        onReceive(env);
      };
    } catch {
      channel = null;
    }
  }

  const publish = (
    partial: Omit<SyncEnvelope, 'id' | 'senderTabId' | 'timestamp'>
  ): SyncEnvelope => {
    const envelope: SyncEnvelope = {
      ...partial,
      id: `sync-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
      senderTabId: tabId,
      timestamp: new Date().toISOString(),
    };
    seenIds.add(envelope.id);
    if (channel) {
      try {
        channel.postMessage(envelope);
      } catch {
        // Ignore closed or unavailable BroadcastChannel errors
      }
    }
    return envelope;
  };

  const close = () => {
    if (channel) {
      try {
        channel.close();
      } catch {
        // Ignore close errors
      }
      channel = null;
    }
  };

  return { tabId, publish, close };
}

// ----------------------------------------------------------------------------
// Defense-in-Depth Store RBAC Guards
// ----------------------------------------------------------------------------

export function canMutateBackofficeOps(role?: EcoParkRole | null): boolean {
  return canManageParkOperations(role);
}

export function canMutatePassCheckIn(role?: EcoParkRole | null): boolean {
  return canCheckInPasses(role);
}

export function canActorCancelPass(
  pass: EcoPass,
  user: AuthenticatedUser | null,
  sessionUnlockedPassIds: string[]
): boolean {
  if (pass.status === 'cancelled') return false;

  // Operations managers (Chef d Exploitation, Direction, Administrateur) can cancel any pass
  if (canManageParkOperations(user?.role)) {
    return true;
  }

  // Non-ops staff (agent_guichet, agent_controle, comptable) cannot cancel passes
  if (user && isStaffRole(user.role)) {
    return false;
  }

  // Anonymized passes cannot be cancelled by public users
  if (pass.ownerEmail === 'anonyme@effacement.local') {
    return false;
  }

  // Authenticated client can cancel only their own pass
  if (user) {
    const normEmail = user.email.trim().toLowerCase();
    return (
      pass.ownerUserId === user.id ||
      pass.ownerEmail?.toLowerCase() === normEmail ||
      pass.leadVisitor.email.trim().toLowerCase() === normEmail
    );
  }

  // Anonymous visitor can cancel only passes unlocked in their active browser tab session
  return sessionUnlockedPassIds.includes(pass.id);
}

// ----------------------------------------------------------------------------
// Live Booking Race-Condition Validator (Backoffice -> Frontend Contract)
// ----------------------------------------------------------------------------

export type BookingConstraintErrorCode =
  | 'INVALID_DATE'
  | 'PAST_DATE'
  | 'MONDAY_REST_DAY'
  | 'TRAIL_CLOSED'
  | 'EMPTY_GUESTS'
  | 'QUOTA_EXCEEDED';

export interface LiveBookingValidationResult {
  ok: boolean;
  code?: BookingConstraintErrorCode;
  error?: string;
  availablePlaces: number;
}

export function validateLiveBookingConstraints(params: {
  visitDate: string;
  todayIso: string;
  guestCount: number;
  dailyCapacityMax: number;
  currentBookedForDate: number;
  selectedTrail: Pick<Trail, 'id' | 'name' | 'status' | 'closureReason'> | null;
}): LiveBookingValidationResult {
  const availablePlaces = Math.max(
    0,
    Math.round(params.dailyCapacityMax) - Math.round(params.currentBookedForDate)
  );

  if (!params.visitDate) {
    return {
      ok: false,
      code: 'INVALID_DATE',
      error: 'Veuillez sélectionner une date de visite.',
      availablePlaces,
    };
  }

  if (params.visitDate < params.todayIso) {
    return {
      ok: false,
      code: 'PAST_DATE',
      error: "La date de visite ne peut pas être antérieure à aujourd'hui.",
      availablePlaces,
    };
  }

  const dayOfWeek = new Date(`${params.visitDate}T12:00:00`).getDay();
  if (dayOfWeek === 1) {
    return {
      ok: false,
      code: 'MONDAY_REST_DAY',
      error:
        'Le Parc et les Loisirs sont fermés le lundi pour repos biologique hebdomadaire (ouverture du mardi au dimanche de 09h00 à 18h00).',
      availablePlaces,
    };
  }

  if (params.selectedTrail && params.selectedTrail.status === 'ferme') {
    const reason =
      params.selectedTrail.closureReason || 'accès temporairement suspendu par le poste de garde';
    return {
      ok: false,
      code: 'TRAIL_CLOSED',
      error: `Le circuit « ${params.selectedTrail.name} » est actuellement fermé (${reason}). Choisissez un autre circuit ou poursuivez sur les zones ouvertes du parc.`,
      availablePlaces,
    };
  }

  if (params.guestCount <= 0) {
    return {
      ok: false,
      code: 'EMPTY_GUESTS',
      error: 'Veuillez inclure au moins un visiteur.',
      availablePlaces,
    };
  }

  if (params.guestCount > availablePlaces) {
    return {
      ok: false,
      code: 'QUOTA_EXCEEDED',
      error:
        availablePlaces <= 0
          ? 'Le quota écologique vient d être atteint pour cette date. Veuillez choisir un autre jour.'
          : `Jauge mise à jour en direct : seulement ${availablePlaces} place(s) restante(s) pour ${params.guestCount} visiteur(s) demandé(s).`,
      availablePlaces,
    };
  }

  return { ok: true, availablePlaces };
}

// ----------------------------------------------------------------------------
// Exact SQL Schema Mapper: EcoPass <-> public.bookings (Migration 1 & 2)
// ----------------------------------------------------------------------------

export interface SupabaseBookingRow {
  reference_code: string;
  visitor_name: string;
  visitor_phone: string;
  visit_date: string;
  visit_profile: string;
  adults_count: number;
  children_count: number;
  toddlers_count: number;
  selected_activities: string[];
  selected_bundle_code: string | null;
  total_fcfa: number;
  payment_method: 'OM' | 'MOMO' | 'GUICHET';
  payment_state: 'PENDING' | 'CONFIRMED' | 'FAILED' | 'EXPIRED' | 'CANCELLED';
  qr_status: 'VALID' | 'USED' | 'WRONG_DATE' | 'EXPIRED' | 'CANCELLED' | 'WRONG_ZONE' | 'UNKNOWN';
  scanned_at: string | null;
  scanned_by: string | null;
}

function mapExperienceToBundle(exp: ExperienceType): {
  bundleCode: string | null;
  activities: string[];
} {
  switch (exp) {
    case 'atelier_botanique':
      return { bundleCode: 'PASS_ROYALE', activities: ['zoo', 'piscine', 'pirogue', 'saveurs'] };
    case 'pack_mobilite':
      return { bundleCode: 'PASS_DECOUVERTE', activities: ['zoo', 'piscine', 'pirogue'] };
    case 'eco_guide':
      return { bundleCode: 'PASS_DECOUVERTE', activities: ['zoo', 'pirogue', 'cheval'] };
    case 'sentiers':
    default:
      return { bundleCode: null, activities: ['zoo'] };
  }
}

function mapMobilityToPaymentMethod(mode: MobilityMode): 'OM' | 'MOMO' | 'GUICHET' {
  if (mode === 'train') return 'OM';
  if (mode === 'voiture_solo') return 'GUICHET';
  return 'MOMO';
}

/**
 * Converts a frontend EcoPass into a strict public.bookings row complying with
 * PostgreSQL CHECK constraints (adults_count + children_count >= 1, total_fcfa Int >= 0).
 */
export function mapEcoPassToSupabaseBookingRow(
  pass: EcoPass,
  scannedByMatricule?: string
): SupabaseBookingRow {
  const rawAdults = pass.adultCount ?? pass.guestCount;
  const rawChildren = pass.childCount ?? 0;
  const safeAdults = rawAdults + rawChildren >= 1 ? Math.max(0, rawAdults) : 1;
  const safeChildren = Math.max(0, rawChildren);
  const { bundleCode, activities } = mapExperienceToBundle(pass.experienceType);

  return {
    reference_code: pass.id,
    visitor_name: pass.leadVisitor.fullName,
    visitor_phone: pass.leadVisitor.phone || '+237 600 00 00 00',
    visit_date: pass.visitDate,
    visit_profile: pass.guestCount >= 20 ? 'groupe' : safeChildren > 0 ? 'famille' : 'individuel',
    adults_count: safeAdults,
    children_count: safeChildren,
    toddlers_count: 0,
    selected_activities: activities,
    selected_bundle_code: bundleCode,
    total_fcfa: Math.max(0, Math.round(pass.totalPriceEur)),
    payment_method: mapMobilityToPaymentMethod(pass.mobilityMode),
    payment_state: pass.status === 'cancelled' ? 'CANCELLED' : 'CONFIRMED',
    qr_status:
      pass.status === 'checked_in'
        ? 'USED'
        : pass.status === 'cancelled'
        ? 'CANCELLED'
        : 'VALID',
    scanned_at: pass.checkInTimestamp || null,
    scanned_by: pass.status === 'checked_in' ? scannedByMatricule || 'GUICHET_RN3' : null,
  };
}

function readSupabaseClientEnv(): { url: string; anonKey: string } | null {
  if (!isSupabaseCloudConfigured()) return null;
  try {
    const metaEnv = (import.meta as unknown as { env?: Record<string, string | undefined> }).env;
    const url = (metaEnv?.VITE_SUPABASE_URL || '').trim().replace(/\/+$/, '');
    const anonKey = (metaEnv?.VITE_SUPABASE_ANON_KEY || '').trim();
    return url && anonKey ? { url, anonKey } : null;
  } catch {
    return null;
  }
}

function readBearerTokenIfPresent(anonKey: string): string {
  if (typeof window === 'undefined') return anonKey;
  try {
    const raw = window.localStorage.getItem(AUTH_STORAGE_KEYS.SUPABASE_SESSION);
    if (!raw) return anonKey;
    const parsed = JSON.parse(raw) as { access_token?: string };
    return parsed?.access_token || anonKey;
  } catch {
    return anonKey;
  }
}

/**
 * Non-blocking optional PostgREST synchronization when VITE_SUPABASE_URL is configured.
 * Silently preserves local autonomous operation when Cloud is unconfigured or unreachable.
 */
export async function syncPassToSupabaseCloudIfActive(
  pass: EcoPass,
  operation: 'upsert' | 'check_in' | 'cancel',
  actorMatricule?: string
): Promise<boolean> {
  const cfg = readSupabaseClientEnv();
  if (!cfg || typeof fetch === 'undefined') return false;

  const bearer = readBearerTokenIfPresent(cfg.anonKey);
  const row = mapEcoPassToSupabaseBookingRow(pass, actorMatricule);

  try {
    if (operation === 'upsert') {
      const res = await fetch(`${cfg.url}/rest/v1/bookings?on_conflict=reference_code`, {
        method: 'POST',
        headers: {
          apikey: cfg.anonKey,
          Authorization: `Bearer ${bearer}`,
          'Content-Type': 'application/json',
          Prefer: 'resolution=merge-duplicates,return=minimal',
        },
        body: JSON.stringify(row),
      });
      return res.ok;
    }

    const patchBody =
      operation === 'check_in'
        ? {
            qr_status: 'USED',
            scanned_at: row.scanned_at || new Date().toISOString(),
            scanned_by: row.scanned_by,
          }
        : {
            payment_state: 'CANCELLED',
            qr_status: 'CANCELLED',
            cancelled_at: new Date().toISOString(),
          };

    const res = await fetch(
      `${cfg.url}/rest/v1/bookings?reference_code=eq.${encodeURIComponent(pass.id)}`,
      {
        method: 'PATCH',
        headers: {
          apikey: cfg.anonKey,
          Authorization: `Bearer ${bearer}`,
          'Content-Type': 'application/json',
          Prefer: 'return=minimal',
        },
        body: JSON.stringify(patchBody),
      }
    );
    return res.ok;
  } catch {
    return false;
  }
}
