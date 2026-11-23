# DATABASE.md — SQLite (`raceguard.db`)

## Table: runs
```sql
CREATE TABLE IF NOT EXISTS runs (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp     TEXT    NOT NULL,           -- ISO 8601
  operation     TEXT    NOT NULL CHECK (operation IN ('increment','decrement')),
  mode          TEXT    NOT NULL CHECK (mode IN ('no_mutex','mutex')),
  threads       INTEGER NOT NULL,
  iterations    INTEGER NOT NULL,
  initial_value INTEGER NOT NULL,
  expected      INTEGER NOT NULL,
  actual        INTEGER NOT NULL,
  lost_updates  INTEGER NOT NULL,
  race_detected INTEGER NOT NULL,           -- 0 / 1
  duration_ms   REAL    NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_runs_mode ON runs(mode, id DESC);
```

## Helper functions (database.py)
- `init_db()` – create table; called at app start.
- `insert_run(result: dict) -> int` – returns new id.
- `get_runs(limit=50)` – newest first, list of dicts.
- `get_latest(mode, operation=None)` – newest run for mode (optional operation) or `None`.
- `get_stats()` – `{total_runs, races_detected, races_prevented}`.
- `clear_runs()` – delete all rows.

## Rules
- Use parameterized queries only. `row_factory = sqlite3.Row`.
- Open a new connection per call (thread-safe with Flask threaded server).
- DB file lives next to `app.py`.
