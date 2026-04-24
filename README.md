# SOC Lite

A lightweight Streamlit app to **report**, **search**, and **analyze** cybersecurity incidents.

## Features

- Submit incident reports with:
  - reporter name (or guest mode)
  - title
  - incident type
  - severity score (0.0 to 10.0)
  - affected targets
  - discovery date
  - description
- Search and filter reports by:
  - reporter name
  - incident type
  - rating range
  - date range
- Visualize incident data in a dashboard:
  - reporters vs severity stacked bar chart
  - severity pie chart
  - incident activity heatmap

---

## Project Structure

- `home.py` — main app entry and top navigation.
- `welcome.py` — intro page with quick workflow.
- `inputFormsPage.py` — incident submission form.
- `search.py` — searchable/paginated report list.
- `dashboard.py` — charts and visual analytics.
- `info.py` — shared constants, data loading/saving, helper functions.
- `reports.json` — incident report storage.
- `reporters.json` — reporters storage.

---

## Requirements

Use Python 3.10+ (recommended).

Install dependencies:

```bash
pip install streamlit pandas numpy altair
```

If you prefer using a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
pip install streamlit pandas numpy altair
```

---

## Run the App

From project root:

```bash
streamlit run home.py
```

You can also run:

```bash
streamlit run welcome.py
```

Since `home.py` defines the app navigation, it is the recommended entry point.

---

## Data Model

Reports are persisted in `reports.json` as objects like:

```json
{
  "name": "guest",
  "title": "Broken auth flow",
  "type": "Unauth Access",
  "rating": 8.2,
  "severity": "High",
  "description": "Detailed explanation...",
  "time": "2026-04-24",
  "affectedTargets": ["Web", "API"]
}
```

Reporters are persisted in `reporters.json` (as list items created from report submissions).

---

## Page-by-Page Notes

### 1) Welcome (`welcome.py`)

- Overview of app purpose.
- Describes the normal workflow:
  1. Report an incident
  2. Search reports
  3. Review dashboard trends

### 2) Report An Incident (`inputFormsPage.py`)

- Guest reporting supported (`isGuest` in session state).
- Validation rules:
  - non-guest name: at least 3 characters
  - title: at least 3 characters
  - description: required
  - at least one affected target required
- On submit:
  - severity derived from rating via `ratingToSeverity`
  - report appended to `reports.json` via `addReport(...)`
  - reporter added to `reporters.json` via `addReporter(...)`

### 3) Search (`search.py`)

- Filters by name, type, rating range, and date range.
- Reads reports with `load_reports()` so newly submitted reports appear after rerun.
- Displays paginated table-like layout with styled severity/rating badges.

### 4) Dashboard (`dashboard.py`)

- Builds visual analytics with Altair:
  - stacked bar: reporter vs severity counts
  - pie chart: severity distribution
  - heatmap: daily incident activity by week/day

---

## Core Utilities (`info.py`)

- `load_reports()` / `save_reports()`
- `load_reporters()` / `save_reporters()`
- `addReport(...)` and `addReporter(...)`
- `ratingToSeverity(rating)`:
  - `< 4` -> Low
  - `< 7` -> Medium
  - `< 9` -> High
  - `>= 9` -> Critical

Also includes shared enums/lists:
- `incidentTypes`
- `affectedTargetsTypes`
- `severityKeys`
- OWASP/CWE top lists (reference data)

---

## Troubleshooting

### Streamlit command not found

Use:

```bash
python -m streamlit run home.py
```

### JSON decode error

A malformed `reports.json` or `reporters.json` will break loading. Validate JSON format and fix trailing commas / missing quotes.

### No new report visible in Search

Search page uses current data from `load_reports()`. If you still don’t see a report, check active filters (name/type/rating/date) and clear them.

---

## Notes

- Uploaded files in `inputFormsPage.py` are currently accepted in UI but not persisted to disk.
- Data storage is file-based JSON (simple and local), not a database.

---

## Future Improvements (Optional)

- Add `requirements.txt`.
- Persist uploaded evidence files and link them to reports.
- Add edit/delete actions for reports.
- Add tests for `info.py` utility functions.
- Add validation and fallback handling for empty/corrupt data files.
