// ============================================================================
// ECOPARK CAMEROUN (YAOUNDÉ – AHALA) — APPLICATION SHELL & VIEW ROUTER
// (src/App.tsx)
// ============================================================================

import { useState } from 'react';
import { Navbar } from './components/layout/Navbar';
import { Footer } from './components/layout/Footer';
import { ImmersiveSection } from './components/layout/ImmersiveSection';
import { HeroCanopy } from './components/discovery/HeroCanopy';
import { ImpactBanner } from './components/discovery/ImpactBanner';
import { AhalaShowcase } from './components/discovery/AhalaShowcase';
import { InteractiveTopoMap } from './components/map/InteractiveTopoMap';
import { ElevationProfile, ScrubPayload } from './components/map/ElevationProfile';
import { TrailCatalog } from './components/trails/TrailCatalog';
import { SpeciesAtlas } from './components/biodiversity/SpeciesAtlas';
import { BookingWizard } from './components/booking/BookingWizard';
import { DigitalEcoPass } from './components/booking/DigitalEcoPass';
import { CitizenSentinel } from './components/field/CitizenSentinel';
import { RangerDashboard } from './components/admin/RangerDashboard';
import { ColorAtlasDrawer } from './components/design-system/ColorAtlasDrawer';
import { useEcoPark } from './context/EcoParkContext';
import { recordMotionOrigin, useEcoMotion } from './utils/ecoMotion';
import {
  Compass,
  Ticket,
  QrCode,
  CheckCircle2,
  AlertTriangle,
  XCircle,
  ChevronRight,
} from 'lucide-react';
import { TrailStatus } from './types/ecosystem';

