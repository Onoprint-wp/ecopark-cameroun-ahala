// ============================================================================
// ECO-PARK SYNCHRONIZED ELEVATION PROFILE (src/components/map/ElevationProfile.tsx)
// Feature F17 — SVG Elevation Chart with Bidirectional Map Scrubber Synchronization
// ============================================================================

import React, { useState, useRef, useMemo } from 'react';
import { useEcoPark } from '../../context/EcoParkContext';
import { Trail } from '../../types/ecosystem';
import {
  Info,
  CheckCircle2,
  AlertTriangle,
  XCircle,
} from 'lucide-react';

export interface ScrubPayload {
  x: number;
  y: number;
  elevationM: number;
  distanceKm: number;
  slopePercent?: number;
  poiLabel?: string;
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
  const [hoverIndex, setHoverIndex] = useState<number | null>(null);
  const [hoverPoint, setHoverPoint] = useState<ScrubPayload | null>(null);

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
  const getX = (distKm: number) => padLeft + (distKm / maxDistance) * plotWidth;
  const getY = (altM: number) => padTop + (1 - (altM - minAlt) / altRange) * plotHeight;

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
      // Use smooth cubic bezier curve
      const prev = pts[i - 1];
      const curr = pts[i];
      const midX = (prev.px + curr.px) / 2;
      dLine += ` C ${midX.toFixed(1)},${prev.py.toFixed(1)} ${midX.toFixed(1)},${curr.py.toFixed(1)} ${curr.px.toFixed(1)},${curr.py.toFixed(1)}`;
    }

    // Area path closing to bottom baseline
    const baseY = (padTop + plotHeight).toFixed(1);
    const firstX = pts[0].px.toFixed(1);
    const lastX = pts[pts.length - 1].px.toFixed(1);
    const dArea = `${dLine} L ${lastX},${baseY} L ${firstX},${baseY} Z`;

    return { linePath: dLine, areaPath: dArea, scaledPoints: pts };
  }, [profile, maxDistance, minAlt, altRange, plotWidth, plotHeight]);

  // Pointer move handler for interactive scrubbing
  const handlePointerMove = (e: React.PointerEvent<SVGSVGElement>) => {
    if (!svgRef.current || scaledPoints.length === 0) return;

    const rect = svgRef.current.getBoundingClientRect();
    const mouseX = e.clientX - rect.left;
    const svgX = (mouseX / rect.width) * svgWidth;

    // Find closest profile point
    let closestIdx = 0;
    let minDiff = Infinity;

    scaledPoints.forEach((pt, idx) => {
      const diff = Math.abs(pt.px - svgX);
      if (diff < minDiff) {
        minDiff = diff;
        closestIdx = idx;
      }
    });

    const target = scaledPoints[closestIdx];
    setHoverIndex(closestIdx);

    const payload: ScrubPayload = {
      x: target.mapCoord.x,
      y: target.mapCoord.y,
      elevationM: target.elevationM,
      distanceKm: target.distanceKm,
      slopePercent: target.slopePercent,
      poiLabel: target.poiLabel,
    };

    setHoverPoint(payload);
    if (onScrub) {
      onScrub(payload);
    }
  };

  const handlePointerLeave = () => {
    setHoverIndex(null);
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
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-[var(--border-default)]/60">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <span className="text-xs font-mono font-semibold uppercase tracking-wider text-[var(--brand-primary)]">
              Profil Altimétrique & Relief
            </span>
            {statusBadge()}
          </div>
          <h3 className="font-['Fraunces'] text-lg sm:text-xl font-bold text-[var(--text-primary)]">
            {activeTrail.name}
          </h3>
          <p className="text-xs text-[var(--text-muted)] italic font-serif">
            {activeTrail.subtitle}
          </p>
        </div>

        {/* Trail Quick Metrics */}
        <div className="flex items-center gap-3 sm:gap-4 text-xs font-mono">
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
          <Info className="w-3 h-3 text-[var(--brand-primary)]" />
          <span>Survolez le relief pour synchroniser la carte</span>
        </div>

        {/* Floating Tooltip during Scrub */}
        {hoverPoint && (
          <div
            className="absolute z-20 pointer-events-none px-2.5 py-1.5 rounded-lg bg-[#1F2421] text-white text-[11px] font-mono shadow-xl border border-[#52B788] -translate-x-1/2 -translate-y-full mb-2"
            style={{
              left: `${(getX(hoverPoint.distanceKm) / svgWidth) * 100}%`,
              top: `${(getY(hoverPoint.elevationM) / svgHeight) * 100}%`,
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
            {/* Elevation Area Gradient */}
            <linearGradient id="elevationAreaGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#52B788" stopOpacity="0.45" />
              <stop offset="50%" stopColor="#52B788" stopOpacity="0.15" />
              <stop offset="100%" stopColor="#52B788" stopOpacity="0.02" />
            </linearGradient>

            {/* Pattern for grid lines */}
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

          {/* Area under the curve */}
          {areaPath && (
            <path
              d={areaPath}
              fill="url(#elevationAreaGradient)"
              className="transition-all duration-300"
            />
          )}

          {/* Main Elevation Curve Line */}
          {linePath && (
            <path
              d={linePath}
              fill="none"
              stroke="#52B788"
              strokeWidth="2.75"
              strokeLinecap="round"
              strokeLinejoin="round"
              filter="url(#glow-elevation)"
            />
          )}

          {/* Key POI Station Markers on the Curve */}
          {scaledPoints.map((pt, idx) => {
            if (!pt.poiLabel) return null;
            return (
              <g key={idx} className="transition-all duration-150">
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

          {/* Active Scrubber Guideline & Marker */}
          {hoverIndex !== null && scaledPoints[hoverIndex] && (
            <g>
              <line
                x1={scaledPoints[hoverIndex].px}
                y1={padTop}
                x2={scaledPoints[hoverIndex].px}
                y2={padTop + plotHeight}
                stroke="#E76F51"
                strokeWidth="1.5"
                strokeDasharray="3 3"
              />
              <circle
                cx={scaledPoints[hoverIndex].px}
                cy={scaledPoints[hoverIndex].py}
                r="6"
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
          Changer de profil :
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
                  ? 'bg-[var(--brand-primary)] text-white shadow-xs'
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
