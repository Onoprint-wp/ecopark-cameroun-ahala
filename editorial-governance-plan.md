# Plan de Gouvernance Éditoriale & Clarté Durable - ECOPARK CAMEROUN

## Goal
Établir une gouvernance éditoriale durable, éliminer tout jargon banni et coquilles d'élision sur l'ensemble du dépôt ECOPARK CAMEROUN, et garantir la parité stricte SSOT (tarifs, garanties, modèles sortants) protégée par un garde-fou CI automatisé sans aucune régression.

## Tasks
- [x] Task 1: Nettoyage typographique & orthographique de base (Lot 1) : Éliminer 100 % des tirets cadratin/demi-cadratin (`\u2014`/`\u2013`), corriger les ~182 élisions sans apostrophe (`d Ahala` -> `d'Ahala`, `d entrée` -> `d'entrée`, `l eau` -> `l'eau`, etc.) et rétablir les accents français manquants sur minuscules et majuscules (`À`, `É`, `Ê`, `Ç`) dans `src/`, `index.html`, `public/manifest.json`, `public/styles/theme.css` et les migrations SQL. -> Verify: Recherche globale regex `\u2013|\u2014|[djlmnst] [A-Za-zÀ-ÿ]` retournant 0 occurrence dans les chaînes visibles de `src/`, et `npm test` vert.
- [x] Task 2: Bannissement du jargon, anglicismes et formules IA (Lot 2) : Remplacer le jargon technique visible (`Onboarding` -> Inscription rapide, `RBAC` en JSX visible -> Droits d'accès tout en conservant `id="rbac-governance-title"`, `Staff` visible -> Équipe, `Day-Use` -> Séjour en journée, `Check-in / Check-out` visible -> Arrivée / Départ, `Best-Seller` -> Le plus choisi, `B2B` visible -> Entreprises et groupes, `Espace Cliente` -> Espace Client, `PBKDF2-HMAC-SHA256` dans la vue publique -> chiffrement sécurisé des mots de passe, `IQA` -> Qualité de l'air), supprimer les 4 clichés IA « au cœur d » et 2 « incontournable », et harmoniser le vouvoiement exclusif (`vous`). -> Verify: Recherche des termes bannis retournant 0 occurrence dans les textes UI publics et conservation des IDs et enums techniques.
- [x] Task 3: Rythme de lecture & conformité stricte aux tests GEO (Lot 3) : Découper les phrases longues (> 30-35 mots) en phrases courtes et directes tout en garantissant que le `<h1>` de `HeroCanopy.tsx` reste `<= 12` mots terminé par un point `.`, et que les 4 résumés `bluf` de `ImpactBanner.tsx` comptent chacun entre 40 et 55 mots découpés en 2 à 3 phrases courtes de 15 à 17 mots avec guillemets doubles stricts. -> Verify: Exécution de `src/utils/ecosystemE2E.test.ts` (lignes 427-449) réussie à 100 %.
- [x] Task 4: Parité SSOT Tarifs & Garanties dans `public/llms.txt` et `public/agents.txt` (Lot 4 / G2) : Aligner rigoureusement `public/llms.txt` et `public/agents.txt` sur `src/utils/ecoMobility.ts` (Pass Découverte à 2 500 FCFA adulte / 1 500 FCFA enfant, ajout du Pass Journée Complète à 4 500 FCFA / 2 500 FCFA, Pass Journée Royale à 8 500 FCFA / 4 500 FCFA, Suites Prestige VIP jusqu'à 45 000 FCFA, Navette A/R à 1 500 FCFA / 1 000 FCFA, Garantie Météo RN3 à 90 jours, et 100 % d'accents français rétablis). -> Verify: Validation de cohérence exacte mot à mot et chiffre à chiffre avec `src/utils/ecoMobility.ts` et `AhalaShowcase.tsx`.
- [x] Task 5: Gouvernance des saisies dynamiques en direct (G1) : Créer le module léger `src/utils/editorialSanitizer.ts` (nettoyage automatique des tirets longs, normalisation des espaces), l'intégrer aux formulaires de `RangerDashboard.tsx` (`closureReasonInput`, `interventionNoteInput`) et `CitizenSentinel.tsx` (`description`), assainir les modèles `CLOSURE_PRESETS` et `PHOTO_PRESETS`, et ajouter la migration SQL `supabase/migrations/20261114000001_editorial_governance_constraints.sql`. -> Verify: Tests unitaires prouvant le nettoyage immédiat des saisies avec tirets longs et maintien des tests de synchronisation backoffice.
- [x] Task 6: Centralisation et assainissement des modèles sortants (G5) : Créer le module `src/utils/outgoingTemplates.ts` centralisant les 13 liens et messages pré-remplis WhatsApp `wa.me` vers les 3 numéros officiels (`+237 672 56 45 98`, `+237 694 60 14 49`, `+237 697 13 62 03`) avec encodage sécurisé, et corriger les coquilles d'apostrophes du billet SVG vectoriel dans `src/components/booking/DigitalEcoPass.tsx`. -> Verify: Inspection du template SVG exporté et test unitaire validant la syntaxe XML et l'absence de toute coquille d'élision.
- [x] Task 7: Garde-fou CI automatique bloquant (G6) : Créer le fichier de test unitaire et d'intégration `src/utils/editorialGovernance.test.ts` (automatiquement pris en compte par le script `test` de `package.json` et la CI GitHub Actions) bloquant tout encodage corrompu (`\uFFFD`, `Ã©`), tout tiret long (`\u2014`/`\u2013`), tout jargon banni ou cliché IA, toute élision sans apostrophe dans `src/`, et toute dérive des tarifs/garanties entre `src/utils/ecoMobility.ts` et `public/llms.txt` / `public/agents.txt`. -> Verify: `npm test` exécutant avec succès la nouvelle suite en moins de 1 seconde.
- [x] Task 8: Audit final Zéro Régression & validation de build : Vérifier que `npm test` passe à 100 %, exécuter `npm run build` (`tsc -b && vite build`) avec 0 erreur, vérifier le script inline de `.github/workflows/ci.yml` (artefacts de distribution complets, rewrites Vercel >= 20, migrations SQL >= 8), et auditer `git diff` pour confirmer 0 dérive non autorisée sur les prix, devises, numéros de téléphone et enums techniques. -> Verify: Pipeline `npm test` et `npm run build` 100 % vert et certification de non-régression.

