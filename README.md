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

---

## Run the App

From project root:

```bash
streamlit run home.py
```

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

To generate random info, use this : 

```bash
python3 - <<'PY'
import json, random
from datetime import date, timedelta

out_file = "reports.json"
n = 250

incident_types = [
    "Phishing","Malware","Ransomware","DDoS","Brute Force","SQLI","XSS",
    "Unauth Access","Data Breach","Priv Esc","MITM","Zero-Days",
    "Insider Threat","Network Intrusion","Creds Theft","Email Compromise",
    "Supply Chain","Config Error","Sus Login Activity"
]
targets = ["Web","APK","IOS","Network","Web3","API"]
names = ["guest","0Day","Hasan Sheet","Mohammad Shokor","Alice Red","Blue Team"]

def rating_to_severity(r):
    if r < 4: return "Low"
    if r < 7: return "Medium"
    if r < 9: return "High"
    return "Critical"

start = date(2025, 10, 27)
end = date.today()
days = (end - start).days

items = []
for _ in range(n):
    rating = round(random.uniform(0, 10), 1)
    d = start + timedelta(days=random.randint(0, max(days, 0)))
    items.append({
        "name": random.choice(names),
        "title": "",
        "type": random.choice(incident_types),
        "rating": rating,
        "severity": rating_to_severity(rating),
        "description": "",
        "time": d.isoformat(),
        "affectedTargets": random.sample(targets, k=random.randint(1, 3))
    })

with open(out_file, "w", encoding="utf-8") as f:
    json.dump(items, f, ensure_ascii=False, indent=2)

print(f"Generated {out_file} with {n} random reports")
PY
```

and for reporters from this file : 
```bash
python3 - <<'PY'
import json

src = "reports.json"          
dst = "reporters.json"

with open(src, "r", encoding="utf-8") as f:
    reports = json.load(f)

names = sorted({r.get("name", "").strip() for r in reports if r.get("name", "").strip()})
reporters = [{"name": n} for n in names]

with open(dst, "w", encoding="utf-8") as f:
    json.dump(reporters, f, ensure_ascii=False, indent=2)

print(f"Generated {dst} with {len(reporters)} unique reporters")
PY
```
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
- This readme file was generated by ai (cause it is not a main file, just a clarifying file to make reading files easier ) and I (mohammad mahdi) profread it :}
- Where I mentioned that code was generated by ai, it is generated by ai, all other peices of codes are made/modified by me :)
- More than 70% of code was fully controlled by me (the other 30% are just time consuming or extra things)

---

## Future Improvements I might consider doing

- create a login and signup page so it tracks names of reporters
- create a chatbot to ask about information of statiscis of all incidents reported so we improve our system (obv I need to learn how to create a chatbot)
- make some pages limited to admin-only instead of accessible to all users