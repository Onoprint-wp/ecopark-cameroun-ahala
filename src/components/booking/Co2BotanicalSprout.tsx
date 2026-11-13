// ============================================================================
// CO2 BOTANICAL SPROUT VISUALIZER (src/components/booking/Co2BotanicalSprout.tsx)
// « De la graine à l'arbre » — Combined Rolling Counter + Living SVG Sapling
// ============================================================================

import React from 'react';
import { Sparkles, Leaf } from 'lucide-react';
import { MobilityMode } from '../../types/ecosystem';
import {
  computeBotanicalGrowthStage,
  useAnimatedNumber,
} from '../../utils/ecoMotion';

export interface Co2BotanicalSproutProps {
  co2AvoidedKg: number;
  mobilityMode: MobilityMode;
  guestCount: number;
}

const BRANCH_DEFS = [
  { id: 1, d: 'M 90,94 Q 72,86 60,74', strokeW: 2.4 },
  { id: 2, d: 'M 90,80 Q 108,72 120,60', strokeW: 2.3 },
  { id: 3, d: 'M 90,64 Q 70,54 56,42', strokeW: 2.0 },
  { id: 4, d: 'M 90,48 Q 110,38 122,28', strokeW: 1.9 },
];

const LEAF_DEFS = [
  { id: 1, cx: 58, cy: 72, rot: -38, color: '#52B788' },
  { id: 2, cx: 122, cy: 58, rot: 36, color: '#74C69D' },
  { id: 3, cx: 74, cy: 84, rot: -22, color: '#40916C' },
  { id: 4, cx: 106, cy: 70, rot: 25, color: '#52B788' },
  { id: 5, cx: 54, cy: 40, rot: -42, color: '#74C69D' },
  { id: 6, cx: 124, cy: 26, rot: 38, color: '#52B788' },
  { id: 7, cx: 82, cy: 32, rot: -18, color: '#95D5B2' },
  { id: 8, cx: 96, cy: 20, rot: 12, color: '#74C69D' },
];

