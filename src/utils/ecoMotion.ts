// ============================================================================
// ECO-MOTION ENGINE & KINETIC SOBRIETY GOVERNANCE (src/utils/ecoMotion.ts)
// Zero external dependencies · GPU-only (transform, opacity, clip-path)
// Respects prefers-reduced-motion, hidden tab pause & OLED eco-energy mode
// ============================================================================

import { useState, useEffect, useRef } from 'react';
import { flushSync } from 'react-dom';
import type { TrailStatus } from '../types/ecosystem.ts';

export type ViewTransitionKind = 'lisiere' | 'sunrise' | 'oled-extinguish';

export interface MotionOrigin {
  x: number;
  y: number;
  timestamp: number;
}

export interface ClipOriginMetrics {
  originX: string;
  originY: string;
  endRadiusPx: number;
}

export interface QrModuleSeed {
  row: number;
  col: number;
  delayMs: number;
  isFinder: boolean;
}

export interface BotanicalGrowthStage {
  stage: number; // Normalized 0..1
  isWilted: boolean;
  stemDrawRatio: number; // 0.35..1
  activeBranches: number; // 0..4
  activeLeaves: number; // 0..8
  stageLabel: string;
}

export interface TrailWavePayload {
  trailId: string;
  status: TrailStatus;
  timestamp: number;
}

interface ViewTransitionHandle {
  finished: Promise<void>;
  ready: Promise<void>;
  updateCallbackDone: Promise<void>;
}

type DocumentWithVT = Document & {
  startViewTransition?: (callback: () => void) => ViewTransitionHandle;
};

const TRAIL_WAVE_STORAGE_KEY = 'eco_park_ahala_v2_last_trail_wave';
export const TRAIL_WAVE_EVENT_NAME = 'ecopark:trail-wave';

let lastRecordedOrigin: MotionOrigin | null = null;

// ----------------------------------------------------------------------------
// 1. Pure Mathematical & Geometric Helpers (Unit-Testable in Node)
// ----------------------------------------------------------------------------

/**
 * Computes CSS clip-path origin coordinates and exact Euclidean radius to the
 * farthest viewport corner so circular/organic reveals cover 100% of screen.
 */
export function computeOrganicClipOrigin(
  x: number,
  y: number,
  viewportWidth: number,
  viewportHeight: number
): ClipOriginMetrics {
  const safeW = Math.max(1, viewportWidth);
  const safeH = Math.max(1, viewportHeight);
  const clampedX = Math.max(0, Math.min(safeW, x));
  const clampedY = Math.max(0, Math.min(safeH, y));

  const maxDx = Math.max(clampedX, safeW - clampedX);
  const maxDy = Math.max(clampedY, safeH - clampedY);
  const endRadiusPx = Math.ceil(Math.hypot(maxDx, maxDy));

  return {
    originX: `${Math.round(clampedX)}px`,
    originY: `${Math.round(clampedY)}px`,
    endRadiusPx,
  };
}

/**
 * Computes deterministic spiral botanical germination delays for every dark
 * module in an ISO QR matrix:
 * - 3 corner Finder Patterns (7x7) lock early (0..110ms) for instant scanner readiness
 * - Data & alignment modules germinate outward from center along a spiral wave
 */
export function computeSpiralGerminationDelays(
  matrix: boolean[][],
  maxDelayMs: number = 640
): QrModuleSeed[] {
  const size = matrix.length;
  if (size === 0) return [];

  const center = (size - 1) / 2;
  const maxRadius = Math.max(1, Math.hypot(center, center));
  const safeMaxDelay = Math.max(140, maxDelayMs);
  const seeds: QrModuleSeed[] = [];

  const getFinderAnchorCenter = (r: number, c: number): [number, number] | null => {
    if (r < 7 && c < 7) return [3, 3];
    if (r < 7 && c >= size - 7) return [3, size - 4];
    if (r >= size - 7 && c < 7) return [size - 4, 3];
    return null;
  };

  for (let r = 0; r < size; r++) {
    const rowArr = matrix[r];
    if (!rowArr) continue;
    for (let c = 0; c < rowArr.length; c++) {
      if (!rowArr[c]) continue;

      const finderCenter = getFinderAnchorCenter(r, c);
      if (finderCenter) {
        const distFromFinderCore = Math.hypot(r - finderCenter[0], c - finderCenter[1]);
        const finderDelay = Math.round(Math.min(1, distFromFinderCore / 4.5) * 110);
        seeds.push({
          row: r,
          col: c,
          delayMs: finderDelay,
          isFinder: true,
        });
      } else {
        const dr = r - center;
        const dc = c - center;
        const radialNorm = Math.min(1, Math.hypot(dr, dc) / maxRadius);
        const angleNorm = (Math.atan2(dr, dc) + Math.PI) / (2 * Math.PI);
        const spiralScore = Math.min(1, radialNorm * 0.78 + angleNorm * 0.22);
        const delayMs = Math.round(65 + spiralScore * (safeMaxDelay - 65));

        seeds.push({
          row: r,
          col: c,
          delayMs,
          isFinder: false,
        });
      }
    }
  }

  return seeds;
}

