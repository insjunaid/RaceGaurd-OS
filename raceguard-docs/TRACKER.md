# TRACKER.md — Live Progress (UPDATE AFTER EVERY TASK)

**Current phase:** Phase 0
**Last updated:** —
**Overall:** 0 / 38 tasks

## Phase 0 — Setup
- [ ] 0.1 Create folder structure per ARCHITECTURE.md
- [ ] 0.2 requirements.txt, venv instructions, .gitignore (venv, *.db, __pycache__)
- [ ] 0.3 Minimal app.py runs and serves "hello" on :5000

## Phase 1 — Backend core
- [ ] 1.1 database.py: schema + init_db
- [ ] 1.2 database.py: insert_run, get_runs, get_latest, get_stats, clear_runs
- [ ] 1.3 simulator.py: SharedCounter, worker_unsafe, worker_safe
- [ ] 1.4 simulator.py: run_simulation() returns full result dict
- [ ] 1.5 Engine verification (TESTING.md "Engine")

## Phase 2 — API
- [ ] 2.1 Input validation helper
- [ ] 2.2 POST /api/simulate
- [ ] 2.3 POST /api/compare
- [ ] 2.4 GET /api/runs, /api/runs/latest, /api/stats
- [ ] 2.5 DELETE /api/runs
- [ ] 2.6 API verification (TESTING.md "API")

## Phase 3 — Design system
- [ ] 3.1 style.css tokens, typography, base layout
- [ ] 3.2 .frame double-rule component, buttons, inputs, toggles
- [ ] 3.3 Status cards, stat figures, tables, empty states, toast
- [ ] 3.4 base.html (nav, footer, fonts) + common.js

## Phase 4 — Views
- [ ] 4.1 Dashboard (cards + stats strip)
- [ ] 4.2 Thread Simulator (form, preview line, result)
- [ ] 4.3 Race Detection
- [ ] 4.4 Race Prevention
- [ ] 4.5 Result Comparison: form + side-by-side table
- [ ] 4.6 Result Comparison: Chart.js bar chart
- [ ] 4.7 Result Comparison: SQLite run-log table + clear
- [ ] 4.8 Overview / Theory (CONTENT.md)

## Phase 5 — Polish & verify
- [ ] 5.1 Responsive pass (390px, 768px, 1280px)
- [ ] 5.2 Accessibility pass (focus, aria, contrast)
- [ ] 5.3 Error/empty/loading states everywhere
- [ ] 5.4 Full TESTING.md UI checklist
- [ ] 5.5 Start server, visit all 6 views, fix issues
- [ ] 5.6 README.md for the project root (setup + run + screenshots list)

## Phase 6 — Final
- [ ] 6.1 Final acceptance run from clean environment
- [ ] 6.2 Update this tracker to 100%

## Log
| Date | Task | Note |
|---|---|---|
