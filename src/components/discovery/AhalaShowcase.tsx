// ============================================================================
// ECOPARK CAMEROUN (YAOUNDE - AHALA) - VALIDATED PRODUCTION SHOWCASE
// (src/components/discovery/AhalaShowcase.tsx)
// Fiche mémo n°4 (Profil B - 7/7 Temps complets) :
// - Temps 4 : Comparateur Auto-Segmentant des 3 Pass + Price Framing inversé réel
//             + Tableaux comparatifs <table> natifs JAMAIS masqués hors du DOM
// - Temps 5 : Tandem Asymétrique Double CTA (.cta-pill + .cta-chevron ›)
// - Temps 7 : Cross-Sell Complémentaire Pertinent (Navette, Pergola, Nourrissage, Garderie)
// - Loi 1 & Loi 2 : 0 tiret cadratin/demi-cadratin, tabular-nums intégral, cadrage visages 4:3/16:9
// ============================================================================

import React, { useState, useEffect } from 'react';
import { useEcoPark } from '../../context/EcoParkContext';
import {
  type ShowcaseTab,
  type ShowcaseNavDetail,
  SHOWCASE_TAB_PATH_MAP,
  SHOWCASE_DEEP_PATHS,
  SHOWCASE_NAV_EVENT,
  resolveShowcaseTabFromPath,
  getPhotoObjectPosition,
} from '../../utils/ecoRouting';
import {
  BedDouble,
  Utensils,
  Ticket,
  GraduationCap,
  Building2,
  CheckCircle2,
  PhoneCall,
  Sparkles,
  MapPin,
  Clock,
  ShieldCheck,
  Heart,
  Bus,
  Baby,
  Fish,
  Crown,
} from 'lucide-react';

