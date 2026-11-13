// ============================================================================
// CITIZEN SENTINEL FIELD FORM & COMMUNITY FEED (src/components/field/CitizenSentinel.tsx)
// Features F24 & F25: Participative field reporting and live observation feed
// ============================================================================

import React, { useState, useMemo, useEffect } from 'react';
import {
  ShieldAlert,
  MapPin,
  Camera,
  ThumbsUp,
  CheckCircle2,
  AlertTriangle,
  Clock,
  Send,
  Eye,
  Flower2,
  Trash2,
  CloudRain,
  Compass,
  Check,
  Sparkles,
} from 'lucide-react';
import { useEcoPark } from '../../context/EcoParkContext';
import {
  CitizenReportType,
  ReportSeverity,
  ReportStatus,
  ReportInput,
} from '../../types/ecosystem';

export const CitizenSentinel: React.FC = () => {
  const {
    reports,
    trails,
    selectedTrailId: globalSelectedTrailId,
    setSelectedTrailId: setGlobalSelectedTrailId,
    setActiveView,
    submitCitizenReport,
    upvoteReport,
  } = useEcoPark();

  // Active view tab: Form (F24) vs Feed (F25)
  const [activeTab, setActiveTab] = useState<'form' | 'feed'>('form');

  // Form states (F24) — synced with global selectedTrailId when navigated from Map / Atlas
  const [selectedTrailId, setSelectedTrailId] = useState<string>(
    globalSelectedTrailId || (trails.length > 0 ? trails[0].id : 'canopee')
  );
  const [reportType, setReportType] = useState<CitizenReportType>('faune_rare');

  useEffect(() => {
    if (globalSelectedTrailId && trails.some((t) => t.id === globalSelectedTrailId)) {
      setSelectedTrailId(globalSelectedTrailId);
    }
  }, [globalSelectedTrailId, trails]);
  const [severity, setSeverity] = useState<ReportSeverity>('info');
  const [title, setTitle] = useState<string>('');
  const [description, setDescription] = useState<string>('');
  const [landmark, setLandmark] = useState<string>('');
  const [reporterName, setReporterName] = useState<string>('Sentinelle #' + Math.floor(100 + Math.random() * 900));

  // Simulated GPS Coordinates (Yaoundé – Ahala Barrière, RN3)
  const [gpsCoordinates, setGpsCoordinates] = useState<string>('[GPS 3.792° N, 11.488° E - Alt. 725m · Ahala RN3]');
  const [gpsRefreshing, setGpsRefreshing] = useState<boolean>(false);
  const [gpsPulseKey, setGpsPulseKey] = useState<number>(0);

  // Simulated Photo Attachment
  const [selectedPhotoPreset, setSelectedPhotoPreset] = useState<string>('photo-faune-1');

  // Form validation & submission feedback
  const [formErrors, setFormErrors] = useState<Record<string, string>>({});
  const [submittedReportId, setSubmittedReportId] = useState<string | null>(null);
  const [lastCreatedReportId, setLastCreatedReportId] = useState<string | null>(null);

  // Feed filtering states (F25)
  const [feedCategoryFilter, setFeedCategoryFilter] = useState<string>('all');
  const [feedTrailFilter, setFeedTrailFilter] = useState<string>('all');
  const [feedStatusFilter, setFeedStatusFilter] = useState<string>('all');

  // Photo presets with realistic descriptions at Yaoundé-Ahala
  const PHOTO_PRESETS = [
    {
      id: 'photo-faune-1',
      title: 'Animation au Sanctuaire du Gorille « ToTo »',
      meta: 'Jardin Zoologique d Ahala · Soigneur présent',
      accent: '#52B788',
    },
    {
      id: 'photo-obstacle-1',
      title: 'Palme tombée près de l embarcadère des pirogues',
      meta: 'Quai du lac d Ahala · Intervention entretien',
      accent: '#D48359',
    },
    {
      id: 'photo-flore-1',
      title: 'Récolte bio sur la parcelle CFP MINEFOP',
      meta: 'Ferme-école Agroécologie · Légumes du Château des Saveurs',
      accent: '#357A5B',
    },
    {
      id: 'photo-meteo-1',
      title: 'Averse tropicale passagère sur la Piscine Semi-Olympique',
      meta: 'Bassin sécurisé par les maîtres-nageurs',
      accent: '#E63946',
    },
  ];

  // Refresh GPS Simulation
  const refreshGpsLocation = () => {
    setGpsRefreshing(true);
    setTimeout(() => {
      const lat = (3.788 + Math.random() * 0.008).toFixed(3);
      const lon = (11.484 + Math.random() * 0.008).toFixed(3);
      const alt = Math.floor(710 + Math.random() * 50);
      setGpsCoordinates(`[GPS ${lat}° N, ${lon}° E - Alt. ${alt}m · Ahala RN3]`);
      setGpsRefreshing(false);
      setGpsPulseKey((prev) => prev + 1);
    }, 400);
  };

  // Helper icons for categories
  const renderCategoryIcon = (type: CitizenReportType, className: string = 'w-4 h-4') => {
    switch (type) {
      case 'faune_rare':
        return <Eye className={className} />;
      case 'flore_remarquable':
        return <Flower2 className={className} />;
      case 'obstacle_sentier':
        return <AlertTriangle className={className} />;
      case 'danger_meteo':
        return <CloudRain className={className} />;
      case 'dechet_incivisme':
        return <Trash2 className={className} />;
    }
  };

  const getCategoryLabel = (type: CitizenReportType): string => {
    switch (type) {
      case 'faune_rare':
        return 'Faune Remarquable';
      case 'flore_remarquable':
        return 'Flore Protégée';
      case 'obstacle_sentier':
        return 'Obstacle Sentier';
      case 'danger_meteo':
        return 'Risque Météo';
      case 'dechet_incivisme':
        return 'Dégradation / Déchets';
    }
  };

  // Status Badge Helper
  const renderStatusBadge = (status: ReportStatus) => {
    switch (status) {
      case 'valide':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-[11px] font-semibold bg-emerald-100 text-emerald-800 dark:bg-emerald-950/80 dark:text-emerald-300 border border-emerald-300 dark:border-emerald-800">
            <CheckCircle2 className="w-3 h-3 text-emerald-600 dark:text-emerald-400" />
            Vérifié par Éco-Garde
          </span>
        );
      case 'resolu':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-[11px] font-semibold bg-teal-100 text-teal-800 dark:bg-teal-950/80 dark:text-teal-300 border border-teal-300 dark:border-teal-800">
            <Check className="w-3 h-3 text-teal-600 dark:text-teal-400" />
            Résolu sur le Terrain
          </span>
        );
      case 'en_attente':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-[11px] font-semibold bg-amber-100 text-amber-800 dark:bg-amber-950/80 dark:text-amber-300 border border-amber-300 dark:border-amber-800">
            <Clock className="w-3 h-3 text-amber-600 dark:text-amber-400" />
            Reçu · En cours d évaluation
          </span>
        );
      case 'rejete':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-[11px] font-semibold bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300 border border-gray-300 dark:border-gray-700">
            Non retenu
          </span>
        );
    }
  };

  // Severity Badge Helper
  const renderSeverityBadge = (sev: ReportSeverity) => {
    switch (sev) {
      case 'critique':
        return (
          <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-red-100 text-red-800 dark:bg-red-950 dark:text-red-300 border border-red-300 dark:border-red-800 uppercase">
            Critique
          </span>
        );
      case 'modere':
        return (
          <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300 border border-amber-300 dark:border-amber-800 uppercase">
            Modéré
          </span>
        );
      case 'mineur':
        return (
          <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-yellow-100 text-yellow-800 dark:bg-yellow-950 dark:text-yellow-300 border border-yellow-300 dark:border-yellow-800 uppercase">
            Mineur
          </span>
        );
      case 'info':
        return (
          <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-blue-100 text-blue-800 dark:bg-blue-950 dark:text-blue-300 border border-blue-300 dark:border-blue-800 uppercase">
            Info
          </span>
        );
    }
  };

  // Submit Handler
  const handleSubmitReport = (e: React.FormEvent) => {
    e.preventDefault();
    const errors: Record<string, string> = {};

    if (!title.trim()) {
      errors.title = 'Veuillez renseigner un intitulé précis.';
    }
    if (!description.trim()) {
      errors.description = 'Une description détaillée est requise pour guider les gardes.';
    }
    if (!landmark.trim()) {
      errors.landmark = 'Précisez un repère visuel (borne, passerelle, virage).';
    }

    if (Object.keys(errors).length > 0) {
      setFormErrors(errors);
      return;
    }

    setFormErrors({});

    const reportInput: ReportInput = {
      type: reportType,
      trailId: selectedTrailId,
      severity,
      title: title.trim(),
      description: `${description.trim()} — ${gpsCoordinates}`,
      landmark: landmark.trim(),
      reporterName: reporterName.trim() || 'Sentinelle Anonyme',
    };

    const newReport = submitCitizenReport(reportInput);
    setSubmittedReportId(newReport.id);
    setLastCreatedReportId(newReport.id);

    // Reset fields
    setTitle('');
    setDescription('');
    setLandmark('');

    // Switch to feed after sonar echo completes
    setTimeout(() => {
      setSubmittedReportId(null);
      setActiveTab('feed');
    }, 1650);
  };

  // Filtered feed computation (F25)
  const filteredReports = useMemo(() => {
    return reports.filter((r) => {
      if (feedCategoryFilter !== 'all' && r.type !== feedCategoryFilter) {
        return false;
      }
      if (feedTrailFilter !== 'all' && r.trailId !== feedTrailFilter) {
        return false;
      }
      if (feedStatusFilter !== 'all' && r.status !== feedStatusFilter) {
        return false;
      }
      return true;
    });
  }, [reports, feedCategoryFilter, feedTrailFilter, feedStatusFilter]);

  return (
    <div className="space-y-6">
      {/* Tab Navigation & Statistics Banner */}
      <div className="p-4 sm:p-6 rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-default)] shadow-xs flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <ShieldAlert className="w-5 h-5 text-[var(--brand-primary)]" />
            <h2 className="font-['Barlow_Semi_Condensed'] text-xl sm:text-2xl font-bold text-[var(--text-primary)]">
              Sentinelle Nature &amp; Veille Participative
            </h2>
          </div>
          <p className="text-xs text-[var(--text-muted)] mt-1">
            Les randonneurs contribuent en direct à la cartographie de la biodiversité et au signalement des incidents sur les sentiers.
          </p>
        </div>

        {/* Tab Buttons */}
        <div className="flex items-center gap-1.5 p-1 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)] shrink-0">
          <button
            onClick={() => setActiveTab('form')}
            className={`px-4 py-2 rounded-lg text-xs font-bold transition-all cursor-pointer flex items-center gap-1.5 ${
              activeTab === 'form'
                ? 'bg-[var(--brand-primary)] text-white shadow-xs'
                : 'text-[var(--text-primary)] hover:bg-[var(--bg-surface)]'
            }`}
          >
            <Send className="w-3.5 h-3.5" />
            <span>Nouveau Signalement</span>
          </button>

          <button
            onClick={() => setActiveTab('feed')}
            className={`px-4 py-2 rounded-lg text-xs font-bold transition-all cursor-pointer flex items-center gap-1.5 ${
              activeTab === 'feed'
                ? 'bg-[var(--brand-primary)] text-white shadow-xs'
                : 'text-[var(--text-primary)] hover:bg-[var(--bg-surface)]'
            }`}
          >
            <Eye className="w-3.5 h-3.5" />
            <span>Observations Communauté ({reports.length})</span>
          </button>
        </div>
      </div>

      {/* =================================================================== */}
      {/* VUE A : FORMULAIRE DE SIGNALEMENT TERRAIN (F24)                     */}
      {/* =================================================================== */}
      {activeTab === 'form' && (
        <form onSubmit={handleSubmitReport} className="space-y-6">
          {submittedReportId && (
            <div className="p-5 rounded-2xl bg-emerald-50 dark:bg-emerald-950/80 border border-emerald-400 dark:border-emerald-700 text-emerald-950 dark:text-emerald-100 flex items-center gap-4 shadow-md overflow-hidden relative">
              <div className="relative w-11 h-11 rounded-full bg-emerald-600/15 flex items-center justify-center shrink-0">
                <span
                  aria-hidden="true"
                  className="eco-sonar-wave absolute inset-0 rounded-full border-2 border-emerald-500/70"
                />
                <span
                  aria-hidden="true"
                  style={{ animationDelay: '260ms' }}
                  className="eco-sonar-wave absolute inset-0 rounded-full border border-emerald-400/60"
                />
                <MapPin className="w-5 h-5 text-emerald-700 dark:text-emerald-300 eco-pin-drop relative z-10" />
              </div>
              <div>
                <h4 className="font-bold text-sm flex items-center gap-2">
                  <span>Signalement {submittedReportId} émis par onde sonar aux Éco-Gardes !</span>
                </h4>
                <p className="text-xs text-emerald-800 dark:text-emerald-200 mt-0.5">
                  Coordonnées {gpsCoordinates} verrouillées. Ouverture du fil communautaire...
                </p>
              </div>
            </div>
          )}

          {/* Category Pill Radio */}
          <div className="p-6 rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-default)] space-y-4">
            <h3 className="font-['Barlow_Semi_Condensed'] text-base font-bold text-[var(--text-primary)]">
              1. Type d observation constatée sur le terrain
            </h3>

            <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
              {[
                { id: 'faune_rare' as CitizenReportType, label: 'Faune Rare', icon: Eye },
                { id: 'flore_remarquable' as CitizenReportType, label: 'Flore Protégée', icon: Flower2 },
                { id: 'obstacle_sentier' as CitizenReportType, label: 'Obstacle Sentier', icon: AlertTriangle },
                { id: 'danger_meteo' as CitizenReportType, label: 'Risque Météo', icon: CloudRain },
                { id: 'dechet_incivisme' as CitizenReportType, label: 'Incivisme / Déchets', icon: Trash2 },
              ].map((cat) => {
                const isSelected = reportType === cat.id;
                const Icon = cat.icon;
                return (
                  <button
                    key={cat.id}
                    type="button"
                    onClick={() => setReportType(cat.id)}
                    className={`p-3.5 rounded-xl border text-center transition-all cursor-pointer flex flex-col items-center justify-center gap-2 ${
                      isSelected
                        ? 'bg-[var(--bg-elevated)] border-[var(--brand-primary)] ring-2 ring-[var(--brand-primary)]/20 shadow-xs'
                        : 'bg-[var(--bg-canvas)] border-[var(--border-default)] hover:border-[var(--brand-primary)]/50'
                    }`}
                  >
                    <Icon
                      className={`w-5 h-5 ${
                        isSelected ? 'text-[var(--brand-primary)]' : 'text-[var(--text-muted)]'
                      }`}
                    />
                    <span
                      className={`text-xs font-semibold ${
                        isSelected ? 'text-[var(--brand-primary)] font-bold' : 'text-[var(--text-primary)]'
                      }`}
                    >
                      {cat.label}
                    </span>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Trail & Location Coordinates */}
          <div className="p-6 rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-default)] space-y-4">
            <h3 className="font-['Barlow_Semi_Condensed'] text-base font-bold text-[var(--text-primary)]">
              2. Localisation précise sur le tracé
            </h3>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold text-[var(--text-primary)] mb-1.5">
                  Sentier concerné *
                </label>
                <select
                  value={selectedTrailId}
                  onChange={(e) => setSelectedTrailId(e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)] text-xs text-[var(--text-primary)] focus:outline-none focus:ring-1 focus:ring-[var(--brand-primary)] cursor-pointer"
                >
                  {trails.map((t) => (
                    <option key={t.id} value={t.id}>
                      {t.name} ({t.lengthKm} km · {t.biomeLabel})
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-[var(--text-primary)] mb-1.5">
                  Repère visuel de terrain (borne, pont, arbre remarquable) *
                </label>
                <input
                  type="text"
                  placeholder="Ex : 200m après la passerelle du ruisseau, borne #4"
                  value={landmark}
                  onChange={(e) => setLandmark(e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)] text-xs text-[var(--text-primary)] focus:outline-none focus:ring-1 focus:ring-[var(--brand-primary)]"
                />
                {formErrors.landmark && (
                  <p className="text-[11px] text-red-600 dark:text-red-400 mt-1 font-semibold">
                    {formErrors.landmark}
                  </p>
                )}
              </div>
            </div>

            {/* Simulated GPS Tag */}
            <div className="p-3.5 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)] flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs">
              <div className="flex items-center gap-2">
                <MapPin
                  key={gpsPulseKey}
                  className="w-4 h-4 text-emerald-600 dark:text-emerald-400 shrink-0 eco-pin-drop"
                />
                <span className="font-mono text-emerald-800 dark:text-emerald-200 font-bold">
                  {gpsCoordinates}
                </span>
              </div>

              <button
                type="button"
                onClick={refreshGpsLocation}
                disabled={gpsRefreshing}
                className="px-3 py-1.5 rounded-lg bg-[var(--bg-surface)] border border-[var(--border-default)] text-[11px] font-semibold text-[var(--text-primary)] hover:bg-[var(--bg-canvas)] cursor-pointer flex items-center gap-1.5 shrink-0"
              >
                <Compass className={`w-3.5 h-3.5 ${gpsRefreshing ? 'animate-spin' : ''}`} />
                <span>{gpsRefreshing ? 'Acquisition satellite...' : 'Actualiser le tag GPS'}</span>
              </button>
            </div>
          </div>

          {/* Details, Severity & Photo */}
          <div className="p-6 rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-default)] space-y-4">
            <h3 className="font-['Barlow_Semi_Condensed'] text-base font-bold text-[var(--text-primary)]">
              3. Détails &amp; Photo naturaliste
            </h3>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div className="sm:col-span-2 space-y-3">
                <div>
                  <label className="block text-xs font-semibold text-[var(--text-primary)] mb-1">
                    Intitulé synthétique *
                  </label>
                  <input
                    type="text"
                    placeholder="Ex : Nidification observée ou Arbre couché"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    className="w-full px-3.5 py-2.5 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)] text-xs text-[var(--text-primary)] focus:outline-none focus:ring-1 focus:ring-[var(--brand-primary)]"
                  />
                  {formErrors.title && (
                    <p className="text-[11px] text-red-600 dark:text-red-400 mt-1 font-semibold">
                      {formErrors.title}
                    </p>
                  )}
                </div>

                <div>
                  <label className="block text-xs font-semibold text-[var(--text-primary)] mb-1">
                    Description détaillée de l observation *
                  </label>
                  <textarea
                    rows={3}
                    placeholder="Précisez la taille, l état, la couleur, le comportement animal ou l ampleur de l incident pour guider l intervention."
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    className="w-full px-3.5 py-2.5 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)] text-xs text-[var(--text-primary)] focus:outline-none focus:ring-1 focus:ring-[var(--brand-primary)]"
                  />
                  {formErrors.description && (
                    <p className="text-[11px] text-red-600 dark:text-red-400 mt-1 font-semibold">
                      {formErrors.description}
                    </p>
                  )}
                </div>
              </div>

              {/* Severity & Pseudonym */}
              <div className="space-y-3">
                <div>
                  <label className="block text-xs font-semibold text-[var(--text-primary)] mb-1">
                    Niveau de sévérité / priorité
                  </label>
                  <select
                    value={severity}
                    onChange={(e) => setSeverity(e.target.value as ReportSeverity)}
                    className="w-full px-3 py-2.5 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)] text-xs text-[var(--text-primary)] focus:outline-none focus:ring-1 focus:ring-[var(--brand-primary)] cursor-pointer"
                  >
                    <option value="info">Info / Découverte naturaliste</option>
                    <option value="mineur">Mineur / Gêne légère</option>
                    <option value="modere">Modéré / Prudence requise</option>
                    <option value="critique">Critique / Danger ou braconnage</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-[var(--text-primary)] mb-1">
                    Identifiant Sentinelle
                  </label>
                  <input
                    type="text"
                    value={reporterName}
                    onChange={(e) => setReporterName(e.target.value)}
                    className="w-full px-3 py-2 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)] text-xs text-[var(--text-primary)] font-mono focus:outline-none focus:ring-1 focus:ring-[var(--brand-primary)]"
                  />
                </div>
              </div>
            </div>

            {/* Simulated Photo Selector */}
            <div className="pt-2 border-t border-[var(--border-default)]/60 space-y-2">
              <div className="flex items-center gap-2">
                <Camera className="w-4 h-4 text-[var(--brand-primary)]" />
                <label className="font-semibold text-xs text-[var(--text-primary)]">
                  Cliché photographique joint (Simulation capteur embarqué)
                </label>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
                {PHOTO_PRESETS.map((photo) => {
                  const isSelected = selectedPhotoPreset === photo.id;
                  return (
                    <div
                      key={photo.id}
                      onClick={() => setSelectedPhotoPreset(photo.id)}
                      className={`p-3 rounded-xl border transition-all cursor-pointer flex flex-col justify-between ${
                        isSelected
                          ? 'bg-[var(--bg-elevated)] border-[var(--brand-primary)] ring-2 ring-[var(--brand-primary)]/20 shadow-xs'
                          : 'bg-[var(--bg-canvas)] border-[var(--border-default)] hover:border-[var(--brand-primary)]/50'
                      }`}
                    >
                      <div className="space-y-1">
                        <div className="text-xs font-bold text-[var(--text-primary)]">
                          {photo.title}
                        </div>
                        <div className="text-[10px] text-[var(--text-muted)]">
                          {photo.meta}
                        </div>
                      </div>

                      <div className="pt-2 mt-2 flex items-center justify-between text-[10px] font-mono">
                        <span className="text-emerald-700 dark:text-emerald-300 font-semibold">
                          JPG 1080p
                        </span>
                        <div
                          className={`w-3.5 h-3.5 rounded-full border flex items-center justify-center ${
                            isSelected
                              ? 'bg-[var(--brand-primary)] border-[var(--brand-primary)] text-white'
                              : 'border-[var(--border-default)]'
                          }`}
                        >
                          {isSelected && <Check className="w-2.5 h-2.5 stroke-[3]" />}
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>

          {/* Form Actions */}
          <div className="flex items-center justify-end gap-3 pt-2">
            <button
              type="submit"
              className="px-6 py-3 rounded-xl bg-emerald-700 hover:bg-emerald-800 text-white font-bold text-sm shadow-md cursor-pointer flex items-center gap-2 active:scale-95 transition-transform"
            >
              <Send className="w-4 h-4" />
              <span>Transmettre aux Éco-Gardes du Parc</span>
            </button>
          </div>
        </form>
      )}

      {/* =================================================================== */}
      {/* VUE B : FIL COMMUNAUTAIRE DES SENTINELLES (F25)                     */}
      {/* =================================================================== */}
      {activeTab === 'feed' && (
        <div className="space-y-6">
          {/* Feed Filter Bar */}
          <div className="p-4 sm:p-5 rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-default)] flex flex-wrap items-center gap-4 text-xs">
            {/* Category Filter */}
            <div className="flex items-center gap-2">
              <span className="text-[var(--text-muted)] font-semibold">Catégorie :</span>
              <select
                value={feedCategoryFilter}
                onChange={(e) => setFeedCategoryFilter(e.target.value)}
                className="px-3 py-1.5 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)] text-[var(--text-primary)] cursor-pointer"
              >
                <option value="all">Toutes catégories</option>
                <option value="faune_rare">Faune Remarquable</option>
                <option value="flore_remarquable">Flore Protégée</option>
                <option value="obstacle_sentier">Obstacle Sentier</option>
                <option value="danger_meteo">Risque Météo</option>
                <option value="dechet_incivisme">Incivisme / Déchets</option>
              </select>
            </div>

            {/* Trail Filter */}
            <div className="flex items-center gap-2">
              <span className="text-[var(--text-muted)] font-semibold">Sentier :</span>
              <select
                value={feedTrailFilter}
                onChange={(e) => setFeedTrailFilter(e.target.value)}
                className="px-3 py-1.5 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)] text-[var(--text-primary)] cursor-pointer"
              >
                <option value="all">Tous les sentiers</option>
                {trails.map((t) => (
                  <option key={t.id} value={t.id}>
                    {t.name}
                  </option>
                ))}
              </select>
            </div>

            {/* Status Filter */}
            <div className="flex items-center gap-2">
              <span className="text-[var(--text-muted)] font-semibold">Statut :</span>
              <select
                value={feedStatusFilter}
                onChange={(e) => setFeedStatusFilter(e.target.value)}
                className="px-3 py-1.5 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)] text-[var(--text-primary)] cursor-pointer"
              >
                <option value="all">Tous les statuts</option>
                <option value="valide">Vérifiés par Éco-Garde</option>
                <option value="resolu">Résolus sur le terrain</option>
                <option value="en_attente">En attente d évaluation</option>
              </select>
            </div>

            <div className="ml-auto font-mono text-[var(--text-muted)]">
              {filteredReports.length} signalement(s) actif(s)
            </div>
          </div>

          {/* Reports Feed List */}
          <div className="space-y-4">
            {filteredReports.length === 0 ? (
              <div className="p-8 rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-default)] text-center space-y-2">
                <Sparkles className="w-8 h-8 text-[var(--brand-primary)] mx-auto" />
                <h4 className="font-['Barlow_Semi_Condensed'] font-bold text-base text-[var(--text-primary)]">
                  Aucun signalement ne correspond à ces critères
                </h4>
                <p className="text-xs text-[var(--text-muted)]">
                  Modifiez vos filtres ou soyez le premier à transmettre une observation de terrain.
                </p>
              </div>
            ) : (
              filteredReports.map((report) => {
                const trailMatch = trails.find((t) => t.id === report.trailId);
                const isFreshlyEmitted = report.id === lastCreatedReportId;
                return (
                  <div
                    key={report.id}
                    className={`p-5 sm:p-6 rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-default)] hover:shadow-xs transition-shadow space-y-4 ${
                      isFreshlyEmitted ? 'eco-sentinel-fresh ring-2 ring-emerald-500/40' : ''
                    }`}
                  >
                    {/* Top Row: ID, Category, Severity & Status */}
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2.5 pb-3 border-b border-[var(--border-default)]/60">
                      <div className="flex flex-wrap items-center gap-2">
                        <span className="font-['JetBrains_Mono'] font-bold text-xs text-[var(--brand-primary)]">
                          {report.id}
                        </span>
                        {isFreshlyEmitted && (
                          <span className="px-2 py-0.5 rounded-full text-[10px] font-mono font-bold bg-emerald-500/15 text-emerald-700 dark:text-emerald-300 border border-emerald-500/40">
                            ● Écho récent
                          </span>
                        )}
                        <span className="text-[var(--text-muted)]">·</span>
                        <div className="inline-flex items-center gap-1 text-xs font-semibold text-[var(--text-primary)]">
                          {renderCategoryIcon(report.type, 'w-3.5 h-3.5 text-[var(--brand-primary)]')}
                          <span>{getCategoryLabel(report.type)}</span>
                        </div>
                        {renderSeverityBadge(report.severity)}
                      </div>

                      <div className="flex items-center gap-2">
                        {renderStatusBadge(report.status)}
                      </div>
                    </div>

                    {/* Report Content */}
                    <div className="space-y-2">
                      <h4 className="font-['Barlow_Semi_Condensed'] text-base sm:text-lg font-bold text-[var(--text-primary)]">
                        {report.title}
                      </h4>

                      <p className="text-xs text-[var(--text-muted)] leading-relaxed">
                        {report.description}
                      </p>
                    </div>

                    {/* Metadata & Trail Pill */}
                    <div className="flex flex-wrap items-center justify-between gap-3 pt-2 text-[11px] text-[var(--text-muted)] font-sans">
                      <div className="flex flex-wrap items-center gap-2.5">
                        <button
                          type="button"
                          onClick={() => {
                            setGlobalSelectedTrailId(report.trailId);
                            setActiveView('sentiers');
                          }}
                          className="px-2.5 py-1 rounded-md bg-[var(--bg-elevated)] hover:bg-[var(--brand-primary)] hover:text-white border border-[var(--border-default)] font-semibold text-[var(--text-primary)] transition-colors cursor-pointer"
                          title="Localiser ce circuit sur la carte interactive"
                        >
                          📍 {trailMatch ? trailMatch.name : report.trailId}
                        </button>
                        <span>Repère : <strong className="text-[var(--text-primary)]">{report.landmark}</strong></span>
                        <span>Par <span className="font-mono">{report.reporterName}</span></span>
                      </div>

                      {/* Upvote Button with Live Counter */}
                      <button
                        onClick={() => upvoteReport(report.id)}
                        className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl border border-[var(--border-default)] bg-[var(--bg-elevated)] hover:bg-[var(--brand-primary)]/10 text-xs font-semibold text-[var(--text-primary)] hover:text-[var(--brand-primary)] transition-all cursor-pointer active:scale-95"
                        title="Confirmer cette observation sur le terrain"
                      >
                        <ThumbsUp className="w-3.5 h-3.5 text-[var(--brand-primary)]" />
                        <span className="font-mono font-bold">{report.upvotes}</span>
                        <span className="text-[10px] text-[var(--text-muted)]">appuis</span>
                      </button>
                    </div>

                    {/* Eco-Ranger Resolution Note */}
                    {report.rangerNote && (
                      <div className="p-3.5 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-xs text-emerald-900 dark:text-emerald-100 flex items-start gap-2.5">
                        <CheckCircle2 className="w-4 h-4 text-emerald-600 dark:text-emerald-400 shrink-0 mt-0.5" />
                        <div>
                          <strong className="font-semibold">Note d intervention de l Éco-Garde :</strong>{' '}
                          {report.rangerNote}
                        </div>
                      </div>
                    )}
                  </div>
                );
              })
            )}
          </div>
        </div>
      )}
    </div>
  );
};
