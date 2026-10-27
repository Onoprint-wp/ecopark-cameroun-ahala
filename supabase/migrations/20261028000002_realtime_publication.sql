-- ============================================================================
-- ECOPARK — Migration 3 : diffusion temps réel (Phase 3, couche d'accès aux données)
-- Ajoute les tables de contenu public et d'exploitation à la publication
-- « supabase_realtime ». La RLS s'applique aussi aux événements temps réel :
-- un visiteur ne reçoit que les lignes qu'il a le droit de lire.
-- Sans effet hors Supabase (la publication n'existe pas) : migration idempotente.
-- ============================================================================
DO $$
DECLARE
  t TEXT;
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_publication WHERE pubname = 'supabase_realtime') THEN
    RAISE NOTICE 'Publication supabase_realtime absente : temps réel non configuré (environnement de test).';
    RETURN;
  END IF;
  FOREACH t IN ARRAY ARRAY[
    'catalog_activities', 'sales_bundles', 'lodge_cities', 'agenda_events', 'menu_items', 'site_settings',
    'bookings', 'group_quotes', 'cfp_applications', 'appointments'
  ] LOOP
    IF NOT EXISTS (
      SELECT 1 FROM pg_publication_tables
       WHERE pubname = 'supabase_realtime' AND schemaname = 'public' AND tablename = t
    ) THEN
      EXECUTE format('ALTER PUBLICATION supabase_realtime ADD TABLE public.%I', t);
    END IF;
  END LOOP;
END $$;
