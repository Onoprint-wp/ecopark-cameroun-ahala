// ============================================================================
// CRYPTOGRAPHIC AUTHENTICATION & RBAC UNIT TESTS (src/utils/ecoAuth.test.ts)
// PBKDF2-HMAC-SHA256, HMAC-SHA256 Session Signing, Rate Limiting & Loi 2010/012
// ============================================================================

import test from 'node:test';
import assert from 'node:assert/strict';
import {
  PBKDF2_ITERATIONS,
  derivePasswordHashHex,
  generateRandomSaltHex,
  constantTimeHexEqual,
  signSessionToken,
  verifySessionToken,
  validatePasswordStrength,
  registerClientAccount,
  authenticateWithPassword,
  restoreAuthenticatedSession,
  signOutActiveSession,
  updateAccountPassword,
  resetClientPasswordWithPhoneVerification,
  deleteAndAnonymizeClientAccount,
  isStaffRole,
  canCheckInPasses,
  canManageParkOperations,
  resetAuthVaultForTests,
  type SignedSessionClaims,
} from './ecoAuth.ts';

test('EcoPark Real Cryptographic Authentication & RBAC Engine', async (t) => {
  await t.test('PBKDF2-HMAC-SHA256 derives deterministic hashes and rejects wrong passwords', async () => {
    const salt = generateRandomSaltHex(16);
    assert.strictEqual(salt.length, 32, '16-byte salt must produce 32 hex chars');

    const hash1 = await derivePasswordHashHex('Cameroun#2026!', salt, PBKDF2_ITERATIONS);
    const hash2 = await derivePasswordHashHex('Cameroun#2026!', salt, PBKDF2_ITERATIONS);
    const wrongHash = await derivePasswordHashHex('Cameroun#2025!', salt, PBKDF2_ITERATIONS);

    assert.strictEqual(hash1.length, 64, '256-bit SHA-256 hash must produce 64 hex chars');
    assert.ok(constantTimeHexEqual(hash1, hash2), 'Identical password + salt must match');
    assert.ok(!constantTimeHexEqual(hash1, wrongHash), 'Different password must not match');

    const differentSalt = generateRandomSaltHex(16);
    const saltedDiffHash = await derivePasswordHashHex('Cameroun#2026!', differentSalt, PBKDF2_ITERATIONS);
    assert.ok(!constantTimeHexEqual(hash1, saltedDiffHash), 'Unique salt must produce unique hash');
  });

  await t.test('HMAC-SHA256 session tokens verify cleanly and reject payload tampering or expiration', async () => {
    const secretHex = generateRandomSaltHex(32);
    const nowSec = Math.floor(Date.now() / 1000);
    const claims: SignedSessionClaims = {
      sub: 'cli-test-01',
      email: 'visiteur@exemple.cm',
      fullName: 'Nadine Biya',
      phone: '+237690112233',
      role: 'client_connecte',
      provider: 'webcrypto_pbkdf2',
      iat: nowSec,
      exp: nowSec + 3600,
    };

    const token = await signSessionToken(claims, secretHex);
    const verified = await verifySessionToken(token, secretHex, nowSec + 10);
    assert.ok(verified !== null, 'Valid signed token must verify');
    assert.strictEqual(verified?.sub, 'cli-test-01');
    assert.strictEqual(verified?.role, 'client_connecte');

    // Tamper with payload to escalate role -> signature verification MUST reject!
    const [h, , s] = token.split('.');
    const forgedPayload = Buffer.from(
      JSON.stringify({ ...claims, role: 'direction' }),
      'utf8'
    ).toString('base64url');
    const forgedToken = `${h}.${forgedPayload}.${s}`;
    const forgedVerify = await verifySessionToken(forgedToken, secretHex, nowSec + 10);
    assert.strictEqual(forgedVerify, null, 'Privilege-escalation payload tampering must fail HMAC check');

    // Expired token -> MUST reject!
    const expiredVerify = await verifySessionToken(token, secretHex, nowSec + 7200);
    assert.strictEqual(expiredVerify, null, 'Expired session token must be rejected');
  });

  await t.test('Client registration, duplicate prevention, @ecopark-yaounde.com domain protection & session lifecycle', async () => {
    resetAuthVaultForTests();

    // Weak password rejected
    assert.strictEqual(validatePasswordStrength('short1').valid, false);
    const weakRes = await registerClientAccount({
      fullName: 'Marie Atangana',
      email: 'marie@exemple.cm',
      phone: '+237 699 12 34 56',
      password: 'weak',
    });
    assert.strictEqual(weakRes.ok, false);

    // Staff domain spoofing rejected on public registration
    const spoofRes = await registerClientAccount({
      fullName: 'Intrus',
      email: 'hacker@ecopark-yaounde.com',
      phone: '+237 699 12 34 56',
      password: 'StrongPassword#2026',
    });
    assert.strictEqual(spoofRes.ok, false);

    // Valid client registration
    const regRes = await registerClientAccount({
      fullName: 'Marie Atangana',
      email: 'Marie@Exemple.cm',
      phone: '+237 699 12 34 56',
      password: 'AhalaClient#2026',
    });
    assert.strictEqual(regRes.ok, true);
    assert.strictEqual(regRes.user?.role, 'client_connecte');
    assert.strictEqual(regRes.user?.email, 'marie@exemple.cm');

    // Duplicate email rejected
    const dupRes = await registerClientAccount({
      fullName: 'Autre Marie',
      email: 'marie@exemple.cm',
      phone: '+237 677 00 00 00',
      password: 'AhalaClient#2026',
    });
    assert.strictEqual(dupRes.ok, false);

    // Session restores cleanly
    const restored = await restoreAuthenticatedSession();
    assert.strictEqual(restored?.email, 'marie@exemple.cm');

    // Sign out clears session
    await signOutActiveSession();
    assert.strictEqual(await restoreAuthenticatedSession(), null);

    // Sign back in with password
    const loginRes = await authenticateWithPassword('MARIE@exemple.cm', 'AhalaClient#2026');
    assert.strictEqual(loginRes.ok, true);
    assert.strictEqual(loginRes.user?.fullName, 'Marie Atangana');

    // Password change + old password invalidated
    const pwdUpdate = await updateAccountPassword({
      userId: loginRes.user!.id,
      currentPassword: 'AhalaClient#2026',
      newPassword: 'NouveauMdp#2027!',
    });
    assert.strictEqual(pwdUpdate.ok, true);
    const oldLogin = await authenticateWithPassword('marie@exemple.cm', 'AhalaClient#2026');
    assert.strictEqual(oldLogin.ok, false);
    const newLogin = await authenticateWithPassword('marie@exemple.cm', 'NouveauMdp#2027!');
    assert.strictEqual(newLogin.ok, true);

    // Verified phone recovery
    const recoverOk = await resetClientPasswordWithPhoneVerification({
      email: 'marie@exemple.cm',
      phone: '699123456',
      newPassword: 'Recovered#2028!',
    });
    assert.strictEqual(recoverOk.ok, true);

    // Loi n° 2010/012 right to erasure (account deletion & anonymization)
    const delRes = await deleteAndAnonymizeClientAccount({
      userId: newLogin.user!.id,
      password: 'Recovered#2028!',
    });
    assert.strictEqual(delRes.ok, true);
    assert.strictEqual(await restoreAuthenticatedSession(), null);
    const afterDeleteLogin = await authenticateWithPassword('marie@exemple.cm', 'Recovered#2028!');
    assert.strictEqual(afterDeleteLogin.ok, false);
  });

  await t.test('Provisioned Staff accounts authenticate via PBKDF2-SHA256, enforce RBAC & rate-limit brute force', async () => {
    resetAuthVaultForTests();

    // Direction Générale login
    const dirLogin = await authenticateWithPassword(
      'direction@ecopark-yaounde.com',
      'EcoPark-Dir#2026!'
    );
    assert.strictEqual(dirLogin.ok, true);
    assert.strictEqual(dirLogin.user?.role, 'direction');
    assert.strictEqual(isStaffRole(dirLogin.user?.role), true);
    assert.strictEqual(canManageParkOperations(dirLogin.user?.role), true);
    assert.strictEqual(canCheckInPasses(dirLogin.user?.role), true);

    // Agent Contrôle QR login (can check in, cannot close trails / alter daily quota)
    const ctlLogin = await authenticateWithPassword(
      'controle@ecopark-yaounde.com',
      'EcoPark-Qr#2026!'
    );
    assert.strictEqual(ctlLogin.ok, true);
    assert.strictEqual(ctlLogin.user?.role, 'agent_controle');
    assert.strictEqual(canCheckInPasses(ctlLogin.user?.role), true);
    assert.strictEqual(canManageParkOperations(ctlLogin.user?.role), false);

    // Comptable SYSCOHADA login (read-only audit: cannot check in or alter ops)
    const cptLogin = await authenticateWithPassword(
      'comptabilite@ecopark-yaounde.com',
      'EcoPark-Cpt#2026!'
    );
    assert.strictEqual(cptLogin.ok, true);
    assert.strictEqual(cptLogin.user?.role, 'comptable');
    assert.strictEqual(isStaffRole(cptLogin.user?.role), true);
    assert.strictEqual(canCheckInPasses(cptLogin.user?.role), false);
    assert.strictEqual(canManageParkOperations(cptLogin.user?.role), false);

    // Brute-force lockout after 5 wrong attempts
    for (let i = 1; i <= 5; i++) {
      const bad = await authenticateWithPassword('exploitation@ecopark-yaounde.com', `WrongPwd#${i}`);
      assert.strictEqual(bad.ok, false);
      if (i === 5) {
        assert.ok((bad.lockoutRemainingSec || 0) > 0, '5th failure must trigger lockout window');
      }
    }

    // Even valid password must be blocked while lockout window is active
    const blockedValid = await authenticateWithPassword(
      'exploitation@ecopark-yaounde.com',
      'EcoPark-Exp#2026!'
    );
    assert.strictEqual(blockedValid.ok, false);
    assert.ok((blockedValid.lockoutRemainingSec || 0) > 0);
  });
});
