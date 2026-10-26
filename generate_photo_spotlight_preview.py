# -*- coding: utf-8 -*-
"""
Générateur de la version « Mise en Exergue Photographique Apple-Grade × Grand Resort » :
1. Hero 50/50 (.col-6 / .col-6) avec Vitrine Photo HD de 450px + Sélecteur interactif de 4 ambiances en Liquid Glass
2. Bento Grid des 6 Univers avec fenêtres photo agrandies à 340px (+31%), zoom optique au survol et badge d'agrandissement
3. Galerie PUB-14 transformée en Mosaïque Cinéma Pleine Largeur (410px + 230px) sans boutons techniques 404/Maintenance en mode visiteur
4. Lightbox Plein Écran « Liquid Glass » interactive au clic sur n'importe quelle photo avec navigation ←/→, pilule de tarif Ocre Bronze et CTA direct
"""

import pathlib
import re
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(r"c:\Users\PcGamerCm\Downloads\ECO-PARK")
SRC_HTML = ROOT / "etape0-site-live" / "index.html"
PHOTO_HTML = ROOT / "Preview_Mise_En_Exergue_Photos_ECOPARK.html"
ARTIFACT_DIR = pathlib.Path(r"C:\Users\PcGamerCm\.gemini\antigravity\brain\a7ec3e06-7022-4aad-b64e-501927169ab1")
LOCAL_QA_DIR = ROOT / "audit-assets" / "qa-etape0-live"

