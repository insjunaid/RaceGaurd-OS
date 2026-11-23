# RaceGuard — Agent Documentation Index

RaceGuard is a Flask web app that demonstrates **race conditions** with real Python threads,
for both Increment (+) and Decrement (-), with and without a Mutex (`threading.Lock`).

## READ ORDER (mandatory at the start of every session)
1. `AGENT_RULES.md`      – how you must work (read first, always)
2. `TRACKER.md`          – what is done / what is next (update after every task)
3. `PROJECT_BRIEF.md`    – what we are building and why
4. `TECH_STACK.md`       – allowed tools and versions
5. `ARCHITECTURE.md`     – folders, modules, data flow
6. `THREADING_LOGIC.md`  – the core engine (most critical file)
7. `DATABASE.md`         – SQLite schema and queries
8. `API_SPEC.md`         – every endpoint, request and response
9. `UI_UX.md`            – design system and page-by-page layout
10. `CONTENT.md`         – exact copy for the Overview / Theory page
11. `TESTING.md`         – verification checklist and acceptance criteria
12. `DECISIONS.md`       – decisions already made (do not re-litigate)

## Source of truth priority
If files conflict: `THREADING_LOGIC.md` > `API_SPEC.md` > `DATABASE.md` > `ARCHITECTURE.md` > `UI_UX.md` > rest.
