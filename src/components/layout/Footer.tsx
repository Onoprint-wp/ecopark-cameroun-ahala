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
      className="bg-[#1F2421] text-[#E9F5ED] border-t border-[#36403A] pt-14 pb-10 transition-colors overflow-x-clip"
      role="contentinfo"
      aria-label="Pied de page ECOPARK CAMEROUN Yaoundé-Ahala"
    >
      <div className="eco-container">
        {/* Top Grid: Brand, Nav, Contacts Ahala, Horaires */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-10 pb-12 border-b border-[#36403A]/70">
          {/* Column 1: Identity & Legal MPECK MULTI-SERVICES */}
          <div className="space-y-4 min-w-0 break-words">
            <div className="flex items-center gap-3 min-w-0">
              <img
                src="/images/ahala/cropped-LOGO-ECOPARK-Youtube.png"
                alt="Logo Officiel ECOPARK CAMEROUN"
                className="w-11 h-11 rounded-full object-cover border-2 border-[#52B788] bg-white shadow-md shrink-0"
              />
              <div className="min-w-0">
                <span className="type-h3 text-white block break-words">
                  ECOPARK CAMEROUN
                </span>
                <span className="type-badge text-[#B7E4C7] uppercase">
                  Yaoundé, Ahala • RN3
                </span>
              </div>
            </div>

            <p className="type-body-compact text-[#C9D1CC] leading-relaxed">
              Complexe écologique, touristique, hôtelier (30 unités : Ewondo, Chanthel &amp; Bene), gastronomique (<em>Le Château des Saveurs</em>) et Centre de Formation Professionnelle agréé par le <strong>MINEFOP</strong>.
            </p>

            <div className="pt-1 space-y-1 type-footnote text-[#B7E4C7]">
              <div className="flex items-center gap-2">
                <ShieldCheck className="w-4 h-4 text-[#74C69D] shrink-0" />
                <span>
                  <strong>MPECK MULTI-SERVICES</strong> • Fondateur : <strong>Dr Christophe FOE NDI</strong>
                </span>
              </div>
            </div>
          </div>

          {/* Column 2: Navigation Publique & Espace Cliente */}
          <div className="space-y-3 min-w-0 break-words">
            <h3 className="type-card-title text-white">
              Les Pôles d&apos;EcoPark Ahala
            </h3>
            <ul className="space-y-0.5 text-[0.9375rem] text-[#C9D1CC]">
              <li>
                <button
                  type="button"
                  onClick={(e) => handleLinkClick('accueil', e)}
                  className="inline-flex items-center min-h-[44px] py-1.5 hover:text-[#74C69D] transition-colors cursor-pointer text-left"
                >
                  Accueil, Hôtels (30), Château des Saveurs &amp; CFP
                </button>
              </li>
              <li>
                <button
                  type="button"
                  onClick={(e) => handleLinkClick('sentiers', e)}
                  className="inline-flex items-center min-h-[44px] py-1.5 hover:text-[#74C69D] transition-colors cursor-pointer text-left"
                >
                  Plan du Parc, Lac, Pirogues &amp; Piscine Semi-Olympique
                </button>
              </li>
              <li>
                <button
                  type="button"
                  onClick={(e) => handleLinkClick('biodiversite', e)}
                  className="inline-flex items-center min-h-[44px] py-1.5 hover:text-[#74C69D] transition-colors cursor-pointer text-left"
                >
                  Jardin Zoologique (Gorille ToTo, Chimpanzés, Tortues)
                </button>
              </li>
              <li>
                <button
                  type="button"
                  onClick={(e) => handleLinkClick('billetterie', e)}
                  className="inline-flex items-center min-h-[44px] py-1.5 hover:text-[#74C69D] transition-colors cursor-pointer text-left"
                >
                  Réserver un Pass QR (dès 500 FCFA · OM / MoMo)
                </button>
              </li>
              <li>
                <button
                  type="button"
                  onClick={(e) => handleLinkClick('pass', e)}
                  className="inline-flex items-center min-h-[44px] py-1.5 hover:text-[#74C69D] transition-colors cursor-pointer text-left"
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
                  className="inline-flex items-center min-h-[44px] py-1.5 hover:text-[#95D5B2] transition-colors text-[#74C69D] font-medium cursor-pointer text-left"
                >
                  Connexion / Créer un Compte Cliente
                </button>
              </li>
            </ul>
          </div>

          {/* Column 3: Coordonnées Officielles Yaoundé-Ahala (100% Cliquables) */}
          <div className="space-y-3 min-w-0 break-words">
            <h3 className="type-card-title text-white">
              Contacts &amp; Accès Officiels
            </h3>
            <div className="space-y-2.5 text-[0.9375rem] text-[#C9D1CC]">
              <div className="flex items-start gap-2.5">
                <MapPin className="w-4 h-4 text-[#74C69D] mt-1 shrink-0" />
                <div>
                  <div className="font-semibold text-white">Quartier Ahala Barrière, Yaoundé</div>
                  <div className="type-footnote text-[#B7E4C7]">
                    En face de la station-service Tradex Ahala (RN3, route 100 % goudronnée • Parking gratuit)
                  </div>
                </div>
              </div>

              <div className="flex items-start gap-2.5">
                <PhoneCall className="w-4 h-4 text-[#74C69D] mt-1 shrink-0" />
                <div className="space-y-0.5 min-w-0">
                  <div className="font-mono text-sm font-medium text-white flex flex-wrap items-center gap-x-1">
                    <a href="tel:+237672564598" className="hover:text-[#74C69D] hover:underline inline-flex items-center min-h-[44px] xl:min-h-[36px]">
                      +237 672 56 45 98
                    </a>
                    <span>/</span>
                    <a href="tel:+237697136203" className="hover:text-[#74C69D] hover:underline inline-flex items-center min-h-[44px] xl:min-h-[36px]">
                      +237 697 13 62 03
                    </a>
                  </div>
                  <div className="type-footnote text-[#B7E4C7]">
                    Hôtels &amp; Cités 24h/24 :{' '}
                    <a
                      href="tel:+237694601449"
                      className="text-[#D8F3DC] hover:text-white font-mono hover:underline inline-flex items-center min-h-[44px] xl:min-h-0"
                    >
                      +237 694 60 14 49
                    </a>
                  </div>
                </div>
              </div>

              <div className="flex items-start gap-2.5">
                <Mail className="w-4 h-4 text-[#74C69D] mt-1 shrink-0" />
                <div className="min-w-0">
                  <a
                    href="mailto:info@ecopark-yaounde.com"
                    className="font-mono text-sm text-white hover:text-[#74C69D] hover:underline inline-flex items-center min-h-[44px] xl:min-h-0 break-all"
                  >
                    info@ecopark-yaounde.com
                  </a>
                  <div className="type-footnote text-[#B7E4C7]">
                    Devis Groupes, Écoles, Salle 500 pl. &amp; CFP MINEFOP
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Column 4: Horaires Officiels & Météo d'Ahala */}
          <div className="space-y-3 min-w-0">
            <h3 className="type-card-title text-white">
              Horaires &amp; Météo d&apos;Ahala
            </h3>
            <div className="p-3.5 rounded-xl bg-[#29302C] border border-[#46534B] space-y-2.5 type-footnote font-mono text-[#E9F5ED] tabular-nums">
              <div className="flex flex-wrap items-baseline justify-between gap-x-2 gap-y-0.5 min-w-0">
                <span className="text-[#B7E4C7] flex items-center gap-1.5 min-w-0">
                  <Sun className="w-3.5 h-3.5 text-amber-400 shrink-0" /> Parc &amp; Loisirs
                </span>
                <span className="text-white font-bold whitespace-normal">Mar au Dim 09h à 18h</span>
              </div>
              <div className="flex flex-wrap items-baseline justify-between gap-x-2 gap-y-0.5 min-w-0">
                <span className="text-[#B7E4C7] flex items-center gap-1.5 min-w-0">
                  <Leaf className="w-3.5 h-3.5 text-[#74C69D] shrink-0" /> Hôtels Ewondo / Chanthel / Bene
                </span>
                <span className="text-[#74C69D] font-bold whitespace-normal">24h/24 · 7j/7</span>
              </div>
              <div className="flex flex-wrap items-baseline justify-between gap-x-2 gap-y-0.5 min-w-0">
                <span className="text-[#B7E4C7] flex items-center gap-1.5 min-w-0">
                  <Wind className="w-3.5 h-3.5 text-sky-400 shrink-0" /> Château des Saveurs
                </span>
                <span className="text-sky-300 font-bold whitespace-normal">7j/7 · 07h à 23h</span>
              </div>
              <div className="flex flex-wrap items-baseline justify-between gap-x-2 gap-y-0.5 pt-1.5 border-t border-[#36403A] min-w-0">
                <span className="text-[#B7E4C7]">Repos biologique</span>
                <span className="text-amber-300 font-bold whitespace-normal">Lundi (Parc)</span>
              </div>
              <div className="flex flex-wrap items-baseline justify-between gap-x-2 gap-y-0.5 pt-1.5 border-t border-[#36403A] min-w-0">
                <span className="text-[#B7E4C7]">Météo Ahala</span>
                <span className="text-white whitespace-normal">
                  {telemetry.temperatureC}°C · {telemetry.weatherCondition.split('·')[0].trim()}
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Bottom Bar: Copyright, Legal Pages & Discreet Staff Access */}
        <div className="pt-8 flex flex-col lg:flex-row items-center justify-between gap-4 type-footnote text-[#B7E4C7] tabular-nums">
          <div className="text-center lg:text-left">
            © 2026 MPECK MULTI-SERVICES • ECOPARK CAMEROUN (Yaoundé, Ahala Barrière, RN3). Tous droits réservés.
          </div>

          <div className="flex flex-wrap items-center justify-center gap-x-3 gap-y-1">
            <button
              type="button"
              onClick={(e) => handleLegalClick('/mentions-legales', e)}
              className="inline-flex items-center min-h-[44px] px-1 hover:text-white transition-colors cursor-pointer"
            >
              Mentions légales
            </button>
            <span aria-hidden="true">·</span>
            <button
              type="button"
              onClick={(e) => handleLegalClick('/cgv', e)}
              className="inline-flex items-center min-h-[44px] px-1 hover:text-white transition-colors cursor-pointer"
            >
              CGV &amp; Billetterie FCFA
            </button>
            <span aria-hidden="true">·</span>
            <button
              type="button"
              onClick={(e) => handleLegalClick('/confidentialite', e)}
              className="inline-flex items-center min-h-[44px] px-1 hover:text-white transition-colors cursor-pointer"
            >
              Confidentialité (Loi 2010/012)
            </button>
            <span aria-hidden="true">·</span>
            <button
              type="button"
              onClick={handleStaffCockpitClick}
              className="inline-flex items-center gap-1 min-h-[44px] px-2 text-[#D8F3DC] hover:text-amber-300 transition-colors cursor-pointer"
              title="Accès réservé au personnel habilité MPECK MULTI-SERVICES"
            >
              <Lock className="w-3.5 h-3.5" />
              <span>Cockpit Pro</span>
            </button>
          </div>
        </div>
      </div>
    </footer>
  );
};
