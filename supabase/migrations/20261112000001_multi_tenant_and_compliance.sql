-- ============================================================================
-- ECOPARK CAMEROUN (Yaoundé-Ahala) - Migration 8 :
-- Isolation Multi-Tenant (tenant_id), Sécurité RLS Complémentaire & Conformité
-- Suppression/Anonymisation de Compte (Loi n° 2010/012 / RGPD / Stores)
-- ============================================================================

-- 1. Ajout idempotent de la clé d'isolation Multi-Tenant (tenant_id)
ALTER TABLE public.catalog_activities
  ADD COLUMN IF NOT EXISTS tenant_id TEXT NOT NULL DEFAULT 'ecopark-yaounde-ahala';

ALTER TABLE public.sales_bundles
  ADD COLUMN IF NOT EXISTS tenant_id TEXT NOT NULL DEFAULT 'ecopark-yaounde-ahala';

ALTER TABLE public.lodge_cities
  ADD COLUMN IF NOT EXISTS tenant_id TEXT NOT NULL DEFAULT 'ecopark-yaounde-ahala';

ALTER TABLE public.bookings
  ADD COLUMN IF NOT EXISTS tenant_id TEXT NOT NULL DEFAULT 'ecopark-yaounde-ahala';

ALTER TABLE public.group_quotes
  ADD COLUMN IF NOT EXISTS tenant_id TEXT NOT NULL DEFAULT 'ecopark-yaounde-ahala';

ALTER TABLE public.cfp_applications
  ADD COLUMN IF NOT EXISTS tenant_id TEXT NOT NULL DEFAULT 'ecopark-yaounde-ahala';

ALTER TABLE public.appointments
  ADD COLUMN IF NOT EXISTS tenant_id TEXT NOT NULL DEFAULT 'ecopark-yaounde-ahala';

ALTER TABLE public.audit_logs
  ADD COLUMN IF NOT EXISTS tenant_id TEXT NOT NULL DEFAULT 'ecopark-yaounde-ahala';

-- 2. Table des demandes de suppression / anonymisation de compte (Loi n° 2010/012 & Stores)
CREATE TABLE IF NOT EXISTS public.account_deletion_requests (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id TEXT NOT NULL DEFAULT 'ecopark-yaounde-ahala',
  requester_reference TEXT NOT NULL,
  requester_phone_masked TEXT NOT NULL DEFAULT '',
  reason TEXT NOT NULL DEFAULT 'Demande utilisateur (droit à l''effacement)',
  status TEXT NOT NULL DEFAULT 'PROCESSED_ANONYMIZED'
    CHECK (status IN ('PENDING', 'PROCESSED_ANONYMIZED', 'REJECTED_LEGAL_HOLD')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

ALTER TABLE public.account_deletion_requests ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "account_deletion_insert_public" ON public.account_deletion_requests;
CREATE POLICY "account_deletion_insert_public"
  ON public.account_deletion_requests
  FOR INSERT
  WITH CHECK (tenant_id = 'ecopark-yaounde-ahala');

DROP POLICY IF EXISTS "account_deletion_select_governance" ON public.account_deletion_requests;
CREATE POLICY "account_deletion_select_governance"
  ON public.account_deletion_requests
  FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM public.staff_profiles sp
      WHERE sp.user_id = auth.uid()
        AND sp.is_active = TRUE
        AND sp.role IN ('direction', 'administrateur_plateforme', 'comptable')
    )
  );
