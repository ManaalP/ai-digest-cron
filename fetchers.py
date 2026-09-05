"""
fetchers.py - Primary AI news and research fetchers.

Each fetcher returns a list of dicts:
  {
    "source": str,
    "title": str,
    "url": str,
    "published": datetime,
    "raw_text": str,
    "image_url": str | None,
    "community_score": int,
  }

published is timezone-aware UTC. Sources use RSS or public APIs (no login walls).
"""

import re
import feedparser
import calendar
import requests
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 ai-digest/1.2"}
REDDIT_HEADERS = {"User-Agent": "linux:ai-news-digest:v1.2 (by /u/personal_ai_bot)"}


def _safe_parsed_date(entry):
    """Accurately parse entry date into timezone-aware UTC datetime."""
    # 1. feedparser parsed tuple (most reliable)
    for key in ("published_parsed", "updated_parsed"):
        tup = entry.get(key)
        if tup:
            try:
                return datetime.fromtimestamp(calendar.timegm(tup), tz=timezone.utc)
            except Exception:
                pass

    # 2. String parsing (Atom ISO 8601 or RFC 2822)
    for key in ("published", "updated"):
        val = entry.get(key)
        if val:
            val_str = str(val).strip()
            # Try ISO 8601
            try:
                clean_iso = val_str.replace("Z", "+00:00")
                return datetime.fromisoformat(clean_iso).astimezone(timezone.utc)
            except Exception:
                pass
            # Try RFC 2822
            try:
                return parsedate_to_datetime(val_str).astimezone(timezone.utc)
            except Exception:
                pass

    return None


def _extract_image(entry):
    """Attempt to extract an article thumbnail/image from RSS entry."""
    # 1. media_content
    for media in entry.get("media_content", []):
        url = media.get("url")
        if url and not url.endswith(".svg"):
            return url

    # 2. media_thumbnail
    for thumb in entry.get("media_thumbnail", []):
        url = thumb.get("url")
        if url and not url.endswith(".svg"):
            return url

    # 3. enclosures
    for enc in entry.get("enclosures", []):
        url = enc.get("href")
        if url and ("image" in enc.get("type", "") or url.endswith((".jpg", ".png", ".webp", ".jpeg"))):
            return url

    # 4. embedded <img> in summary or content
    for text_candidate in [entry.get("summary"), entry.get("description")] + [c.get("value") for c in entry.get("content", [])]:
        if text_candidate:
            m = re.search(r'<img [^>]*src=["\']([^"\']+\.(?:jpg|jpeg|png|webp|gif)[^"\']*)["\']', text_candidate, re.IGNORECASE)
            if m:
                return m.group(1)
            m2 = re.search(r'<img [^>]*src=["\']([^"\']+)["\']', text_candidate, re.IGNORECASE)
            if m2 and not m2.group(1).endswith((".svg", ".ico", "pixel", "tracking")):
                return m2.group(1)

    return None


def _rss(source_name, feed_url, limit=20):
    items = []
    try:
        feed = feedparser.parse(feed_url, request_headers=HEADERS)
        for entry in feed.entries[:limit]:
            pub_date = _safe_parsed_date(entry)
            if not pub_date:
                continue
            items.append({
                "source": source_name,
                "title": entry.get("title", "").strip(),
                "url": entry.get("link", ""),
                "published": pub_date,
                "raw_text": (entry.get("summary") or entry.get("description") or "")[:3500],
                "image_url": _extract_image(entry),
                "community_score": 0,
            })
    except Exception as e:
        print(f"[fetchers] {source_name} RSS failed: {e}")
    return items


def fetch_simon_willison():
    return _rss("Simon Willison's Weblog", "https://simonwillison.net/atom/everything/", limit=20)


def fetch_interconnects():
    return _rss("Interconnects (Nathan Lambert)", "https://www.interconnects.ai/feed", limit=15)


