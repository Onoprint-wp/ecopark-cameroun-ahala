// ============================================================================
// ECO-PARK CENTRAL REACTIVE STORE (src/context/EcoParkContext.tsx)
// Bidirectional Backoffice (/exploitation) <-> Frontend Sync with RBAC Guards
// ============================================================================

import React, {
  createContext,
  useContext,
  useState,
  useEffect,
  useCallback,
  useMemo,
  useRef,
  ReactNode,
} from 'react';
import {
  ActiveView,
  Trail,
  TrailStatus,
  EcoPass,
  BookingInput,
  CitizenReport,
  ReportInput,
  ReportStatus,
  ParkTelemetry,
  EcoParkContextType,
  EcoParkRole,
} from '../types/ecosystem';
import {
  INITIAL_TELEMETRY,
  INITIAL_POIS,
  INITIAL_TRAILS,
  INITIAL_SPECIES,
  INITIAL_PASSES,
  INITIAL_REPORTS,
} from '../data/initialParkData';
import { useTheme } from './ThemeContext';
import { useAuth } from './AuthContext';
import { runEcoViewTransition, emitTrailStatusWave } from '../utils/ecoMotion';
import { resolveViewFromPath, VIEW_PATH_MAP } from '../utils/ecoRouting';
import {
  verifyAnonymousPassLookup,
  anonymizeClientPassesList,
  isSupabaseCloudConfigured,
} from '../utils/ecoAuth';
import {
  createEcoSyncBus,
  generateTabInstanceId,
  isCrossTabSyncedKey,
  canMutateBackofficeOps,
  canMutatePassCheckIn,
  canActorCancelPass,
  syncPassToSupabaseCloudIfActive,
  type EcoSyncBusHandle,
  type SyncDomain,
  type SyncEnvelope,
  type SyncMeta,
} from '../utils/ecoSyncBus';

// Storage keys under strict eco_park_ahala_v2_* namespace
export const STORAGE_KEYS = {
  // Shared cross-tab domain keys (localStorage + BroadcastChannel)
  TRAILS: 'eco_park_ahala_v2_trails',
  TELEMETRY: 'eco_park_ahala_v2_telemetry',
  PASSES: 'eco_park_ahala_v2_passes',
  REPORTS: 'eco_park_ahala_v2_reports',

  // Tab-isolated UI & navigation keys (sessionStorage ONLY - never hijacks other tabs)
  ACTIVE_VIEW: 'eco_park_ahala_v2_active_view',
  SELECTED_TRAIL: 'eco_park_ahala_v2_selected_trail',
  SELECTED_SPECIES: 'eco_park_ahala_v2_selected_species',
  ACTIVE_PASS_ID: 'eco_park_ahala_v2_active_pass_id',
  DRAWER_OPEN: 'eco_park_ahala_v2_drawer_open',
  SESSION_UNLOCKED_PASSES: 'eco_park_ahala_v2_session_unlocked_passes',
};

// Resilient safeLocalStorage helper for shared cross-tab domain data
export const safeLocalStorage = {
  getItem: <T,>(key: string, fallback: T): T => {
    if (typeof window === 'undefined') return fallback;
    try {
      const item = window.localStorage.getItem(key);
      if (item === null) return fallback;
      return JSON.parse(item) as T;
    } catch (err) {
      console.warn(`[safeLocalStorage] Failed to parse key "${key}", reverting to fallback:`, err);
      return fallback;
    }
  },
  setItem: <T,>(key: string, value: T): void => {
    if (typeof window === 'undefined') return;
    try {
      window.localStorage.setItem(key, JSON.stringify(value));
    } catch (err) {
      console.warn(`[safeLocalStorage] Failed to write key "${key}":`, err);
    }
  },
  removeItem: (key: string): void => {
    if (typeof window === 'undefined') return;
    try {
      window.localStorage.removeItem(key);
    } catch (err) {
      console.warn(`[safeLocalStorage] Failed to remove key "${key}":`, err);
    }
  },
};

