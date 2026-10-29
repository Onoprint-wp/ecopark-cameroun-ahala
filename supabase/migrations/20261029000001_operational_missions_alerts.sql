-- ============================================================================
-- ECOPARK CAMEROUN (Yaoundé-Ahala) — Migration 5 : Fiches de Mission A4,
-- Gouvernance des 3 Visas Interactifs & Centre d'Alertes de Poste Temps Réel
--
--  1. Table public.operational_missions (Règle « 1 Commande = 1 Fiche de Mission
--     selon l'affectation du poste », check-list terrain et 3 Visas d'émargement)
--  2. Table public.operational_alerts (Notifications temps réel par pôle avec
--     acquittement « J'ai pris en charge »)
--  3. RPC public.sign_mission_visa(p_mission_ref, p_visa_key, p_actor_name) :
--     application stricte de la Matrice des Approbations :
--       - Visa #1 (Émission Exploitation) & Visa #3 (Clôture & Remise Dotation) :
--         réservés à responsable_exploitation, direction, administrateur_plateforme
--       - Visa #2 (Émargement Prise de Poste Agent) : ouvert à toute l'équipe
--         terrain (agent_guichet, agent_controle, exploitation, direction, admin)
--  4. RPC public.acknowledge_operational_alert(p_alert_ref) : acquittement temps
--     réel et bascule automatique de la mission en « EN_COURS » avec Visa #2
--  5. Triggers d'audit SHA-256 (audit_row_change), RLS par rôle et Realtime
-- ============================================================================

-- ============================================================================
-- 1. TABLE DES FICHES DE MISSION OPÉRATIONNELLES A4 (public.operational_missions)
-- ============================================================================
CREATE TABLE IF NOT EXISTS public.operational_missions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  mission_ref TEXT NOT NULL UNIQUE,               -- ex : MSN-2026-101
  order_ref TEXT,                                 -- ex : EPK-2026-8841, DEV-2026-312, CFP-2026-109, POS-2026-10421
  order_customer TEXT NOT NULL DEFAULT 'Exploitation ECOPARK',
  order_total_fcfa INTEGER NOT NULL DEFAULT 0 CHECK (order_total_fcfa >= 0),
  order_summary TEXT NOT NULL DEFAULT '',
  pole TEXT NOT NULL CHECK (pole IN ('GUICHET_CAISSE', 'CONTROLE_QR', 'HEBERGEMENT', 'CUISINE_SAVEURS')),
  pole_label TEXT NOT NULL,
  badge_class TEXT NOT NULL DEFAULT 'eco-cat-nature',
  secondary_poles TEXT[] NOT NULL DEFAULT '{}',
  agent_name TEXT NOT NULL,
  agent_matricule TEXT NOT NULL,
  agent_role TEXT NOT NULL,
  mission_date DATE NOT NULL DEFAULT CURRENT_DATE,
  shift_label TEXT NOT NULL,
  priority TEXT NOT NULL DEFAULT 'NORMALE' CHECK (priority IN ('NORMALE', 'HAUTE', 'URGENTE')),
  status TEXT NOT NULL DEFAULT 'ASSIGNEE' CHECK (status IN ('ASSIGNEE', 'EN_COURS', 'TERMINEE')),
  title TEXT NOT NULL,
  location TEXT NOT NULL,
  objective TEXT NOT NULL,
  equipment TEXT NOT NULL DEFAULT '',
  guardrail TEXT NOT NULL DEFAULT '',
  checklist JSONB NOT NULL DEFAULT '[]'::jsonb CHECK (jsonb_typeof(checklist) = 'array'),
  visas JSONB NOT NULL DEFAULT '{}'::jsonb CHECK (jsonb_typeof(visas) = 'object'),
  assigned_by TEXT NOT NULL DEFAULT 'Chef d''Exploitation Ahala',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_by UUID,
  version INTEGER NOT NULL DEFAULT 1
);

