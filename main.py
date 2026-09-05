#!/usr/bin/env python3
"""
Daily AI-news digest. Run this from cron once a day.

    0 7 * * *  cd /path/to/ai-digest-cron && /path/to/venv/bin/python main.py >> logs/run.log 2>&1

See README.md for setup.
"""

import os
import sys
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

from db import get_db
from fetchers import fetch_all
from summarizer import MultiProviderSummarizer
from emailer import send_email

load_dotenv()


def env(name, default=None, required=False):
    val = os.getenv(name, default)
    if required and not val:
        print(f"[main] Missing required env var: {name}. Copy .env.example to .env and fill it in.")
        sys.exit(1)
    return val


def main():
    db_path = env("DB_PATH", "./digest.db")
    database_url = env("DATABASE_URL")  # if set (e.g. Supabase), Postgres is used instead of SQLite

    provider_priority = [p.strip() for p in env("PROVIDER_PRIORITY", "anthropic,openai,google").split(",") if p.strip()]
    provider_configs = {
        "anthropic": {"api_key": env("ANTHROPIC_API_KEY"), "model": env("ANTHROPIC_MODEL", "claude-sonnet-5")},
        "openai": {"api_key": env("OPENAI_API_KEY"), "model": env("OPENAI_MODEL", "gpt-4.1-mini")},
        "google": {"api_key": env("GOOGLE_API_KEY"), "model": env("GOOGLE_MODEL", "gemini-2.0-flash")},
    }

    max_articles = int(env("MAX_ARTICLES_PER_RUN", "15"))
    lookback_hours = int(env("LOOKBACK_HOURS", "26"))
    cont_days = int(env("CONTINUATION_LOOKBACK_DAYS", "21"))
    cont_threshold = float(env("CONTINUATION_SIMILARITY_THRESHOLD", "0.34"))

    smtp_host = env("SMTP_HOST", required=True)
    smtp_port = int(env("SMTP_PORT", "587"))
    smtp_username = env("SMTP_USERNAME", required=True)
    smtp_password = env("SMTP_PASSWORD", required=True)
    email_from = env("EMAIL_FROM", required=True)
    email_to = [e.strip() for e in env("EMAIL_TO", required=True).split(",") if e.strip()]

    print(f"[main] Run started {datetime.now(timezone.utc).isoformat()}")

    db = get_db(database_url, db_path)
    # Maintain strict 7-day retention in database
    db.cleanup_older_than(days=7)

    try:
        summarizer = MultiProviderSummarizer(provider_configs, provider_priority)
    except RuntimeError as e:
        print(f"[main] {e}")
        sys.exit(1)

    from ranker import rank_and_structure_digest

    raw_items = fetch_all()
    print(f"[main] Fetched {len(raw_items)} raw items across all sources.")

    # Filter out URLs already stored in DB
    fresh_unseen = [it for it in raw_items if it.get("url") and not db.url_exists(it["url"])]

    # Structure into Highlights, Top 10, and 1-Liners (strict 24h window)
    digest_data = rank_and_structure_digest(fresh_unseen, lookback_hours=lookback_hours)
    top_articles = digest_data["top_10"]

    if not top_articles:
        print("[main] Nothing new to send today.")
        return

    print(f"[main] Processing {len(top_articles)} top-ranked articles with AI summarizer...")
    for item in top_articles:
        try:
            result = summarizer.summarize(item["title"], item.get("raw_text", ""), item["source"])
            item["summary"] = result["summary"]
            item["entities"] = result["entities"]
        except Exception as e:
            print(f"[main] LLM Summarization failed for '{item['title']}', using excerpt: {e}")

        continuation = db.find_continuation(item.get("entities", []), cont_days, cont_threshold)
        item["continuation"] = continuation
        parent_id = continuation["id"] if continuation else None

        db.insert_article(
            source=item["source"],
            title=item["title"],
            url=item["url"],
            published_date=item["published"].isoformat() if item.get("published") else "",
            summary=item["summary"],
            entities=item.get("entities", []),
            parent_id=parent_id,
            category=item.get("category"),
            category_tag=item.get("category_tag"),
            dev_impact_score=item.get("dev_impact_score", 75),
            is_groundbreaking=item.get("is_groundbreaking", False),
            image_url=item.get("image_url"),
            dev_use_case=item.get("dev_use_case"),
            one_liner=item.get("one_liner"),
        )

    send_email(smtp_host, smtp_port, smtp_username, smtp_password,
               email_from, email_to, digest_data)
    print(f"[main] Done. Sent digest with {len(top_articles)} featured articles and {len(digest_data['one_liners'])} 1-liners.")


if __name__ == "__main__":
    if "--sample" in sys.argv or "--dry-run" in sys.argv:
        from sample_run import generate_sample_digest
        generate_sample_digest()
    else:
        main()
