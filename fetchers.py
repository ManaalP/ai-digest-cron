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


def _rss(source_name, feed_url, limit=20, content_type="article"):
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
                "content_type": content_type,
            })
    except Exception as e:
        print(f"[fetchers] {source_name} RSS failed: {e}")
    return items


def _youtube_rss(channel_name, feed_url, limit=10):
    items = []
    try:
        feed = feedparser.parse(feed_url, request_headers=HEADERS)
        for entry in feed.entries[:limit]:
            pub_date = _safe_parsed_date(entry)
            if not pub_date:
                continue
            thumb = None
            if entry.get("media_thumbnail") and len(entry["media_thumbnail"]) > 0:
                thumb = entry["media_thumbnail"][0].get("url")
            vid_id = entry.get("yt_videoid") or (entry.get("link", "").split("v=")[-1] if "v=" in entry.get("link", "") else None)
            desc = (entry.get("summary") or entry.get("description") or "")[:2000]
            items.append({
                "source": channel_name,
                "title": entry.get("title", "").strip(),
                "url": entry.get("link", ""),
                "published": pub_date,
                "raw_text": desc,
                "image_url": thumb,
                "community_score": 50,
                "content_type": "video",
                "video_id": vid_id,
            })
    except Exception as e:
        print(f"[fetchers] YouTube {channel_name} failed: {e}")
    return items


def fetch_simon_willison():
    return _rss("Simon Willison's Weblog", "https://simonwillison.net/atom/everything/", limit=20)


def fetch_interconnects():
    return _rss("Interconnects (Nathan Lambert)", "https://www.interconnects.ai/feed", limit=15, content_type="newsletter")


def fetch_ahead_of_ai():
    return _rss("Ahead of AI (Sebastian Raschka)", "https://magazine.sebastianraschka.com/feed", limit=15, content_type="newsletter")


def fetch_semianalysis():
    return _rss("SemiAnalysis", "https://www.semianalysis.com/feed", limit=15, content_type="newsletter")


def fetch_latent_space():
    return _rss("Latent Space (Swyx & Alessio)", "https://www.latent.space/feed", limit=15, content_type="newsletter")


def fetch_import_ai():
    return _rss("Import AI (Jack Clark)", "https://importai.substack.com/feed", limit=15, content_type="newsletter")


def fetch_one_useful_thing():
    return _rss("One Useful Thing (Ethan Mollick)", "https://www.oneusefulthing.org/feed", limit=15, content_type="newsletter")


def fetch_pragmatic_engineer():
    return _rss("The Pragmatic Engineer", "https://newsletter.pragmaticengineer.com/feed", limit=15, content_type="newsletter")


def fetch_fireship_videos():
    return _youtube_rss("Fireship", "https://www.youtube.com/feeds/videos.xml?channel_id=UCsBjURrPoezykLs9EqgamOA", limit=8)


def fetch_karpathy_videos():
    return _youtube_rss("Andrej Karpathy", "https://www.youtube.com/feeds/videos.xml?channel_id=UCXUPKJO5MZqnPe7lhA1Dx0g", limit=6)


def fetch_twominutepapers_videos():
    return _youtube_rss("Two Minute Papers", "https://www.youtube.com/feeds/videos.xml?channel_id=UCbfYPyITQ-7l4upoX8nvctg", limit=8)


def fetch_yannic_videos():
    return _youtube_rss("Yannic Kilcher", "https://www.youtube.com/feeds/videos.xml?channel_id=UCZHmQk67mSJgfCCTn7xBfew", limit=8)


def fetch_mattwolfe_videos():
    return _youtube_rss("Matt Wolfe", "https://www.youtube.com/feeds/videos.xml?channel_id=UCnmgS84t6q459etY2x-JL4A", limit=8)


def fetch_wesroth_videos():
    return _youtube_rss("Wes Roth", "https://www.youtube.com/feeds/videos.xml?channel_id=UCqcbQf6yw5KzRoDDcZ_wDOA", limit=8)