export default function App() {
  const {
    activeView,
    setActiveView,
    effectiveTheme,
    telemetry,
    trails,
    selectedTrailId,
    setSelectedTrailId,
    species,
    setSelectedSpeciesId,
  } = useEcoPark();

  // Global kinetic sobriety governance (tab visibility, OLED pause, reduced-motion)
  useEcoMotion(effectiveTheme === 'dark');

  const [scrubPoint, setScrubPoint] = useState<ScrubPayload | null>(null);
  const spotlightTrailId = selectedTrailId || trails[0]?.id || null;

  // Status helper badges
  const renderTrailStatusBadge = (status: TrailStatus) => {
    switch (status) {
      case 'fluide':
        return (
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800 dark:bg-emerald-950/80 dark:text-emerald-300 border border-emerald-300 dark:border-emerald-800">
            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" />
            Ouvert / Fluide
          </span>
        );
      case 'balise':
        return (
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-amber-100 text-amber-800 dark:bg-amber-950/80 dark:text-amber-300 border border-amber-300 dark:border-amber-800">
            <AlertTriangle className="w-3.5 h-3.5 text-amber-600 dark:text-amber-400" />
            Accès Encadré
          </span>
        );
      case 'ferme':
        return (
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-red-100 text-red-800 dark:bg-red-950/80 dark:text-red-300 border border-red-300 dark:border-red-800">
            <XCircle className="w-3.5 h-3.5 text-red-600 dark:text-red-400" />
            Réservé Résidents / VIP
          </span>
        );
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-[var(--bg-canvas)] text-[var(--text-primary)] antialiased transition-colors duration-200">
      {/* Sticky Navigation Header */}
      <Navbar />

      {/* Main View Router Content */}
      <main className="eco-main-stage flex-1 w-full" id="main-content">
        {/* ================================================================= */}
        {/* VUE 1 : ACCUEIL & LES 5 PÔLES D'ECOPARK CAMEROUN (YAOUNDÉ-AHALA)  */}
        {/* ================================================================= */}
        {activeView === 'accueil' && (
          <div className="eco-view-enter pb-16">
            {/* Full-Bleed Immersive Header Stack (Zero White Gap Between Hero & ImpactBanner) */}
            <div>
              {/* Hero Canopy Section (F14) */}
              <HeroCanopy />

              {/* 4 Pillars & Official Production Metrics (F15) */}
              <ImpactBanner />
            </div>

            <div className="space-y-14 pt-12">
              {/* Validated Production Showcase: Hotels (30), Château des Saveurs, Tariffs, B2B & CFP MINEFOP */}
              <AhalaShowcase />

              {/* Quick Circuits & Zones Showcase */}
              <div className="eco-container space-y-6">
                <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
                  <div>
                    <span className="text-xs font-semibold tracking-wider text-[var(--brand-primary)] uppercase">
                      Orientation &amp; Plan du Domaine d&apos;Ahala
                    </span>
                    <h2 className="font-['Barlow_Semi_Condensed'] text-2xl sm:text-3xl font-bold text-[var(--text-primary)] mt-1">
                      Les 6 Circuits &amp; Secteurs Officiels du Parc
                    </h2>
                  </div>
                  <button
                    onClick={(e) => {
                      recordMotionOrigin(e);
                      setActiveView('sentiers');
                    }}
                    className="inline-flex items-center gap-1 text-sm font-semibold text-[var(--brand-primary)] hover:underline cursor-pointer"
                  >
                    <span>Ouvrir la carte interactive complète du domaine</span>
                    <ChevronRight className="w-4 h-4" />
                  </button>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {trails.map((trail) => (
                    <div
                      key={trail.id}
                      onPointerDown={() => setSelectedTrailId(trail.id)}
                      onClick={(e) => {
                        recordMotionOrigin(e);
                        setSelectedTrailId(trail.id);
                        setActiveView('sentiers');
                      }}
                      className={`${
                        spotlightTrailId === trail.id ? 'vt-trail-spotlight ' : ''
                      }p-5 rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-default)] hover:shadow-md hover:-translate-y-0.5 transition-all cursor-pointer group flex flex-col justify-between`}
                    >
                      <div className="space-y-3">
                        <div className="flex items-center justify-between gap-2">
                          {renderTrailStatusBadge(trail.status)}
                          <span className="text-xs font-mono font-medium text-[var(--text-muted)]">
                            {trail.lengthKm} km · {Math.floor(trail.durationMin / 60)}h{trail.durationMin % 60 > 0 ? `${trail.durationMin % 60}` : '00'}
                          </span>
                        </div>

                        <h3 className="font-['Barlow_Semi_Condensed'] text-lg font-bold text-[var(--text-primary)] group-hover:text-[var(--brand-primary)] transition-colors">
                          {trail.name}
                        </h3>

                        <p className="text-xs text-[var(--text-muted)] line-clamp-2 leading-relaxed">
                          {trail.description}
                        </p>
                      </div>

                      <div className="pt-4 mt-4 border-t border-[var(--border-default)]/60 flex items-center justify-between text-xs text-[var(--text-muted)]">
                        <span className="truncate pr-2">{trail.biomeLabel}</span>
                        <span className="font-mono text-[var(--text-primary)] font-semibold shrink-0">Alt. {trail.maxElevationM}m</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Quick Zoological & Heritage Showcase */}
              <div className="eco-container space-y-6 pt-2">
                <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
                  <div>
                    <span className="text-xs font-semibold tracking-wider text-[var(--brand-primary)] uppercase">
                      Jardin Zoologique &amp; Patrimoine Vivant d&apos;Ahala
                    </span>
                    <h2 className="font-['Barlow_Semi_Condensed'] text-2xl sm:text-3xl font-bold text-[var(--text-primary)] mt-1">
                      Gorille « ToTo », Chimpanzés, Bassins Piscicoles &amp; Flore
                    </h2>
                  </div>
                  <button
                    onClick={(e) => {
                      recordMotionOrigin(e);
                      setSelectedSpeciesId(null);
                      setActiveView('biodiversite');
                    }}
                    className="inline-flex items-center gap-1 text-sm font-semibold text-[var(--brand-primary)] hover:underline cursor-pointer"
                  >
                    <span>Consulter les 8 fiches du Jardin Zoologique &amp; Biodiversité</span>
                    <ChevronRight className="w-4 h-4" />
                  </button>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
                  {species.slice(0, 4).map((sp) => (
                    <div
                      key={sp.id}
                      onClick={(e) => {
                        recordMotionOrigin(e);
                        setSelectedSpeciesId(sp.id);
                        setActiveView('biodiversite');
                      }}
                      className="rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-default)] hover:shadow-md hover:-translate-y-0.5 transition-all cursor-pointer group overflow-hidden flex flex-col justify-between"
                    >
                      {sp.photoUrl && (
                        <div className="h-40 w-full overflow-hidden bg-[#1F2421]">
                          <img
                            src={sp.photoUrl}
                            alt={sp.commonName}
                            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                          />
                        </div>
                      )}
                      <div className="p-4">
                        <div className="text-xs font-mono text-[var(--brand-primary)] font-semibold uppercase">
                          {sp.categoryLabel}
                        </div>
                        <div className="font-['Barlow_Semi_Condensed'] font-bold text-base text-[var(--text-primary)] mt-1 group-hover:text-[var(--brand-primary)]">
                          {sp.commonName}
                        </div>
                        <div className="text-[11px] italic text-[var(--text-muted)]">
                          {sp.scientificName}
                        </div>
                        <div className="mt-3 inline-block px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-[var(--bg-elevated)] border border-[var(--border-default)] text-[var(--text-primary)]">
                          Statut : {sp.iucnStatus} · {sp.iucnLabel}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ================================================================= */}
        {/* VUE 2 : CARTE INTERACTIVE DU DOMAINE D'AHALA & 6 CIRCUITS         */}
        {/* ================================================================= */}
        {activeView === 'sentiers' && (
          <div className="eco-view-enter space-y-10 pb-16">
            <ImmersiveSection variant="forest" className="py-10">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div className="space-y-1">
                  <div className="inline-flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-[#B7E4C7]">
                    <Compass className="w-4 h-4 text-[#74C69D]" />
                    <span>Cartographie Interactive d&apos;ECOPARK CAMEROUN (Yaoundé – Ahala, RN3)</span>
                  </div>
                  <h1 className="font-['Barlow_Semi_Condensed'] text-2xl sm:text-4xl font-bold text-white mt-1">
                    Plan du Parc, 10 Pôles &amp; 6 Circuits Officiels
                  </h1>
                </div>
                <div className="text-xs text-[#E9F5ED]/80 font-mono bg-[#1F2421]/80 px-3 py-2 rounded-xl border border-[#36403A]">
                  Zoo Gorille ToTo · Lac &amp; Pirogues · Piscine Semi-Olympique · Cités Hôtelières · CFP MINEFOP
                </div>
              </div>
            </ImmersiveSection>

            <div className="eco-container space-y-10">
              {/* Interactive Topographic Map (F16) */}
              <InteractiveTopoMap scrubPoint={scrubPoint} />

              {/* Synchronized Elevation Profile with Scrubber (F17) — Shared Element Target */}
              <ElevationProfile onScrub={setScrubPoint} className="vt-trail-spotlight" />

              {/* Trail Catalog & Multicriteria Filters (F18) */}
              <TrailCatalog
                onSelectTrailOnMap={(trailId) => {
                  setSelectedTrailId(trailId);
                  window.scrollTo({ top: 0, behavior: 'smooth' });
                }}
              />
            </div>
          </div>
        )}

        {/* ================================================================= */}
        {/* VUE 3 : JARDIN ZOOLOGIQUE & BIODIVERSITÉ D'AHALA (F19)            */}
        {/* ================================================================= */}
        {activeView === 'biodiversite' && (
          <div className="eco-view-enter">
            <SpeciesAtlas />
          </div>
        )}

        {/* ================================================================= */}
        {/* VUE 4 : BILLETTERIE & PASS TOUT-INCLUS EN FCFA (F20, F21)         */}
        {/* ================================================================= */}
        {activeView === 'billetterie' && (
          <div className="eco-view-enter space-y-8 pb-16">
            <ImmersiveSection variant="canopy" className="py-10">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                  <div className="inline-flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-[#B7E4C7]">
                    <Ticket className="w-4 h-4 text-[#74C69D]" />
                    <span>Billetterie Officielle en FCFA · Orange Money (#150#) · MTN MoMo (*126#) · Guichet</span>
                  </div>
                  <h1 className="font-['Barlow_Semi_Condensed'] text-2xl sm:text-4xl font-bold text-white mt-1">
                    Réserver votre Pass QR Code — ECOPARK CAMEROUN (Yaoundé – Ahala)
                  </h1>
                </div>
                <div className="text-xs text-[#E9F5ED]/80 font-mono bg-[#0B1D15]/60 px-3 py-2 rounded-xl border border-[#36403A]">
                  Places disponibles aujourd&apos;hui : {Math.max(0, telemetry.dailyCapacityMax - telemetry.currentOccupancy)} / {telemetry.dailyCapacityMax}
                </div>
              </div>
            </ImmersiveSection>

            <div className="eco-container">
              <BookingWizard />
            </div>
          </div>
        )}

        {/* ================================================================= */}
        {/* VUE 5 : MON PASS QR (ECP-2026-XXXXX) & AVIS VISITEURS (F22..F25)  */}
        {/* ================================================================= */}
        {activeView === 'pass' && (
          <div className="eco-view-enter space-y-10 pb-16">
            <ImmersiveSection variant="bark" className="py-10">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                  <div className="inline-flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-[#74C69D]">
                    <QrCode className="w-4 h-4 text-[#52B788]" />
                    <span>Espace Visiteur &amp; Pass QR Code (ECP-2026-XXXXX)</span>
                  </div>
                  <h1 className="font-['Barlow_Semi_Condensed'] text-2xl sm:text-4xl font-bold text-white mt-1">
                    Mon Pass QR &amp; Retours d&apos;Expérience à Ahala
                  </h1>
                </div>
                <div className="text-xs text-[#E9F5ED]/80 font-mono bg-[#121614]/80 px-3 py-2 rounded-xl border border-[#36403A]">
                  Garantie Météo RN3 (Report gratuit 90j) · Mode Plein Soleil &amp; OLED
                </div>
              </div>
            </ImmersiveSection>

            <div className="eco-container space-y-12">
              {/* Feature F22 & F23: Interactive Digital Eco-Pass Card */}
              <section aria-label="Mon Éco-Pass Actif">
                <DigitalEcoPass />
              </section>

              {/* Feature F24 & F25: Citizen Sentinel Field Form & Community Feed */}
              <section aria-label="Sentinelle Nature &amp; Veille Participative" className="pt-6 border-t border-[var(--border-default)]">
                <CitizenSentinel />
              </section>
            </div>
          </div>
        )}

        {/* ================================================================= */}
        {/* VUE 6 : CONSOLE DE SUPERVISION ÉCO-GARDE (F26, F27, F28)          */}
        {/* ================================================================= */}
        {activeView === 'ranger' && (
          <div className="eco-view-enter">
            <RangerDashboard />
          </div>
        )}
      </main>

      {/* Slide-over Color Atlas Drawer & WCAG Tester (F29, F30) */}
      <ColorAtlasDrawer />

      {/* Ecological Footer */}
      <Footer />
    </div>
  );
}
