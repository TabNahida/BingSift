\
from __future__ import annotations
import re
from datetime import datetime, timedelta
from urllib.parse import urlparse, quote_plus
from bs4 import BeautifulSoup

def _extract_domain(url: str) -> str:
    try:
        return urlparse(url).netloc
    except Exception:
        return ""

def _parse_relative_time(text: str, now_dt: datetime) -> datetime | None:
    text_l = text.strip().lower()
    text_l = text_l.replace("mins", "minutes").replace("min", "minute")
    text_l = text_l.replace("hrs", "hours").replace("hr", "hour")
    text_l = text_l.replace("sec", "second").replace("secs", "seconds")
    m = re.search(r"(\\d+)\\s+(second|seconds|minute|minutes|hour|hours|day|days|week|weeks|month|months|year|years)\\s+ago", text_l)
    if not m:
        return None
    n = int(m.group(1))
    unit = m.group(2)
    if "second" in unit:
        delta = timedelta(seconds=n)
    elif "minute" in unit:
        delta = timedelta(minutes=n)
    elif "hour" in unit:
        delta = timedelta(hours=n)
    elif "day" in unit:
        delta = timedelta(days=n)
    elif "week" in unit:
        delta = timedelta(weeks=n)
    elif "month" in unit:
        delta = timedelta(days=30*n)
    elif "year" in unit:
        delta = timedelta(days=365*n)
    else:
        return None
    return now_dt - delta

def _parse_absolute_date(text: str) -> datetime | None:
    text_c = text.strip()
    text_c = re.sub(r"[•·|—-]\\s*", " ", text_c)
    fmts = [
        "%b %d, %Y", "%d %b %Y", "%Y-%m-%d", "%B %d, %Y", "%d %B %Y",
        "%b %d %Y", "%d/%m/%Y", "%m/%d/%Y", "%Y/%m/%d", "%Y.%m.%d", "%d.%m.%Y"
    ]
    for fmt in fmts:
        try:
            return datetime.strptime(text_c, fmt)
        except Exception:
            pass
    m = re.search(r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\\s+\\d{1,2},\\s+\\d{4}", text_c, flags=re.I)
    if m:
        for fmt in ("%b %d, %Y", "%B %d, %Y"):
            try:
                return datetime.strptime(m.group(0), fmt)
            except Exception:
                pass
    m2 = re.search(r"\\b\\d{1,2}\\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\\s+\\d{4}\\b", text_c, flags=re.I)
    if m2:
        for fmt in ("%d %b %Y", "%d %B %Y"):
            try:
                return datetime.strptime(m2.group(0), fmt)
            except Exception:
                pass
    return None

def _guess_time(block_text: str, now_dt: datetime) -> datetime | None:
    dt = _parse_relative_time(block_text, now_dt)
    if dt:
        return dt
    return _parse_absolute_date(block_text)

def build_bing_url(query: str, *, when: str | None = None, site: str | None = None,
                   lang: str | None = None, country: str | None = None, safe: bool | None = None) -> str:
    q = query
    if site:
        q = f"site:{site} {q}"
    params = [("q", q)]
    when_map = {"day": 1440, "week": 10080, "month": 43200, "year": 525600}
    if when in when_map:
        params.append(("qft", f"+filterui:age-lt{when_map[when]}"))
    if lang:
        params.append(("setlang", lang))
    if country:
        params.append(("cc", country.split("-")[-1].lower()))
        params.append(("mkt", country))
    if safe is not None:
        params.append(("adlt", "off" if safe else "strict"))
    param_str = "&".join([f"{k}={quote_plus(v)}" for k,v in params])
    return f"https://www.bing.com/search?{param_str}"

def parse_html(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    now = datetime.now()
    out = []
    for li in soup.select("#b_results li.b_algo"):
        a = li.select_one("h2 a")
        if not a: 
            continue
        href = a.get("href","").strip()
        title = a.get_text(" ", strip=True)
        snippet = ""
        p = li.select_one(".b_caption p") or li.find("p")
        if p:
            snippet = p.get_text(" ", strip=True)
        display_url = ""
        cite = li.select_one("cite")
        if cite:
            display_url = cite.get_text(" ", strip=True)
        attrib_text = ""
        attrib = li.select_one(".b_attribution") or li.select_one(".b_tpcn")
        if attrib:
            attrib_text = attrib.get_text(" ", strip=True)
        block_text = " ".join([attrib_text, snippet])
        dt = _guess_time(block_text, now)
        out.append({
            "title": title,
            "url": href,
            "domain": _extract_domain(href),
            "display_url": display_url,
            "snippet": snippet,
            "attribution": attrib_text,
            "guessed_time_iso": dt.isoformat() if dt else None,
        })
    # optional: news-like cards
    for card in soup.select(".news-card, .news-card__item, .b_pressItem"):
        a = card.select_one("a")
        if not a:
            continue
        href = a.get("href","").strip()
        title = a.get_text(" ", strip=True)
        t_candidate = card.get_text(" ", strip=True)
        dt = _guess_time(t_candidate, now)
        out.append({
            "title": title,
            "url": href,
            "domain": _extract_domain(href),
            "display_url": "",
            "snippet": "",
            "attribution": "",
            "guessed_time_iso": dt.isoformat() if dt else None,
        })
    return out
