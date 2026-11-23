"""
simulator.py - Real multithreading simulation engine for RaceGuard.
Follows THREADING_LOGIC.md strictly:
- Pure logic, no Flask imports.
- Uses threading.Thread and threading.Lock from Python standard library.
- time.sleep(0) yields the GIL between read and write in both safe and unsafe workers.
"""

from datetime import datetime
import threading
import time
from typing import Any, Dict


class SharedCounter:
    """Shared state container for counter."""

    def __init__(self, value: int):
        self.value = value


def worker_unsafe(counter: SharedCounter, iterations: int, delta: int) -> None:
    """
    Unsynchronized worker.
    Splits read-modify-write into explicit steps and yields GIL with time.sleep(0),
    creating a window where another thread can interleave and cause lost updates.
    """
    for _ in range(iterations):
        local = counter.value          # READ  (may become stale)
        time.sleep(0)                  # YIELD: forces thread switch -> window for race
        counter.value = local + delta  # WRITE (overwrites others' updates)


def worker_safe(
    counter: SharedCounter,
    iterations: int,
    delta: int,
    lock: threading.Lock,
) -> None:
    """
    Synchronized worker.
    Uses threading.Lock as a mutex to protect the critical section.
    Contains the exact same time.sleep(0) yield to prove that the mutex,
    not thread scheduling or luck, preserves correctness.
    """
    for _ in range(iterations):
        with lock:                     # CRITICAL SECTION: one thread at a time
            local = counter.value
            time.sleep(0)              # same yield -> proves the lock saves us
            counter.value = local + delta


def run_simulation(
    threads: int,
    operation: str,
    iterations: int,
    mode: str,
) -> Dict[str, Any]:
    """
    Execute a real multithreaded simulation.

    Parameters:
    - threads: number of threads to spawn (1 to 64)
    - operation: 'increment' or 'decrement'
    - iterations: iterations per thread (1 to 50000)
    - mode: 'no_mutex' or 'mutex'

    Returns a result dictionary formatted per API_SPEC.md.
    """
    delta = 1 if operation == "increment" else -1
    initial_value = 0 if operation == "increment" else threads * iterations
    expected = initial_value + delta * threads * iterations

    counter = SharedCounter(initial_value)
    lock = threading.Lock() if mode == "mutex" else None

    threads_list = []
    for _ in range(threads):
        if mode == "mutex":
            t = threading.Thread(
                target=worker_safe,
                args=(counter, iterations, delta, lock),
            )
        else:
            t = threading.Thread(
                target=worker_unsafe,
                args=(counter, iterations, delta),
            )
        threads_list.append(t)

    # Measure real execution duration with high resolution
    start_time = time.perf_counter()
    for t in threads_list:
        t.start()
    for t in threads_list:
        t.join()
    duration_ms = round((time.perf_counter() - start_time) * 1000, 2)

    actual = counter.value
    lost_updates = abs(expected - actual)
    race_detected = (actual != expected)
    timestamp = datetime.now().isoformat(timespec="seconds")

    return {
        "threads": threads,
        "operation": operation,
        "iterations": iterations,
        "mode": mode,
        "initial_value": initial_value,
        "expected": expected,
        "actual": actual,
        "lost_updates": lost_updates,
        "race_detected": race_detected,
        "duration_ms": duration_ms,
        "timestamp": timestamp,
    }
