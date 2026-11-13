// ============================================================================
// ECOPARK CAMEROUN (YAOUNDÉ – AHALA) — VALIDATED PRODUCTION SHOWCASE
// (src/components/discovery/AhalaShowcase.tsx)
// Complete Production Content: Hotels (30 units), Le Château des Saveurs,
// Official Activity Tariffs (FCFA), B2B/Schools (500-seat hall) & CFP MINEFOP
// ============================================================================

import React, { useState, useEffect } from 'react';
import { useEcoPark } from '../../context/EcoParkContext';
import {
  type ShowcaseTab,
  SHOWCASE_TAB_PATH_MAP,
  SHOWCASE_DEEP_PATHS,
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
  ArrowRight,
  Heart,
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
    window.addEventListener('popstate', handlePopState);
    return () => window.removeEventListener('popstate', handlePopState);
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

  const HOTELS = [
    {
      id: 'ewondo',
      name: 'Hôtel Ewondo • Loges & Mini-Suites VIP',
      badge: '4 Mini-Suites VIP · Standing Supérieur',
      priceRange: '25 000 à 30 000 FCFA',
      unit: '/ nuitée',
      photo: '/images/ahala/chambre.jpeg',
      description:
        'Loges spacieuses et Mini-Suites VIP nichées au calme sous les arbres d Ahala, idéales pour les séjours romantiques, cadres en mission et week-ends détente.',
      features: [
        'Climatisation split silencieuse & Lit King-Size orthopédique',
        'Terrasse privative sur jardin, Eau chaude & TV écran plat Canal+',
        'Accès gratuit au Parc & Jardin Zoologique pendant le séjour',
        'Service en chambre depuis Le Château des Saveurs (07h–23h)',
      ],
    },
    {
      id: 'chanthel',
      name: 'Hôtel Chanthel • Chambres Confort',
      badge: '12 Chambres Climatisées · 3 Paliers',
      priceRange: '15 000 à 25 000 FCFA',
      unit: '/ nuitée (15k / 20k / 25k)',
      photo: '/images/ahala/IMG-20260713-WA0051_043420.jpg',
      description:
        'Un cocon de fraîcheur forestière offrant le meilleur rapport qualité-prix de Yaoundé-Sud avec 3 catégories de confort adaptées aux familles et voyageurs.',
      features: [
        'Paliers officiels : 15 000 FCFA, 20 000 FCFA et 25 000 FCFA / nuitée',
        'Salle d eau privative moderne, climatisation & literie grand confort',
        'Environnement calme et verdoyant à 15 min du centre-ville',
        'Parking gratuit sous vidéosurveillance 24h/24 face Tradex RN3',
      ],
    },
    {
      id: 'bene',
      name: 'Hôtel Bene • Chambres Standard & Day-Use',
      badge: '10 Chambres · Grande Véranda d Étage',
      priceRange: '10 000 à 15 000 FCFA',
      unit: '/ nuitée ou Day-Use',
      photo: '/images/ahala/IMG-20260809-WA0009.jpg',
      description:
        'Solution économique, propre et sécurisée disposant d une grande véranda conviviale à l étage pouvant accueillir de petites réunions de groupe.',
      features: [
        'Tarif accessible : 10 000 à 15 000 FCFA (Nuitée ou Repos Day-Use)',
        'Grande véranda d étage aménagée pour échanges et détente',
        'Réception Hôtellerie ouverte 24h/24 et 7j/7',
        'Check-in dès 14h00 · Check-out jusqu à 11h00',
      ],
    },
    {
      id: 'suites-vip',
      name: 'Suites Privées Prestige VIP',
      badge: '4 Suites Haut de Gamme · Salon Privé',
      priceRange: '30 000 à 45 000 FCFA',
      unit: '/ nuitée',
      photo: '/images/ahala/local_cameroon_gastronomy_pergola.png',
      description:
        'Expérience présidentielle à EcoPark Cameroun avec salon privé climatisé, chambre séparée, room-service prioritaire et accès coupe-file aux loisirs.',
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
      desc: 'Tilapia, carpe ou silure pêché directement dans nos bassins d Ahala, mariné aux épices du terroir et braisé au feu de bois, servi avec plantains mûrs, miondo ou frites.',
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
      desc: 'Feuilles de ndolé fraîches longuement préparées aux arachides onctueuses, crevettes et viande fondante.',
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
    { name: 'Entrée Parc & Jardin Zoologique seul (Gorille ToTo, chimpanzés, tortues)', adult: '1 000 FCFA', child: '500 FCFA', note: 'Gratuit (< 3 ans)' },
    { name: 'Balade en Pirogue sur le lac (45 min, gilet de sauvetage fourni)', adult: '1 000 FCFA', child: '500 FCFA', note: 'Embarcadère sécurisé' },
    { name: 'Piscine Semi-Olympique surveillée par maîtres-nageurs', adult: '2 500 FCFA', child: '1 500 FCFA', note: 'Enfant week-end guichet : 2 500 FCFA' },
    { name: 'Balade à Cheval & Initiation Manège Équestre', adult: '1 000 FCFA', child: '500 FCFA', note: 'Casque & moniteur inclus' },
    { name: 'Musée Culturel et du Patrimoine Camerounais', adult: '1 000 FCFA', child: '500 FCFA', note: 'Visite commentée' },
    { name: 'Bibliothèque & Espace Lecture Jeunesse', adult: '500 FCFA', child: '500 FCFA', note: 'Accès journée' },
    { name: 'Aire de Jeux Enfants & Châteaux Gonflables', adult: '—', child: '500 FCFA', note: 'Surveillance dédiée' },
    { name: 'Pêche de Loisir aux Étangs Piscicoles', adult: '2 000 FCFA', child: '2 000 FCFA', note: 'Matériel & conseils inclus' },
    { name: 'Sachet de Nourrissage (Poissons des bassins & Tortues)', adult: '500 FCFA', child: '500 FCFA', note: 'Activité coup de cœur enfants' },
    { name: 'Halte-Garderie & Crèche Sécurisée', adult: '1 500 FCFA', child: '1 500 FCFA', note: 'Tarif groupe : 1 000 FCFA / enfant' },
    { name: 'Navette Climatisée Aller-Retour (Yaoundé ↔ Ahala)', adult: '1 500 FCFA', child: '1 000 FCFA', note: 'Bus 5, 18 et 32 places' },
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

  return (
    <section
      id="ahala-production-showcase"
      aria-label="Pôles Officiels ECOPARK CAMEROUN Yaoundé-Ahala"
      className="eco-container space-y-8"
    >
      {/* Section Header */}
      <div className="flex flex-col xl:flex-row xl:items-end justify-between gap-5 border-b border-[var(--border-default)] pb-6">
        <div className="space-y-2 flex-1">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[var(--brand-primary)]/10 text-[var(--brand-primary)] text-xs font-mono font-bold uppercase tracking-wider">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Complexe Intégré · MPECK MULTI-SERVICES (Fondateur : Dr Christophe FOE NDI)</span>
          </div>
          <h2 className="font-['Barlow_Semi_Condensed'] text-2xl sm:text-4xl font-bold text-[var(--text-primary)] tracking-tight">
            Les 5 Pôles Officiels d&apos;ECOPARK CAMEROUN à Yaoundé – Ahala
          </h2>
          <p className="text-sm sm:text-base text-[var(--text-muted)] max-w-4xl">
            Situé au quartier <strong>Ahala Barrière (en face de la station-service Tradex Ahala, RN3)</strong> à 15 minutes du centre-ville de Yaoundé. Retrouvez l&apos;intégralité de nos offres et tarifs officiels en FCFA.
          </p>
        </div>

        {/* Navigation Pill Tabs */}
        <div className="flex flex-wrap gap-2 shrink-0">
          {[
            { id: 'hebergements', label: 'Hôtels & Suites (30)', icon: BedDouble },
            { id: 'saveurs', label: 'Château des Saveurs', icon: Utensils },
            { id: 'tarifs', label: 'Tarifs Activités & Pass', icon: Ticket },
            { id: 'entreprise', label: 'Groupes, Écoles & Salle 500 pl.', icon: Building2 },
            { id: 'formation', label: 'CFP Agréé MINEFOP', icon: GraduationCap },
          ].map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                type="button"
                onClick={() => handleSelectShowcaseTab(tab.id as ShowcaseTab)}
                className={`px-3.5 py-2.5 rounded-xl text-xs sm:text-sm font-semibold transition-all flex items-center gap-2 cursor-pointer ${
                  isActive
                    ? 'bg-[var(--brand-primary)] text-white shadow-sm'
                    : 'bg-[var(--bg-surface)] text-[var(--text-primary)] border border-[var(--border-default)] hover:border-[var(--brand-primary)]'
                }`}
              >
                <Icon className="w-4 h-4" />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* =================================================================== */}
      {/* TAB 1 : HÉBERGEMENTS & SÉJOURS NATURE (30 UNITÉS)                   */}
      {/* =================================================================== */}
      {activeTab === 'hebergements' && (
        <div className="space-y-8 animate-in fade-in duration-200">
          {/* Top Highlight Banner: Pack Escapade Couple VIP */}
          <div className="p-6 rounded-2xl bg-gradient-to-r from-[#1B4332] to-[#2D6A4F] text-white shadow-md flex flex-col lg:flex-row lg:items-center justify-between gap-6">
            <div className="space-y-2 flex-1 max-w-4xl">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/15 text-[#B7E4C7] text-xs font-mono font-bold uppercase">
                <Heart className="w-3.5 h-3.5 text-amber-300" />
                <span>Offre Signature Tout-Inclus · Réception Hôtellerie 24h/24 &amp; 7j/7</span>
              </div>
              <h3 className="font-['Barlow_Semi_Condensed'] text-2xl sm:text-3xl font-bold">
                Pack Escapade Couple VIP — 45 000 FCFA (pour 2 personnes)
              </h3>
              <p className="text-sm text-[#E9F5ED]/90 leading-relaxed">
                Inclut <strong>1 nuitée en Mini-Suite VIP (Hôtel Ewondo)</strong> + <strong>Dîner gastronomique pour 2 au restaurant « Le Château des Saveurs »</strong> + <strong>Accès illimité au Parc &amp; Jardin Zoologique</strong>. Check-in 14h00 · Check-out 11h00.
              </p>
            </div>

            <div className="flex flex-wrap items-center gap-3 shrink-0">
              <a
                href="https://wa.me/237694601449?text=Bonjour%20EcoPark%20Cameroun%2C%20je%20souhaite%20r%C3%A9server%20un%20h%C3%A9bergement%20%C3%A0%20Ahala."
                target="_blank"
                rel="noreferrer"
                className="px-5 py-3 rounded-xl bg-[#D4A373] hover:bg-[#e0b284] text-[#1F2421] font-bold text-xs sm:text-sm shadow-sm flex items-center gap-2"
              >
                <PhoneCall className="w-4 h-4" />
                <span>WhatsApp Hôtels : +237 694 60 14 49</span>
              </a>
              <button
                type="button"
                onClick={() => {
                  setSelectedTrailId('piste-eco-gardes');
                  setActiveView('billetterie');
                }}
                className="px-4 py-3 rounded-xl bg-white/15 hover:bg-white/25 text-white font-semibold text-xs sm:text-sm border border-white/25 cursor-pointer flex items-center gap-1.5"
              >
                <span>Réserver un Pass Parc</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* 4 Hotels & Suites Cards (4:3 face-safe framing + non-overlapping badges) */}
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
            {HOTELS.map((hotel) => (
              <div
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
                      <span className="px-2.5 py-1 rounded-lg bg-[#1B4332] text-white font-['Barlow_Semi_Condensed'] font-bold text-sm shadow-2xs">
                        {hotel.priceRange}{' '}
                        <span className="text-[11px] font-normal text-[#B7E4C7]">{hotel.unit}</span>
                      </span>
                    </div>

                    <h3 className="font-['Barlow_Semi_Condensed'] text-xl font-bold text-[var(--text-primary)]">
                      {hotel.name}
                    </h3>
                    <p className="text-xs sm:text-sm text-[var(--text-muted)] leading-relaxed">
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

                <div className="px-5 py-3.5 bg-[var(--bg-elevated)] border-t border-[var(--border-default)] flex items-center justify-between gap-2 text-xs">
                  <span className="font-mono text-[11px] text-[var(--text-muted)] truncate">
                    24h/24 · +237 694 60 14 49
                  </span>
                  <a
                    href={`https://wa.me/237694601449?text=${encodeURIComponent(`Bonjour EcoPark Cameroun, je souhaite réserver : ${hotel.name} (${hotel.priceRange})`)}`}
                    target="_blank"
                    rel="noreferrer"
                    className="font-bold text-[var(--brand-primary)] hover:underline flex items-center gap-1 shrink-0"
                  >
                    <span>Disponibilité</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </a>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* =================================================================== */}
      {/* TAB 2 : GASTRONOMIE « LE CHÂTEAU DES SAVEURS »                      */}
      {/* =================================================================== */}
      {activeTab === 'saveurs' && (
        <div className="space-y-8 animate-in fade-in duration-200">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
            <div className="lg:col-span-5 rounded-2xl overflow-hidden border border-[var(--border-default)] shadow-md bg-[#1F2421]">
              <div className="aspect-[16/9] w-full overflow-hidden bg-[#1F2421]">
                <img
                  src="/images/ahala/local_cameroon_gastronomy_pergola.png"
                  alt="Restaurant Le Château des Saveurs — Pergolas au bord du lac d'Ahala"
                  className="w-full h-full object-cover"
                  style={{ objectPosition: getPhotoObjectPosition('/images/ahala/local_cameroon_gastronomy_pergola.png') }}
                />
              </div>
              <div className="p-5 bg-[#1F2421] text-[#E9F5ED] space-y-2">
                <div className="text-xs font-mono text-[#74C69D] uppercase font-bold">
                  Ouvert 7j/7 de 07h00 à 23h00 · Sans billet d&apos;entrée parc le soir
                </div>
                <div className="font-['Barlow_Semi_Condensed'] text-xl font-bold text-white">
                  3 Ambiances : Pergolas du Lac · Salle VIP New Look (60 pl.) · Boukarous &amp; Eco SNACK
                </div>
                <p className="text-xs text-[#C9D1CC]">
                  Notre philosophie <strong>« Du bassin à la braise »</strong> : poissons pêchés à la demande dans nos étangs d&apos;Ahala et légumes récoltés sur nos parcelles agroécologiques.
                </p>
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
                      <span className="px-2.5 py-1 rounded-lg bg-[var(--brand-primary)] text-white font-['Barlow_Semi_Condensed'] font-bold text-sm">
                        {item.price}
                      </span>
                    </div>
                    <h4 className="font-['Barlow_Semi_Condensed'] text-base font-bold text-[var(--text-primary)]">
                      {item.name}
                    </h4>
                    <p className="text-xs text-[var(--text-muted)] leading-relaxed">
                      {item.desc}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* =================================================================== */}
      {/* TAB 3 : GRILLE TARIFAIRE OFFICIELLE DES ACTIVITÉS (FCFA)            */}
      {/* =================================================================== */}
      {activeTab === 'tarifs' && (
        <div className="space-y-6 animate-in fade-in duration-200">
          <div className="rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-default)] overflow-hidden shadow-xs">
            <div className="p-5 bg-[var(--bg-elevated)] border-b border-[var(--border-default)] flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <div>
                <h3 className="font-['Barlow_Semi_Condensed'] text-xl font-bold text-[var(--text-primary)]">
                  Grille Tarifaire Officielle des Activités à l&apos;Unité (en FCFA)
                </h3>
                <p className="text-xs text-[var(--text-muted)]">
                  Horaires Parc &amp; Loisirs : Mardi au Dimanche de 09h00 à 18h00 (Fermé le lundi pour repos biologique et maintenance).
                </p>
              </div>
              <button
                type="button"
                onClick={() => {
                  setSelectedTrailId('marais');
                  setActiveView('billetterie');
                }}
                className="px-4 py-2.5 rounded-xl bg-[var(--brand-primary)] text-white font-bold text-xs cursor-pointer flex items-center gap-1.5 self-start sm:self-auto"
              >
                <Ticket className="w-4 h-4" />
                <span>Réserver un Pass Tout-Inclus (dès 1 000 FCFA)</span>
              </button>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse text-xs sm:text-sm">
                <thead>
                  <tr className="border-b border-[var(--border-default)] bg-[var(--bg-canvas)] text-[var(--text-muted)] font-mono text-xs uppercase">
                    <th className="py-3.5 px-4 font-semibold">Activité / Service à Yaoundé-Ahala</th>
                    <th className="py-3.5 px-4 font-semibold">Adulte (13+ ans)</th>
                    <th className="py-3.5 px-4 font-semibold">Enfant (3–12 ans)</th>
                    <th className="py-3.5 px-4 font-semibold">Précisions Officielles</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[var(--border-default)]/60">
                  {UNIT_ACTIVITIES.map((act, idx) => (
                    <tr key={idx} className="hover:bg-[var(--bg-elevated)]/60 transition-colors">
                      <td className="py-3 px-4 font-semibold text-[var(--text-primary)]">{act.name}</td>
                      <td className="py-3 px-4 font-mono font-bold text-[var(--brand-primary)]">{act.adult}</td>
                      <td className="py-3 px-4 font-mono font-bold text-[var(--text-primary)]">{act.child}</td>
                      <td className="py-3 px-4 text-xs text-[var(--text-muted)]">{act.note}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* =================================================================== */}
      {/* TAB 4 : GROUPES, ÉCOLES, SÉMINAIRES & SALLE 500 PLACES              */}
      {/* =================================================================== */}
      {activeTab === 'entreprise' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 animate-in fade-in duration-200">
          <div className="p-6 rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-default)] space-y-3">
            <span className="px-2.5 py-1 rounded-md bg-emerald-500/10 text-[var(--brand-primary)] font-mono text-xs font-bold">
              Excursions Scolaires &amp; Arbres de Noël
            </span>
            <h3 className="font-['Barlow_Semi_Condensed'] text-2xl font-bold text-[var(--text-primary)]">
              Forfait Excursion Scolaire Clé en Main — 1 350 FCFA / élève
            </h3>
            <p className="text-xs sm:text-sm text-[var(--text-muted)] leading-relaxed">
              Circuit pédagogique encadré incluant la visite du Jardin Zoologique (Gorille « ToTo », chimpanzés, tortues), la découverte des bassins piscicoles, l&apos;accès à l&apos;aire de pique-nique sécurisée et la <strong>gratuité pour les enseignants accompagnateurs</strong>.
            </p>
          </div>

          <div className="p-6 rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-default)] space-y-3">
            <span className="px-2.5 py-1 rounded-md bg-emerald-500/10 text-[var(--brand-primary)] font-mono text-xs font-bold">
              Team Building &amp; Séminaires B2B (Min. 15 pers.)
            </span>
            <h3 className="font-['Barlow_Semi_Condensed'] text-2xl font-bold text-[var(--text-primary)]">
              Forfait Séminaire &amp; Journée au Vert — 15 000 FCFA / participant
            </h3>
            <p className="text-xs sm:text-sm text-[var(--text-muted)] leading-relaxed">
              Salle de réunion climatisée équipée (vidéoprojecteur, sonorisation, Wi-Fi), 2 pauses-café, déjeuner gastronomique au restaurant « Le Château des Saveurs » et détente en fin de journée (Piscine Semi-Olympique ou Balade en Pirogue).
            </p>
          </div>

          <div className="p-6 rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-default)] space-y-3">
            <span className="px-2.5 py-1 rounded-md bg-emerald-500/10 text-[var(--brand-primary)] font-mono text-xs font-bold">
              Grandes Réceptions, Mariages &amp; Congrès
            </span>
            <h3 className="font-['Barlow_Semi_Condensed'] text-2xl font-bold text-[var(--text-primary)]">
              Salle Polyvalente « Menkii Essomba Anton » — 500 Places Assises
            </h3>
            <p className="text-xs sm:text-sm text-[var(--text-muted)] leading-relaxed">
              Infrastructure événementielle de référence à Yaoundé-Ahala : 500 places assises climatisées, scène modulable, régie son &amp; lumière professionnelle, loges VIP, groupe électrogène de secours et service traiteur du Château des Saveurs.
            </p>
          </div>

          <div className="p-6 rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-default)] space-y-3">
            <span className="px-2.5 py-1 rounded-md bg-emerald-500/10 text-[var(--brand-primary)] font-mono text-xs font-bold">
              Familles Nombreuses, Associations &amp; Comités
            </span>
            <h3 className="font-['Barlow_Semi_Condensed'] text-2xl font-bold text-[var(--text-primary)]">
              Remise Officielle Groupes (20+ pers.) — -30 % (700 FCFA / adulte)
            </h3>
            <p className="text-xs sm:text-sm text-[var(--text-muted)] leading-relaxed">
              Dès 20 participants, l&apos;entrée adulte au Parc &amp; Jardin Zoologique passe à <strong>700 FCFA au lieu de 1 000 FCFA</strong> (tarif enfant maintenu à 500 FCFA). Devis sur mesure sous référence <code>DEV-2026-XXXX</code> au <strong>+237 672 56 45 98</strong>.
            </p>
          </div>
        </div>
      )}

      {/* =================================================================== */}
      {/* TAB 5 : CENTRE DE FORMATION PROFESSIONNELLE CFP AGRÉÉ MINEFOP       */}
      {/* =================================================================== */}
      {activeTab === 'formation' && (
        <div className="space-y-6 animate-in fade-in duration-200">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
            <div className="lg:col-span-5 rounded-2xl overflow-hidden border border-[var(--border-default)] bg-[#1F2421] shadow-md">
              <div className="aspect-[16/9] w-full overflow-hidden bg-[#1F2421]">
                <img
                  src="/images/ahala/local_cameroon_cfp_students.png"
                  alt="Apprenants du CFP ECOPARK agréé par le MINEFOP à Yaoundé-Ahala"
                  className="w-full h-full object-cover"
                  style={{ objectPosition: getPhotoObjectPosition('/images/ahala/local_cameroon_cfp_students.png') }}
                />
              </div>
              <div className="p-5 text-[#E9F5ED] space-y-2">
                <div className="text-xs font-mono font-bold text-[#74C69D] uppercase">
                  Diplômes d&apos;État DQP / CQP · Agrément Officiel MINEFOP
                </div>
                <h3 className="font-['Barlow_Semi_Condensed'] text-2xl font-bold text-white">
                  Inscription : 50 000 FCFA · Scolarité : 250 000 FCFA / an
                </h3>
                <p className="text-xs text-[#C9D1CC] leading-relaxed">
                  Payable en <strong>4 tranches souples</strong> : 100 000 FCFA à la rentrée + 3 tranches de 50 000 FCFA. Cursus intensif de 12 mois avec <strong>70 % de pratique réelle</strong> sur les infrastructures d&apos;EcoPark Cameroun.
                </p>
              </div>
            </div>

            <div className="lg:col-span-7 space-y-3">
              <h3 className="font-['Barlow_Semi_Condensed'] text-2xl font-bold text-[var(--text-primary)]">
                Les 5 Filières Professionnelles de Référence à Yaoundé-Ahala
              </h3>
              <div className="grid grid-cols-1 gap-3">
                {CFP_PROGRAMS.map((prog) => (
                  <div
                    key={prog.num}
                    className="p-4 rounded-xl bg-[var(--bg-surface)] border border-[var(--border-default)] flex items-start gap-4"
                  >
                    <span className="px-3 py-1.5 rounded-lg bg-[var(--brand-primary)] text-white font-mono font-bold text-xs shrink-0">
                      {prog.num}
                    </span>
                    <div>
                      <h4 className="font-['Barlow_Semi_Condensed'] text-base font-bold text-[var(--text-primary)]">
                        {prog.title}
                      </h4>
                      <p className="text-xs text-[var(--text-muted)] mt-0.5 leading-relaxed">
                        {prog.outcome}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Bottom Practical Info Strip */}
      <div className="p-4 sm:p-5 rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-default)] flex flex-wrap items-center justify-between gap-4 text-xs">
        <div className="flex items-center gap-2 text-[var(--text-primary)] font-medium">
          <MapPin className="w-4 h-4 text-[var(--brand-primary)] shrink-0" />
          <span>
            <strong>Accès :</strong> Yaoundé – Ahala Barrière, en face de la station-service Tradex Ahala (RN3, route 100 % goudronnée, parking gratuit).
          </span>
        </div>
        <div className="flex flex-wrap items-center gap-4 font-mono text-[var(--text-muted)]">
          <span className="flex items-center gap-1">
            <Clock className="w-3.5 h-3.5 text-[var(--brand-primary)]" />
            Parc : Mar–Dim 09h–18h · Hôtels 24h/24 · Restaurant 07h–23h
          </span>
          <span className="flex items-center gap-1 text-[var(--brand-primary)] font-bold">
            <ShieldCheck className="w-3.5 h-3.5" />
            WhatsApp : +237 672 56 45 98
          </span>
        </div>
      </div>
    </section>
  );
};