CREATE INDEX IF NOT EXISTS idx_operational_missions_pole ON public.operational_missions (pole, status);
CREATE INDEX IF NOT EXISTS idx_operational_missions_order_ref ON public.operational_missions (order_ref);

-- ============================================================================
-- 2. TABLE DES ALERTES DE POSTE TEMPS RÉEL (public.operational_alerts)
-- ============================================================================
CREATE TABLE IF NOT EXISTS public.operational_alerts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  alert_ref TEXT NOT NULL UNIQUE,                 -- ex : ALT-2026-201
  mission_ref TEXT NOT NULL REFERENCES public.operational_missions(mission_ref) ON DELETE CASCADE,
  order_ref TEXT,
  customer_name TEXT NOT NULL,
  order_summary TEXT NOT NULL DEFAULT '',
  amount_fcfa INTEGER NOT NULL DEFAULT 0 CHECK (amount_fcfa >= 0),
  pole TEXT NOT NULL CHECK (pole IN ('GUICHET_CAISSE', 'CONTROLE_QR', 'HEBERGEMENT', 'CUISINE_SAVEURS')),
  pole_label TEXT NOT NULL,
  badge_class TEXT NOT NULL DEFAULT 'eco-cat-nature',
  agent_name TEXT NOT NULL,
  agent_matricule TEXT NOT NULL,
  title TEXT NOT NULL,
  acknowledged BOOLEAN NOT NULL DEFAULT FALSE,
  acknowledged_at TIMESTAMPTZ,
  acknowledged_by TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_by UUID,
  version INTEGER NOT NULL DEFAULT 1
);

CREATE INDEX IF NOT EXISTS idx_operational_alerts_unread ON public.operational_alerts (acknowledged, pole);

-- ============================================================================
-- 3. TRIGGERS DE VERSIONING & JOURNAL D'AUDIT IMMUABLE SHA-256
-- ============================================================================
CREATE OR REPLACE FUNCTION public.ecopark_touch_operational_row()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
  NEW.updated_at := NOW();
  NEW.updated_by := auth.uid();
  IF TG_OP = 'INSERT' THEN
    NEW.version := 1;
  ELSE
    NEW.version := COALESCE(OLD.version, 0) + 1;
  END IF;
  RETURN NEW;
END $$;

DROP TRIGGER IF EXISTS trg_operational_missions_touch ON public.operational_missions;
CREATE TRIGGER trg_operational_missions_touch
  BEFORE INSERT OR UPDATE ON public.operational_missions
  FOR EACH ROW EXECUTE FUNCTION public.ecopark_touch_operational_row();

DROP TRIGGER IF EXISTS trg_operational_missions_audit ON public.operational_missions;
CREATE TRIGGER trg_operational_missions_audit
  AFTER INSERT OR UPDATE OR DELETE ON public.operational_missions
  FOR EACH ROW EXECUTE FUNCTION public.audit_row_change();

DROP TRIGGER IF EXISTS trg_operational_alerts_touch ON public.operational_alerts;
CREATE TRIGGER trg_operational_alerts_touch
  BEFORE INSERT OR UPDATE ON public.operational_alerts
  FOR EACH ROW EXECUTE FUNCTION public.ecopark_touch_operational_row();

DROP TRIGGER IF EXISTS trg_operational_alerts_audit ON public.operational_alerts;
CREATE TRIGGER trg_operational_alerts_audit
  AFTER INSERT OR UPDATE OR DELETE ON public.operational_alerts
  FOR EACH ROW EXECUTE FUNCTION public.audit_row_change();