export const AhalaShowcase: React.FC = () => {
  const { setActiveView, setSelectedTrailId } = useEcoPark();
  const [activeTab, setActiveTab] = useState<ShowcaseTab>(() =>
    typeof window !== 'undefined' ? resolveShowcaseTabFromPath(window.location.pathname) : 'hebergements'
  );

  useEffect(() => {
    if (typeof window === 'undefined') return;
    const clean = window.location.pathname.replace(/\/+$/, '').toLowerCase();
    if (SHOWCASE_DEEP_PATHS.includes(clean)) {
      setTimeout(() => {
        document.getElementById('ahala-production-showcase')?.scrollIntoView({ behavior: 'smooth' });
      }, 150);
    }

    const handlePopState = () => {
      setActiveTab(resolveShowcaseTabFromPath(window.location.pathname));
    };

    const handleShowcaseNav = (ev: Event) => {
      const customEv = ev as CustomEvent<ShowcaseNavDetail>;
      const detail = customEv.detail;
      if (detail?.tab) {
        setActiveTab(detail.tab);
      }
      const targetId = detail?.anchorId || 'ahala-production-showcase';
      setTimeout(() => {
        document.getElementById(targetId)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 60);
    };

    window.addEventListener('popstate', handlePopState);
    window.addEventListener(SHOWCASE_NAV_EVENT, handleShowcaseNav as EventListener);
    return () => {
      window.removeEventListener('popstate', handlePopState);
      window.removeEventListener(SHOWCASE_NAV_EVENT, handleShowcaseNav as EventListener);
    };
  }, []);

  const handleSelectShowcaseTab = (tab: ShowcaseTab) => {
    setActiveTab(tab);
    if (typeof window !== 'undefined') {
      const nextPath = SHOWCASE_TAB_PATH_MAP[tab];
      if (window.location.pathname !== nextPath) {
        window.history.pushState({ showcaseTab: tab }, '', nextPath);
      }
    }
  };

  // TEMPS 4 : Comparateur Auto-Segmentant des 3 Pass Tout-Inclus (Price Framing Inversé unitaire réel)
  const PASS_COMPARATOR = [
    {
      id: 'decouverte',
      trailKey: 'roches-moussues',
      badge: 'Formule #1 · Famille & Nature',
      name: 'Pass Découverte Nature',
      tagline: 'Explorez le zoo. Glissez sur le lac. Initiez les enfants à cheval.',
      childPrice: 1500,
      adultPrice: 2500,
      featured: false,
      features: [
        'Entrée Parc & Jardin Zoologique (Gorille « ToTo », chimpanzés, tortues)',
        'Balade en Pirogue sur le lac (45 min, gilet fourni)',
        'Balade à cheval & initiation au manège équestre',
        '1 QR Code unique coupe-file + Garantie Météo RN3 (90j)',
      ],
    },
    {
      id: 'complete',
      trailKey: 'marais',
      badge: 'Formule #2 · Le Plus Choisi',
      name: 'Pass Journée Complète',
      tagline: 'Visitez la faune. Traversez l eau. Nagez en bassin semi-olympique.',
      childPrice: 2500,
      adultPrice: 4500,
      featured: true,
      features: [
        'Entrée Parc & Jardin Zoologique complet',
        'Accès Piscine Semi-Olympique surveillée par maîtres-nageurs',
        'Balade en Pirogue de 45 min sur le lac d Ahala',
        '1 QR Code unique coupe-file + Parking gratuit face Tradex',
      ],
    },
    {
      id: 'royale',
      trailKey: 'piste-eco-gardes',
      badge: 'Formule #3 · VIP Gastronomie',
      name: 'Pass Journée Royale',
      tagline: 'Vivez toutes les activités. Déjeunez au bord du lac. Zéro file d attente.',
      childPrice: 4500,
      adultPrice: 8500,
      featured: false,
      features: [
        'Zoo + Piscine Semi-Olympique + Balade en Pirogue',
        'Repas chaud inclus au restaurant « Le Château des Saveurs »',
        'Accès prioritaire coupe-file aux embarcadères et bassins',
        'Idéal week-end famille, couple ou invités de marque',
      ],
    },
  ];

  const HOTELS = [
    {
      id: 'bene',
      name: 'Hôtel Bene • Chambres Standard & Day-Use',
      badge: '10 Chambres · Grande Véranda d Étage',
      priceFraming: 'Dès 10 000 FCFA',
      priceRange: '10 000 à 15 000 FCFA',
      unit: '/ nuitée ou Day-Use',
      photo: '/images/ahala/IMG-20260809-WA0009.jpg',
      description:
        'Solution économique, propre et sécurisée disposant d une grande véranda conviviale à l étage pouvant accueillir de petites réunions.',
      features: [
        'À partir de 10 000 FCFA (Nuitée ou Repos Day-Use jusqu à 15 000 FCFA)',
        'Grande véranda d étage aménagée pour échanges et détente',
        'Réception Hôtellerie ouverte 24h/24 et 7j/7',
        'Check-in dès 14h00 · Check-out jusqu à 11h00',
      ],
    },
    {
      id: 'chanthel',
      name: 'Hôtel Chanthel • Chambres Confort',
      badge: '12 Chambres Climatisées · 3 Paliers',
      priceFraming: 'Dès 15 000 FCFA',
      priceRange: '15 000 à 25 000 FCFA',
      unit: '/ nuitée (15k · 20k · 25k)',
      photo: '/images/ahala/IMG-20260713-WA0051_043420.jpg',
      description:
        'Cocon de fraîcheur forestière offrant 3 catégories de confort climatisé adaptées aux familles et voyageurs à 15 min du centre-ville.',
      features: [
        '3 paliers officiels : 15 000 FCFA, 20 000 FCFA et 25 000 FCFA / nuitée',
        'Salle d eau privative moderne, climatisation & literie grand confort',
        'Environnement calme et verdoyant en lisière forestière',
        'Parking gratuit sous vidéosurveillance 24h/24 face Tradex RN3',
      ],
    },
    {
      id: 'ewondo',
      name: 'Hôtel Ewondo • Loges & Mini-Suites VIP',
      badge: '4 Mini-Suites VIP · Standing Supérieur',
      priceFraming: 'Dès 25 000 FCFA',
      priceRange: '25 000 à 30 000 FCFA',
      unit: '/ nuitée',
      photo: '/images/ahala/chambre.jpeg',
      description:
        'Loges spacieuses et Mini-Suites VIP nichées sous les arbres d Ahala pour séjours romantiques, cadres en mission et week-ends détente.',
      features: [
        'Climatisation split silencieuse & Lit King-Size orthopédique',
        'Terrasse privative sur jardin, Eau chaude & TV écran plat Canal+',
        'Accès gratuit au Parc & Jardin Zoologique pendant le séjour',
        'Service en chambre depuis Le Château des Saveurs (07h à 23h)',
      ],
    },
    {
      id: 'suites-vip',
      name: 'Suites Privées Prestige VIP',
      badge: '4 Suites Haut de Gamme · Salon Privé',
      priceFraming: 'Dès 30 000 FCFA',
      priceRange: '30 000 à 45 000 FCFA',
      unit: '/ nuitée',
      photo: '/images/ahala/local_cameroon_gastronomy_pergola.png',
      description:
        'Expérience présidentielle avec salon privé climatisé, chambre séparée, room-service prioritaire et accès coupe-file aux loisirs.',
      features: [
        'Salon de réception privé + Chambre principale climatisée',
        'Room-service dédié du restaurant Le Château des Saveurs',
        'Accès coupe-file Piscine Semi-Olympique & Balade en Pirogue',
        'Accueil personnalisé et discrétion absolue garantie',
      ],
    },
  ];

  const MENU_ITEMS = [
    {
      name: 'Poisson Frais Braisé d Ahala (Du bassin à la braise)',
      price: '5 000 FCFA',
      tag: 'Signature EcoPark',
      desc: 'Tilapia, carpe ou silure pêché dans nos bassins d Ahala, mariné aux épices du terroir et braisé au feu de bois, servi avec plantains mûrs, miondo ou frites.',
    },
    {
      name: 'Poulet DG Royal aux Légumes du Jardin Bio',
      price: '6 500 FCFA',
      tag: 'Gastronomie Royale',
      desc: 'Volaille fermière mijotée aux plantains dorés, carottes, poivrons et herbes aromatiques récoltées sur les parcelles bio du CFP ECOPARK.',
    },
    {
      name: 'Ndolé Royal aux Crevettes & Accompagnements',
      price: '5 500 FCFA',
      tag: 'Tradition Camerounaise',
      desc: 'Feuilles de ndolé fraîches préparées aux arachides onctueuses, crevettes et viande fondante.',
    },
    {
      name: 'Grillades Forestières & Assiette du Jour',
      price: '3 500 FCFA',
      tag: 'Pause Gourmande',
      desc: 'Brochettes, volaille grillée ou plat du jour cuisiné maison par la brigade du Château des Saveurs.',
    },
    {
      name: 'Menu Enfant (< 12 ans · Boisson incluse)',
      price: '2 500 FCFA',
      tag: 'Spécial Familles',
      desc: 'Portion adaptée (poulet croustillant ou poisson sans arêtes) accompagnée de frites dorées et jus de fruits naturel.',
    },
    {
      name: 'Option Pergola Privée sur Pilotis au Bord du Lac',
      price: '+5 000 FCFA',
      tag: 'Cadre Exclusif',
      desc: 'Privatisation d une pergola panoramique au-dessus de l eau pour vos déjeuners en famille, anniversaires ou dîners en amoureux.',
    },
  ];

  const UNIT_ACTIVITIES = [
    { name: 'Entrée Parc & Jardin Zoologique seul (Gorille ToTo, chimpanzés, tortues)', child: '500 FCFA', adult: '1 000 FCFA', note: 'Gratuit (< 3 ans)' },
    { name: 'Balade en Pirogue sur le lac (45 min, gilet de sauvetage fourni)', child: '500 FCFA', adult: '1 000 FCFA', note: 'Embarcadère sécurisé' },
    { name: 'Piscine Semi-Olympique surveillée par maîtres-nageurs', child: '1 500 FCFA', adult: '2 500 FCFA', note: 'Enfant week-end guichet : 2 500 FCFA' },
    { name: 'Balade à Cheval & Initiation Manège Équestre', child: '500 FCFA', adult: '1 000 FCFA', note: 'Casque & moniteur inclus' },
    { name: 'Musée Culturel et du Patrimoine Camerounais', child: '500 FCFA', adult: '1 000 FCFA', note: 'Visite commentée' },
    { name: 'Bibliothèque & Espace Lecture Jeunesse', child: '500 FCFA', adult: '500 FCFA', note: 'Accès journée' },
    { name: 'Aire de Jeux Enfants & Châteaux Gonflables', child: '500 FCFA', adult: 'Accès parent gratuit', note: 'Surveillance dédiée' },
    { name: 'Pêche de Loisir aux Étangs Piscicoles', child: '2 000 FCFA', adult: '2 000 FCFA', note: 'Matériel & conseils inclus' },
    { name: 'Sachet de Nourrissage (Poissons des bassins & Tortues)', child: '500 FCFA', adult: '500 FCFA', note: 'Activité coup de cœur enfants' },
    { name: 'Halte-Garderie & Crèche Sécurisée', child: '1 500 FCFA', adult: '1 500 FCFA', note: 'Tarif groupe : 1 000 FCFA / enfant' },
    { name: 'Navette Climatisée Aller-Retour (Yaoundé <-> Ahala)', child: '1 000 FCFA', adult: '1 500 FCFA', note: 'Bus 5, 18 et 32 places' },
  ];

  const CFP_PROGRAMS = [
    {
      num: '01',
      title: 'Aquaculture & Pisciculture Continentale',
      outcome: 'Maîtrise complète de l alevinage, de la gestion des étangs et de la production de tilapias, carpes et silures.',
    },
    {
      num: '02',
      title: 'Hôtellerie, Restauration & Arts de la Table',
      outcome: 'Formation en immersion directe au restaurant Le Château des Saveurs et dans les 30 unités des Hôtels Ewondo, Chanthel et Bene.',
    },
    {
      num: '03',
      title: 'Élevage & Productions Animales',
      outcome: 'Conduite d élevage moderne, suivi sanitaire, alimentation durable et gestion technico-économique d exploitation.',
    },
    {
      num: '04',
      title: 'Agroécologie & Maraîchage Biologique',
      outcome: 'Production maraîchère sans pesticides chimiques, compostage organique et approvisionnement en circuit court.',
    },
    {
      num: '05',
      title: 'Tourisme Durable, Loisirs & Écoguidage',
      outcome: 'Accueil des visiteurs, gestion de parc de loisirs, animation zoologique et accompagnement d excursions scolaires et B2B.',
    },
  ];

  // TEMPS 7 : Cross-Sell Complémentaire Pertinent (Options réelles validées d'Ahala)
  const CROSS_SELL_OPTIONS = [
    {
      id: 'navette',
      icon: Bus,
      badge: 'Mobilité sans stress',
      title: 'Navette Climatisée A/R',
      price: 'Dès 1 000 FCFA enf. · 1 500 FCFA ad.',
      desc: 'Liaison aller-retour depuis Yaoundé en bus climatisé (5, 18 ou 32 places) jusqu à Ahala Barrière.',
      waText: 'Bonjour EcoPark Cameroun, je souhaite réserver la Navette Climatisée Aller-Retour (1 500 FCFA Ad. / 1 000 FCFA Enf.).',
    },
    {
      id: 'pergola',
      icon: Crown,
      badge: 'Confort VIP sur l eau',
      title: 'Pergola Privée sur Pilotis',
      price: '+5 000 FCFA / groupe',
      desc: 'Espace privatisé au-dessus du lac au Château des Saveurs pour déjeuner familial ou anniversaire.',
      waText: 'Bonjour EcoPark Cameroun, je souhaite réserver une Pergola Privée sur Pilotis (+5 000 FCFA) au Château des Saveurs.',
    },
    {
      id: 'nourrissage',
      icon: Fish,
      badge: 'Coup de cœur enfants',
      title: 'Sachet Nourrissage Faune',
      price: '500 FCFA / sachet',
      desc: 'Nourrissez les poissons des bassins piscicoles et les tortues avec nos granulés calibrés.',
      waText: 'Bonjour EcoPark Cameroun, nous souhaitons ajouter des Sachets de Nourrissage (500 FCFA) à notre visite.',
    },
    {
      id: 'garderie',
      icon: Baby,
      badge: 'Sérénité parents',
      title: 'Halte-Garderie Sécurisée',
      price: 'Dès 1 000 FCFA / enf. (groupe) · 1 500 FCFA',
      desc: 'Espace d éveil encadré pendant que vous profitez de la piscine semi-olympique ou d un séminaire.',
      waText: 'Bonjour EcoPark Cameroun, je souhaite réserver une place en Halte-Garderie Sécurisée à Ahala.',
    },
  ];

  return (
    <div className="space-y-16">
      {/* =================================================================== */}
      {/* TEMPS 4 & TEMPS 5 : COMPARATEUR AUTO-SEGMENTANT DES 3 PASS + DOUBLE CTA */}
      {/* =================================================================== */}
      <section
        id="pass-comparateur"
        aria-label="Comparateur des 3 Pass Tout-Inclus ECOPARK CAMEROUN"
        className="eco-container space-y-7 scroll-mt-36"
      >
        <div className="flex flex-col lg:flex-row lg:items-end justify-between gap-4">
          <div className="space-y-2 max-w-3xl">
            <span className="type-eyebrow uppercase inline-flex items-center gap-2">
              <Ticket className="w-4 h-4" />
              <span>Comparateur Officiel · 1 Seul QR Code Coupe-File</span>
            </span>
            <h2 className="type-h2 text-[var(--text-primary)]">
              Choisissez votre Pass Tout-Inclus en un regard.
            </h2>
            <p className="type-body text-[var(--text-muted)]">
              Entrée parc seule dès <strong className="text-[var(--text-primary)] tabular-nums">500 FCFA enfant</strong> et{' '}
              <strong className="text-[var(--text-primary)] tabular-nums">1 000 FCFA adulte</strong>. Optez pour un Pass combiné pour regrouper vos activités sans attente au guichet.
            </p>
          </div>
          <div className="type-footnote font-mono bg-[var(--bg-surface)] border border-[var(--border-default)] px-3.5 py-2.5 rounded-xl shrink-0 tabular-nums">
            Groupe 20+ pers. : <strong className="text-[var(--brand-primary)]">-30% (Entrée adulte à 700 FCFA)</strong>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 items-stretch">
          {PASS_COMPARATOR.map((pass) => (
            <article
              key={pass.id}
              className={`rounded-2xl p-6 flex flex-col justify-between transition-all tabular-nums ${
                pass.featured
                  ? 'bg-[var(--bg-card)] border-2 border-[var(--brand-primary)] shadow-lg ring-4 ring-[var(--brand-primary)]/10'
                  : 'bg-[var(--bg-surface)] border border-[var(--border-default)] shadow-xs'
              }`}
            >
              <div className="space-y-4">
                <div className="flex items-center justify-between gap-2">
                  <span
                    className={`px-3 py-1 rounded-full text-xs font-mono font-bold ${
                      pass.featured
                        ? 'bg-[var(--brand-primary)] text-[var(--on-primary)]'
                        : 'bg-[var(--brand-primary)]/10 text-[var(--brand-primary)]'
                    }`}
                  >
                    {pass.badge}
                  </span>
                </div>

                <div>
                  <h3 className="type-h3 text-[var(--text-primary)]">{pass.name}</h3>
                  <p className="type-body !text-[14px] !leading-[20px] text-[var(--text-muted)] mt-1">
                    {pass.tagline}
                  </p>
                </div>

                {/* Price Framing Inversé : tarif enfant le plus accessible mis en avant + tarif adulte clair */}
                <div className="p-4 rounded-xl bg-[var(--bg-canvas)] border border-[var(--border-subtle)] space-y-1 tabular-nums">
                  <div className="type-footnote uppercase font-semibold">
                    À partir de (Enfant 3 à 12 ans)
                  </div>
                  <div className="flex items-baseline flex-wrap gap-x-2 gap-y-1">
                    <span className="font-['Barlow_Semi_Condensed'] text-3xl font-bold text-[var(--brand-primary)] tabular-nums">
                      {pass.childPrice.toLocaleString('fr-FR')} FCFA
                    </span>
                    <span className="type-footnote font-semibold">
                      / enfant · ou <strong className="text-[var(--text-primary)]">{pass.adultPrice.toLocaleString('fr-FR')} FCFA</strong> / adulte
                    </span>
                  </div>
                </div>

                <ul className="space-y-2 pt-1">
                  {pass.features.map((feat, i) => (
                    <li key={i} className="flex items-start gap-2 text-xs sm:text-sm text-[var(--text-primary)] leading-snug">
                      <CheckCircle2 className="w-4 h-4 text-[var(--brand-primary)] shrink-0 mt-0.5" />
                      <span>{feat}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* TEMPS 5 : Tandem Asymétrique Double CTA (Pilule Simulateur + Lien Chevron WhatsApp ›) */}
              <div className="pt-5 mt-5 border-t border-[var(--border-subtle)] flex flex-wrap items-center justify-between gap-2">
                <button
                  type="button"
                  onClick={() => {
                    setSelectedTrailId(pass.trailKey);
                    setActiveView('billetterie');
                  }}
                  className="cta-pill flex-1 sm:flex-initial"
                >
                  <Ticket className="w-4 h-4 shrink-0" />
                  <span>Simuler ce Pass</span>
                </button>

                <a
                  href={`https://wa.me/237672564598?text=${encodeURIComponent(
                    `Bonjour EcoPark Cameroun, je souhaite commander le ${pass.name} (${pass.childPrice} FCFA enf. / ${pass.adultPrice} FCFA ad.).`
                  )}`}
                  target="_blank"
                  rel="noreferrer"
                  className="cta-chevron"
                >
                  <span>Commander</span>
                  <span aria-hidden="true" className="text-base leading-none font-bold">›</span>
                </a>
              </div>
            </article>
          ))}
        </div>
      </section>

      {/* =================================================================== */}
      {/* LES 5 PÔLES OFFICIELS D'AHALA (100% RENDUS DANS LE DOM - PROFIL B)  */}
      {/* =================================================================== */}
      <section
        id="ahala-production-showcase"
        aria-label="Pôles Officiels ECOPARK CAMEROUN Yaoundé-Ahala"
        className="eco-container space-y-8 scroll-mt-36"
      >
        {/* Section Header */}
        <div className="flex flex-col xl:flex-row xl:items-end justify-between gap-5 border-b border-[var(--border-default)] pb-6">
          <div className="space-y-2 flex-1">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[var(--brand-primary)]/10 type-eyebrow uppercase">
              <Sparkles className="w-3.5 h-3.5" />
              <span>Complexe Intégré · MPECK MULTI-SERVICES (Fondateur : Dr Christophe FOE NDI)</span>
            </div>
            <h2 className="type-h2 text-[var(--text-primary)]">
              Explorez les cinq pôles du domaine d&apos;Ahala.
            </h2>
            <p className="type-body text-[var(--text-muted)] max-w-4xl">
              Quartier <strong>Ahala Barrière (en face de la station Tradex Ahala, RN3)</strong> à 15 minutes du centre-ville de Yaoundé. Consultez nos hébergements 24h/24, notre table gastronomique, nos grilles FCFA, nos offres B2B et le CFP agréé MINEFOP.
            </p>
          </div>

          {/* Navigation Pill Tabs (>= 48px touch box) */}
          <div className="flex flex-wrap gap-2 shrink-0" role="tablist" aria-label="Pôles d'ECOPARK CAMEROUN">
            {[
              { id: 'hebergements', label: 'Hôtels & Suites (30)', icon: BedDouble },
              { id: 'saveurs', label: 'Château des Saveurs', icon: Utensils },
              { id: 'tarifs', label: 'Tarifs Activités FCFA', icon: Ticket },
              { id: 'entreprise', label: 'Groupes & Salle 500 pl.', icon: Building2 },
              { id: 'formation', label: 'CFP Agréé MINEFOP', icon: GraduationCap },
            ].map((tab) => {
              const Icon = tab.icon;
              const isActive = activeTab === tab.id;
              return (
                <button
                  key={tab.id}
                  type="button"
                  role="tab"
                  aria-selected={isActive}
                  aria-controls={`panel-${tab.id}`}
                  onClick={() => handleSelectShowcaseTab(tab.id as ShowcaseTab)}
                  className={`min-h-[48px] px-4 py-2.5 rounded-full text-xs sm:text-sm font-semibold transition-all flex items-center gap-2 cursor-pointer ${
                    isActive
                      ? 'bg-[var(--brand-primary)] text-[var(--on-primary)] shadow-sm'
                      : 'bg-[var(--bg-surface)] text-[var(--text-primary)] border border-[var(--border-default)] hover:border-[var(--brand-primary)]'
                  }`}
                >
                  <Icon className="w-4 h-4 shrink-0" />
                  <span>{tab.label}</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* =================================================================== */}
        {/* TAB 1 : HÉBERGEMENTS & SÉJOURS NATURE (30 UNITÉS - TOUJOURS EN DOM) */}
        {/* =================================================================== */}
        <div
          id="panel-hebergements"
          role="tabpanel"
          className={activeTab === 'hebergements' ? 'space-y-8 block' : 'hidden'}
        >
          {/* Top Highlight Banner: Pack Escapade Couple VIP */}
          <div className="p-6 rounded-2xl bg-gradient-to-r from-[#1B4332] to-[#2D6A4F] text-white shadow-md flex flex-col lg:flex-row lg:items-center justify-between gap-6 tabular-nums">
            <div className="space-y-2 flex-1 max-w-4xl">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/15 text-[#B7E4C7] text-xs font-mono font-bold uppercase">
                <Heart className="w-3.5 h-3.5 text-amber-300" />
                <span>Offre Signature Tout-Inclus · Réception Hôtellerie 24h/24 &amp; 7j/7</span>
              </div>
              <h3 className="type-h3 !text-2xl sm:!text-3xl text-white">
                Pack Escapade Couple VIP : 22 500 FCFA / pers. (45 000 FCFA pour 2).
              </h3>
              <p className="type-body !text-sm text-[#E9F5ED]/90">
                Inclut <strong>1 nuitée en Mini-Suite VIP (Hôtel Ewondo)</strong> + <strong>Dîner gastronomique pour 2 au restaurant « Le Château des Saveurs »</strong> + <strong>Accès illimité au Parc &amp; Jardin Zoologique</strong>. Check-in 14h00 · Check-out 11h00.
              </p>
            </div>

            {/* Tandem Double CTA */}
            <div className="flex flex-wrap items-center gap-3 shrink-0">
              <button
                type="button"
                onClick={() => {
                  setSelectedTrailId('piste-eco-gardes');
                  setActiveView('billetterie');
                }}
                className="cta-pill cta-pill-canopy"
              >
                <Ticket className="w-4 h-4 shrink-0" />
                <span>Simuler mon séjour &amp; Pass</span>
              </button>
              <a
                href="https://wa.me/237694601449?text=Bonjour%20EcoPark%20Cameroun%2C%20je%20souhaite%20r%C3%A9server%20le%20Pack%20Escapade%20Couple%20VIP%20(45%20000%20FCFA)%20ou%20une%20chambre%20%C3%A0%20Ahala."
                target="_blank"
                rel="noreferrer"
                className="cta-chevron cta-chevron-canopy border border-white/25"
              >
                <PhoneCall className="w-4 h-4 text-[#74C69D] shrink-0" />
                <span>WhatsApp Hôtels (+237 694 60 14 49)</span>
                <span aria-hidden="true" className="text-base leading-none font-bold">›</span>
              </a>
            </div>
          </div>

          {/* 4 Hotels & Suites Cards (4:3 face-safe framing + non-overlapping badges) */}
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6 tabular-nums">
            {HOTELS.map((hotel) => (
              <article
                key={hotel.id}
                className="rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-default)] overflow-hidden shadow-xs hover:shadow-md transition-all flex flex-col justify-between group"
              >
                <div>
                  <div className="relative aspect-[4/3] w-full overflow-hidden bg-[#1F2421]">
                    <img
                      src={hotel.photo}
                      alt={hotel.name}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                      style={{ objectPosition: getPhotoObjectPosition(hotel.photo) }}
                    />
                  </div>

                  <div className="p-5 space-y-3">
                    <div className="flex flex-wrap items-center justify-between gap-2">
                      <span className="px-2.5 py-1 rounded-md bg-[var(--brand-primary)]/10 text-[var(--brand-primary)] text-[11px] font-mono font-bold">
                        {hotel.badge}
                      </span>
                      <span className="px-2.5 py-1 rounded-lg bg-[#1B4332] text-white font-['Barlow_Semi_Condensed'] font-bold text-sm shadow-2xs tabular-nums">
                        {hotel.priceFraming}{' '}
                        <span className="text-[11px] font-normal text-[#B7E4C7]">{hotel.unit}</span>
                      </span>
                    </div>

                    <h3 className="type-h3 !text-xl text-[var(--text-primary)]">
                      {hotel.name}
                    </h3>
                    <p className="type-body !text-xs sm:!text-sm text-[var(--text-muted)]">
                      {hotel.description}
                    </p>
                    <ul className="space-y-1.5 pt-1">
                      {hotel.features.map((feat, idx) => (
                        <li key={idx} className="flex items-start gap-2 text-xs text-[var(--text-primary)]">
                          <CheckCircle2 className="w-4 h-4 text-[var(--brand-primary)] shrink-0 mt-0.5" />
                          <span>{feat}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>

                <div className="px-5 py-2.5 bg-[var(--bg-card)] border-t border-[var(--border-default)] flex items-center justify-between gap-2">
                  <span className="type-footnote font-mono truncate tabular-nums">
                    {hotel.priceRange}
                  </span>
                  <a
                    href={`https://wa.me/237694601449?text=${encodeURIComponent(
                      `Bonjour EcoPark Cameroun, je souhaite vérifier la disponibilité : ${hotel.name} (${hotel.priceRange})`
                    )}`}
                    target="_blank"
                    rel="noreferrer"
                    className="cta-chevron !px-3"
                  >
                    <span>Disponibilité</span>
                    <span aria-hidden="true" className="text-base leading-none font-bold">›</span>
                  </a>
                </div>
              </article>
            ))}
          </div>
        </div>

        {/* =================================================================== */}
        {/* TAB 2 : GASTRONOMIE « LE CHÂTEAU DES SAVEURS » (TOUJOURS EN DOM)    */}
        {/* =================================================================== */}
        <div
          id="panel-saveurs"
          role="tabpanel"
          className={activeTab === 'saveurs' ? 'space-y-8 block' : 'hidden'}
        >
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center tabular-nums">
            <div className="lg:col-span-5 rounded-2xl overflow-hidden border border-[var(--border-default)] shadow-md bg-[#1F2421]">
              <div className="aspect-[16/9] w-full overflow-hidden bg-[#1F2421]">
                <img
                  src="/images/ahala/local_cameroon_gastronomy_pergola.png"
                  alt="Restaurant Le Château des Saveurs à EcoPark Ahala"
                  className="w-full h-full object-cover"
                  style={{ objectPosition: getPhotoObjectPosition('/images/ahala/local_cameroon_gastronomy_pergola.png') }}
                />
              </div>
              <div className="p-5 bg-[#1F2421] text-[#E9F5ED] space-y-2.5">
                <div className="text-xs font-mono text-[#74C69D] uppercase font-bold">
                  Ouvert 7j/7 de 07h00 à 23h00 · Sans billet parc en soirée
                </div>
                <h3 className="type-h3 text-white">
                  Pergolas du Lac, Salle VIP New Look (60 pl.) et Boukarous.
                </h3>
                <p className="type-body !text-xs sm:!text-sm text-[#C9D1CC]">
                  Philosophie <strong>« Du bassin à la braise »</strong> : poissons pêchés à la demande dans nos étangs d&apos;Ahala et légumes récoltés sur nos parcelles agroécologiques.
                </p>
                <div className="pt-2 flex flex-wrap items-center gap-2">
                  <button
                    type="button"
                    onClick={() => {
                      setSelectedTrailId('piste-eco-gardes');
                      setActiveView('billetterie');
                    }}
                    className="cta-pill cta-pill-canopy"
                  >
                    <span>Pass Royale avec Repas (8 500 FCFA)</span>
                  </button>
                  <a
                    href="https://wa.me/237672564598?text=Bonjour%20EcoPark%20Cameroun%2C%20je%20souhaite%20r%C3%A9server%20une%20table%20au%20restaurant%20Le%20Ch%C3%A2teau%20des%20Saveurs."
                    target="_blank"
                    rel="noreferrer"
                    className="cta-chevron cta-chevron-canopy"
                  >
                    <span>Réserver une table</span>
                    <span aria-hidden="true" className="text-base leading-none font-bold">›</span>
                  </a>
                </div>
              </div>
            </div>

            <div className="lg:col-span-7 grid grid-cols-1 sm:grid-cols-2 gap-4">
              {MENU_ITEMS.map((item, i) => (
                <div
                  key={i}
                  className="p-5 rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-default)] flex flex-col justify-between space-y-3"
                >
                  <div className="space-y-1.5">
                    <div className="flex items-center justify-between gap-2">
                      <span className="text-[11px] font-mono font-bold uppercase text-[var(--brand-primary)]">
                        {item.tag}
                      </span>
                      <span className="px-2.5 py-1 rounded-lg bg-[var(--brand-primary)] text-[var(--on-primary)] font-['Barlow_Semi_Condensed'] font-bold text-sm tabular-nums">
                        {item.price}
                      </span>
                    </div>
                    <h4 className="font-['Barlow_Semi_Condensed'] text-lg font-bold text-[var(--text-primary)]">
                      {item.name}
                    </h4>
                    <p className="type-body !text-xs sm:!text-sm text-[var(--text-muted)]">
                      {item.desc}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* =================================================================== */}
        {/* TAB 3 : TABLEAU COMPARATIF <table> NATIF (JAMAIS MASQUÉ HORS DOM !) */}
        {/* =================================================================== */}
        <div
          id="panel-tarifs"
          role="tabpanel"
          className={activeTab === 'tarifs' ? 'space-y-6 block' : 'hidden'}
        >
          <div className="rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-default)] overflow-hidden shadow-xs tabular-nums">
            <div className="p-5 bg-[var(--bg-card)] border-b border-[var(--border-default)] flex flex-col lg:flex-row lg:items-center justify-between gap-4">
              <div>
                <h3 className="type-h3 text-[var(--text-primary)]">
                  Grille Tarifaire Officielle des Activités à l&apos;Unité (FCFA).
                </h3>
                <p className="type-footnote mt-1">
                  Horaires Parc &amp; Loisirs : Mardi au Dimanche de 09h00 à 18h00 (Fermé le lundi pour repos biologique et maintenance).
                </p>
              </div>
              <div className="flex flex-wrap items-center gap-2 shrink-0">
                <button
                  type="button"
                  onClick={() => {
                    setSelectedTrailId('marais');
                    setActiveView('billetterie');
                  }}
                  className="cta-pill"
                >
                  <Ticket className="w-4 h-4 shrink-0" />
                  <span>Simuler mon Pass (dès 500 FCFA)</span>
                </button>
                <a
                  href="https://wa.me/237672564598?text=Bonjour%20EcoPark%20Cameroun%2C%20je%20souhaite%20un%20renseignement%20sur%20les%20tarifs%20d%27Ahala."
                  target="_blank"
                  rel="noreferrer"
                  className="cta-chevron"
                >
                  <span>Devis WhatsApp</span>
                  <span aria-hidden="true" className="text-base leading-none font-bold">›</span>
                </a>
              </div>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse text-xs sm:text-sm tabular-nums">
                <thead>
                  <tr className="border-b border-[var(--border-default)] bg-[var(--bg-canvas)] text-[var(--text-muted)] font-mono text-xs uppercase">
                    <th className="py-3.5 px-4 font-semibold">Activité / Service à Yaoundé - Ahala</th>
                    <th className="py-3.5 px-4 font-semibold">Enfant (3 à 12 ans)</th>
                    <th className="py-3.5 px-4 font-semibold">Adulte (13+ ans)</th>
                    <th className="py-3.5 px-4 font-semibold">Précisions Officielles</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[var(--border-default)]/60">
                  {UNIT_ACTIVITIES.map((act, idx) => (
                    <tr key={idx} className="hover:bg-[var(--bg-card)]/60 transition-colors">
                      <td className="py-3 px-4 font-semibold text-[var(--text-primary)]">{act.name}</td>
                      <td className="py-3 px-4 font-mono font-bold text-[var(--brand-primary)] tabular-nums">{act.child}</td>
                      <td className="py-3 px-4 font-mono font-bold text-[var(--text-primary)] tabular-nums">{act.adult}</td>
                      <td className="py-3 px-4 text-xs text-[var(--text-muted)]">{act.note}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        {/* =================================================================== */}
        {/* TAB 4 : GROUPES, ÉCOLES, SÉMINAIRES & SALLE 500 PLACES (EN DOM)     */}
        {/* =================================================================== */}
        <div
          id="panel-entreprise"
          role="tabpanel"
          className={activeTab === 'entreprise' ? 'grid grid-cols-1 md:grid-cols-2 gap-6' : 'hidden'}
        >
          <div className="p-6 rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-default)] space-y-3 flex flex-col justify-between tabular-nums">
            <div className="space-y-2.5">
              <span className="px-2.5 py-1 rounded-md bg-emerald-500/10 text-[var(--brand-primary)] font-mono text-xs font-bold inline-block">
                Excursions Scolaires &amp; Arbres de Noël
              </span>
              <h3 className="type-h3 text-[var(--text-primary)]">
                À partir de 1 350 FCFA / élève · Excursion Scolaire Clé en Main.
              </h3>
              <p className="type-body !text-sm text-[var(--text-muted)]">
                Circuit pédagogique encadré incluant le Jardin Zoologique (Gorille « ToTo », chimpanzés, tortues), la découverte des bassins piscicoles, l&apos;aire de pique-nique sécurisée et la <strong>gratuité pour les enseignants accompagnateurs</strong>.
              </p>
            </div>
            <div className="pt-3 flex flex-wrap items-center gap-2">
              <a
                href="https://wa.me/237672564598?text=Bonjour%20EcoPark%20Cameroun%2C%20je%20souhaite%20un%20devis%20Excursion%20Scolaire%20(1%20350%20FCFA%20%2F%20%C3%A9l%C3%A8ve)."
                target="_blank"
                rel="noreferrer"
                className="cta-chevron !px-0"
              >
                <span>Demander un devis école</span>
                <span aria-hidden="true" className="text-base leading-none font-bold">›</span>
              </a>
            </div>
          </div>

          <div className="p-6 rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-default)] space-y-3 flex flex-col justify-between tabular-nums">
            <div className="space-y-2.5">
              <span className="px-2.5 py-1 rounded-md bg-emerald-500/10 text-[var(--brand-primary)] font-mono text-xs font-bold inline-block">
                Team Building &amp; Séminaires B2B (Min. 15 pers.)
              </span>
              <h3 className="type-h3 text-[var(--text-primary)]">
                À partir de 15 000 FCFA / participant · Journée Séminaire au Vert.
              </h3>
              <p className="type-body !text-sm text-[var(--text-muted)]">
                Salle climatisée équipée (vidéoprojecteur, sonorisation, Wi-Fi), 2 pauses-café, déjeuner gastronomique au restaurant « Le Château des Saveurs » et détente (Piscine Semi-Olympique ou Pirogue).
              </p>
            </div>
            <div className="pt-3 flex flex-wrap items-center gap-2">
              <a
                href="https://wa.me/237672564598?text=Bonjour%20EcoPark%20Cameroun%2C%20nous%20souhaitons%20organiser%20un%20S%C3%A9minaire%20B2B%20(15%20000%20FCFA%20%2F%20participant)."
                target="_blank"
                rel="noreferrer"
                className="cta-chevron !px-0"
              >
                <span>Demander un devis B2B</span>
                <span aria-hidden="true" className="text-base leading-none font-bold">›</span>
              </a>
            </div>
          </div>

          <div className="p-6 rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-default)] space-y-3 flex flex-col justify-between tabular-nums">
            <div className="space-y-2.5">
              <span className="px-2.5 py-1 rounded-md bg-emerald-500/10 text-[var(--brand-primary)] font-mono text-xs font-bold inline-block">
                Grandes Réceptions, Mariages &amp; Congrès
              </span>
              <h3 className="type-h3 text-[var(--text-primary)]">
                Salle Polyvalente « Menkii Essomba Anton » · 500 Places Assises.
              </h3>
              <p className="type-body !text-sm text-[var(--text-muted)]">
                500 places assises climatisées, scène modulable, régie son &amp; lumière professionnelle, loges VIP, groupe électrogène de secours et service traiteur du Château des Saveurs.
              </p>
            </div>
            <div className="pt-3 flex flex-wrap items-center gap-2">
              <a
                href="https://wa.me/237672564598?text=Bonjour%20EcoPark%20Cameroun%2C%20je%20souhaite%20privatiser%20la%20Salle%20Polyvalente%20Menkii%20Essomba%20Anton%20(500%20places)."
                target="_blank"
                rel="noreferrer"
                className="cta-chevron !px-0"
              >
                <span>Vérifier une date de salle</span>
                <span aria-hidden="true" className="text-base leading-none font-bold">›</span>
              </a>
            </div>
          </div>

          <div className="p-6 rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-default)] space-y-3 flex flex-col justify-between tabular-nums">
            <div className="space-y-2.5">
              <span className="px-2.5 py-1 rounded-md bg-emerald-500/10 text-[var(--brand-primary)] font-mono text-xs font-bold inline-block">
                Familles Nombreuses, Associations &amp; Comités
              </span>
              <h3 className="type-h3 text-[var(--text-primary)]">
                À partir de 700 FCFA / adulte · Remise Groupe 20+ (-30 %).
              </h3>
              <p className="type-body !text-sm text-[var(--text-muted)]">
                Dès 20 participants, l&apos;entrée adulte au Parc &amp; Jardin Zoologique passe à <strong>700 FCFA au lieu de 1 000 FCFA</strong> (enfant à 500 FCFA). Référence devis <code>DEV-2026-XXXX</code> au <strong>+237 672 56 45 98</strong>.
              </p>
            </div>
            <div className="pt-3 flex flex-wrap items-center gap-2">
              <button
                type="button"
                onClick={() => setActiveView('billetterie')}
                className="cta-pill"
              >
                <span>Simuler un tarif Groupe (-30%)</span>
              </button>
            </div>
          </div>
        </div>

        {/* =================================================================== */}
        {/* TAB 5 : CFP AGRÉÉ MINEFOP - PRICE FRAMING INVERSÉ 4 TRANCHES (DOM)  */}
        {/* =================================================================== */}
        <div
          id="panel-formation"
          role="tabpanel"
          className={activeTab === 'formation' ? 'space-y-6 block' : 'hidden'}
        >
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center tabular-nums">
            <div className="lg:col-span-5 rounded-2xl overflow-hidden border border-[var(--border-default)] bg-[#1F2421] shadow-md">
              <div className="aspect-[16/9] w-full overflow-hidden bg-[#1F2421]">
                <img
                  src="/images/ahala/local_cameroon_cfp_students.png"
                  alt="Apprenants du CFP ECOPARK agréé par le MINEFOP à Yaoundé-Ahala"
                  className="w-full h-full object-cover"
                  style={{ objectPosition: getPhotoObjectPosition('/images/ahala/local_cameroon_cfp_students.png') }}
                />
              </div>
              <div className="p-5 text-[#E9F5ED] space-y-2.5">
                <div className="text-xs font-mono font-bold text-[#74C69D] uppercase">
                  Diplômes d&apos;État DQP / CQP · Agrément Officiel MINEFOP
                </div>
                {/* Price Framing Inversé sur l'échéancier réel validé en 4 tranches */}
                <h3 className="type-h3 text-white">
                  À partir de 50 000 FCFA / tranche · Scolarité 250 000 FCFA / an.
                </h3>
                <p className="type-body !text-xs sm:!text-sm text-[#C9D1CC]">
                  Inscription officielle : <strong>50 000 FCFA</strong>. Scolarité réglable en <strong>4 tranches souples</strong> : 100 000 FCFA à la rentrée + 3 tranches de 50 000 FCFA. Cursus de 12 mois avec <strong>70 % de pratique réelle</strong> sur le complexe d&apos;Ahala.
                </p>
                <div className="pt-2">
                  <a
                    href="https://wa.me/237672564598?text=Bonjour%20CFP%20EcoPark%20MINEFOP%2C%20je%20souhaite%20recevoir%20le%20dossier%20d%27inscription%20(50%20000%20FCFA%20%2B%204%20tranches)."
                    target="_blank"
                    rel="noreferrer"
                    className="cta-pill cta-pill-canopy"
                  >
                    <GraduationCap className="w-4 h-4 shrink-0" />
                    <span>Demander le dossier CFP sur WhatsApp ›</span>
                  </a>
                </div>
              </div>
            </div>

            <div className="lg:col-span-7 space-y-3">
              <h3 className="type-h3 text-[var(--text-primary)]">
                Cinq filières professionnelles en immersion réelle à Ahala.
              </h3>
              <div className="grid grid-cols-1 gap-3">
                {CFP_PROGRAMS.map((prog) => (
                  <div
                    key={prog.num}
                    className="p-4 rounded-xl bg-[var(--bg-surface)] border border-[var(--border-default)] flex items-start gap-4"
                  >
                    <span className="px-3 py-1.5 rounded-lg bg-[var(--brand-primary)] text-[var(--on-primary)] font-mono font-bold text-xs shrink-0 tabular-nums">
                      {prog.num}
                    </span>
                    <div>
                      <h4 className="font-['Barlow_Semi_Condensed'] text-lg font-bold text-[var(--text-primary)]">
                        {prog.title}
                      </h4>
                      <p className="type-body !text-xs sm:!text-sm text-[var(--text-muted)] mt-0.5">
                        {prog.outcome}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* =================================================================== */}
      {/* TEMPS 7 : CROSS-SELL COMPLÉMENTAIRE PERTINENT (OPTIONS D'AHALA)     */}
      {/* =================================================================== */}
      <section
        id="cross-sell-options"
        aria-label="Options et services complémentaires ECOPARK CAMEROUN"
        className="eco-container space-y-6"
      >
        <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
          <div className="space-y-1.5">
            <span className="type-eyebrow uppercase">Confort &amp; Services Associés</span>
            <h2 className="type-h2 text-[var(--text-primary)]">
              Complétez votre journée à Ahala.
            </h2>
          </div>
          <span className="type-footnote font-mono tabular-nums">
            Réservation en ligne ou ajout direct au guichet RN3
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-5 tabular-nums">
          {CROSS_SELL_OPTIONS.map((opt) => {
            const Icon = opt.icon;
            return (
              <article
                key={opt.id}
                className="p-5 rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-default)] flex flex-col justify-between space-y-4 shadow-xs"
              >
                <div className="space-y-2.5">
                  <div className="flex items-center justify-between gap-2">
                    <span className="w-9 h-9 rounded-xl bg-[var(--brand-primary)]/10 text-[var(--brand-primary)] flex items-center justify-center shrink-0">
                      <Icon className="w-4 h-4" />
                    </span>
                    <span className="type-footnote font-mono font-semibold text-[var(--brand-primary)]">
                      {opt.badge}
                    </span>
                  </div>
                  <h3 className="type-h3 !text-xl text-[var(--text-primary)]">{opt.title}</h3>
                  <div className="font-['Barlow_Semi_Condensed'] font-bold text-lg text-[var(--brand-primary)] tabular-nums">
                    {opt.price}
                  </div>
                  <p className="type-body !text-xs sm:!text-sm text-[var(--text-muted)]">
                    {opt.desc}
                  </p>
                </div>

                <div className="pt-3 border-t border-[var(--border-subtle)] flex items-center justify-between">
                  <button
                    type="button"
                    onClick={() => setActiveView('billetterie')}
                    className="cta-chevron !px-2"
                  >
                    <span>Simuler</span>
                    <span aria-hidden="true" className="text-base leading-none font-bold">›</span>
                  </button>
                  <a
                    href={`https://wa.me/237672564598?text=${encodeURIComponent(opt.waText)}`}
                    target="_blank"
                    rel="noreferrer"
                    className="cta-chevron !px-2"
                  >
                    <span>WhatsApp</span>
                    <span aria-hidden="true" className="text-base leading-none font-bold">›</span>
                  </a>
                </div>
              </article>
            );
          })}
        </div>

        {/* Bottom Practical Info Strip */}
        <div className="p-4 sm:p-5 rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-default)] flex flex-wrap items-center justify-between gap-4 text-xs tabular-nums">
          <div className="flex items-center gap-2 text-[var(--text-primary)] font-medium">
            <MapPin className="w-4 h-4 text-[var(--brand-primary)] shrink-0" />
            <span>
              <strong>Accès :</strong> Yaoundé - Ahala Barrière, en face de la station-service Tradex Ahala (RN3, route 100 % goudronnée, parking gratuit).
            </span>
          </div>
          <div className="flex flex-wrap items-center gap-4 font-mono text-[var(--text-muted)] tabular-nums">
            <span className="flex items-center gap-1">
              <Clock className="w-3.5 h-3.5 text-[var(--brand-primary)]" />
              Parc : Mar-Dim 09h-18h · Hôtels 24h/24 · Restaurant 07h-23h
            </span>
            <span className="flex items-center gap-1 text-[var(--brand-primary)] font-bold">
              <ShieldCheck className="w-3.5 h-3.5" />
              WhatsApp : +237 672 56 45 98
            </span>
          </div>
        </div>
      </section>
    </div>
  );
};
