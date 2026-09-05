# AI Developments Daily Digest

A self-contained script that pulls from primary/technical AI-news sources,
summarizes each item to 100–200 words with Claude, tracks stories over time
in a local SQLite database, flags when a new article continues an earlier
one, and emails you the digest. Runs unattended via cron.

## Sources included out of the box

- Hugging Face Daily Papers
- arXiv cs.AI (latest submissions)
- Simon Willison's Weblog
- Interconnects (Nathan Lambert)
- Ahead of AI (Sebastian Raschka)
- SemiAnalysis
- Anthropic / OpenAI / Google DeepMind blogs
- Hacker News (AI-keyword filtered, points > 30)
- r/LocalLLaMA (top of the day)

All via RSS or public APIs — no login-walled scraping, so it won't break
on layout changes. Add or remove sources in `fetchers.py`; each fetcher is
independent and one failing doesn't block the rest.

OpenReview, LMSYS Arena, and Artificial Analysis don't expose reliable
public feeds/APIs for this kind of polling, so they're not wired in — the
digest links you'll get instead point to the underlying arXiv/HN/blog posts
that usually cover their findings. You can add manual link-checks for those
if you want (see "Extending" below).

## How continuation tracking works

Every summarized article also gets 2–6 short "entities" extracted by Claude
(model names, org names, paper titles). Before sending a new article, the
script checks the database for anything sent in the last 21 days (configurable)
whose entity set overlaps enough (Jaccard similarity ≥ 0.34, configurable).
If it finds a match, the email shows:

> ↳ Continuation of *[earlier title]* (2026-08-30)

with a link back to that original source. This is a heuristic based on
shared named entities, not full semantic search — it works well for
"same model/paper, new development" stories, less well for thematically
related but differently-named stories.

## AI provider fallback

The summarization step can use Anthropic, OpenAI, and/or Google Gemini, tried
in the order set by `PROVIDER_PRIORITY` (default `anthropic,openai,google`).
You only need one key configured — the others are optional. When the current
provider fails for any reason (rate limit, quota exhausted, outage, malformed
response), the script automatically tries the next one in the list, and if a
provider fails twice in a row it's skipped for the rest of that run so a
rate-limit storm doesn't cost a retry on every remaining article. Leave a
provider's API key blank in `.env` (or don't set its secret in GitHub) to
skip it entirely — you don't need all three.

Model names for OpenAI and Google move fast; the defaults in `.env.example`
are a starting point, not a guarantee — check each provider's current docs
for what's live on your account and adjust `OPENAI_MODEL`/`GOOGLE_MODEL`.

## Setup — Option A: your own VPS (traditional cron)

1. **Get an Anthropic API key** at https://console.anthropic.com if you
   don't have one, and a Gmail (or other SMTP) app password for sending mail.
   The Anthropic API is billed separately from any claude.ai subscription —
   it's pay-per-token, but at ~15 articles/day with a small model this runs
   to well under $1/month. Check current pricing at https://docs.claude.com.

2. **Copy the config:**
   ```
   cp .env.example .env
   ```
   Fill in `ANTHROPIC_API_KEY`, `SMTP_*`, `EMAIL_FROM`, `EMAIL_TO`.
   For Gmail: enable 2FA, then create an "App Password" — use that as
   `SMTP_PASSWORD`, not your normal password. Leave `DATABASE_URL` unset —
   this path uses the local SQLite file.

3. **Install and schedule:**
   ```
   chmod +x setup_cron.sh
   ./setup_cron.sh 07:00
   ```
   This creates a virtualenv, installs dependencies, and adds a cron entry
   for 7:00 AM server time daily. Pass a different `HH:MM` to change the time.

4. **Test it manually first:**
   ```
   venv/bin/python main.py
   ```
   Check `logs/run.log` and your inbox. First run may pull a lot if your
   feeds have recent activity — tune `MAX_ARTICLES_PER_RUN` and
   `LOOKBACK_HOURS` in `.env` if it's too much or too little.

## Setup — Option B: fully free (Supabase + GitHub Actions, no server)

This runs the same script with zero infrastructure of your own: Supabase's
free Postgres tier holds the database, and a GitHub Actions scheduled
workflow replaces the cron daemon. Only ongoing cost is the Anthropic API
usage (a few cents a month at this volume).

