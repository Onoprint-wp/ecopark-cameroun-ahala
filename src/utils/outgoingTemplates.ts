/**
 * ECOPARK CAMEROUN - Centralisation et Assainissement des Modèles Sortants (G5)
 *
 * Ce module centralise l'ensemble des coordonnées officielles, générateurs d'URL
 * et modèles de messages sortants (notamment WhatsApp wa.me) pour garantir :
 * - 0 coquille d'élision
 * - 0 tiret long (\u2014 / \u2013)
 * - 0 caractère d'encodage dégradé
 * - Un routage strict vers les 3 lignes téléphoniques officielles agréées
 */

import { sanitizeEditorialText } from './editorialSanitizer.ts';

/**
 * Numéros de téléphone officiels du complexe EcoPark Cameroun
 */
export const OFFICIAL_PHONE_NUMBERS = {
  /** Direction générale, Accueil général, Billetterie, Restaurant, Groupes, CFP MINEFOP */
  DIRECTION: '+237 672 56 45 98',
  /** Pôle Hôtelier, Réservations Cités Hôtelières et Suites Prestige VIP */
  HOTEL: '+237 694 60 14 49',
  /** Standard officiel et renseignements généraux (agents.txt / llms.txt) */
  STANDARD: '+237 697 13 62 03',
} as const;

/**
 * Chiffres stricts au format international E.164 sans séparateur
 */
export const OFFICIAL_PHONE_DIGITS = {
  DIRECTION: '237672564598',
  HOTEL: '237694601449',
  STANDARD: '237697136203',
} as const;

/**
 * Liste des numéros autorisés sous forme de tableau
 */
export const AUTHORIZED_PHONE_DIGITS: readonly string[] = [
  OFFICIAL_PHONE_DIGITS.DIRECTION,
  OFFICIAL_PHONE_DIGITS.HOTEL,
  OFFICIAL_PHONE_DIGITS.STANDARD,
] as const;

/**
 * Normalise une chaîne téléphonique pour n'extraire que les chiffres
 */
export function normalizePhoneToDigits(phone: string): string {
  if (!phone) return '';
  return phone.replace(/\D/g, '');
}

/**
 * Vérifie si un numéro donné correspond à l'un des 3 numéros officiels autorisés
 */
export function isValidOfficialPhoneNumber(phone: string): boolean {
  const digits = normalizePhoneToDigits(phone);
  return AUTHORIZED_PHONE_DIGITS.includes(digits);
}

/**
 * Modèles pré-remplis officiels de messages sortants WhatsApp
 */
export const OUTGOING_WHATSAPP_TEMPLATES = {
  /** Billetterie et accueil général */
  TICKETING_RESERVATION:
    "Bonjour EcoPark Cameroun, je souhaite réserver une visite ou un Pass à Ahala.",
  PRICING_INQUIRY:
    "Bonjour EcoPark Cameroun, je souhaite un renseignement sur les tarifs d'Ahala.",

  /** Gastronomie - Restaurant Le Château des Saveurs */
  RESTAURANT_TABLE:
    "Bonjour EcoPark Cameroun, je souhaite réserver une table au restaurant Le Château des Saveurs.",

  /** Pôle Hôtelier et Suites VIP */
  HOTEL_ESCAPE_COUPLE:
    "Bonjour EcoPark Cameroun, je souhaite réserver le Pack Escapade Couple VIP (45 000 FCFA) ou une chambre à Ahala.",
  HOTEL_ROOM_GENERAL:
    "Bonjour EcoPark Cameroun, je souhaite réserver une chambre ou une suite à Ahala.",

  /** Séminaires, Groupes et Événements B2B */
  GROUP_SCHOOL_EXCURSION:
    "Bonjour EcoPark Cameroun, je souhaite un devis Excursion Scolaire (1 350 FCFA / élève).",
  GROUP_CORPORATE_SEMINAR:
    "Bonjour EcoPark Cameroun, nous souhaitons organiser un Séminaire Entreprises (15 000 FCFA / participant).",
  GROUP_HALL_PRIVATIZATION:
    "Bonjour EcoPark Cameroun, je souhaite privatiser la Salle Polyvalente Menkii Essomba Anton (500 places).",

  /** Centre de Formation Professionnelle CFP MINEFOP */
  CFP_ADMISSION_FILE:
    "Bonjour CFP EcoPark MINEFOP, je souhaite recevoir le dossier d'inscription (50 000 FCFA + 4 tranches).",

  /** Services complémentaires (Cross-Sell Ahala) */
  CROSS_SELL_SHUTTLE:
    "Bonjour EcoPark Cameroun, je souhaite réserver la Navette Climatisée Aller-Retour (1 500 FCFA Ad. / 1 000 FCFA Enf.).",
  CROSS_SELL_PERGOLA:
    "Bonjour EcoPark Cameroun, je souhaite réserver une Pergola Privée sur Pilotis (+5 000 FCFA) au Château des Saveurs.",
  CROSS_SELL_FEEDING:
    "Bonjour EcoPark Cameroun, nous souhaitons ajouter des Sachets de Nourrissage (500 FCFA) à notre visite.",
  CROSS_SELL_NURSERY:
    "Bonjour EcoPark Cameroun, je souhaite réserver une place en Halte-Garderie Sécurisée à Ahala.",
} as const;

/**
 * Construit le message pré-rempli de commande d'un Pass Tout-Inclus
 */
export function buildPassOrderMessage(
  passName: string,
  childPrice: number | string,
  adultPrice: number | string
): string {
  return sanitizeEditorialText(
    `Bonjour EcoPark Cameroun, je souhaite commander le ${passName} (${childPrice} FCFA enf. / ${adultPrice} FCFA ad.).`
  );
}

/**
 * Construit le message pré-rempli de vérification de disponibilité hôtelière
 */
export function buildHotelAvailabilityMessage(
  hotelName: string,
  priceRange: string
): string {
  return sanitizeEditorialText(
    `Bonjour EcoPark Cameroun, je souhaite vérifier la disponibilité : ${hotelName} (${priceRange})`
  );
}

/**
 * Construit une URL de contact WhatsApp wa.me sécurisée, assainie et encodée.
 *
 * @param recipientNumber Numéro destinataire (+237... ou 237...)
 * @param messageText Message textuel pré-rempli
 * @returns URL wa.me complète prête pour les liens href
 */
export function getWhatsAppUrl(
  recipientNumber: string,
  messageText: string = ''
): string {
  const cleanDigits = normalizePhoneToDigits(recipientNumber);

  // Par défaut sur la Direction si numéro invalide ou absent
  const targetDigits = AUTHORIZED_PHONE_DIGITS.includes(cleanDigits)
    ? cleanDigits
    : OFFICIAL_PHONE_DIGITS.DIRECTION;

  if (!messageText) {
    return `https://wa.me/${targetDigits}`;
  }

  const sanitized = sanitizeEditorialText(messageText);
  return `https://wa.me/${targetDigits}?text=${encodeURIComponent(sanitized)}`;
}
