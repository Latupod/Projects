/**
 * app.js — Main application controller
 *
 * Layer: Application entry point (orchestrates everything)
 * Role: Starts the app, handles page navigation, wires each screen to its
 *       services and UI modules. This is the "main()" of the project.
 *
 * Grand scheme:
 *   1. initDatabase() — open IndexedDB, seed defaults
 *   2. registerServiceWorker() — enable offline use
 *   3. navigateTo(page) — load HTML fragment + run page init
 *   4. Each init*Page function calls services for data, ui/* for display
 *
 * Loaded from index.html as type="module".
 */

import { initDatabase, getSettings } from "./db.js";
import { currentYearMonth } from "./models.js";
import { getDashboardSummary } from "./services/dashboard.js";
import { listCategories } from "./services/budgets.js";
import { addTransaction, listTransactions } from "./services/transactions.js";
import {
  renderDashboardSummary,
  renderRecentTransactions,
} from "./ui/dashboard.js";
import { renderBudgetBars } from "./ui/budget-bars.js";
import { bindTransactionForm } from "./ui/transaction-form.js";
import {
  bindHistoryFilters,
  populateHistoryCategoryFilter,
  renderTransactionList,
} from "./ui/history-list.js";
import { exportCsvFile, exportJsonFile, importJsonFile } from "./export.js";

/** Maps route name (URL hash) to HTML file under pages/ */
const PAGE_FILES = {
  dashboard: "pages/dashboard.html",
  add: "pages/add-transaction.html",
  history: "pages/history.html",
  budgets: "pages/budgets.html",
  settings: "pages/settings.html",
};

/** Header title shown for each route */
const PAGE_TITLES = {
  dashboard: "Dashboard",
  add: "Add transaction",
  history: "History",
  budgets: "Budgets",
  settings: "Settings",
};

/** Currently active page name (dashboard, add, history, …) */
let currentPage = "dashboard";

/** Cached settings from DB (currency, etc.) — loaded once at startup */
let settings = null;

/**
 * Application entry point: DB init, service worker, first page load.
 * @returns {Promise<void>}
 */
async function main() {
  await initDatabase();
  settings = await getSettings();

  registerServiceWorker();
  bindNavigation();
  await navigateTo(getPageFromHash());

  // Re-navigate when user uses back/forward or hash links
  window.addEventListener("hashchange", () => {
    navigateTo(getPageFromHash());
  });
}

/**
 * Parses window.location.hash into a valid page name.
 * @returns {string} e.g. "dashboard" — defaults to dashboard if hash is unknown
 */
function getPageFromHash() {
  const page = window.location.hash.replace("#", "");
  return PAGE_FILES[page] ? page : "dashboard";
}

/**
 * Attaches click handlers to bottom navigation links.
 * Sets URL hash instead of full page reload (SPA-style routing).
 * @returns {void}
 */
function bindNavigation() {
  document.querySelectorAll("[data-page]").forEach((link) => {
    link.addEventListener("click", (event) => {
      const page = link.dataset.page;
      if (!PAGE_FILES[page]) {
        return;
      }

      event.preventDefault();
      window.location.hash = page;
    });
  });
}

/**
 * Switches to a page: updates nav/title, loads HTML, runs page-specific init.
 * @param {string} page - Route name from PAGE_FILES keys
 * @returns {Promise<void>}
 */
async function navigateTo(page) {
  currentPage = page;
  setActiveNav(page);
  setPageTitle(PAGE_TITLES[page]);

  const html = await loadPage(PAGE_FILES[page]);
  const container = document.getElementById("app-content");
  container.innerHTML = html;

  await initPage(page);
}

/**
 * Fetches a page HTML fragment from pages/.
 * @param {string} path - e.g. "pages/dashboard.html"
 * @returns {Promise<string>} HTML text to inject into #app-content
 */
async function loadPage(path) {
  const response = await fetch(path);
  if (!response.ok) {
    throw new Error(`Failed to load page: ${path}`);
  }
  return response.text();
}

/**
 * Highlights the active item in the bottom navigation bar.
 * @param {string} page - Current route name
 * @returns {void}
 */
function setActiveNav(page) {
  document.querySelectorAll(".bottom-nav__link").forEach((link) => {
    link.classList.toggle("bottom-nav__link--active", link.dataset.page === page);
  });
}

/**
 * Updates the header <h1> text.
 * @param {string} title - From PAGE_TITLES
 * @returns {void}
 */
