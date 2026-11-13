// ============================================================================
// ECO-PARK ENVIRONMENTAL IMPACT BANNER (src/components/discovery/ImpactBanner.tsx)
// Feature F15 — Deep Bark #1F2421 Immersive Container & 4 Core Ecological Metrics
// ============================================================================

import React, { useState } from 'react';
import { useEcoPark } from '../../context/EcoParkContext';
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
  const { telemetry } = useEcoPark();
  const [activeMetricIndex, setActiveMetricIndex] = useState<number | null>(null);

  const metrics = [
    {
      id: 'solar',
      title: 'Autonomie Solaire',
      value: `${telemetry.solarAutonomyPercent}%`,
      unit: 'énergie propre',
      accentColor: '#F4A261', // Warm Earth tone
      bgGlow: 'from-amber-500/10 to-transparent',
      icon: Sun,
      headline: 'Réseau photovoltaïque décentralisé et stockage batterie',
      summary: 'La réserve produit la quasi-totalité de son électricité grâce au soleil.',
      breakdown: [
        '16 bornes de recharge pour vélos à assistance électrique (Pôle Éco-Mobilité)',
        'Postes de commandement et refuges éco-gardes 100% autonomes',
        'Stations de pompage et microfiltration solaire de l eau potable aux fontaines',
        'Éclairage nocturne zéro pollution lumineuse alimenté par batteries basse tension',
      ],
      kpiNote: '94% d autonomie mesurée sur les 30 derniers jours',
    },
    {
      id: 'co2',
      title: 'CO₂ Évité Cumulé',
      value: `${telemetry.totalCo2AvoidedKg.toLocaleString('fr-FR')} kg`,
      unit: 'carbone épargné',
      accentColor: '#52B788', // Fresh Leaf
      bgGlow: 'from-emerald-500/10 to-transparent',
      icon: Leaf,
      headline: 'Bilan positif propulsé par la billetterie éco-mobilité',
      summary: 'Économie équivalente à 21 400 km de trajets en voiture thermique.',
      breakdown: [
        'Réductions tarifaires incitatives (-20% à -30%) pour trains, vélos et navettes',
        '84% des randonneurs du jour ont emprunté un moyen de transport décarboné',
        'Navettes électriques bio-circulaires gratuites depuis la gare TER',
        'Empreinte carbone du site compensée à 100% par la régénération forestière',
      ],
      kpiNote: 'Calcul certifié conforme à la méthodologie ADEME Bilan Carbone',
    },
    {
      id: 'iqa',
      title: 'Qualité de l Air',
      value: `IQA ${telemetry.airQualityIqa}`,
      unit: telemetry.airQualityStatus,
      accentColor: '#74C69D', // Soft Mint
      bgGlow: 'from-sky-500/10 to-transparent',
      icon: Wind,
      headline: 'Microclimat forestier préservé et purification naturelle',
      summary: 'Concentration en particules fines PM2.5 inférieure à 4 µg/m³.',
      breakdown: [
        'Interdiction totale de véhicules thermiques sur l ensemble des 420 hectares',
        'Filtre végétal continu composé de 140 000 arbres feuillus et résineux',
        'Réseau de 12 capteurs atmosphériques autonomes communicant en LoRaWAN',
        'Bio-indicateurs vivants : 14 espèces de lichens fruticuleux ultra-sensibles florissantes',
      ],
      kpiNote: 'Indice Atmo normalisé officiel mesuré toutes les 15 minutes',
    },
    {
      id: 'sanctuary',
      title: 'Sanctuaire Préservé',
      value: '420 ha',
      unit: 'haute protection',
      accentColor: '#B7E4C7', // Light canopy
      bgGlow: 'from-teal-500/10 to-transparent',
      icon: ShieldCheck,
      headline: 'Zone biologique intégrale sanctuarisée pour les générations futures',
      summary: 'Capacité journalière régulée et zéro produit phytosanitaire.',
      breakdown: [
        'Plafond quotidien strict fixé par l éco-garde en chef pour éviter le piétinement',
        '8 espèces endémiques prioritaires surveillées par pièges photographiques',
        'Fermetures saisonnières ciblées des sentiers lors des périodes de nidification',
        'Corridors biologiques continus sans clôture pour la libre circulation de la faune',
      ],
      kpiNote: 'Classé Réserve Biologique Intégrale (RBI) d intérêt communautaire',
    },
  ];

  return (
    <ImmersiveSection
      variant="bark"
      className="py-14 sm:py-18 border-y border-[#36403A]"
      containerClassName="space-y-8"
      id="impact-banner"
      ariaLabel="Bandeau d impact environnemental et écologique"
    >
      {/* Editorial Header */}
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 pb-2">
        <div className="space-y-2 max-w-2xl">
          <div className="inline-flex items-center gap-2 text-xs font-mono font-semibold uppercase tracking-wider text-[#74C69D]">
            <Sparkles className="w-3.5 h-3.5 text-[#52B788]" />
            <span>Transparence Écologique · Données Temps Réel</span>
          </div>
          <h2 className="font-['Fraunces'] text-2xl sm:text-3xl lg:text-4xl font-bold text-white tracking-tight">
            Notre Impact Environnemental Mesurable
          </h2>
          <p className="text-sm text-[#C9D1CC] leading-relaxed">
            Chaque Éco-Pass finance directement la régénération des sols et la quiétude des espèces.
            Découvrez les 4 indicateurs fondamentaux suivis en temps réel par notre équipe d éco-gardes.
          </p>
        </div>

        <div className="text-xs font-mono text-[#8EBAA0] bg-[#121614] px-3 py-2 rounded-xl border border-[#29302C] self-start md:self-auto shrink-0">
          <span className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
            Station d écologie quantitative #01
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
              {/* Top Accent Icon & Value */}
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
                  <div className="font-['Fraunces'] text-2xl sm:text-3xl font-bold tracking-tight text-white font-mono">
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

              {/* Bottom Quick Indicator */}
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
                Fiche d audit télémétrique · {metrics[activeMetricIndex].title}
              </span>
              <h3 className="font-['Fraunces'] text-xl font-bold text-white">
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
