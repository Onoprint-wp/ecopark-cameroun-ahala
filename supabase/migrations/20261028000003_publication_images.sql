-- ============================================================================
-- ECOPARK — Migration 4 : une image pour chaque publication
--  1. Colonnes image_src / image_alt sur toutes les fiches publiables
--  2. Sources d'image autorisées (photothèque du site ou stockage Supabase, jamais javascript:)
--  3. Images par défaut des fiches déjà en ligne (photos actuelles du site)
--  4. Règle : aucune fiche ne peut être PUBLIÉE sans image (trigger, y compris via RPC)
--  5. RPC admin_duplicate / admin_set_status : l'image suit la copie et le remplacement
--  6. Espace de stockage « ecopark-media » (Supabase Storage) : lecture publique,
--     dépôt réservé à l'équipe éditoriale, JPEG / PNG / WebP, 5 Mo maximum
-- ============================================================================

-- 1. Colonnes
ALTER TABLE public.catalog_activities ADD COLUMN IF NOT EXISTS image_src TEXT, ADD COLUMN IF NOT EXISTS image_alt TEXT;
ALTER TABLE public.sales_bundles      ADD COLUMN IF NOT EXISTS image_src TEXT, ADD COLUMN IF NOT EXISTS image_alt TEXT;
ALTER TABLE public.lodge_cities       ADD COLUMN IF NOT EXISTS image_src TEXT, ADD COLUMN IF NOT EXISTS image_alt TEXT;
ALTER TABLE public.agenda_events      ADD COLUMN IF NOT EXISTS image_alt TEXT;
ALTER TABLE public.menu_items         ADD COLUMN IF NOT EXISTS image_alt TEXT;

-- 3. Images par défaut (avant les contraintes et le trigger)
UPDATE public.catalog_activities SET
  image_src = CASE slug
    WHEN 'zoo' THEN 'audit-assets/ecopark-real-media/chimpanze.jpeg'
    WHEN 'piscine' THEN 'audit-assets/stitch-canopee-vivante/local_cameroon_pool_pirogue.png'
    WHEN 'pirogue' THEN 'audit-assets/ecopark-real-media/balade_pirogue3.jpg'
    WHEN 'cheval' THEN 'audit-assets/stitch-canopee-vivante/local_cameroon_family_canopy.png'
    WHEN 'saveurs' THEN 'audit-assets/stitch-canopee-vivante/local_cameroon_gastronomy_pergola.png'
    WHEN 'nutrition_poissons' THEN 'audit-assets/ecopark-real-media/balade_pirogue3.jpg'
    WHEN 'pergola_lac' THEN 'audit-assets/stitch-canopee-vivante/local_cameroon_gastronomy_pergola.png'
    WHEN 'navette_yaounde' THEN 'audit-assets/ecopark-real-media/IMG-20260809-WA0009.jpg'
    ELSE 'audit-assets/stitch-canopee-vivante/local_cameroon_family_canopy.png' END,
  image_alt = CASE slug
    WHEN 'zoo' THEN 'Chimpanzé du jardin zoologique d''ECOPARK Ahala'
    WHEN 'piscine' THEN 'Piscine semi-olympique et lac d''Ahala'
    WHEN 'pirogue' THEN 'Balade en pirogue sur le lac d''Ahala'
    WHEN 'cheval' THEN 'Famille en promenade sous la canopée du parc'
    WHEN 'saveurs' THEN 'Repas camerounais sous les pergolas du Château des Saveurs'
    WHEN 'nutrition_poissons' THEN 'Lac et étangs d''Ahala'
    WHEN 'pergola_lac' THEN 'Pergola au bord du lac'
    WHEN 'navette_yaounde' THEN 'Groupe accueilli à ECOPARK Ahala'
    ELSE title END
WHERE image_src IS NULL;

