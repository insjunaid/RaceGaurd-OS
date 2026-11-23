"""
app.py - Flask web application for RaceGuard.
Provides JSON API endpoints per API_SPEC.md and HTML page routes per ARCHITECTURE.md.
"""

from typing import Optional
from flask import Flask, jsonify, redirect, render_template, request

import database
import simulator

app = Flask(__name__)

# Initialize SQLite database on startup
database.init_db()


def validate_params(data: dict, require_mode: bool = True) -> Optional[str]:
    """
    Validate simulation parameters according to API_SPEC.md:
    - threads: int 1-64
    - iterations: int 1-50000
    - threads * iterations <= 400000
    - operation: 'increment' | 'decrement'
    - mode: 'no_mutex' | 'mutex' (if require_mode is True)
    """
    if not isinstance(data, dict):
        return "Request body must be a JSON object"

    threads = data.get("threads")
    if (
        threads is None
        or not isinstance(threads, int)
        or isinstance(threads, bool)
        or threads < 1
        or threads > 64
    ):
        return "threads must be an integer between 1 and 64"

    iterations = data.get("iterations")
    if (
        iterations is None
        or not isinstance(iterations, int)
        or isinstance(iterations, bool)
        or iterations < 1
        or iterations > 50000
    ):
        return "iterations must be an integer between 1 and 50000"

    if threads * iterations > 400000:
        return "threads * iterations must be <= 400000"

    operation = data.get("operation")
    if operation not in ("increment", "decrement"):
        return "operation must be 'increment' or 'decrement'"

    if require_mode:
        mode = data.get("mode")
        if mode not in ("no_mutex", "mutex"):
            return "mode must be 'no_mutex' or 'mutex'"

    return None


# ---------------------------------------------------------------------------
# API Routes
# ---------------------------------------------------------------------------


@app.route("/api/simulate", methods=["POST"])
def api_simulate():
    """
    POST /api/simulate
    Body: {"threads":8, "operation":"increment", "iterations":1000, "mode":"no_mutex"}
    -> 200 Result object (saved to DB).
    """
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Invalid or missing JSON payload"}), 400

    error = validate_params(data, require_mode=True)
    if error:
        return jsonify({"error": error}), 400

    result = simulator.run_simulation(
        threads=data["threads"],
        operation=data["operation"],
        iterations=data["iterations"],
        mode=data["mode"],
    )

    row_id = database.insert_run(result)
    result["id"] = row_id
    return jsonify(result), 200


@app.route("/api/compare", methods=["POST"])
def api_compare():
    """
    POST /api/compare
    Body: {"threads":8, "operation":"increment", "iterations":1000}
    Runs BOTH modes (no_mutex then mutex), saves both.
    -> 200 {"no_mutex": Result, "mutex": Result}
    """
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Invalid or missing JSON payload"}), 400

    error = validate_params(data, require_mode=False)
    if error:
        return jsonify({"error": error}), 400

    threads = data["threads"]
    operation = data["operation"]
    iterations = data["iterations"]

    # 1. Run without mutex
    res_no = simulator.run_simulation(
        threads=threads,
        operation=operation,
        iterations=iterations,
        mode="no_mutex",
    )
    res_no["id"] = database.insert_run(res_no)

    # 2. Run with mutex
    res_mu = simulator.run_simulation(
        threads=threads,
        operation=operation,
        iterations=iterations,
        mode="mutex",
    )
    res_mu["id"] = database.insert_run(res_mu)

    return jsonify({"no_mutex": res_no, "mutex": res_mu}), 200


@app.route("/api/runs", methods=["GET"])
def api_get_runs():
    """
    GET /api/runs?limit=50
    -> 200 {"runs": [Result, ...]} newest first.
    """
    limit_param = request.args.get("limit", "50")
    try:
        limit = int(limit_param)
        if limit <= 0:
            limit = 50
    except ValueError:
        limit = 50

    runs = database.get_runs(limit=limit)
    return jsonify({"runs": runs}), 200


@app.route("/api/runs/latest", methods=["GET"])
def api_get_latest_run():
    """
    GET /api/runs/latest?mode=no_mutex|mutex[&operation=increment|decrement]
    -> 200 Result, or 200 {"run": null} if none.
    """
    mode = request.args.get("mode")
    if mode not in ("no_mutex", "mutex"):
        return jsonify({"error": "mode query parameter is required ('no_mutex' or 'mutex')"}), 400

    operation = request.args.get("operation")
    if operation is not None and operation not in ("increment", "decrement"):
        return jsonify({"error": "operation must be 'increment' or 'decrement'"}), 400

    latest = database.get_latest(mode=mode, operation=operation)
    if latest is None:
        return jsonify({"run": None}), 200
    return jsonify(latest), 200


@app.route("/api/stats", methods=["GET"])
def api_get_stats():
    """
    GET /api/stats
    -> 200 {"total_runs": 10, "races_detected": 5, "races_prevented": 5}
    """
    stats = database.get_stats()
    return jsonify(stats), 200


@app.route("/api/runs", methods=["DELETE"])
def api_clear_runs():
    """
    DELETE /api/runs
    -> 200 {"deleted": true}
    """
    database.clear_runs()
    return jsonify({"deleted": True}), 200


# ---------------------------------------------------------------------------
# HTML Page Routes (per ARCHITECTURE.md)
# ---------------------------------------------------------------------------


@app.route("/")
def page_dashboard():
    return render_template("dashboard.html")


@app.route("/simulator")
def page_simulator():
    return render_template("simulator.html")


@app.route("/detection")
def page_detection():
    return render_template("detection.html")


@app.route("/prevention")
def page_prevention():
    return render_template("prevention.html")


@app.route("/comparison")
def page_comparison():
    return render_template("comparison.html")


@app.route("/compare")
def page_compare_alias():
    return redirect("/comparison")


@app.route("/history")
def page_history_alias():
    return redirect("/comparison")


@app.route("/overview")
def page_overview():
    return render_template("overview.html")


if __name__ == "__main__":
    app.run(port=5000, debug=True)