1. **Create a Supabase project** at https://supabase.com (free tier). In
   *Project Settings → Database*, copy the connection string — use the
   **"Session pooler"** or **direct connection** URI (starts with
   `postgresql://postgres...`), not the pgbouncer transaction-mode one,
   since this script opens short-lived connections once a day, not a pool.
   You can optionally run `supabase_schema.sql` in the SQL Editor first,
   or just let the script create the table itself on first run.

2. **Push this project to a new GitHub repo** (private is fine — this fits
   comfortably in the free 2,000 min/month Actions quota at ~1-2 min/run):
   ```
   git init && git add . && git commit -m "Initial commit"
   git remote add origin https://github.com/<you>/<repo>.git
   git push -u origin main
   ```
   `.env` is for local testing only — **don't commit it** (it's already
   covered by the `.gitignore` below); secrets for Actions are set separately.

3. **Add repo secrets:** GitHub repo → *Settings → Secrets and variables →
   Actions → New repository secret*. Add:
   - `ANTHROPIC_API_KEY` and/or `OPENAI_API_KEY` and/or `GOOGLE_API_KEY`
     (at least one, more for automatic fallback)
   - `DATABASE_URL` (the Supabase connection string from step 1)
   - `SMTP_HOST`, `SMTP_PORT`, `SMTP_USERNAME`, `SMTP_PASSWORD`
   - `EMAIL_FROM`, `EMAIL_TO`

   Optional — if you want non-default models or a different fallback order,
   add these as repo *variables* (not secrets, since they're not sensitive):
   `PROVIDER_PRIORITY`, `ANTHROPIC_MODEL`, `OPENAI_MODEL`, `GOOGLE_MODEL`.

4. **That's it.** `.github/workflows/daily-digest.yml` is already in this
   project and will start firing on its schedule once pushed. Trigger it
   manually first to test: repo → *Actions* tab → *Daily AI Digest* →
   *Run workflow*. Check the run logs and your inbox.

**Two GitHub Actions quirks worth knowing:**
- Scheduled runs can lag under platform load, especially at round times —
  the included workflow uses `13 7 * * *` (7:13 AM UTC) rather than
  `0 7 * * *` for this reason. Times are UTC; convert from your local time.
- GitHub auto-disables `schedule:` triggers on repos with no commits in 60
  days. The included `.github/workflows/keepalive.yml` makes a trivial
  monthly commit so this never silently stops — no action needed from you,
  just don't delete that file.

## Files

| File | Purpose |
|---|---|
| `main.py` | Orchestrates fetch → summarize → continuation-match → store → email |
| `fetchers.py` | One function per source, all returning a common item shape |
| `providers.py` | Adapter classes for Anthropic/OpenAI/Google, one shared interface |
| `summarizer.py` | Rotates across configured providers, skipping ones that keep failing |
| `db.py` | SQLite storage + Jaccard-similarity continuation matching |
| `emailer.py` | Builds and sends the HTML/plain-text email |
| `digest.db` | Created on first run (SQLite path only) — your growing article history |
| `supabase_schema.sql` | Same schema, for the Postgres/Supabase path |
| `.github/workflows/daily-digest.yml` | The free scheduled runner (Option B) |
| `.github/workflows/keepalive.yml` | Stops GitHub's 60-day auto-disable from silently killing the schedule |

## Extending

- **Different delivery:** swap `emailer.py`'s `send_email` call in `main.py`
  for a Slack webhook POST or a Telegram `sendMessage` call — the digest
  data structure (`digest_articles`) stays the same either way.
- **More sources:** add a function to `fetchers.py` returning the same
  dict shape (`source`, `title`, `url`, `published`, `raw_text`), then add
  it to `ALL_FETCHERS`.
- **Smarter continuation matching:** if entity-overlap heuristics ever feel
  too loose/strict, swap `db.find_continuation`'s Jaccard scoring for
  embedding similarity (e.g. Voyage AI embeddings) — the interface
  (`entities in`, `match dict out`) doesn't need to change.
- **Cost control:** each article costs one small Claude call. At
  `MAX_ARTICLES_PER_RUN=15`/day with Claude Sonnet that's well under a
  cent/day in API cost at typical pricing — but check current pricing at
  https://docs.claude.com if you scale volume up a lot.

## Uninstall

```
crontab -l | grep -v "ai-digest-cron/main.py" | crontab -
```
