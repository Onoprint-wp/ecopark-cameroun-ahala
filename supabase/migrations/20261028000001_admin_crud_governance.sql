-- ============================================================================
-- ECOPARK CAMEROUN (Yaoundé-Ahala) — Migration 2 : Gouvernance CRUD de l'Administration
-- Phase 1 du plan d'implémentation (ADM-01 à ADM-08)
--
--  1. Corrections du schéma Sprint 1 (CHECK lodge_city, colonne client)
--  2. Cycle de vie commun : DRAFT / PUBLISHED / ARCHIVED + verrou optimiste (version)
--  3. Nouvelles tables : agenda_events, menu_items, daily_quotas, site_settings,
--     staff_profiles, gateway_health
--  4. Rôles : current_ecopark_role(), ecopark_has_role() (MFA aal2 pour Direction/Admin)
--  5. Journal d'audit immuable chaîné SHA-256 + trigger générique audit_row_change()
--  6. Règles de gouvernance tarifaire (seule la Direction publie / modifie un prix publié)
--  7. RPC : admin_duplicate, admin_set_status, admin_delete, get_availability,
--     log_admin_event, verify_audit_chain, get_my_profile
--  8. Politiques RLS complètes (8 tables Sprint 1 + 6 nouvelles tables)
--  9. Données initiales (agenda, carte, réglages, passerelles) reprises du site live
--
-- Hypothèse : base Supabase (schéma auth, rôles anon / authenticated / service_role).
-- ============================================================================

-- ============================================================================
-- 1. CORRECTIONS DU SCHÉMA SPRINT 1
-- ============================================================================

-- La colonne lodge_city était déclarée deux fois : le CHECK de la migration 1
-- (ADD COLUMN IF NOT EXISTS ... CHECK) n'a donc jamais été appliqué.
DO $$ BEGIN
  ALTER TABLE public.bookings
    ADD CONSTRAINT chk_bookings_lodge_city
    CHECK (lodge_city IS NULL OR lodge_city IN ('EWONDO', 'CHANTHEL', 'BENE'));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

-- Rattachement optionnel d'une réservation à un compte client (ACC — Mon Espace)
ALTER TABLE public.bookings
  ADD COLUMN IF NOT EXISTS customer_user_id UUID REFERENCES auth.users(id) ON DELETE SET NULL;

-- ============================================================================
-- 2. CYCLE DE VIE COMMUN DES CONTENUS ADMINISTRABLES
-- ============================================================================
DO $$ BEGIN
  CREATE TYPE content_status AS ENUM ('DRAFT', 'PUBLISHED', 'ARCHIVED');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

-- 2.1 Catalogue des activités (ADM-01 / ADM-02)
ALTER TABLE public.catalog_activities
  ADD COLUMN IF NOT EXISTS sku TEXT,
  ADD COLUMN IF NOT EXISTS status content_status NOT NULL DEFAULT 'PUBLISHED',
  ADD COLUMN IF NOT EXISTS sort_order INTEGER NOT NULL DEFAULT 0,
  ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  ADD COLUMN IF NOT EXISTS updated_by UUID,
  ADD COLUMN IF NOT EXISTS version INTEGER NOT NULL DEFAULT 1,
  ADD COLUMN IF NOT EXISTS duplicated_from UUID REFERENCES public.catalog_activities(id) ON DELETE SET NULL,
  ADD COLUMN IF NOT EXISTS first_published_at TIMESTAMPTZ;

UPDATE public.catalog_activities
   SET sku = 'CAT-' || upper(replace(slug, '_', '-'))
 WHERE sku IS NULL;
UPDATE public.catalog_activities
   SET status = CASE WHEN is_active THEN 'PUBLISHED'::content_status ELSE 'ARCHIVED'::content_status END,
       first_published_at = COALESCE(first_published_at, created_at);
UPDATE public.catalog_activities c
   SET sort_order = s.rn * 10
  FROM (SELECT id, row_number() OVER (ORDER BY created_at, slug) AS rn FROM public.catalog_activities) s
 WHERE s.id = c.id AND c.sort_order = 0;
ALTER TABLE public.catalog_activities ALTER COLUMN sku SET NOT NULL;
DO $$ BEGIN
  ALTER TABLE public.catalog_activities ADD CONSTRAINT uq_catalog_activities_sku UNIQUE (sku);
EXCEPTION WHEN duplicate_object OR duplicate_table THEN NULL; END $$;

-- 2.2 Formules packagées
ALTER TABLE public.sales_bundles
  ADD COLUMN IF NOT EXISTS sku TEXT,
  ADD COLUMN IF NOT EXISTS status content_status NOT NULL DEFAULT 'PUBLISHED',
  ADD COLUMN IF NOT EXISTS sort_order INTEGER NOT NULL DEFAULT 0,
  ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  ADD COLUMN IF NOT EXISTS updated_by UUID,
  ADD COLUMN IF NOT EXISTS version INTEGER NOT NULL DEFAULT 1,
  ADD COLUMN IF NOT EXISTS duplicated_from UUID REFERENCES public.sales_bundles(id) ON DELETE SET NULL,
  ADD COLUMN IF NOT EXISTS first_published_at TIMESTAMPTZ;

UPDATE public.sales_bundles SET sku = 'PCK-' || replace(bundle_code, '_', '-') WHERE sku IS NULL;
UPDATE public.sales_bundles SET first_published_at = COALESCE(first_published_at, created_at);
UPDATE public.sales_bundles b
   SET sort_order = s.rn * 10
  FROM (SELECT id, row_number() OVER (ORDER BY created_at, bundle_code) AS rn FROM public.sales_bundles) s
 WHERE s.id = b.id AND b.sort_order = 0;
ALTER TABLE public.sales_bundles ALTER COLUMN sku SET NOT NULL;
DO $$ BEGIN
  ALTER TABLE public.sales_bundles ADD CONSTRAINT uq_sales_bundles_sku UNIQUE (sku);
EXCEPTION WHEN duplicate_object OR duplicate_table THEN NULL; END $$;

-- 2.3 Cités hôtelières (pas de duplication : les codes sont figés par le CHECK des réservations)
ALTER TABLE public.lodge_cities
  ADD COLUMN IF NOT EXISTS sku TEXT,
  ADD COLUMN IF NOT EXISTS status content_status NOT NULL DEFAULT 'PUBLISHED',
  ADD COLUMN IF NOT EXISTS sort_order INTEGER NOT NULL DEFAULT 0,
  ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  ADD COLUMN IF NOT EXISTS updated_by UUID,
  ADD COLUMN IF NOT EXISTS version INTEGER NOT NULL DEFAULT 1,
  ADD COLUMN IF NOT EXISTS duplicated_from UUID,
  ADD COLUMN IF NOT EXISTS first_published_at TIMESTAMPTZ;

UPDATE public.lodge_cities SET sku = 'LOD-' || code WHERE sku IS NULL;
UPDATE public.lodge_cities SET first_published_at = COALESCE(first_published_at, created_at);
UPDATE public.lodge_cities SET sort_order = CASE code WHEN 'BENE' THEN 10 WHEN 'CHANTHEL' THEN 20 WHEN 'EWONDO' THEN 30 ELSE 40 END
 WHERE sort_order = 0;
ALTER TABLE public.lodge_cities ALTER COLUMN sku SET NOT NULL;
DO $$ BEGIN
  ALTER TABLE public.lodge_cities ADD CONSTRAINT uq_lodge_cities_sku UNIQUE (sku);
EXCEPTION WHEN duplicate_object OR duplicate_table THEN NULL; END $$;

-- ============================================================================
-- 3. NOUVELLES TABLES
-- ============================================================================

-- 3.1 Agenda de la semaine (/agenda — PUB-15 / PUB-16, ADM-04)
--     Structure calquée sur WEEKLY_AGENDA_CATALOG du site live.
CREATE TABLE IF NOT EXISTS public.agenda_events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  code TEXT NOT NULL UNIQUE,                      -- ex : EVT_DIMANCHE_ROYAL
  day_filter TEXT NOT NULL,                       -- MER_JEU, VENDREDI, SAMEDI, DIMANCHE...
  target_weekday SMALLINT NOT NULL CHECK (target_weekday BETWEEN 0 AND 6), -- 0 = dimanche (convention JS)
  badge TEXT NOT NULL,
  title TEXT NOT NULL,
  short_label TEXT NOT NULL,
  price_text TEXT NOT NULL DEFAULT '',
  from_price_fcfa INTEGER CHECK (from_price_fcfa IS NULL OR from_price_fcfa >= 0),
  spots_text TEXT NOT NULL DEFAULT '',
  description TEXT NOT NULL DEFAULT '',
  schedule JSONB NOT NULL DEFAULT '[]'::jsonb CHECK (jsonb_typeof(schedule) = 'array'),
  bundle_code TEXT,                               -- PASS_DECOUVERTE, PASS_ROYALE, CUSTOM...
  dish TEXT,
  meal_slot TEXT,
  pergola BOOLEAN NOT NULL DEFAULT FALSE,
  nutrition BOOLEAN NOT NULL DEFAULT FALSE,
  image_src TEXT,
  status content_status NOT NULL DEFAULT 'DRAFT',
  sort_order INTEGER NOT NULL DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_by UUID,
  version INTEGER NOT NULL DEFAULT 1,
  duplicated_from UUID REFERENCES public.agenda_events(id) ON DELETE SET NULL,
  first_published_at TIMESTAMPTZ
);

