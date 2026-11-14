// ============================================================================
// ECOPARK CAMEROUN (YAOUNDE - AHALA) - STICKY NAVIGATION & CHAPTERNAV
// (src/components/layout/Navbar.tsx)
// Fiche mémo n°4 : Temps 1 (Bandeau Friction 0s), .type-nav, Temps 2 (Chapternav)
// & Scission stricte Profil B (Public) vs Profil C (Exploitation / Guichet)
// ============================================================================

import React, { useState } from 'react';
import {
  Trees,
  Sun,
  Moon,
  Monitor,
  Eye,
  Palette,
  Wind,
  Users,
  Menu,
  X,
  Compass,
  Ticket,
  QrCode,
  ShieldAlert,
  ChevronDown,
  PhoneCall,
  ShieldCheck,
  BedDouble,
  Utensils,
  Building2,
  GraduationCap,
  Sparkles,
  User,
  Mail,
} from 'lucide-react';
import { useEcoPark } from '../../context/EcoParkContext';
import { useAuth } from '../../context/AuthContext';
import { ActiveView, DaltonismMode } from '../../types/ecosystem';
import { isDevEnvironment } from '../../utils/ecoAuth';
import { recordMotionOrigin, useAnimatedNumber } from '../../utils/ecoMotion';
import { dispatchShowcaseNavigation, type ShowcaseTab } from '../../utils/ecoRouting';

