# Hands-on Learning Path

Work through these exercises in order. Each builds on the previous one. Keep your practice lists in **My lists** unless you have a real team scenario.

---

## Exercise 1: Issue tracker (your first list)

**Goal:** Create, edit, filter, and share a basic list.

**Time:** ~30 minutes

### Tasks

- [ ] Create list from **Issue tracker** template named `Learning - Issue Tracker`
- [ ] Add 5 real or fictional issues with varied Status and Priority
- [ ] Create view **High Priority Open**: Status ≠ Done AND Priority = High
- [ ] Create **Board** view grouped by Status
- [ ] Share with one colleague (or second account) with Edit access
- [ ] Add a comment on one item and @mention someone

### Success criteria

You can explain: item vs column vs view, and how Board view differs from Grid.

### Reflect (write in `notes/exercise-01.md`)

- What columns would you add for your actual work?
- What would you remove from the template?

---

## Exercise 2: Design your own schema

**Goal:** Build a blank list and design columns intentionally.

**Time:** ~45 minutes

### Scenario

Track **team book recommendations**: title, author, genre, recommended by, date added, read (yes/no), rating (1–5).

### Tasks

- [ ] **+ New list** → **Blank list** → `Learning - Book Recommendations`
- [ ] Add columns with appropriate types (don't use Text for everything)
- [ ] Add 10 items
- [ ] Create **Gallery** view (shows cards — good for visual lists)
- [ ] Create view **Unread**: Read = No
- [ ] Apply conditional formatting: highlight rows where Rating ≥ 4 (if available in your tenant)

### Success criteria

Every column has the correct type; at least two custom views exist.

---

## Exercise 3: Rules and notifications

**Goal:** Automate without Power Automate.

**Time:** ~30 minutes

Use your Issue Tracker list from Exercise 1.

### Tasks

- [ ] Rule: When **Status** changes to **Done**, notify the person in **Assigned To**
- [ ] Rule: When **Due Date** is approaching (if template supports), notify assignee — *or* create a manual rule you can trigger
- [ ] Test each rule with a test item
- [ ] Document which rules worked in `notes/exercise-03.md`

### Success criteria

You receive (or assignee receives) an email or Teams notification from a rule.

---

## Exercise 4: Lists in Microsoft Teams

**Goal:** Embed a list where your team collaborates.

**Time:** ~30 minutes

### Tasks

- [ ] Open a Team channel (or create a test Team)
- [ ] **+ Add a tab** → **Lists** → choose your Issue Tracker or create new in channel
- [ ] Post in channel: link to a specific item (open item → copy link)
- [ ] Have a conversation in channel while editing the list in the tab

### Success criteria

Team members can see and edit the list without leaving Teams.

---

## Exercise 5: Import from Excel

**Goal:** Migrate spreadsheet data into a list.

**Time:** ~45 minutes

### Tasks

- [ ] Create a small Excel table (5–10 rows): columns Title, Category, Quantity, Owner
- [ ] In Lists: **+ New list** → **From Excel** → upload file
- [ ] Verify column types mapped correctly (fix any that imported as Text incorrectly)
- [ ] Add one **Choice** column after import and categorize items

### Success criteria

Excel data lives in Lists with usable column types.

---

## Exercise 6: Introduction to Power Automate

**Goal:** One workflow triggered by list changes.

**Time:** ~1 hour  
**Prerequisite:** Power Automate access (usually included in M365)

### Scenario

When a new item is created in Issue Tracker, post a message to a Teams channel.

### Tasks

- [ ] Open list → **Integrate** → **Power Automate** → **Create a flow**
- [ ] Trigger: **When an item is created**
- [ ] Action: **Post message in a chat or channel** (Teams)
- [ ] Include dynamic fields: Title, Priority, Assigned To
- [ ] Create a test item and confirm message appears

### Success criteria

Flow runs automatically on new items. Check **Flow run history** if it fails.

---

## Exercise 7: Capstone — solve a real problem

**Goal:** Build something you'll actually use for 2+ weeks.

**Time:** 2–3 hours design + ongoing use

### Pick one

1. Personal **job application tracker** (company, role, status, date applied, follow-up)
2. **Home maintenance** log (appliance, last service, next due, vendor)
3. **Side project backlog** (feature, priority, status, estimate)
4. Your own idea — write one paragraph in `notes/capstone-brief.md`

### Requirements

- [ ] At least 8 columns, 3+ column types
- [ ] 3+ views (including one non-grid view)
- [ ] At least 1 rule or Power Automate flow
- [ ] Shared with at least one other person OR used daily yourself
- [ ] Document structure in `notes/capstone-design.md`

---

## Skill checklist (self-assessment)

Rate yourself 1–5 after completing exercises:

| Skill | 1 | 3 | 5 |
|-------|---|---|---|
| Create list from template / blank / Excel | | | |
| Choose correct column types | | | |
| Create and share views | | | |
| Board and Calendar views | | | |
| Sharing and permissions | | | |
| Built-in rules | | | |
| Teams integration | | | |
| Power Automate trigger on list | | | |
| Know when *not* to use Lists | | | |

---

## When you're ready for advanced topics

- **Lookup columns** — relate two lists (e.g. Projects → Tasks)
- **Calculated columns** — simple formulas
- **JSON column/view formatting** — custom visuals
- **Microsoft Graph** — read/write lists from code
- **Power Apps** — custom forms replacing default new/edit experience
- **Content types** — reuse column sets across lists (SharePoint admin territory)

Add notes on these in `notes/advanced/` as you explore.
