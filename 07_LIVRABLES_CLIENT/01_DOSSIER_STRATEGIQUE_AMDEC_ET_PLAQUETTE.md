# 📊 01 - DOSSIER STRATÉGIQUE, MATRICE AMDEC & PLAQUETTE COMMERCIALE B2B (`01_DOSSIER_STRATEGIQUE_AMDEC_ET_PLAQUETTE.md`)

* **Client** : **ECOPARK CAMEROUN (Yaoundé - Ahala, Route Nationale N°3, Face Station Tradex)**
* **Direction Générale** : Dr Christophe FOÉ NDI (`+237 697 13 62 03`)
* **Référence Code Source** : Relié à `etape0-site-live/index.html`, `etape0-site-live/js/ecopark-data.js`, `etape0-site-live/js/ecopark-admin.js` et `supabase/migrations/`.

---

## 1. Synthèse Exécutive, PESTEL & Matrice Océan Bleu (ERRC)

### 1.1 Diagnostic PESTEL Physique, Électrique & Réglementaire (Yaoundé - Ahala)
* **Politique & Institutionnel** : Agrément **MINEFOP** pour les 5 filières du CFP ECOPARK (`50 000 FCFA` inscription + `250 000 FCFA` scolarité en 4 tranches) ; conformité **MINTOUL** (hôtellerie & loisirs) et **MINFOF** (parc animalier).
* **Économique & Monétaire (CEMAC / XAF)** : Tarification 100 % en Francs CFA entiers (`INTEGER`), paiement hybride **Orange Money**, **MTN MoMo** et **Espèces BEAC** au guichet.
* **Technologique & Électrique** : Résilience complète aux micro-coupures 3G/4G et électriques sur l'axe Ahala-Nsimalen grâce au moteur `LocalDemoDriver` + file persistante `offlineScansQueue` + PWA Service Worker `sw.js`.
* **Climatique** : Garantie Pluie Ahala permettant le **report gratuit sous 30 jours** de tout billet QR en cas d'averse tropicale.

### 1.2 Matrice Océan Bleu (ERRC) Appliquée à ECOPARK
* **Éliminer** : Les tickets papier sans traçabilité, les prix flous sur Facebook et l'attente en plein soleil au portail.
* **Réduire** : Le temps de contrôle au portail (`< 5s` par scan QR), le délai d'émission d'un devis école/entreprise (`< 60s`).
* **Renforcer** : La transparence tarifaire Adulte (`1 000 F`) vs Enfant (`500 F`), le contrôle contradictoire des espèces BEAC (`AGT-09`).
* **Créer** : Le **Totem Interactif des 11 Services**, les **3 Pass Tout-Inclus Coupe-File QR**, le routage automatique **`1 Commande = 1 Fiche de Mission A4 à 3 Visas`** et le **Grand Livre Analytique SYSCOHADA à 6 axes (`ANA-01` à `ANA-06`)**.

---

## 2. Architecture de Revenus à 4 Piliers (`40 % / 25 % / 20 % / 15 %`) & 4 Poches SYSCOHADA

| Pilier de Revenus | Poids | Offres ECOPARK & Tarifs Officiels FCFA | Axe Analytique SYSCOHADA |
| :--- | :---: | :--- | :--- |
| **1. Récurrent & B2B (Écoles, Séminaires, CFP)** | **40 %** | Sorties scolaires (`500 F/élève`), Salle Menkii 500 places (`dès 250 000 F`), CFP MINEFOP (`250 000 F`). | `ANA-05` (`7065`) & `ANA-06` (`7066`) |
| **2. Cœur d'Attraction & Flux Week-End** | **25 %** | Zoo (`1 000 F` / `500 F`), Piscine (`2 500 F` / `1 500 F`), Pirogue (`1 000 F` / `500 F`), Pass Découverte (`3 000 F`). | `ANA-01` (`7061`) & `ANA-02` (`7062`) |
| **3. Marges Hôtellerie & Gastronomie** | **20 %** | 4 Cités Hôtelières (`10 000 F` à `30 000 F/nuit`) & Restaurant *Le Château des Saveurs* (`dès 3 500 F`). | `ANA-03` (`7063`) & `ANA-04` (`7064`) |
| **4. Seconde Vie & Upsell (Order Bumps)** | **15 %** | Pergola privée (`10 000 F`), Navette A/R (`3 000 F`), Canne à pêche (`2 000 F`), Poisson frais étang. | Ventilé `ANA-01` à `ANA-05` |

