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

  // Occupancy metrics and dynamic color status
  const occupancyPercent = Math.round(
    (telemetry.currentOccupancy / telemetry.dailyCapacityMax) * 100
  );

  let occupancyBadgeStyle = 'bg-emerald-100 text-emerald-800 border-emerald-300 dark:bg-emerald-950/70 dark:text-emerald-300 dark:border-emerald-800';
  if (occupancyPercent >= 90) {
    occupancyBadgeStyle = 'bg-red-100 text-red-800 border-red-300 dark:bg-red-950/70 dark:text-red-300 dark:border-red-800';
  } else if (occupancyPercent >= 70) {
    occupancyBadgeStyle = 'bg-amber-100 text-amber-800 border-amber-300 dark:bg-amber-950/70 dark:text-amber-300 dark:border-amber-800';
  }

  const handleNavClick = (view: ActiveView) => {
    setActiveView(view);
    setMobileMenuOpen(false);
  };

  const cycleTheme = () => {
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
    <header className="sticky top-0 z-40 w-full backdrop-blur-md bg-[var(--bg-canvas)]/95 border-b border-[var(--border-default)] transition-colors duration-200">
      {/* Official Production Topbar: Yaoundé – Ahala Barrière */}
      <div className="bg-[#1B4332] text-[#E9F5ED] text-[11px] py-1.5 px-4 border-b border-[#2D6A4F]/60">
        <div className="max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-2">
          <div className="flex items-center gap-2 font-medium">
            <MapPin className="w-3.5 h-3.5 text-[#74C69D] shrink-0" />
            <span>
              <strong>Yaoundé – Ahala Barrière (Face station Tradex, RN3)</strong> • Parc : Mar–Dim 09h00–18h00 • Hôtels 24h/24 • Restaurant 07h–23h • Parking gratuit
            </span>
          </div>
          <div className="hidden md:flex items-center gap-4 font-mono text-[#B7E4C7]">
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

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16 md:h-20 gap-2">
          {/* Official Brand Logo & Title */}
          <button
            onClick={() => handleNavClick('accueil')}
            className="flex items-center gap-3 text-left group focus:outline-none focus-visible:ring-2 focus-visible:ring-[var(--brand-primary)] rounded-lg p-1 cursor-pointer"
            aria-label="ECOPARK CAMEROUN - Retour à l'accueil"
          >
            <img
              src="/images/ahala/cropped-LOGO-ECOPARK-Youtube.png"
              alt="Logo Officiel ECOPARK CAMEROUN"
              className="w-10 h-10 md:w-11 md:h-11 rounded-full object-cover border-2 border-[var(--brand-primary)] shadow-sm group-hover:scale-105 transition-transform duration-200 bg-white"
            />
            <div className="flex flex-col">
              <span className="font-['Barlow_Semi_Condensed'] font-bold text-lg md:text-xl tracking-tight text-[var(--text-primary)] leading-none">
                ECOPARK CAMEROUN
              </span>
              <span className="text-[10px] md:text-xs text-[var(--text-muted)] font-semibold tracking-wide uppercase mt-0.5">
                Yaoundé – Ahala • Dès 500 FCFA
              </span>
            </div>
          </button>

          {/* Desktop Navigation Links */}
          <nav className="hidden xl:flex items-center gap-1" aria-label="Navigation principale">
            {NAV_ITEMS.map((item) => {
              const Icon = item.icon;
              const isActive = activeView === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => handleNavClick(item.id)}
                  className={`flex items-center gap-1.5 px-3 py-2 rounded-lg text-xs sm:text-sm font-semibold transition-all duration-150 relative cursor-pointer ${
                    isActive
                      ? 'text-[var(--brand-primary)] bg-[var(--bg-surface)] font-bold shadow-xs'
                      : 'text-[var(--text-muted)] hover:text-[var(--text-primary)] hover:bg-[var(--bg-surface)]/60'
                  }`}
                >
                  <Icon className={`w-4 h-4 ${isActive ? 'text-[var(--brand-primary)]' : 'text-[var(--text-muted)]'}`} />
                  <span>{item.label}</span>
                  {isActive && (
                    <span className="absolute bottom-0 left-2 right-2 h-0.5 bg-[var(--brand-primary)] rounded-full" />
                  )}
                </button>
              );
            })}
          </nav>

          {/* Telemetry Badges & Quick Controls */}
          <div className="flex items-center gap-2 sm:gap-2.5">
            {/* Live Occupancy Gauge Badge */}
            <div
              className={`hidden md:flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg border text-xs font-mono font-medium shadow-2xs ${occupancyBadgeStyle}`}
              title="Affluence instantanée du parc à Yaoundé-Ahala"
            >
              <Users className="w-3.5 h-3.5" />
              <span>
                {telemetry.currentOccupancy}/{telemetry.dailyCapacityMax}{' '}
                <span className="opacity-80">({occupancyPercent}%)</span>
              </span>
            </div>

            {/* Weather & Temperature Badge */}
            <div
              className="hidden sm:flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg border border-sky-300 bg-sky-50 text-sky-900 dark:border-sky-800 dark:bg-sky-950/70 dark:text-sky-200 text-xs font-mono font-medium shadow-2xs"
              title="Météo locale et qualité de l'air à Yaoundé-Ahala"
            >
              <Wind className="w-3.5 h-3.5 text-sky-600 dark:text-sky-400" />
              <span>{telemetry.temperatureC}°C · Ahala</span>
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
                className={`flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg border text-xs font-medium transition-colors shadow-2xs cursor-pointer ${
                  daltonismMode !== 'normal'
                    ? 'border-[var(--brand-primary)] bg-[var(--brand-primary)]/10 text-[var(--brand-primary)] font-semibold'
                    : 'border-[var(--border-default)] bg-[var(--bg-surface)] hover:bg-[var(--bg-elevated)] text-[var(--text-primary)]'
                }`}
                title="Filtres d'accessibilité visuelle (Deutéranopie, Protanopie, Tritanopie)"
                aria-expanded={daltonismDropdownOpen}
                aria-label="Sélecteur d'accessibilité daltonisme"
              >
                <Eye className="w-4 h-4" />
                <span className="hidden 2xl:inline">{daltonismLabels[daltonismMode]}</span>
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
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[var(--brand-primary)] text-white hover:bg-[var(--brand-secondary)] text-xs font-semibold shadow-xs transition-transform active:scale-95 cursor-pointer"
              title="Ouvrir le laboratoire chromatique Adobe Color & testeur de contraste WCAG"
              aria-label="Ouvrir l'Atelier Chromatique"
            >
              <Palette className="w-4 h-4" />
              <span className="hidden sm:inline">Atelier Couleurs</span>
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
                  onClick={() => handleNavClick(item.id)}
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
