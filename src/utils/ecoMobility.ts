// ============================================================================
// ECO-MOBILITY & CARBON ENGINE (src/utils/ecoMobility.ts)
// ============================================================================

import { ExperienceType, MobilityMode } from '../types/ecosystem';

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
    label: 'Vélo & Mobilité Douce',
    shortLabel: 'Vélo / Douce',
    description: 'Arrivée à vélo classique, VAE ou à pied depuis les gares et véloroutes.',
    discountPercent: 30,
    co2AvoidedKgPerPerson: 10.5,
    iconName: 'Bike',
    carbonBadge: '-30% · 10.5 kg CO₂ évités / pers.',
    ademeNote: 'Empreinte 0 g CO₂eq/km — Borne de recharge solaire et consigne gratuites sur place.',
    highlight: true,
  },
  {
    id: 'train',
    label: 'Train Régional TER',
    shortLabel: 'Train TER',
    description: 'Ligne alpine avec arrêt direct en gare du Parc. Billet combiné SNCF / ECO-PARK.',
    discountPercent: 25,
    co2AvoidedKgPerPerson: 8.4,
    iconName: 'Train',
    carbonBadge: '-25% · 8.4 kg CO₂ évités / pers.',
    ademeNote: 'Émissions TER : ~2.4 g CO₂eq/voyageur-km contre ~193 g pour une voiture thermique.',
    highlight: true,
  },
  {
    id: 'navette_electrique',
    label: 'Navette Électrique du Parc',
    shortLabel: 'Navette Électrique',
    description: 'Navette 100% électrique alimentée par la ferme solaire de la réserve forestière.',
    discountPercent: 20,
    co2AvoidedKgPerPerson: 6.2,
    iconName: 'Bus',
    carbonBadge: '-20% · 6.2 kg CO₂ évités / pers.',
    ademeNote: 'Navette intercommunale cadencée toutes les 20 min depuis les parkings relais aval.',
  },
  {
    id: 'covoiturage',
    label: 'Covoiturage (3 pers. minimum)',
    shortLabel: 'Covoiturage (≥3)',
    description: 'Arrivée groupée à 3 passagers ou plus dans un même véhicule partagé.',
    discountPercent: 10,
    co2AvoidedKgPerPerson: 4.1,
    iconName: 'Users',
    carbonBadge: '-10% · 4.1 kg CO₂ évités / pers.',
    ademeNote: 'Division par 3 des émissions de circulation et réduction de l occupation des sols de stationnement.',
  },
  {
    id: 'voiture_solo',
    label: 'Voiture Individuelle Thermique',
    shortLabel: 'Voiture Solo',
    description: 'Véhicule personnel standard thermique (sans partage de trajet).',
    discountPercent: 0,
    co2AvoidedKgPerPerson: 0,
    iconName: 'Car',
    carbonBadge: '0% réduction · 0 kg CO₂ évité',
    ademeNote: 'Tarif plein sans bonus écologique. Contribution carbone intégrée aux actions de reforestation.',
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
    title: 'Accès Libre aux 6 Sentiers',
    badge: 'Formule Découverte',
    description: 'Accès illimité aux 6 sentiers balisés, points de vue et aires d observation ornithologiques.',
    adultPrice: 12,
    childPrice: 6,
    pmrPrice: 6,
    features: [
      'Accès aux 6 parcours de la réserve',
      'Carte vectorielle et profil altimétrique',
      'Accès libre aux observatoires faune',
    ],
  },
  {
    id: 'eco_guide',
    title: 'Sortie Naturaliste avec Éco-Garde',
    badge: 'Immersion Faune & Flore',
    description: 'Sortie de 3 heures en petit groupe (max 12 pers.) guidée par un garde-forestier certifié.',
    adultPrice: 24,
    childPrice: 14,
    pmrPrice: 14,
    features: [
      'Guidage spécialisé par un éco-garde',
      'Longues-vues Swarovski fournies',
      'Identification empreintes & chants d oiseaux',
    ],
  },
  {
    id: 'atelier_botanique',
    title: 'Atelier Botanique & Herbier Vivant',
    badge: 'Pédagogie & Savoirs',
    description: 'Session immersive d identification des plantes médicinales et endémiques avec confection d un herbier numérique.',
    adultPrice: 28,
    childPrice: 16,
    pmrPrice: 16,
    features: [
      'Atelier 2h30 au rucher et jardin conservatoire',
      'Kit loupe de terrain inclus',
      'Accès aux fiches de l Atlas taxonomique',
    ],
  },
  {
    id: 'pack_mobilite',
    title: 'Pack Mobilité Douce + Vélo Solaire',
    badge: 'Tout-en-un Bas Carbone',
    description: 'Billet combiné incluant la mise à disposition d un vélo à assistance solaire et accès sentiers VTT.',
    adultPrice: 18,
    childPrice: 10,
    pmrPrice: 10,
    features: [
      'Location VAE solaire 1 demi-journée',
      'Accès aux pistes cyclables balisées',
      'Casque et sacoche étanche fournis',
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

  // If covoiturage is selected with fewer than 3 guests, reduce discount to 0 with explanation
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

  const discountAmountEur = Number(((grossTotalEur * actualDiscountPercent) / 100).toFixed(2));
  const netTotalEur = Number(Math.max(0, grossTotalEur - discountAmountEur).toFixed(2));
  const unitPriceEur = Number((netTotalEur / totalGuests).toFixed(2));

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

export function formatEur(amount: number): string {
  return amount.toLocaleString('fr-FR', {
    style: 'currency',
    currency: 'EUR',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });
}

export function formatCo2(kg: number): string {
  return `${kg.toLocaleString('fr-FR', { minimumFractionDigits: 1, maximumFractionDigits: 1 })} kg CO₂`;
}
