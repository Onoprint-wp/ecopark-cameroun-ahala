-- ============================================================================
-- ECOPARK CAMEROUN (Yaoundé-Ahala) - Migration 9 :
-- Gouvernance Éditoriale & Contraintes d'Hygiène Textuelle (G1)
-- Interdiction stricte des tirets cadratin et demi-cadratin sur les flux dynamiques
-- ============================================================================

-- 1. Fonction SQL d'assainissement éditorial automatique
-- Remplace les tirets longs par le tiret standard et normalise les espaces
CREATE OR REPLACE FUNCTION public.fn_sanitize_editorial_text(raw_text TEXT)
RETURNS TEXT AS $$
BEGIN
  IF raw_text IS NULL THEN
    RETURN NULL;
  END IF;

  -- Remplacement de chr(8212) [em-dash] et chr(8211) [en-dash] par le tiret standard '-'
  RETURN btrim(
    regexp_replace(
      regexp_replace(raw_text, chr(8212) || '|' || chr(8211), '-', 'g'),
      '\s+', ' ', 'g'
    )
  );
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- 2. Création ou mise à jour de la table des sentiers (park_trails)
CREATE TABLE IF NOT EXISTS public.park_trails (
  id TEXT PRIMARY KEY,
  code TEXT NOT NULL UNIQUE,
  name TEXT NOT NULL,
  difficulty TEXT NOT NULL DEFAULT 'facile',
  distance_km NUMERIC(4, 2) NOT NULL DEFAULT 1.0,
  duration_minutes INTEGER NOT NULL DEFAULT 30,
  pmr_accessible BOOLEAN NOT NULL DEFAULT true,
  status TEXT NOT NULL DEFAULT 'fluide' CHECK (status IN ('fluide', 'balise', 'ferme')),
  closure_reason TEXT,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT ck_park_trails_no_long_dash
    CHECK (closure_reason IS NULL OR (position(chr(8212) in closure_reason) = 0 AND position(chr(8211) in closure_reason) = 0))
);

-- 3. Création ou mise à jour de la table des signalements citoyens (citizen_reports)
CREATE TABLE IF NOT EXISTS public.citizen_reports (
  id TEXT PRIMARY KEY,
  trail_id TEXT REFERENCES public.park_trails(id) ON DELETE SET NULL,
  severity TEXT NOT NULL DEFAULT 'info' CHECK (severity IN ('info', 'attention', 'urgence')),
  report_type TEXT NOT NULL DEFAULT 'flore',
  title TEXT NOT NULL,
  description TEXT NOT NULL,
  landmark TEXT NOT NULL DEFAULT '',
  status TEXT NOT NULL DEFAULT 'nouveau' CHECK (status IN ('nouveau', 'valide', 'resolu', 'rejete')),
  upvotes INTEGER NOT NULL DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT ck_citizen_reports_no_long_dash
    CHECK (position(chr(8212) in description) = 0 AND position(chr(8211) in description) = 0)
);

-- 4. Création ou mise à jour de la table des interventions d'éco-gardes (ranger_interventions)
CREATE TABLE IF NOT EXISTS public.ranger_interventions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  report_id TEXT REFERENCES public.citizen_reports(id) ON DELETE CASCADE,
  trail_id TEXT REFERENCES public.park_trails(id) ON DELETE SET NULL,
  ranger_name TEXT NOT NULL,
  notes TEXT,
  action_type TEXT NOT NULL DEFAULT 'patrouille',
  status TEXT NOT NULL DEFAULT 'resolu' CHECK (status IN ('en_cours', 'resolu', 'transmis')),
  resolved_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT ck_ranger_interventions_no_long_dash
    CHECK (notes IS NULL OR (position(chr(8212) in notes) = 0 AND position(chr(8211) in notes) = 0))
);

-- 5. Trigger d'assainissement automatique sur insertion/mise à jour
CREATE OR REPLACE FUNCTION public.trg_fn_sanitize_editorial_columns()
RETURNS TRIGGER AS $$
BEGIN
  IF TG_TABLE_NAME = 'park_trails' AND NEW.closure_reason IS NOT NULL THEN
    NEW.closure_reason := public.fn_sanitize_editorial_text(NEW.closure_reason);
  ELSIF TG_TABLE_NAME = 'citizen_reports' AND NEW.description IS NOT NULL THEN
    NEW.description := public.fn_sanitize_editorial_text(NEW.description);
    NEW.title := public.fn_sanitize_editorial_text(NEW.title);
  ELSIF TG_TABLE_NAME = 'ranger_interventions' AND NEW.notes IS NOT NULL THEN
    NEW.notes := public.fn_sanitize_editorial_text(NEW.notes);
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Application idempotente des triggers
DROP TRIGGER IF EXISTS trg_sanitize_park_trails ON public.park_trails;
CREATE TRIGGER trg_sanitize_park_trails
  BEFORE INSERT OR UPDATE OF closure_reason ON public.park_trails
  FOR EACH ROW EXECUTE FUNCTION public.trg_fn_sanitize_editorial_columns();

DROP TRIGGER IF EXISTS trg_sanitize_citizen_reports ON public.citizen_reports;
CREATE TRIGGER trg_sanitize_citizen_reports
  BEFORE INSERT OR UPDATE OF title, description ON public.citizen_reports
  FOR EACH ROW EXECUTE FUNCTION public.trg_fn_sanitize_editorial_columns();

DROP TRIGGER IF EXISTS trg_sanitize_ranger_interventions ON public.ranger_interventions;
CREATE TRIGGER trg_sanitize_ranger_interventions
  BEFORE INSERT OR UPDATE OF notes ON public.ranger_interventions
  FOR EACH ROW EXECUTE FUNCTION public.trg_fn_sanitize_editorial_columns();

-- 6. Activation de la sécurité Row Level Security (RLS)
ALTER TABLE public.park_trails ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.citizen_reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.ranger_interventions ENABLE ROW LEVEL SECURITY;

-- Politiques de lecture publique et écriture authentifiée
DROP POLICY IF EXISTS "park_trails_select_public" ON public.park_trails;
CREATE POLICY "park_trails_select_public" ON public.park_trails FOR SELECT USING (true);

DROP POLICY IF EXISTS "citizen_reports_select_public" ON public.citizen_reports;
CREATE POLICY "citizen_reports_select_public" ON public.citizen_reports FOR SELECT USING (true);

DROP POLICY IF EXISTS "citizen_reports_insert_public" ON public.citizen_reports;
CREATE POLICY "citizen_reports_insert_public" ON public.citizen_reports FOR INSERT WITH CHECK (true);

DROP POLICY IF EXISTS "ranger_interventions_select_auth" ON public.ranger_interventions;
CREATE POLICY "ranger_interventions_select_auth" ON public.ranger_interventions FOR SELECT USING (true);