-- ============================================================================
-- 4. RPC DE SIGNATURE INTERACTIVE DES 3 VISAS (Matrice des Approbations)
-- ============================================================================
CREATE OR REPLACE FUNCTION public.sign_mission_visa(
  p_mission_ref TEXT,
  p_visa_key TEXT,
  p_actor_name TEXT DEFAULT NULL
) RETURNS JSONB
LANGUAGE plpgsql SECURITY DEFINER SET search_path = public, pg_temp AS $$
DECLARE
  v_role ecopark_role := public.current_ecopark_role();
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

  -- Règle de gouvernance (Matrice des 6 Processus) :
  -- Visa #1 (Émission Responsable Exploitation) et Visa #3 (Clôture & Remise Dotation)
  -- exigent le rôle responsable_exploitation, direction ou administrateur_plateforme.
  IF p_visa_key IN ('visa1', 'visa3') AND NOT public.ecopark_is_content_editor() THEN
    RAISE EXCEPTION 'ECOPARK_VISA_REQUIRES_EXPLOITATION'
      USING ERRCODE = '42501',
            HINT = 'Les Visas #1 (Émission) et #3 (Clôture & Dotation) relèvent exclusivement du Chef d''Exploitation ou de la Direction.';
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
    v_visas := jsonb_set(v_visas, '{visa1}', jsonb_build_object(
      'signed', TRUE,
      'actor', v_row.assigned_by,
      'timestamp', v_stamp
    ));
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
  ELSIF p_visa_key = 'visa3' THEN
    IF NOT COALESCE((v_visas -> 'visa2' ->> 'signed')::boolean, FALSE) THEN
      v_visas := jsonb_set(v_visas, '{visa2}', jsonb_build_object(
        'signed', TRUE,
        'actor', v_row.agent_name || ' (' || v_row.agent_matricule || ')',
        'timestamp', v_stamp
      ));
    END IF;
    v_visas := jsonb_set(v_visas, '{visa3}', jsonb_build_object('signed', TRUE, 'actor', v_actor, 'timestamp', v_stamp));
    v_status := 'TERMINEE';
    -- Cocher tous les points de contrôle à la clôture contradictoire
    SELECT COALESCE(jsonb_agg(jsonb_set(elem, '{done}', 'true'::jsonb)), '[]'::jsonb)
      INTO v_checklist
      FROM jsonb_array_elements(COALESCE(v_row.checklist, '[]'::jsonb)) elem;
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
-- 5. RPC D'ACQUITTEMENT D'UNE ALERTE DE POSTE (public.acknowledge_operational_alert)
-- ============================================================================
CREATE OR REPLACE FUNCTION public.acknowledge_operational_alert(
  p_alert_ref TEXT
) RETURNS JSONB
LANGUAGE plpgsql SECURITY DEFINER SET search_path = public, pg_temp AS $$
DECLARE
  v_alert public.operational_alerts%ROWTYPE;
  v_actor TEXT;
BEGIN
  IF NOT public.ecopark_is_staff() THEN
    RAISE EXCEPTION 'ECOPARK_FORBIDDEN'
      USING ERRCODE = '42501',
            HINT = 'Seul un membre de l''équipe ECOPARK peut acquitter une alerte de poste.';
  END IF;

  SELECT * INTO v_alert FROM public.operational_alerts WHERE alert_ref = p_alert_ref FOR UPDATE;
  IF NOT FOUND THEN
    RAISE EXCEPTION 'ECOPARK_NOT_FOUND' USING ERRCODE = 'P0002';
  END IF;

  v_actor := COALESCE(
    (SELECT full_name FROM public.staff_profiles WHERE user_id = auth.uid()),
    v_alert.agent_name
  );

  PERFORM set_config('ecopark.audit_op', 'ACK_ALERT', TRUE);
  UPDATE public.operational_alerts
     SET acknowledged = TRUE,
         acknowledged_at = NOW(),
         acknowledged_by = v_actor
   WHERE id = v_alert.id
   RETURNING * INTO v_alert;

  -- Bascule automatique de la mission rattachée en « EN_COURS » + émargement Visa #2
  PERFORM public.sign_mission_visa(v_alert.mission_ref, 'visa2', v_actor);
  PERFORM set_config('ecopark.audit_op', '', TRUE);

  RETURN to_jsonb(v_alert);
END $$;

