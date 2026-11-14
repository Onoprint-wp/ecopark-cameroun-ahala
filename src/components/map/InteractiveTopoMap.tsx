// ============================================================================
// ECO-PARK INTERACTIVE TOPOGRAPHIC VECTOR MAP (src/components/map/InteractiveTopoMap.tsx)
// Feature F16 - 1000x700 Pure SVG Topo Engine with 7 Layers & Real-Time Sync
// ============================================================================

import React, { useState, useId, useRef, useEffect, useMemo } from 'react';
import { useEcoPark } from '../../context/EcoParkContext';
import { PointOfInterest, TrailStatus } from '../../types/ecosystem';
import { ScrubPayload } from './ElevationProfile';
import {
  consumeRecentTrailWave,
  TRAIL_WAVE_EVENT_NAME,
  TrailWavePayload,
} from '../../utils/ecoMotion';
import {
  Layers,
  ZoomIn,
  ZoomOut,
  RotateCcw,
  Eye,
  EyeOff,
  Navigation,
  MapPin,
  X,
  Droplet,
  Mountain,
  ShieldCheck,
  Bike,
  Binoculars,
} from 'lucide-react';

export interface InteractiveTopoMapProps {
  scrubPoint?: ScrubPayload | null;
  onSelectTrail?: (trailId: string) => void;
  className?: string;
}