PHOTO_SPOTLIGHT_CSS = """
    /* ==========================================================================
       MISE EN EXERGUE PHOTOGRAPHIQUE (HERO 50/50, BENTO 340PX, MOSAÏQUE & LIGHTBOX)
       ========================================================================== */

    /* 1. Vitrine Hero 50/50 (.col-6 / .col-6) de 455px avec sélecteur d'ambiances Liquid Glass */
    .hero-showcase-frame {
      position: relative;
      height: 455px !important;
      border-radius: 30px !important;
      overflow: hidden;
      box-shadow: 0 28px 68px rgba(29, 73, 13, 0.16) !important;
      background: var(--color-surface-soft);
      cursor: zoom-in;
    }
    .hero-showcase-frame > img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      object-position: center 30%;
      transition: transform 0.65s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.25s ease;
    }
    .hero-showcase-frame:hover > img {
      transform: scale(1.035);
    }
    .hero-switcher-bar {
      position: absolute;
      left: 16px;
      right: 16px;
      bottom: 16px;
      padding: 8px 10px;
      border-radius: 20px;
      background: rgba(20, 34, 17, 0.68);
      backdrop-filter: saturate(180%) blur(18px);
      -webkit-backdrop-filter: saturate(180%) blur(18px);
      border: 1px solid rgba(255, 255, 255, 0.18);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      z-index: 4;
    }
    .hero-thumb-btn {
      flex: 1;
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 6px 8px;
      border-radius: 13px;
      border: 1px solid transparent;
      background: transparent;
      color: rgba(255, 255, 255, 0.82);
      font-size: 12.5px;
      font-weight: 600;
      cursor: pointer;
      text-align: left;
      transition: all 0.2s ease;
    }
    .hero-thumb-btn img {
      width: 34px;
      height: 34px;
      border-radius: 8px;
      object-fit: cover;
      flex-shrink: 0;
      border: 1px solid rgba(255, 255, 255, 0.28);
    }
    .hero-thumb-btn:hover,
    .hero-thumb-btn.active {
      background: rgba(255, 255, 255, 0.18);
      color: #FFFFFF;
      border-color: rgba(196, 125, 43, 0.75);
    }

    /* 2. Fenêtres d'Immersion Bento Grid portées de 260px à 340px (+31%) + Zoom Optique */
    .bento-card .card-media-wrapper,
    .bento-card.bento-wide .card-media-wrapper {
      height: 340px !important;
      position: relative;
      overflow: hidden;
      cursor: zoom-in;
    }
    .bento-card .card-media-wrapper img,
    .gallery-mosaic-item img {
      transition: transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .bento-card:hover .card-media-wrapper img,
    .gallery-mosaic-item:hover img {
      transform: scale(1.05);
    }

    /* Bouton flottant loupe "Agrandir" en coin supérieur droit des photos */
    .photo-zoom-pill {
      position: absolute;
      top: 14px;
      right: 14px;
      z-index: 3;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 6px 12px;
      border-radius: 980px;
      background: rgba(20, 34, 17, 0.62);
      color: #FFFFFF;
      backdrop-filter: saturate(180%) blur(14px);
      -webkit-backdrop-filter: saturate(180%) blur(14px);
      border: 1px solid rgba(255, 255, 255, 0.22);
      font-size: 12.5px;
      font-weight: 600;
      pointer-events: none;
      transition: background 0.2s ease, transform 0.2s ease;
    }
    .bento-card:hover .photo-zoom-pill,
    .gallery-mosaic-item:hover .photo-zoom-pill,
    .hero-showcase-frame:hover .photo-zoom-pill {
      background: rgba(29, 73, 13, 0.90);
      transform: scale(1.04);
    }

    /* 3. Mosaïque Photographique Cinéma pour la Galerie PUB-14 */
    .gallery-mosaic-item {
      position: relative;
      border-radius: 22px;
      overflow: hidden;
      background: var(--color-surface-soft);
      cursor: zoom-in;
      box-shadow: 0 12px 32px rgba(29, 73, 13, 0.08);
    }
    .gallery-mosaic-item.mosaic-tall {
      height: 410px;
    }
    .gallery-mosaic-item.mosaic-pano {
      height: 235px;
    }
    .gallery-mosaic-item img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }
    .gallery-caption-bar {
      position: absolute;
      left: 0;
      right: 0;
      bottom: 0;
      padding: 28px 20px 16px;
      background: linear-gradient(to top, rgba(16, 28, 13, 0.86) 0%, rgba(16, 28, 13, 0.35) 65%, transparent 100%);
      color: #FFFFFF;
      display: flex;
      align-items: flex-end;
      justify-content: space-between;
      gap: 12px;
    }
    .gallery-caption-bar strong {
      display: block;
      font-family: var(--font-heading);
      font-size: 1.2rem;
      font-weight: 600;
      color: #FFFFFF;
    }
    .gallery-caption-bar span {
      font-size: 13.5px;
      color: rgba(255, 255, 255, 0.84);
    }

    /* 4. Lightbox Plein Écran « Liquid Glass » */
    .ecopark-lightbox-overlay {
      display: none;
      position: fixed;
      inset: 0;
      z-index: 4000;
      background: rgba(14, 24, 12, 0.88);
      backdrop-filter: saturate(180%) blur(24px);
      -webkit-backdrop-filter: saturate(180%) blur(24px);
      align-items: center;
      justify-content: center;
      padding: 28px;
    }
    .ecopark-lightbox-overlay.open {
      display: flex;
    }
    .ecopark-lightbox-modal {
      max-width: 1140px;
      width: 100%;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }
    .ecopark-lightbox-top {
      display: flex;
      align-items: center;
      justify-content: space-between;
      color: #FFFFFF;
    }
    .ecopark-lightbox-stage {
      position: relative;
      width: 100%;
      height: 70vh;
      max-height: 680px;
      border-radius: 26px;
      overflow: hidden;
      background: #0D170B;
      box-shadow: 0 32px 80px rgba(0, 0, 0, 0.48);
      border: 1px solid rgba(255, 255, 255, 0.14);
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .ecopark-lightbox-stage img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }
    .lightbox-nav-btn {
      position: absolute;
      top: 50%;
      transform: translateY(-50%);
      width: 48px;
      height: 48px;
      border-radius: 50%;
      border: 1px solid rgba(255, 255, 255, 0.25);
      background: rgba(20, 34, 17, 0.72);
      color: #FFFFFF;
      backdrop-filter: blur(12px);
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: all 0.2s ease;
    }
    .lightbox-nav-btn:hover {
      background: var(--color-brand-deep);
      border-color: var(--color-accent-ochre);
    }
    .lightbox-nav-prev { left: 18px; }
    .lightbox-nav-next { right: 18px; }
    .ecopark-lightbox-footer {
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 16px;
      padding: 16px 24px;
      border-radius: 20px;
      background: rgba(255, 255, 255, 0.96);
      color: var(--color-text);
    }
"""

