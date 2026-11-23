# API_SPEC.md

All responses JSON. Errors: `{"error": "message"}` with HTTP 400.

## Validation (server-side)
- `threads`: int 1–64
- `iterations`: int 1–50000
- `threads * iterations <= 400000`
- `operation`: `"increment"` | `"decrement"`
- `mode`: `"no_mutex"` | `"mutex"`

## Result object
```json
{"id":12,"timestamp":"...","operation":"increment","mode":"no_mutex","threads":8,"iterations":1000,
 "initial_value":0,"expected":8000,"actual":5321,"lost_updates":2679,"race_detected":true,"duration_ms":41.7}
```

## POST /api/simulate
Body: `{"threads":8,"operation":"increment","iterations":1000,"mode":"no_mutex"}`
-> 200 Result object (saved to DB).

## POST /api/compare
Body: `{"threads":8,"operation":"increment","iterations":1000}`
Runs BOTH modes (no_mutex then mutex), saves both.
-> 200 `{"no_mutex": Result, "mutex": Result}`

## GET /api/runs?limit=50
-> 200 `{"runs":[Result,...]}` newest first.

## GET /api/runs/latest?mode=no_mutex|mutex[&operation=increment|decrement]
-> 200 Result, or 200 `{"run": null}` if none. (Always 200 for the empty state.)

## GET /api/stats
-> 200 `{"total_runs":10,"races_detected":5,"races_prevented":5}`

## DELETE /api/runs
-> 200 `{"deleted": true}`

## Page routes
`/`, `/simulator`, `/detection`, `/prevention`, `/comparison`, `/overview` (GET, HTML).
