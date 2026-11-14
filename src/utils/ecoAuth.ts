// ============================================================================
// ECOPARK CAMEROUN (YAOUNDÉ, AHALA) - REAL DUAL-ENGINE AUTHENTICATION
// (src/utils/ecoAuth.ts)
// 1. Cloud Engine: Native Supabase GoTrue REST (/auth/v1/*) + RPC get_my_profile()
// 2. Autonomous Engine: Web Crypto PBKDF2-HMAC-SHA256 (120k iter.) + HMAC-SHA256
//    signed session tokens, constant-time byte verification & rate limiting.
// Zero cleartext passwords. Zero mock bypass.
// ============================================================================

import type {
  AssignedPole,
  AuthenticatedUser,
  EcoParkRole,
} from '../types/ecosystem.ts';

export const AUTH_STORAGE_KEYS = {
  ACCOUNTS: 'eco_park_ahala_v2_auth_accounts',
  SESSION_TOKEN: 'eco_park_ahala_v2_auth_session_token',
  SUPABASE_SESSION: 'eco_park_ahala_v2_supabase_session',
  SIGNING_SECRET: 'eco_park_ahala_v2_auth_hmac_key',
  LOGIN_ATTEMPTS: 'eco_park_ahala_v2_auth_attempts',
  DELETION_LOG: 'eco_park_ahala_v2_account_deletions',
} as const;

export const PBKDF2_ITERATIONS = 120_000;
const SESSION_TTL_CLIENT_SEC = 7 * 24 * 3600; // 7 days
const SESSION_TTL_STAFF_SEC = 12 * 3600;      // 12 hours
const MAX_FAILED_ATTEMPTS = 5;
const LOCKOUT_WINDOW_MS = 2 * 60 * 1000;      // 2 minutes lockout after 5 failures

