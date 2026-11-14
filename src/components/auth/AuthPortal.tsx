// ============================================================================
// ECOPARK CAMEROUN (YAOUNDÉ, AHALA) - PORTAIL D'AUTHENTIFICATION (/Connexion)
// (src/components/auth/AuthPortal.tsx)
// Connexion Cliente, Création de Compte, Accès Cockpit Pro, Mot de Passe Oublié
// & Gouvernance de Compte (Changement MDP + Droit à l'effacement Loi 2010/012)
// ============================================================================

import React, { useState, useEffect } from 'react';
import {
  Lock,
  Mail,
  User,
  Phone,
  Eye,
  EyeOff,
  ShieldCheck,
  ShieldAlert,
  ArrowRight,
  CheckCircle2,
  AlertCircle,
  KeyRound,
  LogOut,
  Ticket,
  Trash2,
} from 'lucide-react';
import { useAuth, type AuthPortalInitialMode } from '../../context/AuthContext';
import { useEcoPark } from '../../context/EcoParkContext';
import { ImmersiveSection } from '../layout/ImmersiveSection';
import {
  validatePasswordStrength,
  getRoleDisplayLabel,
  isStaffRole,
} from '../../utils/ecoAuth';
import type { ActiveView } from '../../types/ecosystem';

export interface AuthPortalProps {
  forcedMode?: AuthPortalInitialMode;
  targetAfterAuth?: ActiveView;
  embedded?: boolean;
}

