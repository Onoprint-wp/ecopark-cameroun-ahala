/**
 * ECOPARK CAMEROUN (YAOUNDÉ - AHALA, RN3) - MOTEUR CONCIERGE VIRTUEL BILINGUE (FR / EN)
 * (src/utils/conciergeEngine.ts)
 *
 * Moteur déterministe autonome (100 % Edge / navigateur sur Vercel, zéro base externe requise
 * avant mise en service opérationnelle, zéro clé API tierce exposée) ancré sur les sources
 * officielles du complexe : ecoMobility.ts et outgoingTemplates.ts.
 */

import type { ActiveView } from '../types/ecosystem.ts';
import type { ShowcaseTab } from './ecoRouting.ts';
import { EXPERIENCES_CATALOG } from './ecoMobility.ts';
import { sanitizeEditorialText } from './editorialSanitizer.ts';
import {
  getWhatsAppUrl,
  OFFICIAL_PHONE_NUMBERS,
} from './outgoingTemplates.ts';

export type ConciergeLang = 'fr' | 'en';

export type ConciergeIntent =
  | 'tarifs'
  | 'hotels'
  | 'restaurant'
  | 'evenements'
  | 'cfp'
  | 'acces'
  | 'paiement'
  | 'avis'
  | 'general';

export interface ConciergeNavigationAction {
  label: string;
  targetView: ActiveView;
  showcaseTab?: ShowcaseTab;
  anchorId?: string;
}

export interface ConciergeReply {
  intent: ConciergeIntent;
  lang: ConciergeLang;
  headline: string;
  body: string;
  bullets: string[];
  navAction?: ConciergeNavigationAction;
  whatsappLabel: string;
  whatsappPhone: string;
  whatsappUrl: string;
}

export interface ConciergeQuickPrompt {
  id: string;
  label: string;
  query: string;
}

export const CONCIERGE_QUICK_PROMPTS: Record<ConciergeLang, readonly ConciergeQuickPrompt[]> = {
  fr: [
    {
      id: 'tarifs',
      label: 'Tarifs & Pass QR',
      query: 'Quels sont les tarifs du parc, de la piscine et des Pass Tout-Inclus ?',
    },
    {
      id: 'hotels',
      label: 'Hôtels 24h/24',
      query: 'Quels sont les tarifs des chambres et suites dans vos cités hôtelières ?',
    },
    {
      id: 'evenements',
      label: 'Salle 500 pl. & Groupes',
      query: 'Comment réserver la salle de 500 places pour un séminaire ou une sortie scolaire ?',
    },
    {
      id: 'restaurant',
      label: 'Restaurant',
      query: 'Quelle est la carte du restaurant Le Château des Saveurs et ses horaires ?',
    },
    {
      id: 'cfp',
      label: 'CFP MINEFOP',
      query: 'Quelles sont les filières et frais de scolarité du CFP agréé MINEFOP ?',
    },
    {
      id: 'acces',
      label: 'Accès RN3 & Météo',
      query: "Où se situe ECOPARK à Ahala, quels sont les horaires et la Garantie Météo ?",
    },
    {
      id: 'avis',
      label: 'Donner un avis',
      query: "Je souhaite partager un avis ou une suggestion sur mon passage à ECOPARK.",
    },
  ],
  en: [
    {
      id: 'tarifs',
      label: 'Rates & QR Passes',
      query: 'What are the park, swimming pool and all-inclusive QR pass rates in FCFA?',
    },
    {
      id: 'hotels',
      label: '24/7 Hotels',
      query: 'What are the nightly rates for your hotel rooms and VIP suites?',
    },
    {
      id: 'evenements',
      label: '500-Seat Hall & Groups',
      query: 'How can we book the 500-seat conference hall for a corporate seminar or school trip?',
    },
    {
      id: 'restaurant',
      label: 'Restaurant',
      query: 'What dishes and opening hours do you offer at Le Château des Saveurs restaurant?',
    },
    {
      id: 'cfp',
      label: 'MINEFOP Training',
      query: 'What vocational programs and tuition fees apply at CFP ECOPARK?',
    },
    {
      id: 'acces',
      label: 'Directions & Hours',
      query: 'Where is ECOPARK located in Yaoundé Ahala and what is the weather guarantee?',
    },
    {
      id: 'avis',
      label: 'Guest Feedback',
      query: 'I would like to leave guest feedback or a review about our visit.',
    },
  ],
};