ZOOM_ICON_SVG = '<svg class="svg-mono" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="8"/><line x1="21" x2="16.65" y1="21" y2="16.65"/><line x1="11" x2="11" y1="8" y2="14"/><line x1="8" x2="14" y1="11" y2="11"/></svg>'

HERO_NEW_RIGHT_COL = f"""              <div class="col-6">
                <div class="hero-showcase-frame" id="heroShowcaseFrame" onclick="openEcoparkLightbox(window._currentHeroSlideIdx || 0)">
                  <span class="photo-zoom-pill">{ZOOM_ICON_SVG} Plein écran HD</span>
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
                </div>
              </div>"""

GALLERY_MOSAIC_NEW = f"""              <!-- Galerie Photographique Immersive Pleine Largeur (PUB-14) -->
              <div class="col-12 card" id="sec-PUB-14">
                <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;">
                  <div>
                    <span class="eyebrow eyebrow-hospitality" style="margin-bottom:4px;">Immersion Visuelle Haute Définition</span>
                    <h3><span class="icon-medallion"><svg class="svg-mono" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"/><circle cx="12" cy="13" r="3"/></svg></span> <span class="tech-code-tag">PUB-14 à PUB-22 — </span>L'Expérience ECOPARK Yaoundé-Ahala en Grand Format</h3>
                  </div>
                  <div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center;">
                    <button type="button" class="btn btn-secondary btn-sm btn-ochre-outline" onclick="openEcoparkLightbox(1)">{ZOOM_ICON_SVG} Ouvrir la Visionneuse Plein Écran (10 Photos)</button>
                    <div class="tech-code-tag" style="display:inline-flex;gap:6px;flex-wrap:wrap;">
                      <button class="btn btn-secondary btn-sm" onclick="inspectScreen('PUB-14')">PUB-14 Galerie</button>
                      <button class="btn btn-secondary btn-sm" onclick="inspectScreen('PUB-15')">PUB-15/16 Actualités</button>
                      <button class="btn btn-secondary btn-sm" onclick="inspectScreen('PUB-18')">PUB-18 Contact</button>
                      <button class="btn btn-secondary btn-sm" onclick="inspectScreen('PUB-20')">PUB-20 Mentions légales</button>
                      <button class="btn btn-secondary btn-sm" onclick="inspectScreen('PUB-21')">PUB-21 Page 404</button>
                      <button class="btn btn-secondary btn-sm" onclick="inspectScreen('PUB-22')">PUB-22 Maintenance</button>
                    </div>
                  </div>
                </div>

                <div class="grid-12" style="margin-top:12px;gap:20px;">
                  <!-- Photo Maîtresse 1 (Col-7, 410px) -->
                  <div class="col-7 gallery-mosaic-item mosaic-tall" onclick="openEcoparkLightbox(1)">
                    <span class="photo-zoom-pill">{ZOOM_ICON_SVG} Agrandir en HD</span>
                    <img src="audit-assets/stitch-canopee-vivante/local_cameroon_pool_pirogue.png" alt="Vue panoramique Piscine Semi-Olympique et Lac d'Ahala" />
                    <div class="gallery-caption-bar">
                      <div>
                        <strong>Piscine Semi-Olympique & Plan d'Eau d'Ahala</strong>
                        <span>Baignade surveillée et loisirs nautiques au cœur de la palmeraie</span>
                      </div>
                      <span class="price-pill">1 500 / 2 500 FCFA</span>
                    </div>
                  </div>

                  <!-- Photo Maîtresse 2 (Col-5, 410px, Photo Réelle ECOPARK) -->
                  <div class="col-5 gallery-mosaic-item mosaic-tall" onclick="openEcoparkLightbox(4)">
                    <span class="photo-zoom-pill">{ZOOM_ICON_SVG} Agrandir en HD</span>
                    <img src="audit-assets/ecopark-real-media/IMG-20260809-WA0009.jpg" alt="Accueil jeunesse et événements en plein air devant la fresque d'ECOPARK" />
                    <div class="gallery-caption-bar">
                      <div>
                        <strong>Esplanade Plein Air & Sorties Jeunesse</strong>
                        <span>Accueil des écoles, colonies et événements devant la fresque d'Ahala</span>
                      </div>
                      <span class="price-pill">Dès 20 pers.</span>
                    </div>
                  </div>

                  <!-- Ligne Panoramique (4 x Col-3, 235px) -->
                  <div class="col-3 gallery-mosaic-item mosaic-pano" onclick="openEcoparkLightbox(0)">
                    <span class="photo-zoom-pill">{ZOOM_ICON_SVG} Zoom</span>
                    <img src="audit-assets/ecopark-real-media/balade_pirogue3.jpg" alt="Balade en pirogue sur le lac d'Ahala" />
                    <div class="gallery-caption-bar" style="padding:16px 14px 12px;">
                      <div>
                        <strong style="font-size:1.02rem;">Lac & Balade en Pirogue</strong>
                        <span style="font-size:12px;">500 / 1 000 FCFA • Gilet fourni</span>
                      </div>
                    </div>
                  </div>

                  <div class="col-3 gallery-mosaic-item mosaic-pano" onclick="openEcoparkLightbox(2)">
                    <span class="photo-zoom-pill">{ZOOM_ICON_SVG} Zoom</span>
                    <img src="audit-assets/stitch-canopee-vivante/local_cameroon_gastronomy_pergola.png" alt="Restaurant Le Château des Saveurs" />
                    <div class="gallery-caption-bar" style="padding:16px 14px 12px;">
                      <div>
                        <strong style="font-size:1.02rem;">Le Château des Saveurs</strong>
                        <span style="font-size:12px;">Poisson braisé & Poulet DG</span>
                      </div>
                    </div>
                  </div>

                  <div class="col-3 gallery-mosaic-item mosaic-pano" onclick="openEcoparkLightbox(3)">
                    <span class="photo-zoom-pill">{ZOOM_ICON_SVG} Zoom</span>
                    <img src="audit-assets/stitch-canopee-vivante/local_cameroon_family_canopy.png" alt="Sortie familiale à ECOPARK Yaoundé" />
                    <div class="gallery-caption-bar" style="padding:16px 14px 12px;">
                      <div>
                        <strong style="font-size:1.02rem;">Allées Botaniques & Famille</strong>
                        <span style="font-size:12px;">Gratuit moins de 3 ans</span>
                      </div>
                    </div>
                  </div>

                  <div class="col-3 gallery-mosaic-item mosaic-pano" onclick="openEcoparkLightbox(5)">
                    <span class="photo-zoom-pill">{ZOOM_ICON_SVG} Zoom</span>
                    <img src="audit-assets/ecopark-real-media/IMG-20260713-WA0051_043420.jpg" alt="Équipe technique Zoo et Cuisine ECOPARK" />
                    <div class="gallery-caption-bar" style="padding:16px 14px 12px;">
                      <div>
                        <strong style="font-size:1.02rem;">Équipes Zoo & Biosécurité</strong>
                        <span style="font-size:12px;">Encadrement professionnel</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>"""