def fetch_ahead_of_ai():
    return _rss("Ahead of AI (Sebastian Raschka)", "https://magazine.sebastianraschka.com/feed", limit=15)


def fetch_semianalysis():
    return _rss("SemiAnalysis", "https://www.semianalysis.com/feed", limit=15)


def fetch_anthropic_news():
    return _rss("Anthropic News", "https://www.anthropic.com/news/rss.xml", limit=10)


def fetch_openai_news():
    return _rss("OpenAI Blog", "https://openai.com/news/rss.xml", limit=15)


def fetch_googledeepmind_news():
    return _rss("Google DeepMind Blog", "https://deepmind.google/blog/rss.xml", limit=15)


def fetch_techcrunch_ai():
    return _rss("TechCrunch AI", "https://techcrunch.com/category/artificial-intelligence/feed/", limit=20)


def fetch_theverge_ai():
    return _rss("The Verge AI", "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml", limit=15)


def fetch_reddit_localllama(limit=20):
    items = []
    try:
        resp = requests.get(
            "https://www.reddit.com/r/LocalLLaMA/top/.rss?t=day",
            headers=REDDIT_HEADERS, timeout=15,
        )
        if resp.status_code == 429:
            # Fallback to alternative hot feed
            resp = requests.get(
                "https://www.reddit.com/r/LocalLLaMA/hot/.rss",
                headers=REDDIT_HEADERS, timeout=15,
            )
        resp.raise_for_status()
        feed = feedparser.parse(resp.text)
        for entry in feed.entries[:limit]:
            pub_date = _safe_parsed_date(entry)
            if not pub_date:
                continue
            items.append({
                "source": "r/LocalLLaMA (top today)",
                "title": entry.get("title", "").strip(),
                "url": entry.get("link", ""),
                "published": pub_date,
                "raw_text": (entry.get("summary") or "")[:3500],
                "image_url": _extract_image(entry),
                "community_score": 15,
            })
    except Exception as e:
        print(f"[fetchers] r/LocalLLaMA failed: {e}")
    return items


def fetch_hn_ai(limit=25):
    """Hacker News high-signal AI stories via Algolia API."""
    items = []
    queries = ["LLM", "AI", "OpenAI", "Claude", "agentic", "vLLM"]
    seen_ids = set()

    for q in queries:
        try:
            resp = requests.get(
                "https://hn.algolia.com/api/v1/search_by_date",
                params={"tags": "story", "query": q, "numericFilters": "points>15"},
                headers=HEADERS, timeout=10,
            )
            resp.raise_for_status()
            data = resp.json()
            for hit in data.get("hits", []):
                object_id = hit.get("objectID")
                if object_id in seen_ids:
                    continue
                seen_ids.add(object_id)

                url = hit.get("url") or f"https://news.ycombinator.com/item?id={object_id}"
                created = hit.get("created_at")
                try:
                    published = datetime.fromisoformat(created.replace("Z", "+00:00"))
                except (TypeError, ValueError):
                    published = datetime.now(timezone.utc)

                points = hit.get("points", 0)
                comments = hit.get("num_comments", 0)
                items.append({
                    "source": "Hacker News",
                    "title": hit.get("title", "").strip(),
                    "url": url,
                    "published": published,
                    "raw_text": f"{points} points, {comments} comments on Hacker News. Discussion on AI applications and engineering.",
                    "image_url": None,
                    "community_score": points,
                })
                if len(items) >= limit:
                    break
        except Exception as e:
            print(f"[fetchers] Hacker News query '{q}' failed: {e}")
        if len(items) >= limit:
            break

    return items


