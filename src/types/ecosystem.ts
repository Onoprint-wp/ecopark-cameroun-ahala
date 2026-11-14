// ============================================================================
// ECO-PARK DOMAIN CONTRACTS (src/types/ecosystem.ts)
// ============================================================================

export type ActiveView =
  | 'accueil'
  | 'sentiers'
  | 'biodiversite'
  | 'billetterie'
  | 'pass'
  | 'ranger'
  | 'connexion'
  | 'legal'
  | 'color_atlas';

export type EcoParkRole =
  | 'visiteur_anonyme'
  | 'client_connecte'
  | 'agent_guichet'
  | 'agent_controle'
  | 'comptable'
  | 'responsable_exploitation'
  | 'direction'
  | 'administrateur_plateforme';

export type AssignedPole =
  | 'GUICHET_CAISSE'
  | 'CONTROLE_QR'
  | 'HEBERGEMENT'
  | 'CUISINE_SAVEURS'
  | 'FINANCE_COMPTA'
  | 'DIRECTION_GENERALE';

export interface AuthenticatedUser {
  id: string;
  email: string;
  fullName: string;
  phone: string;
  role: EcoParkRole;
  matricule?: string;
  assignedPole?: AssignedPole;
  postLabel?: string;
  provider: 'supabase' | 'webcrypto_pbkdf2';
  createdAt: string;
}

export type ThemeMode = 'auto' | 'light' | 'dark';
export type EffectiveTheme = 'light' | 'dark';
export type DaltonismMode = 'normal' | 'deuteranopia' | 'protanopia' | 'tritanopia';

export type TrailStatus = 'fluide' | 'balise' | 'ferme';
export type TrailDifficulty = 'tres_facile' | 'facile' | 'moyen' | 'difficile' | 'expert' | 'sportif';
export type BiomeType =
  | 'canopee'
  | 'cretes'
  | 'marais'
  | 'sous_bois'
  | 'geologie'
  | 'vallon'
  | 'foret_primaire'
  | 'crete_rocheuse'
  | 'zone_humide'
  | 'vallee_ombragee';

export interface MapCoordinate {
  x: number; // SVG viewBox coordinate (0-1000)
  y: number; // SVG viewBox coordinate (0-700)
}

export interface ElevationPoint {
  distanceKm: number;    // Distance from departure in km
  elevationM: number;    // Elevation in meters
  slopePercent?: number; // Instantaneous slope percentage
  poiId?: string;        // Optional linked POI ID
  poiLabel?: string;     // Short landmark label
  mapCoord: MapCoordinate; // Geographic coordinate mapped on SVG map
}

export type POICategory =
  | 'park_entrance'
  | 'water'
  | 'bird_blind'
  | 'solar_bike'
  | 'ranger_post'
  | 'viewpoint'
  | 'lookout'
  | 'shelter'
  | 'bike';

export interface PointOfInterest {
  id: string;
  category: POICategory;
  categoryLabel: string;
  name: string;
  description: string;
  altitudeM: number;
  coordinates: MapCoordinate;
  trailIds: string[];
  iconName: string;
  services?: string[];
}

export interface Trail {
  id: string;                      // e.g. 'canopee' or 't-1'
  slug: string;
  name: string;                    // e.g. "Sentier de la Canopée Ancienne"
  subtitle: string;
  description: string;
  difficulty: TrailDifficulty;
  lengthKm: number;
  distanceKm?: number;             // Alias for lengthKm
  durationMin: number;
  elevationGainM: number;
  minElevationM: number;
  maxElevationM: number;
  pmrAccessible: boolean;
  biome: BiomeType;
  biomeLabel: string;
  status: TrailStatus;             // Controlled dynamically by Ranger
  closureReason?: string;          // e.g. "Nidification du Faucon Pèlerin"
  currentOccupancy: number;        // Live headcount on this trail
  maxCapacity: number;             // Carrying capacity
  elevationProfile: ElevationPoint[];
  mapPath: string;                 // SVG path definition `d="M... C..."`
  svgPath?: string;                // Alias for mapPath
  startPoint: MapCoordinate;
  endPoint: MapCoordinate;
  poiCoordinates: {
    id: string;
    name: string;
    type: POICategory;
    coord: MapCoordinate;
  }[];
  featuredSpeciesIds: string[];    // Links to endemic species atlas
  associatedSpeciesIds?: string[]; // Alias
  associatedPoiIds?: string[];
}

