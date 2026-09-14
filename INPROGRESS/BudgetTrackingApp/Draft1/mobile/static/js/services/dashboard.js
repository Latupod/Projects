/**
 * services/dashboard.js — Dashboard summary aggregator
 *
 * Layer: Services
 * Role: Combines transaction totals, recent items, and budget progress
 *       into one object for the home screen.
 *
 * Flow: app.js initDashboardPage → getDashboardSummary → ui/dashboard.js
 */

import { currentYearMonth } from "../models.js";
import { listTransactions, sumByType } from "./transactions.js";
import { getBudgetProgress } from "./budgets.js";

/**
 * Builds all data needed to render the Dashboard page.
 *
 * @param {string} [month=currentYearMonth()] - YYYY-MM to summarise
 * @returns {Promise<Object>} {
 *   month, expenses (pence), income (pence), balance (pence),
 *   recent (last 5 transactions), budgets (from getBudgetProgress)
 * }
 */
export async function getDashboardSummary(month = currentYearMonth()) {
  const transactions = await listTransactions({ month });
  const expenses = sumByType(transactions, "expense");
  const income = sumByType(transactions, "income");
  const recent = transactions.slice(0, 5);
  const budgets = await getBudgetProgress(transactions, month);

  return {
    month,
    expenses,
    income,
    balance: income - expenses,
    recent,
    budgets,
  };
}