LIGHTBOX_MODAL_HTML = f"""
  <!-- ========================================================================
       LIGHTBOX PLEIN ÉCRAN « LIQUID GLASS » (VISIONNEUSE HAUTE DÉFINITION)
       ======================================================================== -->
  <div id="ecoparkLightbox" class="ecopark-lightbox-overlay" onclick="closeEcoparkLightbox(event)">
    <div class="ecopark-lightbox-modal" onclick="event.stopPropagation()">
      <div class="ecopark-lightbox-top">
        <div style="display:flex;align-items:center;gap:12px;">
          <span class="price-pill" id="lightboxCounter">Photo 1 / 10</span>
          <span style="font-size:14px;color:rgba(255,255,255,0.80);">ECOPARK CAMEROUN • Yaoundé-Ahala</span>
        </div>
        <button type="button" class="btn btn-secondary btn-sm" onclick="closeEcoparkLightbox()">Fermer (Échap)</button>
      </div>
      <div class="ecopark-lightbox-stage">
        <button type="button" class="lightbox-nav-btn lightbox-nav-prev" onclick="stepEcoparkLightbox(-1)" aria-label="Photo précédente">
          <svg class="svg-mono" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m15 18-6-6 6-6"/></svg>
        </button>
        <img id="lightboxMainImg" src="audit-assets/ecopark-real-media/IMG_20260829_172016-1-scaled.jpg" alt="Aperçu grand format ECOPARK" />
        <button type="button" class="lightbox-nav-btn lightbox-nav-next" onclick="stepEcoparkLightbox(1)" aria-label="Photo suivante">
          <svg class="svg-mono" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg>
        </button>
      </div>
      <div class="ecopark-lightbox-footer">
        <div>
          <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px;">
            <strong id="lightboxTitle" style="font-family:var(--font-heading);font-size:1.35rem;color:var(--color-brand-deep);">Allées Botaniques & Palmeraie d'Ahala</strong>
            <span class="price-pill" id="lightboxPrice">500 / 1 000 FCFA</span>
          </div>
          <p id="lightboxDesc" style="font-size:14.5px;color:var(--color-text-muted);margin:0;">
            Promenade au cœur du complexe agro-écotouristique d'ECOPARK à Yaoundé-Ahala (Nationale N°3).
          </p>
        </div>
        <div style="display:flex;gap:10px;">
          <button type="button" class="btn btn-primary btn-sm" onclick="closeEcoparkLightbox(); navigateFamily('RES', 'RES-03');">Simuler mon budget & Réserver</button>
        </div>
      </div>
    </div>
  </div>
"""

