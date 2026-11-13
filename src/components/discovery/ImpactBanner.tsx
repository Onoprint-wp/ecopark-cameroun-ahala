// ============================================================================
// ECOPARK CAMEROUN (YAOUNDÉ – AHALA) — 4 PILLARS & IMPACT BANNER
// (src/components/discovery/ImpactBanner.tsx)
// Deep Bark #1F2421 Immersive Container & 4 Validated Production Metrics
// ============================================================================

import React, { useState } from 'react';
import { ImmersiveSection } from '../layout/ImmersiveSection';
import {
  Sun,
  Leaf,
  Wind,
  ShieldCheck,
  Info,
  ChevronDown,
  ChevronUp,
  Sparkles,
  CheckCircle2,
} from 'lucide-react';

export const ImpactBanner: React.FC = () => {
  const [activeMetricIndex, setActiveMetricIndex] = useState<number | null>(null);

  const metrics = [
    {
      id: 'loisirs',
      title: 'Loisirs, Zoo & Pirogue',
      value: 'Dès 500 FCFA',
      unit: 'enfant / 1 000 FCFA adulte',
      accentColor: '#F4A261',
      bgGlow: 'from-amber-500/10 to-transparent',
      icon: Sun,
      headline: 'Jardin Zoologique (Gorille ToTo), Pirogues, Piscine Semi-Olympique & Équitation',
      summary: 'Tarifs populaires accessibles à toutes les familles de Yaoundé du mardi au dimanche.',
      breakdown: [
        'Entrée Parc & Jardin Zoologique (Gorille ToTo, chimpanzés, tortues) : 1 000 FCFA adulte / 500 FCFA enfant',
        'Balade en Pirogue sur le lac (45 min, gilet fourni) : 1 000 FCFA adulte / 500 FCFA enfant',
        'Piscine Semi-Olympique surveillée : 2 500 FCFA adulte / 1 500 FCFA enfant (semaine & prévente)',
        'Balade à cheval (1 000 / 500 FCFA), Musée Culturel (1 000 / 500 FCFA), Jeux & Bibliothèque (500 FCFA)',
      ],
      kpiNote: '3 Pass Tout-Inclus (1 QR Code) : 2 500 FCFA, 4 500 FCFA et 8 500 FCFA (repas inclus)',
    },
    {
      id: 'hebergements',
      title: 'Cités Hôtelières 24h/24',
      value: '30 Unités',
      unit: '10 000 à 45 000 FCFA / nuit',
      accentColor: '#52B788',
      bgGlow: 'from-emerald-500/10 to-transparent',
      icon: Leaf,
      headline: 'Hôtel Ewondo VIP, Hôtel Chanthel, Hôtel Bene & Suites Privées Prestige',
      summary: 'Réception ouverte 24h/24 et 7j/7 (Check-in 14h00 · Check-out 11h00) dans un écrin forestier.',
      breakdown: [
        'Hôtel Ewondo (4 Loges & Mini-Suites VIP) : 25 000 à 30 000 FCFA / nuitée',
        'Hôtel Chanthel (12 Chambres Confort climatisées) : 15 000, 20 000 et 25 000 FCFA / nuitée',
        'Hôtel Bene (10 Chambres Standard & Day-Use avec grande véranda) : 10 000 à 15 000 FCFA',
        'Suites Privées Prestige VIP (30 000 à 45 000 FCFA) & Pack Escapade Couple VIP (45 000 FCFA)',
      ],
      kpiNote: 'Contact direct Réception Hôtels & Cités : WhatsApp +237 694 60 14 49',
    },
    {
      id: 'gastronomie',
      title: 'Le Château des Saveurs',
      value: '07h – 23h',
      unit: '7j/7 · Du bassin à la braise',
      accentColor: '#74C69D',
      bgGlow: 'from-sky-500/10 to-transparent',
      icon: Wind,
      headline: 'Haute gastronomie camerounaise au bord de l eau, Salle VIP New Look & Boukarous',
      summary: 'Poissons frais pêchés dans nos bassins et légumes bio récoltés sur place à Ahala.',
      breakdown: [
        'Poisson Frais Braisé d Ahala (Tilapia / Carpe / Silure du bassin) : 5 000 FCFA TTC',
        'Poulet DG Royal aux plantains mûrs : 6 500 FCFA · Ndolé Royal aux Crevettes : 5 500 FCFA',
        'Grillades & Assiette du jour : 3 500 FCFA · Menu Enfant (< 12 ans) : 2 500 FCFA',
        'Pergola Privée sur pilotis au bord du lac (+5 000 FCFA) & Salle climatisée VIP New Look (60 couverts)',
      ],
      kpiNote: 'Accès libre au restaurant en soirée jusqu à 23h00 sans billet d entrée parc',
    },
    {
      id: 'formation_b2b',
      title: 'CFP MINEFOP & Salle 500 pl.',
      value: '5 Filières',
      unit: 'DQP/CQP + Événementiel',
      accentColor: '#B7E4C7',
      bgGlow: 'from-teal-500/10 to-transparent',
      icon: ShieldCheck,
      headline: 'Centre de Formation Professionnelle agréé MINEFOP & Salle « Menkii Essomba Anton »',
      summary: '70 % de pratique réelle sur le site d Ahala et complexe événementiel de 500 places assises.',
      breakdown: [
        '5 filières DQP/CQP (12 mois) : Aquaculture, Hôtellerie-Restauration, Élevage, Agroécologie, Écoguidage',
        'Tarifs officiels CFP : Inscription 50 000 FCFA · Scolarité 250 000 FCFA en 4 tranches (100k + 3×50k)',
        'Salle Polyvalente « Menkii Essomba Anton » (500 places assises climatisées, son & lumière)',
        'Forfait Excursion Scolaire (1 350 FCFA/élève), Séminaire B2B (15 000 FCFA/pers.) & Groupe 20+ (-30%)',
      ],
      kpiNote: 'MPECK MULTI-SERVICES — Fondateur & Promoteur : Dr Christophe FOE NDI',
    },
  ];

  return (
    <ImmersiveSection
      variant="bark"
      className="py-12 sm:py-16 border-y border-[#36403A]"
      containerClassName="space-y-8"
      id="impact-banner"
      ariaLabel="Les 4 piliers officiels d ECOPARK CAMEROUN à Yaoundé-Ahala"
    >
      {/* Editorial Header */}
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 pb-2">
        <div className="space-y-2 max-w-2xl">
          <div className="inline-flex items-center gap-2 text-xs font-mono font-semibold uppercase tracking-wider text-[#74C69D]">
            <Sparkles className="w-3.5 h-3.5 text-[#52B788]" />
            <span>Chiffres Clés &amp; Tarifs Validés · Yaoundé – Ahala Barrière (RN3)</span>
          </div>
          <h2 className="font-['Barlow_Semi_Condensed'] text-2xl sm:text-3xl lg:text-4xl font-bold text-white tracking-tight">
            Un Écosystème Unique Réunissant Nature, Saveurs, Séjour &amp; Formation
          </h2>
          <p className="text-sm text-[#C9D1CC] leading-relaxed">
            Cliquez sur chaque pôle pour afficher le détail officiel des prestations, horaires et tarifs en FCFA validés en production.
          </p>
        </div>

        <div className="text-xs font-mono text-[#8EBAA0] bg-[#121614] px-3 py-2 rounded-xl border border-[#29302C] self-start md:self-auto shrink-0">
          <span className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
            En face de la station Tradex Ahala (RN3)
          </span>
        </div>
      </div>

      {/* 4 Core Metrics Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-5">
        {metrics.map((metric, idx) => {
          const Icon = metric.icon;
          const isExpanded = activeMetricIndex === idx;

          return (
            <div
              key={metric.id}
              role="button"
              tabIndex={0}
              aria-expanded={isExpanded}
              onClick={() => setActiveMetricIndex(isExpanded ? null : idx)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                  e.preventDefault();
                  setActiveMetricIndex(isExpanded ? null : idx);
                }
              }}
              className={`group relative p-5 sm:p-6 rounded-2xl bg-[#29302C]/90 backdrop-blur-md border transition-all duration-200 cursor-pointer flex flex-col justify-between ${
                isExpanded
                  ? 'border-[#52B788] shadow-lg ring-2 ring-[#52B788]/20 bg-[#29302C]'
                  : 'border-[#36403A] hover:border-[#52B788]/60 hover:bg-[#303834]'
              }`}
            >
              <div>
                <div className="flex items-center justify-between gap-2 mb-3">
                  <div
                    className="p-2.5 rounded-xl bg-[#1F2421] border border-[#36403A]"
                    style={{ color: metric.accentColor }}
                  >
                    <Icon className="w-5 h-5" />
                  </div>

                  <span className="text-[11px] font-mono text-[#8EBAA0] flex items-center gap-1 group-hover:text-white transition-colors">
                    Détails
                    {isExpanded ? (
                      <ChevronUp className="w-3.5 h-3.5 text-[#52B788]" />
                    ) : (
                      <ChevronDown className="w-3.5 h-3.5 text-[#8EBAA0]" />
                    )}
                  </span>
                </div>

                <div className="space-y-1">
                  <div className="font-['Barlow_Semi_Condensed'] text-2xl sm:text-3xl font-bold tracking-tight text-white">
                    {metric.value}
                  </div>
                  <div className="text-xs font-semibold text-[#8EBAA0] uppercase tracking-wider">
                    {metric.title}
                  </div>
                </div>

                <p className="text-xs text-[#C9D1CC] mt-2.5 line-clamp-2 leading-relaxed">
                  {metric.summary}
                </p>
              </div>

              <div className="pt-4 mt-4 border-t border-[#36403A]/70 flex items-center justify-between text-[11px] font-mono text-[#8EBAA0]">
                <span>{metric.unit}</span>
                <Info className="w-3.5 h-3.5 opacity-60 group-hover:opacity-100 transition-opacity" />
              </div>
            </div>
          );
        })}
      </div>

      {/* Expanded Breakdown Card when a metric is selected */}
      {activeMetricIndex !== null && (
        <div className="p-6 sm:p-7 rounded-2xl bg-[#121614] border border-[#52B788]/60 shadow-xl space-y-4 animate-in fade-in duration-200">
          <div className="flex items-start justify-between gap-4">
            <div className="space-y-1">
              <span className="text-xs font-mono font-semibold text-[#52B788] uppercase tracking-wider">
                Fiche Officielle · {metrics[activeMetricIndex].title}
              </span>
              <h3 className="font-['Barlow_Semi_Condensed'] text-xl font-bold text-white">
                {metrics[activeMetricIndex].headline}
              </h3>
              <p className="text-xs text-[#C9D1CC] font-mono">
                {metrics[activeMetricIndex].kpiNote}
              </p>
            </div>

            <button
              type="button"
              onClick={() => setActiveMetricIndex(null)}
              className="p-1.5 rounded-lg bg-[#29302C] hover:bg-[#36403A] text-[#C9D1CC] hover:text-white transition-colors cursor-pointer text-xs font-mono"
              aria-label="Fermer le détail"
            >
              Fermer ✕
            </button>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
            {metrics[activeMetricIndex].breakdown.map((item, i) => (
              <div
                key={i}
                className="p-3.5 rounded-xl bg-[#1F2421] border border-[#36403A] flex items-start gap-2.5 text-xs text-[#E9F5ED] leading-relaxed"
              >
                <CheckCircle2 className="w-4 h-4 text-[#52B788] shrink-0 mt-0.5" />
                <span>{item}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </ImmersiveSection>
  );
};
