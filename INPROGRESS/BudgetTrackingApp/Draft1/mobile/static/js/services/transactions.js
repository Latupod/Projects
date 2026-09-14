/**
 * services/transactions.js — Transaction business logic
 *
 * Layer: Services (between UI and database)
 * Role: Filtering, sorting, adding, and aggregating transactions.
 *       Validates via models.js before saving; never talks to the DOM.
 *
 * Flow: app.js / dashboard.js → this file → db.js + models.js
 */

import {
  addTransaction as saveTransaction,
  deleteTransaction as removeTransaction,
  getTransactions,
} from "../db.js";
import { createTransaction } from "../models.js";

/**
 * Loads transactions from DB, optionally filters, sorts newest first.
 * Used by History page, Dashboard summary, and budget calculations.
 *
 * @param {Object} [filters={}]
 * @param {string} [filters.month=""] - YYYY-MM; empty = all months
 * @param {string} [filters.categoryId=""] - Category id; empty = all categories
 * @returns {Promise<Array<Object>>} Filtered, sorted transaction list
 */
export async function listTransactions(filters = {}) {
  const transactions = await getTransactions();
  const { month = "", categoryId = "" } = filters;

  return transactions
    .filter((item) => {
      const matchesMonth = month ? item.date.startsWith(month) : true;
      const matchesCategory = categoryId ? item.category_id === categoryId : true;
      return matchesMonth && matchesCategory;
    })
    .sort((a, b) => b.date.localeCompare(a.date));
}

/**
 * Validates form input, saves a new transaction, returns it.
 * Called from app.js when the user submits the Add Transaction form.
 *
 * @param {Object} input - Raw form fields (amount in pounds, not pence)
 * @returns {Promise<Object>} The saved transaction (amount in pence)
 */
export async function addTransaction(input) {
  const transaction = createTransaction(input);
  await saveTransaction(transaction);
  return transaction;
}

/**
 * Removes a transaction by id (wire up from History UI when you add delete).
 * @param {string} id
 * @returns {Promise<void>}
 */
export async function deleteTransaction(id) {
  await removeTransaction(id);
}

/**
 * Sums amounts for one type (expense or income) across a transaction list.
 * Pure function — no DB access. Used by dashboard summary.
 *
 * @param {Array<Object>} transactions - Already filtered list
 * @param {"expense"|"income"} type
 * @returns {number} Total in pence
 */
export function sumByType(transactions, type) {
  return transactions
    .filter((item) => item.type === type)
    .reduce((total, item) => total + item.amount, 0);
}

/**
 * Totals expense spending per category for budget progress bars.
 *
 * @param {Array<Object>} transactions - Usually one month's expenses
 * @param {Array<Object>} categories - All categories (initialises map keys)
 * @returns {Map<string, number>} category_id → total spent in pence
 */
export function spendingByCategory(transactions, categories) {
  const totals = new Map(categories.map((category) => [category.id, 0]));

  for (const item of transactions) {
    if (item.type !== "expense") {
      continue;
    }
    totals.set(item.category_id, (totals.get(item.category_id) ?? 0) + item.amount);
  }

  return totals;
}
