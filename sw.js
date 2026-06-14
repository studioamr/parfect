/* PARFECT service worker: la app funciona offline una vez visitada. */
const CACHE = 'parfect-v5';
const ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './icon.svg',
  './css/styles.css?v=5',
  './js/ui.js?v=5',
  './js/store.js?v=5',
  './js/stats.js?v=5',
  './js/trainer.js?v=5',
  './js/views-public.js?v=5',
  './js/views-home.js?v=5',
  './js/views-round.js?v=5',
  './js/views-modules.js?v=5',
  './js/party.js?v=5',
  './js/views-party.js?v=5',
  './js/sync.js?v=5',
  './js/app.js?v=5',
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
  e.respondWith(
    caches.match(e.request).then((hit) =>
      hit ||
      fetch(e.request).then((res) => {
        if (res.ok) {
          const copy = res.clone();
          caches.open(CACHE).then((c) => c.put(e.request, copy));
        }
        return res;
      }).catch(() => (e.request.mode === 'navigate' ? caches.match('./') : undefined))
    )
  );
});
