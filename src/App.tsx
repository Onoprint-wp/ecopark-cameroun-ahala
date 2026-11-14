// ============================================================================
// ECOPARK CAMEROUN (YAOUNDE - AHALA) - APPLICATION SHELL & VIEW ROUTER
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
import { AuthPortal } from './components/auth/AuthPortal';
import { LegalNoticeView } from './components/legal/LegalNoticeView';
import { ColorAtlasDrawer } from './components/design-system/ColorAtlasDrawer';
import { useEcoPark } from './context/EcoParkContext';
import { useAuth } from './context/AuthContext';
import { getRoleDisplayLabel, isDevEnvironment } from './utils/ecoAuth';
import { recordMotionOrigin, useEcoMotion } from './utils/ecoMotion';
import { getPhotoObjectPosition } from './utils/ecoRouting';
import {
  Compass,
  Ticket,
  QrCode,
  CheckCircle2,
  AlertTriangle,
  XCircle,
  ChevronRight,
  ShieldAlert,
  Lock,
  User,
  LogOut,
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

  const {
    user,
    isAuthLoading,
    isAuthenticated,
    isStaff,
    logout,
    setAuthPortalMode,
  } = useAuth();

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
              <div className="eco-container space-y-6 tabular-nums">
                <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
                  <div>
                    <span className="type-eyebrow uppercase">
                      Orientation &amp; Plan du Domaine d&apos;Ahala
                    </span>
                    <h2 className="type-h2 text-[var(--text-primary)] mt-1">
                      Six circuits balisés au cœur d&apos;Ahala.
                    </h2>
                  </div>
                  <button
                    onClick={(e) => {
                      recordMotionOrigin(e);
                      setActiveView('sentiers');
                    }}
                    className="cta-chevron self-start sm:self-auto"
                  >
                    <span>Ouvrir la carte interactive</span>
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
                      }p-5 rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-default)] hover:shadow-md hover:-translate-y-0.5 transition-all cursor-pointer group flex flex-col justify-between tabular-nums`}
                    >
                      <div className="space-y-3">
                        <div className="flex items-center justify-between gap-2">
                          {renderTrailStatusBadge(trail.status)}
                          <span className="text-xs font-mono font-medium text-[var(--text-muted)] tabular-nums">
                            {trail.lengthKm} km · {Math.floor(trail.durationMin / 60)}h{trail.durationMin % 60 > 0 ? `${trail.durationMin % 60}` : '00'}
                          </span>
                        </div>

                        <h3 className="type-h3 !text-xl text-[var(--text-primary)] group-hover:text-[var(--brand-primary)] transition-colors">
                          {trail.name}
                        </h3>

                        <p className="type-body !text-xs sm:!text-sm text-[var(--text-muted)] line-clamp-2">
                          {trail.description}
                        </p>
                      </div>

                      <div className="pt-4 mt-4 border-t border-[var(--border-default)]/60 flex items-center justify-between text-xs text-[var(--text-muted)] tabular-nums">
                        <span className="truncate pr-2">{trail.biomeLabel}</span>
                        <span className="font-mono text-[var(--text-primary)] font-semibold shrink-0">Alt. {trail.maxElevationM}m</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Quick Zoological & Heritage Showcase */}
              <div className="eco-container space-y-6 pt-2 tabular-nums">
                <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
                  <div>
                    <span className="type-eyebrow uppercase">
                      Jardin Zoologique &amp; Patrimoine Vivant d&apos;Ahala
                    </span>
                    <h2 className="type-h2 text-[var(--text-primary)] mt-1">
                      Gorille « ToTo », chimpanzés, bassins et flore.
                    </h2>
                  </div>
                  <button
                    onClick={(e) => {
                      recordMotionOrigin(e);
                      setSelectedSpeciesId(null);
                      setActiveView('biodiversite');
                    }}
                    className="cta-chevron self-start sm:self-auto"
                  >
                    <span>Consulter les 8 fiches biodiversité</span>
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
                        <div className="aspect-[4/3] w-full overflow-hidden bg-[#1F2421]">
                          <img
                            src={sp.photoUrl}
                            alt={sp.commonName}
                            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                            style={{ objectPosition: getPhotoObjectPosition(sp.photoUrl) }}
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
                    <span>Cartographie Interactive d&apos;ECOPARK CAMEROUN (Yaoundé - Ahala, RN3)</span>
                  </div>
                  <h1 className="type-h2 text-white mt-1">
                    Plan du parc et six circuits officiels.
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

              {/* Synchronized Elevation Profile with Scrubber (F17) - Shared Element Target */}
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
                  <h1 className="type-h2 text-white mt-1">
                    Réservez votre Pass QR à Yaoundé, Ahala.
                  </h1>
                </div>
                <div className="text-xs text-[#E9F5ED]/80 font-mono bg-[#0B1D15]/60 px-3 py-2 rounded-xl border border-[#36403A] tabular-nums">
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
        {/* VUE 5 : ESPACE CLIENTE (/mon-espace) - AUTHENTIFICATION REQUISE    */}
        {/* ================================================================= */}
        {activeView === 'pass' && (
          <div className="eco-view-enter space-y-10 pb-16">
            <ImmersiveSection variant="bark" className="py-10">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                  <div className="inline-flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-[#74C69D]">
                    <QrCode className="w-4 h-4 text-[#52B788]" />
                    <span>Espace Cliente Sécurisé &amp; Pass QR Code (ECP-2026-XXXXX)</span>
                  </div>
                  <h1 className="font-['Barlow_Semi_Condensed'] text-2xl sm:text-4xl font-bold text-white mt-1">
                    {isAuthenticated && user
                      ? `Bienvenue, ${user.fullName}`
                      : 'Mon Espace Cliente & Mes Réservations QR'}
                  </h1>
                </div>

                {isAuthenticated && user ? (
                  <div className="flex flex-wrap items-center gap-2">
                    <button
                      type="button"
                      onClick={() => setActiveView('connexion')}
                      className="px-3.5 py-2 rounded-xl bg-white/10 hover:bg-white/20 border border-white/20 text-xs font-semibold text-white inline-flex items-center gap-1.5 cursor-pointer"
                    >
                      <User className="w-3.5 h-3.5 text-[#74C69D]" />
                      <span>Mon Compte ({getRoleDisplayLabel(user.role)})</span>
                    </button>
                    <button
                      type="button"
                      onClick={async () => {
                        await logout();
                        setActiveView('accueil');
                      }}
                      className="px-3.5 py-2 rounded-xl bg-rose-950/60 hover:bg-rose-900/80 border border-rose-500/40 text-xs font-semibold text-rose-200 inline-flex items-center gap-1.5 cursor-pointer"
                    >
                      <LogOut className="w-3.5 h-3.5" />
                      <span>Déconnexion</span>
                    </button>
                  </div>
                ) : (
                  <div className="text-xs text-[#E9F5ED]/80 font-mono bg-[#121614]/80 px-3 py-2 rounded-xl border border-[#36403A]">
                    Données personnelles protégées (Loi n° 2010/012) · Garantie Météo 90j
                  </div>
                )}
              </div>
            </ImmersiveSection>

            <div className="eco-container space-y-12">
              {isAuthLoading ? (
                <div className="max-w-xl mx-auto p-8 rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-default)] text-center text-sm text-[var(--text-muted)] font-mono">
                  Vérification de votre session chiffrée...
                </div>
              ) : !isAuthenticated ? (
                <div className="space-y-8">
                  <section aria-label="Consultation Unitaire Pass QR Visiteur">
                    <DigitalEcoPass />
                  </section>

                  <div className="pt-6 border-t border-[var(--border-default)] space-y-5">
                    <div className="max-w-xl mx-auto p-4 rounded-2xl bg-emerald-50/80 dark:bg-emerald-950/40 border border-emerald-300 dark:border-emerald-800 flex items-start gap-3 text-xs text-emerald-950 dark:text-emerald-100">
                      <Lock className="w-4 h-4 text-emerald-600 dark:text-emerald-400 shrink-0 mt-0.5" />
                      <div>
                        <strong>Onboarding Espace Cliente (60s · Session 7 jours) :</strong> Créez gratuitement votre compte ou connectez-vous pour centraliser tous vos Pass QR, pré-remplir vos réservations et accéder aux signalements Sentinelle Nature.
                      </div>
                    </div>
                    <AuthPortal forcedMode="client_login" targetAfterAuth="pass" embedded />
                  </div>
                </div>
              ) : (
                <>
                  {/* Feature F22 & F23: Personal Scoped Digital Eco-Pass Card */}
                  <section aria-label="Mes Éco-Pass Nominatifs">
                    <DigitalEcoPass />
                  </section>

                  {/* Feature F24 & F25: Citizen Sentinel Field Form & Community Feed */}
                  <section
                    aria-label="Sentinelle Nature &amp; Veille Participative"
                    className="pt-6 border-t border-[var(--border-default)]"
                  >
                    <CitizenSentinel />
                  </section>
                </>
              )}
            </div>
          </div>
        )}

        {/* ================================================================= */}
        {/* VUE 6 : COCKPIT PRO (/exploitation) - PROFIL C STRICT (< 20px)     */}
        {/* ================================================================= */}
        {activeView === 'ranger' && (
          <div className="eco-view-enter">
            {isAuthLoading ? (
              <div className="eco-container py-16">
                <div className="max-w-xl mx-auto p-8 rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-default)] text-center text-sm text-[var(--text-muted)] font-mono">
                  Vérification des habilitations Cockpit Pro...
                </div>
              </div>
            ) : !isAuthenticated ? (
              <div className="space-y-6 pt-6 pb-16 font-sans tabular-nums">
                <div className="eco-container">
                  <div className="p-4 rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-default)] flex flex-col md:flex-row md:items-center justify-between gap-3">
                    <div>
                      <div className="inline-flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-amber-700 dark:text-amber-400">
                        <ShieldAlert className="w-4 h-4" />
                        <span>Accès Professionnel Protégé · RBAC ECOPARK CAMEROUN</span>
                      </div>
                      <h1 className="font-sans text-base font-bold text-[var(--text-primary)] mt-0.5">
                        Authentification Cockpit Pro &amp; Exploitation Ahala
                      </h1>
                    </div>
                    <div className="text-xs text-[var(--text-muted)] font-mono bg-[var(--bg-elevated)] px-3 py-2 rounded-xl border border-[var(--border-default)]">
                      Direction · Exploitation · Contrôle QR RN3 · Comptabilité
                    </div>
                  </div>
                </div>

                <div className="eco-container">
                  <AuthPortal forcedMode="staff_login" targetAfterAuth="ranger" embedded />
                </div>
              </div>
            ) : !isStaff ? (
              <div className="eco-container py-16 font-sans">
                <div className="max-w-xl mx-auto p-8 rounded-3xl bg-[var(--bg-surface)] border border-amber-400/60 shadow-xl text-center space-y-5">
                  <div className="w-14 h-14 rounded-2xl bg-amber-100 dark:bg-amber-950 text-amber-700 dark:text-amber-300 mx-auto flex items-center justify-center">
                    <ShieldAlert className="w-7 h-7" />
                  </div>
                  <div className="space-y-2">
                    <span className="text-xs font-mono font-bold uppercase tracking-wider text-amber-700 dark:text-amber-400">
                      Erreur 403 · Habilitation Insuffisante
                    </span>
                    <h1 className="font-sans text-base font-bold text-[var(--text-primary)]">
                      Zone Réservée au Personnel d&apos;Exploitation
                    </h1>
                    <p className="text-xs sm:text-sm text-[var(--text-muted)] leading-relaxed">
                      Vous êtes actuellement connecté(e) en tant que <strong>{user?.fullName}</strong> (<code>Espace Cliente</code>). Le Cockpit Pro d&apos;Ahala est strictement réservé aux agents habilités de MPECK MULTI-SERVICES.
                    </p>
                  </div>
                  <div className="flex flex-wrap items-center justify-center gap-3 pt-2">
                    <button
                      type="button"
                      onClick={() => setActiveView('pass')}
                      className="min-h-[48px] px-5 py-2.5 rounded-xl bg-[var(--brand-primary)] hover:bg-[var(--brand-secondary)] text-white text-xs font-bold cursor-pointer"
                    >
                      Retourner à mon Espace Cliente
                    </button>
                    <button
                      type="button"
                      onClick={async () => {
                        await logout();
                        setAuthPortalMode('staff_login');
                        setActiveView('connexion');
                      }}
                      className="min-h-[48px] px-5 py-2.5 rounded-xl border border-[var(--border-default)] bg-[var(--bg-elevated)] text-xs font-semibold text-[var(--text-primary)] hover:border-amber-500 cursor-pointer"
                    >
                      Changer de compte (Staff)
                    </button>
                  </div>
                </div>
              </div>
            ) : (
              <RangerDashboard />
            )}
          </div>
        )}

        {/* ================================================================= */}
        {/* VUE 7 : PORTAIL /Connexion (CLIENT, INSCRIPTION, STAFF & PROFIL)  */}
        {/* ================================================================= */}
        {activeView === 'connexion' && <AuthPortal />}

        {/* ================================================================= */}
        {/* VUE 8 : MENTIONS LÉGALES, CGV & POLITIQUE DE CONFIDENTIALITÉ      */}
        {/* ================================================================= */}
        {activeView === 'legal' && <LegalNoticeView />}
      </main>

      {/* Slide-over Color Atlas Drawer - Restricted to DEV or explicit /atelier-couleurs route */}
      {(isDevEnvironment() || activeView === 'color_atlas') && <ColorAtlasDrawer />}

      {/* Ecological Footer */}
      <Footer />
    </div>
  );
}
