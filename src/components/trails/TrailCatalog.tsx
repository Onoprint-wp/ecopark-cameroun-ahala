// ============================================================================
// ECO-PARK TRAIL CATALOG & MULTICRITERIA FILTERS (src/components/trails/TrailCatalog.tsx)
// Feature F18 — Filterable Trail Grid with Mini Sparklines & Live Sync
// ============================================================================

import React, { useState, useMemo } from 'react';
import { useEcoPark } from '../../context/EcoParkContext';
import {
  TrailDifficulty,
  TrailStatus,
} from '../../types/ecosystem';
import {
  Search,
  Compass,
  Ticket,
  CheckCircle2,
  AlertTriangle,
  XCircle,
  Accessibility,
  Trees,
  RotateCcw,
} from 'lucide-react';

export interface TrailCatalogProps {
  onSelectTrailOnMap?: (trailId: string) => void;
  className?: string;
}

export const TrailCatalog: React.FC<TrailCatalogProps> = ({
  onSelectTrailOnMap,
  className = '',
}) => {
  const { trails, selectedTrailId, setSelectedTrailId, setActiveView } = useEcoPark();

  // Filter states
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [selectedBiome, setSelectedBiome] = useState<string>('all');
  const [selectedDifficulty, setSelectedDifficulty] = useState<string>('all');
  const [pmrOnly, setPmrOnly] = useState<boolean>(false);
  const [selectedStatus, setSelectedStatus] = useState<string>('all');

  // Filter logic
  const filteredTrails = useMemo(() => {
    return trails.filter((trail) => {
      // Search text match
      if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase();
        const matchesName = trail.name.toLowerCase().includes(q);
        const matchesSub = trail.subtitle.toLowerCase().includes(q);
        const matchesDesc = trail.description.toLowerCase().includes(q);
        const matchesBiome = trail.biomeLabel.toLowerCase().includes(q);
        if (!matchesName && !matchesSub && !matchesDesc && !matchesBiome) {
          return false;
        }
      }

      // Biome match
      if (selectedBiome !== 'all' && trail.biome !== selectedBiome) {
        return false;
      }

      // Difficulty match
      if (selectedDifficulty !== 'all' && trail.difficulty !== selectedDifficulty) {
        return false;
      }

      // PMR match
      if (pmrOnly && !trail.pmrAccessible) {
        return false;
      }

      // Status match
      if (selectedStatus !== 'all' && trail.status !== selectedStatus) {
        return false;
      }

      return true;
    });
  }, [trails, searchQuery, selectedBiome, selectedDifficulty, pmrOnly, selectedStatus]);

  // Reset filters
  const handleResetFilters = () => {
    setSearchQuery('');
    setSelectedBiome('all');
    setSelectedDifficulty('all');
    setPmrOnly(false);
    setSelectedStatus('all');
  };

  const hasActiveFilters =
    searchQuery !== '' ||
    selectedBiome !== 'all' ||
    selectedDifficulty !== 'all' ||
    pmrOnly ||
    selectedStatus !== 'all';

  // Status badge renderer
  const renderStatusBadge = (status: TrailStatus) => {
    switch (status) {
      case 'fluide':
        return (
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300 border border-emerald-300 dark:border-emerald-800">
            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" />
            Fluide / Ouvert
          </span>
        );
      case 'balise':
        return (
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300 border border-amber-300 dark:border-amber-800">
            <AlertTriangle className="w-3.5 h-3.5 text-amber-600 dark:text-amber-400" />
            Balisé / Prudence
          </span>
        );
      case 'ferme':
        return (
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-red-100 text-red-800 dark:bg-red-950 dark:text-red-300 border border-red-300 dark:border-red-800">
            <XCircle className="w-3.5 h-3.5 text-red-600 dark:text-red-400" />
            Fermé (Nidification)
          </span>
        );
    }
  };

  // Difficulty badge label & color
  const renderDifficultyBadge = (difficulty: TrailDifficulty) => {
    switch (difficulty) {
      case 'tres_facile':
      case 'facile':
        return (
          <span className="px-2 py-0.5 rounded text-[11px] font-semibold bg-emerald-50 text-emerald-700 dark:bg-emerald-950/60 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800">
            Facile
          </span>
        );
      case 'moyen':
        return (
          <span className="px-2 py-0.5 rounded text-[11px] font-semibold bg-blue-50 text-blue-700 dark:bg-blue-950/60 dark:text-blue-300 border border-blue-200 dark:border-blue-800">
            Modéré
          </span>
        );
      case 'difficile':
      case 'sportif':
        return (
          <span className="px-2 py-0.5 rounded text-[11px] font-semibold bg-amber-50 text-amber-700 dark:bg-amber-950/60 dark:text-amber-300 border border-amber-200 dark:border-amber-800">
            Sportif
          </span>
        );
      case 'expert':
        return (
          <span className="px-2 py-0.5 rounded text-[11px] font-semibold bg-purple-50 text-purple-700 dark:bg-purple-950/60 dark:text-purple-300 border border-purple-200 dark:border-purple-800">
            Expert
          </span>
        );
    }
  };

  // Mini sparkline SVG renderer
  const renderSparkline = (profile: { distanceKm: number; elevationM: number }[]) => {
    if (!profile || profile.length < 2) return null;
    const minAlt = Math.min(...profile.map((p) => p.elevationM));
    const maxAlt = Math.max(...profile.map((p) => p.elevationM));
    const range = Math.max(1, maxAlt - minAlt);
    const maxDist = profile[profile.length - 1].distanceKm || 1;

    const w = 120;
    const h = 28;

    const pts = profile.map((p) => {
      const x = (p.distanceKm / maxDist) * w;
      const y = h - ((p.elevationM - minAlt) / range) * (h - 6) - 3;
      return `${x.toFixed(1)},${y.toFixed(1)}`;
    });

    const d = `M ${pts.join(' L ')}`;
    return (
      <svg
        viewBox={`0 0 ${w} ${h}`}
        className="w-28 h-7 overflow-visible inline-block"
        aria-hidden="true"
      >
        <path d={d} fill="none" stroke="#52B788" strokeWidth="1.75" strokeLinecap="round" />
      </svg>
    );
  };

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Editorial Header */}
      <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
        <div>
          <span className="text-xs font-semibold tracking-wider text-[var(--brand-primary)] uppercase">
            Topographie & Randonnée Responsable
          </span>
          <h2 className="font-['Fraunces'] text-2xl sm:text-3xl font-bold text-[var(--text-primary)] mt-1">
            Catalogue des Sentiers de la Réserve
          </h2>
          <p className="text-xs text-[var(--text-muted)] mt-1">
            Découvrez nos 6 parcours tracés dans le respect des aires de quiétude animale.
          </p>
        </div>

        <div className="text-xs font-mono text-[var(--text-muted)]">
          <strong>{filteredTrails.length}</strong> sentier{filteredTrails.length > 1 ? 's' : ''} affiché{filteredTrails.length > 1 ? 's' : ''} sur {trails.length}
        </div>
      </div>

      {/* Multicriteria Filter Bar Container */}
      <div className="p-4 sm:p-5 rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-default)] shadow-xs space-y-4">
        {/* Row 1: Search Input & PMR Toggle */}
        <div className="flex flex-col md:flex-row items-stretch md:items-center justify-between gap-3">
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-[var(--text-muted)] absolute left-3.5 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Rechercher par nom de sentier, biome, crête..."
              className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)] text-sm text-[var(--text-primary)] placeholder-[var(--text-muted)] focus:outline-none focus:ring-2 focus:ring-[var(--brand-primary)]"
            />
            {searchQuery && (
              <button
                type="button"
                onClick={() => setSearchQuery('')}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-xs text-[var(--text-muted)] hover:text-[var(--text-primary)]"
              >
                ✕
              </button>
            )}
          </div>

          {/* PMR Checkbox Toggle */}
          <label className="inline-flex items-center gap-2 px-3.5 py-2.5 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)] text-xs font-semibold text-[var(--text-primary)] cursor-pointer hover:bg-[var(--bg-surface)] transition-colors select-none">
            <input
              type="checkbox"
              checked={pmrOnly}
              onChange={(e) => setPmrOnly(e.target.checked)}
              className="rounded accent-[var(--brand-primary)] w-4 h-4 cursor-pointer"
            />
            <Accessibility className="w-4 h-4 text-[var(--brand-primary)]" />
            <span>Accessible PMR & Poussettes</span>
          </label>
        </div>

        {/* Row 2: Biome Selector, Difficulty Chips & Status Filter */}
        <div className="flex flex-wrap items-center justify-between gap-3 pt-2 border-t border-[var(--border-default)]/60 text-xs">
          <div className="flex flex-wrap items-center gap-2">
            <span className="font-mono text-[var(--text-muted)]">Biome :</span>
            <select
              value={selectedBiome}
              onChange={(e) => setSelectedBiome(e.target.value)}
              className="px-3 py-1.5 rounded-lg bg-[var(--bg-elevated)] border border-[var(--border-default)] text-xs text-[var(--text-primary)] focus:outline-none focus:ring-1 focus:ring-[var(--brand-primary)] cursor-pointer"
            >
              <option value="all">Tous les biomes</option>
              <option value="canopee">Canopée Primaire</option>
              <option value="cretes">Crêtes & Falaises</option>
              <option value="marais">Zone Humide & Marais</option>
              <option value="sous_bois">Sous-bois & Cascades</option>
              <option value="geologie">Éboulis Géologiques</option>
              <option value="vallon">Vallon Bocager</option>
            </select>

            <span className="font-mono text-[var(--text-muted)] ml-2">Difficulté :</span>
            <div className="inline-flex flex-wrap gap-1">
              {[
                { id: 'all', label: 'Toutes' },
                { id: 'facile', label: 'Facile' },
                { id: 'moyen', label: 'Modéré' },
                { id: 'difficile', label: 'Sportif' },
                { id: 'expert', label: 'Expert' },
              ].map((diff) => (
                <button
                  key={diff.id}
                  type="button"
                  onClick={() => setSelectedDifficulty(diff.id)}
                  className={`px-2.5 py-1 rounded-md text-[11px] font-semibold transition-colors cursor-pointer ${
                    selectedDifficulty === diff.id
                      ? 'bg-[var(--brand-primary)] text-white'
                      : 'bg-[var(--bg-elevated)] text-[var(--text-primary)] hover:bg-[var(--border-default)]'
                  }`}
                >
                  {diff.label}
                </button>
              ))}
            </div>

            <span className="font-mono text-[var(--text-muted)] ml-2">Statut :</span>
            <select
              value={selectedStatus}
              onChange={(e) => setSelectedStatus(e.target.value)}
              className="px-3 py-1.5 rounded-lg bg-[var(--bg-elevated)] border border-[var(--border-default)] text-xs text-[var(--text-primary)] focus:outline-none focus:ring-1 focus:ring-[var(--brand-primary)] cursor-pointer"
            >
              <option value="all">Tous les états</option>
              <option value="fluide">Fluide / Ouvert</option>
              <option value="balise">Balisé / Prudence</option>
              <option value="ferme">Fermé (Nidification)</option>
            </select>
          </div>

          {/* Reset Filters button */}
          {hasActiveFilters && (
            <button
              type="button"
              onClick={handleResetFilters}
              className="inline-flex items-center gap-1.5 px-2.5 py-1 text-xs text-[var(--text-muted)] hover:text-red-500 transition-colors cursor-pointer ml-auto"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              <span>Réinitialiser les filtres</span>
            </button>
          )}
        </div>
      </div>

      {/* Trail Cards Grid */}
      {filteredTrails.length === 0 ? (
        <div className="p-12 text-center rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-default)] space-y-3">
          <Trees className="w-10 h-10 text-[var(--text-muted)] mx-auto opacity-40" />
          <h3 className="font-['Fraunces'] text-lg font-bold text-[var(--text-primary)]">
            Aucun sentier ne correspond à vos filtres
          </h3>
          <p className="text-xs text-[var(--text-muted)]">
            Essayez d élargir vos critères de recherche ou réinitialisez les filtres.
          </p>
          <button
            type="button"
            onClick={handleResetFilters}
            className="px-4 py-2 rounded-xl bg-[var(--brand-primary)] text-white text-xs font-semibold cursor-pointer"
          >
            Afficher tous les sentiers
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredTrails.map((trail) => {
            const isSelected = selectedTrailId === trail.id;

            return (
              <div
                key={trail.id}
                className={`p-6 rounded-2xl bg-[var(--bg-surface)] border transition-all duration-200 flex flex-col justify-between ${
                  isSelected
                    ? 'border-[var(--brand-primary)] shadow-md ring-2 ring-[var(--brand-primary)]/20'
                    : 'border-[var(--border-default)] hover:shadow-xs'
                }`}
              >
                {/* Header: Status badge & Distance */}
                <div className="space-y-3">
                  <div className="flex items-center justify-between gap-2">
                    {renderStatusBadge(trail.status)}
                    <span className="text-xs font-mono font-bold text-[var(--text-primary)]">
                      {trail.lengthKm} km
                    </span>
                  </div>

                  <div>
                    <h3 className="font-['Fraunces'] text-lg font-bold text-[var(--text-primary)]">
                      {trail.name}
                    </h3>
                    <p className="text-xs text-[var(--text-muted)] italic font-serif mt-0.5">
                      {trail.subtitle}
                    </p>
                  </div>

                  <p className="text-xs text-[var(--text-muted)] leading-relaxed line-clamp-3">
                    {trail.description}
                  </p>

                  {/* Closure Notice Warning if Closed or Balisé */}
                  {trail.closureReason && (
                    <div className="p-3 rounded-xl bg-amber-500/10 dark:bg-amber-950/40 border border-amber-500/30 text-xs text-amber-800 dark:text-amber-200 space-y-1">
                      <div className="font-semibold flex items-center gap-1.5 text-amber-700 dark:text-amber-300">
                        <AlertTriangle className="w-3.5 h-3.5 shrink-0" />
                        <span>Avis Éco-Garde :</span>
                      </div>
                      <p className="text-[11px] leading-relaxed opacity-90">{trail.closureReason}</p>
                    </div>
                  )}

                  {/* Technical specs grid */}
                  <div className="grid grid-cols-4 gap-2 text-center text-xs font-mono pt-3 border-t border-[var(--border-default)]/60">
                    <div className="p-2 rounded-lg bg-[var(--bg-elevated)]">
                      <div className="text-[10px] text-[var(--text-muted)]">D+</div>
                      <div className="font-bold text-[var(--brand-primary)]">+{trail.elevationGainM}m</div>
                    </div>
                    <div className="p-2 rounded-lg bg-[var(--bg-elevated)]">
                      <div className="text-[10px] text-[var(--text-muted)]">Durée</div>
                      <div className="font-bold text-[var(--text-primary)]">
                        {Math.floor(trail.durationMin / 60)}h{trail.durationMin % 60 > 0 ? `${trail.durationMin % 60}` : '00'}
                      </div>
                    </div>
                    <div className="p-2 rounded-lg bg-[var(--bg-elevated)]">
                      <div className="text-[10px] text-[var(--text-muted)]">Niveau</div>
                      <div className="font-bold text-[var(--text-primary)] capitalize">
                        {renderDifficultyBadge(trail.difficulty)}
                      </div>
                    </div>
                    <div className="p-2 rounded-lg bg-[var(--bg-elevated)]">
                      <div className="text-[10px] text-[var(--text-muted)]">PMR</div>
                      <div className="font-bold text-[var(--text-primary)]">
                        {trail.pmrAccessible ? 'Oui' : 'Non'}
                      </div>
                    </div>
                  </div>

                  {/* Mini Sparkline & Biome indicator */}
                  <div className="pt-2 flex items-center justify-between text-xs text-[var(--text-muted)]">
                    <span className="font-mono text-[11px]">{trail.biomeLabel}</span>
                    {renderSparkline(trail.elevationProfile)}
                  </div>
                </div>

                {/* Bottom Actions: Voir sur la carte / Réserver */}
                <div className="pt-4 mt-4 border-t border-[var(--border-default)]/60 flex items-center gap-2">
                  <button
                    type="button"
                    onClick={() => {
                      setSelectedTrailId(trail.id);
                      if (onSelectTrailOnMap) {
                        onSelectTrailOnMap(trail.id);
                      }
                    }}
                    className={`flex-1 py-2 px-3 rounded-xl text-xs font-semibold transition-all flex items-center justify-center gap-1.5 cursor-pointer ${
                      isSelected
                        ? 'bg-[var(--brand-primary)] text-white shadow-xs'
                        : 'bg-[var(--bg-elevated)] hover:bg-[var(--brand-primary)] hover:text-white text-[var(--text-primary)] border border-[var(--border-default)]'
                    }`}
                  >
                    <Compass className="w-3.5 h-3.5" />
                    <span>{isSelected ? 'Sélectionné sur Carte' : 'Voir sur la Carte'}</span>
                  </button>

                  <button
                    type="button"
                    onClick={() => setActiveView('billetterie')}
                    disabled={trail.status === 'ferme'}
                    className={`py-2 px-3 rounded-xl text-xs font-semibold transition-all flex items-center justify-center gap-1.5 cursor-pointer ${
                      trail.status === 'ferme'
                        ? 'bg-[var(--bg-elevated)] text-[var(--text-muted)] opacity-50 cursor-not-allowed border border-[var(--border-default)]'
                        : 'bg-[#52B788] hover:bg-[#40916C] text-[#0B1D15] font-bold shadow-xs'
                    }`}
                    title={trail.status === 'ferme' ? 'Sentier fermé à la réservation' : 'Réserver un Éco-Pass pour ce sentier'}
                  >
                    <Ticket className="w-3.5 h-3.5" />
                    <span>Réserver</span>
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
