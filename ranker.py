"""
ranker.py - Article ranking, categorization, and scoring engine.

Prioritizes software developer impact, practical applications, and groundbreaking
breakthroughs (e.g. cancer/biology/robotics/3D generation) over generic corporate news.
"""

import re
import html
import concurrent.futures
import urllib.parse
from datetime import datetime, timedelta, timezone
import requests


def is_reachable_url(url: str, timeout: float = 3.5) -> bool:
    """Live HTTP verification ensuring URL is accessible and does not return 404/410/broken."""
    if not url or not isinstance(url, str):
        return False
    url = url.strip()
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        return False
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        resp = requests.head(url, headers=headers, allow_redirects=True, timeout=timeout)
        if resp.status_code in (404, 410):
            print(f"[verifier] ❌ Discarded broken URL ({resp.status_code}): {url}")
            return False
        if resp.status_code == 405:  # Method Not Allowed for HEAD
            r2 = requests.get(url, headers=headers, stream=True, timeout=timeout)
            if r2.status_code in (404, 410):
                print(f"[verifier] ❌ Discarded broken URL ({r2.status_code}): {url}")
                return False
        return True
    except Exception:
        # Retry with streaming GET in case HEAD was blocked or timed out
        try:
            r3 = requests.get(url, headers=headers, stream=True, timeout=timeout)
            if r3.status_code in (404, 410):
                print(f"[verifier] ❌ Discarded broken URL ({r3.status_code}): {url}")
                return False
            return True
        except Exception:
            print(f"[verifier] ⚠️ Unreachable URL: {url}")
            return False


