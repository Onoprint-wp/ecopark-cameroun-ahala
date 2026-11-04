-- ============================================================================
-- ECOPARK Cameroun — Synchronisation Officielle Novembre 2026
-- Date : 2026-11-04
-- Aligne la base sur les mises à jour réelles du site ecopark-yaounde.com
-- ============================================================================

-- 1. CATALOGUE DES ACTIVITÉS : Nouveautés, Totem et Ajustements Tarifaires
-- ----------------------------------------------------------------------------

-- A. Totem Services (sécurisation SQL idempotente)
INSERT INTO public.catalog_activities (
  id, slug, sku, title, pole, description,
  child_price_fcfa, adult_price_fcfa, group_adult_price_fcfa, group_child_price_fcfa,
  daily_capacity, is_active, status, sort_order, image_src, image_alt
) VALUES
  ('a1100001-0000-4000-8000-000000000001', 'musee', 'CAT-MUSEE', 'Musée Culturel & Patrimoine du Cameroun', 'CULTURE_EDUCATION',
   'Exposition permanente d''objets d''art traditionnel, chefferies, biodiversité d''Ahala et histoire culturelle du Cameroun.',
   500, 1000, 500, 500, 300, TRUE, 'PUBLISHED', 85,
   'audit-assets/ecopark-real-media/totem-services-ecopark.png', 'Musée Culturel et Patrimoine ECOPARK Ahala'),
  ('a1100002-0000-4000-8000-000000000002', 'bibliotheque', 'CAT-BIBLIOTHEQUE', 'Bibliothèque & Espace Lecture Jeunesse', 'CULTURE_EDUCATION',
   'Salle de lecture calme, contes africains, ouvrages scolaires et fonds documentaire agro-pastoral & hôtelier du CFP.',
   500, 1000, 500, 500, 150, TRUE, 'PUBLISHED', 90,
   'audit-assets/stitch-canopee-vivante/local_cameroon_cfp_students.png', 'Bibliothèque et espace lecture ECOPARK'),
  ('a1100003-0000-4000-8000-000000000003', 'aire_jeux', 'CAT-AIRE-JEUX', 'Aire de Jeux Enfants, Toboggans & Manèges', 'FAMILLE_ENFANCE',
   'Parc de jeux sécurisé en plein air pour les enfants : toboggans, balançoires, parcours ludiques et manèges sous la canopée.',
   500, 500, 500, 500, 350, TRUE, 'PUBLISHED', 95,
   'audit-assets/stitch-canopee-vivante/local_cameroon_family_canopy.png', 'Aire de jeux enfants à ECOPARK Ahala'),
  ('a1100004-0000-4000-8000-000000000004', 'creche_garderie', 'CAT-CRECHE-GARDERIE', 'Crèche-Garderie & Halte-Garderie Sécurisée', 'FAMILLE_ENFANCE',
   'Accueil encadré des tout-petits et enfants par des éducatrices qualifiées pendant vos séminaires, mariages ou moments détente.',
   1500, 1500, 1000, 500, 80, TRUE, 'PUBLISHED', 100,
   'audit-assets/stitch-canopee-vivante/local_cameroon_family_canopy.png', 'Crèche-garderie sécurisée ECOPARK Ahala')
ON CONFLICT (slug) DO UPDATE SET
  group_adult_price_fcfa = EXCLUDED.group_adult_price_fcfa,
  adult_price_fcfa = EXCLUDED.adult_price_fcfa;