export interface StoredVaultAccount {
  id: string;
  email: string;
  fullName: string;
  phone: string;
  role: EcoParkRole;
  matricule?: string;
  assignedPole?: AssignedPole;
  postLabel?: string;
  saltHex: string;
  hashHex: string;
  iterations: number;
  isActive: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface SignedSessionClaims {
  sub: string;
  email: string;
  fullName: string;
  phone: string;
  role: EcoParkRole;
  matricule?: string;
  assignedPole?: AssignedPole;
  postLabel?: string;
  provider: 'supabase' | 'webcrypto_pbkdf2';
  iat: number;
  exp: number;
}

export interface AuthResult {
  ok: boolean;
  user?: AuthenticatedUser;
  token?: string;
  error?: string;
  lockoutRemainingSec?: number;
}

export interface PasswordValidationResult {
  valid: boolean;
  score: 0 | 1 | 2 | 3 | 4;
  errors: string[];
}

// Pre-provisioned Staff Accounts (Salted PBKDF2-HMAC-SHA256, 120,000 iterations - NO cleartext)
const PROVISIONED_STAFF_ACCOUNTS: StoredVaultAccount[] = [
  {
    id: 'staff-dir-001',
    email: 'direction@ecopark-yaounde.com',
    fullName: 'Dr Christophe FOE NDI',
    phone: '+237 672 56 45 98',
    role: 'direction',
    matricule: 'MAT-DIR-01',
    assignedPole: 'DIRECTION_GENERALE',
    postLabel: 'Direction Générale • MPECK MULTI-SERVICES',
    saltHex: 'e76e342ed22b612538c2154d47cf5fd1',
    hashHex: '8581799f53d4827eb4616d7065a6276d5e83da2983c806db9ce2a94e7cc7dae2',
    iterations: PBKDF2_ITERATIONS,
    isActive: true,
    createdAt: '2026-10-26T08:00:00.000Z',
    updatedAt: '2026-10-26T08:00:00.000Z',
  },
  {
    id: 'staff-exp-001',
    email: 'exploitation@ecopark-yaounde.com',
    fullName: "Thomas D. • Chef d'Exploitation",
    phone: '+237 694 60 14 49',
    role: 'responsable_exploitation',
    matricule: 'MAT-EXP-01',
    assignedPole: 'CONTROLE_QR',
    postLabel: "Chef d'Exploitation Ahala Barrière",
    saltHex: '1fb2885499db4afb4afa54dd704ee9fa',
    hashHex: '8b01c0913e9e62bc927c5d4ec33af78db8726cda0698ed9a0b9a85f82979f08b',
    iterations: PBKDF2_ITERATIONS,
    isActive: true,
    createdAt: '2026-10-26T08:00:00.000Z',
    updatedAt: '2026-10-26T08:00:00.000Z',
  },
  {
    id: 'staff-ctl-002',
    email: 'controle@ecopark-yaounde.com',
    fullName: 'Poste Contrôle QR • Entrée RN3',
    phone: '+237 697 13 62 03',
    role: 'agent_controle',
    matricule: 'MAT-CTL-02',
    assignedPole: 'CONTROLE_QR',
    postLabel: 'Contrôle Pass QR & Sécurité Sentiers',
    saltHex: '345544c92d9c6ce02390a3d6b1060c5d',
    hashHex: '8274d86f167bcb34290732adf1d2b3bc201c88593d8cdfd602cf44c891d299d1',
    iterations: PBKDF2_ITERATIONS,
    isActive: true,
    createdAt: '2026-10-26T08:00:00.000Z',
    updatedAt: '2026-10-26T08:00:00.000Z',
  },
  {
    id: 'staff-cpt-003',
    email: 'comptabilite@ecopark-yaounde.com',
    fullName: 'Service Comptabilité SYSCOHADA',
    phone: '+237 672 56 45 98',
    role: 'comptable',
    matricule: 'MAT-CPT-03',
    assignedPole: 'FINANCE_COMPTA',
    postLabel: 'Audit & Comptabilité Analytique (6 Pôles)',
    saltHex: 'ce2e7822be0fbc8c1c2f20734a0c0940',
    hashHex: '3b3495e07ee141cb7c8af804d1c3b4c076997c670b7fd32da93dd0ad5cfe41ff',
    iterations: PBKDF2_ITERATIONS,
    isActive: true,
    createdAt: '2026-10-26T08:00:00.000Z',
    updatedAt: '2026-10-26T08:00:00.000Z',
  },
];

// ----------------------------------------------------------------------------
// Role & Permission Governance Helpers (Aligned with Supabase RLS Migrations)
// ----------------------------------------------------------------------------

export function isStaffRole(role?: EcoParkRole | null): boolean {
  if (!role) return false;
  return (
    role === 'agent_guichet' ||
    role === 'agent_controle' ||
    role === 'comptable' ||
    role === 'responsable_exploitation' ||
    role === 'direction' ||
    role === 'administrateur_plateforme'
  );
}

export function canCheckInPasses(role?: EcoParkRole | null): boolean {
  if (!role) return false;
  return (
    role === 'agent_guichet' ||
    role === 'agent_controle' ||
    role === 'responsable_exploitation' ||
    role === 'direction' ||
    role === 'administrateur_plateforme'
  );
}

export function canManageParkOperations(role?: EcoParkRole | null): boolean {
  if (!role) return false;
  return (
    role === 'responsable_exploitation' ||
    role === 'direction' ||
    role === 'administrateur_plateforme'
  );
}

export function getRoleDisplayLabel(role?: EcoParkRole | null): string {
  switch (role) {
    case 'direction':
      return 'Direction Générale';
    case 'administrateur_plateforme':
      return 'Administrateur Plateforme';
    case 'responsable_exploitation':
      return "Chef d'Exploitation";
    case 'agent_controle':
      return 'Contrôle QR & Éco-Garde';
    case 'agent_guichet':
      return 'Agent Guichet RN3';
    case 'comptable':
      return 'Comptable SYSCOHADA';
    case 'client_connecte':
      return 'Espace Cliente / Visiteur';
    default:
      return 'Visiteur';
  }
}

// ----------------------------------------------------------------------------
// Password Strength & Input Validation
// ----------------------------------------------------------------------------

export function validatePasswordStrength(password: string): PasswordValidationResult {
  const errors: string[] = [];
  let score = 0;

  if (password.length >= 8) score += 1;
  else errors.push('Au moins 8 caractères requis.');

  if (/[A-Z]/.test(password) && /[a-z]/.test(password)) score += 1;
  else errors.push('Inclure au moins une majuscule et une minuscule.');

  if (/\d/.test(password)) score += 1;
  else errors.push('Inclure au moins un chiffre.');

  if (/[^A-Za-z0-9]/.test(password) || password.length >= 12) score += 1;

  return {
    valid: errors.length === 0,
    score: Math.min(4, score) as 0 | 1 | 2 | 3 | 4,
    errors,
  };
}

export function normalizeEmail(email: string): string {
  return email.trim().toLowerCase();
}

export function normalizePhoneDigits(phone: string): string {
  return phone.replace(/[^\d+]/g, '');
}

// ----------------------------------------------------------------------------
// Low-Level Web Crypto Primitives (Browser + Node 22 globalThis.crypto.subtle)
// ----------------------------------------------------------------------------

function bytesToHex(bytes: Uint8Array): string {
  return Array.from(bytes)
    .map((b) => b.toString(16).padStart(2, '0'))
    .join('');
}

function hexToBytes(hex: string): Uint8Array {
  const clean = hex.trim();
  const out = new Uint8Array(clean.length / 2);
  for (let i = 0; i < out.length; i++) {
    out[i] = parseInt(clean.slice(i * 2, i * 2 + 2), 16);
  }
  return out;
}

function encodeBase64Url(input: string | Uint8Array): string {
  const bytes = typeof input === 'string' ? new TextEncoder().encode(input) : input;
  let binary = '';
  for (let i = 0; i < bytes.length; i++) {
    binary += String.fromCharCode(bytes[i]);
  }
  return btoa(binary).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

function decodeBase64UrlToBytes(b64url: string): Uint8Array {
  const padded = b64url.replace(/-/g, '+').replace(/_/g, '/') + '==='.slice((b64url.length + 3) % 4);
  const binary = atob(padded);
  const out = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) {
    out[i] = binary.charCodeAt(i);
  }
  return out;
}

export function constantTimeHexEqual(hexA: string, hexB: string): boolean {
  if (hexA.length !== hexB.length || hexA.length === 0) return false;
  const a = hexToBytes(hexA);
  const b = hexToBytes(hexB);
  if (a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i++) {
    diff |= a[i] ^ b[i];
  }
  return diff === 0;
}

export async function derivePasswordHashHex(
  password: string,
  saltHex: string,
  iterations: number = PBKDF2_ITERATIONS
): Promise<string> {
  const enc = new TextEncoder();
  const keyMaterial = await globalThis.crypto.subtle.importKey(
    'raw',
    enc.encode(password),
    'PBKDF2',
    false,
    ['deriveBits']
  );
  const saltBytes = hexToBytes(saltHex);
  const derivedBits = await globalThis.crypto.subtle.deriveBits(
    {
      name: 'PBKDF2',
      salt: saltBytes as BufferSource,
      iterations,
      hash: 'SHA-256',
    },
    keyMaterial,
    256
  );
  return bytesToHex(new Uint8Array(derivedBits));
}

export function generateRandomSaltHex(byteLength: number = 16): string {
  const buf = new Uint8Array(byteLength);
  globalThis.crypto.getRandomValues(buf);
  return bytesToHex(buf);
}

export async function signSessionToken(
  claims: SignedSessionClaims,
  secretHex: string
): Promise<string> {
  const headerB64 = encodeBase64Url(JSON.stringify({ alg: 'HS256', typ: 'ECP-SESS' }));
  const payloadB64 = encodeBase64Url(JSON.stringify(claims));
  const signingInput = `${headerB64}.${payloadB64}`;

  const key = await globalThis.crypto.subtle.importKey(
    'raw',
    hexToBytes(secretHex) as BufferSource,
    { name: 'HMAC', hash: 'SHA-256' },
    false,
    ['sign']
  );

  const signature = await globalThis.crypto.subtle.sign(
    'HMAC',
    key,
    new TextEncoder().encode(signingInput)
  );
  return `${signingInput}.${encodeBase64Url(new Uint8Array(signature))}`;
}

export async function verifySessionToken(
  token: string,
  secretHex: string,
  nowSec: number = Math.floor(Date.now() / 1000)
): Promise<SignedSessionClaims | null> {
  try {
    const parts = token.split('.');
    if (parts.length !== 3) return null;
    const [headerB64, payloadB64, sigB64] = parts;
    const signingInput = `${headerB64}.${payloadB64}`;

    const key = await globalThis.crypto.subtle.importKey(
      'raw',
      hexToBytes(secretHex) as BufferSource,
      { name: 'HMAC', hash: 'SHA-256' },
      false,
      ['verify']
    );

    const sigBytes = decodeBase64UrlToBytes(sigB64);
    const valid = await globalThis.crypto.subtle.verify(
      'HMAC',
      key,
      sigBytes as BufferSource,
      new TextEncoder().encode(signingInput)
    );
    if (!valid) return null;

    const claimsText = new TextDecoder().decode(decodeBase64UrlToBytes(payloadB64));
    const claims = JSON.parse(claimsText) as SignedSessionClaims;
    if (!claims.sub || !claims.email || !claims.exp || claims.exp <= nowSec) {
      return null;
    }
    return claims;
  } catch {
    return null;
  }
}

// ----------------------------------------------------------------------------
// Storage Adapter (Browser localStorage + In-Memory Fallback for Node Tests)
// ----------------------------------------------------------------------------

const memoryStore = new Map<string, string>();

function readRawStorage(key: string): string | null {
  if (typeof window !== 'undefined' && window.localStorage) {
    try {
      return window.localStorage.getItem(key);
    } catch {
      return memoryStore.get(key) ?? null;
    }
  }
  return memoryStore.get(key) ?? null;
}

function writeRawStorage(key: string, value: string): void {
  memoryStore.set(key, value);
  if (typeof window !== 'undefined' && window.localStorage) {
    try {
      window.localStorage.setItem(key, value);
    } catch {
      // Ignore quota errors
    }
  }
}

function removeRawStorage(key: string): void {
  memoryStore.delete(key);
  if (typeof window !== 'undefined' && window.localStorage) {
    try {
      window.localStorage.removeItem(key);
    } catch {
      // Ignore storage errors
    }
  }
}

function getOrCreateSigningSecretHex(): string {
  const existing = readRawStorage(AUTH_STORAGE_KEYS.SIGNING_SECRET);
  if (existing && /^[0-9a-f]{64}$/i.test(existing)) {
    return existing;
  }
  const created = generateRandomSaltHex(32);
  writeRawStorage(AUTH_STORAGE_KEYS.SIGNING_SECRET, created);
  return created;
}

export function loadVaultAccounts(): StoredVaultAccount[] {
  const raw = readRawStorage(AUTH_STORAGE_KEYS.ACCOUNTS);
  let stored: StoredVaultAccount[] = [];
  if (raw) {
    try {
      const parsed = JSON.parse(raw);
      if (Array.isArray(parsed)) stored = parsed;
    } catch {
      stored = [];
    }
  }

  // Merge provisioned staff accounts if not already present (preserving any password updates)
  const byEmail = new Map<string, StoredVaultAccount>();
  for (const staff of PROVISIONED_STAFF_ACCOUNTS) {
    byEmail.set(normalizeEmail(staff.email), staff);
  }
  for (const acc of stored) {
    if (acc && typeof acc.email === 'string') {
      byEmail.set(normalizeEmail(acc.email), acc);
    }
  }
  return Array.from(byEmail.values());
}

function saveVaultAccounts(accounts: StoredVaultAccount[]): void {
  writeRawStorage(AUTH_STORAGE_KEYS.ACCOUNTS, JSON.stringify(accounts));
}

// ----------------------------------------------------------------------------
// Anti-Brute-Force Rate Limiter
// ----------------------------------------------------------------------------

interface LoginAttemptRecord {
  count: number;
  lockedUntilMs: number;
}

function getAttemptMap(): Record<string, LoginAttemptRecord> {
  const raw = readRawStorage(AUTH_STORAGE_KEYS.LOGIN_ATTEMPTS);
  if (!raw) return {};
  try {
    return JSON.parse(raw) as Record<string, LoginAttemptRecord>;
  } catch {
    return {};
  }
}

function checkRateLimit(emailKey: string, nowMs: number = Date.now()): number {
  const map = getAttemptMap();
  const entry = map[emailKey];
  if (!entry) return 0;
  if (entry.lockedUntilMs > nowMs) {
    return Math.ceil((entry.lockedUntilMs - nowMs) / 1000);
  }
  return 0;
}

function recordFailedAttempt(emailKey: string, nowMs: number = Date.now()): number {
  const map = getAttemptMap();
  const prev = map[emailKey] || { count: 0, lockedUntilMs: 0 };
  const nextCount = prev.lockedUntilMs > 0 && prev.lockedUntilMs <= nowMs ? 1 : prev.count + 1;
  const lockedUntilMs = nextCount >= MAX_FAILED_ATTEMPTS ? nowMs + LOCKOUT_WINDOW_MS : 0;
  map[emailKey] = { count: nextCount, lockedUntilMs };
  writeRawStorage(AUTH_STORAGE_KEYS.LOGIN_ATTEMPTS, JSON.stringify(map));
  return lockedUntilMs > nowMs ? Math.ceil((lockedUntilMs - nowMs) / 1000) : 0;
}

function clearFailedAttempts(emailKey: string): void {
  const map = getAttemptMap();
  if (map[emailKey]) {
    delete map[emailKey];
    writeRawStorage(AUTH_STORAGE_KEYS.LOGIN_ATTEMPTS, JSON.stringify(map));
  }
}

// ----------------------------------------------------------------------------
// Supabase Cloud Detection & GoTrue REST Client
// ----------------------------------------------------------------------------

function getSupabaseConfig(): { url: string; anonKey: string } | null {
  try {
    const metaEnv = (import.meta as unknown as { env?: Record<string, string | undefined> }).env;
    const url = metaEnv?.VITE_SUPABASE_URL?.trim() || '';
    const anonKey = metaEnv?.VITE_SUPABASE_ANON_KEY?.trim() || '';
    if (
      !url ||
      !anonKey ||
      url.includes('votre-projet.supabase.co') ||
      anonKey.includes('votre_cle_publique_anon_ici')
    ) {
      return null;
    }
    return { url: url.replace(/\/+$/, ''), anonKey };
  } catch {
    return null;
  }
}

export function isSupabaseCloudConfigured(): boolean {
  return getSupabaseConfig() !== null;
}

export function isDevEnvironment(): boolean {
  try {
    const metaEnv = (import.meta as unknown as { env?: { DEV?: boolean } }).env;
    return Boolean(metaEnv?.DEV);
  } catch {
    return false;
  }
}

async function resolveSupabaseUserProfile(
  cfg: { url: string; anonKey: string },
  accessToken: string,
  authUser: {
    id: string;
    email?: string;
    created_at?: string;
    user_metadata?: Record<string, unknown>;
  }
): Promise<AuthenticatedUser> {
  let role: EcoParkRole = 'client_connecte';
  let fullName = String(authUser.user_metadata?.full_name || authUser.email?.split('@')[0] || 'Cliente EcoPark');
  const phone = String(authUser.user_metadata?.phone || '');
  let matricule: string | undefined;
  let assignedPole: AssignedPole | undefined;
  let postLabel: string | undefined;

  try {
    const rpcRes = await fetch(`${cfg.url}/rest/v1/rpc/get_my_profile`, {
      method: 'POST',
      headers: {
        apikey: cfg.anonKey,
        Authorization: `Bearer ${accessToken}`,
        'Content-Type': 'application/json',
      },
      body: '{}',
    });
    if (rpcRes.ok) {
      const profile = (await rpcRes.json()) as Record<string, unknown>;
      if (typeof profile?.role === 'string' && profile.role !== 'visiteur_anonyme') {
        role = profile.role as EcoParkRole;
      }
      if (typeof profile?.full_name === 'string' && profile.full_name.trim()) {
        fullName = profile.full_name.trim();
      }
      if (typeof profile?.matricule === 'string') {
        matricule = profile.matricule;
      }
      if (typeof profile?.assigned_pole === 'string') {
        assignedPole = profile.assigned_pole as AssignedPole;
      }
      if (typeof profile?.post_label === 'string') {
        postLabel = profile.post_label;
      }
    }
  } catch {
    // Fallback to GoTrue user_metadata if RPC is unreachable
  }

  return {
    id: authUser.id,
    email: normalizeEmail(authUser.email || ''),
    fullName,
    phone,
    role,
    matricule,
    assignedPole,
    postLabel,
    provider: 'supabase',
    createdAt: authUser.created_at || new Date().toISOString(),
  };
}

// ----------------------------------------------------------------------------
// High-Level Real Authentication Operations
// ----------------------------------------------------------------------------

function vaultAccountToUser(acc: StoredVaultAccount): AuthenticatedUser {
  return {
    id: acc.id,
    email: acc.email,
    fullName: acc.fullName,
    phone: acc.phone,
    role: acc.role,
    matricule: acc.matricule,
    assignedPole: acc.assignedPole,
    postLabel: acc.postLabel,
    provider: 'webcrypto_pbkdf2',
    createdAt: acc.createdAt,
  };
}

async function issueLocalSignedSession(user: AuthenticatedUser): Promise<string> {
  const nowSec = Math.floor(Date.now() / 1000);
  const ttl = isStaffRole(user.role) ? SESSION_TTL_STAFF_SEC : SESSION_TTL_CLIENT_SEC;
  const claims: SignedSessionClaims = {
    sub: user.id,
    email: user.email,
    fullName: user.fullName,
    phone: user.phone,
    role: user.role,
    matricule: user.matricule,
    assignedPole: user.assignedPole,
    postLabel: user.postLabel,
    provider: user.provider,
    iat: nowSec,
    exp: nowSec + ttl,
  };
  const secretHex = getOrCreateSigningSecretHex();
  const token = await signSessionToken(claims, secretHex);
  writeRawStorage(AUTH_STORAGE_KEYS.SESSION_TOKEN, token);
  return token;
}

export async function registerClientAccount(input: {
  fullName: string;
  email: string;
  phone: string;
  password: string;
}): Promise<AuthResult> {
  const fullName = input.fullName.trim();
  const email = normalizeEmail(input.email);
  const phone = input.phone.trim();

  if (fullName.length < 2) {
    return { ok: false, error: 'Veuillez renseigner votre nom complet (au moins 2 caractères).' };
  }
  if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return { ok: false, error: 'Veuillez saisir une adresse email valide.' };
  }
  const phoneDigits = normalizePhoneDigits(phone);
  if (phoneDigits.length < 8) {
    return { ok: false, error: 'Veuillez saisir un numéro de téléphone valide (ex: +237 6XX XX XX XX).' };
  }

