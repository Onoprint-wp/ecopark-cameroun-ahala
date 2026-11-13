// ============================================================================
// ECOPARK CAMEROUN (YAOUNDÉ – AHALA) — HERO CANOPY SECTION
// (src/components/discovery/HeroCanopy.tsx)
// Official Production Hero with Validated Texts, FCFA Tariffs, Photos & Telemetry
// ============================================================================

import React from 'react';
import { useEcoPark } from '../../context/EcoParkContext';
import { ImmersiveSection } from '../layout/ImmersiveSection';
import { recordMotionOrigin } from '../../utils/ecoMotion';
import { getPhotoObjectPosition } from '../../utils/ecoRouting';
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
  MapPin,
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
      className="py-12 sm:py-16 lg:py-20 relative overflow-hidden"
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

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-10 xl:gap-12 items-stretch">
        {/* Left Column: Official ECOPARK CAMEROUN Editorial Headline & Actions */}
        <div className="lg:col-span-7 flex flex-col justify-between space-y-5 text-center md:text-left">
          <div className="space-y-5">
            {/* Top Location Pill Tag */}
            <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-white/10 backdrop-blur-md border border-white/20 text-xs font-medium text-[#B7E4C7] shadow-xs">
              <MapPin className="w-4 h-4 text-[#74C69D] shrink-0" />
              <span className="font-mono tracking-tight">
                Yaoundé – Ahala Barrière (Face station Tradex, RN3) • À 15 min du Centre-Ville
              </span>
            </div>

            {/* Main Title in Barlow Semi Condensed */}
            <h1 className="font-['Barlow_Semi_Condensed'] text-3xl sm:text-5xl xl:text-6xl font-bold tracking-tight text-white leading-[1.08]">
              Le Plus Grand Complexe Écologique &amp; de Loisirs{' '}
              <span className="text-[#74C69D]">à Yaoundé – Ahala.</span>
            </h1>

            {/* Official Validated Subtitle in Source Sans 3 */}
            <p className="text-base sm:text-lg text-[#E9F5ED]/95 leading-relaxed font-sans">
              Jardin Zoologique (Gorille <strong>« ToTo »</strong>, chimpanzés, tortues), Balade en Pirogue sur le lac, Piscine Semi-Olympique, Manège Équestre, Restaurant gastronomique{' '}
              <strong>« Le Château des Saveurs »</strong> (07h–23h), <strong>30 Unités d&apos;Hébergement</strong> (Hôtels Ewondo, Chanthel &amp; Bene 24h/24) et <strong>CFP agréé MINEFOP</strong>.
            </p>

            {/* Official Price & Offer Cards (Full Width 3-Col Grid) */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-2.5 pt-1 text-left">
              <div className="px-3.5 py-2.5 rounded-xl bg-[#D4A373]/20 border border-[#D4A373]/50 text-[#F4E3CF]">
                <div className="text-[10px] font-mono uppercase tracking-wider text-[#EBD5BE]">Entrée Parc &amp; Zoo</div>
                <div className="font-['Barlow_Semi_Condensed'] font-bold text-base text-white mt-0.5">
                  1 000 FCFA Ad. · 500 FCFA Enf.
                </div>
              </div>
              <div className="px-3.5 py-2.5 rounded-xl bg-white/10 border border-white/20 text-white">
                <div className="text-[10px] font-mono uppercase tracking-wider text-[#B7E4C7]">3 Pass Tout-Inclus</div>
                <div className="font-['Barlow_Semi_Condensed'] font-bold text-base text-white mt-0.5">
                  2 500 · 4 500 · 8 500 FCFA
                </div>
              </div>
              <div className="px-3.5 py-2.5 rounded-xl bg-white/10 border border-white/20 text-white">
                <div className="text-[10px] font-mono uppercase tracking-wider text-[#B7E4C7]">Hôtels &amp; Suites 24h/24</div>
                <div className="font-['Barlow_Semi_Condensed'] font-bold text-base text-white mt-0.5">
                  10 000 à 45 000 FCFA / nuit
                </div>
              </div>
            </div>

            {/* Core CTAs */}
            <div className="pt-1 flex flex-wrap gap-3.5 justify-center md:justify-start">
              <button
                type="button"
                onClick={(e) => {
                  recordMotionOrigin(e);
                  setActiveView('billetterie');
                }}
                className="px-6 py-3.5 rounded-xl bg-[#52B788] hover:bg-[#40916C] text-[#0B1D15] font-bold text-sm shadow-lg hover:shadow-emerald-950/40 transition-all flex items-center gap-2 cursor-pointer active:scale-95 group focus:outline-none focus:ring-2 focus:ring-emerald-400"
              >
                <Ticket className="w-4 h-4 text-[#0B1D15] group-hover:rotate-12 transition-transform" />
                <span>Réserver mon Pass QR (dès 500 FCFA)</span>
                <span className="text-xs bg-[#1B4332]/20 px-2 py-0.5 rounded-md font-mono">
                  {availablePlaces} pl.
                </span>
              </button>

              <button
                type="button"
                onPointerDown={() => setSelectedTrailId('canopee')}
                onClick={(e) => {
                  recordMotionOrigin(e);
                  setSelectedTrailId('canopee');
                  setActiveView('sentiers');
                }}
                className="px-6 py-3.5 rounded-xl bg-white/10 hover:bg-white/20 text-white font-semibold text-sm border border-white/20 backdrop-blur-xs transition-all flex items-center gap-2 cursor-pointer active:scale-95 focus:outline-none focus:ring-2 focus:ring-white/50"
              >
                <Compass className="w-4 h-4 text-[#74C69D]" />
                <span>Plan du Parc &amp; 6 Circuits</span>
                <ArrowRight className="w-3.5 h-3.5 text-[#B7E4C7]" />
              </button>
            </div>
          </div>

          {/* Bottom Reassurance & Key Operational Metrics Bar */}
          <div className="pt-4 border-t border-white/15 flex flex-wrap items-center justify-center md:justify-between gap-3 text-xs text-[#C8E6D3]/95 font-sans">
            <span className="flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-[#52B788] shrink-0" />
              Orange Money (#150#) · MTN MoMo (*126#) · Guichet
            </span>
            <span className="flex items-center gap-1.5">
              <ShieldCheck className="w-4 h-4 text-[#52B788] shrink-0" />
              Garantie Météo RN3 (report 90j)
            </span>
            <span className="flex items-center gap-1.5">
              <Sparkles className="w-4 h-4 text-[#52B788] shrink-0" />
              Route 100% goudronnée &amp; Parking gratuit
            </span>
          </div>
        </div>

        {/* Right Column: Official Photos Mosaic + Live Ahala Telemetry Card */}
        <div className="lg:col-span-5 flex flex-col justify-between space-y-4">
          {/* 3-Photo Authentic Collage from Production (aspect-4/3 + face-safe objectPosition + non-overlapping caption bar) */}
          <div className="grid grid-cols-3 gap-3">
            <div className="flex flex-col rounded-xl overflow-hidden border border-white/20 shadow-md bg-[#121614]">
              <div className="relative aspect-[4/3] w-full overflow-hidden bg-[#1F2421]">
                <img
                  src="/images/ahala/balade_pirogue3.jpg"
                  alt="Balade en pirogue sur le lac d'Ahala"
                  className="w-full h-full object-cover"
                  style={{ objectPosition: getPhotoObjectPosition('/images/ahala/balade_pirogue3.jpg') }}
                />
              </div>
              <div className="px-2 py-1.5 bg-[#121614] border-t border-white/10 text-[10px] sm:text-[11px] font-bold text-[#E9F5ED] truncate text-center">
                Pirogue · 1 000 FCFA
              </div>
            </div>
            <div className="flex flex-col rounded-xl overflow-hidden border border-white/20 shadow-md bg-[#121614]">
              <div className="relative aspect-[4/3] w-full overflow-hidden bg-[#1F2421]">
                <img
                  src="/images/ahala/local_cameroon_gastronomy_pergola.png"
                  alt="Le Château des Saveurs à EcoPark Ahala"
                  className="w-full h-full object-cover"
                  style={{ objectPosition: getPhotoObjectPosition('/images/ahala/local_cameroon_gastronomy_pergola.png') }}
                />
              </div>
              <div className="px-2 py-1.5 bg-[#121614] border-t border-white/10 text-[10px] sm:text-[11px] font-bold text-[#E9F5ED] truncate text-center">
                Château des Saveurs
              </div>
            </div>
            <div className="flex flex-col rounded-xl overflow-hidden border border-white/20 shadow-md bg-[#121614]">
              <div className="relative aspect-[4/3] w-full overflow-hidden bg-[#1F2421]">
                <img
                  src="/images/ahala/chambre.jpeg"
                  alt="Hôtels Ewondo, Chanthel & Bene à EcoPark Cameroun"
                  className="w-full h-full object-cover"
                  style={{ objectPosition: getPhotoObjectPosition('/images/ahala/chambre.jpeg') }}
                />
              </div>
              <div className="px-2 py-1.5 bg-[#121614] border-t border-white/10 text-[10px] sm:text-[11px] font-bold text-[#E9F5ED] truncate text-center">
                Hôtels dès 10 000 FCFA
              </div>
            </div>
          </div>

          <div className="flex-1 p-5 sm:p-6 rounded-2xl bg-[#1F2421]/95 backdrop-blur-md border border-[#36403A] shadow-2xl text-white flex flex-col justify-between space-y-4">
            {/* Telemetry Header */}
            <div className="flex items-center justify-between border-b border-[#36403A] pb-3.5">
              <div className="flex items-center gap-2.5">
                <span className="relative flex h-3 w-3">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
                  <span className="relative inline-flex rounded-full h-3 w-3 bg-emerald-500" />
                </span>
                <span className="font-['Barlow_Semi_Condensed'] font-semibold text-base tracking-wide text-white">
                  État du Complexe d&apos;Ahala en Direct
                </span>
              </div>
              <span className="text-[11px] font-mono text-[#8EBAA0] bg-[#121614] px-2.5 py-1 rounded-md border border-[#29302C]">
                RN3 · Face Tradex
              </span>
            </div>

            {/* Quota Gauge with Dynamic Thresholds */}
            <div className="space-y-2">
              <div className="flex items-center justify-between text-xs font-mono">
                <span className="flex items-center gap-1.5 font-sans font-medium text-white">
                  <Users className="w-3.5 h-3.5 text-[#52B788]" />
                  Capacité Journalière du Parc
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
                <span>{availablePlaces} places restantes aujourd&apos;hui</span>
                <span>{telemetry.dailyCapacityMax} max</span>
              </div>
            </div>

            {/* 4 Telemetry Metrics Grid */}
            <div className="grid grid-cols-2 gap-3 pt-1">
              <div className="p-3 rounded-xl bg-[#29302C] border border-[#36403A]/80 flex flex-col justify-between">
                <div className="text-[11px] text-[#8EBAA0] flex items-center gap-1.5 font-sans">
                  <Wind className="w-3.5 h-3.5 text-sky-400" />
                  Air &amp; Microclimat
                </div>
                <div className="mt-1.5">
                  <div className="text-lg font-bold text-sky-300 font-mono">
                    IQA {telemetry.airQualityIqa}
                  </div>
                  <div className="text-[10px] text-[#C9D1CC] font-sans mt-0.5">
                    {telemetry.airQualityStatus} · Forêt d&apos;Ahala
                  </div>
                </div>
              </div>

              <div className="p-3 rounded-xl bg-[#29302C] border border-[#36403A]/80 flex flex-col justify-between">
                <div className="text-[11px] text-[#8EBAA0] flex items-center gap-1.5 font-sans">
                  <Sun className="w-3.5 h-3.5 text-amber-400" />
                  Autonomie &amp; Eau
                </div>
                <div className="mt-1.5">
                  <div className="text-lg font-bold text-amber-300 font-mono">
                    {telemetry.solarAutonomyPercent}%
                  </div>
                  <div className="text-[10px] text-[#C9D1CC] font-sans mt-0.5">
                    Solaire &amp; Groupe secours
                  </div>
                </div>
              </div>

              <div className="p-3 rounded-xl bg-[#29302C] border border-[#36403A]/80 flex flex-col justify-between">
                <div className="text-[11px] text-[#8EBAA0] flex items-center gap-1.5 font-sans">
                  <Leaf className="w-3.5 h-3.5 text-[#52B788]" />
                  Navettes &amp; Groupes
                </div>
                <div className="mt-1.5">
                  <div className="text-lg font-bold text-emerald-300 font-mono">
                    {telemetry.totalCo2AvoidedKg.toLocaleString('fr-FR')} kg
                  </div>
                  <div className="text-[10px] text-[#C9D1CC] font-sans mt-0.5">
                    CO₂ évité (Bus 5/18/32 pl.)
                  </div>
                </div>
              </div>

              <div className="p-3 rounded-xl bg-[#29302C] border border-[#36403A]/80 flex flex-col justify-between">
                <div className="text-[11px] text-[#8EBAA0] flex items-center gap-1.5 font-sans">
                  <Trees className="w-3.5 h-3.5 text-[#52B788]" />
                  Circuits du Parc
                </div>
                <div className="mt-1.5">
                  <div className="text-lg font-bold text-white font-mono">
                    {openTrailsCount} / {trails.length}
                  </div>
                  <div className="text-[10px] text-[#C9D1CC] font-sans mt-0.5">
                    {cautionedTrailsCount > 0 && `${cautionedTrailsCount} encadré · `}
                    {closedTrailsCount > 0 && `${closedTrailsCount} résidents VIP`}
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