export type SpeciesCategory =
  | 'faune'
  | 'flore'
  | 'avifaune'
  | 'herpetofaune'
  | 'oiseaux'
  | 'mammiferes'
  | 'amphibiens'
  | 'insectes';

export type ConservationStatus = 'LC' | 'NT' | 'VU' | 'EN' | 'CR'; // IUCN Red List

export interface Species {
  id: string;                      // e.g. 'sp-1'
  commonName: string;              // e.g. "Chouette de Tengmalm"
  scientificName: string;          // e.g. "Aegolius funereus"
  category: SpeciesCategory;
  categoryLabel: string;
  iucnStatus: ConservationStatus;
  iucnLabel: string;
  observationSeason: ('Printemps' | 'Été' | 'Automne' | 'Hiver')[];
  bestTime: string;                // e.g. "Crépuscule & Nuit"
  trailIds: string[];              // Associated trails where spotted
  description: string;
  habitat: string;
  dietOrFloraType: string;
  protectionCharter: string;
  sightingsCount: number;
  iconName: string;
  identificationTips?: string[];
  fieldIndices?: string;
  ecoRangerGuideline?: string;
  photoUrl?: string;
}

export type ExperienceType =
  | 'sentiers'
  | 'eco_guide'
  | 'atelier_botanique'
  | 'pack_mobilite';

export type TimeSlot =
  | '08h30 - 11h30'
  | '09h00 - 12h00'
  | '11h30 - 14h30'
  | '12h00 - 15h00'
  | '14h30 - 17h30'
  | '15h00 - 18h00'
  | '17h30 - 20h00';

export type MobilityMode =
  | 'train'
  | 'navette_electrique'
  | 'velo'
  | 'covoiturage'
  | 'voiture_solo';

export interface EcoPass {
  id: string;                      // e.g. "ECO-2026-8942-XF"
  createdAt: string;               // ISO 8601
  visitDate: string;               // YYYY-MM-DD
  timeSlot: TimeSlot;
  experienceType: ExperienceType;
  guestCount: number;
  adultCount?: number;
  childCount?: number;
  pmrCount?: number;
  mobilityMode: MobilityMode;
  co2AvoidedKg: number;
  discountAppliedPercent: number;
  unitPriceEur: number;
  totalPriceEur: number;
  leadVisitor: {
    fullName: string;
    email: string;
    phone: string;
  };
  ownerUserId?: string;
  ownerEmail?: string;
  zeroTraceCharterSigned: boolean;
  qrPayload: string;               // Deterministic token encoded in the QR SVG
  status: 'confirmed' | 'checked_in' | 'cancelled';
  checkInTimestamp?: string;
}

export type BookingInput = Omit<EcoPass, 'id' | 'createdAt' | 'qrPayload' | 'status'>;

export type CitizenReportType =
  | 'faune_rare'
  | 'flore_remarquable'
  | 'obstacle_sentier'
  | 'dechet_incivisme'
  | 'danger_meteo';

export type ReportSeverity = 'info' | 'mineur' | 'modere' | 'critique';
export type ReportStatus = 'en_attente' | 'valide' | 'rejete' | 'resolu';