LIGHTBOX_JS = """
    // ========================================================================
    // VITRINE HERO INTERACTIVE & LIGHTBOX PLEIN ÉCRAN « LIQUID GLASS »
    // ========================================================================
    window._currentHeroSlideIdx = 0;
    const ECOPARK_GALLERY_ITEMS = [
      {
        src: 'audit-assets/ecopark-real-media/balade_pirogue3.jpg',
        title: 'Balade en Pirogue sur le Lac d\\'Ahala',
        price: '500 / 1 000 FCFA',
        desc: 'Traversée paisible sur le plan d\\'eau naturel d\\'ECOPARK avec gilet de sauvetage fourni.'
      },
      {
        src: 'audit-assets/stitch-canopee-vivante/local_cameroon_pool_pirogue.png',
        title: 'Piscine Semi-Olympique & Loisirs Nautiques',
        price: '1 500 / 2 500 FCFA',
        desc: 'Baignade surveillée par maître-nageur pour enfants et adultes au cœur de la palmeraie.'
      },
      {
        src: 'audit-assets/stitch-canopee-vivante/local_cameroon_gastronomy_pergola.png',
        title: 'Le Château des Saveurs — Gastronomie Camerounaise',
        price: 'Plats 3 500 – 8 500 FCFA',
        desc: 'Poisson d\\'eau douce braisé d\\'Ahala, poulet DG, Ndolè et jus naturels.'
      },
      {
        src: 'audit-assets/stitch-canopee-vivante/local_cameroon_family_canopy.png',
        title: 'Allées Botaniques & Sortie Familiale sous la Canopée',
        price: 'Gratuit < 3 ans',
        desc: 'Aires de détente sécurisées pour les familles à 15 minutes du centre de Yaoundé.'
      },
      {
        src: 'audit-assets/ecopark-real-media/IMG-20260809-WA0009.jpg',
        title: 'Esplanade Plein Air & Accueil Jeunesse / Écoles',
        price: 'Devis Groupe dès 20 pers.',
        desc: 'Accueil des excursions scolaires et événements en plein air devant la fresque d\\'ECOPARK.'
      },
      {
        src: 'audit-assets/ecopark-real-media/IMG-20260713-WA0051_043420.jpg',
        title: 'Équipes Techniques Zoo, Cuisine & Biosécurité',
        price: 'Encadrement professionnel',
        desc: 'Équipes permanentes dédiées à l\\'entretien zoologique, sanitaire et hôtelier du parc.'
      },
      {
        src: 'audit-assets/stitch-canopee-vivante/local_cameroon_cfp_students.png',
        title: 'Campus & Travaux Pratiques CFP ECOPARK',
        price: '50 000 + 250 000 FCFA',
        desc: 'Centre de Formation Professionnelle agréé MINEFOP (Aquaculture, Hôtellerie, Agropastoral).'
      },
      {
        src: 'audit-assets/ecopark-real-media/chimpanze.jpeg',
        title: 'Jardin Zoologique & Observation de la Faune',
        price: '500 / 1 000 FCFA',
        desc: 'Découverte pédagogique des primates, tortues géantes, paons et antilopes.'
      },
      {
        src: 'audit-assets/ecopark-real-media/chambre.jpeg',
        title: 'Cités Hôtelières : Ewondo, Chanthel & Bene',
        price: '10 000 – 30 000 FCFA',
        desc: 'Hébergement calme en pleine nature (repos en journée ou nuitée complète).'
      },
      {
        src: 'audit-assets/stitch-canopee-vivante/local_cameroon_school_excursion.png',
        title: 'Excursions Scolaires & Sorties Pédagogiques',
        price: 'Tarif enfant protégé 500 FCFA',
        desc: 'Accueil dédié des écoles maternelles, primaires et secondaires dès 20 élèves.'
      }
    ];

    function setHeroShowcase(idx, btnEl) {
      window._currentHeroSlideIdx = idx;
      const item = ECOPARK_GALLERY_ITEMS[idx] || ECOPARK_GALLERY_ITEMS[0];
      const img = document.getElementById('heroShowcaseImg');
      if (img) {
        img.src = item.src;
        img.alt = item.title;
      }
      document.querySelectorAll('.hero-thumb-btn').forEach(b => b.classList.remove('active'));
      if (btnEl) btnEl.classList.add('active');
    }

    window._lightboxIdx = 0;
    function openEcoparkLightbox(idx) {
      window._lightboxIdx = (idx + ECOPARK_GALLERY_ITEMS.length) % ECOPARK_GALLERY_ITEMS.length;
      const item = ECOPARK_GALLERY_ITEMS[window._lightboxIdx];
      document.getElementById('lightboxMainImg').src = item.src;
      document.getElementById('lightboxTitle').textContent = item.title;
      document.getElementById('lightboxPrice').textContent = item.price;
      document.getElementById('lightboxDesc').textContent = item.desc;
      document.getElementById('lightboxCounter').textContent = `Photo ${window._lightboxIdx + 1} / ${ECOPARK_GALLERY_ITEMS.length}`;
      document.getElementById('ecoparkLightbox').classList.add('open');
    }

    function stepEcoparkLightbox(delta) {
      openEcoparkLightbox(window._lightboxIdx + delta);
    }

    function closeEcoparkLightbox(ev) {
      if (ev && ev.target && ev.target.id !== 'ecoparkLightbox') return;
      document.getElementById('ecoparkLightbox').classList.remove('open');
    }

    document.addEventListener('keydown', function(e) {
      const lb = document.getElementById('ecoparkLightbox');
      if (!lb || !lb.classList.contains('open')) return;
      if (e.key === 'Escape') closeEcoparkLightbox();
      if (e.key === 'ArrowRight') stepEcoparkLightbox(1);
      if (e.key === 'ArrowLeft') stepEcoparkLightbox(-1);
    });
"""

