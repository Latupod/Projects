# Budget Tracking App — Project Structure (Path A)

Offline-first Progressive Web App (PWA) for iPhone, with optional Python tools on your laptop for backup and analysis.

**Primary goal:** Use the app anywhere on your iPhone without network access. All data lives on the phone.

**Secondary goal:** Export data from your phone and import or analyze it on your laptop later using Python.

---

## Architecture Overview

```
┌─────────────────────────────────────┐
│           iPhone (primary)          │
│  PWA — runs fully offline           │
│  IndexedDB / sql.js — local storage │
│  Export → JSON or CSV file          │
└──────────────┬──────────────────────┘
               │  AirDrop / iCloud / email (when you choose)
               ▼
┌─────────────────────────────────────┐
│         Laptop (secondary)          │
│  Python import & analysis scripts   │
│  No server required for daily use   │
└─────────────────────────────────────┘
```

No laptop, no local network, and no internet are required for day-to-day budgeting on your phone.

---

## Directory Structure

```
budget-app/
│
├── mobile/                          # PRIMARY — the app you use on iPhone
│   ├── index.html                   # Entry point; dashboard shell
│   ├── manifest.json                # PWA config (name, icons, theme, standalone mode)
│   ├── sw.js                        # Service worker — caches app for offline use
│   │
│   ├── pages/                       # Separate HTML views (or single-page sections)
│   │   ├── dashboard.html           # Balance, month spend, budget progress
│   │   ├── add-transaction.html     # Quick expense/income entry
│   │   ├── history.html             # Transaction list with filters
│   │   └── budgets.html             # Set and edit category limits
│   │
│   ├── static/
│   │   ├── css/
│   │   │   ├── base.css             # Typography, colours, layout variables
│   │   │   ├── components.css       # Buttons, cards, forms, nav
│   │   │   └── mobile.css           # Thumb-friendly sizing, safe areas for iPhone
│   │   │
│   │   ├── js/
│   │   │   ├── app.js               # App init, routing, navigation
│   │   │   ├── db.js                # IndexedDB or sql.js — open DB, CRUD helpers
│   │   │   ├── models.js            # Transaction, Category, Budget shapes & validation
│   │   │   ├── services/
│   │   │   │   ├── transactions.js  # Add, list, filter, delete transactions
│   │   │   │   ├── budgets.js       # Monthly limits, remaining amounts, alerts
│   │   │   │   └── dashboard.js     # Totals, summaries for home screen
│   │   │   ├── ui/
│   │   │   │   ├── dashboard.js     # Render dashboard widgets
│   │   │   │   ├── transaction-form.js
│   │   │   │   ├── history-list.js
│   │   │   │   └── budget-bars.js   # Visual budget progress bars
│   │   │   └── export.js            # Export/import JSON and CSV on device
│   │   │
│   │   └── icons/
│   │       ├── icon-192.png         # PWA home screen icon
│   │       ├── icon-512.png
│   │       └── apple-touch-icon.png   # iOS Add to Home Screen icon
│   │
│   └── lib/                         # Optional third-party scripts (vendored, offline)
│       └── sql-wasm.js                # Only if using sql.js instead of IndexedDB
│
├── laptop/                          # SECONDARY — run on your PC when syncing/analysing
│   ├── import_data.py               # Load JSON/CSV export from phone into SQLite or pandas
│   ├── export_report.py             # Generate spending summaries or charts
│   ├── merge_backups.py             # Combine multiple phone exports (optional)
│   ├── db/
│   │   └── laptop.sqlite            # Local copy of imported data (gitignored)
│   └── requirements.txt
│
├── shared/
│   └── schema.json                  # Documented export format (categories, transactions, meta)
│
├── tests/
│   ├── mobile/                      # Browser tests or manual test checklist
│   └── laptop/
│       └── test_import_data.py      # Verify import handles sample exports
│
├── samples/
│   └── sample_export.json           # Example export file for testing laptop scripts
│
├── .gitignore
├── README.md                        # How to install on iPhone and run laptop scripts
└── PROJECT_STRUCTURE.md             # This file
```

---

## Folder Responsibilities

### `mobile/` — iPhone app (offline)

Everything the user interacts with on their phone lives here. The app must work after being added to the Home Screen and with no network connection.

| Item | Purpose |
|------|---------|
| `index.html` | Loads CSS/JS, registers the service worker, shows the main UI |
| `manifest.json` | Makes the app installable; sets name, colours, and `display: standalone` |
| `sw.js` | Caches HTML, CSS, JS, and icons so the app loads offline |
| `pages/` | One screen per core task (dashboard, add, history, budgets) |
| `static/js/db.js` | All persistence — create DB, save and read records |
| `static/js/models.js` | Data shapes and validation (amounts, dates, categories) |
| `static/js/services/` | Business logic — totals, budget remaining, month filters |
| `static/js/ui/` | DOM rendering only; calls into `services/` |
| `static/js/export.js` | Build a downloadable JSON/CSV file from local data |

