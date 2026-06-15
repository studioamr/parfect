/* PARFECT service worker: la app funciona offline una vez visitada. */
const CACHE = 'parfect-v25';
const ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './icon.svg',
  './css/styles.css?v=25',
  './js/ui.js?v=25',
  './js/store.js?v=25',
  './js/stats.js?v=25',
  './js/trainer.js?v=25',
  './js/views-public.js?v=25',
  './js/views-home.js?v=25',
  './js/views-round.js?v=25',
  './js/views-modules.js?v=25',
  './js/drills-library.js?v=25',
  './js/party.js?v=25',
  './js/views-party.js?v=25',
  './js/trophies.js?v=25',
  './js/views-trophies.js?v=25',
  './js/strategy.js?v=25',
  './js/sync.js?v=25',
  './js/app.js?v=25',
];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(ASSETS)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (e) => {
  const url = new URL(e.request.url);
  if (e.request.method !== 'GET' || url.origin !== location.origin) return; // fuentes/CDN: red normal

  const isNav = e.request.mode === 'navigate' || url.pathname.endsWith('/') || url.pathname.endsWith('index.html');

  // HTML (navegación): red primero para ver siempre la última versión; cae a cache si no hay internet.
  if (isNav) {
    e.respondWith(
      fetch(e.request).then((res) => {
        const copy = res.clone();
        caches.open(CACHE).then((c) => c.put('./index.html', copy));
        return res;
      }).catch(() => caches.match('./index.html').then((h) => h || caches.match('./')))
    );
    return;
  }

  // Resto (assets con ?v=): cache primero, rápido; si no está, red y se guarda.
  e.respondWith(
    caches.match(e.request).then((hit) =>
      hit ||
      fetch(e.request).then((res) => {
        if (res.ok) {
          const copy = res.clone();
          caches.open(CACHE).then((c) => c.put(e.request, copy));
        }
        return res;
      })
    )
  );
});
