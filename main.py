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

load_dotenv()


def env(name, default=None, required=False):
    val = os.getenv(name)
    if val is None or (isinstance(val, str) and val.strip() == ""):
        val = default
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
        "google": {"api_key": env("GOOGLE_API_KEY"), "model": env("GOOGLE_MODEL", "gemini-3.6-flash")},
    }

    try:
        max_articles = int(env("MAX_ARTICLES_PER_RUN", "15"))
    except (TypeError, ValueError):
        max_articles = 15

    try:
        lookback_hours = int(env("LOOKBACK_HOURS", "26"))
    except (TypeError, ValueError):
        lookback_hours = 26

    try:
        cont_days = int(env("CONTINUATION_LOOKBACK_DAYS", "21"))
    except (TypeError, ValueError):
        cont_days = 21

    try:
        cont_threshold = float(env("CONTINUATION_SIMILARITY_THRESHOLD", "0.34"))
    except (TypeError, ValueError):
        cont_threshold = 0.34

    # SMTP credentials (optional: if omitted, updates DB without sending email)
    smtp_host = env("SMTP_HOST", required=False)
    smtp_port_raw = env("SMTP_PORT", "587")
    try:
        smtp_port = int(smtp_port_raw) if smtp_port_raw else 587
    except (TypeError, ValueError):
        smtp_port = 587

    smtp_username = env("SMTP_USERNAME", required=False)
    smtp_password = env("SMTP_PASSWORD", required=False)
    email_from = env("EMAIL_FROM", required=False)
    email_to_raw = env("EMAIL_TO", required=False)
    email_to = [e.strip() for e in email_to_raw.split(",") if e.strip()] if email_to_raw else []

    print(f"[main] Run started {datetime.now(timezone.utc).isoformat()}")

    try:
        db = get_db(database_url, db_path)
    except Exception as e:
        print(f"[main] Database connection notice ({e}). Falling back to local SQLite ({db_path}).")
        from db import SQLiteDigestDB
        db = SQLiteDigestDB(db_path)

    # Clean reset support
    if "--reset" in sys.argv:
        print("[main] --reset requested: Purging old database records...")
        db.purge_all_articles()

    # Retention window defaults to 28 days (4 full rolling weeks)
    try:
        retention_days = int(env("RETENTION_DAYS", "28"))
    except (TypeError, ValueError):
        retention_days = 28

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

    from ranker import get_weekly_windows, rank_and_structure_weekly_digest, is_social_media, is_video

    raw_items = fetch_all()
    print(f"[main] Fetched {len(raw_items)} raw items across all news, research, video, and social sources.")

    # High-speed batch unseen URL check
    all_urls = [it["url"] for it in raw_items if it.get("url")]
    unseen_set = db.filter_unseen_urls(all_urls) if hasattr(db, "filter_unseen_urls") else {u for u in all_urls if not db.url_exists(u)}
    fresh_unseen = [it for it in raw_items if it.get("url") in unseen_set]

    # Calculate weekly windows (Week 1 = Aug 30 - Sep 05, 2026 for reference date 2026-09-06)
    weekly_windows = get_weekly_windows()
    target_weeks = [weekly_windows[0]]
    if "--all-weeks" in sys.argv or "--reset" in sys.argv:
        target_weeks = weekly_windows
    for arg in sys.argv:
        if arg.startswith("--week-index="):
            try:
                idx = int(arg.split("=", 1)[1])
                if 0 <= idx < len(weekly_windows):
                    target_weeks = [weekly_windows[idx]]
            except ValueError:
                pass

    total_added = 0
    for target_week in target_weeks:
        print(f"\n[main] Processing edition: {target_week['short_label']} ({target_week['start']} to {target_week['end']})")

        # Structure weekly digest with live URL verification
        digest_data = rank_and_structure_weekly_digest(
            fresh_unseen,
            start_date=target_week["start"],
            end_date=target_week["end"]
        )

        top_articles = digest_data.get("top_articles", [])
        videos = digest_data.get("videos", [])
        social_buzz = digest_data.get("social_buzz", [])
        one_liners = digest_data.get("one_liners", [])

        print(f"[main] Storing {len(top_articles)} articles, {len(videos)} videos, {len(social_buzz)} social items, {len(one_liners)} quick-hits in database for {target_week['short_label']}...")

        # 1. Process and store Top Articles (with optional LLM summarization)
        for item in top_articles:
            if summarizer and not is_social_media(item):
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
                content_type=item.get("content_type", "article"),
                week_id=target_week["id"],
                week_label=target_week["label"],
                video_id=item.get("video_id"),
            )

        # 2. Process and store Videos
        for item in videos:
            db.insert_article(
                source=item["source"],
                title=item["title"],
                url=item["url"],
                published_date=item["published"].isoformat() if item.get("published") else "",
                summary=item.get("raw_text", ""),
                entities=item.get("entities", []),
                parent_id=None,
                category="🎥 AI Video Breakdown",
                category_tag="VIDEO",
                dev_impact_score=item.get("dev_impact_score", 80),
                is_groundbreaking=False,
                image_url=item.get("image_url"),
                dev_use_case=item.get("dev_use_case", "Watch technical breakdown and architecture walkthrough."),
                one_liner=item.get("one_liner", item.get("title")),
                content_type="video",
                week_id=target_week["id"],
                week_label=target_week["label"],
                video_id=item.get("video_id"),
            )

        # 3. Process and store Social Media Buzz & Founder Takes
        for item in social_buzz:
            db.insert_article(
                source=item["source"],
                title=item["title"],
                url=item["url"],
                published_date=item["published"].isoformat() if item.get("published") else "",
                summary=item.get("raw_text", ""),
                entities=item.get("entities", []),
                parent_id=None,
                category="💬 Community Buzz & Founder Takes",
                category_tag="SOCIAL",
                dev_impact_score=item.get("dev_impact_score", 70),
                is_groundbreaking=False,
                image_url=item.get("image_url"),
                dev_use_case="Real-world practitioner discussions, model quirks, and founder perspectives.",
                one_liner=item.get("one_liner", item.get("title")),
                content_type="social_buzz",
                week_id=target_week["id"],
                week_label=target_week["label"],
                video_id=None,
            )

        # 4. Process and store Quick-Hit 1-Liners (up to 15)
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
                content_type="one_liner",
                week_id=target_week["id"],
                week_label=target_week["label"],
                video_id=item.get("video_id"),
            )

        total_added += len(top_articles) + len(videos) + len(social_buzz) + len(one_liners)

    print(f"\n[main] Database successfully updated with {total_added} total verified items across editions.")

    # Automatically sync seed_7days.json and rebuild index.html
    try:
        from db import export_db_to_seed
        export_db_to_seed(db)
        import subprocess
        subprocess.run([sys.executable, "build_webapp.py"], check=True)
        print("[main] Automatically refreshed 4-week seed dataset and rebuilt index.html.")
    except Exception as e:
        print(f"[main] Web app auto-build notice: {e}")


if __name__ == "__main__":
    if "--sample" in sys.argv or "--dry-run" in sys.argv:
        from sample_run import generate_sample_digest
        generate_sample_digest()
    else:
        main()


def handler(request=None, response=None):
    return {"status": "ok", "message": "Weekly AI Digest Cron"}


app = handler

