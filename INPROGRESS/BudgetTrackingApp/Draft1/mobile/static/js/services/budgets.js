/**
 * services/budgets.js — Category and budget progress logic
 *
 * Layer: Services
 * Role: Lists categories, updates limits, computes how much budget is left
 *       per category for the current month.
 *
 * Flow: dashboard.js / budgets page → this file → db.js + transactions.js
 */

import { getCategories, updateCategory } from "../db.js";
import { spendingByCategory } from "./transactions.js";

/**
 * All categories sorted alphabetically (dropdowns, budget list, dashboard).
 * @returns {Promise<Array<Object>>}
 */
export async function listCategories() {
  const categories = await getCategories();
  return categories.sort((a, b) => a.name.localeCompare(b.name));
}

/**
 * Updates a category's monthly_limit in pounds.
 * Expand: call from Budgets page when user edits a limit.
 *
 * @param {string} categoryId
 * @param {number|string} monthlyLimit - New limit in pounds
 * @returns {Promise<Object>} Updated category record
 * @throws {Error} If category id not found
 */
export async function updateCategoryLimit(categoryId, monthlyLimit) {
  const categories = await getCategories();
  const category = categories.find((item) => item.id === categoryId);

  if (!category) {
    throw new Error("Category not found");
  }

  const updated = {
    ...category,
    monthly_limit: Number(monthlyLimit) || 0,
  };

  await updateCategory(updated);
  return updated;
}

/**
 * For each category, calculates spent vs limit for one month (dashboard bars).
 *
 * @param {Array<Object>} transactions - Typically this month's transactions
 * @param {string} month - YYYY-MM used to filter transaction dates
 * @returns {Promise<Array<Object>>} One progress object per category:
 *   { category, spentPence, limitPence, remainingPence, percentUsed, isOver }
 */
export async function getBudgetProgress(transactions, month) {
  const categories = await listCategories();
  const monthTransactions = transactions.filter((item) => item.date.startsWith(month));
  const spentByCategory = spendingByCategory(monthTransactions, categories);

  return categories.map((category) => {
    const spentPence = spentByCategory.get(category.id) ?? 0;
    const limitPence = Math.round(category.monthly_limit * 100);
    const remainingPence = limitPence - spentPence;

    return {
      category,
      spentPence,
      limitPence,
      remainingPence,
      percentUsed: limitPence > 0 ? Math.min((spentPence / limitPence) * 100, 100) : 0,
      isOver: limitPence > 0 && spentPence > limitPence,
    };
  });
}