// Resilient safeSessionStorage helper for strictly tab-local navigation & UI state
export const safeSessionStorage = {
  getItem: <T,>(key: string, fallback: T): T => {
    if (typeof window === 'undefined' || !window.sessionStorage) return fallback;
    try {
      const item = window.sessionStorage.getItem(key);
      if (item === null) return fallback;
      return JSON.parse(item) as T;
    } catch {
      return fallback;
    }
  },
  setItem: <T,>(key: string, value: T): void => {
    if (typeof window === 'undefined' || !window.sessionStorage) return;
    try {
      window.sessionStorage.setItem(key, JSON.stringify(value));
    } catch {
      // Ignore quota or privacy errors
    }
  },
  removeItem: (key: string): void => {
    if (typeof window === 'undefined' || !window.sessionStorage) return;
    try {
      window.sessionStorage.removeItem(key);
    } catch {
      // Ignore storage errors
    }
  },
};

const EcoParkContext = createContext<EcoParkContextType | undefined>(undefined);

export interface EcoParkProviderProps {
  children: ReactNode;
}

export const EcoParkProvider: React.FC<EcoParkProviderProps> = ({ children }) => {
  const {
    themeMode,
    effectiveTheme,
    setThemeMode,
    daltonismMode,
    setDaltonismMode,
    highContrastOutdoor,
    setHighContrastOutdoor,
  } = useTheme();

  const { user } = useAuth();
  const userRef = useRef(user);
  userRef.current = user;

  const tabIdRef = useRef<string>(generateTabInstanceId());
  const syncBusRef = useRef<EcoSyncBusHandle | null>(null);

  const [syncMeta, setSyncMeta] = useState<SyncMeta>(() => ({
    tabId: tabIdRef.current,
    transport: isSupabaseCloudConfigured() ? 'supabase_hybrid' : 'broadcast_storage',
    lastSyncedAt: null,
    lastDomain: 'init',
    lastActorRole: null,
    publishedCount: 0,
    receivedCount: 0,
  }));

  // Tab-isolated navigation state (resolved from URL pathname first, then sessionStorage)
  const [activeView, setActiveViewState] = useState<ActiveView>(() => {
    if (typeof window !== 'undefined') {
      const fromUrl = resolveViewFromPath(window.location.pathname);
      if (fromUrl) return fromUrl;
    }
    return safeSessionStorage.getItem<ActiveView>(STORAGE_KEYS.ACTIVE_VIEW, 'accueil');
  });

  // Tab-isolated UI states (never overwrite other tabs)
  const [colorDrawerOpen, setColorDrawerOpenState] = useState<boolean>(() =>
    safeSessionStorage.getItem<boolean>(STORAGE_KEYS.DRAWER_OPEN, false)
  );

  const [selectedTrailId, setSelectedTrailIdState] = useState<string | null>(() =>
    safeSessionStorage.getItem<string | null>(STORAGE_KEYS.SELECTED_TRAIL, null)
  );

  const [selectedSpeciesId, setSelectedSpeciesIdState] = useState<string | null>(() =>
    safeSessionStorage.getItem<string | null>(STORAGE_KEYS.SELECTED_SPECIES, null)
  );

  const [activePassId, setActivePassIdState] = useState<string | null>(() =>
    safeSessionStorage.getItem<string | null>(STORAGE_KEYS.ACTIVE_PASS_ID, null)
  );

  const [sessionUnlockedPassIds, setSessionUnlockedPassIdsState] = useState<string[]>(() =>
    safeSessionStorage.getItem<string[]>(STORAGE_KEYS.SESSION_UNLOCKED_PASSES, [])
  );
  const sessionUnlockedRef = useRef<string[]>(sessionUnlockedPassIds);
  sessionUnlockedRef.current = sessionUnlockedPassIds;

  // Shared cross-tab domain states (persisted in localStorage + BroadcastChannel)
  const [telemetry, setTelemetryState] = useState<ParkTelemetry>(() =>
    safeLocalStorage.getItem<ParkTelemetry>(STORAGE_KEYS.TELEMETRY, INITIAL_TELEMETRY)
  );

  const [trails, setTrailsState] = useState<Trail[]>(() =>
    safeLocalStorage.getItem<Trail[]>(STORAGE_KEYS.TRAILS, INITIAL_TRAILS)
  );

  const [passes, setPassesState] = useState<EcoPass[]>(() =>
    safeLocalStorage.getItem<EcoPass[]>(STORAGE_KEYS.PASSES, INITIAL_PASSES)
  );

  const [reports, setReportsState] = useState<CitizenReport[]>(() =>
    safeLocalStorage.getItem<CitizenReport[]>(STORAGE_KEYS.REPORTS, INITIAL_REPORTS)
  );

  // Live synchronous refs so cross-domain mutators & sync listeners never read stale closures
  const telemetryRef = useRef<ParkTelemetry>(telemetry);
  telemetryRef.current = telemetry;
  const trailsRef = useRef<Trail[]>(trails);
  trailsRef.current = trails;
  const passesRef = useRef<EcoPass[]>(passes);
  passesRef.current = passes;
  const reportsRef = useRef<CitizenReport[]>(reports);
  reportsRef.current = reports;

  const unlockPassForSession = useCallback((passId: string) => {
    setSessionUnlockedPassIdsState((prev) => {
      const next = prev.includes(passId) ? prev : [passId, ...prev];
      sessionUnlockedRef.current = next;
      safeSessionStorage.setItem(STORAGE_KEYS.SESSION_UNLOCKED_PASSES, next);
      return next;
    });
  }, []);

  // Reconcile global on-site occupancy = open trails headcount + today's net booked pass delta
  const reconcileTodayOccupancy = useCallback(
    (trailsList: Trail[], passesList: EcoPass[], dailyMax: number): number => {
      const todayIso = new Date().toISOString().split('T')[0];
      const openTrailsOccupancy = trailsList
        .filter((t) => t.status !== 'ferme')
        .reduce((sum, t) => sum + t.currentOccupancy, 0);

      const seedTodayGuests = INITIAL_PASSES.filter(
        (p) => p.visitDate === todayIso && p.status !== 'cancelled'
      ).reduce((sum, p) => sum + p.guestCount, 0);

      const activeTodayGuests = passesList
        .filter((p) => p.visitDate === todayIso && p.status !== 'cancelled')
        .reduce((sum, p) => sum + p.guestCount, 0);

      const todayNetDelta = activeTodayGuests - seedTodayGuests;
      return Math.max(0, Math.min(dailyMax, openTrailsOccupancy + todayNetDelta));
    },
    []
  );

  const publishSyncUpdate = useCallback(
    (
      domain: SyncDomain,
      payload: {
        trails?: Trail[];
        telemetry?: ParkTelemetry;
        passes?: EcoPass[];
        reports?: CitizenReport[];
      }
    ) => {
      const actorRole: EcoParkRole = userRef.current?.role || 'visiteur_anonyme';
      const sent = syncBusRef.current?.publish({
        domain,
        actorRole,
        ...payload,
      });
      const ts = sent?.timestamp || new Date().toISOString();
      setSyncMeta((prev) => ({
        ...prev,
        lastSyncedAt: ts,
        lastDomain: domain,
        lastActorRole: actorRole,
        publishedCount: prev.publishedCount + 1,
      }));
    },
    []
  );

  // Browser Back / Forward URL history synchronization (tab-local)
  useEffect(() => {
    if (typeof window === 'undefined') return;
    const handlePopState = () => {
      const resolved = resolveViewFromPath(window.location.pathname) || 'accueil';
      safeSessionStorage.setItem(STORAGE_KEYS.ACTIVE_VIEW, resolved);
      setActiveViewState(resolved);
    };
    window.addEventListener('popstate', handlePopState);
    return () => window.removeEventListener('popstate', handlePopState);
  }, []);

  // --------------------------------------------------------------------------
  // Tab-Isolated UI Mutators (sessionStorage ONLY)
  // --------------------------------------------------------------------------

  const setActiveView = useCallback((view: ActiveView) => {
    safeSessionStorage.setItem(STORAGE_KEYS.ACTIVE_VIEW, view);
    if (typeof window !== 'undefined') {
      const targetPath = VIEW_PATH_MAP[view] || '/';
      if (window.location.pathname !== targetPath) {
        window.history.pushState({ ecoView: view }, '', targetPath);
      }
    }

    runEcoViewTransition('lisiere', () => {
      setActiveViewState(view);
      if (typeof window !== 'undefined') {
        window.scrollTo({ top: 0, behavior: 'instant' as ScrollBehavior });
      }
    });
  }, []);

  const setColorDrawerOpen = useCallback((open: boolean) => {
    setColorDrawerOpenState(open);
    safeSessionStorage.setItem(STORAGE_KEYS.DRAWER_OPEN, open);
  }, []);

  const setSelectedTrailId = useCallback((trailId: string | null) => {
    setSelectedTrailIdState(trailId);
    safeSessionStorage.setItem(STORAGE_KEYS.SELECTED_TRAIL, trailId);
  }, []);

  const setSelectedSpeciesId = useCallback((speciesId: string | null) => {
    setSelectedSpeciesIdState(speciesId);
    safeSessionStorage.setItem(STORAGE_KEYS.SELECTED_SPECIES, speciesId);
  }, []);

  const setActivePassId = useCallback((id: string | null) => {
    setActivePassIdState(id);
    safeSessionStorage.setItem(STORAGE_KEYS.ACTIVE_PASS_ID, id);
  }, []);

  // --------------------------------------------------------------------------
  // RBAC-Guarded Backoffice & Bidirectional Domain Mutators
  // --------------------------------------------------------------------------

  const setDailyCapacity = useCallback(
    (newCap: number) => {
      if (!canMutateBackofficeOps(userRef.current?.role)) {
        console.warn('[EcoPark RBAC] setDailyCapacity refused: operational staff role required.');
        return;
      }

      const clampedMax = Math.max(500, Math.min(3000, Math.round(newCap)));
      const updatedTelem: ParkTelemetry = {
        ...telemetryRef.current,
        dailyCapacityMax: clampedMax,
        currentOccupancy: reconcileTodayOccupancy(
          trailsRef.current,
          passesRef.current,
          clampedMax
        ),
      };

      telemetryRef.current = updatedTelem;
      safeLocalStorage.setItem(STORAGE_KEYS.TELEMETRY, updatedTelem);
      setTelemetryState(updatedTelem);
      publishSyncUpdate('telemetry', { telemetry: updatedTelem });
    },
    [publishSyncUpdate, reconcileTodayOccupancy]
  );

  const updateTrailStatus = useCallback(
    (trailId: string, status: TrailStatus, closureReason?: string) => {
      if (!canMutateBackofficeOps(userRef.current?.role)) {
        console.warn('[EcoPark RBAC] updateTrailStatus refused: operational staff role required.');
        return;
      }

      emitTrailStatusWave(trailId, status);
      const nextTrails = trailsRef.current.map((trail) => {
        if (trail.id !== trailId && trail.slug !== trailId) return trail;
        const updatedOccupancy =
          status === 'ferme'
            ? 0
            : trail.status === 'ferme'
            ? Math.floor(trail.maxCapacity * 0.4)
            : trail.currentOccupancy;

        const nextNotice =
          status === 'fluide'
            ? undefined
            : closureReason !== undefined
            ? closureReason
            : status === 'ferme'
            ? trail.closureReason || 'Fermeture préventive temporaire'
            : trail.closureReason || 'Circulation encadrée par les Éco-Gardes';

        return {
          ...trail,
          status,
          closureReason: nextNotice,
          currentOccupancy: updatedOccupancy,
        };
      });

      const updatedTelem: ParkTelemetry = {
        ...telemetryRef.current,
        currentOccupancy: reconcileTodayOccupancy(
          nextTrails,
          passesRef.current,
          telemetryRef.current.dailyCapacityMax
        ),
      };

      trailsRef.current = nextTrails;
      telemetryRef.current = updatedTelem;
      safeLocalStorage.setItem(STORAGE_KEYS.TRAILS, nextTrails);
      safeLocalStorage.setItem(STORAGE_KEYS.TELEMETRY, updatedTelem);
      setTrailsState(nextTrails);
      setTelemetryState(updatedTelem);
      publishSyncUpdate('trails', { trails: nextTrails, telemetry: updatedTelem });
    },
    [publishSyncUpdate, reconcileTodayOccupancy]
  );

  const bookPass = useCallback(
    (input: BookingInput): EcoPass => {
      const randomDigits = Math.floor(10000 + Math.random() * 90000);
      const newId = `ECP-2026-${randomDigits}`;
      const nowIso = new Date().toISOString();

      const newPass: EcoPass = {
        ...input,
        unitPriceEur: Math.round(input.unitPriceEur),
        totalPriceEur: Math.round(input.totalPriceEur),
        ownerEmail: (input.ownerEmail || input.leadVisitor.email || '').trim().toLowerCase(),
        id: newId,
        createdAt: nowIso,
        status: 'confirmed',
        qrPayload: `ECOPARK-AHALA:PASS:${newId}:DATE=${input.visitDate}:SLOT=${input.timeSlot}:GUESTS=${input.guestCount}:FORMULE=${input.experienceType.toUpperCase()}:MODE=${input.mobilityMode}`,
      };

      const nextPasses = [newPass, ...passesRef.current];
      const nextTelem: ParkTelemetry = {
        ...telemetryRef.current,
        currentOccupancy: reconcileTodayOccupancy(
          trailsRef.current,
          nextPasses,
          telemetryRef.current.dailyCapacityMax
        ),
        totalCo2AvoidedKg: Number(
          (telemetryRef.current.totalCo2AvoidedKg + input.co2AvoidedKg).toFixed(1)
        ),
      };

      passesRef.current = nextPasses;
      telemetryRef.current = nextTelem;
      safeLocalStorage.setItem(STORAGE_KEYS.PASSES, nextPasses);
      safeLocalStorage.setItem(STORAGE_KEYS.TELEMETRY, nextTelem);
      setPassesState(nextPasses);
      setTelemetryState(nextTelem);

      setActivePassId(newId);
      unlockPassForSession(newId);
      publishSyncUpdate('passes', { passes: nextPasses, telemetry: nextTelem });
      void syncPassToSupabaseCloudIfActive(newPass, 'upsert');

      return newPass;
    },
    [publishSyncUpdate, reconcileTodayOccupancy, setActivePassId, unlockPassForSession]
  );

  const cancelPass = useCallback(
    (passId: string) => {
      const targetPass = passesRef.current.find((p) => p.id === passId);
      if (!targetPass) return;

      if (!canActorCancelPass(targetPass, userRef.current, sessionUnlockedRef.current)) {
        console.warn('[EcoPark RBAC] cancelPass refused: caller does not own or manage this pass.');
        return;
      }

      const releasedCo2Kg = targetPass.co2AvoidedKg;
      const cancelledPass: EcoPass = { ...targetPass, status: 'cancelled' };
      const nextPasses = passesRef.current.map((p) => (p.id === passId ? cancelledPass : p));

      const updatedTelem: ParkTelemetry = {
        ...telemetryRef.current,
        currentOccupancy: reconcileTodayOccupancy(
          trailsRef.current,
          nextPasses,
          telemetryRef.current.dailyCapacityMax
        ),
        totalCo2AvoidedKg: Math.max(
          0,
          Number((telemetryRef.current.totalCo2AvoidedKg - releasedCo2Kg).toFixed(1))
        ),
      };

      passesRef.current = nextPasses;
      telemetryRef.current = updatedTelem;
      safeLocalStorage.setItem(STORAGE_KEYS.PASSES, nextPasses);
      safeLocalStorage.setItem(STORAGE_KEYS.TELEMETRY, updatedTelem);
      setPassesState(nextPasses);
      setTelemetryState(updatedTelem);
      publishSyncUpdate('passes', { passes: nextPasses, telemetry: updatedTelem });
      void syncPassToSupabaseCloudIfActive(
        cancelledPass,
        'cancel',
        userRef.current?.matricule
      );
    },
    [publishSyncUpdate, reconcileTodayOccupancy]
  );

  const checkInPass = useCallback(
    (passId: string) => {
      if (!canMutatePassCheckIn(userRef.current?.role)) {
        console.warn('[EcoPark RBAC] checkInPass refused: check-in staff role required.');
        return;
      }

      const target = passesRef.current.find((p) => p.id === passId);
      if (!target || target.status === 'cancelled' || target.status === 'checked_in') return;

      const nowIso = new Date().toISOString();
      const checkedInPass: EcoPass = {
        ...target,
        status: 'checked_in',
        checkInTimestamp: nowIso,
      };
      const next = passesRef.current.map((p) => (p.id === passId ? checkedInPass : p));

      passesRef.current = next;
      safeLocalStorage.setItem(STORAGE_KEYS.PASSES, next);
      setPassesState(next);
      publishSyncUpdate('passes', { passes: next });
      void syncPassToSupabaseCloudIfActive(
        checkedInPass,
        'check_in',
        userRef.current?.matricule
      );
    },
    [publishSyncUpdate]
  );

  const claimPassByReference = useCallback(
    (
      referenceCode: string,
      contactEmailOrPhone: string,
      userId: string,
      userEmail: string
    ): { ok: boolean; error?: string; pass?: EcoPass } => {
      const lookup = verifyAnonymousPassLookup(
        passesRef.current,
        referenceCode,
        contactEmailOrPhone
      );
      if (!lookup.ok || !lookup.pass) {
        return {
          ok: false,
          error:
            lookup.error ||
            'Aucun billet trouvé avec cette référence ou coordonnées non concordantes.',
        };
      }

      const claimedPass: EcoPass = {
        ...lookup.pass,
        ownerUserId: userId,
        ownerEmail: userEmail.trim().toLowerCase(),
      };

      const next = passesRef.current.map((p) => (p.id === claimedPass.id ? claimedPass : p));
      passesRef.current = next;
      safeLocalStorage.setItem(STORAGE_KEYS.PASSES, next);
      setPassesState(next);
      setActivePassId(claimedPass.id);
      publishSyncUpdate('passes', { passes: next });
      return { ok: true, pass: claimedPass };
    },
    [publishSyncUpdate, setActivePassId]
  );

  const lookupPassAnonymously = useCallback(
    (
      referenceCode: string,
      contactEmailOrPhone: string
    ): { ok: boolean; error?: string; pass?: EcoPass } => {
      const res = verifyAnonymousPassLookup(
        passesRef.current,
        referenceCode,
        contactEmailOrPhone
      );
      if (res.ok && res.pass) {
        unlockPassForSession(res.pass.id);
        setActivePassId(res.pass.id);
      }
      return res;
    },
    [setActivePassId, unlockPassForSession]
  );

  const anonymizeUserPasses = useCallback(
    (userId: string, userEmail: string): number => {
      const { updatedPasses, anonymizedCount } = anonymizeClientPassesList(
        passesRef.current,
        userId,
        userEmail
      );
      if (anonymizedCount > 0) {
        passesRef.current = updatedPasses;
        safeLocalStorage.setItem(STORAGE_KEYS.PASSES, updatedPasses);
        setPassesState(updatedPasses);
        publishSyncUpdate('passes', { passes: updatedPasses });
      }
      sessionUnlockedRef.current = [];
      setSessionUnlockedPassIdsState([]);
      safeSessionStorage.removeItem(STORAGE_KEYS.SESSION_UNLOCKED_PASSES);
      return anonymizedCount;
    },
    [publishSyncUpdate]
  );

  const submitCitizenReport = useCallback(
    (input: ReportInput): CitizenReport => {
      const reportIndex = Math.floor(100 + Math.random() * 900);
      const newId = `REP-2026-${reportIndex}`;
      const nowIso = new Date().toISOString();

      const newReport: CitizenReport = {
        ...input,
        id: newId,
        timestamp: nowIso,
        status: 'en_attente',
        upvotes: 0,
      };

      const next = [newReport, ...reportsRef.current];
      reportsRef.current = next;
      safeLocalStorage.setItem(STORAGE_KEYS.REPORTS, next);
      setReportsState(next);
      publishSyncUpdate('reports', { reports: next });

      return newReport;
    },
    [publishSyncUpdate]
  );

  const updateReportStatus = useCallback(
    (reportId: string, status: ReportStatus, rangerNote?: string) => {
      if (!canMutateBackofficeOps(userRef.current?.role)) {
        console.warn('[EcoPark RBAC] updateReportStatus refused: operational staff role required.');
        return;
      }

      const next = reportsRef.current.map((rep) => {
        if (rep.id === reportId) {
          return {
            ...rep,
            status,
            rangerNote: rangerNote !== undefined ? rangerNote : rep.rangerNote,
            resolvedAt: status === 'resolu' ? new Date().toISOString() : rep.resolvedAt,
          };
        }
        return rep;
      });

      reportsRef.current = next;
      safeLocalStorage.setItem(STORAGE_KEYS.REPORTS, next);
      setReportsState(next);
      publishSyncUpdate('reports', { reports: next });
    },
    [publishSyncUpdate]
  );

  const upvoteReport = useCallback(
    (reportId: string) => {
      const next = reportsRef.current.map((rep) =>
        rep.id === reportId ? { ...rep, upvotes: rep.upvotes + 1 } : rep
      );
      reportsRef.current = next;
      safeLocalStorage.setItem(STORAGE_KEYS.REPORTS, next);
      setReportsState(next);
      publishSyncUpdate('reports', { reports: next });
    },
    [publishSyncUpdate]
  );

  const resetToSeedData = useCallback(() => {
    if (!canMutateBackofficeOps(userRef.current?.role)) {
      console.warn('[EcoPark RBAC] resetToSeedData refused: operational staff role required.');
      return;
    }

    trailsRef.current = INITIAL_TRAILS;
    telemetryRef.current = INITIAL_TELEMETRY;
    passesRef.current = INITIAL_PASSES;
    reportsRef.current = INITIAL_REPORTS;

    safeLocalStorage.setItem(STORAGE_KEYS.TRAILS, INITIAL_TRAILS);
    safeLocalStorage.setItem(STORAGE_KEYS.TELEMETRY, INITIAL_TELEMETRY);
    safeLocalStorage.setItem(STORAGE_KEYS.PASSES, INITIAL_PASSES);
    safeLocalStorage.setItem(STORAGE_KEYS.REPORTS, INITIAL_REPORTS);

    setTrailsState(INITIAL_TRAILS);
    setTelemetryState(INITIAL_TELEMETRY);
    setPassesState(INITIAL_PASSES);
    setReportsState(INITIAL_REPORTS);
    setSelectedTrailIdState(null);
    setSelectedSpeciesIdState(null);
    setActivePassIdState('ECP-2026-8942');
    setColorDrawerOpenState(false);

    sessionUnlockedRef.current = [];
    setSessionUnlockedPassIdsState([]);
    safeSessionStorage.removeItem(STORAGE_KEYS.SESSION_UNLOCKED_PASSES);

    publishSyncUpdate('reset', {
      trails: INITIAL_TRAILS,
      telemetry: INITIAL_TELEMETRY,
      passes: INITIAL_PASSES,
      reports: INITIAL_REPORTS,
    });
  }, [publishSyncUpdate]);

  // --------------------------------------------------------------------------
  // Real-Time Bidirectional Sync: BroadcastChannel + StorageEvent Fallback
  // (Strictly scoped to shared domain state; never hijacks tab navigation)
  // --------------------------------------------------------------------------
  useEffect(() => {
    const applyIncomingEnvelope = (env: SyncEnvelope) => {
      if (env.trails) {
        trailsRef.current = env.trails;
        setTrailsState(env.trails);
      }
      if (env.telemetry) {
        telemetryRef.current = env.telemetry;
        setTelemetryState(env.telemetry);
      }
      if (env.passes) {
        passesRef.current = env.passes;
        setPassesState(env.passes);
      }
      if (env.reports) {
        reportsRef.current = env.reports;
        setReportsState(env.reports);
      }
      setSyncMeta((prev) => ({
        ...prev,
        lastSyncedAt: env.timestamp,
        lastDomain: env.domain,
        lastActorRole: env.actorRole,
        receivedCount: prev.receivedCount + 1,
      }));
    };

    const bus = createEcoSyncBus(tabIdRef.current, applyIncomingEnvelope);
    syncBusRef.current = bus;

    const handleStorageEvent = (event: StorageEvent) => {
      if (!event.key || event.newValue === null) return;
      // Ignore all tab-local navigation & UI keys (ACTIVE_VIEW, SELECTED_TRAIL, etc.)
      if (!isCrossTabSyncedKey(event.key)) return;

      try {
        const nowIso = new Date().toISOString();
        if (event.key === STORAGE_KEYS.TRAILS) {
          const parsed = JSON.parse(event.newValue) as Trail[];
          trailsRef.current = parsed;
          setTrailsState(parsed);
          setSyncMeta((prev) => ({ ...prev, lastSyncedAt: nowIso, lastDomain: 'trails' }));
        } else if (event.key === STORAGE_KEYS.TELEMETRY) {
          const parsed = JSON.parse(event.newValue) as ParkTelemetry;
          telemetryRef.current = parsed;
          setTelemetryState(parsed);
          setSyncMeta((prev) => ({ ...prev, lastSyncedAt: nowIso, lastDomain: 'telemetry' }));
        } else if (event.key === STORAGE_KEYS.PASSES) {
          const parsed = JSON.parse(event.newValue) as EcoPass[];
          passesRef.current = parsed;
          setPassesState(parsed);
          setSyncMeta((prev) => ({ ...prev, lastSyncedAt: nowIso, lastDomain: 'passes' }));
        } else if (event.key === STORAGE_KEYS.REPORTS) {
          const parsed = JSON.parse(event.newValue) as CitizenReport[];
          reportsRef.current = parsed;
          setReportsState(parsed);
          setSyncMeta((prev) => ({ ...prev, lastSyncedAt: nowIso, lastDomain: 'reports' }));
        }
      } catch (err) {
        console.warn('[EcoParkContext] Error syncing cross-tab storage event:', err);
      }
    };

    if (typeof window !== 'undefined') {
      window.addEventListener('storage', handleStorageEvent);
    }

    return () => {
      bus.close();
      syncBusRef.current = null;
      if (typeof window !== 'undefined') {
        window.removeEventListener('storage', handleStorageEvent);
      }
    };
  }, []);

  // Compute active pass
  const activePass = useMemo(() => {
    if (!activePassId) return passes[0] || null;
    return passes.find((p) => p.id === activePassId) || passes[0] || null;
  }, [passes, activePassId]);

  const value: EcoParkContextType = {
    // Navigation & View
    activeView,
    setActiveView,

    // Theming & Daltonism
    themeMode,
    effectiveTheme,
    setThemeMode,
    daltonismMode,
    setDaltonismMode,
    colorDrawerOpen,
    setColorDrawerOpen,
    highContrastOutdoor,
    setHighContrastOutdoor,

    // Telemetry & Capacity
    telemetry,
    setDailyCapacity,

    // Trails
    trails,
    updateTrailStatus,
    selectedTrailId,
    setSelectedTrailId,

    // Points of interest (reference constant)
    pois: INITIAL_POIS,

    // Species
    species: INITIAL_SPECIES,
    selectedSpeciesId,
    setSelectedSpeciesId,

    // Bookings & Passes
    passes,
    activePass,
    activePassId,
    setActivePassId,
    sessionUnlockedPassIds,
    bookPass,
    cancelPass,
    checkInPass,
    claimPassByReference,
    lookupPassAnonymously,
    anonymizeUserPasses,

    // Citizen Sentinel
    reports,
    submitCitizenReport,
    updateReportStatus,
    upvoteReport,

    // State Management, Reset & Sync Telemetry
    resetToSeedData,
    syncMeta,
  };

  return <EcoParkContext.Provider value={value}>{children}</EcoParkContext.Provider>;
};

export function useEcoPark(): EcoParkContextType {
  const context = useContext(EcoParkContext);
  if (!context) {
    throw new Error('useEcoPark must be used within an EcoParkProvider');
  }
  return context;
}
