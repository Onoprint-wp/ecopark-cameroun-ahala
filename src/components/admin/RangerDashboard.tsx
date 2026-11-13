// ============================================================================
// RANGER SUPERVISION COCKPIT (src/components/admin/RangerDashboard.tsx)
// Features F26 (Cockpit), F27 (Trail Status Manager), F28 (Sentinel Moderation Queue)
// ============================================================================

import React, { useState, useMemo, useRef, useEffect } from 'react';
import {
  ShieldAlert,
  ShieldCheck,
  RotateCcw,
  Sliders,
  CheckCircle2,
  AlertTriangle,
  XCircle,
  Eye,
  Activity,
  TreePine,
  TrendingUp,
  MapPin,
  Clock,
  Check,
  X,
  FileText,
  AlertOctagon,
  Flower2,
  Trash2,
  CloudRain,
  Radio,
  Sparkles,
} from 'lucide-react';
import { useEcoPark } from '../../context/EcoParkContext';
import {
  TrailStatus,
  ReportStatus,
  ReportSeverity,
  CitizenReportType,
} from '../../types/ecosystem';
import { ImmersiveSection } from '../layout/ImmersiveSection';

export const RangerDashboard: React.FC = () => {
  const {
    telemetry,
    setDailyCapacity,
    trails,
    updateTrailStatus,
    reports,
    updateReportStatus,
    passes,
    resetToSeedData,
  } = useEcoPark();

  // --------------------------------------------------------------------------
  // State: Reset Confirmation Modal
  // --------------------------------------------------------------------------
  const [showResetConfirm, setShowResetConfirm] = useState(false);
  const [toastMessage, setToastMessage] = useState<string | null>(null);
  const toastTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const showToast = (msg: string) => {
    if (toastTimeoutRef.current) {
      clearTimeout(toastTimeoutRef.current);
    }
    setToastMessage(msg);
    toastTimeoutRef.current = setTimeout(() => {
      setToastMessage(null);
      toastTimeoutRef.current = null;
    }, 3000);
  };

  useEffect(() => {
    return () => {
      if (toastTimeoutRef.current) {
        clearTimeout(toastTimeoutRef.current);
      }
    };
  }, []);

  // --------------------------------------------------------------------------
  // State: Trail Status Manager (F27)
  // --------------------------------------------------------------------------
  const [activeClosureTrailId, setActiveClosureTrailId] = useState<string | null>(null);
  const [closureReasonInput, setClosureReasonInput] = useState<string>('');

  const CLOSURE_PRESETS = [
    'Nidification Aigle botté (Arrêté de quiétude préfectoral)',
    'Éboulement rocheux instable suite aux intempéries',
    'Arbre centenaire menaçant de choir en travers du sentier',
    'Risque incendie sévère — Canicule et sécheresse extrême',
    'Crue du ruisseau des Mousses & passerelle submergée',
  ];

  const handleOpenClosureDialog = (trailId: string, currentReason?: string) => {
    setActiveClosureTrailId(trailId);
    setClosureReasonInput(currentReason || CLOSURE_PRESETS[0]);
  };

  const handleConfirmClosure = (trailId: string) => {
    const reason = closureReasonInput.trim() || 'Fermeture préventive temporaire';
    updateTrailStatus(trailId, 'ferme', reason);
    setActiveClosureTrailId(null);
    setClosureReasonInput('');
    showToast(`Sentier fermé avec motif de protection enregistré`);
  };

  const handleSetTrailStatus = (trailId: string, status: TrailStatus) => {
    if (status === 'ferme') {
      handleOpenClosureDialog(trailId);
    } else if (status === 'balise') {
      updateTrailStatus(trailId, 'balise', 'Prudence requise — Balisage d entretien en cours');
      showToast(`Sentier passé en statut Balisé / Prudence`);
    } else {
      updateTrailStatus(trailId, 'fluide');
      showToast(`Sentier rouvert en circulation fluide`);
    }
  };

  // --------------------------------------------------------------------------
  // State: Sentinel Moderation Queue (F28)
  // --------------------------------------------------------------------------
  const [reportStatusFilter, setReportStatusFilter] = useState<'all' | ReportStatus>('all');
  const [reportTypeFilter, setReportTypeFilter] = useState<'all' | CitizenReportType>('all');
  const [reportTrailFilter, setReportTrailFilter] = useState<string>('all');

  // Resolution note dialog state
  const [resolvingReportId, setResolvingReportId] = useState<string | null>(null);
  const [interventionNoteInput, setInterventionNoteInput] = useState<string>('');

  const RESOLUTION_PRESETS = [
    'Équipe sentiers intervenue ce matin : obstacle débité et évacué.',
    'Balisage consolidé et platelage refixé avec vis inox.',
    'Observation enregistrée dans le registre biologique officiel de la réserve.',
    'Nettoyage et évacuation des déchets effectués lors de la patrouille.',
  ];

  const handleOpenResolutionDialog = (reportId: string) => {
    setResolvingReportId(reportId);
    setInterventionNoteInput(RESOLUTION_PRESETS[0]);
  };

  const handleConfirmResolution = (reportId: string) => {
    const note = interventionNoteInput.trim() || 'Intervention de terrain validée par l équipe technique';
    updateReportStatus(reportId, 'resolu', note);
    setResolvingReportId(null);
    setInterventionNoteInput('');
    showToast(`Signalement ${reportId} marqué Résolu avec note d intervention`);
  };

  const handleValidateReport = (reportId: string) => {
    updateReportStatus(reportId, 'valide', 'Signalement authentifié et validé par l éco-garde de service');
    showToast(`Signalement ${reportId} authentifié`);
  };

  const handleRejectReport = (reportId: string) => {
    updateReportStatus(reportId, 'rejete', 'Signalement non avéré ou doublon classé sans suite');
    showToast(`Signalement ${reportId} rejeté`);
  };

  // Filtered reports list
  const filteredReports = useMemo(() => {
    return reports.filter((r) => {
      if (reportStatusFilter !== 'all' && r.status !== reportStatusFilter) return false;
      if (reportTypeFilter !== 'all' && r.type !== reportTypeFilter) return false;
      if (reportTrailFilter !== 'all' && r.trailId !== reportTrailFilter) return false;
      return true;
    });
  }, [reports, reportStatusFilter, reportTypeFilter, reportTrailFilter]);

  // Counts for filters
  const reportCounts = useMemo(() => {
    return {
      total: reports.length,
      en_attente: reports.filter((r) => r.status === 'en_attente').length,
      valide: reports.filter((r) => r.status === 'valide').length,
      resolu: reports.filter((r) => r.status === 'resolu').length,
      rejete: reports.filter((r) => r.status === 'rejete').length,
    };
  }, [reports]);

  // --------------------------------------------------------------------------
  // Analytics: Hourly Histogram Calculation (08h - 20h)
  // --------------------------------------------------------------------------
  const HOURLY_DATA = useMemo(() => {
    const hours = [
      { h: '08h', label: '08:00 - 09:00', weight: 0.04 },
      { h: '09h', label: '09:00 - 10:00', weight: 0.07 },
      { h: '10h', label: '10:00 - 11:00', weight: 0.12 },
      { h: '11h', label: '11:00 - 12:00', weight: 0.15 },
      { h: '12h', label: '12:00 - 13:00', weight: 0.11 },
      { h: '13h', label: '13:00 - 14:00', weight: 0.08 },
      { h: '14h', label: '14:00 - 15:00', weight: 0.14 },
      { h: '15h', label: '15:00 - 16:00', weight: 0.13 },
      { h: '16h', label: '16:00 - 17:00', weight: 0.08 },
      { h: '17h', label: '17:00 - 18:00', weight: 0.05 },
      { h: '18h', label: '18:00 - 19:00', weight: 0.02 },
      { h: '19h', label: '19:00 - 20:00', weight: 0.01 },
    ];

    const totalVisitors = telemetry.currentOccupancy;
    const currentHour = new Date().getHours();

    return hours.map((item, index) => {
      const estimatedCount = Math.round(totalVisitors * item.weight);
      const hourNum = 8 + index;
      const isCurrent = currentHour === hourNum;
      return {
        ...item,
        hourNum,
        count: estimatedCount,
        isCurrent,
      };
    });
  }, [telemetry.currentOccupancy]);

  const maxHourlyCount = useMemo(() => {
    return Math.max(...HOURLY_DATA.map((d) => d.count), 150);
  }, [HOURLY_DATA]);

  // --------------------------------------------------------------------------
  // Analytics: Eco-Mobility Modal Share Breakdown
  // --------------------------------------------------------------------------
  const MOBILITY_BREAKDOWN = useMemo(() => {
    const counts: Record<string, number> = {
      train: 0,
      navette_electrique: 0,
      velo: 0,
      covoiturage: 0,
      voiture_solo: 0,
    };

    // Aggregate from booked passes
    passes.forEach((p) => {
      if (counts[p.mobilityMode] !== undefined) {
        counts[p.mobilityMode] += p.guestCount;
      }
    });

    // Add baseline realistic distribution if passes are few
    counts.train += 340;
    counts.navette_electrique += 215;
    counts.velo += 158;
    counts.covoiturage += 85;
    counts.voiture_solo += 44;

    const total = Object.values(counts).reduce((a, b) => a + b, 0);

    const MODES = [
      { id: 'train', label: 'Train express', color: '#2D6A4F', count: counts.train },
      { id: 'navette_electrique', label: 'Navette électrique', color: '#52B788', count: counts.navette_electrique },
      { id: 'velo', label: 'Vélo & VAE', color: '#D4A373', count: counts.velo },
      { id: 'covoiturage', label: 'Covoiturage', color: '#E76F51', count: counts.covoiturage },
      { id: 'voiture_solo', label: 'Voiture solo', color: '#46534B', count: counts.voiture_solo },
    ];

    let currentAngle = 0;
    const slices = MODES.map((m) => {
      const percent = total > 0 ? (m.count / total) * 100 : 0;
      const angle = (percent / 100) * 360;
      const startAngle = currentAngle;
      currentAngle += angle;

      return {
        ...m,
        percent: Math.round(percent),
        startAngle,
        endAngle: currentAngle,
      };
    });

    return { total, slices };
  }, [passes]);

  // Helper for SVG Pie/Doughnut slice path
  const getDoughnutSlicePath = (
    cx: number,
    cy: number,
    rInner: number,
    rOuter: number,
    startAngleDeg: number,
    endAngleDeg: number
  ) => {
    const toRad = (deg: number) => ((deg - 90) * Math.PI) / 180;
    const p1 = { x: cx + rOuter * Math.cos(toRad(startAngleDeg)), y: cy + rOuter * Math.sin(toRad(startAngleDeg)) };
    const p2 = { x: cx + rOuter * Math.cos(toRad(endAngleDeg)), y: cy + rOuter * Math.sin(toRad(endAngleDeg)) };
    const p3 = { x: cx + rInner * Math.cos(toRad(endAngleDeg)), y: cy + rInner * Math.sin(toRad(endAngleDeg)) };
    const p4 = { x: cx + rInner * Math.cos(toRad(startAngleDeg)), y: cy + rInner * Math.sin(toRad(startAngleDeg)) };

    const largeArc = endAngleDeg - startAngleDeg > 180 ? 1 : 0;

    return `M ${p1.x} ${p1.y} A ${rOuter} ${rOuter} 0 ${largeArc} 1 ${p2.x} ${p2.y} L ${p3.x} ${p3.y} A ${rInner} ${rInner} 0 ${largeArc} 0 ${p4.x} ${p4.y} Z`;
  };

  // Trail status badge renderer
  const renderTrailBadge = (status: TrailStatus) => {
    switch (status) {
      case 'fluide':
        return (
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800 dark:bg-emerald-950/80 dark:text-emerald-300 border border-emerald-300 dark:border-emerald-800">
            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" />
            <span>Fluide / Ouvert</span>
          </span>
        );
      case 'balise':
        return (
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-amber-100 text-amber-800 dark:bg-amber-950/80 dark:text-amber-300 border border-amber-300 dark:border-amber-800">
            <AlertTriangle className="w-3.5 h-3.5 text-amber-600 dark:text-amber-400" />
            <span>Balisé / Prudence</span>
          </span>
        );
      case 'ferme':
        return (
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-red-100 text-red-800 dark:bg-red-950/80 dark:text-red-300 border border-red-300 dark:border-red-800 animate-pulse">
            <XCircle className="w-3.5 h-3.5 text-red-600 dark:text-red-400" />
            <span>Fermé / Protection</span>
          </span>
        );
    }
  };

  // Report category icon renderer
  const renderCategoryIcon = (type: CitizenReportType) => {
    switch (type) {
      case 'faune_rare':
        return <Eye className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" />;
      case 'flore_remarquable':
        return <Flower2 className="w-3.5 h-3.5 text-teal-600 dark:text-teal-400" />;
      case 'obstacle_sentier':
        return <AlertTriangle className="w-3.5 h-3.5 text-amber-600 dark:text-amber-400" />;
      case 'dechet_incivisme':
        return <Trash2 className="w-3.5 h-3.5 text-rose-600 dark:text-rose-400" />;
      case 'danger_meteo':
        return <CloudRain className="w-3.5 h-3.5 text-sky-600 dark:text-sky-400" />;
    }
  };

  // Report severity badge
  const renderSeverityBadge = (severity: ReportSeverity) => {
    switch (severity) {
      case 'critique':
        return (
          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-red-100 text-red-800 border border-red-300 dark:bg-red-950/80 dark:text-red-300">
            <AlertOctagon className="w-3 h-3 text-red-600" />
            CRITIQUE
          </span>
        );
      case 'modere':
        return (
          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-amber-100 text-amber-800 border border-amber-300 dark:bg-amber-950/80 dark:text-amber-300">
            MODÉRÉ
          </span>
        );
      case 'mineur':
        return (
          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-zinc-100 text-zinc-700 border border-zinc-300 dark:bg-zinc-800 dark:text-zinc-300">
            MINEUR
          </span>
        );
      case 'info':
        return (
          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-emerald-100 text-emerald-800 border border-emerald-300 dark:bg-emerald-950/80 dark:text-emerald-300">
            INFO
          </span>
        );
    }
  };

  return (
    <div className="space-y-10 pb-16">
      {/* Toast Notification */}
      {toastMessage && (
        <div className="fixed bottom-6 right-6 z-50 p-4 rounded-xl bg-[var(--brand-primary)] text-white text-xs font-semibold shadow-2xl flex items-center gap-2 border border-emerald-400 animate-in fade-in slide-in-from-bottom duration-200">
          <CheckCircle2 className="w-4 h-4 text-emerald-300 shrink-0" />
          <span>{toastMessage}</span>
        </div>
      )}

      {/* Immersive Section Header */}
      <ImmersiveSection variant="bark" className="py-10">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="inline-flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-amber-300">
              <ShieldAlert className="w-4 h-4 text-amber-400" />
              <span>Poste de Commandement Central</span>
            </div>
            <h1 className="font-['Fraunces'] text-2xl sm:text-4xl font-bold text-white mt-1">
              Console de Supervision Éco-Garde
            </h1>
          </div>
          <div className="text-xs text-[#E9F5ED]/80 font-mono bg-[#121614]/80 px-3 py-2 rounded-xl border border-[#36403A]">
            Contrôle Dynamique des 6 Sentiers &amp; Régulation des Quotas
          </div>
        </div>
      </ImmersiveSection>

      {/* Cockpit Officer & Status Bar */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="p-6 rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-default)] flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-sm">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-amber-600 to-amber-800 flex items-center justify-center text-white shadow-sm shrink-0">
              <ShieldAlert className="w-6 h-6" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-xs font-mono font-bold uppercase tracking-wider text-amber-700 dark:text-amber-400">
                  Poste de Commandement Central
                </span>
                <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-mono font-bold bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300 border border-emerald-300">
                  <Radio className="w-2.5 h-2.5 animate-pulse text-emerald-500" />
                  VHF CANAL 15 ACTIF
                </span>
              </div>
              <h1 className="font-['Fraunces'] text-xl sm:text-2xl font-bold text-[var(--text-primary)] mt-0.5">
                Garde Chef : Thomas D. (#GARDE-04)
              </h1>
              <p className="text-xs text-[var(--text-muted)]">
                Supervision temps réel des 6 sentiers, des créneaux d affluence et de la sécurité terrain
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => setShowResetConfirm(true)}
              className="inline-flex items-center gap-2 px-3.5 py-2 rounded-xl border border-[var(--border-default)] bg-[var(--bg-elevated)] hover:bg-[var(--bg-surface)] text-xs font-semibold text-[var(--text-primary)] transition-all cursor-pointer shadow-xs active:scale-95"
              title="Réinitialiser les données aux valeurs de référence initiales"
            >
              <RotateCcw className="w-3.5 h-3.5 text-amber-600 dark:text-amber-400" />
              <span>Réinitialiser la Démo</span>
            </button>
          </div>
        </div>
      </div>

      {/* Main Cockpit Sections */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-10">
        {/* ================================================================= */}
        {/* SECTION 1: DAILY QUOTA REGULATOR (F26)                            */}
        {/* ================================================================= */}
        <section aria-labelledby="quota-regulator-title">
          <div className="p-6 sm:p-8 rounded-3xl bg-[var(--bg-surface)] border border-[var(--border-default)] shadow-sm space-y-6">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div>
                <div className="inline-flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-[var(--brand-primary)]">
                  <Sliders className="w-4 h-4 text-[var(--brand-primary)]" />
                  <span>Régulation Écologique par Quota</span>
                </div>
                <h2
                  id="quota-regulator-title"
                  className="font-['Fraunces'] text-xl sm:text-2xl font-bold text-[var(--text-primary)] mt-1"
                >
                  Régulateur de Capacité Journalière
                </h2>
                <p className="text-xs text-[var(--text-muted)] mt-1 max-w-xl">
                  Ajustez le plafond journalier de visiteurs pour moduler la pression anthropique selon
                  la fragilité saisonnière, la météo et les indices de reproduction de la faune.
                </p>
              </div>

              {/* Big Quota Indicator */}
              <div className="p-4 rounded-2xl bg-[var(--bg-elevated)] border border-[var(--border-default)] text-right font-mono min-w-[200px] shadow-xs">
                <div className="text-[11px] text-[var(--text-muted)] uppercase tracking-wider">
                  Plafond Fixé
                </div>
                <div className="text-3xl sm:text-4xl font-['Fraunces'] font-bold text-[var(--brand-primary)]">
                  {telemetry.dailyCapacityMax}
                </div>
                <div className="text-xs text-[var(--text-muted)] mt-0.5">
                  visiteurs max / 24h
                </div>
              </div>
            </div>

            {/* Slider with visual track */}
            <div className="space-y-3 pt-2">
              <input
                type="range"
                min={500}
                max={2500}
                step={50}
                value={telemetry.dailyCapacityMax}
                onChange={(e) => setDailyCapacity(Number(e.target.value))}
                className="w-full h-3 rounded-lg bg-[var(--bg-canvas)] accent-[var(--brand-primary)] cursor-pointer border border-[var(--border-default)]"
                aria-label="Ajuster le quota journalier de visiteurs"
              />

              <div className="flex justify-between text-xs font-mono text-[var(--text-muted)]">
                <span>500 (Sanctuaire quiétude)</span>
                <span>1500 (Régime nominal)</span>
                <span>2500 (Plafond haute saison)</span>
              </div>
            </div>

            {/* Quick Presets Buttons */}
            <div className="pt-2 border-t border-[var(--border-default)]/60 flex flex-wrap items-center gap-2">
              <span className="text-xs font-semibold text-[var(--text-primary)] mr-2">
                Paliers préconfigurés :
              </span>
              {[500, 1000, 1500, 2000, 2500].map((presetVal) => {
                const isActive = telemetry.dailyCapacityMax === presetVal;
                return (
                  <button
                    key={presetVal}
                    onClick={() => {
                      setDailyCapacity(presetVal);
                      showToast(`Quota ajusté à ${presetVal} visiteurs`);
                    }}
                    className={`px-3 py-1.5 rounded-xl border text-xs font-mono font-bold transition-all cursor-pointer ${
                      isActive
                        ? 'bg-[var(--brand-primary)] text-white border-[var(--brand-primary)] shadow-xs scale-105'
                        : 'bg-[var(--bg-elevated)] text-[var(--text-primary)] border-[var(--border-default)] hover:border-[var(--brand-primary)]'
                    }`}
                  >
                    {presetVal} places
                  </button>
                );
              })}
            </div>

            {/* Live Capacity Telemetry Snapshot */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-2">
              <div className="p-3.5 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)]">
                <span className="text-[10px] font-mono text-[var(--text-muted)] uppercase">
                  Présents sur site
                </span>
                <div className="text-xl font-bold font-mono text-[var(--text-primary)] mt-1">
                  {telemetry.currentOccupancy}
                </div>
                <span className="text-[11px] text-[var(--text-muted)]">visiteurs enregistrés</span>
              </div>

              <div className="p-3.5 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)]">
                <span className="text-[10px] font-mono text-[var(--text-muted)] uppercase">
                  Places disponibles
                </span>
                <div className="text-xl font-bold font-mono text-emerald-700 dark:text-emerald-400 mt-1">
                  {Math.max(0, telemetry.dailyCapacityMax - telemetry.currentOccupancy)}
                </div>
                <span className="text-[11px] text-[var(--text-muted)]">réservables aujourd hui</span>
              </div>

              <div className="p-3.5 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)]">
                <span className="text-[10px] font-mono text-[var(--text-muted)] uppercase">
                  Taux de remplissage
                </span>
                <div className="text-xl font-bold font-mono text-[var(--brand-primary)] mt-1">
                  {Math.round((telemetry.currentOccupancy / telemetry.dailyCapacityMax) * 100)}%
                </div>
                <span className="text-[11px] text-[var(--text-muted)]">de la jauge écologique</span>
              </div>

              <div className="p-3.5 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)]">
                <span className="text-[10px] font-mono text-[var(--text-muted)] uppercase">
                  Indice Qualité Air
                </span>
                <div className="text-xl font-bold font-mono text-emerald-700 dark:text-emerald-400 mt-1">
                  {telemetry.airQualityIqa} / 100
                </div>
                <span className="text-[11px] text-emerald-800 dark:text-emerald-300 font-semibold">
                  {telemetry.airQualityStatus}
                </span>
              </div>
            </div>
          </div>
        </section>

        {/* ================================================================= */}
        {/* SECTION 2: CHARTS & ECO-ANALYTICS (F26)                           */}
        {/* ================================================================= */}
        <section className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* 1. Hourly Occupancy Histogram (2 Cols) */}
          <div className="lg:col-span-2 p-6 rounded-3xl bg-[var(--bg-surface)] border border-[var(--border-default)] shadow-sm space-y-4 flex flex-col justify-between">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <div>
                <div className="flex items-center gap-2">
                  <Activity className="w-4 h-4 text-[var(--brand-primary)]" />
                  <h3 className="font-['Fraunces'] text-lg font-bold text-[var(--text-primary)]">
                    Histogramme d Affluence Horaire (08h00 - 20h00)
                  </h3>
                </div>
                <p className="text-xs text-[var(--text-muted)]">
                  Distribution continue des entrées et créneau de fréquentation de pointe
                </p>
              </div>

              <div className="flex items-center gap-2 text-xs font-mono">
                <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-[var(--bg-elevated)] border border-[var(--border-default)]">
                  <span className="w-2.5 h-2.5 rounded-full bg-[var(--brand-primary)]" />
                  <span>Flux estimé</span>
                </span>
                <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-[var(--bg-elevated)] border border-[var(--border-default)] text-amber-700 dark:text-amber-400">
                  <span className="w-2.5 h-2.5 rounded-full bg-amber-500 animate-pulse" />
                  <span>Heure actuelle</span>
                </span>
              </div>
            </div>

            {/* SVG Histogram Chart */}
            <div className="w-full aspect-[21/9] min-h-[220px] pt-4">
              <svg
                viewBox="0 0 600 200"
                className="w-full h-full overflow-visible"
                role="img"
                aria-label="Graphique d affluence horaire des visiteurs"
              >
                {/* Horizontal Grid lines */}
                <line x1="40" y1="30" x2="580" y2="30" stroke="currentColor" strokeOpacity="0.1" strokeDasharray="3 3" />
                <line x1="40" y1="80" x2="580" y2="80" stroke="currentColor" strokeOpacity="0.1" strokeDasharray="3 3" />
                <line x1="40" y1="130" x2="580" y2="130" stroke="currentColor" strokeOpacity="0.1" strokeDasharray="3 3" />
                <line x1="40" y1="170" x2="580" y2="170" stroke="currentColor" strokeOpacity="0.2" />

                {/* Y-axis labels */}
                <text x="32" y="34" textAnchor="end" className="text-[10px] font-mono fill-[var(--text-muted)]">
                  {maxHourlyCount}
                </text>
                <text x="32" y="84" textAnchor="end" className="text-[10px] font-mono fill-[var(--text-muted)]">
                  {Math.round(maxHourlyCount * 0.66)}
                </text>
                <text x="32" y="134" textAnchor="end" className="text-[10px] font-mono fill-[var(--text-muted)]">
                  {Math.round(maxHourlyCount * 0.33)}
                </text>
                <text x="32" y="174" textAnchor="end" className="text-[10px] font-mono fill-[var(--text-muted)]">
                  0
                </text>

                {/* Histogram Bars */}
                {HOURLY_DATA.map((bar, idx) => {
                  const barWidth = 32;
                  const x = 55 + idx * 43;
                  const barHeight = Math.max(4, (bar.count / maxHourlyCount) * 140);
                  const y = 170 - barHeight;

                  return (
                    <g key={bar.h} className="group cursor-pointer">
                      {/* Bar fill */}
                      <rect
                        x={x}
                        y={y}
                        width={barWidth}
                        height={barHeight}
                        rx="5"
                        fill={bar.isCurrent ? '#E76F51' : '#52B788'}
                        className="transition-all duration-200 group-hover:opacity-80 group-hover:scale-y-105"
                      />

                      {/* Top count label */}
                      <text
                        x={x + barWidth / 2}
                        y={y - 5}
                        textAnchor="middle"
                        className="text-[10px] font-mono font-bold fill-[var(--text-primary)] opacity-0 group-hover:opacity-100 transition-opacity"
                      >
                        {bar.count}
                      </text>

                      {/* X-axis label */}
                      <text
                        x={x + barWidth / 2}
                        y="186"
                        textAnchor="middle"
                        className={`text-[10px] font-mono ${
                          bar.isCurrent
                            ? 'font-bold fill-[#E76F51]'
                            : 'fill-[var(--text-muted)]'
                        }`}
                      >
                        {bar.h}
                      </text>
                    </g>
                  );
                })}
              </svg>
            </div>

            <div className="pt-3 border-t border-[var(--border-default)]/60 flex items-center justify-between text-xs text-[var(--text-muted)]">
              <span>Pic d affluence estimé : <strong>11h00 - 12h00</strong> et <strong>14h00 - 15h00</strong></span>
              <span className="font-mono">Rythme d écoulement nominal</span>
            </div>
          </div>

          {/* 2. Eco-Mobility Modal Share Breakdown (1 Col) */}
          <div className="p-6 rounded-3xl bg-[var(--bg-surface)] border border-[var(--border-default)] shadow-sm space-y-4 flex flex-col justify-between">
            <div>
              <div className="flex items-center gap-2">
                <TrendingUp className="w-4 h-4 text-[var(--brand-primary)]" />
                <h3 className="font-['Fraunces'] text-lg font-bold text-[var(--text-primary)]">
                  Part Modale Éco-Mobilité
                </h3>
              </div>
              <p className="text-xs text-[var(--text-muted)]">
                Origine des transports des visiteurs du parc
              </p>
            </div>

            {/* Doughnut SVG Chart */}
            <div className="relative w-44 h-44 mx-auto my-2">
              <svg viewBox="0 0 200 200" className="w-full h-full">
                {MOBILITY_BREAKDOWN.slices.map((slice) => {
                  const pathData = getDoughnutSlicePath(
                    100,
                    100,
                    55,
                    88,
                    slice.startAngle,
                    slice.endAngle
                  );
                  return (
                    <path
                      key={slice.id}
                      d={pathData}
                      fill={slice.color}
                      className="hover:opacity-85 transition-opacity cursor-pointer"
                    >
                      <title>{`${slice.label}: ${slice.percent}% (${slice.count} pers.)`}</title>
                    </path>
                  );
                })}
              </svg>

              {/* Central Avoided CO2 metric */}
              <div className="absolute inset-0 flex flex-col items-center justify-center text-center pointer-events-none">
                <span className="text-[10px] font-mono text-[var(--text-muted)] uppercase">
                  CO₂ Évité
                </span>
                <span className="text-base font-bold font-mono text-[var(--brand-primary)]">
                  {telemetry.totalCo2AvoidedKg} kg
                </span>
                <span className="text-[9px] text-[var(--text-muted)]">cumul global</span>
              </div>
            </div>

            {/* Modal Legend */}
            <div className="space-y-1.5 pt-2 border-t border-[var(--border-default)]/60 text-xs">
              {MOBILITY_BREAKDOWN.slices.map((m) => (
                <div key={m.id} className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span
                      className="w-2.5 h-2.5 rounded-full shrink-0"
                      style={{ backgroundColor: m.color }}
                    />
                    <span className="text-[var(--text-primary)]">{m.label}</span>
                  </div>
                  <span className="font-mono font-bold text-[var(--text-primary)]">
                    {m.percent}%
                  </span>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* ================================================================= */}
        {/* SECTION 3: DYNAMIC TRAIL STATUS MANAGER (F27)                     */}
        {/* ================================================================= */}
        <section aria-labelledby="trail-status-manager-title" className="space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <div>
              <div className="inline-flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-[var(--brand-primary)]">
                <TreePine className="w-4 h-4 text-[var(--brand-primary)]" />
                <span>Gestionnaire d Infrastructure</span>
              </div>
              <h2
                id="trail-status-manager-title"
                className="font-['Fraunces'] text-xl sm:text-2xl font-bold text-[var(--text-primary)] mt-1"
              >
                Contrôle d État des 6 Sentiers Officiels
              </h2>
            </div>

            <div className="text-xs font-mono text-[var(--text-muted)]">
              {trails.filter((t) => t.status === 'fluide').length} ouverts ·{' '}
              {trails.filter((t) => t.status === 'balise').length} balisés ·{' '}
              {trails.filter((t) => t.status === 'ferme').length} fermés
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {trails.map((trail) => {
              const isClosed = trail.status === 'ferme';
              const occupancyRatio = Math.round((trail.currentOccupancy / trail.maxCapacity) * 100);

              return (
                <div
                  key={trail.id}
                  className={`p-5 rounded-2xl border transition-all flex flex-col justify-between space-y-4 shadow-sm ${
                    isClosed
                      ? 'bg-red-50/60 dark:bg-red-950/20 border-red-300 dark:border-red-900'
                      : 'bg-[var(--bg-surface)] border-[var(--border-default)]'
                  }`}
                >
                  <div className="space-y-3">
                    {/* Top Row: Title & Badge */}
                    <div className="flex items-start justify-between gap-2">
                      <div>
                        <span className="text-[10px] font-mono uppercase text-[var(--brand-primary)] font-semibold">
                          {trail.biomeLabel}
                        </span>
                        <h3 className="font-['Fraunces'] font-bold text-base text-[var(--text-primary)]">
                          {trail.name}
                        </h3>
                      </div>
                      {renderTrailBadge(trail.status)}
                    </div>

                    {/* Technical stats */}
                    <div className="flex items-center gap-3 text-xs text-[var(--text-muted)] font-mono">
                      <span>{trail.lengthKm} km</span>
                      <span>·</span>
                      <span>+{trail.elevationGainM}m D+</span>
                      <span>·</span>
                      <span className="capitalize">{trail.difficulty.replace('_', ' ')}</span>
                    </div>

                    {/* Affluence Progress */}
                    <div className="space-y-1">
                      <div className="flex justify-between text-xs font-mono">
                        <span className="text-[var(--text-muted)]">Fréquentation :</span>
                        <span className="font-bold text-[var(--text-primary)]">
                          {trail.currentOccupancy} / {trail.maxCapacity} ({occupancyRatio}%)
                        </span>
                      </div>
                      <div className="w-full h-1.5 rounded-full bg-[var(--bg-canvas)] overflow-hidden">
                        <div
                          className={`h-full rounded-full transition-all duration-300 ${
                            isClosed
                              ? 'bg-zinc-400'
                              : occupancyRatio >= 80
                              ? 'bg-amber-500'
                              : 'bg-emerald-500'
                          }`}
                          style={{ width: `${Math.min(100, occupancyRatio)}%` }}
                        />
                      </div>
                    </div>

                    {/* Closure Reason Banner if closed */}
                    {isClosed && trail.closureReason && (
                      <div className="p-3 rounded-xl bg-red-100/80 dark:bg-red-900/40 border border-red-300 dark:border-red-800 text-xs text-red-900 dark:text-red-200 flex items-start gap-2">
                        <AlertTriangle className="w-4 h-4 text-red-600 dark:text-red-400 shrink-0 mt-0.5" />
                        <div>
                          <strong className="font-semibold">Motif de fermeture :</strong>{' '}
                          {trail.closureReason}
                        </div>
                      </div>
                    )}
                  </div>

                  {/* Dynamic Action Buttons */}
                  <div className="pt-3 border-t border-[var(--border-default)]/60 space-y-2">
                    <div className="text-[11px] font-semibold text-[var(--text-muted)] uppercase">
                      Changer l état opérationnel :
                    </div>

                    <div className="grid grid-cols-3 gap-1.5 text-xs">
                      <button
                        onClick={() => handleSetTrailStatus(trail.id, 'fluide')}
                        className={`p-2 rounded-xl border font-bold text-center transition-all cursor-pointer ${
                          trail.status === 'fluide'
                            ? 'bg-emerald-600 text-white border-emerald-600 shadow-xs'
                            : 'bg-[var(--bg-elevated)] text-[var(--text-primary)] border-[var(--border-default)] hover:bg-[var(--bg-canvas)]'
                        }`}
                      >
                        Fluide
                      </button>

                      <button
                        onClick={() => handleSetTrailStatus(trail.id, 'balise')}
                        className={`p-2 rounded-xl border font-bold text-center transition-all cursor-pointer ${
                          trail.status === 'balise'
                            ? 'bg-amber-600 text-white border-amber-600 shadow-xs'
                            : 'bg-[var(--bg-elevated)] text-[var(--text-primary)] border-[var(--border-default)] hover:bg-[var(--bg-canvas)]'
                        }`}
                      >
                        Balisé
                      </button>

                      <button
                        onClick={() => handleSetTrailStatus(trail.id, 'ferme')}
                        className={`p-2 rounded-xl border font-bold text-center transition-all cursor-pointer ${
                          trail.status === 'ferme'
                            ? 'bg-red-600 text-white border-red-600 shadow-xs'
                            : 'bg-[var(--bg-elevated)] text-[var(--text-primary)] border-[var(--border-default)] hover:bg-[var(--bg-canvas)]'
                        }`}
                      >
                        Fermer
                      </button>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </section>

        {/* ================================================================= */}
        {/* SECTION 4: CITIZEN SENTINEL MODERATION QUEUE (F28)                */}
        {/* ================================================================= */}
        <section aria-labelledby="sentinel-moderation-title" className="space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <div className="inline-flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-[var(--brand-primary)]">
                <FileText className="w-4 h-4 text-[var(--brand-primary)]" />
                <span>Veille Participative Citoyenne</span>
              </div>
              <h2
                id="sentinel-moderation-title"
                className="font-['Fraunces'] text-xl sm:text-2xl font-bold text-[var(--text-primary)] mt-1"
              >
                File de Modération des Signalements Sentinelle
              </h2>
              <p className="text-xs text-[var(--text-muted)] mt-1">
                Authentifiez les découvertes naturalistes et régulez les alertes d obstacles terrain
              </p>
            </div>

            {/* Status Filter Badges */}
            <div className="flex flex-wrap items-center gap-1.5 p-1 rounded-xl bg-[var(--bg-surface)] border border-[var(--border-default)]">
              <button
                onClick={() => setReportStatusFilter('all')}
                className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
                  reportStatusFilter === 'all'
                    ? 'bg-[var(--bg-elevated)] text-[var(--brand-primary)] font-bold shadow-xs'
                    : 'text-[var(--text-muted)] hover:text-[var(--text-primary)]'
                }`}
              >
                Tous ({reportCounts.total})
              </button>
              <button
                onClick={() => setReportStatusFilter('en_attente')}
                className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
                  reportStatusFilter === 'en_attente'
                    ? 'bg-[var(--bg-elevated)] text-amber-700 dark:text-amber-400 font-bold shadow-xs'
                    : 'text-[var(--text-muted)] hover:text-[var(--text-primary)]'
                }`}
              >
                En attente ({reportCounts.en_attente})
              </button>
              <button
                onClick={() => setReportStatusFilter('valide')}
                className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
                  reportStatusFilter === 'valide'
                    ? 'bg-[var(--bg-elevated)] text-emerald-700 dark:text-emerald-400 font-bold shadow-xs'
                    : 'text-[var(--text-muted)] hover:text-[var(--text-primary)]'
                }`}
              >
                Validés ({reportCounts.valide})
              </button>
              <button
                onClick={() => setReportStatusFilter('resolu')}
                className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
                  reportStatusFilter === 'resolu'
                    ? 'bg-[var(--bg-elevated)] text-sky-700 dark:text-sky-400 font-bold shadow-xs'
                    : 'text-[var(--text-muted)] hover:text-[var(--text-primary)]'
                }`}
              >
                Résolus ({reportCounts.resolu})
              </button>
              <button
                onClick={() => setReportStatusFilter('rejete')}
                className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
                  reportStatusFilter === 'rejete'
                    ? 'bg-[var(--bg-elevated)] text-zinc-700 dark:text-zinc-400 font-bold shadow-xs'
                    : 'text-[var(--text-muted)] hover:text-[var(--text-primary)]'
                }`}
              >
                Rejetés ({reportCounts.rejete})
              </button>
            </div>
          </div>

          {/* Additional Multi-criteria Filters */}
          <div className="flex flex-wrap items-center gap-3 p-3.5 rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-default)] text-xs">
            <div className="flex items-center gap-2">
              <span className="text-[var(--text-muted)] font-semibold">Sentier :</span>
              <select
                value={reportTrailFilter}
                onChange={(e) => setReportTrailFilter(e.target.value)}
                className="px-2.5 py-1.5 rounded-lg bg-[var(--bg-elevated)] border border-[var(--border-default)] text-[var(--text-primary)] cursor-pointer"
              >
                <option value="all">Tous les sentiers</option>
                {trails.map((t) => (
                  <option key={t.id} value={t.id}>
                    {t.name}
                  </option>
                ))}
              </select>
            </div>

            <div className="flex items-center gap-2">
              <span className="text-[var(--text-muted)] font-semibold">Catégorie :</span>
              <select
                value={reportTypeFilter}
                onChange={(e) => setReportTypeFilter(e.target.value as 'all' | CitizenReportType)}
                className="px-2.5 py-1.5 rounded-lg bg-[var(--bg-elevated)] border border-[var(--border-default)] text-[var(--text-primary)] cursor-pointer"
              >
                <option value="all">Toutes catégories</option>
                <option value="faune_rare">Faune rare</option>
                <option value="flore_remarquable">Flore remarquable</option>
                <option value="obstacle_sentier">Obstacle sentier</option>
                <option value="danger_meteo">Risque météo</option>
                <option value="dechet_incivisme">Incivisme / Déchets</option>
              </select>
            </div>

            <div className="ml-auto font-mono text-[var(--text-muted)]">
              {filteredReports.length} signalement(s) filtré(s)
            </div>
          </div>

          {/* Reports List */}
          <div className="space-y-4">
            {filteredReports.length === 0 ? (
              <div className="p-8 rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-default)] text-center space-y-2">
                <Sparkles className="w-8 h-8 text-[var(--brand-primary)] mx-auto" />
                <h4 className="font-['Fraunces'] font-bold text-base text-[var(--text-primary)]">
                  Aucun signalement ne correspond à ces critères
                </h4>
                <p className="text-xs text-[var(--text-muted)]">
                  Modifiez vos filtres de modération ou revenez plus tard.
                </p>
              </div>
            ) : (
              filteredReports.map((rep) => {
                const trailMatch = trails.find((t) => t.id === rep.trailId);
                const isPending = rep.status === 'en_attente';
                const isResolved = rep.status === 'resolu';
                const isValidated = rep.status === 'valide';
                const isRejected = rep.status === 'rejete';

                return (
                  <div
                    key={rep.id}
                    className="p-5 sm:p-6 rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-default)] space-y-4 shadow-sm hover:shadow-md transition-shadow"
                  >
                    {/* Top Row: ID, Category, Severity & Status */}
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-[var(--border-default)]/60">
                      <div className="flex flex-wrap items-center gap-2 text-xs">
                        <span className="font-['JetBrains_Mono'] font-bold text-xs text-[var(--brand-primary)]">
                          {rep.id}
                        </span>
                        <span className="text-[var(--text-muted)]">·</span>
                        <div className="inline-flex items-center gap-1 font-semibold text-[var(--text-primary)]">
                          {renderCategoryIcon(rep.type)}
                          <span className="capitalize">{rep.type.replace('_', ' ')}</span>
                        </div>
                        {renderSeverityBadge(rep.severity)}
                      </div>

                      <div className="flex items-center gap-2">
                        {isPending && (
                          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-semibold bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300 border border-amber-300">
                            <Clock className="w-3.5 h-3.5 text-amber-600" />
                            En attente de revue
                          </span>
                        )}
                        {isValidated && (
                          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300 border border-emerald-300">
                            <Check className="w-3.5 h-3.5 text-emerald-600" />
                            Validé éco-garde
                          </span>
                        )}
                        {isResolved && (
                          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-semibold bg-sky-100 text-sky-800 dark:bg-sky-950 dark:text-sky-300 border border-sky-300">
                            <CheckCircle2 className="w-3.5 h-3.5 text-sky-600" />
                            Résolu sur le terrain
                          </span>
                        )}
                        {isRejected && (
                          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-semibold bg-zinc-100 text-zinc-700 dark:bg-zinc-800 dark:text-zinc-300 border border-zinc-300">
                            <X className="w-3.5 h-3.5 text-zinc-500" />
                            Rejeté / Classé
                          </span>
                        )}
                      </div>
                    </div>

                    {/* Report Content */}
                    <div className="space-y-1.5">
                      <h4 className="font-['Fraunces'] text-base sm:text-lg font-bold text-[var(--text-primary)]">
                        {rep.title}
                      </h4>
                      <p className="text-xs text-[var(--text-muted)] leading-relaxed">
                        {rep.description}
                      </p>
                    </div>

                    {/* Location & Sender Metadata */}
                    <div className="flex flex-wrap items-center justify-between gap-3 text-[11px] text-[var(--text-muted)] pt-1">
                      <div className="flex flex-wrap items-center gap-3">
                        <span className="flex items-center gap-1 text-[var(--text-primary)] font-semibold">
                          <MapPin className="w-3 h-3 text-[var(--brand-primary)]" />
                          <span>{trailMatch ? trailMatch.name : rep.trailId}</span>
                        </span>
                        <span>Repère : <strong className="text-[var(--text-primary)]">{rep.landmark}</strong></span>
                        <span>Transmis par <span className="font-mono">{rep.reporterName}</span></span>
                      </div>
                      <div className="font-mono">
                        {new Date(rep.timestamp).toLocaleTimeString('fr-FR', {
                          hour: '2-digit',
                          minute: '2-digit',
                        })}
                      </div>
                    </div>

                    {/* Forester Intervention Note Banner */}
                    {rep.rangerNote && (
                      <div className="p-3.5 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-xs text-emerald-900 dark:text-emerald-100 flex items-start gap-2.5">
                        <ShieldCheck className="w-4 h-4 text-emerald-600 dark:text-emerald-400 shrink-0 mt-0.5" />
                        <div>
                          <strong className="font-semibold">Note d intervention de l Éco-Garde :</strong>{' '}
                          {rep.rangerNote}
                        </div>
                      </div>
                    )}

                    {/* Moderation Actions Bar */}
                    <div className="pt-3 border-t border-[var(--border-default)]/60 flex flex-wrap items-center justify-between gap-3">
                      <div className="text-xs text-[var(--text-muted)] font-mono">
                        Actions de commandement :
                      </div>

                      <div className="flex flex-wrap items-center gap-2">
                        {!isValidated && !isResolved && (
                          <button
                            onClick={() => handleValidateReport(rep.id)}
                            className="px-3 py-1.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold transition-all cursor-pointer shadow-xs active:scale-95 flex items-center gap-1"
                          >
                            <Check className="w-3.5 h-3.5" />
                            <span>Valider</span>
                          </button>
                        )}

                        {!isResolved && (
                          <button
                            onClick={() => handleOpenResolutionDialog(rep.id)}
                            className="px-3 py-1.5 rounded-xl bg-sky-600 hover:bg-sky-700 text-white text-xs font-semibold transition-all cursor-pointer shadow-xs active:scale-95 flex items-center gap-1"
                          >
                            <CheckCircle2 className="w-3.5 h-3.5" />
                            <span>Résoudre &amp; Commenter</span>
                          </button>
                        )}

                        {!isRejected && (
                          <button
                            onClick={() => handleRejectReport(rep.id)}
                            className="px-3 py-1.5 rounded-xl border border-[var(--border-default)] bg-[var(--bg-elevated)] hover:bg-red-50 hover:text-red-700 dark:hover:bg-red-950/40 text-[var(--text-muted)] text-xs font-semibold transition-all cursor-pointer"
                          >
                            <span>Rejeter</span>
                          </button>
                        )}
                      </div>
                    </div>
                  </div>
                );
              })
            )}
          </div>
        </section>
      </div>

      {/* =================================================================== */}
      {/* MODAL 1: TRAIL CLOSURE REASON DIALOG (F27)                          */}
      {/* =================================================================== */}
      {activeClosureTrailId && (
        <div className="fixed inset-0 z-50 overflow-y-auto bg-black/60 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="w-full max-w-lg rounded-3xl bg-[var(--bg-elevated)] border border-[var(--border-default)] shadow-2xl p-6 sm:p-7 space-y-5 animate-in fade-in zoom-in-95 duration-200">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-red-100 dark:bg-red-950 text-red-600 dark:text-red-400 flex items-center justify-center shrink-0">
                  <XCircle className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="font-['Fraunces'] font-bold text-lg text-[var(--text-primary)]">
                    Fermeture d Urgence de Sentier
                  </h3>
                  <span className="text-xs text-[var(--text-muted)] font-mono">
                    {trails.find((t) => t.id === activeClosureTrailId)?.name}
                  </span>
                </div>
              </div>

              <button
                onClick={() => setActiveClosureTrailId(null)}
                className="p-2 rounded-lg text-[var(--text-muted)] hover:text-[var(--text-primary)] cursor-pointer"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <p className="text-xs text-[var(--text-muted)] leading-relaxed">
              La fermeture du sentier sera répercutée <strong>instantanément</strong> sur la Carte
              Topographique interactive (tracé rouge hachuré), désactivera la réservation dans le
              catalogue et décrémentera la capacité globale.
            </p>

            <div className="space-y-3">
              <label className="block text-xs font-semibold text-[var(--text-primary)]">
                Motifs fréquents de fermeture :
              </label>

              <div className="space-y-1.5">
                {CLOSURE_PRESETS.map((preset) => (
                  <button
                    key={preset}
                    type="button"
                    onClick={() => setClosureReasonInput(preset)}
                    className={`w-full text-left p-2.5 rounded-xl border text-xs transition-colors cursor-pointer ${
                      closureReasonInput === preset
                        ? 'bg-[var(--brand-primary)]/10 border-[var(--brand-primary)] text-[var(--brand-primary)] font-semibold'
                        : 'bg-[var(--bg-surface)] border-[var(--border-default)] text-[var(--text-muted)] hover:text-[var(--text-primary)]'
                    }`}
                  >
                    {preset}
                  </button>
                ))}
              </div>

              <div className="pt-2">
                <label className="block text-xs font-semibold text-[var(--text-primary)] mb-1">
                  Motif officiel détaillé (affiché aux randonneurs) :
                </label>
                <textarea
                  rows={3}
                  value={closureReasonInput}
                  onChange={(e) => setClosureReasonInput(e.target.value)}
                  placeholder="Précisez la raison et la durée estimée de la fermeture..."
                  className="w-full px-3.5 py-2.5 rounded-xl bg-[var(--bg-surface)] border border-[var(--border-default)] text-xs text-[var(--text-primary)] focus:outline-none focus:ring-1 focus:ring-red-500"
                />
              </div>
            </div>

            <div className="pt-3 border-t border-[var(--border-default)] flex items-center justify-end gap-3">
              <button
                type="button"
                onClick={() => setActiveClosureTrailId(null)}
                className="px-4 py-2 rounded-xl border border-[var(--border-default)] text-xs font-semibold text-[var(--text-muted)] hover:text-[var(--text-primary)] cursor-pointer"
              >
                Annuler
              </button>

              <button
                type="button"
                onClick={() => handleConfirmClosure(activeClosureTrailId)}
                className="px-5 py-2 rounded-xl bg-red-600 hover:bg-red-700 text-white text-xs font-bold transition-all cursor-pointer shadow-md"
              >
                Appliquer la fermeture
              </button>
            </div>
          </div>
        </div>
      )}

      {/* =================================================================== */}
      {/* MODAL 2: RESOLUTION NOTE DIALOG (F28)                               */}
      {/* =================================================================== */}
      {resolvingReportId && (
        <div className="fixed inset-0 z-50 overflow-y-auto bg-black/60 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="w-full max-w-lg rounded-3xl bg-[var(--bg-elevated)] border border-[var(--border-default)] shadow-2xl p-6 sm:p-7 space-y-5 animate-in fade-in zoom-in-95 duration-200">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-sky-100 dark:bg-sky-950 text-sky-600 dark:text-sky-400 flex items-center justify-center shrink-0">
                  <CheckCircle2 className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="font-['Fraunces'] font-bold text-lg text-[var(--text-primary)]">
                    Clôturer &amp; Résoudre le Signalement
                  </h3>
                  <span className="text-xs text-[var(--text-muted)] font-mono">
                    {resolvingReportId}
                  </span>
                </div>
              </div>

              <button
                onClick={() => setResolvingReportId(null)}
                className="p-2 rounded-lg text-[var(--text-muted)] hover:text-[var(--text-primary)] cursor-pointer"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <p className="text-xs text-[var(--text-muted)] leading-relaxed">
              Enregistrez la note d intervention officielle. Cette information sera directement
              consultable par la communauté dans l espace Sentinelle Nature.
            </p>

            <div className="space-y-3">
              <label className="block text-xs font-semibold text-[var(--text-primary)]">
                Modèles d intervention type :
              </label>

              <div className="space-y-1.5">
                {RESOLUTION_PRESETS.map((preset) => (
                  <button
                    key={preset}
                    type="button"
                    onClick={() => setInterventionNoteInput(preset)}
                    className={`w-full text-left p-2.5 rounded-xl border text-xs transition-colors cursor-pointer ${
                      interventionNoteInput === preset
                        ? 'bg-sky-500/10 border-sky-500 text-sky-700 dark:text-sky-300 font-semibold'
                        : 'bg-[var(--bg-surface)] border-[var(--border-default)] text-[var(--text-muted)] hover:text-[var(--text-primary)]'
                    }`}
                  >
                    {preset}
                  </button>
                ))}
              </div>

              <div className="pt-2">
                <label className="block text-xs font-semibold text-[var(--text-primary)] mb-1">
                  Note d intervention de l Éco-Garde :
                </label>
                <textarea
                  rows={3}
                  value={interventionNoteInput}
                  onChange={(e) => setInterventionNoteInput(e.target.value)}
                  placeholder="Décrivez les mesures prises sur place par l'équipe technique..."
                  className="w-full px-3.5 py-2.5 rounded-xl bg-[var(--bg-surface)] border border-[var(--border-default)] text-xs text-[var(--text-primary)] focus:outline-none focus:ring-1 focus:ring-sky-500"
                />
              </div>
            </div>

            <div className="pt-3 border-t border-[var(--border-default)] flex items-center justify-end gap-3">
              <button
                type="button"
                onClick={() => setResolvingReportId(null)}
                className="px-4 py-2 rounded-xl border border-[var(--border-default)] text-xs font-semibold text-[var(--text-muted)] hover:text-[var(--text-primary)] cursor-pointer"
              >
                Annuler
              </button>

              <button
                type="button"
                onClick={() => handleConfirmResolution(resolvingReportId)}
                className="px-5 py-2 rounded-xl bg-sky-600 hover:bg-sky-700 text-white text-xs font-bold transition-all cursor-pointer shadow-md"
              >
                Confirmer la résolution
              </button>
            </div>
          </div>
        </div>
      )}

      {/* =================================================================== */}
      {/* MODAL 3: RESET TO SEED CONFIRMATION MODAL                           */}
      {/* =================================================================== */}
      {showResetConfirm && (
        <div className="fixed inset-0 z-50 overflow-y-auto bg-black/60 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="w-full max-w-md rounded-3xl bg-[var(--bg-elevated)] border border-[var(--border-default)] shadow-2xl p-6 sm:p-7 space-y-4 animate-in fade-in zoom-in-95 duration-200">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-amber-100 dark:bg-amber-950 text-amber-600 dark:text-amber-400 flex items-center justify-center shrink-0">
                <RotateCcw className="w-5 h-5" />
              </div>
              <h3 className="font-['Fraunces'] font-bold text-lg text-[var(--text-primary)]">
                Réinitialisation Démo
              </h3>
            </div>

            <p className="text-xs text-[var(--text-muted)] leading-relaxed">
              Voulez-vous restaurer les données d origine (6 sentiers, quotas nominaux, 3 billets initiaux
              et 5 signalements Sentinelle) ? Cette action réinitialisera le `localStorage`.
            </p>

            <div className="pt-3 border-t border-[var(--border-default)] flex items-center justify-end gap-3">
              <button
                type="button"
                onClick={() => setShowResetConfirm(false)}
                className="px-4 py-2 rounded-xl border border-[var(--border-default)] text-xs font-semibold text-[var(--text-muted)] hover:text-[var(--text-primary)] cursor-pointer"
              >
                Annuler
              </button>

              <button
                type="button"
                onClick={() => {
                  resetToSeedData();
                  setShowResetConfirm(false);
                  showToast('Données réinitialisées aux valeurs de référence');
                }}
                className="px-5 py-2 rounded-xl bg-[var(--brand-primary)] text-white text-xs font-bold transition-all cursor-pointer shadow-md"
              >
                Confirmer la réinitialisation
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
