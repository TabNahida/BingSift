# **BingSift — Clean Bing Search Parser**

**BingSift** is a small toolkit for:

* Parsing **Bing search result pages (SERP HTML)** into clean structured data
* Building **filtered Bing search URLs**
* Extracting **original target URLs** from Bing *click redirect* pages
* (Optional) **Fetching** SERP / click pages over the network with headers, retries and delays

All parsing is done offline from HTML files unless you explicitly enable network fetching.

---

## Install

```bash
pip install -e .
```

---

## Features Overview

| Feature | Description |
| --- | --- |
| SERP HTML parsing | Extract: title, url, domain, display_url, snippet, attribution, guessed_time |
| Time guessing | Supports “2 hours ago”, “Oct 20, 2025”, etc. (heuristic) |
| Filtering | include / exclude keywords, allow / deny domains |
| URL builder | Generate Bing search URLs with freshness / site / market filters |
| Click target extractor | Extract original link from Bing click pages |
| Network fetch (optional) | Fetch Bing SERP pages or click pages with retry / timeout / headers |

---

## Command Line Usage

### **Parse a saved SERP HTML file**

```bash
bingsift parse search.html --out results.json
```

### **Parse + filter**

```bash
bingsift parse search.html \
  --include intel xeon \
  --exclude wikipedia \
  --allow-domain intel.com
```

### **Build a Bing URL**

```bash
bingsift url "intel earnings" --when week --country en-GB
```

### **Extract original URL from a saved click page**

```bash
bingsift bingclick click_page.html
```

---

## Network-enabled commands

### **Fetch + Parse SERP (by query)**

```bash
bingsift fetch-parse --query "nvidia blackwell" --when day --out results.json
```

### **Fetch + Parse SERP (by full URL)**

```bash
bingsift fetch-parse --url "https://www.bing.com/search?q=intel"
```

### **Fetch a click page + extract real URL**

```bash
bingsift fetch-click "https://www.bing.com/ck/a?..."
```

Common fetch options:

```
--timeout 12        Request timeout (seconds)
--retries 2         Retry attempts
--delay 1.0         Delay before request (polite)
--ua "..."          Custom User-Agent
--proxy http://...  Proxy server
```

---

## Python Library Usage

### **Parse a saved SERP**

```python
from bingsift import parse_html

html = open("search.html").read()
rows = parse_html(html)
print(rows[0])
```

---

### **Filter results**

```python
from bingsift import filter_results

filtered = filter_results(
    rows,
    include=["cpu", "benchmark"],
    allow_domains=["anandtech.com"]
)
```

---

### **Build a search URL**

```python
from bingsift import build_bing_url

url = build_bing_url("intel meteor lake", when="week", country="en-US")
print(url)
```

---

### **Extract click redirect real URL**

```python
from bingsift import extract_bing_click_target

click_html = open("click.html").read()
real = extract_bing_click_target(click_html)
print(real)
```

---

### **Network fetch + parse**

```python
from bingsift.net import fetch_serp_by_query

rows = fetch_serp_by_query(
    query="amd mi300",
    when="day",
    include=["performance"]
)
```

### **Async Network fetch + parse**

```python
import asyncio
from bingsift.net import fetch_serp_by_query_async

async def main():
    rows = await fetch_serp_by_query_async(
        query="amd mi300",
        when="day",
        include=["performance"]
    )
    # Process results here

# Run the async function
asyncio.run(main())
```

---

### **Network fetch click redirect**

```python
from bingsift.net import fetch_click_and_extract

real = fetch_click_and_extract("https://www.bing.com/ck/a?...")
print(real)
```

### **Async Network fetch click redirect**

```python
import asyncio
from bingsift.net import fetch_click_and_extract_async

async def main():
    real = await fetch_click_and_extract_async("https://www.bing.com/ck/a?...")
    print(real)

# Run the async function
asyncio.run(main())
```

---

## Notes

* You are responsible for complying with Bing Terms and robots.txt
* This library does **not** scrape JS-rendered results
* Click extraction uses **no regex**, only deterministic JS scanning
* Works best with real HTML from browsers or Bing "click" redirect pages

---

## License

MIT