-- ============================================================================
-- 6. POLITIQUES RLS & DROITS D'EXÉCUTION
-- ============================================================================
ALTER TABLE public.operational_missions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.operational_alerts ENABLE ROW LEVEL SECURITY;

-- Lecture réservée aux membres de l'équipe opérationnelle (aucun accès visiteur anonyme)
DROP POLICY IF EXISTS "operational_missions_staff_read" ON public.operational_missions;
CREATE POLICY "operational_missions_staff_read" ON public.operational_missions
  FOR SELECT TO authenticated USING (public.ecopark_is_staff());

DROP POLICY IF EXISTS "operational_missions_staff_insert" ON public.operational_missions;
CREATE POLICY "operational_missions_staff_insert" ON public.operational_missions
  FOR INSERT TO authenticated WITH CHECK (public.ecopark_is_staff());

DROP POLICY IF EXISTS "operational_missions_staff_update" ON public.operational_missions;
CREATE POLICY "operational_missions_staff_update" ON public.operational_missions
  FOR UPDATE TO authenticated
  USING (public.ecopark_is_staff()) WITH CHECK (public.ecopark_is_staff());

DROP POLICY IF EXISTS "operational_missions_editor_delete" ON public.operational_missions;
CREATE POLICY "operational_missions_editor_delete" ON public.operational_missions
  FOR DELETE TO authenticated USING (public.ecopark_is_content_editor());

DROP POLICY IF EXISTS "operational_alerts_staff_read" ON public.operational_alerts;
CREATE POLICY "operational_alerts_staff_read" ON public.operational_alerts
  FOR SELECT TO authenticated USING (public.ecopark_is_staff());

DROP POLICY IF EXISTS "operational_alerts_staff_insert" ON public.operational_alerts;
CREATE POLICY "operational_alerts_staff_insert" ON public.operational_alerts
  FOR INSERT TO authenticated WITH CHECK (public.ecopark_is_staff());

DROP POLICY IF EXISTS "operational_alerts_staff_update" ON public.operational_alerts;
CREATE POLICY "operational_alerts_staff_update" ON public.operational_alerts
  FOR UPDATE TO authenticated
  USING (public.ecopark_is_staff()) WITH CHECK (public.ecopark_is_staff());

DROP POLICY IF EXISTS "operational_alerts_editor_delete" ON public.operational_alerts;
CREATE POLICY "operational_alerts_editor_delete" ON public.operational_alerts
  FOR DELETE TO authenticated USING (public.ecopark_is_content_editor());

DO $$ BEGIN
  GRANT SELECT, INSERT, UPDATE, DELETE ON public.operational_missions TO anon, authenticated, service_role;
  GRANT SELECT, INSERT, UPDATE, DELETE ON public.operational_alerts TO anon, authenticated, service_role;
  REVOKE EXECUTE ON FUNCTION public.sign_mission_visa(TEXT, TEXT, TEXT) FROM PUBLIC, anon;
  REVOKE EXECUTE ON FUNCTION public.acknowledge_operational_alert(TEXT) FROM PUBLIC, anon;
  GRANT EXECUTE ON FUNCTION public.sign_mission_visa(TEXT, TEXT, TEXT) TO authenticated;
  GRANT EXECUTE ON FUNCTION public.acknowledge_operational_alert(TEXT) TO authenticated;
EXCEPTION WHEN undefined_object THEN NULL; END $$;

