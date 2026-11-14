// ============================================================================
// AUTOMATED UNIT TESTS - QR CODE GENERATOR (src/utils/qrCodeGenerator.test.ts)
// ISO/IEC 18004 Matrix Verification & SVG Path Integrity
// ============================================================================

import test from 'node:test';
import assert from 'node:assert/strict';
import {
  generateQrMatrix,
  generateQrSvgPath,
  generateQrSvgString,
} from './qrCodeGenerator.ts';

test('Zero-Dependency Pure TypeScript SVG QR Code Generator', async (t) => {
  await t.test('Matrix dimensions match ISO QR specifications for versions 1, 2, and 3', () => {
    // Short string fits in Version 1 (21x21)
    const m1 = generateQrMatrix('ECO-PARK', { eccLevel: 'L' });
    assert.strictEqual(m1.length, 21, 'Version 1 matrix height must be 21');
    assert.strictEqual(m1[0].length, 21, 'Version 1 matrix width must be 21');

    // Standard Eco-Pass payload fits in Version 2 (25x25) or Version 3 (29x29)
    const passPayload = 'ECOPARK:PASS:ECO-2026-8942-XF:DATE=2026-05-18:SLOT=09h30:GUESTS=2:MODE=train';
    const mPass = generateQrMatrix(passPayload, { eccLevel: 'M' });
    assert.ok(mPass.length >= 25, 'Standard pass payload must generate at least 25x25 matrix');
    assert.strictEqual(mPass.length, mPass[0].length, 'Matrix must be strictly square');
  });

  await t.test('Finder patterns are properly positioned at top-left, top-right, bottom-left', () => {
    const matrix = generateQrMatrix('TEST-FINDER', { eccLevel: 'M' });
    const size = matrix.length;

    // Verify 7x7 outer border of top-left finder pattern
    for (let i = 0; i < 7; i++) {
      assert.strictEqual(matrix[0][i], true, `Top-left finder top edge at col ${i} must be black`);
      assert.strictEqual(matrix[6][i], true, `Top-left finder bottom edge at col ${i} must be black`);
      assert.strictEqual(matrix[i][0], true, `Top-left finder left edge at row ${i} must be black`);
      assert.strictEqual(matrix[i][6], true, `Top-left finder right edge at row ${i} must be black`);
    }

    // Center 3x3 core of top-left finder must be black
    for (let r = 2; r <= 4; r++) {
      for (let c = 2; c <= 4; c++) {
        assert.strictEqual(matrix[r][c], true, `Top-left finder core at (${r},${c}) must be black`);
      }
    }

    // Top-right finder outer border
    for (let i = 0; i < 7; i++) {
      assert.strictEqual(matrix[0][size - 7 + i], true, `Top-right finder top edge at col ${i}`);
      assert.strictEqual(matrix[6][size - 7 + i], true, `Top-right finder bottom edge at col ${i}`);
    }

    // Bottom-left finder outer border
    for (let i = 0; i < 7; i++) {
      assert.strictEqual(matrix[size - 7 + i][0], true, `Bottom-left finder left edge at row ${i}`);
      assert.strictEqual(matrix[size - 7 + i][6], true, `Bottom-left finder right edge at row ${i}`);
    }
  });

  await t.test('Timing patterns exist on row 6 and column 6 with alternating modules', () => {
    const matrix = generateQrMatrix('TEST-TIMING', { eccLevel: 'L' });
    const size = matrix.length;

    // Check horizontal timing pattern between finders (col 8 to size - 9)
    for (let col = 8; col <= size - 9; col++) {
      const expected = col % 2 === 0;
      assert.strictEqual(matrix[6][col], expected, `Horizontal timing pattern at col ${col} should alternate`);
    }

    // Check vertical timing pattern between finders (row 8 to size - 9)
    for (let row = 8; row <= size - 9; row++) {
      const expected = row % 2 === 0;
      assert.strictEqual(matrix[row][6], expected, `Vertical timing pattern at row ${row} should alternate`);
    }
  });

  await t.test('SVG path generation calculates quiet zone and valid SVG path syntax', () => {
    const payload = 'ECOPARK:PASS:ECO-2026-0001-AA';
    const quietZone = 3;
    const { pathData, size, quietZone: qz } = generateQrSvgPath(payload, { quietZone, eccLevel: 'M' });

    assert.strictEqual(qz, 3, 'Quiet zone must equal specified 3 modules');
    assert.ok(size > 21 + 2 * quietZone, 'Total SVG dimension must include matrix plus quiet zone on both sides');
    assert.ok(pathData.length > 50, 'Path data must not be empty');
    assert.ok(pathData.startsWith('M'), 'Path data must start with M command');
    assert.ok(pathData.includes('h1v1h-1z'), 'Path data must contain module rect commands (h1v1h-1z)');
  });

  await t.test('SVG string generation outputs valid XML SVG with crispEdges and correct colors', () => {
    const payload = 'ECO-PARK-TEST-SVG';
    const svgString = generateQrSvgString(payload, {
      fgColor: '#1B4332',
      bgColor: '#E9F5ED',
      pixelSize: 200,
    });

    assert.ok(svgString.includes('<svg xmlns="http://www.w3.org/2000/svg"'), 'Must contain SVG opening tag');
    assert.ok(svgString.includes('shape-rendering="crispEdges"'), 'Must include shape-rendering crispEdges');
    assert.ok(svgString.includes('fill="#1B4332"'), 'Must render foreground with specified Forest color');
    assert.ok(svgString.includes('fill="#E9F5ED"'), 'Must render background rect with specified Mist color');
    assert.ok(svgString.includes('width="200" height="200"'), 'Must set pixel dimensions');
  });
});
