// ============================================================================
// GERMINATING QR CODE SVG (src/components/booking/GerminatingQrCode.tsx)
// Spiral Botanical Seed Germination -> Settles into 1-Node ISO Crisp Vector Path
// ============================================================================

import React, { useMemo, useState, useEffect } from 'react';
import {
  EccLevel,
  generateQrMatrix,
  generateQrSvgPath,
} from '../../utils/qrCodeGenerator';
import {
  computeSpiralGerminationDelays,
  isReducedMotionPreferred,
} from '../../utils/ecoMotion';

export interface GerminatingQrCodeProps {
  value: string;
  size?: number;
  fgColor?: string;
  bgColor?: string;
  quietZone?: number;
  eccLevel?: EccLevel;
  germinationKey?: string | number;
  disableAnimation?: boolean;
  title?: string;
  className?: string;
}

export const GerminatingQrCode: React.FC<GerminatingQrCodeProps> = ({
  value,
  size = 184,
  fgColor = '#1B4332',
  bgColor = '#FFFFFF',
  quietZone = 2,
  eccLevel = 'M',
  germinationKey = 0,
  disableAnimation = false,
  title = 'Éco-Pass QR Code',
  className = '',
}) => {
  const shouldSkipMotion = disableAnimation || isReducedMotionPreferred();
  const [isSettled, setIsSettled] = useState<boolean>(shouldSkipMotion);

  useEffect(() => {
    if (shouldSkipMotion) {
      setIsSettled(true);
      return;
    }

    setIsSettled(false);
    const timer = window.setTimeout(() => {
      setIsSettled(true);
    }, 1080);

    return () => window.clearTimeout(timer);
  }, [value, germinationKey, shouldSkipMotion]);

  const { seeds, pathData, viewBoxSize } = useMemo(() => {
    const matrix = generateQrMatrix(value, { eccLevel, quietZone });
    const computedSeeds = computeSpiralGerminationDelays(matrix, 620);
    const crisp = generateQrSvgPath(value, { eccLevel, quietZone });
    return {
      seeds: computedSeeds,
      pathData: crisp.pathData,
      viewBoxSize: crisp.size,
    };
  }, [value, eccLevel, quietZone]);

  return (
    <svg
      role="img"
      aria-label={title}
      viewBox={`0 0 ${viewBoxSize} ${viewBoxSize}`}
      width={size}
      height={size}
      shapeRendering={isSettled ? 'crispEdges' : 'geometricPrecision'}
      className={className}
      style={{ display: 'block', maxWidth: '100%', height: 'auto' }}
    >
      <title>{title}</title>
      {bgColor !== 'transparent' && (
        <rect width={viewBoxSize} height={viewBoxSize} fill={bgColor} />
      )}

      {isSettled ? (
        <path d={pathData} fill={fgColor} />
      ) : (
        <g key={`bloom-${germinationKey}`}>
          {seeds.map((seed) => (
            <rect
              key={`${seed.row}-${seed.col}`}
              x={seed.col + quietZone - 0.02}
              y={seed.row + quietZone - 0.02}
              width={1.04}
              height={1.04}
              rx={seed.isFinder ? 0.08 : 0.18}
              fill={fgColor}
              className="eco-qr-seed"
              style={{ '--seed-delay': `${seed.delayMs}ms` } as React.CSSProperties}
            />
          ))}
        </g>
      )}
    </svg>
  );
};
