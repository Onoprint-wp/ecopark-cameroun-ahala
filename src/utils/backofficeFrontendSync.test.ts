// ============================================================================
// BACKOFFICE <-> FRONTEND BIDIRECTIONAL SYNC & RBAC STORE TESTS
// (src/utils/backofficeFrontendSync.test.ts)
// ============================================================================

import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {
  INITIAL_PASSES,
  INITIAL_REPORTS,
  INITIAL_TELEMETRY,
  INITIAL_TRAILS,
} from '../data/initialParkData.ts';
import type {
  AuthenticatedUser,
  EcoParkRole,
  EcoPass,
} from '../types/ecosystem.ts';
import {
  SHARED_DOMAIN_KEYS,
  TAB_LOCAL_UI_KEYS,
  canActorCancelPass,
  canMutateBackofficeOps,
  canMutatePassCheckIn,
  createEcoSyncBus,
  isCrossTabSyncedKey,
  mapEcoPassToSupabaseBookingRow,
  validateLiveBookingConstraints,
  type SyncEnvelope,
} from './ecoSyncBus.ts';

function makeActor(role: EcoParkRole, overrides: Partial<AuthenticatedUser> = {}): AuthenticatedUser {
  return {
    id: overrides.id || `usr-${role}`,
    email: overrides.email || `${role}@ecopark-yaounde.com`,
    fullName: overrides.fullName || `Profil ${role}`,
    phone: overrides.phone || '+237 690 00 00 00',
    role,
    matricule: overrides.matricule || 'MAT-TEST-01',
    assignedPole: overrides.assignedPole || 'CONTROLE_QR',
    provider: 'webcrypto_pbkdf2',
    createdAt: new Date().toISOString(),
  };
}

function waitForEnvelope(
  predicate: (env: SyncEnvelope) => boolean,
  inbox: SyncEnvelope[],
  timeoutMs = 1500
): Promise<SyncEnvelope> {
  return new Promise((resolve, reject) => {
    const start = Date.now();
    const check = () => {
      const found = inbox.find(predicate);
      if (found) {
        resolve(found);
        return;
      }
      if (Date.now() - start > timeoutMs) {
        reject(new Error(`Timeout waiting for BroadcastChannel envelope (${inbox.length} received)`));
        return;
      }
      setTimeout(check, 10);
    };
    check();
  });
}

test('Anomalie 1 : Isolation stricte de la navigation inter-onglets (sessionStorage vs localStorage)', () => {
  // All 4 shared domain keys must sync across Backoffice and Frontend tabs
  for (const domainKey of SHARED_DOMAIN_KEYS) {
    assert.equal(
      isCrossTabSyncedKey(domainKey),
      true,
      `Domain key ${domainKey} must be cross-tab synced`
    );
  }

  // All 6 UI & navigation keys must NEVER sync across tabs (prevents /exploitation hijacking)
  for (const uiKey of TAB_LOCAL_UI_KEYS) {
    assert.equal(
      isCrossTabSyncedKey(uiKey),
      false,
      `UI key ${uiKey} must remain strictly tab-local`
    );
  }
  assert.equal(isCrossTabSyncedKey('unknown_random_key'), false);

  // Structural verification of EcoParkContext.tsx: UI keys use safeSessionStorage, never safeLocalStorage
  const ctxSource = fs.readFileSync(
    path.resolve(process.cwd(), 'src/context/EcoParkContext.tsx'),
    'utf8'
  );
  const localUiRefs = [
    'STORAGE_KEYS.ACTIVE_VIEW',
    'STORAGE_KEYS.SELECTED_TRAIL',
    'STORAGE_KEYS.SELECTED_SPECIES',
    'STORAGE_KEYS.ACTIVE_PASS_ID',
    'STORAGE_KEYS.DRAWER_OPEN',
    'STORAGE_KEYS.SESSION_UNLOCKED_PASSES',
  ];
  for (const token of localUiRefs) {
    assert.equal(
      ctxSource.includes(`safeLocalStorage.setItem(${token}`),
      false,
      `${token} must never be written to safeLocalStorage`
    );
    assert.equal(
      ctxSource.includes(`safeLocalStorage.getItem(${token}`),
      false,
      `${token} must never be read from safeLocalStorage`
    );
  }
});