-- B. Nouvelles activités officielles : Balade en forêt (200 ha) et Location Canne à Pêche
INSERT INTO public.catalog_activities (
  id, slug, sku, title, pole, description,
  child_price_fcfa, adult_price_fcfa, group_adult_price_fcfa, group_child_price_fcfa,
  daily_capacity, is_active, status, sort_order, image_src, image_alt
) VALUES
  ('a1100006-0000-4000-8000-000000000006', 'balade_foret', 'CAT-BALADE-FORET', 'Balade en forêt (> 200 ha)', 'NATURE_FAUNE',
   'Parcours pédestre guidé d''environ 40 min au cœur du massif forestier et des collines préservées d''Ahala.',
   500, 1000, 700, 500, 300, TRUE, 'PUBLISHED', 15,
   'audit-assets/ecopark-real-media/IMG_20260829_172016-1-scaled.jpg', 'Balade en forêt guidée sous la canopée d''Ahala'),
  ('a1100007-0000-4000-8000-000000000007', 'peche_canne', 'CAT-PECHE-CANNE', 'Location Canne à Pêche — Étangs d''Ahala', 'EAU_PLEIN_AIR',
   'Mise à disposition d''une canne à pêche avec ligne et appâts pour pêcher dans les étangs piscicoles d''Ahala.',
   2000, 2000, 2000, 2000, 100, TRUE, 'PUBLISHED', 25,
   'audit-assets/stitch-canopee-vivante/local_cameroon_freshwater_pond.png', 'Location canne à pêche aux étangs d''Ahala')
ON CONFLICT (slug) DO UPDATE SET
  child_price_fcfa = EXCLUDED.child_price_fcfa,
  adult_price_fcfa = EXCLUDED.adult_price_fcfa,
  group_adult_price_fcfa = EXCLUDED.group_adult_price_fcfa,
  group_child_price_fcfa = EXCLUDED.group_child_price_fcfa,
  status = 'PUBLISHED';

-- C. Ajustements des tarifs groupes et adultes sur les activités existantes
UPDATE public.catalog_activities SET
  adult_price_fcfa = 1000,
  group_adult_price_fcfa = 500
WHERE slug = 'bibliotheque';

UPDATE public.catalog_activities SET
  group_adult_price_fcfa = 500
WHERE slug = 'musee';

UPDATE public.catalog_activities SET
  group_adult_price_fcfa = 700
WHERE slug IN ('pirogue', 'cheval');


-- 2. HÔTELLERIE (LODGE_CITIES) : 3 HÔTELS / 30 UNITÉS MAX 30 000 FCFA
-- ----------------------------------------------------------------------------

-- A. Autoriser SUITES_PRIVEES dans la contrainte des réservations
ALTER TABLE public.bookings DROP CONSTRAINT IF EXISTS chk_bookings_lodge_city;
ALTER TABLE public.bookings ADD CONSTRAINT chk_bookings_lodge_city
  CHECK (lodge_city IS NULL OR lodge_city IN ('EWONDO', 'CHANTHEL', 'BENE', 'SUITES_PRIVEES'));

-- B. Mettre à jour les 3 cités hôtelières existantes
UPDATE public.lodge_cities SET
  name = 'Hôtel Bene (Standard)',
  category = 'Pavillon Standard',
  min_price_fcfa = 10000,
  max_price_fcfa = 15000,
  total_rooms = 10,
  available_rooms = LEAST(available_rooms, 10),
  amenities = ARRAY['Lit double confort', 'Salle d''eau privée', 'Proximité étangs & nature', 'Véranda réceptions à l''étage']
WHERE code = 'BENE';

UPDATE public.lodge_cities SET
  name = 'Hôtel Chanthel (Confort)',
  category = 'Pavillon Nature Confort',
  min_price_fcfa = 15000,
  max_price_fcfa = 25000,
  total_rooms = 12,
  available_rooms = LEAST(available_rooms, 12),
  amenities = ARRAY['Ventilation / Climatisation', 'Salle d''eau privée', 'Calme forestier', 'Chambres 15 000 / 20 000 / 25 000 FCFA'],
  image_src = 'audit-assets/ecopark-real-media/hotel-chanthel.jpeg',
  image_alt = 'Hôtel Chanthel à ECOPARK Ahala'
WHERE code = 'CHANTHEL';

UPDATE public.lodge_cities SET
  name = 'Hôtel Ewondo — Mini-Suites VIP',
  category = 'Mini-Suites Haut Standing Climatisées',
  min_price_fcfa = 25000,
  max_price_fcfa = 30000,
  total_rooms = 4,
  available_rooms = LEAST(available_rooms, 4),
  amenities = ARRAY['Climatisation', 'Eau chaude', 'Petit-déjeuner inclus', 'Accès Parc inclus', 'Mini-Suites 25 000 à 30 000 FCFA']