  const pwdCheck = validatePasswordStrength(input.password);
  if (!pwdCheck.valid) {
    return { ok: false, error: pwdCheck.errors.join(' ') };
  }

  // Reserve @ecopark-yaounde.com domain for verified staff provisioning
  if (email.endsWith('@ecopark-yaounde.com')) {
    return {
      ok: false,
      error: "Les adresses professionnelles @ecopark-yaounde.com relèvent exclusivement de la Direction Générale.",
    };
  }

  const supaCfg = getSupabaseConfig();
  if (supaCfg) {
    try {
      const res = await fetch(`${supaCfg.url}/auth/v1/signup`, {
        method: 'POST',
        headers: {
          apikey: supaCfg.anonKey,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email,
          password: input.password,
          data: {
            full_name: fullName,
            phone,
            role: 'client_connecte',
          },
        }),
      });
      const data = (await res.json()) as Record<string, unknown>;
      if (!res.ok) {
        const msg = String(data?.msg || data?.error_description || data?.message || "Échec de création du compte.");
        return { ok: false, error: msg };
      }

      const accessToken = typeof data.access_token === 'string' ? data.access_token : '';
      const rawUser = (data.user || data) as {
        id: string;
        email?: string;
        created_at?: string;
        user_metadata?: Record<string, unknown>;
      };

      if (!accessToken) {
        return {
          ok: false,
          error: 'Compte créé. Veuillez confirmer le lien reçu par email puis vous connecter.',
        };
      }

      writeRawStorage(
        AUTH_STORAGE_KEYS.SUPABASE_SESSION,
        JSON.stringify({
          access_token: accessToken,
          refresh_token: data.refresh_token,
          expires_at: data.expires_at,
        })
      );

      const user = await resolveSupabaseUserProfile(supaCfg, accessToken, rawUser);
      return { ok: true, user, token: accessToken };
    } catch {
      return { ok: false, error: 'Impossible de joindre le serveur Supabase Auth. Vérifiez votre connexion.' };
    }
  }

  // Autonomous Cryptographic Vault (PBKDF2-HMAC-SHA256)
  const accounts = loadVaultAccounts();
  if (accounts.some((a) => normalizeEmail(a.email) === email)) {
    return {
      ok: false,
      error: 'Un compte existe déjà avec cette adresse email. Connectez-vous ou réinitialisez votre mot de passe.',
    };
  }

  const saltHex = generateRandomSaltHex(16);
  const hashHex = await derivePasswordHashHex(input.password, saltHex, PBKDF2_ITERATIONS);
  const nowIso = new Date().toISOString();
  const idBytes = new Uint8Array(8);
  globalThis.crypto.getRandomValues(idBytes);

  const newAccount: StoredVaultAccount = {
    id: `cli-${bytesToHex(idBytes)}`,
    email,
    fullName,
    phone,
    role: 'client_connecte',
    saltHex,
    hashHex,
    iterations: PBKDF2_ITERATIONS,
    isActive: true,
    createdAt: nowIso,
    updatedAt: nowIso,
  };

  saveVaultAccounts([...accounts, newAccount]);
  const user = vaultAccountToUser(newAccount);
  const token = await issueLocalSignedSession(user);
  return { ok: true, user, token };
}