UPDATE public.sales_bundles SET
  image_src = CASE bundle_code
    WHEN 'PASS_DECOUVERTE' THEN 'audit-assets/ecopark-real-media/chimpanze.jpeg'
    WHEN 'PASS_ROYALE' THEN 'audit-assets/ecopark-real-media/IMG-20260713-WA0051_043420.jpg'
    WHEN 'PACK_COUPLE_EWONDO' THEN 'audit-assets/ecopark-real-media/chambre.jpeg'
    ELSE 'audit-assets/stitch-canopee-vivante/local_cameroon_family_canopy.png' END,
  image_alt = CASE bundle_code
    WHEN 'PASS_DECOUVERTE' THEN 'Rencontre avec les animaux du jardin zoologique'
    WHEN 'PASS_ROYALE' THEN 'Grand dimanche au bord du lac d''Ahala'
    WHEN 'PACK_COUPLE_EWONDO' THEN 'Chambre de la Cité Ewondo'
    ELSE title END
WHERE image_src IS NULL;

UPDATE public.lodge_cities SET
  image_src = 'audit-assets/ecopark-real-media/chambre.jpeg',
  image_alt = 'Chambre de la ' || name
WHERE image_src IS NULL;

UPDATE public.agenda_events SET image_alt = short_label WHERE image_alt IS NULL;
UPDATE public.menu_items SET image_alt = name WHERE image_alt IS NULL;

-- 2. Sources autorisées : photothèque du site (audit-assets/...) ou URL https (stockage Supabase)
DO $$
DECLARE
  t TEXT;