/**
 * Maps avoided CO₂ (kg) to a multi-stage botanical growth profile used by the
 * "De la graine à l'arbre" SVG calculator in BookingWizard.
 */
export function computeBotanicalGrowthStage(co2AvoidedKg: number): BotanicalGrowthStage {
  if (!Number.isFinite(co2AvoidedKg) || co2AvoidedKg <= 0) {
    return {
      stage: 0,
      isWilted: true,
      stemDrawRatio: 0.36,
      activeBranches: 0,
      activeLeaves: 1,
      stageLabel: 'Pousse en dormance (0 kg CO₂ évité)',
    };
  }

  // Normalize 0..20 kg avoided for typical group bookings (1..6 visitors)
  const stage = Math.min(1, Math.max(0.12, co2AvoidedKg / 18));
  const stemDrawRatio = Number((0.42 + stage * 0.58).toFixed(2));
  const activeBranches = Math.min(4, Math.max(1, Math.ceil(stage * 4)));
  const activeLeaves = Math.min(8, Math.max(2, Math.ceil(stage * 8)));

  let stageLabel = 'Jeune pousse forestière';
  if (stage >= 0.85) {
    stageLabel = 'Arbre canopée d’Ahala épanoui';
  } else if (stage >= 0.5) {
    stageLabel = 'Arbuste vigoureux en croissance';
  }

  return {
    stage: Number(stage.toFixed(3)),
    isWilted: false,
    stemDrawRatio,
    activeBranches,
    activeLeaves,
    stageLabel,
  };
}

/**
 * Smooth easeOutExpo interpolation for odometer and telemetry counters.
 */
export function interpolateEaseOutExpo(from: number, to: number, progress: number): number {
  const t = Math.max(0, Math.min(1, progress));
  if (t === 1) return to;
  const eased = 1 - Math.pow(2, -10 * t);
  return from + (to - from) * eased;
}

// ----------------------------------------------------------------------------
// 2. Browser Motion Governance & View Transitions API Orchestration
// ----------------------------------------------------------------------------

export function isReducedMotionPreferred(): boolean {
  if (typeof window === 'undefined' || typeof window.matchMedia !== 'function') {
    return false;
  }
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
}

/**
 * Records pointer coordinates on click/tap so subsequent View Transitions
 * expand organically from the exact interactive trigger.
 */
export function recordMotionOrigin(
  event?: { clientX?: number; clientY?: number } | null
): void {
  if (typeof window === 'undefined' || typeof document === 'undefined') return;

  const x =
    event && typeof event.clientX === 'number' && event.clientX > 0
      ? event.clientX
      : window.innerWidth / 2;
  const y =
    event && typeof event.clientY === 'number' && event.clientY > 0
      ? event.clientY
      : 48;

  lastRecordedOrigin = { x, y, timestamp: Date.now() };

  const metrics = computeOrganicClipOrigin(x, y, window.innerWidth, window.innerHeight);
  const root = document.documentElement;
  root.style.setProperty('--vt-origin-x', metrics.originX);
  root.style.setProperty('--vt-origin-y', metrics.originY);
  root.style.setProperty('--vt-end-radius', `${metrics.endRadiusPx}px`);
}

/**
 * Executes a state mutation inside the native View Transitions API when
 * supported and permitted by user motion preferences; degrades cleanly to an
 * immediate update otherwise.
 */
