# ARCHITECTURE.md

## Folder structure
```
raceguard/
├── app.py                  # Flask app factory, routes (pages + API)
├── simulator.py            # Thread engine (see THREADING_LOGIC.md)
├── database.py             # SQLite helpers (see DATABASE.md)
├── requirements.txt
├── raceguard.db            # auto-created on first run (gitignored)
├── templates/
│   ├── base.html           # nav, footer, fonts, block content
│   ├── dashboard.html
│   ├── simulator.html
│   ├── detection.html
│   ├── prevention.html
│   ├── comparison.html
│   └── overview.html
└── static/
    ├── css/style.css       # full design system (tokens first)
    ├── js/
    │   ├── common.js       # fetch helpers, formatting, toast, nav highlight
    │   ├── simulator.js
    │   ├── detection.js
    │   ├── prevention.js
    │   └── comparison.js   # Chart.js + table + logs
    └── vendor/             # optional local chart.js
```

## Routes (pages)
| URL | Template |
|---|---|
| `/` | dashboard.html |
| `/simulator` | simulator.html |
| `/detection` | detection.html |
| `/prevention` | prevention.html |
| `/comparison` | comparison.html |
| `/overview` | overview.html |

API routes: see `API_SPEC.md`.

## Data flow
```
Simulator form --POST /api/simulate--> simulator.run_simulation()
      spawns N threads (lock or no lock) -> final value
      -> database.insert_run() -> JSON result -> UI result card
Detection / Prevention pages --GET /api/runs/latest?mode=...--> latest run card
Comparison page --POST /api/compare (runs both)--> table + chart
               --GET /api/runs--> log table
```

## Module responsibilities
- `simulator.py`: pure logic, no Flask imports. Returns a dict (see API_SPEC result object).
- `database.py`: `init_db()`, `insert_run()`, `get_runs(limit)`, `get_latest(mode, operation=None)`, `clear_runs()`, `get_stats()`.
- `app.py`: validation, routing, JSON errors. No business logic.
- JS files: one per page, use `common.js` helpers. No inline scripts except tiny config.

## Shared UI state
No server sessions. Detection/Prevention pages read the latest run from SQLite, so refresh-safe.
If no run exists, show a friendly empty state with a button linking to `/simulator`.