test('Anomalie 2 : Bus BroadcastChannel temps reel et verification des 5 contrats bidirectionnels', async () => {
  const testChannel = `eco_park_test_sync_${Date.now()}_${Math.random().toString(36).slice(2, 7)}`;
  const backofficeInbox: SyncEnvelope[] = [];
  const frontendInbox: SyncEnvelope[] = [];

  const backofficeBus = createEcoSyncBus(
    'tab-backoffice-exp',
    (env) => backofficeInbox.push(env),
    testChannel
  );
  const frontendBus = createEcoSyncBus(
    'tab-frontend-visiteur',
    (env) => frontendInbox.push(env),
    testChannel
  );

  try {
    // Contrat 1 (Backoffice -> Frontend) : Regulation de la jauge journaliere (1500 -> 2150)
    const updatedTelemetry = { ...INITIAL_TELEMETRY, dailyCapacityMax: 2150 };
    backofficeBus.publish({
      domain: 'telemetry',
      actorRole: 'responsable_exploitation',
      telemetry: updatedTelemetry,
    });

    const c1 = await waitForEnvelope((e) => e.domain === 'telemetry', frontendInbox);
    assert.equal(c1.telemetry?.dailyCapacityMax, 2150);
    assert.equal(c1.actorRole, 'responsable_exploitation');
    // Zero self-echo on sender tab
    assert.equal(backofficeInbox.length, 0);

    // Contrat 2 (Backoffice -> Frontend) : Fermeture biologique d un sentier
    const closedTrails = INITIAL_TRAILS.map((t, idx) =>
      idx === 0 ? { ...t, status: 'ferme' as const, closureReason: 'Nidification Gorille ToTo' } : t
    );
    backofficeBus.publish({
      domain: 'trails',
      actorRole: 'direction',
      trails: closedTrails,
    });

    const c2 = await waitForEnvelope((e) => e.domain === 'trails', frontendInbox);
    assert.equal(c2.trails?.[0].status, 'ferme');
    assert.equal(c2.trails?.[0].closureReason, 'Nidification Gorille ToTo');

    // Contrat 3 (Frontend -> Backoffice) : Emission d un nouveau Pass QR visiteur
    const bookedPass: EcoPass = {
      ...INITIAL_PASSES[0],
      id: 'ECP-2026-99101',
      status: 'confirmed',
      guestCount: 4,
      totalPriceEur: 10000,
    };
    frontendBus.publish({
      domain: 'passes',
      actorRole: 'client_connecte',
      passes: [bookedPass, ...INITIAL_PASSES],
    });

    const c3 = await waitForEnvelope(
      (e) => e.domain === 'passes' && e.actorRole === 'client_connecte',
      backofficeInbox
    );
    assert.equal(c3.passes?.[0].id, 'ECP-2026-99101');
    assert.equal(c3.passes?.[0].status, 'confirmed');

    // Contrat 4 (Backoffice -> Frontend) : Validation Check-In QR au Guichet RN3
    const checkedInPass: EcoPass = {
      ...bookedPass,
      status: 'checked_in',
      checkInTimestamp: '2026-11-14T10:15:00.000Z',
    };
    backofficeBus.publish({
      domain: 'passes',
      actorRole: 'agent_controle',
      passes: [checkedInPass, ...INITIAL_PASSES],
    });

    const c4 = await waitForEnvelope(
      (e) => e.domain === 'passes' && e.actorRole === 'agent_controle',
      frontendInbox
    );
    assert.equal(c4.passes?.[0].status, 'checked_in');
    assert.equal(c4.passes?.[0].checkInTimestamp, '2026-11-14T10:15:00.000Z');

    // Contrat 5 (Frontend <-> Backoffice) : Signalement Sentinelle puis moderation Eco-Garde
    const newReport = {
      ...INITIAL_REPORTS[0],
      id: 'REP-2026-777',
      status: 'en_attente' as const,
      title: 'Branche sur passerelle lac',
    };
    frontendBus.publish({
      domain: 'reports',
      actorRole: 'visiteur_anonyme',
      reports: [newReport, ...INITIAL_REPORTS],
    });

    const c5a = await waitForEnvelope((e) => e.domain === 'reports', backofficeInbox);
    assert.equal(c5a.reports?.[0].id, 'REP-2026-777');
    assert.equal(c5a.reports?.[0].status, 'en_attente');

    const resolvedReport = {
      ...newReport,
      status: 'resolu' as const,
      rangerNote: 'Degage par patrouille RN3',
    };
    backofficeBus.publish({
      domain: 'reports',
      actorRole: 'responsable_exploitation',
      reports: [resolvedReport, ...INITIAL_REPORTS],
    });

    const c5b = await waitForEnvelope(
      (e) => e.domain === 'reports' && e.actorRole === 'responsable_exploitation',
      frontendInbox
    );
    assert.equal(c5b.reports?.[0].status, 'resolu');
    assert.equal(c5b.reports?.[0].rangerNote, 'Degage par patrouille RN3');
  } finally {
    backofficeBus.close();
    frontendBus.close();
  }
});

