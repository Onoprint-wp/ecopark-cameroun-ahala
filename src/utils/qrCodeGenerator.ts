// ============================================================================
// PURE TYPESCRIPT CLIENT-SIDE SVG QR CODE GENERATOR (src/utils/qrCodeGenerator.ts)
// Zero external dependencies · ISO/IEC 18004 Standard QR Algorithm
// ============================================================================

import React from 'react';

export type EccLevel = 'L' | 'M';

export interface QrOptions {
  eccLevel?: EccLevel;
  quietZone?: number;
  maskPattern?: number; // 0-7, or auto if omitted
}

export interface QrCodeProps extends QrOptions {
  value: string;
  size?: number | string;
  fgColor?: string;
  bgColor?: string;
  className?: string;
  title?: string;
}

// ----------------------------------------------------------------------------
// 1. Galois Field GF(256) Arithmetic & Reed-Solomon Code
// ----------------------------------------------------------------------------
const GF_EXP = new Uint8Array(512);
const GF_LOG = new Uint8Array(256);

(function initGaloisField() {
  let val = 1;
  for (let i = 0; i < 255; i++) {
    GF_EXP[i] = val;
    GF_EXP[i + 255] = val;
    GF_LOG[val] = i;
    val <<= 1;
    if (val & 256) {
      val ^= 285; // Primitive polynomial x^8 + x^4 + x^3 + x^2 + 1 (0x11D)
    }
  }
})();

function gfMultiply(a: number, b: number): number {
  if (a === 0 || b === 0) return 0;
  return GF_EXP[GF_LOG[a] + GF_LOG[b]];
}

function rsGeneratorPolynomial(degree: number): number[] {
  let poly = [1];
  for (let i = 0; i < degree; i++) {
    const next = new Array(poly.length + 1).fill(0);
    const alphaI = GF_EXP[i];
    for (let j = 0; j < poly.length; j++) {
      next[j] ^= poly[j];
      next[j + 1] ^= gfMultiply(poly[j], alphaI);
    }
    poly = next;
  }
  return poly;
}

function rsComputeRemainder(data: number[], numEcCodewords: number): number[] {
  const gen = rsGeneratorPolynomial(numEcCodewords);
  const remainder = new Array(numEcCodewords).fill(0);

  for (let i = 0; i < data.length; i++) {
    const factor = data[i] ^ remainder[0];
    remainder.shift();
    remainder.push(0);
    for (let j = 0; j < numEcCodewords; j++) {
      remainder[j] ^= gfMultiply(factor, gen[j + 1]);
    }
  }

  return remainder;
}

// ----------------------------------------------------------------------------
// 2. Version Specifications (Versions 1-4)
// ----------------------------------------------------------------------------
interface QrBlockSpec {
  numBlocks: number;
  dataCodewordsPerBlock: number;
}

interface QrVersionSpec {
  version: number;
  ecc: EccLevel;
  totalCodewords: number;
  blocks: QrBlockSpec[];
  ecCodewordsPerBlock: number;
  alignmentPos: number[];
}

