-- Supabase Schema for AI Engineering Digest Web App
-- Run this in the Supabase SQL Editor (Dashboard -> SQL Editor -> New Query)

-- 1. Create articles table with developer-impact & categorization fields
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
    sent_at TIMESTAMPTZ,
    content_type TEXT DEFAULT 'article',
    week_id TEXT,
    week_label TEXT,
    video_id TEXT
);

-- 2. Indexes for fast calendar & weekly querying and continuation tracking
CREATE INDEX IF NOT EXISTS idx_articles_published_date ON articles (published_date DESC);
CREATE INDEX IF NOT EXISTS idx_articles_fetched_at ON articles (fetched_at DESC);
CREATE INDEX IF NOT EXISTS idx_articles_category ON articles (category_tag);
CREATE INDEX IF NOT EXISTS idx_articles_groundbreaking ON articles (is_groundbreaking);
CREATE INDEX IF NOT EXISTS idx_articles_content_type ON articles (content_type);
CREATE INDEX IF NOT EXISTS idx_articles_week_id ON articles (week_id);

-- GIN index for fast JSONB entity intersection matching (continuation linking)
CREATE INDEX IF NOT EXISTS idx_articles_entities_gin ON articles USING gin (entities);

-- 3. Row Level Security (RLS)
-- Enables public anonymous read access so the Vercel frontend can query articles via Supabase Anon Key
ALTER TABLE articles ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Allow anonymous read access" ON articles;
CREATE POLICY "Allow anonymous read access"
    ON articles FOR SELECT
    TO anon, authenticated
    USING (true);

-- 4. Automatic 28-day retention cleanup function (4 full rolling weeks)
CREATE OR REPLACE FUNCTION purge_articles_older_than_28_days()
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM articles
    WHERE published_date < (NOW() - INTERVAL '28 days');
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- 5. Helper view for frontend past 4 weeks feed
CREATE OR REPLACE VIEW recent_4_weeks_articles AS
SELECT 
    id,
    source,
    title,
    url,
    published_date,
    DATE(published_date AT TIME ZONE 'UTC') AS published_day,
    summary,
    dev_use_case,
    one_liner,
    category,
    category_tag,
    dev_impact_score,
    is_groundbreaking,
    image_url,
    entities,
    parent_id,
    content_type,
    week_id,
    week_label,
    video_id
FROM articles
WHERE published_date >= (NOW() - INTERVAL '28 days')
ORDER BY is_groundbreaking DESC, dev_impact_score DESC, published_date DESC;

-- Backward-compatibility view alias
CREATE OR REPLACE VIEW recent_7_days_articles AS
SELECT * FROM recent_4_weeks_articles;
