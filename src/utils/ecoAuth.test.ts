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
  canAuditFinancials,
  canManageRbacGovernance,
  getRoleDisplayLabel,
  listProvisionedStaffDirectory,
  getDeletionComplianceLog,
  resetAuthVaultForTests,
  type SignedSessionClaims,
} from './ecoAuth.ts';
import type { EcoParkRole } from '../types/ecosystem.ts';

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

    // Compliance log records anonymized trace without PII
    const logs = getDeletionComplianceLog();
    assert.strictEqual(logs.length, 1);
    assert.strictEqual(logs[0].status, 'PROCESSED_ANONYMIZED');
    assert.ok(logs[0].requester_reference.length > 0);
    assert.ok(!JSON.stringify(logs).toLowerCase().includes('marie'));
  });

  await t.test('All 8 EcoParkRole profiles & all 6 Provisioned Staff accounts enforce exact RBAC permissions & brute-force lockout', async () => {
    resetAuthVaultForTests();

    // 1. Complete 8-role RBAC permission matrix check
    const expectedRbacMatrix: Array<{
      role: EcoParkRole;
      staff: boolean;
      checkIn: boolean;
      ops: boolean;
      compta: boolean;
      rbacGov: boolean;
    }> = [
      { role: 'visiteur_anonyme', staff: false, checkIn: false, ops: false, compta: false, rbacGov: false },
      { role: 'client_connecte', staff: false, checkIn: false, ops: false, compta: false, rbacGov: false },
      { role: 'agent_guichet', staff: true, checkIn: true, ops: false, compta: false, rbacGov: false },
      { role: 'agent_controle', staff: true, checkIn: true, ops: false, compta: false, rbacGov: false },
      { role: 'comptable', staff: true, checkIn: false, ops: false, compta: true, rbacGov: false },
      { role: 'responsable_exploitation', staff: true, checkIn: true, ops: true, compta: false, rbacGov: false },
      { role: 'direction', staff: true, checkIn: true, ops: true, compta: true, rbacGov: true },
      { role: 'administrateur_plateforme', staff: true, checkIn: true, ops: true, compta: true, rbacGov: true },
    ];

    for (const row of expectedRbacMatrix) {
      assert.strictEqual(isStaffRole(row.role), row.staff, `${row.role} isStaffRole`);
      assert.strictEqual(canCheckInPasses(row.role), row.checkIn, `${row.role} canCheckInPasses`);
      assert.strictEqual(canManageParkOperations(row.role), row.ops, `${row.role} canManageParkOperations`);
      assert.strictEqual(canAuditFinancials(row.role), row.compta, `${row.role} canAuditFinancials`);
      assert.strictEqual(canManageRbacGovernance(row.role), row.rbacGov, `${row.role} canManageRbacGovernance`);
      assert.ok(getRoleDisplayLabel(row.role).length > 0, `${row.role} display label non-empty`);
    }

    // 2. Sanitized staff directory exposes all 6 provisioned staff accounts and 0 secrets
    const directory = listProvisionedStaffDirectory();
    assert.strictEqual(directory.length, 6, 'All 6 internal staff roles must be provisioned');
    for (const entry of directory) {
      const rawEntry = entry as unknown as Record<string, unknown>;
      assert.strictEqual('saltHex' in rawEntry, false);
      assert.strictEqual('hashHex' in rawEntry, false);
    }

    // 3. Authenticate all 6 provisioned staff accounts via real PBKDF2-HMAC-SHA256
    const staffCredentials: Array<{ email: string; pwd: string; role: EcoParkRole; matricule: string }> = [
      { email: 'direction@ecopark-yaounde.com', pwd: 'EcoPark-Dir#2026!', role: 'direction', matricule: 'MAT-DIR-01' },
      { email: 'exploitation@ecopark-yaounde.com', pwd: 'EcoPark-Exp#2026!', role: 'responsable_exploitation', matricule: 'MAT-EXP-01' },
      { email: 'controle@ecopark-yaounde.com', pwd: 'EcoPark-Qr#2026!', role: 'agent_controle', matricule: 'MAT-CTL-02' },
      { email: 'guichet@ecopark-yaounde.com', pwd: 'EcoPark-Gui#2026!', role: 'agent_guichet', matricule: 'MAT-GUI-04' },
      { email: 'comptabilite@ecopark-yaounde.com', pwd: 'EcoPark-Cpt#2026!', role: 'comptable', matricule: 'MAT-CPT-03' },
      { email: 'admin@ecopark-yaounde.com', pwd: 'EcoPark-Adm#2026!', role: 'administrateur_plateforme', matricule: 'MAT-ADM-00' },
    ];

    for (const cred of staffCredentials) {
      const authRes = await authenticateWithPassword(cred.email, cred.pwd);
      assert.strictEqual(authRes.ok, true, `Staff login must succeed for ${cred.email}`);
      assert.strictEqual(authRes.user?.role, cred.role);
      assert.strictEqual(authRes.user?.matricule, cred.matricule);
      await signOutActiveSession();
    }

    // 4. Brute-force lockout after 5 wrong attempts
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