export const Navbar: React.FC = () => {
  const {
    activeView,
    setActiveView,
    themeMode,
    effectiveTheme,
    setThemeMode,
    daltonismMode,
    setDaltonismMode,
    colorDrawerOpen,
    setColorDrawerOpen,
    telemetry,
    passes,
    sessionUnlockedPassIds,
  } = useEcoPark();

  const { user, isAuthenticated, isStaff, setAuthPortalMode } = useAuth();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [daltonismDropdownOpen, setDaltonismDropdownOpen] = useState(false);

  // Scission stricte Profil C : aucune bannière promo ni Chapternav commercial en console métier
  const isOperationalCockpit = activeView === 'ranger';
  const showColorAtlasBtn = isDevEnvironment() || activeView === 'color_atlas';

  // Nav views definition (Supervision affichée uniquement au staff connecté ; accès discret en pied de page)
  const NAV_ITEMS: { id: ActiveView; label: string; icon: React.ComponentType<{ className?: string }> }[] = [
    { id: 'accueil', label: 'Accueil & 5 Pôles', icon: Trees },
    { id: 'sentiers', label: 'Carte & Activités', icon: Compass },
    { id: 'biodiversite', label: 'Zoo & Faune', icon: Eye },
    { id: 'billetterie', label: 'Réserver (FCFA)', icon: Ticket },
    { id: 'pass', label: 'Mon Espace QR', icon: QrCode },
    ...(isStaff ? [{ id: 'ranger' as ActiveView, label: 'Cockpit Pro', icon: ShieldAlert }] : []),
  ];

  // Temps 2 : Chapternav visuel 1 clic (>= 5 gammes / pôles métiers)
  const CHAPTER_ITEMS: {
    key: string;
    label: string;
    sub: string;
    icon: React.ComponentType<{ className?: string }>;
    targetView: ActiveView;
    showcaseTab?: ShowcaseTab;
    anchorId?: string;
  }[] = [
    {
      key: 'pass-comparateur',
      label: '3 Pass Tout-Inclus',
      sub: 'Dès 1 500 FCFA',
      icon: Sparkles,
      targetView: 'accueil',
      anchorId: 'pass-comparateur',
    },
    {
      key: 'hebergements',
      label: 'Hôtels 24h/24',
      sub: '30 unités · 10k FCFA',
      icon: BedDouble,
      targetView: 'accueil',
      showcaseTab: 'hebergements',
      anchorId: 'ahala-production-showcase',
    },
    {
      key: 'saveurs',
      label: 'Château des Saveurs',
      sub: '07h-23h · Dès 2 500 FCFA',
      icon: Utensils,
      targetView: 'accueil',
      showcaseTab: 'saveurs',
      anchorId: 'ahala-production-showcase',
    },
    {
      key: 'tarifs',
      label: 'Grille Tarifs FCFA',
      sub: 'Parc dès 500 FCFA',
      icon: Ticket,
      targetView: 'accueil',
      showcaseTab: 'tarifs',
      anchorId: 'ahala-production-showcase',
    },
    {
      key: 'entreprise',
      label: 'Groupes & Salle 500 pl.',
      sub: '-30% dès 20 pers.',
      icon: Building2,
      targetView: 'accueil',
      showcaseTab: 'entreprise',
      anchorId: 'ahala-production-showcase',
    },
    {
      key: 'formation',
      label: 'CFP MINEFOP',
      sub: '5 filières · 4 tranches',
      icon: GraduationCap,
      targetView: 'accueil',
      showcaseTab: 'formation',
      anchorId: 'ahala-production-showcase',
    },
    {
      key: 'zoo',
      label: 'Zoo Gorille ToTo',
      sub: '8 espèces & bassins',
      icon: Eye,
      targetView: 'biodiversite',
    },
    {
      key: 'circuits',
      label: 'Plan & 6 Circuits',
      sub: 'Carte interactive',
      icon: Compass,
      targetView: 'sentiers',
    },
  ];

  // Occupancy metrics and dynamic color status + smooth rolling counter
  const animatedOccupancy = useAnimatedNumber(telemetry.currentOccupancy, 480, 0);
  const occupancyPercent = Math.min(
    100,
    Math.max(0, Math.round((telemetry.currentOccupancy / telemetry.dailyCapacityMax) * 100))
  );
  const activePassesCount = isStaff
    ? passes.filter((p) => p.status === 'confirmed').length
    : isAuthenticated && user
    ? passes.filter(
        (p) =>
          p.status !== 'cancelled' &&
          p.ownerEmail !== 'anonyme@effacement.local' &&
          ((p.ownerUserId && p.ownerUserId === user.id) ||
            (p.ownerEmail && p.ownerEmail.toLowerCase() === user.email.toLowerCase()) ||
            p.leadVisitor.email.trim().toLowerCase() === user.email.trim().toLowerCase())
      ).length
    : passes.filter(
        (p) =>
          p.status !== 'cancelled' &&
          p.ownerEmail !== 'anonyme@effacement.local' &&
          sessionUnlockedPassIds.includes(p.id)
      ).length;

  let occupancyBadgeStyle =
    'bg-emerald-100 text-emerald-800 border-emerald-300 dark:bg-emerald-950/70 dark:text-emerald-300 dark:border-emerald-800';
  let waveFillColor = '#52B788';
  let wavePeriodSec = '4.2s';
  if (occupancyPercent >= 90) {
    occupancyBadgeStyle =
      'bg-red-100 text-red-800 border-red-300 dark:bg-red-950/70 dark:text-red-300 dark:border-red-800';
    waveFillColor = '#DC2626';
    wavePeriodSec = '1.6s';
  } else if (occupancyPercent >= 70) {
    occupancyBadgeStyle =
      'bg-amber-100 text-amber-800 border-amber-300 dark:bg-amber-950/70 dark:text-amber-300 dark:border-amber-800';
    waveFillColor = '#D97706';
    wavePeriodSec = '2.4s';
  }

  const handleNavClick = (view: ActiveView, e?: React.MouseEvent<HTMLElement>) => {
    if (e) recordMotionOrigin(e);
    setActiveView(view);
    setMobileMenuOpen(false);
  };

  const handleChapterClick = (
    item: (typeof CHAPTER_ITEMS)[number],
    e: React.MouseEvent<HTMLButtonElement>
  ) => {
    recordMotionOrigin(e);
    setMobileMenuOpen(false);
    if (activeView !== item.targetView) {
      setActiveView(item.targetView);
    }
    if (item.showcaseTab || item.anchorId) {
      setTimeout(() => {
        dispatchShowcaseNavigation({
          tab: item.showcaseTab,
          anchorId: item.anchorId,
        });
      }, 60);
    }
  };

  const cycleTheme = (e: React.MouseEvent<HTMLButtonElement>) => {
    recordMotionOrigin(e);
    if (themeMode === 'auto') setThemeMode('light');
    else if (themeMode === 'light') setThemeMode('dark');
    else setThemeMode('auto');
  };

  const themeLabels: Record<'auto' | 'light' | 'dark', string> = {
    auto: 'Auto',
    light: 'Clair',
    dark: 'Sombre',
  };

  const daltonismLabels: Record<DaltonismMode, string> = {
    normal: 'Normale',
    deuteranopia: 'Deutéranopie',
    protanopia: 'Protanopie',
    tritanopia: 'Tritanopie',
  };

  return (
    <header className="eco-sticky-navbar sticky top-0 z-40 w-full backdrop-blur-md bg-[var(--bg-canvas)]/95 border-b border-[var(--border-default)] transition-colors duration-200">
      {/* TEMPS 1 (Fiche mémo n°4) : Bandeau Levée de Friction Prix / Garantie dès 0s (désactivé en Profil C Métier) */}
      {!isOperationalCockpit && (
        <div className="bg-[#1B4332] text-[#E9F5ED] text-[12px] leading-4 py-1.5 border-b border-[#2D6A4F]/60 tabular-nums">
          <div className="eco-container flex items-center justify-between gap-3 min-w-0">
            <div className="flex items-center gap-2 font-medium min-w-0 flex-1 overflow-hidden">
              <ShieldCheck className="w-3.5 h-3.5 text-[#74C69D] shrink-0" />
              <span className="truncate sm:whitespace-normal block min-w-0">
                <strong>Entrée dès 500 FCFA enf. / 1 000 FCFA ad.</strong> • Garantie Météo RN3 (report gratuit 90j) • Parking gratuit face Tradex Ahala • Hôtels 24h/24
              </span>
            </div>
            <div className="hidden lg:flex items-center gap-2.5 font-mono text-[11px] text-[#B7E4C7] shrink-0 tabular-nums">
              <span className="inline-flex items-center gap-1">
                <PhoneCall className="w-3 h-3 text-[#74C69D] shrink-0" />
                <span>WhatsApp :</span>
                <a
                  href="https://wa.me/237672564598"
                  target="_blank"
                  rel="noreferrer"
                  className="hover:text-white hover:underline"
                >
                  +237 672 56 45 98
                </a>
                <span>/</span>
                <a
                  href="https://wa.me/237694601449"
                  target="_blank"
                  rel="noreferrer"
                  className="hover:text-white hover:underline"
                >
                  +237 694 60 14 49
                </a>
              </span>
              <span>•</span>
              <a
                href="mailto:info@ecopark-yaounde.com"
                className="hover:text-white hover:underline inline-flex items-center gap-1"
              >
                <Mail className="w-3 h-3 text-[#74C69D] shrink-0" />
                <span>info@ecopark-yaounde.com</span>
              </a>
              <span>•</span>
              <span>Mar-Dim 09h-18h</span>
            </div>
          </div>
        </div>
      )}

      {/* Niveau 1 : Global Nav (.type-nav : 12px, -0.010em, 44px Desktop / 48px Mobile) */}
      <div className="eco-container">
        <div className="flex items-center justify-between min-h-[56px] md:min-h-[64px] py-1.5 gap-2 w-full min-w-0">
          {/* Official Brand Logo & Title */}
          <button
            onClick={(e) => handleNavClick('accueil', e)}
            className="touch-target-48 flex items-center gap-2 sm:gap-2.5 text-left group min-w-0 shrink focus:outline-none focus-visible:ring-2 focus-visible:ring-[var(--brand-primary)] rounded-lg py-1 pr-1 cursor-pointer"
            aria-label="ECOPARK CAMEROUN - Retour à l'accueil"
          >
            <img
              src="/images/ahala/cropped-LOGO-ECOPARK-Youtube.png"
              alt="Logo Officiel ECOPARK CAMEROUN"
              className="w-9 h-9 sm:w-10 sm:h-10 shrink-0 rounded-full object-cover border-2 border-[var(--brand-primary)] shadow-sm group-hover:scale-105 transition-transform duration-200 bg-white"
            />
            <div className="flex flex-col min-w-0">
              <span className="font-['Barlow_Semi_Condensed'] font-bold text-base sm:text-lg md:text-xl tracking-tight text-[var(--text-primary)] leading-none truncate">
                ECOPARK CAMEROUN
              </span>
              <span className="text-[10px] sm:text-[11px] text-[var(--text-muted)] font-semibold tracking-wide uppercase mt-0.5 tabular-nums truncate">
                {isOperationalCockpit ? 'Poste Exploitation RN3' : 'Yaoundé - Ahala • Dès 500 FCFA'}
              </span>
            </div>
          </button>

          {/* Desktop Navigation Links (.type-nav) */}
          <nav className="hidden xl:flex items-center justify-center gap-0.5 shrink-0" aria-label="Navigation principale">
            {NAV_ITEMS.map((item) => {
              const Icon = item.icon;
              const isActive = activeView === item.id;
              return (
                <button
                  key={item.id}
                  data-motion-target={item.id === 'pass' ? 'nav-pass' : undefined}
                  onClick={(e) => handleNavClick(item.id, e)}
                  className={`type-nav flex items-center gap-1.5 px-2.5 rounded-lg whitespace-nowrap shrink-0 transition-all duration-150 relative cursor-pointer ${
                    isActive
                      ? 'text-[var(--brand-primary)] bg-[var(--bg-surface)] font-semibold shadow-xs'
                      : 'text-[var(--text-primary)]/85 hover:text-[var(--text-primary)] hover:bg-[var(--bg-surface)]/60'
                  }`}
                >
                  <Icon
                    className={`w-3.5 h-3.5 shrink-0 ${
                      isActive ? 'text-[var(--brand-primary)]' : 'text-[var(--text-muted)]'
                    }`}
                  />
                  <span>{item.label}</span>
                  {item.id === 'pass' && activePassesCount > 0 && (
                    <span className="ml-0.5 px-1.5 py-0.5 rounded-full bg-[var(--brand-primary)]/15 text-[var(--brand-primary)] font-mono text-[10px] font-bold tabular-nums">
                      {activePassesCount}
                    </span>
                  )}
                  {isActive && (
                    <span className="vt-nav-pill absolute bottom-1 left-2.5 right-2.5 h-0.5 bg-[var(--brand-primary)] rounded-full" />
                  )}
                </button>
              );
            })}
          </nav>

          {/* Telemetry Badges & Quick Controls */}
          <div className="flex items-center gap-1.5 shrink-0">
            {/* Live Occupancy Liquid Gauge Badge */}
            <div
              data-motion-target="nav-quota"
              className={`hidden md:flex items-center gap-1.5 px-2.5 min-h-[40px] rounded-lg border text-xs font-mono font-medium whitespace-nowrap shrink-0 shadow-2xs transition-colors tabular-nums ${occupancyBadgeStyle}`}
              title={`Respiration écologique d'Ahala : ${telemetry.currentOccupancy} / ${telemetry.dailyCapacityMax} visiteurs (${occupancyPercent}%)`}
            >
              <svg
                width="16"
                height="16"
                viewBox="0 0 20 20"
                className="shrink-0 rounded-full ring-1 ring-current/30 overflow-hidden bg-black/10 dark:bg-black/40"
                aria-hidden="true"
              >
                <defs>
                  <clipPath id="nav-quota-flask">
                    <circle cx="10" cy="10" r="9.5" />
                  </clipPath>
                  <pattern id="nav-quota-stripes" width="4" height="4" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
                    <line x1="0" y1="0" x2="0" y2="4" stroke="#FFFFFF" strokeWidth="1.2" strokeOpacity="0.45" />
                  </pattern>
                  <pattern id="nav-quota-hatch" width="4" height="4" patternUnits="userSpaceOnUse">
                    <path d="M0,0 L4,4 M4,0 L0,4" stroke="#FFFFFF" strokeWidth="0.9" strokeOpacity="0.55" />
                  </pattern>
                </defs>
                <g clipPath="url(#nav-quota-flask)">
                  <g
                    style={{
                      transform: `translate3d(0, ${Math.max(1, 20 - (occupancyPercent / 100) * 19)}px, 0)`,
                      transition: 'transform 520ms cubic-bezier(0.22, 1, 0.36, 1)',
                    }}
                  >
                    <g
                      className="eco-liquid-wave-track eco-ambient-anim"
                      style={{ '--wave-period': wavePeriodSec } as React.CSSProperties}
                    >
                      <path
                        d="M 0,2 Q 5,0 10,2 T 20,2 T 30,2 T 40,2 L 40,24 L 0,24 Z"
                        fill={waveFillColor}
                      />
                    </g>
                    {occupancyPercent >= 70 && occupancyPercent < 90 && (
                      <rect x="0" y="1" width="20" height="22" fill="url(#nav-quota-stripes)" />
                    )}
                    {occupancyPercent >= 90 && (
                      <rect x="0" y="1" width="20" height="22" fill="url(#nav-quota-hatch)" />
                    )}
                  </g>
                </g>
                <Users className="hidden" />
              </svg>
              <span>
                {Math.round(animatedOccupancy)}/{telemetry.dailyCapacityMax}
              </span>
            </div>

            {/* Weather & Temperature Badge */}
            <div
              className="hidden sm:flex items-center gap-1.5 px-2.5 min-h-[40px] rounded-lg border border-sky-300 bg-sky-50 text-sky-900 dark:border-sky-800 dark:bg-sky-950/70 dark:text-sky-200 text-xs font-mono font-medium whitespace-nowrap shrink-0 shadow-2xs tabular-nums"
              title="Météo locale et qualité de l'air à Yaoundé-Ahala"
            >
              <Wind className="w-3.5 h-3.5 text-sky-600 dark:text-sky-400 shrink-0" />
              <span>{telemetry.temperatureC}°C</span>
            </div>

            {/* Quick Theme Switcher (Garde-fou 2 : >= 48px sur tactile, masqué sous md et placé dans le tiroir mobile) */}
            <button
              onClick={cycleTheme}
              className="hidden md:flex touch-target-48 lg:min-h-[44px] items-center justify-center gap-1.5 px-2.5 rounded-lg border border-[var(--border-default)] bg-[var(--bg-surface)] hover:bg-[var(--bg-elevated)] text-[var(--text-primary)] text-xs font-medium transition-colors shadow-2xs cursor-pointer"
              title={`Thème actuel : ${themeLabels[themeMode]} (${effectiveTheme === 'dark' ? 'Sombre' : 'Clair'}). Cliquer pour basculer.`}
              aria-label="Basculer le thème clair, sombre ou automatique"
            >
              {themeMode === 'auto' ? (
                <Monitor className="w-4 h-4 text-[var(--text-muted)]" />
              ) : effectiveTheme === 'dark' ? (
                <Moon className="w-4 h-4 text-emerald-400" />
              ) : (
                <Sun className="w-4 h-4 text-amber-600" />
              )}
              <span className="hidden 2xl:inline">{themeLabels[themeMode]}</span>
            </button>

            {/* Daltonism Accessibility Selector (masqué sous md et placé dans le tiroir mobile) */}
            <div className="hidden md:block relative">
              <button
                onClick={() => setDaltonismDropdownOpen(!daltonismDropdownOpen)}
                className={`touch-target-48 lg:min-h-[44px] flex items-center justify-center gap-1 px-2.5 rounded-lg border text-xs font-medium transition-colors shadow-2xs cursor-pointer ${
                  daltonismMode !== 'normal'
                    ? 'border-[var(--brand-primary)] bg-[var(--brand-primary)]/10 text-[var(--brand-primary)] font-semibold'
                    : 'border border-[var(--border-default)] bg-[var(--bg-surface)] hover:bg-[var(--bg-elevated)] text-[var(--text-primary)]'
                }`}
                title={`Filtres d'accessibilité visuelle (${daltonismLabels[daltonismMode]})`}
                aria-expanded={daltonismDropdownOpen}
                aria-label="Sélecteur d'accessibilité daltonisme"
              >
                <Eye className="w-4 h-4" />
                {daltonismMode !== 'normal' && (
                  <span className="hidden 2xl:inline">{daltonismLabels[daltonismMode]}</span>
                )}
                <ChevronDown className="w-3 h-3 opacity-70" />
              </button>

              {daltonismDropdownOpen && (
                <div className="absolute right-0 mt-2 w-52 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)] shadow-xl py-1.5 z-50">
                  <div className="px-3 py-1.5 text-[11px] font-semibold text-[var(--text-muted)] uppercase tracking-wider border-b border-[var(--border-default)] mb-1">
                    Vision des Couleurs
                  </div>
                  {(['normal', 'deuteranopia', 'protanopia', 'tritanopia'] as DaltonismMode[]).map((mode) => (
                    <button
                      key={mode}
                      onClick={() => {
                        setDaltonismMode(mode);
                        setDaltonismDropdownOpen(false);
                      }}
                      className={`w-full min-h-[48px] text-left px-3 py-2 text-xs flex items-center justify-between hover:bg-[var(--bg-surface)] cursor-pointer ${
                        daltonismMode === mode
                          ? 'text-[var(--brand-primary)] font-bold bg-[var(--brand-primary)]/10'
                          : 'text-[var(--text-primary)]'
                      }`}
                    >
                      <span>{daltonismLabels[mode]}</span>
                      {daltonismMode === mode && <span className="text-[var(--brand-primary)] font-bold">✓</span>}
                    </button>
                  ))}
                </div>
              )}
            </div>

            {/* Connexion / Mon Compte Button */}
            <button
              type="button"
              onClick={(e) => {
                recordMotionOrigin(e);
                if (!isAuthenticated) {
                  setAuthPortalMode('client_login');
                }
                setActiveView('connexion');
              }}
              className={`touch-target-48 lg:min-h-[44px] flex items-center justify-center gap-1.5 px-3 rounded-full text-xs font-semibold whitespace-nowrap shrink-0 shadow-xs transition-colors cursor-pointer ${
                activeView === 'connexion' || isAuthenticated
                  ? 'bg-[var(--brand-primary)] text-[var(--on-primary)] hover:bg-[var(--brand-primary-hover)]'
                  : 'border border-[var(--border-default)] bg-[var(--bg-surface)] hover:bg-[var(--bg-elevated)] text-[var(--text-primary)]'
              }`}
              aria-label={isAuthenticated ? 'Mon compte connecté' : 'Se connecter ou créer un compte'}
            >
              <User className="w-4 h-4 shrink-0" />
              <span className="hidden sm:inline">
                {isAuthenticated && user ? user.fullName.split(' ')[0] : 'Connexion'}
              </span>
            </button>

            {/* Atelier Chromatique Button (DEV ou /atelier-couleurs uniquement) */}
            {showColorAtlasBtn && (
              <button
                onClick={() => setColorDrawerOpen(!colorDrawerOpen)}
                className="touch-target-48 lg:min-h-[44px] flex items-center justify-center gap-1.5 px-3 rounded-lg bg-[var(--brand-primary)] text-[var(--on-primary)] hover:bg-[var(--brand-primary-hover)] text-xs font-semibold whitespace-nowrap shrink-0 shadow-xs transition-transform active:scale-95 cursor-pointer"
                title="Ouvrir le laboratoire chromatique Adobe Color & testeur de contraste WCAG"
                aria-label="Ouvrir l'Atelier Chromatique"
              >
                <Palette className="w-4 h-4 shrink-0" />
                <span className="hidden 2xl:inline">Atelier</span>
              </button>
            )}

            {/* Mobile Hamburger Toggle Button (>= 48x48px) */}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="xl:hidden touch-target-48 flex items-center justify-center p-2 rounded-lg text-[var(--text-primary)] hover:bg-[var(--bg-surface)] focus:outline-none focus:ring-2 focus:ring-[var(--brand-primary)] cursor-pointer"
              aria-label={mobileMenuOpen ? 'Fermer le menu mobile' : 'Ouvrir le menu mobile'}
              aria-expanded={mobileMenuOpen}
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* TEMPS 2 (Fiche mémo n°4 - Profil B) : Chapternav Visuel 1 Clic (masqué en Profil C Métier) */}
      {!isOperationalCockpit && (
        <div className="border-t border-[var(--border-subtle)] bg-[var(--bg-surface)]/85">
          <div className="eco-container">
            <nav
              aria-label="Orientation rapide par pôle métier (Chapternav)"
              className="eco-chapternav-scroll flex items-center justify-between gap-1.5 py-0.5"
            >
              {CHAPTER_ITEMS.map((chap) => {
                const Icon = chap.icon;
                return (
                  <button
                    key={chap.key}
                    type="button"
                    onClick={(e) => handleChapterClick(chap, e)}
                    className="type-chapternav group flex items-center gap-2 px-3 py-1.5 rounded-lg text-[var(--text-primary)] hover:bg-[var(--bg-elevated)] hover:text-[var(--brand-primary)] whitespace-nowrap shrink-0 transition-colors cursor-pointer"
                  >
                    <span className="w-6 h-6 rounded-full bg-[var(--brand-primary)]/10 text-[var(--brand-primary)] flex items-center justify-center shrink-0 group-hover:bg-[var(--brand-primary)] group-hover:text-[var(--on-primary)] transition-colors">
                      <Icon className="w-3.5 h-3.5" />
                    </span>
                    <span className="flex flex-col text-left">
                      <span className="font-semibold leading-tight">{chap.label}</span>
                      <span className="text-[10px] text-[var(--text-muted)] leading-tight tabular-nums">
                        {chap.sub}
                      </span>
                    </span>
                  </button>
                );
              })}
            </nav>
          </div>
        </div>
      )}

      {/* Mobile Navigation Dropdown Drawer */}
      {mobileMenuOpen && (
        <div className="xl:hidden border-t border-[var(--border-default)] bg-[var(--bg-canvas)] px-4 pt-3 pb-6 space-y-3 shadow-lg">
          <div className="flex items-center justify-between py-2 px-1 text-xs text-[var(--text-muted)] border-b border-[var(--border-default)] font-mono tabular-nums">
            <span>
              Affluence: {telemetry.currentOccupancy}/{telemetry.dailyCapacityMax} ({occupancyPercent}%)
            </span>
            <span>{telemetry.temperatureC}°C · Ahala RN3</span>
          </div>

          <div className="grid grid-cols-1 gap-1">
            {NAV_ITEMS.map((item) => {
              const Icon = item.icon;
              const isActive = activeView === item.id;
              return (
                <button
                  key={item.id}
                  onClick={(e) => handleNavClick(item.id, e)}
                  className={`flex items-center justify-between gap-3 w-full min-h-[48px] px-3 py-2.5 rounded-lg text-sm font-medium transition-colors cursor-pointer ${
                    isActive
                      ? 'bg-[var(--brand-primary)] text-[var(--on-primary)] font-semibold'
                      : 'text-[var(--text-primary)] hover:bg-[var(--bg-surface)]'
                  }`}
                >
                  <span className="flex items-center gap-3">
                    <Icon className={`w-5 h-5 ${isActive ? 'text-[var(--on-primary)]' : 'text-[var(--text-muted)]'}`} />
                    <span>{item.label}</span>
                  </span>
                  {item.id === 'pass' && activePassesCount > 0 && (
                    <span className="px-2 py-0.5 rounded-full bg-black/15 text-xs font-mono font-bold tabular-nums">
                      {activePassesCount}
                    </span>
                  )}
                </button>
              );
            })}

            <button
              type="button"
              onClick={(e) => {
                if (!isAuthenticated) {
                  setAuthPortalMode('client_login');
                }
                handleNavClick('connexion', e);
              }}
              className={`flex items-center gap-3 w-full min-h-[48px] px-3 py-2.5 rounded-lg text-sm font-semibold transition-colors cursor-pointer ${
                activeView === 'connexion'
                  ? 'bg-[var(--brand-primary)] text-[var(--on-primary)]'
                  : 'bg-[var(--bg-surface)] text-[var(--brand-primary)] border border-[var(--border-default)]'
              }`}
            >
              <User className="w-5 h-5" />
              <span>
                {isAuthenticated && user ? `Mon Compte (${user.fullName})` : 'Connexion / Créer un Compte'}
              </span>
            </button>
          </div>

          {/* Mobile Theme & Accessibility Controls */}
          <div className="pt-3 border-t border-[var(--border-default)] grid grid-cols-2 gap-2">
            <button
              type="button"
              onClick={cycleTheme}
              className="min-h-[48px] px-3 py-2 rounded-lg border border-[var(--border-default)] bg-[var(--bg-surface)] text-xs font-semibold text-[var(--text-primary)] flex items-center justify-center gap-2 cursor-pointer"
            >
              {themeMode === 'auto' ? (
                <Monitor className="w-4 h-4 text-[var(--text-muted)]" />
              ) : effectiveTheme === 'dark' ? (
                <Moon className="w-4 h-4 text-emerald-400" />
              ) : (
                <Sun className="w-4 h-4 text-amber-600" />
              )}
              <span>Thème : {themeLabels[themeMode]}</span>
            </button>

            <button
              type="button"
              onClick={() => {
                const order: DaltonismMode[] = ['normal', 'deuteranopia', 'protanopia', 'tritanopia'];
                const next = order[(order.indexOf(daltonismMode) + 1) % order.length];
                setDaltonismMode(next);
              }}
              className="min-h-[48px] px-3 py-2 rounded-lg border border-[var(--border-default)] bg-[var(--bg-surface)] text-xs font-semibold text-[var(--text-primary)] flex items-center justify-center gap-2 cursor-pointer"
            >
              <Eye className="w-4 h-4 text-[var(--brand-primary)]" />
              <span className="truncate">Vision : {daltonismLabels[daltonismMode]}</span>
            </button>
          </div>
        </div>
      )}
    </header>
  );
};
