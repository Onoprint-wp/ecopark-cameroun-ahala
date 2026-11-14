/**
 * ECOPARK CAMEROUN - Suite de Tests Automatisée de Gouvernance Éditoriale & Garde-fou CI (G6)
 *
 * Ce garde-fou CI bloquant protège l'ensemble du dépôt contre :
 * 1. Les altérations d'encodage (mojibake \uFFFD, UTF-8 corrompu) et erreurs de syntaxe JSON.
 * 2. La réintroduction de tirets longs cadratin (\u2014) ou demi-cadratin (\u2013).
 * 3. Les clichés d'écriture artificielle (IA) et termes de jargon banni.
 * 4. Les élisions françaises orphelines sans apostrophe.
 * 5. Les dérives de tarification ou de garantie entre les sources de vérité et les fichiers LLM/agents.
 * 6. Les régressions sur les modules d'assainissement dynamique et modèles sortants.
 * 7. L'absence ou la non-conformité du plan de gouvernance éditoriale racine.
 */

import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {
  sanitizeEditorialText,
  detectEditorialViolations,
  isEditorialCompliant,
  CLOSURE_REASON_TEMPLATES,
  BANNED_AI_CLICHES,
  BANNED_JARGON_TERMS,
} from './editorialSanitizer.ts';
import {
  getWhatsAppUrl,
  isValidOfficialPhoneNumber,
  normalizePhoneToDigits,
  OFFICIAL_PHONE_NUMBERS,
  OFFICIAL_PHONE_DIGITS,
  OUTGOING_WHATSAPP_TEMPLATES,
} from './outgoingTemplates.ts';
import {
  EXPERIENCES_CATALOG,
  MOBILITY_OPTIONS,
} from './ecoMobility.ts';

const rootDir = process.cwd();

/**
 * Fonction utilitaire récursive pour parcourir l'arborescence des fichiers
 */
function walkDirectory(dir: string): string[] {
  let fileList: string[] = [];
  const entries = fs.readdirSync(dir);
  for (const entry of entries) {
    if (['node_modules', '.git', 'dist', '.agents'].includes(entry)) {
      continue;
    }
    const fullPath = path.join(dir, entry);
    const stat = fs.statSync(fullPath);
    if (stat.isDirectory()) {
      fileList = fileList.concat(walkDirectory(fullPath));
    } else {
      fileList.push(fullPath);
    }
  }
  return fileList;
}