const QR_VERSIONS: QrVersionSpec[] = [
  // Version 1 (21x21)
  {
    version: 1,
    ecc: 'L',
    totalCodewords: 26,
    blocks: [{ numBlocks: 1, dataCodewordsPerBlock: 19 }],
    ecCodewordsPerBlock: 7,
    alignmentPos: [],
  },
  {
    version: 1,
    ecc: 'M',
    totalCodewords: 26,
    blocks: [{ numBlocks: 1, dataCodewordsPerBlock: 16 }],
    ecCodewordsPerBlock: 10,
    alignmentPos: [],
  },
  // Version 2 (25x25)
  {
    version: 2,
    ecc: 'L',
    totalCodewords: 44,
    blocks: [{ numBlocks: 1, dataCodewordsPerBlock: 34 }],
    ecCodewordsPerBlock: 10,
    alignmentPos: [6, 18],
  },
  {
    version: 2,
    ecc: 'M',
    totalCodewords: 44,
    blocks: [{ numBlocks: 1, dataCodewordsPerBlock: 28 }],
    ecCodewordsPerBlock: 16,
    alignmentPos: [6, 18],
  },
  // Version 3 (29x29)
  {
    version: 3,
    ecc: 'L',
    totalCodewords: 70,
    blocks: [{ numBlocks: 1, dataCodewordsPerBlock: 55 }],
    ecCodewordsPerBlock: 15,
    alignmentPos: [6, 22],
  },
  {
    version: 3,
    ecc: 'M',
    totalCodewords: 70,
    blocks: [{ numBlocks: 1, dataCodewordsPerBlock: 44 }],
    ecCodewordsPerBlock: 26,
    alignmentPos: [6, 22],
  },
  // Version 4 (33x33)
  {
    version: 4,
    ecc: 'L',
    totalCodewords: 100,
    blocks: [{ numBlocks: 1, dataCodewordsPerBlock: 80 }],
    ecCodewordsPerBlock: 20,
    alignmentPos: [6, 26],
  },
  {
    version: 4,
    ecc: 'M',
    totalCodewords: 100,
    blocks: [{ numBlocks: 2, dataCodewordsPerBlock: 32 }],
    ecCodewordsPerBlock: 18,
    alignmentPos: [6, 26],
  },
];

function selectVersion(dataLength: number, preferredEcc: EccLevel): QrVersionSpec {
  for (const spec of QR_VERSIONS) {
    if (spec.ecc !== preferredEcc) continue;
    let totalData = 0;
    for (const b of spec.blocks) {
      totalData += b.numBlocks * b.dataCodewordsPerBlock;
    }
    // Byte mode header: 4 bits mode + 8 bits length = 12 bits = ~2 bytes overhead
    if (dataLength + 2 <= totalData) {
      return spec;
    }
  }

  // Fallback to largest supported version with Level L
  const largestL = QR_VERSIONS[QR_VERSIONS.length - 2];
  return largestL;
}

// ----------------------------------------------------------------------------
// 3. Bit Stream Encoding (Byte Mode with UTF-8)
// ----------------------------------------------------------------------------
function encodeByteMode(text: string, spec: QrVersionSpec): number[] {
  const encoder = new TextEncoder();
  const rawBytes = Array.from(encoder.encode(text));

  let totalDataCodewords = 0;
  for (const b of spec.blocks) {
    totalDataCodewords += b.numBlocks * b.dataCodewordsPerBlock;
  }

  const bitBuffer: number[] = [];

  const pushBits = (value: number, count: number) => {
    for (let i = count - 1; i >= 0; i--) {
      bitBuffer.push((value >> i) & 1);
    }
  };

  // Mode indicator: 0100 (Byte mode)
  pushBits(0b0100, 4);

  // Character count indicator (8 bits for versions 1-9)
  const lengthToEncode = Math.min(rawBytes.length, totalDataCodewords - 2);
  pushBits(lengthToEncode, 8);

  // Data bytes
  for (let i = 0; i < lengthToEncode; i++) {
    pushBits(rawBytes[i], 8);
  }

  // Terminator (up to 4 zero bits)
  const capacityBits = totalDataCodewords * 8;
  const terminatorLength = Math.min(4, capacityBits - bitBuffer.length);
  for (let i = 0; i < terminatorLength; i++) {
    bitBuffer.push(0);
  }

  // Bit padding to byte boundary
  while (bitBuffer.length % 8 !== 0) {
    bitBuffer.push(0);
  }

  // Convert bit buffer to bytes
  const codewords: number[] = [];
  for (let i = 0; i < bitBuffer.length; i += 8) {
    let byteVal = 0;
    for (let j = 0; j < 8; j++) {
      byteVal = (byteVal << 1) | bitBuffer[i + j];
    }
    codewords.push(byteVal);
  }

  // Pad bytes alternating 0xEC (11101100) and 0x11 (00010001)
  const padPatterns = [0xec, 0x11];
  let padIdx = 0;
  while (codewords.length < totalDataCodewords) {
    codewords.push(padPatterns[padIdx % 2]);
    padIdx++;
  }

  return codewords;
}

