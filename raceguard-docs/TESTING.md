# TESTING.md — Verification Checklist

## Engine (run a quick script or pytest-less asserts)
- [ ] increment, 8x1000, mutex -> actual == 8000, race_detected False (repeat 10x, all pass)
- [ ] decrement, 8x1000, mutex -> actual == 0 (repeat 10x)
- [ ] increment, 8x1000, no_mutex -> actual != 8000 in at least 9 of 10 runs
- [ ] decrement, 8x1000, no_mutex -> actual != 0 in at least 9 of 10 runs
- [ ] threads=1 no_mutex -> correct, no race
- [ ] lost_updates == abs(expected - actual)

## API
- [ ] POST /api/simulate valid -> 200 and row saved
- [ ] Invalid inputs (threads 0, 100, iterations -5, bad mode) -> 400 with error message
- [ ] /api/compare saves exactly 2 rows
- [ ] /api/runs/latest empty DB -> `{"run": null}`
- [ ] DELETE /api/runs empties table

## UI (open every view)
- [ ] Dashboard: 4 quick cards link correctly, stats strip loads
- [ ] Simulator: defaults 8 / Increment / 1000 / Without Mutex; preview line correct for both operations
- [ ] Decrement preview shows "8,000 − 8 × 1,000 = 0"
- [ ] Detection: red card after a no_mutex run; empty state when none
- [ ] Prevention: green card after a mutex run
- [ ] Comparison: table, Chart.js chart renders, log table lists runs, Clear logs works
- [ ] Overview: all 6 sections present
- [ ] No console errors, no 404s on static files
- [ ] Layout OK at 1280px and 390px width
- [ ] Design matches UI_UX.md (ivory, serif headings, double-ruled frames, mono figures)

## Final acceptance
Fresh clone -> `pip install -r requirements.txt` -> `python app.py` -> all items above pass.