def fetch_anthropic_news(limit=10):
    items = []
    try:
        resp = requests.get(
            "https://www.anthropic.com/news",
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"},
            timeout=10,
        )
        if resp.ok:
            links = re.findall(r'href="(/news/[a-z0-9\-]+)"', resp.text)
            seen = set()
            now = datetime.now(timezone.utc)
            for l in links:
                if l not in seen and l != "/news" and not l.endswith("/feed") and not l.endswith("/rss"):
                    seen.add(l)
                    full_url = f"https://www.anthropic.com{l}"
                    slug = l.replace("/news/", "")
                    title = slug.replace("-", " ").title()
                    summary = ""
                    pub_dt = now
                    try:
                        art_resp = requests.get(full_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=5)
                        if art_resp.ok:
                            t_match = re.search(r'<title>(.*?)</title>', art_resp.text)
                            if t_match:
                                title = t_match.group(1).replace(r"\ Anthropic", "").replace("| Anthropic", "").strip()
                            d_match = re.search(r'<meta name="description" content="(.*?)"', art_resp.text)
                            if d_match:
                                summary = d_match.group(1).strip()
                            # Parse genuine publication date from page
                            date_match = re.search(r'(\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}\b)', art_resp.text)
                            if date_match:
                                raw_d = date_match.group(1).replace(',', '')
                                try:
                                    pub_dt = datetime.strptime(raw_d, '%b %d %Y').replace(tzinfo=timezone.utc)
                                except ValueError:
                                    pub_dt = datetime.strptime(raw_d, '%B %d %Y').replace(tzinfo=timezone.utc)
                    except Exception:
                        pass

                    items.append({
                        "source": "Anthropic News",
                        "title": title,
                        "url": full_url,
                        "published": pub_dt,
                        "summary": summary or f"Official Anthropic announcement regarding {title}.",
                        "raw_text": summary,
                        "category": "🛠️ Developer Tooling & Agents",
                        "category_tag": "DEV TOOLS",
                        "dev_impact_score": 92,
                        "is_groundbreaking": "opus" in slug or "standard" in slug,
                        "image_url": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=600&auto=format&fit=crop&q=80",
                        "dev_use_case": f"Frontier developer capabilities and platform updates from Anthropic.",
                        "one_liner": summary[:140] if summary else f"Anthropic updates: {title}.",
                        "content_type": "article",
                    })
                    if len(items) >= limit:
                        break
    except Exception as e:
        print(f"[fetchers] Anthropic News fetch failed: {e}")
    return items


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
            "https://www.reddit.com/r/LocalLLaMA/top/.rss?t=week",
            headers=REDDIT_HEADERS, timeout=15,
        )
        if resp.status_code == 429:
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
                "source": "r/LocalLLaMA",
                "title": entry.get("title", "").strip(),
                "url": entry.get("link", ""),
                "published": pub_date,
                "raw_text": (entry.get("summary") or "")[:3500],
                "image_url": _extract_image(entry),
                "community_score": 15,
                "content_type": "social_buzz",
            })
    except Exception as e:
        print(f"[fetchers] r/LocalLLaMA failed: {e}")
    return items


def fetch_reddit_machinelearning(limit=20):
    items = []
    try:
        resp = requests.get(
            "https://www.reddit.com/r/MachineLearning/top/.rss?t=week",
            headers=REDDIT_HEADERS, timeout=15,
        )
        if resp.status_code == 429:
            resp = requests.get(
                "https://www.reddit.com/r/MachineLearning/hot/.rss",
                headers=REDDIT_HEADERS, timeout=15,
            )
        resp.raise_for_status()
        feed = feedparser.parse(resp.text)
        for entry in feed.entries[:limit]:
            pub_date = _safe_parsed_date(entry)
            if not pub_date:
                continue
            items.append({
                "source": "r/MachineLearning",
                "title": entry.get("title", "").strip(),
                "url": entry.get("link", ""),
                "published": pub_date,
                "raw_text": (entry.get("summary") or "")[:3500],
                "image_url": _extract_image(entry),
                "community_score": 25,
                "content_type": "social_buzz",
            })
    except Exception as e:
        print(f"[fetchers] r/MachineLearning failed: {e}")
    return items


def fetch_founder_buzz(limit=15):
    """Curated AI founder takes, X/Twitter debates, and technical perspectives."""
    items = []
    queries = ["founder", "show hn", "why I built", "lessons learned scaling", "benchmarks are flawed"]
    seen_ids = set()
    for q in queries:
        try:
            resp = requests.get(
                "https://hn.algolia.com/api/v1/search_by_date",
                params={"tags": "story", "query": q, "numericFilters": "points>20"},
                headers=HEADERS, timeout=10,
            )
            resp.raise_for_status()
            data = resp.json()
            for hit in data.get("hits", []):
                oid = hit.get("objectID")
                if oid in seen_ids:
                    continue
                seen_ids.add(oid)
                pts = hit.get("points", 0)
                comm = hit.get("num_comments", 0)
                created = hit.get("created_at")
                try:
                    published = datetime.fromisoformat(created.replace("Z", "+00:00"))
                except Exception:
                    published = datetime.now(timezone.utc)
                items.append({
                    "source": "Founder & Community Takes",
                    "title": hit.get("title", "").strip(),
                    "url": hit.get("url") or f"https://news.ycombinator.com/item?id={oid}",
                    "published": published,
                    "raw_text": f"Founder & Community Discussion: {pts} upvotes, {comm} comments.",
                    "image_url": None,
                    "community_score": pts,
                    "content_type": "social_buzz",
                })
                if len(items) >= limit:
                    break
        except Exception as e:
            print(f"[fetchers] fetch_founder_buzz query '{q}' failed: {e}")
        if len(items) >= limit:
            break
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
                    "content_type": "article",
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
                "content_type": "article",
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
                "content_type": "article",
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
                "content_type": "article",
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
    fetch_latent_space,
    fetch_import_ai,
    fetch_one_useful_thing,
    fetch_pragmatic_engineer,
    fetch_openai_news,
    fetch_googledeepmind_news,
    fetch_anthropic_news,
    fetch_fireship_videos,
    fetch_karpathy_videos,
    fetch_twominutepapers_videos,
    fetch_yannic_videos,
    fetch_mattwolfe_videos,
    fetch_wesroth_videos,
    fetch_reddit_localllama,
    fetch_reddit_machinelearning,
    fetch_founder_buzz,
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