export async function authenticateWithPassword(
  emailInput: string,
  password: string
): Promise<AuthResult> {
  const email = normalizeEmail(emailInput);
  if (!email || !password) {
    return { ok: false, error: 'Veuillez renseigner votre adresse email et votre mot de passe.' };
  }

  const lockedSec = checkRateLimit(email);
  if (lockedSec > 0) {
    return {
      ok: false,
      lockoutRemainingSec: lockedSec,
      error: `Trop de tentatives infructueuses. Réessayez dans ${lockedSec} secondes.`,
    };
  }

  const supaCfg = getSupabaseConfig();
  if (supaCfg) {
    try {
      const res = await fetch(`${supaCfg.url}/auth/v1/token?grant_type=password`, {
        method: 'POST',
        headers: {
          apikey: supaCfg.anonKey,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });
      const data = (await res.json()) as Record<string, unknown>;
      if (!res.ok || typeof data.access_token !== 'string') {
        const waitSec = recordFailedAttempt(email);
        return {
          ok: false,
          lockoutRemainingSec: waitSec || undefined,
          error:
            waitSec > 0
              ? `Identifiants incorrects. Compte temporairement verrouillé (${waitSec}s).`
              : 'Email ou mot de passe incorrect.',
        };
      }

      clearFailedAttempts(email);
      const accessToken = data.access_token;
      writeRawStorage(
        AUTH_STORAGE_KEYS.SUPABASE_SESSION,
        JSON.stringify({
          access_token: accessToken,
          refresh_token: data.refresh_token,
          expires_at: data.expires_at,
        })
      );

      const rawUser = (data.user || {}) as {
        id: string;
        email?: string;
        created_at?: string;
        user_metadata?: Record<string, unknown>;
      };
      const user = await resolveSupabaseUserProfile(supaCfg, accessToken, rawUser);
      return { ok: true, user, token: accessToken };
    } catch {
      return { ok: false, error: "Erreur réseau lors de l'authentification Supabase." };
    }
  }

  // Autonomous Cryptographic Vault Verification
  const accounts = loadVaultAccounts();
  const target = accounts.find((a) => normalizeEmail(a.email) === email);

  if (!target || !target.isActive) {
    // Perform dummy PBKDF2 work to prevent account enumeration timing leaks
    await derivePasswordHashHex(password, '00112233445566778899aabbccddeeff', PBKDF2_ITERATIONS);
    const waitSec = recordFailedAttempt(email);
    return {
      ok: false,
      lockoutRemainingSec: waitSec || undefined,
      error: 'Email ou mot de passe incorrect.',
    };
  }

  const computedHash = await derivePasswordHashHex(password, target.saltHex, target.iterations);
  if (!constantTimeHexEqual(computedHash, target.hashHex)) {
    const waitSec = recordFailedAttempt(email);
    return {
      ok: false,
      lockoutRemainingSec: waitSec || undefined,
      error:
        waitSec > 0
          ? `Identifiants incorrects. Par sécurité, veuillez patienter ${waitSec}s.`
          : 'Email ou mot de passe incorrect.',
    };
  }

  clearFailedAttempts(email);
  const user = vaultAccountToUser(target);
  const token = await issueLocalSignedSession(user);
  return { ok: true, user, token };
}

export async function restoreAuthenticatedSession(): Promise<AuthenticatedUser | null> {
  const supaCfg = getSupabaseConfig();
  if (supaCfg) {
    const rawSupa = readRawStorage(AUTH_STORAGE_KEYS.SUPABASE_SESSION);
    if (!rawSupa) return null;
    try {
      const parsed = JSON.parse(rawSupa) as {
        access_token?: string;
        refresh_token?: string;
        expires_at?: number;
      };
      let accessToken = parsed.access_token || '';
      const nowSec = Math.floor(Date.now() / 1000);

      if (parsed.expires_at && parsed.expires_at <= nowSec + 30 && parsed.refresh_token) {
        const refreshRes = await fetch(`${supaCfg.url}/auth/v1/token?grant_type=refresh_token`, {
          method: 'POST',
          headers: {
            apikey: supaCfg.anonKey,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ refresh_token: parsed.refresh_token }),
        });
        if (refreshRes.ok) {
          const refreshed = (await refreshRes.json()) as Record<string, unknown>;
          if (typeof refreshed.access_token === 'string') {
            accessToken = refreshed.access_token;
            writeRawStorage(
              AUTH_STORAGE_KEYS.SUPABASE_SESSION,
              JSON.stringify({
                access_token: refreshed.access_token,
                refresh_token: refreshed.refresh_token,
                expires_at: refreshed.expires_at,
              })
            );
          }
        }
      }

      if (!accessToken) return null;
      const userRes = await fetch(`${supaCfg.url}/auth/v1/user`, {
        headers: {
          apikey: supaCfg.anonKey,
          Authorization: `Bearer ${accessToken}`,
        },
      });
      if (!userRes.ok) {
        removeRawStorage(AUTH_STORAGE_KEYS.SUPABASE_SESSION);
        return null;
      }
      const authUser = (await userRes.json()) as {
        id: string;
        email?: string;
        created_at?: string;
        user_metadata?: Record<string, unknown>;
      };
      return await resolveSupabaseUserProfile(supaCfg, accessToken, authUser);
    } catch {
      return null;
    }
  }

  const token = readRawStorage(AUTH_STORAGE_KEYS.SESSION_TOKEN);
  if (!token) return null;

  const secretHex = getOrCreateSigningSecretHex();
  const claims = await verifySessionToken(token, secretHex);
  if (!claims) {
    removeRawStorage(AUTH_STORAGE_KEYS.SESSION_TOKEN);
    return null;
  }

  // Re-validate against authoritative vault account so deleted/disabled accounts or tampered roles never persist
  const accounts = loadVaultAccounts();
  const account = accounts.find((a) => a.id === claims.sub && normalizeEmail(a.email) === normalizeEmail(claims.email));
  if (!account || !account.isActive || account.role !== claims.role) {
    removeRawStorage(AUTH_STORAGE_KEYS.SESSION_TOKEN);
    return null;
  }

  return vaultAccountToUser(account);
}

