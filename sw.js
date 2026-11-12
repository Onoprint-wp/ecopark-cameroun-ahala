/**
 * sw.js - Service Worker PWA Offline-First pour ECOPARK CAMEROUN (Yaoundé-Ahala)
 * Assure la disponibilité hors-ligne du guichet POS, du scanner QR (AGT-05) et de la vitrine.
 */
const CACHE_NAME = 'ecopark-ahala-pwa-v5';
const CORE_ASSETS = [
  '/',
  '/index.html',
  '/manifest.json',
  '/content-snapshot.json',
  '/js/ecopark-data.js',
  '/js/ecopark-admin.js',
  '/locales/fr.json',
  '/locales/en.json'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(CORE_ASSETS)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;
  const reqUrl = new URL(event.request.url);
  if (reqUrl.origin !== self.location.origin) return;

  event.respondWith(
    fetch(event.request)
      .then((response) => {
        if (response && response.status === 200 && response.type === 'basic') {
          const clone = response.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
        }
        return response;
      })
      .catch(() =>
        caches.match(event.request).then((cached) => {
          if (cached) return cached;
          if (event.request.mode === 'navigate') {
            return caches.match('/index.html');
          }
          return new Response('', { status: 504, statusText: 'Offline' });
        })
      )
  );
});
