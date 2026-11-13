// ============================================================================
// W3C RELATIVE LUMINANCE & WCAG 2.1 CONTRAST CALCULATOR (src/utils/wcagContrast.ts)
// Feature F30: Pure TypeScript mathematical contrast engine & daltonism simulation
// ============================================================================

import type { DaltonismMode } from '../types/ecosystem';

export interface RGB {
  r: number; // 0 - 255
  g: number; // 0 - 255
  b: number; // 0 - 255
}

export interface ContrastVerdict {
  ratio: number;
  ratioFormatted: string; // e.g. "14.07:1"
  aaNormalText: boolean;  // >= 4.5:1
  aaaNormalText: boolean; // >= 7.0:1
  aaLargeText: boolean;   // >= 3.0:1
  aaaLargeText: boolean;  // >= 4.5:1
  uiComponent: boolean;   // >= 3.0:1 (WCAG 2.1 Non-text contrast)
  overallLevel: 'AAA' | 'AA' | 'AA Large' | 'Échec';
  badgeColor: string;
}

export interface VisionSimulationResult {
  mode: DaltonismMode | 'achromatopsia';
  label: string;
  simulatedFgHex: string;
  simulatedBgHex: string;
  contrastRatio: number;
  contrastFormatted: string;
  aaNormalPass: boolean;
  uiPass: boolean;
}

/**
 * Normalizes a hex string to standard 6-character lowercase hex with leading '#'
 */
