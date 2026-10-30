const CACHE_NAME = "data-talk-v2";

const FILES_TO_CACHE = [

    "./",
    "./index.html",

    "./manifest.json",

    "./css/style.css",
    "./css/layout.css",
    "./css/match.css",
    "./css/players.css",
    "./css/events.css",
    "./css/responsive.css",

    "./js/state.js",
    "./js/app.js",
    "./js/timer.js",
    "./js/scoreboard.js",
    "./js/players.js",
    "./js/events.js",
    "./js/timeline.js",
    "./js/substitutions.js",
    "./js/storage.js",
    "./js/export.js",
    "./js/stats.js",
    "./js/ui.js",

    "./assets/logo.png",
    "./icons/icon-192.png",
    "./icons/icon-512.png"
];


self.addEventListener("install", event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(FILES_TO_CACHE))
            .then(() => self.skipWaiting())
    );
});

self.addEventListener("fetch", event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => {

                return response || fetch(event.request);
            })
    );
});

self.addEventListener("activate", event => {
    event.waitUntil(
        clients.claim()
    );
});

