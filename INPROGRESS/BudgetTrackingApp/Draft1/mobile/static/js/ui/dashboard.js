/**
 * ui/dashboard.js — Dashboard screen rendering
 *
 * Layer: UI (DOM only — no database, no business rules)
 * Role: Takes summary data from services and writes HTML into the page.
 *
 * Flow: app.js initDashboardPage → services/dashboard.js → these render functions
 */

import { formatMoney } from "../models.js";

/**
 * Renders the three top cards: Spent, Income, Balance.
 *
 * @param {HTMLElement} container - #summary-grid from pages/dashboard.html
 * @param {Object} summary - From getDashboardSummary(); amounts in pence
 * @param {string} [currency="GBP"] - From app settings
 * @returns {void}
 */
export function renderDashboardSummary(container, summary, currency = "GBP") {
  container.innerHTML = `
    <article class="summary-card">
      <span class="summary-card__label">Spent</span>
      <span class="summary-card__value amount--expense">${formatMoney(summary.expenses, currency)}</span>
    </article>
    <article class="summary-card">
      <span class="summary-card__label">Income</span>
      <span class="summary-card__value amount--income">${formatMoney(summary.income, currency)}</span>
    </article>
    <article class="summary-card">
      <span class="summary-card__label">Balance</span>
      <span class="summary-card__value">${formatMoney(summary.balance, currency)}</span>
    </article>
  `;
}

/**
 * Renders the "Recent transactions" list on the dashboard (max 5 items).
 *
 * @param {HTMLElement} listElement - #recent-transactions
 * @param {Array<Object>} transactions - From summary.recent
 * @param {Array<Object>} categories - Used to resolve category_id → name
 * @param {string} [currency="GBP"]
 * @returns {void}
 */
export function renderRecentTransactions(listElement, transactions, categories, currency = "GBP") {
  if (!transactions.length) {
    listElement.innerHTML = `<li class="empty-state">No transactions yet this month.</li>`;
    return;
  }

  const categoryMap = new Map(categories.map((item) => [item.id, item.name]));

  listElement.innerHTML = transactions
    .map((item) => {
      const categoryName = categoryMap.get(item.category_id) ?? "Unknown";
      const amountClass = item.type === "income" ? "amount--income" : "amount--expense";
      const prefix = item.type === "income" ? "+" : "-";

      return `
        <li class="list__item">
          <div>
            <div class="list__primary">${categoryName}</div>
            <div class="list__secondary">${item.date}${item.note ? ` · ${item.note}` : ""}</div>
          </div>
          <div class="${amountClass}">${prefix}${formatMoney(item.amount, currency)}</div>
        </li>
      `;
    })
    .join("");
}
