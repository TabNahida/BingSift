# bingsift 0.2.0

> Sift Bing search result pages into clean JSON/CSV, build time/site-filtered URLs, **and** extract the original target URL from Bing click/redirect HTML — all with a tiny, dependency-light toolkit.

## Features
- **Parse SERP HTML** (`bing.com/search?q=` pages) into structured rows:
  - `title`, `url`, `domain`, `display_url`, `snippet`, `attribution`, `guessed_time_iso`
- **Guess timestamps** from lines like “2 hours ago” or “Oct 20, 2025” (heuristics).
- **Filter results**: include/exclude keywords, allow/deny domains.
- **Build Bing URLs** with freshness filters (`day/week/month/year`), `site:` restriction, language/market parameters.
- **Extract original click target** from Bing click/redirect HTML (script setting `var u = "..."`) — **no regex**.

> ⚠️ Respect Bing/Microsoft Terms and robots.txt. This package does **not** fetch pages. It parses **saved HTML** and **builds URLs** for you to open in a browser.

## Install (editable)
```bash
pip install -e .
```

## CLI
```bash
# Parse a saved SERP HTML
bingsift parse search.html --out results.json

# Parse + filter inline
bingsift parse search.html --include xeon --exclude wikipedia --allow-domain intel.com

# Build a filtered Bing URL (open it in your browser)
bingsift url "intel xeon roadmap" --when month --site anandtech.com --country en-GB

# Extract a click target from a Bing click HTML (prints the URL only)
bingsift bingclick article1.html
```

## Library
```python
from bingsift import parse_html, filter_results, build_bing_url, extract_bing_click_target

html = open("search.html", "r", encoding="utf-8", errors="ignore").read()
rows = parse_html(html)

rows = filter_results(
    rows,
    include=["xeon"],
    exclude=["wikipedia"],
    allow_domains=["intel.com"],
    deny_domains=None,
)

url = build_bing_url("intel xeon roadmap", when="week", site="anandtech.com", country="en-GB")

click_html = open("article1.html", "r", encoding="utf-8", errors="ignore").read()
original = extract_bing_click_target(click_html)  # -> string or None
```

## Notes on Time Guessing
We infer `guessed_time_iso` from “relative” strings (`X minutes/hours/days/weeks/months/years ago`) or a handful of common “absolute date” formats (e.g., `Oct 20, 2025`, `20 Oct 2025`, `2025-10-20`). The goal is robustness without extra heavy deps. If you need richer parsing, consider plugging in `dateparser` yourself.

## License
MIT