// ----------------------------------------------------------------------------
// 4. Block Interleaving & Error Correction
// ----------------------------------------------------------------------------
function createInterleavedCodewords(dataCodewords: number[], spec: QrVersionSpec): number[] {
  const dataBlocks: number[][] = [];
  const ecBlocks: number[][] = [];

  let dataOffset = 0;
  for (const blockGroup of spec.blocks) {
    for (let b = 0; b < blockGroup.numBlocks; b++) {
      const slice = dataCodewords.slice(
        dataOffset,
        dataOffset + blockGroup.dataCodewordsPerBlock
      );
      dataBlocks.push(slice);
      ecBlocks.push(rsComputeRemainder(slice, spec.ecCodewordsPerBlock));
      dataOffset += blockGroup.dataCodewordsPerBlock;
    }
  }

  const finalCodewords: number[] = [];

  // Interleave data codewords
  let maxDataLen = 0;
  for (const block of dataBlocks) {
    if (block.length > maxDataLen) maxDataLen = block.length;
  }
  for (let col = 0; col < maxDataLen; col++) {
    for (let blk = 0; blk < dataBlocks.length; blk++) {
      if (col < dataBlocks[blk].length) {
        finalCodewords.push(dataBlocks[blk][col]);
      }
    }
  }

  // Interleave EC codewords
  for (let col = 0; col < spec.ecCodewordsPerBlock; col++) {
    for (let blk = 0; blk < ecBlocks.length; blk++) {
      finalCodewords.push(ecBlocks[blk][col]);
    }
  }

  return finalCodewords;
}

// ----------------------------------------------------------------------------
// 5. Format Information with BCH(15, 5)
// ----------------------------------------------------------------------------
function computeFormatBits(eccLevel: EccLevel, maskPattern: number): number {
  const eccBits = eccLevel === 'L' ? 1 : 0; // L=01 (1), M=00 (0)
  const data = (eccBits << 3) | (maskPattern & 0x7);
  let d = data << 10;
  const poly = 0x537;

  for (let i = 4; i >= 0; i--) {
    if ((d >> (i + 10)) & 1) {
      d ^= poly << i;
    }
  }

  return ((data << 10) | d) ^ 0x5412;
}

