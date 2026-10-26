# -*- coding: utf-8 -*-
"""
Implémentation des 3 animations HyperFrames (heygen-com/hyperframes + Apple Motion Design)
sur ECOPARK Cameroun (Yaoundé-Ahala) :
1. Animation 1 — « HyperFrames Scene Reel » sur le Hero (#sec-PUB-01, window.__timelines["ecopark-hero-reel"])
2. Animation 2 — « Staggered Bento Reveal & Tracé Vectoriel SVG du Parc (Zones A -> E) » (#sec-PUB-03 & #sec-PUB-13, window.__timelines["ecopark-ahala-map"])
3. Animation 3 — « Kinetic FCFA Odometer & Apple Wallet QR Pass 3D Reveal » (#sec-RES-03 & #sec-RES-09, window.__timelines["ecopark-qr-pass"])
"""
import pathlib

ROOT = pathlib.Path(r"c:\Users\PcGamerCm\Downloads\ECO-PARK")
TARGETS = [
    ROOT / "etape0-site-live" / "index.html",
    ROOT / "Prototype_Interactif_ECOPARK_NEW_LOOK.html",
]

HYPERFRAMES_CSS = """
    /* ==========================================================================
       HYPERFRAMES MOTION SYSTEM (heygen-com/hyperframes × Apple cubic-bezier)
       Courbe maîtresse : cubic-bezier(0.16, 1, 0.3, 1) • Held Poster Garanti
       ========================================================================== */
    :root {
      --hf-ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
      --hf-reel-duration: 6000ms;
    }

    /* --- ANIMATION 1 : HYPERFRAMES SCENE REEL (HERO 50/50 & KPI SYNC) --- */
    .hero-thumb-btn {
      position: relative;
      overflow: hidden;
    }
    .hero-playhead-bar {
      position: absolute;
      left: 0;
      bottom: 0;
      height: 3px;
      width: 100%;
      background: linear-gradient(90deg, var(--color-accent-ochre), #E59A3E);
      transform: scaleX(0);
      transform-origin: left center;
      opacity: 0;
      pointer-events: none;
    }
    .hero-thumb-btn.active .hero-playhead-bar {
      opacity: 1;
      animation: hfPlayheadProgress var(--hf-reel-duration) linear forwards;
    }
    .hero-showcase-frame.hf-reel-paused .hero-thumb-btn.active .hero-playhead-bar {
      animation-play-state: paused;
    }
    @keyframes hfPlayheadProgress {
      from { transform: scaleX(0); }
      to   { transform: scaleX(1); }
    }

    .hero-scene-caption-pill {
      position: absolute;
      top: 14px;
      left: 14px;
      z-index: 4;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 6px 13px;
      border-radius: 980px;
      background: rgba(20, 34, 17, 0.68);
      color: #FFFFFF;
      backdrop-filter: saturate(180%) blur(16px);
      -webkit-backdrop-filter: saturate(180%) blur(16px);
      border: 1px solid rgba(255, 255, 255, 0.22);
      font-size: 12.5px;
      font-weight: 600;
      pointer-events: none;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.18);
    }
    .hero-scene-caption-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--color-accent-ochre);
      box-shadow: 0 0 0 3px rgba(196, 125, 43, 0.28);
      flex-shrink: 0;
    }

    .hero-kpi-sync-card {
      transition: transform 0.45s var(--hf-ease-out-expo),
                  box-shadow 0.45s var(--hf-ease-out-expo),
                  border-color 0.45s var(--hf-ease-out-expo);
      border: 1.5px solid transparent;
    }
    .hero-kpi-sync-card.kpi-active-sync {
      transform: translate3d(0, -3px, 0);
      border-color: var(--color-accent-ochre) !important;
      box-shadow: 0 12px 26px rgba(196, 125, 43, 0.16) !important;
    }

    /* --- ANIMATION 2 : STAGGERED BENTO REVEAL & TRACÉ SVG PARC AHALA --- */
    .hf-stagger-ready {
      opacity: 0;
      transform: translate3d(0, 24px, 0) scale(0.985);
      will-change: transform, opacity;
    }
    .hf-stagger-visible {
      opacity: 1 !important;
      transform: translate3d(0, 0, 0) scale(1) !important;
      transition: opacity 0.68s var(--hf-ease-out-expo),
                  transform 0.68s var(--hf-ease-out-expo);
    }

    .ahala-map-widget {
      margin-top: 14px;
      padding: 14px 16px;
      border-radius: 20px;
      background: linear-gradient(145deg, #F4F9F0 0%, #EDF4E7 60%, #FBF5EC 100%);
      border: 1px solid rgba(29, 73, 13, 0.14);
      position: relative;
      overflow: hidden;
    }
    .ahala-map-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
      margin-bottom: 10px;
    }
    .ahala-map-svg {
      width: 100%;
      height: 158px;
      display: block;
      border-radius: 14px;
      background: rgba(255, 255, 255, 0.72);
      border: 1px solid rgba(29, 73, 13, 0.08);
    }
    .ahala-node-group {
      cursor: pointer;
      transition: transform 0.3s var(--hf-ease-out-expo);
    }
    .ahala-node-circle {
      transition: r 0.35s var(--hf-ease-out-expo), fill 0.35s ease, stroke 0.35s ease;
    }
    .ahala-node-group.node-active .ahala-node-circle {
      fill: var(--color-accent-ochre) !important;
      stroke: #FFFFFF !important;
    }
    .ahala-node-pulse {
      transform-origin: center;
      opacity: 0;
    }
    .ahala-node-group.node-active .ahala-node-pulse {
      animation: hfNodePulse 1.8s var(--hf-ease-out-expo) infinite;
    }
    @keyframes hfNodePulse {
      0%   { opacity: 0.65; r: 13px; }
      100% { opacity: 0; r: 24px; }
    }
    .ahala-zone-detail-bar {
      margin-top: 10px;
      padding: 9px 12px;
      border-radius: 12px;
      background: #FFFFFF;
      border: 1px solid rgba(196, 125, 43, 0.28);
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
      font-size: 13.5px;
    }

    /* --- ANIMATION 3 : KINETIC FCFA ODOMETER & APPLE WALLET QR PASS 3D --- */
    #grandTotalFCFA,
    #subZoo, #subPiscine, #subPirogue, #subCheval, #subRepas {
      font-variant-numeric: tabular-nums;
      display: inline-block;
      transition: transform 0.35s var(--hf-ease-out-expo), color 0.35s ease;
    }
    #grandTotalFCFA.hf-odometer-bump {
      transform: scale(1.06);
      color: var(--color-accent-ochre-deep) !important;
    }

    #demoTicketCard {
      position: relative;
      overflow: hidden;
      transform-origin: center top;
      will-change: transform, box-shadow;
    }
    .qr-pass-sheen {
      position: absolute;
      top: 0;
      left: 0;
      width: 65%;
      height: 100%;
      background: linear-gradient(
        105deg,
        rgba(255, 255, 255, 0) 0%,
        rgba(251, 245, 236, 0.65) 45%,
        rgba(196, 125, 43, 0.22) 52%,
        rgba(255, 255, 255, 0) 100%
      );
      transform: translateX(-140%) skewX(-18deg);
      pointer-events: none;
      z-index: 3;
      opacity: 0;
    }

    @media (prefers-reduced-motion: reduce) {
      .hero-thumb-btn.active .hero-playhead-bar {
        animation: none !important;
        transform: scaleX(1) !important;
      }
      .hf-stagger-ready {
        opacity: 1 !important;
        transform: none !important;
      }
    }
"""