function formatFcfa(amount: number): string {
  return amount.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ') + ' FCFA';
}

/**
 * Détecte automatiquement si la question saisie est formulée en anglais ou en français.
 */
export function detectConciergeLanguage(
  query: string,
  fallbackLang: ConciergeLang = 'fr'
): ConciergeLang {
  const normalized = query.toLowerCase().trim();
  if (!normalized) return fallbackLang;

  const englishMarkers =
    /\b(hello|hi|how much|price|rates|room|rooms|hotel|booking|book|pool|swimming|where|when|open|opening|hours|conference|hall|school|training|tuition|menu|food|feedback|review|thank you|thanks|english|shuttle|weather)\b/i;
  const frenchMarkers =
    /\b(bonjour|bonsoir|combien|tarif|tarifs|prix|chambre|chambres|hôtel|hôtels|réserver|piscine|où|quand|horaire|horaires|salle|séminaire|école|scolaire|formation|scolarité|repas|poisson|avis|merci|navette|météo)\b/i;

  const hasEn = englishMarkers.test(normalized);
  const hasFr = frenchMarkers.test(normalized);

  if (hasEn && !hasFr) return 'en';
  if (hasFr && !hasEn) return 'fr';
  return fallbackLang;
}

/**
 * Identifie l'intention principale du visiteur à partir de sa question libre.
 */
export function classifyConciergeIntent(query: string): ConciergeIntent {
  const q = query.toLowerCase();

  if (
    /\b(avis|suggestion|plainte|réclamation|félicitation|retour|satisfaction|commentaire|feedback|review|complaint|compliment|rating)\b/i.test(
      q
    )
  ) {
    return 'avis';
  }

  if (
    /\b(cfp|minefop|formation|formations|filière|filières|scolarité|diplôme|dqp|cqp|apprenant|inscription|pisciculture|agropastoral|training|vocational|tuition|course|schooling)\b/i.test(
      q
    )
  ) {
    return 'cfp';
  }

  if (
    /\b(chambre|chambres|hôtel|hôtels|hotel|hotels|suite|suites|ewondo|chanthel|bene|nuit|nuitée|hébergement|loger|dormir|couple|lodge|room|rooms|stay|overnight|accommodation)\b/i.test(
      q
    )
  ) {
    return 'hotels';
  }

  if (
    /\b(salle|menkii|500|séminaire|seminaire|mariage|entreprise|entreprises|banquet|groupe|groupes|école|ecole|scolaire|élève|eleve|association|conference|seminar|wedding|corporate|group|school)\b/i.test(
      q
    )
  ) {
    return 'evenements';
  }

  if (
    /\b(restaurant|château des saveurs|chateau des saveurs|manger|repas|menu|carte|poisson|braisé|poulet dg|ndolé|ndole|grillade|pergola|boisson|dîner|déjeuner|food|dining|eat|lunch|dinner|dish|fish)\b/i.test(
      q
    )
  ) {
    return 'restaurant';
  }

  if (
    /\b(mobile money|orange money|momo|mtn|airtel|carte bancaire|espèces|especes|payer|paiement|règlement|reglement|qr|billet|pass électronique|pay|payment|cash|ticket)\b/i.test(
      q
    ) &&
    !/\b(combien|tarif|tarifs|prix|how much|rates)\b/i.test(q)
  ) {
    return 'paiement';
  }

  if (
    /\b(où|adresse|itinéraire|itineraire|tradex|rn3|ahala|horaire|horaires|ouvert|ouverture|fermé|lundi|navette|bus|parking|pluie|météo|meteo|garantie|where|location|directions|address|open|opening|hours|shuttle|weather|rain)\b/i.test(
      q
    )
  ) {
    return 'acces';
  }

  if (
    /\b(tarif|tarifs|prix|combien|coût|cout|entrée|entree|zoo|piscine|pirogue|cheval|manège|manege|pass|formule|adulte|enfant|price|prices|rate|rates|cost|how much|pool|canoe|horse)\b/i.test(
      q
    )
  ) {
    return 'tarifs';
  }

  return 'general';
}