def build_and_capture():
    html = SRC_HTML.read_text(encoding="utf-8")

    # 1. Injecter le CSS de mise en exergue photographique
    if "MISE EN EXERGUE PHOTOGRAPHIQUE" not in html:
        html = html.replace("</style>", PHOTO_SPOTLIGHT_CSS + "\n  </style>", 1)

    # 2. Rééquilibrer le Hero (#sec-PUB-01) en 50/50 (.col-6 / .col-6) avec la vitrine interactive HD
    html = html.replace(
        '<div class="grid-12" style="align-items:center;">\n              <div class="col-7">',
        '<div class="grid-12" style="align-items:center;">\n              <div class="col-6">',
        1
    )
    old_hero_right_pattern = re.compile(
        r'<div class="col-5">\s*<div class="leaf-photo-frame"[\s\S]*?</div>\s*</div>',
        re.MULTILINE
    )
    html, n_hero = old_hero_right_pattern.subn(HERO_NEW_RIGHT_COL, html, count=1)
    assert n_hero == 1, "Colonne photo du Hero introuvable"

    # 3. Ajouter les badges loupe et le clic Lightbox sur les 6 cartes Bento (#sec-PUB-03)
    bento_lightbox_map = [
        ('src="audit-assets/ecopark-real-media/chimpanze.jpeg"', 7),
        ('src="audit-assets/stitch-canopee-vivante/local_cameroon_pool_pirogue.png"', 2),
        ('src="audit-assets/stitch-canopee-vivante/local_cameroon_gastronomy_pergola.png"', 3),
        ('src="audit-assets/ecopark-real-media/chambre.jpeg"', 8),
        ('src="audit-assets/stitch-canopee-vivante/local_cameroon_school_excursion.png"', 9),
        ('src="audit-assets/ecopark-real-media/1786968889976.jpg"', 6),
    ]
    for img_attr, lb_idx in bento_lightbox_map:
        html = html.replace(
            f'<div class="card-media-wrapper">\n                  <img {img_attr}',
            f'<div class="card-media-wrapper" onclick="openEcoparkLightbox({lb_idx})">\n                  <span class="photo-zoom-pill">{ZOOM_ICON_SVG} Agrandir</span>\n                  <img {img_attr}',
            1
        )

    # 4. Remplacer la petite galerie col-3 par la Mosaïque Photographique Cinéma (PUB-14)
    old_gallery_pattern = re.compile(
        r'<!-- Aperçu des écrans PUB-14, PUB-15/16, PUB-18, PUB-20, PUB-21, PUB-22 -->\s*<div class="col-12 card">[\s\S]*?</div>\s*</div>\s*</div>\s*</div>\s*</div>\s*</section>',
        re.MULTILINE
    )
    new_gallery_tail = GALLERY_MOSAIC_NEW + "\n            </div>\n          </div>\n        </div>\n      </section>"
    html, n_gal = old_gallery_pattern.subn(new_gallery_tail, html, count=1)
    assert n_gal == 1, "Section Galerie PUB-14 introuvable"

    # 5. Injecter la modale Lightbox et ses fonctions JS
    html = html.replace(
        '<!-- ========================================================================\n       MODALES TRANSACTIONNELLES SPRINT 1',
        LIGHTBOX_MODAL_HTML + '\n  <!-- ========================================================================\n       MODALES TRANSACTIONNELLES SPRINT 1',
        1
    )
    html = html.replace("</script>", LIGHTBOX_JS + "\n  </script>", 1)

    PHOTO_HTML.write_text(html, encoding="utf-8")
    print(f"[OK] Preview Mise en Exergue Photos ecrite : {PHOTO_HTML}")

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    LOCAL_QA_DIR.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 940})
        page.goto(PHOTO_HTML.as_uri(), wait_until="networkidle")
        page.wait_for_timeout(400)

        # Capture 1 : Hero 50/50 (.col-6 / .col-6) avec Vitrine Photo Ultra-HD de 455px et Sélecteur 4 vues en Liquid Glass
        s1 = ARTIFACT_DIR / "photo_validation_1_hero_50_50_selecteur_hd.png"
        page.screenshot(path=str(s1), full_page=False)
        (LOCAL_QA_DIR / s1.name).write_bytes(s1.read_bytes())

        # Capture 2 : Bento Grid avec fenêtres photo portées de 260px à 340px (+31%) et pilules d'agrandissement
        page.evaluate("window.scrollTo(0, document.getElementById('sec-PUB-03').offsetTop - 75);")
        page.wait_for_timeout(350)
        s2 = ARTIFACT_DIR / "photo_validation_2_bento_340px_loupe.png"
        page.screenshot(path=str(s2), full_page=False)
        (LOCAL_QA_DIR / s2.name).write_bytes(s2.read_bytes())

        # Capture 3 : Nouvelle Galerie PUB-14 en Mosaïque Cinéma Pleine Largeur (410px + 235px)
        page.evaluate("window.scrollTo(0, document.getElementById('sec-PUB-14').getBoundingClientRect().top + window.scrollY - 75);")
        page.wait_for_timeout(350)
        s3 = ARTIFACT_DIR / "photo_validation_3_galerie_mosaique_cinema_hd.png"
        page.screenshot(path=str(s3), full_page=False)
        (LOCAL_QA_DIR / s3.name).write_bytes(s3.read_bytes())

        # Capture 4 : Visionneuse Lightbox Plein Écran « Liquid Glass » ouverte sur Piscine & Lac
        page.evaluate("openEcoparkLightbox(1);")
        page.wait_for_timeout(350)
        s4 = ARTIFACT_DIR / "photo_validation_4_lightbox_liquid_glass_ouverte.png"
        page.screenshot(path=str(s4), full_page=False)
        (LOCAL_QA_DIR / s4.name).write_bytes(s4.read_bytes())

        browser.close()
    print("[OK] 4 captures de validation Mise en Exergue Photos generees avec succes.")

if __name__ == "__main__":
    build_and_capture()
