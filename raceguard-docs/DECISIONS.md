# DECISIONS.md — Do not re-litigate

| # | Decision | Reason |
|---|---|---|
| 1 | Multi-page Jinja app, not SPA | Simple, matches 6 named views |
| 2 | `time.sleep(0)` between read and write | Makes race reliably visible under the GIL; identical in both modes for fairness |
| 3 | Decrement starts at `threads*iterations` | Matches spec: 8,000 -> 0 |
| 4 | Raw `sqlite3`, no ORM | Minimal dependencies |
| 5 | Detection/Prevention read latest run from DB | Refresh-safe, no sessions |
| 6 | Chart.js from CDN with optional local fallback | Simple; works offline if vendored |
| 7 | Limits: threads<=64, iterations<=50000, total<=400000 | Keep requests fast |
| 8 | Vanilla JS, custom CSS | Full control of editorial look |

(Add new decisions below with date.)
