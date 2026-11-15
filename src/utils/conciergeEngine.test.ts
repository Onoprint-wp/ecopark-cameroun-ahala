import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {
  CONCIERGE_QUICK_PROMPTS,
  classifyConciergeIntent,
  detectConciergeLanguage,
  generateConciergeReply,
  getConciergeWelcome,
} from './conciergeEngine.ts';
import { isEditorialCompliant } from './editorialSanitizer.ts';
import { OFFICIAL_PHONE_DIGITS } from './outgoingTemplates.ts';

test('Concierge Virtuel Bilingue FR/EN & Conformité Loi 2024/017', async (t) => {
  await t.test('Détection automatique FR/EN et routage métier (tarifs, hôtels, salle 500 pl., CFP, avis)', () => {
    assert.strictEqual(detectConciergeLanguage('Bonjour, quels sont vos tarifs ?', 'en'), 'fr');
    assert.strictEqual(detectConciergeLanguage('Hello, how much are the hotel rooms?', 'fr'), 'en');

    assert.strictEqual(classifyConciergeIntent('Prix entrée piscine et parc'), 'tarifs');
    assert.strictEqual(classifyConciergeIntent('Suite VIP Ewondo disponible cette nuit ?'), 'hotels');
    assert.strictEqual(classifyConciergeIntent('Devis salle Menkii 500 places séminaire'), 'evenements');
    assert.strictEqual(classifyConciergeIntent('Menu poisson braisé Château des Saveurs'), 'restaurant');
    assert.strictEqual(classifyConciergeIntent('Inscription formation CFP MINEFOP'), 'cfp');
    assert.strictEqual(classifyConciergeIntent('Horaires et itinéraire station Tradex Ahala'), 'acces');
    assert.strictEqual(classifyConciergeIntent('Règlement par MTN MoMo ou Orange Money'), 'paiement');
    assert.strictEqual(classifyConciergeIntent('Je veux laisser un avis suite à ma visite'), 'avis');
  });

  await t.test('Exactitude SSOT FCFA et routage WhatsApp dédié Hôtels vs Direction', () => {
    const tarifsFr = generateConciergeReply('Quels sont les tarifs du parc ?', 'fr');
    assert.strictEqual(tarifsFr.intent, 'tarifs');
    assert.strictEqual(tarifsFr.lang, 'fr');
    const joinedTarifs = tarifsFr.bullets.join(' ');
    assert.ok(joinedTarifs.includes('1 000 FCFA') && joinedTarifs.includes('500 FCFA'));
    assert.ok(joinedTarifs.includes('2 500 FCFA') && joinedTarifs.includes('4 500 FCFA') && joinedTarifs.includes('8 500 FCFA'));
    assert.ok(tarifsFr.whatsappUrl.startsWith(`https://wa.me/${OFFICIAL_PHONE_DIGITS.DIRECTION}?text=`));

    const hotelsEn = generateConciergeReply('Hello, how much are the hotel rooms tonight?', 'fr');
    assert.strictEqual(hotelsEn.intent, 'hotels');
    assert.strictEqual(hotelsEn.lang, 'en');
    const joinedHotels = hotelsEn.bullets.join(' ');
    assert.ok(joinedHotels.includes('10 000') && joinedHotels.includes('45 000 FCFA'));
    assert.ok(
      hotelsEn.whatsappUrl.startsWith(`https://wa.me/${OFFICIAL_PHONE_DIGITS.HOTEL}?text=`),
      'Les demandes hôtelières doivent cibler la ligne Réception Hôtels 24h/24'
    );

    const cfpFr = generateConciergeReply('Frais scolarité CFP MINEFOP', 'fr');
    assert.strictEqual(cfpFr.intent, 'cfp');
    assert.ok(cfpFr.bullets.join(' ').includes('50 000 FCFA') && cfpFr.bullets.join(' ').includes('250 000 FCFA'));
  });

  await t.test('Conformité éditoriale intégrale (zéro tiret long, zéro cliché IA, zéro jargon banni)', () => {
    for (const lang of ['fr', 'en'] as const) {
      const welcome = getConciergeWelcome(lang);
      assert.strictEqual(isEditorialCompliant(welcome.title), true);
      assert.strictEqual(isEditorialCompliant(welcome.subtitle), true);
      assert.strictEqual(isEditorialCompliant(welcome.greeting), true);

      for (const prompt of CONCIERGE_QUICK_PROMPTS[lang]) {
        assert.strictEqual(isEditorialCompliant(prompt.label), true);
        assert.strictEqual(isEditorialCompliant(prompt.query), true);

        const reply = generateConciergeReply(prompt.query, lang);
        assert.strictEqual(isEditorialCompliant(reply.headline), true, `Headline non conforme: ${reply.headline}`);
        assert.strictEqual(isEditorialCompliant(reply.body), true, `Body non conforme: ${reply.body}`);
        for (const bullet of reply.bullets) {
          assert.strictEqual(isEditorialCompliant(bullet), true, `Bullet non conforme: ${bullet}`);
        }
        assert.strictEqual(isEditorialCompliant(reply.whatsappLabel), true);
      }
    }
  });

  await t.test('Conformité Loi n° 2024/017 et vérité technique sans Supabase dans LegalNoticeView.tsx', () => {
    const legalPath = path.resolve(process.cwd(), 'src/components/legal/LegalNoticeView.tsx');
    const legalContent = fs.readFileSync(legalPath, 'utf8');

    assert.ok(
      legalContent.includes('2024/017'),
      'LegalNoticeView.tsx doit référencer la Loi n° 2024/017 sur la protection des données personnelles'
    );
    assert.ok(
      !legalContent.includes('Supabase Auth'),
      'LegalNoticeView.tsx ne doit pas affirmer utiliser Supabase Auth tant que le déploiement est autonome sur Vercel'
    );
  });
});
