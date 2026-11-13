// ============================================================================
// ECO-PARK CENTRAL REACTIVE STORE (src/context/EcoParkContext.tsx)
// ============================================================================

import React, {
  createContext,
  useContext,
  useState,
  useEffect,
  useCallback,
  useMemo,
  ReactNode,
} from 'react';
import {
  ActiveView,
  Trail,
  TrailStatus,
  EcoPass,
  BookingInput,
  CitizenReport,
  ReportInput,
  ReportStatus,
  ParkTelemetry,
  EcoParkContextType,
} from '../types/ecosystem';
import {
  INITIAL_TELEMETRY,
  INITIAL_POIS,
  INITIAL_TRAILS,
  INITIAL_SPECIES,
  INITIAL_PASSES,
  INITIAL_REPORTS,
} from '../data/initialParkData';
import { useTheme } from './ThemeContext';

// Storage keys under strict eco_park_ahala_v2_* namespace
export const STORAGE_KEYS = {
  TRAILS: 'eco_park_ahala_v2_trails',
  TELEMETRY: 'eco_park_ahala_v2_telemetry',
  PASSES: 'eco_park_ahala_v2_passes',
  REPORTS: 'eco_park_ahala_v2_reports',
  ACTIVE_VIEW: 'eco_park_ahala_v2_active_view',
  SELECTED_TRAIL: 'eco_park_ahala_v2_selected_trail',
  SELECTED_SPECIES: 'eco_park_ahala_v2_selected_species',
  ACTIVE_PASS_ID: 'eco_park_ahala_v2_active_pass_id',
  DRAWER_OPEN: 'eco_park_ahala_v2_drawer_open',
};

// Resilient safeLocalStorage helper wrapping all browser storage operations
export const safeLocalStorage = {
  getItem: <T,>(key: string, fallback: T): T => {
    if (typeof window === 'undefined') return fallback;
    try {
      const item = window.localStorage.getItem(key);
      if (item === null) return fallback;
      return JSON.parse(item) as T;
    } catch (err) {
      console.warn(`[safeLocalStorage] Failed to parse key "${key}", reverting to fallback:`, err);
      return fallback;
    }
  },
  setItem: <T,>(key: string, value: T): void => {
    if (typeof window === 'undefined') return;
    try {
      window.localStorage.setItem(key, JSON.stringify(value));
    } catch (err) {
      console.warn(`[safeLocalStorage] Failed to write key "${key}":`, err);
    }
  },
  removeItem: (key: string): void => {
    if (typeof window === 'undefined') return;
    try {
      window.localStorage.removeItem(key);
    } catch (err) {
      console.warn(`[safeLocalStorage] Failed to remove key "${key}":`, err);
    }
  },
};

const EcoParkContext = createContext<EcoParkContextType | undefined>(undefined);

export interface EcoParkProviderProps {
  children: ReactNode;
}

