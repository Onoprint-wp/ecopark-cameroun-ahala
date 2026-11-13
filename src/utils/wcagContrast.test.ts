// ============================================================================
// WCAG CONTRAST ENGINE UNIT TESTS (src/utils/wcagContrast.test.ts)
// Feature F30: Verification of W3C relative luminance, ratios & daltonism
// ============================================================================

import { test, describe } from 'node:test';
import assert from 'node:assert/strict';
import {
  hexToRgb,
  rgbToHex,
  normalizeHex,
  getRelativeLuminance,
  getContrastRatio,
  getWCAGCompliance,
  simulateColorBlindness,
  auditColorPairDaltonism,
} from './wcagContrast.ts';

describe('WCAG 2.1 Contrast Engine & W3C Relative Luminance', () => {
  test('hexToRgb and rgbToHex handle standard and short hex codes', () => {
    assert.deepEqual(hexToRgb('#FFFFFF'), { r: 255, g: 255, b: 255 });
    assert.deepEqual(hexToRgb('#000000'), { r: 0, g: 0, b: 0 });
    assert.deepEqual(hexToRgb('#FFF'), { r: 255, g: 255, b: 255 });
    assert.deepEqual(hexToRgb('1B4332'), { r: 27, g: 67, b: 50 });
    assert.equal(rgbToHex({ r: 27, g: 67, b: 50 }), '#1B4332');
    assert.equal(normalizeHex('#fff'), '#FFFFFF');
    assert.equal(normalizeHex('1b4332'), '#1B4332');
  });

  test('W3C Relative Luminance calculation bounds', () => {
    const lumBlack = getRelativeLuminance({ r: 0, g: 0, b: 0 });
    const lumWhite = getRelativeLuminance({ r: 255, g: 255, b: 255 });
    assert.equal(lumBlack, 0);
    assert.equal(Math.round(lumWhite * 100) / 100, 1);
  });

  test('Contrast ratio bounds: Black on White equals 21:1, Identical equals 1:1', () => {
    const bwRatio = getContrastRatio('#000000', '#FFFFFF');
    const sameRatio = getContrastRatio('#52B788', '#52B788');
    assert.equal(bwRatio, 21);
    assert.equal(sameRatio, 1);
  });

  test('Authoritative ECO-PARK reference color pairs match COLOR-SYSTEM.md specification', () => {
    // 1. Bark on Mist -> Expected 14.07 : 1 (AAA)
    const barkOnMist = getContrastRatio('#1F2421', '#E9F5ED');
    assert.equal(barkOnMist, 14.07);
    const comp1 = getWCAGCompliance(barkOnMist);
    assert.equal(comp1.aaNormalText, true);
    assert.equal(comp1.aaaNormalText, true);
    assert.equal(comp1.overallLevel, 'AAA');

    // 2. White on Deep Forest -> Expected 11.08 : 1 (AAA)
    const whiteOnForest = getContrastRatio('#FFFFFF', '#1B4332');
    assert.equal(whiteOnForest, 11.08);
    const comp2 = getWCAGCompliance(whiteOnForest);
    assert.equal(comp2.aaNormalText, true);
    assert.equal(comp2.aaaNormalText, true);
    assert.equal(comp2.overallLevel, 'AAA');

    // 3. Mist on Deep Forest -> Expected 9.89 : 1 (AAA)
    const mistOnForest = getContrastRatio('#E9F5ED', '#1B4332');
    assert.equal(mistOnForest, 9.89);
    const comp3 = getWCAGCompliance(mistOnForest);
    assert.equal(comp3.aaNormalText, true);
    assert.equal(comp3.aaaNormalText, true);
    assert.equal(comp3.overallLevel, 'AAA');

    // 4. Bark on Earth -> Expected 6.97 : 1 (AA Normal, AAA Large)
    const barkOnEarth = getContrastRatio('#1F2421', '#D4A373');
    assert.equal(barkOnEarth, 6.97);
    const comp4 = getWCAGCompliance(barkOnEarth);
    assert.equal(comp4.aaNormalText, true);
    assert.equal(comp4.aaaNormalText, false);
    assert.equal(comp4.aaaLargeText, true);
    assert.equal(comp4.overallLevel, 'AA');

    // 5. Bark on Leaf -> Expected 6.37 : 1 (AA Normal, AAA Large)
    const barkOnLeaf = getContrastRatio('#1F2421', '#52B788');
    assert.equal(barkOnLeaf, 6.37);
    const comp5 = getWCAGCompliance(barkOnLeaf);
    assert.equal(comp5.aaNormalText, true);
    assert.equal(comp5.aaaNormalText, false);
    assert.equal(comp5.aaaLargeText, true);
    assert.equal(comp5.overallLevel, 'AA');
  });

  test('WCAG 2.1 threshold classification', () => {
    // Exactly 7.0 -> AAA
    const cAaa = getWCAGCompliance(7.0);
    assert.equal(cAaa.aaaNormalText, true);
    assert.equal(cAaa.overallLevel, 'AAA');

    // 4.5 to 6.99 -> AA
    const cAa = getWCAGCompliance(4.5);
    assert.equal(cAa.aaNormalText, true);
    assert.equal(cAa.aaaNormalText, false);
    assert.equal(cAa.overallLevel, 'AA');

    // 3.0 to 4.49 -> AA Large
    const cLarge = getWCAGCompliance(3.2);
    assert.equal(cLarge.aaNormalText, false);
    assert.equal(cLarge.aaLargeText, true);
    assert.equal(cLarge.uiComponent, true);
    assert.equal(cLarge.overallLevel, 'AA Large');

    // < 3.0 -> Échec
    const cFail = getWCAGCompliance(2.5);
    assert.equal(cFail.aaNormalText, false);
    assert.equal(cFail.aaLargeText, false);
    assert.equal(cFail.uiComponent, false);
    assert.equal(cFail.overallLevel, 'Échec');
  });

  test('Color blindness simulation outputs valid hex and consistent contrast', () => {
    const modes = ['deuteranopia', 'protanopia', 'tritanopia', 'achromatopsia'] as const;

    for (const mode of modes) {
      const sim = simulateColorBlindness('#52B788', mode);
      assert.match(sim, /^#[0-9A-F]{6}$/i);
    }

    const audit = auditColorPairDaltonism('#1F2421', '#E9F5ED');
    assert.equal(audit.length, 5);
    // All modes for high-contrast Bark on Mist must pass AA
    for (const res of audit) {
      assert.ok(res.contrastRatio > 7.0, `Expected > 7.0 for ${res.mode}, got ${res.contrastRatio}`);
      assert.equal(res.aaNormalPass, true);
      assert.equal(res.uiPass, true);
    }
  });
});
