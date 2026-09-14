/**
 * ui/history-list.js — History page rendering and filters
 *
 * Layer: UI
 * Role: Month/category filters and full transaction list for the History screen.
 *
 * Flow: app.js initHistoryPage → listTransactions → renderTransactionList
 */

import { formatMoney } from "../models.js";

/**
 * Fills the history category filter dropdown (includes "All categories").
 *
 * @param {HTMLSelectElement} selectElement - #history-category
 * @param {Array<Object>} categories
 * @returns {void}
 */
export function populateHistoryCategoryFilter(selectElement, categories) {
  const options = categories
    .map((category) => `<option value="${category.id}">${category.name}</option>`)
    .join("");

  selectElement.innerHTML = `<option value="">All categories</option>${options}`;
}

/**
 * Renders the filtered transaction list on the History page.
 *
 * @param {HTMLElement} listElement - #transaction-list
 * @param {Array<Object>} transactions - From listTransactions(filters)
 * @param {Array<Object>} categories - For id → name lookup
 * @param {string} [currency="GBP"]
 * @returns {void}
 */
export function renderTransactionList(listElement, transactions, categories, currency = "GBP") {
  if (!transactions.length) {
    listElement.innerHTML = `<li class="empty-state">No transactions match these filters.</li>`;
    return;
  }

  const categoryMap = new Map(categories.map((item) => [item.id, item.name]));

  listElement.innerHTML = transactions
    .map((item) => {
      const categoryName = categoryMap.get(item.category_id) ?? "Unknown";
      const amountClass = item.type === "income" ? "amount--income" : "amount--expense";
      const prefix = item.type === "income" ? "+" : "-";

      return `
        <li class="list__item" data-id="${item.id}">
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

/**
 * Re-runs a callback whenever the user changes month or category filter.
 *
 * @param {HTMLFormElement} formElement - #history-filters
 * @param {function(Object): void} onChange - Receives { month, categoryId };
 *   app.js uses this to reload and re-render the list
 * @returns {void}
 */
export function bindHistoryFilters(formElement, onChange) {
  formElement.addEventListener("change", () => {
    const formData = new FormData(formElement);
    onChange({
      month: formData.get("month") ?? "",
      categoryId: formData.get("category_id") ?? "",
    });
  });
}
