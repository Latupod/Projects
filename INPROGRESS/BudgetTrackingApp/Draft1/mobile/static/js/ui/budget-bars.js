/**
 * ui/budget-bars.js — Budget progress bar rendering
 *
 * Layer: UI
 * Role: Draws per-category progress bars on the Dashboard.
 *
 * Flow: app.js → getDashboardSummary().budgets → renderBudgetBars
 */

import { formatMoney } from "../models.js";

/**
 * Renders horizontal budget bars for each category.
 *
 * @param {HTMLElement} container - #budget-bars from pages/dashboard.html
 * @param {Array<Object>} budgets - From getBudgetProgress(); each item has
 *   category, spentPence, limitPence, percentUsed, isOver, remainingPence
 * @param {string} [currency="GBP"]
 * @returns {void}
 */
export function renderBudgetBars(container, budgets, currency = "GBP") {
  if (!budgets.length) {
    container.innerHTML = `<p class="empty-state">Add categories to track budgets.</p>`;
    return;
  }

  container.innerHTML = budgets
    .map(({ category, spentPence, limitPence, percentUsed, isOver, remainingPence }) => {
      const limitLabel =
        limitPence > 0
          ? `${formatMoney(spentPence, currency)} / ${formatMoney(limitPence, currency)}`
          : `${formatMoney(spentPence, currency)} spent`;

      const remainingLabel =
        limitPence > 0
          ? isOver
            ? `Over by ${formatMoney(Math.abs(remainingPence), currency)}`
            : `${formatMoney(remainingPence, currency)} left`
          : "No limit set";

      return `
        <div class="budget-bar">
          <div class="budget-bar__header">
            <span>${category.name}</span>
            <span>${remainingLabel}</span>
          </div>
          <div class="budget-bar__track">
            <div
              class="budget-bar__fill ${isOver ? "budget-bar__fill--over" : ""}"
              style="width: ${percentUsed}%"
            ></div>
          </div>
          <div class="list__secondary">${limitLabel}</div>
        </div>
      `;
    })
    .join("");
}
