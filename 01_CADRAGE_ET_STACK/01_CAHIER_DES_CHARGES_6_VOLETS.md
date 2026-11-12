# 📘 01 - CAHIER DES CHARGES CONTRACTUEL EN 6 VOLETS & MATRICE AMDEC (`01_CAHIER_DES_CHARGES_6_VOLETS.md`)

* **Projet** : **ECOPARK CAMEROUN (Yaoundé - Ahala, RN3)**
* **Référence Maître** : Synchronisé avec `02_SUITE_CONTRACTUELLE_6_CDC.md`, `MATRICE_COUVERTURE_77_ECRANS_ECOPARK.md` et `supabase/migrations/`.

---

## 1. Synthèse des 6 Cahiers des Charges (CCTP, CCAG, CCSE, CCÉditorial, CCGraphique, CCTMA)

| Volet Contractuel | Périmètre & Engagements Clés (100 % Implémentés dans le Code) |
| :--- | :--- |
| **1. CCTP (Technique & Fonctionnel)** | **78 écrans opérationnels** (`77` contractuels + `ADM-09` Inbox Leads 1-clic) : Vitrine 6 sous-pages (`PUB-01..22`), Simulateur 4 parcours en 5 étapes (`RES-01..06`), Espace Client OTP (`ACC-01..05`), Guichet POS & Scanner QR 7 verdicts (`AGT-01..09`), Exploitation & Fiches de Mission A4 (`EXP-01..06`), Direction & Compta Analytique SYSCOHADA (`DIR-01..05`), Console CRUD (`ADM-01..09`). |
| **2. CCAG (Administratif & Juridique OHADA)** | **Clause de Réserve de Propriété Intellectuelle (Loi 3.3)** : cession intégrale du code, des designs et des accès maîtres (`GitHub`, `Vercel`, `Supabase`) **uniquement après encaissement effectif de 100 % du prix convenu**. Réversibilité *Zero Vendor Lock-in* garantie sous 15 jours. |
| **3. CCSE (Sécurité, RLS & Exploitation)** | Conformité **Loi camerounaise n° 2010/012**, isolation Multi-Tenant (`tenant_id`), `ENABLE ROW LEVEL SECURITY` sur 100 % des tables publiques, filtrage RBAC en mémoire (`sanitizeForRole()`), contrôle MFA `aal2` pour la publication des tarifs, sas d'upload *Magic Bytes* (`%PDF-`, JPEG, PNG), journal d'audit immuable chaîné `SHA-256`. |
| **4. CCÉditorial (Copywriting & GEO IA 2026)** | Architecture *Agentic GEO 2026* (`ecopark-geo-2026/`, `llms.txt`, `agents.txt`, `robots.txt` 9 bots IA, `sitemap.xml` `hreflang="fr|en|x-default"`), capsules BLUF (`40-55 mots`) & AEO (`35-40 mots`), bilinguisme `FR/EN` sans rechargement (`locales/fr.json`, `locales/en.json`). |
| **5. CCGraphique (Design System & Print FOGRA39)** | Direction artistique *Canopée Vivante* (`tokens.json` W3C, `.stitch/DESIGN.md`), Tri-Thème `Zero-FOUC` (`Light #F7F5EF`, `Dark OLED #090D16`, `Sun Mode >= 7:1`), `tabular-nums`, table `HEX <-> CMJN FOGRA39 (TAC <= 300 %) <-> Pantone <-> RAL`, Sticker Vinyle QR (`Bleed 3mm`, `Safe Zone 4mm`, `300 DPI`, `Outlines`). |
| **6. CCTMA (Tierce Maintenance & SLA)** | **GTI `< 4h`** (7j/7 de 07h00 à 21h00), **GTR Anomalie Critique `P1 < 2h`** (Guichet/QR/Paiement), **RPO `< 5 min`** / **RTO `< 2h`**, sauvegarde quotidienne chiffrée `AES-256` et frontière *In-Scope / Out-of-Scope* explicite. |

---

## 2. Matrice AMDEC Industrielle ($\text{Criticité} = F \times G \times ND$) Reliée au Code