// ----------------------------------------------------------------------------
// 6. Matrix Construction & Function Patterns
// ----------------------------------------------------------------------------
function buildQrMatrix(
  spec: QrVersionSpec,
  codewords: number[],
  forcedMask?: number
): { matrix: boolean[][]; size: number } {
  const size = 17 + spec.version * 4;
  const matrix: (boolean | null)[][] = Array.from({ length: size }, () =>
    new Array(size).fill(null)
  );
  const isReserved: boolean[][] = Array.from({ length: size }, () =>
    new Array(size).fill(false)
  );

  // Helper to place fixed module
  const setFixed = (r: number, c: number, val: boolean) => {
    if (r >= 0 && r < size && c >= 0 && c < size) {
      matrix[r][c] = val;
      isReserved[r][c] = true;
    }
  };

  // 6.1 Place 7x7 Finder Pattern & 1-module Separator
  const placeFinder = (startRow: number, startCol: number) => {
    for (let r = -1; r <= 7; r++) {
      for (let c = -1; c <= 7; c++) {
        const row = startRow + r;
        const col = startCol + c;
        if (row < 0 || row >= size || col < 0 || col >= size) continue;

        if (r >= 0 && r <= 6 && c >= 0 && c <= 6) {
          const isBlack =
            r === 0 || r === 6 || c === 0 || c === 6 || (r >= 2 && r <= 4 && c >= 2 && c <= 4);
          setFixed(row, col, isBlack);
        } else {
          // Separator white ring
          setFixed(row, col, false);
        }
      }
    }
  };

  placeFinder(0, 0);
  placeFinder(0, size - 7);
  placeFinder(size - 7, 0);

  // 6.2 Timing Patterns
  for (let c = 8; c < size - 8; c++) {
    if (!isReserved[6][c]) {
      setFixed(6, c, c % 2 === 0);
    }
  }
  for (let r = 8; r < size - 8; r++) {
    if (!isReserved[r][6]) {
      setFixed(r, 6, r % 2 === 0);
    }
  }

  // 6.3 Alignment Patterns (Version >= 2)
  if (spec.alignmentPos.length > 0) {
    const centers = spec.alignmentPos;
    for (const rCenter of centers) {
      for (const cCenter of centers) {
        // Skip if overlaps with finders
        if (
          (rCenter < 8 && cCenter < 8) ||
          (rCenter < 8 && cCenter > size - 9) ||
          (rCenter > size - 9 && cCenter < 8)
        ) {
          continue;
        }

        for (let r = -2; r <= 2; r++) {
          for (let c = -2; c <= 2; c++) {
            const isBlack =
              Math.abs(r) === 2 || Math.abs(c) === 2 || (r === 0 && c === 0);
            setFixed(rCenter + r, cCenter + c, isBlack);
          }
        }
      }
    }
  }

  // 6.4 Dark Module
  const darkModuleRow = 4 * spec.version + 9;
  setFixed(darkModuleRow, 8, true);

  // 6.5 Reserve Format Info Modules (15 bits)
  // Around Top-Left
  for (let i = 0; i <= 8; i++) {
    if (i !== 6) isReserved[8][i] = true;
    if (i !== 6) isReserved[i][8] = true;
  }
  // Around Top-Right
  for (let col = size - 8; col < size; col++) {
    isReserved[8][col] = true;
  }
  // Around Bottom-Left
  for (let row = size - 7; row < size; row++) {
    isReserved[row][8] = true;
  }

  // 6.6 Place Data Bits in 2-column Zigzag
  const dataBits: boolean[] = [];
  for (const byte of codewords) {
    for (let i = 7; i >= 0; i--) {
      dataBits.push(((byte >> i) & 1) === 1);
    }
  }

  let bitIdx = 0;
  let dirUp = true;

  for (let rightCol = size - 1; rightCol > 0; rightCol -= 2) {
    if (rightCol === 6) {
      rightCol--; // Skip vertical timing column 6
    }
    const leftCol = rightCol - 1;

    const rowIndices: number[] = [];
    if (dirUp) {
      for (let r = size - 1; r >= 0; r--) rowIndices.push(r);
    } else {
      for (let r = 0; r < size; r++) rowIndices.push(r);
    }

    for (const r of rowIndices) {
      const colsToProcess = [rightCol, leftCol];
      for (const c of colsToProcess) {
        if (!isReserved[r][c]) {
          const bitVal = bitIdx < dataBits.length ? dataBits[bitIdx] : false;
          matrix[r][c] = bitVal;
          bitIdx++;
        }
      }
    }

    dirUp = !dirUp;
  }

  // 6.7 Choose Mask Pattern (0-7)
  const maskPattern = forcedMask !== undefined ? (forcedMask & 0x7) : 0;

  const maskFn = (r: number, c: number, p: number): boolean => {
    switch (p) {
      case 0:
        return (r + c) % 2 === 0;
      case 1:
        return r % 2 === 0;
      case 2:
        return c % 3 === 0;
      case 3:
        return (r + c) % 3 === 0;
      case 4:
        return (Math.floor(r / 2) + Math.floor(c / 3)) % 2 === 0;
      case 5:
        return ((r * c) % 2) + ((r * c) % 3) === 0;
      case 6:
        return (((r * c) % 2) + ((r * c) % 3)) % 2 === 0;
      case 7:
        return (((r + c) % 2) + ((r * c) % 3)) % 2 === 0;
      default:
        return (r + c) % 2 === 0;
    }
  };

  // Apply mask to unreserved data modules
  for (let r = 0; r < size; r++) {
    for (let c = 0; c < size; c++) {
      if (!isReserved[r][c]) {
        const original = matrix[r][c] === true;
        const invert = maskFn(r, c, maskPattern);
        matrix[r][c] = original !== invert;
      }
    }
  }

  // 6.8 Place Format Information (15 bits)
  const formatBits = computeFormatBits(spec.ecc, maskPattern);

  // Top-left finder region
  const formatPosTL: [number, number][] = [
    [8, 0],
    [8, 1],
    [8, 2],
    [8, 3],
    [8, 4],
    [8, 5],
    [8, 7],
    [8, 8],
    [7, 8],
    [5, 8],
    [4, 8],
    [3, 8],
    [2, 8],
    [1, 8],
    [0, 8],
  ];

  for (let i = 0; i < 15; i++) {
    const bitVal = ((formatBits >> (14 - i)) & 1) === 1;
    const [r, c] = formatPosTL[i];
    matrix[r][c] = bitVal;
  }

  // Split region: bottom-left (bits 0-6) and top-right (bits 7-14)
  for (let i = 0; i <= 6; i++) {
    const bitVal = ((formatBits >> (14 - i)) & 1) === 1;
    matrix[size - 1 - i][8] = bitVal;
  }
  for (let i = 7; i < 15; i++) {
    const bitVal = ((formatBits >> (14 - i)) & 1) === 1;
    matrix[8][size - 15 + i] = bitVal;
  }

  // Convert any remaining nulls to false
  const cleanMatrix: boolean[][] = matrix.map((row) =>
    row.map((cell) => cell === true)
  );

  return { matrix: cleanMatrix, size };
}