test('Anomalie 3a : Gardes RBAC du store sur les 8 profils EcoParkRole', () => {
  const opsRoles: EcoParkRole[] = [
    'responsable_exploitation',
    'direction',
    'administrateur_plateforme',
  ];
  const nonOpsRoles: EcoParkRole[] = [
    'visiteur_anonyme',
    'client_connecte',
    'agent_guichet',
    'agent_controle',
    'comptable',
  ];

  for (const r of opsRoles) {
    assert.equal(canMutateBackofficeOps(r), true, `${r} should mutate park ops`);
  }
  for (const r of nonOpsRoles) {
    assert.equal(canMutateBackofficeOps(r), false, `${r} must NOT mutate park ops`);
  }
  assert.equal(canMutateBackofficeOps(null), false);

  // Check-In permissions
  assert.equal(canMutatePassCheckIn('agent_guichet'), true);
  assert.equal(canMutatePassCheckIn('agent_controle'), true);
  assert.equal(canMutatePassCheckIn('responsable_exploitation'), true);
  assert.equal(canMutatePassCheckIn('direction'), true);
  assert.equal(canMutatePassCheckIn('administrateur_plateforme'), true);
  assert.equal(canMutatePassCheckIn('comptable'), false);
  assert.equal(canMutatePassCheckIn('client_connecte'), false);
  assert.equal(canMutatePassCheckIn('visiteur_anonyme'), false);
  assert.equal(canMutatePassCheckIn(null), false);

  // Pass cancellation ownership & staff matrix
  const samplePass: EcoPass = {
    ...INITIAL_PASSES[0],
    id: 'ECP-2026-54321',
    status: 'confirmed',
    ownerUserId: 'usr-owner-1',
    ownerEmail: 'amina@client.cm',
    leadVisitor: {
      fullName: 'Amina Ndongo',
      email: 'amina@client.cm',
      phone: '+237 699 11 22 33',
    },
  };

  // Owner client can cancel; another client cannot
  const ownerClient = makeActor('client_connecte', {
    id: 'usr-owner-1',
    email: 'amina@client.cm',
  });
  const otherClient = makeActor('client_connecte', {
    id: 'usr-other-2',
    email: 'autre@client.cm',
  });
  assert.equal(canActorCancelPass(samplePass, ownerClient, []), true);
  assert.equal(canActorCancelPass(samplePass, otherClient, []), false);

  // Anonymous visitor can cancel ONLY if unlocked in current tab session
  assert.equal(canActorCancelPass(samplePass, null, []), false);
  assert.equal(canActorCancelPass(samplePass, null, ['ECP-2026-54321']), true);

  // Read-only / gate staff cannot cancel passes; ops managers can
  assert.equal(canActorCancelPass(samplePass, makeActor('comptable'), []), false);
  assert.equal(canActorCancelPass(samplePass, makeActor('agent_guichet'), []), false);
  assert.equal(canActorCancelPass(samplePass, makeActor('agent_controle'), []), false);
  assert.equal(canActorCancelPass(samplePass, makeActor('responsable_exploitation'), []), true);
  assert.equal(canActorCancelPass(samplePass, makeActor('direction'), []), true);
  assert.equal(canActorCancelPass(samplePass, makeActor('administrateur_plateforme'), []), true);

  // Already cancelled pass cannot be cancelled again
  assert.equal(
    canActorCancelPass({ ...samplePass, status: 'cancelled' }, makeActor('direction'), []),
    false
  );
});

