// ============================================================================
// INTERACTIVE DIGITAL ECO-PASS CARD (src/components/booking/DigitalEcoPass.tsx)
// Feature F22 & F23: Pure SVG QR code pass, Outdoor Mode & Ticket Management
// ============================================================================

import React, { useState } from 'react';
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
} from 'lucide-react';
import { useEcoPark } from '../../context/EcoParkContext';
import { EcoPass } from '../../types/ecosystem';
import { QRCodeSVG, generateQrSvgString } from '../../utils/qrCodeGenerator';
import { formatEur, formatCo2, MOBILITY_OPTIONS } from '../../utils/ecoMobility';

export const DigitalEcoPass: React.FC = () => {
  const {
    passes,
    activePass,
    activePassId,
    setActivePassId,
    cancelPass,
    checkInPass,
    highContrastOutdoor,
    setHighContrastOutdoor,
    setActiveView,
  } = useEcoPark();

  // Local state for OLED mode vs Full Sunlight mode when outdoor mode is active
  const [outdoorVariant, setOutdoorVariant] = useState<'sunlight' | 'oled'>('sunlight');
  const [showCancelModal, setShowCancelModal] = useState<boolean>(false);
  const [downloadSuccess, setDownloadSuccess] = useState<boolean>(false);

  // Selected pass resolution
  const currentPass: EcoPass | null =
    activePass ||
    (passes.length > 0
      ? passes.find((p) => p.id === activePassId) || passes[0]
      : null);

  // Helper to find mobility details
  const getMobilityInfo = (mode: string) => {
    return MOBILITY_OPTIONS.find((m) => m.id === mode) || MOBILITY_OPTIONS[0];
  };

  // SVG Pass Download Action
  const handleDownloadSvg = () => {
    if (!currentPass) return;

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
  <text x="30" y="45" font-family="'Source Sans 3', sans-serif" font-size="11" font-weight="bold" fill="#B7E4C7" letter-spacing="2">ECOPARK CAMEROUN · YAOUNDÉ – AHALA BARRIÈRE (RN3)</text>
  <text x="30" y="80" class="title" fill="#FFFFFF">Pass QR Officiel d Accès (Dès 500 FCFA)</text>

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

  <text x="320" y="630" class="label">Mode d Acheminement</text>
  <text x="320" y="650" class="value">${currentPass.mobilityMode.toUpperCase()} (-${currentPass.discountAppliedPercent}%)</text>

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

  // Empty State
  if (!currentPass || passes.length === 0) {
    return (
      <div className="max-w-2xl mx-auto p-8 rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-default)] text-center space-y-5">
        <div className="w-16 h-16 rounded-2xl bg-emerald-100 dark:bg-emerald-950 text-emerald-700 dark:text-emerald-300 mx-auto flex items-center justify-center">
          <Ticket className="w-8 h-8" />
        </div>
        <div>
          <h2 className="font-['Barlow_Semi_Condensed'] text-2xl font-bold text-[var(--text-primary)]">
            Aucun Éco-Pass enregistré
          </h2>
          <p className="text-xs text-[var(--text-muted)] mt-1.5 max-w-md mx-auto leading-relaxed">
            Pour accéder aux sentiers de la réserve et réguler la capacité écologique, réservez votre créneau dès maintenant.
          </p>
        </div>
        <button
          onClick={() => setActiveView('billetterie')}
          className="px-6 py-3 rounded-xl bg-[var(--brand-primary)] text-white font-bold text-sm shadow-xs hover:bg-[var(--brand-secondary)] cursor-pointer inline-flex items-center gap-2"
        >
          <span>Accéder à la billetterie régulée</span>
          <ArrowRight className="w-4 h-4" />
        </button>
      </div>
    );
  }

  const mobilityInfo = getMobilityInfo(currentPass.mobilityMode);

  return (
    <div className="space-y-6">
      {/* Pass Switcher & Controls */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-4 rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-default)]">
        <div>
          <span className="text-xs font-semibold text-[var(--brand-primary)] uppercase tracking-wider">
            Portefeuille Éco-Pass ({passes.length})
          </span>
          <div className="flex flex-wrap items-center gap-2 mt-1">
            {passes.map((pass) => (
              <button
                key={pass.id}
                onClick={() => setActivePassId(pass.id)}
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

        {/* Outdoor Mode Controls */}
        <div className="flex items-center gap-2">
          <button
            onClick={() => setHighContrastOutdoor(!highContrastOutdoor)}
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

      {/* Main Digital Pass Card Container */}
      <div
        id="printable-eco-pass"
        className={`max-w-2xl mx-auto rounded-3xl transition-all duration-300 overflow-hidden shadow-lg border ${
          highContrastOutdoor && outdoorVariant === 'oled'
            ? 'bg-black text-[#52B788] border-emerald-900 ring-2 ring-emerald-500/30'
            : highContrastOutdoor && outdoorVariant === 'sunlight'
            ? 'bg-white text-black border-4 border-black'
            : 'bg-[var(--bg-surface)] text-[var(--text-primary)] border-[var(--border-default)]'
        }`}
      >
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
              ECOPARK CAMEROUN · YAOUNDÉ – AHALA BARRIÈRE (FACE TRADEX RN3)
            </span>
            <h2 className="font-['Barlow_Semi_Condensed'] text-2xl font-bold mt-0.5">
              Pass QR Officiel — Complexe Écologique &amp; Loisirs
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
              <div className="font-bold text-sm capitalize text-[var(--text-primary)]">
                {currentPass.experienceType.replace('_', ' ')}
              </div>
            </div>
          </div>

          {/* QR Code Presentation Box */}
          <div className="flex flex-col items-center justify-center p-6 rounded-2xl bg-[var(--bg-elevated)] border border-[var(--border-default)] space-y-3">
            <div className="p-4 rounded-xl bg-white shadow-xs border border-gray-200">
              <QRCodeSVG
                value={
                  currentPass.qrPayload ||
                  `ECOPARK:PASS:${currentPass.id}:DATE=${currentPass.visitDate}:GUESTS=${currentPass.guestCount}`
                }
                size={180}
                fgColor="#1B4332"
                bgColor="#FFFFFF"
                quietZone={2}
                title={`Éco-Pass QR Code pour ${currentPass.id}`}
              />
            </div>

            <div className="text-center space-y-1">
              <span className="text-xs font-mono font-semibold text-[var(--text-primary)]">
                Scannable aux portiques et par les Éco-Gardes
              </span>
              <p className="text-[11px] text-[var(--text-muted)] font-mono">
                Payload SVG vectoriel certifié ISO/IEC 18004
              </p>
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

        {/* Pass Actions Bar */}
        <div className="p-6 bg-[var(--bg-canvas)] border-t border-[var(--border-default)] flex flex-wrap items-center justify-between gap-3 print:hidden">
          {/* Check-In Action Button */}
          {currentPass.status === 'confirmed' ? (
            <button
              onClick={() => checkInPass(currentPass.id)}
              className="px-4 py-2.5 rounded-xl bg-emerald-700 hover:bg-emerald-800 text-white font-bold text-xs shadow-xs cursor-pointer flex items-center gap-1.5 active:scale-95 transition-transform"
            >
              <CheckCircle2 className="w-4 h-4" />
              <span>Valider l entrée terrain (Check-In)</span>
            </button>
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

            {currentPass.status !== 'cancelled' && (
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
