// ============================================================================
// SLIDE-OVER COLOR ATLAS DRAWER (src/components/design-system/ColorAtlasDrawer.tsx)
// Feature F29: Slide-over design system drawer, Adobe Color palettes & WCAG tester
// ============================================================================

import React, { useState, useEffect } from 'react';
import {
  X,
  Palette,
  Layers,
  SlidersHorizontal,
  Copy,
  Check,
  ExternalLink,
  ShieldCheck,
  ArrowRightLeft,
  Eye,
  Sparkles,
} from 'lucide-react';
import { useEcoPark } from '../../context/EcoParkContext';
import {
  getContrastRatio,
  getWCAGCompliance,
  auditColorPairDaltonism,
  normalizeHex,
  getRelativeLuminance,
  hexToRgb,
} from '../../utils/wcagContrast';

interface ColorStep {
  step: string;
  hex: string;
}

interface Pillar {
  id: string;
  name: string;
  subtitle: string;
  hex: string;
  rgb: string;
  cssVar: string;
  role: string;
  auditNotes: string;
  contrastWhite: string;
  contrastBark: string;
}

export const ColorAtlasDrawer: React.FC = () => {
  const { colorDrawerOpen, setColorDrawerOpen } = useEcoPark();

  // Active Tab: 'pillars' | 'scales' | 'tester'
  const [activeTab, setActiveTab] = useState<'pillars' | 'scales' | 'tester'>('pillars');

  // Copy feedback state
  const [copiedItem, setCopiedItem] = useState<string | null>(null);

  // Scales tab: active scale family
  const [activeScaleFamily, setActiveScaleFamily] = useState<'forest' | 'leaf' | 'earth' | 'mist' | 'bark'>('forest');

  // WCAG Contrast Tester state
  const [fgColor, setFgColor] = useState<string>('#1F2421'); // Deep Bark
  const [bgColor, setBgColor] = useState<string>('#E9F5ED'); // Soft Mist

  // Close on Escape key
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && colorDrawerOpen) {
        setColorDrawerOpen(false);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [colorDrawerOpen, setColorDrawerOpen]);

  const copyToClipboard = (text: string, label: string) => {
    navigator.clipboard.writeText(text);
    setCopiedItem(label);
    setTimeout(() => {
      setCopiedItem(null);
    }, 2200);
  };

  // --------------------------------------------------------------------------
  // Data: 5 Core Chromatic Pillars
  // --------------------------------------------------------------------------
  const PILLARS: Pillar[] = [
    {
      id: 'forest',
      name: 'Deep Forest Green',
      subtitle: 'Canopée Primaire & Identité',
      hex: '#1B4332',
      rgb: 'rgb(27, 67, 50)',
      cssVar: '--color-forest-800',
      role: 'En-têtes, boutons principaux (CTA), navigation supérieure, immersion éditoriale',
      auditNotes: '11.08:1 sur blanc (AAA) · 9.89:1 sur Soft Mist (AAA)',
      contrastWhite: '11.08:1',
      contrastBark: '1.27:1',
    },
    {
      id: 'leaf',
      name: 'Fresh Leaf / Emerald',
      subtitle: 'Feuille & Végétation Active',
      hex: '#52B788',
      rgb: 'rgb(82, 183, 136)',
      cssVar: '--color-leaf-500',
      role: 'Badges éco, indicateurs positifs, états actifs, accents interactifs, sentiers fluides',
      auditNotes: '6.37:1 avec Deep Bark (AA texte normal, AAA grand texte)',
      contrastWhite: '2.21:1',
      contrastBark: '6.37:1',
    },
    {
      id: 'earth',
      name: 'Warm Earth / Ochre',
      subtitle: 'Terre & Roches Sédimentaires',
      hex: '#D4A373',
      rgb: 'rgb(212, 163, 115)',
      cssVar: '--color-earth-400',
      role: 'Mise en avant chaleureuse, balisage sentiers, alertes modérées, cartographie',
      auditNotes: '6.97:1 avec Deep Bark (AA texte normal, AAA grand texte)',
      contrastWhite: '2.02:1',
      contrastBark: '6.97:1',
    },
    {
      id: 'mist',
      name: 'Soft Mist / Sage',
      subtitle: 'Brume & Surfaces Naturelles',
      hex: '#E9F5ED',
      rgb: 'rgb(233, 245, 237)',
      cssVar: '--color-mist-100',
      role: 'Fond de section naturel, cartes douces, arrière-plan haute lisibilité plein soleil',
      auditNotes: '14.07:1 avec Deep Bark (AAA optimal)',
      contrastWhite: '1.13:1',
      contrastBark: '14.07:1',
    },
    {
      id: 'bark',
      name: 'Deep Bark / Charcoal',
      subtitle: 'Écorce & Typographie Sombre',
      hex: '#1F2421',
      rgb: 'rgb(31, 36, 33)',
      cssVar: '--color-bark-900',
      role: 'Corps de texte haute lisibilité, bordures structurantes, mode sombre OLED',
      auditNotes: 'Absorption lumineuse maximale pour supprimer la fatigue oculaire',
      contrastWhite: '15.91:1',
      contrastBark: '1.00:1',
    },
  ];

  // --------------------------------------------------------------------------
  // Data: 50 -> 950 Ramps
  // --------------------------------------------------------------------------
  const COLOR_SCALES: Record<'forest' | 'leaf' | 'earth' | 'mist' | 'bark', { name: string; steps: ColorStep[] }> = {
    forest: {
      name: 'Forest (Canopée)',
      steps: [
        { step: '50', hex: '#EDF7F2' },
        { step: '100', hex: '#D8F3DC' },
        { step: '200', hex: '#B7E4C7' },
        { step: '300', hex: '#95D5B2' },
        { step: '400', hex: '#74C69D' },
        { step: '500', hex: '#52B788' },
        { step: '600', hex: '#40916C' },
        { step: '700', hex: '#2D6A4F' },
        { step: '800', hex: '#1B4332' },
        { step: '900', hex: '#112A1F' },
        { step: '950', hex: '#081C15' },
      ],
    },
    leaf: {
      name: 'Leaf (Feuille)',
      steps: [
        { step: '50', hex: '#F0FAF5' },
        { step: '100', hex: '#D8F3DC' },
        { step: '200', hex: '#B7E4C7' },
        { step: '300', hex: '#95D5B2' },
        { step: '400', hex: '#74C69D' },
        { step: '500', hex: '#52B788' },
        { step: '600', hex: '#3D996E' },
        { step: '700', hex: '#2D7A56' },
        { step: '800', hex: '#215C41' },
        { step: '900', hex: '#163E2C' },
        { step: '950', hex: '#0B2218' },
      ],
    },
    earth: {
      name: 'Earth (Terre & Ocres)',
      steps: [
        { step: '50', hex: '#FBF6F0' },
        { step: '100', hex: '#F5EBE0' },
        { step: '200', hex: '#EBD5BE' },
        { step: '300', hex: '#E0BC99' },
        { step: '400', hex: '#D4A373' },
        { step: '500', hex: '#C08852' },
        { step: '600', hex: '#A46E3B' },
        { step: '700', hex: '#84562D' },
        { step: '800', hex: '#684324' },
        { step: '900', hex: '#4E321B' },
        { step: '950', hex: '#2E1C0E' },
      ],
    },
    mist: {
      name: 'Mist (Brumes & Sauge)',
      steps: [
        { step: '50', hex: '#F6FBF8' },
        { step: '100', hex: '#E9F5ED' },
        { step: '200', hex: '#D4E9DC' },
        { step: '300', hex: '#B5D6C2' },
        { step: '400', hex: '#8EBAA0' },
        { step: '500', hex: '#699B7E' },
        { step: '600', hex: '#527F66' },
        { step: '700', hex: '#3E634F' },
        { step: '800', hex: '#2C4738' },
        { step: '900', hex: '#1C2E24' },
        { step: '950', hex: '#111C16' },
      ],
    },
    bark: {
      name: 'Bark (Écorce & Encre)',
      steps: [
        { step: '50', hex: '#F4F6F5' },
        { step: '100', hex: '#E4E8E5' },
        { step: '200', hex: '#C9D1CC' },
        { step: '300', hex: '#A3B0A8' },
        { step: '400', hex: '#7B8C82' },
        { step: '500', hex: '#5C6B62' },
        { step: '600', hex: '#46534B' },
        { step: '700', hex: '#36403A' },
        { step: '800', hex: '#29302C' },
        { step: '900', hex: '#1F2421' },
        { step: '950', hex: '#121614' },
      ],
    },
  };

  // --------------------------------------------------------------------------
  // Data: 5 Explored Adobe Color Palettes
  // --------------------------------------------------------------------------
  const ADOBE_PALETTES = [
    {
      name: 'Forest & Nature',
      query: 'forest nature',
      swatches: ['#0D2329', '#203B3A', '#395246', '#6D7F6A', '#AAB89B'],
    },
    {
      name: 'This Green',
      query: 'forest nature',
      swatches: ['#616C59', '#354737', '#2F392B', '#302E1E', '#0A110B'],
    },
    {
      name: 'Green bokeh background forest',
      query: 'forest nature',
      swatches: ['#295937', '#0B2516', '#163625', '#7AA968', '#4D814B'],
    },
    {
      name: 'Green Eco Tree',
      query: 'eco green',
      swatches: ['#0D590A', '#148C11', '#25D91A', '#63F250', '#C2F2B8'],
    },
    {
      name: 'Eco friendly',
      query: 'eco green',
      swatches: ['#2D5A27', '#84A98C', '#CAD2C5', '#52796F', '#354F52'],
    },
  ];

  // Quick preset chips for tester
  const QUICK_PRESETS = [
    { label: 'Bark', hex: '#1F2421' },
    { label: 'Mist', hex: '#E9F5ED' },
    { label: 'Forest', hex: '#1B4332' },
    { label: 'Leaf', hex: '#52B788' },
    { label: 'Earth', hex: '#D4A373' },
    { label: 'Blanc', hex: '#FFFFFF' },
    { label: 'Canvas Nuit', hex: '#121614' },
  ];

  // Calculated WCAG Metrics for current FG / BG
  const currentRatio = getContrastRatio(fgColor, bgColor);
  const verdict = getWCAGCompliance(currentRatio);
  const daltonismAudit = auditColorPairDaltonism(fgColor, bgColor);

  const swapColors = () => {
    const temp = fgColor;
    setFgColor(bgColor);
    setBgColor(temp);
  };

  if (!colorDrawerOpen) return null;

  return (
    <div
      className="fixed inset-0 z-50 overflow-hidden"
      role="dialog"
      aria-modal="true"
      aria-labelledby="color-atlas-title"
    >
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black/60 backdrop-blur-xs transition-opacity duration-300"
        onClick={() => setColorDrawerOpen(false)}
        aria-hidden="true"
      />

      {/* Drawer Container (Responsive max-w-xl to max-w-2xl) */}
      <div className="fixed inset-y-0 right-0 max-w-full flex pl-4 sm:pl-10">
        <div className="w-screen max-w-2xl bg-[var(--bg-elevated)] border-l border-[var(--border-default)] shadow-2xl flex flex-col animate-in slide-in-from-right duration-300">
          {/* Header */}
          <div className="p-5 sm:p-6 border-b border-[var(--border-default)] flex items-center justify-between gap-4 bg-[var(--bg-surface)]/50">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-[#52B788] to-[#1B4332] flex items-center justify-center text-white shadow-sm shrink-0">
                <Palette className="w-5 h-5" />
              </div>
              <div>
                <h2
                  id="color-atlas-title"
                  className="font-['Fraunces'] font-bold text-lg sm:text-xl text-[var(--text-primary)] leading-tight"
                >
                  Atelier Chromatique
                </h2>
                <p className="text-xs text-[var(--text-muted)] mt-0.5">
                  5 Piliers Adobe Color · Échelles 50 → 950 · Moteur WCAG 2.1
                </p>
              </div>
            </div>

            <div className="flex items-center gap-2">
              <a
                href="/color-atlas-standalone.html"
                target="_blank"
                rel="noreferrer"
                className="hidden sm:inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-[var(--border-default)] bg-[var(--bg-elevated)] text-xs font-semibold text-[var(--text-primary)] hover:bg-[var(--bg-surface)] transition-colors cursor-pointer"
                title="Ouvrir le prototype interactif autonome dans un nouvel onglet"
              >
                <span>Plein écran</span>
                <ExternalLink className="w-3.5 h-3.5 text-[var(--brand-primary)]" />
              </a>

              <button
                onClick={() => setColorDrawerOpen(false)}
                className="p-2 rounded-lg text-[var(--text-muted)] hover:text-[var(--text-primary)] hover:bg-[var(--bg-surface)] transition-colors cursor-pointer"
                aria-label="Fermer l atelier chromatique"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
          </div>

          {/* Tab Navigation */}
          <div className="px-5 sm:px-6 pt-3 border-b border-[var(--border-default)] flex gap-2 overflow-x-auto bg-[var(--bg-elevated)]">
            <button
              onClick={() => setActiveTab('pillars')}
              className={`flex items-center gap-2 px-3.5 py-2.5 rounded-t-lg text-xs font-bold transition-all border-b-2 cursor-pointer shrink-0 ${
                activeTab === 'pillars'
                  ? 'border-[var(--brand-primary)] text-[var(--brand-primary)] bg-[var(--bg-surface)]'
                  : 'border-transparent text-[var(--text-muted)] hover:text-[var(--text-primary)]'
              }`}
            >
              <Palette className="w-4 h-4" />
              <span>Piliers Chromatiques</span>
            </button>

            <button
              onClick={() => setActiveTab('scales')}
              className={`flex items-center gap-2 px-3.5 py-2.5 rounded-t-lg text-xs font-bold transition-all border-b-2 cursor-pointer shrink-0 ${
                activeTab === 'scales'
                  ? 'border-[var(--brand-primary)] text-[var(--brand-primary)] bg-[var(--bg-surface)]'
                  : 'border-transparent text-[var(--text-muted)] hover:text-[var(--text-primary)]'
              }`}
            >
              <Layers className="w-4 h-4" />
              <span>Échelles 50 → 950</span>
            </button>

            <button
              onClick={() => setActiveTab('tester')}
              className={`flex items-center gap-2 px-3.5 py-2.5 rounded-t-lg text-xs font-bold transition-all border-b-2 cursor-pointer shrink-0 ${
                activeTab === 'tester'
                  ? 'border-[var(--brand-primary)] text-[var(--brand-primary)] bg-[var(--bg-surface)]'
                  : 'border-transparent text-[var(--text-muted)] hover:text-[var(--text-primary)]'
              }`}
            >
              <SlidersHorizontal className="w-4 h-4" />
              <span>Palettes Adobe &amp; Testeur WCAG</span>
            </button>
          </div>

          {/* Drawer Body */}
          <div className="flex-1 overflow-y-auto p-5 sm:p-6 space-y-6">
            {/* Notification Toast for Clipboard Copy */}
            {copiedItem && (
              <div className="sticky top-0 z-30 p-2.5 rounded-xl bg-emerald-600 text-white text-xs font-semibold shadow-lg flex items-center justify-between animate-in fade-in duration-200">
                <div className="flex items-center gap-2">
                  <Check className="w-4 h-4" />
                  <span>{copiedItem}</span>
                </div>
                <span className="text-[10px] opacity-80">Prêt à coller</span>
              </div>
            )}

            {/* ============================================================= */}
            {/* TAB 1: PILIERS CHROMATIQUES                                   */}
            {/* ============================================================= */}
            {activeTab === 'pillars' && (
              <div className="space-y-5">
                <div className="p-4 rounded-xl bg-[var(--bg-surface)] border border-[var(--border-default)] text-xs text-[var(--text-muted)] space-y-1.5">
                  <div className="font-semibold text-[var(--text-primary)] flex items-center gap-2">
                    <ShieldCheck className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
                    <span>Charte d Accessibilité Validée sur Adobe Color</span>
                  </div>
                  <p>
                    Les 5 piliers constituent l armature graphique d ECO-PARK. Chaque teinte a été choisie
                    sur le cercle chromatique pour concilier immersion naturelle et ratios WCAG AAA stricts.
                  </p>
                </div>

                <div className="space-y-4">
                  {PILLARS.map((pillar) => (
                    <div
                      key={pillar.id}
                      className="p-4 sm:p-5 rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-default)] hover:shadow-sm transition-all space-y-3"
                    >
                      {/* Swatch & Identity */}
                      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                        <div className="flex items-center gap-3">
                          <div
                            className="w-12 h-12 rounded-xl border border-black/15 shadow-inner shrink-0"
                            style={{ backgroundColor: pillar.hex }}
                          />
                          <div>
                            <h3 className="font-['Fraunces'] font-bold text-base text-[var(--text-primary)]">
                              {pillar.name}
                            </h3>
                            <div className="text-xs text-[var(--text-muted)]">
                              {pillar.subtitle}
                            </div>
                          </div>
                        </div>

                        {/* 1-Click Copy Chips */}
                        <div className="flex flex-wrap items-center gap-1.5">
                          <button
                            onClick={() => copyToClipboard(pillar.hex, `HEX ${pillar.hex} copié`)}
                            className="px-2.5 py-1 rounded-lg bg-[var(--bg-elevated)] border border-[var(--border-default)] font-mono text-xs font-bold text-[var(--text-primary)] hover:border-[var(--brand-primary)] hover:text-[var(--brand-primary)] transition-colors cursor-pointer flex items-center gap-1"
                            title="Copier le code HEX"
                          >
                            <Copy className="w-3 h-3" />
                            <span>{pillar.hex}</span>
                          </button>

                          <button
                            onClick={() => copyToClipboard(pillar.rgb, `RGB ${pillar.rgb} copié`)}
                            className="px-2 py-1 rounded-lg bg-[var(--bg-elevated)] border border-[var(--border-default)] font-mono text-[11px] text-[var(--text-muted)] hover:text-[var(--text-primary)] transition-colors cursor-pointer"
                            title="Copier la valeur RGB"
                          >
                            RGB
                          </button>

                          <button
                            onClick={() => copyToClipboard(pillar.cssVar, `Variable ${pillar.cssVar} copiée`)}
                            className="px-2 py-1 rounded-lg bg-[var(--bg-elevated)] border border-[var(--border-default)] font-mono text-[11px] text-[var(--text-muted)] hover:text-[var(--text-primary)] transition-colors cursor-pointer"
                            title="Copier la variable CSS"
                          >
                            CSS
                          </button>
                        </div>
                      </div>

                      {/* Usage & Audit Notes */}
                      <div className="pt-2 border-t border-[var(--border-default)]/60 text-xs space-y-1">
                        <div>
                          <span className="font-semibold text-[var(--text-primary)]">Rôle : </span>
                          <span className="text-[var(--text-muted)]">{pillar.role}</span>
                        </div>
                        <div className="flex items-center gap-1 text-[11px] text-emerald-800 dark:text-emerald-300 font-mono">
                          <Sparkles className="w-3 h-3 text-emerald-600 dark:text-emerald-400 shrink-0" />
                          <span>{pillar.auditNotes}</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* ============================================================= */}
            {/* TAB 2: ÉCHELLES 50 -> 950                                      */}
            {/* ============================================================= */}
            {activeTab === 'scales' && (
              <div className="space-y-5">
                {/* Scale Family Selector */}
                <div className="flex flex-wrap items-center gap-1.5 p-1 rounded-xl bg-[var(--bg-surface)] border border-[var(--border-default)]">
                  {(['forest', 'leaf', 'earth', 'mist', 'bark'] as const).map((fam) => (
                    <button
                      key={fam}
                      onClick={() => setActiveScaleFamily(fam)}
                      className={`flex-1 min-w-[70px] py-1.5 px-2 rounded-lg text-xs font-semibold capitalize transition-all cursor-pointer ${
                        activeScaleFamily === fam
                          ? 'bg-[var(--bg-elevated)] text-[var(--brand-primary)] shadow-xs font-bold border border-[var(--border-default)]'
                          : 'text-[var(--text-muted)] hover:text-[var(--text-primary)]'
                      }`}
                    >
                      {fam}
                    </button>
                  ))}
                </div>

                {/* Swatches List for the active family */}
                <div className="space-y-2">
                  <div className="flex items-center justify-between text-xs text-[var(--text-muted)] px-1">
                    <span className="font-bold text-[var(--text-primary)]">
                      Nuancier {COLOR_SCALES[activeScaleFamily].name}
                    </span>
                    <span>11 échelons harmoniques (50 à 950)</span>
                  </div>

                  <div className="space-y-1.5">
                    {COLOR_SCALES[activeScaleFamily].steps.map((st) => {
                      const rgb = hexToRgb(st.hex) || { r: 128, g: 128, b: 128 };
                      const lum = getRelativeLuminance(rgb);
                      const isDark = lum < 0.25;
                      const textColor = isDark ? '#FFFFFF' : '#121614';
                      const badgeBg = isDark ? 'bg-white/15 text-white' : 'bg-black/10 text-black';

                      return (
                        <div
                          key={st.step}
                          onClick={() => copyToClipboard(st.hex, `Échelon ${st.step} (${st.hex}) copié`)}
                          className="group relative p-3 rounded-xl border border-black/10 flex items-center justify-between transition-transform hover:scale-[1.01] active:scale-[0.99] cursor-pointer shadow-xs"
                          style={{ backgroundColor: st.hex }}
                          title={`Cliquez pour copier ${st.hex}`}
                        >
                          <div className="flex items-center gap-3">
                            <span
                              className={`px-2 py-0.5 rounded text-xs font-mono font-bold ${badgeBg}`}
                            >
                              {st.step}
                            </span>
                            <span
                              className="font-mono text-xs font-bold tracking-wider"
                              style={{ color: textColor }}
                            >
                              {st.hex}
                            </span>
                          </div>

                          <div className="flex items-center gap-2 text-xs font-mono" style={{ color: textColor }}>
                            <span className="text-[10px] opacity-75">
                              Lum: {Math.round(lum * 100)}%
                            </span>
                            <Copy className="w-3.5 h-3.5 opacity-60 group-hover:opacity-100 transition-opacity" />
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>

                {/* Quick copy all CSS variables for this scale */}
                <div className="pt-2 flex justify-end">
                  <button
                    onClick={() => {
                      const snippet = COLOR_SCALES[activeScaleFamily].steps
                        .map((s) => `--color-${activeScaleFamily}-${s.step}: ${s.hex};`)
                        .join('\n');
                      copyToClipboard(snippet, `Variables CSS de l'échelle ${activeScaleFamily} copiées`);
                    }}
                    className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-[var(--border-default)] bg-[var(--bg-surface)] text-xs font-semibold text-[var(--brand-primary)] hover:bg-[var(--bg-elevated)] transition-colors cursor-pointer"
                  >
                    <Copy className="w-3.5 h-3.5" />
                    <span>Copier les variables CSS de cette échelle</span>
                  </button>
                </div>
              </div>
            )}

            {/* ============================================================= */}
            {/* TAB 3: PALETTES ADOBE COLOR & TESTEUR WCAG 2.1                 */}
            {/* ============================================================= */}
            {activeTab === 'tester' && (
              <div className="space-y-6">
                {/* 1. Explored Adobe Palettes */}
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <h3 className="font-['Fraunces'] font-bold text-sm text-[var(--text-primary)]">
                      Palettes Thématiques Extraites d Adobe Color Explore
                    </h3>
                    <span className="text-[11px] text-[var(--text-muted)] font-mono">
                      5 harmonies certifiées
                    </span>
                  </div>

                  <div className="space-y-2.5">
                    {ADOBE_PALETTES.map((pal) => (
                      <div
                        key={pal.name}
                        className="p-3 rounded-xl bg-[var(--bg-surface)] border border-[var(--border-default)] space-y-2"
                      >
                        <div className="flex items-center justify-between text-xs">
                          <span className="font-bold text-[var(--text-primary)]">{pal.name}</span>
                          <span className="text-[10px] font-mono text-[var(--text-muted)]">
                            req: {pal.query}
                          </span>
                        </div>

                        {/* 5 Swatches Bar */}
                        <div className="grid grid-cols-5 gap-1.5 rounded-lg overflow-hidden">
                          {pal.swatches.map((hex, idx) => (
                            <button
                              key={idx}
                              onClick={() => {
                                setFgColor(hex);
                                copyToClipboard(hex, `Couleur ${hex} sélectionnée pour le texte`);
                              }}
                              className="group relative h-9 rounded-md border border-black/10 flex flex-col items-center justify-center transition-transform hover:scale-105 active:scale-95 cursor-pointer"
                              style={{ backgroundColor: hex }}
                              title={`Cliquer pour définir ${hex} comme couleur de texte`}
                            >
                              <span className="text-[9px] font-mono text-white/90 drop-shadow-xs font-bold opacity-0 group-hover:opacity-100 transition-opacity">
                                FG
                              </span>
                            </button>
                          ))}
                        </div>

                        <div className="flex items-center justify-between text-[11px]">
                          <div className="flex gap-2 font-mono text-[10px] text-[var(--text-muted)]">
                            {pal.swatches.map((h, i) => (
                              <span key={i}>{h}</span>
                            ))}
                          </div>
                          <button
                            onClick={() => {
                              setFgColor(pal.swatches[0]);
                              setBgColor(pal.swatches[4]);
                            }}
                            className="text-[10px] text-[var(--brand-primary)] font-semibold hover:underline cursor-pointer"
                          >
                            Tester cette paire
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* 2. Interactive WCAG Contrast Calculator (Feature F30) */}
                <div className="p-5 rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-default)] space-y-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="font-['Fraunces'] font-bold text-base text-[var(--text-primary)]">
                        Calculateur de Contraste WCAG 2.1 en Temps Réel
                      </h3>
                      <p className="text-xs text-[var(--text-muted)]">
                        Formule W3C de luminance relative &amp; simulation de vision
                      </p>
                    </div>

                    <button
                      onClick={swapColors}
                      className="p-2 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)] text-[var(--text-primary)] hover:border-[var(--brand-primary)] transition-all cursor-pointer flex items-center gap-1 text-xs font-semibold"
                      title="Inverser Premier Plan et Arrière-Plan"
                    >
                      <ArrowRightLeft className="w-3.5 h-3.5" />
                      <span className="hidden sm:inline">Inverser</span>
                    </button>
                  </div>

                  {/* Color Selectors */}
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    {/* Foreground Input */}
                    <div className="space-y-2">
                      <label className="block text-xs font-semibold text-[var(--text-primary)]">
                        Texte (Premier Plan)
                      </label>
                      <div className="flex items-center gap-2">
                        <input
                          type="color"
                          value={normalizeHex(fgColor)}
                          onChange={(e) => setFgColor(e.target.value.toUpperCase())}
                          className="w-10 h-10 rounded-lg cursor-pointer border border-[var(--border-default)] bg-transparent p-0.5"
                        />
                        <input
                          type="text"
                          value={fgColor}
                          onChange={(e) => setFgColor(e.target.value)}
                          className="flex-1 px-3 py-2 rounded-lg bg-[var(--bg-elevated)] border border-[var(--border-default)] text-xs font-mono font-bold text-[var(--text-primary)] focus:outline-none focus:ring-1 focus:ring-[var(--brand-primary)]"
                        />
                      </div>
                    </div>

                    {/* Background Input */}
                    <div className="space-y-2">
                      <label className="block text-xs font-semibold text-[var(--text-primary)]">
                        Fond (Arrière-Plan)
                      </label>
                      <div className="flex items-center gap-2">
                        <input
                          type="color"
                          value={normalizeHex(bgColor)}
                          onChange={(e) => setBgColor(e.target.value.toUpperCase())}
                          className="w-10 h-10 rounded-lg cursor-pointer border border-[var(--border-default)] bg-transparent p-0.5"
                        />
                        <input
                          type="text"
                          value={bgColor}
                          onChange={(e) => setBgColor(e.target.value)}
                          className="flex-1 px-3 py-2 rounded-lg bg-[var(--bg-elevated)] border border-[var(--border-default)] text-xs font-mono font-bold text-[var(--text-primary)] focus:outline-none focus:ring-1 focus:ring-[var(--brand-primary)]"
                        />
                      </div>
                    </div>
                  </div>

                  {/* Quick Preset Chips */}
                  <div className="flex flex-wrap items-center gap-1.5 pt-1">
                    <span className="text-[10px] text-[var(--text-muted)] font-semibold uppercase">
                      Raccourcis :
                    </span>
                    {QUICK_PRESETS.map((p) => (
                      <button
                        key={p.label}
                        onClick={() => setFgColor(p.hex)}
                        onContextMenu={(e) => {
                          e.preventDefault();
                          setBgColor(p.hex);
                        }}
                        className="px-2 py-0.5 rounded text-[10px] font-mono border border-[var(--border-default)] bg-[var(--bg-elevated)] hover:bg-[var(--bg-canvas)] transition-colors cursor-pointer flex items-center gap-1"
                        title="Clic gauche: Texte | Clic droit: Fond"
                      >
                        <span
                          className="w-2 h-2 rounded-full border border-black/20"
                          style={{ backgroundColor: p.hex }}
                        />
                        <span>{p.label}</span>
                      </button>
                    ))}
                  </div>

                  {/* Live Rendering Preview Card */}
                  <div
                    className="p-5 rounded-2xl border border-black/10 transition-colors shadow-inner space-y-3"
                    style={{ backgroundColor: bgColor, color: fgColor }}
                  >
                    <div className="text-[10px] font-mono font-bold uppercase tracking-wider opacity-75">
                      Aperçu de Rendu Typographique &amp; Composant
                    </div>
                    <div className="font-['Fraunces'] text-xl sm:text-2xl font-bold leading-tight">
                      Forêt &amp; Canopée Sauvage ECO-PARK
                    </div>
                    <p className="text-xs leading-relaxed max-w-lg opacity-90 font-sans">
                      La réserve naturelle préserve les corridors biologiques essentiels. Cette surface
                      illustre le contraste perçu dans l interface en conditions réelles.
                    </p>
                    <div className="pt-2 flex items-center gap-2">
                      <span
                        className="px-3 py-1.5 rounded-lg text-xs font-bold border"
                        style={{
                          borderColor: fgColor,
                          backgroundColor: bgColor,
                          color: fgColor,
                        }}
                      >
                        Composant UI Actif
                      </span>
                      <span className="text-[11px] font-mono opacity-80">
                        {currentRatio >= 3.0 ? '✓ Ratio UI Valide' : '⚠ Non conforme UI'}
                      </span>
                    </div>
                  </div>

                  {/* Contrast Scoreboard & Conformance Badges */}
                  <div className="p-4 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)] flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                    <div>
                      <div className="text-[10px] text-[var(--text-muted)] font-mono uppercase font-semibold">
                        Ratio Mathématique W3C
                      </div>
                      <div className="text-3xl font-['Fraunces'] font-bold text-[var(--text-primary)]">
                        {verdict.ratioFormatted}
                      </div>
                    </div>

                    <div className="flex flex-wrap items-center gap-2">
                      {/* Normal Text AA */}
                      <div
                        className={`px-2.5 py-1 rounded-lg text-xs font-bold border flex items-center gap-1 ${
                          verdict.aaNormalText
                            ? 'bg-emerald-100 text-emerald-800 border-emerald-300 dark:bg-emerald-950/70 dark:text-emerald-300 dark:border-emerald-800'
                            : 'bg-red-100 text-red-800 border-red-300 dark:bg-red-950/70 dark:text-red-300 dark:border-red-800'
                        }`}
                      >
                        {verdict.aaNormalText ? <Check className="w-3.5 h-3.5" /> : <X className="w-3.5 h-3.5" />}
                        <span>AA Normal (4.5:1)</span>
                      </div>

                      {/* Normal Text AAA */}
                      <div
                        className={`px-2.5 py-1 rounded-lg text-xs font-bold border flex items-center gap-1 ${
                          verdict.aaaNormalText
                            ? 'bg-emerald-100 text-emerald-800 border-emerald-300 dark:bg-emerald-950/70 dark:text-emerald-300 dark:border-emerald-800'
                            : 'bg-zinc-100 text-zinc-600 border-zinc-300 dark:bg-zinc-800 dark:text-zinc-400 dark:border-zinc-700'
                        }`}
                      >
                        {verdict.aaaNormalText ? <Check className="w-3.5 h-3.5" /> : <X className="w-3.5 h-3.5" />}
                        <span>AAA Normal (7.0:1)</span>
                      </div>

                      {/* UI Non-Text (3.0:1) */}
                      <div
                        className={`px-2.5 py-1 rounded-lg text-xs font-bold border flex items-center gap-1 ${
                          verdict.uiComponent
                            ? 'bg-teal-100 text-teal-800 border-teal-300 dark:bg-teal-950/70 dark:text-teal-300 dark:border-teal-800'
                            : 'bg-red-100 text-red-800 border-red-300 dark:bg-red-950/70 dark:text-red-300 dark:border-red-800'
                        }`}
                      >
                        {verdict.uiComponent ? <Check className="w-3.5 h-3.5" /> : <X className="w-3.5 h-3.5" />}
                        <span>Composants UI (3.0:1)</span>
                      </div>
                    </div>
                  </div>

                  {/* 3. Daltonism Vision Deficiency Simulation Table */}
                  <div className="space-y-2 pt-2 border-t border-[var(--border-default)]/60">
                    <div className="flex items-center gap-2">
                      <Eye className="w-4 h-4 text-[var(--brand-primary)]" />
                      <h4 className="text-xs font-bold text-[var(--text-primary)]">
                        Simulation Matricielle du Daltonisme (Brettel / Viénot)
                      </h4>
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
                      {daltonismAudit.map((sim) => (
                        <div
                          key={sim.mode}
                          className="p-2.5 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)] flex items-center justify-between gap-2"
                        >
                          <div className="flex items-center gap-2 min-w-0">
                            {/* Color chips preview */}
                            <div className="flex items-center -space-x-1 shrink-0">
                              <span
                                className="w-4 h-4 rounded-full border border-black/20"
                                style={{ backgroundColor: sim.simulatedBgHex }}
                                title={`Fond simulé: ${sim.simulatedBgHex}`}
                              />
                              <span
                                className="w-4 h-4 rounded-full border border-black/20 shadow-xs"
                                style={{ backgroundColor: sim.simulatedFgHex }}
                                title={`Texte simulé: ${sim.simulatedFgHex}`}
                              />
                            </div>

                            <span className="text-[11px] font-semibold text-[var(--text-primary)] truncate">
                              {sim.label}
                            </span>
                          </div>

                          <div className="flex items-center gap-1.5 shrink-0 font-mono">
                            <span className="text-[11px] font-bold text-[var(--text-primary)]">
                              {sim.contrastFormatted}
                            </span>
                            {sim.aaNormalPass ? (
                              <span className="w-2 h-2 rounded-full bg-emerald-500" title="Conforme AA" />
                            ) : sim.uiPass ? (
                              <span className="w-2 h-2 rounded-full bg-amber-500" title="Conforme grand texte uniquement" />
                            ) : (
                              <span className="w-2 h-2 rounded-full bg-red-500" title="Non conforme" />
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
