-- ============================================================================
-- ECOPARK CAMEROUN (Yaoundé-Ahala) — Migration 6 :
--   1. 8e Rôle Utilisateur « comptable » & Rattachement Pôle/Matricule (ADM-05)
--   2. Notation Objective (/60) + Managériale (/40) des Agents de Terrain au Visa #3
--   3. RPC de Comptabilité Générale SYSCOHADA & Comptabilité Analytique (6 Pôles)
-- ============================================================================

-- 1. Ajout idempotent du 8e rôle « comptable » dans l'énumération ecopark_role
ALTER TYPE public.ecopark_role ADD VALUE IF NOT EXISTS 'comptable';

-- 2. Enrichissement de public.staff_profiles (Matricule & Pôle d'affectation)
ALTER TABLE public.staff_profiles
  ADD COLUMN IF NOT EXISTS matricule TEXT NOT NULL DEFAULT 'MAT-EXP-01',
  ADD COLUMN IF NOT EXISTS assigned_pole TEXT NOT NULL DEFAULT 'GUICHET_CAISSE';

DO $$ BEGIN
  ALTER TABLE public.staff_profiles
    ADD CONSTRAINT chk_staff_profiles_assigned_pole
    CHECK (assigned_pole IN (
      'GUICHET_CAISSE',
      'CONTROLE_QR',
      'HEBERGEMENT',
      'CUISINE_SAVEURS',
      'FINANCE_COMPTA',
      'DIRECTION_GENERALE'
    ));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

-- 3. Mise à jour des fonctions d'habilitation pour inclure le Comptable (lecture seule financière)
--    Note : LANGUAGE plpgsql permet d'exécuter ALTER TYPE ... ADD VALUE et CREATE FUNCTION
--    dans le même bloc de migration sans erreur 55P04 (check_safe_enum_use).
CREATE OR REPLACE FUNCTION public.ecopark_is_staff()
RETURNS BOOLEAN LANGUAGE plpgsql STABLE AS $$
BEGIN
  RETURN public.ecopark_has_role(ARRAY[
    'agent_guichet',
    'agent_controle',
    'comptable',
    'responsable_exploitation',
    'direction',
    'administrateur_plateforme'
  ]::ecopark_role[]);
END $$;

CREATE OR REPLACE FUNCTION public.ecopark_is_accountant_or_editor()
RETURNS BOOLEAN LANGUAGE plpgsql STABLE AS $$
BEGIN
  RETURN public.ecopark_has_role(ARRAY[
    'comptable',
    'responsable_exploitation',
    'direction',
    'administrateur_plateforme'
  ]::ecopark_role[]);
END $$;

CREATE OR REPLACE FUNCTION public.ecopark_is_accountant_or_governance()
RETURNS BOOLEAN LANGUAGE plpgsql STABLE AS $$
BEGIN
  RETURN public.ecopark_has_role(ARRAY[
    'comptable',
    'direction',
    'administrateur_plateforme'
  ]::ecopark_role[]);
END $$;

-- Mise à jour de get_my_profile() pour exposer matricule et assigned_pole
CREATE OR REPLACE FUNCTION public.get_my_profile()
RETURNS JSONB
LANGUAGE sql STABLE SECURITY DEFINER SET search_path = public, pg_temp AS $$
  SELECT jsonb_build_object(
    'user_id', auth.uid(),
    'role', public.current_ecopark_role(),
    'full_name', sp.full_name,
    'matricule', sp.matricule,
    'assigned_pole', sp.assigned_pole,
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

-- Politiques RLS : le comptable lit les devis B2B, les dossiers CFP, les RDV et le journal d'audit,
-- mais ne peut modifier aucun tarif ni aucun dossier opérationnel.
DO $$
DECLARE
  t TEXT;
BEGIN
  FOREACH t IN ARRAY ARRAY['group_quotes','cfp_applications','appointments'] LOOP
    EXECUTE format('DROP POLICY IF EXISTS "%1$s_ops_read" ON public.%1$I', t);
    EXECUTE format('CREATE POLICY "%1$s_ops_read" ON public.%1$I
                    FOR SELECT TO authenticated USING (public.ecopark_is_accountant_or_editor())', t);
  END LOOP;
END $$;

DROP POLICY IF EXISTS "audit_logs_governance_read" ON public.audit_logs;
CREATE POLICY "audit_logs_governance_read" ON public.audit_logs
  FOR SELECT TO authenticated USING (public.ecopark_is_accountant_or_governance());

-- ============================================================================
-- 4. COLONNES DE NOTATION DES AGENTS DE TERRAIN SUR public.operational_missions
-- ============================================================================
ALTER TABLE public.operational_missions
  ADD COLUMN IF NOT EXISTS rating_auto_60 INTEGER NOT NULL DEFAULT 0 CHECK (rating_auto_60 BETWEEN 0 AND 60),
  ADD COLUMN IF NOT EXISTS rating_supervisor_40 INTEGER NOT NULL DEFAULT 0 CHECK (rating_supervisor_40 BETWEEN 0 AND 40),
  ADD COLUMN IF NOT EXISTS rating_total_100 INTEGER NOT NULL DEFAULT 0 CHECK (rating_total_100 BETWEEN 0 AND 100),
  ADD COLUMN IF NOT EXISTS rating_stars NUMERIC(2,1) NOT NULL DEFAULT 0.0 CHECK (rating_stars BETWEEN 0.0 AND 5.0),
  ADD COLUMN IF NOT EXISTS rating_comment TEXT NOT NULL DEFAULT '',
  ADD COLUMN IF NOT EXISTS rated_at TIMESTAMPTZ,
  ADD COLUMN IF NOT EXISTS rated_by TEXT;

UPDATE public.operational_missions
   SET rating_auto_60 = 58,
       rating_supervisor_40 = 38,
       rating_total_100 = 96,
       rating_stars = 4.8,
       rating_comment = 'Mise en place braises exemplaire et service 13h00 sans attente.',
       rated_at = COALESCE(rated_at, NOW()),
       rated_by = COALESCE(rated_by, 'Chef d''Exploitation Ahala')
 WHERE mission_ref = 'MSN-2026-104' AND rating_total_100 = 0;

-- ============================================================================
-- 5. RPC : CLÔTURE VISA #3 & NOTATION SUR 100 POINTS (rate_mission_on_visa3)
-- ============================================================================
CREATE OR REPLACE FUNCTION public.rate_mission_on_visa3(
  p_mission_ref TEXT,
  p_supervisor_40 INTEGER DEFAULT 36,
  p_comment TEXT DEFAULT '',
  p_cash_gap_fcfa INTEGER DEFAULT 0,
  p_actor_name TEXT DEFAULT NULL
) RETURNS JSONB
LANGUAGE plpgsql SECURITY DEFINER SET search_path = public, pg_temp AS $$
DECLARE
  v_row public.operational_missions%ROWTYPE;
  v_visas JSONB;
  v_checklist JSONB;
  v_actor TEXT;
  v_stamp TEXT := to_char(NOW() AT TIME ZONE 'Africa/Douala', 'DD/MM/YYYY HH24:MI');
  v_total_items INTEGER := 0;
  v_done_items INTEGER := 0;
  v_pts_punctuality INTEGER := 20;
  v_pts_checklist INTEGER := 20;
  v_pts_compliance INTEGER := 20;
  v_auto_60 INTEGER;
  v_sup_40 INTEGER;
  v_total_100 INTEGER;
  v_stars NUMERIC(2,1);
BEGIN
  IF NOT public.ecopark_is_content_editor() THEN
    RAISE EXCEPTION 'ECOPARK_VISA_REQUIRES_EXPLOITATION'
      USING ERRCODE = '42501',
            HINT = 'Seul le Chef d''Exploitation ou la Direction peut clôturer le Visa #3 et noter un agent de terrain.';
  END IF;

  SELECT * INTO v_row FROM public.operational_missions WHERE mission_ref = p_mission_ref FOR UPDATE;
  IF NOT FOUND THEN
    RAISE EXCEPTION 'ECOPARK_NOT_FOUND' USING ERRCODE = 'P0002';
  END IF;

  v_actor := COALESCE(
    NULLIF(btrim(p_actor_name), ''),
    (SELECT full_name FROM public.staff_profiles WHERE user_id = auth.uid()),
    v_row.assigned_by
  );

  -- Calcul du score automatique sur 60 points :
  -- 1) Ponctualité & réactivité (20 pts)
  v_pts_punctuality := 20;
  -- 2) Exécution de la check-list (20 pts)
  SELECT count(*)::int, count(*) FILTER (WHERE COALESCE((elem ->> 'done')::boolean, FALSE))::int
    INTO v_total_items, v_done_items
    FROM jsonb_array_elements(COALESCE(v_row.checklist, '[]'::jsonb)) elem;
  IF v_total_items > 0 THEN
    -- À la clôture Visa #3, si au moins la moitié était déjà pointée en cours de poste : 20/20, sinon prorata min 14/20
    v_pts_checklist := GREATEST(14, round((v_done_items::numeric / v_total_items::numeric) * 20)::int);
    IF v_done_items = v_total_items THEN
      v_pts_checklist := 20;
    END IF;
  END IF;
  -- 3) Conformité caisse / dotation matériel (20 pts)
  IF abs(COALESCE(p_cash_gap_fcfa, 0)) = 0 THEN
    v_pts_compliance := 20;
  ELSIF abs(COALESCE(p_cash_gap_fcfa, 0)) <= 2000 THEN
    v_pts_compliance := 10;
  ELSE
    v_pts_compliance := 0;
  END IF;

  v_auto_60 := LEAST(60, GREATEST(0, v_pts_punctuality + v_pts_checklist + v_pts_compliance));
  v_sup_40  := LEAST(40, GREATEST(0, COALESCE(p_supervisor_40, 36)));
  v_total_100 := v_auto_60 + v_sup_40;
  v_stars := round((v_total_100::numeric / 20.0), 1);

  v_visas := COALESCE(v_row.visas, '{}'::jsonb);
  IF NOT (v_visas ? 'visa1') THEN
    v_visas := jsonb_set(v_visas, '{visa1}', jsonb_build_object('signed', TRUE, 'actor', v_row.assigned_by, 'timestamp', v_stamp));
  END IF;
  IF NOT COALESCE((v_visas -> 'visa2' ->> 'signed')::boolean, FALSE) THEN
    v_visas := jsonb_set(v_visas, '{visa2}', jsonb_build_object('signed', TRUE, 'actor', v_row.agent_name || ' (' || v_row.agent_matricule || ')', 'timestamp', v_stamp));
  END IF;
  v_visas := jsonb_set(v_visas, '{visa3}', jsonb_build_object('signed', TRUE, 'actor', v_actor, 'timestamp', v_stamp));

  SELECT COALESCE(jsonb_agg(jsonb_set(elem, '{done}', 'true'::jsonb)), '[]'::jsonb)
    INTO v_checklist
    FROM jsonb_array_elements(COALESCE(v_row.checklist, '[]'::jsonb)) elem;

  PERFORM set_config('ecopark.audit_op', 'VISA_VISA3', TRUE);
  UPDATE public.operational_missions
     SET visas = v_visas,
         status = 'TERMINEE',
         checklist = v_checklist,
         rating_auto_60 = v_auto_60,
         rating_supervisor_40 = v_sup_40,
         rating_total_100 = v_total_100,
         rating_stars = v_stars,
         rating_comment = COALESCE(NULLIF(btrim(p_comment), ''), 'Clôture contradictoire conforme.'),
         rated_at = NOW(),
         rated_by = v_actor
   WHERE id = v_row.id
   RETURNING * INTO v_row;
  PERFORM set_config('ecopark.audit_op', '', TRUE);

  RETURN to_jsonb(v_row);
