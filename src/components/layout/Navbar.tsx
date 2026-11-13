// ============================================================================
// ECOPARK CAMEROUN (YAOUNDÉ – AHALA) — STICKY NAVIGATION HEADER
// (src/components/layout/Navbar.tsx)
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
  MapPin,
  PhoneCall,
} from 'lucide-react';
import { useEcoPark } from '../../context/EcoParkContext';
import { ActiveView, DaltonismMode } from '../../types/ecosystem';
import { recordMotionOrigin, useAnimatedNumber } from '../../utils/ecoMotion';

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
  } = useEcoPark();

  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [daltonismDropdownOpen, setDaltonismDropdownOpen] = useState(false);

  // Nav views definition
  const NAV_ITEMS: { id: ActiveView; label: string; icon: React.ComponentType<{ className?: string }> }[] = [
    { id: 'accueil', label: 'Accueil & 5 Pôles', icon: Trees },
    { id: 'sentiers', label: 'Carte & Activités', icon: Compass },
    { id: 'biodiversite', label: 'Zoo & Faune', icon: Eye },
    { id: 'billetterie', label: 'Réserver (FCFA)', icon: Ticket },
    { id: 'pass', label: 'Mon Pass QR', icon: QrCode },
    { id: 'ranger', label: 'Supervision', icon: ShieldAlert },
  ];

  // Occupancy metrics and dynamic color status + smooth rolling counter
  const animatedOccupancy = useAnimatedNumber(telemetry.currentOccupancy, 480, 0);
  const occupancyPercent = Math.min(
    100,
    Math.max(0, Math.round((telemetry.currentOccupancy / telemetry.dailyCapacityMax) * 100))
  );
  const activePassesCount = passes.filter((p) => p.status !== 'cancelled').length;

  let occupancyBadgeStyle = 'bg-emerald-100 text-emerald-800 border-emerald-300 dark:bg-emerald-950/70 dark:text-emerald-300 dark:border-emerald-800';
  let waveFillColor = '#52B788';
  let wavePeriodSec = '4.2s';
  if (occupancyPercent >= 90) {
    occupancyBadgeStyle = 'bg-red-100 text-red-800 border-red-300 dark:bg-red-950/70 dark:text-red-300 dark:border-red-800';
    waveFillColor = '#DC2626';
    wavePeriodSec = '1.6s';
  } else if (occupancyPercent >= 70) {
    occupancyBadgeStyle = 'bg-amber-100 text-amber-800 border-amber-300 dark:bg-amber-950/70 dark:text-amber-300 dark:border-amber-800';
    waveFillColor = '#D97706';
    wavePeriodSec = '2.4s';
  }

  const handleNavClick = (view: ActiveView, e?: React.MouseEvent<HTMLElement>) => {
    if (e) recordMotionOrigin(e);
    setActiveView(view);
    setMobileMenuOpen(false);
  };

  const cycleTheme = (e: React.MouseEvent<HTMLButtonElement>) => {
    recordMotionOrigin(e);
    if (themeMode === 'auto') setThemeMode('light');
    else if (themeMode === 'light') setThemeMode('dark');
    else setThemeMode('auto');
  };

  const daltonismLabels: Record<DaltonismMode, string> = {
    normal: 'Normale',
    deuteranopia: 'Deutéranopie',
    protanopia: 'Protanopie',
    tritanopia: 'Tritanopie',
  };

  return (
    <header className="eco-sticky-navbar sticky top-0 z-40 w-full backdrop-blur-md bg-[var(--bg-canvas)]/95 border-b border-[var(--border-default)] transition-colors duration-200">
      {/* Official Production Topbar: Yaoundé – Ahala Barrière */}
      <div className="bg-[#1B4332] text-[#E9F5ED] text-[11px] py-1.5 border-b border-[#2D6A4F]/60">
        <div className="eco-container flex flex-wrap items-center justify-between gap-2">
          <div className="flex items-center gap-2 font-medium min-w-0">
            <MapPin className="w-3.5 h-3.5 text-[#74C69D] shrink-0" />
            <span className="truncate sm:whitespace-normal">
              <strong>Yaoundé – Ahala Barrière (Face station Tradex, RN3)</strong> • Parc : Mar–Dim 09h00–18h00 • Hôtels 24h/24 • Restaurant 07h–23h • Parking gratuit
            </span>
          </div>
          <div className="hidden lg:flex items-center gap-4 font-mono text-[#B7E4C7] shrink-0">
            <a
              href="https://wa.me/237672564598"
              target="_blank"
              rel="noreferrer"
              className="hover:text-white flex items-center gap-1"
            >
              <PhoneCall className="w-3 h-3 text-[#74C69D]" />
              <span>WhatsApp : +237 672 56 45 98 / +237 694 60 14 49</span>
            </a>
            <span>•</span>
            <span>info@ecopark-yaounde.com</span>
          </div>
        </div>
      </div>

      <div className="eco-container">
        <div className="flex items-center justify-between h-16 md:h-20 gap-2 w-full min-w-0">
          {/* Official Brand Logo & Title */}
          <button
            onClick={(e) => handleNavClick('accueil', e)}
            className="flex items-center gap-2.5 text-left group shrink-0 focus:outline-none focus-visible:ring-2 focus-visible:ring-[var(--brand-primary)] rounded-lg py-1 pr-1 cursor-pointer"
            aria-label="ECOPARK CAMEROUN - Retour à l'accueil"
          >
            <img
              src="/images/ahala/cropped-LOGO-ECOPARK-Youtube.png"
              alt="Logo Officiel ECOPARK CAMEROUN"
              className="w-10 h-10 md:w-11 md:h-11 shrink-0 rounded-full object-cover border-2 border-[var(--brand-primary)] shadow-sm group-hover:scale-105 transition-transform duration-200 bg-white"
            />
            <div className="flex flex-col whitespace-nowrap">
              <span className="font-['Barlow_Semi_Condensed'] font-bold text-lg md:text-xl tracking-tight text-[var(--text-primary)] leading-none">
                ECOPARK CAMEROUN
              </span>
              <span className="text-[10px] md:text-[11px] text-[var(--text-muted)] font-semibold tracking-wide uppercase mt-0.5">
                Yaoundé – Ahala • Dès 500 FCFA
              </span>
            </div>
          </button>

          {/* Desktop Navigation Links */}
          <nav className="hidden xl:flex items-center justify-center gap-1 shrink-0" aria-label="Navigation principale">
            {NAV_ITEMS.map((item) => {
              const Icon = item.icon;
              const isActive = activeView === item.id;
              return (
                <button
                  key={item.id}
                  data-motion-target={item.id === 'pass' ? 'nav-pass' : undefined}
                  onClick={(e) => handleNavClick(item.id, e)}
                  className={`flex items-center gap-1.5 px-2.5 py-2 rounded-lg text-xs xl:text-[13px] font-semibold whitespace-nowrap shrink-0 transition-all duration-150 relative cursor-pointer ${
                    isActive
                      ? 'text-[var(--brand-primary)] bg-[var(--bg-surface)] font-bold shadow-xs'
                      : 'text-[var(--text-muted)] hover:text-[var(--text-primary)] hover:bg-[var(--bg-surface)]/60'
                  }`}
                >
                  <Icon className={`w-3.5 h-3.5 shrink-0 ${isActive ? 'text-[var(--brand-primary)]' : 'text-[var(--text-muted)]'}`} />
                  <span>{item.label}</span>
                  {item.id === 'pass' && activePassesCount > 0 && (
                    <span className="ml-0.5 px-1.5 py-0.2 rounded-full bg-[var(--brand-primary)]/15 text-[var(--brand-primary)] font-mono text-[10px] font-bold">
                      {activePassesCount}
                    </span>
                  )}
                  {isActive && (
                    <span className="vt-nav-pill absolute bottom-0 left-2 right-2 h-0.5 bg-[var(--brand-primary)] rounded-full" />
                  )}
                </button>
              );
            })}
          </nav>

          {/* Telemetry Badges & Quick Controls */}
          <div className="flex items-center gap-1.5 shrink-0">
            {/* Live Occupancy Liquid Gauge Badge (« Respiration écologique ») */}
            <div
              data-motion-target="nav-quota"
              className={`hidden md:flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg border text-xs font-mono font-medium whitespace-nowrap shrink-0 shadow-2xs transition-colors ${occupancyBadgeStyle}`}
              title={`Respiration écologique d'Ahala : ${telemetry.currentOccupancy} / ${telemetry.dailyCapacityMax} visiteurs (${occupancyPercent}%)`}
            >
              {/* Miniature Liquid Wave Vessel with Daltonism-Safe Threshold Patterns */}
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
              className="hidden sm:flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg border border-sky-300 bg-sky-50 text-sky-900 dark:border-sky-800 dark:bg-sky-950/70 dark:text-sky-200 text-xs font-mono font-medium whitespace-nowrap shrink-0 shadow-2xs"
              title="Météo locale et qualité de l'air à Yaoundé-Ahala"
            >
              <Wind className="w-3.5 h-3.5 text-sky-600 dark:text-sky-400 shrink-0" />
              <span>{telemetry.temperatureC}°C</span>
            </div>

            {/* Quick Theme Switcher */}
            <button
              onClick={cycleTheme}
              className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg border border-[var(--border-default)] bg-[var(--bg-surface)] hover:bg-[var(--bg-elevated)] text-[var(--text-primary)] text-xs font-medium transition-colors shadow-2xs cursor-pointer"
              title={`Thème actuel : ${themeMode} (${effectiveTheme}). Cliquer pour basculer.`}
              aria-label="Basculer le thème clair, sombre ou automatique"
            >
              {themeMode === 'auto' ? (
                <Monitor className="w-4 h-4 text-[var(--text-muted)]" />
              ) : effectiveTheme === 'dark' ? (
                <Moon className="w-4 h-4 text-emerald-400" />
              ) : (
                <Sun className="w-4 h-4 text-amber-600" />
              )}
              <span className="hidden lg:inline capitalize">{themeMode}</span>
            </button>

            {/* Daltonism Accessibility Selector */}
            <div className="relative">
              <button
                onClick={() => setDaltonismDropdownOpen(!daltonismDropdownOpen)}
                className={`flex items-center gap-1 px-2.5 py-1.5 rounded-lg border text-xs font-medium transition-colors shadow-2xs cursor-pointer ${
                  daltonismMode !== 'normal'
                    ? 'border-[var(--brand-primary)] bg-[var(--brand-primary)]/10 text-[var(--brand-primary)] font-semibold'
                    : 'border-[var(--border-default)] bg-[var(--bg-surface)] hover:bg-[var(--bg-elevated)] text-[var(--text-primary)]'
                }`}
                title={`Filtres d'accessibilité visuelle (${daltonismLabels[daltonismMode]})`}
                aria-expanded={daltonismDropdownOpen}
                aria-label="Sélecteur d'accessibilité daltonisme"
              >
                <Eye className="w-4 h-4" />
                {daltonismMode !== 'normal' && (
                  <span className="hidden xl:inline">{daltonismLabels[daltonismMode]}</span>
                )}
                <ChevronDown className="w-3 h-3 opacity-70" />
              </button>

              {daltonismDropdownOpen && (
                <div className="absolute right-0 mt-2 w-48 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)] shadow-xl py-1.5 z-50 animate-in fade-in slide-in-from-top-2 duration-150">
                  <div className="px-3 py-1 text-[11px] font-semibold text-[var(--text-muted)] uppercase tracking-wider border-b border-[var(--border-default)] mb-1">
                    Vision des Couleurs
                  </div>
                  {(['normal', 'deuteranopia', 'protanopia', 'tritanopia'] as DaltonismMode[]).map((mode) => (
                    <button
                      key={mode}
                      onClick={() => {
                        setDaltonismMode(mode);
                        setDaltonismDropdownOpen(false);
                      }}
                      className={`w-full text-left px-3 py-2 text-xs flex items-center justify-between hover:bg-[var(--bg-surface)] cursor-pointer ${
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

            {/* Atelier Chromatique High-Visibility Button */}
            <button
              onClick={() => setColorDrawerOpen(!colorDrawerOpen)}
              className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-[var(--brand-primary)] text-white hover:bg-[var(--brand-secondary)] text-xs font-semibold whitespace-nowrap shrink-0 shadow-xs transition-transform active:scale-95 cursor-pointer"
              title="Ouvrir le laboratoire chromatique Adobe Color & testeur de contraste WCAG"
              aria-label="Ouvrir l'Atelier Chromatique"
            >
              <Palette className="w-4 h-4 shrink-0" />
              <span className="hidden sm:inline">
                Atelier<span className="hidden 2xl:inline"> Couleurs</span>
              </span>
            </button>

            {/* Mobile Hamburger Toggle Button */}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="xl:hidden p-2 rounded-lg text-[var(--text-primary)] hover:bg-[var(--bg-surface)] focus:outline-none focus:ring-2 focus:ring-[var(--brand-primary)]"
              aria-label={mobileMenuOpen ? 'Fermer le menu mobile' : 'Ouvrir le menu mobile'}
              aria-expanded={mobileMenuOpen}
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Navigation Dropdown Drawer */}
      {mobileMenuOpen && (
        <div className="xl:hidden border-t border-[var(--border-default)] bg-[var(--bg-canvas)] px-4 pt-3 pb-6 space-y-2 shadow-lg animate-in slide-in-from-top-4 duration-200">
          <div className="flex items-center justify-between py-2 px-1 text-xs text-[var(--text-muted)] border-b border-[var(--border-default)] mb-2 font-mono">
            <span>Affluence: {telemetry.currentOccupancy}/{telemetry.dailyCapacityMax} ({occupancyPercent}%)</span>
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
                  className={`flex items-center gap-3 w-full px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                    isActive
                      ? 'bg-[var(--brand-primary)] text-white font-semibold'
                      : 'text-[var(--text-primary)] hover:bg-[var(--bg-surface)]'
                  }`}
                >
                  <Icon className={`w-5 h-5 ${isActive ? 'text-white' : 'text-[var(--text-muted)]'}`} />
                  <span>{item.label}</span>
                </button>
              );
            })}
          </div>
        </div>
      )}
    </header>
  );
};
