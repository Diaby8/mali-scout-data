-- ============================================
-- HISTORIQUE DES COACHS - EQUIPE NATIONALE
-- ============================================

CREATE TABLE IF NOT EXISTS coaches_history (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    nationality TEXT,
    start_date TEXT NOT NULL,
    end_date TEXT,
    team TEXT DEFAULT 'Mali A',
    matches INTEGER DEFAULT 0,
    wins INTEGER DEFAULT 0,
    draws INTEGER DEFAULT 0,
    losses INTEGER DEFAULT 0,
    goals_for INTEGER DEFAULT 0,
    goals_against INTEGER DEFAULT 0,
    achievements TEXT,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- RLS
ALTER TABLE coaches_history ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow all" ON coaches_history FOR ALL USING (true) WITH CHECK (true);

-- Index
CREATE INDEX IF NOT EXISTS idx_coaches_start ON coaches_history(start_date);
