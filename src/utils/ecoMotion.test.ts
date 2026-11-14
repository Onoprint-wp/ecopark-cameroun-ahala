// ============================================================================
// AUTOMATED UNIT TESTS - ECO-MOTION ENGINE (src/utils/ecoMotion.test.ts)
// ============================================================================

import test from 'node:test';
import assert from 'node:assert/strict';
import { generateQrMatrix } from './qrCodeGenerator.ts';
import {
  computeOrganicClipOrigin,
  computeSpiralGerminationDelays,
  computeBotanicalGrowthStage,
  interpolateEaseOutExpo,
} from './ecoMotion.ts';

test('Eco-Motion Engine & Combined Animation Geometries', async (t) => {
  await t.test('computeOrganicClipOrigin covers farthest viewport corner accurately', () => {
    const metrics = computeOrganicClipOrigin(100, 50, 1280, 800);
    assert.strictEqual(metrics.originX, '100px');
    assert.strictEqual(metrics.originY, '50px');
    // Distance from (100, 50) to (1280, 800) = hypot(1180, 750) = 1398.17 -> ceil 1399
    assert.strictEqual(metrics.endRadiusPx, 1399);
  });

  await t.test('computeSpiralGerminationDelays anchors finder patterns early and spirals outward', () => {
    const matrix = generateQrMatrix('ECOPARK-AHALA:PASS:ECP-2026-8942', { eccLevel: 'M' });
    const seeds = computeSpiralGerminationDelays(matrix, 600);

    const totalDarkModules = matrix.reduce(
      (sum, row) => sum + row.filter(Boolean).length,
      0
    );
    assert.strictEqual(seeds.length, totalDarkModules, 'Every dark QR module must receive a seed');

    const finderSeeds = seeds.filter((s) => s.isFinder);
    const dataSeeds = seeds.filter((s) => !s.isFinder);
    assert.ok(finderSeeds.length > 50, 'Must classify 3 ISO finder patterns');
    assert.ok(dataSeeds.length > 50, 'Must classify central/spiral data modules');

    // Finder anchors must complete within <= 110ms for instant camera lock
    for (const fs of finderSeeds) {
      assert.ok(fs.delayMs >= 0 && fs.delayMs <= 110, `Finder delay ${fs.delayMs}ms out of bounds`);
    }

    // Center-adjacent modules must germinate earlier than outer-edge data modules
    const center = (matrix.length - 1) / 2;
    const innerData = dataSeeds.filter(
      (s) => Math.hypot(s.row - center, s.col - center) < 4
    );
    const outerData = dataSeeds.filter(
      (s) => Math.hypot(s.row - center, s.col - center) > center * 0.9
    );
    if (innerData.length > 0 && outerData.length > 0) {
      const avgInner = innerData.reduce((acc, s) => acc + s.delayMs, 0) / innerData.length;
      const avgOuter = outerData.reduce((acc, s) => acc + s.delayMs, 0) / outerData.length;
      assert.ok(avgInner < avgOuter, 'Inner spiral seeds must germinate before outer ring seeds');
    }
  });

  await t.test('computeBotanicalGrowthStage wilts at 0 kg and flourishes with low-carbon transport', () => {
    const soloCar = computeBotanicalGrowthStage(0);
    assert.strictEqual(soloCar.isWilted, true);
    assert.strictEqual(soloCar.activeBranches, 0);

    const carpool = computeBotanicalGrowthStage(6.4);
    assert.strictEqual(carpool.isWilted, false);
    assert.ok(carpool.activeBranches >= 2);

    const trainGroup = computeBotanicalGrowthStage(22.5);
    assert.strictEqual(trainGroup.isWilted, false);
    assert.strictEqual(trainGroup.stage, 1);
    assert.strictEqual(trainGroup.activeBranches, 4);
    assert.strictEqual(trainGroup.activeLeaves, 8);
  });

  await t.test('interpolateEaseOutExpo is monotonic and exact at endpoints', () => {
    assert.strictEqual(interpolateEaseOutExpo(10, 110, 0), 10);
    assert.strictEqual(interpolateEaseOutExpo(10, 110, 1), 110);
    const mid = interpolateEaseOutExpo(10, 110, 0.5);
    assert.ok(mid > 90 && mid < 110, 'EaseOutExpo reaches >80% of delta by halfway point');
  });
});