export const Co2BotanicalSprout: React.FC<Co2BotanicalSproutProps> = ({
  co2AvoidedKg,
  mobilityMode,
  guestCount,
}) => {
  const growth = computeBotanicalGrowthStage(co2AvoidedKg);
  const animatedKg = useAnimatedNumber(co2AvoidedKg, 560, 1);

  const trunkColor = growth.isWilted ? '#A46E3B' : '#2D6A4F';
  const stemDashOffset = Math.round((1 - growth.stemDrawRatio) * 100);

  return (
    <div className="p-4 sm:p-5 rounded-2xl bg-[var(--bg-elevated)] border border-[var(--border-default)] flex flex-col sm:flex-row items-center gap-5 transition-colors">
      {/* Living Botanical SVG Canvas */}
      <div className="relative w-36 h-28 shrink-0 rounded-xl bg-[#121614] border border-[#2D6A4F]/60 flex items-center justify-center overflow-hidden shadow-inner">
        {/* Soft canopy radial aura when thriving */}
        <div
          className="absolute inset-0 pointer-events-none transition-opacity duration-500"
          style={{
            opacity: growth.isWilted ? 0.12 : 0.25 + growth.stage * 0.45,
            background: growth.isWilted
              ? 'radial-gradient(circle at 50% 75%, rgba(212, 163, 115, 0.35), transparent 70%)'
              : 'radial-gradient(circle at 50% 40%, rgba(82, 183, 136, 0.45), transparent 72%)',
          }}
        />

        <svg
          viewBox="0 0 180 130"
          className="w-full h-full relative z-10"
          role="img"
          aria-label={`Visualisation botanique : ${growth.stageLabel}`}
        >
          {/* Forest soil mound & seed */}
          <path
            d="M 38,118 Q 90,104 142,118 Z"
            fill="#4E321B"
            stroke="#D4A373"
            strokeWidth="1.2"
            strokeOpacity="0.65"
          />
          <ellipse cx="90" cy="114" rx="7" ry="4" fill="#D4A373" opacity="0.85" />

          {/* Animated Plant Group (droops gently if voiture_solo = 0 kg avoided) */}
          <g
            style={{
              transformOrigin: '90px 114px',
              transform: growth.isWilted ? 'rotate(14deg) scale(0.86)' : 'rotate(0deg) scale(1)',
              transition: 'transform 520ms cubic-bezier(0.22, 1, 0.36, 1)',
            }}
          >
            {/* Central Stem */}
            <path
              d="M 90,114 C 89,92 91,62 90,22"
              pathLength={100}
              fill="none"
              stroke={trunkColor}
              strokeWidth="3.6"
              strokeLinecap="round"
              strokeDasharray="100"
              strokeDashoffset={stemDashOffset}
              style={{
                transition: 'stroke-dashoffset 560ms cubic-bezier(0.22, 1, 0.36, 1), stroke 350ms ease',
              }}
            />

            {/* Lateral Branches */}
            {BRANCH_DEFS.map((b) => {
              const visible = b.id <= growth.activeBranches;
              return (
                <path
                  key={b.id}
                  d={b.d}
                  pathLength={100}
                  fill="none"
                  stroke={trunkColor}
                  strokeWidth={b.strokeW}
                  strokeLinecap="round"
                  strokeDasharray="100"
                  strokeDashoffset={visible ? 0 : 100}
                  style={{
                    transition: `stroke-dashoffset 480ms cubic-bezier(0.22, 1, 0.36, 1) ${b.id * 65}ms`,
                  }}
                />
              );
            })}

            {/* Sprouting Leaves */}
            {LEAF_DEFS.map((leaf) => {
              const isLeafActive = !growth.isWilted && leaf.id <= growth.activeLeaves;
              return (
                <g
                  key={leaf.id}
                  transform={`translate(${leaf.cx}, ${leaf.cy}) rotate(${leaf.rot})`}
                >
                  <path
                    d="M 0,0 C -6,-8 -4,-17 0,-21 C 4,-17 6,-8 0,0 Z"
                    fill={leaf.color}
                    className="eco-leaf-sprout"
                    style={{
                      opacity: isLeafActive ? 1 : 0,
                      transform: isLeafActive ? 'scale(1)' : 'scale(0.05)',
                      transitionDelay: `${leaf.id * 45}ms`,
                    }}
                  />
                </g>
              );
            })}

            {/* Single drooping amber leaf when wilted */}
            {growth.isWilted && (
              <g transform="translate(96, 86) rotate(68)">
                <path
                  d="M 0,0 C -5,-7 -3,-14 0,-17 C 3,-14 5,-7 0,0 Z"
                  fill="#D4A373"
                  opacity="0.85"
                />
              </g>
            )}
          </g>
        </svg>
      </div>

      {/* Live Rolling CO2 Telemetry & Guidance */}
      <div className="flex-1 space-y-1.5 text-center sm:text-left">
        <div className="inline-flex items-center gap-1.5 text-[11px] font-mono font-bold uppercase tracking-wider text-[var(--brand-primary)]">
          <Leaf className="w-3.5 h-3.5 text-[#52B788]" />
          <span>Simulateur « De la graine à l&apos;arbre »</span>
        </div>

        <div className="flex flex-wrap items-baseline justify-center sm:justify-start gap-2">
          <span
            className={`font-mono text-2xl sm:text-3xl font-extrabold tracking-tight ${
              growth.isWilted
                ? 'text-amber-700 dark:text-amber-400'
                : 'text-emerald-700 dark:text-emerald-400'
            }`}
          >
            +{animatedKg.toFixed(1)} kg CO₂
          </span>
          <span className="text-xs text-[var(--text-muted)] font-medium">
            évités ({guestCount} visiteur{guestCount > 1 ? 's' : ''})
          </span>
        </div>

        <p className="text-xs text-[var(--text-primary)] font-semibold flex items-center justify-center sm:justify-start gap-1.5">
          <Sparkles className="w-3.5 h-3.5 text-[#52B788] shrink-0" />
          <span>{growth.stageLabel}</span>
        </p>

        <p className="text-[11px] text-[var(--text-muted)] leading-relaxed">
          {mobilityMode === 'voiture_solo'
            ? 'Astuce : optez pour la Prévente Orange Money / MTN MoMo, la Navette Climatisée ou le Tarif Groupe 20+ (-30 %) pour amplifier votre bonus écologique.'
            : 'Chaque kilogramme de CO₂ évité contribue directement à la préservation du microclimat forestier d’Ahala.'}
        </p>
      </div>
    </div>
  );
};