export const AuthPortal: React.FC<AuthPortalProps> = ({
  forcedMode,
  targetAfterAuth,
  embedded = false,
}) => {
  const {
    user,
    isStaff,
    isCloudSupabaseActive,
    pendingRedirectView,
    setPendingRedirectView,
    authPortalMode,
    setAuthPortalMode,
    login,
    registerClient,
    logout,
    changePassword,
    resetClientPassword,
    deleteMyAccount,
  } = useAuth();

  const { setActiveView } = useEcoPark();

  const [mode, setMode] = useState<AuthPortalInitialMode>(forcedMode || authPortalMode);
  useEffect(() => {
    if (forcedMode) setMode(forcedMode);
    else setMode(authPortalMode);
  }, [forcedMode, authPortalMode]);

  const switchMode = (next: AuthPortalInitialMode) => {
    setMode(next);
    setAuthPortalMode(next);
    setErrorMsg(null);
    setSuccessMsg(null);
  };

  // Form states
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [privacyAccepted, setPrivacyAccepted] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  // Account settings states (when already logged in)
  const [currentPwd, setCurrentPwd] = useState('');
  const [newPwd, setNewPwd] = useState('');
  const [deletePwd, setDeletePwd] = useState('');
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

  const [submitting, setSubmitting] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);

  const pwdStrength = validatePasswordStrength(password);

  const navigateAfterSuccess = (loggedRole?: string) => {
    const destination =
      targetAfterAuth ||
      pendingRedirectView ||
      (isStaffRole(loggedRole as any) ? 'ranger' : 'pass');
    setPendingRedirectView(null);
    setActiveView(destination);
  };

  const handleLoginSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg(null);
    setSuccessMsg(null);
    setSubmitting(true);

    const res = await login(email, password);
    setSubmitting(false);

    if (!res.ok || !res.user) {
      setErrorMsg(res.error || 'Identifiants incorrects.');
      return;
    }

    if (mode === 'staff_login' && !isStaffRole(res.user.role)) {
      setErrorMsg(
        "Ce compte correspond à un Espace Cliente et ne dispose pas des habilitations Cockpit Pro. Redirection vers votre Espace Cliente..."
      );
      setTimeout(() => setActiveView('pass'), 1100);
      return;
    }

    setPassword('');
    navigateAfterSuccess(res.user.role);
  };

  const handleRegisterSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg(null);
    setSuccessMsg(null);

    if (password !== confirmPassword) {
      setErrorMsg('Les deux mots de passe ne correspondent pas.');
      return;
    }
    if (!privacyAccepted) {
      setErrorMsg(
        'Veuillez accepter la Politique de Confidentialité (Loi n° 2010/012) pour créer votre Espace Cliente.'
      );
      return;
    }

    setSubmitting(true);
    const res = await registerClient({ fullName, email, phone, password });
    setSubmitting(false);

    if (!res.ok || !res.user) {
      setErrorMsg(res.error || 'Impossible de créer le compte.');
      return;
    }

    setPassword('');
    setConfirmPassword('');
    navigateAfterSuccess(res.user.role);
  };

  const handleRecoverSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg(null);
    setSuccessMsg(null);
    setSubmitting(true);

    const res = await resetClientPassword({
      email,
      phone,
      newPassword: password,
    });
    setSubmitting(false);

    if (!res.ok) {
      setErrorMsg(res.error || 'Réinitialisation impossible.');
      return;
    }

    setSuccessMsg(res.message || 'Mot de passe mis à jour.');
    setPassword('');
    setTimeout(() => switchMode('client_login'), 1800);
  };

  const handleChangePassword = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg(null);
    setSuccessMsg(null);
    setSubmitting(true);
    const res = await changePassword(currentPwd, newPwd);
    setSubmitting(false);
    if (!res.ok) {
      setErrorMsg(res.error || 'Échec du changement de mot de passe.');
      return;
    }
    setCurrentPwd('');
    setNewPwd('');
    setSuccessMsg('Votre mot de passe a été mis à jour avec succès.');
  };

  const handleDeleteAccount = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg(null);
    setSubmitting(true);
    const res = await deleteMyAccount(deletePwd);
    setSubmitting(false);
    if (!res.ok) {
      setErrorMsg(res.error || 'Suppression refusée.');
      return;
    }
    setShowDeleteConfirm(false);
    setActiveView('accueil');
  };

  // ==========================================================================
  // CONNECTED PROFILE & SECURITY MANAGEMENT VIEW
  // ==========================================================================
  if (user && !embedded) {
    return (
      <div className="eco-view-enter space-y-10 pb-16">
        <ImmersiveSection variant="canopy" className="py-10">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <div className="inline-flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-[#B7E4C7]">
                <ShieldCheck className="w-4 h-4 text-[#74C69D]" />
                <span>Session Authentifiée · {getRoleDisplayLabel(user.role)}</span>
              </div>
              <h1 className="font-['Barlow_Semi_Condensed'] text-2xl sm:text-4xl font-bold text-white mt-1">
                Mon Compte &amp; Sécurité : {user.fullName}
              </h1>
            </div>
            <button
              type="button"
              onClick={async () => {
                await logout();
                setActiveView('accueil');
              }}
              className="px-4 py-2.5 rounded-xl bg-white/10 hover:bg-white/20 text-white border border-white/25 text-xs font-bold inline-flex items-center gap-2 cursor-pointer self-start sm:self-auto"
            >
              <LogOut className="w-4 h-4 text-rose-300" />
              <span>Se déconnecter</span>
            </button>
          </div>
        </ImmersiveSection>

        <div className="eco-container max-w-3xl space-y-6">
          {/* Active Session Summary */}
          <div className="p-6 rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-default)] shadow-xs space-y-5">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-[var(--border-default)]">
              <div>
                <span className="text-xs font-mono font-bold uppercase text-[var(--brand-primary)]">
                  Identité Vérifiée
                </span>
                <h2 className="font-['Barlow_Semi_Condensed'] text-2xl font-bold text-[var(--text-primary)] mt-0.5">
                  {user.fullName}
                </h2>
                <p className="text-xs text-[var(--text-muted)] font-mono mt-0.5">
                  {user.email} {user.phone ? `· ${user.phone}` : ''}
                  {user.matricule ? ` · ${user.matricule}` : ''}
                </p>
              </div>

              <div className="flex flex-wrap gap-2">
                {isStaff ? (
                  <button
                    type="button"
                    onClick={() => setActiveView('ranger')}
                    className="px-4 py-2.5 rounded-xl bg-amber-600 hover:bg-amber-700 text-white text-xs font-bold inline-flex items-center gap-1.5 cursor-pointer"
                  >
                    <ShieldAlert className="w-4 h-4" />
                    <span>Ouvrir le Cockpit Pro</span>
                  </button>
                ) : (
                  <button
                    type="button"
                    onClick={() => setActiveView('pass')}
                    className="px-4 py-2.5 rounded-xl bg-[var(--brand-primary)] hover:bg-[var(--brand-secondary)] text-white text-xs font-bold inline-flex items-center gap-1.5 cursor-pointer"
                  >
                    <Ticket className="w-4 h-4" />
                    <span>Accéder à mon Espace Cliente</span>
                  </button>
                )}
              </div>
            </div>

            {errorMsg && (
              <div className="p-3.5 rounded-xl bg-red-50 dark:bg-red-950/60 border border-red-300 dark:border-red-800 text-red-800 dark:text-red-200 text-xs flex items-start gap-2">
                <AlertCircle className="w-4 h-4 shrink-0 mt-0.5" />
                <span>{errorMsg}</span>
              </div>
            )}
            {successMsg && (
              <div className="p-3.5 rounded-xl bg-emerald-50 dark:bg-emerald-950/60 border border-emerald-300 dark:border-emerald-800 text-emerald-800 dark:text-emerald-200 text-xs flex items-start gap-2">
                <CheckCircle2 className="w-4 h-4 shrink-0 mt-0.5" />
                <span>{successMsg}</span>
              </div>
            )}

            {/* Password Update Form */}
            <form onSubmit={handleChangePassword} className="space-y-4">
              <h3 className="font-['Barlow_Semi_Condensed'] text-lg font-bold text-[var(--text-primary)] flex items-center gap-2">
                <KeyRound className="w-4 h-4 text-[var(--brand-primary)]" />
                <span>Modifier mon mot de passe</span>
              </h3>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-semibold text-[var(--text-primary)] mb-1">
                    Mot de passe actuel
                  </label>
                  <input
                    type="password"
                    required
                    value={currentPwd}
                    onChange={(e) => setCurrentPwd(e.target.value)}
                    autoComplete="current-password"
                    className="w-full px-3.5 py-2.5 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)] text-sm text-[var(--text-primary)]"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-[var(--text-primary)] mb-1">
                    Nouveau mot de passe (8+ car., Maj, chiffre)
                  </label>
                  <input
                    type="password"
                    required
                    value={newPwd}
                    onChange={(e) => setNewPwd(e.target.value)}
                    autoComplete="new-password"
                    className="w-full px-3.5 py-2.5 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)] text-sm text-[var(--text-primary)]"
                  />
                </div>
              </div>
              <button
                type="submit"
                disabled={submitting}
                className="px-4 py-2.5 rounded-xl bg-[var(--brand-primary)] hover:bg-[var(--brand-secondary)] text-white text-xs font-bold cursor-pointer disabled:opacity-60"
              >
                Mettre à jour le mot de passe
              </button>
            </form>

            {/* Right to Erasure (Loi n° 2010/012 - Client Only) */}
            {!isStaff && (
              <div className="pt-5 border-t border-[var(--border-default)] space-y-3">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                  <div>
                    <h4 className="font-['Barlow_Semi_Condensed'] text-base font-bold text-red-700 dark:text-red-400">
                      Droit à l&apos;effacement &amp; Suppression de compte
                    </h4>
                    <p className="text-xs text-[var(--text-muted)]">
                      Conformément à la Loi camerounaise n° 2010/012 et au RGPD, vous pouvez anonymiser et supprimer votre compte client à tout moment.
                    </p>
                  </div>
                  <button
                    type="button"
                    onClick={() => setShowDeleteConfirm(!showDeleteConfirm)}
                    className="px-3.5 py-2 rounded-xl border border-red-300 dark:border-red-800 text-red-700 dark:text-red-300 hover:bg-red-50 dark:hover:bg-red-950/40 text-xs font-semibold inline-flex items-center gap-1.5 cursor-pointer self-start sm:self-auto"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                    <span>Supprimer mon compte</span>
                  </button>
                </div>

                {showDeleteConfirm && (
                  <form
                    onSubmit={handleDeleteAccount}
                    className="p-4 rounded-xl bg-red-50/70 dark:bg-red-950/30 border border-red-300 dark:border-red-800 space-y-3"
                  >
                    <p className="text-xs text-red-800 dark:text-red-200">
                      Saisissez votre mot de passe pour confirmer la suppression irréversible et l&apos;anonymisation de votre compte :
                    </p>
                    <div className="flex flex-col sm:flex-row gap-2">
                      <input
                        type="password"
                        required
                        placeholder="Mot de passe de confirmation"
                        value={deletePwd}
                        onChange={(e) => setDeletePwd(e.target.value)}
                        className="flex-1 px-3.5 py-2 rounded-xl bg-[var(--bg-surface)] border border-red-300 dark:border-red-700 text-sm text-[var(--text-primary)]"
                      />
                      <button
                        type="submit"
                        disabled={submitting}
                        className="px-4 py-2 rounded-xl bg-red-600 hover:bg-red-700 text-white text-xs font-bold cursor-pointer"
                      >
                        Confirmer l&apos;effacement
                      </button>
                    </div>
                  </form>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    );
  }

  // ==========================================================================
  // LOGIN / REGISTER / STAFF / RECOVERY PORTAL CARD
  // ==========================================================================
  const cardContent = (
    <div className="max-w-xl mx-auto w-full">
      <div className="rounded-3xl bg-[var(--bg-surface)] border border-[var(--border-default)] shadow-xl overflow-hidden">
        {/* Top Mode Tabs */}
        <div className="grid grid-cols-3 bg-[var(--bg-elevated)] border-b border-[var(--border-default)] text-xs font-semibold">
          <button
            type="button"
            onClick={() => switchMode('client_login')}
            className={`py-3.5 px-2 text-center transition-colors cursor-pointer border-b-2 ${
              mode === 'client_login' || mode === 'recover'
                ? 'border-[var(--brand-primary)] text-[var(--brand-primary)] bg-[var(--bg-surface)] font-bold'
                : 'border-transparent text-[var(--text-muted)] hover:text-[var(--text-primary)]'
            }`}
          >
            Connexion Cliente
          </button>
          <button
            type="button"
            onClick={() => switchMode('client_register')}
            className={`py-3.5 px-2 text-center transition-colors cursor-pointer border-b-2 ${
              mode === 'client_register'
                ? 'border-[var(--brand-primary)] text-[var(--brand-primary)] bg-[var(--bg-surface)] font-bold'
                : 'border-transparent text-[var(--text-muted)] hover:text-[var(--text-primary)]'
            }`}
          >
            Créer un Compte
          </button>
          <button
            type="button"
            onClick={() => switchMode('staff_login')}
            className={`py-3.5 px-2 text-center transition-colors cursor-pointer border-b-2 ${
              mode === 'staff_login'
                ? 'border-amber-600 text-amber-700 dark:text-amber-400 bg-[var(--bg-surface)] font-bold'
                : 'border-transparent text-[var(--text-muted)] hover:text-[var(--text-primary)]'
            }`}
          >
            Cockpit Pro
          </button>
        </div>

        <div className="p-6 sm:p-8 space-y-5">
          {/* Contextual Header */}
          <div className="space-y-1">
            <div className="inline-flex items-center gap-1.5 text-[11px] font-mono font-bold uppercase tracking-wider text-[var(--brand-primary)]">
              {mode === 'staff_login' ? (
                <>
                  <ShieldAlert className="w-3.5 h-3.5 text-amber-600 dark:text-amber-400" />
                  <span className="text-amber-700 dark:text-amber-400">
                    Accès Réservé au Personnel Habilité (RBAC)
                  </span>
                </>
              ) : (
                <>
                  <ShieldCheck className="w-3.5 h-3.5" />
                  <span>
                    {isCloudSupabaseActive
                      ? 'Authentification Supabase Cloud Chiffrée'
                      : 'Authentification Chiffrée PBKDF2-SHA256'}
                  </span>
                </>
              )}
            </div>

            <h2 className="font-['Barlow_Semi_Condensed'] text-2xl font-bold text-[var(--text-primary)]">
              {mode === 'client_login' && 'Accéder à votre Espace Cliente & Pass QR'}
              {mode === 'client_register' && 'Créer votre Espace Cliente ECOPARK'}
              {mode === 'staff_login' && 'Connexion Cockpit Pro & Supervision Ahala'}
              {mode === 'recover' && 'Réinitialiser votre mot de passe'}
            </h2>
            <p className="text-xs text-[var(--text-muted)] leading-relaxed">
              {mode === 'client_login' &&
                'Retrouvez vos Pass QR réservés en FCFA, téléchargez vos billets officiels et gérez vos visites en toute confidentialité.'}
              {mode === 'client_register' &&
                'Inscrivez-vous en 30 secondes pour rattacher automatiquement vos billets QR (Orange Money, MTN MoMo ou Guichet) à votre espace personnel.'}
              {mode === 'staff_login' &&
                'Authentification obligatoire pour la Direction Générale, le Chef d’Exploitation, le Guichet RN3, le Contrôle QR et la Comptabilité.'}
              {mode === 'recover' &&
                (isCloudSupabaseActive
                  ? 'Saisissez votre adresse email pour recevoir un lien sécurisé de réinitialisation.'
                  : 'Confirmez votre email et le numéro de téléphone associé à votre compte pour définir un nouveau mot de passe.')}
            </p>
          </div>

          {errorMsg && (
            <div
              role="alert"
              className="p-3.5 rounded-xl bg-red-50 dark:bg-red-950/60 border border-red-300 dark:border-red-800 text-red-800 dark:text-red-200 text-xs flex items-start gap-2.5"
            >
              <AlertCircle className="w-4 h-4 shrink-0 mt-0.5 text-red-600 dark:text-red-400" />
              <span>{errorMsg}</span>
            </div>
          )}

          {successMsg && (
            <div
              role="status"
              className="p-3.5 rounded-xl bg-emerald-50 dark:bg-emerald-950/60 border border-emerald-300 dark:border-emerald-800 text-emerald-800 dark:text-emerald-200 text-xs flex items-start gap-2.5"
            >
              <CheckCircle2 className="w-4 h-4 shrink-0 mt-0.5 text-emerald-600 dark:text-emerald-400" />
              <span>{successMsg}</span>
            </div>
          )}

          {/* =============================================================== */}
          {/* FORM 1: CLIENT LOGIN OR STAFF LOGIN                             */}
          {/* =============================================================== */}
          {(mode === 'client_login' || mode === 'staff_login') && (
            <form onSubmit={handleLoginSubmit} className="space-y-4">
              <div>
                <label
                  htmlFor="auth-login-email"
                  className="block text-xs font-semibold text-[var(--text-primary)] mb-1.5"
                >
                  {mode === 'staff_login'
                    ? 'Email professionnel (@ecopark-yaounde.com)'
                    : 'Adresse email'}
                </label>
                <div className="relative">
                  <Mail className="w-4 h-4 text-[var(--text-muted)] absolute left-3.5 top-1/2 -translate-y-1/2" />
                  <input
                    id="auth-login-email"
                    type="email"
                    required
                    autoComplete="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder={
                      mode === 'staff_login'
                        ? 'prenom.poste@ecopark-yaounde.com'
                        : 'votre.email@exemple.cm'
                    }
                    className="w-full pl-10 pr-4 py-3 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)] text-sm text-[var(--text-primary)] placeholder-[var(--text-muted)] focus:outline-none focus:ring-2 focus:ring-[var(--brand-primary)]"
                  />
                </div>
              </div>

              <div>
                <div className="flex items-center justify-between mb-1.5">
                  <label
                    htmlFor="auth-login-password"
                    className="text-xs font-semibold text-[var(--text-primary)]"
                  >
                    Mot de passe
                  </label>
                  {mode === 'client_login' && (
                    <button
                      type="button"
                      onClick={() => switchMode('recover')}
                      className="text-xs font-semibold text-[var(--brand-primary)] hover:underline cursor-pointer"
                    >
                      Mot de passe oublié ?
                    </button>
                  )}
                </div>
                <div className="relative">
                  <Lock className="w-4 h-4 text-[var(--text-muted)] absolute left-3.5 top-1/2 -translate-y-1/2" />
                  <input
                    id="auth-login-password"
                    type={showPassword ? 'text' : 'password'}
                    required
                    autoComplete="current-password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="••••••••••••"
                    className="w-full pl-10 pr-11 py-3 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)] text-sm text-[var(--text-primary)] placeholder-[var(--text-muted)] focus:outline-none focus:ring-2 focus:ring-[var(--brand-primary)]"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    aria-label={showPassword ? 'Masquer le mot de passe' : 'Afficher le mot de passe'}
                    className="absolute right-3 top-1/2 -translate-y-1/2 p-1.5 text-[var(--text-muted)] hover:text-[var(--text-primary)] cursor-pointer"
                  >
                    {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  </button>
                </div>
              </div>

              <button
                type="submit"
                disabled={submitting}
                className={`w-full py-3.5 px-5 rounded-xl font-bold text-sm text-white shadow-sm transition-all flex items-center justify-center gap-2 cursor-pointer disabled:opacity-60 ${
                  mode === 'staff_login'
                    ? 'bg-amber-600 hover:bg-amber-700'
                    : 'bg-[var(--brand-primary)] hover:bg-[var(--brand-secondary)]'
                }`}
              >
                <span>
                  {submitting
                    ? 'Vérification cryptographique...'
                    : mode === 'staff_login'
                    ? 'Ouvrir le Cockpit Pro'
                    : 'Se connecter à mon Espace Cliente'}
                </span>
                <ArrowRight className="w-4 h-4" />
              </button>

              {mode === 'client_login' && (
                <div className="pt-2 text-center text-xs text-[var(--text-muted)]">
                  Première visite sur ECOPARK CAMEROUN ?{' '}
                  <button
                    type="button"
                    onClick={() => switchMode('client_register')}
                    className="font-bold text-[var(--brand-primary)] hover:underline cursor-pointer"
                  >
                    Créer mon compte gratuitement
                  </button>
                </div>
              )}
            </form>
          )}

          {/* =============================================================== */}
          {/* FORM 2: CLIENT REGISTRATION                                     */}
          {/* =============================================================== */}
          {mode === 'client_register' && (
            <form onSubmit={handleRegisterSubmit} className="space-y-4">
              <div>
                <label
                  htmlFor="auth-reg-name"
                  className="block text-xs font-semibold text-[var(--text-primary)] mb-1"
                >
                  Nom complet *
                </label>
                <div className="relative">
                  <User className="w-4 h-4 text-[var(--text-muted)] absolute left-3.5 top-1/2 -translate-y-1/2" />
                  <input
                    id="auth-reg-name"
                    type="text"
                    required
                    autoComplete="name"
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                    placeholder="Ex: Marie-Claire Atangana"
                    className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)] text-sm text-[var(--text-primary)]"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
                <div>
                  <label
                    htmlFor="auth-reg-email"
                    className="block text-xs font-semibold text-[var(--text-primary)] mb-1"
                  >
                    Adresse email *
                  </label>
                  <div className="relative">
                    <Mail className="w-4 h-4 text-[var(--text-muted)] absolute left-3.5 top-1/2 -translate-y-1/2" />
                    <input
                      id="auth-reg-email"
                      type="email"
                      required
                      autoComplete="email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      placeholder="nom@exemple.cm"
                      className="w-full pl-10 pr-3 py-2.5 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)] text-sm text-[var(--text-primary)]"
                    />
                  </div>
                </div>

                <div>
                  <label
                    htmlFor="auth-reg-phone"
                    className="block text-xs font-semibold text-[var(--text-primary)] mb-1"
                  >
                    Téléphone WhatsApp / Mobile Money *
                  </label>
                  <div className="relative">
                    <Phone className="w-4 h-4 text-[var(--text-muted)] absolute left-3.5 top-1/2 -translate-y-1/2" />
                    <input
                      id="auth-reg-phone"
                      type="tel"
                      required
                      autoComplete="tel"
                      value={phone}
                      onChange={(e) => setPhone(e.target.value)}
                      placeholder="+237 6XX XX XX XX"
                      className="w-full pl-10 pr-3 py-2.5 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)] text-sm text-[var(--text-primary)]"
                    />
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
                <div>
                  <label
                    htmlFor="auth-reg-pwd"
                    className="block text-xs font-semibold text-[var(--text-primary)] mb-1"
                  >
                    Mot de passe *
                  </label>
                  <div className="relative">
                    <Lock className="w-4 h-4 text-[var(--text-muted)] absolute left-3.5 top-1/2 -translate-y-1/2" />
                    <input
                      id="auth-reg-pwd"
                      type={showPassword ? 'text' : 'password'}
                      required
                      autoComplete="new-password"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      placeholder="Min. 8 caractères"
                      className="w-full pl-10 pr-10 py-2.5 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)] text-sm text-[var(--text-primary)]"
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      aria-label={showPassword ? 'Masquer' : 'Afficher'}
                      className="absolute right-2.5 top-1/2 -translate-y-1/2 p-1 text-[var(--text-muted)] cursor-pointer"
                    >
                      {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                    </button>
                  </div>
                </div>

                <div>
                  <label
                    htmlFor="auth-reg-pwd2"
                    className="block text-xs font-semibold text-[var(--text-primary)] mb-1"
                  >
                    Confirmer le mot de passe *
                  </label>
                  <input
                    id="auth-reg-pwd2"
                    type={showPassword ? 'text' : 'password'}
                    required
                    autoComplete="new-password"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    placeholder="Répéter le mot de passe"
                    className="w-full px-3.5 py-2.5 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)] text-sm text-[var(--text-primary)]"
                  />
                </div>
              </div>

              {/* Password Strength Meter */}
              {password.length > 0 && (
                <div className="space-y-1">
                  <div className="flex gap-1.5 h-1.5">
                    {[1, 2, 3, 4].map((lvl) => (
                      <div
                        key={lvl}
                        className={`flex-1 rounded-full transition-colors ${
                          pwdStrength.score >= lvl
                            ? pwdStrength.score >= 3
                              ? 'bg-emerald-500'
                              : 'bg-amber-500'
                            : 'bg-[var(--border-default)]'
                        }`}
                      />
                    ))}
                  </div>
                  <p className="text-[11px] text-[var(--text-muted)]">
                    {pwdStrength.valid
                      ? 'Robustesse conforme (PBKDF2-SHA256).'
                      : pwdStrength.errors[0]}
                  </p>
                </div>
              )}

              <label className="flex items-start gap-2.5 text-xs text-[var(--text-muted)] cursor-pointer select-none pt-1">
                <input
                  type="checkbox"
                  checked={privacyAccepted}
                  onChange={(e) => setPrivacyAccepted(e.target.checked)}
                  className="mt-0.5 w-4 h-4 rounded accent-[var(--brand-primary)] shrink-0"
                />
                <span>
                  J&apos;accepte le traitement sécurisé de mes données de réservation conformément à la{' '}
                  <button
                    type="button"
                    onClick={() => setActiveView('legal')}
                    className="text-[var(--brand-primary)] font-semibold hover:underline cursor-pointer"
                  >
                    Politique de Confidentialité (Loi n° 2010/012)
                  </button>
                  .
                </span>
              </label>

              <button
                type="submit"
                disabled={submitting}
                className="w-full py-3.5 px-5 rounded-xl bg-[var(--brand-primary)] hover:bg-[var(--brand-secondary)] font-bold text-sm text-white shadow-sm transition-all flex items-center justify-center gap-2 cursor-pointer disabled:opacity-60"
              >
                <span>{submitting ? 'Création sécurisée...' : 'Créer mon Espace Cliente'}</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </form>
          )}

          {/* =============================================================== */}
          {/* FORM 3: PASSWORD RECOVERY                                       */}
          {/* =============================================================== */}
          {mode === 'recover' && (
            <form onSubmit={handleRecoverSubmit} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-[var(--text-primary)] mb-1">
                  Adresse email du compte
                </label>
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="votre.email@exemple.cm"
                  className="w-full px-3.5 py-2.5 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)] text-sm text-[var(--text-primary)]"
                />
              </div>

              {!isCloudSupabaseActive && (
                <>
                  <div>
                    <label className="block text-xs font-semibold text-[var(--text-primary)] mb-1">
                      Téléphone enregistré lors de l&apos;inscription
                    </label>
                    <input
                      type="tel"
                      required
                      value={phone}
                      onChange={(e) => setPhone(e.target.value)}
                      placeholder="+237 6XX XX XX XX"
                      className="w-full px-3.5 py-2.5 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)] text-sm text-[var(--text-primary)]"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-semibold text-[var(--text-primary)] mb-1">
                      Nouveau mot de passe souhaité
                    </label>
                    <input
                      type="password"
                      required
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      placeholder="Min. 8 caractères, Majuscule & Chiffre"
                      className="w-full px-3.5 py-2.5 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)] text-sm text-[var(--text-primary)]"
                    />
                  </div>
                </>
              )}

              <div className="flex items-center justify-between gap-3 pt-1">
                <button
                  type="button"
                  onClick={() => switchMode('client_login')}
                  className="text-xs font-semibold text-[var(--text-muted)] hover:text-[var(--text-primary)] cursor-pointer"
                >
                  ← Retour à la connexion
                </button>
                <button
                  type="submit"
                  disabled={submitting}
                  className="px-5 py-2.5 rounded-xl bg-[var(--brand-primary)] text-white text-xs font-bold cursor-pointer"
                >
                  Réinitialiser
                </button>
              </div>
            </form>
          )}
        </div>
      </div>
    </div>
  );

  if (embedded) {
    return cardContent;
  }

  return (
    <div className="eco-view-enter space-y-10 pb-16">
      <ImmersiveSection variant="canopy" className="py-10">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="inline-flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-[#B7E4C7]">
              <Lock className="w-4 h-4 text-[#74C69D]" />
              <span>Authentification Sécurisée · ECOPARK CAMEROUN (Yaoundé, Ahala)</span>
            </div>
            <h1 className="font-['Barlow_Semi_Condensed'] text-2xl sm:text-4xl font-bold text-white mt-1">
              Connexion Espace Cliente &amp; Cockpit Pro
            </h1>
          </div>
          <div className="text-xs text-[#E9F5ED]/85 font-mono bg-[#0B1D15]/60 px-3.5 py-2 rounded-xl border border-[#36403A]">
            Protection des données · Loi n° 2010/012 &amp; RBAC
          </div>
        </div>
      </ImmersiveSection>

      <div className="eco-container">{cardContent}</div>
    </div>
  );
};