test('Garde-fou CI & Gouvernance Éditoriale Durable (G6)', async (t) => {
  const allFiles = walkDirectory(rootDir);

  // ==========================================================================
  // Test 1 : Intégrité d'encodage et validation des fichiers JSON
  // ==========================================================================
  await t.test('Test 1 : Intégrité d\'encodage UTF-8 et syntaxe JSON stricte', () => {
    const textFiles = allFiles.filter((filePath) => {
      const rel = path.relative(rootDir, filePath).replace(/\\/g, '/');
      return (
        (rel.startsWith('src/') ||
          rel.startsWith('public/') ||
          rel.startsWith('supabase/') ||
          rel === 'index.html') &&
        /\.(ts|tsx|json|html|sql|txt)$/.test(rel)
      );
    });

    assert.ok(textFiles.length >= 40, `Le corpus de fichiers audités doit être suffisant (trouvé ${textFiles.length})`);

    // Regex détectant le caractère de remplacement \uFFFD et le mojibake UTF-8
    const corruptedEncodingPattern = /[\uFFFD]|\u00C3[\u0080-\u00BF]/;

    for (const file of textFiles) {
      const content = fs.readFileSync(file, 'utf8');
      assert.ok(
        !corruptedEncodingPattern.test(content),
        `Caractère d'encodage corrompu détecté dans : ${file}`
      );

      // Si le fichier est un JSON, vérifier la validité syntaxique
      if (file.endsWith('.json')) {
        assert.doesNotThrow(
          () => JSON.parse(content),
          `Le fichier JSON ${file} doit être un JSON syntaxiquement valide`
        );
      }
    }
  });

  // ==========================================================================
  // Test 2 : Zéro tiret long (\u2014 / \u2013) dans l'ensemble du projet
  // ==========================================================================
  await t.test('Test 2 : Zéro tiret cadratin (\\u2014) et demi-cadratin (\\u2013)', () => {
    const targetFiles = allFiles.filter((filePath) => {
      const rel = path.relative(rootDir, filePath).replace(/\\/g, '/');
      return (
        (rel.startsWith('src/') ||
          rel.startsWith('public/') ||
          rel.startsWith('supabase/migrations/') ||
          rel === 'index.html') &&
        /\.(ts|tsx|html|sql|txt|json|css)$/.test(rel)
      );
    });

    const longDashPattern = /[\u2013\u2014]/;
    const filesWithLongDash: string[] = [];

    for (const file of targetFiles) {
      const content = fs.readFileSync(file, 'utf8');
      if (longDashPattern.test(content)) {
        filesWithLongDash.push(file);
      }
    }

    assert.deepStrictEqual(
      filesWithLongDash,
      [],
      `Aucun tiret long ne doit être présent dans le dépôt. Détecté dans : ${filesWithLongDash.join(', ')}`
    );
  });

  // ==========================================================================
  // Test 3 : Éradication du jargon banni et des clichés d'écriture artificielle IA
  // ==========================================================================
  await t.test('Test 3 : Éradication des clichés IA et du jargon banni dans les composants et données UI', () => {
    const uiFiles = allFiles.filter((filePath) => {
      const rel = path.relative(rootDir, filePath).replace(/\\/g, '/');
      return (
        (rel.startsWith('src/components/') && rel.endsWith('.tsx')) ||
        rel === 'src/App.tsx' ||
        rel === 'src/data/initialParkData.ts' ||
        rel === 'src/utils/ecoMobility.ts'
      );
    });

    assert.ok(uiFiles.length >= 15, 'Tous les composants TSX et données UI doivent être audités');

    for (const file of uiFiles) {
      const content = fs.readFileSync(file, 'utf8');
      const lower = content.toLowerCase();

      // Vérification des clichés IA
      for (const cliche of BANNED_AI_CLICHES) {
        assert.ok(
          !lower.includes(cliche.toLowerCase()),
          `Cliché IA proscrit « ${cliche} » détecté dans ${file}`
        );
      }

      // Vérification stricte du jargon banni UI (aucune exception tolérée)
      for (const jargon of BANNED_JARGON_TERMS) {
        assert.ok(
          !content.includes(jargon),
          `Jargon banni « ${jargon} » détecté dans ${file}`
        );
      }

      // Vérification de la centralisation des liens WhatsApp (zéro wa.me codé en dur dans les composants)
      if (file.endsWith('.tsx')) {
        assert.ok(
          !content.includes('https://wa.me/'),
          `Lien https://wa.me/ codé en dur détecté dans ${file} : utiliser getWhatsAppUrl() depuis outgoingTemplates.ts`
        );
      }
    }
  });

  // ==========================================================================
  // Test 4 : Zéro élision française sans apostrophe dans src/
  // ==========================================================================
  await t.test('Test 4 : Zéro élision française orpheline sans apostrophe dans src/', () => {
    const sourceFiles = allFiles.filter((filePath) => {
      const rel = path.relative(rootDir, filePath).replace(/\\/g, '/');
      return (
        rel.startsWith('src/') &&
        (rel.endsWith('.ts') || rel.endsWith('.tsx')) &&
        !rel.includes('.test.ts') &&
        !rel.endsWith('editorialSanitizer.ts')
      );
    });

    const unelidedPatterns = [
      { pattern: /\bd\s+Ahala\b/i, name: "d'Ahala" },
      { pattern: /\bd\s+entrée\b/i, name: "d'entrée" },
      { pattern: /\bl\s+eau\b/i, name: "l'eau" },
      { pattern: /\bvient\s+d\s+être\b/i, name: "vient d'être" },
      { pattern: /\bd\s+alevinage\b/i, name: "d'alevinage" },
      { pattern: /\bd\s+évaluation\b/i, name: "d'évaluation" },
      { pattern: /\bl\s+Hôtel\b/i, name: "l'Hôtel" },
      { pattern: /\baujourd\s+hui\b/i, name: "aujourd'hui" },
      { pattern: /\bd\s+hébergement\b/i, name: "d'hébergement" },
      { pattern: /\bl\s+accès\b/i, name: "l'accès" },
      { pattern: /\bl\s+ombrage\b/i, name: "l'ombrage" },
      { pattern: /\bd\s+ombre\b/i, name: "d'ombre" },
      { pattern: /\bl\s+Éco-Pass\b/i, name: "l'Éco-Pass" },
      { pattern: /\bJ\s+ai\b/i, name: "J'ai" },
      { pattern: /\bm\s+engage\b/i, name: "m'engage" },
      { pattern: /\bl\s+équipe\b/i, name: "l'équipe" },
      { pattern: /\bd\s+intervention\b/i, name: "d'intervention" },
      { pattern: /\bl\s+éco-garde\b/i, name: "l'éco-garde" },
    ];

    for (const file of sourceFiles) {
      const content = fs.readFileSync(file, 'utf8');
      for (const { pattern, name } of unelidedPatterns) {
        assert.ok(
          !pattern.test(content),
          `Élision orpheline sans apostrophe détectée dans ${file} pour « ${name} »`
        );
      }
    }
  });

  // ==========================================================================
  // Test 5 : Parité SSOT stricte Tarifs & Garanties (src/ vs public/llms.txt & public/agents.txt)
  // ==========================================================================
  await t.test('Test 5 : Parité SSOT stricte Tarifs, Garanties & Accents français dans llms.txt et agents.txt', () => {
    const llmsPath = path.resolve(rootDir, 'public/llms.txt');
    const agentsPath = path.resolve(rootDir, 'public/agents.txt');

    assert.ok(fs.existsSync(llmsPath), 'public/llms.txt doit exister');
    assert.ok(fs.existsSync(agentsPath), 'public/agents.txt doit exister');

    const llmsContent = fs.readFileSync(llmsPath, 'utf8');
    const agentsContent = fs.readFileSync(agentsPath, 'utf8');

    // 1. Pass Découverte Nature (2 500 FCFA adulte / 1 500 FCFA enfant)
    assert.ok(
      /2\s*500/.test(llmsContent),
      'public/llms.txt doit contenir le tarif officiel de 2 500 FCFA pour le Pass Découverte'
    );
    assert.ok(
      /2500|2\s*500/.test(agentsContent),
      'public/agents.txt doit contenir le tarif officiel de 2 500 FCFA pour le Pass Découverte'
    );

    // 2. Pass Journée Complète (4 500 FCFA adulte / 2 500 FCFA enfant)
    assert.ok(
      /4\s*500/.test(llmsContent),
      'public/llms.txt doit contenir le Pass Journée Complète à 4 500 FCFA'
    );
    assert.ok(
      /4500|4\s*500/.test(agentsContent),
      'public/agents.txt doit contenir le Pass Journée Complète à 4 500 FCFA'
    );

    // 3. Pass Journée Royale (8 500 FCFA adulte / 4 500 FCFA enfant)
    assert.ok(
      /8\s*500/.test(llmsContent),
      'public/llms.txt doit contenir le Pass Journée Royale à 8 500 FCFA'
    );
    assert.ok(
      /8500|8\s*500/.test(agentsContent),
      'public/agents.txt doit contenir le Pass Journée Royale à 8 500 FCFA'
    );

    // 4. Plafond Suites Prestige VIP (45 000 FCFA)
    assert.ok(
      /45\s*000/.test(llmsContent),
      'public/llms.txt doit mentionner le palier Suites Prestige VIP jusqu\'à 45 000 FCFA'
    );
    assert.ok(
      /45000|45\s*000/.test(agentsContent),
      'public/agents.txt doit mentionner le palier Suites Prestige VIP jusqu\'à 45 000 FCFA'
    );

    // 5. Navette Climatisée A/R (1 500 FCFA adulte / 1 000 FCFA enfant)
    assert.ok(
      /1\s*500/.test(llmsContent) && /1\s*000/.test(llmsContent),
      'public/llms.txt doit contenir la tarification navette 1 500 FCFA / 1 000 FCFA'
    );
    assert.ok(
      /1500|1\s*500/.test(agentsContent),
      'public/agents.txt doit contenir la tarification navette 1 500 FCFA'
    );

    // 6. Garantie Météo RN3 à 90 jours
    assert.ok(
      /Garantie Météo RN3/i.test(llmsContent) && /90\s*jours/i.test(llmsContent),
      'public/llms.txt doit stipuler la Garantie Météo RN3 valable 90 jours'
    );
    assert.ok(
      /90\s*jours/i.test(agentsContent),
      'public/agents.txt doit stipuler la garantie météo de 90 jours'
    );

    // 7. Rétablissement complet des accents français (100 %)
    assert.ok(
      /[éèêàâôûîç]/i.test(llmsContent),
      'public/llms.txt doit contenir les accents français (Yaoundé, Météo, etc.)'
    );
    assert.ok(
      /[éèêàâôûîç]/i.test(agentsContent),
      'public/agents.txt doit contenir les accents français'
    );
  });

  // ==========================================================================
  // Test 6 : Tests unitaires de editorialSanitizer.ts & outgoingTemplates.ts
  // ==========================================================================
  await t.test('Test 6 : Tests unitaires de conformité éditoriale et modèles sortants', () => {
    // 1. Assainissement des tirets longs
    const dirtyDashText = 'Visite guidée \u2014 découverte des biomes \u2013 sentier de pirogue';
    const cleanedDashText = sanitizeEditorialText(dirtyDashText);
    assert.strictEqual(
      cleanedDashText,
      'Visite guidée - découverte des biomes - sentier de pirogue',
      'Les tirets longs doivent être convertis en tirets standards'
    );

    // 2. Normalisation des espaces multiples et trim
    const dirtySpacesText = '  Sentier    ouvert    en     saison   sèche.   ';
    const cleanedSpacesText = sanitizeEditorialText(dirtySpacesText);
    assert.strictEqual(
      cleanedSpacesText,
      'Sentier ouvert en saison sèche.',
      'Les espaces multiples et superflus doivent être normalisés'
    );

    // 3. Gestion des entrées nulles / vides
    assert.strictEqual(sanitizeEditorialText(null), '');
    assert.strictEqual(sanitizeEditorialText(undefined), '');
    assert.strictEqual(sanitizeEditorialText(''), '');

    // 4. Détection d'infractions (detectEditorialViolations)
    const textWithCliche = 'Une immersion au cœur de la faune sauvage.';
    const violationsCliche = detectEditorialViolations(textWithCliche);
    assert.ok(
      violationsCliche.length > 0,
      'detectEditorialViolations doit identifier le cliché IA « au cœur d »'
    );

    const textWithJargon = 'Session Day-Use disponible à l\'accueil.';
    const violationsJargon = detectEditorialViolations(textWithJargon);
    assert.ok(
      violationsJargon.length > 0,
      'detectEditorialViolations doit identifier le jargon « Day-Use »'
    );

    const textWithLongDash = 'Sentier balisé \u2014 prudence requise';
    const violationsLongDash = detectEditorialViolations(textWithLongDash);
    assert.ok(
      violationsLongDash.length > 0,
      'detectEditorialViolations doit identifier les tirets longs'
    );

    const cleanText = 'Sentier botanique sécurisé et balisé par nos guides.';
    assert.strictEqual(
      detectEditorialViolations(cleanText).length,
      0,
      'Un texte conforme ne doit produire aucune violation'
    );
    assert.strictEqual(isEditorialCompliant(cleanText), true);

    // 5. Validation des modèles pré-approuvés de fermeture
    assert.ok(
      CLOSURE_REASON_TEMPLATES.length >= 5,
      'CLOSURE_REASON_TEMPLATES doit contenir au moins 5 motifs'
    );
    for (const template of CLOSURE_REASON_TEMPLATES) {
      assert.strictEqual(
        detectEditorialViolations(template).length,
        0,
        `Le modèle de fermeture « ${template} » doit être strictement conforme`
      );
    }

    // 6. Validation du générateur de lien WhatsApp (outgoingTemplates)
    const whatsappUrl = getWhatsAppUrl(
      OFFICIAL_PHONE_NUMBERS.DIRECTION,
      OUTGOING_WHATSAPP_TEMPLATES.TICKETING_RESERVATION
    );
    assert.ok(
      whatsappUrl.startsWith('https://wa.me/237672564598?text='),
      'L\'URL WhatsApp doit cibler le numéro officiel de la direction'
    );
    assert.ok(
      whatsappUrl.includes(encodeURIComponent('Bonjour EcoPark Cameroun')),
      'Le message textuel doit être encodé via encodeURIComponent'
    );

    // 7. Validation des numéros de téléphone officiels
    assert.strictEqual(OFFICIAL_PHONE_DIGITS.DIRECTION, '237672564598');
    assert.strictEqual(OFFICIAL_PHONE_DIGITS.HOTEL, '237694601449');
    assert.strictEqual(OFFICIAL_PHONE_DIGITS.STANDARD, '237697136203');
    assert.strictEqual(isValidOfficialPhoneNumber('+237 672 56 45 98'), true);
    assert.strictEqual(isValidOfficialPhoneNumber('+237 694 60 14 49'), true);
    assert.strictEqual(isValidOfficialPhoneNumber('+237 697 13 62 03'), true);
    assert.strictEqual(isValidOfficialPhoneNumber('+237 600 00 00 00'), false);
    assert.strictEqual(normalizePhoneToDigits('+237 672-56-45-98'), '237672564598');

    // 8. Vérification de la disponibilité des catalogues
    assert.ok(EXPERIENCES_CATALOG.length >= 3, 'EXPERIENCES_CATALOG doit contenir au moins 3 formules');
    assert.ok(MOBILITY_OPTIONS.length >= 2, 'MOBILITY_OPTIONS doit contenir au moins 2 options');
  });

  // ==========================================================================
  // Test 7 : Présence et conformité du plan de gouvernance éditoriale racine
  // ==========================================================================
  await t.test('Test 7 : Conformité structurelle du plan editorial-governance-plan.md', () => {
    const planPath = path.resolve(rootDir, 'editorial-governance-plan.md');
    assert.ok(
      fs.existsSync(planPath),
      'Le plan editorial-governance-plan.md doit impérativement exister à la racine'
    );

    const planContent = fs.readFileSync(planPath, 'utf8');

    // 1. Vérification de l'objectif (1 phrase)
    assert.ok(
      planContent.includes('## Goal'),
      'Le plan doit contenir une section ## Goal'
    );

    // 2. Vérification des 8 tâches atomiques
    const taskMatches = planContent.match(/-\s*\[[ x]\]\s*Task\s*\d+/gi) || [];
    assert.strictEqual(
      taskMatches.length,
      8,
      `Le plan doit contenir exactement 8 tâches atomiques (trouvé ${taskMatches.length})`
    );

    // 3. Vérification du glossaire de 20 entrées
    const glossaryTableMatches = planContent.match(/\|\s*\d+\s*\|/g) || [];
    assert.strictEqual(
      glossaryTableMatches.length,
      20,
      `Le glossaire officiel doit comporter exactement 20 entrées (trouvé ${glossaryTableMatches.length})`
    );

    // 4. Section Done When
    assert.ok(
      planContent.includes('## Done When'),
      'Le plan doit comporter la section ## Done When'
    );
  });
});
