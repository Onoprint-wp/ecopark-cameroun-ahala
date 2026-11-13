// ============================================================================
// ECO-PARK HERO CANOPY SECTION (src/components/discovery/HeroCanopy.tsx)
// Feature F14 — Editorial Hero Canopy with Dynamic Quota Telemetry & CTAs
// ============================================================================

import React from 'react';
import { useEcoPark } from '../../context/EcoParkContext';
import { ImmersiveSection } from '../layout/ImmersiveSection';
import {
  Sparkles,
  Ticket,
  Compass,
  Users,
  Wind,
  Sun,
  Leaf,
  Trees,
  ArrowRight,
  ShieldCheck,
  CheckCircle2,
} from 'lucide-react';

export const HeroCanopy: React.FC = () => {
  const { telemetry, trails, setActiveView, setSelectedTrailId } = useEcoPark();

  const openTrailsCount = trails.filter((t) => t.status === 'fluide').length;
  const cautionedTrailsCount = trails.filter((t) => t.status === 'balise').length;
  const closedTrailsCount = trails.filter((t) => t.status === 'ferme').length;

  const availablePlaces = Math.max(0, telemetry.dailyCapacityMax - telemetry.currentOccupancy);
  const occupancyRatio = Math.min(
    100,
    Math.round((telemetry.currentOccupancy / telemetry.dailyCapacityMax) * 100)
  );

  return (
    <ImmersiveSection
      variant="canopy"
      className="py-14 sm:py-20 lg:py-24 relative overflow-hidden"
      containerClassName="relative z-10"
    >
      {/* Subtle organic background decoration */}
      <div
        className="absolute -top-24 -right-24 w-96 h-96 rounded-full bg-emerald-500/10 blur-3xl pointer-events-none"
        aria-hidden="true"
      />
      <div
        className="absolute -bottom-24 -left-24 w-80 h-80 rounded-full bg-emerald-800/20 blur-3xl pointer-events-none"
        aria-hidden="true"
      />

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 lg:gap-14 items-center">
        {/* Left Column: Editorial Headline & Actions */}
        <div className="lg:col-span-7 space-y-6 text-center md:text-left">
          {/* Top Pill Tag */}
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-white/10 backdrop-blur-md border border-white/20 text-xs font-medium text-[#B7E4C7] shadow-xs">
            <Sparkles className="w-4 h-4 text-[#74C69D] animate-pulse" />
            <span className="font-mono tracking-tight">
              Réserve Biologique Intégrale · 420 Hectares Préservés
            </span>
          </div>

          {/* Main Title in Fraunces */}
          <h1 className="font-['Fraunces'] text-3xl sm:text-5xl lg:text-6xl font-bold tracking-tight text-white leading-[1.12]">
            Explorez le sanctuaire, <br className="hidden sm:inline" />
            <span className="text-[#74C69D] italic font-serif">en harmonie avec la Terre.</span>
          </h1>

          {/* Subtitle in DM Sans */}
          <p className="text-base sm:text-lg text-[#E9F5ED]/90 max-w-2xl leading-relaxed mx-auto md:mx-0 font-sans">
            Un écosystème forestier protégé régulé par un quota écologique strict.
            Parcourez 6 sentiers d altitude cartographiés en SVG haute précision, découvrez 8 espèces
            endémiques protégées et accédez à notre billetterie décarbonée à impact positif.
          </p>

          {/* Core CTAs */}
          <div className="pt-2 flex flex-wrap gap-3.5 justify-center md:justify-start">
            <button
              type="button"
              onClick={() => setActiveView('billetterie')}
              className="px-6 py-3.5 rounded-xl bg-[#52B788] hover:bg-[#40916C] text-[#0B1D15] font-bold text-sm shadow-lg hover:shadow-emerald-950/40 transition-all flex items-center gap-2 cursor-pointer active:scale-95 group focus:outline-none focus:ring-2 focus:ring-emerald-400"
            >
              <Ticket className="w-4 h-4 text-[#0B1D15] group-hover:rotate-12 transition-transform" />
              <span>Réserver un Éco-Pass</span>
              <span className="text-xs bg-[#1B4332]/20 px-2 py-0.5 rounded-md font-mono">
                {availablePlaces} dispo
              </span>
            </button>

            <button
              type="button"
              onClick={() => {
                setSelectedTrailId('canopee');
                setActiveView('sentiers');
              }}
              className="px-6 py-3.5 rounded-xl bg-white/10 hover:bg-white/20 text-white font-semibold text-sm border border-white/20 backdrop-blur-xs transition-all flex items-center gap-2 cursor-pointer active:scale-95 focus:outline-none focus:ring-2 focus:ring-white/50"
            >
              <Compass className="w-4 h-4 text-[#74C69D]" />
              <span>Explorer la Carte & Sentiers</span>
              <ArrowRight className="w-3.5 h-3.5 text-[#B7E4C7]" />
            </button>
          </div>

          {/* Value props reassurance */}
          <div className="pt-4 flex flex-wrap items-center justify-center md:justify-start gap-4 sm:gap-6 text-xs text-[#C8E6D3]/80 font-sans">
            <span className="flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-[#52B788]" />
              Zéro déchet imposé
            </span>
            <span className="flex items-center gap-1.5">
              <ShieldCheck className="w-4 h-4 text-[#52B788]" />
              Accompagnement éco-gardes
            </span>
            <span className="flex items-center gap-1.5">
              <Sun className="w-4 h-4 text-[#52B788]" />
              Énergie 100% renouvelable
            </span>
          </div>
        </div>

        {/* Right Column: Live Reserve Telemetry Snapshot Card */}
        <div className="lg:col-span-5">
          <div className="p-6 sm:p-7 rounded-2xl bg-[#1F2421]/95 backdrop-blur-md border border-[#36403A] shadow-2xl text-white space-y-5">
            {/* Telemetry Header */}
            <div className="flex items-center justify-between border-b border-[#36403A] pb-4">
              <div className="flex items-center gap-2.5">
                <span className="relative flex h-3 w-3">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
                  <span className="relative inline-flex rounded-full h-3 w-3 bg-emerald-500" />
                </span>
                <span className="font-['Fraunces'] font-semibold text-base tracking-wide text-white">
                  Télémétrie en Direct
                </span>
              </div>
              <span className="text-[11px] font-mono text-[#8EBAA0] bg-[#121614] px-2.5 py-1 rounded-md border border-[#29302C]">
                Capteurs temps réel
              </span>
            </div>

            {/* Quota Gauge with Dynamic Thresholds */}
            <div className="space-y-2">
              <div className="flex items-center justify-between text-xs font-mono">
                <span className="flex items-center gap-1.5 font-sans font-medium text-white">
                  <Users className="w-3.5 h-3.5 text-[#52B788]" />
                  Quota Quotidien du Parc
                </span>
                <span className="text-[#C9D1CC]">
                  <strong className="text-white">{telemetry.currentOccupancy}</strong> / {telemetry.dailyCapacityMax} (
                  <span
                    className={
                      occupancyRatio >= 90
                        ? 'text-red-400 font-bold'
                        : occupancyRatio >= 70
                        ? 'text-amber-400 font-bold'
                        : 'text-emerald-400 font-bold'
                    }
                  >
                    {occupancyRatio}%
                  </span>
                  )
                </span>
              </div>

              {/* Progress Track */}
              <div className="w-full h-3 bg-[#121614] rounded-full overflow-hidden p-0.5 border border-[#36403A]">
                <div
                  className={`h-full rounded-full transition-all duration-700 ease-out ${
                    occupancyRatio >= 90
                      ? 'bg-red-500'
                      : occupancyRatio >= 70
                      ? 'bg-amber-500'
                      : 'bg-[#52B788]'
                  }`}
                  style={{ width: `${occupancyRatio}%` }}
                />
              </div>

              <div className="flex justify-between text-[10px] font-mono text-[#8EBAA0]">
                <span>0</span>
                <span>{availablePlaces} places restantes aujourd hui</span>
                <span>{telemetry.dailyCapacityMax} max</span>
              </div>
            </div>

            {/* 4 Telemetry Metrics Grid */}
            <div className="grid grid-cols-2 gap-3 pt-1">
              {/* Air Quality */}
              <div className="p-3.5 rounded-xl bg-[#29302C] border border-[#36403A]/80 flex flex-col justify-between">
                <div className="text-[11px] text-[#8EBAA0] flex items-center gap-1.5 font-sans">
                  <Wind className="w-3.5 h-3.5 text-sky-400" />
                  Qualité de l Air
                </div>
                <div className="mt-2">
                  <div className="text-xl font-bold text-sky-300 font-mono">
                    IQA {telemetry.airQualityIqa}
                  </div>
                  <div className="text-[10px] text-[#C9D1CC] font-sans mt-0.5">
                    {telemetry.airQualityStatus} · Purifié
                  </div>
                </div>
              </div>

              {/* Solar Autonomy */}
              <div className="p-3.5 rounded-xl bg-[#29302C] border border-[#36403A]/80 flex flex-col justify-between">
                <div className="text-[11px] text-[#8EBAA0] flex items-center gap-1.5 font-sans">
                  <Sun className="w-3.5 h-3.5 text-amber-400" />
                  Solaire & Réseau
                </div>
                <div className="mt-2">
                  <div className="text-xl font-bold text-amber-300 font-mono">
                    {telemetry.solarAutonomyPercent}%
                  </div>
                  <div className="text-[10px] text-[#C9D1CC] font-sans mt-0.5">
                    Autonomie énergétique
                  </div>
                </div>
              </div>

              {/* CO2 Avoided */}
              <div className="p-3.5 rounded-xl bg-[#29302C] border border-[#36403A]/80 flex flex-col justify-between">
                <div className="text-[11px] text-[#8EBAA0] flex items-center gap-1.5 font-sans">
                  <Leaf className="w-3.5 h-3.5 text-[#52B788]" />
                  CO₂ Évité Cumulé
                </div>
                <div className="mt-2">
                  <div className="text-xl font-bold text-emerald-300 font-mono">
                    {telemetry.totalCo2AvoidedKg.toLocaleString('fr-FR')} kg
                  </div>
                  <div className="text-[10px] text-[#C9D1CC] font-sans mt-0.5">
                    Éco-mobilité active
                  </div>
                </div>
              </div>

              {/* Open Trails */}
              <div className="p-3.5 rounded-xl bg-[#29302C] border border-[#36403A]/80 flex flex-col justify-between">
                <div className="text-[11px] text-[#8EBAA0] flex items-center gap-1.5 font-sans">
                  <Trees className="w-3.5 h-3.5 text-[#52B788]" />
                  Sentiers du Parc
                </div>
                <div className="mt-2">
                  <div className="text-xl font-bold text-white font-mono">
                    {openTrailsCount} / {trails.length}
                  </div>
                  <div className="text-[10px] text-[#C9D1CC] font-sans mt-0.5">
                    {cautionedTrailsCount > 0 && `${cautionedTrailsCount} balisé · `}
                    {closedTrailsCount > 0 && `${closedTrailsCount} fermé (nidification)`}
                  </div>
                </div>
              </div>
            </div>

            {/* Weather snapshot footer */}
            <div className="pt-2 border-t border-[#36403A] flex items-center justify-between text-xs text-[#8EBAA0] font-sans">
              <span className="flex items-center gap-1.5">
                <span className="w-2 h-2 rounded-full bg-amber-400" />
                {telemetry.weatherCondition}
              </span>
              <span className="font-mono text-white font-semibold">
                {telemetry.temperatureC}°C · {telemetry.humidityPercent}% hum.
              </span>
            </div>
          </div>
        </div>
      </div>
    </ImmersiveSection>
  );
};
