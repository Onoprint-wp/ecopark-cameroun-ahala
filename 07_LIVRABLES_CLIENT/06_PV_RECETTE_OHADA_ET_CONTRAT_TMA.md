# ⚖️ 06 - PROCÈS-VERBAL DE RECETTE DÉFINITIVE OHADA, CONTRATS B2B & CONTRAT TMA (`06_PV_RECETTE_OHADA_ET_CONTRAT_TMA.md`)

* **Maître d'Ouvrage (Client)** : **ECOPARK YAOUNDÉ (ECOPARK CAMEROUN)**, Quartier Ahala Barrière (Face Station Tradex, RN3), Yaoundé, représenté par son Promoteur & Directeur Général, **Dr Christophe FOÉ NDI** (`+237 697 13 62 03`).
* **Maître d'Œuvre (Prestataire)** : **ONOGRAPH SARL**, Yaoundé, Cameroun.
* **Date d'établissement** : 12 Novembre 2026.

---

## 1. Procès-Verbal de Recette Définitive Contradictoire (Droit OHADA)

### 1.1 Constat de Conformité Technique & Fonctionnelle (100 % GO)
Les parties ont procédé à la vérification contradictoire de la plateforme **ECOPARK CAMEROUN (« Canopée Vivante » V4)** et attestent la validation sans réserve des jalons suivants :
1. **Couverture Fonctionnelle (`78 / 78` Écrans)** : Validation intégrale des 77 écrans contractuels (`PUB-01..22`, `RES-01..06`, `ACC-01..05`, `AGT-01..09`, `EXP-01..06`, `DIR-01..05`, `ADM-01..08`) et de l'extension `ADM-09` (Inbox Leads 1-clic).
2. **Intégrité Financière & Comptable SYSCOHADA** : Tous les calculs sont exécutés en entiers `INTEGER` FCFA (`0` `Float`), le garde-fou tarif enfant (`500 FCFA`) est actif en base et en interface, et le Grand Livre Analytique à 6 axes (`ANA-01` à `ANA-06`) est équilibré à 100 % avec le Journal Général OHADA (`Débit = Crédit`).
3. **Sécurité PostgreSQL RLS, Multi-Tenant & Audit Immuable** : `ENABLE ROW LEVEL SECURITY` actif sur 100 % des tables publiques, clé `tenant_id` déployée, publication des tarifs verrouillée par `MFA aal2` (Direction) et chaîne `SHA-256` (`audit_logs`) intègre (`81/81` tests DB et `112/112` tests Data validés).
4. **Résilience Terrain Offline-First & PWA Mobile** : Fonctionnement vérifié du scanner QR hors-ligne (`offlineScansQueue`), du billetage BEAC contradictoire (`AGT-09`), du Mode Soleil (`Sun Mode >= 7:1`) et du manifeste PWA (`manifest.json` + `sw.js`).

### 1.2 Clause OHADA de Réserve de Propriété Intellectuelle (Loi 3.3 - Impérative)
> **ARTICLE SPÉCIAL - RÉSERVE DE PROPRIÉTÉ INTELLECTUELLE :**
> Conformément aux dispositions de l'Acte Uniforme OHADA portant sur le Droit Commercial Général et de l'Accord de Bangui révisé (OAPI), **la cession définitive des droits patrimoniaux de propriété intellectuelle sur le code source, les schémas de base de données, les Design Tokens et les supports graphiques, ainsi que le transfert des accès administrateurs maîtres (`GitHub`, `Vercel`, `Supabase`), sont strictement subordonnés à l'encaissement effectif et intégral de 100 % du prix convenu au contrat**. Jusqu'au complet paiement du solde, l'ensemble des livrables demeure la propriété entière et exclusive du Maître d'Œuvre (**ONOGRAPH SARL**).

---

## 2. Contrat de Tierce Maintenance Applicative (TMA), SLA & Frontière du Périmètre