export function getConciergeWelcome(lang: ConciergeLang): {
  title: string;
  subtitle: string;
  greeting: string;
} {
  if (lang === 'en') {
    return {
      title: 'ECOPARK Virtual Concierge',
      subtitle: '24/7 Bilingual Desk • Yaoundé - Ahala (RN3)',
      greeting:
        'Welcome to ECOPARK CAMEROUN! Ask me anything in English or French about our FCFA rates, 24/7 hotel residences, 500-seat Menkii hall, restaurant, CFP MINEFOP vocational center, or transfer your request directly to our WhatsApp desk.',
    };
  }
  return {
    title: 'Concierge Virtuel ECOPARK',
    subtitle: 'Accueil bilingue 24h/24 • Yaoundé - Ahala (RN3)',
    greeting:
      "Bienvenue à ECOPARK CAMEROUN ! Posez-moi votre question en français ou en anglais : tarifs officiels FCFA, 4 cités hôtelières 24h/24, salle Menkii de 500 places, restaurant, CFP agréé MINEFOP, ou transférez votre dossier pré-qualifié sur WhatsApp en 1 clic.",
  };
}

/**
 * Génère la réponse structurée, vérifiée et conforme du Concierge Virtuel.
 */
export function generateConciergeReply(
  rawQuery: string,
  preferredLang: ConciergeLang = 'fr'
): ConciergeReply {
  const cleanQuery = sanitizeEditorialText(rawQuery);
  const lang = detectConciergeLanguage(cleanQuery, preferredLang);
  const intent = classifyConciergeIntent(cleanQuery);

  const zoo = EXPERIENCES_CATALOG.find((e) => e.id === 'sentiers') || EXPERIENCES_CATALOG[0];
  const decouverte = EXPERIENCES_CATALOG.find((e) => e.id === 'eco_guide') || EXPERIENCES_CATALOG[1];
  const complete = EXPERIENCES_CATALOG.find((e) => e.id === 'pack_mobilite') || EXPERIENCES_CATALOG[2];
  const royale = EXPERIENCES_CATALOG.find((e) => e.id === 'atelier_botanique') || EXPERIENCES_CATALOG[3];

  switch (intent) {
    case 'tarifs': {
      const phone = OFFICIAL_PHONE_NUMBERS.DIRECTION;
      if (lang === 'en') {
        const waMsg = `Hello EcoPark Cameroun, Concierge inquiry regarding Park & QR Passes (${cleanQuery || 'FCFA rates'}).`;
        return {
          intent,
          lang,
          headline: 'Official Park, Pool & All-Inclusive Pass Rates (FCFA)',
          body: 'All tickets are issued in XAF (FCFA) with free admission for children under 3 years old and a 30% group discount starting at 20 guests:',
          bullets: [
            `Park & Zoo Entry (Gorilla ToTo): ${formatFcfa(zoo.adultPrice)} adult / ${formatFcfa(zoo.childPrice)} child`,
            `Discovery Pass (Zoo + Canoe + Horseback): ${formatFcfa(decouverte.adultPrice)} adult / ${formatFcfa(decouverte.childPrice)} child`,
            `Full-Day Pass (Zoo + Supervised Pool + Canoe): ${formatFcfa(complete.adultPrice)} adult / ${formatFcfa(complete.childPrice)} child`,
            `Royal Pass (Zoo + Pool + Canoe + Hot Meal): ${formatFcfa(royale.adultPrice)} adult / ${formatFcfa(royale.childPrice)} child`,
          ],
          navAction: {
            label: 'Book a QR Pass Online',
            targetView: 'billetterie',
          },
          whatsappLabel: 'Confirm via WhatsApp Desk',
          whatsappPhone: phone,
          whatsappUrl: getWhatsAppUrl(phone, waMsg),
        };
      }

      const waMsg = `Bonjour EcoPark Cameroun, suite à mon échange avec le Concierge Virtuel, je souhaite réserver un Pass ou vérifier les tarifs (${cleanQuery || 'grille FCFA'}).`;
      return {
        intent,
        lang,
        headline: 'Grille officielle Parc, Piscine & Pass Coupe-File QR',
        body: "Tous nos tarifs sont nets en FCFA (gratuit avant 3 ans, remise de -30 % dès 20 participants sur l'entrée parc) :",
        bullets: [
          `Entrée Parc & Jardin Zoologique (Gorille ToTo) : ${formatFcfa(zoo.adultPrice)} adulte / ${formatFcfa(zoo.childPrice)} enfant`,
          `Pass Découverte Nature (Zoo + Pirogue + Cheval) : ${formatFcfa(decouverte.adultPrice)} adulte / ${formatFcfa(decouverte.childPrice)} enfant`,
          `Pass Journée Complète (Zoo + Piscine + Pirogue) : ${formatFcfa(complete.adultPrice)} adulte / ${formatFcfa(complete.childPrice)} enfant`,
          `Pass Journée Royale (Activités + Repas complet) : ${formatFcfa(royale.adultPrice)} adulte / ${formatFcfa(royale.childPrice)} enfant`,
        ],
        navAction: {
          label: 'Réserver mon Pass QR',
          targetView: 'billetterie',
        },
        whatsappLabel: 'Poursuivre sur WhatsApp Billetterie',
        whatsappPhone: phone,
        whatsappUrl: getWhatsAppUrl(phone, waMsg),
      };
    }

    case 'hotels': {
      const phone = OFFICIAL_PHONE_NUMBERS.HOTEL;
      if (lang === 'en') {
        const waMsg = `Hello EcoPark Hotel Desk, Concierge availability check for our stay at Ahala (${cleanQuery || 'hotel booking'}).`;
        return {
          intent,
          lang,
          headline: '24/7 Hotel Residences & VIP Suites at Ahala (30 Units)',
          body: 'Our hotel reception welcomes guests 24/7 with check-in from 2:00 PM, check-out until 11:00 AM, backup power and guarded parking:',
          bullets: [
            'Cité Bene (Nature Rooms): 10 000 to 15 000 FCFA / night',
            'Cité Chanthel (Comfort Pavilions): 15 000 to 25 000 FCFA / night',
            'Hôtel Ewondo (VIP Mini-Suites, AC & hot water): 25 000 to 30 000 FCFA / night',
            'Ewondo Prestige VIP Suites: 30 000 to 45 000 FCFA / night (Couple Escape Pack: 45 000 FCFA / 1 night or 70 000 FCFA / 2 nights with breakfast & activities)',
          ],
          navAction: {
            label: 'Explore the 4 Hotel Residences',
            targetView: 'accueil',
            showcaseTab: 'hebergements',
            anchorId: 'ahala-production-showcase',
          },
          whatsappLabel: 'Check Room Availability (24/7 WhatsApp)',
          whatsappPhone: phone,
          whatsappUrl: getWhatsAppUrl(phone, waMsg),
        };
      }

      const waMsg = `Bonjour Réception Hôtels EcoPark, via le Concierge Virtuel, je souhaite vérifier la disponibilité d'un hébergement à Ahala (${cleanQuery || 'séjour hôtelier'}).`;
      return {
        intent,
        lang,
        headline: 'Les 4 gammes hôtelières ouvertes 24h/24 (30 unités à Ahala)',
        body: "Notre réception hôtelière vous accueille 24h/24 et 7j/7 (arrivée dès 14h00, départ jusqu'à 11h00, parking sécurisé gratuit) :",
        bullets: [
          'Cité Bene (Chambres Nature) : 10 000 à 15 000 FCFA / nuit',
          'Cité Chanthel (Pavillons Confort) : 15 000 à 25 000 FCFA / nuit',
          'Hôtel Ewondo (Mini-Suites VIP climatisées) : 25 000 à 30 000 FCFA / nuit',
          'Suites Prestige VIP Ewondo : 30 000 à 45 000 FCFA / nuit (Pack Escapade Couple VIP : 45 000 FCFA / 1 nuit ou 70 000 FCFA / 2 nuits avec petit-déjeuner, piscine et pirogue)',
        ],
        navAction: {
          label: 'Voir les 4 cités hôtelières',
          targetView: 'accueil',
          showcaseTab: 'hebergements',
          anchorId: 'ahala-production-showcase',
        },
        whatsappLabel: 'Vérifier les disponibilités (WhatsApp Hôtels)',
        whatsappPhone: phone,
        whatsappUrl: getWhatsAppUrl(phone, waMsg),
      };
    }

    case 'evenements': {
      const phone = OFFICIAL_PHONE_NUMBERS.DIRECTION;
      if (lang === 'en') {
        const waMsg = `Hello EcoPark Events Desk, Concierge quote request for a group, school trip or Menkii 500-seat hall (${cleanQuery || 'event quote'}).`;
        return {
          intent,
          lang,
          headline: 'Menkii 500-Seat Conference Hall, Seminars & School Trips',
          body: 'ECOPARK hosts corporate seminars, diplomatic receptions, weddings and school excursions with dedicated catering and backup power:',
          bullets: [
            'Menkii Essomba Anton Hall: 500 seated places, HD projection, sound system & generator',
            'Corporate Seminar Package: from 15 000 FCFA / participant (hall, coffee break, lunch & relaxation)',
            'School Excursions: Park entry from 500 FCFA / student or educational package at 1 350 FCFA / student (1 free teacher per 10 students)',
            'Groups of 20+ visitors: automatic 30% discount on adult park admission',
          ],
          navAction: {
            label: 'View Group & Seminar Packages',
            targetView: 'accueil',
            showcaseTab: 'entreprise',
            anchorId: 'ahala-production-showcase',
          },
          whatsappLabel: 'Request a Proforma Quote on WhatsApp',
          whatsappPhone: phone,
          whatsappUrl: getWhatsAppUrl(phone, waMsg),
        };
      }

      const waMsg = `Bonjour Direction EcoPark, via le Concierge Virtuel, je souhaite un devis Groupe, École ou Salle Menkii 500 places (${cleanQuery || 'devis événement'}).`;
      return {
        intent,
        lang,
        headline: 'Salle Menkii (500 places), Séminaires & Sorties scolaires',
        body: 'Nous accompagnons les entreprises, ministères, ONG, écoles et familles avec groupe électrogène de secours et service traiteur intégré :',
        bullets: [
          'Salle Polyvalente Menkii Essomba Anton : 500 places assises, sonorisation et vidéoprojection HD',
          'Forfait Séminaire Entreprises : dès 15 000 FCFA / participant (salle, pause-café, déjeuner et détente)',
          'Sorties scolaires : entrée parc dès 500 FCFA / élève ou forfait pédagogique complet à 1 350 FCFA / élève (1 encadrant gratuit pour 10 élèves)',
          'Groupes constitués (20+ pers.) : remise immédiate de -30 % sur l\'entrée adulte',
        ],
        navAction: {
          label: 'Consulter l\'offre Groupes & Salle 500 pl.',
          targetView: 'accueil',
          showcaseTab: 'entreprise',
          anchorId: 'ahala-production-showcase',
        },
        whatsappLabel: 'Demander un devis sur WhatsApp',
        whatsappPhone: phone,
        whatsappUrl: getWhatsAppUrl(phone, waMsg),
      };
    }

    case 'restaurant': {
      const phone = OFFICIAL_PHONE_NUMBERS.DIRECTION;
      if (lang === 'en') {
        const waMsg = `Hello EcoPark Restaurant, Concierge table or pergola booking at Le Château des Saveurs (${cleanQuery || 'table reservation'}).`;
        return {
          intent,
          lang,
          headline: 'Gastronomy at Le Château des Saveurs (Open 7/7, 7 AM - 11 PM)',
          body: 'Enjoy authentic Cameroonian cuisine and fresh fish harvested from our Ahala ponds, served in the dining room or lakeside boukarous:',
          bullets: [
            'Fresh Braised Fish from Ahala Ponds: 5 000 FCFA',
            'Royal Poulet DG with Ripe Plantains: 6 500 FCFA',
            'Royal Ndolé (Shrimp & Beef): 4 500 FCFA',
            'Boukarou Grill Platter: 3 500 FCFA • Kids Menu: 2 500 FCFA • Private Lakeside Pergola available',
          ],
          navAction: {
            label: 'See Menu & Dining Spaces',
            targetView: 'accueil',
            showcaseTab: 'saveurs',
            anchorId: 'ahala-production-showcase',
          },
          whatsappLabel: 'Reserve a Table or Pergola on WhatsApp',
          whatsappPhone: phone,
          whatsappUrl: getWhatsAppUrl(phone, waMsg),
        };
      }

      const waMsg = `Bonjour EcoPark Cameroun, via le Concierge Virtuel, je souhaite réserver une table ou une pergola au restaurant Le Château des Saveurs (${cleanQuery || 'réservation table'}).`;
      return {
        intent,
        lang,
        headline: 'Restaurant « Le Château des Saveurs » (7j/7 de 07h00 à 23h00)',
        body: "Savourez nos spécialités camerounaises et le poisson frais issu des étangs d'Ahala, en salle climatisée ou sous les boukarous au bord de l'eau :",
        bullets: [
          "Poisson braisé frais des étangs d'Ahala : 5 000 FCFA",
          'Poulet DG Royal au plantain mûr : 6 500 FCFA',
          'Ndolé Royal crevettes et bœuf : 4 500 FCFA',
          'Grillades boukarous : 3 500 FCFA • Menu Enfant : 2 500 FCFA • Pergola privée sur pilotis sur réservation',
        ],
        navAction: {
          label: 'Voir la carte du Château des Saveurs',
          targetView: 'accueil',
          showcaseTab: 'saveurs',
          anchorId: 'ahala-production-showcase',
        },
        whatsappLabel: 'Réserver une table sur WhatsApp',
        whatsappPhone: phone,
        whatsappUrl: getWhatsAppUrl(phone, waMsg),
      };
    }

    case 'cfp': {
      const phone = OFFICIAL_PHONE_NUMBERS.DIRECTION;
      if (lang === 'en') {
        const waMsg = `Hello CFP EcoPark MINEFOP, Concierge request for the enrollment file (${cleanQuery || 'CFP admission'}).`;
        return {
          intent,
          lang,
          headline: 'CFP ECOPARK Vocational Center (Accredited by MINEFOP)',
          body: 'Train directly on a real hospitality, culinary and aquaculture campus over 12 months (DQP / CQP national diplomas, minimum age 16):',
          bullets: [
            '5 accredited tracks: Hospitality & Lodging, Culinary Arts, Event Decoration, Agropastoral Production, Fish Farming & Aquaculture',
            'Registration fee: 50 000 FCFA',
            'Annual tuition: 250 000 FCFA payable in 4 installments',
            'Hands-on practice inside ECOPARK hotels, restaurant and fish ponds',
          ],
          navAction: {
            label: 'Explore the 5 CFP MINEFOP Tracks',
            targetView: 'accueil',
            showcaseTab: 'formation',
            anchorId: 'ahala-production-showcase',
          },
          whatsappLabel: 'Request Admission File via WhatsApp',
          whatsappPhone: phone,
          whatsappUrl: getWhatsAppUrl(phone, waMsg),
        };
      }

      const waMsg = `Bonjour CFP EcoPark MINEFOP, via le Concierge Virtuel, je souhaite recevoir le dossier d'inscription (${cleanQuery || 'admission CFP'}).`;
      return {
        intent,
        lang,
        headline: 'Centre de Formation Professionnelle CFP ECOPARK (agréé MINEFOP)',
        body: "Formez-vous en 12 mois (diplômes d'État DQP / CQP, dès 16 ans) avec travaux pratiques réels sur nos hôtels, nos cuisines et nos étangs piscicoles :",
        bullets: [
          '5 filières qualifiantes : Hôtellerie & Hébergement, Restauration & Art Culinaire, Décoration & Événementiel, Production Agropastorale, Pisciculture & Aquaculture',
          'Frais d\'inscription : 50 000 FCFA',
          'Scolarité annuelle : 250 000 FCFA payable en 4 tranches souples',
        ],
        navAction: {
          label: 'Découvrir les 5 filières CFP MINEFOP',
          targetView: 'accueil',
          showcaseTab: 'formation',
          anchorId: 'ahala-production-showcase',
        },
        whatsappLabel: 'Recevoir le dossier CFP sur WhatsApp',
        whatsappPhone: phone,
        whatsappUrl: getWhatsAppUrl(phone, waMsg),
      };
    }

    case 'acces': {
      const phone = OFFICIAL_PHONE_NUMBERS.STANDARD;
      if (lang === 'en') {
        const waMsg = `Hello EcoPark Cameroun, Concierge inquiry about directions, shuttle or opening hours (${cleanQuery || 'Ahala access'}).`;
        return {
          intent,
          lang,
          headline: 'Location on RN3, Opening Hours, Shuttle & 90-Day Weather Guarantee',
          body: 'ECOPARK CAMEROUN is located 15 minutes from downtown Yaoundé via a 100% paved road:',
          bullets: [
            'Address: Ahala Barrière district, directly across from Tradex Ahala gas station (National Road N3), free guarded parking 24/7',
            'Hours: Park & Leisure Tuesday to Sunday 09:00 - 18:00 (Monday biological rest) • Hotels open 24/7 • Restaurant open 7/7 (07:00 - 23:00)',
            'Air-conditioned round-trip shuttle (Yaoundé - Ahala): 1 500 FCFA adult / 1 000 FCFA child',
            'RN3 Weather Guarantee: free 90-day date reschedule in case of heavy tropical rain, or free cancellation 48h prior',
          ],
          navAction: {
            label: 'Open Interactive Map & Circuits',
            targetView: 'sentiers',
          },
          whatsappLabel: 'Get GPS Pin & Shuttle Info on WhatsApp',
          whatsappPhone: phone,
          whatsappUrl: getWhatsAppUrl(phone, waMsg),
        };
      }

      const waMsg = `Bonjour EcoPark Cameroun, via le Concierge Virtuel, je souhaite un renseignement sur l'accès RN3, la navette ou les horaires (${cleanQuery || 'accès Ahala'}).`;
      return {
        intent,
        lang,
        headline: 'Itinéraire RN3, Horaires, Navette & Garantie Météo 90 jours',
        body: 'Le complexe est accessible en 15 minutes depuis le centre de Yaoundé par une route 100 % goudronnée :',
        bullets: [
          'Repère exact : Quartier Ahala Barrière, juste en face de la station-service Tradex Ahala (RN3), grand parking gratuit surveillé 24h/24',
          'Horaires : Parc & Loisirs du mardi au dimanche de 09h00 à 18h00 (repos biologique le lundi) • Hôtels 24h/24 • Restaurant 7j/7 (07h00 à 23h00)',
          'Navette climatisée aller-retour Yaoundé - Ahala : 1 500 FCFA adulte / 1 000 FCFA enfant',
          'Garantie Météo RN3 : report 100 % gratuit de votre Pass QR valable 90 jours en cas de forte pluie tropicale',
        ],
        navAction: {
          label: 'Ouvrir le plan interactif',
          targetView: 'sentiers',
        },
        whatsappLabel: 'Recevoir la position sur WhatsApp',
        whatsappPhone: phone,
        whatsappUrl: getWhatsAppUrl(phone, waMsg),
      };
    }

    case 'paiement': {
      const phone = OFFICIAL_PHONE_NUMBERS.DIRECTION;
      if (lang === 'en') {
        const waMsg = `Hello EcoPark Cameroun, Concierge assistance for Mobile Money or group payment (${cleanQuery || 'payment'}).`;
        return {
          intent,
          lang,
          headline: 'Mobile Money, Cash & Offline-Ready QR Tickets',
          body: 'Book in 2 minutes and keep your personal QR Pass accessible on your phone even during network drops:',
          bullets: [
            'Accepted methods: Orange Money Cameroon, MTN Mobile Money, FCFA cash at the Ahala gate, or bank transfer for corporate bookings',
            'Instant personal QR code (ECP-2026-XXXXX) for priority gate entry without queue',
            'CEMAC visitors & diaspora: WhatsApp assistance available for cross-border Mobile Money or group proforma',
          ],
          navAction: {
            label: 'Generate My QR Pass Now',
            targetView: 'billetterie',
          },
          whatsappLabel: 'Payment Assistance on WhatsApp',
          whatsappPhone: phone,
          whatsappUrl: getWhatsAppUrl(phone, waMsg),
        };
      }

      const waMsg = `Bonjour EcoPark Cameroun, via le Concierge Virtuel, j'ai besoin d'une assistance règlement Mobile Money ou virement (${cleanQuery || 'paiement'}).`;
      return {
        intent,
        lang,
        headline: 'Règlement Mobile Money, Guichet FCFA & Billet QR hors ligne',
        body: 'Votre réservation génère immédiatement un Pass QR nominatif consultable même en cas de baisse de réseau mobile :',
        bullets: [
          "Moyens acceptés : Orange Money (#150#), MTN Mobile Money (*126#), espèces FCFA au guichet d'Ahala ou virement bancaire entreprises",
          'File prioritaire coupe-file au poste RN3 avec votre code ECP-2026-XXXXX',
          'Visiteurs zone CEMAC et diaspora : assistance directe sur WhatsApp pour vos réservations groupes et séjours',
        ],
        navAction: {
          label: 'Émettre mon Pass QR maintenant',
          targetView: 'billetterie',
        },
        whatsappLabel: 'Assistance règlement sur WhatsApp',
        whatsappPhone: phone,
        whatsappUrl: getWhatsAppUrl(phone, waMsg),
      };
    }

    case 'avis': {
      const phone = OFFICIAL_PHONE_NUMBERS.DIRECTION;
      if (lang === 'en') {
        const waMsg = `Hello EcoPark Management, Guest Feedback submitted via Virtual Concierge: "${cleanQuery || 'Visit feedback'}".`;
        return {
          intent,
          lang,
          headline: 'Guest Experience & Priority Management Follow-Up',
          body: 'Thank you for sharing your feedback! Every guest review helps Dr Christophe FOE NDI and our teams keep Ahala welcoming and safe:',
          bullets: [
            'Compliments are shared directly with our park rangers, hotel reception and kitchen brigade',
            'Any service concern is escalated with priority to General Management for rapid resolution',
            'Click below to send your detailed note directly to the Management WhatsApp line',
          ],
          whatsappLabel: 'Send My Review to Management (WhatsApp)',
          whatsappPhone: phone,
          whatsappUrl: getWhatsAppUrl(phone, waMsg),
        };
      }

      const waMsg = `Bonjour Direction EcoPark, retour d'expérience visiteur transmis via le Concierge Virtuel : « ${cleanQuery || 'Avis client'} ».`;
      return {
        intent,
        lang,
        headline: 'Écoute Visiteurs & Suivi Qualité Direction',
        body: "Merci pour votre retour d'expérience ! Chaque avis est pris en compte par nos équipes d'Ahala pour élever la qualité d'accueil :",
        bullets: [
          'Vos encouragements sont transmis aux équipes du Parc, du Château des Saveurs et des Cités Hôtelières',
          "Toute remarque ou insatisfaction bénéficie d'un suivi prioritaire auprès de la Direction d'exploitation",
          'Transmettez votre message complet en 1 clic sur la ligne directe Direction ci-dessous',
        ],
        whatsappLabel: 'Transmettre mon avis à la Direction (WhatsApp)',
        whatsappPhone: phone,
        whatsappUrl: getWhatsAppUrl(phone, waMsg),
      };
    }

    case 'general':
    default: {
      const phone = OFFICIAL_PHONE_NUMBERS.DIRECTION;
      if (lang === 'en') {
        const waMsg = `Hello EcoPark Cameroun, I have a question via the Virtual Concierge: "${cleanQuery || 'General inquiry'}".`;
        return {
          intent: 'general',
          lang,
          headline: 'Your 5-Pole Eco-Tourism & Hospitality Complex in Yaoundé - Ahala',
          body: 'Here are the key highlights of ECOPARK CAMEROUN (across from Tradex Ahala, RN3) while I connect you to the right service:',
          bullets: [
            'Leisure & Zoo: Entry from 500 FCFA child / 1 000 FCFA adult • All-inclusive QR Passes from 2 500 to 8 500 FCFA',
            '24/7 Hotels & Dining: 30 rooms & VIP suites (10 000 to 45 000 FCFA/night) • Le Château des Saveurs open 7/7',
            'Events & Vocational Campus: 500-seat Menkii Hall • CFP accredited by MINEFOP (5 tracks)',
          ],
          navAction: {
            label: 'Book Tickets or Plan My Visit',
            targetView: 'billetterie',
          },
          whatsappLabel: 'Chat with a Human Advisor on WhatsApp',
          whatsappPhone: phone,
          whatsappUrl: getWhatsAppUrl(phone, waMsg),
        };
      }

      const waMsg = `Bonjour EcoPark Cameroun, j'ai une demande via le Concierge Virtuel : « ${cleanQuery || 'Renseignement général'} ».`;
      return {
        intent: 'general',
        lang,
        headline: 'Les 5 pôles ECOPARK CAMEROUN à votre service (Yaoundé - Ahala)',
        body: "Voici l'essentiel pour préparer votre venue en face de la station Tradex Ahala (RN3), ou basculer vers un conseiller humain :",
        bullets: [
          'Parc, Zoo & Piscine : entrée dès 500 FCFA enfant / 1 000 FCFA adulte • Pass QR Tout-Inclus de 2 500 à 8 500 FCFA',
          'Hôtels 24h/24 & Gastronomie : 30 chambres et suites VIP (10 000 à 45 000 FCFA/nuit) • Restaurant Le Château des Saveurs 7j/7',
          'Événements & Formation : Salle Menkii de 500 places • CFP agréé MINEFOP (5 filières qualifiantes)',
        ],
        navAction: {
          label: 'Accéder à la billetterie QR',
          targetView: 'billetterie',
        },
        whatsappLabel: 'Parler à un conseiller sur WhatsApp',
        whatsappPhone: phone,
        whatsappUrl: getWhatsAppUrl(phone, waMsg),
      };
    }
  }
}
