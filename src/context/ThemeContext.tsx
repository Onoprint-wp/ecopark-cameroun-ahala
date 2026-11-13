// ============================================================================
// ECO-PARK THEME & VISION CONTEXT (src/context/ThemeContext.tsx)
// ============================================================================

import React, {
  createContext,
  useContext,
  useState,
  useEffect,
  useCallback,
  ReactNode,
} from 'react';
import {
  ThemeMode,
  EffectiveTheme,
  DaltonismMode,
  ThemeContextType,
} from '../types/ecosystem';
import { runEcoViewTransition } from '../utils/ecoMotion';

const THEME_STORAGE_KEY = 'eco_park_v1_theme';
const LEGACY_THEME_STORAGE_KEY = 'eco-park-theme';
const VISION_STORAGE_KEY = 'eco_park_v1_daltonism';
const LEGACY_VISION_STORAGE_KEY = 'eco-park-vision';
const HIGH_CONTRAST_STORAGE_KEY = 'eco_park_v1_high_contrast';

function safeGetStorage<T extends string>(keys: string[], fallback: T): T {
  if (typeof window === 'undefined') return fallback;
  for (const k of keys) {
    try {
      const val = localStorage.getItem(k);
      if (val) return val as T;
    } catch {
      // Continue to next key or fallback
    }
  }
  return fallback;
}