| Mode de Défaillance | Effet sur l'Exploitation | $F$ | $G$ | $ND$ | Criticité $C$ | Verrou Technique Implémenté dans le Code Source |
| :--- | :--- | :-: | :-: | :-: | :---: | :--- |
| **1. Modification non autorisée d'un tarif en ligne** | Perte de chiffre d'affaires ou litige client au portail | 3 | 5 | 4 | **60 (Critique)** | Trigger SQL `ECOPARK_PUBLISHED_PRICE_LOCKED` + obligation de rôle `direction` avec double authentification `MFA aal2` (`admin_set_status`). |
| **2. Inversion tarif Enfant Groupe > Individuel** | Incohérence commerciale (ex. saisir 700 F au lieu de 500 F) | 4 | 4 | 3 | **48 (Élevée)** | Contrainte SQL `chk_child_group_price_never_higher_than_individual` + blocage immédiat du bouton `#admEdSave` dans `ecopark-admin.js`. |
| **3. Fraude par réutilisation d'un billet QR** | Entrées multiples non payées aux tourniquets | 5 | 5 | 3 | **75 (Critique)** | Signature `SIG-V4-*` + passage atomique à `USED` dès le 1er scan + rejet des doublons même en mode hors-ligne (`offlineScansQueue`). |
| **4. Écart d'espèces en clôture de caisse guichet** | Coulage financier sur la poche `571` | 4 | 5 | 3 | **60 (Critique)** | Grille de billetage BEAC (`AGT-09`) : si `|Écart| > 2 000 FCFA`, verrouillage de la clôture sans motif obligatoire et alerte Direction + PV A4 contradictoire. |
| **5. Altération a posteriori du journal d'audit** | Dissimulation d'une fraude interne | 2 | 5 | 5 | **50 (Élevée)** | Trigger `trg_audit_logs_immutable` interdisant `UPDATE`/`DELETE`/`TRUNCATE` + chaînage cryptographique `SHA-256` vérifié par `verify_audit_chain()`. |
| **6. Commande payée non préparée sur le terrain** | Client VIP ou groupe scolaire attendu sans loge ni table prête | 3 | 5 | 3 | **45 (Élevée)** | Règle `dispatchOrderToPostMission()` : `1 Commande = 1 Fiche de Mission A4` routée vers le pôle concerné + alerte sonore/visuelle temps réel. |
| **7. Upload d'un fichier malveillant renommé en image/PDF** | Compromission XSS ou exécution de script dans le Back-Office | 2 | 5 | 4 | **40 (Élevée)** | Inspection binaire des *Magic Bytes* (`%PDF-`, `FF D8 FF`, `89 50 4E 47`) en RAM + contrainte SQL `image_src_safe` + ré-encodage Canvas. |

---

## 3. Matrice RBAC des 8 Rôles & Frontière Contractuelle (*In-Scope vs Out-of-Scope*)

### 3.1 Les 8 Rôles RBAC (`ecopark_role`)
1. `visiteur_anonyme` : Consultation du catalogue publié (`status = 'PUBLISHED'`), disponibilités `get_availability()`, création de réservation ou demande de devis (`EN_ETUDE`).
2. `client_connecte` (`client_b2b`) : Consultation de ses propres dossiers dans `/mon-espace` après vérification OTP 4 derniers chiffres (`verifyVisitorAccessCode()`), téléchargement billet QR et devis A4, demande de suppression de compte (`deleteAccount()`).
3. `agent_guichet` (`MAT-GUI-01`) : Prise de poste par matricule (`verifyShiftAgentLogin()`), vente POS (`AGT-03`), émargement Visa #2 sur fiche de mission, clôture de caisse contradictoire (`AGT-09`). Aucun accès à l'audit ni à la modification des tarifs.
4. `agent_controle` (`MAT-CTL-02`) : Scan QR en ligne et hors-ligne (`AGT-05`/`AGT-06`), acquittement des alertes de portail, émargement Visa #2.
5. `responsable_exploitation` (`MAT-EXP-01`) : Gestion des jauges (`ADM-03`), de l'agenda et des ruptures cuisine (`ADM-04`), préparation des brouillons tarifaires (`DRAFT`), assignation des missions terrain et signature du Visa #3 avec notation `/100`.
6. `comptable` (`MAT-CPT-01`) : Lecture seule sur le catalogue, accès complet au Grand Livre Analytique SYSCOHADA à 6 axes (`DIR-05`), aux exports CSV OHADA et au journal d'audit financier (`ADM-08`).
7. `direction` (`MAT-DIR-01` - Dr Christophe FOÉ NDI) : Publication des tarifs sous `MFA aal2`, baromètre stratégique des 11 services (`DIR-01..05`), vérification d'intégrité `SHA-256` (`verify_audit_chain()`), réception du Condensé Quotidien WhatsApp de 20h00.
8. `administrateur_plateforme` (`MAT-ADM-01`) : Gestion des comptes d'équipe (`ADM-05`, sans pouvoir modifier son propre rôle `ECOPARK_SELF_ROLE_CHANGE_FORBIDDEN`) et supervision des passerelles (`ADM-06`).

### 3.2 Frontière Explicite du Périmètre (*In-Scope Phase 1* vs *Out-of-Scope Phase 2*)
* **Inclus dans le Périmètre Forfaitaire Phase 1 (*In-Scope*)** : L'intégralité des 78 écrans, la base PostgreSQL/Supabase à 8 migrations RLS, la PWA mobile hors-ligne, le kit GEO IA 2026 (`ecopark-geo-2026/`) et les 6 dossiers livrables `07_LIVRABLES_CLIENT/`.
* **Exclus du Périmètre Phase 1 (*Out-of-Scope - Réservés à la Phase 2 sur avenant/devis séparé*)** :
  1. Fourniture physique et câblage électrique RS-485 de tourniquets tripodes métalliques motorisés.
  2. Interfaçage matériel avec des caisses enregistreuses fiscales propriétaires fermées.
  3. Gestion de la paie mensuelle CNPS/DIPE hors primes d'excellence opérationnelle du parc.