export function runEcoViewTransition(
  kind: ViewTransitionKind,
  updateCallback: () => void
): void {
  if (typeof window === 'undefined' || typeof document === 'undefined') {
    updateCallback();
    return;
  }

  const doc = document as DocumentWithVT;
  if (isReducedMotionPreferred() || typeof doc.startViewTransition !== 'function') {
    updateCallback();
    return;
  }

  // Refresh origin fallback if no recent click was captured in the last 700ms
  const now = Date.now();
  if (!lastRecordedOrigin || now - lastRecordedOrigin.timestamp > 700) {
    const metrics = computeOrganicClipOrigin(
      window.innerWidth / 2,
      44,
      window.innerWidth,
      window.innerHeight
    );
    document.documentElement.style.setProperty('--vt-origin-x', metrics.originX);
    document.documentElement.style.setProperty('--vt-origin-y', metrics.originY);
    document.documentElement.style.setProperty('--vt-end-radius', `${metrics.endRadiusPx}px`);
  }

  const root = document.documentElement;
  root.dataset.vtKind = kind;

  try {
    const transition = doc.startViewTransition(() => {
      flushSync(() => {
        updateCallback();
      });
    });

    transition.finished
      .catch(() => {
        // Ignore skipped/superseded transition rejections on rapid navigation
      })
      .finally(() => {
        if (root.dataset.vtKind === kind) {
          delete root.dataset.vtKind;
        }
      });
  } catch {
    delete root.dataset.vtKind;
    updateCallback();
  }
}

// ----------------------------------------------------------------------------
// 3. Cross-View Cartographic Wave Bus (RangerDashboard <-> InteractiveTopoMap)
// ----------------------------------------------------------------------------

export function emitTrailStatusWave(trailId: string, status: TrailStatus): void {
  if (typeof window === 'undefined') return;
  const payload: TrailWavePayload = {
    trailId,
    status,
    timestamp: Date.now(),
  };

  try {
    window.sessionStorage.setItem(TRAIL_WAVE_STORAGE_KEY, JSON.stringify(payload));
  } catch {
    // Ignore sessionStorage restrictions
  }

  window.dispatchEvent(new CustomEvent<TrailWavePayload>(TRAIL_WAVE_EVENT_NAME, { detail: payload }));
}

export function consumeRecentTrailWave(maxAgeMs: number = 30000): TrailWavePayload | null {
  if (typeof window === 'undefined') return null;
  try {
    const raw = window.sessionStorage.getItem(TRAIL_WAVE_STORAGE_KEY);
    if (!raw) return null;
    const parsed = JSON.parse(raw) as TrailWavePayload;
    window.sessionStorage.removeItem(TRAIL_WAVE_STORAGE_KEY);
    if (Date.now() - parsed.timestamp <= maxAgeMs) {
      return parsed;
    }
  } catch {
    // Ignore malformed payload
  }
  return null;
}

// ----------------------------------------------------------------------------
// 4. Web Animations API FLIP / Arc Token Flight (Booking -> Navbar Quota/Pass)
// ----------------------------------------------------------------------------

export function launchQuotaFlightToken(
  sourceEl: HTMLElement | null,
  targetSelector: string,
  badgeText: string,
  accentHex: string = '#52B788'
): void {
  if (
    typeof window === 'undefined' ||
    typeof document === 'undefined' ||
    !sourceEl ||
    isReducedMotionPreferred()
  ) {
    return;
  }

  const targetEl = document.querySelector<HTMLElement>(targetSelector);
  if (!targetEl || typeof document.body.animate !== 'function') return;

  const srcRect = sourceEl.getBoundingClientRect();
  const dstRect = targetEl.getBoundingClientRect();
  if (dstRect.width === 0 && dstRect.height === 0) return;

  const startX = srcRect.left + srcRect.width / 2;
  const startY = srcRect.top + srcRect.height / 2;
  const endX = dstRect.left + dstRect.width / 2;
  const endY = dstRect.top + dstRect.height / 2;

  const midX = (startX + endX) / 2;
  const midY = Math.min(startY, endY) - 64;

  const token = document.createElement('div');
  token.setAttribute('aria-hidden', 'true');
  token.textContent = badgeText;
  Object.assign(token.style, {
    position: 'fixed',
    left: '0px',
    top: '0px',
    zIndex: '9999',
    pointerEvents: 'none',
    padding: '4px 10px',
    borderRadius: '9999px',
    backgroundColor: '#1B4332',
    color: '#E9F5ED',
    border: `1.5px solid ${accentHex}`,
    boxShadow: '0 10px 24px -6px rgba(18, 22, 20, 0.55)',
    fontFamily: "'JetBrains Mono', monospace",
    fontSize: '11px',
    fontWeight: '700',
    whiteSpace: 'nowrap',
    willChange: 'transform, opacity',
  });

  document.body.appendChild(token);

  const animation = token.animate(
    [
      {
        transform: `translate3d(${startX}px, ${startY}px, 0) translate(-50%, -50%) scale(0.75)`,
        opacity: 0,
      },
      {
        transform: `translate3d(${startX}px, ${startY - 14}px, 0) translate(-50%, -50%) scale(1.06)`,
        opacity: 1,
        offset: 0.18,
      },
      {
        transform: `translate3d(${midX}px, ${midY}px, 0) translate(-50%, -50%) scale(0.96)`,
        opacity: 0.98,
        offset: 0.58,
      },
      {
        transform: `translate3d(${endX}px, ${endY}px, 0) translate(-50%, -50%) scale(0.45)`,
        opacity: 0.15,
      },
    ],
    {
      duration: 720,
      easing: 'cubic-bezier(0.22, 1, 0.36, 1)',
      fill: 'forwards',
    }
  );

  animation.finished
    .catch(() => {})
    .finally(() => {
      token.remove();
      targetEl.setAttribute('data-motion-pulse', 'true');
      window.setTimeout(() => {
        targetEl.removeAttribute('data-motion-pulse');
      }, 650);
    });
}