WHERE code = 'EWONDO';

-- C. Cité SUITES_PRIVEES (4e code pour compatibilité simulateur & suites de tests)
INSERT INTO public.lodge_cities (
  id, code, sku, name, category,
  min_price_fcfa, max_price_fcfa, total_rooms, available_rooms,
  amenities, status, sort_order, image_src, image_alt
) VALUES (
  'a1100005-0000-4000-8000-000000000005', 'SUITES_PRIVEES', 'LOD-SUITES-PRIVEES',
  'Hôtel Ewondo — Suites Privées Élégantes', 'Suites Privées Haut Standing',
  30000, 30000, 4, 2,
  ARRAY['Salon privé climatisé', 'Literie King-Size', 'Service en suite Château des Saveurs', 'Accès coupe-file Piscine & Zoo', 'Tarif unique 30 000 FCFA'],
  'PUBLISHED', 40,
  'audit-assets/ecopark-real-media/chambre.jpeg', 'Suites Privées Élégantes Hôtel Ewondo ECOPARK Ahala'
)
ON CONFLICT (code) DO UPDATE SET
  name = EXCLUDED.name,
  min_price_fcfa = EXCLUDED.min_price_fcfa,
  max_price_fcfa = EXCLUDED.max_price_fcfa,
  total_rooms = EXCLUDED.total_rooms,
  available_rooms = EXCLUDED.available_rooms,
  amenities = EXCLUDED.amenities;


-- 3. RESTAURATION (MENU_ITEMS) : 3 ESPACES DÈS 3 500 FCFA
-- ----------------------------------------------------------------------------

-- A. Renseigner les prix des 4 plats signature historiques
UPDATE public.menu_items SET price_fcfa = 5000,
  image_src = 'audit-assets/ecopark-real-media/restaurant-vip-new-look.jpg.png',
  image_alt = 'Poisson Braisé d''Ahala au Restaurant VIP New Look'
WHERE sku = 'MNU-POISSON-BRAISE';

UPDATE public.menu_items SET price_fcfa = 6500,
  image_src = 'audit-assets/ecopark-real-media/Le-Chateau-des-Saveurs.jpeg',
  image_alt = 'Poulet DG Royal au Château des Saveurs'
WHERE sku = 'MNU-POULET-DG';

UPDATE public.menu_items SET price_fcfa = 5500,
  image_src = 'audit-assets/ecopark-real-media/restaurant-vip1.jpg',
  image_alt = 'Ndolé Royal au Restaurant VIP'
WHERE sku = 'MNU-NDOLE-ROYAL';

UPDATE public.menu_items SET price_fcfa = 2500
WHERE sku = 'MNU-MENU-ENFANT';

-- B. Ajouter l'Assiette du Jour à 3 500 FCFA (Boukarous / Restaurant VIP)
INSERT INTO public.menu_items (
  sku, category, name, description, price_fcfa,
  is_signature, in_stock, preorder_enabled, image_src, image_alt, status, sort_order
) VALUES (
  'MNU-ASSIETTE-JOUR', 'GRILLADE',
  'Grillades & Assiette du Jour — Boukarous / Restaurant VIP',
  'Sélection du jour braisée au feu de bois (viandes savoureuses ou poisson) servie avec garniture au choix dans les Boukarous ombragés ou au Restaurant VIP New Look.',
  3500, FALSE, TRUE, TRUE,
  'audit-assets/ecopark-real-media/boucarous.jpg', 'Assiette du Jour et Grillades aux Boukarous ECOPARK Ahala',
  'PUBLISHED', 25
)
ON CONFLICT (sku) DO UPDATE SET
  name = EXCLUDED.name,
  price_fcfa = EXCLUDED.price_fcfa,
  description = EXCLUDED.description,
  image_src = EXCLUDED.image_src;
