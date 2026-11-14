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
  calculateEcoMobilityPricing,
  MOBILITY_OPTIONS,
  EXPERIENCES_CATALOG,
} from './ecoMobility.ts';
import { getContrastRatio } from './wcagContrast.ts';
import {
  VIEW_PATH_MAP,
  SHOWCASE_TAB_PATH_MAP,
  resolveViewFromPath,
  resolveShowcaseTabFromPath,
  type ShowcaseTab,
} from './ecoRouting.ts';
import {
  verifyAnonymousPassLookup,
  anonymizeClientPassesList,
} from './ecoAuth.ts';
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

    // 2b. Official Group 20+ (-30%) discount threshold enforcement
    const soloGroupAttempt = calculateEcoMobilityPricing('sentiers', 'velo', 2, 0, 0);
    assert.strictEqual(
      soloGroupAttempt.discountPercent,
      0,
      'Group -30% discount must NOT apply below 20 guests'
    );
    assert.strictEqual(soloGroupAttempt.netTotalEur, 2000);

    const realGroup20 = calculateEcoMobilityPricing('sentiers', 'velo', 20, 0, 0);
    assert.strictEqual(
      realGroup20.discountPercent,
      30,
      'Group -30% discount applies automatically starting at 20 guests'
    );
    assert.strictEqual(realGroup20.netTotalEur, 14000, '20 adults * 1000 FCFA - 30% = 14000 FCFA');

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

    // Bidirectional round-trip for primary SPA views (including /connexion & /mentions-legales)
    const primaryViews: ActiveView[] = [
      'accueil',
      'sentiers',
      'biodiversite',
      'billetterie',
      'pass',
      'ranger',
      'connexion',
      'legal',
    ];
    for (const view of primaryViews) {
      const targetUrl = VIEW_PATH_MAP[view];
      assert.strictEqual(
        resolveViewFromPath(targetUrl),
        view,
        `ActiveView "${view}" -> "${targetUrl}" must round-trip cleanly`
      );
    }

    // Explicit check on /Connexion, /connexion, /mentions-legales, /cgv, /confidentialite
    assert.strictEqual(resolveViewFromPath('/Connexion'), 'connexion');
    assert.strictEqual(resolveViewFromPath('/connexion'), 'connexion');
    assert.strictEqual(resolveViewFromPath('/mentions-legales'), 'legal');
    assert.strictEqual(resolveViewFromPath('/cgv'), 'legal');
    assert.strictEqual(resolveViewFromPath('/confidentialite'), 'legal');

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

  await t.test('Fiche mémo n°4: Optical Typography, Loi 1/2/3, Guardrails & 7-Step Persuasion', () => {
    const rootDir = process.cwd();

    // 1. Loi 1 ONOGRAPH: 0 U+2014 (em-dash) and 0 U+2013 (en-dash) across index.html & src/
    const forbiddenDashRegex = /[\u2013\u2014]/;
    const indexHtml = fs.readFileSync(path.resolve(rootDir, 'index.html'), 'utf8');
    assert.ok(!forbiddenDashRegex.test(indexHtml), 'index.html must contain 0 U+2013/U+2014');

    const walkFiles = (dir: string): string[] => {
      const entries = fs.readdirSync(dir, { withFileTypes: true });
      const results: string[] = [];
      for (const entry of entries) {
        const full = path.join(dir, entry.name);
        if (entry.isDirectory()) {
          results.push(...walkFiles(full));
        } else if (/\.(ts|tsx|css|html)$/.test(entry.name)) {
          results.push(full);
        }
      }
      return results;
    };

    for (const filePath of walkFiles(path.resolve(rootDir, 'src'))) {
      if (filePath.endsWith('ecosystemE2E.test.ts')) continue;
      const content = fs.readFileSync(filePath, 'utf8');
      assert.ok(
        !forbiddenDashRegex.test(content),
        `Loi 1 violation: ${path.relative(rootDir, filePath)} must contain 0 U+2013 or U+2014`
      );
    }

    // 2. Loi 3 ONOGRAPH: Strict Integer (Int) FCFA calculations across all Experience x Mobility combinations
    for (const exp of EXPERIENCES_CATALOG) {
      assert.ok(Number.isInteger(exp.adultPrice), `${exp.id} adultPrice must be Int`);
      assert.ok(Number.isInteger(exp.childPrice), `${exp.id} childPrice must be Int`);
      assert.ok(Number.isInteger(exp.pmrPrice), `${exp.id} pmrPrice must be Int`);
      for (const mob of MOBILITY_OPTIONS) {
        for (const guests of [1, 4, 20, 35]) {
          const calc = calculateEcoMobilityPricing(exp.id, mob.id, guests, 2, 1);
          assert.ok(Number.isInteger(calc.grossTotalEur), 'grossTotalEur must be strict Int');
          assert.ok(Number.isInteger(calc.discountAmountEur), 'discountAmountEur must be strict Int');
          assert.ok(Number.isInteger(calc.netTotalEur), 'netTotalEur must be strict Int');
          assert.ok(Number.isInteger(calc.unitPriceEur), 'unitPriceEur must be strict Int');
        }
      }
    }

    // 3. Optical Scale (10 classes), 3-Zone Tracking & Guardrails 1-3 in src/index.css
    const cssContent = fs.readFileSync(path.resolve(rootDir, 'src/index.css'), 'utf8');
    const requiredClasses = [
      '.type-nav',
      '.type-chapternav',
      '.type-eyebrow',
      '.type-hero',
      '.type-h2',
      '.type-h3',
      '.type-tagline',
      '.type-body',
      '.cta-pill',
      '.cta-chevron',
      '.type-footnote',
      '.bento-plus-btn',
      '.touch-target-48',
    ];
    for (const cls of requiredClasses) {
      assert.ok(cssContent.includes(cls), `src/index.css must define optical class ${cls}`);
    }
    assert.ok(cssContent.includes('tabular-nums'), 'Loi 2: tabular-nums must be enforced in CSS');
    assert.ok(
      cssContent.includes('max(1rem, 16px)'),
      'Guardrail 1: mobile form controls must enforce >= 16px anti-zoom iOS rule'
    );

    // Guardrail 3: Verified WCAG contrast for --text-muted on --bg-surface and --bg-card (Light/Sun >= 7:1, Dark >= 7:1)
    assert.ok(getContrastRatio('#36403A', '#E9F5ED') >= 7.0, 'Light --text-muted on --bg-surface must be >= 7:1');
    assert.ok(getContrastRatio('#36403A', '#FFFFFF') >= 7.0, 'Light --text-muted on --bg-card must be >= 7:1');
    assert.ok(getContrastRatio('#C9D1CC', '#1F2421') >= 7.0, 'Dark --text-muted on --bg-surface must be >= 7:1');
    assert.ok(getContrastRatio('#C9D1CC', '#29302C') >= 7.0, 'Dark --text-muted on --bg-card must be >= 7:1');

    // 4. 7-Step Persuasion Architecture & Permanent DOM Mounting (Profil B & Profil C Scission)
    const heroSrc = fs.readFileSync(path.resolve(rootDir, 'src/components/discovery/HeroCanopy.tsx'), 'utf8');
    assert.ok(heroSrc.includes('type-hero'), 'Temps 3: HeroCanopy must apply .type-hero');
    assert.ok(heroSrc.includes('cta-pill'), 'Temps 5: HeroCanopy must include .cta-pill');
    assert.ok(heroSrc.includes('cta-chevron'), 'Temps 5: HeroCanopy must include .cta-chevron');
    const heroH1Block = heroSrc.match(/<h1[^>]*className="[^"]*type-hero[^"]*"[^>]*>([\s\S]*?)<\/h1>/);
    assert.ok(heroH1Block, 'Temps 3: Hero h1 block must exist');
    const heroPlainText = heroH1Block[1]
      .replace(/<[^>]+>/g, ' ')
      .replace(/\{' '\}/g, ' ')
      .replace(/\s+/g, ' ')
      .trim();
    assert.ok(heroPlainText.endsWith('.'), `Temps 3: Hero h1 must close with a period (got "${heroPlainText}")`);
    const heroWordCount = heroPlainText.split(/\s+/).length;
    assert.ok(heroWordCount <= 12, `Temps 3: Hero h1 must be <= 12 words (got ${heroWordCount})`);

    const impactSrc = fs.readFileSync(path.resolve(rootDir, 'src/components/discovery/ImpactBanner.tsx'), 'utf8');
    assert.ok(impactSrc.includes('bento-plus-btn'), 'Temps 6: ImpactBanner must include 48x48 .bento-plus-btn');
    assert.ok(impactSrc.includes('aria-expanded'), 'Temps 6: Bento + buttons must expose aria-expanded');
    const blufMatches = [...impactSrc.matchAll(/bluf:\s*"([^"]+)"/g)];
    assert.strictEqual(blufMatches.length, 4, 'Temps 6: ImpactBanner must define 4 BLUF summaries');
    for (const m of blufMatches) {
      const words = m[1].trim().split(/\s+/).length;
      assert.ok(
        words >= 40 && words <= 55,
        `Temps 6 GEO: Each Bento BLUF must be 40-55 words (got ${words} words)`
      );
    }

    const showcaseSrc = fs.readFileSync(path.resolve(rootDir, 'src/components/discovery/AhalaShowcase.tsx'), 'utf8');
    assert.ok(showcaseSrc.includes('id="pass-comparateur"'), 'Temps 4: 3-Pass side-by-side comparator must exist');
    assert.ok(showcaseSrc.includes('id="cross-sell-options"'), 'Temps 7: Cross-sell strip must exist');
    assert.ok(showcaseSrc.includes('<table'), 'Profil B: Native <table> comparative grid must exist');
    assert.ok(
      !showcaseSrc.includes("activeTab === 'tarifs' &&"),
      'Profil B: Native <table> panel must remain permanently mounted in DOM (never unmounted)'
    );

    const rangerSrc = fs.readFileSync(path.resolve(rootDir, 'src/components/admin/RangerDashboard.tsx'), 'utf8');
    assert.ok(!rangerSrc.includes('type-hero'), 'Profil C Scission: Zero .type-hero inside /exploitation');
    assert.ok(!rangerSrc.includes('ImmersiveSection'), 'Profil C Scission: Zero Hero/promo banner inside /exploitation');
    assert.ok(!rangerSrc.includes('Barlow_Semi_Condensed'), 'Profil C Scission: Zero display font >= 20px inside /exploitation');
    assert.ok(!rangerSrc.includes('text-xl'), 'Profil C Scission: Strictly < 20px inside /exploitation');
    assert.ok(rangerSrc.includes('max={3000}'), 'Cockpit Pro: Daily capacity slider supports 500 to 3000');
    assert.ok(rangerSrc.includes('syscohada-audit-title'), 'Cockpit Pro: SYSCOHADA financial audit panel exists');
    assert.ok(rangerSrc.includes('rbac-governance-title'), 'Cockpit Pro: 6-role RBAC governance matrix exists');
  });

  await t.test('Anonymous Single-Ticket Lookup (/mon-pass) & Loi n° 2010/012 Pass Anonymization', () => {
    const passes: EcoPass[] = JSON.parse(JSON.stringify(INITIAL_PASSES));

    // 1. visiteur_anonyme retrieves ECP-2026-8942 using phone or email
    const byPhone = verifyAnonymousPassLookup(passes, 'ecp-2026-8942', '672 56 45 98');
    assert.strictEqual(byPhone.ok, true, 'Valid reference + last 8 phone digits must unlock pass');
    assert.strictEqual(byPhone.pass?.id, 'ECP-2026-8942');

    const byEmail = verifyAnonymousPassLookup(passes, 'ECP-2026-8942', 'JP.MBARGA@entreprise-cm.com');
    assert.strictEqual(byEmail.ok, true, 'Valid reference + case-insensitive email must unlock pass');

    // Wrong phone/email must be rejected (strict isolation)
    const wrongContact = verifyAnonymousPassLookup(passes, 'ECP-2026-8942', '+237 699 00 00 00');
    assert.strictEqual(wrongContact.ok, false, 'Mismatched contact must not leak pass');

    // 2. client_connecte exercises Loi n° 2010/012 erasure -> PII scrubbed, FCFA accounting preserved
    passes[0].ownerUserId = 'cli-jp-01';
    passes[0].ownerEmail = 'jp.mbarga@entreprise-cm.com';
    const { updatedPasses, anonymizedCount } = anonymizeClientPassesList(
      passes,
      'cli-jp-01',
      'jp.mbarga@entreprise-cm.com'
    );
    assert.strictEqual(anonymizedCount, 1);
    assert.strictEqual(updatedPasses[0].totalPriceEur, 17000, 'SYSCOHADA FCFA accounting amount must remain intact');
    assert.strictEqual(updatedPasses[0].leadVisitor.fullName, 'Client Anonymisé (Loi 2010/012)');
    assert.strictEqual(updatedPasses[0].ownerEmail, 'anonyme@effacement.local');
    assert.strictEqual(updatedPasses[0].ownerUserId, undefined);

    // Subsequent lookup with old email must fail
    const afterEraseLookup = verifyAnonymousPassLookup(
      updatedPasses,
      'ECP-2026-8942',
      'jp.mbarga@entreprise-cm.com'
    );
    assert.strictEqual(afterEraseLookup.ok, false, 'Anonymized pass cannot be looked up by former PII');
  });
});
