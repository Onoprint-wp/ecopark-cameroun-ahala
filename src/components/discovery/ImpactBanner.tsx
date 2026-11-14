// ============================================================================
// ECOPARK CAMEROUN (YAOUNDE - AHALA) - BENTO REASSURANCE & PROGRESSIVE '+' DRAWERS
// (src/components/discovery/ImpactBanner.tsx)
// Fiche mémo n°4 : Temps 6 (Cartes Bento + bouton '+' 48x48px + BLUF 40-55 mots
// rendu en permanence dans le DOM HTML pour indexation GEO / IA et lecture épurée)
// ============================================================================

import React, { useState } from 'react';
import { ImmersiveSection } from '../layout/ImmersiveSection';
import {
  Sun,
  Leaf,
  Wind,
  ShieldCheck,
  Plus,
  Sparkles,
  CheckCircle2,
} from 'lucide-react';

export const ImpactBanner: React.FC = () => {
  const [expandedIds, setExpandedIds] = useState<Record<string, boolean>>({});

  const toggleCard = (id: string) => {
    setExpandedIds((prev) => ({ ...prev, [id]: !prev[id] }));
  };

  const metrics = [
    {
      id: 'loisirs',
      title: 'Loisirs, Zoo & Pirogue',
      value: 'Dès 500 FCFA',
      unit: 'enfant · 1 000 FCFA adulte',
      accentColor: '#F4A261',
      icon: Sun,
      summary: 'Accès famille du mardi au dimanche. Jardin Zoologique, lac et piscine surveillée.',
      bluf: "Situé à Yaoundé, Ahala Barrière face à la station Tradex sur la RN3, ECOPARK CAMEROUN ouvre du mardi au dimanche de 09h00 à 18h00. L'entrée coûte 500 FCFA par enfant et 1 000 FCFA par adulte, incluant le Jardin Zoologique du gorille ToTo et l'accès aux 3 Pass Tout-Inclus.",
      breakdown: [
        'Entrée Parc & Jardin Zoologique (Gorille ToTo, chimpanzés, tortues) : 500 FCFA enf. / 1 000 FCFA ad.',
        'Balade en Pirogue sur le lac (45 min, gilet fourni) : 500 FCFA enf. / 1 000 FCFA ad.',
        'Piscine Semi-Olympique surveillée : 1 500 FCFA enf. / 2 500 FCFA ad. (semaine & prévente)',
        'Manège équestre (500 / 1 000 FCFA), Musée Culturel (500 / 1 000 FCFA), Jeux (500 FCFA)',
      ],
      kpiNote: '3 Pass Tout-Inclus (1 QR Code) : 2 500 FCFA, 4 500 FCFA et 8 500 FCFA',
    },
    {
      id: 'hebergements',
      title: 'Cités Hôtelières 24h/24',
      value: '30 Unités',
      unit: 'Dès 10 000 FCFA / nuit',
      accentColor: '#52B788',
      icon: Leaf,
      summary: 'Réception ouverte 24h/24 et 7j/7. Calme forestier et parking sécurisé.',
      bluf: "Le pôle hôtelier d'ECOPARK CAMEROUN compte 30 unités climatisées réparties entre l'Hôtel Bene dès 10 000 FCFA, l'Hôtel Chanthel de 15 000 à 25 000 FCFA, l'Hôtel Ewondo VIP et 4 Suites Prestige jusqu'à 45 000 FCFA par nuitée, avec réception ouverte 24h/24 et parking gratuit sécurisé.",
      breakdown: [
        'Hôtel Bene (10 Chambres Standard & Day-Use, grande véranda) : 10 000 à 15 000 FCFA',
        'Hôtel Chanthel (12 Chambres Confort climatisées) : 15 000, 20 000 et 25 000 FCFA / nuitée',
        'Hôtel Ewondo (4 Loges & Mini-Suites VIP) : 25 000 à 30 000 FCFA / nuitée',
        'Suites Privées Prestige VIP (30 000 à 45 000 FCFA) & Pack Couple VIP (45 000 FCFA)',
      ],
      kpiNote: 'Réception Hôtels 24h/24 (Check-in 14h00 · Check-out 11h00) : +237 694 60 14 49',
    },
    {
      id: 'gastronomie',
      title: 'Le Château des Saveurs',
      value: '07h à 23h',
      unit: '7j/7 · Du bassin à la braise',
      accentColor: '#74C69D',
      icon: Wind,
      summary: 'Poissons pêchés dans nos bassins. Légumes bio récoltés sur place.',
      bluf: "Ouvert 7j/7 de 07h00 à 23h00 sans billet d'entrée parc en soirée, le restaurant Le Château des Saveurs sert poissons frais braisés pêchés sur place dès 5 000 FCFA, Poulet DG Royal à 6 500 FCFA et menus enfants à 2 500 FCFA sous pergolas.",
      breakdown: [
        'Poisson Frais Braisé d Ahala (Tilapia, Carpe ou Silure du bassin) : 5 000 FCFA TTC',
        'Poulet DG Royal aux plantains mûrs : 6 500 FCFA · Ndolé Royal aux Crevettes : 5 500 FCFA',
        'Grillades & Assiette du jour : 3 500 FCFA · Menu Enfant (< 12 ans) : 2 500 FCFA',
        'Pergola Privée sur pilotis (+5 000 FCFA) & Salle climatisée VIP New Look (60 couverts)',
      ],
      kpiNote: 'Accès libre au restaurant en soirée jusqu à 23h00 sans billet parc',
    },
    {
      id: 'formation_b2b',
      title: 'CFP MINEFOP & Salle 500 pl.',
      value: '5 Filières',
      unit: 'Dès 50 000 FCFA / tranche',
      accentColor: '#B7E4C7',
      icon: ShieldCheck,
      summary: '70 % de pratique réelle sur site. Salle événementielle de 500 places.',
      bluf: "Agréé par le MINEFOP, le CFP ECOPARK forme en 12 mois avec 70 % de pratique réelle sur 5 filières DQP et CQP, pour 50 000 FCFA d'inscription et 250 000 FCFA payables en 4 tranches, adossé à la salle climatisée Menkii Essomba Anton de 500 places.",
      breakdown: [
        '5 filières DQP/CQP (12 mois) : Aquaculture, Hôtellerie-Restauration, Élevage, Agroécologie, Écoguidage',
        'Échéancier officiel CFP : Inscription 50 000 FCFA · Scolarité 250 000 FCFA en 4 tranches (100k + 3x50k)',
        'Salle Polyvalente « Menkii Essomba Anton » (500 places assises climatisées, son & lumière)',
        'Excursion Scolaire (1 350 FCFA/élève), Séminaire B2B (15 000 FCFA/pers.) & Groupe 20+ (-30%)',
      ],
      kpiNote: 'MPECK MULTI-SERVICES • Fondateur & Promoteur : Dr Christophe FOE NDI',
    },
  ];

  return (
    <ImmersiveSection
      variant="bark"
      className="py-12 sm:py-16 border-y border-[#36403A]"
      containerClassName="space-y-8"
      id="impact-banner"
      ariaLabel="Preuves factuelles et 4 piliers officiels d ECOPARK CAMEROUN à Yaoundé-Ahala"
    >
      {/* Editorial Header (Échelle optique : .type-eyebrow, .type-h2 <= 12 mots + point final, .type-body) */}
      <div className="flex flex-col lg:flex-row lg:items-end justify-between gap-6 pb-2">
        <div className="space-y-2.5 max-w-4xl">
          <div className="inline-flex items-center gap-2 type-eyebrow !text-[#74C69D] uppercase">
            <Sparkles className="w-3.5 h-3.5 text-[#52B788]" />
            <span>Preuves Factuelles &amp; Tarifs Officiels · Yaoundé - Ahala Barrière (RN3)</span>
          </div>
          <h2 className="type-h2 text-white">
            Quatre pôles complémentaires sur un seul domaine.
          </h2>
          <p className="type-body text-[#C9D1CC]">
            Ouvrez le bouton <strong className="text-white">+</strong> de chaque carte Bento pour consulter la synthèse factuelle et le détail des tarifs officiels en FCFA.
          </p>
        </div>

        <div className="text-xs font-mono text-[#B7E4C7] bg-[#121614] px-3.5 py-2.5 rounded-xl border border-[#29302C] self-start lg:self-auto shrink-0 tabular-nums">
          <span className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
            Face station Tradex Ahala (RN3)
          </span>
        </div>
      </div>

      {/* TEMPS 6 : 4 Cartes Bento Réassurance + Tiroir '+' permanent dans le DOM HTML */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4 sm:gap-5 items-start">
        {metrics.map((metric) => {
          const Icon = metric.icon;
          const isExpanded = Boolean(expandedIds[metric.id]);
          const drawerId = `bento-drawer-${metric.id}`;

          return (
            <article
              key={metric.id}
              className={`rounded-2xl bg-[#29302C]/95 backdrop-blur-md border transition-all duration-200 p-5 sm:p-6 flex flex-col justify-between tabular-nums ${
                isExpanded
                  ? 'border-[#52B788] shadow-xl ring-2 ring-[#52B788]/25 bg-[#29302C]'
                  : 'border-[#36403A] hover:border-[#52B788]/60'
              }`}
            >
              <div>
                <div className="flex items-center justify-between gap-3 mb-3">
                  <div
                    className="p-2.5 rounded-xl bg-[#1F2421] border border-[#36403A]"
                    style={{ color: metric.accentColor }}
                  >
                    <Icon className="w-5 h-5" />
                  </div>

                  {/* Garde-fou 2 : Bouton rond '+' de 48x48px strict */}
                  <button
                    type="button"
                    aria-expanded={isExpanded}
                    aria-controls={drawerId}
                    aria-label={`${isExpanded ? 'Masquer' : 'Afficher'} les preuves détaillées : ${metric.title}`}
                    onClick={() => toggleCard(metric.id)}
                    className={`bento-plus-btn border ${
                      isExpanded
                        ? 'bg-[#52B788] text-[#081C15] border-[#52B788]'
                        : 'bg-[#1F2421] text-[#E9F5ED] border-[#46534B] hover:border-[#52B788] hover:text-[#74C69D]'
                    }`}
                  >
                    <Plus
                      className={`w-5 h-5 transition-transform duration-200 ${
                        isExpanded ? 'rotate-45' : 'rotate-0'
                      }`}
                    />
                  </button>
                </div>

                <div className="space-y-1">
                  <div className="font-['Barlow_Semi_Condensed'] text-2xl sm:text-3xl font-bold tracking-tight text-white tabular-nums">
                    {metric.value}
                  </div>
                  <h3 className="type-h3 !text-[21px] sm:!text-[22px] text-[#E9F5ED]">
                    {metric.title}
                  </h3>
                </div>

                <p className="type-body !text-[14px] !leading-[20px] text-[#C9D1CC] mt-2">
                  {metric.summary}
                </p>
              </div>

              <div className="pt-3.5 mt-4 border-t border-[#36403A]/80 flex items-center justify-between type-footnote !text-[#B7E4C7] font-mono tabular-nums">
                <span>{metric.unit}</span>
                <span>{isExpanded ? 'Réduire' : 'Preuves +'}</span>
              </div>

              {/* Tiroir progressif TOUJOURS présent dans le DOM HTML initial (indexation GEO / IA 100 %) */}
              <div
                id={drawerId}
                className={`grid transition-all duration-250 ease-out ${
                  isExpanded ? 'grid-rows-[1fr] opacity-100 mt-4 pt-4 border-t border-[#46534B]' : 'grid-rows-[0fr] opacity-0'
                }`}
              >
                <div className="overflow-hidden space-y-3">
                  {/* Synthèse BLUF (Bottom Line Up Front : 40 à 55 mots calibrés Google XYZ) */}
                  <p className="text-xs leading-relaxed text-[#E9F5ED] bg-[#1F2421] p-3 rounded-xl border border-[#36403A] tabular-nums">
                    {metric.bluf}
                  </p>

                  <ul className="space-y-2">
                    {metric.breakdown.map((item, i) => (
                      <li
                        key={i}
                        className="flex items-start gap-2 text-xs text-[#C9D1CC] leading-relaxed tabular-nums"
                      >
                        <CheckCircle2 className="w-3.5 h-3.5 text-[#52B788] shrink-0 mt-0.5" />
                        <span>{item}</span>
                      </li>
                    ))}
                  </ul>

                  <div className="text-[11px] font-mono text-[#74C69D] pt-1 tabular-nums">
                    {metric.kpiNote}
                  </div>
                </div>
              </div>
            </article>
          );
        })}
      </div>
    </ImmersiveSection>
  );
};
