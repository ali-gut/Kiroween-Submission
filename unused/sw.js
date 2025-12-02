// Service Worker - Prevents page reload and caches everything
const CACHE_NAME = 'witch-chat-v1';

self.addEventListener('install', (event) => {
    console.log('Service Worker installing');
    self.skipWaiting();
});

self.addEventListener('activate', (event) => {
    console.log('Service Worker activating');
    event.waitUntil(clients.claim());
});

self.addEventListener('fetch', (event) => {
    // Intercept all requests to prevent reload
    event.respondWith(
        caches.match(event.request).then((response) => {
            if (response) {
                return response;
            }
            return fetch(event.request).then((response) => {
                // Cache the response
                if (event.request.method === 'GET') {
                    const responseClone = response.clone();
                    caches.open(CACHE_NAME).then((cache) => {
                        cache.put(event.request, responseClone);
                    });
                }
                return response;
            });
        })
    );
});
