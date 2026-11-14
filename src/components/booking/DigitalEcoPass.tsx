// ============================================================================
// INTERACTIVE DIGITAL ECO-PASS CARD (src/components/booking/DigitalEcoPass.tsx)
// Feature F22 & F23: Pure SVG QR code pass, Outdoor Mode & Ticket Management
// ============================================================================

import React, { useState, useRef, useMemo } from 'react';
import {
  Calendar,
  Clock,
  Users,
  Leaf,
  Printer,
  Download,
  CheckCircle2,
  XCircle,
  Sun,
  Moon,
  Sparkles,
  ShieldCheck,
  AlertCircle,
  ArrowRight,
  Ticket,
  Maximize2,
  RotateCcw,
  Award,
  KeyRound,
  QrCode,
} from 'lucide-react';
import { useEcoPark } from '../../context/EcoParkContext';
import { useAuth } from '../../context/AuthContext';
import { EcoPass } from '../../types/ecosystem';
import { generateQrSvgString } from '../../utils/qrCodeGenerator';
import { formatEur, formatCo2, MOBILITY_OPTIONS, getExperienceInfo } from '../../utils/ecoMobility';
import { GerminatingQrCode } from './GerminatingQrCode';
import { Co2BotanicalSprout } from './Co2BotanicalSprout';
import { isReducedMotionPreferred, recordMotionOrigin } from '../../utils/ecoMotion';
import { canActorCancelPass } from '../../utils/ecoSyncBus';

