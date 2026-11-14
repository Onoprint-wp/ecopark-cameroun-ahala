// ============================================================================
// ECOPARK CAMEROUN (YAOUNDÉ, AHALA) - PAGES LÉGALES & CONFORMITÉ
// (src/components/legal/LegalNoticeView.tsx)
// Mentions Légales, CGV / Billetterie FCFA & Politique de Confidentialité
// ============================================================================

import React, { useState, useEffect } from 'react';
import { ShieldCheck, FileText, Scale, Lock, ArrowLeft } from 'lucide-react';
import { ImmersiveSection } from '../layout/ImmersiveSection';
import { useEcoPark } from '../../context/EcoParkContext';
import { resolveLegalTabFromPath, type LegalTab } from '../../utils/ecoRouting';

export const LegalNoticeView: React.FC = () => {
  const { setActiveView } = useEcoPark();
  const [tab, setTab] = useState<LegalTab>(() =>
    typeof window !== 'undefined' ? resolveLegalTabFromPath(window.location.pathname) : 'mentions'
  );

  useEffect(() => {
    const onPop = () => setTab(resolveLegalTabFromPath(window.location.pathname));
    window.addEventListener('popstate', onPop);
    return () => window.removeEventListener('popstate', onPop);
  }, []);

  const selectTab = (next: LegalTab, path: string) => {
    setTab(next);
    if (typeof window !== 'undefined' && window.location.pathname !== path) {
      window.history.pushState({ legalTab: next }, '', path);
    }
  };

  return (
    <div className="eco-view-enter space-y-10 pb-16">
      <ImmersiveSection variant="forest" className="py-10">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="inline-flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-[#B7E4C7]">
              <Scale className="w-4 h-4 text-[#74C69D]" />
              <span>Informations Légales &amp; Réglementaires · MPECK MULTI-SERVICES</span>
            </div>
            <h1 className="font-['Barlow_Semi_Condensed'] text-2xl sm:text-4xl font-bold text-white mt-1">
              Mentions Légales, CGV &amp; Protection des Données
            </h1>
          </div>
          <button
            type="button"
            onClick={() => setActiveView('accueil')}
            className="px-4 py-2.5 rounded-xl bg-white/10 hover:bg-white/20 text-white border border-white/25 text-xs font-bold inline-flex items-center gap-2 cursor-pointer self-start md:self-auto"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Retour à l&apos;accueil</span>
          </button>
        </div>
      </ImmersiveSection>

      <div className="eco-container max-w-4xl space-y-6">
        <div className="flex flex-wrap gap-2">
          <button
            type="button"
            onClick={() => selectTab('mentions', '/mentions-legales')}
            className={`px-4 py-2.5 rounded-xl text-xs font-bold flex items-center gap-2 cursor-pointer transition-colors ${
              tab === 'mentions'
                ? 'bg-[var(--brand-primary)] text-white'
                : 'bg-[var(--bg-surface)] border border-[var(--border-default)] text-[var(--text-primary)]'
            }`}
          >
            <FileText className="w-4 h-4" />
            <span>Mentions Légales</span>
          </button>
          <button
            type="button"
            onClick={() => selectTab('cgv', '/cgv')}
            className={`px-4 py-2.5 rounded-xl text-xs font-bold flex items-center gap-2 cursor-pointer transition-colors ${
              tab === 'cgv'
                ? 'bg-[var(--brand-primary)] text-white'
                : 'bg-[var(--bg-surface)] border border-[var(--border-default)] text-[var(--text-primary)]'
            }`}
          >
            <Scale className="w-4 h-4" />
            <span>CGV &amp; Billetterie FCFA</span>
          </button>
          <button
            type="button"
            onClick={() => selectTab('confidentialite', '/confidentialite')}
            className={`px-4 py-2.5 rounded-xl text-xs font-bold flex items-center gap-2 cursor-pointer transition-colors ${
              tab === 'confidentialite'
                ? 'bg-[var(--brand-primary)] text-white'
                : 'bg-[var(--bg-surface)] border border-[var(--border-default)] text-[var(--text-primary)]'
            }`}
          >
            <Lock className="w-4 h-4" />
            <span>Confidentialité (Loi n° 2010/012)</span>
          </button>
        </div>

        <div className="p-6 sm:p-8 rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-default)] shadow-xs space-y-5 text-sm text-[var(--text-primary)] leading-relaxed">
          {tab === 'mentions' && (
            <div className="space-y-4">
              <h2 className="font-['Barlow_Semi_Condensed'] text-2xl font-bold">
                1. Éditeur &amp; Exploitant du Complexe ECOPARK CAMEROUN
              </h2>
              <p className="text-xs sm:text-sm text-[var(--text-muted)]">
                Le complexe écologique, touristique, hôtelier, gastronomique et de formation professionnelle{' '}
                <strong>ECOPARK CAMEROUN</strong> est exploité par la société <strong>MPECK MULTI-SERVICES</strong>, fondée et promue par le <strong>Dr Christophe FOE NDI</strong>.
              </p>
              <ul className="space-y-2 text-xs sm:text-sm list-disc pl-5">
                <li>
                  <strong>Siège &amp; Site d&apos;exploitation :</strong> Quartier Ahala Barrière, Route Nationale N°3 (RN3), en face de la station-service Tradex Ahala, Yaoundé, République du Cameroun.
                </li>
                <li>
                  <strong>Téléphones officiels :</strong>{' '}
                  <a href="tel:+237672564598" className="text-[var(--brand-primary)] underline">+237 672 56 45 98</a> /{' '}
                  <a href="tel:+237697136203" className="text-[var(--brand-primary)] underline">+237 697 13 62 03</a> (Parc &amp; Loisirs) ·{' '}
                  <a href="tel:+237694601449" className="text-[var(--brand-primary)] underline">+237 694 60 14 49</a> (Réception Hôtels 24h/24).
                </li>
                <li>
                  <strong>Contact électronique :</strong>{' '}
                  <a href="mailto:info@ecopark-yaounde.com" className="text-[var(--brand-primary)] underline">
                    info@ecopark-yaounde.com
                  </a>
                </li>
                <li>
                  <strong>Agrément Formation Professionnelle :</strong> Centre de Formation Professionnelle (CFP ECOPARK) agréé par le Ministère de l&apos;Emploi et de la Formation Professionnelle (MINEFOP), diplômes DQP / CQP.
                </li>
              </ul>
            </div>
          )}

          {tab === 'cgv' && (
            <div className="space-y-4">
              <h2 className="font-['Barlow_Semi_Condensed'] text-2xl font-bold">
                2. Conditions Générales de Vente, Tarifs FCFA &amp; Garantie Météo
              </h2>
              <ul className="space-y-2.5 text-xs sm:text-sm list-disc pl-5">
                <li>
                  <strong>Devise officielle :</strong> Tous les tarifs du Parc, du Jardin Zoologique, de la Piscine Semi-Olympique, des Cités Hôtelières (Ewondo, Chanthel, Bene), du restaurant <em>Le Château des Saveurs</em> et du CFP sont exprimés en <strong>Francs CFA (XAF / FCFA) TTC</strong>.
                </li>
                <li>
                  <strong>Horaires d&apos;ouverture :</strong> Parc &amp; Loisirs ouverts du mardi au dimanche de 09h00 à 18h00 (fermeture hebdomadaire le lundi pour repos biologique et maintenance). Réception Hôtelière ouverte 24h/24 et 7j/7. Restaurant ouvert 7j/7 de 07h00 à 23h00.
                </li>
                <li>
                  <strong>Tarif Enfant &amp; Groupes :</strong> Gratuité pour les enfants de moins de 3 ans. Le tarif réduit Groupe (-30 % sur l&apos;entrée adulte parc) s&apos;applique exclusivement aux réservations constituées d&apos;au moins <strong>20 participants</strong>.
                </li>
                <li>
                  <strong>Contrôle d&apos;accès QR :</strong> Chaque Pass QR (<code>ECP-2026-XXXXX</code>) est personnel et validé uniquement par les agents habilités au poste d&apos;entrée RN3 d&apos;Ahala Barrière.
                </li>
                <li>
                  <strong>Garantie Météo RN3 :</strong> En cas de fortes intempéries tropicales constatées par l&apos;exploitation, le visiteur bénéficie d&apos;un report gratuit de sa date de visite valable 90 jours, ou d&apos;une annulation sans frais effectuée au moins 48h avant le créneau réservé.
                </li>
              </ul>
            </div>
          )}

          {tab === 'confidentialite' && (
            <div className="space-y-4">
              <h2 className="font-['Barlow_Semi_Condensed'] text-2xl font-bold flex items-center gap-2">
                <ShieldCheck className="w-5 h-5 text-[var(--brand-primary)]" />
                <span>3. Protection des Données Personnelles (Loi n° 2010/012 &amp; RGPD)</span>
              </h2>
              <p className="text-xs sm:text-sm text-[var(--text-muted)]">
                Conformément à la Loi camerounaise n° 2010/012 du 21 décembre 2010 relative à la cybersécurité et à la cybercriminalité ainsi qu&apos;aux standards internationaux RGPD :
              </p>
              <ul className="space-y-2.5 text-xs sm:text-sm list-disc pl-5">
                <li>
                  <strong>Finalité stricte :</strong> Vos nom, email et numéro de téléphone ne sont collectés que pour l&apos;émission de vos Pass QR nominatifs, vos réservations hôtelières, vos devis B2B/CFP et la sécurité d&apos;accès au domaine.
                </li>
                <li>
                  <strong>Chiffrement &amp; Cloisonnement :</strong> Les mots de passe sont dérivés cryptographiquement (PBKDF2-HMAC-SHA256 / Supabase Auth) et chaque Espace Cliente est strictement isolé. Aucun visiteur tiers ne peut consulter vos réservations.
                </li>
                <li>
                  <strong>Droit d&apos;accès, de rectification et d&apos;effacement :</strong> Vous pouvez modifier votre mot de passe ou supprimer/anonymiser intégralement votre compte directement depuis votre profil (<code>/connexion</code>) ou en écrivant à{' '}
                  <a href="mailto:info@ecopark-yaounde.com" className="text-[var(--brand-primary)] underline">
                    info@ecopark-yaounde.com
                  </a>.
                </li>
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
