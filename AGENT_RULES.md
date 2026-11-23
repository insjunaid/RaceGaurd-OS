# AGENT_RULES.md — Working Rules

## Session start routine
1. Read `README.md`, then `TRACKER.md`.
2. Re-open the doc(s) relevant to the next task before writing code.
3. Work on ONE tracker task at a time, in order.

## While working
- Never invent endpoints, columns or file names. Use `API_SPEC.md`, `DATABASE.md`, `ARCHITECTURE.md`.
- Never change the threading logic without re-reading `THREADING_LOGIC.md`.
- Keep code simple, commented, and PEP8 formatted. No unused dependencies.
- No frontend frameworks. Vanilla JS + Chart.js only.
- All numeric inputs are validated on the server (see `API_SPEC.md`) and on the client.
- Keep the UI exactly in the design system of `UI_UX.md` (ivory, serif headings, double-ruled frames).

## After every task
- Tick the box in `TRACKER.md`, add a one-line note + date in its "Log" section.
- If a decision was made that is not in `DECISIONS.md`, add it there.
- Run the relevant check from `TESTING.md` before ticking.

## Definition of done (whole project)
Every item in `TESTING.md` passes, server starts with `python app.py`, all 6 views render cleanly with no console errors.

## Forbidden
- Using `multiprocessing`, `asyncio`, or fake/random results to simulate a race. Real `threading.Thread` only.
- Making the "with mutex" run wrong, or "without mutex" artificially hard-coded wrong.
- Leaving TODOs or placeholder text in final UI.
