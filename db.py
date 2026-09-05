"""
Storage for the AI digest, supporting both SQLite and Supabase/PostgreSQL.

Features:
  - Rolling 7-day retention: cleanup_older_than(days=7)
  - Rich developer-focused metadata storage (impact scores, categories, images)
  - Cross-day continuation tracking via entity matching
"""

import sqlite3
import json
from datetime import datetime, timedelta, timezone
from contextlib import contextmanager


def get_db(database_url, sqlite_path):
    """Factory: returns PostgresDigestDB if database_url is provided, else SQLiteDigestDB."""
    if database_url:
        return PostgresDigestDB(database_url)
    return SQLiteDigestDB(sqlite_path)


class SQLiteDigestDB:
    SCHEMA = """
    CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source TEXT NOT NULL,
        title TEXT NOT NULL,
        url TEXT NOT NULL UNIQUE,
        published_date TEXT,
        fetched_at TEXT NOT NULL,
        summary TEXT,
        dev_use_case TEXT,
        one_liner TEXT,
        category TEXT,
        category_tag TEXT,
        dev_impact_score INTEGER DEFAULT 75,
        is_groundbreaking INTEGER DEFAULT 0,
        image_url TEXT,
        entities TEXT,
        parent_id INTEGER,
        sent_at TEXT,
        FOREIGN KEY (parent_id) REFERENCES articles (id)
    );
    CREATE INDEX IF NOT EXISTS idx_articles_published_date ON articles (published_date);
    CREATE INDEX IF NOT EXISTS idx_articles_fetched_at ON articles (fetched_at);
    """

    def __init__(self, db_path):
        self.db_path = db_path
        with self._conn() as conn:
            conn.executescript(self.SCHEMA)
            # Run lightweight migration for existing DBs if columns are missing
            for col, col_type in [
                ("dev_use_case", "TEXT"),
                ("one_liner", "TEXT"),
                ("category", "TEXT"),
                ("category_tag", "TEXT"),
                ("dev_impact_score", "INTEGER DEFAULT 75"),
                ("is_groundbreaking", "INTEGER DEFAULT 0"),
                ("image_url", "TEXT"),
            ]:
                try:
                    conn.execute(f"ALTER TABLE articles ADD COLUMN {col} {col_type};")
                except sqlite3.OperationalError:
                    pass  # column already exists

    @contextmanager
    def _conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def url_exists(self, url):
        with self._conn() as conn:
            row = conn.execute("SELECT 1 FROM articles WHERE url = ?", (url,)).fetchone()
            return row is not None

    def filter_unseen_urls(self, urls):
        """Batch-check hundreds of URLs in single query chunks."""
        if not urls:
            return set()
        url_list = list(urls)
        existing = set()
        with self._conn() as conn:
            for i in range(0, len(url_list), 500):
                chunk = url_list[i:i+500]
                placeholders = ",".join("?" for _ in chunk)
                rows = conn.execute(f"SELECT url FROM articles WHERE url IN ({placeholders})", chunk).fetchall()
                for r in rows:
                    existing.add(r[0])
        return set(urls) - existing

    def cleanup_older_than(self, days=7):
        """Purge articles older than N days to maintain strict rolling retention."""
        cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
        with self._conn() as conn:
            cur = conn.execute("DELETE FROM articles WHERE published_date < ?", (cutoff,))
            count = cur.rowcount
        print(f"[db] Pruned {count} articles older than {days} days.")
        return count

    def get_all_recent_articles(self, days=7):
        cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT * FROM articles WHERE published_date >= ? ORDER BY published_date DESC, dev_impact_score DESC",
                (cutoff,)
            ).fetchall()
            return [dict(r) for r in rows]

    def _recent_entity_index(self, days):
        cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT id, title, url, published_date, entities FROM articles "
                "WHERE published_date >= ?",
                (cutoff,),
            ).fetchall()
        result = []
        for r in rows:
            try:
                ents = set(e.lower() for e in json.loads(r["entities"] or "[]"))
            except (json.JSONDecodeError, TypeError):
                ents = set()
            if ents:
                result.append((r["id"], r["title"], r["url"], r["published_date"], ents))
        return result

    def find_continuation(self, entities, days=7, threshold=0.25):
        return _best_match(entities, self._recent_entity_index(days), threshold)

    def insert_article(self, source, title, url, published_date, summary,
                       entities, parent_id=None, mark_sent=True,
                       category=None, category_tag=None, dev_impact_score=75,
                       is_groundbreaking=False, image_url=None,
                       dev_use_case=None, one_liner=None):
        now = datetime.now(timezone.utc).isoformat()
        with self._conn() as conn:
            cur = conn.execute(
                """INSERT INTO articles
                   (source, title, url, published_date, fetched_at, summary,
                    dev_use_case, one_liner, category, category_tag,
                    dev_impact_score, is_groundbreaking, image_url,
                    entities, parent_id, sent_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (source, title, url, published_date, now, summary,
                 dev_use_case, one_liner, category, category_tag,
                 dev_impact_score, 1 if is_groundbreaking else 0, image_url,
                 json.dumps(entities), parent_id, now if mark_sent else None),
            )
            return cur.lastrowid

    def purge_all_articles(self):
        """Purge all articles for a clean database reset."""
        with self._conn() as conn:
            conn.execute("DELETE FROM articles;")
            conn.commit()

    def get_articles_by_day(self, day_iso_str):
        """Retrieve all articles published on a specific YYYY-MM-DD."""
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT * FROM articles WHERE substr(published_date, 1, 10) = ? "
                "ORDER BY is_groundbreaking DESC, dev_impact_score DESC",
                (day_iso_str,),
            ).fetchall()
            return [dict(r) for r in rows]


class PostgresDigestDB:
    SCHEMA = """
    CREATE TABLE IF NOT EXISTS articles (
        id SERIAL PRIMARY KEY,
        source TEXT NOT NULL,
        title TEXT NOT NULL,
        url TEXT NOT NULL UNIQUE,
        published_date TIMESTAMPTZ NOT NULL,
        fetched_at TIMESTAMPTZ NOT NULL DEFAULT now(),
        summary TEXT,
        dev_use_case TEXT,
        one_liner TEXT,
        category TEXT DEFAULT '🔬 Applied Research',
        category_tag TEXT DEFAULT 'RESEARCH',
        dev_impact_score INTEGER DEFAULT 75,
        is_groundbreaking BOOLEAN DEFAULT false,
        image_url TEXT,
        entities JSONB DEFAULT '[]'::jsonb,
        parent_id INTEGER REFERENCES articles (id) ON DELETE SET NULL,
        sent_at TIMESTAMPTZ
    );
    CREATE INDEX IF NOT EXISTS idx_articles_published_date ON articles (published_date DESC);
    CREATE INDEX IF NOT EXISTS idx_articles_fetched_at ON articles (fetched_at DESC);
    CREATE INDEX IF NOT EXISTS idx_articles_entities_gin ON articles USING gin (entities);
    """

    def __init__(self, database_url):
        import psycopg2
        self._psycopg2 = psycopg2
        self.database_url = database_url
        self._connection = None
        with self._conn() as conn, conn.cursor() as cur:
            cur.execute(self.SCHEMA)
            # Add columns if migrating an older database
            for col, col_type in [
                ("dev_use_case", "TEXT"),
                ("one_liner", "TEXT"),
                ("category", "TEXT DEFAULT '🔬 Applied Research'"),
                ("category_tag", "TEXT DEFAULT 'RESEARCH'"),
                ("dev_impact_score", "INTEGER DEFAULT 75"),
                ("is_groundbreaking", "BOOLEAN DEFAULT false"),
                ("image_url", "TEXT"),
            ]:
                try:
                    cur.execute(f"ALTER TABLE articles ADD COLUMN IF NOT EXISTS {col} {col_type};")
                except Exception:
                    conn.rollback()
            conn.commit()

    @contextmanager
    def _conn(self):
        if self._connection is None or self._connection.closed:
            self._connection = self._psycopg2.connect(self.database_url)
        try:
            yield self._connection
        except Exception:
            if self._connection and not self._connection.closed:
                self._connection.rollback()
            raise

    def url_exists(self, url):
        with self._conn() as conn, conn.cursor() as cur:
            cur.execute("SELECT 1 FROM articles WHERE url = %s", (url,))
            return cur.fetchone() is not None

    def filter_unseen_urls(self, urls):
        """Batch-check hundreds of URLs in a single roundtrip query."""
        if not urls:
            return set()
        with self._conn() as conn, conn.cursor() as cur:
            cur.execute("SELECT url FROM articles WHERE url = ANY(%s)", (list(urls),))
            existing = {r[0] for r in cur.fetchall()}
            return set(urls) - existing

    def cleanup_older_than(self, days=7):
        """Delete articles older than N days to maintain strict rolling retention."""
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        with self._conn() as conn, conn.cursor() as cur:
            cur.execute("DELETE FROM articles WHERE published_date < %s", (cutoff,))
            count = cur.rowcount
            conn.commit()
        print(f"[db] Supabase: Pruned {count} articles older than {days} days.")
        return count

    def get_all_recent_articles(self, days=7):
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        with self._conn() as conn, conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM articles WHERE published_date >= %s ORDER BY published_date DESC, dev_impact_score DESC",
                (cutoff,)
            )
            cols = [desc[0] for desc in cur.description]
            return [dict(zip(cols, row)) for row in cur.fetchall()]

    def _recent_entity_index(self, days=7):
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        with self._conn() as conn, conn.cursor() as cur:
            cur.execute(
                "SELECT id, title, url, published_date, entities FROM articles "
                "WHERE published_date >= %s",
                (cutoff,),
            )
            rows = cur.fetchall()
        result = []
        for (aid, title, url, published_date, entities) in rows:
            ents = set(e.lower() for e in (entities or []))
            if ents:
                pub_str = published_date.isoformat() if published_date else None
                result.append((aid, title, url, pub_str, ents))
        return result

    def find_continuation(self, entities, days=7, threshold=0.25):
        return _best_match(entities, self._recent_entity_index(days), threshold)

    def insert_article(self, source, title, url, published_date, summary,
                       entities, parent_id=None, mark_sent=True,
                       category=None, category_tag=None, dev_impact_score=75,
                       is_groundbreaking=False, image_url=None,
                       dev_use_case=None, one_liner=None):
        from psycopg2.extras import Json
        now = datetime.now(timezone.utc)
        with self._conn() as conn, conn.cursor() as cur:
            cur.execute(
                """INSERT INTO articles
                   (source, title, url, published_date, fetched_at, summary,
                    dev_use_case, one_liner, category, category_tag,
                    dev_impact_score, is_groundbreaking, image_url,
                    entities, parent_id, sent_at)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                   ON CONFLICT (url) DO NOTHING
                   RETURNING id""",
                (source, title, url, published_date, now, summary,
                 dev_use_case, one_liner, category, category_tag,
                 dev_impact_score, is_groundbreaking, image_url,
                 Json(entities), parent_id, now if mark_sent else None),
            )
            row = cur.fetchone()
            conn.commit()
            return row[0] if row else None

    def purge_all_articles(self):
        """Purge all articles for a clean database reset."""
        with self._conn() as conn, conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE articles RESTART IDENTITY CASCADE;")
            conn.commit()
        print("[db] Supabase: Truncated articles table.")

    def get_articles_by_day(self, day_iso_str):
        """Retrieve all articles published on a specific YYYY-MM-DD."""
        with self._conn() as conn, conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM articles WHERE published_date::text LIKE %s "
                "ORDER BY is_groundbreaking DESC, dev_impact_score DESC",
                (f"{day_iso_str}%",),
            )
            cols = [desc[0] for desc in cur.description]
            return [dict(zip(cols, row)) for row in cur.fetchall()]


def _best_match(entities, index, threshold):
    candidate_set = set(e.lower() for e in entities)
    if not candidate_set:
        return None
    best = None
    for aid, title, url, published_date, ents in index:
        overlap = candidate_set & ents
        union = candidate_set | ents
        score = len(overlap) / len(union) if union else 0.0
        if score >= threshold and (best is None or score > best["score"]):
            best = {"id": aid, "title": title, "url": url,
                    "published_date": published_date, "score": score}
    return best


def export_db_to_seed(db, output_file="seed_7days.json"):
    """Export recent database articles directly to seed_7days.json so static builds match live DB."""
    rows = db.get_all_recent_articles(days=7)
    grouped = {}
    for r in rows:
        p_date = r.get("published_date")
        if not p_date:
            continue
        if isinstance(p_date, datetime):
            d_str = p_date.strftime("%Y-%m-%d")
        else:
            d_str = str(p_date)[:10]

        if d_str not in grouped:
            try:
                dt_obj = datetime.strptime(d_str, "%Y-%m-%d")
                day_name = dt_obj.strftime("%a, %b %d")
            except Exception:
                day_name = d_str
            grouped[d_str] = {
                "date": d_str,
                "day_name": day_name,
                "highlights": [],
                "top_10": [],
                "one_liners": []
            }

        entities_val = r.get("entities")
        if isinstance(entities_val, str):
            try:
                entities_val = json.loads(entities_val)
            except Exception:
                entities_val = []
        elif not isinstance(entities_val, list):
            entities_val = []

        art = {
            "source": r.get("source"),
            "title": r.get("title"),
            "url": r.get("url"),
            "published": str(r.get("published_date")),
            "summary": r.get("summary"),
            "dev_use_case": r.get("dev_use_case"),
            "one_liner": r.get("one_liner"),
            "category": r.get("category"),
            "category_tag": r.get("category_tag"),
            "dev_impact_score": r.get("dev_impact_score", 75),
            "is_groundbreaking": bool(r.get("is_groundbreaking")),
            "entities": entities_val,
            "image_url": r.get("image_url")
        }
        if art["is_groundbreaking"] or len(grouped[d_str]["top_10"]) < 10:
            grouped[d_str]["top_10"].append(art)
        else:
            grouped[d_str]["one_liners"].append(art)

    # Generate executive highlights for each date
    from ranker import generate_executive_highlights
    for d_str, day_data in grouped.items():
        all_day_items = day_data["top_10"] + day_data["one_liners"]
        day_data["highlights"] = generate_executive_highlights(all_day_items)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(grouped, f, indent=2)
    print(f"[export] Successfully exported {len(rows)} articles across {len(grouped)} dates to {output_file}")
    return grouped
