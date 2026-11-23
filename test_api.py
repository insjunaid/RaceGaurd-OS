"""
test_api.py - Verification script for Phase 2 API endpoints.
Tests all criteria from TESTING.md "API".
"""

from pathlib import Path
import json
import sqlite3

from app import app
import database

def test_api():
    print("--- Running API Verification Tests ---")
    client = app.test_client()

    # 1. Start with clean database
    del_res = client.delete("/api/runs")
    assert del_res.status_code == 200
    assert del_res.get_json() == {"deleted": True}

    # 2. /api/runs/latest empty DB -> {"run": null}
    latest_res = client.get("/api/runs/latest?mode=no_mutex")
    assert latest_res.status_code == 200
    assert latest_res.get_json() == {"run": None}, f"Expected {{'run': None}}, got {latest_res.get_json()}"
    print("  -> GET /api/runs/latest empty DB verified")

    # 3. Invalid inputs test (threads 0, 100, iterations -5, bad mode, etc.) -> 400 with error message
    bad_inputs = [
        ({"threads": 0, "operation": "increment", "iterations": 1000, "mode": "no_mutex"}, "threads 0"),
        ({"threads": 100, "operation": "increment", "iterations": 1000, "mode": "no_mutex"}, "threads 100"),
        ({"threads": 8, "operation": "increment", "iterations": -5, "mode": "no_mutex"}, "iterations -5"),
        ({"threads": 8, "operation": "increment", "iterations": 60000, "mode": "no_mutex"}, "iterations > 50000"),
        ({"threads": 50, "operation": "increment", "iterations": 10000, "mode": "no_mutex"}, "threads * iterations > 400000"),
        ({"threads": 8, "operation": "multiply", "iterations": 1000, "mode": "no_mutex"}, "bad operation"),
        ({"threads": 8, "operation": "increment", "iterations": 1000, "mode": "magic"}, "bad mode"),
        ({}, "empty dict"),
    ]

    for payload, desc in bad_inputs:
        res = client.post("/api/simulate", json=payload)
        assert res.status_code == 400, f"Expected 400 for {desc}, got {res.status_code}"
        data = res.get_json()
        assert "error" in data, f"Expected 'error' in response for {desc}, got {data}"
    print("  -> Invalid inputs test verified (all returned 400 with error message)")

    # 4. POST /api/simulate valid -> 200 and row saved
    valid_payload = {
        "threads": 8,
        "operation": "increment",
        "iterations": 1000,
        "mode": "mutex",
    }
    sim_res = client.post("/api/simulate", json=valid_payload)
    assert sim_res.status_code == 200, f"Expected 200, got {sim_res.status_code}"
    sim_data = sim_res.get_json()
    assert "id" in sim_data and sim_data["id"] is not None
    assert sim_data["actual"] == 8000
    assert sim_data["race_detected"] is False
    assert sim_data["lost_updates"] == 0

    # Verify row was saved in DB
    runs_res = client.get("/api/runs")
    assert runs_res.status_code == 200
    runs_data = runs_res.get_json()
    assert len(runs_data["runs"]) == 1
    assert runs_data["runs"][0]["id"] == sim_data["id"]
    print("  -> POST /api/simulate valid and row saved verified")

    # 5. /api/runs/latest with data
    latest_res2 = client.get("/api/runs/latest?mode=mutex")
    assert latest_res2.status_code == 200
    latest_data = latest_res2.get_json()
    assert latest_data["id"] == sim_data["id"]
    assert latest_data["mode"] == "mutex"

    # 6. /api/compare saves exactly 2 rows
    runs_before = len(client.get("/api/runs").get_json()["runs"])
    comp_payload = {
        "threads": 8,
        "operation": "decrement",
        "iterations": 1000,
    }
    comp_res = client.post("/api/compare", json=comp_payload)
    assert comp_res.status_code == 200
    comp_data = comp_res.get_json()
    assert "no_mutex" in comp_data and "mutex" in comp_data
    assert comp_data["mutex"]["actual"] == 0
    assert comp_data["mutex"]["race_detected"] is False

    runs_after = len(client.get("/api/runs").get_json()["runs"])
    assert runs_after == runs_before + 2, f"Expected 2 new rows, had {runs_before} now {runs_after}"
    print("  -> POST /api/compare saves exactly 2 rows verified")

    # 7. GET /api/stats
    stats_res = client.get("/api/stats")
    assert stats_res.status_code == 200
    stats_data = stats_res.get_json()
    assert stats_data["total_runs"] == 3
    assert stats_data["races_prevented"] >= 2
    print(f"  -> GET /api/stats verified: {stats_data}")

    # 8. DELETE /api/runs empties table
    del_res = client.delete("/api/runs")
    assert del_res.status_code == 200
    assert del_res.get_json() == {"deleted": True}
    assert len(client.get("/api/runs").get_json()["runs"]) == 0
    print("  -> DELETE /api/runs empties table verified")

    print("\nAll Phase 2 API verification tests passed successfully!")


if __name__ == "__main__":
    test_api()