export const DigitalEcoPass: React.FC = () => {
  const {
    passes,
    activePassId,
    setActivePassId,
    sessionUnlockedPassIds,
    cancelPass,
    checkInPass,
    claimPassByReference,
    lookupPassAnonymously,
    highContrastOutdoor,
    setHighContrastOutdoor,
    setActiveView,
  } = useEcoPark();

  const { user, isStaff, canCheckIn } = useAuth();

  // Local state for OLED mode vs Full Sunlight mode when outdoor mode is active
  const [outdoorVariant, setOutdoorVariant] = useState<'sunlight' | 'oled'>('sunlight');
  const [showCancelModal, setShowCancelModal] = useState<boolean>(false);
  const [downloadSuccess, setDownloadSuccess] = useState<boolean>(false);
  const [germinationReplayCount, setGerminationReplayCount] = useState<number>(0);
  const [isFlippedBack, setIsFlippedBack] = useState<boolean>(false);
  const [isPointerActive, setIsPointerActive] = useState<boolean>(false);
  const card3dRef = useRef<HTMLDivElement | null>(null);

  // Claim existing pass state
  const [showClaimForm, setShowClaimForm] = useState<boolean>(false);
  const [claimRefInput, setClaimRefInput] = useState<string>('');
  const [claimContactInput, setClaimContactInput] = useState<string>('');
  const [claimFeedback, setClaimFeedback] = useState<{ ok: boolean; text: string } | null>(null);

  // Strict per-user pass isolation (Clients NEVER see other visitors' passes; anonymous visitors only see tab-unlocked passes)
  const scopedPasses = useMemo<EcoPass[]>(() => {
    if (!user) {
      return passes.filter(
        (p) =>
          sessionUnlockedPassIds.includes(p.id) &&
          p.ownerEmail !== 'anonyme@effacement.local'
      );
    }
    if (isStaff) return passes;
    const normEmail = user.email.trim().toLowerCase();
    return passes.filter(
      (p) =>
        p.ownerEmail !== 'anonyme@effacement.local' &&
        (p.ownerUserId === user.id ||
          p.ownerEmail?.toLowerCase() === normEmail ||
          p.leadVisitor.email.trim().toLowerCase() === normEmail)
    );
  }, [passes, user, isStaff, sessionUnlockedPassIds]);

  const handleClaimSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setClaimFeedback(null);
    if (!user) {
      const anonRes = lookupPassAnonymously(claimRefInput, claimContactInput);
      if (!anonRes.ok) {
        setClaimFeedback({
          ok: false,
          text: anonRes.error || 'Aucun billet trouvé avec ces coordonnées.',
        });
        return;
      }
      setClaimFeedback({
        ok: true,
        text: `Pass ${anonRes.pass?.id} déverrouillé pour votre session en cours.`,
      });
      setClaimRefInput('');
      setClaimContactInput('');
      setShowClaimForm(false);
      return;
    }
    const res = claimPassByReference(claimRefInput, claimContactInput, user.id, user.email);
    if (!res.ok) {
      setClaimFeedback({ ok: false, text: res.error || 'Rattachement impossible.' });
      return;
    }
    setClaimFeedback({
      ok: true,
      text: `Pass ${res.pass?.id} rattaché avec succès à votre Espace Cliente.`,
    });
    setClaimRefInput('');
    setClaimContactInput('');
    setShowClaimForm(false);
  };

  const resetCardTiltAndGlare = () => {
    const el = card3dRef.current;
    if (el) {
      el.style.setProperty('--pass-tilt-x', '0deg');
      el.style.setProperty('--pass-tilt-y', '0deg');
      el.style.setProperty('--glare-opacity', '0');
    }
    setIsPointerActive(false);
  };

  const handleCardPointerMove = (e: React.PointerEvent<HTMLDivElement>) => {
    if (highContrastOutdoor || isReducedMotionPreferred() || e.pointerType === 'touch') {
      return;
    }
    const el = card3dRef.current;
    if (!el) return;

    const rect = el.getBoundingClientRect();
    if (rect.width <= 0 || rect.height <= 0) return;

    const relX = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
    const relY = Math.max(0, Math.min(1, (e.clientY - rect.top) / rect.height));
    const tiltX = ((0.5 - relY) * 8.5).toFixed(2);
    const tiltY = ((relX - 0.5) * 9.5).toFixed(2);

    el.style.setProperty('--pass-tilt-x', `${tiltX}deg`);
    el.style.setProperty('--pass-tilt-y', `${tiltY}deg`);
    el.style.setProperty('--glare-x', `${Math.round(relX * 100)}%`);
    el.style.setProperty('--glare-y', `${Math.round(relY * 100)}%`);
    el.style.setProperty('--glare-opacity', '1');
    if (!isPointerActive) setIsPointerActive(true);
  };

  // Selected pass resolution strictly within scopedPasses
  const currentPass: EcoPass | null =
    scopedPasses.length > 0
      ? scopedPasses.find((p) => p.id === activePassId) || scopedPasses[0]
      : null;

  // Helper to find mobility details
  const getMobilityInfo = (mode: string) => {
    return MOBILITY_OPTIONS.find((m) => m.id === mode) || MOBILITY_OPTIONS[0];
  };

  // SVG Pass Download Action
  const handleDownloadSvg = () => {
    if (!currentPass) return;

    const svgMobility = getMobilityInfo(currentPass.mobilityMode);
    const svgExperience = getExperienceInfo(currentPass.experienceType);

    const qrSvg = generateQrSvgString(
      currentPass.qrPayload || `ECOPARK:PASS:${currentPass.id}`,
      { fgColor: '#1B4332', bgColor: '#FFFFFF', pixelSize: 220 }
    );

    const fullTicketSvg = `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="600" height="850" viewBox="0 0 600 850">
  <defs>
    <style>
      .title { font-family: 'Barlow Semi Condensed', serif; font-size: 24px; font-weight: bold; fill: #1B4332; }
      .subtitle { font-family: 'Source Sans 3', sans-serif; font-size: 12px; fill: #36403A; }
      .label { font-family: 'Source Sans 3', sans-serif; font-size: 11px; fill: #78847C; font-weight: 600; text-transform: uppercase; }
      .value { font-family: 'Source Sans 3', sans-serif; font-size: 15px; fill: #1F2421; font-weight: bold; }
      .mono { font-family: 'JetBrains Mono', monospace; font-size: 14px; fill: #1B4332; font-weight: bold; }
      .badge { font-family: 'Source Sans 3', sans-serif; font-size: 12px; fill: #52B788; font-weight: bold; }
    </style>
  </defs>

  <!-- Ticket Background -->
  <rect width="600" height="850" rx="24" fill="#F6FBF8" stroke="#8EBAA0" stroke-width="2"/>
  <rect x="0" y="0" width="600" height="110" rx="24" fill="#1B4332"/>
  <rect x="0" y="90" width="600" height="20" fill="#1B4332"/>

  <!-- Header -->
  <text x="30" y="45" font-family="'Source Sans 3', sans-serif" font-size="11" font-weight="bold" fill="#B7E4C7" letter-spacing="2">ECOPARK CAMEROUN · YAOUNDÉ, AHALA BARRIÈRE (RN3)</text>
  <text x="30" y="80" class="title" fill="#FFFFFF">${svgExperience.title}</text>

  <!-- Pass ID & Status -->
  <text x="30" y="150" class="label">Identifiant Unique</text>
  <text x="30" y="172" class="mono">${currentPass.id}</text>

  <text x="380" y="150" class="label">Statut du Billet</text>
  <text x="380" y="172" class="value" fill="#52B788">${currentPass.status.toUpperCase()}</text>

  <!-- Divider Line -->
  <line x1="30" y1="195" x2="570" y2="195" stroke="#8EBAA0" stroke-dasharray="6,6" stroke-width="1.5"/>

  <!-- QR Code Placement -->
  <g transform="translate(190, 220)">
    ${qrSvg}
  </g>
  <text x="300" y="470" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="11" fill="#36403A">Présentez ce QR Code aux bornes d entrée du Parc</text>

  <!-- Divider Line -->
  <line x1="30" y1="495" x2="570" y2="495" stroke="#8EBAA0" stroke-dasharray="6,6" stroke-width="1.5"/>

  <!-- Details Grid -->
  <text x="30" y="535" class="label">Visiteur Référent</text>
  <text x="30" y="555" class="value">${currentPass.leadVisitor.fullName}</text>
  <text x="30" y="575" class="subtitle">${currentPass.leadVisitor.email}</text>

  <text x="320" y="535" class="label">Date &amp; Créneau Horodaté</text>
  <text x="320" y="555" class="value">${currentPass.visitDate}</text>
  <text x="320" y="575" class="subtitle">${currentPass.timeSlot}</text>

  <text x="30" y="630" class="label">Nombre de Visiteurs</text>
  <text x="30" y="650" class="value">${currentPass.guestCount} pers.</text>

  <text x="320" y="630" class="label">Mode d Accès &amp; Paiement</text>
  <text x="320" y="650" class="value">${svgMobility.shortLabel}${currentPass.discountAppliedPercent > 0 ? ` (-${currentPass.discountAppliedPercent}%)` : ''}</text>

  <text x="30" y="715" class="label">Contribution Carbone Évitée</text>
  <text x="30" y="738" font-family="'JetBrains Mono', monospace" font-size="16" font-weight="bold" fill="#2D6A4F">+${currentPass.co2AvoidedKg} kg CO₂ évités</text>

  <text x="320" y="715" class="label">Montant Réglé (TTC)</text>
  <text x="320" y="738" class="value">${formatEur(currentPass.totalPriceEur)}</text>

  <!-- Footer Charter -->
  <rect x="30" y="775" width="540" height="50" rx="10" fill="#E9F5ED"/>
  <text x="50" y="805" font-family="'Source Sans 3', sans-serif" font-size="11" fill="#1B4332">✓ Garantie Météo RN3 (report gratuit 90j) · Orange Money / MTN MoMo / Guichet</text>
</svg>`;

    const blob = new Blob([fullTicketSvg], { type: 'image/svg+xml;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `eco-pass-${currentPass.id}.svg`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);

    setDownloadSuccess(true);
    setTimeout(() => setDownloadSuccess(false), 3000);
  };

  // Print Action
  const handlePrint = () => {
    window.print();
  };

  // Empty State (Scoped to Authenticated Client or Anonymous Single-Ticket Lookup)
  if (!currentPass || scopedPasses.length === 0) {
    return (
      <div className="max-w-2xl mx-auto space-y-6">
        <div className="p-8 rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-default)] text-center space-y-5">
          <div className="w-16 h-16 rounded-2xl bg-emerald-100 dark:bg-emerald-950 text-emerald-700 dark:text-emerald-300 mx-auto flex items-center justify-center">
            <Ticket className="w-8 h-8" />
          </div>
          <div>
            <h2 className="font-['Barlow_Semi_Condensed'] text-2xl font-bold text-[var(--text-primary)]">
              {user
                ? 'Aucun Pass QR rattaché à votre Espace Cliente'
                : 'Récupération Unitaire de Pass QR (Visiteur sans compte)'}
            </h2>
            <p className="text-xs sm:text-sm text-[var(--text-muted)] mt-1.5 max-w-md mx-auto leading-relaxed">
              {user
                ? 'Réservez votre prochain créneau en FCFA (Orange Money, MTN MoMo ou Guichet) ou rattachez ci-dessous un billet déjà émis.'
                : 'Affichez immédiatement un Pass QR acheté sans compte avec sa référence (ECP-2026-XXXXX) et le téléphone ou e-mail de réservation, ou réservez votre visite.'}
            </p>
          </div>
          <button
            type="button"
            onClick={(e) => {
              recordMotionOrigin(e);
              setActiveView('billetterie');
            }}
            className="px-6 py-3 rounded-xl bg-[var(--brand-primary)] text-white font-bold text-sm shadow-xs hover:bg-[var(--brand-secondary)] cursor-pointer inline-flex items-center gap-2"
          >
            <span>Réserver un Pass QR (dès 500 FCFA)</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>

        {/* Claim / Anonymous Lookup Existing Pass Form */}
        <form
          onSubmit={handleClaimSubmit}
          aria-label={user ? 'Rattacher un Pass QR existant' : 'Récupération unitaire de Pass QR'}
          className="p-6 rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-default)] space-y-4"
        >
          <div className="flex items-center gap-2">
            <KeyRound className="w-4 h-4 text-[var(--brand-primary)]" />
            <h3 className="font-['Barlow_Semi_Condensed'] text-lg font-bold text-[var(--text-primary)]">
              {user
                ? 'Vous avez déjà réservé un billet (ECP-2026-XXXXX) ?'
                : 'Afficher mon Pass QR unitaire (ECP-2026-XXXXX)'}
            </h3>
          </div>
          <p className="text-xs text-[var(--text-muted)]">
            {user
              ? "Saisissez la référence de votre Pass ainsi que l'adresse email ou le numéro de téléphone utilisé lors de la réservation pour l'ajouter à votre portefeuille personnel."
              : "Saisissez la référence exacte de votre billet ainsi que le numéro de téléphone ou l'adresse e-mail utilisés lors de l'achat (déverrouillage strictement limité à cet onglet)."}
          </p>

          {claimFeedback && (
            <div
              className={`p-3 rounded-xl text-xs border ${
                claimFeedback.ok
                  ? 'bg-emerald-50 dark:bg-emerald-950/60 border-emerald-300 text-emerald-800 dark:text-emerald-200'
                  : 'bg-red-50 dark:bg-red-950/60 border-red-300 text-red-800 dark:text-red-200'
              }`}
            >
              {claimFeedback.text}
            </div>
          )}

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <input
              type="text"
              required
              aria-label="Référence du Pass QR"
              placeholder="Référence (ex: ECP-2026-8942)"
              value={claimRefInput}
              onChange={(e) => setClaimRefInput(e.target.value)}
              className="px-3.5 py-2.5 min-h-[44px] rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)] text-xs font-mono text-[var(--text-primary)]"
            />
            <input
              type="text"
              required
              aria-label="Email ou téléphone du billet"
              placeholder="Email ou téléphone du billet"
              value={claimContactInput}
              onChange={(e) => setClaimContactInput(e.target.value)}
              className="px-3.5 py-2.5 min-h-[44px] rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)] text-xs text-[var(--text-primary)]"
            />
          </div>

          <button
            type="submit"
            className="px-4 py-2.5 min-h-[44px] rounded-xl bg-[var(--brand-primary)] hover:bg-[var(--brand-secondary)] text-white text-xs font-bold transition-colors cursor-pointer"
          >
            {user ? 'Rattacher ce billet à mon compte' : 'Afficher mon Pass QR'}
          </button>
        </form>
      </div>
    );
  }

  const mobilityInfo = getMobilityInfo(currentPass.mobilityMode);
  const experienceInfo = getExperienceInfo(currentPass.experienceType);
  const qrPayloadValue =
    currentPass.qrPayload ||
    `ECOPARK:PASS:${currentPass.id}:DATE=${currentPass.visitDate}:GUESTS=${currentPass.guestCount}`;

  return (
    <div className="space-y-6">
      {/* Pass Switcher & Controls */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-4 rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-default)]">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-xs font-semibold text-[var(--brand-primary)] uppercase tracking-wider">
              {isStaff
                ? `Registre Global des Pass (${scopedPasses.length})`
                : user
                ? `Mon Portefeuille Éco-Pass (${scopedPasses.length})`
                : `Session Visiteur · Pass Déverrouillé (${scopedPasses.length})`}
            </span>
            {!isStaff && (
              <button
                type="button"
                onClick={() => setShowClaimForm(!showClaimForm)}
                className="text-[11px] font-semibold text-[var(--text-muted)] hover:text-[var(--brand-primary)] underline cursor-pointer"
              >
                {user ? '+ Rattacher un billet' : '+ Chercher un autre billet'}
              </button>
            )}
          </div>
          <div className="flex flex-wrap items-center gap-2 mt-1.5">
            {scopedPasses.map((pass) => (
              <button
                key={pass.id}
                type="button"
                onClick={() => {
                  setActivePassId(pass.id);
                  setIsFlippedBack(false);
                }}
                className={`px-3 py-1.5 rounded-xl text-xs font-mono font-bold transition-all cursor-pointer flex items-center gap-1.5 ${
                  pass.id === currentPass.id
                    ? 'bg-[var(--brand-primary)] text-white shadow-xs'
                    : 'bg-[var(--bg-elevated)] border border-[var(--border-default)] text-[var(--text-primary)] hover:border-[var(--brand-primary)]'
                }`}
              >
                <span>{pass.id}</span>
                <span
                  className={`w-2 h-2 rounded-full ${
                    pass.status === 'confirmed'
                      ? 'bg-emerald-400'
                      : pass.status === 'checked_in'
                      ? 'bg-blue-400'
                      : 'bg-red-400'
                  }`}
                />
              </button>
            ))}
          </div>
        </div>

        {/* Outdoor Mode & 3D Flip Controls */}
        <div className="flex flex-wrap items-center gap-2">
          <button
            type="button"
            onClick={() => {
              resetCardTiltAndGlare();
              setIsFlippedBack((prev) => !prev);
            }}
            className={`px-3.5 py-2 rounded-xl text-xs font-semibold border transition-all cursor-pointer flex items-center gap-1.5 ${
              isFlippedBack
                ? 'bg-[var(--brand-primary)] text-white border-[var(--brand-primary)] shadow-xs'
                : 'bg-[var(--bg-elevated)] border-[var(--border-default)] text-[var(--text-primary)] hover:bg-[var(--bg-surface)]'
            }`}
            title="Retourner le Pass en 3D pour consulter le Certificat Carbone & la Charte Zéro-Trace"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span>{isFlippedBack ? 'Voir Recto (QR Code)' : 'Certificat Verso 3D'}</span>
          </button>

          <button
            onClick={() => {
              resetCardTiltAndGlare();
              setHighContrastOutdoor(!highContrastOutdoor);
            }}
            className={`px-3.5 py-2 rounded-xl text-xs font-semibold border transition-all cursor-pointer flex items-center gap-1.5 ${
              highContrastOutdoor
                ? 'bg-amber-500 text-black border-amber-600 font-bold shadow-xs'
                : 'bg-[var(--bg-elevated)] border-[var(--border-default)] text-[var(--text-primary)] hover:bg-[var(--bg-surface)]'
            }`}
            title="Activer le mode contraste élevé pour lecture sous le soleil ou en économie OLED"
          >
            <Maximize2 className="w-3.5 h-3.5" />
            <span>Mode Extérieur Plein Soleil</span>
          </button>

          {highContrastOutdoor && (
            <div className="flex items-center gap-1 bg-[var(--bg-canvas)] p-1 rounded-xl border border-[var(--border-default)]">
              <button
                onClick={() => setOutdoorVariant('sunlight')}
                className={`p-1.5 rounded-lg text-xs cursor-pointer ${
                  outdoorVariant === 'sunlight'
                    ? 'bg-amber-400 text-black font-bold'
                    : 'text-[var(--text-muted)]'
                }`}
                title="Plein Soleil (Fond blanc éclatant)"
              >
                <Sun className="w-4 h-4" />
              </button>
              <button
                onClick={() => setOutdoorVariant('oled')}
                className={`p-1.5 rounded-lg text-xs cursor-pointer ${
                  outdoorVariant === 'oled'
                    ? 'bg-black text-emerald-400 font-bold ring-1 ring-emerald-500'
                    : 'text-[var(--text-muted)]'
                }`}
                title="Éco-Énergie OLED (Noir absolu #000000)"
              >
                <Moon className="w-4 h-4" />
              </button>
            </div>
          )}
        </div>
      </div>

      {showClaimForm && !isStaff && (
        <form
          onSubmit={handleClaimSubmit}
          className="max-w-2xl mx-auto p-5 rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-default)] space-y-3"
        >
          <div className="text-xs font-bold text-[var(--text-primary)] flex items-center gap-1.5">
            <KeyRound className="w-4 h-4 text-[var(--brand-primary)]" />
            <span>
              {user
                ? 'Rattacher un Pass existant (ECP-2026-XXXXX)'
                : 'Afficher un autre Pass QR unitaire (ECP-2026-XXXXX)'}
            </span>
          </div>
          {claimFeedback && (
            <div
              className={`p-2.5 rounded-xl text-xs border ${
                claimFeedback.ok
                  ? 'bg-emerald-50 dark:bg-emerald-950/60 border-emerald-300 text-emerald-800 dark:text-emerald-200'
                  : 'bg-red-50 dark:bg-red-950/60 border-red-300 text-red-800 dark:text-red-200'
              }`}
            >
              {claimFeedback.text}
            </div>
          )}
          <div className="flex flex-col sm:flex-row gap-2.5">
            <input
              type="text"
              required
              placeholder="ECP-2026-XXXXX"
              value={claimRefInput}
              onChange={(e) => setClaimRefInput(e.target.value)}
              className="flex-1 px-3 py-2 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)] text-xs font-mono text-[var(--text-primary)]"
            />
            <input
              type="text"
              required
              placeholder="Email ou téléphone du billet"
              value={claimContactInput}
              onChange={(e) => setClaimContactInput(e.target.value)}
              className="flex-1 px-3 py-2 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)] text-xs text-[var(--text-primary)]"
            />
            <button
              type="submit"
              className="px-4 py-2 rounded-xl bg-[var(--brand-primary)] text-white text-xs font-bold cursor-pointer"
            >
              Rattacher
            </button>
          </div>
        </form>
      )}

      {/* Main Digital Pass 3D Stage & Card Container */}
      <div className="eco-pass-3d-stage max-w-2xl mx-auto">
        <div
          id="printable-eco-pass"
          ref={card3dRef}
          onPointerMove={handleCardPointerMove}
          onPointerLeave={resetCardTiltAndGlare}
          style={
            {
              '--pass-flip-y': isFlippedBack ? '180deg' : '0deg',
            } as React.CSSProperties
          }
          className={`eco-pass-3d-card ${
            isPointerActive ? 'is-pointer-active' : ''
          } relative grid rounded-3xl shadow-lg border ${
            highContrastOutdoor && outdoorVariant === 'oled'
              ? 'bg-black text-[#52B788] border-emerald-900 ring-2 ring-emerald-500/30'
              : highContrastOutdoor && outdoorVariant === 'sunlight'
              ? 'bg-white text-black border-4 border-black'
              : 'bg-[var(--bg-surface)] text-[var(--text-primary)] border-[var(--border-default)]'
          }`}
        >
          {/* Holographic Forest-Ochre Glare Layer (disabled in High-Contrast Outdoor mode) */}
          {!highContrastOutdoor && (
            <div
              aria-hidden="true"
              className="eco-pass-holo-glare pointer-events-none absolute inset-0 rounded-3xl z-20 print:hidden"
            />
          )}

          {/* =============================================================== */}
          {/* FACE RECTO : QR CODE GERMINATIF & CONTRÔLE D'ACCÈS              */}
          {/* =============================================================== */}
          <div
            aria-hidden={isFlippedBack}
            className={`eco-pass-face [grid-area:1/1] flex flex-col justify-between overflow-hidden rounded-3xl ${
              isFlippedBack ? 'pointer-events-none' : ''
            }`}
          >
            <div>
              {/* Pass Top Banner */}
              <div
                className={`p-6 sm:p-7 flex flex-col sm:flex-row sm:items-center justify-between gap-4 ${
                  highContrastOutdoor && outdoorVariant === 'oled'
                    ? 'bg-[#0B1D15] border-b border-emerald-950 text-emerald-100'
                    : highContrastOutdoor && outdoorVariant === 'sunlight'
                    ? 'bg-black text-white'
                    : 'bg-[#1B4332] text-white'
                }`}
              >
                <div>
                  <span className="text-[11px] font-mono font-semibold uppercase tracking-widest text-[#B7E4C7]">
                    ECOPARK CAMEROUN · YAOUNDÉ, AHALA BARRIÈRE (FACE TRADEX RN3)
                  </span>
                  <h2 className="type-h3 !text-white mt-0.5">
                    Pass QR Officiel : Complexe Écologique &amp; Loisirs
                  </h2>
                </div>

                <div className="flex items-center gap-2">
                  <span
                    className={`px-3 py-1 rounded-full text-xs font-mono font-bold uppercase tracking-wider ${
                      currentPass.status === 'confirmed'
                        ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-400'
                        : currentPass.status === 'checked_in'
                        ? 'bg-blue-500/20 text-blue-300 border border-blue-400'
                        : 'bg-red-500/20 text-red-300 border border-red-400'
                    }`}
                  >
                    {currentPass.status === 'confirmed' && 'Confirmé · Accès Valide'}
                    {currentPass.status === 'checked_in' && 'Check-In Effectué'}
                    {currentPass.status === 'cancelled' && 'Pass Annulé'}
                  </span>
                </div>
              </div>

              {/* Pass Body */}
              <div className="p-6 sm:p-8 space-y-6">
                {/* Header Row: ID & Experience */}
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-[var(--border-default)]/60">
                  <div>
                    <div className="text-xs font-mono text-[var(--text-muted)]">Numéro de Billet</div>
                    <div className="font-['JetBrains_Mono'] text-xl font-bold tracking-tight text-[var(--brand-primary)]">
                      {currentPass.id}
                    </div>
                  </div>

                  <div className="sm:text-right">
                    <div className="text-xs text-[var(--text-muted)]">Formule Souscrite</div>
                    <div className="font-['Barlow_Semi_Condensed'] font-bold text-base text-[var(--text-primary)]">
                      {experienceInfo.title}
                    </div>
                    <div className="text-[11px] font-mono text-[var(--brand-primary)] font-semibold">
                      {experienceInfo.badge}
                    </div>
                  </div>
                </div>

                {/* QR Code Presentation Box with Spiral Seed Germination */}
                <div className="flex flex-col items-center justify-center p-6 rounded-2xl bg-[var(--bg-elevated)] border border-[var(--border-default)] space-y-3">
                  <div className="p-4 rounded-xl bg-white shadow-xs border border-gray-200">
                    <GerminatingQrCode
                      value={qrPayloadValue}
                      size={180}
                      fgColor={highContrastOutdoor ? '#000000' : '#1B4332'}
                      bgColor="#FFFFFF"
                      quietZone={2}
                      germinationKey={`${currentPass.id}-${germinationReplayCount}`}
                      disableAnimation={highContrastOutdoor && outdoorVariant === 'oled'}
                      title={`Éco-Pass QR Code pour ${currentPass.id}`}
                    />
                  </div>

                  <div className="text-center space-y-1">
                    <span className="text-xs font-mono font-semibold text-[var(--text-primary)]">
                      Scannable aux portiques et par les Éco-Gardes
                    </span>
                    <p className="text-[11px] text-[var(--text-muted)] font-mono">
                      Germination spirale botanique · Vecteur ISO/IEC 18004 1-nœud
                    </p>
                  </div>

                  <div className="flex flex-wrap items-center justify-center gap-2 pt-1 print:hidden">
                    <button
                      type="button"
                      onClick={() => setGerminationReplayCount((c) => c + 1)}
                      className="px-3 py-1.5 rounded-lg bg-[var(--bg-surface)] border border-[var(--border-default)] text-[11px] font-mono font-semibold text-[var(--text-primary)] hover:border-[var(--brand-primary)] cursor-pointer inline-flex items-center gap-1.5 transition-colors"
                      title="Rejouer l'éclosion organique des modules QR"
                    >
                      <Sparkles className="w-3 h-3 text-[#52B788]" />
                      <span>Rejouer la germination</span>
                    </button>

                    <button
                      type="button"
                      onClick={() => {
                        resetCardTiltAndGlare();
                        setIsFlippedBack(true);
                      }}
                      className="px-3 py-1.5 rounded-lg bg-[var(--bg-surface)] border border-[var(--border-default)] text-[11px] font-mono font-semibold text-[var(--brand-primary)] hover:bg-[var(--bg-canvas)] cursor-pointer inline-flex items-center gap-1.5 transition-colors"
                    >
                      <RotateCcw className="w-3 h-3" />
                      <span>Voir le certificat carbone (Verso 3D)</span>
                    </button>
                  </div>
                </div>

                {/* Details Grid */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs font-sans">
                  <div className="space-y-1 p-3.5 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)]">
                    <div className="text-[var(--text-muted)] flex items-center gap-1.5">
                      <Users className="w-3.5 h-3.5 text-[var(--brand-primary)]" />
                      <span>Titulaire du Billet</span>
                    </div>
                    <div className="font-bold text-sm text-[var(--text-primary)]">
                      {currentPass.leadVisitor.fullName}
                    </div>
                    <div className="text-[var(--text-muted)] font-mono text-[11px]">
                      {currentPass.leadVisitor.email} · {currentPass.leadVisitor.phone}
                    </div>
                  </div>

                  <div className="space-y-1 p-3.5 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)]">
                    <div className="text-[var(--text-muted)] flex items-center gap-1.5">
                      <Calendar className="w-3.5 h-3.5 text-[var(--brand-primary)]" />
                      <span>Date &amp; Créneau d Arrivée</span>
                    </div>
                    <div className="font-bold text-sm text-[var(--text-primary)]">
                      {currentPass.visitDate}
                    </div>
                    <div className="text-[var(--brand-primary)] font-mono font-semibold text-[11px] flex items-center gap-1">
                      <Clock className="w-3 h-3" />
                      {currentPass.timeSlot}
                    </div>
                  </div>

                  <div className="space-y-1 p-3.5 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)]">
                    <div className="text-[var(--text-muted)] flex items-center gap-1.5">
                      <Leaf className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" />
                      <span>Mode d Acheminement</span>
                    </div>
                    <div className="font-bold text-sm text-[var(--text-primary)]">
                      {mobilityInfo.label}
                    </div>
                    <div className="text-emerald-700 dark:text-emerald-400 font-mono text-[11px] font-semibold">
                      Réduction de {currentPass.discountAppliedPercent}% appliquée
                    </div>
                  </div>

                  <div className="space-y-1 p-3.5 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)]">
                    <div className="text-[var(--text-muted)] flex items-center gap-1.5">
                      <Sparkles className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" />
                      <span>Bilan Carbone Évité</span>
                    </div>
                    <div className="font-mono font-bold text-sm text-emerald-600 dark:text-emerald-400">
                      +{formatCo2(currentPass.co2AvoidedKg)}
                    </div>
                    <div className="text-[var(--text-muted)] text-[11px]">
                      Pour {currentPass.guestCount} visiteur(s)
                    </div>
                  </div>
                </div>

                {/* Price & Charter Badge */}
                <div className="p-4 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)] flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs">
                  <div className="flex items-center gap-2">
                    <ShieldCheck className="w-4 h-4 text-emerald-600 shrink-0" />
                    <span className="text-[var(--text-muted)]">
                      Charte Zéro-Trace acceptée · Randonnée éco-responsable
                    </span>
                  </div>
                  <div className="font-mono font-bold text-[var(--text-primary)] text-sm sm:text-right">
                    Réglé : {formatEur(currentPass.totalPriceEur)}
                  </div>
                </div>
              </div>
            </div>

            {/* Pass Actions Bar (Check-In strictly reserved to Staff RBAC) */}
            <div className="p-6 bg-[var(--bg-canvas)] border-t border-[var(--border-default)] flex flex-wrap items-center justify-between gap-3 print:hidden">
              {currentPass.status === 'confirmed' ? (
                isStaff && canCheckIn ? (
                  <button
                    type="button"
                    onClick={() => checkInPass(currentPass.id)}
                    className="px-4 py-2.5 rounded-xl bg-amber-600 hover:bg-amber-700 text-white font-bold text-xs shadow-xs cursor-pointer flex items-center gap-1.5 active:scale-95 transition-transform"
                  >
                    <CheckCircle2 className="w-4 h-4" />
                    <span>Valider Check-In Guichet RN3 (Staff)</span>
                  </button>
                ) : (
                  <span className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-xs font-mono font-semibold text-emerald-800 dark:text-emerald-300">
                    <QrCode className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400 shrink-0" />
                    <span>À présenter au contrôle QR d&apos;Ahala Barrière (RN3)</span>
                  </span>
                )
              ) : currentPass.status === 'checked_in' ? (
                <span className="text-xs font-mono font-bold text-emerald-600 dark:text-emerald-400 flex items-center gap-1.5">
                  <CheckCircle2 className="w-4 h-4" />
                  Entrée validée le {new Date(currentPass.checkInTimestamp || '').toLocaleTimeString('fr-FR')}
                </span>
              ) : (
                <span className="text-xs font-mono font-bold text-red-600 dark:text-red-400 flex items-center gap-1.5">
                  <XCircle className="w-4 h-4" />
                  Pass annulé
                </span>
              )}

              {/* Utility Action Buttons */}
              <div className="flex items-center gap-2">
                <button
                  onClick={handleDownloadSvg}
                  className="px-3.5 py-2 rounded-xl bg-[var(--bg-surface)] border border-[var(--border-default)] text-xs font-semibold text-[var(--text-primary)] hover:bg-[var(--bg-elevated)] cursor-pointer flex items-center gap-1.5"
                  title="Télécharger le fichier vectoriel SVG de l Éco-Pass"
                >
                  <Download className="w-3.5 h-3.5" />
                  <span>SVG Ticket</span>
                </button>

                <button
                  onClick={handlePrint}
                  className="px-3.5 py-2 rounded-xl bg-[var(--bg-surface)] border border-[var(--border-default)] text-xs font-semibold text-[var(--text-primary)] hover:bg-[var(--bg-elevated)] cursor-pointer flex items-center gap-1.5"
                  title="Imprimer ou enregistrer en PDF"
                >
                  <Printer className="w-3.5 h-3.5" />
                  <span>Imprimer</span>
                </button>

                {canActorCancelPass(currentPass, user, sessionUnlockedPassIds) && (
                  <button
                    onClick={() => setShowCancelModal(true)}
                    className="px-3.5 py-2 rounded-xl text-xs font-semibold text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-950/50 border border-transparent hover:border-red-300 dark:hover:border-red-900 cursor-pointer flex items-center gap-1"
                    title="Annuler ce pass et libérer la jauge du parc"
                  >
                    <span>Annuler</span>
                  </button>
                )}
              </div>
            </div>
          </div>

          {/* =============================================================== */}
          {/* FACE VERSO 3D : CERTIFICAT CARBONE & CHARTE ZÉRO-TRACE          */}
          {/* =============================================================== */}
          <div
            aria-hidden={!isFlippedBack}
            className={`eco-pass-face eco-pass-face-back [grid-area:1/1] flex flex-col justify-between overflow-hidden rounded-3xl print:hidden ${
              !isFlippedBack ? 'pointer-events-none' : ''
            }`}
          >
            <div>
              {/* Verso Top Banner */}
              <div className="p-6 sm:p-7 bg-[#1F2421] text-[#E9F5ED] border-b border-[#2D6A4F]/50 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div>
                  <span className="text-[11px] font-mono font-semibold uppercase tracking-widest text-[#D4A373]">
                    VERSO OFFICIEL · ATTESTATION D&apos;IMPACT ÉCOLOGIQUE
                  </span>
                  <h3 className="font-['Barlow_Semi_Condensed'] text-2xl font-bold mt-0.5 text-white flex items-center gap-2">
                    <Award className="w-6 h-6 text-[#52B788] shrink-0" />
                    <span>Certificat Carbone &amp; Serment Zéro-Trace</span>
                  </h3>
                </div>

                <span className="px-3 py-1 rounded-full text-xs font-mono font-bold bg-[#1B4332] text-[#B7E4C7] border border-[#52B788]/50 self-start sm:self-center">
                  {currentPass.id}
                </span>
              </div>

              {/* Verso Body */}
              <div className="p-6 sm:p-8 space-y-6">
                {/* Embedded Botanical Sprout Visualizer */}
                <Co2BotanicalSprout
                  co2AvoidedKg={currentPass.co2AvoidedKg}
                  mobilityMode={currentPass.mobilityMode}
                  guestCount={currentPass.guestCount}
                />

                {/* 4 Pillars of Signed Zero-Trace Charter */}
                <div className="space-y-3">
                  <div className="flex items-center gap-2 text-xs font-mono font-bold uppercase tracking-wider text-[var(--brand-primary)]">
                    <ShieldCheck className="w-4 h-4 text-[#52B788]" />
                    <span>Engagements Zéro-Trace signés par {currentPass.leadVisitor.fullName}</span>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                    <div className="p-3.5 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)] space-y-1">
                      <div className="font-bold text-[var(--text-primary)]">1. Quiétude de la Faune</div>
                      <p className="text-[var(--text-muted)] text-[11px] leading-relaxed">
                        Silence acoustique aux abords du Sanctuaire du Gorille « ToTo » et des zones de nidification.
                      </p>
                    </div>

                    <div className="p-3.5 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)] space-y-1">
                      <div className="font-bold text-[var(--text-primary)]">2. Zéro Déchet Intégral</div>
                      <p className="text-[var(--text-muted)] text-[11px] leading-relaxed">
                        Aucun rejet plastique ou organique hors des points de tri sélectif d&apos;Ahala.
                      </p>
                    </div>

                    <div className="p-3.5 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)] space-y-1">
                      <div className="font-bold text-[var(--text-primary)]">3. Respect des Tracés</div>
                      <p className="text-[var(--text-muted)] text-[11px] leading-relaxed">
                        Maintien strict sur les sentiers balisés pour protéger l&apos;humus forestier de l&apos;érosion.
                      </p>
                    </div>

                    <div className="p-3.5 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)] space-y-1">
                      <div className="font-bold text-[var(--text-primary)]">4. Garantie Météo RN3</div>
                      <p className="text-[var(--text-muted)] text-[11px] leading-relaxed">
                        Report gratuit sous 90 jours en cas d&apos;alerte orage tropical émise par les Éco-Gardes.
                      </p>
                    </div>
                  </div>
                </div>

                {/* Cryptographic / Field Verification Stamp */}
                <div className="p-4 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)] flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-[11px] font-mono text-[var(--text-muted)]">
                  <span>
                    Émis le {new Date(currentPass.createdAt).toLocaleDateString('fr-FR')} · Poste de garde RN3 Ahala Barrière
                  </span>
                  <span className="text-[var(--brand-primary)] font-bold">
                    Urgence Éco-Gardes : +237 672 56 45 98
                  </span>
                </div>
              </div>
            </div>

            {/* Verso Footer Bar */}
            <div className="p-6 bg-[var(--bg-canvas)] border-t border-[var(--border-default)] flex items-center justify-between gap-3">
              <span className="text-xs font-mono text-[var(--text-muted)]">
                Face 2/2 · Certificat écologique vérifié
              </span>

              <button
                type="button"
                onClick={() => {
                  resetCardTiltAndGlare();
                  setIsFlippedBack(false);
                }}
                className="px-4 py-2.5 rounded-xl bg-[var(--brand-primary)] text-[var(--on-primary)] font-bold text-xs shadow-xs cursor-pointer inline-flex items-center gap-1.5 hover:opacity-95 transition-opacity"
              >
                <RotateCcw className="w-3.5 h-3.5" />
                <span>Retourner vers le QR Code (Recto 3D)</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Download Success Toast */}
      {downloadSuccess && (
        <div className="p-3.5 rounded-xl bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-200 border border-emerald-300 dark:border-emerald-800 text-xs font-semibold flex items-center gap-2 max-w-md mx-auto shadow-sm animate-fade-in">
          <CheckCircle2 className="w-4 h-4 text-emerald-600" />
          <span>Fichier SVG vectoriel téléchargé avec succès !</span>
        </div>
      )}

      {/* Cancel Confirmation Modal */}
      {showCancelModal && (
        <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-xs flex items-center justify-center p-4 animate-fade-in">
          <div className="w-full max-w-md p-6 rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-default)] shadow-xl space-y-4">
            <div className="flex items-center gap-3 text-red-600 dark:text-red-400">
              <AlertCircle className="w-6 h-6" />
              <h3 className="font-['Barlow_Semi_Condensed'] text-lg font-bold text-[var(--text-primary)]">
                Annuler cet Éco-Pass ?
              </h3>
            </div>

            <p className="text-xs text-[var(--text-muted)] leading-relaxed">
              En annulant le pass <strong className="text-[var(--text-primary)] font-mono">{currentPass.id}</strong>,
              vos {currentPass.guestCount} places seront immédiatement réattribuées à la jauge écologique du parc pour d autres visiteurs.
            </p>

            <div className="pt-2 flex items-center justify-end gap-3">
              <button
                onClick={() => setShowCancelModal(false)}
                className="px-4 py-2 rounded-xl border border-[var(--border-default)] text-xs font-bold text-[var(--text-primary)] hover:bg-[var(--bg-elevated)] cursor-pointer"
              >
                Garder mon pass
              </button>
              <button
                onClick={() => {
                  cancelPass(currentPass.id);
                  setShowCancelModal(false);
                }}
                className="px-4 py-2 rounded-xl bg-red-600 hover:bg-red-700 text-white font-bold text-xs shadow-xs cursor-pointer"
              >
                Confirmer l annulation
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