* **4 Poches de Trésorerie SYSCOHADA (`DIR-05`)** : `571` Caisse Espèces Guichet, `521` Banques & Mobile Money (`5581 OM` / `5582 MoMo`), `661` Charges Personnel & Primes (filtrées par `sanitizeForRole()`), `108` Compte de l'Exploitant.

---

## 3. Grille AMDEC Industrielle Reliée aux Garde-Fous du Code Source

| Risque Opérationnel | $F \times G \times ND$ | Verrou Technique dans le Code Source |
| :--- | :---: | :--- |
| **Modification sauvage d'un tarif publié** | `3 x 5 x 4 = 60` | Trigger SQL `ECOPARK_PUBLISHED_PRICE_LOCKED` + obligation de rôle `direction` sous `MFA aal2`. |
| **Erreur tarifaire Enfant Groupe > Individuel** | `4 x 4 x 3 = 48` | Contrainte SQL `chk_child_group_price_never_higher_than_individual` + blocage UI `#admEdSave`. |
| **Fraude par photocopie ou partage WhatsApp d'un QR** | `5 x 5 x 3 = 75` | Signature `SIG-V4-*` + passage immédiat à `USED` + rejet des doublons dans `offlineScansQueue`. |
| **Coulage d'espèces au guichet en fin de poste** | `4 x 5 x 3 = 60` | Billetage BEAC (`AGT-09`) : blocage si écart `> 2 000 FCFA` sans justification + PV A4 signé. |
| **Falsification du journal d'audit** | `2 x 5 x 5 = 50` | Trigger `trg_audit_logs_immutable` (`Append-Only`) + chaîne `SHA-256` (`verify_audit_chain()`). |

---

## 4. Plaquette Commerciale B2B, Écoles & Séminaires (Cascade des 3 Cerveaux)

### 4.1 Accroche Cerveau Reptilien (`50 ms` - Sécurité & Proximité)
> **« Votre séminaire de 500 personnes ou sortie scolaire au vert, à 15 minutes de Yaoundé (Ahala RN3). »**
* Parking bitumé sécurisé, bus navettes de **5, 18 et 32 places**, domaine clôturé et surveillé, groupe électrogène de secours.

### 4.2 Argumentaire Cerveau Limbique (Zéro Stress Organisateur)
* **1 Commande = 1 Fiche de Mission A4 Dédiée** : Dès validation de votre devis, la Salle Menkii, la cuisine du *Château des Saveurs*, le service d'hébergement et les maîtres-nageurs reçoivent leur feuille de route horodatée à 3 Visas.
* **Tarif Scolaire Sanctuarisé** : **500 FCFA par élève** avec **1 encadrant gratuit pour 10 élèves**.

### 4.3 Preuves Néocortex (Chiffres & Facture Proforma Immédiate)
* **Salle Menkii Essomba Anton** : `500 places assises`, sonorisation, vidéoprojection, pauses-café et buffet camerounais dès `3 500 FCFA/personne`.
* **Hébergement Délégations** : 4 Cités Hôtelières sur site (`10 000` à `30 000 FCFA/nuit`, Check-in `14h00`, Check-out `11h00`).
* **Action Directe** : Générez votre facture proforma officielle `DEV-2026-XXXX` en 60 secondes sur `/groupes-evenements` ou via WhatsApp au **`+237 697 13 62 03`**.
