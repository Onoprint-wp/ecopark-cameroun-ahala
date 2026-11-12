# FICHE METIER 01 : AGENT DE GUICHET & BILLETTERIE
**Projet** : ECOPARK CAMEROUN (Yaoundé-Ahala)
**Rôle RBAC** : `agent_guichet` (Accès POS, Vente Billets & bracelets, Encaissement Mobile Money / Espèces)
**Objectif** : Emettre un billet ou bracelet en moins de 30 secondes sans erreur de caisse.

---

## 1. Ouverture de Poste (08h00)
1. Allumer la tablette ou le terminal POS et vérifier la connexion Wi-Fi / 4G (ou le témoin **Mode Hors-Ligne Actif**).
2. Se connecter sur la console avec son identifiant nominatif `agent_guichet` (ne jamais partager son code PIN).
3. Vérifier le fond de caisse initial (espèces FCFA) et le stock de bracelets par couleur (Adulte, Enfant, VIP).
4. En cas de fort ensoleillement en extérieur, activer le **Mode Soleil (`sunMode`)** en haut à droite pour un contraste maximal.

---

## 2. Encaissement & Emission de Billet
1. **Sélection du Pass** : Choisir la formule demandée par le visiteur :
   - Pass Découverte : `2 000 FCFA`
   - Pass Loisirs : `5 000 FCFA`
   - Pass VIP Tout Inclus : `10 000 FCFA`
2. **Mode de Règlement** :
   - **Mobile Money (MTN MoMo / Orange Money)** : Saisir le numéro du client, lancer la requête Push USSD et attendre le statut `CONFIRMED` (ne jamais remettre le billet sur simple capture d'écran SMS).
   - **Espèces FCFA** : Encaisser le montant exact, saisir l'encaissement et remettre le reçu + QR Code.
3. **Remise du Bracelet** : Poser et sceller le bracelet au poignet du visiteur immédiatement après validation.

---

## 3. Clôture de Caisse (17h45)
1. Cliquer sur **Clôturer ma session de caisse** dans l'interface Guichet.
2. Compter les espèces physiques et vérifier la concordance avec le total théorique affiché (`Ecart cible = 0 FCFA`).
3. Synchroniser les éventuelles ventes hors-ligne en attente (`IndexedDB -> Supabase`).
4. Signer la feuille de remise de caisse contradictoire avec le Responsable d'Exploitation.

---

## 4. Règles d'Or & Sécurité
- **Zéro Billet Papier Libre** : Toute entrée doit générer un QR Code signé numériquement.
- **Mode Hors-Ligne** : Si la 4G coupe, continuer la vente normalement en espèces ; la synchronisation s'effectue automatiquement dès le retour réseau.
