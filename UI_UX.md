# UI_UX.md — "Classy Editorial" Design System

## Mood
A printed-journal / museum-catalogue feel: ivory paper, hairlines, double-ruled frames, generous whitespace.
Calm, precise, uncluttered. No gradients, no neon, no heavy shadows.

## Design tokens (put in `:root` of style.css)
```
--paper:      #FBF9F4;   /* page background (ivory) */
--surface:    #FFFFFF;   /* cards */
--ink:        #1B1B1B;   /* primary text */
--ink-soft:   #5B574F;   /* secondary text */
--rule:       #D9D3C5;   /* hairlines */
--rule-strong:#1B1B1B;   /* frame lines */
--accent:     #1F3A5F;   /* deep navy for links/buttons */
--danger:     #9B2C2C;  --danger-bg:  #FBF1EF;
--success:    #2F6B4F;  --success-bg: #EFF6F1;
--font-serif: 'Playfair Display', Georgia, serif;
--font-sans:  'Inter', system-ui, sans-serif;
--font-mono:  'JetBrains Mono', ui-monospace, monospace;
```
## Typography
- H1: serif 44–52px, tight line-height, small caps eyebrow above (sans, 12px, letter-spacing .18em, uppercase).
- H2/H3: serif. Body: sans 16px/1.65. All numbers/figures: mono, tabular-nums.

## The "framed card" (signature element)
```
.frame { background:var(--surface); border:1px solid var(--rule-strong); padding:28px; position:relative; }
.frame::after { content:""; position:absolute; inset:5px; border:1px solid var(--rule); pointer-events:none; }
```
Double-rule: outer 1px ink line + inner hairline 5px inset. Use for every major card.
Section dividers: `border-top: 3px double var(--rule-strong)` under page headings.

## Layout
- Max width 1120px, centered. 8px spacing grid. Section gap 56px.
- Top nav: wordmark "RaceGuard" (serif, with small italic tagline), links: Dashboard · Simulator · Detection · Prevention · Comparison · Overview. Active link = underline 2px ink. Hairline beneath nav.
- Footer: hairline, small centered text "RaceGuard — a study in concurrency".
- Responsive: grid collapses to 1 column < 760px; nav becomes wrapping row.

## Components
- **Button primary**: ink/navy fill, ivory text, square corners (2px), uppercase small-tracking; hover = invert (white bg, navy border).
- **Inputs**: bottom-border-only or 1px hairline box, mono values, labels in small caps.
- **Segmented toggle** for Operation (+ Increment / − Decrement) and Mode (Without Mutex / With Mutex).
- **Stat figure**: big mono number, small caps label below, hairline divider between stats.
- **Status cards**: `.frame.danger` (red left rule 4px, danger-bg) "Race Condition Detected!"; `.frame.success` (green left rule, success-bg) "Race Condition Prevented!". Include icon glyph (✕ / ✓) as text, not images.
- **Table**: no vertical lines, hairline row rules, serif header caps, mono cells.
- **Loading**: button text "Running threads…" + subtle thin progress line. **Toast** for errors.

## Page layouts
### 1. Dashboard
Hero: eyebrow "Concurrency, demonstrated" / H1 "Welcome to RaceGuard" / lead paragraph (2 lines). Then 4 quick cards in 2x2 grid (framed): **Thread Simulator**, **Race Detection**, **Race Prevention**, **Result Comparison** — each with roman numeral (I–IV), one-line description, "Open →" link. Below: stats strip (Total runs · Races detected · Races prevented) from `/api/stats`. Small link to Overview.

### 2. Thread Simulator
Left (form frame): Number of Threads (default 8), Operation toggle, Iterations per Thread (default 1000), Execution Mode toggle, Run button. A live "Expected result" preview line updates as inputs change (e.g. "Expected: 0 + 8 × 1000 = 8,000").
Right (result frame): after run, shows expected / actual / lost updates / duration and the matching status card (red or green). Empty state before first run.
Note shown if threads = 1.

### 3. Race Detection
Red framed card: "Race Condition Detected!" + explanation sentence + three stats: Expected, Actual, Lost Updates. Shows operation/threads/iterations of the latest `no_mutex` run. Buttons: "Run again" (calls /api/simulate with same params), "Go to Simulator". Empty state if none.

### 4. Race Prevention
Green framed card: "Race Condition Prevented!" + text: "Mutex lock ensures only one thread enters the critical section at a time, giving the exact expected value." Stats: Expected, Actual (equal), Lost Updates 0. Small illustrated sequence (pure CSS/text) of Lock → Critical Section → Unlock.

### 5. Result Comparison
- "Run comparison" form (threads, operation, iterations) -> POST /api/compare.
- Side-by-side table: columns Without Mutex | With Mutex; rows Expected, Actual, Lost Updates, Race Detected?, Duration.
- Chart.js bar chart: grouped bars Expected vs Actual for each mode. Colors: expected = ink-soft, actual(no mutex) = danger, actual(mutex) = success. Serif title, mono ticks, hairline grid.
- Run log table (SQLite): id, time, op, mode, threads×iters, expected, actual, status badge. "Clear logs" button (confirm).

### 6. Overview / Theory
Editorial long-form: two-column on desktop, drop cap first paragraph, numbered sections, pull-quote frame for the key formula. Content from `CONTENT.md`.

## Accessibility
Contrast AA, visible focus rings (2px navy outline), aria-labels on toggles, status conveyed with text + icon not color alone.
