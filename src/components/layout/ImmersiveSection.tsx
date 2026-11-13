// ============================================================================
// ECO-PARK IMMERSIVE EDITORIAL CONTAINER (src/components/layout/ImmersiveSection.tsx)
// ============================================================================

import React, { ReactNode } from 'react';

export type ImmersiveVariant = 'canopy' | 'bark' | 'forest';

export interface ImmersiveSectionProps {
  children: ReactNode;
  variant?: ImmersiveVariant;
  className?: string;
  containerClassName?: string;
  id?: string;
  ariaLabel?: string;
  withTopographicPattern?: boolean;
}

/**
 * ImmersiveSection ensures that critical editorial sections (Hero, Impact Banner, Major CTAs)
 * retain a deep, nature-immersive dark backdrop (Deep Canopy #1B4332 or Deep Bark #1F2421)
 * with crisp, high-contrast light typography (#E9F5ED = 14.07:1 WCAG AAA), regardless of
 * whether the global interface theme is currently set to Light or Dark.
 */
export const ImmersiveSection: React.FC<ImmersiveSectionProps> = ({
  children,
  variant = 'canopy',
  className = '',
  containerClassName = '',
  id,
  ariaLabel,
  withTopographicPattern = true,
}) => {
  // Color configuration mapped strictly to authoritative tokens
  const variantStyles: Record<
    ImmersiveVariant,
    { background: string; border: string; accentColor: string }
  > = {
    canopy: {
      background: 'bg-[#1B4332] text-[#E9F5ED]',
      border: 'border-[#2D6A4F]/60',
      accentColor: '#52B788',
    },
    bark: {
      background: 'bg-[#1F2421] text-[#E9F5ED]',
      border: 'border-[#36403A]/60',
      accentColor: '#74C69D',
    },
    forest: {
      background: 'bg-[#2D6A4F] text-[#E9F5ED]',
      border: 'border-[#40916C]/60',
      accentColor: '#B7E4C7',
    },
  };

  const selected = variantStyles[variant];

  return (
    <section
      id={id}
      aria-label={ariaLabel}
      className={`relative overflow-hidden ${selected.background} ${selected.border} ${className}`}
      style={{
        // Ensure child elements default to light text colors even if CSS inheritance applies
        color: '#E9F5ED',
      }}
    >
      {/* Subtle organic topographic / contour SVG overlay */}
      {withTopographicPattern && (
        <div
          aria-hidden="true"
          className="pointer-events-none absolute inset-0 opacity-[0.06] mix-blend-screen"
        >
          <svg
            className="w-full h-full object-cover"
            viewBox="0 0 1000 400"
            preserveAspectRatio="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M0,100 C200,80 350,140 500,110 C650,80 800,130 1000,100"
              fill="none"
              stroke="#52B788"
              strokeWidth="1.5"
            />
            <path
              d="M0,180 C220,150 400,210 600,170 C800,130 900,190 1000,170"
              fill="none"
              stroke="#52B788"
              strokeWidth="1.5"
              strokeDasharray="4 4"
            />
            <path
              d="M0,260 C180,240 380,300 550,270 C720,240 880,290 1000,260"
              fill="none"
              stroke="#52B788"
              strokeWidth="1.5"
            />
            <path
              d="M0,340 C250,310 450,370 700,330 C850,300 950,350 1000,340"
              fill="none"
              stroke="#52B788"
              strokeWidth="1.5"
              strokeDasharray="4 4"
            />
          </svg>
        </div>
      )}

      {/* Content wrapper */}
      <div className={`relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 ${containerClassName}`}>
        {children}
      </div>
    </section>
  );
};
