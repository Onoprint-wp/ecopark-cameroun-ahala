// ============================================================================
// ECO-PARK SYNCHRONIZED ELEVATION PROFILE (src/components/map/ElevationProfile.tsx)
// Feature F17 — SVG Elevation Chart with Bidirectional Map Scrubber & Live Trace
// ============================================================================

import React, { useState, useRef, useMemo, useEffect, useCallback } from 'react';
import { useEcoPark } from '../../context/EcoParkContext';
import { Trail } from '../../types/ecosystem';
import { isReducedMotionPreferred } from '../../utils/ecoMotion';
import {
  Info,
  CheckCircle2,
  AlertTriangle,
  XCircle,
  Play,
  Square,
  Footprints,
} from 'lucide-react';

export interface ScrubPayload {
  x: number;
  y: number;
  elevationM: number;
  distanceKm: number;
  slopePercent?: number;
  poiLabel?: string;
  progressRatio?: number; // Continuous 0..1 ratio along the selected trail
}

export interface ElevationProfileProps {
  onScrub?: (payload: ScrubPayload | null) => void;
  className?: string;
}

export const ElevationProfile: React.FC<ElevationProfileProps> = ({
  onScrub,
  className = '',
}) => {
  const { trails, selectedTrailId, setSelectedTrailId } = useEcoPark();

  // Selected trail or default to first open trail
  const activeTrail: Trail = useMemo(() => {
    if (selectedTrailId) {
      const found = trails.find((t) => t.id === selectedTrailId);
      if (found) return found;
    }
    const firstOpen = trails.find((t) => t.status === 'fluide');
    return firstOpen || trails[0];
  }, [trails, selectedTrailId]);

  const svgRef = useRef<SVGSVGElement | null>(null);
  const [scrubCursor, setScrubCursor] = useState<{ px: number; py: number } | null>(null);
  const [hoverPoint, setHoverPoint] = useState<ScrubPayload | null>(null);
  const [isSimulatingWalk, setIsSimulatingWalk] = useState<boolean>(false);
  const [drawCycle, setDrawCycle] = useState<number>(0);

  const profile = activeTrail.elevationProfile || [];
  const maxDistance = activeTrail.lengthKm || profile[profile.length - 1]?.distanceKm || 6.4;

  const minAlt = Math.max(0, activeTrail.minElevationM - 20);
  const maxAlt = activeTrail.maxElevationM + 30;
  const altRange = Math.max(1, maxAlt - minAlt);

  // SVG dimensions
  const svgWidth = 640;
  const svgHeight = 180;
  const padLeft = 48;
  const padRight = 24;
  const padTop = 20;
  const padBottom = 34;

  const plotWidth = svgWidth - padLeft - padRight;
  const plotHeight = svgHeight - padTop - padBottom;

  // Coordinate scales
  const getX = useCallback(
    (distKm: number) => padLeft + (distKm / Math.max(0.1, maxDistance)) * plotWidth,
    [maxDistance, plotWidth]
  );
  const getY = useCallback(
    (altM: number) => padTop + (1 - (altM - minAlt) / altRange) * plotHeight,
    [minAlt, altRange, plotHeight]
  );

  // Reset scrub & replay synchronized self-drawing when active trail changes
  useEffect(() => {
    setIsSimulatingWalk(false);
    setScrubCursor(null);
    setHoverPoint(null);
    setDrawCycle((c) => c + 1);
    if (onScrub) onScrub(null);
  }, [activeTrail.id, onScrub]);

  // Build SVG path string for the elevation line and area fill
  const { linePath, areaPath, scaledPoints } = useMemo(() => {
    if (profile.length === 0) {
      return { linePath: '', areaPath: '', scaledPoints: [] };
    }

    const pts = profile.map((pt) => ({
      ...pt,
      px: getX(pt.distanceKm),
      py: getY(pt.elevationM),
    }));

    // Line path
    let dLine = `M ${pts[0].px.toFixed(1)},${pts[0].py.toFixed(1)}`;
    for (let i = 1; i < pts.length; i++) {
      const prev = pts[i - 1];
      const curr = pts[i];
      const midX = (prev.px + curr.px) / 2;
      dLine += ` C ${midX.toFixed(1)},${prev.py.toFixed(1)} ${midX.toFixed(1)},${curr.py.toFixed(1)} ${curr.px.toFixed(1)},${curr.py.toFixed(1)}`;
    }

    const baseY = (padTop + plotHeight).toFixed(1);
    const firstX = pts[0].px.toFixed(1);
    const lastX = pts[pts.length - 1].px.toFixed(1);
    const dArea = `${dLine} L ${lastX},${baseY} L ${firstX},${baseY} Z`;

    return { linePath: dLine, areaPath: dArea, scaledPoints: pts };
  }, [profile, getX, getY, plotHeight]);

  // Continuous interpolation along profile for 60fps scrubber & auto-walk sync
  const updateAtProgressRatio = useCallback(
    (ratio: number) => {
      if (scaledPoints.length === 0) return;
      const clampedRatio = Math.max(0, Math.min(1, ratio));
      const targetDist = clampedRatio * maxDistance;

      // Locate surrounding segment in scaledPoints
      let segIdx = 0;
      for (let i = 0; i < scaledPoints.length - 1; i++) {
        if (targetDist >= scaledPoints[i].distanceKm) {
          segIdx = i;
        }
      }

      const p0 = scaledPoints[segIdx];
      const p1 = scaledPoints[Math.min(scaledPoints.length - 1, segIdx + 1)];
      const segSpan = Math.max(0.0001, p1.distanceKm - p0.distanceKm);
      const localT = p0 === p1 ? 0 : Math.max(0, Math.min(1, (targetDist - p0.distanceKm) / segSpan));

      const interpElev = Math.round(p0.elevationM + (p1.elevationM - p0.elevationM) * localT);
      const interpMapX = p0.mapCoord.x + (p1.mapCoord.x - p0.mapCoord.x) * localT;
      const interpMapY = p0.mapCoord.y + (p1.mapCoord.y - p0.mapCoord.y) * localT;
      const interpPx = getX(targetDist);
      const interpPy = getY(interpElev);

      // Snap POI label if close to a landmark
      let nearPoi: string | undefined;
      let nearSlope: number | undefined = p0.slopePercent;
      for (const sp of scaledPoints) {
        if (Math.abs(sp.distanceKm - targetDist) <= maxDistance * 0.055) {
          if (sp.poiLabel) nearPoi = sp.poiLabel;
          if (sp.slopePercent !== undefined) nearSlope = sp.slopePercent;
        }
      }

      const payload: ScrubPayload = {
        x: interpMapX,
        y: interpMapY,
        elevationM: interpElev,
        distanceKm: Number(targetDist.toFixed(2)),
        slopePercent: nearSlope,
        poiLabel: nearPoi,
        progressRatio: clampedRatio,
      };

      setScrubCursor({ px: interpPx, py: interpPy });
      setHoverPoint(payload);
      if (onScrub) {
        onScrub(payload);
      }
    },
    [scaledPoints, maxDistance, getX, getY, onScrub]
  );

  // Virtual Hiker Auto-Walk Loop (« Tracé vivant »)
  useEffect(() => {
    if (!isSimulatingWalk || typeof window === 'undefined') return;

    // Ensure map knows which trail is being walked
    if (selectedTrailId !== activeTrail.id) {
      setSelectedTrailId(activeTrail.id);
    }

    const durationMs = isReducedMotionPreferred() ? 2200 : 6800;
    const startTime = performance.now();
    let rafId = 0;

    const step = (now: number) => {
      if (document.visibilityState === 'hidden') {
        setIsSimulatingWalk(false);
        return;
      }
      const elapsed = now - startTime;
      const ratio = Math.min(1, elapsed / durationMs);
      updateAtProgressRatio(ratio);

      if (ratio < 1) {
        rafId = window.requestAnimationFrame(step);
      } else {
        setIsSimulatingWalk(false);
      }
    };

    rafId = window.requestAnimationFrame(step);
    return () => window.cancelAnimationFrame(rafId);
  }, [isSimulatingWalk, activeTrail.id, selectedTrailId, setSelectedTrailId, updateAtProgressRatio]);

  // Pointer move handler for interactive continuous scrubbing
  const handlePointerMove = (e: React.PointerEvent<SVGSVGElement>) => {
    if (!svgRef.current || scaledPoints.length === 0) return;
    if (isSimulatingWalk) setIsSimulatingWalk(false);

    const rect = svgRef.current.getBoundingClientRect();
    const mouseX = e.clientX - rect.left;
    const svgX = (mouseX / rect.width) * svgWidth;
    const ratio = (svgX - padLeft) / Math.max(1, plotWidth);

    // Ensure selectedTrailId is synced so map highlights this trail
    if (selectedTrailId !== activeTrail.id) {
      setSelectedTrailId(activeTrail.id);
    }

    updateAtProgressRatio(ratio);
  };

  const handlePointerLeave = () => {
    if (isSimulatingWalk) return;
    setScrubCursor(null);
    setHoverPoint(null);
    if (onScrub) {
      onScrub(null);
    }
  };

  // Status helper badge
  const statusBadge = () => {
    switch (activeTrail.status) {
      case 'fluide':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300 border border-emerald-300 dark:border-emerald-800">
            <CheckCircle2 className="w-3 h-3 text-emerald-600 dark:text-emerald-400" />
            Ouvert / Fluide
          </span>
        );
      case 'balise':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300 border border-amber-300 dark:border-amber-800">
            <AlertTriangle className="w-3 h-3 text-amber-600 dark:text-amber-400" />
            Balisé / Prudence
          </span>
        );
      case 'ferme':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-red-100 text-red-800 dark:bg-red-950 dark:text-red-300 border border-red-300 dark:border-red-800">
            <XCircle className="w-3 h-3 text-red-600 dark:text-red-400" />
            Fermé (Nidification)
          </span>
        );
    }
  };

  return (
    <div
      className={`p-5 sm:p-6 rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-default)] shadow-xs space-y-4 ${className}`}
    >
      {/* Top Header & Trail Stats */}
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-3 pb-3 border-b border-[var(--border-default)]/60">
        <div className="space-y-1">
          <div className="flex flex-wrap items-center gap-2">
            <span className="text-xs font-mono font-semibold uppercase tracking-wider text-[var(--brand-primary)]">
              Profil Altimétrique &amp; Tracé Vivant
            </span>
            {statusBadge()}
            <button
              type="button"
              onClick={() => {
                if (isSimulatingWalk) {
                  setIsSimulatingWalk(false);
                  setScrubCursor(null);
                  setHoverPoint(null);
                  if (onScrub) onScrub(null);
                } else {
                  setSelectedTrailId(activeTrail.id);
                  setIsSimulatingWalk(true);
                }
              }}
              className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[11px] font-mono font-bold transition-all cursor-pointer border ${
                isSimulatingWalk
                  ? 'bg-[#E76F51] text-white border-[#E76F51] shadow-xs'
                  : 'bg-[var(--bg-elevated)] text-[var(--brand-primary)] border-[var(--border-default)] hover:border-[var(--brand-primary)]'
              }`}
              title="Animer un randonneur le long du tracé topographique et du profil altimétrique"
            >
              {isSimulatingWalk ? (
                <>
                  <Square className="w-3 h-3 fill-current" />
                  <span>Stop randonneur</span>
                </>
              ) : (
                <>
                  <Play className="w-3 h-3 fill-current" />
                  <span>Simuler parcours</span>
                </>
              )}
            </button>
          </div>
          <h3 className="font-['Barlow_Semi_Condensed'] text-lg sm:text-xl font-bold text-[var(--text-primary)]">
            {activeTrail.name}
          </h3>
          <p className="text-xs text-[var(--text-muted)] italic font-serif">
            {activeTrail.subtitle}
          </p>
        </div>

        {/* Trail Quick Metrics */}
        <div className="flex flex-wrap items-center gap-2.5 sm:gap-3.5 text-xs font-mono">
          <div className="p-2 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)] text-center min-w-[70px]">
            <div className="text-[10px] text-[var(--text-muted)] font-sans">Distance</div>
            <div className="font-bold text-[var(--text-primary)]">{activeTrail.lengthKm} km</div>
          </div>
          <div className="p-2 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)] text-center min-w-[70px]">
            <div className="text-[10px] text-[var(--text-muted)] font-sans">D+ Gain</div>
            <div className="font-bold text-[var(--brand-primary)]">+{activeTrail.elevationGainM}m</div>
          </div>
          <div className="p-2 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)] text-center min-w-[70px]">
            <div className="text-[10px] text-[var(--text-muted)] font-sans">Alt. Max</div>
            <div className="font-bold text-[var(--text-primary)]">{activeTrail.maxElevationM}m</div>
          </div>
          <div className="p-2 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)] text-center min-w-[70px]">
            <div className="text-[10px] text-[var(--text-muted)] font-sans">Durée</div>
            <div className="font-bold text-[var(--text-primary)]">
              {Math.floor(activeTrail.durationMin / 60)}h{activeTrail.durationMin % 60 > 0 ? `${activeTrail.durationMin % 60}` : '00'}
            </div>
          </div>
        </div>
      </div>

      {/* SVG Elevation Chart Container */}
      <div className="relative w-full rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)] overflow-hidden p-2 sm:p-3 select-none">
        {/* Scrubber instructions badge */}
        <div className="absolute top-3 right-3 z-10 hidden sm:flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-[var(--bg-surface)]/90 backdrop-blur-xs border border-[var(--border-default)] text-[10px] font-mono text-[var(--text-muted)]">
          {isSimulatingWalk ? (
            <>
              <Footprints className="w-3 h-3 text-[#E76F51] animate-pulse" />
              <span className="text-[var(--text-primary)] font-semibold">Parcours en direct sur la carte…</span>
            </>
          ) : (
            <>
              <Info className="w-3 h-3 text-[var(--brand-primary)]" />
              <span>Survolez le relief pour guider le randonneur sur la carte</span>
            </>
          )}
        </div>

        {/* Floating Tooltip during Scrub or Simulation */}
        {hoverPoint && scrubCursor && (
          <div
            className="absolute z-20 pointer-events-none px-2.5 py-1.5 rounded-lg bg-[#1F2421] text-white text-[11px] font-mono shadow-xl border border-[#52B788] -translate-x-1/2 -translate-y-full mb-2 transition-transform duration-75"
            style={{
              left: `${Math.min(88, Math.max(12, (scrubCursor.px / svgWidth) * 100))}%`,
              top: `${Math.max(24, (scrubCursor.py / svgHeight) * 100)}%`,
            }}
          >
            <div className="font-bold text-[#52B788]">
              {hoverPoint.poiLabel ? hoverPoint.poiLabel : `Km ${hoverPoint.distanceKm.toFixed(1)}`}
            </div>
            <div className="text-[#C9D1CC] text-[10px]">
              Alt: <strong>{hoverPoint.elevationM} m</strong>
              {hoverPoint.slopePercent !== undefined && ` · Pente: ${hoverPoint.slopePercent}%`}
            </div>
          </div>
        )}

        <svg
          ref={svgRef}
          viewBox={`0 0 ${svgWidth} ${svgHeight}`}
          className="w-full h-auto cursor-crosshair touch-none"
          onPointerMove={handlePointerMove}
          onPointerLeave={handlePointerLeave}
          aria-label={`Profil altimétrique pour ${activeTrail.name}`}
        >
          <defs>
            <linearGradient id="elevationAreaGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#52B788" stopOpacity="0.45" />
              <stop offset="50%" stopColor="#52B788" stopOpacity="0.15" />
              <stop offset="100%" stopColor="#52B788" stopOpacity="0.02" />
            </linearGradient>

            <filter id="glow-elevation" x="-20%" y="-20%" width="140%" height="140%">
              <feDropShadow dx="0" dy="0" stdDeviation="3" floodColor="#52B788" floodOpacity="0.6" />
            </filter>
          </defs>

          {/* Horizontal Altitude Grid Lines */}
          {[minAlt, Math.round((minAlt + maxAlt) / 2), maxAlt].map((alt) => {
            const y = getY(alt);
            return (
              <g key={alt}>
                <line
                  x1={padLeft}
                  y1={y}
                  x2={svgWidth - padRight}
                  y2={y}
                  stroke="currentColor"
                  strokeOpacity="0.12"
                  strokeDasharray="4 4"
                />
                <text
                  x={padLeft - 8}
                  y={y + 3}
                  textAnchor="end"
                  fill="currentColor"
                  fillOpacity="0.55"
                  className="font-mono text-[10px]"
                >
                  {alt}m
                </text>
              </g>
            );
          })}

          {/* Vertical Distance Markers */}
          {[0, maxDistance * 0.25, maxDistance * 0.5, maxDistance * 0.75, maxDistance].map(
            (dist, idx) => {
              const x = getX(dist);
              return (
                <g key={idx}>
                  <line
                    x1={x}
                    y1={padTop}
                    x2={x}
                    y2={padTop + plotHeight}
                    stroke="currentColor"
                    strokeOpacity="0.08"
                  />
                  <text
                    x={x}
                    y={padTop + plotHeight + 16}
                    textAnchor="middle"
                    fill="currentColor"
                    fillOpacity="0.55"
                    className="font-mono text-[10px]"
                  >
                    {dist.toFixed(1)} km
                  </text>
                </g>
              );
            }
          )}

          {/* Synchronized Progressive Area Fill */}
          {areaPath && (
            <path
              key={`area-${activeTrail.id}-${drawCycle}`}
              d={areaPath}
              fill="url(#elevationAreaGradient)"
              className="eco-elevation-area-reveal"
            />
          )}

          {/* Synchronized Self-Drawing Elevation Curve Line */}
          {linePath && (
            <path
              key={`line-${activeTrail.id}-${drawCycle}`}
              d={linePath}
              pathLength={1000}
              fill="none"
              stroke="#52B788"
              strokeWidth="2.75"
              strokeLinecap="round"
              strokeLinejoin="round"
              filter="url(#glow-elevation)"
              className="eco-trail-self-draw"
            />
          )}

          {/* Key POI Station Markers Popping Along the Curve */}
          {scaledPoints.map((pt, idx) => {
            if (!pt.poiLabel) return null;
            const delayMs = Math.round((pt.distanceKm / Math.max(0.1, maxDistance)) * 680);
            return (
              <g
                key={`${activeTrail.id}-poi-${idx}-${drawCycle}`}
                className="eco-poi-pop"
                style={{ '--poi-delay': `${delayMs}ms` } as React.CSSProperties}
              >
                <line
                  x1={pt.px}
                  y1={pt.py}
                  x2={pt.px}
                  y2={padTop + plotHeight}
                  stroke="#52B788"
                  strokeOpacity="0.25"
                  strokeDasharray="2 2"
                />
                <circle
                  cx={pt.px}
                  cy={pt.py}
                  r="4"
                  fill="#1F2421"
                  stroke="#52B788"
                  strokeWidth="2"
                />
                <text
                  x={pt.px}
                  y={pt.py - 9}
                  textAnchor="middle"
                  fill="currentColor"
                  fillOpacity="0.85"
                  className="font-mono text-[9px] font-semibold"
                >
                  {pt.poiLabel}
                </text>
              </g>
            );
          })}

          {/* Active Continuous Scrubber Guideline & Marker */}
          {scrubCursor && (
            <g>
              <line
                x1={scrubCursor.px}
                y1={padTop}
                x2={scrubCursor.px}
                y2={padTop + plotHeight}
                stroke="#E76F51"
                strokeWidth="1.5"
                strokeDasharray="3 3"
              />
              <circle
                cx={scrubCursor.px}
                cy={scrubCursor.py}
                r="6.5"
                fill="#E76F51"
                stroke="#FFFFFF"
                strokeWidth="2"
              />
            </g>
          )}
        </svg>
      </div>

      {/* Trail Switcher Quick Buttons */}
      <div className="pt-2 flex flex-wrap items-center gap-2">
        <span className="text-xs font-mono text-[var(--text-muted)] mr-1">
          Changer de tracé vivant :
        </span>
        {trails.map((trail) => {
          const isCurrent = trail.id === activeTrail.id;
          return (
            <button
              key={trail.id}
              type="button"
              onClick={() => setSelectedTrailId(trail.id)}
              className={`px-3 py-1.5 rounded-xl text-xs font-semibold font-mono transition-all cursor-pointer ${
                isCurrent
                  ? 'bg-[var(--brand-primary)] text-white shadow-xs scale-[1.02]'
                  : 'bg-[var(--bg-elevated)] hover:bg-[var(--bg-surface)] text-[var(--text-primary)] border border-[var(--border-default)]'
              }`}
            >
              {trail.name.split('&')[0].trim()} (+{trail.elevationGainM}m)
            </button>
          );
        })}
      </div>
    </div>
  );
};
