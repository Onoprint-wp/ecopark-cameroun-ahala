// ============================================================================
// ECOPARK CAMEROUN (YAOUNDÉ – AHALA) — OFFICIAL FOOTER
// (src/components/layout/Footer.tsx)
// ============================================================================

import React from 'react';
import {
  PhoneCall,
  Sun,
  Wind,
  Leaf,
  ShieldCheck,
  RotateCcw,
  Sparkles,
  ExternalLink,
  MapPin,
  Mail,
} from 'lucide-react';
import { useEcoPark } from '../../context/EcoParkContext';
import { ActiveView } from '../../types/ecosystem';
import { recordMotionOrigin, useEcoMotion } from '../../utils/ecoMotion';

export const Footer: React.FC = () => {
  const { telemetry, effectiveTheme, setActiveView, setColorDrawerOpen, resetToSeedData } = useEcoPark();
  const motionState = useEcoMotion(effectiveTheme === 'dark');

  const handleLinkClick = (view: ActiveView, e?: React.MouseEvent<HTMLElement>) => {
    if (e) recordMotionOrigin(e);
    setActiveView(view);
  };

  const handleResetDemo = () => {
    if (
      window.confirm(
        'Réinitialiser les données de simulation (circuits, réservations FCFA, signalements et télémétrie) ?'
      )
    ) {
      resetToSeedData();
    }
  };

  return (
    <footer
      className="bg-[#1F2421] text-[#E9F5ED] border-t border-[#36403A] pt-14 pb-10 transition-colors"
      role="contentinfo"
      aria-label="Pied de page ECOPARK CAMEROUN Yaoundé-Ahala"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Top Grid: Brand, Nav, Contacts Ahala, Telemetry */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-10 pb-12 border-b border-[#36403A]/70">
          {/* Column 1: Identity & Legal MPECK MULTI-SERVICES */}
          <div className="space-y-4">
            <div className="flex items-center gap-3">
              <img
                src="/images/ahala/cropped-LOGO-ECOPARK-Youtube.png"
                alt="Logo Officiel ECOPARK CAMEROUN"
                className="w-11 h-11 rounded-full object-cover border-2 border-[#52B788] bg-white shadow-md"
              />
              <div>
                <span className="font-['Barlow_Semi_Condensed'] font-bold text-xl tracking-tight text-white block">
                  ECOPARK CAMEROUN
                </span>
                <span className="text-xs text-[#8EBAA0] font-semibold tracking-wide uppercase">
                  Yaoundé – Ahala • RN3
                </span>
              </div>
            </div>

            <p className="text-xs sm:text-sm text-[#C9D1CC] leading-relaxed">
              Complexe écologique, touristique, hôtelier (30 unités : Ewondo, Chanthel &amp; Bene), gastronomique (<em>Le Château des Saveurs</em>) et Centre de Formation Professionnelle agréé par le <strong>MINEFOP</strong>.
            </p>

            <div className="pt-1 space-y-1 text-xs text-[#8EBAA0]">
              <div className="flex items-center gap-2">
                <ShieldCheck className="w-4 h-4 text-[#52B788] shrink-0" />
                <span>
                  <strong>MPECK MULTI-SERVICES</strong> • Fondateur : <strong>Dr Christophe FOE NDI</strong>
                </span>
              </div>
            </div>
          </div>

          {/* Column 2: Navigation Rapide */}
          <div className="space-y-3">
            <h3 className="font-['Barlow_Semi_Condensed'] text-base font-semibold text-white tracking-wide">
              Les Pôles d&apos;EcoPark Ahala
            </h3>
            <ul className="space-y-2 text-sm text-[#C9D1CC]">
              <li>
                <button
                  onClick={(e) => handleLinkClick('accueil', e)}
                  className="hover:text-[#52B788] transition-colors cursor-pointer text-left"
                >
                  Accueil, Hôtels (30), Château des Saveurs &amp; CFP
                </button>
              </li>
              <li>
                <button
                  onClick={(e) => handleLinkClick('sentiers', e)}
                  className="hover:text-[#52B788] transition-colors cursor-pointer text-left"
                >
                  Plan du Parc, Lac, Pirogues &amp; Piscine Semi-Olympique
                </button>
              </li>
              <li>
                <button
                  onClick={(e) => handleLinkClick('biodiversite', e)}
                  className="hover:text-[#52B788] transition-colors cursor-pointer text-left"
                >
                  Jardin Zoologique (Gorille ToTo, Chimpanzés, Tortues)
                </button>
              </li>
              <li>
                <button
                  onClick={(e) => handleLinkClick('billetterie', e)}
                  className="hover:text-[#52B788] transition-colors cursor-pointer text-left"
                >
                  Réserver un Pass QR (dès 500 FCFA · OM / MoMo)
                </button>
              </li>
              <li>
                <button
                  onClick={(e) => handleLinkClick('pass', e)}
                  className="hover:text-[#52B788] transition-colors cursor-pointer text-left"
                >
                  Mon Pass QR (ECP-2026-XXXXX) &amp; Avis Visiteurs
                </button>
              </li>
              <li>
                <button
                  onClick={(e) => handleLinkClick('ranger', e)}
                  className="hover:text-[#52B788] transition-colors text-amber-300 font-medium cursor-pointer text-left"
                >
                  Console de Supervision &amp; Exploitation Ahala
                </button>
              </li>
            </ul>
          </div>

          {/* Column 3: Coordonnées Officielles Yaoundé-Ahala */}
          <div className="space-y-3">
            <h3 className="font-['Barlow_Semi_Condensed'] text-base font-semibold text-white tracking-wide">
              Contacts &amp; Accès Officiels
            </h3>
            <div className="space-y-2.5 text-xs sm:text-sm text-[#C9D1CC]">
              <div className="flex items-start gap-2.5">
                <MapPin className="w-4 h-4 text-[#52B788] mt-0.5 shrink-0" />
                <div>
                  <div className="font-semibold text-white">Quartier Ahala Barrière, Yaoundé</div>
                  <div className="text-xs text-[#8EBAA0]">
                    En face de la station-service Tradex Ahala (RN3, route 100 % goudronnée • Parking gratuit)
                  </div>
                </div>
              </div>

              <div className="flex items-start gap-2.5">
                <PhoneCall className="w-4 h-4 text-[#52B788] mt-0.5 shrink-0" />
                <div>
                  <div className="font-mono font-medium text-white">+237 672 56 45 98 / +237 697 13 62 03</div>
                  <div className="text-xs text-[#8EBAA0]">Hôtels &amp; Cités 24h/24 : +237 694 60 14 49</div>
                </div>
              </div>

              <div className="flex items-start gap-2.5">
                <Mail className="w-4 h-4 text-[#52B788] mt-0.5 shrink-0" />
                <div>
                  <div className="font-mono text-xs text-white">info@ecopark-yaounde.com</div>
                  <div className="text-xs text-[#8EBAA0]">Devis Groupes, Écoles, Salle 500 pl. &amp; CFP</div>
                </div>
              </div>

              <div className="pt-1">
                <a
                  href="/color-atlas-standalone.html"
                  target="_blank"
                  rel="noreferrer"
                  className="inline-flex items-center gap-1.5 text-xs text-[#74C69D] hover:underline"
                >
                  <span>Charte Chromatique Adobe Color Standalone</span>
                  <ExternalLink className="w-3 h-3" />
                </a>
              </div>
            </div>
          </div>

          {/* Column 4: Télémétrie & Horaires Officiels */}
          <div className="space-y-3">
            <h3 className="font-['Barlow_Semi_Condensed'] text-base font-semibold text-white tracking-wide">
              Horaires &amp; Météo d&apos;Ahala
            </h3>
            <div className="p-3.5 rounded-xl bg-[#29302C] border border-[#46534B] space-y-2 text-xs font-mono">
              <div className="flex items-center justify-between">
                <span className="text-[#8EBAA0] flex items-center gap-1.5">
                  <Sun className="w-3.5 h-3.5 text-amber-400" /> Parc &amp; Loisirs
                </span>
                <span className="text-white font-bold">Mar–Dim 09h–18h</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-[#8EBAA0] flex items-center gap-1.5">
                  <Leaf className="w-3.5 h-3.5 text-[#52B788]" /> Hôtels Ewondo/Chanthel/Bene
                </span>
                <span className="text-[#52B788] font-bold">24h/24 · 7j/7</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-[#8EBAA0] flex items-center gap-1.5">
                  <Wind className="w-3.5 h-3.5 text-sky-400" /> Château des Saveurs
                </span>
                <span className="text-sky-300 font-bold">7j/7 · 07h–23h</span>
              </div>
              <div className="flex items-center justify-between pt-1 border-t border-[#36403A]">
                <span className="text-[#8EBAA0]">Météo Ahala</span>
                <span className="text-white">{telemetry.temperatureC}°C · {telemetry.weatherCondition.split('·')[0]}</span>
              </div>
              <div className="flex items-center justify-between pt-1 border-t border-[#36403A]">
                <span className="text-[#8EBAA0]">Sobriété Cinétique</span>
                <span className="text-[#52B788] font-bold">
                  {motionState.reducedMotion
                    ? 'Mouvement Réduit'
                    : motionState.oledEcoPaused
                    ? 'OLED · Pause Ambiante'
                    : 'GPU 0-Layout'}
                </span>
              </div>
            </div>

            <div className="flex items-center justify-between pt-1">
              <button
                onClick={() => setColorDrawerOpen(true)}
                className="inline-flex items-center gap-1.5 text-xs text-[#74C69D] hover:text-white transition-colors cursor-pointer"
              >
                <Sparkles className="w-3.5 h-3.5" />
                <span>Ouvrir l&apos;Atelier Couleurs</span>
              </button>

              <button
                onClick={handleResetDemo}
                className="inline-flex items-center gap-1 text-xs text-[#8EBAA0] hover:text-red-300 transition-colors cursor-pointer"
                title="Rétablir les données initiales"
              >
                <RotateCcw className="w-3 h-3" />
                <span>Reset Démo</span>
              </button>
            </div>
          </div>
        </div>

        {/* Bottom Bar: Copyright & Ecological Standards */}
        <div className="pt-8 flex flex-col md:flex-row items-center justify-between gap-4 text-xs text-[#8EBAA0]">
          <div>
            © 2026 MPECK MULTI-SERVICES — ECOPARK CAMEROUN (Yaoundé – Ahala Barrière, RN3). Tous droits réservés.
          </div>
          <div className="flex flex-wrap items-center gap-3">
            <span>Polices : Barlow Semi Condensed &amp; Source Sans 3</span>
            <span>·</span>
            <span>Conformité WCAG 2.1 AAA</span>
            <span>·</span>
            <span>Paiement Orange Money &amp; MTN MoMo</span>
          </div>
        </div>
      </div>
    </footer>
  );
};
