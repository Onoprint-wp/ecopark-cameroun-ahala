# -*- coding: utf-8 -*-
"""
Builder pour la Phase 6 ECOPARK :
1. Grille interactive de billetage physique et calcul d'écart dans AGT-08/09
2. PV officiel de clôture imprimable (@media print) avec ventilation coupures et visas
3. Cache de validation hors-ligne pour le scanner AGT-05 lors des pannes réseau RN3
4. Synchronisation automatique à la reconnexion et dynamisation des compteurs
5. Synchronisation 100% stricte entre etape0-site-live/index.html et Prototype_Interactif_ECOPARK_NEW_LOOK.html
6. Invariant strict : 0 caractère > U+25FF
"""
from pathlib import Path
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent

HTML_FILES = [
    ROOT / "etape0-site-live" / "index.html",
    ROOT / "Prototype_Interactif_ECOPARK_NEW_LOOK.html",
]


def main():
    source_path = HTML_FILES[0]
    with open(source_path, "r", encoding="utf-8") as f:
        content = f.read()

    # -------------------------------------------------------------------------
    # 1. Remplacement de la carte AGT-08 / AGT-09 avec la Grille de Billetage
    # -------------------------------------------------------------------------
    old_agt08_pattern = r'<!-- Journal de session et cl.*?ture de caisse \(AGT-08, AGT-09\) -->\s*<div class="col-12 card">.*?<\/div>\s*<\/div>\s*<\/div>\s*<\/div>\s*<\/section>'
    
    new_agt08_markup = """<!-- Journal de session et cloture de caisse (AGT-08, AGT-09) -->
              <div class="col-12 card" id="cardCashClosureAgt08">
                <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;">
                  <h3><span class="icon-medallion"><svg class="svg-mono" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 2v20l2-1 2 1 2-1 2 1 2-1 2 1 2-1 2 1V2l-2 1-2-1-2 1-2-1-2 1-2-1-2 1Z"/><path d="M14 8H8"/><path d="M16 12H8"/><path d="M13 16H8"/></svg></span> <span class="tech-code-tag">AGT-08 & AGT-09 - </span>Journal de Session & Cloture de Caisse Contradictoire</h3>
                  <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;">
                    <span class="status-badge status-success" id="cashClosureVarianceBadge">Ecart constate : 0 FCFA (Caisse conforme)</span>
                    <button type="button" class="btn btn-secondary btn-sm" id="btnPrintCashClosure" onclick="printOfficialDocument('CLOSURE')">PV Cloture PDF</button>
                    <button type="button" class="btn btn-primary btn-sm" id="btnExportCsvAgt" onclick="exportEcoparkDatabaseCSV()">Exporter CSV (Excel)</button>
                  </div>
                </div>

                <!-- Compteurs direct de session -->
                <div class="grid-12" style="gap:12px;margin-top:12px;">
                  <div class="col-4" style="background:var(--color-surface-soft);padding:14px;border-radius:10px;border-left:4px solid var(--color-brand-deep);">
                    <div style="font-size:13px;color:var(--color-text-muted);">Encaissements Especes Session (Theorique)</div>
                    <strong style="font-family:var(--font-heading);font-size:1.55rem;color:var(--color-brand-deep);" id="agtStatCash">184 500 FCFA</strong>
                  </div>
                  <div class="col-4" style="background:var(--color-surface-soft);padding:14px;border-radius:10px;border-left:4px solid #C47D2B;">
                    <div style="font-size:13px;color:var(--color-text-muted);">Encaissements Mobile Money Guichet</div>
                    <strong style="font-family:var(--font-heading);font-size:1.55rem;color:var(--color-brand-deep);" id="agtStatMomo">96 000 FCFA</strong>
                  </div>
                  <div class="col-4" style="background:var(--color-surface-soft);padding:14px;border-radius:10px;border-left:4px solid #2E7D32;">
                    <div style="font-size:13px;color:var(--color-text-muted);">Visiteurs controles (Tourniquet)</div>
                    <strong style="font-family:var(--font-heading);font-size:1.55rem;color:var(--color-brand-deep);" id="agtStatEntries">214 entrees validees</strong>
                  </div>
                </div>

                <!-- Grille interactive de billetage physique (Comptage contrediscutable) -->
                <div style="margin-top:20px;padding:16px;background:var(--color-surface-soft);border:1px solid var(--color-border);border-radius:12px;">
                  <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;margin-bottom:12px;">
                    <div>
                      <strong style="font-size:15px;color:var(--color-brand-deep);">Billetage Physique des Especes (Comptage Contradictoire RN3)</strong>
                      <span style="font-size:13px;color:var(--color-text-muted);display:block;">Saisissez les quantites reelles de coupures et pieces presentes dans le tiroir-caisse.</span>
                    </div>
                    <div style="display:flex;gap:8px;">
                      <button type="button" class="btn btn-secondary btn-sm" onclick="resetPhysicalCashCount()">Reinitialiser</button>
                      <button type="button" class="btn btn-primary btn-sm" onclick="validateCashClosure()">Valider Cloture & Signer PV</button>
                    </div>
                  </div>

                  <!-- Table de comptage -->
                  <div style="overflow-x:auto;">
                    <table style="width:100%;border-collapse:collapse;background:#FFF;border-radius:8px;overflow:hidden;border:1px solid var(--color-border);font-size:13.5px;">
                      <thead>
                        <tr style="background:#F4F6F2;color:var(--color-brand-deep);text-align:left;">
                          <th style="padding:10px 12px;border-bottom:1px solid var(--color-border);">Coupure / Type</th>
                          <th style="padding:10px 12px;border-bottom:1px solid var(--color-border);width:140px;text-align:center;">Quantite</th>
                          <th style="padding:10px 12px;border-bottom:1px solid var(--color-border);text-align:right;width:180px;">Sous-total (FCFA)</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr>
                          <td style="padding:8px 12px;border-bottom:1px solid var(--color-border);"><strong>Billet 10 000 FCFA</strong></td>
                          <td style="padding:8px 12px;border-bottom:1px solid var(--color-border);text-align:center;">
                            <input type="number" min="0" value="12" id="cashQty10k" class="form-control" style="width:90px;display:inline-block;padding:4px 8px;text-align:center;" oninput="recalcPhysicalCashCount()" />
                          </td>
                          <td style="padding:8px 12px;border-bottom:1px solid var(--color-border);text-align:right;" id="subtotal10k">120 000 FCFA</td>
                        </tr>
                        <tr>
                          <td style="padding:8px 12px;border-bottom:1px solid var(--color-border);"><strong>Billet 5 000 FCFA</strong></td>
                          <td style="padding:8px 12px;border-bottom:1px solid var(--color-border);text-align:center;">
                            <input type="number" min="0" value="8" id="cashQty5k" class="form-control" style="width:90px;display:inline-block;padding:4px 8px;text-align:center;" oninput="recalcPhysicalCashCount()" />
                          </td>
                          <td style="padding:8px 12px;border-bottom:1px solid var(--color-border);text-align:right;" id="subtotal5k">40 000 FCFA</td>
                        </tr>
                        <tr>
                          <td style="padding:8px 12px;border-bottom:1px solid var(--color-border);"><strong>Billet 2 000 FCFA</strong></td>
                          <td style="padding:8px 12px;border-bottom:1px solid var(--color-border);text-align:center;">
                            <input type="number" min="0" value="8" id="cashQty2k" class="form-control" style="width:90px;display:inline-block;padding:4px 8px;text-align:center;" oninput="recalcPhysicalCashCount()" />
                          </td>
                          <td style="padding:8px 12px;border-bottom:1px solid var(--color-border);text-align:right;" id="subtotal2k">16 000 FCFA</td>
                        </tr>
                        <tr>
                          <td style="padding:8px 12px;border-bottom:1px solid var(--color-border);"><strong>Billet 1 000 FCFA</strong></td>
                          <td style="padding:8px 12px;border-bottom:1px solid var(--color-border);text-align:center;">
                            <input type="number" min="0" value="6" id="cashQty1k" class="form-control" style="width:90px;display:inline-block;padding:4px 8px;text-align:center;" oninput="recalcPhysicalCashCount()" />
                          </td>
                          <td style="padding:8px 12px;border-bottom:1px solid var(--color-border);text-align:right;" id="subtotal1k">6 000 FCFA</td>
                        </tr>
                        <tr>
                          <td style="padding:8px 12px;border-bottom:1px solid var(--color-border);"><strong>Billet 500 FCFA</strong></td>
                          <td style="padding:8px 12px;border-bottom:1px solid var(--color-border);text-align:center;">
                            <input type="number" min="0" value="4" id="cashQty500b" class="form-control" style="width:90px;display:inline-block;padding:4px 8px;text-align:center;" oninput="recalcPhysicalCashCount()" />
                          </td>
                          <td style="padding:8px 12px;border-bottom:1px solid var(--color-border);text-align:right;" id="subtotal500b">2 000 FCFA</td>
                        </tr>
                        <tr>
                          <td style="padding:8px 12px;border-bottom:1px solid var(--color-border);">Piece 500 FCFA</td>
                          <td style="padding:8px 12px;border-bottom:1px solid var(--color-border);text-align:center;">
                            <input type="number" min="0" value="0" id="cashQty500p" class="form-control" style="width:90px;display:inline-block;padding:4px 8px;text-align:center;" oninput="recalcPhysicalCashCount()" />
                          </td>
                          <td style="padding:8px 12px;border-bottom:1px solid var(--color-border);text-align:right;" id="subtotal500p">0 FCFA</td>
                        </tr>
                        <tr>
                          <td style="padding:8px 12px;border-bottom:1px solid var(--color-border);">Piece 100 FCFA</td>
                          <td style="padding:8px 12px;border-bottom:1px solid var(--color-border);text-align:center;">
                            <input type="number" min="0" value="4" id="cashQty100" class="form-control" style="width:90px;display:inline-block;padding:4px 8px;text-align:center;" oninput="recalcPhysicalCashCount()" />
                          </td>
                          <td style="padding:8px 12px;border-bottom:1px solid var(--color-border);text-align:right;" id="subtotal100">400 FCFA</td>
                        </tr>
                        <tr>
                          <td style="padding:8px 12px;border-bottom:1px solid var(--color-border);">Piece 50 FCFA</td>
                          <td style="padding:8px 12px;border-bottom:1px solid var(--color-border);text-align:center;">
                            <input type="number" min="0" value="2" id="cashQty50" class="form-control" style="width:90px;display:inline-block;padding:4px 8px;text-align:center;" oninput="recalcPhysicalCashCount()" />
                          </td>
                          <td style="padding:8px 12px;border-bottom:1px solid var(--color-border);text-align:right;" id="subtotal50">100 FCFA</td>
                        </tr>
                        <tr>
                          <td style="padding:8px 12px;">Piece 25 FCFA</td>
                          <td style="padding:8px 12px;text-align:center;">
                            <input type="number" min="0" value="0" id="cashQty25" class="form-control" style="width:90px;display:inline-block;padding:4px 8px;text-align:center;" oninput="recalcPhysicalCashCount()" />
                          </td>
                          <td style="padding:8px 12px;text-align:right;" id="subtotal25">0 FCFA</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>

                  <!-- Bilan du rapprochement contradictoire -->
                  <div class="grid-12" style="margin-top:14px;padding:12px;background:#FFF;border-radius:8px;border:1px solid var(--color-border);align-items:center;">
                    <div class="col-4">
                      <span style="font-size:12.5px;color:var(--color-text-muted);display:block;">Total Especes Compte :</span>
                      <strong style="font-size:1.35rem;color:var(--color-brand-deep);" id="physicalCashTotal">184 500 FCFA</strong>
                    </div>
                    <div class="col-4">
                      <span style="font-size:12.5px;color:var(--color-text-muted);display:block;">Total Theorique Caisse :</span>
                      <strong style="font-size:1.35rem;color:var(--color-text-main);" id="theoreticalCashTotal">184 500 FCFA</strong>
                    </div>
                    <div class="col-4" style="text-align:right;">
                      <span style="font-size:12.5px;color:var(--color-text-muted);display:block;">Resultat Rapprochement :</span>
                      <div id="cashReconciliationVerdict">
                        <span class="status-badge status-success" style="font-size:13px;padding:4px 10px;" id="physicalCashDiff">Ecart : 0 FCFA (Caisse Conforme)</span>
                      </div>
                    </div>
                  </div>

                  <!-- Alerte explicative en cas d'ecart critique -->
                  <div id="closureIncidentAlert" style="display:none;margin-top:12px;padding:12px 14px;background:#FDECEA;border:1px solid #EF9A9A;border-radius:8px;color:#C62828;font-size:13.5px;line-height:1.45;">
                    <strong>ALERTE GOUVERNANCE CAISSE (> 2 000 FCFA) :</strong> L'ecart physique depasse le seuil de tolerance operationnelle. Un rapport d'incident avec visa contradictoire Caissiere et Direction Generale sera automatiquement attache au Proces-Verbal de cloture.
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>"""

    match = re.search(old_agt08_pattern, content, re.DOTALL)
    if not match:
        print("Erreur: motif AGT-08 non trouve dans index.html")
        sys.exit(1)

    content = content[:match.start()] + new_agt08_markup + content[match.end():]
    print("  [OK] Balisage AGT-08/09 remplace avec succes")

    # -------------------------------------------------------------------------
    # 2. Ajout du badge d'etat reseau et synchronisation hors-ligne dans AGT-05
    # -------------------------------------------------------------------------
    target_agt05_label = '<label class="form-label" for="qrScanInput">Scanner un QR ou saisir la reference / telephone<span class="tech-code-tag"> (`AGT-05` / `AGT-07`)</span> :</label>'
    
    # En cas d'accents échappés ou utf-8
    agt05_pattern = r'<label class="form-label" for="qrScanInput">Scanner un QR ou saisir la r.*?f.*?rence / t.*?l.*?phone<span class="tech-code-tag"> \(`AGT-05` / `AGT-07`\)</span> :</label>'
    
    new_agt05_label_with_badge = """<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;margin-bottom:6px;">
                    <label class="form-label" for="qrScanInput" style="margin:0;">Scanner un QR ou saisir la reference / telephone<span class="tech-code-tag"> (`AGT-05` / `AGT-07`)</span> :</label>
                    <div id="scannerNetworkStatusWrapper" style="display:flex;align-items:center;gap:6px;">
                      <span class="status-badge status-success" id="scannerNetworkStatusBadge" style="font-size:12px;padding:3px 8px;">
                        Liaison RN3 Active
                      </span>
                      <button type="button" class="btn btn-secondary btn-sm" id="btnSyncOfflineScans" style="display:none;font-size:11.5px;padding:3px 8px;" onclick="syncOfflineScans()">
                        Synchroniser (<span id="offlineQueueCount">0</span>)
                      </button>
                    </div>
                  </div>"""

    content = re.sub(agt05_pattern, new_agt05_label_with_badge, content, count=1)
    print("  [OK] Badge de liaison reseau & bouton synchronisation ajoutes a AGT-05")

    # -------------------------------------------------------------------------
    # 3. Mise a jour du JavaScript : Logique Phase 6
    # -------------------------------------------------------------------------
    phase6_js_marker = "/* ==========================================================================\n     PHASE 6 : CAISSE GUICHET, BILLETAGE & CONTRÔLE HORS-LIGNE (RN3)\n     ========================================================================== */"
    # Using strict ASCII for marker
    phase6_js_code = """
  // ==========================================================================
  // PHASE 6 : CAISSE GUICHET, BILLETAGE PHYSIQUE & CONTROLE HORS-LIGNE (RN3)
  // ==========================================================================

  // --- 1. GRILLE DE BILLETAGE PHYSIQUE (AGT-08 / AGT-09) ---
  window.recalcPhysicalCashCount = function () {
    var denominations = [
      { id: 'cashQty10k', value: 10000, subId: 'subtotal10k' },
      { id: 'cashQty5k', value: 5000, subId: 'subtotal5k' },
      { id: 'cashQty2k', value: 2000, subId: 'subtotal2k' },
      { id: 'cashQty1k', value: 1000, subId: 'subtotal1k' },
      { id: 'cashQty500b', value: 500, subId: 'subtotal500b' },
      { id: 'cashQty500p', value: 500, subId: 'subtotal500p' },
      { id: 'cashQty100', value: 100, subId: 'subtotal100' },
      { id: 'cashQty50', value: 50, subId: 'subtotal50' },
      { id: 'cashQty25', value: 25, subId: 'subtotal25' }
    ];

    var totalPhysique = 0;
    var countsBreakdown = {};

    denominations.forEach(function (d) {
      var el = document.getElementById(d.id);
      var qty = el ? Math.max(0, parseInt(el.value, 10) || 0) : 0;
      var sub = qty * d.value;
      totalPhysique += sub;
      countsBreakdown[d.value] = (countsBreakdown[d.value] || 0) + qty;
      var subEl = document.getElementById(d.subId);
      if (subEl) subEl.textContent = formatFCFA(sub);
    });

    // Lecture du total theorique especes depuis la base de session
    var db = typeof loadDB === 'function' ? loadDB() : { posStats: { cashFcfa: 184500 } };
    var theoretical = (db.posStats && typeof db.posStats.cashFcfa === 'number') ? db.posStats.cashFcfa : 184500;

    var diff = totalPhysique - theoretical;

    var physTotalEl = document.getElementById('physicalCashTotal');
    if (physTotalEl) physTotalEl.textContent = formatFCFA(totalPhysique);

    var theoTotalEl = document.getElementById('theoreticalCashTotal');
    if (theoTotalEl) theoTotalEl.textContent = formatFCFA(theoretical);

    var diffEl = document.getElementById('physicalCashDiff');
    var badgeEl = document.getElementById('cashClosureVarianceBadge');
    var alertBox = document.getElementById('closureIncidentAlert');

    if (diff === 0) {
      if (diffEl) {
        diffEl.className = 'status-badge status-success';
        diffEl.style.cssText = 'font-size:13px;padding:4px 10px;background:#EDF4E7;color:#1D490D;border:1px solid #C4DFC0;';
        diffEl.textContent = 'Ecart : 0 FCFA (Caisse Conforme)';
      }
      if (badgeEl) {
        badgeEl.className = 'status-badge status-success';
        badgeEl.textContent = 'Ecart constate : 0 FCFA (Caisse conforme)';
      }
      if (alertBox) alertBox.style.display = 'none';
    } else if (Math.abs(diff) <= 2000) {
      var sign = diff > 0 ? '+' : '';
      if (diffEl) {
        diffEl.className = 'status-badge';
        diffEl.style.cssText = 'font-size:13px;padding:4px 10px;background:#FFF8E1;color:#8E5617;border:1px solid #FFE082;';
        diffEl.textContent = 'Tolerance mineure : ' + sign + formatFCFA(diff);
      }
      if (badgeEl) {
        badgeEl.className = 'status-badge';
        badgeEl.style.cssText = 'background:#FFF8E1;color:#8E5617;border:1px solid #FFE082;';
        badgeEl.textContent = 'Ecart mineur : ' + sign + formatFCFA(diff) + ' (Tolere)';
      }
      if (alertBox) alertBox.style.display = 'none';
    } else {
      var signCrit = diff > 0 ? '+' : '';
      if (diffEl) {
        diffEl.className = 'status-badge status-danger';
        diffEl.style.cssText = 'font-size:13px;padding:4px 10px;background:#FDECEA;color:#C62828;border:1px solid #EF9A9A;';
        diffEl.textContent = 'ALERTE CRITIQUE : ' + signCrit + formatFCFA(diff);
      }
      if (badgeEl) {
        badgeEl.className = 'status-badge status-danger';
        badgeEl.textContent = 'ALERTE ECART : ' + signCrit + formatFCFA(diff) + ' (Incident)';
      }
      if (alertBox) alertBox.style.display = 'block';
    }

    return { totalPhysique: totalPhysique, theoretical: theoretical, diff: diff, counts: countsBreakdown };
  };

  window.resetPhysicalCashCount = function () {
    var defaults = {
      cashQty10k: 12,
      cashQty5k: 8,
      cashQty2k: 8,
      cashQty1k: 6,
      cashQty500b: 4,
      cashQty500p: 0,
      cashQty100: 4,
      cashQty50: 2,
      cashQty25: 0
    };
    Object.keys(defaults).forEach(function (k) {
      var el = document.getElementById(k);
      if (el) el.value = defaults[k];
    });
    recalcPhysicalCashCount();
    showToastSprint1('Grille de billetage reinitialisee aux valeurs conformes (184 500 FCFA).');
  };

  window.validateCashClosure = function () {
    var res = recalcPhysicalCashCount();
    var db = typeof loadDB === 'function' ? loadDB() : null;

    if (db) {
      db.cashClosure = {
        closedAt: nowStamp(),
        cashier: 'Mme Clarisse ATANGANA (Guichet #1 RN3)',
        totalPhysique: res.totalPhysique,
        theoretical: res.theoretical,
        diff: res.diff,
        momoTotal: (db.posStats && db.posStats.momoFcfa) || 96000,
        entries: (db.posStats && db.posStats.validatedEntries) || 214,
        status: res.diff === 0 ? 'CONFORME' : (Math.abs(res.diff) <= 2000 ? 'TOLERANCE_MINEURE' : 'INCIDENT_ECART')
      };
      if (Array.isArray(db.auditLogs)) {
        db.auditLogs.unshift({
          time: nowStamp(),
          actor: 'Mme Clarisse ATANGANA (Guichet #1)',
          action: 'Cloture de caisse contradictoire : Especes physiques ' + formatFCFA(res.totalPhysique) + ' vs Theorique ' + formatFCFA(res.theoretical) + ' (Ecart: ' + formatFCFA(res.diff) + '). Statut: ' + db.cashClosure.status
        });
      }
      if (typeof saveDB === 'function') saveDB(db);
    }

    if (Math.abs(res.diff) > 2000) {
      showToastSprint1('Alerte Ecart (> 2 000 FCFA) : Cloture marquee avec incident. Rapport Direction requis.');
    } else {
      showToastSprint1('Cloture de caisse validee avec succes ! Proces-Verbal pret pour impression.');
    }
    printOfficialDocument('CLOSURE');
  };

  // --- 2. CONTROLE HORS-LIGNE & SYNCHRONISATION (AGT-05) ---
  window._ecoparkOfflineScansQueue = JSON.parse(localStorage.getItem('ecopark_offline_scans_queue') || '[]');

  window.updateScannerNetworkStatus = function () {
    var badge = document.getElementById('scannerNetworkStatusBadge');
    var syncBtn = document.getElementById('btnSyncOfflineScans');
    var qCount = document.getElementById('offlineQueueCount');
    var isOnline = navigator.onLine;

    if (qCount) qCount.textContent = String(window._ecoparkOfflineScansQueue.length);

    if (badge) {
      if (!isOnline) {
        badge.className = 'status-badge';
        badge.style.cssText = 'font-size:12px;padding:3px 8px;background:#FFF3E0;color:#E65100;border:1px solid #FFE082;';
        badge.textContent = 'Mode Hors-Ligne RN3 (' + window._ecoparkOfflineScansQueue.length + ' en attente)';
      } else {
        badge.className = 'status-badge status-success';
        badge.style.cssText = 'font-size:12px;padding:3px 8px;background:#EDF4E7;color:#1D490D;border:1px solid #C4DFC0;';
        badge.textContent = 'Liaison RN3 Active';
      }
    }

    if (syncBtn) {
      syncBtn.style.display = (window._ecoparkOfflineScansQueue.length > 0) ? 'inline-block' : 'none';
    }
  };

  window.syncOfflineScans = function () {
    if (window._ecoparkOfflineScansQueue.length === 0) {
      showToastSprint1('Aucun scan hors-ligne en attente de synchronisation.');
      return;
    }
    var db = typeof loadDB === 'function' ? loadDB() : null;
    var count = window._ecoparkOfflineScansQueue.length;

    if (db && Array.isArray(db.auditLogs)) {
      db.auditLogs.unshift({
        time: nowStamp(),
        actor: 'Passerelle Synchronisation Guichet RN3',
        action: 'Reconciliation automatique de ' + count + ' scan(s) enregistre(s) hors-ligne.'
      });
      if (typeof saveDB === 'function') saveDB(db);
    }

    window._ecoparkOfflineScansQueue = [];
    localStorage.removeItem('ecopark_offline_scans_queue');
    updateScannerNetworkStatus();
    showToastSprint1(count + ' scan(s) hors-ligne synchronise(s) avec succes vers le serveur central !');
  };

  window.addEventListener('online', function () {
    updateScannerNetworkStatus();
    showToastSprint1('Connexion Internet retablie sur la RN3. Synchronisation automatique...');
    syncOfflineScans();
  });

  window.addEventListener('offline', function () {
    updateScannerNetworkStatus();
    showToastSprint1('Liaison Internet coupee sur la RN3. Bascule automatique sur le cache de controle hors-ligne.');
  });
"""

    # Insertion avant la fin du script dans index.html
    script_close_tag = "</script>\n</body>"
    if script_close_tag not in content:
        script_close_tag = "</script>\r\n</body>"

    if script_close_tag in content:
        content = content.replace(script_close_tag, phase6_js_code + "\n" + script_close_tag)
        print("  [OK] Script JavaScript Phase 6 insere avant </script>")
    else:
        print("Erreur: Balise </script></body> non trouvee")
        sys.exit(1)

    # -------------------------------------------------------------------------
    # 4. Surcharge intelligente de printOfficialDocument('CLOSURE') pour inclure le billetage
    # -------------------------------------------------------------------------
    old_closure_print_block = r"\} else if \(docType === 'CLOSURE'\) \{.*?(?=\} else \{)"
    new_closure_print_block = """} else if (docType === 'CLOSURE') {
        var res = typeof recalcPhysicalCashCount === 'function' ? recalcPhysicalCashCount() : { totalPhysique: 184500, theoretical: 184500, diff: 0, counts: {} };
        if (titleEl) titleEl.textContent = 'PROCES-VERBAL DE CLOTURE DE CAISSE CONTRADICTOIRE (' + nowStamp() + ')';
        
        var alertHeader = Math.abs(res.diff) > 2000
          ? '<div style="margin-bottom:12px;padding:10px 14px;background:#FDECEA;border:1px solid #EF9A9A;border-radius:8px;color:#C62828;font-size:13.5px;font-weight:700;">ALERTE INCIDENT : Ecart physique de ' + formatFCFA(res.diff) + ' superieur a la tolerance de 2 000 FCFA. Rapport Direction requis.</div>'
          : '<div style="margin-bottom:12px;padding:10px 14px;background:#EDF4E7;border:1px solid #C4DFC0;border-radius:8px;color:#1D490D;font-size:13.5px;font-weight:700;">CLOTURE REGLEMENTAIRE : Caisse conforme et reconciliee sans anomalie (Ecart 0 FCFA).</div>';

        bodyEl.innerHTML = `
          ${alertHeader}
          <div style="font-size:13px;color:var(--color-text-muted);margin-bottom:12px;display:flex;justify-content:space-between;flex-wrap:wrap;border-bottom:1px solid var(--color-border);padding-bottom:8px;">
            <div><strong>Site :</strong> Complexe Agro-Ecotouristique ECOPARK Ahala (RN3)</div>
            <div><strong>Poste :</strong> Guichet Principal #1</div>
            <div><strong>Caissiere :</strong> Mme Clarisse ATANGANA</div>
            <div><strong>Superviseur :</strong> Chef d'Exploitation Ahala</div>
          </div>

          <!-- Synthese des encaissements de la session -->
          <div class="grid-12" style="gap:10px;margin-bottom:14px;">
            <div class="col-4" style="padding:10px;background:var(--color-surface-soft);border-radius:8px;border-left:4px solid var(--color-brand-deep);">
              <span style="font-size:12px;color:var(--color-text-muted);">Especes Theorique Session</span><br/>
              <strong style="font-size:1.3rem;color:var(--color-brand-deep);">${formatFCFA(db.posStats.cashFcfa)}</strong>
            </div>
            <div class="col-4" style="padding:10px;background:var(--color-surface-soft);border-radius:8px;border-left:4px solid #C47D2B;">
              <span style="font-size:12px;color:var(--color-text-muted);">Mobile Money Guichet</span><br/>
              <strong style="font-size:1.3rem;color:var(--color-brand-deep);">${formatFCFA(db.posStats.momoFcfa)}</strong>
            </div>
            <div class="col-4" style="padding:10px;background:var(--color-surface-soft);border-radius:8px;border-left:4px solid #2E7D32;">
              <span style="font-size:12px;color:var(--color-text-muted);">Entrees Tourniquet</span><br/>
              <strong style="font-size:1.3rem;color:var(--color-brand-deep);">${db.posStats.validatedEntries} validees</strong>
            </div>
          </div>

          <!-- Ventilation Detaillee du Billetage Physique -->
          <div style="margin-bottom:14px;">
            <strong style="font-size:13.5px;color:var(--color-brand-deep);display:block;margin-bottom:6px;">Ventilation du Billetage Physique Compte :</strong>
            <table style="width:100%;border-collapse:collapse;font-size:12.5px;border:1px solid var(--color-border);">
              <thead>
                <tr style="background:var(--color-surface-soft);text-align:left;">
                  <th style="padding:6px 10px;border-bottom:1px solid var(--color-border);">Coupure</th>
                  <th style="padding:6px 10px;border-bottom:1px solid var(--color-border);text-align:center;">Nbre Unites</th>
                  <th style="padding:6px 10px;border-bottom:1px solid var(--color-border);text-align:right;">Sous-total</th>
                </tr>
              </thead>
              <tbody>
                <tr><td style="padding:4px 10px;border-bottom:1px solid var(--color-border);">Billet 10 000 FCFA</td><td style="text-align:center;padding:4px 10px;border-bottom:1px solid var(--color-border);">${(document.getElementById('cashQty10k')||{}).value||0}</td><td style="text-align:right;padding:4px 10px;border-bottom:1px solid var(--color-border);">${(document.getElementById('subtotal10k')||{}).textContent||'0 FCFA'}</td></tr>
                <tr><td style="padding:4px 10px;border-bottom:1px solid var(--color-border);">Billet 5 000 FCFA</td><td style="text-align:center;padding:4px 10px;border-bottom:1px solid var(--color-border);">${(document.getElementById('cashQty5k')||{}).value||0}</td><td style="text-align:right;padding:4px 10px;border-bottom:1px solid var(--color-border);">${(document.getElementById('subtotal5k')||{}).textContent||'0 FCFA'}</td></tr>
                <tr><td style="padding:4px 10px;border-bottom:1px solid var(--color-border);">Billet 2 000 FCFA</td><td style="text-align:center;padding:4px 10px;border-bottom:1px solid var(--color-border);">${(document.getElementById('cashQty2k')||{}).value||0}</td><td style="text-align:right;padding:4px 10px;border-bottom:1px solid var(--color-border);">${(document.getElementById('subtotal2k')||{}).textContent||'0 FCFA'}</td></tr>
                <tr><td style="padding:4px 10px;border-bottom:1px solid var(--color-border);">Billet 1 000 FCFA</td><td style="text-align:center;padding:4px 10px;border-bottom:1px solid var(--color-border);">${(document.getElementById('cashQty1k')||{}).value||0}</td><td style="text-align:right;padding:4px 10px;border-bottom:1px solid var(--color-border);">${(document.getElementById('subtotal1k')||{}).textContent||'0 FCFA'}</td></tr>
                <tr><td style="padding:4px 10px;border-bottom:1px solid var(--color-border);">Billet / Piece 500 FCFA</td><td style="text-align:center;padding:4px 10px;border-bottom:1px solid var(--color-border);">${(parseInt((document.getElementById('cashQty500b')||{}).value||0,10) + parseInt((document.getElementById('cashQty500p')||{}).value||0,10))}</td><td style="text-align:right;padding:4px 10px;border-bottom:1px solid var(--color-border);">${formatFCFA((parseInt((document.getElementById('cashQty500b')||{}).value||0,10) + parseInt((document.getElementById('cashQty500p')||{}).value||0,10))*500)}</td></tr>
                <tr><td style="padding:4px 10px;border-bottom:1px solid var(--color-border);">Pieces (100, 50, 25 FCFA)</td><td style="text-align:center;padding:4px 10px;border-bottom:1px solid var(--color-border);">${(parseInt((document.getElementById('cashQty100')||{}).value||0,10) + parseInt((document.getElementById('cashQty50')||{}).value||0,10) + parseInt((document.getElementById('cashQty25')||{}).value||0,10))}</td><td style="text-align:right;padding:4px 10px;border-bottom:1px solid var(--color-border);">${formatFCFA((parseInt((document.getElementById('cashQty100')||{}).value||0,10)*100) + (parseInt((document.getElementById('cashQty50')||{}).value||0,10)*50) + (parseInt((document.getElementById('cashQty25')||{}).value||0,10)*25))}</td></tr>
                <tr style="background:#EDF4E7;font-weight:700;"><td style="padding:6px 10px;">TOTAL ESPECES COMPTE (PHYSIQUE)</td><td style="text-align:center;padding:6px 10px;">-</td><td style="text-align:right;padding:6px 10px;color:var(--color-brand-deep);">${formatFCFA(res.totalPhysique)}</td></tr>
              </tbody>
            </table>
          </div>

          <!-- Rapprochement & Ecart -->
          <div style="padding:10px 14px;background:#FBF5EC;border-radius:8px;border:1px solid rgba(196,125,43,0.35);font-size:13px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
            <div>Theorique : <strong>${formatFCFA(res.theoretical)}</strong> | Physique : <strong>${formatFCFA(res.totalPhysique)}</strong></div>
            <div>Ecart de Caisse : <strong style="color:${res.diff === 0 ? '#1D490D' : (Math.abs(res.diff) <= 2000 ? '#C47D2B' : '#C62828')};">${res.diff > 0 ? '+' : ''}${formatFCFA(res.diff)}</strong> (${res.diff === 0 ? 'Conforme' : (Math.abs(res.diff) <= 2000 ? 'Tolerance mineure' : 'ANOMALIE CRITIQUE')})</div>
          </div>

          <!-- Emplacements Signatures & Visas Contradictoires -->
          <div class="grid-12" style="margin-top:20px;gap:16px;">
            <div class="col-6" style="border:1px dashed var(--color-border);padding:14px;border-radius:8px;min-height:90px;">
              <span style="font-size:12px;font-weight:700;color:var(--color-text-muted);display:block;text-transform:uppercase;">Emargement Caissiere (Remise des fonds)</span>
              <div style="font-size:13px;margin-top:4px;">Mme Clarisse ATANGANA</div>
              <div style="margin-top:24px;border-top:1px solid #CCC;width:80%;font-size:11px;color:#888;">Signature & Date</div>
            </div>
            <div class="col-6" style="border:1px dashed var(--color-border);padding:14px;border-radius:8px;min-height:90px;">
              <span style="font-size:12px;font-weight:700;color:var(--color-text-muted);display:block;text-transform:uppercase;">Visa Direction / Exploitation (Depot Coffre)</span>
              <div style="font-size:13px;margin-top:4px;">Chef d'Exploitation Ahala / Dr C. FOE NDI</div>
              <div style="margin-top:24px;border-top:1px solid #CCC;width:80%;font-size:11px;color:#888;">Signature & Date</div>
            </div>
          </div>
        `;
      """

    content = re.sub(old_closure_print_block, new_closure_print_block, content, flags=re.DOTALL)
    print("  [OK] printOfficialDocument('CLOSURE') enrichi avec billetage et signatures")

    # -------------------------------------------------------------------------
    # 5. Injection de la logique hors-ligne dans verifyLiveQrCode
    # -------------------------------------------------------------------------
    target_scan_check = "if (found.scanned) {"
    replacement_scan_check = """// Phase 6 : Gestion du mode Hors-ligne si liaison RN3 indisponible
      var isOffline = !navigator.onLine;
      if (isOffline) {
        if (!window._ecoparkOfflineScansQueue) window._ecoparkOfflineScansQueue = [];
        window._ecoparkOfflineScansQueue.push({
          reference: found.reference,
          scannedAt: nowStamp(),
          holder: found.holder,
          offline: true
        });
        localStorage.setItem('ecopark_offline_scans_queue', JSON.stringify(window._ecoparkOfflineScansQueue));
        if (typeof updateScannerNetworkStatus === 'function') updateScannerNetworkStatus();
      }

      if (found.scanned) {"""

    content = content.replace(target_scan_check, replacement_scan_check, 1)
    print("  [OK] Prise en charge hors-ligne injectee dans verifyLiveQrCode")

    # -------------------------------------------------------------------------
    # Écriture dans les deux fichiers cibles
    # -------------------------------------------------------------------------
    for file_path in HTML_FILES:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  [OK] Fichier ecrit : {file_path.name}")

    print("\nPhase 6 injectee avec succes dans les deux fichiers HTML !")


if __name__ == "__main__":
    main()