def verify_urls_concurrently(items: list, max_workers: int = 16) -> list:
    """Verify all candidate URLs concurrently with a thread pool."""
    if not items:
        return []
    valid_items = []
    print(f"[verifier] Verifying live reachability for {len(items)} candidate URLs...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_item = {executor.submit(is_reachable_url, it.get("url")): it for it in items if it.get("url")}
        for future in concurrent.futures.as_completed(future_to_item):
            item = future_to_item[future]
            try:
                if future.result():
                    valid_items.append(item)
            except Exception:
                pass
    print(f"[verifier] ✅ {len(valid_items)} / {len(items)} URLs passed live reachability audit.")
    return valid_items



GROUNDBREAKING_PATTERNS = [
    r"\b(cancer|oncology|tumor|disease|cure|biomarker|protein fold|genomics|biomedical|brain-computer|bci|paralysis|speech restoration)\b",
    r"\b(3d (?:reconstruction|model|mesh|gaussian|generation)|neural radiance|world model|physical reasoning)\b",
    r"\b(robot(?:ic|ics)?|dexterous manipulation|humanoid|bimanual|embodied ai)\b",
    r"\b(first gigawatt|breakthrough|landmark discovery)\b",
]

DEV_TOOLING_PATTERNS = [
    r"\b(agentic coding|code generation|copilot|ide|compiler|codebase|debugger|dev tool|software engineer|github|cli|terminal|sdk|library|open source)\b",
    r"\b(claude code|cursor|cline|roo code|windsurf|codex|devin|aider)\b",
    r"\b(unit test|refactoring|pull request|git|python|typescript|rust|c\+\+)\b",
]

LOCAL_INFERENCE_PATTERNS = [
    r"\b(localllama|local llm|ollama|vllm|llama\.cpp|sglang|tensorrt|exllamav2)\b",
    r"\b(quantization|gguf|awq|fp8|int4|bitsandbytes)\b",
    r"\b(vram|rtx 4090|gpu memory|kv cache|cache offload|throughput|latency|speculative decoding)\b",
    r"\b(qwen|deepseek|mistral|llama 3|phi|gemma)\b",
]

PRACTICAL_APP_PATTERNS = [
    r"\b(production|enterprise|workflow|automation|cybersecurity|security|rogue agent|data pipeline|real-time|rag|vector db)\b",
    r"\b(deployment|api integration|cost optimization|evals|benchmark reliability)\b",
]

SPECULATION_OR_GOSSIP_PATTERNS = [
    r"\b(talks for series|valuation|pre-ipo|funding round|lawsuit|gossip|rumor|feud)\b",
]


def clean_text(raw_text: str) -> str:
    if not raw_text:
        return ""
    text = re.sub(r"<[^>]+>", " ", raw_text)
    text = html.unescape(text)
    text = re.sub(r"submitted by\s+/u/\S+.*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\[link\]\s*\[comments\]", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_entities(title: str, text: str) -> list:
    patterns = [
        r"\b(GPT-?[\w\.]+)\b",
        r"\b(Claude[\w\.\s-]*)\b",
        r"\b(Gemini[\w\.\s-]*)\b",
        r"\b(Llama[\w\.\s-]*)\b",
        r"\b(Qwen[\w\.\s-]*)\b",
        r"\b(DeepSeek[\w\.\s-]*)\b",
        r"\b(Mistral[\w\.\s-]*)\b",
        r"\b(vLLM|Ollama|GGUF|KV Cache|RoboTok|VeriPhy|Blender|Astra)\b",
        r"\b(OpenAI|Anthropic|Google DeepMind|Meta AI|Microsoft|xAI|Hugging Face)\b",
    ]
    found = set()
    content = f"{title} {text}"
    for pat in patterns:
        for m in re.findall(pat, content, re.IGNORECASE):
            found.add(m.strip())
    if not found:
        tokens = re.findall(r"\b[A-Z][a-zA-Z0-9-]{2,}\b", title)
        found = set(tokens[:4])
    return list(found)[:5]


def score_and_classify_article(item: dict) -> dict:
    title = item.get("title", "")
    raw = item.get("raw_text", "")
    text = clean_text(raw)
    content = f"{title} {text}".lower()

    score = 30.0
    category = "🔬 Applied Research"
    category_tag = "RESEARCH"
    is_groundbreaking = False
    dev_impact_score = 50

    # 1. Groundbreaking check
    ground_matches = sum(len(re.findall(pat, content)) for pat in GROUNDBREAKING_PATTERNS)
    if ground_matches > 0:
        is_groundbreaking = True
        score += 100.0 + min(ground_matches * 10, 30)
        category = "🚨 Groundbreaking Breakthrough"
        category_tag = "BREAKTHROUGH"
        dev_impact_score = 95

    # 2. Developer Tooling & Agentic Coding
    dev_matches = sum(len(re.findall(pat, content)) for pat in DEV_TOOLING_PATTERNS)
    if dev_matches > 0:
        score += 75.0 + min(dev_matches * 8, 30)
        dev_impact_score = max(dev_impact_score, 88 + min(dev_matches * 3, 10))
        if not is_groundbreaking:
            category = "🛠️ Developer Tooling & Agents"
            category_tag = "DEV TOOLS"

    # 3. Local Inference & Hardware Efficiency
    local_matches = sum(len(re.findall(pat, content)) for pat in LOCAL_INFERENCE_PATTERNS)
    if local_matches > 0:
        score += 65.0 + min(local_matches * 7, 25)
        dev_impact_score = max(dev_impact_score, 82 + min(local_matches * 3, 12))
        if not is_groundbreaking and category_tag != "DEV TOOLS":
            category = "⚡ Local AI & Inference Optimization"
            category_tag = "LOCAL AI"

    # 4. Practical Application & Production
    app_matches = sum(len(re.findall(pat, content)) for pat in PRACTICAL_APP_PATTERNS)
    if app_matches > 0:
        score += 55.0 + min(app_matches * 6, 20)
        dev_impact_score = max(dev_impact_score, 75 + min(app_matches * 3, 15))
        if not is_groundbreaking and category_tag not in ("DEV TOOLS", "LOCAL AI"):
            category = "🚀 Practical App & Security"
            category_tag = "PRODUCTION"

    # 5. Speculation / gossip penalty
    spec_matches = sum(len(re.findall(pat, content)) for pat in SPECULATION_OR_GOSSIP_PATTERNS)
    if spec_matches > 0 and not is_groundbreaking and category_tag not in ("DEV TOOLS", "LOCAL AI"):
        score -= 30.0
        dev_impact_score = max(20, dev_impact_score - 30)

    # Community signal boost
    comm_score = item.get("community_score", 0)
    score += min(comm_score * 0.15, 20.0)

    # Create technical summary (100-130 words)
    words = text.split()
    if len(words) > 120:
        summary = " ".join(words[:120]) + "..."
    elif len(words) < 20:
        summary = f"{title}. New technical release from {item.get('source')} offering practical insights and implementations for engineers."
    else:
        summary = text

    # Generate developer & practical use case statement
    if "agent" in content or "code" in content or "blender" in content:
        dev_use_case = "Enables automated software workflows, local execution, and tooling integration for engineers building autonomous or assisted development pipelines."
    elif "inference" in content or "kv" in content or "vram" in content or "4090" in content or "qwen" in content:
        dev_use_case = "Reduces local compute and VRAM overhead, improving inference throughput and deployment cost-efficiency for local or self-hosted models."
    elif is_groundbreaking:
        dev_use_case = "Demonstrates fundamental algorithmic expansion into complex real-world environments, opening new horizons for cross-disciplinary AI applications."
    elif "security" in content or "wiki" in content or "rogue" in content:
        dev_use_case = "Critical considerations for sandbox isolation, agent permission boundaries, and defense-in-depth monitoring in autonomous multi-agent deployments."
    else:
        dev_use_case = "Provides practical architecture patterns and benchmarks that engineers can test and apply in current AI-assisted pipelines."

    # 1-liner summary
    if len(words) > 18:
        one_liner = " ".join(words[:18]) + "..."
    else:
        one_liner = text or title

    entities = extract_entities(title, text)

    return {
        "source": item.get("source", ""),
        "title": title,
        "url": item.get("url", ""),
        "published": item.get("published"),
        "raw_text": raw,
        "summary": summary,
        "dev_use_case": dev_use_case,
        "one_liner": one_liner,
        "category": category,
        "category_tag": category_tag,
        "score": round(score, 2),
        "dev_impact_score": min(99, dev_impact_score),
        "is_groundbreaking": is_groundbreaking,
        "entities": entities,
        "image_url": item.get("image_url"),
    }


def generate_executive_highlights(articles: list) -> list:
    """Creates a concise 3-4 bullet executive brief summarizing the 24h run."""
    highlights = []

    # Check for groundbreaking news
    groundbreaking = [a for a in articles if a["is_groundbreaking"]]
    if groundbreaking:
        top_g = groundbreaking[0]
        highlights.append(
            f"<strong>Breakthrough in Physical/Medical AI:</strong> {top_g['title']} showcases major advances in real-world models and domain capabilities."
        )

    # Check for developer tooling & coding agents
    dev_articles = [a for a in articles if a["category_tag"] == "DEV TOOLS"]
    if dev_articles:
        top_d = dev_articles[0]
        highlights.append(
            f"<strong>Developer Tooling & Coding Agents:</strong> Practical agentic workflows are accelerating, highlighted by <em>{top_d['title']}</em>."
        )

    # Check for local inference & performance
    local_articles = [a for a in articles if a["category_tag"] == "LOCAL AI"]
    if local_articles:
        top_l = local_articles[0]
        highlights.append(
            f"<strong>Hardware & Local Inference:</strong> Optimization for low-latency memory and KV offloading remains a top priority with releases like <em>{top_l['title']}</em>."
        )

    # Check for safety / production security
    sec_articles = [a for a in articles if "security" in a["summary"].lower() or "rogue" in a["title"].lower() or "incident" in a["title"].lower()]
    if sec_articles:
        top_s = sec_articles[0]
        highlights.append(
            f"<strong>Agent Sandboxing & Safety:</strong> New findings around autonomous multi-agent behavior highlight the need for strict execution guardrails."
        )

    if len(highlights) < 3:
        highlights.append(
            "<strong>Rapid Applied Research Iteration:</strong> Fresh arXiv and Hugging Face preprints continue pushing distillation and prompt optimization boundaries."
        )

    return highlights[:4]


AI_RELEVANCE_PATTERNS = [
    r"\b(artificial intelligence|machine learning|deep learning)\b",
    r"\b(llm|llms|gpt|claude|gemini|deepseek|llama|qwen|mistral|grok|cohere)\b",
    r"\b(neural network|transformer|attention mechanism|weights|checkpoint|safetensors)\b",
    r"\b(gguf|vllm|ollama|kv cache|sglang|tgi|exllama|nvfp4)\b",
    r"\b(reasoning model|prompt engineering|context window|fine-tuning|pretraining|rlvr|rlhf|dpo)\b",
    r"\b(coding agent|software agent|autonomous agent|agentic|multi-agent|vibecoding)\b",
    r"\b(openai|anthropic|google deepmind|meta ai|hugging face|mistral ai|coderabbit|artificial analysis|mlperf)\b",
    r"\bai\s+(model|models|agent|agents|workstation|tool|tools|research|system|systems|incident)\b",
]


def is_ai_relevant(item: dict) -> bool:
    title = item.get("title", "")
    raw = item.get("raw_text", "")
    content = f"{title} {raw}".lower()
    return any(re.search(pat, content, re.IGNORECASE) for pat in AI_RELEVANCE_PATTERNS)


def is_social_media(item: dict) -> bool:
    source = (item.get("source") or "").lower()
    url = (item.get("url") or "").lower()
    content_type = item.get("content_type", "")
    if content_type == "social_buzz":
        return True
    return any(x in url for x in ["reddit.com", "twitter.com", "x.com", "linkedin.com"]) or source.startswith("r/") or "reddit" in source or "founder" in source.lower()


def is_video(item: dict) -> bool:
    content_type = item.get("content_type", "")
    url = (item.get("url") or "").lower()
    return content_type == "video" or "youtube.com" in url or "youtu.be" in url


def is_reddit_article(item: dict) -> bool:
    return is_social_media(item)


def get_weekly_windows(ref_date=None) -> list:
    """Calculate the 4 rolling 7-day calendar weeks for historical chips."""
    if ref_date is None:
        ref_date = datetime(2026, 9, 6, tzinfo=timezone.utc).date()
    elif isinstance(ref_date, datetime):
        ref_date = ref_date.date()
    elif isinstance(ref_date, str):
        ref_date = datetime.fromisoformat(ref_date).date()

    weeks = []
    for i in range(4):
        end_d = ref_date - timedelta(days=1 + (i * 7))
        start_d = end_d - timedelta(days=6)
        w_label = f"{start_d.strftime('%b %d')} – {end_d.strftime('%b %d, %Y')}"
        w_id = f"{start_d.strftime('%Y-%m-%d')}_{end_d.strftime('%Y-%m-%d')}"
        weeks.append({
            "index": i + 1,
            "id": w_id,
            "label": w_label,
            "short_label": f"Week {i + 1} ({start_d.strftime('%b %d')}–{end_d.strftime('%b %d')})",
            "start": start_d.isoformat(),
            "end": end_d.isoformat(),
        })
    return weeks


def rank_and_structure_weekly_digest(raw_items: list, start_date: str = None, end_date: str = None, ref_date=None) -> dict:
    now = datetime.now(timezone.utc)
    weekly_windows = get_weekly_windows(ref_date)
    curr_week = weekly_windows[0]

    target_start = start_date or curr_week["start"]
    target_end = end_date or curr_week["end"]

    start_dt = datetime.fromisoformat(target_start).replace(tzinfo=timezone.utc)
    end_dt = datetime.fromisoformat(target_end).replace(hour=23, minute=59, second=59, tzinfo=timezone.utc)

    # 1. Strictly filter by weekly date boundaries and require AI relevance
    fresh_items = []
    for it in raw_items:
        pub = it.get("published")
        if not pub:
            continue
        if start_dt <= pub <= end_dt and it.get("url") and is_ai_relevant(it):
            fresh_items.append(it)

    # Deduplicate by URL and normalized title
    seen_urls = set()
    seen_titles = set()
    deduped = []
    for it in fresh_items:
        url = it["url"].strip()
        norm_title = re.sub(r"\W+", "", it.get("title", "").lower())
        if url in seen_urls or norm_title in seen_titles:
            continue
        seen_urls.add(url)
        seen_titles.add(norm_title)
        deduped.append(it)

    # Live URL reachability audit: discard broken, 404, or non-existent URLs
    verified_items = verify_urls_concurrently(deduped)

    # Score and classify each item
    scored = [score_and_classify_article(it) for it in verified_items]
    scored.sort(key=lambda x: (x["score"], x["published"] or datetime.min.replace(tzinfo=timezone.utc)), reverse=True)

    # 2. Segregate Videos
    videos = [a for a in scored if is_video(a)]
    videos.sort(key=lambda x: x["published"] or datetime.min.replace(tzinfo=timezone.utc), reverse=True)
    selected_videos = videos[:8]
    video_urls = {v["url"] for v in selected_videos}

    # 3. Segregate Social Media Buzz & Founder Takes
    social_items = [a for a in scored if is_social_media(a) and a["url"] not in video_urls]
    social_items.sort(key=lambda x: (x.get("community_score", 0), x["score"]), reverse=True)
    selected_social_buzz = social_items[:10]

    # 4. Pick Top 10 Featured Articles:
    # RULE: strictly at most 1 Reddit / social media item in top_articles!
    top_articles = []
    top_article_urls = set()
    social_in_top = 0

    groundbreaking = [a for a in scored if a["is_groundbreaking"] and not is_social_media(a) and a["url"] not in video_urls]
    for g in groundbreaking[:2]:
        top_articles.append(g)
        top_article_urls.add(g["url"])

    for a in scored:
        if len(top_articles) >= 10:
            break
        if a["url"] in top_article_urls or a["url"] in video_urls:
            continue
        if is_social_media(a):
            if social_in_top < 1:  # At most 1 social media / Reddit post in main articles
                top_articles.append(a)
                top_article_urls.add(a["url"])
                social_in_top += 1
        else:
            top_articles.append(a)
            top_article_urls.add(a["url"])

    # 5. Pick Quick-Hit 1-Liners (15 items)
    # Here, more Reddit, founder takes, and short tech updates are permitted and prioritized
    remaining = [a for a in scored if a["url"] not in top_article_urls and a["url"] not in video_urls]
    reddit_remaining = [a for a in remaining if is_social_media(a)]
    other_remaining = [a for a in remaining if not is_social_media(a)]

    max_quick_hits = 15
    selected_one_liners = []
    one_liner_urls = set()

    # Include up to 6 engaging community discussions
    for r in reddit_remaining[:6]:
        selected_one_liners.append(r)
        one_liner_urls.add(r["url"])

    # Fill remaining slots up to 15 with technical news/research
    for o in other_remaining:
        if len(selected_one_liners) >= max_quick_hits:
            break
        if o["url"] not in one_liner_urls:
            selected_one_liners.append(o)
            one_liner_urls.add(o["url"])

    # If still under 15, pull remaining social discussions
    for r in reddit_remaining[6:]:
        if len(selected_one_liners) >= max_quick_hits:
            break
        if r["url"] not in one_liner_urls:
            selected_one_liners.append(r)
            one_liner_urls.add(r["url"])

    selected_one_liners.sort(key=lambda x: (x["score"], x["published"] or datetime.min.replace(tzinfo=timezone.utc)), reverse=True)
    one_liners = selected_one_liners[:max_quick_hits]

    # Generate executive weekly highlights from top articles
    highlights = generate_executive_highlights(top_articles)

    week_label = f"{start_dt.strftime('%b %d')} – {end_dt.strftime('%b %d, %Y')}"
    week_id = f"{target_start}_{target_end}"

    return {
        "week_id": week_id,
        "week_label": week_label,
        "start_date": target_start,
        "end_date": target_end,
        "weekly_windows": weekly_windows,
        "total_scanned": len(raw_items),
        "total_fresh": len(deduped),
        "groundbreaking_count": len(groundbreaking),
        "highlights": highlights,
        "top_articles": top_articles,
        "top_10": top_articles,  # Alias for backward compatibility
        "videos": selected_videos,
        "social_buzz": selected_social_buzz,
        "one_liners": one_liners,
        "generated_at": now,
    }


def rank_and_structure_digest(raw_items: list, lookback_hours: int = 168, target_date: str = None) -> dict:
    """Wrapper ensuring backward compatibility with main.py calls."""
    if target_date and "_" in target_date:
        s, e = target_date.split("_", 1)
        return rank_and_structure_weekly_digest(raw_items, start_date=s, end_date=e)
    return rank_and_structure_weekly_digest(raw_items)
