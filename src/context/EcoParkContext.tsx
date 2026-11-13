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
  useRef,
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
import { runEcoViewTransition, emitTrailStatusWave } from '../utils/ecoMotion';
import { resolveViewFromPath, VIEW_PATH_MAP } from '../utils/ecoRouting';

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

  // Navigation state (resolved from URL pathname via shared ecoRouting engine)
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

  // Live synchronous refs so cross-domain mutators never read stale closures
  const trailsRef = useRef<Trail[]>(trails);
  trailsRef.current = trails;
  const passesRef = useRef<EcoPass[]>(passes);
  passesRef.current = passes;

  // Reconcile global on-site occupancy = open trails headcount + today's net booked pass delta
  const reconcileTodayOccupancy = useCallback(
    (trailsList: Trail[], passesList: EcoPass[], dailyMax: number): number => {
      const todayIso = new Date().toISOString().split('T')[0];
      const openTrailsOccupancy = trailsList
        .filter((t) => t.status !== 'ferme')
        .reduce((sum, t) => sum + t.currentOccupancy, 0);

      const seedTodayGuests = INITIAL_PASSES.filter(
        (p) => p.visitDate === todayIso && p.status !== 'cancelled'
      ).reduce((sum, p) => sum + p.guestCount, 0);

      const activeTodayGuests = passesList
        .filter((p) => p.visitDate === todayIso && p.status !== 'cancelled')
        .reduce((sum, p) => sum + p.guestCount, 0);

      const todayNetDelta = activeTodayGuests - seedTodayGuests;
      return Math.max(0, Math.min(dailyMax, openTrailsOccupancy + todayNetDelta));
    },
    []
  );

  // Browser Back / Forward URL history synchronization
  useEffect(() => {
    if (typeof window === 'undefined') return;
    const handlePopState = () => {
      const resolved = resolveViewFromPath(window.location.pathname) || 'accueil';
      safeLocalStorage.setItem(STORAGE_KEYS.ACTIVE_VIEW, resolved);
      setActiveViewState(resolved);
    };
    window.addEventListener('popstate', handlePopState);
    return () => window.removeEventListener('popstate', handlePopState);
  }, []);

  // --------------------------------------------------------------------------
  // Mutators with localStorage persistence
  // --------------------------------------------------------------------------

  const setActiveView = useCallback((view: ActiveView) => {
    safeLocalStorage.setItem(STORAGE_KEYS.ACTIVE_VIEW, view);
    if (typeof window !== 'undefined') {
      const targetPath = VIEW_PATH_MAP[view] || '/';
      if (window.location.pathname !== targetPath) {
        window.history.pushState({ ecoView: view }, '', targetPath);
      }
    }

    runEcoViewTransition('lisiere', () => {
      setActiveViewState(view);
      if (typeof window !== 'undefined') {
        window.scrollTo({ top: 0, behavior: 'instant' as ScrollBehavior });
      }
    });
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
      emitTrailStatusWave(trailId, status);
      const nextTrails = trailsRef.current.map((trail) => {
        if (trail.id !== trailId && trail.slug !== trailId) return trail;
        const updatedOccupancy =
          status === 'ferme'
            ? 0
            : trail.status === 'ferme'
            ? Math.floor(trail.maxCapacity * 0.4)
            : trail.currentOccupancy;

        const nextNotice =
          status === 'fluide'
            ? undefined
            : closureReason !== undefined
            ? closureReason
            : status === 'ferme'
            ? trail.closureReason || 'Fermeture préventive temporaire'
            : trail.closureReason || 'Circulation encadrée par les Éco-Gardes';

        return {
          ...trail,
          status,
          closureReason: nextNotice,
          currentOccupancy: updatedOccupancy,
        };
      });

      trailsRef.current = nextTrails;
      safeLocalStorage.setItem(STORAGE_KEYS.TRAILS, nextTrails);
      setTrailsState(nextTrails);

      // Reconcile global occupancy without clobbering today's active pass bookings
      setTelemetryState((prevTelem) => {
        const updatedTelem: ParkTelemetry = {
          ...prevTelem,
          currentOccupancy: reconcileTodayOccupancy(
            nextTrails,
            passesRef.current,
            prevTelem.dailyCapacityMax
          ),
        };
        safeLocalStorage.setItem(STORAGE_KEYS.TELEMETRY, updatedTelem);
        return updatedTelem;
      });
    },
    [reconcileTodayOccupancy]
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
        qrPayload: `ECOPARK-AHALA:PASS:${newId}:DATE=${input.visitDate}:SLOT=${input.timeSlot}:GUESTS=${input.guestCount}:FORMULE=${input.experienceType.toUpperCase()}:MODE=${input.mobilityMode}`,
      };

      const nextPasses = [newPass, ...passesRef.current];
      passesRef.current = nextPasses;
      safeLocalStorage.setItem(STORAGE_KEYS.PASSES, nextPasses);
      setPassesState(nextPasses);

      setActivePassId(newId);

      // Reconcile today's park occupancy (only increments if visitDate === today) & add avoided CO2
      setTelemetryState((prev) => {
        const next: ParkTelemetry = {
          ...prev,
          currentOccupancy: reconcileTodayOccupancy(
            trailsRef.current,
            nextPasses,
            prev.dailyCapacityMax
          ),
          totalCo2AvoidedKg: Number((prev.totalCo2AvoidedKg + input.co2AvoidedKg).toFixed(1)),
        };
        safeLocalStorage.setItem(STORAGE_KEYS.TELEMETRY, next);
        return next;
      });

      return newPass;
    },
    [reconcileTodayOccupancy, setActivePassId]
  );

  const cancelPass = useCallback(
    (passId: string) => {
      let wasCancelled = false;
      let releasedCo2Kg = 0;

      const nextPasses = passesRef.current.map((p) => {
        if (p.id === passId && p.status !== 'cancelled') {
          wasCancelled = true;
          releasedCo2Kg = p.co2AvoidedKg;
          return { ...p, status: 'cancelled' as const };
        }
        return p;
      });

      if (!wasCancelled) return;

      passesRef.current = nextPasses;
      safeLocalStorage.setItem(STORAGE_KEYS.PASSES, nextPasses);
      setPassesState(nextPasses);

      setTelemetryState((prevTelem) => {
        const updated: ParkTelemetry = {
          ...prevTelem,
          currentOccupancy: reconcileTodayOccupancy(
            trailsRef.current,
            nextPasses,
            prevTelem.dailyCapacityMax
          ),
          totalCo2AvoidedKg: Math.max(
            0,
            Number((prevTelem.totalCo2AvoidedKg - releasedCo2Kg).toFixed(1))
          ),
        };
        safeLocalStorage.setItem(STORAGE_KEYS.TELEMETRY, updated);
        return updated;
      });
    },
    [reconcileTodayOccupancy]
  );

  const checkInPass = useCallback((passId: string) => {
    const nowIso = new Date().toISOString();
    const next = passesRef.current.map((p) => {
      if (p.id === passId && p.status !== 'cancelled') {
        return { ...p, status: 'checked_in' as const, checkInTimestamp: nowIso };
      }
      return p;
    });
    passesRef.current = next;
    safeLocalStorage.setItem(STORAGE_KEYS.PASSES, next);
    setPassesState(next);
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
    trailsRef.current = INITIAL_TRAILS;
    passesRef.current = INITIAL_PASSES;

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