function safeSetStorage(key: string, value: string): void {
  if (typeof window === 'undefined') return;
  try {
    localStorage.setItem(key, value);
  } catch {
    // Gracefully handle storage quota or privacy mode errors
  }
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export interface ThemeProviderProps {
  children: ReactNode;
}

export const ThemeProvider: React.FC<ThemeProviderProps> = ({ children }) => {
  const [themeMode, setThemeModeState] = useState<ThemeMode>(() => {
    const saved = safeGetStorage<ThemeMode>([THEME_STORAGE_KEY, LEGACY_THEME_STORAGE_KEY], 'auto');
    if (saved === 'light' || saved === 'dark' || saved === 'auto') return saved;
    return 'auto';
  });

  const [daltonismMode, setDaltonismModeState] = useState<DaltonismMode>(() => {
    const saved = safeGetStorage<DaltonismMode>(
      [VISION_STORAGE_KEY, LEGACY_VISION_STORAGE_KEY],
      'normal'
    );
    if (
      saved === 'normal' ||
      saved === 'deuteranopia' ||
      saved === 'protanopia' ||
      saved === 'tritanopia'
    ) {
      return saved;
    }
    return 'normal';
  });

  const [highContrastOutdoor, setHighContrastOutdoorState] = useState<boolean>(() => {
    try {
      return localStorage.getItem(HIGH_CONTRAST_STORAGE_KEY) === 'true';
    } catch {
      return false;
    }
  });

  const [effectiveTheme, setEffectiveTheme] = useState<EffectiveTheme>('light');

  // Compute effective theme and update HTML attributes
  const syncThemeDOM = useCallback((mode: ThemeMode) => {
    if (typeof window === 'undefined') return;
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    let isDark = false;
    if (mode === 'dark') {
      isDark = true;
    } else if (mode === 'light') {
      isDark = false;
    } else {
      isDark = mediaQuery.matches;
    }

    const currentEffective: EffectiveTheme = isDark ? 'dark' : 'light';
    setEffectiveTheme(currentEffective);

    const root = document.documentElement;
    if (isDark) {
      root.classList.add('dark');
      root.setAttribute('data-theme', 'dark');
    } else {
      root.classList.remove('dark');
      root.setAttribute('data-theme', 'light');
    }
  }, []);

  // Update theme mode and persist (with Sunrise / OLED Extinguish View Transition)
  const setThemeMode = useCallback(
    (newMode: ThemeMode) => {
      safeSetStorage(THEME_STORAGE_KEY, newMode);
      safeSetStorage(LEGACY_THEME_STORAGE_KEY, newMode);

      if (typeof window === 'undefined') {
        setThemeModeState(newMode);
        return;
      }

      const osPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      const nextIsDark = newMode === 'dark' ? true : newMode === 'light' ? false : osPrefersDark;
      const prevIsDark = document.documentElement.classList.contains('dark');

      if (nextIsDark !== prevIsDark) {
        const vtKind = nextIsDark ? 'oled-extinguish' : 'sunrise';
        runEcoViewTransition(vtKind, () => {
          setThemeModeState(newMode);
          syncThemeDOM(newMode);
        });
      } else {
        setThemeModeState(newMode);
        syncThemeDOM(newMode);
      }
    },
    [syncThemeDOM]
  );

  // Update daltonism mode and persist
  const setDaltonismMode = useCallback((newVision: DaltonismMode) => {
    setDaltonismModeState(newVision);
    safeSetStorage(VISION_STORAGE_KEY, newVision);
    safeSetStorage(LEGACY_VISION_STORAGE_KEY, newVision);

    if (typeof document !== 'undefined') {
      const root = document.documentElement;
      if (newVision === 'normal') {
        root.removeAttribute('data-vision');
      } else {
        root.setAttribute('data-vision', newVision);
      }
    }
  }, []);

  // Update high contrast outdoor mode
  const setHighContrastOutdoor = useCallback((enabled: boolean) => {
    setHighContrastOutdoorState(enabled);
    safeSetStorage(HIGH_CONTRAST_STORAGE_KEY, String(enabled));
    if (typeof document !== 'undefined') {
      const root = document.documentElement;
      if (enabled) {
        root.setAttribute('data-outdoor-contrast', 'true');
      } else {
        root.removeAttribute('data-outdoor-contrast');
      }
    }
  }, []);

  // Synchronize on mount and listen to OS media query changes
  useEffect(() => {
    syncThemeDOM(themeMode);

    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    const handleSystemChange = () => {
      if (themeMode === 'auto') {
        syncThemeDOM('auto');
      }
    };

    mediaQuery.addEventListener('change', handleSystemChange);
    return () => mediaQuery.removeEventListener('change', handleSystemChange);
  }, [themeMode, syncThemeDOM]);

  // Synchronize daltonism on mount
  useEffect(() => {
    const root = document.documentElement;
    if (daltonismMode === 'normal') {
      root.removeAttribute('data-vision');
    } else {
      root.setAttribute('data-vision', daltonismMode);
    }
  }, [daltonismMode]);

  // Synchronize outdoor contrast on mount
  useEffect(() => {
    const root = document.documentElement;
    if (highContrastOutdoor) {
      root.setAttribute('data-outdoor-contrast', 'true');
    } else {
      root.removeAttribute('data-outdoor-contrast');
    }
  }, [highContrastOutdoor]);

  // Listen to cross-tab storage changes
  useEffect(() => {
    const handleStorage = (e: StorageEvent) => {
      if (!e.key) return;
      if (e.key === THEME_STORAGE_KEY || e.key === LEGACY_THEME_STORAGE_KEY) {
        if (e.newValue === 'light' || e.newValue === 'dark' || e.newValue === 'auto') {
          setThemeModeState(e.newValue);
          syncThemeDOM(e.newValue);
        }
      } else if (e.key === VISION_STORAGE_KEY || e.key === LEGACY_VISION_STORAGE_KEY) {
        if (
          e.newValue === 'normal' ||
          e.newValue === 'deuteranopia' ||
          e.newValue === 'protanopia' ||
          e.newValue === 'tritanopia'
        ) {
          setDaltonismMode(e.newValue);
        }
      } else if (e.key === HIGH_CONTRAST_STORAGE_KEY) {
        setHighContrastOutdoor(e.newValue === 'true');
      }
    };

    window.addEventListener('storage', handleStorage);
    return () => window.removeEventListener('storage', handleStorage);
  }, [syncThemeDOM, setDaltonismMode, setHighContrastOutdoor]);

  return (
    <ThemeContext.Provider
      value={{
        themeMode,
        effectiveTheme,
        setThemeMode,
        daltonismMode,
        setDaltonismMode,
        highContrastOutdoor,
        setHighContrastOutdoor,
      }}
    >
      {children}
    </ThemeContext.Provider>
  );
};

export function useTheme(): ThemeContextType {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
}