AHALA_SVG_WIDGET_HTML = """
                <!-- Animation 2 HyperFrames : Tracé Vectoriel Interactif de l'Itinéraire (Zones A → E) -->
                <div class="ahala-map-widget clip" id="ahalaMapContainer" data-composition-id="ecopark-ahala-map" data-start="0" data-duration="2.4" data-track-index="1">
                  <div class="ahala-map-header">
                    <span style="font-size:12.5px;font-weight:700;color:var(--color-brand-deep);letter-spacing:0.03em;text-transform:uppercase;">
                      Parcours Interactif Ahala Barrière (Nationale N°3 → Zones A à E)
                    </span>
                    <button type="button" class="btn btn-secondary btn-sm btn-ochre-outline" style="min-height:30px;padding:4px 12px;font-size:12px;" onclick="replayAhalaMapTimeline()">
                      <svg class="svg-mono" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polygon points="5 3 19 12 5 21 5 3"/></svg> Animer l'itinéraire A → E
                    </button>
                  </div>
                  <svg id="ahalaTrailSvg" class="ahala-map-svg" viewBox="0 0 560 155" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Carte vectorielle interactive des Zones A à E d'ECOPARK Yaoundé-Ahala">
                    <!-- Grille topographique subtile & Rivière/Lac d'Ahala -->
                    <ellipse cx="305" cy="52" rx="64" ry="26" fill="#E3F1EC" stroke="#1D490D" stroke-opacity="0.18" stroke-dasharray="3 3"/>
                    <text x="272" y="48" text-anchor="middle" fill="#1D490D" fill-opacity="0.65" font-size="9.5" font-weight="600">Lac d'Ahala</text>
                    <!-- Tracé de fond pointillé -->
                    <path id="ahalaBasePath" d="M 38 118 C 82 118, 92 78, 128 78 C 168 78, 188 112, 224 112 C 260 112, 272 52, 314 52 C 356 52, 378 106, 418 106 C 458 106, 480 64, 518 64" stroke="#1D490D" stroke-opacity="0.22" stroke-width="3" stroke-dasharray="5 5" stroke-linecap="round"/>
                    <!-- Tracé actif animé par HyperFrames (Ocre Bronze #C47D2B) -->
                    <path id="ahalaActivePath" d="M 38 118 C 82 118, 92 78, 128 78 C 168 78, 188 112, 224 112 C 260 112, 272 52, 314 52 C 356 52, 378 106, 418 106 C 458 106, 480 64, 518 64" stroke="#C47D2B" stroke-width="4" stroke-linecap="round" stroke-dasharray="540" stroke-dashoffset="0"/>

                    <!-- Point de départ : Route Nationale N°3 (Tradex Ahala) -->
                    <g transform="translate(38, 118)" onclick="selectAhalaZone(0)" style="cursor:pointer;">
                      <rect x="-26" y="-12" width="52" height="24" rx="6" fill="#1D490D"/>
                      <text x="0" y="4" text-anchor="middle" fill="#FFFFFF" font-size="9.5" font-weight="700">RN3 Tradex</text>
                    </g>

                    <!-- Zone A : Accueil & Guichet QR -->
                    <g class="ahala-node-group node-active" id="ahalaNode0" transform="translate(128, 78)" onclick="selectAhalaZone(0)">
                      <circle class="ahala-node-pulse" cx="0" cy="0" r="14" fill="none" stroke="#C47D2B" stroke-width="2"/>
                      <circle class="ahala-node-circle" cx="0" cy="0" r="13" fill="#1D490D" stroke="#FFFFFF" stroke-width="2.5"/>
                      <text x="0" y="4" text-anchor="middle" fill="#FFFFFF" font-size="10.5" font-weight="700">A</text>
                      <text x="0" y="-19" text-anchor="middle" fill="#1E281B" font-size="10" font-weight="700">Accueil QR</text>
                    </g>

                    <!-- Zone B : Cœur Vert & Zoo -->
                    <g class="ahala-node-group" id="ahalaNode1" transform="translate(224, 112)" onclick="selectAhalaZone(1)">
                      <circle class="ahala-node-pulse" cx="0" cy="0" r="14" fill="none" stroke="#C47D2B" stroke-width="2"/>
                      <circle class="ahala-node-circle" cx="0" cy="0" r="13" fill="#1D490D" stroke="#FFFFFF" stroke-width="2.5"/>
                      <text x="0" y="4" text-anchor="middle" fill="#FFFFFF" font-size="10.5" font-weight="700">B</text>
                      <text x="0" y="27" text-anchor="middle" fill="#1E281B" font-size="10" font-weight="700">Parc &amp; Zoo</text>
                    </g>

                    <!-- Zone C : Lac & Équitation -->
                    <g class="ahala-node-group" id="ahalaNode2" transform="translate(314, 52)" onclick="selectAhalaZone(2)">
                      <circle class="ahala-node-pulse" cx="0" cy="0" r="14" fill="none" stroke="#C47D2B" stroke-width="2"/>
                      <circle class="ahala-node-circle" cx="0" cy="0" r="13" fill="#1D490D" stroke="#FFFFFF" stroke-width="2.5"/>
                      <text x="0" y="4" text-anchor="middle" fill="#FFFFFF" font-size="10.5" font-weight="700">C</text>
                      <text x="0" y="-19" text-anchor="middle" fill="#1E281B" font-size="10" font-weight="700">Pirogue &amp; Cheval</text>
                    </g>

                    <!-- Zone D : Piscine & Château des Saveurs -->
                    <g class="ahala-node-group" id="ahalaNode3" transform="translate(418, 106)" onclick="selectAhalaZone(3)">
                      <circle class="ahala-node-pulse" cx="0" cy="0" r="14" fill="none" stroke="#C47D2B" stroke-width="2"/>
                      <circle class="ahala-node-circle" cx="0" cy="0" r="13" fill="#1D490D" stroke="#FFFFFF" stroke-width="2.5"/>
                      <text x="0" y="4" text-anchor="middle" fill="#FFFFFF" font-size="10.5" font-weight="700">D</text>
                      <text x="0" y="27" text-anchor="middle" fill="#1E281B" font-size="10" font-weight="700">Piscine &amp; Saveurs</text>
                    </g>

                    <!-- Zone E : Loges & CFP -->
                    <g class="ahala-node-group" id="ahalaNode4" transform="translate(518, 64)" onclick="selectAhalaZone(4)">
                      <circle class="ahala-node-pulse" cx="0" cy="0" r="14" fill="none" stroke="#C47D2B" stroke-width="2"/>
                      <circle class="ahala-node-circle" cx="0" cy="0" r="13" fill="#1D490D" stroke="#FFFFFF" stroke-width="2.5"/>
                      <text x="0" y="4" text-anchor="middle" fill="#FFFFFF" font-size="10.5" font-weight="700">E</text>
                      <text x="0" y="-19" text-anchor="middle" fill="#1E281B" font-size="10" font-weight="700">Loges &amp; CFP</text>
                    </g>
                  </svg>
                  <div class="ahala-zone-detail-bar" id="ahalaZoneDetailBar">
                    <div id="ahalaZoneDetailText">
                      <strong>Zone A → E (Itinéraire Complet) :</strong> Accès direct depuis la Nationale N°3 (après station Tradex Ahala), parking gratuit 150 places.
                    </div>
                    <span class="price-pill" id="ahalaZoneDetailPrice">Entrée 500 / 1 000 FCFA</span>
                  </div>
                </div>
"""