### `laptop/` — Backup and analysis (optional)

Python scripts you run only when you want to pull data off your phone or run richer reports. Not needed for daily use.

| Item | Purpose |
|------|---------|
| `import_data.py` | Read `shared/schema.json` format; load into SQLite or a DataFrame |
| `export_report.py` | Monthly/category breakdowns, charts (pandas + matplotlib) |
| `merge_backups.py` | Deduplicate and merge exports from different dates |
| `requirements.txt` | e.g. `pandas`, `matplotlib` — keep minimal |

### `shared/`

Single source of truth for the **export file format** so mobile `export.js` and laptop `import_data.py` stay compatible.

### `tests/` and `samples/`

Light tests for import logic; a sample export file so you can develop laptop scripts without your phone connected.

---

## Data Model

Stored locally on the phone (IndexedDB object stores or sql.js tables).

### Category

```json
{
  "id": "uuid-or-int",
  "name": "Food",
  "monthly_limit": 200.00,
  "colour": "#4CAF50"
}
```

### Transaction

```json
{
  "id": "uuid-or-int",
  "amount": 12.50,
  "date": "2026-06-17",
  "category_id": "food",
  "note": "Lunch",
  "type": "expense"
}
```

`type` is either `"expense"` or `"income"`.

### Settings (optional, single record)

```json
{
  "currency": "GBP",
  "term_start_month": 9,
  "default_categories_created": true
}
```

### Export bundle (`shared/schema.json` format)

```json
{
  "version": 1,
  "exported_at": "2026-06-17T14:30:00Z",
  "settings": { },
  "categories": [ ],
  "transactions": [ ]
}
```

---

## Core Screens (v1)

1. **Dashboard** — current month spend, income, balance, budget bars per category  
2. **Add transaction** — amount, category, date (default today), note, expense/income toggle  
3. **History** — list with filter by month and category  
4. **Budgets** — set monthly limit per category  
5. **Settings / Export** — export JSON or CSV; optional import from backup file  

---

## Offline Behaviour

1. User opens the app from the Home Screen (installed PWA).  
2. Service worker serves cached `mobile/` assets — no network request.  
3. All reads and writes go to IndexedDB (or sql.js) on the device.  
4. Export creates a file in memory and triggers a download/save via the browser.  
5. Import (optional) reads a file the user selects from Files app — still fully local.  

---

## Sync Workflow (phone → laptop)

1. On iPhone: open **Settings / Export** → download `budget_backup_YYYY-MM-DD.json`.  
2. Transfer file to laptop (AirDrop, iCloud Drive, email, USB).  
3. On laptop: `python laptop/import_data.py path/to/budget_backup.json`  
4. Optionally: `python laptop/export_report.py` for charts or term summaries.  
5. To restore on a new phone: import the same JSON file via the mobile import screen.  

No live sync in v1 — manual export/import is enough for a personal uni budget app.

---

## Tech Choices (Path A)

| Layer | Choice | Why |
|-------|--------|-----|
| Phone UI | HTML, CSS, JavaScript | Runs in Safari; no Mac or Xcode needed |
| Phone storage | IndexedDB (or sql.js) | Built into the browser; persists on device |
| Offline shell | Service worker + `manifest.json` | Installable PWA; works without network |
| Laptop tools | Python 3 + pandas (optional) | Matches your comfort zone for analysis |
| Money handling | Store amounts as integers (pence) or decimal strings in JS | Avoid floating-point rounding bugs |

---

## Suggested Build Order

| Phase | Focus |
|-------|--------|
| 1 | `models.js`, `db.js` — categories and transactions CRUD |
| 2 | Add transaction + history screens |
| 3 | Dashboard and budget remaining logic |
| 4 | `manifest.json`, `sw.js`, icons — install on iPhone |
| 5 | `export.js` + `shared/schema.json` |
| 6 | `laptop/import_data.py` + sample export test |

---

## Getting the App onto Your iPhone (no Mac required)

1. Host `mobile/` on any static host (GitHub Pages, Netlify) **once** to install, **or** serve from a simple local static server during development.  
2. Open the URL in **Safari** on iPhone 15.  
3. Tap **Share → Add to Home Screen**.  
4. After the service worker caches assets, the app works offline — including away from Wi‑Fi.  

For development, you can also use a USB tool or cloud deploy; after caching, daily use does not depend on that host being reachable.

---

## Out of Scope for v1

- Bank API / open banking integration  
- Receipt scanning or OCR  
- Real-time sync between phone and laptop  
- Multi-user or shared household budgets  
- Native App Store distribution  

These can be revisited once the offline core works well for daily uni use.
