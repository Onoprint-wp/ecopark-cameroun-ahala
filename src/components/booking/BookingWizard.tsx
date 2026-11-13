// ============================================================================
// 3-STEP QUOTA BOOKING WIZARD (src/components/booking/BookingWizard.tsx)
// Feature F20 & F21: Ecological quota regulation & carbon discount engine
// ============================================================================

import React, { useState, useMemo } from 'react';
import {
  Calendar,
  Clock,
  Users,
  ShieldCheck,
  CheckCircle2,
  AlertTriangle,
  ArrowRight,
  ArrowLeft,
  Leaf,
  Train,
  Bus,
  Bike,
  Car,
  Check,
  Sparkles,
  Footprints,
} from 'lucide-react';
import { useEcoPark } from '../../context/EcoParkContext';
import {
  ExperienceType,
  TimeSlot,
  MobilityMode,
  BookingInput,
} from '../../types/ecosystem';
import {
  EXPERIENCES_CATALOG,
  MOBILITY_OPTIONS,
  calculateEcoMobilityPricing,
  formatEur,
  formatCo2,
} from '../../utils/ecoMobility';

export const BookingWizard: React.FC = () => {
  const {
    telemetry,
    passes,
    bookPass,
    setActiveView,
    setActivePassId,
  } = useEcoPark();

  // Wizard state
  const [currentStep, setCurrentStep] = useState<1 | 2 | 3>(1);

  // Step 1: Experience & Date
  const [experienceType, setExperienceType] = useState<ExperienceType>('sentiers');
  const todayStr = useMemo(() => new Date().toISOString().split('T')[0], []);
  const [visitDate, setVisitDate] = useState<string>(todayStr);

  // Step 2: Timeslot, Guests & Lead Visitor
  const [timeSlot, setTimeSlot] = useState<TimeSlot>('08h30 - 11h30');
  const [adultCount, setAdultCount] = useState<number>(2);
  const [childCount, setChildCount] = useState<number>(0);
  const [pmrCount, setPmrCount] = useState<number>(0);

  const [leadName, setLeadName] = useState<string>('');
  const [leadEmail, setLeadEmail] = useState<string>('');
  const [leadPhone, setLeadPhone] = useState<string>('06 82 45 19 33');

  // Step 3: Eco-Mobility & Charter
  const [mobilityMode, setMobilityMode] = useState<MobilityMode>('train');
  const [charterAccepted, setCharterAccepted] = useState<boolean>(false);

  // Validation errors
  const [formErrors, setFormErrors] = useState<Record<string, string>>({});
  const [bookingSuccess, setBookingSuccess] = useState<string | null>(null);

  // Total guests
  const totalGuests = adultCount + childCount + pmrCount;

  // Real-time capacity check for selected date
  const capacityMetrics = useMemo(() => {
    let bookedForDate = 0;
    if (visitDate === todayStr) {
      bookedForDate = telemetry.currentOccupancy;
    } else {
      bookedForDate = passes
        .filter((p) => p.visitDate === visitDate && p.status !== 'cancelled')
        .reduce((sum, p) => sum + p.guestCount, 0);
      // Realistic baseline for future days
      if (bookedForDate === 0) {
        bookedForDate = Math.round(telemetry.dailyCapacityMax * 0.45);
      }
    }

    const available = Math.max(0, telemetry.dailyCapacityMax - bookedForDate);
    const occupancyRatio = Math.min(
      100,
      Math.round((bookedForDate / telemetry.dailyCapacityMax) * 100)
    );

    return {
      dailyMax: telemetry.dailyCapacityMax,
      currentBooked: bookedForDate,
      available,
      occupancyRatio,
      isOverbooked: totalGuests > available,
    };
  }, [visitDate, todayStr, telemetry.dailyCapacityMax, telemetry.currentOccupancy, passes, totalGuests]);

  // Dynamic pricing breakdown
  const pricing = useMemo(() => {
    return calculateEcoMobilityPricing(
      experienceType,
      mobilityMode,
      adultCount,
      childCount,
      pmrCount
    );
  }, [experienceType, mobilityMode, adultCount, childCount, pmrCount]);

  // Timeslot catalog with contextual labels
  const TIMESLOTS: { id: TimeSlot; label: string; period: string; recommendation: string }[] = [
    {
      id: '08h30 - 11h30',
      label: '08h30 - 11h30',
      period: 'Matinée Canopée',
      recommendation: 'Idéal faune & fraîcheur matinale',
    },
    {
      id: '11h30 - 14h30',
      label: '11h30 - 14h30',
      period: 'Zénith Botanique',
      recommendation: 'Parfait pour pause panoramique & sentiers ombragés',
    },
    {
      id: '14h30 - 17h30',
      label: '14h30 - 17h30',
      period: 'Après-Midi Panorama',
      recommendation: 'Lumière rasante sur les crêtes rocheuses',
    },
    {
      id: '17h30 - 20h00',
      label: '17h30 - 20h00',
      period: 'Crépuscule Doré',
      recommendation: 'Sortie des rapaces nocturnes & observation silence',
    },
  ];

  // Helper icons for transport
  const renderMobilityIcon = (mode: MobilityMode) => {
    switch (mode) {
      case 'velo':
        return <Bike className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />;
      case 'train':
        return <Train className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />;
      case 'navette_electrique':
        return <Bus className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />;
      case 'covoiturage':
        return <Users className="w-5 h-5 text-amber-600 dark:text-amber-400" />;
      case 'voiture_solo':
        return <Car className="w-5 h-5 text-[var(--text-muted)]" />;
    }
  };

  // Step 1 Validation
  const validateStep1 = () => {
    if (!visitDate) {
      setFormErrors({ date: 'Veuillez sélectionner une date de visite.' });
      return false;
    }
    if (capacityMetrics.available <= 0) {
      setFormErrors({
        capacity: 'Le quota écologique est complet pour cette date. Choisissez une autre date.',
      });
      return false;
    }
    setFormErrors({});
    return true;
  };

  // Step 2 Validation
  const validateStep2 = () => {
    const errors: Record<string, string> = {};
    if (totalGuests <= 0) {
      errors.guests = 'Veuillez inclure au moins un visiteur.';
    }
    if (totalGuests > capacityMetrics.available) {
      errors.capacity = `Capacité insuffisante : seulement ${capacityMetrics.available} places restantes pour cette date.`;
    }
    if (!leadName.trim()) {
      errors.leadName = 'Le nom du visiteur référent est obligatoire.';
    }
    if (!leadEmail.trim() || !leadEmail.includes('@') || !leadEmail.includes('.')) {
      errors.leadEmail = 'Une adresse email valide est requise pour recevoir l Éco-Pass.';
    }
    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  // Step 3 Validation & Submit
  const handleFinalBooking = (e: React.FormEvent) => {
    e.preventDefault();
    if (!charterAccepted) {
      setFormErrors({ charter: 'Vous devez accepter la Charte Zéro-Trace pour valider le pass.' });
      return;
    }

    const bookingInput: BookingInput = {
      visitDate,
      timeSlot,
      experienceType,
      guestCount: totalGuests,
      adultCount,
      childCount,
      pmrCount,
      mobilityMode,
      co2AvoidedKg: pricing.totalCo2AvoidedKg,
      discountAppliedPercent: pricing.discountPercent,
      unitPriceEur: pricing.unitPriceEur,
      totalPriceEur: pricing.netTotalEur,
      leadVisitor: {
        fullName: leadName.trim(),
        email: leadEmail.trim(),
        phone: leadPhone.trim(),
      },
      zeroTraceCharterSigned: true,
    };

    const newPass = bookPass(bookingInput);
    setActivePassId(newPass.id);
    setBookingSuccess(newPass.id);

    // Short timeout to transition to pass view
    setTimeout(() => {
      setActiveView('pass');
    }, 1200);
  };

  return (
    <div className="space-y-8">
      {/* Step Progress Header */}
      <div className="p-4 sm:p-6 rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-default)] shadow-xs">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <span className="text-xs font-semibold tracking-wider text-[var(--brand-primary)] uppercase">
              Parcours de Réservation Éco-Régulé
            </span>
            <h2 className="font-['Fraunces'] text-xl sm:text-2xl font-bold text-[var(--text-primary)] mt-0.5">
              Étape {currentStep} sur 3 :{' '}
              {currentStep === 1 && 'Expérience & Date Régulée'}
              {currentStep === 2 && 'Créneau Horodaté & Visiteurs'}
              {currentStep === 3 && 'Éco-Mobilité & Charte Zéro-Trace'}
            </h2>
          </div>

          {/* Step Bubbles */}
          <div className="flex items-center gap-2">
            {[1, 2, 3].map((stepNum) => {
              const isPast = currentStep > stepNum;
              const isCurrent = currentStep === stepNum;
              return (
                <div key={stepNum} className="flex items-center">
                  <div
                    className={`w-9 h-9 rounded-full flex items-center justify-center text-xs font-bold transition-all ${
                      isCurrent
                        ? 'bg-[var(--brand-primary)] text-white ring-4 ring-[var(--brand-primary)]/20 shadow-xs'
                        : isPast
                        ? 'bg-emerald-600 text-white'
                        : 'bg-[var(--bg-elevated)] text-[var(--text-muted)] border border-[var(--border-default)]'
                    }`}
                  >
                    {isPast ? <Check className="w-4 h-4 stroke-[3]" /> : stepNum}
                  </div>
                  {stepNum < 3 && (
                    <div
                      className={`w-6 sm:w-10 h-0.5 mx-1 transition-colors ${
                        isPast ? 'bg-emerald-600' : 'bg-[var(--border-default)]'
                      }`}
                    />
                  )}
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Booking Success Banner */}
      {bookingSuccess && (
        <div className="p-6 rounded-2xl bg-emerald-50 dark:bg-emerald-950/80 border border-emerald-400 dark:border-emerald-700 text-emerald-950 dark:text-emerald-100 flex items-center gap-4 animate-fade-in shadow-md">
          <div className="p-3 rounded-xl bg-emerald-600 text-white shrink-0">
            <CheckCircle2 className="w-6 h-6" />
          </div>
          <div>
            <h3 className="font-['Fraunces'] text-lg font-bold">
              Éco-Pass émis avec succès !
            </h3>
            <p className="text-xs text-emerald-800 dark:text-emerald-200 mt-1">
              Référence : <span className="font-mono font-bold">{bookingSuccess}</span>. Redirection immédiate vers votre compagnon terrain vectoriel...
            </p>
          </div>
        </div>
      )}

      {/* =================================================================== */}
      {/* ÉTAPE 1 : CHOIX DE L'EXPÉRIENCE & DATE                              */}
      {/* =================================================================== */}
      {currentStep === 1 && (
        <div className="space-y-6">
          {/* Real-Time Capacity Threshold Indicator */}
          <div className="p-5 rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-default)] space-y-3">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <div className="flex items-center gap-2">
                <Footprints className="w-5 h-5 text-[var(--brand-primary)]" />
                <span className="font-semibold text-sm text-[var(--text-primary)]">
                  Jauge écologique pour le {visitDate}
                </span>
              </div>
              <div className="text-xs font-mono font-bold">
                <span
                  className={
                    capacityMetrics.occupancyRatio >= 90
                      ? 'text-red-600 dark:text-red-400'
                      : capacityMetrics.occupancyRatio >= 70
                      ? 'text-amber-600 dark:text-amber-400'
                      : 'text-emerald-600 dark:text-emerald-400'
                  }
                >
                  {capacityMetrics.available} places disponibles
                </span>{' '}
                <span className="text-[var(--text-muted)] font-normal">
                  / {capacityMetrics.dailyMax} max
                </span>
              </div>
            </div>

            {/* Gauge bar */}
            <div className="w-full h-3 rounded-full bg-[var(--bg-elevated)] border border-[var(--border-default)] overflow-hidden">
              <div
                className={`h-full transition-all duration-500 rounded-full ${
                  capacityMetrics.occupancyRatio >= 90
                    ? 'bg-red-500'
                    : capacityMetrics.occupancyRatio >= 70
                    ? 'bg-amber-500'
                    : 'bg-[#52B788]'
                }`}
                style={{ width: `${capacityMetrics.occupancyRatio}%` }}
              />
            </div>
            <p className="text-[11px] text-[var(--text-muted)]">
              Le plafond est fixé par le garde-forestier pour protéger les périodes sensibles de reproduction et éviter l érosion des sentiers.
            </p>
          </div>

          {/* Date Selector */}
          <div className="p-6 rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-default)] space-y-4">
            <div className="flex items-center gap-2">
              <Calendar className="w-4 h-4 text-[var(--brand-primary)]" />
              <label htmlFor="visit-date-input" className="font-bold text-sm text-[var(--text-primary)]">
                Date de visite souhaitée
              </label>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 items-center">
              <div>
                <input
                  id="visit-date-input"
                  type="date"
                  value={visitDate}
                  min={todayStr}
                  onChange={(e) => setVisitDate(e.target.value)}
                  className="w-full px-4 py-2.5 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)] text-sm text-[var(--text-primary)] focus:outline-none focus:ring-2 focus:ring-[var(--brand-primary)] cursor-pointer"
                />
              </div>

              <div className="text-xs text-[var(--text-muted)] leading-relaxed">
                Réservations ouvertes jusqu à 30 jours à l avance. En cas de fermeture météo imprévue, votre pass est automatiquement reporté.
              </div>
            </div>

            {formErrors.date && (
              <p className="text-xs text-red-600 dark:text-red-400 font-semibold flex items-center gap-1.5">
                <AlertTriangle className="w-3.5 h-3.5" />
                {formErrors.date}
              </p>
            )}
            {formErrors.capacity && (
              <p className="text-xs text-red-600 dark:text-red-400 font-semibold flex items-center gap-1.5">
                <AlertTriangle className="w-3.5 h-3.5" />
                {formErrors.capacity}
              </p>
            )}
          </div>

          {/* Experiences Grid */}
          <div className="space-y-3">
            <h3 className="font-['Fraunces'] text-lg font-bold text-[var(--text-primary)]">
              Sélectionnez votre formule de découverte
            </h3>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {EXPERIENCES_CATALOG.map((exp) => {
                const isSelected = experienceType === exp.id;
                return (
                  <div
                    key={exp.id}
                    onClick={() => setExperienceType(exp.id)}
                    className={`p-5 rounded-2xl border transition-all cursor-pointer flex flex-col justify-between ${
                      isSelected
                        ? 'bg-[var(--bg-elevated)] border-[var(--brand-primary)] shadow-md ring-2 ring-[var(--brand-primary)]/20'
                        : 'bg-[var(--bg-surface)] border-[var(--border-default)] hover:border-[var(--brand-primary)]/60 hover:bg-[var(--bg-elevated)]'
                    }`}
                  >
                    <div className="space-y-2">
                      <div className="flex items-center justify-between gap-2">
                        <span className="text-[11px] font-mono font-bold uppercase tracking-wider text-[var(--brand-primary)]">
                          {exp.badge}
                        </span>
                        <span className="font-['Fraunces'] font-bold text-base text-[var(--text-primary)]">
                          {exp.adultPrice} € <span className="text-xs font-normal text-[var(--text-muted)]">/ adulte</span>
                        </span>
                      </div>

                      <h4 className="font-['Fraunces'] text-base font-bold text-[var(--text-primary)]">
                        {exp.title}
                      </h4>

                      <p className="text-xs text-[var(--text-muted)] leading-relaxed">
                        {exp.description}
                      </p>

                      <ul className="pt-2 space-y-1 text-xs text-[var(--text-primary)]">
                        {exp.features.map((feat, idx) => (
                          <li key={idx} className="flex items-center gap-1.5 text-[11px] text-[var(--text-muted)]">
                            <Check className="w-3.5 h-3.5 text-emerald-600 shrink-0" />
                            <span>{feat}</span>
                          </li>
                        ))}
                      </ul>
                    </div>

                    <div className="pt-4 mt-4 border-t border-[var(--border-default)]/60 flex items-center justify-between">
                      <span className="text-[11px] text-[var(--text-muted)]">
                        Enfant / PMR : {exp.childPrice} €
                      </span>
                      <div
                        className={`w-5 h-5 rounded-full border flex items-center justify-center ${
                          isSelected
                            ? 'border-[var(--brand-primary)] bg-[var(--brand-primary)] text-white'
                            : 'border-[var(--border-default)]'
                        }`}
                      >
                        {isSelected && <Check className="w-3 h-3 stroke-[3]" />}
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Step 1 Actions */}
          <div className="pt-4 flex items-center justify-end">
            <button
              type="button"
              onClick={() => {
                if (validateStep1()) {
                  setCurrentStep(2);
                }
              }}
              disabled={capacityMetrics.available <= 0}
              className="px-6 py-3 rounded-xl bg-[var(--brand-primary)] text-white font-bold text-sm shadow-xs hover:bg-[var(--brand-secondary)] disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer flex items-center gap-2"
            >
              <span>Continuer vers le créneau & visiteurs</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}

      {/* =================================================================== */}
      {/* ÉTAPE 2 : CRÉNEAU, NOMBRE DE VISITEURS & COORDONNÉES                */}
      {/* =================================================================== */}
      {currentStep === 2 && (
        <div className="space-y-6">
          {/* Timeslot Selection */}
          <div className="space-y-3">
            <div className="flex items-center gap-2">
              <Clock className="w-4 h-4 text-[var(--brand-primary)]" />
              <h3 className="font-['Fraunces'] text-lg font-bold text-[var(--text-primary)]">
                Sélectionnez votre créneau d arrivée
              </h3>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
              {TIMESLOTS.map((slot) => {
                const isSelected = timeSlot === slot.id;
                return (
                  <div
                    key={slot.id}
                    onClick={() => setTimeSlot(slot.id)}
                    className={`p-4 rounded-xl border transition-all cursor-pointer flex flex-col justify-between ${
                      isSelected
                        ? 'bg-[var(--bg-elevated)] border-[var(--brand-primary)] shadow-sm ring-2 ring-[var(--brand-primary)]/20'
                        : 'bg-[var(--bg-surface)] border-[var(--border-default)] hover:border-[var(--brand-primary)]/60'
                    }`}
                  >
                    <div>
                      <div className="text-xs font-mono font-bold text-[var(--brand-primary)]">
                        {slot.period}
                      </div>
                      <div className="font-['Fraunces'] font-bold text-base text-[var(--text-primary)] mt-1">
                        {slot.label}
                      </div>
                      <p className="text-[11px] text-[var(--text-muted)] mt-1 leading-snug">
                        {slot.recommendation}
                      </p>
                    </div>

                    <div className="pt-3 mt-3 border-t border-[var(--border-default)]/60 flex items-center justify-end">
                      <div
                        className={`w-4 h-4 rounded-full border flex items-center justify-center ${
                          isSelected
                            ? 'border-[var(--brand-primary)] bg-[var(--brand-primary)] text-white'
                            : 'border-[var(--border-default)]'
                        }`}
                      >
                        {isSelected && <Check className="w-2.5 h-2.5 stroke-[3]" />}
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Guest Breakdown Counters */}
          <div className="p-6 rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-default)] space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Users className="w-4 h-4 text-[var(--brand-primary)]" />
                <h4 className="font-bold text-sm text-[var(--text-primary)]">
                  Composition du groupe (Total : {totalGuests} personnes)
                </h4>
              </div>
              <span className="text-xs font-mono text-[var(--brand-primary)] font-bold">
                {capacityMetrics.available} places restantes aujourd hui
              </span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-2">
              {/* Adults Counter */}
              <div className="p-4 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)] flex items-center justify-between">
                <div>
                  <div className="font-bold text-xs text-[var(--text-primary)]">Adultes</div>
                  <div className="text-[11px] text-[var(--text-muted)]">18 ans et plus</div>
                </div>
                <div className="flex items-center gap-2.5">
                  <button
                    type="button"
                    onClick={() => setAdultCount(Math.max(1, adultCount - 1))}
                    className="w-8 h-8 rounded-lg bg-[var(--bg-surface)] border border-[var(--border-default)] font-bold text-sm text-[var(--text-primary)] hover:bg-[var(--border-default)]/30 flex items-center justify-center cursor-pointer"
                  >
                    -
                  </button>
                  <span className="font-mono font-bold text-sm w-4 text-center">{adultCount}</span>
                  <button
                    type="button"
                    onClick={() => {
                      if (totalGuests < capacityMetrics.available) {
                        setAdultCount(adultCount + 1);
                      }
                    }}
                    disabled={totalGuests >= capacityMetrics.available}
                    className="w-8 h-8 rounded-lg bg-[var(--bg-surface)] border border-[var(--border-default)] font-bold text-sm text-[var(--text-primary)] hover:bg-[var(--border-default)]/30 disabled:opacity-40 disabled:cursor-not-allowed flex items-center justify-center cursor-pointer"
                  >
                    +
                  </button>
                </div>
              </div>

              {/* Children Counter */}
              <div className="p-4 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)] flex items-center justify-between">
                <div>
                  <div className="font-bold text-xs text-[var(--text-primary)]">Enfants</div>
                  <div className="text-[11px] text-[var(--text-muted)]">3 à 17 ans (-50%)</div>
                </div>
                <div className="flex items-center gap-2.5">
                  <button
                    type="button"
                    onClick={() => setChildCount(Math.max(0, childCount - 1))}
                    className="w-8 h-8 rounded-lg bg-[var(--bg-surface)] border border-[var(--border-default)] font-bold text-sm text-[var(--text-primary)] hover:bg-[var(--border-default)]/30 flex items-center justify-center cursor-pointer"
                  >
                    -
                  </button>
                  <span className="font-mono font-bold text-sm w-4 text-center">{childCount}</span>
                  <button
                    type="button"
                    onClick={() => {
                      if (totalGuests < capacityMetrics.available) {
                        setChildCount(childCount + 1);
                      }
                    }}
                    disabled={totalGuests >= capacityMetrics.available}
                    className="w-8 h-8 rounded-lg bg-[var(--bg-surface)] border border-[var(--border-default)] font-bold text-sm text-[var(--text-primary)] hover:bg-[var(--border-default)]/30 disabled:opacity-40 disabled:cursor-not-allowed flex items-center justify-center cursor-pointer"
                  >
                    +
                  </button>
                </div>
              </div>

              {/* PMR Counter */}
              <div className="p-4 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)] flex items-center justify-between">
                <div>
                  <div className="font-bold text-xs text-[var(--text-primary)]">Accès PMR</div>
                  <div className="text-[11px] text-[var(--text-muted)]">Mobilité réduite</div>
                </div>
                <div className="flex items-center gap-2.5">
                  <button
                    type="button"
                    onClick={() => setPmrCount(Math.max(0, pmrCount - 1))}
                    className="w-8 h-8 rounded-lg bg-[var(--bg-surface)] border border-[var(--border-default)] font-bold text-sm text-[var(--text-primary)] hover:bg-[var(--border-default)]/30 flex items-center justify-center cursor-pointer"
                  >
                    -
                  </button>
                  <span className="font-mono font-bold text-sm w-4 text-center">{pmrCount}</span>
                  <button
                    type="button"
                    onClick={() => {
                      if (totalGuests < capacityMetrics.available) {
                        setPmrCount(pmrCount + 1);
                      }
                    }}
                    disabled={totalGuests >= capacityMetrics.available}
                    className="w-8 h-8 rounded-lg bg-[var(--bg-surface)] border border-[var(--border-default)] font-bold text-sm text-[var(--text-primary)] hover:bg-[var(--border-default)]/30 disabled:opacity-40 disabled:cursor-not-allowed flex items-center justify-center cursor-pointer"
                  >
                    +
                  </button>
                </div>
              </div>
            </div>

            {formErrors.capacity && (
              <p className="text-xs text-red-600 dark:text-red-400 font-semibold flex items-center gap-1.5 pt-1">
                <AlertTriangle className="w-3.5 h-3.5" />
                {formErrors.capacity}
              </p>
            )}
          </div>

          {/* Lead Visitor Details */}
          <div className="p-6 rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-default)] space-y-4">
            <h4 className="font-bold text-sm text-[var(--text-primary)]">
              Coordonnées du visiteur référent
            </h4>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div>
                <label className="block text-xs font-semibold text-[var(--text-primary)] mb-1">
                  Nom et prénom *
                </label>
                <input
                  type="text"
                  placeholder="Ex : Claire Delaunay"
                  value={leadName}
                  onChange={(e) => setLeadName(e.target.value)}
                  className="w-full px-3.5 py-2 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)] text-xs text-[var(--text-primary)] focus:outline-none focus:ring-1 focus:ring-[var(--brand-primary)]"
                />
                {formErrors.leadName && (
                  <p className="text-[11px] text-red-600 dark:text-red-400 mt-1 font-semibold">
                    {formErrors.leadName}
                  </p>
                )}
              </div>

              <div>
                <label className="block text-xs font-semibold text-[var(--text-primary)] mb-1">
                  Adresse email *
                </label>
                <input
                  type="email"
                  placeholder="claire.delaunay@nature.fr"
                  value={leadEmail}
                  onChange={(e) => setLeadEmail(e.target.value)}
                  className="w-full px-3.5 py-2 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)] text-xs text-[var(--text-primary)] focus:outline-none focus:ring-1 focus:ring-[var(--brand-primary)]"
                />
                {formErrors.leadEmail && (
                  <p className="text-[11px] text-red-600 dark:text-red-400 mt-1 font-semibold">
                    {formErrors.leadEmail}
                  </p>
                )}
              </div>

              <div>
                <label className="block text-xs font-semibold text-[var(--text-primary)] mb-1">
                  Téléphone (alertes météo)
                </label>
                <input
                  type="tel"
                  placeholder="06 12 34 56 78"
                  value={leadPhone}
                  onChange={(e) => setLeadPhone(e.target.value)}
                  className="w-full px-3.5 py-2 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)] text-xs text-[var(--text-primary)] focus:outline-none focus:ring-1 focus:ring-[var(--brand-primary)]"
                />
              </div>
            </div>
          </div>

          {/* Step 2 Actions */}
          <div className="pt-4 flex items-center justify-between">
            <button
              type="button"
              onClick={() => setCurrentStep(1)}
              className="px-5 py-2.5 rounded-xl border border-[var(--border-default)] text-xs font-bold text-[var(--text-primary)] hover:bg-[var(--bg-elevated)] cursor-pointer flex items-center gap-2"
            >
              <ArrowLeft className="w-4 h-4" />
              <span>Retour à l étape 1</span>
            </button>

            <button
              type="button"
              onClick={() => {
                if (validateStep2()) {
                  setCurrentStep(3);
                }
              }}
              className="px-6 py-3 rounded-xl bg-[var(--brand-primary)] text-white font-bold text-sm shadow-xs hover:bg-[var(--brand-secondary)] cursor-pointer flex items-center gap-2"
            >
              <span>Continuer vers l Éco-Mobilité</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}

      {/* =================================================================== */}
      {/* ÉTAPE 3 : ÉCO-MOBILITÉ, TARIFICATION & CHARTE ZÉRO-TRACE             */}
      {/* =================================================================== */}
      {currentStep === 3 && (
        <form onSubmit={handleFinalBooking} className="space-y-6">
          {/* Transport Selector (F21 Engine) */}
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Leaf className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
                <h3 className="font-['Fraunces'] text-lg font-bold text-[var(--text-primary)]">
                  Mode d acheminement vers le Parc (Bonus Éco-Mobilité)
                </h3>
              </div>
              <span className="text-xs text-[var(--brand-primary)] font-semibold">
                Jusqu à -30% de réduction immédiate
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {MOBILITY_OPTIONS.map((opt) => {
                const isSelected = mobilityMode === opt.id;
                return (
                  <div
                    key={opt.id}
                    onClick={() => setMobilityMode(opt.id)}
                    className={`p-4 rounded-xl border transition-all cursor-pointer flex items-start gap-3.5 ${
                      isSelected
                        ? 'bg-[var(--bg-elevated)] border-[var(--brand-primary)] shadow-sm ring-2 ring-[var(--brand-primary)]/20'
                        : 'bg-[var(--bg-surface)] border-[var(--border-default)] hover:border-[var(--brand-primary)]/60'
                    }`}
                  >
                    <div className="p-2.5 rounded-xl bg-[var(--bg-canvas)] border border-[var(--border-default)] shrink-0">
                      {renderMobilityIcon(opt.id)}
                    </div>

                    <div className="space-y-1 flex-1">
                      <div className="flex items-center justify-between gap-2">
                        <div className="font-bold text-xs text-[var(--text-primary)]">
                          {opt.label}
                        </div>
                        <span
                          className={`text-[10px] font-mono font-bold px-2 py-0.5 rounded-full ${
                            opt.discountPercent > 0
                              ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300 border border-emerald-300 dark:border-emerald-800'
                              : 'bg-[var(--bg-canvas)] text-[var(--text-muted)] border border-[var(--border-default)]'
                          }`}
                        >
                          {opt.carbonBadge}
                        </span>
                      </div>

                      <p className="text-[11px] text-[var(--text-muted)] leading-relaxed">
                        {opt.description}
                      </p>

                      <div className="text-[10px] text-emerald-700 dark:text-emerald-400 font-mono pt-1">
                        ADEME : {opt.ademeNote}
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Dynamic Price & Avoided CO2 Summary Card */}
          <div className="p-6 rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-default)] shadow-xs space-y-4">
            <h4 className="font-['Fraunces'] text-base font-bold text-[var(--text-primary)]">
              Récapitulatif Écologique & Tarifaire
            </h4>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 pb-4 border-b border-[var(--border-default)] text-xs">
              <div>
                <div className="text-[var(--text-muted)]">Visiteurs</div>
                <div className="font-bold text-[var(--text-primary)] mt-0.5">
                  {pricing.totalGuests} pers. ({pricing.adultCount}A, {pricing.childCount}E, {pricing.pmrCount}PMR)
                </div>
              </div>

              <div>
                <div className="text-[var(--text-muted)]">Tarif Brut</div>
                <div className="font-bold text-[var(--text-primary)] mt-0.5">
                  {formatEur(pricing.grossTotalEur)}
                </div>
              </div>

              <div>
                <div className="text-[var(--text-muted)]">Réduction Éco ({pricing.discountPercent}%)</div>
                <div className="font-bold text-emerald-600 dark:text-emerald-400 mt-0.5">
                  -{formatEur(pricing.discountAmountEur)}
                </div>
              </div>

              <div>
                <div className="text-[var(--text-muted)]">CO₂ Évité Certifié</div>
                <div className="font-mono font-bold text-emerald-600 dark:text-emerald-400 mt-0.5 flex items-center gap-1">
                  <Sparkles className="w-3.5 h-3.5" />
                  +{formatCo2(pricing.totalCo2AvoidedKg)}
                </div>
              </div>
            </div>

            {/* Total Amount to Pay */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <div>
                <span className="text-xs text-[var(--text-muted)]">
                  Total net à régler pour l émission de l Éco-Pass :
                </span>
                <div className="font-['Fraunces'] text-2xl font-bold text-[var(--brand-primary)]">
                  {formatEur(pricing.netTotalEur)}
                  <span className="text-xs font-normal text-[var(--text-muted)] ml-2">
                    ({formatEur(pricing.unitPriceEur)} / personne)
                  </span>
                </div>
              </div>

              <div className="text-xs font-mono text-[var(--text-muted)] bg-[var(--bg-elevated)] px-3 py-2 rounded-xl border border-[var(--border-default)]">
                QR Code SVG généré instantanément
              </div>
            </div>
          </div>

          {/* Zero-Trace Charter Commitment */}
          <div className="p-6 rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-default)] space-y-4">
            <div className="flex items-center gap-2 text-emerald-700 dark:text-emerald-400">
              <ShieldCheck className="w-5 h-5" />
              <h4 className="font-bold text-sm text-[var(--text-primary)]">
                Engagement Solennel : Charte Zéro-Trace du Parc
              </h4>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs text-[var(--text-muted)]">
              <div className="p-3 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)]">
                <strong className="text-[var(--text-primary)]">1. Silence & Quiétude :</strong> Respect strict des zones de nidification balisées et des observatoires ornithologiques.
              </div>
              <div className="p-3 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)]">
                <strong className="text-[var(--text-primary)]">2. Zéro Déchet :</strong> Emport systématique de tous déchets, même biodégradables (épluchures).
              </div>
              <div className="p-3 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)]">
                <strong className="text-[var(--text-primary)]">3. Rester sur le Tracé :</strong> Interdiction de couper les lacets pour prévenir le ravinement des sols.
              </div>
              <div className="p-3 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)]">
                <strong className="text-[var(--text-primary)]">4. Cueillette Interdite :</strong> Protection absolue des orchidées rares et de la flore alpine protégée.
              </div>
            </div>

            <label className="flex items-start gap-3 p-3.5 rounded-xl bg-[var(--bg-canvas)] border border-[var(--border-default)] cursor-pointer select-none">
              <input
                type="checkbox"
                checked={charterAccepted}
                onChange={(e) => setCharterAccepted(e.target.checked)}
                className="mt-0.5 w-4 h-4 rounded text-emerald-600 focus:ring-emerald-500 cursor-pointer"
              />
              <span className="text-xs text-[var(--text-primary)] font-medium leading-relaxed">
                J ai pris connaissance de la Charte Zéro-Trace et je m engage, pour moi-même et les membres de mon groupe, à respecter la tranquillité de la réserve forestière.
              </span>
            </label>

            {formErrors.charter && (
              <p className="text-xs text-red-600 dark:text-red-400 font-semibold flex items-center gap-1.5">
                <AlertTriangle className="w-3.5 h-3.5" />
                {formErrors.charter}
              </p>
            )}
          </div>

          {/* Step 3 Actions */}
          <div className="pt-4 flex items-center justify-between">
            <button
              type="button"
              onClick={() => setCurrentStep(2)}
              className="px-5 py-2.5 rounded-xl border border-[var(--border-default)] text-xs font-bold text-[var(--text-primary)] hover:bg-[var(--bg-elevated)] cursor-pointer flex items-center gap-2"
            >
              <ArrowLeft className="w-4 h-4" />
              <span>Retour aux coordonnées</span>
            </button>

            <button
              type="submit"
              disabled={!charterAccepted || bookingSuccess !== null}
              className="px-7 py-3.5 rounded-xl bg-emerald-700 hover:bg-emerald-800 text-white font-bold text-sm shadow-md disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer flex items-center gap-2 transition-all active:scale-95"
            >
              <CheckCircle2 className="w-4 h-4" />
              <span>Confirmer la réservation & Émettre l Éco-Pass</span>
            </button>
          </div>
        </form>
      )}
    </div>
  );
};