## Glossaire officiel du projet (20 entrées)

### Jargon technique banni, anglicismes & clichés IA (13 entrées)
| # | Terme d'origine | Terme de remplacement recommandé | Contexte d'application |
|---|---|---|---|
| 1 | `Onboarding` | Inscription rapide / Création de compte | Tunnel de réservation et espaces utilisateurs |
| 2 | `RBAC` (texte visible UI) | Droits d'accès / Accès réservé par métier | Titres et libellés visibles de l'administration |
| 3 | `PBKDF2-HMAC-SHA256` | Chiffrement sécurisé des mots de passe | Mentions légales publiques (`LegalNoticeView.tsx`) |
| 4 | `Day-Use` | Séjour en journée / Repos en journée | Fiches hôtelières et options d'hébergement |
| 5 | `Check-in / Check-out` | Arrivée dès 14h / Départ jusqu'à 11h | Hôtellerie et confirmations de séjour |
| 6 | `Best-Seller` | Le plus choisi | Badges de mise en avant des formules de pass |
| 7 | `B2B` (visible utilisateur) | Entreprises et groupes | Menus, devis et formulaires événementiels |
| 8 | `Espace Cliente` / `Compte Cliente` | Espace Client / Mon Espace Visiteur | Navigation, boutons et modales d'authentification |
| 9 | `IQA` (hors badge très étroit) | Qualité de l'air (indice de pureté forestière) | Indicateurs écologiques et télémétrie parc |
| 10 | `Staff` (visible UI) | Équipe / Personnel d'encadrement | Tableaux de bord et descriptions de postes |
| 11 | « au cœur de / d' » (cliché IA) | à, dans, au centre de, ou phrase directe | Présentations du parc et descriptions d'activités |
| 12 | « incontournable(s) » (cliché IA) | majeur(e), emblématique, essentiel(le) | Catalogues de loisirs et formules de découverte |
| 13 | « dans un monde où », « catalyseur », « révolutionner », « véritable levier », « plongeons dans » | Suppression ou formulation factuelle | Tous les contenus descriptifs et marketing |

### Termes réglementaires et légaux conservés (7 entrées)
| # | Terme conservé (Règle 4) | Explication pédagogique obligatoire hors bouton (Règle G3) |
|---|---|---|
| 14 | `MINEFOP` | Ministère de l'Emploi et de la Formation Professionnelle (tutelle de l'État agréant les 5 filières CFP EcoPark). |
| 15 | `DQP / CQP` | Diplôme de Qualification Professionnelle / Certificat de Qualification Professionnelle (titres nationaux officiels). |
| 16 | `SYSCOHADA` | Système Comptable OHADA (référentiel légal de conformité et de traçabilité financière en Afrique Centrale). |
| 17 | `UICN` | Union Internationale pour la Conservation de la Nature (standards de protection de la faune et des espèces sensibles). |
| 18 | `Loi n° 2010/012` | Loi camerounaise sur la cybersécurité et la protection des données (garantissant l'anonymisation des visiteurs). |
| 19 | `Garantie Météo RN3` | Engagement officiel de report gratuit valable 90 jours en cas d'intempéries tropicales à Ahala. |
| 20 | `FCFA` / `XAF` | Franc CFA CEMAC (devise officielle unique de facturation et de règlement sur tout le complexe). |

## Done When
- [x] 0 tiret cadratin (`\u2014`) et 0 tiret demi-cadratin (`\u2013`) dans l'ensemble du dépôt (`src/`, `index.html`, `public/`, `supabase/migrations/`).
- [x] 100 % des ~182 élisions françaises sans apostrophe corrigées dans les textes visibles de `src/`.
- [x] 100 % des accents français rétablis dans `public/llms.txt`, `public/agents.txt` et les textes de l'application.
- [x] Parité tarifaire et des garanties SSOT vérifiée à 100 % entre `src/utils/ecoMobility.ts` et `public/llms.txt` + `public/agents.txt`.
- [x] Modèles de liens WhatsApp centralisés et billet SVG `DigitalEcoPass.tsx` exempt de toute coquille d'élision.
- [x] Module `src/utils/editorialSanitizer.ts` fonctionnel et migration SQL `20261114000001_editorial_governance_constraints.sql` ajoutée.
- [x] Garde-fou unitaire CI `src/utils/editorialGovernance.test.ts` actif, exécuté par `npm test` et passant à 100 %.
- [x] `npm run build` (`tsc -b && vite build`) compile avec 0 avertissement ni erreur TypeScript.
- [x] Toutes les assertions structurelles existantes (`ecosystemE2E.test.ts` lignes 427-468) demeurent 100 % vertes.
- [x] Audit `git diff` certifiant 0 % de modification non autorisée sur les prix FCFA, numéros de téléphone, clés d'API et rewrites.
