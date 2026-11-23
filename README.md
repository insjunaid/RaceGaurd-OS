# RaceGuard

> **"Detect. Prevent. Understand race conditions."**

RaceGuard is an educational Flask web application designed to demonstrate race conditions using real Python multithreading (`threading.Thread` and `threading.Lock`) for both Increment (`+`) and Decrement (`-`) operations, with and without mutual exclusion.

Built with a **classy editorial design** (ivory paper surfaces, double-ruled frames, serif headings, clean sans body, and tabular monospace figures), it provides a complete environment to explore concurrency anomalies and verification.

---

## Concurrency Mechanics

In CPython, the Global Interpreter Lock (GIL) and brief bytecode sequences can cause basic operations like `counter += 1` to appear coincidentally correct. RaceGuard isolates and exposes the classic read-modify-write race condition by splitting the operation into explicit phases:

```python
# Unsynchronized Worker (Window for race)
local = counter.value          # READ (can become stale)
time.sleep(0)                  # YIELD: forces thread context switch
counter.value = local + delta  # WRITE (silently overwrites concurrent updates)

# Synchronized Worker (Protected Critical Section)
with lock:
    local = counter.value
    time.sleep(0)              # Identical yield proves mutex lock prevents races
    counter.value = local + delta
```

### Core Invariants:
- **Default Scenario**: 8 threads &times; 1,000 iterations.
- **Increment (+)**: Counter starts at `0`. Expected final value: `8,000`. Without mutex: final value `< 8,000` (**Race Condition Detected**).
- **Decrement (-)**: Counter starts at `8,000`. Expected final value: `0`. Without mutex: final value `> 0` (**Race Condition Detected**).
- **With Mutex**: Guaranteed exact expected value for both operations (**Race Condition Prevented**).
- **Single Thread**: Correct final value with informative note ("A race requires at least 2 threads").

---

## 6 Application Views

1. **Dashboard (`/`)**: High-level overview featuring four framed entry cards (Modules I–IV) and a live SQLite statistics strip (*Total runs*, *Races detected*, *Races prevented*).
2. **Thread Simulator (`/simulator`)**: Interactive control panel to configure thread count (1–64), operation (`+` / `−`), iterations per thread (1–50,000), and execution mode. Includes dynamic formula preview, validation bounds, and diagnostic status cards.
3. **Race Detection (`/detection`)**: Diagnostic inspection view that loads the most recent unsynchronized (`no_mutex`) run, highlighting the discrepancy between expected and actual values alongside lost update counts, with a "Run again" action.
4. **Race Prevention (`/prevention`)**: Educational verification view that inspects the most recent synchronized (`mutex`) run, illustrating the three-stage mutex lifecycle (*Acquire &rarr; Critical Section &rarr; Release*).
5. **Result Comparison (`/comparison`)**: Benchmark runner executing both modes sequentially under identical parameters, featuring side-by-side metric tables, a grouped bar chart powered by Chart.js, and an SQLite historical run log with a "Clear logs" option.
6. **Overview / Theory (`/overview`)**: Editorial two-column essay detailing concurrency principles, the critical section, increment/decrement cases, and the invariant formula.

---

## Quickstart & Setup

### Prerequisites
- Python 3.10+ (tested on Python 3.12)

### 1. Create and Activate Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Application
```bash
python app.py
```
Open **[http://127.0.0.1:5000](http://127.0.0.1:5000)** in your web browser.

---

## API Reference

| Method | Endpoint | Description | Payload / Response |
|---|---|---|---|
| `POST` | `/api/simulate` | Run simulation and persist to SQLite | `{"threads":8, "operation":"increment", "iterations":1000, "mode":"no_mutex"}` &rarr; `200 Result` |
| `POST` | `/api/compare` | Run both modes sequentially | `{"threads":8, "operation":"increment", "iterations":1000}` &rarr; `200 {"no_mutex": Result, "mutex": Result}` |
| `GET` | `/api/runs?limit=50` | Retrieve recent simulation runs | `200 {"runs": [Result, ...]}` |
| `GET` | `/api/runs/latest?mode=...` | Retrieve latest run for mode | `200 Result` or `200 {"run": null}` |
| `GET` | `/api/stats` | Retrieve aggregate counts | `200 {"total_runs": N, "races_detected": N, "races_prevented": N}` |
| `DELETE` | `/api/runs` | Clear all historical logs | `200 {"deleted": true}` |

---

## Automated Verification

RaceGuard includes dedicated test suites adhering to `TESTING.md`:

```bash
# Verify SQLite helpers and core multithreading engine guarantees
python test_engine.py

# Verify API endpoints, input validation, and HTTP responses
python test_api.py
```