export function normalizeHex(hex: string): string {
  if (!hex) return '#000000';
  let cleaned = hex.trim().replace(/^#/, '');
  if (cleaned.length === 3) {
    cleaned = cleaned
      .split('')
      .map((c) => c + c)
      .join('');
  }
  if (cleaned.length !== 6) {
    return '#000000';
  }
  return '#' + cleaned.toUpperCase();
}

/**
 * Parses a Hex color string (#RGB or #RRGGBB) to 8-bit RGB components
 */
export function hexToRgb(hex: string): RGB | null {
  if (!hex) return null;
  const cleaned = hex.trim().replace(/^#/, '');
  let r: number, g: number, b: number;

  if (cleaned.length === 3) {
    r = parseInt(cleaned[0] + cleaned[0], 16);
    g = parseInt(cleaned[1] + cleaned[1], 16);
    b = parseInt(cleaned[2] + cleaned[2], 16);
  } else if (cleaned.length === 6) {
    r = parseInt(cleaned.substring(0, 2), 16);
    g = parseInt(cleaned.substring(2, 4), 16);
    b = parseInt(cleaned.substring(4, 6), 16);
  } else {
    return null;
  }

  if (isNaN(r) || isNaN(g) || isNaN(b)) {
    return null;
  }

  return { r, g, b };
}

/**
 * Converts RGB components to formatted Hex string
 */
export function rgbToHex(rgb: RGB): string {
  const clamp = (val: number) => Math.max(0, Math.min(255, Math.round(val)));
  const rHex = clamp(rgb.r).toString(16).padStart(2, '0').toUpperCase();
  const gHex = clamp(rgb.g).toString(16).padStart(2, '0').toUpperCase();
  const bHex = clamp(rgb.b).toString(16).padStart(2, '0').toUpperCase();
  return `#${rHex}${gHex}${bHex}`;
}

/**
 * Computes W3C WCAG 2.1 Relative Luminance (L) of an RGB color
 * Formula: L = 0.2126 * R_lin + 0.7152 * G_lin + 0.0722 * B_lin
 * where C_lin = C_srgb <= 0.04045 ? C_srgb / 12.92 : ((C_srgb + 0.055) / 1.055)^2.4
 */
export function getRelativeLuminance(rgb: RGB): number {
  const channelToLinear = (c255: number): number => {
    const cSrgb = c255 / 255;
    if (cSrgb <= 0.04045) {
      return cSrgb / 12.92;
    }
    return Math.pow((cSrgb + 0.055) / 1.055, 2.4);
  };

  const rLin = channelToLinear(rgb.r);
  const gLin = channelToLinear(rgb.g);
  const bLin = channelToLinear(rgb.b);

  return 0.2126 * rLin + 0.7152 * gLin + 0.0722 * bLin;
}

/**
 * Calculates WCAG 2.1 Contrast Ratio between two colors
 * Ratio = (L1 + 0.05) / (L2 + 0.05) where L1 is the lighter of the two
 * Returns a number between 1.0 and 21.0
 */
export function getContrastRatio(colorA: string, colorB: string): number {
  const rgbA = hexToRgb(colorA) || { r: 0, g: 0, b: 0 };
  const rgbB = hexToRgb(colorB) || { r: 255, g: 255, b: 255 };

  const lumA = getRelativeLuminance(rgbA);
  const lumB = getRelativeLuminance(rgbB);

  const l1 = Math.max(lumA, lumB);
  const l2 = Math.min(lumA, lumB);

  const ratio = (l1 + 0.05) / (l2 + 0.05);
  return Math.round(ratio * 100) / 100;
}

/**
 * Evaluates WCAG 2.1 AA/AAA compliance thresholds for a given contrast ratio
 */
export function getWCAGCompliance(ratio: number): ContrastVerdict {
  const aaNormalText = ratio >= 4.5;
  const aaaNormalText = ratio >= 7.0;
  const aaLargeText = ratio >= 3.0;
  const aaaLargeText = ratio >= 4.5;
  const uiComponent = ratio >= 3.0;

  let overallLevel: 'AAA' | 'AA' | 'AA Large' | 'Échec' = 'Échec';
  let badgeColor = 'text-red-700 bg-red-100 border-red-300 dark:bg-red-950/60 dark:text-red-300 dark:border-red-800';

  if (aaaNormalText) {
    overallLevel = 'AAA';
    badgeColor = 'text-emerald-800 bg-emerald-100 border-emerald-300 dark:bg-emerald-950/70 dark:text-emerald-300 dark:border-emerald-800';
  } else if (aaNormalText) {
    overallLevel = 'AA';
    badgeColor = 'text-teal-800 bg-teal-100 border-teal-300 dark:bg-teal-950/70 dark:text-teal-300 dark:border-teal-800';
  } else if (aaLargeText) {
    overallLevel = 'AA Large';
    badgeColor = 'text-amber-800 bg-amber-100 border-amber-300 dark:bg-amber-950/70 dark:text-amber-300 dark:border-amber-800';
  }

  return {
    ratio,
    ratioFormatted: `${ratio.toFixed(2)}:1`,
    aaNormalText,
    aaaNormalText,
    aaLargeText,
    aaaLargeText,
    uiComponent,
    overallLevel,
    badgeColor,
  };
}

// ----------------------------------------------------------------------------
// COLOR BLINDNESS MATRIX SIMULATION (Brettel/Vienot sRGB approximations)
// ----------------------------------------------------------------------------

export type DeficiencyMode = DaltonismMode | 'achromatopsia';

/**
 * Simulates how an RGB color is perceived under various forms of color vision deficiency
 */
export function simulateRgbDaltonism(rgb: RGB, mode: DeficiencyMode): RGB {
  const { r, g, b } = rgb;

  switch (mode) {
    case 'normal':
      return { r, g, b };

    case 'protanopia': {
      // Red-blind: L-cone deficiency
      const simR = 0.56667 * r + 0.43333 * g + 0.0 * b;
      const simG = 0.55833 * r + 0.44167 * g + 0.0 * b;
      const simB = 0.0 * r + 0.24167 * g + 0.75833 * b;
      return {
        r: Math.round(Math.min(255, Math.max(0, simR))),
        g: Math.round(Math.min(255, Math.max(0, simG))),
        b: Math.round(Math.min(255, Math.max(0, simB))),
      };
    }

    case 'deuteranopia': {
      // Green-blind: M-cone deficiency
      const simR = 0.625 * r + 0.375 * g + 0.0 * b;
      const simG = 0.7 * r + 0.3 * g + 0.0 * b;
      const simB = 0.0 * r + 0.3 * g + 0.7 * b;
      return {
        r: Math.round(Math.min(255, Math.max(0, simR))),
        g: Math.round(Math.min(255, Math.max(0, simG))),
        b: Math.round(Math.min(255, Math.max(0, simB))),
      };
    }

    case 'tritanopia': {
      // Blue-blind: S-cone deficiency
      const simR = 0.95 * r + 0.05 * g + 0.0 * b;
      const simG = 0.0 * r + 0.43333 * g + 0.56667 * b;
      const simB = 0.0 * r + 0.475 * g + 0.525 * b;
      return {
        r: Math.round(Math.min(255, Math.max(0, simR))),
        g: Math.round(Math.min(255, Math.max(0, simG))),
        b: Math.round(Math.min(255, Math.max(0, simB))),
      };
    }

    case 'achromatopsia': {
      // Monochromacy (total color blindness) - relative luminance greyscale
      const grey = Math.round(0.2126 * r + 0.7152 * g + 0.0722 * b);
      return {
        r: Math.min(255, Math.max(0, grey)),
        g: Math.min(255, Math.max(0, grey)),
        b: Math.min(255, Math.max(0, grey)),
      };
    }

    default:
      return { r, g, b };
  }
}

/**
 * Simulates color blindness on a Hex string and returns the simulated Hex
 */
export function simulateColorBlindness(hex: string, mode: DeficiencyMode): string {
  const rgb = hexToRgb(hex);
  if (!rgb) return hex;
  const simulatedRgb = simulateRgbDaltonism(rgb, mode);
  return rgbToHex(simulatedRgb);
}

/**
 * Calculates the perceived contrast ratio under color blindness simulation
 */
export function getSimulatedContrastRatio(
  colorA: string,
  colorB: string,
  mode: DeficiencyMode
): number {
  if (mode === 'normal') {
    return getContrastRatio(colorA, colorB);
  }
  const simA = simulateColorBlindness(colorA, mode);
  const simB = simulateColorBlindness(colorB, mode);
  return getContrastRatio(simA, simB);
}

/**
 * Comprehensive Daltonism Audit for a color pair across all common deficiencies
 */
export function auditColorPairDaltonism(
  fgHex: string,
  bgHex: string
): VisionSimulationResult[] {
  const modes: { mode: DeficiencyMode; label: string }[] = [
    { mode: 'normal', label: 'Vision Normale (Trichromate)' },
    { mode: 'deuteranopia', label: 'Deutéranopie (Déficit vert)' },
    { mode: 'protanopia', label: 'Protanopie (Déficit rouge)' },
    { mode: 'tritanopia', label: 'Tritanopie (Déficit bleu)' },
    { mode: 'achromatopsia', label: 'Achromatopsie (Niveaux de gris)' },
  ];

  return modes.map(({ mode, label }) => {
    const simFg = simulateColorBlindness(fgHex, mode);
    const simBg = simulateColorBlindness(bgHex, mode);
    const ratio = getContrastRatio(simFg, simBg);

    return {
      mode,
      label,
      simulatedFgHex: simFg,
      simulatedBgHex: simBg,
      contrastRatio: ratio,
      contrastFormatted: `${ratio.toFixed(2)}:1`,
      aaNormalPass: ratio >= 4.5,
      uiPass: ratio >= 3.0,
    };
  });
}
