/**
 * sw.js — Service Worker (offline caching)
 *
 * Layer: PWA infrastructure (separate from app logic; runs in background)
 * Role: On first visit, caches all app files (HTML, CSS, JS). Later requests
 *       are served from cache so the app works without network on your iPhone.
 *
 * Registered from app.js registerServiceWorker().
 * Not an ES module — uses self.addEventListener API.
 */

/** Cache bucket name; bump version when you change ASSETS list to force refresh */
const CACHE_NAME = "budget-tracker-v1";

/** Every file the app needs to run offline (must stay in sync with project files) */
const ASSETS = [
  "./",
  "./index.html",
  "./manifest.json",
  "./pages/dashboard.html",
  "./pages/add-transaction.html",
  "./pages/history.html",
  "./pages/budgets.html",
  "./pages/settings.html",
  "./static/css/base.css",
  "./static/css/components.css",
  "./static/css/mobile.css",
  "./static/icons/icon.svg",
  "./static/js/app.js",
  "./static/js/db.js",
  "./static/js/models.js",
  "./static/js/export.js",
  "./static/js/services/transactions.js",
  "./static/js/services/budgets.js",
  "./static/js/services/dashboard.js",
  "./static/js/ui/dashboard.js",
  "./static/js/ui/transaction-form.js",
  "./static/js/ui/history-list.js",
  "./static/js/ui/budget-bars.js",
];

/**
 * Install: download and store all ASSETS in the browser cache.
 * skipWaiting() activates this worker immediately instead of waiting for tabs to close.
 */
self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS))
  );
  self.skipWaiting();
});

/**
 * Activate: delete old caches from previous CACHE_NAME versions.
 * claim() takes control of open pages right away.
 */
self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys
          .filter((key) => key !== CACHE_NAME)
          .map((key) => caches.delete(key))
      )
    )
  );
  self.clients.claim();
});

/**
 * Fetch: for each network request, return cached file if available,
 * otherwise fall back to network (cache-first strategy).
 */
self.addEventListener("fetch", (event) => {
  event.respondWith(
    caches.match(event.request).then((cached) => cached || fetch(event.request))
  );
});