export async function signOutActiveSession(): Promise<void> {
  const supaCfg = getSupabaseConfig();
  if (supaCfg) {
    const rawSupa = readRawStorage(AUTH_STORAGE_KEYS.SUPABASE_SESSION);
    if (rawSupa) {
      try {
        const parsed = JSON.parse(rawSupa) as { access_token?: string };
        if (parsed.access_token) {
          await fetch(`${supaCfg.url}/auth/v1/logout`, {
            method: 'POST',
            headers: {
              apikey: supaCfg.anonKey,
              Authorization: `Bearer ${parsed.access_token}`,
            },
          });
        }
      } catch {
        // Ignore network errors on logout
      }
    }
    removeRawStorage(AUTH_STORAGE_KEYS.SUPABASE_SESSION);
  }
  removeRawStorage(AUTH_STORAGE_KEYS.SESSION_TOKEN);
}

export async function updateAccountPassword(input: {
  userId: string;
  currentPassword: string;
  newPassword: string;
}): Promise<{ ok: boolean; error?: string }> {
  const pwdCheck = validatePasswordStrength(input.newPassword);
  if (!pwdCheck.valid) {
    return { ok: false, error: pwdCheck.errors.join(' ') };
  }

  const supaCfg = getSupabaseConfig();
  if (supaCfg) {
    const rawSupa = readRawStorage(AUTH_STORAGE_KEYS.SUPABASE_SESSION);
    if (!rawSupa) return { ok: false, error: 'Session expirée.' };
    try {
      const parsed = JSON.parse(rawSupa) as { access_token?: string };
      const res = await fetch(`${supaCfg.url}/auth/v1/user`, {
        method: 'PUT',
        headers: {
          apikey: supaCfg.anonKey,
          Authorization: `Bearer ${parsed.access_token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ password: input.newPassword }),
      });
      if (!res.ok) {
        return { ok: false, error: 'Impossible de mettre à jour le mot de passe sur le serveur.' };
      }
      return { ok: true };
    } catch {
      return { ok: false, error: 'Erreur réseau lors de la mise à jour.' };
    }
  }

  const accounts = loadVaultAccounts();
  const idx = accounts.findIndex((a) => a.id === input.userId);
  if (idx === -1) return { ok: false, error: 'Compte introuvable.' };

  const target = accounts[idx];
  const currentHash = await derivePasswordHashHex(input.currentPassword, target.saltHex, target.iterations);
  if (!constantTimeHexEqual(currentHash, target.hashHex)) {
    return { ok: false, error: 'Votre mot de passe actuel est incorrect.' };
  }

  const newSaltHex = generateRandomSaltHex(16);
  const newHashHex = await derivePasswordHashHex(input.newPassword, newSaltHex, PBKDF2_ITERATIONS);
  const updated: StoredVaultAccount = {
    ...target,
    saltHex: newSaltHex,
    hashHex: newHashHex,
    iterations: PBKDF2_ITERATIONS,
    updatedAt: new Date().toISOString(),
  };

  const next = [...accounts];
  next[idx] = updated;
  saveVaultAccounts(next);
  await issueLocalSignedSession(vaultAccountToUser(updated));
  return { ok: true };
}

export async function resetClientPasswordWithPhoneVerification(input: {
  email: string;
  phone: string;
  newPassword: string;
}): Promise<{ ok: boolean; message?: string; error?: string }> {
  const email = normalizeEmail(input.email);
  if (!email) {
    return { ok: false, error: 'Veuillez renseigner votre adresse email.' };
  }

  const supaCfg = getSupabaseConfig();
  if (supaCfg) {
    try {
      await fetch(`${supaCfg.url}/auth/v1/recover`, {
        method: 'POST',
        headers: {
          apikey: supaCfg.anonKey,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email }),
      });
      return {
        ok: true,
        message: 'Si un compte correspond à cet email, un lien sécurisé de réinitialisation vous a été envoyé.',
      };
    } catch {
      return { ok: false, error: 'Impossible de contacter le service de récupération.' };
    }
  }

  const pwdCheck = validatePasswordStrength(input.newPassword);
  if (!pwdCheck.valid) {
    return { ok: false, error: pwdCheck.errors.join(' ') };
  }

  const accounts = loadVaultAccounts();
  const idx = accounts.findIndex((a) => normalizeEmail(a.email) === email);
  if (idx === -1) {
    return { ok: false, error: 'Aucun compte client ne correspond à ces coordonnées.' };
  }

  const target = accounts[idx];
  if (isStaffRole(target.role)) {
    return {
      ok: false,
      error: 'Pour un compte du personnel habilité, veuillez contacter la Direction Générale MPECK MULTI-SERVICES.',
    };
  }

  const inputDigits = normalizePhoneDigits(input.phone).replace(/^\+/, '');
  const storedDigits = normalizePhoneDigits(target.phone).replace(/^\+/, '');
  if (!inputDigits || inputDigits.length < 8 || !storedDigits.endsWith(inputDigits.slice(-8))) {
    return { ok: false, error: 'Aucun compte client ne correspond à ces coordonnées.' };
  }

  const newSaltHex = generateRandomSaltHex(16);
  const newHashHex = await derivePasswordHashHex(input.newPassword, newSaltHex, PBKDF2_ITERATIONS);
  const next = [...accounts];
  next[idx] = {
    ...target,
    saltHex: newSaltHex,
    hashHex: newHashHex,
    iterations: PBKDF2_ITERATIONS,
    updatedAt: new Date().toISOString(),
  };
  saveVaultAccounts(next);

  return {
    ok: true,
    message: 'Votre nouveau mot de passe a été enregistré avec succès. Vous pouvez vous connecter.',
  };
}

export async function deleteAndAnonymizeClientAccount(input: {
  userId: string;
  password: string;
  reason?: string;
}): Promise<{ ok: boolean; error?: string }> {
  const accounts = loadVaultAccounts();
  const target = accounts.find((a) => a.id === input.userId);
  if (!target) {
    return { ok: false, error: 'Compte introuvable.' };
  }
  if (isStaffRole(target.role)) {
    return { ok: false, error: 'Un compte personnel habilité ne peut être révoqué que par la Direction Générale.' };
  }

  const computedHash = await derivePasswordHashHex(input.password, target.saltHex, target.iterations);
  if (!constantTimeHexEqual(computedHash, target.hashHex)) {
    return { ok: false, error: 'Mot de passe de confirmation incorrect.' };
  }

  // Record anonymized compliance entry (Loi camerounaise n° 2010/012 & Migration 8)
  const rawDeletions = readRawStorage(AUTH_STORAGE_KEYS.DELETION_LOG);
  let logs: unknown[] = [];
  if (rawDeletions) {
    try {
      logs = JSON.parse(rawDeletions) as unknown[];
    } catch {
      logs = [];
    }
  }
  const maskedPhone = target.phone.slice(0, 4) + '••••' + target.phone.slice(-2);
  logs.unshift({
    id: `del-${Date.now()}`,
    requester_reference: target.id,
    requester_phone_masked: maskedPhone,
    reason: input.reason || "Demande utilisateur (droit à l'effacement, Loi n° 2010/012)",
    status: 'PROCESSED_ANONYMIZED',
    created_at: new Date().toISOString(),
  });
  writeRawStorage(AUTH_STORAGE_KEYS.DELETION_LOG, JSON.stringify(logs));

  const remaining = accounts.filter((a) => a.id !== input.userId);
  saveVaultAccounts(remaining);
  await signOutActiveSession();
  return { ok: true };
}

export function resetAuthVaultForTests(): void {
  memoryStore.clear();
}
