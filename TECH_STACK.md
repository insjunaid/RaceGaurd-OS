# TECH_STACK.md

| Layer | Choice | Notes |
|---|---|---|
| Language | Python 3.10+ | |
| Web framework | Flask 3.x | Jinja2 templates, JSON API |
| Concurrency | `threading.Thread`, `threading.Lock` | Standard library only |
| Database | SQLite via stdlib `sqlite3` | No ORM |
| Frontend | HTML5, CSS3 (custom, no framework), vanilla JS (ES6 fetch) | |
| Charts | Chart.js 4.x | CDN `https://cdn.jsdelivr.net/npm/chart.js@4.4.1` ; fallback: vendor into `static/vendor/chart.umd.min.js` |
| Fonts | Google Fonts: Playfair Display (headings), Inter (body), JetBrains Mono (numbers) | Provide system serif/sans/mono fallbacks |

## requirements.txt
```
Flask>=3.0
```

## Run
```
python -m venv venv
venv\Scripts\activate        # Windows   (source venv/bin/activate on Mac/Linux)
pip install -r requirements.txt
python app.py                # http://127.0.0.1:5000
```

## Rules
- No other pip packages unless recorded in `DECISIONS.md`.
- Flask `threaded=True` is fine; the simulator spawns its own worker threads per request.
