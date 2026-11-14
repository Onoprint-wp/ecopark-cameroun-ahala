// ============================================================================
// ECOPARK CAMEROUN (YAOUNDÉ, AHALA) - AUTHENTICATION & RBAC CONTEXT
// (src/context/AuthContext.tsx)
// ============================================================================

import React, {
  createContext,
  useContext,
  useState,
  useEffect,
  useCallback,
  useMemo,
  type ReactNode,
} from 'react';
import type { ActiveView, AuthenticatedUser } from '../types/ecosystem';
import {
  AUTH_STORAGE_KEYS,
  authenticateWithPassword,
  registerClientAccount,
  restoreAuthenticatedSession,
  signOutActiveSession,
  updateAccountPassword,
  resetClientPasswordWithPhoneVerification,
  deleteAndAnonymizeClientAccount,
  isStaffRole,
  canCheckInPasses,
  canManageParkOperations,
  isSupabaseCloudConfigured,
  type AuthResult,
} from '../utils/ecoAuth';

export type AuthPortalInitialMode = 'client_login' | 'client_register' | 'staff_login' | 'recover';

export interface AuthContextType {
  user: AuthenticatedUser | null;
  isAuthLoading: boolean;
  isAuthenticated: boolean;
  isStaff: boolean;
  canCheckIn: boolean;
  canManageOps: boolean;
  isCloudSupabaseActive: boolean;
  pendingRedirectView: ActiveView | null;
  setPendingRedirectView: (view: ActiveView | null) => void;
  authPortalMode: AuthPortalInitialMode;
  setAuthPortalMode: (mode: AuthPortalInitialMode) => void;
  login: (email: string, password: string) => Promise<AuthResult>;
  registerClient: (input: {
    fullName: string;
    email: string;
    phone: string;
    password: string;
  }) => Promise<AuthResult>;
  logout: () => Promise<void>;
  changePassword: (currentPassword: string, newPassword: string) => Promise<{ ok: boolean; error?: string }>;
  resetClientPassword: (input: {
    email: string;
    phone: string;
    newPassword: string;
  }) => Promise<{ ok: boolean; message?: string; error?: string }>;
  deleteMyAccount: (password: string, reason?: string) => Promise<{ ok: boolean; error?: string }>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<AuthenticatedUser | null>(null);
  const [isAuthLoading, setIsAuthLoading] = useState<boolean>(true);
  const [pendingRedirectView, setPendingRedirectView] = useState<ActiveView | null>(null);
  const [authPortalMode, setAuthPortalMode] = useState<AuthPortalInitialMode>(() => {
    if (typeof window !== 'undefined') {
      const path = window.location.pathname.toLowerCase();
      const params = new URLSearchParams(window.location.search);
      if (params.get('mode') === 'staff' || path === '/cockpit-pro') return 'staff_login';
      if (params.get('mode') === 'register' || path === '/inscription') return 'client_register';
    }
    return 'client_login';
  });

  // Restore cryptographic or Supabase session on mount
  useEffect(() => {
    let mounted = true;
    restoreAuthenticatedSession()
      .then((restored) => {
        if (mounted) {
          setUser(restored);
          setIsAuthLoading(false);
        }
      })
      .catch(() => {
        if (mounted) {
          setUser(null);
          setIsAuthLoading(false);
        }
      });

    return () => {
      mounted = false;
    };
  }, []);

  // Cross-tab session sync (instant sign-out / sign-in across tabs)
  useEffect(() => {
    const handleStorage = (event: StorageEvent) => {
      if (
        event.key === AUTH_STORAGE_KEYS.SESSION_TOKEN ||
        event.key === AUTH_STORAGE_KEYS.SUPABASE_SESSION ||
        event.key === AUTH_STORAGE_KEYS.ACCOUNTS
      ) {
        restoreAuthenticatedSession().then((restored) => setUser(restored));
      }
    };
    window.addEventListener('storage', handleStorage);
    return () => window.removeEventListener('storage', handleStorage);
  }, []);

  const login = useCallback(async (email: string, password: string): Promise<AuthResult> => {
    const res = await authenticateWithPassword(email, password);
    if (res.ok && res.user) {
      setUser(res.user);
    }
    return res;
  }, []);

  const registerClient = useCallback(
    async (input: {
      fullName: string;
      email: string;
      phone: string;
      password: string;
    }): Promise<AuthResult> => {
      const res = await registerClientAccount(input);
      if (res.ok && res.user) {
        setUser(res.user);
      }
      return res;
    },
    []
  );

  const logout = useCallback(async () => {
    await signOutActiveSession();
    setUser(null);
  }, []);

  const changePassword = useCallback(
    async (currentPassword: string, newPassword: string) => {
      if (!user) return { ok: false, error: 'Aucune session active.' };
      return updateAccountPassword({
        userId: user.id,
        currentPassword,
        newPassword,
      });
    },
    [user]
  );

  const resetClientPassword = useCallback(
    async (input: { email: string; phone: string; newPassword: string }) => {
      return resetClientPasswordWithPhoneVerification(input);
    },
    []
  );

  const deleteMyAccount = useCallback(
    async (password: string, reason?: string) => {
      if (!user) return { ok: false, error: 'Aucune session active.' };
      const res = await deleteAndAnonymizeClientAccount({
        userId: user.id,
        password,
        reason,
      });
      if (res.ok) {
        setUser(null);
      }
      return res;
    },
    [user]
  );

  const value = useMemo<AuthContextType>(
    () => ({
      user,
      isAuthLoading,
      isAuthenticated: Boolean(user),
      isStaff: isStaffRole(user?.role),
      canCheckIn: canCheckInPasses(user?.role),
      canManageOps: canManageParkOperations(user?.role),
      isCloudSupabaseActive: isSupabaseCloudConfigured(),
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
    }),
    [
      user,
      isAuthLoading,
      pendingRedirectView,
      authPortalMode,
      login,
      registerClient,
      logout,
      changePassword,
      resetClientPassword,
      deleteMyAccount,
    ]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export function useAuth(): AuthContextType {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return ctx;
}
