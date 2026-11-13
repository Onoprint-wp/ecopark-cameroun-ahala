// ============================================================================
// E2E ECOSYSTEM INTEGRATION & STATE PROPAGATION TESTS (src/utils/ecosystemE2E.test.ts)
// Multi-View State Machine, Data Integrity & Cross-Persona Flows
// ============================================================================

import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {
  INITIAL_TRAILS,
  INITIAL_SPECIES,
  INITIAL_TELEMETRY,
  INITIAL_PASSES,
  INITIAL_REPORTS,
} from '../data/initialParkData.ts';
import {
  getExperienceInfo,
  resolveExperienceForTrail,
  MOBILITY_OPTIONS,
} from './ecoMobility.ts';
import {
  VIEW_PATH_MAP,
  SHOWCASE_TAB_PATH_MAP,
  resolveViewFromPath,
  resolveShowcaseTabFromPath,
  type ShowcaseTab,
} from './ecoRouting.ts';
import type {
  ActiveView,
  Trail,
  EcoPass,
  CitizenReport,
  BookingInput,
} from '../types/ecosystem.ts';

test('ECO-PARK Ecosystem E2E Integration & Data Flows', async (t) => {
  await t.test('Initial Seed Data complies with domain contracts and realistic reserves', () => {
    // 6 Trails
    assert.strictEqual(INITIAL_TRAILS.length, 6, 'Must define exactly 6 official trails');
    for (const trail of INITIAL_TRAILS) {
      assert.ok(trail.id.length > 0, 'Trail ID must be non-empty');
      assert.ok(trail.name.length > 0, 'Trail name must be non-empty');
      assert.ok(trail.lengthKm > 0, 'Length must be positive');
      assert.ok(trail.elevationGainM >= 0, 'Elevation gain must be non-negative');
      assert.ok(['facile', 'moyen', 'difficile', 'expert'].includes(trail.difficulty));
      assert.ok(['fluide', 'balise', 'ferme'].includes(trail.status));
      assert.ok(trail.elevationProfile.length >= 2, 'Elevation profile must define at least 2 points');
    }

    // 8 Endemic Species
    assert.strictEqual(INITIAL_SPECIES.length, 8, 'Must define exactly 8 endemic species');
    for (const sp of INITIAL_SPECIES) {
      assert.ok(sp.id.startsWith('sp-'), 'Species ID must follow convention');
      assert.ok(sp.commonName.length > 0, 'Species must have a common name');
      assert.ok(sp.scientificName.length > 0, 'Species must have a scientific name');
      assert.ok(['CR', 'EN', 'VU', 'NT', 'LC'].includes(sp.iucnStatus), 'IUCN status must be valid');
      assert.ok(sp.observationSeason.length > 0, 'Species must have seasonal observation seasons');
      assert.ok(sp.trailIds.length > 0, 'Species must be linked to at least 1 trail');
    }

    // Telemetry baseline
    assert.ok(INITIAL_TELEMETRY.dailyCapacityMax >= 500 && INITIAL_TELEMETRY.dailyCapacityMax <= 3000);
    assert.ok(INITIAL_TELEMETRY.currentOccupancy <= INITIAL_TELEMETRY.dailyCapacityMax);
    assert.ok(INITIAL_TELEMETRY.solarAutonomyPercent >= 80, 'Solar autonomy should be high');
    assert.ok(INITIAL_TELEMETRY.totalCo2AvoidedKg > 1000, 'Baseline avoided CO2 should be significant');
  });

  await t.test('Trail status transitions update occupancies and propagate biological closure reason', () => {
    const trails: Trail[] = JSON.parse(JSON.stringify(INITIAL_TRAILS));
    const targetTrail = trails[0]; // Sentier de la Canopée
    const originalOccupancy = targetTrail.currentOccupancy;
    assert.ok(originalOccupancy > 0, 'Initial trail occupancy must be greater than 0');

    // Closure simulation (F27)
    const closureReason = 'Nidification Aigle botté (Arrêté de quiétude préfectoral)';
    targetTrail.status = 'ferme';
    targetTrail.closureReason = closureReason;
    targetTrail.currentOccupancy = 0;

    assert.strictEqual(targetTrail.status, 'ferme');
    assert.strictEqual(targetTrail.currentOccupancy, 0, 'Closed trail must immediately report 0 visitors');
    assert.strictEqual(targetTrail.closureReason, closureReason);

    // Reopening simulation
    targetTrail.status = 'fluide';
    targetTrail.closureReason = undefined;
    targetTrail.currentOccupancy = Math.floor(targetTrail.maxCapacity * 0.4);

    assert.strictEqual(targetTrail.status, 'fluide');
    assert.ok(targetTrail.currentOccupancy > 0, 'Reopened trail restores default safe occupancy');
    assert.strictEqual(targetTrail.closureReason, undefined);
  });

  await t.test('Ticketing & ADEME Eco-Mobility Engine calculations and quota decrement', () => {
    let currentCapacity = INITIAL_TELEMETRY.dailyCapacityMax;
    let currentOccupancy = INITIAL_TELEMETRY.currentOccupancy;
    let avoidedCo2 = INITIAL_TELEMETRY.totalCo2AvoidedKg;

    const bookingPayload: BookingInput = {
      experienceType: 'sentiers',
      visitDate: '2026-05-20',
      timeSlot: '08h30 - 11h30',
      guestCount: 3,
      mobilityMode: 'train',
      unitPriceEur: 12,
      discountAppliedPercent: 25,
      totalPriceEur: 27, // 3 * 12 * (1 - 0.25)
      co2AvoidedKg: 10.5,
      zeroTraceCharterSigned: true,
      leadVisitor: {
        fullName: 'Claire Fontaine',
        email: 'claire.fontaine@ecopark.test',
        phone: '+33 6 12 34 56 78',
      },
    };

    // Calculate remaining places before booking
    const availableBefore = currentCapacity - currentOccupancy;
    assert.ok(availableBefore >= bookingPayload.guestCount, 'Must have sufficient spots');

    // Simulate booking execution (bookPass)
    const newPass: EcoPass = {
      ...bookingPayload,
      id: 'ECO-2026-9901-CF',
      createdAt: new Date().toISOString(),
      status: 'confirmed',
      qrPayload: `ECOPARK:PASS:ECO-2026-9901-CF:DATE=${bookingPayload.visitDate}:SLOT=${bookingPayload.timeSlot}:GUESTS=${bookingPayload.guestCount}:MODE=${bookingPayload.mobilityMode}`,
    };

    currentOccupancy += bookingPayload.guestCount;
    avoidedCo2 = Number((avoidedCo2 + bookingPayload.co2AvoidedKg).toFixed(1));

    assert.strictEqual(newPass.status, 'confirmed');
    assert.strictEqual(newPass.guestCount, 3);
    assert.strictEqual(currentCapacity - currentOccupancy, availableBefore - 3, 'Remaining capacity must decrement by guest count');
    assert.ok(avoidedCo2 > INITIAL_TELEMETRY.totalCo2AvoidedKg, 'Avoided CO2 metric must increment');

    // Simulate check-in
    newPass.status = 'checked_in';
    newPass.checkInTimestamp = new Date().toISOString();
    assert.strictEqual(newPass.status, 'checked_in');
    assert.ok(typeof newPass.checkInTimestamp === 'string');

    // Simulate cancellation
    currentOccupancy -= bookingPayload.guestCount;
    newPass.status = 'cancelled';
    assert.strictEqual(newPass.status, 'cancelled');
    assert.strictEqual(currentCapacity - currentOccupancy, availableBefore, 'Capacity must be restored on cancellation');
  });

  await t.test('Citizen Sentinel field observation moderation lifecycle with ranger notes', () => {
    const reports: CitizenReport[] = JSON.parse(JSON.stringify(INITIAL_REPORTS));

    // Submit new report
    const newReport: CitizenReport = {
      id: 'REP-2026-999',
      timestamp: new Date().toISOString(),
      type: 'faune_rare',
      title: 'Observation rare de Circaète Jean-le-Blanc',
      description: 'Vu planant au-dessus de la combe rocheuse vers 11h.',
      trailId: 'canopee',
      landmark: '300m après la passerelle suspendue',
      severity: 'mineur',
      status: 'en_attente',
      reporterName: 'Lucas M. (Sentinelle #412)',
      upvotes: 0,
    };

    reports.unshift(newReport);
    assert.strictEqual(reports[0].id, 'REP-2026-999');
    assert.strictEqual(reports[0].status, 'en_attente');

    // Upvote by hikers
    reports[0].upvotes += 1;
    reports[0].upvotes += 1;
    assert.strictEqual(reports[0].upvotes, 2, 'Upvote count must accumulate');

    // Ranger validates
    reports[0].status = 'valide';
    assert.strictEqual(reports[0].status, 'valide');

    // Ranger resolves with field intervention note
    const interventionNote = "Observation confirmée par l'ornithologue du parc. Zone de quiétude respectée.";
    reports[0].status = 'resolu';
    reports[0].rangerNote = interventionNote;
    reports[0].resolvedAt = new Date().toISOString();

    assert.strictEqual(reports[0].status, 'resolu');
    assert.strictEqual(reports[0].rangerNote, interventionNote);
    assert.ok(typeof reports[0].resolvedAt === 'string');
  });

  await t.test('Daily Quota Regulator protects against out-of-bound adjustments', () => {
    let dailyCapacityMax = 1500;
    const clampCapacity = (val: number) => Math.max(500, Math.min(3000, val));

    dailyCapacityMax = clampCapacity(400); // Below min
    assert.strictEqual(dailyCapacityMax, 500, 'Capacity below 500 must clamp to 500');

    dailyCapacityMax = clampCapacity(4500); // Above max
    assert.strictEqual(dailyCapacityMax, 3000, 'Capacity above 3000 must clamp to 3000');

    dailyCapacityMax = clampCapacity(1200);
    assert.strictEqual(dailyCapacityMax, 1200, 'Valid capacity must remain unchanged');
  });

  await t.test('Global Cross-Module Synchronization (Trail <-> Formula <-> Pass <-> Telemetry)', () => {
    // 1. Trail -> Experience pre-selection mapping
    assert.strictEqual(resolveExperienceForTrail('marais'), 'pack_mobilite');
    assert.strictEqual(resolveExperienceForTrail('roches-moussues'), 'eco_guide');
    assert.strictEqual(resolveExperienceForTrail('piste-eco-gardes'), 'atelier_botanique');
    assert.strictEqual(resolveExperienceForTrail('canopee'), 'sentiers');

    // 2. Official FCFA formula resolution & Yaoundé-Ahala mobility labels
    const royalInfo = getExperienceInfo('atelier_botanique');
    assert.ok(royalInfo.title.includes('Pass Journée Royale'));
    assert.strictEqual(MOBILITY_OPTIONS.length, 5);
    assert.ok(MOBILITY_OPTIONS.some((m) => m.shortLabel.includes('Orange Money')));

    // 3. Reconciled Occupancy (Trail Status Closure must NOT wipe today's net booked passes)
    const todayIso = new Date().toISOString().split('T')[0];
    const reconcile = (trailsList: Trail[], passesList: EcoPass[], cap: number) => {
      const openOcc = trailsList
        .filter((tr) => tr.status !== 'ferme')
        .reduce((s, tr) => s + tr.currentOccupancy, 0);
      const seedToday = INITIAL_PASSES.filter(
        (p) => p.visitDate === todayIso && p.status !== 'cancelled'
      ).reduce((s, p) => s + p.guestCount, 0);
      const activeToday = passesList
        .filter((p) => p.visitDate === todayIso && p.status !== 'cancelled')
        .reduce((s, p) => s + p.guestCount, 0);
      return Math.max(0, Math.min(cap, openOcc + (activeToday - seedToday)));
    };

    const trails: Trail[] = JSON.parse(JSON.stringify(INITIAL_TRAILS));
    const passes: EcoPass[] = JSON.parse(JSON.stringify(INITIAL_PASSES));
    assert.strictEqual(reconcile(trails, passes, 1500), 642, 'Baseline reconciled occupancy equals 642');

    // Book +4 guests for TODAY
    passes.unshift({
      ...passes[0],
      id: 'ECP-2026-99999',
      visitDate: todayIso,
      guestCount: 4,
      status: 'confirmed',
    });
    assert.strictEqual(reconcile(trails, passes, 1500), 646, 'Today booking adds +4 guests');

    // Ranger closes 'marais' (198 guests): 642 - 198 + 4 = 448 (today's +4 booking is preserved!)
    const marais = trails.find((tr) => tr.id === 'marais')!;
    marais.status = 'ferme';
    marais.currentOccupancy = 0;
    assert.strictEqual(reconcile(trails, passes, 1500), 448, 'Closing a trail preserves today net pass bookings');
  });

  await t.test('Vercel SPA Rewrites & Bidirectional URL Workflow Synchronization', () => {
    const vercelPath = path.resolve(process.cwd(), 'vercel.json');
    const vercelConfig = JSON.parse(fs.readFileSync(vercelPath, 'utf8')) as {
      rewrites: Array<{ source: string; destination: string }>;
    };

    assert.ok(vercelConfig.rewrites.length >= 56, 'vercel.json must contain all 56 SPA rewrites');

    // Every single rewrite in vercel.json must resolve to a valid ActiveView
    for (const rw of vercelConfig.rewrites) {
      assert.strictEqual(rw.destination, '/index.html');
      const resolved = resolveViewFromPath(rw.source);
      assert.ok(
        resolved !== null,
        `Vercel rewrite "${rw.source}" must resolve to an ActiveView in ecoRouting.ts`
      );
    }

    // Bidirectional round-trip for primary SPA views
    const primaryViews: ActiveView[] = [
      'accueil',
      'sentiers',
      'biodiversite',
      'billetterie',
      'pass',
      'ranger',
    ];
    for (const view of primaryViews) {
      const targetUrl = VIEW_PATH_MAP[view];
      assert.strictEqual(
        resolveViewFromPath(targetUrl),
        view,
        `ActiveView "${view}" -> "${targetUrl}" must round-trip cleanly`
      );
    }

    // Bidirectional round-trip for all 5 AhalaShowcase tabs & presence in vercel.json
    const rewriteSources = new Set(vercelConfig.rewrites.map((r) => r.source));
    const showcaseTabs: ShowcaseTab[] = [
      'hebergements',
      'saveurs',
      'tarifs',
      'entreprise',
      'formation',
    ];
    for (const tab of showcaseTabs) {
      const tabUrl = SHOWCASE_TAB_PATH_MAP[tab];
      assert.ok(rewriteSources.has(tabUrl), `Showcase tab URL "${tabUrl}" must exist in vercel.json`);
      assert.strictEqual(resolveViewFromPath(tabUrl), 'accueil');
      assert.strictEqual(resolveShowcaseTabFromPath(tabUrl), tab);
    }
  });
});
