/**
 * ui/transaction-form.js — Add Transaction form wiring
 *
 * Layer: UI
 * Role: Populates the category dropdown and handles form submit on the Add page.
 *
 * Flow: app.js initAddPage → bindTransactionForm → onSubmit → services/transactions.addTransaction
 */

import { todayISO } from "../models.js";

/**
 * Fills a <select> with one <option> per category.
 *
 * @param {HTMLSelectElement} selectElement - #category-select
 * @param {Array<Object>} categories - From listCategories()
 * @returns {void}
 */
export function populateCategorySelect(selectElement, categories) {
  selectElement.innerHTML = categories
    .map((category) => `<option value="${category.id}">${category.name}</option>`)
    .join("");
}

/**
 * Connects the add-transaction form: default date, submit handler, reset after save.
 *
 * @param {HTMLFormElement} formElement - #transaction-form
 * @param {Object} options
 * @param {Array<Object>} options.categories - For the category dropdown
 * @param {function(Object): Promise<void>} options.onSubmit - Called with form payload;
 *   app.js passes a function that saves and navigates to dashboard
 * @returns {void}
 */
export function bindTransactionForm(formElement, { categories, onSubmit }) {
  const dateInput = formElement.querySelector('[name="date"]');
  const categorySelect = formElement.querySelector('[name="category_id"]');

  populateCategorySelect(categorySelect, categories);
  dateInput.value = todayISO();

  formElement.addEventListener("submit", async (event) => {
    event.preventDefault();

    const formData = new FormData(formElement);
    const payload = {
      amount: formData.get("amount"),
      category_id: formData.get("category_id"),
      date: formData.get("date"),
      note: formData.get("note") ?? "",
      type: formData.get("type"),
    };

    await onSubmit(payload);
    formElement.reset();
    dateInput.value = todayISO();
  });
}
