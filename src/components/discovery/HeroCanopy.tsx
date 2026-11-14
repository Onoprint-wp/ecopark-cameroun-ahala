// ============================================================================
// ECOPARK CAMEROUN (YAOUNDE - AHALA) - HERO CANOPY SECTION
// (src/components/discovery/HeroCanopy.tsx)
// Fiche mémo n°4 : Temps 3 (Point Final <= 12 mots + Rythme Ternaire + Preuve Visuelle)
// & Temps 5 (Tandem Asymétrique Double CTA : Pilule Simulateur + Lien Chevron ›)
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
  ShieldCheck,
  CheckCircle2,
  MapPin,
  PhoneCall,
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
      className="py-10 sm:py-14 lg:py-16 relative overflow-hidden"
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
        {/* Left Column : Optical Flagship Hierarchy + Ternary Rhythm + Double CTA */}
        <div className="lg:col-span-7 flex flex-col justify-between space-y-5 text-left">
          <div className="space-y-4">
            {/* Niveau 3 : Eyebrow (.type-eyebrow : 14px Desktop / 12px Mobile) */}
            <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-white/10 backdrop-blur-md border border-white/20 shadow-xs">
              <MapPin className="w-4 h-4 text-[#74C69D] shrink-0" />
              <span className="type-eyebrow !text-[#B7E4C7] tabular-nums">
                Yaoundé - Ahala Barrière (Face station Tradex, RN3) • À 15 min du centre
              </span>
            </div>

            {/* Niveau 4 : Titre Hero Principal (.type-hero : <= 12 mots + Point Final Catégorique, 0 cadratin) */}
            <h1 className="type-hero text-white">
              Complexe écologique et loisirs{' '}
              <span className="text-[#74C69D]">à Yaoundé, Ahala.</span>
            </h1>

            {/* Niveau 7 : Tagline en Rythme Ternaire (2 bénéfices ressentis + 1 preuve chiffrée vérifiable) */}
            <p className="type-tagline text-[#E9F5ED] tabular-nums">
              Respirez en forêt. Savourez au bord de l&apos;eau. 30 chambres et loisirs dès 500 FCFA.
            </p>

            {/* Niveau 8 : Corps éditorial fluide (.type-body : 17px/25px Desktop, 15px/22px Mobile) */}
            <p className="type-body text-[#E9F5ED]/90 max-w-3xl tabular-nums">
              Jardin Zoologique (Gorille <strong>« ToTo »</strong>, chimpanzés, tortues), pirogue sur le lac, piscine semi-olympique, manège équestre, restaurant{' '}
              <strong>« Le Château des Saveurs »</strong> (07h à 23h), hôtels Ewondo, Chanthel et Bene (24h/24) et <strong>CFP agréé MINEFOP</strong>.
            </p>

            {/* Price Framing Inversé : unité la plus accessible d'abord, tabular-nums strict */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-2.5 pt-1 tabular-nums">
              <div className="px-3.5 py-2.5 rounded-xl bg-[#D4A373]/20 border border-[#D4A373]/50 text-[#F4E3CF]">
                <div className="type-footnote !text-[#EBD5BE] uppercase font-semibold">Entrée Parc &amp; Zoo</div>
                <div className="font-bold text-base text-white mt-0.5 tabular-nums">
                  Dès 500 FCFA enf. · 1 000 FCFA ad.
                </div>
              </div>
              <div className="px-3.5 py-2.5 rounded-xl bg-white/10 border border-white/20 text-white">
                <div className="type-footnote !text-[#B7E4C7] uppercase font-semibold">3 Pass Tout-Inclus</div>
                <div className="font-bold text-base text-white mt-0.5 tabular-nums">
                  Dès 1 500 FCFA · 2 500 à 8 500 FCFA
                </div>
              </div>
              <div className="px-3.5 py-2.5 rounded-xl bg-white/10 border border-white/20 text-white">
                <div className="type-footnote !text-[#B7E4C7] uppercase font-semibold">30 Hôtels &amp; Suites 24h/24</div>
                <div className="font-bold text-base text-white mt-0.5 tabular-nums">
                  Dès 10 000 FCFA / nuit (ou 45 000 VIP)
                </div>
              </div>
            </div>

            {/* Niveau 9 & TEMPS 5 : Tandem Asymétrique « Double CTA » (Loi de Hick, >= 48px, +30% tolérance sur 375px) */}
            <div className="pt-2 flex flex-wrap items-center gap-3">
              {/* Visiteur Niveau 3/4 (Hésitant) : Pilule pleine -> Simulateur de Pass QR sans engagement */}
              <button
                type="button"
                onClick={(e) => {
                  recordMotionOrigin(e);
                  setActiveView('billetterie');
                }}
                className="cta-pill cta-pill-canopy shadow-lg hover:shadow-emerald-950/40 group focus:outline-none focus:ring-2 focus:ring-emerald-300"
              >
                <Ticket className="w-4 h-4 text-[#081C15] shrink-0 group-hover:rotate-12 transition-transform" />
                <span>Simuler mon Pass QR (dès 500 FCFA)</span>
                <span className="text-xs bg-[#081C15]/15 px-2 py-0.5 rounded-full font-mono tabular-nums">
                  {availablePlaces} pl.
                </span>
              </button>

              {/* Visiteur Niveau 5 (Décidé) : Lien discret à chevron -> Réservation directe WhatsApp pré-rempli */}
              <a
                href="https://wa.me/237672564598?text=Bonjour%20EcoPark%20Cameroun%2C%20je%20souhaite%20r%C3%A9server%20une%20visite%20ou%20un%20Pass%20%C3%A0%20Ahala."
                target="_blank"
                rel="noreferrer"
                className="cta-chevron cta-chevron-canopy border border-white/20"
              >
                <PhoneCall className="w-4 h-4 text-[#74C69D] shrink-0" />
                <span>Réserver sur WhatsApp</span>
                <span aria-hidden="true" className="text-base leading-none font-bold">›</span>
              </a>

              {/* Orientation visuelle secondaire */}
              <button
                type="button"
                onPointerDown={() => setSelectedTrailId('canopee')}
                onClick={(e) => {
                  recordMotionOrigin(e);
                  setSelectedTrailId('canopee');
                  setActiveView('sentiers');
                }}
                className="cta-chevron cta-chevron-canopy"
              >
                <Compass className="w-4 h-4 text-[#74C69D] shrink-0" />
                <span>Plan &amp; 6 circuits</span>
                <span aria-hidden="true" className="text-base leading-none font-bold">›</span>
              </button>
            </div>
          </div>

          {/* Niveau 10 : Réassurance factuelle (.type-footnote >= 4.5:1) */}
          <div className="pt-4 border-t border-white/15 flex flex-wrap items-center justify-between gap-3 type-footnote !text-[#D8F3DC] tabular-nums">
            <span className="flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-[#52B788] shrink-0" />
              Orange Money (#150#) · MTN MoMo (*126#) · Guichet
            </span>
            <span className="flex items-center gap-1.5">
              <ShieldCheck className="w-4 h-4 text-[#52B788] shrink-0" />
              Garantie Météo RN3 (report gratuit 90j)
            </span>
            <span className="flex items-center gap-1.5">
              <Sparkles className="w-4 h-4 text-[#52B788] shrink-0" />
              Route 100% goudronnée &amp; Parking gratuit
            </span>
          </div>
        </div>

        {/* Right Column : Preuve Visuelle Authentique (Face-Safe 4:3) + Télémétrie Temps Réel (tabular-nums) */}
        <div className="lg:col-span-5 flex flex-col justify-between space-y-4">
          {/* 3-Photo Authentic Collage (aspect-4/3 + face-safe objectPosition + non-overlapping caption bar) */}
          <div className="grid grid-cols-3 gap-3 tabular-nums">
            <div className="flex flex-col rounded-xl overflow-hidden border border-white/20 shadow-md bg-[#121614]">
              <div className="relative aspect-[4/3] w-full overflow-hidden bg-[#1F2421]">
                <img
                  src="/images/ahala/balade_pirogue3.jpg"
                  alt="Balade en pirogue sur le lac d'Ahala"
                  className="w-full h-full object-cover"
                  style={{ objectPosition: getPhotoObjectPosition('/images/ahala/balade_pirogue3.jpg') }}
                />
              </div>
              <div className="px-2 py-1.5 bg-[#121614] border-t border-white/10 text-[11px] font-bold text-[#E9F5ED] truncate text-center">
                Pirogue · 500 FCFA enf.
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
              <div className="px-2 py-1.5 bg-[#121614] border-t border-white/10 text-[11px] font-bold text-[#E9F5ED] truncate text-center">
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
              <div className="px-2 py-1.5 bg-[#121614] border-t border-white/10 text-[11px] font-bold text-[#E9F5ED] truncate text-center">
                Hôtels dès 10 000 FCFA
              </div>
            </div>
          </div>

          <div className="flex-1 p-5 sm:p-6 rounded-2xl bg-[#1F2421]/95 backdrop-blur-md border border-[#36403A] shadow-2xl text-white flex flex-col justify-between space-y-4 tabular-nums">
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
              <div className="flex items-center justify-between text-xs font-mono tabular-nums">
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

              <div className="flex justify-between text-[11px] font-mono text-[#B7E4C7] tabular-nums">
                <span>0</span>
                <span>{availablePlaces} places restantes aujourd&apos;hui</span>
                <span>{telemetry.dailyCapacityMax} max</span>
              </div>
            </div>

            {/* 4 Telemetry Metrics Grid */}
            <div className="grid grid-cols-2 gap-3 pt-1 tabular-nums">
              <div className="p-3 rounded-xl bg-[#29302C] border border-[#36403A]/80 flex flex-col justify-between">
                <div className="text-[11px] text-[#C9D1CC] flex items-center gap-1.5 font-sans">
                  <Wind className="w-3.5 h-3.5 text-sky-400" />
                  Air &amp; Microclimat
                </div>
                <div className="mt-1.5">
                  <div className="text-lg font-bold text-sky-300 font-mono tabular-nums">
                    IQA {telemetry.airQualityIqa}
                  </div>
                  <div className="text-[11px] text-[#C9D1CC] font-sans mt-0.5">
                    {telemetry.airQualityStatus} · Forêt d&apos;Ahala
                  </div>
                </div>
              </div>

              <div className="p-3 rounded-xl bg-[#29302C] border border-[#36403A]/80 flex flex-col justify-between">
                <div className="text-[11px] text-[#C9D1CC] flex items-center gap-1.5 font-sans">
                  <Sun className="w-3.5 h-3.5 text-amber-400" />
                  Autonomie &amp; Eau
                </div>
                <div className="mt-1.5">
                  <div className="text-lg font-bold text-amber-300 font-mono tabular-nums">
                    {telemetry.solarAutonomyPercent}%
                  </div>
                  <div className="text-[11px] text-[#C9D1CC] font-sans mt-0.5">
                    Solaire &amp; Groupe secours
                  </div>
                </div>
              </div>

              <div className="p-3 rounded-xl bg-[#29302C] border border-[#36403A]/80 flex flex-col justify-between">
                <div className="text-[11px] text-[#C9D1CC] flex items-center gap-1.5 font-sans">
                  <Leaf className="w-3.5 h-3.5 text-[#52B788]" />
                  Navettes &amp; Groupes
                </div>
                <div className="mt-1.5">
                  <div className="text-lg font-bold text-emerald-300 font-mono tabular-nums">
                    {telemetry.totalCo2AvoidedKg.toLocaleString('fr-FR')} kg
                  </div>
                  <div className="text-[11px] text-[#C9D1CC] font-sans mt-0.5">
                    CO₂ évité (Bus 5/18/32 pl.)
                  </div>
                </div>
              </div>

              <div className="p-3 rounded-xl bg-[#29302C] border border-[#36403A]/80 flex flex-col justify-between">
                <div className="text-[11px] text-[#C9D1CC] flex items-center gap-1.5 font-sans">
                  <Trees className="w-3.5 h-3.5 text-[#52B788]" />
                  Circuits du Parc
                </div>
                <div className="mt-1.5">
                  <div className="text-lg font-bold text-white font-mono tabular-nums">
                    {openTrailsCount} / {trails.length}
                  </div>
                  <div className="text-[11px] text-[#C9D1CC] font-sans mt-0.5">
                    {cautionedTrailsCount > 0 && `${cautionedTrailsCount} encadré · `}
                    {closedTrailsCount > 0 && `${closedTrailsCount} résidents VIP`}
                  </div>
                </div>
              </div>
            </div>

            {/* Weather snapshot footer */}
            <div className="pt-2 border-t border-[#36403A] flex items-center justify-between text-xs text-[#C9D1CC] font-sans tabular-nums">
              <span className="flex items-center gap-1.5">
                <span className="w-2 h-2 rounded-full bg-amber-400" />
                {telemetry.weatherCondition}
              </span>
              <span className="font-mono text-white font-semibold tabular-nums">
                {telemetry.temperatureC}°C · {telemetry.humidityPercent}% hum.
              </span>
            </div>
          </div>
        </div>
      </div>
    </ImmersiveSection>
  );
};