HYPERFRAMES_JS = """
    // ========================================================================
    // MOTEUR D'ANIMATIONS HYPERFRAMES (heygen-com/hyperframes × Apple Motion)
    // Registre officiel : window.__timelines
    //   1. "ecopark-hero-reel" (Hero 50/50 Scene Reel + Playhead Ocre + Sync KPI)
    //   2. "ecopark-ahala-map" (Staggered Bento Reveal + Tracé SVG Zones A -> E)
    //   3. "ecopark-qr-pass"   (Kinetic FCFA Odometer + Apple Wallet QR Pass 3D)
    // ========================================================================
    window.__timelines = window.__timelines || {};

    const HERO_REEL_META = [
      { kpiIdx: 0, label: 'Scène 1/4 • Lac & Pirogues', price: '500 / 1 000 FCFA' },
      { kpiIdx: 1, label: 'Scène 2/4 • Piscine Semi-Olympique', price: '1 500 / 2 500 FCFA' },
      { kpiIdx: 2, label: 'Scène 3/4 • Château des Saveurs & Loges', price: '3 500 – 30 000 FCFA' },
      { kpiIdx: 0, label: 'Scène 4/4 • Canopée & Sortie Famille', price: 'Gratuit < 3 ans' }
    ];

    function syncHeroKpiAndCaption(idx) {
      const meta = HERO_REEL_META[idx] || HERO_REEL_META[0];
      const capText = document.getElementById('heroSceneCaptionText');
      if (capText) {
        capText.textContent = `${meta.label} — ${meta.price}`;
      }
      const capPill = document.getElementById('heroSceneCaptionPill');
      if (capPill && capPill.animate) {
        capPill.animate([
          { opacity: 0.4, transform: 'translate3d(0, 8px, 0)' },
          { opacity: 1, transform: 'translate3d(0, 0, 0)' }
        ], { duration: 480, easing: 'cubic-bezier(0.16, 1, 0.3, 1)', fill: 'forwards' });
      }
      [0, 1, 2].forEach(i => {
        const card = document.getElementById('heroKpiCard' + i);
        if (card) card.classList.toggle('kpi-active-sync', i === meta.kpiIdx);
      });
    }

    // Surcharge enrichie de setHeroShowcase avec transition optique HyperFrames
    setHeroShowcase = function(idx, btnEl) {
      const buttons = Array.from(document.querySelectorAll('.hero-thumb-btn'));
      const safeIdx = ((idx % 4) + 4) % 4;
      window._currentHeroSlideIdx = safeIdx;
      const item = ECOPARK_GALLERY_ITEMS[safeIdx] || ECOPARK_GALLERY_ITEMS[0];
      const img = document.getElementById('heroShowcaseImg');
      if (img) {
        img.src = item.src;
        img.alt = item.title;
        if (img.animate && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
          img.animate([
            { transform: 'scale(1.06)', opacity: 0.76 },
            { transform: 'scale(1)', opacity: 1 }
          ], { duration: 750, easing: 'cubic-bezier(0.16, 1, 0.3, 1)', fill: 'forwards' });
        }
      }
      buttons.forEach((b, i) => {
        b.classList.remove('active');
        // Force reflow pour relancer la barre de progression Ocre Bronze
        if (i === safeIdx || b === btnEl) {
          void b.offsetWidth;
          b.classList.add('active');
        }
      });
      syncHeroKpiAndCaption(safeIdx);
      resetHeroReelInterval();
    };

    window._heroReelPaused = false;
    function resetHeroReelInterval() {
      clearInterval(window._heroReelTimer);
      if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
      window._heroReelTimer = setInterval(() => {
        if (window._heroReelPaused) return;
        const lb = document.getElementById('ecoparkLightbox');
        if (lb && lb.classList.contains('open')) return;
        const nextIdx = ((window._currentHeroSlideIdx || 0) + 1) % 4;
        const btns = document.querySelectorAll('.hero-thumb-btn');
        setHeroShowcase(nextIdx, btns[nextIdx]);
      }, 6000);
    }

    (function initHeroReelTimeline() {
      const frame = document.getElementById('heroShowcaseFrame');
      if (frame) {
        frame.addEventListener('mouseenter', () => {
          window._heroReelPaused = true;
          frame.classList.add('hf-reel-paused');
        });
        frame.addEventListener('mouseleave', () => {
          window._heroReelPaused = false;
          frame.classList.remove('hf-reel-paused');
        });
      }
      syncHeroKpiAndCaption(0);
      resetHeroReelInterval();

      window.__timelines['ecopark-hero-reel'] = {
        id: 'ecopark-hero-reel',
        duration: 24,
        fps: 60,
        tracks: 3,
        play() {
          window._heroReelPaused = false;
          if (frame) frame.classList.remove('hf-reel-paused');
          resetHeroReelInterval();
        },
        pause() {
          window._heroReelPaused = true;
          if (frame) frame.classList.add('hf-reel-paused');
        },
        seek(seconds) {
          const idx = Math.floor((seconds || 0) / 6) % 4;
          const btns = document.querySelectorAll('.hero-thumb-btn');
          setHeroShowcase(idx, btns[idx]);
        }
      };
    })();

    // --- ANIMATION 2 : STAGGERED BENTO REVEAL & TRACÉ VECTORIEL SVG AHALA ---
    const AHALA_ZONES_INFO = [
      {
        title: 'Zone A — Entrée, Parking 150 places & Guichets QR',
        desc: 'Accès direct depuis la Nationale N°3 (Ahala Barrière, après Tradex). Contrôle rapide des billets électroniques QR.',
        price: 'Parking Gratuit'
      },
      {
        title: 'Zone B — Cœur Vert : Jardin Zoologique & Allées Botaniques',
        desc: 'Observation des primates (chimpanzés, singes), tortues géantes, paons, autruches et antilopes sous la canopée.',
        price: '500 / 1 000 FCFA'
      },
      {
        title: "Zone C — Lac Naturel d'Ahala, Pirogues & Équitation",
        desc: 'Embarcadère sécurisé avec gilets de sauvetage fournis, traversée en pirogue/pédalo et carrière équestre.',
        price: '500 / 1 000 FCFA'
      },
      {
        title: 'Zone D — Piscine Semi-Olympique & Le Château des Saveurs',
        desc: 'Baignade surveillée par maître-nageur (1 500 / 2 500 FCFA) et gastronomie camerounaise (poisson braisé, poulet DG).',
        price: '1 500 – 8 500 FCFA'
      },
      {
        title: 'Zone E — Cités Hôtelières (Bene, Chanthel, Ewondo) & Campus CFP',
        desc: 'Pavillons de séjour au calme (10 000 à 30 000 FCFA) et Centre de Formation Professionnelle agréé MINEFOP.',
        price: '10 000 – 30 000 FCFA'
      }
    ];

    function selectAhalaZone(zoneIdx) {
      const z = AHALA_ZONES_INFO[zoneIdx] || AHALA_ZONES_INFO[0];
      for (let i = 0; i < 5; i++) {
        const node = document.getElementById('ahalaNode' + i);
        if (node) node.classList.toggle('node-active', i <= zoneIdx);
      }
      const txtEl = document.getElementById('ahalaZoneDetailText');
      const priceEl = document.getElementById('ahalaZoneDetailPrice');
      if (txtEl) txtEl.innerHTML = `<strong>${z.title} :</strong> ${z.desc}`;
      if (priceEl) priceEl.textContent = z.price;
    }

    function replayAhalaMapTimeline() {
      const activePath = document.getElementById('ahalaActivePath');
      if (activePath && activePath.animate) {
        activePath.animate([
          { strokeDashoffset: 540 },
          { strokeDashoffset: 0 }
        ], { duration: 1650, easing: 'cubic-bezier(0.16, 1, 0.3, 1)', fill: 'forwards' });
      }
      for (let i = 0; i < 5; i++) {
        const node = document.getElementById('ahalaNode' + i);
        if (node) node.classList.remove('node-active');
        setTimeout(() => {
          if (node) node.classList.add('node-active');
          if (i === 4) {
            const txtEl = document.getElementById('ahalaZoneDetailText');
            const priceEl = document.getElementById('ahalaZoneDetailPrice');
            if (txtEl) txtEl.innerHTML = '<strong>Zone A → E (Itinéraire Complet) :</strong> Accès direct Nationale N°3 (après station Tradex Ahala), 5 pôles connectés.';
            if (priceEl) priceEl.textContent = 'Entrée 500 / 1 000 FCFA';
          } else {
            selectAhalaZone(i);
          }
        }, i * 260 + 120);
      }
    }

    (function initBentoAndMapTimelines() {
      window.__timelines['ecopark-ahala-map'] = {
        id: 'ecopark-ahala-map',
        duration: 2.4,
        fps: 60,
        tracks: 2,
        play: replayAhalaMapTimeline,
        seek(t) {
          const activePath = document.getElementById('ahalaActivePath');
          if (activePath) {
            const progress = Math.max(0, Math.min(1, (t || 0) / 2.4));
            activePath.style.strokeDashoffset = String(Math.round(540 * (1 - progress)));
          }
        }
      };

      const cards = Array.from(document.querySelectorAll('#sec-PUB-03 .bento-card, #sec-PUB-14 .gallery-mosaic-item'));
      if ('IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        cards.forEach((c, idx) => {
          c.classList.add('clip', 'hf-stagger-ready');
          c.setAttribute('data-start', ((idx % 6) * 0.08).toFixed(2));
          c.setAttribute('data-duration', '0.68');
          c.setAttribute('data-track-index', String((idx % 3) + 1));
        });
        const io = new IntersectionObserver((entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              const el = entry.target;
              const delayMs = Math.round(parseFloat(el.getAttribute('data-start') || '0') * 1000);
              setTimeout(() => {
                el.classList.add('hf-stagger-visible');
              }, delayMs);
              io.unobserve(el);
            }
          });
        }, { threshold: 0.08 });
        cards.forEach(c => io.observe(c));

        const mapBox = document.getElementById('ahalaMapContainer');
        if (mapBox) {
          const mapIo = new IntersectionObserver((entries) => {
            entries.forEach(e => {
              if (e.isIntersecting) {
                replayAhalaMapTimeline();
                mapIo.unobserve(e.target);
              }
            });
          }, { threshold: 0.25 });
          mapIo.observe(mapBox);
        }
      } else {
        cards.forEach(c => c.classList.add('hf-stagger-visible'));
      }
    })();

    // --- ANIMATION 3 : KINETIC FCFA ODOMETER & APPLE WALLET QR PASS 3D REVEAL ---
    window._lastGrandTotalValue = 14000;
    function animateFcfaOdometer(el, fromVal, toVal) {
      if (!el) return;
      // Toujours définir immédiatement la valeur cible exacte dans data-target-fcfa et textContent final
      el.setAttribute('data-target-fcfa', String(toVal));
      if (fromVal === toVal || window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        el.textContent = formatFCFA(toVal);
        return;
      }
      el.classList.add('hf-odometer-bump');
      clearTimeout(window._odometerBumpTimer);
      window._odometerBumpTimer = setTimeout(() => el.classList.remove('hf-odometer-bump'), 360);

      const startTime = performance.now();
      const duration = 340;
      if (window._odometerRafId) cancelAnimationFrame(window._odometerRafId);

      function tick(now) {
        const elapsed = now - startTime;
        const t = Math.min(1, elapsed / duration);
        // Courbe Apple cubic-bezier(0.16, 1, 0.3, 1) approximée par easeOutExpo
        const eased = t === 1 ? 1 : 1 - Math.pow(2, -10 * t);
        const current = Math.round((fromVal + (toVal - fromVal) * eased) / 50) * 50;
        el.textContent = formatFCFA(t >= 1 ? toVal : current);
        if (t < 1) {
          window._odometerRafId = requestAnimationFrame(tick);
        } else {
          el.textContent = formatFCFA(toVal);
        }
      }
      // On met immédiatement la valeur cible exacte pour garantir la lecture synchrone, puis on anime visuellement si visible
      el.textContent = formatFCFA(toVal);
      if (el.animate) {
        el.animate([
          { transform: 'translateY(5px) scale(1.05)', opacity: 0.72 },
          { transform: 'translateY(0) scale(1)', opacity: 1 }
        ], { duration: 380, easing: 'cubic-bezier(0.16, 1, 0.3, 1)', fill: 'forwards' });
      }
    }

    const _origRecalcSimulatorForHf = recalcSimulator;
    recalcSimulator = function() {
      const prevTotal = window._lastGrandTotalValue || 14000;
      _origRecalcSimulatorForHf();
      const grandEl = document.getElementById('grandTotalFCFA');
      if (grandEl) {
        const newTotal = parseInt((grandEl.textContent || '').replace(/[^0-9]/g, ''), 10) || 0;
        window._lastGrandTotalValue = newTotal;
        animateFcfaOdometer(grandEl, prevTotal, newTotal);
      }
    };

    function triggerQrPass3DReveal() {
      const card = document.getElementById('demoTicketCard');
      const sheen = document.getElementById('qrPassSheen');
      if (card && card.animate && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        card.animate([
          { transform: 'perspective(900px) rotateX(9deg) translateY(10px) scale(0.965)', boxShadow: '0 8px 20px rgba(29, 73, 13, 0.08)' },
          { transform: 'perspective(900px) rotateX(-1.5deg) translateY(-2px) scale(1.01)', boxShadow: '0 26px 58px rgba(196, 125, 43, 0.24)', offset: 0.65 },
          { transform: 'none', boxShadow: '0 14px 34px rgba(29, 73, 13, 0.10)' }
        ], { duration: 780, easing: 'cubic-bezier(0.16, 1, 0.3, 1)', fill: 'forwards' });
      }
      if (sheen && sheen.animate && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        sheen.animate([
          { transform: 'translateX(-140%) skewX(-18deg)', opacity: 0 },
          { opacity: 0.95, offset: 0.2 },
          { transform: 'translateX(220%) skewX(-18deg)', opacity: 0 }
        ], { duration: 1050, easing: 'cubic-bezier(0.16, 1, 0.3, 1)', fill: 'forwards' });
      }
    }

    const _origCreateLiveBookingForHf = createLiveBookingSprint1;
    createLiveBookingSprint1 = function() {
      _origCreateLiveBookingForHf();
      triggerQrPass3DReveal();
    };

    window.__timelines['ecopark-qr-pass'] = {
      id: 'ecopark-qr-pass',
      duration: 1.05,
      fps: 60,
      tracks: 2,
      play: triggerQrPass3DReveal,
      seek() {}
    };
"""


