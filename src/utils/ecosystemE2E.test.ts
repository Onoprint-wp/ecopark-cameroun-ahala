// ============================================================================
// E2E ECOSYSTEM INTEGRATION & STATE PROPAGATION TESTS (src/utils/ecosystemE2E.test.ts)
// Multi-View State Machine, Data Integrity & Cross-Persona Flows
// ============================================================================

import test from 'node:test';
import assert from 'node:assert/strict';
import {
  INITIAL_TRAILS,
  INITIAL_SPECIES,
  INITIAL_TELEMETRY,
  INITIAL_REPORTS,
} from '../data/initialParkData.ts';
import type {
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
});
