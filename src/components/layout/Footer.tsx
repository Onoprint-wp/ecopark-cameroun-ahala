// ============================================================================
// ECOPARK CAMEROUN (YAOUNDÉ, AHALA) - OFFICIAL PRODUCTION FOOTER
// (src/components/layout/Footer.tsx)
// Cleaned Pre-Launch Footer: Clickable Contacts, Legal Links & Discreet Staff Access
// ============================================================================

import React from 'react';
import {
  PhoneCall,
  Sun,
  Wind,
  Leaf,
  ShieldCheck,
  MapPin,
  Mail,
  Lock,
} from 'lucide-react';
import { useEcoPark } from '../../context/EcoParkContext';
import { useAuth } from '../../context/AuthContext';
import { ActiveView } from '../../types/ecosystem';
import { recordMotionOrigin } from '../../utils/ecoMotion';

export const Footer: React.FC = () => {
  const { telemetry, setActiveView } = useEcoPark();
  const { isStaff, setAuthPortalMode } = useAuth();

  const handleLinkClick = (view: ActiveView, e?: React.MouseEvent<HTMLElement>) => {
    if (e) recordMotionOrigin(e);
    setActiveView(view);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleLegalClick = (path: string, e: React.MouseEvent<HTMLButtonElement>) => {
    recordMotionOrigin(e);
    window.history.pushState({}, '', path);
    window.dispatchEvent(new PopStateEvent('popstate'));
    setActiveView('legal');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleStaffCockpitClick = (e: React.MouseEvent<HTMLButtonElement>) => {
    recordMotionOrigin(e);
    if (isStaff) {
      setActiveView('ranger');
    } else {
      setAuthPortalMode('staff_login');
      setActiveView('connexion');
    }
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <footer
      className="bg-[#1F2421] text-[#E9F5ED] border-t border-[#36403A] pt-14 pb-10 transition-colors"
      role="contentinfo"
      aria-label="Pied de page ECOPARK CAMEROUN Yaoundé-Ahala"
    >
      <div className="eco-container">
        {/* Top Grid: Brand, Nav, Contacts Ahala, Horaires */}
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
                <span className="font-['Barlow_Semi_Condensed'] font-bold text-[21px] leading-[25px] tracking-[0.011em] text-white block">
                  ECOPARK CAMEROUN
                </span>
                <span className="text-xs text-[#8EBAA0] font-semibold tracking-wide uppercase">
                  Yaoundé, Ahala • RN3
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

          {/* Column 2: Navigation Publique & Espace Cliente */}
          <div className="space-y-3">
            <h3 className="text-base font-semibold text-white">
              Les Pôles d&apos;EcoPark Ahala
            </h3>
            <ul className="space-y-2 text-sm text-[#C9D1CC]">
              <li>
                <button
                  type="button"
                  onClick={(e) => handleLinkClick('accueil', e)}
                  className="hover:text-[#52B788] transition-colors cursor-pointer text-left"
                >
                  Accueil, Hôtels (30), Château des Saveurs &amp; CFP
                </button>
              </li>
              <li>
                <button
                  type="button"
                  onClick={(e) => handleLinkClick('sentiers', e)}
                  className="hover:text-[#52B788] transition-colors cursor-pointer text-left"
                >
                  Plan du Parc, Lac, Pirogues &amp; Piscine Semi-Olympique
                </button>
              </li>
              <li>
                <button
                  type="button"
                  onClick={(e) => handleLinkClick('biodiversite', e)}
                  className="hover:text-[#52B788] transition-colors cursor-pointer text-left"
                >
                  Jardin Zoologique (Gorille ToTo, Chimpanzés, Tortues)
                </button>
              </li>
              <li>
                <button
                  type="button"
                  onClick={(e) => handleLinkClick('billetterie', e)}
                  className="hover:text-[#52B788] transition-colors cursor-pointer text-left"
                >
                  Réserver un Pass QR (dès 500 FCFA · OM / MoMo)
                </button>
              </li>
              <li>
                <button
                  type="button"
                  onClick={(e) => handleLinkClick('pass', e)}
                  className="hover:text-[#52B788] transition-colors cursor-pointer text-left"
                >
                  Mon Espace Cliente &amp; Mes Billets QR
                </button>
              </li>
              <li>
                <button
                  type="button"
                  onClick={(e) => {
                    setAuthPortalMode('client_login');
                    handleLinkClick('connexion', e);
                  }}
                  className="hover:text-[#52B788] transition-colors text-[#74C69D] font-medium cursor-pointer text-left"
                >
                  Connexion / Créer un Compte Cliente
                </button>
              </li>
            </ul>
          </div>

          {/* Column 3: Coordonnées Officielles Yaoundé-Ahala (100% Cliquables) */}
          <div className="space-y-3">
            <h3 className="text-base font-semibold text-white">
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
                <div className="space-y-0.5">
                  <div className="font-mono font-medium text-white">
                    <a href="tel:+237672564598" className="hover:text-[#74C69D] hover:underline">
                      +237 672 56 45 98
                    </a>{' '}
                    /{' '}
                    <a href="tel:+237697136203" className="hover:text-[#74C69D] hover:underline">
                      +237 697 13 62 03
                    </a>
                  </div>
                  <div className="text-xs text-[#8EBAA0]">
                    Hôtels &amp; Cités 24h/24 :{' '}
                    <a
                      href="tel:+237694601449"
                      className="text-[#B7E4C7] hover:text-white font-mono hover:underline"
                    >
                      +237 694 60 14 49
                    </a>
                  </div>
                </div>
              </div>

              <div className="flex items-start gap-2.5">
                <Mail className="w-4 h-4 text-[#52B788] mt-0.5 shrink-0" />
                <div>
                  <a
                    href="mailto:info@ecopark-yaounde.com"
                    className="font-mono text-xs text-white hover:text-[#74C69D] hover:underline block"
                  >
                    info@ecopark-yaounde.com
                  </a>
                  <div className="text-xs text-[#8EBAA0]">
                    Devis Groupes, Écoles, Salle 500 pl. &amp; CFP MINEFOP
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Column 4: Horaires Officiels & Météo d'Ahala */}
          <div className="space-y-3">
            <h3 className="text-base font-semibold text-white">
              Horaires &amp; Météo d&apos;Ahala
            </h3>
            <div className="p-3.5 rounded-xl bg-[#29302C] border border-[#46534B] space-y-2 text-xs font-mono tabular-nums">
              <div className="flex items-center justify-between">
                <span className="text-[#8EBAA0] flex items-center gap-1.5">
                  <Sun className="w-3.5 h-3.5 text-amber-400" /> Parc &amp; Loisirs
                </span>
                <span className="text-white font-bold">Mar au Dim 09h à 18h</span>
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
                <span className="text-sky-300 font-bold">7j/7 · 07h à 23h</span>
              </div>
              <div className="flex items-center justify-between pt-1 border-t border-[#36403A]">
                <span className="text-[#8EBAA0]">Repos biologique</span>
                <span className="text-amber-300 font-bold">Lundi (Parc)</span>
              </div>
              <div className="flex items-center justify-between pt-1 border-t border-[#36403A]">
                <span className="text-[#8EBAA0]">Météo Ahala</span>
                <span className="text-white">
                  {telemetry.temperatureC}°C · {telemetry.weatherCondition.split('·')[0].trim()}
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Bottom Bar: Copyright, Legal Pages & Discreet Staff Access */}
        <div className="pt-8 flex flex-col lg:flex-row items-center justify-between gap-4 text-xs text-[#8EBAA0] tabular-nums">
          <div className="text-center lg:text-left">
            © 2026 MPECK MULTI-SERVICES • ECOPARK CAMEROUN (Yaoundé, Ahala Barrière, RN3). Tous droits réservés.
          </div>

          <div className="flex flex-wrap items-center justify-center gap-x-4 gap-y-2">
            <button
              type="button"
              onClick={(e) => handleLegalClick('/mentions-legales', e)}
              className="hover:text-white transition-colors cursor-pointer"
            >
              Mentions légales
            </button>
            <span>·</span>
            <button
              type="button"
              onClick={(e) => handleLegalClick('/cgv', e)}
              className="hover:text-white transition-colors cursor-pointer"
            >
              CGV &amp; Billetterie FCFA
            </button>
            <span>·</span>
            <button
              type="button"
              onClick={(e) => handleLegalClick('/confidentialite', e)}
              className="hover:text-white transition-colors cursor-pointer"
            >
              Confidentialité (Loi 2010/012)
            </button>
            <span>·</span>
            <button
              type="button"
              onClick={handleStaffCockpitClick}
              className="inline-flex items-center gap-1 text-[#A7C4B5] hover:text-amber-300 transition-colors cursor-pointer"
              title="Accès réservé au personnel habilité MPECK MULTI-SERVICES"
            >
              <Lock className="w-3 h-3" />
              <span>Cockpit Pro</span>
            </button>
          </div>
        </div>
      </div>
    </footer>
  );
};