export const InteractiveTopoMap: React.FC<InteractiveTopoMapProps> = ({
  scrubPoint,
  onSelectTrail,
  className = '',
}) => {
  const { trails, selectedTrailId, setSelectedTrailId, pois } = useEcoPark();
  const idPrefix = useId();

  // Layer visibility state
  const [showContours, setShowContours] = useState<boolean>(true);
  const [showHydroBiomes, setShowHydroBiomes] = useState<boolean>(true);
  const [showPois, setShowPois] = useState<boolean>(true);
  const [showTrails, setShowTrails] = useState<boolean>(true);

  // Zoom & Pan state
  const [zoomLevel, setZoomLevel] = useState<number>(1);
  const [panOffset, setPanOffset] = useState<{ x: number; y: number }>({ x: 0, y: 0 });

  // Selected POI for popover display
  const [activePoi, setActivePoi] = useState<PointOfInterest | null>(null);

  // Hovered trail id for subtle pre-selection highlight
  const [hoveredTrailId, setHoveredTrailId] = useState<string | null>(null);

  // Synchronized self-drawing epoch & SVG path measurement refs (« Tracé vivant »)
  const [drawEpoch, setDrawEpoch] = useState<number>(0);
  const trailPathRefs = useRef<Record<string, SVGPathElement | null>>({});

  // Cross-view status shockwave emitted from Console Éco-Garde
  const [statusWave, setStatusWave] = useState<TrailWavePayload | null>(null);

  const effectiveSelectedId = useMemo(() => {
    if (selectedTrailId && trails.some((t) => t.id === selectedTrailId)) {
      return selectedTrailId;
    }
    const firstOpen = trails.find((t) => t.status === 'fluide');
    return (firstOpen || trails[0])?.id || null;
  }, [selectedTrailId, trails]);

  useEffect(() => {
    setDrawEpoch((e) => e + 1);
  }, [effectiveSelectedId]);

  useEffect(() => {
    const recent = consumeRecentTrailWave(45000);
    if (recent) {
      setStatusWave(recent);
      setSelectedTrailId(recent.trailId);
      const timer = window.setTimeout(() => setStatusWave(null), 2600);
      return () => window.clearTimeout(timer);
    }
  }, [setSelectedTrailId]);

  useEffect(() => {
    const handleWaveEvent = (ev: Event) => {
      const custom = ev as CustomEvent<TrailWavePayload>;
      if (!custom.detail) return;
      setStatusWave(custom.detail);
      const timer = window.setTimeout(() => {
        setStatusWave((curr) =>
          curr && curr.timestamp === custom.detail.timestamp ? null : curr
        );
      }, 2400);
      return () => window.clearTimeout(timer);
    };

    window.addEventListener(TRAIL_WAVE_EVENT_NAME, handleWaveEvent);
    return () => window.removeEventListener(TRAIL_WAVE_EVENT_NAME, handleWaveEvent);
  }, []);

  // Compute exact SVG Bézier coordinates & tangent heading via getPointAtLength
  const exactHikerBeacon = useMemo(() => {
    if (!scrubPoint) return null;
    const pathEl = effectiveSelectedId ? trailPathRefs.current[effectiveSelectedId] : null;
    if (
      pathEl &&
      scrubPoint.progressRatio !== undefined &&
      typeof pathEl.getTotalLength === 'function'
    ) {
      try {
        const totalLen = pathEl.getTotalLength();
        if (totalLen > 0) {
          const targetLen = Math.max(0, Math.min(totalLen, scrubPoint.progressRatio * totalLen));
          const pt = pathEl.getPointAtLength(targetLen);
          const behind = pathEl.getPointAtLength(Math.max(0, targetLen - 4));
          const ahead = pathEl.getPointAtLength(Math.min(totalLen, targetLen + 4));
          const angleDeg = (Math.atan2(ahead.y - behind.y, ahead.x - behind.x) * 180) / Math.PI;
          return { x: pt.x, y: pt.y, angleDeg };
        }
      } catch {
        // Fallback to interpolated profile coordinates
      }
    }
    return { x: scrubPoint.x, y: scrubPoint.y, angleDeg: 0 };
  }, [scrubPoint, effectiveSelectedId]);

  // Handle zoom controls
  const handleZoomIn = () => setZoomLevel((z) => Math.min(2.5, +(z + 0.25).toFixed(2)));
  const handleZoomOut = () => setZoomLevel((z) => Math.max(0.75, +(z - 0.25).toFixed(2)));
  const handleResetView = () => {
    setZoomLevel(1);
    setPanOffset({ x: 0, y: 0 });
  };

  // Compute dynamic viewBox according to zoom and pan
  const baseWidth = 1000;
  const baseHeight = 700;
  const currentWidth = baseWidth / zoomLevel;
  const currentHeight = baseHeight / zoomLevel;
  const currentMinX = (baseWidth - currentWidth) / 2 + panOffset.x;
  const currentMinY = (baseHeight - currentHeight) / 2 + panOffset.y;
  const currentViewBox = `${currentMinX} ${currentMinY} ${currentWidth} ${currentHeight}`;

  // Helper for Trail Stroke Colors
  const getTrailStroke = (status: TrailStatus) => {
    switch (status) {
      case 'ferme':
        return '#DC2626'; // Red protection
      case 'balise':
        return '#E76F51'; // Terracotta warning
      case 'fluide':
      default:
        return '#52B788'; // Leaf green open
    }
  };

  // Helper for Trail Stroke Dash (Daltonism accessibility)
  const getTrailDashArray = (status: TrailStatus) => {
    switch (status) {
      case 'ferme':
        return '6 6'; // Dashed
      case 'balise':
        return '10 4 2 4'; // Dash-dot
      case 'fluide':
      default:
        return 'none'; // Solid
    }
  };

  // POI Category Icon Renderer
  const renderPoiIcon = (category: string) => {
    switch (category) {
      case 'park_entrance':
        return <Navigation className="w-3.5 h-3.5" />;
      case 'solar_bike':
        return <Bike className="w-3.5 h-3.5" />;
      case 'viewpoint':
        return <Mountain className="w-3.5 h-3.5" />;
      case 'bird_blind':
        return <Binoculars className="w-3.5 h-3.5" />;
      case 'water':
        return <Droplet className="w-3.5 h-3.5" />;
      case 'ranger_post':
        return <ShieldCheck className="w-3.5 h-3.5" />;
      default:
        return <MapPin className="w-3.5 h-3.5" />;
    }
  };

  const handleTrailClick = (trailId: string) => {
    if (effectiveSelectedId === trailId) {
      setDrawEpoch((e) => e + 1);
    }
    setSelectedTrailId(trailId);
    if (onSelectTrail) {
      onSelectTrail(trailId);
    }
  };

  return (
    <div
      className={`relative w-full rounded-2xl bg-[#121614] border border-[#2D6A4F] shadow-xl overflow-hidden select-none ${className}`}
    >
      {/* Top Map Toolbar: Layers, Zoom & Mode Status */}
      <div className="absolute top-3 left-3 right-3 z-20 flex flex-wrap items-center justify-between gap-2.5 pointer-events-none">
        {/* Layer Visibility Toggles */}
        <div className="flex items-center gap-1.5 p-1.5 rounded-xl bg-[#1F2421]/90 backdrop-blur-md border border-[#36403A] text-xs font-mono pointer-events-auto shadow-md">
          <span className="px-2 text-[10px] text-[#8EBAA0] flex items-center gap-1 font-semibold uppercase">
            <Layers className="w-3 h-3 text-[#52B788]" />
            Calques
          </span>

          <button
            type="button"
            onClick={() => setShowContours((v) => !v)}
            className={`px-2 py-1 rounded-lg text-[11px] transition-colors cursor-pointer flex items-center gap-1 ${
              showContours
                ? 'bg-[#29302C] text-[#52B788] font-bold border border-[#52B788]/40'
                : 'text-[#8EBAA0] hover:text-white'
            }`}
            title="Activer/désactiver les courbes de niveau isohypses"
          >
            {showContours ? <Eye className="w-3 h-3" /> : <EyeOff className="w-3 h-3 opacity-60" />}
            <span>Courbes</span>
          </button>

          <button
            type="button"
            onClick={() => setShowHydroBiomes((v) => !v)}
            className={`px-2 py-1 rounded-lg text-[11px] transition-colors cursor-pointer flex items-center gap-1 ${
              showHydroBiomes
                ? 'bg-[#29302C] text-[#52B788] font-bold border border-[#52B788]/40'
                : 'text-[#8EBAA0] hover:text-white'
            }`}
            title="Activer/désactiver l hydrographie et biomes"
          >
            {showHydroBiomes ? <Eye className="w-3 h-3" /> : <EyeOff className="w-3 h-3 opacity-60" />}
            <span>Biomes & Eau</span>
          </button>

          <button
            type="button"
            onClick={() => setShowTrails((v) => !v)}
            className={`px-2 py-1 rounded-lg text-[11px] transition-colors cursor-pointer flex items-center gap-1 ${
              showTrails
                ? 'bg-[#29302C] text-[#52B788] font-bold border border-[#52B788]/40'
                : 'text-[#8EBAA0] hover:text-white'
            }`}
            title="Activer/désactiver le tracé des 6 sentiers"
          >
            {showTrails ? <Eye className="w-3 h-3" /> : <EyeOff className="w-3 h-3 opacity-60" />}
            <span>Sentiers</span>
          </button>

          <button
            type="button"
            onClick={() => setShowPois((v) => !v)}
            className={`px-2 py-1 rounded-lg text-[11px] transition-colors cursor-pointer flex items-center gap-1 ${
              showPois
                ? 'bg-[#29302C] text-[#52B788] font-bold border border-[#52B788]/40'
                : 'text-[#8EBAA0] hover:text-white'
            }`}
            title="Activer/désactiver les 10 points d intérêt"
          >
            {showPois ? <Eye className="w-3 h-3" /> : <EyeOff className="w-3 h-3 opacity-60" />}
            <span>POIs</span>
          </button>
        </div>

        {/* Zoom & View Controls */}
        <div className="flex items-center gap-1 p-1 rounded-xl bg-[#1F2421]/90 backdrop-blur-md border border-[#36403A] pointer-events-auto shadow-md">
          <button
            type="button"
            onClick={handleZoomIn}
            disabled={zoomLevel >= 2.5}
            className="p-1.5 rounded-lg text-[#C9D1CC] hover:text-white hover:bg-[#29302C] disabled:opacity-40 transition-colors cursor-pointer"
            title="Zoom avant"
            aria-label="Zoom avant"
          >
            <ZoomIn className="w-3.5 h-3.5" />
          </button>

          <span className="px-1.5 text-[10px] font-mono font-bold text-[#52B788]">
            {Math.round(zoomLevel * 100)}%
          </span>

          <button
            type="button"
            onClick={handleZoomOut}
            disabled={zoomLevel <= 0.75}
            className="p-1.5 rounded-lg text-[#C9D1CC] hover:text-white hover:bg-[#29302C] disabled:opacity-40 transition-colors cursor-pointer"
            title="Zoom arrière"
            aria-label="Zoom arrière"
          >
            <ZoomOut className="w-3.5 h-3.5" />
          </button>

          <button
            type="button"
            onClick={handleResetView}
            className="p-1.5 rounded-lg text-[#8EBAA0] hover:text-white hover:bg-[#29302C] transition-colors cursor-pointer ml-1 border-l border-[#36403A]"
            title="Réinitialiser l affichage"
            aria-label="Réinitialiser"
          >
            <RotateCcw className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>

      {/* Main SVG Map Canvas */}
      <div className="relative w-full aspect-[10/7] min-h-[460px] sm:min-h-[580px] overflow-hidden">
        <svg
          viewBox={currentViewBox}
          className="w-full h-full object-contain cursor-grab active:cursor-grabbing transition-transform duration-200"
          role="img"
          aria-label="Carte topographique vectorielle de la réserve naturelle ECO-PARK"
        >
          <defs>
            {/* Hypsometric Altitude Gradients */}
            <linearGradient id={`${idPrefix}-hypsometry`} x1="0" y1="1" x2="1" y2="0">
              <stop offset="0%" stopColor="#151C18" />
              <stop offset="40%" stopColor="#1B4332" />
              <stop offset="70%" stopColor="#2D6A4F" />
              <stop offset="100%" stopColor="#357A5B" />
            </linearGradient>

            {/* Trail active glow filter */}
            <filter id={`${idPrefix}-glow`} x="-20%" y="-20%" width="140%" height="140%">
              <feDropShadow dx="0" dy="0" stdDeviation="4" floodColor="#74C69D" floodOpacity="0.8" />
            </filter>

            {/* Wetland subtle water pattern */}
            <pattern id={`${idPrefix}-waterPattern`} width="20" height="20" patternUnits="userSpaceOnUse">
              <path d="M 0,10 Q 5,7 10,10 T 20,10" fill="none" stroke="#52B788" strokeWidth="0.75" opacity="0.3" />
            </pattern>

            {/* Progressive Self-Drawing Masks for Dashed / Closed Trails (Daltonism-safe) */}
            {trails.map((trail) => (
              <mask key={`mask-def-${trail.id}-${drawEpoch}`} id={`${idPrefix}-draw-mask-${trail.id}`}>
                <path
                  d={trail.mapPath}
                  pathLength={1000}
                  fill="none"
                  stroke="#FFFFFF"
                  strokeWidth={24}
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  className={effectiveSelectedId === trail.id ? 'eco-trail-self-draw' : ''}
                />
              </mask>
            ))}
          </defs>

          {/* =============================================================== */}
          {/* LAYER 1: Hypsometry & Relief Shading                            */}
          {/* =============================================================== */}
          <g id="layer-relief-hypsometry">
            {/* Base sanctuary canvas */}
            <rect x="0" y="0" width="1000" height="700" fill={`url(#${idPrefix}-hypsometry)`} />

            {/* Elevated relief zones */}
            {/* Low elevation plateau (120-160m) */}
            <path
              d="M 40,700 C 120,620 280,600 450,620 C 620,640 780,630 960,700 Z"
              fill="#18231D"
              opacity="0.6"
            />
            {/* Middle elevation forest (200-280m) */}
            <path
              d="M 100,450 C 260,390 420,350 580,380 C 740,410 860,360 940,430 L 980,560 C 820,520 640,540 480,520 C 320,500 180,520 80,580 Z"
              fill="#223329"
              opacity="0.5"
            />
            {/* Upper ridge & crags (300-420m) */}
            <path
              d="M 380,240 C 480,180 620,120 760,110 C 860,100 910,130 930,190 C 850,220 740,240 640,280 C 520,320 440,300 380,240 Z"
              fill="#293D32"
              opacity="0.7"
            />
            {/* High peak summit of Grand Cèdre (420m) */}
            <ellipse cx="790" cy="95" rx="50" ry="25" fill="#354E3F" opacity="0.8" />
          </g>

          {/* =============================================================== */}
          {/* LAYER 2: Isohypses (Contour lines 25m secondary & 100m master)  */}
          {/* =============================================================== */}
          {showContours && (
            <g id="layer-contours" className="transition-opacity duration-300">
              {/* Secondary 25m lines (Dashed thin) */}
              <g stroke="#52B788" strokeWidth="0.75" strokeDasharray="3 3" opacity="0.25" fill="none">
                {/* 135m */}
                <path d="M 55,610 C 180,570 320,550 480,575 C 640,600 780,580 945,620" />
                {/* 175m */}
                <path d="M 80,480 C 220,440 370,400 520,430 C 680,460 820,430 935,480" />
                {/* 225m */}
                <path d="M 140,360 C 270,320 420,280 570,305 C 720,330 840,300 925,350" />
                {/* 275m */}
                <path d="M 240,260 C 360,210 500,175 650,190 C 770,205 860,185 920,235" />
                {/* 325m */}
                <path d="M 370,175 C 490,130 610,110 740,110 C 820,115 870,120 915,155" />
                {/* 375m */}
                <path d="M 600,120 C 690,95 780,90 850,105 C 830,125 750,130 680,125" />
              </g>

              {/* Master 100m lines (Continuous with altitude values) */}
              <g stroke="#74C69D" strokeWidth="1.5" opacity="0.45" fill="none">
                {/* 120m */}
                <path d="M 50,680 C 150,650 300,640 450,660 C 600,680 750,670 950,690" />
                {/* 150m */}
                <path d="M 60,540 C 200,500 350,480 500,510 C 680,540 820,520 940,560" />
                {/* 200m */}
                <path d="M 100,420 C 250,380 400,340 550,370 C 700,400 850,370 930,420" />
                {/* 250m */}
                <path d="M 180,310 C 300,260 450,220 600,240 C 750,270 850,230 920,290" />
                {/* 300m */}
                <path d="M 300,210 C 420,160 550,130 700,140 C 800,160 880,140 920,180" />
                {/* 350m */}
                <path d="M 450,140 C 560,100 680,85 780,85 C 840,90 880,105 910,130" />
                {/* 400m summit */}
                <path d="M 720,100 C 760,85 810,85 840,100 C 820,115 770,115 720,100 Z" />
              </g>

              {/* Altitude Numeric Labels (WCAG high contrast) */}
              <g fill="#B7E4C7" className="font-mono text-[10px] font-bold" opacity="0.75">
                <text x="110" y="665">120m</text>
                <text x="90" y="525">150m</text>
                <text x="130" y="405">200m</text>
                <text x="210" y="295">250m</text>
                <text x="330" y="195">300m</text>
                <text x="470" y="125">350m</text>
                <text x="760" y="80">400m</text>
              </g>
            </g>
          )}

          {/* =============================================================== */}
          {/* LAYER 3: Hydrography (Water bodies & streams)                   */}
          {/* =============================================================== */}
          {showHydroBiomes && (
            <g id="layer-hydrography">
              {/* Étang des Hérons */}
              <path
                d="M 120,590 C 130,565 170,555 210,570 C 250,585 270,620 255,650 C 240,680 180,685 145,670 C 115,655 110,615 120,590 Z"
                fill="#2D6A4F"
                fillOpacity="0.45"
                stroke="#52B788"
                strokeWidth="1.5"
              />
              <path
                d="M 120,590 C 130,565 170,555 210,570 C 250,585 270,620 255,650 C 240,680 180,685 145,670 C 115,655 110,615 120,590 Z"
                fill={`url(#${idPrefix}-waterPattern)`}
              />
              <text
                x="185"
                y="635"
                textAnchor="middle"
                fill="#B7E4C7"
                className="font-serif italic text-[11px] font-semibold"
                opacity="0.85"
              >
                Étang des Hérons
              </text>

              {/* Ruisseau des Mousses (meandering stream) */}
              <path
                d="M 760,180 C 700,230 640,280 580,330 C 510,390 440,430 380,480 C 310,540 250,565 210,570"
                fill="none"
                stroke="#52B788"
                strokeWidth="2.25"
                strokeLinecap="round"
                strokeLinejoin="round"
                opacity="0.8"
              />
              <text
                x="470"
                y="410"
                transform="rotate(-28, 470, 410)"
                fill="#74C69D"
                className="font-serif italic text-[9px]"
                opacity="0.75"
              >
                Ruisseau des Mousses
              </text>
            </g>
          )}

          {/* =============================================================== */}
          {/* LAYER 4: Biome Zones & Typography                               */}
          {/* =============================================================== */}
          {showHydroBiomes && (
            <g id="layer-biomes" className="select-none pointer-events-none">
              <text
                x="810"
                y="65"
                fill="#E9F5ED"
                className="font-['Barlow_Semi_Condensed'] font-bold text-[13px] tracking-wide"
                opacity="0.9"
              >
                Crête des Cèdres (420m)
              </text>
              <text
                x="620"
                y="150"
                fill="#B7E4C7"
                className="font-['Barlow_Semi_Condensed'] font-semibold text-[11px]"
                opacity="0.8"
              >
                Chaos Géologique & Karsts
              </text>
              <text
                x="470"
                y="345"
                fill="#B7E4C7"
                className="font-['Barlow_Semi_Condensed'] font-semibold text-[12px]"
                opacity="0.8"
              >
                Canopée Primaire
              </text>
              <text
                x="320"
                y="325"
                fill="#8EBAA0"
                className="font-['Barlow_Semi_Condensed'] font-semibold text-[11px]"
                opacity="0.75"
              >
                Vallée des Fougères
              </text>
              <text
                x="260"
                y="630"
                fill="#8EBAA0"
                className="font-['Barlow_Semi_Condensed'] font-semibold text-[11px]"
                opacity="0.75"
              >
                Marais & Roselières
              </text>
              <text
                x="130"
                y="370"
                fill="#8EBAA0"
                className="font-['Barlow_Semi_Condensed'] font-semibold text-[11px]"
                opacity="0.75"
              >
                Vallon Bocager PMR
              </text>
            </g>
          )}

          {/* =============================================================== */}
          {/* LAYER 5: 6 Trail SVG paths - « Tracé vivant » & Status Waves    */}
          {/* =============================================================== */}
          {showTrails && (
            <g id="layer-trails">
              {trails.map((trail) => {
                const isSelected = effectiveSelectedId === trail.id;
                const isHovered = hoveredTrailId === trail.id;
                const strokeColor = getTrailStroke(trail.status);
                const dashArray = getTrailDashArray(trail.status);
                const isSolidOpen = trail.status === 'fluide';
                const hasWave = statusWave?.trailId === trail.id;

                // Midpoint for Éco-Garde status shockwave
                const midIdx = Math.floor((trail.elevationProfile?.length || 1) / 2);
                const waveCenter =
                  trail.elevationProfile?.[midIdx]?.mapCoord || trail.startPoint;

                // Opacity logic: if one is selected explicitly, dim others
                const trailOpacity = isSelected
                  ? 1.0
                  : selectedTrailId
                  ? 0.3
                  : isHovered
                  ? 1.0
                  : 0.85;

                return (
                  <g
                    key={trail.id}
                    className="cursor-pointer group"
                    onClick={() => handleTrailClick(trail.id)}
                    onMouseEnter={() => setHoveredTrailId(trail.id)}
                    onMouseLeave={() => setHoveredTrailId(null)}
                    tabIndex={0}
                    role="button"
                    aria-label={`${trail.name}, ${trail.lengthKm} km, statut: ${trail.status}`}
                    onKeyDown={(e) => {
                      if (e.key === 'Enter' || e.key === ' ') {
                        handleTrailClick(trail.id);
                      }
                    }}
                  >
                    {/* Invisible wider hit-area + exact geometry ref for getPointAtLength */}
                    <path
                      ref={(el) => {
                        trailPathRefs.current[trail.id] = el;
                      }}
                      d={trail.mapPath}
                      fill="none"
                      stroke="transparent"
                      strokeWidth={18}
                      strokeLinecap="round"
                    />

                    {/* Subtle ghost guide under selected trail while self-drawing */}
                    {isSelected && (
                      <path
                        d={trail.mapPath}
                        fill="none"
                        stroke={strokeColor}
                        strokeWidth={2.5}
                        strokeDasharray="3 5"
                        opacity={0.22}
                      />
                    )}

                    {/* Active Halo Glow */}
                    {isSelected && (
                      <path
                        key={`halo-${trail.id}-${drawEpoch}`}
                        d={trail.mapPath}
                        pathLength={1000}
                        fill="none"
                        stroke={strokeColor}
                        strokeWidth={10}
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        opacity={0.35}
                        filter={`url(#${idPrefix}-glow)`}
                        className="eco-trail-self-draw"
                      />
                    )}

                    {/* Main Trail Path: Progressive Self-Drawing + Daltonism Dash/Hatch */}
                    {isSelected && isSolidOpen ? (
                      <path
                        key={`main-solid-${trail.id}-${drawEpoch}`}
                        d={trail.mapPath}
                        pathLength={1000}
                        fill="none"
                        stroke={strokeColor}
                        strokeWidth={5.5}
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        opacity={trailOpacity}
                        className="eco-trail-self-draw"
                      />
                    ) : (
                      <path
                        key={`main-patterned-${trail.id}-${isSelected ? drawEpoch : 0}`}
                        d={trail.mapPath}
                        fill="none"
                        stroke={strokeColor}
                        strokeWidth={isSelected ? 5.5 : isHovered ? 4.5 : 3.5}
                        strokeDasharray={dashArray}
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        opacity={trailOpacity}
                        mask={isSelected ? `url(#${idPrefix}-draw-mask-${trail.id})` : undefined}
                        className="transition-all duration-200"
                      />
                    )}

                    {/* Daltonism-Safe Cross-Hatch Barrier Ticks (×) on Closed Trails */}
                    {trail.status === 'ferme' &&
                      (trail.elevationProfile || [])
                        .filter((_, idx, arr) => idx > 0 && idx < arr.length - 1)
                        .map((pt, idx) => (
                          <g
                            key={`hatch-${trail.id}-${idx}`}
                            transform={`translate(${pt.mapCoord.x}, ${pt.mapCoord.y})`}
                            opacity={trailOpacity}
                            className="pointer-events-none"
                          >
                            <circle r="5.5" fill="#121614" stroke="#DC2626" strokeWidth="1.25" />
                            <path
                              d="M -2.6,-2.6 L 2.6,2.6 M 2.6,-2.6 L -2.6,2.6"
                              stroke="#FCA5A5"
                              strokeWidth="1.5"
                              strokeLinecap="round"
                            />
                          </g>
                        ))}

                    {/* Concentric Cartographic Shockwave when Ranger modifies trail status */}
                    {hasWave && (
                      <g
                        key={`wave-${trail.id}-${statusWave?.timestamp}`}
                        transform={`translate(${waveCenter.x}, ${waveCenter.y})`}
                        className="pointer-events-none"
                      >
                        {[0, 220, 440].map((delayMs, idx) => (
                          <circle
                            key={idx}
                            r="18"
                            fill="none"
                            stroke={strokeColor}
                            strokeWidth="2.5"
                            className="eco-shockwave-ring"
                            style={{ '--wave-delay': `${delayMs}ms` } as React.CSSProperties}
                          />
                        ))}
                      </g>
                    )}

                    {/* Trail departure / arrival points markers */}
                    <circle
                      cx={trail.startPoint.x}
                      cy={trail.startPoint.y}
                      r={isSelected ? 5.5 : 3.5}
                      fill={strokeColor}
                      stroke="#FFFFFF"
                      strokeWidth={1.5}
                      opacity={trailOpacity}
                    />
                    <circle
                      cx={trail.endPoint.x}
                      cy={trail.endPoint.y}
                      r={isSelected ? 4.5 : 3}
                      fill="#121614"
                      stroke={strokeColor}
                      strokeWidth={2}
                      opacity={trailOpacity}
                    />
                  </g>
                );
              })}
            </g>
          )}

          {/* =============================================================== */}
          {/* LAYER 6: 10 POI Markers (Interactive)                           */}
          {/* =============================================================== */}
          {showPois && (
            <g id="layer-pois">
              {pois.map((poi) => {
                const isActive = activePoi?.id === poi.id;
                return (
                  <g
                    key={poi.id}
                    transform={`translate(${poi.coordinates.x}, ${poi.coordinates.y})`}
                    className="cursor-pointer transition-transform group"
                    onClick={(e) => {
                      e.stopPropagation();
                      setActivePoi(isActive ? null : poi);
                    }}
                    tabIndex={0}
                    role="button"
                    aria-label={`Point d intérêt: ${poi.name}`}
                    onKeyDown={(e) => {
                      if (e.key === 'Enter' || e.key === ' ') {
                        setActivePoi(isActive ? null : poi);
                      }
                    }}
                  >
                    {/* Animated pulse on active POI */}
                    {isActive && (
                      <circle
                        r="14"
                        fill="none"
                        stroke="#52B788"
                        strokeWidth="2"
                        className="animate-ping opacity-75"
                      />
                    )}

                    {/* POI outer circle */}
                    <circle
                      r={isActive ? 10 : 8}
                      fill={isActive ? '#52B788' : '#1F2421'}
                      stroke={isActive ? '#FFFFFF' : '#52B788'}
                      strokeWidth="2"
                      className="group-hover:scale-125 transition-transform"
                    />

                    {/* Inner Center Dot */}
                    <circle
                      r="3.5"
                      fill={isActive ? '#121614' : '#E9F5ED'}
                    />

                    {/* Label on hover or active */}
                    {(isActive || zoomLevel >= 1.4) && (
                      <text
                        y={-14}
                        textAnchor="middle"
                        fill="#FFFFFF"
                        className="font-mono text-[9px] font-bold drop-shadow-md pointer-events-none"
                      >
                        {poi.name.split('&')[0].trim()}
                      </text>
                    )}
                  </g>
                );
              })}
            </g>
          )}

          {/* =============================================================== */}
          {/* LAYER 7: Exact getPointAtLength Hiker Beacon Synced from Profile */}
          {/* =============================================================== */}
          {scrubPoint && exactHikerBeacon && (
            <g
              id="layer-interactive-cursor"
              transform={`translate(${exactHikerBeacon.x}, ${exactHikerBeacon.y})`}
              className="pointer-events-none"
            >
              {/* Radar pulse ripples */}
              <circle r="18" fill="none" stroke="#E76F51" strokeWidth="2" className="animate-ping" />
              <circle r="11" fill="#E76F51" fillOpacity="0.45" stroke="#FFFFFF" strokeWidth="2" />

              {/* Directional Tangent Heading Chevron */}
              <g transform={`rotate(${exactHikerBeacon.angleDeg})`}>
                <polygon points="8,0 -4,-4.5 -1.5,0 -4,4.5" fill="#FFFFFF" />
              </g>

              {/* Viewport-aware Synchronized Callout Box */}
              <g
                transform={`translate(${exactHikerBeacon.x > 820 ? -152 : 15}, ${
                  exactHikerBeacon.y < 75 ? 12 : -36
                })`}
              >
                <rect
                  x="0"
                  y="0"
                  width="138"
                  height="38"
                  rx="6"
                  fill="#1F2421"
                  stroke="#E76F51"
                  strokeWidth="1.5"
                  className="shadow-xl"
                />
                <text x="8" y="15" fill="#E76F51" className="font-mono text-[10px] font-bold">
                  {scrubPoint.poiLabel ? scrubPoint.poiLabel : `Km ${scrubPoint.distanceKm.toFixed(2)}`}
                </text>
                <text x="8" y="29" fill="#E9F5ED" className="font-mono text-[9px]">
                  Alt: {scrubPoint.elevationM} m
                  {scrubPoint.slopePercent !== undefined ? ` · ${scrubPoint.slopePercent}%` : ''}
                </text>
              </g>
            </g>
          )}

          {/* =============================================================== */}
          {/* LAYER 8: Map Chrome (Compass Rose, Metric Scale & North)        */}
          {/* =============================================================== */}
          <g id="layer-map-chrome" className="pointer-events-none select-none">
            {/* North Compass Rose at Top-Right */}
            <g transform="translate(940, 60)">
              <circle r="22" fill="#1F2421" stroke="#36403A" strokeWidth="1" opacity="0.8" />
              {/* North Pointer Needle */}
              <polygon points="0,-18 5,0 0,-4 -5,0" fill="#52B788" />
              <polygon points="0,18 5,0 0,4 -5,0" fill="#36403A" />
              <text x="0" y="-8" textAnchor="middle" fill="#FFFFFF" className="font-mono text-[9px] font-bold">
                N
              </text>
            </g>

            {/* Metric Scale Bar at Bottom-Right */}
            <g transform="translate(850, 665)">
              <rect x="0" y="0" width="110" height="4" fill="#52B788" opacity="0.8" />
              <line x1="0" y1="-3" x2="0" y2="7" stroke="#52B788" strokeWidth="1.5" />
              <line x1="55" y1="-2" x2="55" y2="6" stroke="#52B788" strokeWidth="1" />
              <line x1="110" y1="-3" x2="110" y2="7" stroke="#52B788" strokeWidth="1.5" />
              <text x="0" y="18" fill="#8EBAA0" className="font-mono text-[9px]">0</text>
              <text x="55" y="18" textAnchor="middle" fill="#8EBAA0" className="font-mono text-[9px]">500m</text>
              <text x="110" y="18" textAnchor="end" fill="#8EBAA0" className="font-mono text-[9px]">1 km</text>
            </g>

            {/* Park Cartographic Badge at Bottom-Left */}
            <g transform="translate(30, 665)">
              <text fill="#8EBAA0" className="font-mono text-[9px]">
                ECO-PARK R.B.I. · RGF93 / Lambert-93 · Dénivelé 110m - 420m
              </text>
            </g>
          </g>
        </svg>
      </div>

      {/* POI Detailed Popover Modal when a POI is clicked */}
      {activePoi && (
        <div className="absolute bottom-4 left-4 right-4 sm:left-auto sm:right-4 sm:w-96 z-30 p-5 rounded-2xl bg-[#1F2421]/95 backdrop-blur-md border border-[#52B788] shadow-2xl text-white space-y-3 animate-in fade-in zoom-in-95 duration-150">
          <div className="flex items-start justify-between gap-3">
            <div className="flex items-center gap-2">
              <div className="p-2 rounded-xl bg-[#29302C] text-[#52B788] border border-[#36403A]">
                {renderPoiIcon(activePoi.category)}
              </div>
              <div>
                <span className="text-[10px] font-mono font-semibold uppercase text-[#74C69D]">
                  {activePoi.categoryLabel} · Alt. {activePoi.altitudeM} m
                </span>
                <h4 className="font-['Barlow_Semi_Condensed'] text-base font-bold text-white">
                  {activePoi.name}
                </h4>
              </div>
            </div>

            <button
              type="button"
              onClick={() => setActivePoi(null)}
              className="p-1.5 rounded-lg text-[#C9D1CC] hover:text-white hover:bg-[#29302C] transition-colors cursor-pointer"
              aria-label="Fermer le détail du POI"
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          <p className="text-xs text-[#C9D1CC] leading-relaxed">
            {activePoi.description}
          </p>

          {activePoi.services && activePoi.services.length > 0 && (
            <div className="pt-2 border-t border-[#36403A] flex flex-wrap gap-1.5">
              {activePoi.services.map((svc, i) => (
                <span
                  key={i}
                  className="px-2 py-0.5 rounded-md bg-[#29302C] border border-[#36403A] text-[10px] font-mono text-[#8EBAA0]"
                >
                  ✓ {svc}
                </span>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Bottom Daltonism & Status Legend Bar */}
      <div className="p-3 bg-[#1F2421] border-t border-[#2D6A4F]/60 flex flex-wrap items-center justify-between gap-3 text-xs font-mono text-[#C9D1CC]">
        <div className="flex flex-wrap items-center gap-4">
          <span className="text-[#8EBAA0] font-semibold text-[11px]">Légende :</span>
          <span className="flex items-center gap-1.5">
            <span className="inline-block w-4 h-1 bg-[#52B788] rounded-full" />
            <span className="text-emerald-300 font-medium">Fluide (Trait plein)</span>
          </span>
          <span className="flex items-center gap-1.5">
            <span className="inline-block w-4 h-1 bg-[#E76F51] border-b border-dashed border-[#E76F51]" />
            <span className="text-amber-300 font-medium">Balisé (Trait mixte)</span>
          </span>
          <span className="flex items-center gap-1.5">
            <span className="inline-block w-4 h-1 bg-[#DC2626] border-b border-dotted border-[#DC2626]" />
            <span className="text-red-300 font-medium">Fermé (Pointillés barrière)</span>
          </span>
        </div>

        <div className="text-[11px] text-[#8EBAA0]">
          Cliquez sur un sentier ou POI pour voir ses données détaillées
        </div>
      </div>
    </div>
  );
};