// ----------------------------------------------------------------------------
// 5. React Hooks: Kinetic Sobriety Monitor & Smooth Rolling Counter
// ----------------------------------------------------------------------------

export interface EcoMotionState {
  reducedMotion: boolean;
  pageHidden: boolean;
  oledEcoPaused: boolean;
  ambientActive: boolean;
}

export function useEcoMotion(isOledMode: boolean = false): EcoMotionState {
  const [reducedMotion, setReducedMotion] = useState<boolean>(() => isReducedMotionPreferred());
  const [pageHidden, setPageHidden] = useState<boolean>(() =>
    typeof document !== 'undefined' ? document.visibilityState === 'hidden' : false
  );

  useEffect(() => {
    if (typeof window === 'undefined' || typeof document === 'undefined') return;

    const mq = window.matchMedia('(prefers-reduced-motion: reduce)');
    const handleMotionChange = () => setReducedMotion(mq.matches);
    const handleVisibility = () => setPageHidden(document.visibilityState === 'hidden');

    mq.addEventListener('change', handleMotionChange);
    document.addEventListener('visibilitychange', handleVisibility);

    return () => {
      mq.removeEventListener('change', handleMotionChange);
      document.removeEventListener('visibilitychange', handleVisibility);
    };
  }, []);

  useEffect(() => {
    if (typeof document === 'undefined') return;
    const root = document.documentElement;

    if (reducedMotion) root.setAttribute('data-reduced-motion', 'true');
    else root.removeAttribute('data-reduced-motion');

    if (pageHidden) root.setAttribute('data-page-hidden', 'true');
    else root.removeAttribute('data-page-hidden');

    if (isOledMode) root.setAttribute('data-oled-eco', 'true');
    else root.removeAttribute('data-oled-eco');
  }, [reducedMotion, pageHidden, isOledMode]);

  return {
    reducedMotion,
    pageHidden,
    oledEcoPaused: isOledMode,
    ambientActive: !reducedMotion && !pageHidden && !isOledMode,
  };
}

/**
 * Smoothly animates a numeric value with requestAnimationFrame and easeOutExpo,
 * respecting prefers-reduced-motion.
 */
export function useAnimatedNumber(
  target: number,
  durationMs: number = 520,
  decimals: number = 1
): number {
  const [displayValue, setDisplayValue] = useState<number>(target);
  const currentRef = useRef<number>(target);

  useEffect(() => {
    if (isReducedMotionPreferred() || typeof window === 'undefined') {
      currentRef.current = target;
      setDisplayValue(target);
      return;
    }

    const startValue = currentRef.current;
    if (Math.abs(target - startValue) < 0.001) {
      setDisplayValue(target);
      return;
    }

    let rafId = 0;
    const startTime = performance.now();

    const tick = (now: number) => {
      const elapsed = now - startTime;
      const progress = Math.min(1, elapsed / Math.max(1, durationMs));
      const factor = Math.pow(10, decimals);
      const interpolated =
        Math.round(interpolateEaseOutExpo(startValue, target, progress) * factor) / factor;

      currentRef.current = interpolated;
      setDisplayValue(interpolated);

      if (progress < 1) {
        rafId = window.requestAnimationFrame(tick);
      } else {
        currentRef.current = target;
        setDisplayValue(target);
      }
    };

    rafId = window.requestAnimationFrame(tick);
    return () => window.cancelAnimationFrame(rafId);
  }, [target, durationMs, decimals]);

  return displayValue;
}
