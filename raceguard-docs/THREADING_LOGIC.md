# THREADING_LOGIC.md — CORE ENGINE (read before touching simulator.py)

## Problem
In CPython, the GIL and tiny critical sections mean `counter += 1` often looks "correct".
We MUST make the race reliably visible while still using real threads. Solution: split the
read-modify-write into explicit steps and yield the GIL between read and write.

## Shared state
```python
class SharedCounter:
    def __init__(self, value): self.value = value
```

## Worker (unsynchronized)
```python
def worker_unsafe(counter, iterations, delta):
    for _ in range(iterations):
        local = counter.value        # READ  (may become stale)
        time.sleep(0)                # YIELD: forces thread switch -> window for race
        counter.value = local + delta  # WRITE (overwrites others' updates)
```

## Worker (synchronized)
```python
def worker_safe(counter, iterations, delta, lock):
    for _ in range(iterations):
        with lock:                   # CRITICAL SECTION: one thread at a time
            local = counter.value
            time.sleep(0)            # same yield -> proves the lock, not luck, saves us
            counter.value = local + delta
```
The identical yield in both workers is intentional: it makes the comparison fair.

## Parameters
- `delta = +1` for increment, `-1` for decrement.
- `initial = 0` for increment; `initial = threads * iterations` for decrement (8 x 1000 = 8000).
- `expected = initial + delta * threads * iterations`  (increment -> 8000, decrement -> 0).

## run_simulation(threads, operation, iterations, mode) -> dict
Steps:
1. Build counter with `initial`.
2. Create `threads` `threading.Thread` objects with the right worker. Use `threading.Lock()` only if mode == "mutex".
3. Start timer (`time.perf_counter()`), start all threads, join all, stop timer.
4. `actual = counter.value`; `lost_updates = abs(expected - actual)`.
5. `race_detected = (actual != expected)`.
6. Return dict:
```json
{
  "threads": 8, "operation": "increment", "iterations": 1000, "mode": "no_mutex",
  "initial_value": 0, "expected": 8000, "actual": 5321,
  "lost_updates": 2679, "race_detected": true, "duration_ms": 41.7,
  "timestamp": "2026-11-23T10:15:00"
}
```

## Guarantees to verify
- mode `mutex` -> `actual == expected` ALWAYS, `race_detected == false`.
- mode `no_mutex`, threads >= 2 -> `actual != expected` in practice (verify over 10 runs, see TESTING.md).
- threads == 1 with no_mutex -> no race is possible; result is correct. UI must show a note: "A race needs at least 2 threads."
- Never hard-code or fake results.

## Safety limits (enforced in app.py)
threads 1–64, iterations 1–50000, threads*iterations <= 400000 (keeps requests quick).