END $$;

-- Enrichir sign_mission_visa pour renseigner automatiquement la notation par défaut au Visa #3
CREATE OR REPLACE FUNCTION public.sign_mission_visa(
  p_mission_ref TEXT,
  p_visa_key TEXT,
  p_actor_name TEXT DEFAULT NULL
) RETURNS JSONB
LANGUAGE plpgsql SECURITY DEFINER SET search_path = public, pg_temp AS $$
DECLARE
  v_row public.operational_missions%ROWTYPE;
  v_visas JSONB;
  v_checklist JSONB;
  v_status TEXT;
  v_actor TEXT;
  v_stamp TEXT := to_char(NOW() AT TIME ZONE 'Africa/Douala', 'DD/MM/YYYY HH24:MI');
BEGIN
  IF NOT public.ecopark_is_staff() THEN
    RAISE EXCEPTION 'ECOPARK_FORBIDDEN'
      USING ERRCODE = '42501',
            HINT = 'Seul un membre habilité de l''équipe ECOPARK peut émarger une Fiche de Mission A4.';
  END IF;

  IF p_visa_key NOT IN ('visa1', 'visa2', 'visa3') THEN
    RAISE EXCEPTION 'ECOPARK_INVALID_VISA_KEY'
      USING ERRCODE = '22023',
            HINT = 'Clé de visa attendue : visa1, visa2 ou visa3.';
  END IF;

  IF p_visa_key IN ('visa1', 'visa3') AND NOT public.ecopark_is_content_editor() THEN
    RAISE EXCEPTION 'ECOPARK_VISA_REQUIRES_EXPLOITATION'
      USING ERRCODE = '42501',
            HINT = 'Les Visas #1 (Émission) et #3 (Clôture & Dotation) relèvent exclusivement du Chef d''Exploitation ou de la Direction.';
  END IF;

  IF p_visa_key = 'visa3' THEN
    RETURN public.rate_mission_on_visa3(p_mission_ref, 36, 'Clôture contradictoire conforme.', 0, p_actor_name);
  END IF;

  SELECT * INTO v_row FROM public.operational_missions WHERE mission_ref = p_mission_ref FOR UPDATE;
  IF NOT FOUND THEN
    RAISE EXCEPTION 'ECOPARK_NOT_FOUND' USING ERRCODE = 'P0002';
  END IF;

  v_actor := COALESCE(
    NULLIF(btrim(p_actor_name), ''),
    (SELECT full_name FROM public.staff_profiles WHERE user_id = auth.uid()),
    CASE WHEN p_visa_key = 'visa2' THEN v_row.agent_name || ' (' || v_row.agent_matricule || ')'
         ELSE v_row.assigned_by END
  );

  v_visas := COALESCE(v_row.visas, '{}'::jsonb);
  IF NOT (v_visas ? 'visa1') THEN
    v_visas := jsonb_set(v_visas, '{visa1}', jsonb_build_object('signed', TRUE, 'actor', v_row.assigned_by, 'timestamp', v_stamp));
  END IF;

  v_status := v_row.status;
  v_checklist := v_row.checklist;

  IF p_visa_key = 'visa1' THEN
    v_visas := jsonb_set(v_visas, '{visa1}', jsonb_build_object('signed', TRUE, 'actor', v_actor, 'timestamp', v_stamp));
  ELSIF p_visa_key = 'visa2' THEN
    v_visas := jsonb_set(v_visas, '{visa2}', jsonb_build_object('signed', TRUE, 'actor', v_actor, 'timestamp', v_stamp));
    IF v_status = 'ASSIGNEE' THEN
      v_status := 'EN_COURS';
    END IF;
  END IF;

  PERFORM set_config('ecopark.audit_op', 'VISA_' || upper(p_visa_key), TRUE);
  UPDATE public.operational_missions
     SET visas = v_visas,
         status = v_status,
         checklist = v_checklist
   WHERE id = v_row.id
   RETURNING * INTO v_row;
  PERFORM set_config('ecopark.audit_op', '', TRUE);

  RETURN to_jsonb(v_row);
