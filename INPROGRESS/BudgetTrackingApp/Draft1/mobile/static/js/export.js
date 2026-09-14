/**
 * export.js — Backup and restore (phone ↔ laptop)
 *
 * Layer: Export / import (uses db.js, not UI directly except via app.js buttons)
 * Role: Packages all local data into downloadable JSON/CSV files, or restores
 *       from a JSON backup. Matches shared export schema for future Python import.
 *
 * Flow: Settings page buttons → exportJsonFile / exportCsvFile / importJsonFile
 *       → db.js replaceAllData on import
 */

import {
  EXPORT_VERSION,
  validateExportBundle,
} from "./models.js";
import {
  getCategories,
  getSettings,
  getTransactions,
  replaceAllData,
} from "./db.js";

/**
 * Reads all data from IndexedDB and builds the standard export object.
 *
 * @returns {Promise<Object>} { version, exported_at, settings, categories, transactions }
 */
export async function buildExportBundle() {
  const [settings, categories, transactions] = await Promise.all([
    getSettings(),
    getCategories(),
    getTransactions(),
  ]);

  return {
    version: EXPORT_VERSION,
    exported_at: new Date().toISOString(),
    settings,
    categories,
    transactions,
  };
}

/**
 * Downloads a JSON backup file (Settings → Export JSON).
 * User can AirDrop/email this to their laptop for Python analysis later.
 *
 * @returns {Promise<void>}
 */
export async function exportJsonFile() {
  const bundle = await buildExportBundle();
  const filename = `budget_backup_${new Date().toISOString().slice(0, 10)}.json`;
  downloadTextFile(filename, JSON.stringify(bundle, null, 2), "application/json");
}

/**
 * Downloads transactions as CSV for spreadsheets (Settings → Export CSV).
 * Category ids are resolved to names; amounts converted from pence to pounds.
 *
 * @returns {Promise<void>}
 */
export async function exportCsvFile() {
  const [categories, transactions] = await Promise.all([
    getCategories(),
    getTransactions(),
  ]);

  const categoryMap = new Map(categories.map((item) => [item.id, item.name]));
  const header = ["date", "type", "category", "amount_gbp", "note"];
  const rows = transactions.map((item) => [
    item.date,
    item.type,
    categoryMap.get(item.category_id) ?? "Unknown",
    (item.amount / 100).toFixed(2),
    item.note ?? "",
  ]);

  const csv = [header, ...rows]
    .map((row) => row.map(escapeCsvCell).join(","))
    .join("\n");

  const filename = `budget_transactions_${new Date().toISOString().slice(0, 10)}.csv`;
  downloadTextFile(filename, csv, "text/csv");
}

/**
 * Reads a JSON backup from the file picker and replaces all on-device data.
 * Called from app.js initSettingsPage when user taps Import.
 *
 * @param {File} file - Selected .json file from <input type="file">
 * @returns {Promise<Object>} The validated import bundle
 */
export async function importJsonFile(file) {
  const text = await file.text();
  const bundle = validateExportBundle(JSON.parse(text));

  await replaceAllData({
    settings: bundle.settings,
    categories: bundle.categories,
    transactions: bundle.transactions,
  });

  return bundle;
}

/**
 * Triggers a browser download of a text file (internal helper).
 *
 * @param {string} filename - e.g. budget_backup_2026-06-17.json
 * @param {string} content - File body
 * @param {string} mimeType - e.g. application/json
 * @returns {void}
 */
function downloadTextFile(filename, content, mimeType) {
  const blob = new Blob([content], { type: mimeType });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");

  link.href = url;
  link.download = filename;
  link.click();

  URL.revokeObjectURL(url);
}

/**
 * Escapes a CSV cell if it contains comma, quote, or newline (internal helper).
 *
 * @param {*} value - Cell value
 * @returns {string} Safe CSV field
 */
function escapeCsvCell(value) {
  const text = String(value ?? "");
  if (text.includes(",") || text.includes('"') || text.includes("\n")) {
    return `"${text.replaceAll('"', '""')}"`;
  }
  return text;
}