def fetch_hf_daily_papers(limit=25):
    items = []
    try:
        resp = requests.get("https://huggingface.co/api/daily_papers",
                             headers=HEADERS, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        for entry in data[:limit]:
            paper = entry.get("paper", {})
            paper_id = paper.get("id", "")
            # Accurate publication date from Hugging Face
            pub_str = paper.get("publishedAt") or entry.get("publishedAt")
            published_dt = None
            if pub_str:
                try:
                    published_dt = datetime.fromisoformat(pub_str.replace("Z", "+00:00")).astimezone(timezone.utc)
                except Exception:
                    pass

            if not published_dt:
                continue

            image_url = f"https://cdn-thumbnails.huggingface.co/social-thumbnails/papers/{paper_id}.png"
            items.append({
                "source": "Hugging Face Daily Papers",
                "title": paper.get("title", "").strip(),
                "url": f"https://huggingface.co/papers/{paper_id}",
                "published": published_dt,
                "raw_text": (paper.get("summary") or "")[:3500],
                "image_url": image_url,
                "community_score": paper.get("upvotes", 10),
            })
    except Exception as e:
        print(f"[fetchers] HF Daily Papers failed: {e}")
    return items


def fetch_arxiv_ai(limit=15):
    """Latest AI research papers from cs.AI."""
    items = []
    try:
        resp = requests.get(
            "http://export.arxiv.org/api/query",
            params={"search_query": "cat:cs.AI", "sortBy": "submittedDate",
                    "sortOrder": "descending", "max_results": limit},
            headers=HEADERS, timeout=15,
        )
        resp.raise_for_status()
        feed = feedparser.parse(resp.text)
        for entry in feed.entries[:limit]:
            pub_date = _safe_parsed_date(entry)
            if not pub_date:
                continue
            items.append({
                "source": "arXiv (cs.AI)",
                "title": entry.get("title", "").strip().replace("\n", " "),
                "url": entry.get("link", ""),
                "published": pub_date,
                "raw_text": (entry.get("summary") or "")[:3500],
                "image_url": None,
                "community_score": 5,
            })
    except Exception as e:
        print(f"[fetchers] arXiv AI failed: {e}")
    return items


def fetch_arxiv_software_nlp(limit=15):
    """Latest AI engineering and language papers from cs.SE (Software Eng) and cs.CL (NLP)."""
    items = []
    try:
        resp = requests.get(
            "http://export.arxiv.org/api/query",
            params={"search_query": "cat:cs.SE OR cat:cs.CL", "sortBy": "submittedDate",
                    "sortOrder": "descending", "max_results": limit},
            headers=HEADERS, timeout=15,
        )
        resp.raise_for_status()
        feed = feedparser.parse(resp.text)
        for entry in feed.entries[:limit]:
            pub_date = _safe_parsed_date(entry)
            if not pub_date:
                continue
            items.append({
                "source": "arXiv (Software & Language AI)",
                "title": entry.get("title", "").strip().replace("\n", " "),
                "url": entry.get("link", ""),
                "published": pub_date,
                "raw_text": (entry.get("summary") or "")[:3500],
                "image_url": None,
                "community_score": 5,
            })
    except Exception as e:
        print(f"[fetchers] arXiv cs.SE/CL failed: {e}")
    return items


ALL_FETCHERS = [
    fetch_hn_ai,
    fetch_hf_daily_papers,
    fetch_techcrunch_ai,
    fetch_theverge_ai,
    fetch_simon_willison,
    fetch_interconnects,
    fetch_ahead_of_ai,
    fetch_semianalysis,
    fetch_openai_news,
    fetch_googledeepmind_news,
    fetch_anthropic_news,
    fetch_reddit_localllama,
    fetch_arxiv_ai,
    fetch_arxiv_software_nlp,
]


import concurrent.futures


def fetch_all():
    items = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        future_to_fn = {executor.submit(fn): fn for fn in ALL_FETCHERS}
        for future in concurrent.futures.as_completed(future_to_fn):
            fn = future_to_fn[future]
            try:
                feed_items = future.result()
                items.extend(feed_items)
            except Exception as e:
                print(f"[fetchers] Global failure in {fn.__name__}: {e}")
    return items

