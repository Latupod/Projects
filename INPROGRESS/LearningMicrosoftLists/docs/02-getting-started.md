# Getting Started with Microsoft Lists

## Step 0: Confirm you have access

1. Sign in at [https://lists.microsoft.com](https://lists.microsoft.com) with your work or school Microsoft account.
2. If you see Lists home with **+ New list**, you're ready.
3. If access is blocked, ask your IT admin — Lists may be disabled or require a specific license.

**Alternative entry:** Open **Microsoft Teams** → **Lists** in the left sidebar (if pinned) or search "Lists" in Apps.

---

## Step 1: Understand the home screen

When you open Lists you typically see:

- **Recent lists** — lists you've opened lately
- **My lists** — lists you created or own
- **Favorites** — lists you starred
- **+ New list** — create blank, from template, from Excel, or from existing list

---

## Step 2: Create your first list (recommended: template)

For learning, start with a **template** — not a blank list. Templates teach good column design.

1. Click **+ New list**
2. Choose **Issue tracker** (or **Asset manager** if you prefer)
3. Name it: `Learning - Issue Tracker`
4. Pick where to save:
   - **My lists** — personal sandbox (good for learning)
   - **Team site** — if you want a specific SharePoint team
5. Click **Create**

You should see a grid with sample rows and columns like Title, Description, Status, Priority, Assigned To, Due Date.

---

## Step 3: Learn the main UI areas

```
┌─────────────────────────────────────────────────────────┐
│  List name          [+ New] [Edit in grid view] [...]   │
├─────────────────────────────────────────────────────────┤
│  View tabs: All Items | By Status | My Items | + New    │
├─────────────────────────────────────────────────────────┤
│  □  Title      Status    Priority   Assigned To  Due    │
│  □  Fix login  Active    High       Jane Doe     Jun 5  │
│  □  Update docs Done     Low        John Smith   Jun 1  │
└─────────────────────────────────────────────────────────┘
```

| Area | What it does |
|------|----------------|
| **+ New** | Opens form to add an item (row) |
| **View tabs** | Switch between saved views (filters/layouts) |
| **Column headers** | Click to sort; column menu for filter/hide |
| **Row click** | Opens item **details pane** (full form + comments) |
| **... (Settings)** | List settings, permissions, rules, automation |

---

## Step 4: Add an item

1. Click **+ New**
2. Fill in **Title** (required on most lists)
3. Set **Status**, **Priority**, **Assigned To**, **Due Date**
4. Click **Save**

The item appears in the grid. Click it again to edit or add **comments** (@mention teammates).

---

## Step 5: Edit columns (list design)

1. Click **Settings** (gear) → **List settings**, *or* click a column header → **Column settings** → **Edit**
2. Try changing a **Choice** column (e.g. add a new Status value like `Blocked`)
3. Add a new column: **+ Add column** → choose type → name it

**Tip:** Design columns before you have hundreds of rows. Changing column types later can be painful.

Common column types to learn first:

- **Choice** — fixed options (Status, Priority, Category)
- **Person** — assigns someone from your org
- **Date** — due dates, start dates
- **Yes/No** — flags

---

## Step 6: Create a view

Views are saved filters + layouts. Example: "My open items"

1. Click **All Items** dropdown → **Create new view**
2. Name: `My Open Items`
3. Filter: **Assigned To** is equal to **Me** AND **Status** is not equal to **Done**
4. Optional: hide columns you don't need
5. Save

Try other view types:

- **Calendar view** — needs a date column
- **Board view** — groups by a Choice column (great for Kanban)

---

## Step 7: Share the list

1. Click **Share** (top right)
2. Add people or groups with **Edit** or **Read** access
3. Or copy link for your organization

Permissions inherit from the SharePoint site where the list lives. "Edit" = can change items and usually list design; "Read" = view only.

---

## Step 8: Add a simple rule

1. **Automate** → **Rules** → **Create a rule**
2. Example: **When a column changes** → Priority is **High** → **Notify someone** → Assigned To
3. Save and test by setting an item to High priority

---

## Keyboard and productivity tips

- **Edit in grid view** — bulk edit like Excel (paste from clipboard supported in many scenarios)
- **Filter** on column header — quick narrowing without saving a view
- **Group by** column — collapsible sections in grid view
- **Export to Excel** — for one-off reports (live sync also possible via "Export" options)

---

## Troubleshooting common beginner issues

| Problem | Likely cause |
|---------|----------------|
| Can't find Lists | App not pinned in Teams; try lists.microsoft.com directly |
| Person column empty | Typing name; use picker to select org user |
| Changes not visible to teammate | They need page refresh; check sharing permissions |
| Can't delete column | Column may be referenced by view, rule, or lookup |
| List feels slow | Very large lists (10k+ items) — use indexed columns and filtered views |

---

## Next step

Continue to [Hands-on Learning Path](03-hands-on-learning-path.md) for structured exercises.