function setPageTitle(title) {
  document.getElementById("page-title").textContent = title;
}

/**
 * Dispatches to the correct page initializer after HTML is injected.
 * @param {string} page - Route name
 * @returns {Promise<void>}
 */
async function initPage(page) {
  const categories = await listCategories();

  switch (page) {
    case "dashboard":
      await initDashboardPage(categories);
      break;
    case "add":
      initAddPage(categories);
      break;
    case "history":
      await initHistoryPage(categories);
      break;
    case "budgets":
      initBudgetsPage(categories);
      break;
    case "settings":
      initSettingsPage();
      break;
    default:
      break;
  }
}

/**
 * Dashboard: summary cards, budget bars, recent transactions.
 * @param {Array<Object>} categories - For name lookup in recent list
 * @returns {Promise<void>}
 */
async function initDashboardPage(categories) {
  const summary = await getDashboardSummary();
  renderDashboardSummary(
    document.getElementById("summary-grid"),
    summary,
    settings.currency
  );
  renderBudgetBars(
    document.getElementById("budget-bars"),
    summary.budgets,
    settings.currency
  );
  renderRecentTransactions(
    document.getElementById("recent-transactions"),
    summary.recent,
    categories,
    settings.currency
  );
}

/**
 * Add page: wire form submit → save transaction → go to dashboard.
 * @param {Array<Object>} categories - For category dropdown
 * @returns {void}
 */
function initAddPage(categories) {
  const form = document.getElementById("transaction-form");

  bindTransactionForm(form, {
    categories,
    onSubmit: async (payload) => {
      await addTransaction(payload);
      window.location.hash = "dashboard";
    },
  });
}

/**
 * History page: month/category filters and full transaction list.
 * @param {Array<Object>} categories
 * @returns {Promise<void>}
 */
async function initHistoryPage(categories) {
  const monthInput = document.getElementById("history-month");
  const categorySelect = document.getElementById("history-category");
  const listElement = document.getElementById("transaction-list");

  monthInput.value = currentYearMonth();
  populateHistoryCategoryFilter(categorySelect, categories);

  const refresh = async (filters) => {
    const transactions = await listTransactions(filters);
    renderTransactionList(listElement, transactions, categories, settings.currency);
  };

  bindHistoryFilters(document.getElementById("history-filters"), refresh);
  await refresh({
    month: monthInput.value,
    categoryId: "",
  });
}

/**
 * Budgets page: placeholder list of category limits (expand with edit UI).
 * @param {Array<Object>} categories
 * @returns {void}
 */
function initBudgetsPage(categories) {
  const listElement = document.getElementById("budget-list");

  // Expand: replace this placeholder with editable inputs per category.
  listElement.innerHTML = categories
    .map(
      (category) => `
        <li class="list__item">
          <div>
            <div class="list__primary">${category.name}</div>
            <div class="list__secondary">Monthly limit: £${Number(category.monthly_limit).toFixed(2)}</div>
          </div>
        </li>
      `
    )
    .join("");

  document.getElementById("add-category-btn")?.addEventListener("click", () => {
    // Expand: open a form or prompt to create a new category.
    alert("Expand budgets page: add category creation UI here.");
  });
}

/**
 * Settings page: export JSON/CSV and import JSON backup buttons.
 * @returns {void}
 */
function initSettingsPage() {
  document.getElementById("export-json-btn")?.addEventListener("click", () => {
    exportJsonFile();
  });

  document.getElementById("export-csv-btn")?.addEventListener("click", () => {
    exportCsvFile();
  });

  document.getElementById("import-btn")?.addEventListener("click", async () => {
    const fileInput = document.getElementById("import-file");
    const file = fileInput.files?.[0];

    if (!file) {
      alert("Choose a JSON backup file first.");
      return;
    }

    await importJsonFile(file);
    alert("Import complete.");
    window.location.hash = "dashboard";
  });
}

/**
 * Registers sw.js so the app can load offline after first visit.
 * @returns {void}
 */
function registerServiceWorker() {
  if (!("serviceWorker" in navigator)) {
    return;
  }

  navigator.serviceWorker.register("./sw.js").catch((error) => {
    console.warn("Service worker registration failed:", error);
  });
}

// Start the app; show friendly error if startup fails
main().catch((error) => {
  console.error(error);
  document.getElementById("app-content").innerHTML =
    `<p class="empty-state">Something went wrong starting the app. Check the console.</p>`;
});
