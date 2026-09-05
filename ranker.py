"""
ranker.py - Article ranking, categorization, and scoring engine.

Prioritizes software developer impact, practical applications, and groundbreaking
breakthroughs (e.g. cancer/biology/robotics/3D generation) over generic corporate news.
"""

import re
import html
from datetime import datetime, timedelta, timezone


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


def is_reddit_article(item: dict) -> bool:
    source = (item.get("source") or "").lower()
    url = (item.get("url") or "").lower()
    return "reddit.com" in url or "reddit" in source or source.startswith("r/")


def rank_and_structure_digest(raw_items: list, lookback_hours: int = 24, target_date: str = None) -> dict:
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(hours=lookback_hours)

    # 1. Filter strictly by target date or <= lookback_hours AND require AI relevance
    if target_date:
        fresh_items = [
            it for it in raw_items
            if it.get("published") and it["published"].strftime("%Y-%m-%d") == target_date and it.get("url") and is_ai_relevant(it)
        ]
    else:
        fresh_items = [
            it for it in raw_items
            if it.get("published") and it["published"] >= cutoff and it.get("url") and is_ai_relevant(it)
        ]

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

    # Score and classify each article
    scored = [score_and_classify_article(it) for it in deduped]

    # Sort descending by score, then published date
    scored.sort(key=lambda x: (x["score"], x["published"] or datetime.min.replace(tzinfo=timezone.utc)), reverse=True)

    # Identify groundbreaking articles (non-Reddit only for Top 10)
    groundbreaking = [a for a in scored if a["is_groundbreaking"] and not is_reddit_article(a)]

    # Pick Top 10 articles (main articles):
    # Reddit articles are strictly barred from Top 10
    top_10 = []
    top_10_urls = set()

    for g in groundbreaking[:2]:
        top_10.append(g)
        top_10_urls.add(g["url"])

    for a in scored:
        if len(top_10) >= 10:
            break
        if not is_reddit_article(a) and a["url"] not in top_10_urls:
            top_10.append(a)
            top_10_urls.add(a["url"])

    # Remaining items go to Quick Hits (1-liners)
    # Curate exactly 15 items for Quick-Hit 1-Liners:
    # Ensure Reddit discussions are featured here instead of main articles
    remaining_candidates = [a for a in scored if a["url"] not in top_10_urls]
    reddit_candidates = [a for a in remaining_candidates if is_reddit_article(a)]
    other_candidates = [a for a in remaining_candidates if not is_reddit_article(a)]

    max_quick_hits = 15
    selected_one_liners = []
    selected_urls = set()

    # Prioritize top Reddit discussions into Quick-Hits
    for r in reddit_candidates[:6]:
        selected_one_liners.append(r)
        selected_urls.add(r["url"])

    # Fill remaining slots up to 15 with highest-scoring other candidates
    for o in other_candidates:
        if len(selected_one_liners) >= max_quick_hits:
            break
        if o["url"] not in selected_urls:
            selected_one_liners.append(o)
            selected_urls.add(o["url"])

    # If still under 15, add any remaining Reddit candidates
    for r in reddit_candidates[6:]:
        if len(selected_one_liners) >= max_quick_hits:
            break
        if r["url"] not in selected_urls:
            selected_one_liners.append(r)
            selected_urls.add(r["url"])

    # Sort the 15 one-liners by score descending
    selected_one_liners.sort(key=lambda x: (x["score"], x["published"] or datetime.min.replace(tzinfo=timezone.utc)), reverse=True)
    one_liners = selected_one_liners

    # Generate executive highlights summary from top 10 main articles
    highlights = generate_executive_highlights(top_10)

    return {
        "total_scanned": len(raw_items),
        "total_fresh_24h": len(deduped),
        "groundbreaking_count": len(groundbreaking),
        "highlights": highlights,
        "top_10": top_10,
        "one_liners": one_liners,
        "generated_at": now,
    }
