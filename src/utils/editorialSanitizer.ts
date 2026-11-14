/**
 * ECOPARK CAMEROUN - Module de Gouvernance Éditoriale & Assainissement des Saisies Dynamiques (G1)
 *
 * Règles d'hygiène éditoriale :
 * - Remplacement automatique des tirets cadratin (\u2014) et demi-cadratin (\u2013) par le tiret standard (-).
 * - Normalisation des espaces multiples et suppression des espaces superflus en début/fin.
 * - Détection proactive des infractions (tirets longs, clichés IA, jargon banni, élisions sans apostrophe).
 * - Modèles pré-approuvés de motifs de fermeture et de résolution de terrain.
 */

/**
 * Modèles pré-approuvés officiels pour les motifs de fermeture de sentiers
 */
export const CLOSURE_REASON_TEMPLATES: readonly string[] = [
  "Accès réservé aux résidents des Cités Hôtelières Ewondo, Chanthel et Bene",
  "Privatisation événementielle : Salle Polyvalente Menkii Essomba Anton (500 places)",
  "Travaux pratiques d'alevinage en cours avec les apprenants du CFP MINEFOP",
  "Repos biologique hebdomadaire du lundi et maintenance préventive des bassins",
  "Entretien des berges du lac d'Ahala et contrôle des gilets de sauvetage",
  "Restauration écologique du biotope et suivi vétérinaire de la faune",
] as const;

/**
 * Modèles pré-approuvés officiels pour les notes d'intervention de terrain
 */
export const RESOLUTION_NOTE_TEMPLATES: readonly string[] = [
  "Équipe sentiers intervenue ce matin : obstacle débité et évacué.",
  "Balisage consolidé et platelage refixé avec vis inox.",
  "Observation enregistrée dans le registre biologique officiel de la réserve.",
  "Nettoyage et évacuation des déchets effectués lors de la patrouille.",
  "Intervention de terrain validée par l'équipe technique.",
] as const;

/**
 * Liste des clichés d'écriture artificielle (IA) strictement proscrits
 */
export const BANNED_AI_CLICHES: readonly string[] = [
  'au cœur d',
  'au coeur d',
  'dans un monde où',
  'dans un monde ou',
  'il est important de noter',
  'catalyseur',
  'révolutionner',
  'incontournable',
  'véritable levier',
  'plongeons dans',
] as const;

/**
 * Liste des termes de jargon technique et anglicismes bannis de l'interface publique
 */
export const BANNED_JARGON_TERMS: readonly string[] = [
  'Onboarding',
  'PBKDF2-HMAC-SHA256',
  'Day-Use',
  'Best-Seller',
  'Espace Cliente',
  'Compte Cliente',
] as const;

/**
 * Patterns d'élisions françaises sans apostrophe fréquentes
 */
const UNELIDED_FRENCH_PATTERNS: readonly RegExp[] = [
  /\b([djlmnstc]|qu)\s+(ahala|entrée|eau|alevinage|évaluation|hôtel|hébergement|aujourd|accès|ombrage|ombre|intervention|équipe|éco-garde|expérience|activité|accueil|observation|urgence|apprentissage|option|un|une|autre|autres)\b/i,
  /\b(vient|venait)\s+d\s+être\b/i,
  /\baujourd\s+hui\b/i,
];

/**
 * Nettoie une saisie utilisateur ou dynamique selon les règles de gouvernance éditoriale.
 * - Remplace les tirets longs (\u2014 et \u2013) par le tiret standard (-).
 * - Normalise les espaces multiples en un seul espace.
 * - Supprime les espaces au début et à la fin.
 *
 * @param input Texte brut à nettoyer
 * @returns Texte normalisé et assaini
 */
export function sanitizeEditorialText(input: string | null | undefined): string {
  if (typeof input !== 'string' || !input) {
    return '';
  }

  return input
    .replace(/[\u2014\u2013]/g, '-')
    .replace(/[\u00A0\u200B\u202F\uFEFF]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

/**
 * Détecte les infractions aux règles éditoriales sur une chaîne donnée.
 *
 * @param input Texte à auditer
 * @returns Tableau des libellés des infractions détectées (vide si conforme)
 */
export function detectEditorialViolations(input: string | null | undefined): string[] {
  if (typeof input !== 'string' || !input) {
    return [];
  }

  const violations: string[] = [];

  // 1. Détection des tirets longs (cadratin / demi-cadratin)
  if (/[\u2014\u2013]/.test(input)) {
    violations.push('Présence de tiret long interdit (cadratin \\u2014 ou demi-cadratin \\u2013)');
  }

  // 2. Détection d'encodage corrompu (mojibake UTF-8 / replacement char)
  if (/[\uFFFD]|\u00C3[\u0080-\u00BF]/.test(input)) {
    violations.push('Caractère d\'encodage corrompu détecté');
  }

  // 3. Détection des clichés IA
  const lower = input.toLowerCase();
  for (const cliche of BANNED_AI_CLICHES) {
    if (lower.includes(cliche.toLowerCase())) {
      violations.push(`Cliché IA proscrit détecté : « ${cliche} »`);
    }
  }

  // 4. Détection du jargon banni
  for (const jargon of BANNED_JARGON_TERMS) {
    if (input.includes(jargon)) {
      violations.push(`Jargon ou anglicisme banni détecté : « ${jargon} »`);
    }
  }

  // 5. Détection des élisions françaises sans apostrophe
  for (const pattern of UNELIDED_FRENCH_PATTERNS) {
    if (pattern.test(input)) {
      violations.push('Élision française sans apostrophe détectée');
      break;
    }
  }

  return violations;
}

/**
 * Vérifie si un texte respecte l'ensemble des règles éditoriales
 *
 * @param input Texte à vérifier
 * @returns true si le texte ne contient aucune violation
 */
export function isEditorialCompliant(input: string | null | undefined): boolean {
  return detectEditorialViolations(input).length === 0;
}