-- 3.2 Carte du restaurant « Le Château des Saveurs » (PUB-07, précommande RES, ADM-04)
CREATE TABLE IF NOT EXISTS public.menu_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  sku TEXT NOT NULL UNIQUE,                       -- ex : MNU-POISSON-BRAISE
  category TEXT NOT NULL DEFAULT 'PLAT'
    CHECK (category IN ('ENTREE', 'PLAT', 'GRILLADE', 'MENU_ENFANT', 'DESSERT', 'BOISSON', 'FORMULE')),
  name TEXT NOT NULL,
  description TEXT NOT NULL DEFAULT '',
  price_fcfa INTEGER CHECK (price_fcfa IS NULL OR price_fcfa >= 0), -- NULL = prix non affiché
  is_signature BOOLEAN NOT NULL DEFAULT FALSE,
  in_stock BOOLEAN NOT NULL DEFAULT TRUE,
  preorder_enabled BOOLEAN NOT NULL DEFAULT TRUE, -- proposé dans la précommande cuisine 13h
  image_src TEXT,
  status content_status NOT NULL DEFAULT 'DRAFT',
  sort_order INTEGER NOT NULL DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_by UUID,
  version INTEGER NOT NULL DEFAULT 1,
  duplicated_from UUID REFERENCES public.menu_items(id) ON DELETE SET NULL,
  first_published_at TIMESTAMPTZ
);

-- 3.3 Dérogations de quotas journaliers (ADM-03)
CREATE TABLE IF NOT EXISTS public.daily_quotas (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  activity_id UUID NOT NULL REFERENCES public.catalog_activities(id) ON DELETE CASCADE,
  quota_date DATE NOT NULL,
  capacity INTEGER NOT NULL CHECK (capacity >= 0),
  reason TEXT NOT NULL DEFAULT '',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_by UUID,
  version INTEGER NOT NULL DEFAULT 1,
  CONSTRAINT uq_daily_quotas_activity_date UNIQUE (activity_id, quota_date)
);

-- 3.4 Réglages du site (bandeau météo RN3, horaires...) (ADM-03)
CREATE TABLE IF NOT EXISTS public.site_settings (
  key TEXT PRIMARY KEY,
  value JSONB NOT NULL,
  is_public BOOLEAN NOT NULL DEFAULT TRUE,
  description TEXT NOT NULL DEFAULT '',
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_by UUID,
  version INTEGER NOT NULL DEFAULT 1
);

-- 3.5 Comptes nominatifs de l'équipe (ADM-05)
CREATE TABLE IF NOT EXISTS public.staff_profiles (
  user_id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  full_name TEXT NOT NULL,
  role ecopark_role NOT NULL CHECK (role NOT IN ('visiteur_anonyme', 'client_connecte')),
  post_label TEXT NOT NULL DEFAULT '',            -- ex : « Guichet #1 — Entrée principale »
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  last_seen_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_by UUID,
  version INTEGER NOT NULL DEFAULT 1
);

