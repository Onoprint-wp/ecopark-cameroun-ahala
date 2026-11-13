// ============================================================================
// ECOPARK CAMEROUN (YAOUNDÉ – AHALA) — OFFICIAL PRICING & ACCESS ENGINE
// (src/utils/ecoMobility.ts)
// ============================================================================

import type { ExperienceType, MobilityMode } from '../types/ecosystem.ts';

export interface MobilityOption {
  id: MobilityMode;
  label: string;
  shortLabel: string;
  description: string;
  discountPercent: number;
  co2AvoidedKgPerPerson: number;
  iconName: string;
  carbonBadge: string;
  ademeNote: string;
  highlight?: boolean;
}

export const MOBILITY_OPTIONS: MobilityOption[] = [
  {
    id: 'velo',
    label: 'Tarif Groupe Constitué (20+ pers.) & Associations',
    shortLabel: 'Groupe 20+ (-30%)',
    description:
      'Remise officielle de -30% dès 20 participants (Entrée Adulte à 700 FCFA au lieu de 1 000 FCFA) pour familles nombreuses, associations et comités.',
    discountPercent: 30,
    co2AvoidedKgPerPerson: 6.5,
    iconName: 'Bike',
    carbonBadge: '-30% Groupe (dès 20 pers.)',
    ademeNote: 'Avantage officiel EcoPark Ahala : Entrée Adulte ramenée à 700 FCFA (Enfant : 500 FCFA).',
    highlight: true,
  },
  {
    id: 'train',
    label: 'Prévente Orange Money (#150#) / MTN MoMo (*126#)',
    shortLabel: 'Orange Money / MTN MoMo',
    description:
      'Réservation mobile avec émission immédiate du Pass QR Code (ECP-2026-XXXXX) et file prioritaire sans attente au guichet d Ahala.',
    discountPercent: 0,
    co2AvoidedKgPerPerson: 4.2,
    iconName: 'Train',
    carbonBadge: 'Coupe-File QR · Garantie Météo 90j',
    ademeNote: 'Garantie Météo RN3 incluse : report 100 % gratuit pendant 90 jours ou remboursement Mobile Money ≥ 48h.',
    highlight: true,
  },
  {
    id: 'navette_electrique',
    label: 'Navette Climatisée EcoPark (Yaoundé ↔ Ahala)',
    shortLabel: 'Navette Climatisée',
    description:
      'Liaison aller-retour depuis Yaoundé en navette climatisée (5, 18 ou 32 places) : 1 500 FCFA A/R adulte · 1 000 FCFA A/R enfant.',
    discountPercent: 0,
    co2AvoidedKgPerPerson: 5.8,
    iconName: 'Bus',
    carbonBadge: 'Navette A/R : 1 500 FCFA Ad. / 1 000 FCFA Enf.',
    ademeNote: 'Transport collectif sécurisé jusqu à l entrée d Ahala Barrière (en face de la station Tradex, RN3).',
  },
  {
    id: 'covoiturage',
    label: 'Véhicule Famille RN3 (Parking Gratuit Face Tradex)',
    shortLabel: 'Parking Gratuit RN3',
    description:
      'Accès direct par route 100 % goudronnée (RN3, à 15 min du centre-ville de Yaoundé) avec grand parking gratuit sécurisé en face de la station Tradex Ahala.',
    discountPercent: 0,
    co2AvoidedKgPerPerson: 3.1,
    iconName: 'Users',
    carbonBadge: 'Parking 100% Gratuit & Sécurisé',
    ademeNote: 'Stationnement gratuit sous surveillance 24h/24 pour les visiteurs du parc, du restaurant et des hôtels.',
  },
  {
    id: 'voiture_solo',
    label: 'Paiement Espèces au Guichet d Ahala Barrière',
    shortLabel: 'Espèces au Guichet',
    description:
      'Pré-enregistrement de votre Pass QR Code en ligne et règlement en espèces (FCFA) directement à la caisse principale à votre arrivée.',
    discountPercent: 0,
    co2AvoidedKgPerPerson: 1.5,
    iconName: 'Car',
    carbonBadge: 'Règlement FCFA sur place',
    ademeNote: 'Guichet ouvert du Mardi au Dimanche de 09h00 à 18h00 (Réception Hôtels & Restaurant ouverte 7j/7).',
  },
];

export interface ExperiencePricingDefinition {
  id: ExperienceType;
  title: string;
  badge: string;
  description: string;
  adultPrice: number;
  childPrice: number;
  pmrPrice: number;
  features: string[];
}

