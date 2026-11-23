# PROJECT_BRIEF.md

## Name
**RaceGuard** — "Detect. Prevent. Understand race conditions."

## Purpose
An educational demo that proves race conditions exist using real Python multithreading and shows
that a Mutex (`threading.Lock`) prevents them, for both increment and decrement operations.

## Core scenario
- Default: **8 threads x 1000 iterations**.
- **Increment**: shared counter starts at 0, expected final = **8000**.
- **Decrement**: shared counter starts at 8000, expected final = **0**.
- **Without mutex**: threads read stale values, writes overwrite each other -> final value wrong -> "Race Condition Detected".
- **With mutex**: only one thread in the critical section at a time -> exact expected value -> "Race Condition Prevented".

## Views (6)
1. **Dashboard** – "Welcome to RaceGuard", quick cards: Thread Simulator, Race Detection, Race Prevention, Result Comparison (+ Overview link).
2. **Thread Simulator** – inputs: Number of Threads (default 8), Operation (Increment + / Decrement -), Iterations per thread (default 1000), Execution Mode (Without Mutex / With Mutex), Run button.
3. **Race Detection** – red card "Race Condition Detected!" with expected vs actual, lost updates (shows latest unsynchronized run).
4. **Race Prevention** – green card "Race Condition Prevented!" explaining the lock gives the exact expected value (shows latest synchronized run).
5. **Result Comparison** – side-by-side table (Without vs With Mutex), Chart.js bar chart, SQLite run-log table.
6. **Overview / Theory** – Race Condition, Critical Section, Increment & Decrement cases, Mutex prevention.

## Non-goals
Auth, user accounts, multiprocessing, deployment, cloud DB.

## Success criteria
See `TESTING.md`.