def apply_hyperframes(path: pathlib.Path):
    html = path.read_text(encoding="utf-8")

    # 1. Inject CSS before </style> if not already present
    if "HYPERFRAMES MOTION SYSTEM" not in html:
        html = html.replace("  </style>", HYPERFRAMES_CSS + "\n  </style>", 1)

    # 2. Add IDs and hero-kpi-sync-card classes to the 3 Hero KPI cards
    old_kpi_block = """                <div class="grid-12" style="gap:12px;">
                  <div class="col-4 card" style="padding:14px;background:var(--color-surface-soft);">
                    <strong style="color:var(--color-brand-deep);font-family:var(--font-heading);font-size:1.25rem;">500 / 1 000 FCFA</strong>
                    <span style="font-size:14px;">Entrée Parc & Zoo (Enfant / Adulte)</span>
                  </div>
                  <div class="col-4 card" style="padding:14px;background:var(--color-surface-soft);">
                    <strong style="color:var(--color-brand-deep);font-family:var(--font-heading);font-size:1.25rem;">1 500 / 2 500 FCFA</strong>
                    <span style="font-size:14px;">Piscine semi-olympique (Enfant / Adulte)</span>
                  </div>
                  <div class="col-4 card kpi-card-hospitality" style="padding:14px;">
                    <strong style="font-family:var(--font-heading);font-size:1.25rem;">10 000 – 30 000 FCFA</strong>
                    <span style="font-size:14px;">Séjour Loges Bene, Chanthel & Ewondo</span>
                  </div>
                </div>"""
    new_kpi_block = """                <div class="grid-12" style="gap:12px;">
                  <div class="col-4 card hero-kpi-sync-card kpi-active-sync" id="heroKpiCard0" style="padding:14px;background:var(--color-surface-soft);">
                    <strong style="color:var(--color-brand-deep);font-family:var(--font-heading);font-size:1.25rem;">500 / 1 000 FCFA</strong>
                    <span style="font-size:14px;">Entrée Parc & Zoo (Enfant / Adulte)</span>
                  </div>
                  <div class="col-4 card hero-kpi-sync-card" id="heroKpiCard1" style="padding:14px;background:var(--color-surface-soft);">
                    <strong style="color:var(--color-brand-deep);font-family:var(--font-heading);font-size:1.25rem;">1 500 / 2 500 FCFA</strong>
                    <span style="font-size:14px;">Piscine semi-olympique (Enfant / Adulte)</span>
                  </div>
                  <div class="col-4 card kpi-card-hospitality hero-kpi-sync-card" id="heroKpiCard2" style="padding:14px;">
                    <strong style="font-family:var(--font-heading);font-size:1.25rem;">10 000 – 30 000 FCFA</strong>
                    <span style="font-size:14px;">Séjour Loges Bene, Chanthel & Ewondo</span>
                  </div>
                </div>"""
    if old_kpi_block in html:
        html = html.replace(old_kpi_block, new_kpi_block, 1)

    # 3. Enrich #heroShowcaseFrame with HyperFrames composition attributes, caption pill & playhead bars
    old_hero_frame = """                <div class="hero-showcase-frame" id="heroShowcaseFrame" onclick="openEcoparkLightbox(window._currentHeroSlideIdx || 0)">
                  <span class="photo-zoom-pill"><svg class="svg-mono" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="8"/><line x1="21" x2="16.65" y1="21" y2="16.65"/><line x1="11" x2="11" y1="8" y2="14"/><line x1="8" x2="14" y1="11" y2="11"/></svg> Plein écran HD</span>
                  <img id="heroShowcaseImg" src="audit-assets/ecopark-real-media/balade_pirogue3.jpg" alt="Balade en pirogue sur le lac verdoyant d'ECOPARK à Yaoundé-Ahala" />
                  <div class="hero-switcher-bar" onclick="event.stopPropagation();">
                    <button type="button" class="hero-thumb-btn active" onclick="setHeroShowcase(0, this)">
                      <img src="audit-assets/ecopark-real-media/balade_pirogue3.jpg" alt="Lac & Pirogues" />
                      <span>Lac & Pirogues</span>
                    </button>
                    <button type="button" class="hero-thumb-btn" onclick="setHeroShowcase(1, this)">
                      <img src="audit-assets/stitch-canopee-vivante/local_cameroon_pool_pirogue.png" alt="Piscine & Détente" />
                      <span>Piscine & Eau</span>
                    </button>
                    <button type="button" class="hero-thumb-btn" onclick="setHeroShowcase(2, this)">
                      <img src="audit-assets/stitch-canopee-vivante/local_cameroon_gastronomy_pergola.png" alt="Château des Saveurs" />
                      <span>Saveurs & Loges</span>
                    </button>
                    <button type="button" class="hero-thumb-btn" onclick="setHeroShowcase(3, this)">
                      <img src="audit-assets/stitch-canopee-vivante/local_cameroon_family_canopy.png" alt="Canopée & Famille" />
                      <span>Canopée & Parc</span>
                    </button>
                  </div>
                </div>"""
    new_hero_frame = """                <div class="hero-showcase-frame clip" id="heroShowcaseFrame" data-composition-id="ecopark-hero-reel" data-start="0" data-duration="24" data-track-index="1" onclick="openEcoparkLightbox(window._currentHeroSlideIdx || 0)">
                  <span class="hero-scene-caption-pill clip" id="heroSceneCaptionPill" data-start="0" data-duration="6" data-track-index="2">
                    <span class="hero-scene-caption-dot"></span>
                    <span id="heroSceneCaptionText">Scène 1/4 • Lac &amp; Pirogues — 500 / 1 000 FCFA</span>
                  </span>
                  <span class="photo-zoom-pill"><svg class="svg-mono" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="8"/><line x1="21" x2="16.65" y1="21" y2="16.65"/><line x1="11" x2="11" y1="8" y2="14"/><line x1="8" x2="14" y1="11" y2="11"/></svg> Plein écran HD</span>
                  <img id="heroShowcaseImg" src="audit-assets/ecopark-real-media/balade_pirogue3.jpg" alt="Balade en pirogue sur le lac verdoyant d'ECOPARK à Yaoundé-Ahala" />
                  <div class="hero-switcher-bar" onclick="event.stopPropagation();">
                    <button type="button" class="hero-thumb-btn clip active" data-start="0" data-duration="6" data-track-index="1" onclick="setHeroShowcase(0, this)">
                      <img src="audit-assets/ecopark-real-media/balade_pirogue3.jpg" alt="Lac & Pirogues" />
                      <span>Lac & Pirogues</span>
                      <span class="hero-playhead-bar"></span>
                    </button>
                    <button type="button" class="hero-thumb-btn clip" data-start="6" data-duration="6" data-track-index="1" onclick="setHeroShowcase(1, this)">
                      <img src="audit-assets/stitch-canopee-vivante/local_cameroon_pool_pirogue.png" alt="Piscine & Détente" />
                      <span>Piscine & Eau</span>
                      <span class="hero-playhead-bar"></span>
                    </button>
                    <button type="button" class="hero-thumb-btn clip" data-start="12" data-duration="6" data-track-index="1" onclick="setHeroShowcase(2, this)">
                      <img src="audit-assets/stitch-canopee-vivante/local_cameroon_gastronomy_pergola.png" alt="Château des Saveurs" />
                      <span>Saveurs & Loges</span>
                      <span class="hero-playhead-bar"></span>
                    </button>
                    <button type="button" class="hero-thumb-btn clip" data-start="18" data-duration="6" data-track-index="1" onclick="setHeroShowcase(3, this)">
                      <img src="audit-assets/stitch-canopee-vivante/local_cameroon_family_canopy.png" alt="Canopée & Famille" />
                      <span>Canopée & Parc</span>
                      <span class="hero-playhead-bar"></span>
                    </button>
                  </div>
                </div>"""
    if old_hero_frame in html:
        html = html.replace(old_hero_frame, new_hero_frame, 1)

    # 4. Inject Interactive SVG Park Map into #sec-PUB-13 Orientation card
    target_orientation_end = """                  <li><strong>Zone E (Séjour & Formation)</strong> : Loges Ewondo, Chanthel, Bene et campus du CFP ECOPARK.</li>
                </ul>"""
    if "ahalaTrailSvg" not in html and target_orientation_end in html:
        html = html.replace(target_orientation_end, target_orientation_end + "\n" + AHALA_SVG_WIDGET_HTML, 1)

    # 5. Add HyperFrames attributes & sheen overlay to #demoTicketCard
    old_ticket_open = '<div class="card" id="demoTicketCard">'
    new_ticket_open = '<div class="card clip" id="demoTicketCard" data-composition-id="ecopark-qr-pass" data-start="0" data-duration="1.05" data-track-index="1">\n                  <div class="qr-pass-sheen" id="qrPassSheen"></div>'
    if old_ticket_open in html and "qrPassSheen" not in html:
        html = html.replace(old_ticket_open, new_ticket_open, 1)

    # 6. Inject HyperFrames JS engine before </script>
    if "window.__timelines" not in html:
        html = html.replace("  </script>", HYPERFRAMES_JS + "\n  </script>", 1)

    path.write_text(html, encoding="utf-8")
    print(f"Updated {path} ({len(html.splitlines())} lines)")


if __name__ == "__main__":
    for p in TARGETS:
        apply_hyperframes(p)
