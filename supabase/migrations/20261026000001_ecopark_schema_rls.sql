-- ============================================================================
-- ECOPARK CAMEROUN (Yaoundé-Ahala) — Schéma PostgreSQL / Supabase & Règles RLS
-- Sprint 1 : Socle de Données, Règles Métier FCFA & Sécurité des 7 Rôles
-- Direction validée : « Canopée vivante — Le cercle du vivant »
-- ============================================================================

CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 1. Énumérations des 7 Rôles, 5 États de Paiement Mobile Money & 7 États de Scan QR
DO $$ BEGIN
  CREATE TYPE ecopark_role AS ENUM (
    'visiteur_anonyme',
    'client_connecte',
    'agent_guichet',
    'agent_controle',
    'responsable_exploitation',
    'direction',
    'administrateur_plateforme'
  );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE payment_status AS ENUM (
    'PENDING',    -- En attente de validation téléphone (#150# / *126#)
    'CONFIRMED',  -- Confirmé par Webhook signé
    'FAILED',     -- Échoué (Solde insuffisant / erreur opérateur)
    'EXPIRED',    -- Expiré (Délai USSD dépassé)
    'CANCELLED'   -- Annulé par l'utilisateur
  );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE qr_scan_verdict AS ENUM (
    'VALID',        -- 1/7 Billet valide
    'USED',         -- 2/7 Déjà utilisé
    'WRONG_DATE',   -- 3/7 Mauvaise date de visite
    'EXPIRED',      -- 4/7 Billet expiré
    'CANCELLED',    -- 5/7 Billet annulé
    'WRONG_ZONE',   -- 6/7 Prestation différente (ex: Piscine non incluse)
    'UNKNOWN'       -- 7/7 Code QR inconnu
  );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

-- ============================================================================
-- 2. Catalogue des Activités & Règles Tarifaires avec Protection Enfant (ADM-01, ADM-02, PUB-10)
-- ============================================================================
CREATE TABLE IF NOT EXISTS public.catalog_activities (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  slug TEXT UNIQUE NOT NULL,
  title TEXT NOT NULL,
  pole TEXT NOT NULL, -- 'NATURE_FAUNE', 'EAU_PLEIN_AIR', 'RESTAURATION', 'HEBERGEMENT', 'GROUPES_B2B', 'FORMATION_CFP'
  description TEXT NOT NULL,
  child_price_fcfa INTEGER NOT NULL CHECK (child_price_fcfa >= 0),
  adult_price_fcfa INTEGER NOT NULL CHECK (adult_price_fcfa >= 0),
  group_adult_price_fcfa INTEGER NOT NULL CHECK (group_adult_price_fcfa >= 0),
  group_child_price_fcfa INTEGER NOT NULL CHECK (group_child_price_fcfa >= 0),
  daily_capacity INTEGER NOT NULL DEFAULT 500,
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  -- GARDE-FOU MÉTIER CRITIQUE (Prompt Maître & ADM-02) :
  -- Le tarif enfant en groupe ne peut JAMAIS dépasser le tarif individuel enfant (500 FCFA pour le Zoo),
  -- interdisant l'application erronée du tarif groupe adulte (700 FCFA) aux enfants.
  CONSTRAINT chk_child_group_price_never_higher_than_individual
    CHECK (group_child_price_fcfa <= child_price_fcfa)
);

-- Données initiales officielles ECOPARK Yaoundé-Ahala (en FCFA)
INSERT INTO public.catalog_activities (slug, title, pole, description, child_price_fcfa, adult_price_fcfa, group_adult_price_fcfa, group_child_price_fcfa, daily_capacity)
VALUES
  ('zoo', 'Entrée Parc & Jardin Zoologique', 'NATURE_FAUNE', 'Observation des chimpanzés, tortues géantes, autruches, paons et allées botaniques.', 500, 1000, 700, 500, 1200),
  ('piscine', 'Piscine Semi-Olympique', 'EAU_PLEIN_AIR', 'Baignade surveillée avec maître-nageur sauveteur.', 1500, 2500, 2000, 1500, 300),
  ('pirogue', 'Balade en Pirogue / Pédalo sur le Lac', 'EAU_PLEIN_AIR', 'Traversée commentée du lac d''Ahala avec gilet de sauvetage fourni.', 500, 1000, 800, 500, 250),
  ('cheval', 'Équitation (Tour à Cheval) & Manèges', 'EAU_PLEIN_AIR', 'Initiation équestre encadrée et manèges enfants.', 500, 1000, 800, 500, 200),
  ('saveurs', 'Repas — Le Château des Saveurs', 'RESTAURATION', 'Gastronomie camerounaise : poisson braisé d''Ahala, poulet DG, Ndolè, plantains mûrs.', 2500, 5000, 4500, 2500, 400)
ON CONFLICT (slug) DO NOTHING;

-- ============================================================================
-- 3. Cités Hôtelières : Ewondo, Chanthel & Bene (PUB-08, PUB-09, EXP-04)
-- ============================================================================
CREATE TABLE IF NOT EXISTS public.lodge_cities (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  code TEXT UNIQUE NOT NULL, -- 'EWONDO', 'CHANTHEL', 'BENE'
  name TEXT NOT NULL,
  category TEXT NOT NULL,
  min_price_fcfa INTEGER NOT NULL CHECK (min_price_fcfa > 0),
  max_price_fcfa INTEGER NOT NULL CHECK (max_price_fcfa >= min_price_fcfa),
  total_rooms INTEGER NOT NULL CHECK (total_rooms > 0),
  available_rooms INTEGER NOT NULL CHECK (available_rooms >= 0 AND available_rooms <= total_rooms),
  amenities TEXT[] NOT NULL DEFAULT '{}'
);

INSERT INTO public.lodge_cities (code, name, category, min_price_fcfa, max_price_fcfa, total_rooms, available_rooms, amenities)
VALUES
  ('EWONDO', 'Cité Ewondo (VIP)', 'Haut Standing Climatisé', 25000, 30000, 8, 2, ARRAY['Climatisation', 'Eau chaude', 'Petit-déjeuner', 'Accès Parc inclus']),
  ('CHANTHEL', 'Cité Chanthel (Confort)', 'Pavillon Nature Confort', 15000, 25000, 12, 3, ARRAY['Ventilation/Clim', 'Salle d''eau privée', 'Calme forestier']),
  ('BENE', 'Cité Bene (Standard)', 'Pavillon Détente', 10000, 15000, 10, 0, ARRAY['Lit double', 'Salle d''eau privée', 'Proximité lac'])
ON CONFLICT (code) DO NOTHING;

-- ============================================================================
-- 4. Réservations & Billets QR (RES-01..12, ACC-02..05, AGT-05..07)
-- ============================================================================
CREATE TABLE IF NOT EXISTS public.bookings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  reference_code TEXT UNIQUE NOT NULL, -- ex: ECP-2026-84920
  visitor_name TEXT NOT NULL,
  visitor_phone TEXT NOT NULL,
  visit_date DATE NOT NULL,
  visit_profile TEXT NOT NULL DEFAULT 'famille',
  adults_count INTEGER NOT NULL DEFAULT 1 CHECK (adults_count >= 0),
  children_count INTEGER NOT NULL DEFAULT 0 CHECK (children_count >= 0),
  toddlers_count INTEGER NOT NULL DEFAULT 0 CHECK (toddlers_count >= 0),
  selected_activities TEXT[] NOT NULL DEFAULT '{}',
  total_fcfa INTEGER NOT NULL CHECK (total_fcfa >= 0),
  payment_method TEXT NOT NULL DEFAULT 'OM', -- 'OM', 'MOMO', 'GUICHET'
  payment_state payment_status NOT NULL DEFAULT 'PENDING',
  qr_status qr_scan_verdict NOT NULL DEFAULT 'VALID',
  scanned_at TIMESTAMPTZ,
  scanned_by TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CONSTRAINT chk_at_least_one_adult_or_child CHECK (adults_count + children_count >= 1)
);