-- 3.6 Santé des passerelles (ADM-06 / ADM-07) — AUCUN SECRET n'est stocké ici.
--     Écriture réservée aux Edge Functions (service_role).
CREATE TABLE IF NOT EXISTS public.gateway_health (
  provider TEXT PRIMARY KEY CHECK (provider IN ('ORANGE_MONEY', 'MTN_MOMO', 'WHATSAPP_BUSINESS')),
  display_name TEXT NOT NULL,
  mode TEXT NOT NULL DEFAULT 'SANDBOX' CHECK (mode IN ('OFF', 'SANDBOX', 'LIVE')),
  status TEXT NOT NULL DEFAULT 'UNKNOWN' CHECK (status IN ('UNKNOWN', 'OK', 'DEGRADED', 'DOWN')),
  key_last4 TEXT CHECK (key_last4 IS NULL OR char_length(key_last4) <= 4),
  last_webhook_at TIMESTAMPTZ,
  last_latency_ms INTEGER CHECK (last_latency_ms IS NULL OR last_latency_ms >= 0),
  last_error TEXT,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ============================================================================
-- 4. RÔLES & HABILITATIONS
-- ============================================================================

-- MFA (aal2) exigée pour les rôles à privilèges élevés. Passer à FALSE uniquement
-- le temps d'enrôler le premier administrateur, puis remettre à TRUE.
CREATE OR REPLACE FUNCTION public.ecopark_require_mfa()
RETURNS BOOLEAN LANGUAGE sql IMMUTABLE AS $$ SELECT TRUE $$;

CREATE OR REPLACE FUNCTION public.current_ecopark_role()
RETURNS ecopark_role
LANGUAGE sql STABLE SECURITY DEFINER SET search_path = public, pg_temp AS $$
  SELECT COALESCE(
    (SELECT sp.role FROM public.staff_profiles sp WHERE sp.user_id = auth.uid() AND sp.is_active),
    CASE WHEN auth.uid() IS NULL THEN 'visiteur_anonyme'::ecopark_role ELSE 'client_connecte'::ecopark_role END
  )
$$;

CREATE OR REPLACE FUNCTION public.ecopark_has_role(allowed ecopark_role[])
RETURNS BOOLEAN
LANGUAGE sql STABLE SECURITY DEFINER SET search_path = public, pg_temp AS $$
  SELECT r = ANY(allowed)
     AND (
       r NOT IN ('direction', 'administrateur_plateforme')
       OR NOT public.ecopark_require_mfa()
       OR COALESCE(auth.jwt() ->> 'aal', 'aal1') = 'aal2'
     )
  FROM (SELECT public.current_ecopark_role() AS r) s
$$;

-- Raccourcis lisibles
CREATE OR REPLACE FUNCTION public.ecopark_is_staff()
RETURNS BOOLEAN LANGUAGE sql STABLE AS $$
  SELECT public.ecopark_has_role(ARRAY['agent_guichet','agent_controle','responsable_exploitation','direction','administrateur_plateforme']::ecopark_role[])
$$;

CREATE OR REPLACE FUNCTION public.ecopark_is_content_editor()
RETURNS BOOLEAN LANGUAGE sql STABLE AS $$
  SELECT public.ecopark_has_role(ARRAY['responsable_exploitation','direction','administrateur_plateforme']::ecopark_role[])
$$;

CREATE OR REPLACE FUNCTION public.ecopark_is_governance()
RETURNS BOOLEAN LANGUAGE sql STABLE AS $$
  SELECT public.ecopark_has_role(ARRAY['direction','administrateur_plateforme']::ecopark_role[])
$$;

-- Profil de la session courante (utilisé par la SPA pour ouvrir / fermer les espaces)
CREATE OR REPLACE FUNCTION public.get_my_profile()
RETURNS JSONB
LANGUAGE sql STABLE SECURITY DEFINER SET search_path = public, pg_temp AS $$
  SELECT jsonb_build_object(
    'user_id', auth.uid(),
    'role', public.current_ecopark_role(),
    'full_name', sp.full_name,
    'post_label', sp.post_label,
    'is_active', COALESCE(sp.is_active, FALSE),
    'aal', COALESCE(auth.jwt() ->> 'aal', 'aal1'),
    'mfa_required', public.ecopark_require_mfa()
                    AND public.current_ecopark_role() IN ('direction', 'administrateur_plateforme'),
    'mfa_satisfied', NOT (public.ecopark_require_mfa()
                    AND public.current_ecopark_role() IN ('direction', 'administrateur_plateforme'))
                    OR COALESCE(auth.jwt() ->> 'aal', 'aal1') = 'aal2'
  )
  FROM (SELECT 1) one
  LEFT JOIN public.staff_profiles sp ON sp.user_id = auth.uid()
$$;

-- ============================================================================
-- 5. JOURNAL D'AUDIT IMMUABLE CHAÎNÉ (ADM-08)
-- ============================================================================
ALTER TABLE public.audit_logs
  ADD COLUMN IF NOT EXISTS seq BIGINT GENERATED BY DEFAULT AS IDENTITY,
  ADD COLUMN IF NOT EXISTS actor_id UUID,
  ADD COLUMN IF NOT EXISTS entity_table TEXT,
  ADD COLUMN IF NOT EXISTS entity_id TEXT,
  ADD COLUMN IF NOT EXISTS operation TEXT,
  ADD COLUMN IF NOT EXISTS before_data JSONB,
  ADD COLUMN IF NOT EXISTS after_data JSONB,
  ADD COLUMN IF NOT EXISTS prev_hash TEXT,
  ADD COLUMN IF NOT EXISTS row_hash TEXT;

-- Actions système (migrations, Edge Functions) : pas de rôle applicatif
ALTER TABLE public.audit_logs ALTER COLUMN actor_role DROP NOT NULL;

DO $$ BEGIN
  ALTER TABLE public.audit_logs ADD CONSTRAINT uq_audit_logs_seq UNIQUE (seq);
EXCEPTION WHEN duplicate_object OR duplicate_table THEN NULL; END $$;
CREATE INDEX IF NOT EXISTS idx_audit_logs_created_at ON public.audit_logs (created_at DESC);
CREATE INDEX IF NOT EXISTS idx_audit_logs_entity ON public.audit_logs (entity_table, entity_id);

-- Empreinte canonique d'une ligne (sha256 natif PostgreSQL ≥ 11, sans extension)
CREATE OR REPLACE FUNCTION public.ecopark_audit_hash(
  p_prev TEXT, p_seq BIGINT, p_created_at TIMESTAMPTZ, p_actor_id UUID, p_actor_name TEXT,
  p_actor_role ecopark_role, p_action_code TEXT, p_entity_table TEXT, p_entity_id TEXT,
  p_operation TEXT, p_description TEXT, p_before JSONB, p_after JSONB
) RETURNS TEXT
LANGUAGE sql IMMUTABLE AS $$
  SELECT encode(sha256(convert_to(concat_ws('|',
    COALESCE(p_prev, 'GENESIS'),
    p_seq::text,
    (extract(epoch FROM p_created_at) * 1000000)::bigint::text,
    COALESCE(p_actor_id::text, ''),
    COALESCE(p_actor_name, ''),
    COALESCE(p_actor_role::text, ''),
    COALESCE(p_action_code, ''),
    COALESCE(p_entity_table, ''),
    COALESCE(p_entity_id, ''),
    COALESCE(p_operation, ''),
    COALESCE(p_description, ''),
    COALESCE(p_before::text, ''),
    COALESCE(p_after::text, '')
  ), 'UTF8')), 'hex')
$$;

-- Chaînage : chaque nouvelle entrée scelle la précédente (sérialisé par verrou consultatif)
CREATE OR REPLACE FUNCTION public.ecopark_audit_chain_before_insert()
RETURNS TRIGGER
LANGUAGE plpgsql SECURITY DEFINER SET search_path = public, pg_temp AS $$
DECLARE
  v_prev TEXT;
BEGIN
  PERFORM pg_advisory_xact_lock(hashtext('ecopark_audit_chain'));
  SELECT row_hash INTO v_prev FROM public.audit_logs ORDER BY seq DESC LIMIT 1;
  NEW.created_at := COALESCE(NEW.created_at, NOW());
  NEW.prev_hash := COALESCE(v_prev, 'GENESIS');
  NEW.row_hash := public.ecopark_audit_hash(
    NEW.prev_hash, NEW.seq, NEW.created_at, NEW.actor_id, NEW.actor_name, NEW.actor_role,
    NEW.action_code, NEW.entity_table, NEW.entity_id, NEW.operation, NEW.description,
    NEW.before_data, NEW.after_data);
  RETURN NEW;
END $$;

-- Scellement des entrées déjà présentes (avant activation de l'immuabilité)
DO $$
DECLARE
  r RECORD;
  v_prev TEXT := NULL;
  v_hash TEXT;
BEGIN
  FOR r IN SELECT * FROM public.audit_logs WHERE row_hash IS NULL ORDER BY seq LOOP
    v_hash := public.ecopark_audit_hash(COALESCE(v_prev, 'GENESIS'), r.seq, r.created_at, r.actor_id,
      r.actor_name, r.actor_role, r.action_code, r.entity_table, r.entity_id, r.operation,
      r.description, r.before_data, r.after_data);
    UPDATE public.audit_logs SET prev_hash = COALESCE(v_prev, 'GENESIS'), row_hash = v_hash WHERE id = r.id;
    v_prev := v_hash;
  END LOOP;
END $$;

DROP TRIGGER IF EXISTS trg_audit_logs_chain ON public.audit_logs;
CREATE TRIGGER trg_audit_logs_chain
  BEFORE INSERT ON public.audit_logs
  FOR EACH ROW EXECUTE FUNCTION public.ecopark_audit_chain_before_insert();

-- Immuabilité : aucune modification ni suppression, même par l'administrateur
CREATE OR REPLACE FUNCTION public.ecopark_audit_block_mutation()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
  RAISE EXCEPTION 'ECOPARK_AUDIT_IMMUTABLE'
    USING ERRCODE = '42501',
          HINT = 'Le journal d''audit ADM-08 est en ajout seul : aucune entrée ne peut être modifiée ou supprimée.';
END $$;

DROP TRIGGER IF EXISTS trg_audit_logs_immutable ON public.audit_logs;
CREATE TRIGGER trg_audit_logs_immutable
  BEFORE UPDATE OR DELETE ON public.audit_logs
  FOR EACH ROW EXECUTE FUNCTION public.ecopark_audit_block_mutation();

DROP TRIGGER IF EXISTS trg_audit_logs_no_truncate ON public.audit_logs;
CREATE TRIGGER trg_audit_logs_no_truncate
  BEFORE TRUNCATE ON public.audit_logs
  FOR EACH STATEMENT EXECUTE FUNCTION public.ecopark_audit_block_mutation();

DO $$ BEGIN
  REVOKE UPDATE, DELETE, TRUNCATE ON public.audit_logs FROM anon, authenticated, service_role;
EXCEPTION WHEN undefined_object THEN NULL; END $$;

-- Écriture d'une entrée (fonction interne : non exposée aux clients)
CREATE OR REPLACE FUNCTION public.ecopark_write_audit(
  p_operation TEXT, p_entity_table TEXT, p_entity_id TEXT,
  p_before JSONB, p_after JSONB, p_description TEXT, p_action_code TEXT DEFAULT NULL
) RETURNS VOID
LANGUAGE plpgsql SECURITY DEFINER SET search_path = public, pg_temp AS $$
DECLARE
  v_uid UUID := auth.uid();
  v_name TEXT;
  v_role ecopark_role;
BEGIN
  IF v_uid IS NOT NULL THEN
    SELECT full_name INTO v_name FROM public.staff_profiles WHERE user_id = v_uid;
    v_role := public.current_ecopark_role();
    v_name := COALESCE(v_name, 'Client ' || left(v_uid::text, 8));
  ELSIF COALESCE(auth.jwt() ->> 'role', '') = 'anon' THEN
    v_role := 'visiteur_anonyme';
    v_name := 'Visiteur anonyme (site public)';
  ELSE
    v_role := NULL;
    v_name := 'Système (migration / Edge Function)';
  END IF;

  INSERT INTO public.audit_logs (actor_id, actor_name, actor_role, action_code, description,
                                 entity_table, entity_id, operation, before_data, after_data)
  VALUES (v_uid, v_name, v_role,
          COALESCE(p_action_code, p_operation || ':' || COALESCE(p_entity_table, '-')),
          p_description, p_entity_table, p_entity_id, p_operation, p_before, p_after);
END $$;

-- Trigger générique : toute écriture sur une table administrable est tracée
CREATE OR REPLACE FUNCTION public.audit_row_change()
RETURNS TRIGGER
LANGUAGE plpgsql SECURITY DEFINER SET search_path = public, pg_temp AS $$
DECLARE
  v_before JSONB := CASE WHEN TG_OP IN ('UPDATE', 'DELETE') THEN to_jsonb(OLD) END;
  v_after  JSONB := CASE WHEN TG_OP IN ('INSERT', 'UPDATE') THEN to_jsonb(NEW) END;
  v_row    JSONB := COALESCE(v_after, v_before);
  v_op     TEXT  := NULLIF(current_setting('ecopark.audit_op', TRUE), '');
  v_id     TEXT;
  v_label  TEXT;
  v_verb   TEXT;
BEGIN
  -- Mise à jour sans changement réel (hors champs techniques) : rien à tracer
  IF TG_OP = 'UPDATE'
     AND (v_before - ARRAY['updated_at','updated_by','version','last_seen_at'])
       = (v_after  - ARRAY['updated_at','updated_by','version','last_seen_at']) THEN
    RETURN NEW;
  END IF;

  v_op := COALESCE(v_op, TG_OP);
  v_id := COALESCE(v_row ->> 'id', v_row ->> 'key', v_row ->> 'user_id', v_row ->> 'provider');
  v_label := COALESCE(v_row ->> 'title', v_row ->> 'name', v_row ->> 'full_name', v_row ->> 'key',
                      v_row ->> 'reference_code', v_row ->> 'quote_reference',
                      v_row ->> 'application_ref', v_row ->> 'appointment_ref', v_id);
  v_verb := CASE v_op
    WHEN 'INSERT' THEN 'Ajout'
    WHEN 'UPDATE' THEN 'Modification'
    WHEN 'DELETE' THEN 'Suppression définitive'
    WHEN 'DUPLICATE' THEN 'Duplication (brouillon)'
    WHEN 'PUBLISH' THEN 'Publication'
    WHEN 'ARCHIVE' THEN 'Archivage'
    WHEN 'RESTORE' THEN 'Restauration'
    ELSE v_op END;

  PERFORM public.ecopark_write_audit(
    v_op, TG_TABLE_NAME, v_id, v_before, v_after,
    v_verb || ' — ' || TG_TABLE_NAME || ' « ' || COALESCE(v_label, '?') || ' »');

  RETURN COALESCE(NEW, OLD);
END $$;

-- Vérification d'intégrité de la chaîne (bouton « Vérifier l'intégrité » d'ADM-08)
CREATE OR REPLACE FUNCTION public.verify_audit_chain()
RETURNS TABLE (is_valid BOOLEAN, checked_rows BIGINT, first_broken_seq BIGINT)
LANGUAGE plpgsql STABLE SECURITY DEFINER SET search_path = public, pg_temp AS $$
DECLARE
  r RECORD;
  v_prev TEXT := 'GENESIS';
  v_count BIGINT := 0;
BEGIN
  IF NOT public.ecopark_is_governance() THEN
    RAISE EXCEPTION 'ECOPARK_FORBIDDEN' USING ERRCODE = '42501',
      HINT = 'Réservé à la Direction et à l''Administrateur plateforme.';
  END IF;
  FOR r IN SELECT * FROM public.audit_logs ORDER BY seq LOOP
    v_count := v_count + 1;
    IF r.prev_hash IS DISTINCT FROM v_prev
       OR r.row_hash IS DISTINCT FROM public.ecopark_audit_hash(r.prev_hash, r.seq, r.created_at, r.actor_id,
            r.actor_name, r.actor_role, r.action_code, r.entity_table, r.entity_id, r.operation,
            r.description, r.before_data, r.after_data) THEN
      RETURN QUERY SELECT FALSE, v_count, r.seq;
      RETURN;
    END IF;
    v_prev := r.row_hash;
  END LOOP;
  RETURN QUERY SELECT TRUE, v_count, NULL::BIGINT;
END $$;

-- Événements applicatifs sans écriture de table (rejet garde-fou, export CSV, test passerelle...)
CREATE OR REPLACE FUNCTION public.log_admin_event(
  p_action_code TEXT, p_entity_table TEXT, p_entity_id TEXT, p_description TEXT, p_payload JSONB DEFAULT NULL
) RETURNS VOID
LANGUAGE plpgsql SECURITY DEFINER SET search_path = public, pg_temp AS $$
BEGIN
  IF NOT public.ecopark_is_staff() THEN
    RAISE EXCEPTION 'ECOPARK_FORBIDDEN' USING ERRCODE = '42501';
  END IF;
  IF p_action_code NOT IN ('GUARD_REJECT', 'EXPORT_CSV', 'PRINT_REPORT', 'GATEWAY_TEST', 'LOGIN', 'LOGOUT') THEN
    RAISE EXCEPTION 'ECOPARK_INVALID_EVENT_CODE' USING ERRCODE = '22023';
  END IF;
  PERFORM public.ecopark_write_audit(p_action_code, p_entity_table, p_entity_id, NULL, p_payload,
                                     left(COALESCE(p_description, ''), 500), p_action_code);
END $$;

-- ============================================================================
-- 6. CYCLE DE VIE & GOUVERNANCE TARIFAIRE
-- ============================================================================

-- Horodatage, auteur, version (verrou optimiste) et date de 1re publication
CREATE OR REPLACE FUNCTION public.ecopark_touch_row()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
DECLARE
  v_row JSONB := to_jsonb(NEW);
BEGIN
  NEW.updated_at := NOW();
  NEW.updated_by := auth.uid();
  IF TG_OP = 'INSERT' THEN
    NEW.version := 1;
  ELSE
    NEW.version := OLD.version + 1;
  END IF;
  IF v_row ? 'status' THEN
    IF NEW.status = 'PUBLISHED' AND NEW.first_published_at IS NULL THEN
      NEW.first_published_at := NOW();
    END IF;
  END IF;
  IF TG_TABLE_NAME = 'catalog_activities' THEN
    NEW.is_active := (NEW.status = 'PUBLISHED');
  END IF;
  RETURN NEW;
END $$;

-- Règle de gouvernance (décision n°2) : un brouillon tarifaire est préparé par
-- l'Exploitation ou l'Administrateur, seule la Direction le publie ou modifie un prix publié.
-- Les RPC SECURITY DEFINER (current_user = propriétaire) appliquent leurs propres contrôles.
CREATE OR REPLACE FUNCTION public.ecopark_enforce_price_governance()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
DECLARE
  v_is_direction BOOLEAN;
  v_price_cols TEXT[];
  v_old JSONB;
  v_new JSONB;
  c TEXT;
BEGIN
  IF current_user NOT IN ('anon', 'authenticated') THEN
    RETURN NEW;
  END IF;
  v_is_direction := public.ecopark_has_role(ARRAY['direction']::ecopark_role[]);
  IF v_is_direction THEN
    RETURN NEW;
  END IF;

  IF TG_OP = 'INSERT' THEN
    IF NEW.status <> 'DRAFT' THEN
      RAISE EXCEPTION 'ECOPARK_PUBLISH_REQUIRES_DIRECTION' USING ERRCODE = '42501',
        HINT = 'Une nouvelle offre tarifaire est créée en brouillon ; seule la Direction peut la publier.';
    END IF;
    RETURN NEW;
  END IF;

  IF NEW.status IS DISTINCT FROM OLD.status
     AND (NEW.status = 'PUBLISHED' OR OLD.status = 'PUBLISHED') THEN
    RAISE EXCEPTION 'ECOPARK_PUBLISH_REQUIRES_DIRECTION' USING ERRCODE = '42501',
      HINT = 'Seule la Direction peut publier ou retirer une offre tarifaire en ligne.';
  END IF;

  IF OLD.status = 'PUBLISHED' THEN
    v_price_cols := CASE TG_TABLE_NAME
      WHEN 'catalog_activities' THEN ARRAY['child_price_fcfa','adult_price_fcfa','group_adult_price_fcfa','group_child_price_fcfa']
      WHEN 'sales_bundles' THEN ARRAY['adult_bundle_price_fcfa','child_bundle_price_fcfa']
      WHEN 'lodge_cities' THEN ARRAY['min_price_fcfa','max_price_fcfa']
      ELSE ARRAY[]::TEXT[] END;
    v_old := to_jsonb(OLD);
    v_new := to_jsonb(NEW);
    FOREACH c IN ARRAY v_price_cols LOOP
      IF v_old -> c IS DISTINCT FROM v_new -> c THEN
        RAISE EXCEPTION 'ECOPARK_PUBLISHED_PRICE_LOCKED' USING ERRCODE = '42501',
          HINT = 'Ce tarif est en ligne : dupliquez la fiche en brouillon, puis faites-la publier par la Direction.';
      END IF;
    END LOOP;
  END IF;
  RETURN NEW;
END $$;

-- Empêche un membre de l'équipe de modifier son propre rôle ou de réactiver son compte
CREATE OR REPLACE FUNCTION public.ecopark_staff_self_guard()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
  IF current_user IN ('anon', 'authenticated') AND OLD.user_id = auth.uid()
     AND (NEW.role IS DISTINCT FROM OLD.role OR NEW.is_active IS DISTINCT FROM OLD.is_active) THEN
    RAISE EXCEPTION 'ECOPARK_SELF_ROLE_CHANGE_FORBIDDEN' USING ERRCODE = '42501',
      HINT = 'Un compte ne peut pas modifier son propre rôle ni son propre statut.';
  END IF;
  RETURN NEW;
END $$;

-- Pose des triggers
DO $$
DECLARE
  t TEXT;
BEGIN
  -- Horodatage / version
  FOREACH t IN ARRAY ARRAY['catalog_activities','sales_bundles','lodge_cities','agenda_events',
                           'menu_items','daily_quotas','site_settings','staff_profiles'] LOOP
    EXECUTE format('DROP TRIGGER IF EXISTS trg_%1$s_touch ON public.%1$I', t);
    EXECUTE format('CREATE TRIGGER trg_%1$s_touch BEFORE INSERT OR UPDATE ON public.%1$I
                    FOR EACH ROW EXECUTE FUNCTION public.ecopark_touch_row()', t);
  END LOOP;

  -- Gouvernance tarifaire
  FOREACH t IN ARRAY ARRAY['catalog_activities','sales_bundles','lodge_cities'] LOOP
    EXECUTE format('DROP TRIGGER IF EXISTS trg_%1$s_price_governance ON public.%1$I', t);
    EXECUTE format('CREATE TRIGGER trg_%1$s_price_governance BEFORE INSERT OR UPDATE ON public.%1$I
                    FOR EACH ROW EXECUTE FUNCTION public.ecopark_enforce_price_governance()', t);
  END LOOP;

  -- Audit complet (ajout, modification, suppression)
  FOREACH t IN ARRAY ARRAY['catalog_activities','sales_bundles','lodge_cities','agenda_events',
                           'menu_items','daily_quotas','site_settings','staff_profiles'] LOOP
    EXECUTE format('DROP TRIGGER IF EXISTS trg_%1$s_audit ON public.%1$I', t);
    EXECUTE format('CREATE TRIGGER trg_%1$s_audit AFTER INSERT OR UPDATE OR DELETE ON public.%1$I
                    FOR EACH ROW EXECUTE FUNCTION public.audit_row_change()', t);
  END LOOP;

  -- Audit des changements d'état métier (paiement, scan, report, remboursement, statut de dossier)
  FOREACH t IN ARRAY ARRAY['bookings','group_quotes','cfp_applications','appointments'] LOOP
    EXECUTE format('DROP TRIGGER IF EXISTS trg_%1$s_audit ON public.%1$I', t);
    EXECUTE format('CREATE TRIGGER trg_%1$s_audit AFTER UPDATE OR DELETE ON public.%1$I
                    FOR EACH ROW EXECUTE FUNCTION public.audit_row_change()', t);
  END LOOP;
END $$;

DROP TRIGGER IF EXISTS trg_staff_profiles_self_guard ON public.staff_profiles;
CREATE TRIGGER trg_staff_profiles_self_guard
  BEFORE UPDATE ON public.staff_profiles
  FOR EACH ROW EXECUTE FUNCTION public.ecopark_staff_self_guard();

-- ============================================================================
-- 7. RPC D'ADMINISTRATION (Ajouter / Dupliquer / Publier / Archiver / Supprimer)
-- ============================================================================

-- Valeur unique « base-copie-N » pour une colonne unique (slug, sku, code)
CREATE OR REPLACE FUNCTION public.ecopark_unique_copy_value(p_table REGCLASS, p_col TEXT, p_base TEXT, p_sep TEXT)
RETURNS TEXT LANGUAGE plpgsql STABLE SET search_path = public, pg_temp AS $$
DECLARE
  v_base TEXT := regexp_replace(p_base, '(-|_)copie(-|_)\d+$', '', 'i');
  v_candidate TEXT;
  v_exists BOOLEAN;
  n INTEGER := 0;
BEGIN
  LOOP
    n := n + 1;
    v_candidate := v_base || p_sep || n;
    EXECUTE format('SELECT EXISTS (SELECT 1 FROM %s WHERE %I = $1)', p_table, p_col)
      INTO v_exists USING v_candidate;
    EXIT WHEN NOT v_exists;
  END LOOP;
  RETURN v_candidate;
END $$;

-- Contrôle d'habilitation commun aux RPC
CREATE OR REPLACE FUNCTION public.ecopark_assert_can_manage(p_entity TEXT, p_action TEXT)
RETURNS VOID LANGUAGE plpgsql STABLE SECURITY DEFINER SET search_path = public, pg_temp AS $$
DECLARE
  v_price_entity BOOLEAN := p_entity IN ('catalog_activities', 'sales_bundles', 'lodge_cities');
  v_ok BOOLEAN;
BEGIN
  IF p_entity NOT IN ('catalog_activities', 'sales_bundles', 'lodge_cities', 'agenda_events', 'menu_items') THEN
    RAISE EXCEPTION 'ECOPARK_UNKNOWN_ENTITY' USING ERRCODE = '22023';
  END IF;
  v_ok := CASE
    WHEN v_price_entity AND p_action = 'PUBLISH' THEN public.ecopark_has_role(ARRAY['direction']::ecopark_role[])
    WHEN v_price_entity AND p_action IN ('ARCHIVE', 'DELETE') THEN public.ecopark_is_governance()
    ELSE public.ecopark_is_content_editor()
  END;
  IF NOT v_ok THEN
    RAISE EXCEPTION '%', CASE WHEN v_price_entity AND p_action = 'PUBLISH'
                              THEN 'ECOPARK_PUBLISH_REQUIRES_DIRECTION' ELSE 'ECOPARK_FORBIDDEN' END
      USING ERRCODE = '42501',
            HINT = 'Votre rôle ne permet pas cette action sur ce contenu.';
  END IF;
END $$;

-- DUPLIQUER : la copie est TOUJOURS un brouillon (décision n°3), insérée juste après l'original
CREATE OR REPLACE FUNCTION public.admin_duplicate(p_entity TEXT, p_id UUID)
RETURNS UUID
LANGUAGE plpgsql SECURITY DEFINER SET search_path = public, pg_temp AS $$
DECLARE
  v_new UUID;
  v_found BOOLEAN;
BEGIN
  PERFORM public.ecopark_assert_can_manage(p_entity, 'DUPLICATE');
  PERFORM set_config('ecopark.audit_op', 'DUPLICATE', TRUE);

  IF p_entity = 'catalog_activities' THEN
    INSERT INTO public.catalog_activities (slug, sku, title, pole, description, child_price_fcfa, adult_price_fcfa,
      group_adult_price_fcfa, group_child_price_fcfa, daily_capacity, status, sort_order, duplicated_from)
    SELECT public.ecopark_unique_copy_value('public.catalog_activities', 'slug', slug, '-copie-'),
           public.ecopark_unique_copy_value('public.catalog_activities', 'sku', sku, '-COPIE-'),
           title || ' (Copie)', pole, description, child_price_fcfa, adult_price_fcfa,
           group_adult_price_fcfa, group_child_price_fcfa, daily_capacity, 'DRAFT', sort_order + 1, id
      FROM public.catalog_activities WHERE id = p_id
    RETURNING id INTO v_new;

  ELSIF p_entity = 'sales_bundles' THEN
    INSERT INTO public.sales_bundles (bundle_code, sku, title, subtitle, included_slugs, adult_bundle_price_fcfa,
      child_bundle_price_fcfa, savings_label, is_featured, status, sort_order, duplicated_from)
    SELECT public.ecopark_unique_copy_value('public.sales_bundles', 'bundle_code', bundle_code, '_COPIE_'),
           public.ecopark_unique_copy_value('public.sales_bundles', 'sku', sku, '-COPIE-'),
           title || ' (Copie)', subtitle, included_slugs, adult_bundle_price_fcfa,
           child_bundle_price_fcfa, savings_label, FALSE, 'DRAFT', sort_order + 1, id
      FROM public.sales_bundles WHERE id = p_id
    RETURNING id INTO v_new;

  ELSIF p_entity = 'agenda_events' THEN
    INSERT INTO public.agenda_events (code, day_filter, target_weekday, badge, title, short_label, price_text,
      from_price_fcfa, spots_text, description, schedule, bundle_code, dish, meal_slot, pergola, nutrition,
      image_src, status, sort_order, duplicated_from)
    SELECT public.ecopark_unique_copy_value('public.agenda_events', 'code', code, '_COPIE_'),
           day_filter, target_weekday, badge, title || ' (Copie)', short_label || ' (Copie)', price_text,
           from_price_fcfa, spots_text, description, schedule, bundle_code, dish, meal_slot, pergola, nutrition,
           image_src, 'DRAFT', sort_order + 1, id
      FROM public.agenda_events WHERE id = p_id
    RETURNING id INTO v_new;

  ELSIF p_entity = 'menu_items' THEN
    INSERT INTO public.menu_items (sku, category, name, description, price_fcfa, is_signature, in_stock,
      preorder_enabled, image_src, status, sort_order, duplicated_from)
    SELECT public.ecopark_unique_copy_value('public.menu_items', 'sku', sku, '-COPIE-'),
           category, name || ' (Copie)', description, price_fcfa, is_signature, in_stock,
           preorder_enabled, image_src, 'DRAFT', sort_order + 1, id
      FROM public.menu_items WHERE id = p_id
    RETURNING id INTO v_new;

  ELSE
    RAISE EXCEPTION 'ECOPARK_DUPLICATE_NOT_SUPPORTED' USING ERRCODE = '22023',
      HINT = 'Les cités hôtelières ne se dupliquent pas (codes figés EWONDO / CHANTHEL / BENE).';
  END IF;

  IF v_new IS NULL THEN
    RAISE EXCEPTION 'ECOPARK_NOT_FOUND' USING ERRCODE = 'P0002';
  END IF;
  PERFORM set_config('ecopark.audit_op', '', TRUE);
  RETURN v_new;
END $$;

-- PUBLIER / ARCHIVER / REMETTRE EN BROUILLON
-- p_replace_original = TRUE : publier un brouillon issu d'une duplication remplace les
-- valeurs de la fiche d'origine (même slug public, mêmes réservations), puis archive le brouillon.
CREATE OR REPLACE FUNCTION public.admin_set_status(
  p_entity TEXT, p_id UUID, p_status content_status, p_replace_original BOOLEAN DEFAULT FALSE
) RETURNS UUID
LANGUAGE plpgsql SECURITY DEFINER SET search_path = public, pg_temp AS $$
DECLARE
  v_current content_status;
  v_origin UUID;
  v_origin_status content_status;
  v_target UUID := p_id;
BEGIN
  PERFORM public.ecopark_assert_can_manage(p_entity,
    CASE p_status WHEN 'PUBLISHED' THEN 'PUBLISH' WHEN 'ARCHIVED' THEN 'ARCHIVE' ELSE 'EDIT' END);

  EXECUTE format('SELECT status, duplicated_from FROM public.%I WHERE id = $1', p_entity)
    INTO v_current, v_origin USING p_id;
  IF v_current IS NULL THEN
    RAISE EXCEPTION 'ECOPARK_NOT_FOUND' USING ERRCODE = 'P0002';
  END IF;
  -- Retirer une offre tarifaire en ligne (vers brouillon) relève aussi de la Direction
  IF v_current = 'PUBLISHED' AND p_status = 'DRAFT' THEN
    PERFORM public.ecopark_assert_can_manage(p_entity, 'PUBLISH');
  END IF;

  IF p_status = 'PUBLISHED' AND p_replace_original AND v_origin IS NOT NULL THEN
    EXECUTE format('SELECT status FROM public.%I WHERE id = $1', p_entity) INTO v_origin_status USING v_origin;
  END IF;

  IF v_origin_status = 'PUBLISHED' THEN
    PERFORM set_config('ecopark.audit_op', 'PUBLISH', TRUE);
    IF p_entity = 'catalog_activities' THEN
      UPDATE public.catalog_activities o SET
        title = regexp_replace(d.title, '\s*\(Copie\)$', ''), pole = d.pole, description = d.description,
        child_price_fcfa = d.child_price_fcfa, adult_price_fcfa = d.adult_price_fcfa,
        group_adult_price_fcfa = d.group_adult_price_fcfa, group_child_price_fcfa = d.group_child_price_fcfa,
        daily_capacity = d.daily_capacity
      FROM public.catalog_activities d WHERE d.id = p_id AND o.id = v_origin;
    ELSIF p_entity = 'sales_bundles' THEN
      UPDATE public.sales_bundles o SET
        title = regexp_replace(d.title, '\s*\(Copie\)$', ''), subtitle = d.subtitle,
        included_slugs = d.included_slugs, adult_bundle_price_fcfa = d.adult_bundle_price_fcfa,
        child_bundle_price_fcfa = d.child_bundle_price_fcfa, savings_label = d.savings_label
      FROM public.sales_bundles d WHERE d.id = p_id AND o.id = v_origin;
    ELSIF p_entity = 'agenda_events' THEN
      UPDATE public.agenda_events o SET
        day_filter = d.day_filter, target_weekday = d.target_weekday, badge = d.badge,
        title = regexp_replace(d.title, '\s*\(Copie\)$', ''),
        short_label = regexp_replace(d.short_label, '\s*\(Copie\)$', ''),
        price_text = d.price_text, from_price_fcfa = d.from_price_fcfa, spots_text = d.spots_text,
        description = d.description, schedule = d.schedule, bundle_code = d.bundle_code, dish = d.dish,
        meal_slot = d.meal_slot, pergola = d.pergola, nutrition = d.nutrition, image_src = d.image_src
      FROM public.agenda_events d WHERE d.id = p_id AND o.id = v_origin;
    ELSIF p_entity = 'menu_items' THEN
      UPDATE public.menu_items o SET
        category = d.category, name = regexp_replace(d.name, '\s*\(Copie\)$', ''), description = d.description,
        price_fcfa = d.price_fcfa, is_signature = d.is_signature, in_stock = d.in_stock,
        preorder_enabled = d.preorder_enabled, image_src = d.image_src
      FROM public.menu_items d WHERE d.id = p_id AND o.id = v_origin;
    END IF;
    PERFORM set_config('ecopark.audit_op', 'ARCHIVE', TRUE);
    EXECUTE format('UPDATE public.%I SET status = ''ARCHIVED'' WHERE id = $1', p_entity) USING p_id;
    v_target := v_origin;
  ELSE
    PERFORM set_config('ecopark.audit_op',
      CASE WHEN p_status = 'PUBLISHED' THEN 'PUBLISH'
           WHEN p_status = 'ARCHIVED' THEN 'ARCHIVE'
           ELSE 'RESTORE' END, TRUE);
    EXECUTE format('UPDATE public.%I SET status = $2 WHERE id = $1', p_entity) USING p_id, p_status;
  END IF;

  PERFORM set_config('ecopark.audit_op', '', TRUE);
  RETURN v_target;
END $$;

-- SUPPRIMER : suppression définitive uniquement pour un brouillon jamais publié et non référencé ;
-- sinon archivage (l'historique des ventes reste intact). Renvoie 'DELETED' ou 'ARCHIVED'.
CREATE OR REPLACE FUNCTION public.admin_delete(p_entity TEXT, p_id UUID)
RETURNS TEXT
LANGUAGE plpgsql SECURITY DEFINER SET search_path = public, pg_temp AS $$
DECLARE
  v_row JSONB;
  v_referenced BOOLEAN := FALSE;
BEGIN
  PERFORM public.ecopark_assert_can_manage(p_entity, 'DELETE');
  EXECUTE format('SELECT to_jsonb(t) FROM public.%I t WHERE id = $1', p_entity) INTO v_row USING p_id;
  IF v_row IS NULL THEN
    RAISE EXCEPTION 'ECOPARK_NOT_FOUND' USING ERRCODE = 'P0002';
  END IF;

  IF p_entity = 'catalog_activities' THEN
    SELECT EXISTS (SELECT 1 FROM public.bookings b
                    WHERE (v_row ->> 'slug') = ANY(b.selected_activities) OR (v_row ->> 'slug') = ANY(b.order_bumps))
        OR EXISTS (SELECT 1 FROM public.sales_bundles sb WHERE (v_row ->> 'slug') = ANY(sb.included_slugs))
        OR EXISTS (SELECT 1 FROM public.daily_quotas q WHERE q.activity_id = p_id)
      INTO v_referenced;
  ELSIF p_entity = 'sales_bundles' THEN
    SELECT EXISTS (SELECT 1 FROM public.bookings b WHERE b.selected_bundle_code = v_row ->> 'bundle_code')
      INTO v_referenced;
  ELSIF p_entity = 'lodge_cities' THEN
    SELECT EXISTS (SELECT 1 FROM public.bookings b WHERE b.lodge_city = v_row ->> 'code')
      INTO v_referenced;
  END IF;

  IF (v_row ->> 'status') = 'DRAFT' AND (v_row ->> 'first_published_at') IS NULL AND NOT v_referenced THEN
    PERFORM set_config('ecopark.audit_op', 'DELETE', TRUE);
    EXECUTE format('DELETE FROM public.%I WHERE id = $1', p_entity) USING p_id;
    PERFORM set_config('ecopark.audit_op', '', TRUE);
    RETURN 'DELETED';
  END IF;

  PERFORM set_config('ecopark.audit_op', 'ARCHIVE', TRUE);
  EXECUTE format('UPDATE public.%I SET status = ''ARCHIVED'' WHERE id = $1', p_entity) USING p_id;
  PERFORM set_config('ecopark.audit_op', '', TRUE);
  RETURN 'ARCHIVED';
END $$;

-- DISPONIBILITÉS (baromètre public /reserver, guichet, ADM-03) sans exposer les réservations
CREATE OR REPLACE FUNCTION public.get_availability(p_date DATE)
RETURNS TABLE (slug TEXT, title TEXT, capacity INTEGER, booked INTEGER, remaining INTEGER)
LANGUAGE sql STABLE SECURITY DEFINER SET search_path = public, pg_temp AS $$
  WITH active AS (
    SELECT c.id, c.slug, c.title,
           COALESCE(q.capacity, c.daily_capacity) AS capacity, c.sort_order
      FROM public.catalog_activities c
      LEFT JOIN public.daily_quotas q ON q.activity_id = c.id AND q.quota_date = p_date
     WHERE c.status = 'PUBLISHED'
  ),
  live_bookings AS (
    SELECT b.*
      FROM public.bookings b
     WHERE b.visit_date = p_date
       AND b.cancelled_at IS NULL
       AND (b.payment_state = 'CONFIRMED'
            OR (b.payment_state = 'PENDING' AND (b.hold_expires_at IS NULL OR b.hold_expires_at > NOW())))
  )
  SELECT a.slug, a.title, a.capacity,
         COALESCE(SUM(lb.adults_count + lb.children_count), 0)::INTEGER AS booked,
         GREATEST(a.capacity - COALESCE(SUM(lb.adults_count + lb.children_count), 0), 0)::INTEGER AS remaining
    FROM active a
    LEFT JOIN live_bookings lb
      ON a.slug = ANY(lb.selected_activities)
      OR EXISTS (SELECT 1 FROM public.sales_bundles sb
                  WHERE sb.bundle_code = lb.selected_bundle_code AND a.slug = ANY(sb.included_slugs))
   GROUP BY a.slug, a.title, a.capacity, a.sort_order
   ORDER BY a.sort_order
$$;

-- ============================================================================
-- 8. POLITIQUES RLS
-- ============================================================================
ALTER TABLE public.agenda_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.menu_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.daily_quotas ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.site_settings ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.staff_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.gateway_health ENABLE ROW LEVEL SECURITY;

-- Les anciennes politiques de lecture sont remplacées (statut au lieu de is_active)
DROP POLICY IF EXISTS "Public read active catalog" ON public.catalog_activities;
DROP POLICY IF EXISTS "Public read sales bundles" ON public.sales_bundles;
DROP POLICY IF EXISTS "Public read lodge cities" ON public.lodge_cities;

-- 8.1 Contenus administrables : public = publié ; équipe = tout ; écriture = éditeurs
DO $$
DECLARE
  t TEXT;
BEGIN
  FOREACH t IN ARRAY ARRAY['catalog_activities','sales_bundles','lodge_cities','agenda_events','menu_items'] LOOP
    EXECUTE format('DROP POLICY IF EXISTS "%1$s_public_read_published" ON public.%1$I', t);
    EXECUTE format('CREATE POLICY "%1$s_public_read_published" ON public.%1$I
                    FOR SELECT USING (status = ''PUBLISHED'')', t);
    EXECUTE format('DROP POLICY IF EXISTS "%1$s_staff_read_all" ON public.%1$I', t);
    EXECUTE format('CREATE POLICY "%1$s_staff_read_all" ON public.%1$I
                    FOR SELECT TO authenticated USING (public.ecopark_is_staff())', t);
    EXECUTE format('DROP POLICY IF EXISTS "%1$s_editor_insert" ON public.%1$I', t);
    EXECUTE format('CREATE POLICY "%1$s_editor_insert" ON public.%1$I
                    FOR INSERT TO authenticated WITH CHECK (public.ecopark_is_content_editor())', t);
    EXECUTE format('DROP POLICY IF EXISTS "%1$s_editor_update" ON public.%1$I', t);
    EXECUTE format('CREATE POLICY "%1$s_editor_update" ON public.%1$I
                    FOR UPDATE TO authenticated
                    USING (public.ecopark_is_content_editor()) WITH CHECK (public.ecopark_is_content_editor())', t);
    -- Pas de politique DELETE : la suppression passe obligatoirement par admin_delete()
  END LOOP;
END $$;

-- 8.2 Quotas journaliers
DROP POLICY IF EXISTS "daily_quotas_staff_read" ON public.daily_quotas;
CREATE POLICY "daily_quotas_staff_read" ON public.daily_quotas
  FOR SELECT TO authenticated USING (public.ecopark_is_staff());
DROP POLICY IF EXISTS "daily_quotas_editor_write" ON public.daily_quotas;
CREATE POLICY "daily_quotas_editor_write" ON public.daily_quotas
  FOR ALL TO authenticated
  USING (public.ecopark_is_content_editor()) WITH CHECK (public.ecopark_is_content_editor());

-- 8.3 Réglages du site
DROP POLICY IF EXISTS "site_settings_public_read" ON public.site_settings;
CREATE POLICY "site_settings_public_read" ON public.site_settings
  FOR SELECT USING (is_public OR public.ecopark_is_staff());
DROP POLICY IF EXISTS "site_settings_editor_insert" ON public.site_settings;
CREATE POLICY "site_settings_editor_insert" ON public.site_settings
  FOR INSERT TO authenticated WITH CHECK (public.ecopark_is_content_editor());
DROP POLICY IF EXISTS "site_settings_editor_update" ON public.site_settings;
CREATE POLICY "site_settings_editor_update" ON public.site_settings
  FOR UPDATE TO authenticated
  USING (public.ecopark_is_content_editor()) WITH CHECK (public.ecopark_is_content_editor());
DROP POLICY IF EXISTS "site_settings_admin_delete" ON public.site_settings;
CREATE POLICY "site_settings_admin_delete" ON public.site_settings
  FOR DELETE TO authenticated
  USING (public.ecopark_has_role(ARRAY['administrateur_plateforme']::ecopark_role[]));

-- 8.4 Comptes équipe : chacun lit sa fiche ; Direction / Admin lisent tout ; Admin gère
DROP POLICY IF EXISTS "staff_profiles_self_read" ON public.staff_profiles;
CREATE POLICY "staff_profiles_self_read" ON public.staff_profiles
  FOR SELECT TO authenticated USING (user_id = auth.uid() OR public.ecopark_is_governance());
DROP POLICY IF EXISTS "staff_profiles_admin_insert" ON public.staff_profiles;
CREATE POLICY "staff_profiles_admin_insert" ON public.staff_profiles
  FOR INSERT TO authenticated
  WITH CHECK (public.ecopark_has_role(ARRAY['administrateur_plateforme']::ecopark_role[]));
DROP POLICY IF EXISTS "staff_profiles_admin_update" ON public.staff_profiles;
CREATE POLICY "staff_profiles_admin_update" ON public.staff_profiles
  FOR UPDATE TO authenticated
  USING (public.ecopark_has_role(ARRAY['administrateur_plateforme']::ecopark_role[]))
  WITH CHECK (public.ecopark_has_role(ARRAY['administrateur_plateforme']::ecopark_role[]));

-- 8.5 Passerelles : lecture Direction / Admin ; écriture Edge Functions uniquement (service_role)
DROP POLICY IF EXISTS "gateway_health_governance_read" ON public.gateway_health;
CREATE POLICY "gateway_health_governance_read" ON public.gateway_health
  FOR SELECT TO authenticated USING (public.ecopark_is_governance());

-- 8.6 Journal d'audit : lecture Direction / Admin ; aucune écriture directe
DROP POLICY IF EXISTS "audit_logs_governance_read" ON public.audit_logs;
CREATE POLICY "audit_logs_governance_read" ON public.audit_logs
  FOR SELECT TO authenticated USING (public.ecopark_is_governance());

-- 8.7 Réservations : équipe opérationnelle + client propriétaire
DROP POLICY IF EXISTS "bookings_staff_read" ON public.bookings;
CREATE POLICY "bookings_staff_read" ON public.bookings
  FOR SELECT TO authenticated USING (public.ecopark_is_staff());
DROP POLICY IF EXISTS "bookings_owner_read" ON public.bookings;
CREATE POLICY "bookings_owner_read" ON public.bookings
  FOR SELECT TO authenticated USING (customer_user_id IS NOT NULL AND customer_user_id = auth.uid());
DROP POLICY IF EXISTS "bookings_counter_insert" ON public.bookings;
CREATE POLICY "bookings_counter_insert" ON public.bookings
  FOR INSERT TO authenticated
  WITH CHECK (public.ecopark_has_role(ARRAY['agent_guichet','responsable_exploitation','direction','administrateur_plateforme']::ecopark_role[]));
DROP POLICY IF EXISTS "bookings_ops_update" ON public.bookings;
CREATE POLICY "bookings_ops_update" ON public.bookings
  FOR UPDATE TO authenticated
  USING (public.ecopark_has_role(ARRAY['agent_guichet','responsable_exploitation','direction','administrateur_plateforme']::ecopark_role[]))
  WITH CHECK (public.ecopark_has_role(ARRAY['agent_guichet','responsable_exploitation','direction','administrateur_plateforme']::ecopark_role[]));
-- Les réservations en ligne passeront par la RPC create_booking() (recalcul serveur du total) — Phase 5.
-- Le scan QR (agent_controle) passera par la RPC scan_ticket() — Phase 6.

-- 8.8 Devis, candidatures CFP, rendez-vous : dépôt public, traitement par l'Exploitation
DO $$
DECLARE
  t TEXT;
  v_status_check TEXT;
BEGIN
  FOREACH t IN ARRAY ARRAY['group_quotes','cfp_applications','appointments'] LOOP
    v_status_check := CASE t
      WHEN 'group_quotes' THEN 'status = ''EN_ETUDE'''
      WHEN 'cfp_applications' THEN 'status = ''DOSSIER_RECU'''
      ELSE 'status = ''CONFIRME''' END;
    EXECUTE format('DROP POLICY IF EXISTS "%1$s_public_submit" ON public.%1$I', t);
    EXECUTE format('CREATE POLICY "%1$s_public_submit" ON public.%1$I
                    FOR INSERT TO anon, authenticated WITH CHECK (%2$s)', t, v_status_check);
    EXECUTE format('DROP POLICY IF EXISTS "%1$s_ops_read" ON public.%1$I', t);
    EXECUTE format('CREATE POLICY "%1$s_ops_read" ON public.%1$I
                    FOR SELECT TO authenticated USING (public.ecopark_is_content_editor())', t);
    EXECUTE format('DROP POLICY IF EXISTS "%1$s_ops_update" ON public.%1$I', t);
    EXECUTE format('CREATE POLICY "%1$s_ops_update" ON public.%1$I
                    FOR UPDATE TO authenticated
                    USING (public.ecopark_is_content_editor()) WITH CHECK (public.ecopark_is_content_editor())', t);
  END LOOP;
END $$;

-- 8.9 Droits d'exécution : fonctions internes non exposées
DO $$ BEGIN
  REVOKE EXECUTE ON FUNCTION public.ecopark_write_audit(TEXT, TEXT, TEXT, JSONB, JSONB, TEXT, TEXT) FROM PUBLIC, anon, authenticated;
  REVOKE EXECUTE ON FUNCTION public.ecopark_unique_copy_value(REGCLASS, TEXT, TEXT, TEXT) FROM PUBLIC, anon, authenticated;
  REVOKE EXECUTE ON FUNCTION public.admin_duplicate(TEXT, UUID) FROM PUBLIC, anon;
  REVOKE EXECUTE ON FUNCTION public.admin_set_status(TEXT, UUID, content_status, BOOLEAN) FROM PUBLIC, anon;
  REVOKE EXECUTE ON FUNCTION public.admin_delete(TEXT, UUID) FROM PUBLIC, anon;
  REVOKE EXECUTE ON FUNCTION public.verify_audit_chain() FROM PUBLIC, anon;
  REVOKE EXECUTE ON FUNCTION public.log_admin_event(TEXT, TEXT, TEXT, TEXT, JSONB) FROM PUBLIC, anon;
  GRANT EXECUTE ON FUNCTION public.admin_duplicate(TEXT, UUID) TO authenticated;
  GRANT EXECUTE ON FUNCTION public.admin_set_status(TEXT, UUID, content_status, BOOLEAN) TO authenticated;
  GRANT EXECUTE ON FUNCTION public.admin_delete(TEXT, UUID) TO authenticated;
  GRANT EXECUTE ON FUNCTION public.verify_audit_chain() TO authenticated;
  GRANT EXECUTE ON FUNCTION public.log_admin_event(TEXT, TEXT, TEXT, TEXT, JSONB) TO authenticated;
  GRANT EXECUTE ON FUNCTION public.get_availability(DATE) TO anon, authenticated;
  GRANT EXECUTE ON FUNCTION public.get_my_profile() TO anon, authenticated;
EXCEPTION WHEN undefined_object THEN NULL; END $$;

-- ============================================================================
-- 9. DONNÉES INITIALES (reprises du site live — etape0-site-live/index.html)
-- ============================================================================
INSERT INTO public.agenda_events (code, day_filter, target_weekday, badge, title, short_label, price_text,
  from_price_fcfa, spots_text, description, schedule, bundle_code, dish, meal_slot, pergola, nutrition,
  image_src, status, sort_order)
VALUES
  ('EVT_MERCREDI_CFP', 'MER_JEU', 3, 'Mercredi & Jeudi • 10h00 – 16h00',
   'Journée Pédagogique Faune & Portes Ouvertes Campus CFP', 'Mercredi Pédagogique & Portes Ouvertes CFP',
   'Entrée : 500 FCFA (Enfant) / 1 000 FCFA (Adulte) • Orientation CFP Gratuite', 500,
   'Accès libre & Groupes scolaires sur réservation',
   'Idéal pour les familles en semaine, les écoles maternelles/primaires et les futurs apprenants souhaitant visiter les ateliers pratiques du CFP ECOPARK agréé MINEFOP.',
   jsonb_build_array(
     '10h00 – 11h30 : Visite guidée du Jardin Zoologique (gorille « ToTo », tortues géantes, paons) et des allées botaniques.',
     '11h30 – 13h00 : Démonstration d''aquaculture sur les étangs d''Ahala & séance d''orientation CFP (5 filières, inscription 50 000 FCFA).',
     '13h00 – 16h00 : Déjeuner au Château des Saveurs, balade en pirogue et baignade surveillée.'),
   'PASS_DECOUVERTE', 'Poisson Braisé d''Ahala (Étang frais)', 'Service 12h30', FALSE, TRUE,
   'audit-assets/stitch-canopee-vivante/local_cameroon_cfp_students.png', 'PUBLISHED', 10),
  ('EVT_VENDREDI_AFTERWORK', 'VENDREDI', 5, 'Vendredi • 15h30 – 20h30',
   'Afterwork « Brise du Lac & Poisson Braisé d''Ahala »', 'Vendredi Afterwork Brise du Lac & Grillades',
   'Plats dès 3 500 FCFA • Pergola Privée Bord du Lac : +5 000 FCFA', 3500,
   'Plus que 4 pergolas disponibles ce vendredi',
   'Évitez les embouteillages du vendredi soir à Yaoundé : rejoignez Ahala Barrière (face station Tradex) pour savourer le poisson frais des étangs braisé à la minute sous une pergola privée.',
   jsonb_build_array(
     '15h30 – 17h30 : Accueil coupe-file, promenade au bord du lac d''Ahala et installation sous pergola privée.',
     '17h30 – 20h30 : Service grillades & Poisson Braisé d''Ahala au Château des Saveurs, ambiance musicale douce.',
     'Option Séjour : Possibilité de prolonger en nuitée dans les Cités Bene (10k), Chanthel (15k) ou Ewondo VIP (25k FCFA).'),
   'CUSTOM', 'Poisson Braisé d''Ahala (Étang frais)', 'Service 15h00', TRUE, FALSE,
   'audit-assets/stitch-canopee-vivante/local_cameroon_gastronomy_pergola.png', 'PUBLISHED', 20),
  ('EVT_SAMEDI_FAMILLE', 'SAMEDI', 6, 'Samedi • 10h30 & 15h00',
   'Samedi Famille : Rencontre Soigneurs « Gorille ToTo » & Régate Pirogues', 'Samedi Famille • Gorille ToTo & Pirogues',
   'Pass Découverte : 1 500 FCFA (Enfant) • 2 500 FCFA (Adulte)', 1500,
   'Tarif enfant strictement garanti à 500 FCFA (entrée)',
   'La sortie préférée des enfants à Yaoundé : nourrissage commenté aux étangs, rencontre avec le gorille « ToTo », balade sécurisée en pirogue avec gilet et piscine semi-olympique.',
   jsonb_build_array(
     '10h30 – 12h00 : Rencontre avec les soigneurs du Zoo (« ToTo ») & nourrissage des poissons et tortues aux étangs.',
     '12h30 – 14h30 : Déjeuner familial au Château des Saveurs (Menu Enfant 2 500 FCFA & spécialités camerounaises).',
     '14h30 – 17h30 : Traversée en pirogue sur le lac, initiation équestre encadrée et piscine surveillée par maître-nageur.'),
   'PASS_DECOUVERTE', 'Menu Enfant & Grillades Douces', 'Service 12h30', FALSE, TRUE,
   'audit-assets/ecopark-real-media/balade_pirogue3.jpg', 'PUBLISHED', 30),
  ('EVT_DIMANCHE_ROYAL', 'DIMANCHE', 0, 'Dimanche • 12h00 – 17h30',
   'Grand Dimanche Royal : Buffet Camerounais & Ambiance Acoustique Live', 'Grand Dimanche Royal • Buffet & Live',
   'Pass Journée Royale Tout-Inclus : 4 500 FCFA (Enfant) • 8 500 FCFA (Adulte)', 4500,
   'Réservation QR fortement conseillée (Service 12h30 / 13h30 garanti)',
   'Le grand rendez-vous dominical d''ECOPARK Ahala : grands classiques du Château des Saveurs (Poulet DG Royal, Ndolé Crevettes, Poisson Braisé), ambiance acoustique au bord du lac et accès illimité Parc + Piscine + Pirogue.',
   jsonb_build_array(
     '09h30 – 12h00 : Accès coupe-file au Portail d''Ahala (QR Code), visite du Zoo et balade matinale en pirogue.',
     '12h30 – 15h00 : Grand Service Dominical au Château des Saveurs (zéro attente pour les détenteurs du Pass QR) & animation acoustique.',
     '15h00 – 18h00 : Détente à la Piscine Semi-Olympique et sous les pergolas ombragées.'),
   'PASS_ROYALE', 'Poulet DG Royal Plantain Mûr', 'Service 13h30', TRUE, TRUE,
   'audit-assets/ecopark-real-media/IMG-20260713-WA0051_043420.jpg', 'PUBLISHED', 40)
ON CONFLICT (code) DO NOTHING;

-- Carte : les 4 spécialités de la précommande du site live. Les prix non affichés
-- aujourd'hui sur le site restent à NULL (à renseigner par le restaurant via ADM-04).
INSERT INTO public.menu_items (sku, category, name, description, price_fcfa, is_signature, in_stock,
  preorder_enabled, image_src, status, sort_order)
VALUES
  ('MNU-POISSON-BRAISE', 'GRILLADE', 'Poisson Braisé d''Ahala (Étang frais)',
   'Poisson frais pêché dans les étangs d''Ahala et braisé à la minute aux épices du terroir, servi avec plantains mûrs ou miondo.',
   NULL, TRUE, TRUE, TRUE, 'audit-assets/stitch-canopee-vivante/local_cameroon_gastronomy_pergola.png', 'PUBLISHED', 10),
  ('MNU-POULET-DG', 'PLAT', 'Poulet DG Royal Plantain Mûr',
   'Le grand classique camerounais du Château des Saveurs : volaille fermière, plantains mûrs dorés, légumes frais et sauce parfumée.',
   NULL, TRUE, TRUE, TRUE, 'audit-assets/stitch-canopee-vivante/local_cameroon_gastronomy_pergola.png', 'PUBLISHED', 20),
  ('MNU-NDOLE-ROYAL', 'PLAT', 'Ndolé Royal Crevettes & Miondo',
   'Ndolé onctueux préparé selon la tradition avec crevettes, bœuf fondant et accompagnements chauds.',
   NULL, TRUE, TRUE, TRUE, 'audit-assets/stitch-canopee-vivante/local_cameroon_gastronomy_pergola.png', 'PUBLISHED', 30),
  ('MNU-MENU-ENFANT', 'MENU_ENFANT', 'Menu Enfant & Grillades Douces',
   'Portion adaptée aux enfants (3–12 ans) avec grillades tendres, frites de plantain et jus naturel (Bissap / Ananas).',
   2500, FALSE, TRUE, TRUE, 'audit-assets/stitch-canopee-vivante/local_cameroon_family_canopy.png', 'PUBLISHED', 40)
ON CONFLICT (sku) DO NOTHING;

INSERT INTO public.site_settings (key, value, is_public, description)
VALUES
  ('weather_banner',
   jsonb_build_object(
     'active_preset', 'SUNNY',
     'presets', jsonb_build_object(
       'SUNNY', '27 °C Ensoleillé • Accès RN3 fluide (15 min) • Tous les espaces ouverts',
       'RAIN_GUARANTEE', 'Averse tropicale passagère • Garantie Pluie active (report 90 j gratuit en 1 clic)',
       'WEEKEND_PEAK', 'Grand Dimanche Royal (29 °C ensoleillé) • Forte affluence : billet QR coupe-file recommandé'),
     'custom_message', NULL),
   TRUE, 'Bandeau météo & trafic RN3 affiché en haut du site public (ADM-03).'),
  ('opening_hours',
   jsonb_build_object('label', 'Mar–Dim : 09h00–18h00', 'closed_days', jsonb_build_array('LUNDI')),
   TRUE, 'Horaires affichés dans l''en-tête et le pied de page.')
ON CONFLICT (key) DO NOTHING;

INSERT INTO public.gateway_health (provider, display_name, mode, status)
VALUES
  ('ORANGE_MONEY', 'Orange Money WebPay Cameroun', 'SANDBOX', 'UNKNOWN'),
  ('MTN_MOMO', 'MTN MoMo Collection API', 'SANDBOX', 'UNKNOWN'),
  ('WHATSAPP_BUSINESS', 'Guichet unique WhatsApp Business', 'SANDBOX', 'UNKNOWN')
ON CONFLICT (provider) DO NOTHING;