export const EcoParkProvider: React.FC<EcoParkProviderProps> = ({ children }) => {
  // Theme context bridge
  const {
    themeMode,
    effectiveTheme,
    setThemeMode,
    daltonismMode,
    setDaltonismMode,
    highContrastOutdoor,
    setHighContrastOutdoor,
  } = useTheme();

  // Resolve initial view from production URL pathname if present
  const resolveViewFromPath = (pathname: string): ActiveView | null => {
    const clean = pathname.replace(/\/+$/, '').toLowerCase();
    if (clean === '/activites' || clean === '/fiche-activite') return 'sentiers';
    if (clean === '/reserver' || clean === '/rdv' || clean === '/rendez-vous') return 'billetterie';
    if (clean === '/mon-espace' || clean === '/mes-reservations') return 'pass';
    if (clean === '/exploitation' || clean === '/guichet' || clean === '/direction' || clean === '/admin') return 'ranger';
    if (
      clean === '/hebergements' ||
      clean === '/hotellerie' ||
      clean === '/sejour-restaurant' ||
      clean === '/restaurant' ||
      clean === '/tarifs' ||
      clean === '/nos-tarifs' ||
      clean === '/pack-entreprise' ||
      clean === '/pack-ecole' ||
      clean === '/groupes-evenements' ||
      clean === '/formation' ||
      clean === '/formations' ||
      clean === '/decouvrir'
    ) {
      return 'accueil';
    }
    return null;
  };

  // Navigation state
  const [activeView, setActiveViewState] = useState<ActiveView>(() => {
    if (typeof window !== 'undefined') {
      const fromUrl = resolveViewFromPath(window.location.pathname);
      if (fromUrl) return fromUrl;
    }
    return safeLocalStorage.getItem<ActiveView>(STORAGE_KEYS.ACTIVE_VIEW, 'accueil');
  });

  // Architectural slide-over drawer state
  const [colorDrawerOpen, setColorDrawerOpenState] = useState<boolean>(() =>
    safeLocalStorage.getItem<boolean>(STORAGE_KEYS.DRAWER_OPEN, false)
  );

  // Telemetry & capacity state
  const [telemetry, setTelemetryState] = useState<ParkTelemetry>(() =>
    safeLocalStorage.getItem<ParkTelemetry>(STORAGE_KEYS.TELEMETRY, INITIAL_TELEMETRY)
  );

  // Trails state
  const [trails, setTrailsState] = useState<Trail[]>(() =>
    safeLocalStorage.getItem<Trail[]>(STORAGE_KEYS.TRAILS, INITIAL_TRAILS)
  );

  // Selection states
  const [selectedTrailId, setSelectedTrailIdState] = useState<string | null>(() =>
    safeLocalStorage.getItem<string | null>(STORAGE_KEYS.SELECTED_TRAIL, null)
  );

  const [selectedSpeciesId, setSelectedSpeciesIdState] = useState<string | null>(() =>
    safeLocalStorage.getItem<string | null>(STORAGE_KEYS.SELECTED_SPECIES, null)
  );

  // Booked Passes state
  const [passes, setPassesState] = useState<EcoPass[]>(() =>
    safeLocalStorage.getItem<EcoPass[]>(STORAGE_KEYS.PASSES, INITIAL_PASSES)
  );

  const [activePassId, setActivePassIdState] = useState<string | null>(() =>
    safeLocalStorage.getItem<string | null>(STORAGE_KEYS.ACTIVE_PASS_ID, 'ECP-2026-8942')
  );

  // Citizen Reports state
  const [reports, setReportsState] = useState<CitizenReport[]>(() =>
    safeLocalStorage.getItem<CitizenReport[]>(STORAGE_KEYS.REPORTS, INITIAL_REPORTS)
  );

  // --------------------------------------------------------------------------
  // Mutators with localStorage persistence
  // --------------------------------------------------------------------------

  const setActiveView = useCallback((view: ActiveView) => {
    setActiveViewState(view);
    safeLocalStorage.setItem(STORAGE_KEYS.ACTIVE_VIEW, view);
    if (typeof window !== 'undefined') {
      const viewPathMap: Record<ActiveView, string> = {
        accueil: '/',
        sentiers: '/activites',
        biodiversite: '/decouvrir',
        billetterie: '/reserver',
        pass: '/mon-espace',
        ranger: '/exploitation',
        color_atlas: '/',
      };
      const targetPath = viewPathMap[view] || '/';
      if (window.location.pathname !== targetPath) {
        window.history.replaceState(null, '', targetPath);
      }
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  }, []);

  const setColorDrawerOpen = useCallback((open: boolean) => {
    setColorDrawerOpenState(open);
    safeLocalStorage.setItem(STORAGE_KEYS.DRAWER_OPEN, open);
  }, []);

  const setDailyCapacity = useCallback((newCap: number) => {
    setTelemetryState((prev) => {
      const updated: ParkTelemetry = {
        ...prev,
        dailyCapacityMax: Math.max(500, Math.min(3000, newCap)),
      };
      safeLocalStorage.setItem(STORAGE_KEYS.TELEMETRY, updated);
      return updated;
    });
  }, []);

  const updateTrailStatus = useCallback(
    (trailId: string, status: TrailStatus, closureReason?: string) => {
      setTrailsState((prevTrails) => {
        const nextTrails = prevTrails.map((trail) => {
          if (trail.id !== trailId && trail.slug !== trailId) return trail;
          const updatedOccupancy =
            status === 'ferme' ? 0 : trail.status === 'ferme' ? Math.floor(trail.maxCapacity * 0.4) : trail.currentOccupancy;
          return {
            ...trail,
            status,
            closureReason: status === 'ferme' ? closureReason || 'Fermeture préventive temporaire' : undefined,
            currentOccupancy: updatedOccupancy,
          };
        });
        safeLocalStorage.setItem(STORAGE_KEYS.TRAILS, nextTrails);

        // Recalculate global occupancy based on open trails and baseline bookings
        const openTrailsOccupancy = nextTrails
          .filter((t) => t.status !== 'ferme')
          .reduce((sum, t) => sum + t.currentOccupancy, 0);

        setTelemetryState((prevTelem) => {
          const updatedTelem: ParkTelemetry = {
            ...prevTelem,
            currentOccupancy: Math.min(prevTelem.dailyCapacityMax, openTrailsOccupancy),
          };
          safeLocalStorage.setItem(STORAGE_KEYS.TELEMETRY, updatedTelem);
          return updatedTelem;
        });

        return nextTrails;
      });
    },
    []
  );

  const setSelectedTrailId = useCallback((trailId: string | null) => {
    setSelectedTrailIdState(trailId);
    safeLocalStorage.setItem(STORAGE_KEYS.SELECTED_TRAIL, trailId);
  }, []);

  const setSelectedSpeciesId = useCallback((speciesId: string | null) => {
    setSelectedSpeciesIdState(speciesId);
    safeLocalStorage.setItem(STORAGE_KEYS.SELECTED_SPECIES, speciesId);
  }, []);

  const setActivePassId = useCallback((id: string | null) => {
    setActivePassIdState(id);
    safeLocalStorage.setItem(STORAGE_KEYS.ACTIVE_PASS_ID, id);
  }, []);

  const bookPass = useCallback(
    (input: BookingInput): EcoPass => {
      const randomDigits = Math.floor(10000 + Math.random() * 90000);
      const newId = `ECP-2026-${randomDigits}`;
      const nowIso = new Date().toISOString();

      const newPass: EcoPass = {
        ...input,
        id: newId,
        createdAt: nowIso,
        status: 'confirmed',
        qrPayload: `ECOPARK-AHALA:PASS:${newId}:DATE=${input.visitDate}:SLOT=${input.timeSlot}:GUESTS=${input.guestCount}:MODE=${input.mobilityMode}`,
      };

      setPassesState((prev) => {
        const next = [newPass, ...prev];
        safeLocalStorage.setItem(STORAGE_KEYS.PASSES, next);
        return next;
      });

      setActivePassId(newId);

      // Increment park telemetry occupancy and avoided CO2
      setTelemetryState((prev) => {
        const next: ParkTelemetry = {
          ...prev,
          currentOccupancy: Math.min(prev.dailyCapacityMax, prev.currentOccupancy + input.guestCount),
          totalCo2AvoidedKg: Number((prev.totalCo2AvoidedKg + input.co2AvoidedKg).toFixed(1)),
        };
        safeLocalStorage.setItem(STORAGE_KEYS.TELEMETRY, next);
        return next;
      });

      return newPass;
    },
    [setActivePassId]
  );

  const cancelPass = useCallback((passId: string) => {
    setPassesState((prev) => {
      let releasedGuests = 0;
      const next = prev.map((p) => {
        if (p.id === passId && p.status !== 'cancelled') {
          releasedGuests = p.guestCount;
          return { ...p, status: 'cancelled' as const };
        }
        return p;
      });
      safeLocalStorage.setItem(STORAGE_KEYS.PASSES, next);

      if (releasedGuests > 0) {
        setTelemetryState((prevTelem) => {
          const updated: ParkTelemetry = {
            ...prevTelem,
            currentOccupancy: Math.max(0, prevTelem.currentOccupancy - releasedGuests),
          };
          safeLocalStorage.setItem(STORAGE_KEYS.TELEMETRY, updated);
          return updated;
        });
      }
      return next;
    });
  }, []);

  const checkInPass = useCallback((passId: string) => {
    setPassesState((prev) => {
      const nowIso = new Date().toISOString();
      const next = prev.map((p) => {
        if (p.id === passId) {
          return { ...p, status: 'checked_in' as const, checkInTimestamp: nowIso };
        }
        return p;
      });
      safeLocalStorage.setItem(STORAGE_KEYS.PASSES, next);
      return next;
    });
  }, []);

  const submitCitizenReport = useCallback((input: ReportInput): CitizenReport => {
    const reportIndex = Math.floor(100 + Math.random() * 900);
    const newId = `REP-2026-${reportIndex}`;
    const nowIso = new Date().toISOString();

    const newReport: CitizenReport = {
      ...input,
      id: newId,
      timestamp: nowIso,
      status: 'en_attente',
      upvotes: 0,
    };

    setReportsState((prev) => {
      const next = [newReport, ...prev];
      safeLocalStorage.setItem(STORAGE_KEYS.REPORTS, next);
      return next;
    });

    return newReport;
  }, []);

  const updateReportStatus = useCallback(
    (reportId: string, status: ReportStatus, rangerNote?: string) => {
      setReportsState((prev) => {
        const next = prev.map((rep) => {
          if (rep.id === reportId) {
            return {
              ...rep,
              status,
              rangerNote: rangerNote !== undefined ? rangerNote : rep.rangerNote,
              resolvedAt: status === 'resolu' ? new Date().toISOString() : rep.resolvedAt,
            };
          }
          return rep;
        });
        safeLocalStorage.setItem(STORAGE_KEYS.REPORTS, next);
        return next;
      });
    },
    []
  );

  const upvoteReport = useCallback((reportId: string) => {
    setReportsState((prev) => {
      const next = prev.map((rep) => {
        if (rep.id === reportId) {
          return { ...rep, upvotes: rep.upvotes + 1 };
        }
        return rep;
      });
      safeLocalStorage.setItem(STORAGE_KEYS.REPORTS, next);
      return next;
    });
  }, []);

  const resetToSeedData = useCallback(() => {
    safeLocalStorage.setItem(STORAGE_KEYS.TRAILS, INITIAL_TRAILS);
    safeLocalStorage.setItem(STORAGE_KEYS.TELEMETRY, INITIAL_TELEMETRY);
    safeLocalStorage.setItem(STORAGE_KEYS.PASSES, INITIAL_PASSES);
    safeLocalStorage.setItem(STORAGE_KEYS.REPORTS, INITIAL_REPORTS);
    safeLocalStorage.setItem(STORAGE_KEYS.ACTIVE_VIEW, 'accueil');
    safeLocalStorage.setItem(STORAGE_KEYS.SELECTED_TRAIL, null);
    safeLocalStorage.setItem(STORAGE_KEYS.SELECTED_SPECIES, null);
    safeLocalStorage.setItem(STORAGE_KEYS.ACTIVE_PASS_ID, 'ECP-2026-8942');
    safeLocalStorage.setItem(STORAGE_KEYS.DRAWER_OPEN, false);

    setTrailsState(INITIAL_TRAILS);
    setTelemetryState(INITIAL_TELEMETRY);
    setPassesState(INITIAL_PASSES);
    setReportsState(INITIAL_REPORTS);
    setActiveViewState('accueil');
    setSelectedTrailIdState(null);
    setSelectedSpeciesIdState(null);
    setActivePassIdState('ECP-2026-8942');
    setColorDrawerOpenState(false);
  }, []);

  // --------------------------------------------------------------------------
  // Cross-Tab Reactivity via window storage event
  // --------------------------------------------------------------------------
  useEffect(() => {
    const handleStorageEvent = (event: StorageEvent) => {
      if (!event.key || event.newValue === null) return;

      try {
        if (event.key === STORAGE_KEYS.TRAILS) {
          setTrailsState(JSON.parse(event.newValue));
        } else if (event.key === STORAGE_KEYS.TELEMETRY) {
          setTelemetryState(JSON.parse(event.newValue));
        } else if (event.key === STORAGE_KEYS.PASSES) {
          setPassesState(JSON.parse(event.newValue));
        } else if (event.key === STORAGE_KEYS.REPORTS) {
          setReportsState(JSON.parse(event.newValue));
        } else if (event.key === STORAGE_KEYS.ACTIVE_VIEW) {
          setActiveViewState(JSON.parse(event.newValue));
        } else if (event.key === STORAGE_KEYS.SELECTED_TRAIL) {
          setSelectedTrailIdState(JSON.parse(event.newValue));
        } else if (event.key === STORAGE_KEYS.SELECTED_SPECIES) {
          setSelectedSpeciesIdState(JSON.parse(event.newValue));
        } else if (event.key === STORAGE_KEYS.ACTIVE_PASS_ID) {
          setActivePassIdState(JSON.parse(event.newValue));
        } else if (event.key === STORAGE_KEYS.DRAWER_OPEN) {
          setColorDrawerOpenState(JSON.parse(event.newValue));
        }
      } catch (err) {
        console.warn('[EcoParkContext] Error syncing cross-tab event:', err);
      }
    };

    window.addEventListener('storage', handleStorageEvent);
    return () => window.removeEventListener('storage', handleStorageEvent);
  }, []);

  // Compute active pass
  const activePass = useMemo(() => {
    if (!activePassId) return passes[0] || null;
    return passes.find((p) => p.id === activePassId) || passes[0] || null;
  }, [passes, activePassId]);

  const value: EcoParkContextType = {
    // Navigation & View
    activeView,
    setActiveView,

    // Theming & Daltonism
    themeMode,
    effectiveTheme,
    setThemeMode,
    daltonismMode,
    setDaltonismMode,
    colorDrawerOpen,
    setColorDrawerOpen,
    highContrastOutdoor,
    setHighContrastOutdoor,

    // Telemetry & Capacity
    telemetry,
    setDailyCapacity,

    // Trails
    trails,
    updateTrailStatus,
    selectedTrailId,
    setSelectedTrailId,

    // Points of interest (reference constant)
    pois: INITIAL_POIS,

    // Species
    species: INITIAL_SPECIES,
    selectedSpeciesId,
    setSelectedSpeciesId,

    // Bookings & Passes
    passes,
    activePass,
    activePassId,
    setActivePassId,
    bookPass,
    cancelPass,
    checkInPass,

    // Citizen Sentinel
    reports,
    submitCitizenReport,
    updateReportStatus,
    upvoteReport,

    // State Management & Reset
    resetToSeedData,
  };

  return <EcoParkContext.Provider value={value}>{children}</EcoParkContext.Provider>;
};

export function useEcoPark(): EcoParkContextType {
  const context = useContext(EcoParkContext);
  if (!context) {
    throw new Error('useEcoPark must be used within an EcoParkProvider');
  }
  return context;
}
