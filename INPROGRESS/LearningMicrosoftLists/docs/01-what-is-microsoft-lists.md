# What is Microsoft Lists?

## In one sentence

**Microsoft Lists** is a Microsoft 365 app for creating, sharing, and tracking structured information in customizable tables — with views, rules, and team collaboration built in.

## The mental model

Think of a List as a **smart, shared spreadsheet** that lives in the cloud:

- Each **list** is like a table (e.g. "Project Tasks", "Office Inventory")
- Each **row** is an **item** (one task, one asset, one ticket)
- Each **column** is a **field** with a specific type (text, date, choice, person, etc.)

Unlike a plain Excel file on someone's desktop, Lists is:

- **Collaborative** — multiple people edit at the same time
- **Structured** — column types enforce valid data (dates stay dates, people pick from your org)
- **Viewable** — same data as grid, calendar, board, or gallery
- **Automatable** — rules and Power Automate react to changes
- **Integrated** — works inside Teams, SharePoint, and the Power Platform

## What it is *not*

| Tool | Difference |
|------|------------|
| **Excel** | Excel is best for analysis, formulas, and one-off spreadsheets. Lists is best for ongoing team tracking with permissions and workflows. |
| **Microsoft To Do** | To Do is personal task management. Lists is team-level structured data. |
| **Microsoft Planner** | Planner is Kanban-style project tasks. Lists is more flexible — any columns, any process, not just tasks. |
| **A database (SQL)** | Lists is simpler — no queries, no server admin. Good for team-scale tracking, not enterprise data warehousing. |
| **SharePoint (whole site)** | Lists *runs on* SharePoint infrastructure, but the Lists app gives you a focused experience without building a full SharePoint site. |

## Relationship to SharePoint

Microsoft Lists is the **modern, standalone face** of a capability that has existed for years as **SharePoint lists**. Under the hood:

- Every list is stored in a **SharePoint site** (often a hidden "My lists" site)
- You can open the same list in SharePoint for advanced settings
- Permissions follow Microsoft 365 / SharePoint sharing rules

You do **not** need to be a SharePoint admin to use Lists day to day.

## What people use it for

Common scenarios (Microsoft provides templates for many of these):

- **Issue / bug tracking** — status, priority, assignee, due date
- **Asset management** — laptops, keys, equipment, checkout dates
- **Event planning** — sessions, speakers, rooms, catering
- **Onboarding checklists** — new hire tasks across HR and IT
- **Inventory** — stock levels, reorder points, locations
- **CRM-lite** — contacts, leads, follow-up dates (not a full CRM)
- **Approval queues** — requests with status and owner
- **Content calendars** — publish dates, owners, channels
- **Facilities / maintenance** — tickets, locations, resolution

**Rule of thumb:** If your team is sharing an Excel file to track something over time, Lists is often the better choice.

## Key capabilities

### 1. Column types (fields)

Lists supports rich field types, including:

- Single line text, multi-line text
- Choice (dropdown), multi-choice
- Date and time
- Number, currency
- Yes/No
- Person (from your organization)
- Hyperlink, image
- Lookup (link to another list)
- Calculated columns (limited formulas)

### 2. Views

One list, many ways to see the data:

- **Grid** — traditional spreadsheet view
- **Calendar** — items by date field
- **Board** — Kanban by choice column (like Planner)
- **Gallery** — card layout, good for images or rich items

Views can have their own **sort**, **filter**, and **column visibility**.

### 3. Rules (built-in automation)

Simple "when this, then that" without Power Automate:

- e.g. "When Priority is High, send email to assignee"
- e.g. "When Status is Done, notify creator"

### 4. Formatting

**Conditional formatting** highlights rows or columns (e.g. overdue items in red).

**Column / view formatting** (JSON) allows advanced visual customization for power users.

### 5. Integrations

- **Microsoft Teams** — Lists app + pin lists as channel tabs
- **Power Automate** — workflows on create/update/delete
- **Power Apps** — custom forms and mobile apps on list data
- **Microsoft Graph API** — programmatic access for developers
- **Excel** — export/sync for reporting (with limitations)

## Who is it for?

- **Team leads** tracking work across people
- **Operations / admin** managing assets, requests, inventory
- **Project coordinators** who need more structure than Planner
- **Citizen developers** building lightweight apps on list data
- **Anyone** replacing shared spreadsheets with something maintainable

## Licensing and access

Typically included with Microsoft 365 plans that include SharePoint (Business Standard and above, most Enterprise/Education plans). Your org admin can enable or restrict the Lists app in Teams.

Access URLs:

- Web: [https://lists.microsoft.com](https://lists.microsoft.com)
- Teams: **Lists** in the app rail, or **+ Add a tab** → Lists in a channel
- Mobile: via Teams mobile or browser (dedicated Lists mobile apps were retired; use web/Teams)
