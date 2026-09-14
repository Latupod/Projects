/**
 * db.js — IndexedDB persistence layer
 *
 * Layer: Database (no UI, no business rules)
 * Role: Reads and writes records to the browser's on-device database.
 *       All data stays on the phone; works offline after first load.
 *
 * Flow: services/*.js → db.js → IndexedDB
 *       export.js → replaceAllData (full restore on import)
 *
 * Stores (like tables):
 *   - categories  — budget groups (Food, Rent, …)
 *   - transactions — individual income/expense entries
 *   - settings    — single app config record
 */

import {
  createCategory,
  createDefaultSettings,
  DEFAULT_CATEGORIES,
} from "./models.js";

const DB_NAME = "budget-tracker";
const DB_VERSION = 1;

/** Object store definitions: each record is keyed by its "id" field */
const STORES = {
  categories: { keyPath: "id" },
  transactions: { keyPath: "id" },
  settings: { keyPath: "id" },
};

/** Cached promise so the database is only opened once per app session */
let dbPromise = null;

/**
 * Opens (or creates) the IndexedDB database.
 * Internal helper — other functions call this via withStore or initDatabase.
 *
 * @returns {Promise<IDBDatabase>} Resolves to the live database connection
 */
function openDatabase() {
  if (!dbPromise) {
    dbPromise = new Promise((resolve, reject) => {
      const request = indexedDB.open(DB_NAME, DB_VERSION);

      // Runs only when DB is first created or DB_VERSION is bumped
      request.onupgradeneeded = () => {
        const db = request.result;

        for (const [name, options] of Object.entries(STORES)) {
          if (!db.objectStoreNames.contains(name)) {
            db.createObjectStore(name, options);
          }
        }
      };

      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
  }

  return dbPromise;
}

/**
 * Runs a callback against one object store inside a transaction.
 * Wraps IndexedDB's callback API so callers can use async/await.
 *
 * @param {string} storeName - "categories" | "transactions" | "settings"
 * @param {"readonly"|"readwrite"} mode - read-only or allow writes
 * @param {function(IDBObjectStore): IDBRequest|null} callback - e.g. store => store.getAll()
 * @returns {Promise<*>} Resolves with the IDBRequest result when the transaction completes
 */
async function withStore(storeName, mode, callback) {
  const db = await openDatabase();

  return new Promise((resolve, reject) => {
    const transaction = db.transaction(storeName, mode);
    const store = transaction.objectStore(storeName);
    const request = callback(store);

    transaction.oncomplete = () => resolve(request?.result ?? null);
    transaction.onerror = () => reject(transaction.error);
    if (request) {
      request.onerror = () => reject(request.error);
    }
  });
}

/**
 * App startup: open DB and insert default categories on first run.
 * Called once from app.js main().
 *
 * @returns {Promise<void>}
 */
export async function initDatabase() {
  await openDatabase();
  await seedDefaultsIfNeeded();
}

/**
 * First-launch setup: adds DEFAULT_CATEGORIES if not done yet.
 * Sets default_categories_created so this only runs once.
 *
 * @returns {Promise<void>}
 */
async function seedDefaultsIfNeeded() {
  const settings = await getSettings();

  if (settings.default_categories_created) {
    return;
  }

  for (const category of DEFAULT_CATEGORIES) {
    await addCategory(createCategory(category));
  }

  await saveSettings({
    ...settings,
    default_categories_created: true,
  });
}

/**
 * Returns every record in a store.
 * @param {string} storeName
 * @returns {Promise<Array<Object>>}
 */
export async function getAll(storeName) {
  return withStore(storeName, "readonly", (store) => store.getAll());
}

/**
 * Returns one record by primary key, or undefined if not found.
 * @param {string} storeName
 * @param {string} id
 * @returns {Promise<Object|undefined>}
 */
export async function getById(storeName, id) {
  return withStore(storeName, "readonly", (store) => store.get(id));
}

/**
 * Inserts a new record or updates an existing one (matched by record.id).
 * @param {string} storeName
 * @param {Object} record - Must include an "id" field
 * @returns {Promise<*>}
 */
export async function put(storeName, record) {
  return withStore(storeName, "readwrite", (store) => store.put(record));
}

/**
 * Deletes one record by id.
 * @param {string} storeName
 * @param {string} id
 * @returns {Promise<*>}
 */
export async function remove(storeName, id) {
  return withStore(storeName, "readwrite", (store) => store.delete(id));
}

/**
 * Deletes all records in a store (used internally before import).
 * @param {string} storeName
 * @returns {Promise<*>}
 */
export async function clearStore(storeName) {
  return withStore(storeName, "readwrite", (store) => store.clear());
}

/**
 * Loads app settings, or returns defaults if none saved yet.
 * @returns {Promise<Object>} Settings object (currency, term_start_month, …)
 */
export async function getSettings() {
  const existing = await getById("settings", "settings");
  return existing ?? createDefaultSettings();
}

/**
 * Persists the settings object (always id: "settings").
 * @param {Object} settings
 * @returns {Promise<*>}
 */
export async function saveSettings(settings) {
  return put("settings", settings);
}

/** @returns {Promise<Array<Object>>} All category records */
export async function getCategories() {
  return getAll("categories");
}

/**
 * Saves a new or updated category.
 * @param {Object} category - From createCategory() or an edited record
 */
export async function addCategory(category) {
  return put("categories", category);
}

/** @param {Object} category - Full category object with id */
export async function updateCategory(category) {
  return put("categories", category);
}

/** @param {string} id - Category id to remove */
export async function deleteCategory(id) {
  return remove("categories", id);
}

/** @returns {Promise<Array<Object>>} All transaction records */
export async function getTransactions() {
  return getAll("transactions");
}

/**
 * Saves a new transaction (from services/transactions.js after validation).
 * @param {Object} transaction - From createTransaction()
 */
export async function addTransaction(transaction) {
  return put("transactions", transaction);
}

/** @param {string} id - Transaction id to remove */
export async function deleteTransaction(id) {
  return remove("transactions", id);
}

/**
 * Wipes all stores and replaces with imported backup data.
 * Used by export.js importJsonFile — atomic full restore.
 *
 * @param {Object} params
 * @param {Object} params.settings
 * @param {Array<Object>} params.categories
 * @param {Array<Object>} params.transactions
 * @returns {Promise<void>}
 */
export async function replaceAllData({ settings, categories, transactions }) {
  const db = await openDatabase();

  return new Promise((resolve, reject) => {
    const storeNames = ["settings", "categories", "transactions"];
    const transaction = db.transaction(storeNames, "readwrite");

    transaction.oncomplete = () => resolve();
    transaction.onerror = () => reject(transaction.error);

    for (const name of storeNames) {
      transaction.objectStore(name).clear();
    }

    transaction.objectStore("settings").put(settings);
    for (const category of categories) {
      transaction.objectStore("categories").put(category);
    }
    for (const item of transactions) {
      transaction.objectStore("transactions").put(item);
    }
  });
}