END $$;

-- ============================================================================
-- 6. RPC : GRAND-LIVRE ANALYTIQUE PAR CENTRE DE PROFIT (6 AXES ANA-01 à ANA-06)
-- ============================================================================
CREATE OR REPLACE FUNCTION public.get_analytical_accounting_ledger(
  p_date_from DATE DEFAULT NULL,
  p_date_to DATE DEFAULT NULL
) RETURNS TABLE (
  analytical_code TEXT,
  pole_code TEXT,
  pole_label TEXT,
  ohada_account TEXT,
  transactions_count BIGINT,
  net_revenue_fcfa BIGINT
)
LANGUAGE plpgsql STABLE SECURITY DEFINER SET search_path = public, pg_temp AS $$
BEGIN
  IF NOT public.ecopark_is_accountant_or_editor() THEN
    RAISE EXCEPTION 'ECOPARK_FORBIDDEN'
      USING ERRCODE = '42501',
            HINT = 'Accès réservé au Comptable, à l''Exploitation et à la Direction.';
  END IF;

  RETURN QUERY
  WITH axes AS (
    SELECT 'ANA-01'::text AS a_code, 'NATURE_FAUNE'::text AS p_code, 'Nature, Faune & Jardin Zoologique'::text AS p_label, '7061'::text AS ohada, 1 AS ord
    UNION ALL SELECT 'ANA-02', 'EAU_PLEIN_AIR', 'Eau, Piscine Semi-Olympique & Lac', '7062', 2
    UNION ALL SELECT 'ANA-03', 'RESTAURATION', 'Restaurant Le Château des Saveurs & Pergolas', '7011/7063', 3
    UNION ALL SELECT 'ANA-04', 'HEBERGEMENT', 'Cités Hôtelières (Bene, Chanthel, Ewondo VIP)', '7064', 4
    UNION ALL SELECT 'ANA-05', 'GROUPES_B2B', 'Groupes, Salle Menkii (500 pl.) & Navettes', '7065', 5
    UNION ALL SELECT 'ANA-06', 'FORMATION_CFP', 'Campus CFP Agréé MINEFOP (5 filières)', '7066', 6
  ),
  entries AS (
    -- Réservations hébergement
    SELECT 'HEBERGEMENT'::text AS p_code, b.total_fcfa::bigint AS amt
      FROM public.bookings b
     WHERE b.cancelled_at IS NULL AND b.payment_state = 'CONFIRMED'
       AND b.lodge_city IS NOT NULL
       AND (p_date_from IS NULL OR b.visit_date >= p_date_from)
       AND (p_date_to IS NULL OR b.visit_date <= p_date_to)
    UNION ALL
    -- Réservations journée (ventilées sur Restauration si repas/pergola, Eau si piscine/pirogue, sinon Nature)
    SELECT CASE
             WHEN 'saveurs' = ANY(b.selected_activities) OR b.pergola_reserved OR b.has_pergola THEN 'RESTAURATION'
             WHEN 'piscine' = ANY(b.selected_activities) OR 'pirogue' = ANY(b.selected_activities) THEN 'EAU_PLEIN_AIR'
             ELSE 'NATURE_FAUNE'
           END AS p_code,
           b.total_fcfa::bigint AS amt
      FROM public.bookings b
     WHERE b.cancelled_at IS NULL AND b.payment_state = 'CONFIRMED'
       AND b.lodge_city IS NULL
       AND (p_date_from IS NULL OR b.visit_date >= p_date_from)
       AND (p_date_to IS NULL OR b.visit_date <= p_date_to)
    UNION ALL
    -- Devis groupes B2B validés
    SELECT 'GROUPES_B2B'::text AS p_code, q.estimated_budget_fcfa::bigint AS amt
      FROM public.group_quotes q
     WHERE q.status = 'VALIDE'
       AND (p_date_from IS NULL OR q.preferred_date >= p_date_from)
       AND (p_date_to IS NULL OR q.preferred_date <= p_date_to)
    UNION ALL
    -- Candidatures CFP réglées ou admises
    SELECT 'FORMATION_CFP'::text AS p_code, c.registration_fee_fcfa::bigint AS amt
      FROM public.cfp_applications c
     WHERE c.status IN ('INSCRIPTION_REGLEE', 'ADMIS')
  )
  SELECT ax.a_code, ax.p_code, ax.p_label, ax.ohada,
         COUNT(e.amt)::bigint AS transactions_count,
         COALESCE(SUM(e.amt), 0)::bigint AS net_revenue_fcfa
    FROM axes ax
    LEFT JOIN entries e ON e.p_code = ax.p_code
   GROUP BY ax.a_code, ax.p_code, ax.p_label, ax.ohada, ax.ord
   ORDER BY ax.ord;
END $$;

DO $$ BEGIN
  REVOKE EXECUTE ON FUNCTION public.rate_mission_on_visa3(TEXT, INTEGER, TEXT, INTEGER, TEXT) FROM PUBLIC, anon;
  REVOKE EXECUTE ON FUNCTION public.get_analytical_accounting_ledger(DATE, DATE) FROM PUBLIC, anon;
  GRANT EXECUTE ON FUNCTION public.rate_mission_on_visa3(TEXT, INTEGER, TEXT, INTEGER, TEXT) TO authenticated;
  GRANT EXECUTE ON FUNCTION public.get_analytical_accounting_ledger(DATE, DATE) TO authenticated;
EXCEPTION WHEN undefined_object THEN NULL; END $$;
