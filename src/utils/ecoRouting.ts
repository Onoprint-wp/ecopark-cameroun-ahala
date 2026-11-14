// ============================================================================
// ECOPARK CAMEROUN (YAOUNDE - AHALA) - SPA & VERCEL ROUTING ENGINE
// (src/utils/ecoRouting.ts)
// Bidirectional synchronization between Vercel rewrites, Browser History,
// ActiveView navigation, and AhalaShowcase tabs.
// ============================================================================

import type { ActiveView } from '../types/ecosystem.ts';

export type ShowcaseTab = 'hebergements' | 'saveurs' | 'tarifs' | 'entreprise' | 'formation';
export type LegalTab = 'mentions' | 'cgv' | 'confidentialite';

export const VIEW_PATH_MAP: Record<ActiveView, string> = {
  accueil: '/',
  sentiers: '/activites',
  biodiversite: '/decouvrir',
  billetterie: '/reserver',
  pass: '/mon-espace',
  ranger: '/exploitation',
  connexion: '/connexion',
  legal: '/mentions-legales',
  color_atlas: '/',
};

export const SHOWCASE_TAB_PATH_MAP: Record<ShowcaseTab, string> = {
  hebergements: '/hebergements',
  saveurs: '/restaurant',
  tarifs: '/tarifs',
  entreprise: '/pack-entreprise',
  formation: '/formation',
};

export const SHOWCASE_DEEP_PATHS: readonly string[] = [
  '/hebergements',
  '/hotellerie',
  '/sejour-restaurant',
  '/restaurant',
  '/tarifs',
  '/nos-tarifs',
  '/pack-entreprise',
  '/pack-ecole',
  '/groupes-evenements',
  '/agenda',
  '/evenements',
  '/formation',
  '/formations',
];

export function resolveViewFromPath(pathname: string): ActiveView | null {
  const clean = pathname.replace(/\/+$/, '').toLowerCase();
  if (clean === '' || clean === '/') return 'accueil';
  if (clean === '/activites' || clean === '/fiche-activite') return 'sentiers';
  if (clean === '/decouvrir') return 'biodiversite';
  if (
    clean === '/reserver' ||
    clean === '/rdv' ||
    clean === '/rendez-vous' ||
    clean === '/preparer-ma-visite'
  ) {
    return 'billetterie';
  }
  if (
    clean === '/mon-espace' ||
    clean === '/mes-reservations' ||
    clean === '/espace-cliente'
  ) {
    return 'pass';
  }
  if (
    clean === '/exploitation' ||
    clean === '/cockpit-pro' ||
    clean === '/guichet' ||
    clean === '/direction' ||
    clean === '/admin'
  ) {
    return 'ranger';
  }
  if (
    clean === '/connexion' ||
    clean === '/login' ||
    clean === '/inscription' ||
    clean === '/mon-compte'
  ) {
    return 'connexion';
  }
  if (
    clean === '/mentions-legales' ||
    clean === '/cgv' ||
    clean === '/cgu' ||
    clean === '/confidentialite'
  ) {
    return 'legal';
  }
  if (
    clean === '/hebergements' ||
    clean === '/hotellerie' ||
    clean === '/sejour-restaurant' ||
    clean === '/restaurant' ||
    clean === '/tarifs' ||
    clean === '/nos-tarifs' ||
    clean === '/pack-entreprise' ||
    clean === '/pack-ecole' ||
    clean === '/groupes-evenements' ||
    clean === '/formation' ||
    clean === '/formations' ||
    clean === '/agenda' ||
    clean === '/evenements' ||
    clean === '/contact' ||
    clean === '/whatsapp'
  ) {
    return 'accueil';
  }
  return null;
}

export function resolveShowcaseTabFromPath(pathname: string): ShowcaseTab {
  const clean = pathname.replace(/\/+$/, '').toLowerCase();
  if (clean === '/restaurant' || clean === '/sejour-restaurant') return 'saveurs';
  if (clean === '/tarifs' || clean === '/nos-tarifs') return 'tarifs';
  if (
    clean === '/pack-entreprise' ||
    clean === '/pack-ecole' ||
    clean === '/groupes-evenements' ||
    clean === '/agenda' ||
    clean === '/evenements'
  ) {
    return 'entreprise';
  }
  if (clean === '/formation' || clean === '/formations') return 'formation';
  return 'hebergements';
}

export function resolveLegalTabFromPath(pathname: string): LegalTab {
  const clean = pathname.replace(/\/+$/, '').toLowerCase();
  if (clean === '/cgv' || clean === '/cgu') return 'cgv';
  if (clean === '/confidentialite') return 'confidentialite';
  return 'mentions';
}

export interface ShowcaseNavDetail {
  tab?: ShowcaseTab;
  anchorId?: string;
}

export const SHOWCASE_NAV_EVENT = 'ecopark:showcase-nav';

export function dispatchShowcaseNavigation(detail: ShowcaseNavDetail): void {
  if (typeof window === 'undefined') return;
  if (detail.tab) {
    const nextPath = SHOWCASE_TAB_PATH_MAP[detail.tab];
    if (window.location.pathname !== nextPath) {
      window.history.pushState({ showcaseTab: detail.tab }, '', nextPath);
    }
  }
  window.dispatchEvent(new CustomEvent<ShowcaseNavDetail>(SHOWCASE_NAV_EVENT, { detail }));
}

/**
 * Retourne le point focal CSS (object-position) calibré sur les visages
 * pour chaque photographie officielle d'ECOPARK CAMEROUN à Yaoundé-Ahala,
 * garantissant qu'aucun visage n'est coupé quel que soit le ratio du conteneur.
 */
export function getPhotoObjectPosition(photoUrl?: string): string {
  if (!photoUrl) return '50% 50%';
  if (photoUrl.includes('IMG-20260713-WA0051')) return '50% 12%';
  if (photoUrl.includes('IMG_20260829_172016')) return '50% 20%';
  if (photoUrl.includes('IMG-20260809-WA0009')) return '50% 52%';
  if (photoUrl.includes('balade_pirogue3')) return '50% 60%';
  if (photoUrl.includes('local_cameroon_gastronomy_pergola')) return '56% 40%';
  if (photoUrl.includes('local_cameroon_cfp_students')) return '50% 28%';
  if (photoUrl.includes('local_cameroon_family_canopy')) return '50% 48%';
  if (photoUrl.includes('local_cameroon_pool_pirogue')) return '50% 55%';
  if (photoUrl.includes('chimpanze')) return '45% 35%';
  return '50% 50%';
}
