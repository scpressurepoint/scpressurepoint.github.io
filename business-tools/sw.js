const CACHE_NAME = 'ppw-cache-v1';
const ASSETS = [
  './',
  'index.html',
  'app.css',
  'data-migration.js',
  'manifest.json',
  'jobs.html',
  'calendar.html',
  'quick-add.html',
  'customer-tracker.html',
  'settings.html',
  'map.html',
  'estimate.html',
  'invoice.html',
  '../assets/images/Logo.png'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS))
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))
    )
  );
});

self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;
  event.respondWith(
    caches.match(event.request).then((cached) => {
      if (cached) return cached;
      return fetch(event.request)
        .then((response) => {
          const copy = response.clone();
          if (response.ok && response.type === 'basic') {
            caches.open(CACHE_NAME).then((cache) => cache.put(event.request, copy));
          }
          return response;
        })
        .catch(() => caches.match('index.html'));
    })
  );
});