export const EXPERIENCES_CATALOG: ExperiencePricingDefinition[] = [
  {
    id: 'sentiers',
    title: 'Entrée Parc & Jardin Zoologique Seul',
    badge: 'Tarif Officiel Guichet',
    description:
      'Accès aux allées botaniques ombragées, au Jardin Zoologique (Gorille « ToTo », chimpanzés, tortues) et aux espaces de détente au bord du lac.',
    adultPrice: 1000,
    childPrice: 500,
    pmrPrice: 500,
    features: [
      'Jardin Zoologique (Gorille ToTo, chimpanzés, tortues)',
      'Promenade sous les allées forestières & bord du lac',
      'Gratuit (0 FCFA) pour les tout-petits de moins de 3 ans',
    ],
  },
  {
    id: 'eco_guide',
    title: 'Pass Découverte Nature (Zoo + Pirogue + Cheval)',
    badge: 'Formule Tout-Inclus #1',
    description:
      'Formule combinée idéale en famille réunissant les 3 activités nature incontournables d EcoPark Cameroun avec un seul QR Code.',
    adultPrice: 2500,
    childPrice: 1500,
    pmrPrice: 1500,
    features: [
      'Entrée Parc & Jardin Zoologique complet',
      'Balade en Pirogue sur le lac (45 min, gilet fourni)',
      'Balade à cheval & initiation au manège équestre',
    ],
  },
  {
    id: 'pack_mobilite',
    title: 'Pass Journée Complète (Zoo + Piscine + Pirogue)',
    badge: 'Formule Tout-Inclus #2 · Best-Seller',
    description:
      'Accès privilégié combinant la découverte zoologique, la traversée du lac en pirogue et la baignade dans la piscine semi-olympique surveillée.',
    adultPrice: 4500,
    childPrice: 2500,
    pmrPrice: 2500,
    features: [
      'Entrée Parc & Jardin Zoologique (Gorille ToTo)',
      'Accès Piscine Semi-Olympique surveillée par maîtres-nageurs',
      'Balade en Pirogue de 45 min sur le lac d Ahala',
    ],
  },
  {
    id: 'atelier_botanique',
    title: 'Pass Journée Royale (Zoo + Piscine + Pirogue + Repas)',
    badge: 'Formule VIP Tout-Inclus #3',
    description:
      'L expérience royale complète à Yaoundé-Ahala incluant toutes les activités phares ainsi qu un repas gastronomique au restaurant « Le Château des Saveurs ».',
    adultPrice: 8500,
    childPrice: 4500,
    pmrPrice: 4500,
    features: [
      'Zoo + Piscine Semi-Olympique + Balade en Pirogue',
      'Repas chaud inclus au restaurant « Le Château des Saveurs »',
      'Accès prioritaire coupe-file aux embarcadères & bassins',
    ],
  },
];

export interface PricingBreakdown {
  experienceType: ExperienceType;
  mobilityMode: MobilityMode;
  adultCount: number;
  childCount: number;
  pmrCount: number;
  totalGuests: number;
  adultBaseTotal: number;
  childBaseTotal: number;
  pmrBaseTotal: number;
  grossTotalEur: number;
  discountPercent: number;
  discountAmountEur: number;
  netTotalEur: number;
  unitPriceEur: number;
  co2AvoidedPerPersonKg: number;
  totalCo2AvoidedKg: number;
  mobilityInfo: MobilityOption;
  experienceInfo: ExperiencePricingDefinition;
}

export function calculateEcoMobilityPricing(
  experienceType: ExperienceType,
  mobilityMode: MobilityMode,
  adultCount: number = 1,
  childCount: number = 0,
  pmrCount: number = 0
): PricingBreakdown {
  const experienceInfo =
    EXPERIENCES_CATALOG.find((exp) => exp.id === experienceType) || EXPERIENCES_CATALOG[0];

  const mobilityInfo =
    MOBILITY_OPTIONS.find((opt) => opt.id === mobilityMode) || MOBILITY_OPTIONS[0];

  const totalGuests = Math.max(1, adultCount + childCount + pmrCount);

  let actualDiscountPercent = mobilityInfo.discountPercent;
  let actualCo2Avoided = mobilityInfo.co2AvoidedKgPerPerson;
  if (mobilityMode === 'covoiturage' && totalGuests < 3) {
    actualDiscountPercent = 0;
    actualCo2Avoided = 1.5;
  }

  const adultBaseTotal = adultCount * experienceInfo.adultPrice;
  const childBaseTotal = childCount * experienceInfo.childPrice;
  const pmrBaseTotal = pmrCount * experienceInfo.pmrPrice;
  const grossTotalEur = adultBaseTotal + childBaseTotal + pmrBaseTotal;

  const discountAmountEur = Math.round((grossTotalEur * actualDiscountPercent) / 100);
  const netTotalEur = Math.max(0, grossTotalEur - discountAmountEur);
  const unitPriceEur = Math.round(netTotalEur / totalGuests);

  const totalCo2AvoidedKg = Number((actualCo2Avoided * totalGuests).toFixed(1));

  return {
    experienceType,
    mobilityMode,
    adultCount,
    childCount,
    pmrCount,
    totalGuests,
    adultBaseTotal,
    childBaseTotal,
    pmrBaseTotal,
    grossTotalEur,
    discountPercent: actualDiscountPercent,
    discountAmountEur,
    netTotalEur,
    unitPriceEur,
    co2AvoidedPerPersonKg: actualCo2Avoided,
    totalCo2AvoidedKg,
    mobilityInfo,
    experienceInfo,
  };
}

export function getExperienceInfo(experienceType: ExperienceType): ExperiencePricingDefinition {
  return EXPERIENCES_CATALOG.find((exp) => exp.id === experienceType) || EXPERIENCES_CATALOG[0];
}

export function resolveExperienceForTrail(trailId: string | null | undefined): ExperienceType {
  switch (trailId) {
    case 'marais':
      return 'pack_mobilite';
    case 'roches-moussues':
      return 'eco_guide';
    case 'piste-eco-gardes':
      return 'atelier_botanique';
    case 'canopee':
    case 'vallee-fougeres':
    case 'cretes-cedres':
    default:
      return 'sentiers';
  }
}

export function formatEur(amount: number): string {
  return `${Math.round(amount).toLocaleString('fr-FR')} FCFA`;
}

export function formatCo2(kg: number): string {
  return `${kg.toLocaleString('fr-FR', { minimumFractionDigits: 1, maximumFractionDigits: 1 })} kg CO₂`;
}