-- ============================================================================
-- 7. DONNÉES INITIALES (4 FICHES DE MISSION A4 & 4 ALERTES DE POSTE)
-- ============================================================================
INSERT INTO public.operational_missions (
  mission_ref, order_ref, order_customer, order_total_fcfa, order_summary,
  pole, pole_label, badge_class, secondary_poles,
  agent_name, agent_matricule, agent_role, mission_date, shift_label,
  priority, status, title, location, objective, equipment, guardrail, checklist, visas
) VALUES
  (
    'MSN-2026-101', 'EPK-2026-8841', 'Famille MBARGA Jean-Paul', 15500,
    '2 Adultes, 3 Enfants • Pass Découverte + Piscine + Nutrition Poissons',
    'GUICHET_CAISSE', 'Guichet & Caisse RN3', 'eco-cat-nature', ARRAY['CONTROLE_QR'],
    'Mme Clarisse ATANGANA', 'MAT-GUI-01', 'Caissière Principale Guichet RN3',
    CURRENT_DATE, '08h30 – 18h00 (Journée complète)', 'HAUTE', 'EN_COURS',
    'Ouverture Caisse Guichet #1, Fonds de caisse & Encaissement Visiteurs',
    'Guichet Principal Entrée RN3 (Face Station Tradex Ahala)',
    'Assurer l''encaissement espèces et Mobile Money sans saisie de code PIN, contrôler les réservations en attente de règlement avant 11h00 et éditer le PV de clôture contradictoire.',
    'Terminal Caisse #1 + Fond de caisse 50 000 FCFA + Rouleaux thermiques 80mm + Tampon dateur ECOPARK',
    'Tarif enfant (3–12 ans) protégé à 500 FCFA • Zéro saisie de code PIN Mobile Money dans l''interface',
    '[{"text":"Vérifier le fond de caisse initial (50 000 FCFA) et l''imprimante thermique 80mm","done":true},{"text":"Contrôler la liste des pré-réservations garanties jusqu''à 11h00 (paiement au guichet)","done":true},{"text":"Appliquer strictement le tarif enfant 500 FCFA (3–12 ans) et gratuité < 3 ans","done":true},{"text":"Réaliser le pointage contradictoire des coupures FCFA avant 18h00","done":false}]'::jsonb,
    '{"visa1":{"signed":true,"actor":"Chef d''Exploitation Ahala","timestamp":"08:30"},"visa2":{"signed":true,"actor":"Mme Clarisse ATANGANA (MAT-GUI-01)","timestamp":"08:35"},"visa3":{"signed":false,"actor":"Chef d''Exploitation & Agent","timestamp":""}}'::jsonb
  ),
  (
    'MSN-2026-102', 'DEV-2026-312', 'Complexe Scolaire Bilingue Les Lauréats', 180000,
    '120 élèves • Excursion Scolaire Zoo + Piscine',
    'CONTROLE_QR', 'Contrôle QR, Sécurité & Bassins', 'eco-cat-water', ARRAY['GUICHET_CAISSE'],
    'M. Samuel NKOA', 'MAT-CTL-02', 'Chef de Poste Contrôle QR & Bassins',
    CURRENT_DATE, '08h30 – 18h00 (Journée complète)', 'URGENTE', 'EN_COURS',
    'Contrôle Tourniquet QR, Embarcadère Pirogues & Surveillance Piscine',
    'Tourniquet Principal + Embarcadère Lac d''Ahala + Piscine Semi-Olympique',
    'Garantir le scan systématique des billets QR à l''entrée (rejet immédiat du 2e scan), imposer le port du gilet homologué sur le lac et superviser la baignade.',
    'Scanner QR Hors-Ligne + Talkie-walkie Canal 2 + Lot de 30 Gilets de sauvetage homologués + Trousse 1ers secours',
    'Port du gilet de sauvetage obligatoire avant tout embarquement pirogue • 1 scan unique autorisé par billet QR',
    '[{"text":"Synchroniser le cache hors-ligne des billets QR du jour sur le terminal de contrôle","done":true},{"text":"Vérifier l''état et le bouclage des 30 gilets de sauvetage au ponton du lac","done":true},{"text":"Contrôler le pH du bassin semi-olympique et la présence du maître-nageur","done":true},{"text":"Transmettre le relevé des entrées scannées au Chef d''Exploitation à 18h00","done":false}]'::jsonb,
    '{"visa1":{"signed":true,"actor":"Chef d''Exploitation Ahala","timestamp":"08:30"},"visa2":{"signed":true,"actor":"M. Samuel NKOA (MAT-CTL-02)","timestamp":"08:40"},"visa3":{"signed":false,"actor":"Chef d''Exploitation & Agent","timestamp":""}}'::jsonb
  ),
  (
    'MSN-2026-103', 'CFP-2026-109', 'Séjour & Campus CFP Ahala (Cité Ewondo VIP)', 50000,
    'Préparation Suites VIP Ewondo & Accueil Résidents',
    'HEBERGEMENT', 'Hébergements (Cités Bene, Chanthel & Ewondo)', 'eco-cat-lodge', ARRAY[]::TEXT[],
    'Mme Mireille EBOUA', 'MAT-HEB-03', 'Gouvernante Générale Cités Hôtelières',
    CURRENT_DATE, '08h30 – 18h00 (Journée complète)', 'HAUTE', 'ASSIGNEE',
    'Check-out 11h00, Remise à blanc Cité Ewondo VIP & Accueil Check-in 14h00',
    'Cités Hôtelières Bene, Chanthel, Ewondo VIP & Suites Privées',
    'Superviser les départs avant 11h00, contrôler le ménage, la climatisation et la literie des pavillons, et préparer l''accueil des arrivées dès 14h00.',
    'Trousseau Passe-Partout Cités + Fiches d''état des lieux + Kits d''accueil VIP Ewondo + Talkie-walkie Canal 3',
    'Départ (Check-out) impératif avant 11h00 • Arrivée (Check-in) garantie dès 14h00 • Accès Parc inclus pour les résidents',
    '[{"text":"Récupérer les clés des départs avant 11h00 et vérifier l''état des équipements","done":true},{"text":"Contrôler la climatisation, l''eau chaude et le linge des 8 pavillons Cité Ewondo VIP","done":false},{"text":"Déposer les bracelets d''accès Parc gratuit pour les résidents du jour","done":false},{"text":"Valider l''ouverture du check-in à 14h00 auprès de la réception centrale","done":false}]'::jsonb,
    '{"visa1":{"signed":true,"actor":"Chef d''Exploitation Ahala","timestamp":"08:30"},"visa2":{"signed":false,"actor":"Mme Mireille EBOUA (MAT-HEB-03)","timestamp":""},"visa3":{"signed":false,"actor":"Chef d''Exploitation & Agent","timestamp":""}}'::jsonb
  ),
  (
    'MSN-2026-104', 'EPK-2026-8839', 'Mme NGONO Nadine (Repas Saveurs & Pergola)', 45000,
    'Pack Couple Cité Ewondo VIP + 2 Repas Chauds Château des Saveurs + Pergola',
    'CUISINE_SAVEURS', 'Cuisine Le Château des Saveurs & Pergolas', 'eco-cat-dining', ARRAY[]::TEXT[],
    'Chef Jean-Baptiste MBIDA', 'MAT-CUI-04', 'Chef de Cuisine — Le Château des Saveurs',
    CURRENT_DATE, '11h30 – 20h30 (Service Midi & Soir)', 'HAUTE', 'TERMINEE',
    'Mise en place Braises, Précommandes 13h00 & Dressage Pergolas du Lac',
    'Restaurant Le Château des Saveurs + 10 Pergolas Privées Bord du Lac',
    'Assurer l''approvisionnement en poisson frais des étangs d''Ahala, préparer les précommandes prioritaires de 12h30–13h00 et dresser les pergolas réservées.',
    'Bons de fabrication cuisine + Thermomètre sonde + Charbon écologique + Numéros de table Pergolas 1 à 10',
    'Hygiène chaîne du froid stricte • Priorité absolue aux précommandes famille et groupes scolaires à 12h30',
    '[{"text":"Réceptionner et contrôler les poissons frais issus des étangs piscicoles d''Ahala","done":true},{"text":"Pointer les 18 repas précommandés et les 6 pergolas réservées au bord du lac","done":true},{"text":"Lancer les braises et la mise en place du Poulet DG et du Ndolè dès 10h30","done":true},{"text":"Clôturer la fiche d''inventaire cuisine et le nettoyage des postes en fin de service","done":true}]'::jsonb,
    '{"visa1":{"signed":true,"actor":"Chef d''Exploitation Ahala","timestamp":"08:30"},"visa2":{"signed":true,"actor":"Chef Jean-Baptiste MBIDA (MAT-CUI-04)","timestamp":"10:15"},"visa3":{"signed":true,"actor":"Chef d''Exploitation Ahala","timestamp":"20:30"}}'::jsonb
  )
