# -*- coding: utf-8 -*-
"""
Suite de verification E2E de la synchronisation dans l'ensemble (360° ECOPARK) :
Teste les 10 axes de synchronisation entre Front-Office Public, EcoparkData,
Console Admin (ADM-01..09), Exploitation (EXP), Guichet/Scanner (AGT) et Direction (DIR).
"""
import sys
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_URL = "http://localhost:3000"


def main():
    checks = []

    def check(label, cond, detail=""):
        status = "PASS" if cond else "FAIL"
        print(f"  [{status}] {label}" + (f" — {detail}" if detail else ""))
        checks.append((label, bool(cond)))

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        console_errors = []
        page.on("pageerror", lambda err: console_errors.append(str(err)))
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)

        page.goto(BASE_URL, wait_until="networkidle")
        page.evaluate("() => { localStorage.clear(); }")
        page.reload(wait_until="networkidle")

        # 1. Bug #1 & #2 : Synchronisation temps reel ADM-01 -> /nos-tarifs & Simulateur /reserver
        res_tarif = page.evaluate("""async () => {
          const beforeZoo = getCatalogPriceDynamic('zoo', false, false);
          recalcSimulator();
          const beforeTotal = document.getElementById('grandTotalFCFA').textContent;
          const acts = EcoparkData.content('catalog_activities');
          const zoo = acts.find(a => a.slug === 'zoo');
          await EcoparkData.update('catalog_activities', zoo.id, { adult_price_fcfa: 1500 });
          const afterZoo = getCatalogPriceDynamic('zoo', false, false);
          const afterTotal = document.getElementById('grandTotalFCFA').textContent;
          const pubHtml = document.getElementById('pubCatalogTableBody').innerHTML;
          await EcoparkData.update('catalog_activities', zoo.id, { adult_price_fcfa: 1000 });
          return { beforeZoo, afterZoo, beforeTotal, afterTotal, pubHas1500: pubHtml.includes('1 500') };
        }""")
        check(
            "Sync #1 & #2 : ADM-01 Tarifs -> Simulateur (/reserver) & Grille (/nos-tarifs) en temps reel",
            res_tarif["beforeZoo"] == 1000 and res_tarif["afterZoo"] == 1500 and res_tarif["beforeTotal"] != res_tarif["afterTotal"] and res_tarif["pubHas1500"],
            f"Zoo {res_tarif['beforeZoo']}->{res_tarif['afterZoo']} FCFA, Total {res_tarif['beforeTotal']}->{res_tarif['afterTotal']}"
        )

        # 2. Bug #3 : Auto-guérison (Backfill) des miniatures du catalogue dans localStorage
        res_heal = page.evaluate("""async () => {
          const raw = JSON.parse(localStorage.getItem('ecopark_ahala_db_sprint1_v1'));
          raw.content.catalog_activities.forEach(a => { delete a.image_src; });
          localStorage.setItem('ecopark_ahala_db_sprint1_v1', JSON.stringify(raw));
          await EcoparkData.init();
          const acts = EcoparkData.content('catalog_activities');
          const missing = acts.filter(a => !a.image_src).length;
          return { total: acts.length, missing };
        }""")
        check(
            "Sync #3 : Auto-guerison des images_src manquantes dans localStorage",
            res_heal["total"] >= 8 and res_heal["missing"] == 0,
            f"{res_heal['total']} offres verifiees, {res_heal['missing']} miniature manquante"
        )

        # 3. Bug #4 : Synchronisation Cites Hotelieres (ADM-02), Pass (ADM-01), Agenda (ADM-04) et Menu (ADM-05)
        res_dyn = page.evaluate("""async () => {
          // A. Lodge price update
          const lodges = EcoparkData.content('lodge_cities');
          const ew = lodges.find(l => l.code === 'EWONDO');
          await EcoparkData.update('lodge_cities', ew.id, { min_price_fcfa: 28000 });
          const lodgeDetails = getSelectedLodgeDetails();
          await EcoparkData.update('lodge_cities', ew.id, { min_price_fcfa: 25000 });

          // B. Menu stock toggle
          const dishes = EcoparkData.content('menu_items');
          const ndole = dishes.find(d => d.sku === 'MNU-NDOLE-ROYAL');
          await EcoparkData.update('menu_items', ndole.id, { in_stock: false });
          const optNdole = Array.from(document.getElementById('simDishSelect').options).find(o => o.value.includes('Ndol'));
          const ndoleDisabled = optNdole ? optNdole.disabled : false;
          await EcoparkData.update('menu_items', ndole.id, { in_stock: true });

          // C. Agenda event update
          const evts = EcoparkData.content('agenda_events');
          const dim = evts.find(e => e.code === 'EVT_DIMANCHE_ROYAL');
          await EcoparkData.update('agenda_events', dim.id, { title: 'Grand Dimanche Royal Sync Test' });
          const gridHtml = document.getElementById('weeklyAgendaGrid').innerHTML;
          await EcoparkData.update('agenda_events', dim.id, { title: 'Grand Dimanche Royal : Buffet Camerounais & Ambiance Acoustique Live' });

          return { ewUnit: lodgeDetails.unit, ndoleDisabled, agendaUpdated: gridHtml.includes('Grand Dimanche Royal Sync Test') };
        }""")
        check(
            "Sync #4 : ADM-02 Loges, ADM-04 Agenda & ADM-05 Rupture stock cuisine -> Front-Office",
            res_dyn["ewUnit"] == 28000 and res_dyn["ndoleDisabled"] is True and res_dyn["agendaUpdated"] is True,
            f"Ewondo={res_dyn['ewUnit']} FCFA, Ndole disabled={res_dyn['ndoleDisabled']}, Agenda={res_dyn['agendaUpdated']}"
        )

        # 4. Bug #5 : Conservation du numero de telephone client sur Devis B2B/Ecole vers ADM-09
        res_quote_phone = page.evaluate("""() => {
          document.getElementById('quoteOrgName').value = 'Lycee Bilingue Sync';
          document.getElementById('quotePhone').value = '+237 699 88 77 66';
          const ref = submitGroupQuoteSprint1();
          const lead = getUnifiedLeadsList().find(x => x.reference === ref);
          const waUrl = (function() {
            const origOpen = window.open;
            let captured = '';
            window.open = (u) => { captured = u; };
            openLeadWhatsAppFollowup(ref);
            window.open = origOpen;
            return captured;
          })();
          return { ref, phone: lead ? lead.phone : null, waUrl };
        }""")
        check(
            "Sync #5 : Conservation du telephone client sur Devis Groupe (RES-06 -> ADM-09 -> WhatsApp)",
            res_quote_phone["phone"] == "+237 699 88 77 66" and "237699887766" in res_quote_phone["waUrl"],
            f"Ref={res_quote_phone['ref']}, Phone={res_quote_phone['phone']}"
        )

        # 5. Bug #6 : Reversibilite des statuts BOOKING dans ADM-09 (PROCESSED <-> CONFIRMED <-> NEW) + Compteur AGT
        res_booking_rev = page.evaluate("""() => {
          const bRef = loadDB().bookings[0].reference;
          const entries0 = loadDB().posStats.validatedEntries;
          setLeadInboxStatus('BOOKING', bRef, 'PROCESSED');
          const st1 = getUnifiedLeadsList().find(x => x.reference === bRef).leadStatus;
          const entries1 = loadDB().posStats.validatedEntries;
          setLeadInboxStatus('BOOKING', bRef, 'CONFIRMED');
          const st2 = getUnifiedLeadsList().find(x => x.reference === bRef).leadStatus;
          const entries2 = loadDB().posStats.validatedEntries;
          setLeadInboxStatus('BOOKING', bRef, 'NEW');
          const st3 = getUnifiedLeadsList().find(x => x.reference === bRef).leadStatus;
          setLeadInboxStatus('BOOKING', bRef, 'CONFIRMED');
          return { st1, st2, st3, entries0, entries1, entries2 };
        }""")
        check(
            "Sync #6 : Reversibilite statut BOOKING dans ADM-09 & synchronisation compteur entrees AGT",
            res_booking_rev["st1"] == "PROCESSED"
            and res_booking_rev["st2"] == "CONFIRMED"
            and res_booking_rev["st3"] == "NEW"
            and res_booking_rev["entries1"] == res_booking_rev["entries0"] + 1
            and res_booking_rev["entries2"] == res_booking_rev["entries0"],
            f"{res_booking_rev['st1']} -> {res_booking_rev['st2']} -> {res_booking_rev['st3']} (Entrees: {res_booking_rev['entries0']}->{res_booking_rev['entries1']}->{res_booking_rev['entries2']})"
        )

        # 6. Bug #7 : Vue Exploitation (#view-EXP) affiche plusieurs dossiers recents (Devis, CFP, RDV)
        res_exp_rows = page.evaluate("""() => {
          document.getElementById('quoteOrgName').value = 'Ministere Sync 2';
          document.getElementById('quotePhone').value = '+237 677 11 22 33';
          submitGroupQuoteSprint1();
          syncAllViewsFromDB();
          const expTbody = document.querySelectorAll('#view-EXP table tbody')[1];
          const trCount = expTbody ? expTbody.querySelectorAll('tr').length : 0;
          return { trCount, html: expTbody ? expTbody.innerHTML : '' };
        }""")
        check(
            "Sync #7 : Table Exploitation (#view-EXP) affiche l'historique multi-lignes des derniers dossiers",
            res_exp_rows["trCount"] >= 4 and "Ministere Sync 2" in res_exp_rows["html"] and "Lycee Bilingue Sync" in res_exp_rows["html"],
            f"{res_exp_rows['trCount']} lignes actives dans #view-EXP"
        )

        # 7. Bug #8 : Scanner QR Hors-Ligne (AGT-05) ne met pas en file d'attente un billet deja utilise
        res_offline_scan = page.evaluate("""() => {
          window._ecoparkOfflineScansQueue = [];
          localStorage.removeItem('ecopark_offline_scans_queue');
          const bRef = loadDB().bookings[0].reference;
          document.getElementById('qrScanInput').value = bRef;
          // Simuler mode hors-ligne via getter navigator.onLine
          Object.defineProperty(navigator, 'onLine', { value: false, configurable: true });
          verifyLiveQrCode(); // 1er scan (valide) -> doit entrer dans la file hors-ligne
          const qLenAfterFirst = window._ecoparkOfflineScansQueue.length;
          verifyLiveQrCode(); // 2e scan (deja utilise) -> NE DOIT PAS entrer dans la file hors-ligne
          const qLenAfterSecond = window._ecoparkOfflineScansQueue.length;
          Object.defineProperty(navigator, 'onLine', { value: true, configurable: true });
          syncOfflineScans();
          const qLenAfterSync = window._ecoparkOfflineScansQueue.length;
          return { qLenAfterFirst, qLenAfterSecond, qLenAfterSync };
        }""")
        check(
            "Sync #8 : Scanner QR Hors-Ligne (AGT-05) rejette les doublons et synchronise a la reconnexion",
            res_offline_scan["qLenAfterFirst"] == 1 and res_offline_scan["qLenAfterSecond"] == 1 and res_offline_scan["qLenAfterSync"] == 0,
            f"Queue 1er scan={res_offline_scan['qLenAfterFirst']}, 2e scan={res_offline_scan['qLenAfterSecond']}, apres sync={res_offline_scan['qLenAfterSync']}"
        )

        # 8. Bug #9 : Vente Guichet POS (AGT-03/04) recalcule immediatement la grille de cloture de caisse (AGT-09)
        res_pos_closure = page.evaluate("""() => {
          recalcPhysicalCashCount();
          const theoBefore = document.getElementById('theoreticalCashTotal').textContent;
          clearPos();
          addPosItem('Entrée Zoo Adulte', 1000);
          addPosItem('Entrée Zoo Adulte', 1000);
          addPosItem('Entrée Zoo Adulte', 1000);
          emitPosTicket('Espèces FCFA');
          const theoAfter = document.getElementById('theoreticalCashTotal').textContent;
          const diffText = document.getElementById('physicalCashDiff').textContent;
          return { theoBefore, theoAfter, diffText };
        }""")
        check(
            "Sync #9 : Vente POS Guichet (AGT-03) -> Recalcul immediat Cloture de Caisse (AGT-09)",
            res_pos_closure["theoBefore"] != res_pos_closure["theoAfter"] and "187 500" in res_pos_closure["theoAfter"],
            f"Theorique {res_pos_closure['theoBefore']} -> {res_pos_closure['theoAfter']} ({res_pos_closure['diffText']})"
        )

        # 9. Bug #10 : Synchronisation multi-onglets (BroadcastChannel / storage event)
        page2 = context.new_page()
        page2.goto(BASE_URL, wait_until="networkidle")
        res_multitab = page.evaluate("""async () => {
          await EcoparkData.saveSetting('weather_banner', {
            presets: { SUNNY: '27 C', WEEKEND_PEAK: '29 C', RAIN_GUARANTEE: 'Pluie' },
            active_preset: 'SUNNY',
            custom_message: 'Sync Multi-Onglets Active RN3'
          });
          return document.getElementById('ahalaLiveWeatherText').textContent;
        }""")
        page2.wait_for_timeout(250)
        banner_tab2 = page2.evaluate("() => document.getElementById('ahalaLiveWeatherText').textContent")
        check(
            "Sync #10 : Synchronisation temps reel inter-onglets (Onglet 1 ADM-06 -> Onglet 2 Public)",
            banner_tab2 == "Sync Multi-Onglets Active RN3",
            f"Onglet 1='{res_multitab}' | Onglet 2='{banner_tab2}'"
        )

        # 10. Phase 8 : Synchronisation des 11 Services Officiels du Totem EcoPark CAMEROUN
        res_totem = page.evaluate("""async () => {
          const totemCardCount = document.querySelectorAll('#totem11ServicesInteractiveGrid .totem-plate-btn').length;
          const expZonesCount = document.querySelectorAll('#expTotem11ServicesGrid > div').length;
          const catCount = EcoparkData.content('catalog_activities').length;
          const lodgesCount = EcoparkData.content('lodge_cities').length;
          const hasSuitesPrivees = EcoparkData.content('lodge_cities').some(l => l.code === 'SUITES_PRIVEES');
          const hasMusee = EcoparkData.content('catalog_activities').some(a => a.slug === 'musee');
          const hasBiblio = EcoparkData.content('catalog_activities').some(a => a.slug === 'bibliotheque');
          const hasAireJeux = EcoparkData.content('catalog_activities').some(a => a.slug === 'aire_jeux');
          const hasCreche = EcoparkData.content('catalog_activities').some(a => a.slug === 'creche_garderie');

          // Modifier tarif Musée dans EcoparkData et vérifier la mise à jour temps réel du Totem, RES-01 et Tarifs
          const museeRow = EcoparkData.content('catalog_activities').find(a => a.slug === 'musee');
          const chkMusee = document.getElementById('chkMusee');
          if (chkMusee) chkMusee.checked = true;
          await EcoparkData.update('catalog_activities', museeRow.id, { adult_price_fcfa: 1500, child_price_fcfa: 800 });

          const totemMuseeText = document.querySelector('[data-totem-price="musee"]')?.textContent || '';
          const subMuseeText = document.getElementById('subMusee')?.textContent || '';
          const pubHasMusee1500 = (document.getElementById('pubCatalogTableBody')?.innerHTML || '').includes('1 500');
          await EcoparkData.update('catalog_activities', museeRow.id, { adult_price_fcfa: 1000, child_price_fcfa: 500 });
          if (chkMusee) chkMusee.checked = false;
          recalcSimulator();

          return {
            totemCardCount, expZonesCount, catCount, lodgesCount,
            hasSuitesPrivees, hasMusee, hasBiblio, hasAireJeux, hasCreche,
            totemMuseeText, subMuseeText, pubHasMusee1500
          };
        }""")
        check(
            "Sync #11 : Totem Officiel des 11 Services (Vitrine, Tarifs, RES-01, POS AGT-03, EXP-02 & Admin Catalogue)",
            res_totem["totemCardCount"] == 11
            and res_totem["expZonesCount"] == 11
            and res_totem["catCount"] == 12
            and res_totem["lodgesCount"] == 4
            and res_totem["hasSuitesPrivees"]
            and res_totem["hasMusee"]
            and res_totem["hasBiblio"]
            and res_totem["hasAireJeux"]
            and res_totem["hasCreche"]
            and "1 500" in res_totem["totemMuseeText"]
            and res_totem["subMuseeText"] != "0 FCFA"
            and res_totem["pubHasMusee1500"],
            f"Totem={res_totem['totemCardCount']}/11, EXP={res_totem['expZonesCount']}/11, Cat={res_totem['catCount']}, Lodges={res_totem['lodgesCount']}, Musée={res_totem['totemMuseeText']}, Sub={res_totem['subMuseeText']}"
        )

        check("Aucune erreur console / pageerror", len(console_errors) == 0, f"{len(console_errors)} erreur(s)")

        browser.close()

    failed = [c for c in checks if not c[1]]
    print(f"\nSynthese Synchronisation 360° : {len(checks) - len(failed)}/{len(checks)} verifications reussies.")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