export interface CitizenReport {
  id: string;                      // e.g. "REP-2026-041"
  timestamp: string;               // ISO 8601
  type: CitizenReportType;
  title: string;
  description: string;
  trailId: string;
  landmark: string;                // e.g. "Borne 4B, 300m après la passerelle"
  severity: ReportSeverity;
  status: ReportStatus;            // Governed by Ranger console
  reporterName: string;            // e.g. "Lucas M. (Sentinelle #412)"
  upvotes: number;
  rangerNote?: string;             // Action taken by ranger team
  resolvedAt?: string;
}

export type ReportInput = Omit<CitizenReport, 'id' | 'timestamp' | 'status' | 'upvotes'>;

export interface ParkTelemetry {
  dailyCapacityMax: number;        // Configured by Ranger (e.g. 1500)
  currentOccupancy: number;        // Sum of checked-in + booked today
  airQualityIqa: number;           // e.g. 18 (0-100, 18 = "Très bon")
  airQualityStatus: 'Très Bon' | 'Bon' | 'Moyen' | 'Dégradé';
  temperatureC: number;            // e.g. 21°C
  weatherCondition: string;        // e.g. "Ensoleillé · Microclimat forestier"
  humidityPercent: number;         // e.g. 64%
  solarAutonomyPercent: number;    // e.g. 94%
  totalCo2AvoidedKg: number;       // e.g. 4280 kg
}

export interface ThemeContextType {
  themeMode: ThemeMode;
  effectiveTheme: EffectiveTheme;
  setThemeMode: (mode: ThemeMode) => void;
  daltonismMode: DaltonismMode;
  setDaltonismMode: (mode: DaltonismMode) => void;
  highContrastOutdoor: boolean;
  setHighContrastOutdoor: (enabled: boolean) => void;
}

export interface EcoParkContextType {
  // Navigation & View
  activeView: ActiveView;
  setActiveView: (view: ActiveView) => void;

  // Theming & Vision (Mirroring or directly accessible)
  themeMode: ThemeMode;
  effectiveTheme: EffectiveTheme;
  setThemeMode: (mode: ThemeMode) => void;
  daltonismMode: DaltonismMode;
  setDaltonismMode: (mode: DaltonismMode) => void;
  colorDrawerOpen: boolean;
  setColorDrawerOpen: (open: boolean) => void;
  highContrastOutdoor: boolean;
  setHighContrastOutdoor: (enabled: boolean) => void;

  // Telemetry & Capacity
  telemetry: ParkTelemetry;
  setDailyCapacity: (newCap: number) => void;

  // Trails
  trails: Trail[];
  updateTrailStatus: (trailId: string, status: TrailStatus, closureReason?: string) => void;
  selectedTrailId: string | null;
  setSelectedTrailId: (trailId: string | null) => void;

  // Points of interest
  pois: PointOfInterest[];

  // Species
  species: Species[];
  selectedSpeciesId: string | null;
  setSelectedSpeciesId: (speciesId: string | null) => void;

  // Bookings & Passes
  passes: EcoPass[];
  activePass: EcoPass | null;
  activePassId: string | null;
  setActivePassId: (id: string | null) => void;
  sessionUnlockedPassIds: string[];
  bookPass: (input: BookingInput) => EcoPass;
  cancelPass: (passId: string) => void;
  checkInPass: (passId: string) => void;
  lookupPassAnonymously: (
    referenceCode: string,
    contactEmailOrPhone: string
  ) => { ok: boolean; error?: string; pass?: EcoPass };
  claimPassByReference: (
    referenceCode: string,
    contactEmailOrPhone: string,
    userId: string,
    userEmail: string
  ) => { ok: boolean; error?: string; pass?: EcoPass };
  anonymizeUserPasses: (userId: string, userEmail: string) => number;

  // Citizen Sentinel
  reports: CitizenReport[];
  submitCitizenReport: (input: ReportInput) => CitizenReport;
  updateReportStatus: (reportId: string, status: ReportStatus, rangerNote?: string) => void;
  upvoteReport: (reportId: string) => void;

  // Reset to initial seed
  resetToSeedData: () => void;
}