BEGIN
  FOREACH t IN ARRAY ARRAY['catalog_activities','sales_bundles','lodge_cities','agenda_events','menu_items'] LOOP
    BEGIN
      EXECUTE format(
        'ALTER TABLE public.%1$I ADD CONSTRAINT chk_%1$s_image_src_safe CHECK (image_src IS NULL OR image_src ~ ''^(https://[A-Za-z0-9.-]+/|audit-assets/)[^"''''<>\s]*$'')', t);
    EXCEPTION WHEN duplicate_object THEN NULL;
    END;
    BEGIN
      EXECUTE format('ALTER TABLE public.%1$I ADD CONSTRAINT chk_%1$s_image_alt_len CHECK (image_alt IS NULL OR char_length(image_alt) <= 180)', t);
    EXCEPTION WHEN duplicate_object THEN NULL;
    END;
  END LOOP;
END $$;

-- 4. Pas de publication sans image
CREATE OR REPLACE FUNCTION public.ecopark_require_image_on_publish()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
  IF NEW.status = 'PUBLISHED' AND (NEW.image_src IS NULL OR btrim(NEW.image_src) = '') THEN
    RAISE EXCEPTION 'ECOPARK_IMAGE_REQUIRED' USING ERRCODE = '23514',
      HINT = 'Ajoutez une image à la fiche avant de la publier.';
  END IF;
  IF NEW.image_src IS NOT NULL AND (NEW.image_alt IS NULL OR btrim(NEW.image_alt) = '') THEN
    -- Texte alternatif par défaut (accessibilité) : le titre de la fiche
    NEW.image_alt := left(COALESCE(to_jsonb(NEW) ->> 'title', to_jsonb(NEW) ->> 'name', ''), 180);
  END IF;
  RETURN NEW;
END $$;

DO $$
DECLARE
  t TEXT;
BEGIN
  FOREACH t IN ARRAY ARRAY['catalog_activities','sales_bundles','lodge_cities','agenda_events','menu_items'] LOOP
    EXECUTE format('DROP TRIGGER IF EXISTS trg_%1$s_require_image ON public.%1$I', t);
    EXECUTE format('CREATE TRIGGER trg_%1$s_require_image BEFORE INSERT OR UPDATE ON public.%1$I
                    FOR EACH ROW EXECUTE FUNCTION public.ecopark_require_image_on_publish()', t);
  END LOOP;
END $$;

-- 5a. DUPLIQUER : l'image suit la copie (redéfinition complète de la RPC)
CREATE OR REPLACE FUNCTION public.admin_duplicate(p_entity TEXT, p_id UUID)
RETURNS UUID
LANGUAGE plpgsql SECURITY DEFINER SET search_path = public, pg_temp AS $$
DECLARE
  v_new UUID;
BEGIN
  PERFORM public.ecopark_assert_can_manage(p_entity, 'DUPLICATE');
  PERFORM set_config('ecopark.audit_op', 'DUPLICATE', TRUE);

  IF p_entity = 'catalog_activities' THEN
    INSERT INTO public.catalog_activities (slug, sku, title, pole, description, child_price_fcfa, adult_price_fcfa,
      group_adult_price_fcfa, group_child_price_fcfa, daily_capacity, image_src, image_alt, status, sort_order, duplicated_from)
    SELECT public.ecopark_unique_copy_value('public.catalog_activities', 'slug', slug, '-copie-'),
           public.ecopark_unique_copy_value('public.catalog_activities', 'sku', sku, '-COPIE-'),
           title || ' (Copie)', pole, description, child_price_fcfa, adult_price_fcfa,
           group_adult_price_fcfa, group_child_price_fcfa, daily_capacity, image_src, image_alt, 'DRAFT', sort_order + 1, id
      FROM public.catalog_activities WHERE id = p_id
    RETURNING id INTO v_new;

  ELSIF p_entity = 'sales_bundles' THEN
    INSERT INTO public.sales_bundles (bundle_code, sku, title, subtitle, included_slugs, adult_bundle_price_fcfa,
      child_bundle_price_fcfa, savings_label, is_featured, image_src, image_alt, status, sort_order, duplicated_from)
    SELECT public.ecopark_unique_copy_value('public.sales_bundles', 'bundle_code', bundle_code, '_COPIE_'),
           public.ecopark_unique_copy_value('public.sales_bundles', 'sku', sku, '-COPIE-'),
           title || ' (Copie)', subtitle, included_slugs, adult_bundle_price_fcfa,
           child_bundle_price_fcfa, savings_label, FALSE, image_src, image_alt, 'DRAFT', sort_order + 1, id
      FROM public.sales_bundles WHERE id = p_id
    RETURNING id INTO v_new;

  ELSIF p_entity = 'agenda_events' THEN
    INSERT INTO public.agenda_events (code, day_filter, target_weekday, badge, title, short_label, price_text,
      from_price_fcfa, spots_text, description, schedule, bundle_code, dish, meal_slot, pergola, nutrition,
      image_src, image_alt, status, sort_order, duplicated_from)
    SELECT public.ecopark_unique_copy_value('public.agenda_events', 'code', code, '_COPIE_'),
           day_filter, target_weekday, badge, title || ' (Copie)', short_label || ' (Copie)', price_text,
           from_price_fcfa, spots_text, description, schedule, bundle_code, dish, meal_slot, pergola, nutrition,
           image_src, image_alt, 'DRAFT', sort_order + 1, id
      FROM public.agenda_events WHERE id = p_id
    RETURNING id INTO v_new;

  ELSIF p_entity = 'menu_items' THEN
    INSERT INTO public.menu_items (sku, category, name, description, price_fcfa, is_signature, in_stock,
      preorder_enabled, image_src, image_alt, status, sort_order, duplicated_from)
    SELECT public.ecopark_unique_copy_value('public.menu_items', 'sku', sku, '-COPIE-'),
           category, name || ' (Copie)', description, price_fcfa, is_signature, in_stock,
           preorder_enabled, image_src, image_alt, 'DRAFT', sort_order + 1, id
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

-- 5b. PUBLIER EN REMPLACEMENT : l'image de la version de travail remplace celle en ligne
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
        daily_capacity = d.daily_capacity, image_src = d.image_src, image_alt = d.image_alt
      FROM public.catalog_activities d WHERE d.id = p_id AND o.id = v_origin;
    ELSIF p_entity = 'sales_bundles' THEN
      UPDATE public.sales_bundles o SET
        title = regexp_replace(d.title, '\s*\(Copie\)$', ''), subtitle = d.subtitle,
        included_slugs = d.included_slugs, adult_bundle_price_fcfa = d.adult_bundle_price_fcfa,
        child_bundle_price_fcfa = d.child_bundle_price_fcfa, savings_label = d.savings_label,
        image_src = d.image_src, image_alt = d.image_alt
      FROM public.sales_bundles d WHERE d.id = p_id AND o.id = v_origin;
    ELSIF p_entity = 'agenda_events' THEN
      UPDATE public.agenda_events o SET
        day_filter = d.day_filter, target_weekday = d.target_weekday, badge = d.badge,
        title = regexp_replace(d.title, '\s*\(Copie\)$', ''),
        short_label = regexp_replace(d.short_label, '\s*\(Copie\)$', ''),
        price_text = d.price_text, from_price_fcfa = d.from_price_fcfa, spots_text = d.spots_text,
        description = d.description, schedule = d.schedule, bundle_code = d.bundle_code, dish = d.dish,
        meal_slot = d.meal_slot, pergola = d.pergola, nutrition = d.nutrition,
        image_src = d.image_src, image_alt = d.image_alt
      FROM public.agenda_events d WHERE d.id = p_id AND o.id = v_origin;
    ELSIF p_entity = 'menu_items' THEN
      UPDATE public.menu_items o SET
        category = d.category, name = regexp_replace(d.name, '\s*\(Copie\)$', ''), description = d.description,
        price_fcfa = d.price_fcfa, is_signature = d.is_signature, in_stock = d.in_stock,
        preorder_enabled = d.preorder_enabled, image_src = d.image_src, image_alt = d.image_alt
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

-- 6. Stockage des images (Supabase Storage uniquement ; sans effet ailleurs)
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'storage' AND table_name = 'buckets') THEN
    RAISE NOTICE 'Supabase Storage absent : espace ecopark-media non créé (environnement de test).';
    RETURN;
  END IF;

  INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
  VALUES ('ecopark-media', 'ecopark-media', TRUE, 5242880, ARRAY['image/jpeg', 'image/png', 'image/webp'])
  ON CONFLICT (id) DO UPDATE SET public = TRUE, file_size_limit = 5242880,
    allowed_mime_types = ARRAY['image/jpeg', 'image/png', 'image/webp'];

  EXECUTE 'DROP POLICY IF EXISTS "ecopark_media_public_read" ON storage.objects';
  EXECUTE 'CREATE POLICY "ecopark_media_public_read" ON storage.objects FOR SELECT
           USING (bucket_id = ''ecopark-media'')';
  EXECUTE 'DROP POLICY IF EXISTS "ecopark_media_editor_insert" ON storage.objects';
  EXECUTE 'CREATE POLICY "ecopark_media_editor_insert" ON storage.objects FOR INSERT TO authenticated
           WITH CHECK (bucket_id = ''ecopark-media'' AND public.ecopark_is_content_editor())';
  EXECUTE 'DROP POLICY IF EXISTS "ecopark_media_editor_update" ON storage.objects';
  EXECUTE 'CREATE POLICY "ecopark_media_editor_update" ON storage.objects FOR UPDATE TO authenticated
           USING (bucket_id = ''ecopark-media'' AND public.ecopark_is_content_editor())';
  EXECUTE 'DROP POLICY IF EXISTS "ecopark_media_governance_delete" ON storage.objects';
  EXECUTE 'CREATE POLICY "ecopark_media_governance_delete" ON storage.objects FOR DELETE TO authenticated
           USING (bucket_id = ''ecopark-media'' AND public.ecopark_is_governance())';
END $$;
