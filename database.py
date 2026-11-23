"""
database.py - SQLite database management for RaceGuard.
Uses standard library sqlite3 with parameterized queries and row_factory = sqlite3.Row.
Connections are strictly scoped and closed via contextmanager to avoid Windows file locks.
"""

from contextlib import contextmanager
from pathlib import Path
import sqlite3
from typing import Any, Dict, Generator, List, Optional

DB_FILE = Path(__file__).resolve().parent / "raceguard.db"


@contextmanager
def get_db(db_path: Optional[Path] = None) -> Generator[sqlite3.Connection, None, None]:
    """Provide a scoped SQLite connection with sqlite3.Row factory, auto-closing on exit."""
    conn = sqlite3.connect(db_path or DB_FILE)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_db(db_path: Optional[Path] = None) -> None:
    """Initialize the SQLite database schema and indices."""
    schema = """
    CREATE TABLE IF NOT EXISTS runs (
      id            INTEGER PRIMARY KEY AUTOINCREMENT,
      timestamp     TEXT    NOT NULL,
      operation     TEXT    NOT NULL CHECK (operation IN ('increment','decrement')),
      mode          TEXT    NOT NULL CHECK (mode IN ('no_mutex','mutex')),
      threads       INTEGER NOT NULL,
      iterations    INTEGER NOT NULL,
      initial_value INTEGER NOT NULL,
      expected      INTEGER NOT NULL,
      actual        INTEGER NOT NULL,
      lost_updates  INTEGER NOT NULL,
      race_detected INTEGER NOT NULL,
      duration_ms   REAL    NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_runs_mode ON runs(mode, id DESC);
    """
    with get_db(db_path) as conn:
        conn.executescript(schema)
        conn.commit()


def _row_to_dict(row: sqlite3.Row) -> Dict[str, Any]:
    """Convert a sqlite3.Row into a standard result dictionary."""
    d = dict(row)
    # Ensure race_detected is boolean in python dictionary
    d["race_detected"] = bool(d["race_detected"])
    return d


def insert_run(result: Dict[str, Any], db_path: Optional[Path] = None) -> int:
    """
    Insert a simulation run into the database.
    Returns the new row ID.
    """
    query = """
    INSERT INTO runs (
      timestamp, operation, mode, threads, iterations,
      initial_value, expected, actual, lost_updates, race_detected, duration_ms
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    params = (
        result["timestamp"],
        result["operation"],
        result["mode"],
        result["threads"],
        result["iterations"],
        result["initial_value"],
        result["expected"],
        result["actual"],
        result["lost_updates"],
        1 if result["race_detected"] else 0,
        float(result["duration_ms"]),
    )
    with get_db(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor.lastrowid


def get_runs(limit: int = 50, db_path: Optional[Path] = None) -> List[Dict[str, Any]]:
    """Retrieve newest simulation runs first up to limit."""
    query = "SELECT * FROM runs ORDER BY id DESC LIMIT ?"
    with get_db(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(query, (limit,))
        rows = cursor.fetchall()
        return [_row_to_dict(row) for row in rows]


def get_latest(
    mode: str,
    operation: Optional[str] = None,
    db_path: Optional[Path] = None,
) -> Optional[Dict[str, Any]]:
    """
    Retrieve the newest simulation run for a given mode (and optional operation).
    Returns None if no matching run exists.
    """
    if operation:
        query = """
        SELECT * FROM runs
        WHERE mode = ? AND operation = ?
        ORDER BY id DESC LIMIT 1
        """
        params = (mode, operation)
    else:
        query = """
        SELECT * FROM runs
        WHERE mode = ?
        ORDER BY id DESC LIMIT 1
        """
        params = (mode,)

    with get_db(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        return _row_to_dict(row) if row else None


def get_stats(db_path: Optional[Path] = None) -> Dict[str, int]:
    """
    Calculate summary stats across all simulation runs:
    total_runs, races_detected, races_prevented.
    """
    query = """
    SELECT
      COUNT(*) AS total_runs,
      COALESCE(SUM(CASE WHEN race_detected = 1 THEN 1 ELSE 0 END), 0) AS races_detected,
      COALESCE(SUM(CASE WHEN mode = 'mutex' AND race_detected = 0 THEN 1 ELSE 0 END), 0) AS races_prevented
    FROM runs
    """
    with get_db(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        row = cursor.fetchone()
        return {
            "total_runs": int(row["total_runs"]),
            "races_detected": int(row["races_detected"]),
            "races_prevented": int(row["races_prevented"]),
        }


def clear_runs(db_path: Optional[Path] = None) -> None:
    """Delete all records from the runs table."""
    with get_db(db_path) as conn:
        conn.execute("DELETE FROM runs")
        conn.commit()
