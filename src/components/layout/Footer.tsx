// ============================================================================
// ECO-PARK ECOLOGICAL FOOTER (src/components/layout/Footer.tsx)
// ============================================================================

import React from 'react';
import {
  Trees,
  PhoneCall,
  Sun,
  Wind,
  Leaf,
  ShieldCheck,
  RotateCcw,
  Sparkles,
  ExternalLink,
} from 'lucide-react';
import { useEcoPark } from '../../context/EcoParkContext';
import { ActiveView } from '../../types/ecosystem';

export const Footer: React.FC = () => {
  const { telemetry, setActiveView, setColorDrawerOpen, resetToSeedData } = useEcoPark();

  const handleLinkClick = (view: ActiveView) => {
    setActiveView(view);
  };

  const handleResetDemo = () => {
    if (
      window.confirm(
        'Réinitialiser toutes les données de simulation (sentiers, réservations, signalements et télémétrie) ?'
      )
    ) {
      resetToSeedData();
    }
  };

  return (
    <footer
      className="bg-[#1F2421] text-[#E9F5ED] border-t border-[#36403A] pt-14 pb-10 transition-colors"
      role="contentinfo"
      aria-label="Pied de page ECO-PARK"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Top Grid: Brand, Nav, Emergency, Telemetry */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-10 pb-12 border-b border-[#36403A]/70">
          {/* Column 1: Identity & Ecological Charter */}
          <div className="space-y-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-[#52B788] to-[#1B4332] flex items-center justify-center text-white shadow-md">
                <Trees className="w-5 h-5 text-white" />
              </div>
              <div>
                <span className="font-['Fraunces'] font-bold text-xl tracking-tight text-white block">
                  ECO-PARK
                </span>
                <span className="text-xs text-[#8EBAA0] font-medium tracking-wide uppercase">
                  Sanctuaire Naturel
                </span>
              </div>
            </div>

            <p className="text-sm text-[#C9D1CC] leading-relaxed">
              Réserve biologique intégrale de 420 hectares dédiée à la régénération forestière, à la
              sauvegarde de la biodiversité endémique et à l éco-tourisme régulé à faible impact.
            </p>

            <div className="pt-2 flex items-center gap-2 text-xs text-[#8EBAA0]">
              <ShieldCheck className="w-4 h-4 text-[#52B788]" />
              <span>Label Zéro Artificialisation Nette & RGESN 2026</span>
            </div>
          </div>

          {/* Column 2: Navigation Rapide */}
          <div className="space-y-3">
            <h3 className="font-['Fraunces'] text-base font-semibold text-white tracking-wide">
              Navigation Réserve
            </h3>
            <ul className="space-y-2 text-sm text-[#C9D1CC]">
              <li>
                <button
                  onClick={() => handleLinkClick('accueil')}
                  className="hover:text-[#52B788] transition-colors"
                >
                  Accueil & Découverte
                </button>
              </li>
              <li>
                <button
                  onClick={() => handleLinkClick('sentiers')}
                  className="hover:text-[#52B788] transition-colors"
                >
                  Carte Topographique & Sentiers
                </button>
              </li>
              <li>
                <button
                  onClick={() => handleLinkClick('biodiversite')}
                  className="hover:text-[#52B788] transition-colors"
                >
                  Atlas Faune & Flore Endémique
                </button>
              </li>
              <li>
                <button
                  onClick={() => handleLinkClick('billetterie')}
                  className="hover:text-[#52B788] transition-colors"
                >
                  Billetterie à Quota & Éco-Mobilité
                </button>
              </li>
              <li>
                <button
                  onClick={() => handleLinkClick('pass')}
                  className="hover:text-[#52B788] transition-colors"
                >
                  Mon Éco-Pass & Sentinelle Nature
                </button>
              </li>
              <li>
                <button
                  onClick={() => handleLinkClick('ranger')}
                  className="hover:text-[#52B788] transition-colors text-amber-300 font-medium"
                >
                  Console de Supervision Éco-Garde
                </button>
              </li>
            </ul>
          </div>

          {/* Column 3: Urgence & Contacts de Terrain */}
          <div className="space-y-3">
            <h3 className="font-['Fraunces'] text-base font-semibold text-white tracking-wide">
              Poste Éco-Garde & Urgence
            </h3>
            <div className="space-y-2.5 text-sm text-[#C9D1CC]">
              <div className="flex items-start gap-2.5">
                <PhoneCall className="w-4 h-4 text-[#52B788] mt-0.5 shrink-0" />
                <div>
                  <div className="font-mono font-medium text-white">04 76 00 12 34</div>
                  <div className="text-xs text-[#8EBAA0]">Poste Central de Secours (8h-20h)</div>
                </div>
              </div>

              <div className="flex items-start gap-2.5">
                <Wind className="w-4 h-4 text-[#52B788] mt-0.5 shrink-0" />
                <div>
                  <div className="font-mono text-xs text-white">Canal VHF : 161.425 MHz</div>
                  <div className="text-xs text-[#8EBAA0]">Fréquence radio des patrouilles</div>
                </div>
              </div>

              <div className="pt-2">
                <a
                  href="/color-atlas-standalone.html"
                  target="_blank"
                  rel="noreferrer"
                  className="inline-flex items-center gap-1.5 text-xs text-[#74C69D] hover:underline"
                >
                  <span>Prototype Atelier Chromatique Standalone</span>
                  <ExternalLink className="w-3 h-3" />
                </a>
              </div>
            </div>
          </div>

          {/* Column 4: Télémétrie en Direct */}
          <div className="space-y-3">
            <h3 className="font-['Fraunces'] text-base font-semibold text-white tracking-wide">
              Télémétrie Sanctuaire
            </h3>
            <div className="p-3.5 rounded-xl bg-[#29302C] border border-[#46534B] space-y-2.5 text-xs font-mono">
              <div className="flex items-center justify-between">
                <span className="text-[#8EBAA0] flex items-center gap-1.5">
                  <Sun className="w-3.5 h-3.5 text-amber-400" /> Autonomie Solaire
                </span>
                <span className="text-white font-bold">{telemetry.solarAutonomyPercent}%</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-[#8EBAA0] flex items-center gap-1.5">
                  <Leaf className="w-3.5 h-3.5 text-[#52B788]" /> CO₂ Évité Cumulé
                </span>
                <span className="text-[#52B788] font-bold">{telemetry.totalCo2AvoidedKg} kg</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-[#8EBAA0] flex items-center gap-1.5">
                  <Wind className="w-3.5 h-3.5 text-sky-400" /> Qualité de l Air
                </span>
                <span className="text-sky-300 font-bold">IQA {telemetry.airQualityIqa} · {telemetry.airQualityStatus}</span>
              </div>
              <div className="flex items-center justify-between pt-1 border-t border-[#36403A]">
                <span className="text-[#8EBAA0]">Météo locale</span>
                <span className="text-white">{telemetry.temperatureC}°C · {telemetry.weatherCondition.split('·')[0]}</span>
              </div>
            </div>

            <div className="flex items-center justify-between pt-1">
              <button
                onClick={() => setColorDrawerOpen(true)}
                className="inline-flex items-center gap-1.5 text-xs text-[#74C69D] hover:text-white transition-colors"
              >
                <Sparkles className="w-3.5 h-3.5" />
                <span>Ouvrir l Atelier Couleurs</span>
              </button>

              <button
                onClick={handleResetDemo}
                className="inline-flex items-center gap-1 text-xs text-[#8EBAA0] hover:text-red-300 transition-colors"
                title="Rétablir les données de simulation initiales"
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
            ECO-PARK © 2026 · Sanctuaire Protégé · Système d Information Forestier & Éco-Billetterie
          </div>
          <div className="flex items-center gap-4">
            <span>Conformité WCAG 2.1 AAA</span>
            <span>·</span>
            <span>Éco-Conception Numérique</span>
            <span>·</span>
            <span>Hébergement Bas-Carbone</span>
          </div>
        </div>
      </div>
    </footer>
  );
};
