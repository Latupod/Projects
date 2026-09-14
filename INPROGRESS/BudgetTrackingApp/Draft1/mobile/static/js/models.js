/**
 * models.js — Data shapes, validation, and shared helpers
 *
 * Layer: Models (no database, no UI)
 * Role: Defines what a valid Category, Transaction, or Settings object looks like.
 *       Other files call these functions before saving data or displaying it.
 *
 * Flow: UI → services → createTransaction/createCategory (here) → db.js
 */

/** Allowed values for transaction.type */
export const TRANSACTION_TYPES = ["expense", "income"];

/** Version number embedded in JSON export files; must match on import */
export const EXPORT_VERSION = 1;

/**
 * Generates a unique ID for new records.
 * @returns {string} UUID v4, e.g. "a3f2b1c4-5678-90ab-cdef-1234567890ab"
 */
export function createId() {
  return crypto.randomUUID();
}

/**
 * Today's date in YYYY-MM-DD format (used for form defaults and filtering).
 * @returns {string} e.g. "2026-06-17"
 */
export function todayISO() {
  return new Date().toISOString().slice(0, 10);
}

/**
 * Current calendar month in YYYY-MM format (dashboard and history filters).
 * @returns {string} e.g. "2026-06"
 */
export function currentYearMonth() {
  const now = new Date();
  const month = String(now.getMonth() + 1).padStart(2, "0");
  return `${now.getFullYear()}-${month}`;
}

/**
 * Converts pounds (user input) to integer pence (storage format).
 * Avoids floating-point rounding errors when adding money.
 * @param {number|string} amount - Amount in pounds, e.g. 12.50
 * @returns {number} Amount in pence, e.g. 1250
 */
export function poundsToPence(amount) {
  return Math.round(Number(amount) * 100);
}

/**
 * Converts stored pence back to a pounds string with two decimal places.
 * @param {number} pence - Amount in pence, e.g. 1250
 * @returns {string} e.g. "12.50"
 */
export function penceToPounds(pence) {
  return (Number(pence) / 100).toFixed(2);
}

/**
 * Formats pence as a localised currency string for display in the UI.
 * @param {number} pence - Amount in pence
 * @param {string} [currency="GBP"] - ISO currency code from settings
 * @returns {string} e.g. "£12.50"
 */
export function formatMoney(pence, currency = "GBP") {
  const value = Number(pence) / 100;
  return new Intl.NumberFormat("en-GB", {
    style: "currency",
    currency,
  }).format(value);
}

/**
 * Creates a validated Category object ready to save to IndexedDB.
 * Called by db.js when seeding defaults or when you add category UI.
 *
 * @param {Object} params
 * @param {string} params.name - Display name, e.g. "Food"
 * @param {number} [params.monthly_limit=0] - Budget cap in pounds (not pence)
 * @param {string} [params.colour="#1a5f4a"] - Hex colour for charts/bars
 * @returns {{ id: string, name: string, monthly_limit: number, colour: string }}
 * @throws {Error} If name is missing or blank
 */
export function createCategory({ name, monthly_limit = 0, colour = "#1a5f4a" }) {
  if (!name?.trim()) {
    throw new Error("Category name is required");
  }

  return {
    id: createId(),
    name: name.trim(),
    monthly_limit: Number(monthly_limit) || 0,
    colour,
  };
}

/**
 * Creates a validated Transaction object ready to save to IndexedDB.
 * Called by services/transactions.js when the user submits the add form.
 *
 * @param {Object} params
 * @param {number|string} params.amount - Amount in pounds from the form
 * @param {string} params.date - ISO date YYYY-MM-DD
 * @param {string} params.category_id - ID linking to a Category record
 * @param {string} [params.note=""] - Optional description
 * @param {"expense"|"income"} [params.type="expense"]
 * @returns {{ id: string, amount: number, date: string, category_id: string, note: string, type: string }}
 *   amount is stored in pence
 * @throws {Error} If validation fails (bad type, amount, date, or category)
 */
export function createTransaction({ amount, date, category_id, note = "", type = "expense" }) {
  if (!TRANSACTION_TYPES.includes(type)) {
    throw new Error(`Invalid transaction type: ${type}`);
  }

  if (!category_id) {
    throw new Error("Category is required");
  }

  const pence = poundsToPence(amount);
  if (pence <= 0) {
    throw new Error("Amount must be greater than zero");
  }

  if (!date) {
    throw new Error("Date is required");
  }

  return {
    id: createId(),
    amount: pence,
    date,
    category_id,
    note: note.trim(),
    type,
  };
}

/**
 * Default app settings used on first launch before anything is saved.
 * @returns {{ id: string, currency: string, term_start_month: number, default_categories_created: boolean }}
 */
export function createDefaultSettings() {
  return {
    id: "settings",
    currency: "GBP",
    term_start_month: 9,
    default_categories_created: false,
  };
}

/** Starter categories inserted once on first app open (see db.js seedDefaultsIfNeeded) */
export const DEFAULT_CATEGORIES = [
  { name: "Food", monthly_limit: 200, colour: "#4CAF50" },
  { name: "Transport", monthly_limit: 80, colour: "#2196F3" },
  { name: "Rent", monthly_limit: 600, colour: "#9C27B0" },
  { name: "Entertainment", monthly_limit: 50, colour: "#FF9800" },
  { name: "Other", monthly_limit: 100, colour: "#607D8B" },
];

/**
 * Validates a JSON backup file before import (export.js → replaceAllData).
 * @param {Object} bundle - Parsed JSON from an export file
 * @returns {Object} The same bundle if valid
 * @throws {Error} If version mismatch or required arrays are missing
 */
export function validateExportBundle(bundle) {
  if (!bundle || bundle.version !== EXPORT_VERSION) {
    throw new Error("Unsupported export format");
  }

  if (!Array.isArray(bundle.categories) || !Array.isArray(bundle.transactions)) {
    throw new Error("Export is missing categories or transactions");
  }

  return bundle;
}
