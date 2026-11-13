// ============================================================================
// ECO-PARK ENDEMIC BIODIVERSITY SPECIES ATLAS (src/components/biodiversity/SpeciesAtlas.tsx)
// Feature F19 — 8 Keystone Species with UICN Badges, Seasonal Guides & Trail Links
// ============================================================================

import React, { useState, useMemo, useEffect, useRef } from 'react';
import { useEcoPark } from '../../context/EcoParkContext';
import {
  SpeciesCategory,
  ConservationStatus,
} from '../../types/ecosystem';
import { ImmersiveSection } from '../layout/ImmersiveSection';
import {
  Search,
  Eye,
  Calendar,
  Compass,
  ShieldCheck,
  Sparkles,
  Moon,
  Feather,
  Bug,
  Flower2,
  Droplets,
  ArrowRight,
  X,
  Send,
} from 'lucide-react';

export const SpeciesAtlas: React.FC = () => {
  const {
    species,
    trails,
    reports,
    selectedSpeciesId,
    setSelectedSpeciesId,
    setSelectedTrailId,
    setActiveView,
  } = useEcoPark();

  const speciesCardRefs = useRef<Record<string, HTMLDivElement | null>>({});

  useEffect(() => {
    if (!selectedSpeciesId) return;
    const timer = window.setTimeout(() => {
      const targetEl = speciesCardRefs.current[selectedSpeciesId];
      if (targetEl) {
        targetEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    }, 120);
    return () => window.clearTimeout(timer);
  }, [selectedSpeciesId]);

  // Search & category filters
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [selectedGroup, setSelectedGroup] = useState<string>('all');
  const [selectedSeason, setSelectedSeason] = useState<string>('all');

  // Filtered species list
  const filteredSpecies = useMemo(() => {
    return species.filter((sp) => {
      // Text search
      if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase();
        const matchCommon = sp.commonName.toLowerCase().includes(q);
        const matchScientific = sp.scientificName.toLowerCase().includes(q);
        const matchHabitat = sp.habitat.toLowerCase().includes(q);
        const matchDesc = sp.description.toLowerCase().includes(q);
        if (!matchCommon && !matchScientific && !matchHabitat && !matchDesc) {
          return false;
        }
      }

      // Group / category match
      if (selectedGroup !== 'all') {
        if (selectedGroup === 'oiseaux' && sp.category !== 'oiseaux') return false;
        if (selectedGroup === 'mammiferes' && sp.category !== 'mammiferes') return false;
        if (selectedGroup === 'flore' && sp.category !== 'flore') return false;
        if (selectedGroup === 'amphibiens' && sp.category !== 'amphibiens') return false;
        if (selectedGroup === 'insectes' && sp.category !== 'insectes') return false;
      }

      // Season match
      if (selectedSeason !== 'all') {
        const SEASON_MAP: Record<string, string> = {
          printemps: 'Printemps',
          ete: 'Été',
          automne: 'Automne',
          hiver: 'Hiver',
        };
        const targetSeason = SEASON_MAP[selectedSeason] || selectedSeason;
        if (!sp.observationSeason.includes(targetSeason as any)) {
          return false;
        }
      }

      return true;
    });
  }, [species, searchQuery, selectedGroup, selectedSeason]);

  // Category Icon helper
  const renderCategoryIcon = (cat: SpeciesCategory) => {
    switch (cat) {
      case 'oiseaux':
      case 'avifaune':
        return <Feather className="w-4 h-4 text-sky-500" />;
      case 'mammiferes':
        return <Compass className="w-4 h-4 text-amber-500" />;
      case 'flore':
        return <Flower2 className="w-4 h-4 text-emerald-500" />;
      case 'amphibiens':
        return <Droplets className="w-4 h-4 text-teal-500" />;
      case 'insectes':
        return <Bug className="w-4 h-4 text-indigo-500" />;
      default:
        return <Eye className="w-4 h-4 text-[var(--brand-primary)]" />;
    }
  };

  // IUCN Badge Renderer with tooltip explanations
  const renderIucnBadge = (status: ConservationStatus) => {
    switch (status) {
      case 'LC':
        return (
          <span
            className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-md text-xs font-mono font-bold bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300 border border-emerald-300 dark:border-emerald-800"
            title="Préoccupation mineure (Least Concern) : espèce abondante ou bien protégée."
          >
            UICN · LC
          </span>
        );
      case 'NT':
        return (
          <span
            className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-md text-xs font-mono font-bold bg-teal-100 text-teal-800 dark:bg-teal-950 dark:text-teal-300 border border-teal-300 dark:border-teal-800"
            title="Quasi menacée (Near Threatened) : espèce proche du seuil des menaces."
          >
            UICN · NT
          </span>
        );
      case 'VU':
        return (
          <span
            className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-md text-xs font-mono font-bold bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300 border border-amber-300 dark:border-amber-800"
            title="Vulnérable (Vulnerable) : risque élevé d extinction à l état sauvage."
          >
            UICN · VU
          </span>
        );
      case 'EN':
      case 'CR':
        return (
          <span
            className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-md text-xs font-mono font-bold bg-red-100 text-red-800 dark:bg-red-950 dark:text-red-300 border border-red-300 dark:border-red-800"
            title="En danger / Danger critique : protection stricte prioritaire."
          >
            UICN · {status}
          </span>
        );
    }
  };

  // Navigate to trail on map
  const handleJumpToTrail = (trailId: string) => {
    setSelectedTrailId(trailId);
    setActiveView('sentiers');
  };

  return (
    <div className="space-y-10 pb-16">
      {/* Editorial Header Section */}
      <ImmersiveSection variant="forest" className="py-12 sm:py-16">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div className="space-y-3 max-w-3xl">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/10 backdrop-blur-md border border-white/20 text-xs font-mono text-[#B7E4C7]">
              <Sparkles className="w-3.5 h-3.5 text-[#74C69D]" />
              <span>Jardin Zoologique, Bassins Piscicoles &amp; Flore Tropicale · Yaoundé – Ahala</span>
            </div>

            <h1 className="font-['Barlow_Semi_Condensed'] text-3xl sm:text-4xl lg:text-5xl font-bold text-white tracking-tight leading-tight">
              Jardin Zoologique &amp; Atlas de la Biodiversité d&apos;Ahala
            </h1>

            <p className="text-sm sm:text-base text-[#E9F5ED]/90 leading-relaxed font-sans">
              Découvrez les pensionnaires emblématiques d&apos;ECOPARK CAMEROUN à Yaoundé-Ahala : le Gorille des plaines <strong>« ToTo »</strong>, nos chimpanzés, les tortues géantes, les tilapias et carpes de nos bassins (« Du bassin à la braise »), les chevaux du manège équestre et notre flore tropicale.
            </p>
          </div>

          <div className="p-4 rounded-2xl bg-[#1F2421]/90 border border-[#36403A] text-xs font-mono text-[#8EBAA0] space-y-1 self-start md:self-auto shrink-0 shadow-lg">
            <div className="text-white font-bold text-sm">Visites Guidées &amp; Écoles</div>
            <div>Entrée Zoo : 1 000 FCFA Ad. / 500 FCFA Enf.</div>
            <div>Forfait Scolaire : 1 350 FCFA / élève</div>
          </div>
        </div>
      </ImmersiveSection>

      {/* Main Container */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
        {/* Category Tabs & Search Bar */}
        <div className="p-5 rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-default)] shadow-xs space-y-4">
          <div className="flex flex-col md:flex-row items-stretch md:items-center justify-between gap-4">
            {/* Search Input */}
            <div className="relative flex-1">
              <Search className="w-4 h-4 text-[var(--text-muted)] absolute left-3.5 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Rechercher une espèce par nom, habitat, nom latin..."
                className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)] text-sm text-[var(--text-primary)] placeholder-[var(--text-muted)] focus:outline-none focus:ring-2 focus:ring-[var(--brand-primary)]"
              />
              {searchQuery && (
                <button
                  type="button"
                  onClick={() => setSearchQuery('')}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-xs text-[var(--text-muted)] hover:text-[var(--text-primary)] cursor-pointer"
                >
                  ✕
                </button>
              )}
            </div>

            {/* Season Filter Dropdown */}
            <div className="flex items-center gap-2 text-xs font-mono">
              <Calendar className="w-4 h-4 text-[var(--brand-primary)]" />
              <span className="text-[var(--text-muted)]">Saison :</span>
              <select
                value={selectedSeason}
                onChange={(e) => setSelectedSeason(e.target.value)}
                className="px-3 py-2 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)] text-xs text-[var(--text-primary)] focus:outline-none focus:ring-1 focus:ring-[var(--brand-primary)] cursor-pointer"
              >
                <option value="all">Toutes saisons</option>
                <option value="printemps">Printemps</option>
                <option value="ete">Été</option>
                <option value="automne">Automne</option>
                <option value="hiver">Hiver</option>
              </select>
            </div>
          </div>

          {/* Category Pill Tabs */}
          <div className="pt-2 border-t border-[var(--border-default)]/60 flex flex-wrap gap-2">
            {[
              { id: 'all', label: 'Toutes les espèces', icon: Eye },
              { id: 'oiseaux', label: 'Avifaune (Oiseaux)', icon: Feather },
              { id: 'mammiferes', label: 'Mammifères', icon: Compass },
              { id: 'flore', label: 'Flore Protégée', icon: Flower2 },
              { id: 'amphibiens', label: 'Amphibiens', icon: Droplets },
              { id: 'insectes', label: 'Insectes Rares', icon: Bug },
            ].map((tab) => {
              const TabIcon = tab.icon;
              const isSelected = selectedGroup === tab.id;

              return (
                <button
                  key={tab.id}
                  type="button"
                  onClick={() => setSelectedGroup(tab.id)}
                  className={`px-3.5 py-2 rounded-xl text-xs font-semibold transition-all flex items-center gap-1.5 cursor-pointer ${
                    isSelected
                      ? 'bg-[var(--brand-primary)] text-white shadow-xs'
                      : 'bg-[var(--bg-elevated)] text-[var(--text-primary)] hover:bg-[var(--border-default)]/50'
                  }`}
                >
                  <TabIcon className="w-3.5 h-3.5" />
                  <span>{tab.label}</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Focused Species Banner when navigated from Home */}
        {selectedSpeciesId && species.some((s) => s.id === selectedSpeciesId) && (
          <div className="p-4 rounded-2xl bg-emerald-50/80 dark:bg-emerald-950/40 border border-emerald-300 dark:border-emerald-800 flex flex-wrap items-center justify-between gap-3 text-xs">
            <div className="flex items-center gap-2 text-emerald-900 dark:text-emerald-200 font-semibold">
              <Sparkles className="w-4 h-4 text-emerald-600 dark:text-emerald-400 shrink-0" />
              <span>
                Fiche sélectionnée :{' '}
                <strong>{species.find((s) => s.id === selectedSpeciesId)?.commonName}</strong>
              </span>
            </div>
            <button
              type="button"
              onClick={() => setSelectedSpeciesId(null)}
              className="inline-flex items-center gap-1 px-3 py-1 rounded-lg bg-[var(--bg-surface)] border border-[var(--border-default)] text-[var(--text-primary)] font-semibold hover:border-[var(--brand-primary)] cursor-pointer"
            >
              <X className="w-3.5 h-3.5" />
              <span>Désélectionner</span>
            </button>
          </div>
        )}

        {/* Species Count Summary */}
        <div className="flex items-center justify-between text-xs font-mono text-[var(--text-muted)]">
          <span>
            Affichage de <strong>{filteredSpecies.length}</strong> espèce{filteredSpecies.length > 1 ? 's' : ''} sur {species.length}
          </span>
          <span className="italic font-serif">Synchronisé avec les observations Sentinelle terrain</span>
        </div>

        {/* Species Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 lg:gap-8">
          {filteredSpecies.map((sp) => {
            // Find attached trails
            const attachedTrails = trails.filter((t) => sp.trailIds.includes(t.id));
            const isHighlighted = selectedSpeciesId === sp.id;
            const sentinelBonusSightings = reports.filter(
              (r) =>
                r.status !== 'rejete' &&
                sp.trailIds.includes(r.trailId) &&
                (sp.category === 'flore'
                  ? r.type === 'flore_remarquable'
                  : r.type === 'faune_rare')
            ).length;
            const liveSightingsCount = sp.sightingsCount + sentinelBonusSightings;

            return (
              <div
                key={sp.id}
                ref={(el) => {
                  speciesCardRefs.current[sp.id] = el;
                }}
                onClick={() => setSelectedSpeciesId(isHighlighted ? null : sp.id)}
                className={`p-6 sm:p-7 rounded-2xl bg-[var(--bg-surface)] border shadow-xs hover:shadow-md transition-all duration-200 flex flex-col justify-between space-y-5 cursor-pointer ${
                  isHighlighted
                    ? 'border-[var(--brand-primary)] ring-2 ring-[var(--brand-primary)]/30 shadow-md'
                    : 'border-[var(--border-default)]'
                }`}
              >
                {/* Header: Common Name, Scientific Name & IUCN Badge */}
                <div className="space-y-3">
                  {sp.photoUrl && (
                    <div className="h-48 w-full rounded-xl overflow-hidden bg-[#1F2421] mb-2 border border-[var(--border-default)]">
                      <img
                        src={sp.photoUrl}
                        alt={sp.commonName}
                        className="w-full h-full object-cover"
                        loading="lazy"
                      />
                    </div>
                  )}
                  <div className="flex items-start justify-between gap-3">
                    <div className="space-y-1">
                      <div className="flex items-center gap-2">
                        <span className="p-1 rounded-md bg-[var(--bg-elevated)] border border-[var(--border-default)]">
                          {renderCategoryIcon(sp.category)}
                        </span>
                        <span className="text-xs font-mono font-semibold uppercase tracking-wider text-[var(--brand-primary)]">
                          {sp.categoryLabel}
                        </span>
                      </div>

                      <h2 className="font-['Barlow_Semi_Condensed'] text-xl sm:text-2xl font-bold text-[var(--text-primary)]">
                        {sp.commonName}
                      </h2>

                      <div className="text-xs italic font-serif text-[var(--text-muted)]">
                        {sp.scientificName}
                      </div>
                    </div>

                    <div className="shrink-0">{renderIucnBadge(sp.iucnStatus)}</div>
                  </div>

                  {/* Seasonal Observation, Best Time & Live Sentinel Sightings Badges */}
                  <div className="flex flex-wrap items-center gap-2 pt-1">
                    <div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-[var(--bg-elevated)] border border-[var(--border-default)] text-[11px] font-mono text-[var(--text-primary)]">
                      <Calendar className="w-3 h-3 text-[var(--brand-primary)]" />
                      <span>{sp.observationSeason.join(' · ')}</span>
                    </div>

                    <div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-[var(--bg-elevated)] border border-[var(--border-default)] text-[11px] font-mono text-[var(--text-muted)]">
                      <Moon className="w-3 h-3 text-amber-500" />
                      <span>{sp.bestTime}</span>
                    </div>

                    <div
                      className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-emerald-500/10 border border-emerald-500/25 text-[11px] font-mono font-semibold text-emerald-800 dark:text-emerald-300"
                      title="Cumul des relevés naturalistes et signalements Sentinelle validés sur ses circuits"
                    >
                      <Eye className="w-3 h-3 text-emerald-600 dark:text-emerald-400" />
                      <span>{liveSightingsCount} obs. recensées</span>
                    </div>
                  </div>

                  {/* Monograph Description */}
                  <p className="text-xs sm:text-sm text-[var(--text-muted)] leading-relaxed">
                    {sp.description}
                  </p>

                  {/* Habitat & Diet */}
                  <div className="space-y-1.5 text-xs text-[var(--text-muted)] pt-3 border-t border-[var(--border-default)]/60">
                    <div>
                      <strong className="text-[var(--text-primary)]">Habitat de prédilection :</strong>{' '}
                      {sp.habitat}
                    </div>
                    <div>
                      <strong className="text-[var(--text-primary)]">Régime / Spécificité :</strong>{' '}
                      {sp.dietOrFloraType}
                    </div>
                  </div>

                  {/* Field Identification Tips */}
                  {sp.identificationTips && sp.identificationTips.length > 0 && (
                    <div className="p-3.5 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)] space-y-1.5">
                      <span className="text-[11px] font-mono font-bold uppercase tracking-wider text-[var(--brand-primary)] block">
                        Critères d identification sur le terrain :
                      </span>
                      <ul className="text-xs text-[var(--text-primary)] space-y-1 pl-1">
                        {sp.identificationTips.map((tip, idx) => (
                          <li key={idx} className="flex items-start gap-1.5">
                            <span className="text-[var(--brand-primary)] font-bold">›</span>
                            <span>{tip}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Field Indices & Eco-Ranger Guideline */}
                  <div className="space-y-2 text-xs">
                    {sp.fieldIndices && (
                      <div className="text-[var(--text-muted)]">
                        <strong className="text-[var(--text-primary)]">Indices de présence :</strong>{' '}
                        {sp.fieldIndices}
                      </div>
                    )}

                    <div className="p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-900 dark:text-emerald-200 text-xs flex items-start gap-2">
                      <ShieldCheck className="w-4 h-4 text-emerald-600 dark:text-emerald-400 shrink-0 mt-0.5" />
                      <div>
                        <strong>Consigne de quiétude éco-garde :</strong> {sp.protectionCharter}
                      </div>
                    </div>
                  </div>
                </div>

                {/* Attached Trails Links & Sentinel Reporting Shortcut */}
                <div
                  className="pt-4 border-t border-[var(--border-default)]/60 space-y-2"
                  onClick={(e) => e.stopPropagation()}
                >
                  <div className="flex items-center justify-between gap-2">
                    <span className="text-[11px] font-mono font-semibold text-[var(--text-muted)] uppercase tracking-wider">
                      Sentiers propices à l observation :
                    </span>
                    <button
                      type="button"
                      onClick={() => {
                        if (sp.trailIds[0]) {
                          setSelectedTrailId(sp.trailIds[0]);
                        }
                        setActiveView('pass');
                      }}
                      className="inline-flex items-center gap-1 text-[11px] font-semibold text-[var(--brand-primary)] hover:underline cursor-pointer"
                      title="Transmettre une observation terrain via Sentinelle Nature"
                    >
                      <Send className="w-3 h-3" />
                      <span>Signaler une observation</span>
                    </button>
                  </div>

                  <div className="flex flex-wrap gap-2">
                    {attachedTrails.map((trail) => (
                      <button
                        key={trail.id}
                        type="button"
                        onClick={() => handleJumpToTrail(trail.id)}
                        className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-[var(--bg-elevated)] hover:bg-[var(--brand-primary)] hover:text-white border border-[var(--border-default)] text-xs font-semibold text-[var(--text-primary)] transition-all cursor-pointer group"
                        title={`Localiser le ${trail.name} sur la carte`}
                      >
                        <Compass className="w-3.5 h-3.5 text-[var(--brand-primary)] group-hover:text-white transition-colors" />
                        <span>{trail.name.split('&')[0].trim()}</span>
                        <ArrowRight className="w-3 h-3 opacity-60 group-hover:opacity-100 group-hover:translate-x-0.5 transition-all" />
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
