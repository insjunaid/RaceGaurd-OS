"""
test_engine.py - Verification script for Phase 1 (database.py and simulator.py).
Tests database helpers and all TESTING.md Engine verification criteria.
"""

from pathlib import Path
import os
import sys

from database import (
    clear_runs,
    get_latest,
    get_runs,
    get_stats,
    init_db,
    insert_run,
)
from simulator import run_simulation


def test_database():
    print("--- Testing database.py ---")
    test_db = Path("test_raceguard.db")
    if test_db.exists():
        test_db.unlink()

    init_db(test_db)

    # Initially empty
    assert get_runs(50, test_db) == [], "Empty DB should return empty list"
    assert get_latest("no_mutex", None, test_db) is None, "Empty DB should return None for latest"
    stats = get_stats(test_db)
    assert stats == {"total_runs": 0, "races_detected": 0, "races_prevented": 0}

    # Insert a no_mutex run with race
    run1 = {
        "timestamp": "2026-11-23T12:00:00",
        "operation": "increment",
        "mode": "no_mutex",
        "threads": 8,
        "iterations": 1000,
        "initial_value": 0,
        "expected": 8000,
        "actual": 5200,
        "lost_updates": 2800,
        "race_detected": True,
        "duration_ms": 45.2,
    }
    id1 = insert_run(run1, test_db)
    assert id1 == 1

    # Insert a mutex run
    run2 = {
        "timestamp": "2026-11-23T12:01:00",
        "operation": "increment",
        "mode": "mutex",
        "threads": 8,
        "iterations": 1000,
        "initial_value": 0,
        "expected": 8000,
        "actual": 8000,
        "lost_updates": 0,
        "race_detected": False,
        "duration_ms": 52.1,
    }
    id2 = insert_run(run2, test_db)
    assert id2 == 2

    # Verify get_runs
    runs = get_runs(10, test_db)
    assert len(runs) == 2
    assert runs[0]["id"] == 2 and runs[0]["mode"] == "mutex"
    assert runs[0]["race_detected"] is False
    assert runs[1]["id"] == 1 and runs[1]["race_detected"] is True

    # Verify get_latest
    latest_mutex = get_latest("mutex", None, test_db)
    assert latest_mutex["id"] == 2
    latest_no_mutex = get_latest("no_mutex", "increment", test_db)
    assert latest_no_mutex["id"] == 1
    assert get_latest("no_mutex", "decrement", test_db) is None

    # Verify get_stats
    stats = get_stats(test_db)
    assert stats["total_runs"] == 2
    assert stats["races_detected"] == 1
    assert stats["races_prevented"] == 1

    # Verify clear_runs
    clear_runs(test_db)
    assert len(get_runs(10, test_db)) == 0
    stats = get_stats(test_db)
    assert stats["total_runs"] == 0

    if test_db.exists():
        test_db.unlink()
    print("Database tests passed successfully!")


def test_engine():
    print("\n--- Testing simulator.py against TESTING.md criteria ---")

    # 1. increment, 8x1000, mutex -> actual == 8000, race_detected False (repeat 10x, all pass)
    print("Testing 10x Increment with Mutex (8x1000)...")
    for i in range(10):
        res = run_simulation(8, "increment", 1000, "mutex")
        assert res["actual"] == 8000, f"Run {i+1}: Expected 8000, got {res['actual']}"
        assert res["race_detected"] is False
        assert res["lost_updates"] == 0
        assert res["lost_updates"] == abs(res["expected"] - res["actual"])
    print("  -> Passed 10/10")

    # 2. decrement, 8x1000, mutex -> actual == 0 (repeat 10x)
    print("Testing 10x Decrement with Mutex (8x1000)...")
    for i in range(10):
        res = run_simulation(8, "decrement", 1000, "mutex")
        assert res["actual"] == 0, f"Run {i+1}: Expected 0, got {res['actual']}"
        assert res["race_detected"] is False
        assert res["lost_updates"] == 0
        assert res["lost_updates"] == abs(res["expected"] - res["actual"])
    print("  -> Passed 10/10")

    # 3. increment, 8x1000, no_mutex -> actual != 8000 in at least 9 of 10 runs
    print("Testing 10x Increment WITHOUT Mutex (8x1000)...")
    races_inc = 0
    for i in range(10):
        res = run_simulation(8, "increment", 1000, "no_mutex")
        assert res["lost_updates"] == abs(res["expected"] - res["actual"])
        if res["actual"] != 8000 and res["race_detected"]:
            races_inc += 1
    print(f"  -> Races detected: {races_inc}/10")
    assert races_inc >= 9, f"Expected at least 9/10 races, got {races_inc}"

    # 4. decrement, 8x1000, no_mutex -> actual != 0 in at least 9 of 10 runs
    print("Testing 10x Decrement WITHOUT Mutex (8x1000)...")
    races_dec = 0
    for i in range(10):
        res = run_simulation(8, "decrement", 1000, "no_mutex")
        assert res["lost_updates"] == abs(res["expected"] - res["actual"])
        if res["actual"] != 0 and res["race_detected"]:
            races_dec += 1
    print(f"  -> Races detected: {races_dec}/10")
    assert races_dec >= 9, f"Expected at least 9/10 races, got {races_dec}"

    # 5. threads=1 no_mutex -> correct, no race
    print("Testing threads=1 without mutex (both increment and decrement)...")
    res_single_inc = run_simulation(1, "increment", 1000, "no_mutex")
    assert res_single_inc["actual"] == 1000
    assert res_single_inc["race_detected"] is False
    assert res_single_inc["lost_updates"] == 0

    res_single_dec = run_simulation(1, "decrement", 1000, "no_mutex")
    assert res_single_dec["actual"] == 0
    assert res_single_dec["race_detected"] is False
    assert res_single_dec["lost_updates"] == 0
    print("  -> Passed single-thread tests")

    print("\nAll engine verification criteria in TESTING.md passed!")


if __name__ == "__main__":
    test_database()
    test_engine()