ON CONFLICT (mission_ref) DO NOTHING;

INSERT INTO public.operational_alerts (
  alert_ref, mission_ref, order_ref, customer_name, order_summary, amount_fcfa,
  pole, pole_label, badge_class, agent_name, agent_matricule, title, acknowledged
) VALUES
  (
    'ALT-2026-201', 'MSN-2026-101', 'EPK-2026-8841', 'Famille MBARGA Jean-Paul',
    '2 Adultes, 3 Enfants • Pass Découverte + Piscine + Nutrition Poissons', 15500,
    'GUICHET_CAISSE', 'Guichet & Caisse RN3', 'eco-cat-nature',
    'Mme Clarisse ATANGANA', 'MAT-GUI-01',
    'Commande #EPK-2026-8841 → Guichet & Caisse RN3', FALSE
  ),
  (
    'ALT-2026-202', 'MSN-2026-102', 'DEV-2026-312', 'Complexe Scolaire Bilingue Les Lauréats',
    '120 élèves • Excursion Scolaire Zoo + Piscine', 180000,
    'CONTROLE_QR', 'Contrôle QR, Sécurité & Bassins', 'eco-cat-water',
    'M. Samuel NKOA', 'MAT-CTL-02',
    'Commande #DEV-2026-312 → Contrôle QR & Bassins (120 pers.)', FALSE
  ),
  (
    'ALT-2026-203', 'MSN-2026-103', 'CFP-2026-109', 'Séjour & Campus CFP Ahala',
    'Préparation Cité Ewondo VIP & Accueil Résidents', 50000,
    'HEBERGEMENT', 'Hébergements (Cités Bene, Chanthel & Ewondo)', 'eco-cat-lodge',
    'Mme Mireille EBOUA', 'MAT-HEB-03',
    'Dossier #CFP-2026-109 → Gouvernante Cités Hôtelières', FALSE
  ),
  (
    'ALT-2026-204', 'MSN-2026-104', 'EPK-2026-8839', 'Mme NGONO Nadine',
    'Pack Couple Cité Ewondo VIP + 2 Repas Chauds + Pergola', 45000,
    'CUISINE_SAVEURS', 'Cuisine Le Château des Saveurs & Pergolas', 'eco-cat-dining',
    'Chef Jean-Baptiste MBIDA', 'MAT-CUI-04',
    'Commande #EPK-2026-8839 → Cuisine Château des Saveurs & Pergola', TRUE
  )
ON CONFLICT (alert_ref) DO NOTHING;

-- ============================================================================
-- 8. INSCRIPTION DANS LA PUBLICATION TEMPS RÉEL (supabase_realtime)
-- ============================================================================
DO $$
DECLARE
  t TEXT;
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_publication WHERE pubname = 'supabase_realtime') THEN
    RETURN;
  END IF;
  FOREACH t IN ARRAY ARRAY['operational_missions', 'operational_alerts'] LOOP
    IF NOT EXISTS (
      SELECT 1 FROM pg_publication_tables
       WHERE pubname = 'supabase_realtime' AND schemaname = 'public' AND tablename = t
    ) THEN
      EXECUTE format('ALTER PUBLICATION supabase_realtime ADD TABLE public.%I', t);
    END IF;
  END LOOP;
END $$;