-- ============================================================================
-- 5. Demandes de Devis Groupes, Écoles & Entreprises (RES-06, RES-10, EXP-03)
-- ============================================================================
CREATE TABLE IF NOT EXISTS public.group_quotes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  quote_reference TEXT UNIQUE NOT NULL, -- ex: DEV-2026-3104
  organization_name TEXT NOT NULL,
  contact_name TEXT NOT NULL,
  contact_phone TEXT NOT NULL,
  group_type TEXT NOT NULL, -- 'ecole', 'entreprise', 'mariage_evenement'
  preferred_date DATE NOT NULL,
  participants_count INTEGER NOT NULL CHECK (participants_count >= 10),
  estimated_budget_fcfa INTEGER NOT NULL CHECK (estimated_budget_fcfa >= 0),
  notes TEXT,
  status TEXT NOT NULL DEFAULT 'EN_ETUDE', -- 'EN_ETUDE', 'PROFORMA_ENVOYEE', 'VALIDE', 'ANNULE'
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ============================================================================
-- 6. Candidatures Centre de Formation Professionnelle CFP (PUB-12, EXP-06)
-- ============================================================================
CREATE TABLE IF NOT EXISTS public.cfp_applications (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  application_ref TEXT UNIQUE NOT NULL, -- ex: CFP-2026-0412
  candidate_name TEXT NOT NULL,
  candidate_phone TEXT NOT NULL,
  program_track TEXT NOT NULL, -- 'Aquaculture', 'Hôtellerie-Restauration', 'Agriculture & Élevage'
  registration_fee_fcfa INTEGER NOT NULL DEFAULT 50000 CHECK (registration_fee_fcfa = 50000),
  tuition_fee_fcfa INTEGER NOT NULL DEFAULT 250000 CHECK (tuition_fee_fcfa = 250000),
  status TEXT NOT NULL DEFAULT 'DOSSIER_RECU', -- 'DOSSIER_RECU', 'INSCRIPTION_REGLEE', 'ADMIS'
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ============================================================================
-- 7. Journal d'Audit Immuable (ADM-08)
-- ============================================================================
CREATE TABLE IF NOT EXISTS public.audit_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  actor_name TEXT NOT NULL,
  actor_role ecopark_role NOT NULL,
  action_code TEXT NOT NULL,
  description TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Activation Row Level Security (RLS) sur toutes les tables
ALTER TABLE public.catalog_activities ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.lodge_cities ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.bookings ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.group_quotes ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.cfp_applications ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.audit_logs ENABLE ROW LEVEL SECURITY;

-- Politiques de lecture publique pour le catalogue et les cités hôtelières
CREATE POLICY "Public read active catalog" ON public.catalog_activities
  FOR SELECT USING (is_active = TRUE);

CREATE POLICY "Public read lodge cities" ON public.lodge_cities
  FOR SELECT USING (TRUE);
