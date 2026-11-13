// ============================================================================
// ECO-PARK APPLICATION SHELL & VIEW ROUTER (src/App.tsx)
// ============================================================================

import { useState } from 'react';
import { Navbar } from './components/layout/Navbar';
import { Footer } from './components/layout/Footer';
import { ImmersiveSection } from './components/layout/ImmersiveSection';
import { HeroCanopy } from './components/discovery/HeroCanopy';
import { ImpactBanner } from './components/discovery/ImpactBanner';
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
    telemetry,
    trails,
    setSelectedTrailId,
    species,
  } = useEcoPark();

  const [scrubPoint, setScrubPoint] = useState<ScrubPayload | null>(null);

  // Status helper badges
  const renderTrailStatusBadge = (status: TrailStatus) => {
    switch (status) {
      case 'fluide':
        return (
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800 dark:bg-emerald-950/80 dark:text-emerald-300 border border-emerald-300 dark:border-emerald-800">
            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" />
            Fluide / Ouvert
          </span>
        );
      case 'balise':
        return (
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-amber-100 text-amber-800 dark:bg-amber-950/80 dark:text-amber-300 border border-amber-300 dark:border-amber-800">
            <AlertTriangle className="w-3.5 h-3.5 text-amber-600 dark:text-amber-400" />
            Balisé / Prudence
          </span>
        );
      case 'ferme':
        return (
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-red-100 text-red-800 dark:bg-red-950/80 dark:text-red-300 border border-red-300 dark:border-red-800">
            <XCircle className="w-3.5 h-3.5 text-red-600 dark:text-red-400" />
            Fermé / Protection
          </span>
        );
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-[var(--bg-canvas)] text-[var(--text-primary)] antialiased transition-colors duration-200">
      {/* Sticky Navigation Header */}
      <Navbar />

      {/* Main View Router Content */}
      <main className="flex-1 w-full" id="main-content">
        {/* ================================================================= */}
        {/* VUE 1 : ACCUEIL & DÉCOUVERTE                                      */}
        {/* ================================================================= */}
        {activeView === 'accueil' && (
          <div className="space-y-12 pb-16">
            {/* Hero Canopy Section (F14) */}
            <HeroCanopy />

            {/* Environmental Impact Banner (F15) */}
            <ImpactBanner />

            {/* Quick Trails Showcase */}
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-6">
              <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
                <div>
                  <span className="text-xs font-semibold tracking-wider text-[var(--brand-primary)] uppercase">
                    Cartographie & Topographie
                  </span>
                  <h2 className="font-['Fraunces'] text-2xl sm:text-3xl font-bold text-[var(--text-primary)] mt-1">
                    Les 6 Sentiers Officiels de la Réserve
                  </h2>
                </div>
                <button
                  onClick={() => setActiveView('sentiers')}
                  className="inline-flex items-center gap-1 text-sm font-semibold text-[var(--brand-primary)] hover:underline cursor-pointer"
                >
                  <span>Ouvrir la carte interactive complète</span>
                  <ChevronRight className="w-4 h-4" />
                </button>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {trails.map((trail) => (
                  <div
                    key={trail.id}
                    onClick={() => {
                      setSelectedTrailId(trail.id);
                      setActiveView('sentiers');
                    }}
                    className="p-5 rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-default)] hover:shadow-md transition-all cursor-pointer group flex flex-col justify-between"
                  >
                    <div className="space-y-3">
                      <div className="flex items-center justify-between gap-2">
                        {renderTrailStatusBadge(trail.status)}
                        <span className="text-xs font-mono font-medium text-[var(--text-muted)]">
                          {trail.lengthKm} km · {Math.floor(trail.durationMin / 60)}h{trail.durationMin % 60 > 0 ? `${trail.durationMin % 60}` : '00'}
                        </span>
                      </div>

                      <h3 className="font-['Fraunces'] text-lg font-bold text-[var(--text-primary)] group-hover:text-[var(--brand-primary)] transition-colors">
                        {trail.name}
                      </h3>

                      <p className="text-xs text-[var(--text-muted)] line-clamp-2 leading-relaxed">
                        {trail.description}
                      </p>
                    </div>

                    <div className="pt-4 mt-4 border-t border-[var(--border-default)]/60 flex items-center justify-between text-xs text-[var(--text-muted)]">
                      <span className="capitalize">{trail.biomeLabel}</span>
                      <span className="font-mono text-[var(--text-primary)] font-semibold">+{trail.elevationGainM}m D+</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Quick Species Showcase */}
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-6 pt-6">
              <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
                <div>
                  <span className="text-xs font-semibold tracking-wider text-[var(--brand-primary)] uppercase">
                    Sanctuaire Biologique
                  </span>
                  <h2 className="font-['Fraunces'] text-2xl sm:text-3xl font-bold text-[var(--text-primary)] mt-1">
                    Atlas des Espèces Endémiques
                  </h2>
                </div>
                <button
                  onClick={() => setActiveView('biodiversite')}
                  className="inline-flex items-center gap-1 text-sm font-semibold text-[var(--brand-primary)] hover:underline cursor-pointer"
                >
                  <span>Consulter les 8 fiches botaniques & faune</span>
                  <ChevronRight className="w-4 h-4" />
                </button>
              </div>

              <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
                {species.slice(0, 4).map((sp) => (
                  <div
                    key={sp.id}
                    onClick={() => setActiveView('biodiversite')}
                    className="p-4 rounded-xl bg-[var(--bg-surface)] border border-[var(--border-default)] hover:shadow-xs transition-all cursor-pointer group"
                  >
                    <div className="text-xs font-mono text-[var(--brand-primary)] font-semibold uppercase">
                      {sp.categoryLabel}
                    </div>
                    <div className="font-['Fraunces'] font-bold text-sm text-[var(--text-primary)] mt-1 group-hover:text-[var(--brand-primary)]">
                      {sp.commonName}
                    </div>
                    <div className="text-[11px] italic text-[var(--text-muted)] font-serif">
                      {sp.scientificName}
                    </div>
                    <div className="mt-3 inline-block px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-[var(--bg-elevated)] border border-[var(--border-default)] text-[var(--text-primary)]">
                      UICN : {sp.iucnStatus}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* ================================================================= */}
        {/* VUE 2 : CARTE TOPOGRAPHIQUE & SENTIERS (F16, F17, F18)             */}
        {/* ================================================================= */}
        {activeView === 'sentiers' && (
          <div className="space-y-10 pb-16">
            <ImmersiveSection variant="forest" className="py-10">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div className="space-y-1">
                  <div className="inline-flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-[#B7E4C7]">
                    <Compass className="w-4 h-4 text-[#74C69D]" />
                    <span>Moteur Vectoriel Topographique SVG & Altimétrie</span>
                  </div>
                  <h1 className="font-['Fraunces'] text-2xl sm:text-4xl font-bold text-white mt-1">
                    Carte Topographique & 6 Sentiers
                  </h1>
                </div>
                <div className="text-xs text-[#E9F5ED]/80 font-mono bg-[#1F2421]/80 px-3 py-2 rounded-xl border border-[#36403A]">
                  viewBox 1000x700 · 7 Calques · Scrubber Altimétrique Synchronisé
                </div>
              </div>
            </ImmersiveSection>

            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-10">
              {/* Interactive Topographic Map (F16) */}
              <InteractiveTopoMap scrubPoint={scrubPoint} />

              {/* Synchronized Elevation Profile with Scrubber (F17) */}
              <ElevationProfile onScrub={setScrubPoint} />

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
        {/* VUE 3 : ATLAS DE LA BIODIVERSITÉ (F19)                            */}
        {/* ================================================================= */}
        {activeView === 'biodiversite' && (
          <SpeciesAtlas />
        )}

        {/* ================================================================= */}
        {/* VUE 4 : BILLETTERIE ÉCO-PASS (F20, F21)                           */}
        {/* ================================================================= */}
        {activeView === 'billetterie' && (
          <div className="space-y-8 pb-16">
            <ImmersiveSection variant="canopy" className="py-10">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                  <div className="inline-flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-[#B7E4C7]">
                    <Ticket className="w-4 h-4 text-[#74C69D]" />
                    <span>Régulation Écologique par Quota</span>
                  </div>
                  <h1 className="font-['Fraunces'] text-2xl sm:text-4xl font-bold text-white mt-1">
                    Billetterie Éco-Pass &amp; Éco-Mobilité
                  </h1>
                </div>
                <div className="text-xs text-[#E9F5ED]/80 font-mono bg-[#0B1D15]/60 px-3 py-2 rounded-xl border border-[#36403A]">
                  Capacité restante aujourd&apos;hui : {Math.max(0, telemetry.dailyCapacityMax - telemetry.currentOccupancy)} / {telemetry.dailyCapacityMax} places
                </div>
              </div>
            </ImmersiveSection>

            <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
              <BookingWizard />
            </div>
          </div>
        )}

        {/* ================================================================= */}
        {/* VUE 5 : MON PASS & TERRAIN (F22, F23, F24, F25)                   */}
        {/* ================================================================= */}
        {activeView === 'pass' && (
          <div className="space-y-10 pb-16">
            <ImmersiveSection variant="bark" className="py-10">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                  <div className="inline-flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-[#74C69D]">
                    <QrCode className="w-4 h-4 text-[#52B788]" />
                    <span>Compagnon Terrain du Randonneur &amp; Sentinelle</span>
                  </div>
                  <h1 className="font-['Fraunces'] text-2xl sm:text-4xl font-bold text-white mt-1">
                    Mon Éco-Pass &amp; Sentinelle Nature
                  </h1>
                </div>
                <div className="text-xs text-[#E9F5ED]/80 font-mono bg-[#121614]/80 px-3 py-2 rounded-xl border border-[#36403A]">
                  Billet Vectoriel SVG · Mode Plein Soleil &amp; OLED · Veille Citoyenne
                </div>
              </div>
            </ImmersiveSection>

            <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 space-y-12">
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
        {activeView === 'ranger' && <RangerDashboard />}
      </main>

      {/* Slide-over Color Atlas Drawer & WCAG Tester (F29, F30) */}
      <ColorAtlasDrawer />

      {/* Ecological Footer */}
      <Footer />
    </div>
  );
}