### 2.1 Engagements de Niveau de Service (SLA - Horaire `Africa/Douala`)
* **Garantie de Temps d'Intervention (`GTI`)** : **`< 4 heures`** (7j/7 de 07h00 à 21h00, week-ends et jours fériés inclus).
* **Garantie de Temps de Rétablissement (`GTR`) par Sévérité** :
  * **Anomalie Critique `P1` (Indisponibilité de la billetterie `/reserver`, du scanner QR `AGT-05` ou de la caisse `AGT-03`)** : Contournement ou rétablissement en **`< 2 heures`**.
  * **Anomalie Majeure `P2` (Dysfonctionnement d'un module Back-Office sans blocage des encaissements)** : Correction en **`< 8 heures ouvrées`**.
  * **Anomalie Mineure `P3` (Ajustement cosmétique ou éditorial)** : Correction en **`< 48 heures ouvrées`**.
* **Plan de Reprise d'Activité (`PRA` / `DRP`)** :
  * **RPO (*Recovery Point Objective*)** : **`< 5 minutes`** (sauvegardes continues WAL PostgreSQL + snapshots quotidiens chiffrés `AES-256`).
  * **RTO (*Recovery Time Objective*)** : **`< 2 heures`** (redéploiement instantané depuis le dépôt Git sur Vercel/Supabase).

### 2.2 Frontière Contractuelle Stricte (*In-Scope* vs *Out-of-Scope*)
* **Inclus dans la Garantie Corrective (*In-Scope*)** : Correction de tout bogue affectant les 78 écrans livrés, maintien de la sécurité RLS Supabase, mise à jour des certificats SSL et maintien en condition opérationnelle des exports CSV SYSCOHADA.
* **Exclus de la Garantie et Soumis à Devis Phase 2 (*Out-of-Scope*)** :
  1. Ajout de nouvelles fonctionnalités majeures non prévues dans les 78 écrans réceptionnés.
  2. Fourniture et câblage électrique de tourniquets tripodes métalliques RS-485 ou d'imprimantes thermiques physiques.
  3. Reprise de données corrompues suite à la divulgation volontaire d'un mot de passe ou matricule par un agent.

---

## 3. Modèle de Contrat-Cadre B2B / Forfait Sortie Scolaire (Prêt à Faire Signer par ECOPARK)

> **CONVENTION DE FORFAIT GROUPE / ÉCOLE - ECOPARK CAMEROUN (AHALA RN3)**
> * **Entre** : **ECOPARK CAMEROUN (Yaoundé-Ahala)** et **L'Établissement / Entreprise Souscripteur** : `[Nom de l'École / Entreprise]`.
> * **Référence Devis Système** : `DEV-2026-[XXXX]` | **Date de l'événement** : `[JJ/MM/AAAA]` | **Effectif prévu** : `[N]` participants.
> * **Formule retenue** :
>   * `[ ]` **Forfait Sortie Scolaire Pédagogique** : **`500 FCFA / élève`** (1 encadrant gratuit pour 10 élèves - Accès Parc & Zoo + Aire de détente encadrée).
>   * `[ ]` **Forfait Séminaire / Réception Salle Menkii (500 places)** : Location salle + sonorisation + traiteur *Le Château des Saveurs* selon devis joint.
>   * `[ ]` **Option Navette Climatisée A/R Yaoundé - Ahala** : Bus de `5`, `18` ou `32 places` (`3 000 FCFA / passager`).
> * **Modalités de règlement** : Acompte de **50 %** à la réservation par Orange Money, MTN MoMo ou virement/espèces au guichet ; solde de **50 %** à l'arrivée du groupe au portail d'Ahala contre remise de la facture normalisée et déclenchement de la **Fiche de Mission A4 (`#printableMissionSheetA4`)**.
> * **Garantie Météo** : En cas d'intempérie majeure, l'établissement bénéficie d'un report gratuit de sa date sur **30 jours**.

---

## 4. Bloc de Signatures Officielles du Procès-Verbal

| Pour le Maître d'Ouvrage (**ECOPARK CAMEROUN**) | Pour le Maître d'Œuvre (**ONOGRAPH SARL**) |
| :--- | :--- |
| **Dr Christophe FOÉ NDI**<br/>Promoteur & Directeur Général<br/>*Mention manuscrite : « Bon pour réception définitive »*<br/><br/>Signature & Cachet : ___________________________ | **La Direction Technique ONOGRAPH**<br/>Architecte & Intégrateur Système<br/>*Certifié 100 % Conforme Zero-Error Gate*<br/><br/>Signature & Cachet : ___________________________ |