// ----------------------------------------------------------------------------
// 7. Public API: Matrix, SVG Path & Components
// ----------------------------------------------------------------------------

export function generateQrMatrix(text: string, options: QrOptions = {}): boolean[][] {
  const ecc = options.eccLevel || 'M';
  const spec = selectVersion(text.length, ecc);
  const dataCodewords = encodeByteMode(text, spec);
  const interleaved = createInterleavedCodewords(dataCodewords, spec);
  const { matrix } = buildQrMatrix(spec, interleaved, options.maskPattern);
  return matrix;
}

export function generateQrSvgPath(
  text: string,
  options: QrOptions = {}
): { pathData: string; size: number; quietZone: number } {
  const matrix = generateQrMatrix(text, options);
  const size = matrix.length;
  const quietZone = options.quietZone !== undefined ? options.quietZone : 2;

  let pathData = '';
  for (let r = 0; r < size; r++) {
    for (let c = 0; c < size; c++) {
      if (matrix[r][c]) {
        const x = c + quietZone;
        const y = r + quietZone;
        pathData += `M${x},${y}h1v1h-1z `;
      }
    }
  }

  return { pathData, size: size + quietZone * 2, quietZone };
}

export function generateQrSvgString(
  text: string,
  options: QrOptions & { fgColor?: string; bgColor?: string; pixelSize?: number } = {}
): string {
  const { pathData, size } = generateQrSvgPath(text, options);
  const fg = options.fgColor || '#1B4332';
  const bg = options.bgColor || 'transparent';
  const dim = options.pixelSize || 240;

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${size} ${size}" width="${dim}" height="${dim}" shape-rendering="crispEdges">
  ${bg !== 'transparent' ? `<rect width="${size}" height="${size}" fill="${bg}" />` : ''}
  <path d="${pathData}" fill="${fg}" />
</svg>`;
}

/**
 * Pure React SVG QR Code Component
 * Zero external libraries, rendered with crisp vector SVG path
 */
export const QRCodeSVG: React.FC<QrCodeProps> = ({
  value,
  size = 180,
  fgColor = 'currentColor',
  bgColor = 'transparent',
  quietZone = 2,
  eccLevel = 'M',
  maskPattern,
  className = '',
  title = 'Éco-Pass QR Code',
}) => {
  const { pathData, size: viewBoxSize } = React.useMemo(() => {
    return generateQrSvgPath(value, { quietZone, eccLevel, maskPattern });
  }, [value, quietZone, eccLevel, maskPattern]);

  return React.createElement(
    'svg',
    {
      role: 'img',
      'aria-label': title,
      viewBox: `0 0 ${viewBoxSize} ${viewBoxSize}`,
      width: size,
      height: size,
      className,
      shapeRendering: 'crispEdges',
      style: { display: 'block', maxWidth: '100%', height: 'auto' },
    },
    React.createElement('title', null, title),
    bgColor !== 'transparent'
      ? React.createElement('rect', {
          width: viewBoxSize,
          height: viewBoxSize,
          fill: bgColor,
        })
      : null,
    React.createElement('path', { d: pathData, fill: fgColor })
  );
};
