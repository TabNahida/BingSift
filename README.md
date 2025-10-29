# bingsift

A tiny toolkit to **parse and filter Bing SERP HTML** (from `bing.com/search?q=` pages) into clean JSON/CSV.

> ⚠️ Respect Bing/Microsoft Terms and robots.txt. This package is designed to work with HTML you already have (e.g., saved pages), and to **build URLs** with filters so you can open them in a browser. It **does not** fetch pages itself.

## Features
- Extract `title, url, domain, snippet, attribution, guessed_time`
- Guess result time from lines like “2 hours ago” or “Oct 20, 2025”
- Simple **filters** (domain allow/deny, keyword include/exclude)
- Build Bing URLs with **freshness**: day/week/month/year (via `qft=+filterui:age-lt...`)

## CLI
```bash
# Parse a saved HTML
bingsift parse /path/to/serp.html --out out.json

# Filter inline
bingsift parse search.html --include "Xeon" --exclude "Wikipedia" --allow-domain "intel.com" --when day

# Build a Bing URL with freshness/site filter (just prints the URL)
bingsift url "intel xeon roadmap" --when month --site "anandtech.com" --country "en-GB"
```

## Library
```python
from bingsift import parse_html, filter_results, build_bing_url

with open("search.html","r",encoding="utf-8") as f:
    html = f.read()

rows = parse_html(html)
rows = filter_results(rows, include=["xeon"], exclude=["wikipedia"], allow_domains=["intel.com"])
```

MIT License.
