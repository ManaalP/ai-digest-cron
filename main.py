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

    # SMTP credentials (optional: if omitted, updates DB without sending email)
    smtp_host = env("SMTP_HOST", required=False)
    smtp_port = int(env("SMTP_PORT", "587"))
    smtp_username = env("SMTP_USERNAME", required=False)
    smtp_password = env("SMTP_PASSWORD", required=False)
    email_from = env("EMAIL_FROM", required=False)
    email_to_raw = env("EMAIL_TO", required=False)
    email_to = [e.strip() for e in email_to_raw.split(",") if e.strip()] if email_to_raw else []

    print(f"[main] Run started {datetime.now(timezone.utc).isoformat()}")

    db = get_db(database_url, db_path)

    # Clean reset support
    if "--reset" in sys.argv:
        print("[main] --reset requested: Purging old database records...")
        db.purge_all_articles()

    # Configurable retention window (defaults to 1 day when --yesterday or --one-day-only is passed)
    retention_days = int(env("RETENTION_DAYS", "1" if "--yesterday" in sys.argv or "--one-day-only" in sys.argv else "7"))
    for arg in sys.argv:
        if arg.startswith("--retention-days="):
            try:
                retention_days = int(arg.split("=", 1)[1])
            except ValueError:
                pass
    db.cleanup_older_than(days=retention_days)

    # Check for LLM keys (optional: falls back to intelligent extractive ranking)
    summarizer = None
    has_llm_key = any(cfg.get("api_key") for cfg in provider_configs.values())
    if has_llm_key:
        try:
            summarizer = MultiProviderSummarizer(provider_configs, provider_priority)
            print("[main] MultiProviderSummarizer initialized with configured LLM API keys.")
        except Exception as e:
            print(f"[main] LLM Summarizer init warning: {e}. Using built-in ranking engine.")
    else:
        print("[main] No LLM API keys configured -- using built-in extractive ranking & developer impact engine.")

    from ranker import rank_and_structure_digest

    raw_items = fetch_all()
    print(f"[main] Fetched {len(raw_items)} raw items across all sources.")

    # Filter out URLs already stored in DB using high-speed batch check
    all_urls = [it["url"] for it in raw_items if it.get("url")]
    unseen_set = db.filter_unseen_urls(all_urls) if hasattr(db, "filter_unseen_urls") else {u for u in all_urls if not db.url_exists(u)}
    fresh_unseen = [it for it in raw_items if it.get("url") in unseen_set]

    # Parse command line date targets if specified
    target_date = None
    if "--yesterday" in sys.argv:
        target_date = (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%d")
        print(f"[main] Target date set to completed previous day: {target_date}")
    elif "--today" in sys.argv:
        target_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        print(f"[main] Target date set to today: {target_date}")
    else:
        for arg in sys.argv:
            if arg.startswith("--date="):
                target_date = arg.split("=", 1)[1].strip()
                print(f"[main] Target date explicitly set to: {target_date}")
                break

    # If no target date specified, default strictly to today's date for 1-day isolation
    if not target_date and "--all-recent" not in sys.argv:
        target_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        print(f"[main] Defaulting strictly to current calendar day: {target_date}")

    # Structure into Highlights, Top 10, and 1-Liners (strict 24h window or target date)
    digest_data = rank_and_structure_digest(fresh_unseen, lookback_hours=lookback_hours, target_date=target_date)
    top_articles = digest_data["top_10"]
    one_liners = digest_data.get("one_liners", [])

    if not top_articles and not one_liners:
        print("[main] Database is already up to date with latest 24h articles.")
        return

    print(f"[main] Storing {len(top_articles)} featured and {len(one_liners)} quick-hit articles in database...")

    # Process and store featured top articles
    for item in top_articles:
        if summarizer:
            try:
                result = summarizer.summarize(item["title"], item.get("raw_text", ""), item["source"])
                item["summary"] = result.get("summary") or item.get("summary")
                item["entities"] = result.get("entities") or item.get("entities", [])
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
            summary=item.get("summary", ""),
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

    # Also store remaining quick-hit 1-liners so the web app has full coverage for the day
    for item in one_liners:
        db.insert_article(
            source=item["source"],
            title=item["title"],
            url=item["url"],
            published_date=item["published"].isoformat() if item.get("published") else "",
            summary=item.get("summary") or item.get("one_liner", ""),
            entities=item.get("entities", []),
            parent_id=None,
            category=item.get("category"),
            category_tag=item.get("category_tag"),
            dev_impact_score=item.get("dev_impact_score", 60),
            is_groundbreaking=item.get("is_groundbreaking", False),
            image_url=item.get("image_url"),
            dev_use_case=item.get("dev_use_case"),
            one_liner=item.get("one_liner"),
        )

    print(f"[main] Database successfully updated with {len(top_articles) + len(one_liners)} fresh articles.")

    # Automatically sync seed_7days.json and rebuild index.html
    try:
        from db import export_db_to_seed
        export_db_to_seed(db)
        import subprocess
        subprocess.run([sys.executable, "build_webapp.py"], check=True)
        print("[main] Automatically refreshed seed_7days.json and rebuilt index.html.")
    except Exception as e:
        print(f"[main] Web app auto-build warning: {e}")

    # Email notification (if SMTP credentials are provided)
    if smtp_host and smtp_username and smtp_password and email_from and email_to:
        try:
            send_email(smtp_host, smtp_port, smtp_username, smtp_password,
                       email_from, email_to, digest_data)
            print(f"[main] Sent email digest to {email_to}.")
        except Exception as e:
            print(f"[main] Email delivery skipped/failed: {e}")
    else:
        print("[main] SMTP credentials not provided; skipping email delivery. Database updated for web app.")


if __name__ == "__main__":
    if "--sample" in sys.argv or "--dry-run" in sys.argv:
        from sample_run import generate_sample_digest
        generate_sample_digest()
    else:
        main()

# Top-level handler for Vercel/serverless environments if inspected
def handler(request=None, response=None):
    return {"status": "ok", "message": "AI Pulse Cron CLI"}

app = handler

