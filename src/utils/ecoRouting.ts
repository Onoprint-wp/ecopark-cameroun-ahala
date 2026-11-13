// ============================================================================
// ECOPARK CAMEROUN (YAOUNDÉ – AHALA) — SPA & VERCEL ROUTING ENGINE
// (src/utils/ecoRouting.ts)
// Bidirectional synchronization between Vercel rewrites, Browser History,
// ActiveView navigation, and AhalaShowcase tabs.
// ============================================================================

import type { ActiveView } from '../types/ecosystem.ts';

export type ShowcaseTab = 'hebergements' | 'saveurs' | 'tarifs' | 'entreprise' | 'formation';

export const VIEW_PATH_MAP: Record<ActiveView, string> = {
  accueil: '/',
  sentiers: '/activites',
  biodiversite: '/decouvrir',
  billetterie: '/reserver',
  pass: '/mon-espace',
  ranger: '/exploitation',
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
  if (clean === '/mon-espace' || clean === '/mes-reservations') return 'pass';
  if (
    clean === '/exploitation' ||
    clean === '/guichet' ||
    clean === '/direction' ||
    clean === '/admin'
  ) {
    return 'ranger';
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
