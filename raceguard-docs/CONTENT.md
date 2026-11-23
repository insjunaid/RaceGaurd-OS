# CONTENT.md — Copy for the Overview / Theory page (use as written)

## 1. What is a Race Condition?
A race condition occurs when two or more threads access shared data at the same time and the final result depends on the unpredictable order in which they run. Because an operation like `counter += 1` is really three steps (read, modify, write), another thread can slip in between those steps.

## 2. The Critical Section
The critical section is the part of code that touches shared data. If more than one thread can be inside it at once, updates can be lost. Reading a value before another thread finishes writing means working with a stale value, and the later write silently overwrites the earlier one.

## 3. The Increment Case
8 threads each increment a shared counter by 1 a total of 1,000 times. Expected result: 8 × 1,000 = **8,000**. Without synchronization, threads read stale values and overwrite each other's updates, so the final value is less than 8,000. RaceGuard flags this as a race condition.

## 4. The Decrement Case
Start the counter at 8,000. 8 threads each subtract 1 a total of 1,000 times. Expected result: 8,000 − 8 × 1,000 = **0**. Unsynchronized execution leaves an incorrect non-zero balance, because lost decrements leave the value higher than it should be.

## 5. Mutex Prevention
A mutex (mutual exclusion lock, `threading.Lock` in Python) lets only one thread execute the critical section at a time. Other threads wait until the lock is released. This guarantees no data corruption and yields the exact expected result for both increment and decrement.

## 6. Key formula (pull-quote)
`expected = initial ± (threads × iterations)`   ·   `lost updates = |expected − actual|`

## 7. Try it
Link: "Open the Thread Simulator →"

## Dashboard copy
- Eyebrow: Concurrency, demonstrated
- H1: Welcome to RaceGuard
- Lead: See real Python threads corrupt shared data, then watch a mutex put things right.
- Cards: Thread Simulator — "Configure threads, operation and iterations, then run." / Race Detection — "See exactly how many updates were lost." / Race Prevention — "Watch the mutex deliver the exact result." / Result Comparison — "Compare both modes side by side with charts and logs."

## Status copy
- Red: **Race Condition Detected!** — "Threads overwrote each other's updates. The final value does not match the expected result."
- Green: **Race Condition Prevented!** — "Mutex lock ensures only one thread enters the critical section at a time, giving the exact expected value."