test('Anomalie 3b : Blocage temps reel des courses critiques dans BookingWizard (sentier ferme ou quota abaisse)', () => {
  const todayIso = '2026-11-14'; // Saturday
  const validSunday = '2026-11-15'; // Sunday
  const closedMonday = '2026-11-16'; // Monday (weekly biological rest)

  // 1. Rejects Monday weekly biological closure
  const monCheck = validateLiveBookingConstraints({
    visitDate: closedMonday,
    todayIso,
    guestCount: 2,
    dailyCapacityMax: 1500,
    currentBookedForDate: 400,
    selectedTrail: null,
  });
  assert.equal(monCheck.ok, false);
  assert.equal(monCheck.code, 'MONDAY_REST_DAY');

  // 2. Rejects mid-funnel when Backoffice closes selected trail
  const closedTrailCheck = validateLiveBookingConstraints({
    visitDate: validSunday,
    todayIso,
    guestCount: 3,
    dailyCapacityMax: 1500,
    currentBookedForDate: 400,
    selectedTrail: {
      id: 'trail-01',
      name: 'Sanctuaire Gorille ToTo',
      status: 'ferme',
      closureReason: 'Maintenance veterinaire',
    },
  });
  assert.equal(closedTrailCheck.ok, false);
  assert.equal(closedTrailCheck.code, 'TRAIL_CLOSED');

  // 3. Succeeds immediately once visitor switches to open zones (selectedTrail = null)
  const openZoneCheck = validateLiveBookingConstraints({
    visitDate: validSunday,
    todayIso,
    guestCount: 3,
    dailyCapacityMax: 1500,
    currentBookedForDate: 400,
    selectedTrail: null,
  });
  assert.equal(openZoneCheck.ok, true);
  assert.equal(openZoneCheck.availablePlaces, 1100);

  // 4. Rejects mid-funnel when Backoffice lowers dailyCapacityMax below currentBooked + guestCount
  const loweredQuotaCheck = validateLiveBookingConstraints({
    visitDate: validSunday,
    todayIso,
    guestCount: 5,
    dailyCapacityMax: 600,
    currentBookedForDate: 598,
    selectedTrail: null,
  });
  assert.equal(loweredQuotaCheck.ok, false);
  assert.equal(loweredQuotaCheck.code, 'QUOTA_EXCEEDED');
  assert.equal(loweredQuotaCheck.availablePlaces, 2);
});

test('Anomalie 4 : Conformite stricte du mappeur EcoPass <-> public.bookings avec le schema SQL reel', () => {
  const sqlMigration = fs.readFileSync(
    path.resolve(process.cwd(), 'supabase/migrations/20261026000001_ecopark_schema_rls.sql'),
    'utf8'
  );

  const pass: EcoPass = {
    ...INITIAL_PASSES[0],
    id: 'ECP-2026-44210',
    visitDate: '2026-11-15',
    guestCount: 3,
    adultCount: 2,
    childCount: 1,
    totalPriceEur: 4500,
    mobilityMode: 'train',
    experienceType: 'pack_mobilite',
    status: 'confirmed',
  };

  const confirmedRow = mapEcoPassToSupabaseBookingRow(pass);
  // Every mapped property must exist verbatim in public.bookings SQL migration (zero hallucinated columns)
  for (const colName of Object.keys(confirmedRow)) {
    assert.equal(
      sqlMigration.includes(colName),
      true,
      `Column "${colName}" must exist in 20261026000001_ecopark_schema_rls.sql`
    );
  }
  assert.equal(sqlMigration.includes('cancelled_at'), true);

  // Check SQL invariants (Loi 3 Int FCFA + chk_at_least_one_adult_or_child)
  assert.equal(Number.isInteger(confirmedRow.total_fcfa), true);
  assert.equal(confirmedRow.total_fcfa, 4500);
  assert.equal(confirmedRow.adults_count + confirmedRow.children_count >= 1, true);
  assert.equal(confirmedRow.payment_method, 'OM');
  assert.equal(confirmedRow.payment_state, 'CONFIRMED');
  assert.equal(confirmedRow.qr_status, 'VALID');
  assert.equal(confirmedRow.scanned_by, null);

  // Checked-in transition
  const checkedRow = mapEcoPassToSupabaseBookingRow(
    { ...pass, status: 'checked_in', checkInTimestamp: '2026-11-15T11:00:00.000Z' },
    'MAT-CTL-02'
  );
  assert.equal(checkedRow.qr_status, 'USED');
  assert.equal(checkedRow.scanned_by, 'MAT-CTL-02');
  assert.equal(checkedRow.scanned_at, '2026-11-15T11:00:00.000Z');

  // Cancelled transition
  const cancelledRow = mapEcoPassToSupabaseBookingRow({ ...pass, status: 'cancelled' });
  assert.equal(cancelledRow.payment_state, 'CANCELLED');
  assert.equal(cancelledRow.qr_status, 'CANCELLED');
});
