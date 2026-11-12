# 🗺️ DICTIONNAIRE DE DONNÉES UI STITCH <-> SCHÉMA SQL SUPABASE (`DATA_DICTIONARY_STITCH.md`)

* **Projet Google Stitch** : `projects/522000543872634848`
* **Couverture** : 78 écrans (`PUB-01..22`, `RES-01..06`, `ACC-01..05`, `AGT-01..09`, `EXP-01..06`, `DIR-01..05`, `ADM-01..09`).

| Famille & Écran UI | Sélecteur DOM / Composant Principal | Table SQL / Clé `EcoparkData` | Colonne / RPC Associée |
| :--- | :--- | :--- | :--- |
| **`PUB-01` Accueil Hero** | `#v4CanopyHeroStage`, `#ahalaLiveWeatherBar` | `site_settings` | `weather_banner` (`active_preset`, `custom_message`) |
| **`PUB-03` Catalogue V4** | `#v4ActivityCardsGrid`, `#totem11ServicesInteractiveGrid` | `catalog_activities` | `slug`, `title`, `adult_price_fcfa`, `child_price_fcfa`, `image_src` |
| **`PUB-04` Fiche Activité** | `#v4Pub04Title`, `#v4Pub04SubtotalFcfa` | `catalog_activities` | `description`, `adult_price_fcfa`, `child_price_fcfa` |
| **`PUB-09` Cités Hôtelières** | `#sec-PUB-09`, `#lodgeCitySelect` | `lodge_cities` | `code` (`EWONDO`, `SUITES_PRIVEES`, `CHANTHEL`, `BENE`), `min_price_fcfa`, `max_price_fcfa` |
| **`PUB-10` Tarifs & Calculateur** | `#pubCatalogTableBody`, `#quickCalcAdults`, `#quickCalcChildren` | `catalog_activities`, `sales_bundles` | `recalcQuickDayPrice()`, `adult_bundle_price_fcfa` |
| **`PUB-11` Groupes & Écoles** | `#sec-PUB-11`, `#quoteOrgName`, `#quotePhone` | `group_quotes` | `quote_reference`, `organization_name`, `contact_phone`, `estimated_budget_fcfa` |
| **`PUB-12` Formations CFP** | `#sec-PUB-12` | `cfp_applications` | `track_code`, `applicant_name`, `applicant_phone`, `status` |
| **`RES-01..05` Simulateur** | `#v4ResStepperBar`, `#grandTotalFCFA`, `#demoTicketCard` | `bookings` | `reference_code`, `visit_date`, `total_fcfa`, `qr_status`, `lodge_city` |
| **`ACC-01..05` Mon Espace** | `#view-ACC`, `#accOtpVerifyForm` | `bookings`, `group_quotes` | `verifyVisitorAccessCode()`, `deleteAccount()` |
| **`AGT-01..04` Guichet POS** | `#agtShiftAuthStatusBadge`, `#posCartList` | `staff_profiles`, `bookings` | `verifyShiftAgentLogin()`, `emitPosTicket()` |
| **`AGT-05..06` Scanner QR** | `#qrScanInput`, `#qrVerdictBanner` | `bookings` | `verifyLiveQrCode()`, `offlineScansQueue`, `syncOfflineScans()` |
| **`AGT-09` Clôture Caisse** | `#theoreticalCashTotal`, `#physicalCashTotal`, `#physicalCashDiff` | `audit_logs` | `recalcPhysicalCashCount()`, `printOfficialDocument('CLOSURE')` |
| **`EXP-01..06` Exploitation** | `#sec-EXP-MISSIONS`, `#printableMissionSheetA4`, `#expPostAlertsCenter` | `operational_missions`, `operational_alerts` | `assignOperationalMission()`, `signMissionVisa()`, `rateMissionOnVisa3()` |
| **`DIR-01..04` Baromètre** | `#dirServicesBarometerBody`, `#dirChannelsPerformanceList` | `bookings`, `catalog_activities` | `filterDirectionServices()`, `sendExecutiveWhatsAppDigest20h()` |
| **`DIR-05` Compta SYSCOHADA** | `#dirAnalyticalAccountingBody` | `get_analytical_accounting_ledger()` | `ANA-01` à `ANA-06`, Poches `571`, `521`, `661`, `108`, `exportJournalOHADACSV()` |
| **`ADM-01..09` Console Admin** | `#admCatalogBody`, `#admStaffBody`, `#admAuditBody`, `#sec-ADM-09` | Toutes les tables + `audit_logs` | `admin_duplicate()`, `admin_set_status()`, `verify_audit_chain()` |
