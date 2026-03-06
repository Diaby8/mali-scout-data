-- ============================================
-- MALI SCOUT DATA - Schema Equipe Nationale
-- ============================================

-- Infos generales sur l'equipe nationale
CREATE TABLE IF NOT EXISTS national_team_info (
    id SERIAL PRIMARY KEY,
    team TEXT NOT NULL DEFAULT 'Mali A',
    coach TEXT,
    assistant_coach TEXT,
    federation TEXT DEFAULT 'FEMAFOOT',
    fifa_ranking INTEGER,
    fifa_ranking_date DATE,
    caf_ranking INTEGER,
    nickname TEXT DEFAULT 'Les Aigles',
    confederation TEXT DEFAULT 'CAF',
    captain TEXT,
    stadium TEXT,
    notes TEXT,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Matchs de l'equipe nationale (resultats)
CREATE TABLE IF NOT EXISTS national_matches (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    team TEXT DEFAULT 'Mali A',
    competition TEXT,
    round TEXT,
    venue TEXT,
    city TEXT,
    home_away TEXT CHECK (home_away IN ('home', 'away', 'neutral')),
    opponent TEXT NOT NULL,
    goals_for INTEGER NOT NULL DEFAULT 0,
    goals_against INTEGER NOT NULL DEFAULT 0,
    result TEXT CHECK (result IN ('W', 'D', 'L')),
    penalty_shootout TEXT,
    coach TEXT,
    attendance INTEGER,
    referee TEXT,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(date, opponent, team)
);

-- Convocations (liste des joueurs convoques par match/rassemblement)
CREATE TABLE IF NOT EXISTS squad_callups (
    id SERIAL PRIMARY KEY,
    player_id INTEGER NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    match_id INTEGER REFERENCES national_matches(id) ON DELETE CASCADE,
    competition TEXT,
    date DATE,
    squad_number INTEGER,
    started BOOLEAN DEFAULT FALSE,
    minutes_played INTEGER DEFAULT 0,
    goals INTEGER DEFAULT 0,
    assists INTEGER DEFAULT 0,
    yellow_card BOOLEAN DEFAULT FALSE,
    red_card BOOLEAN DEFAULT FALSE,
    rating REAL,
    notes TEXT,
    UNIQUE(player_id, match_id)
);

-- Competitions (CAN, Qualifs CM, amicaux, etc.)
CREATE TABLE IF NOT EXISTS competitions (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    short_name TEXT,
    type TEXT CHECK (type IN ('continental', 'world_cup_qualif', 'friendly', 'tournament', 'other')),
    year TEXT,
    host_country TEXT,
    mali_result TEXT,
    notes TEXT,
    UNIQUE(name, year)
);

-- Bilan par competition
CREATE TABLE IF NOT EXISTS competition_records (
    id SERIAL PRIMARY KEY,
    competition_id INTEGER REFERENCES competitions(id) ON DELETE CASCADE,
    matches_played INTEGER DEFAULT 0,
    wins INTEGER DEFAULT 0,
    draws INTEGER DEFAULT 0,
    losses INTEGER DEFAULT 0,
    goals_for INTEGER DEFAULT 0,
    goals_against INTEGER DEFAULT 0,
    notes TEXT
);

-- Index
CREATE INDEX IF NOT EXISTS idx_national_matches_date ON national_matches(date);
CREATE INDEX IF NOT EXISTS idx_national_matches_comp ON national_matches(competition);
CREATE INDEX IF NOT EXISTS idx_national_matches_opponent ON national_matches(opponent);
CREATE INDEX IF NOT EXISTS idx_squad_callups_player ON squad_callups(player_id);
CREATE INDEX IF NOT EXISTS idx_squad_callups_match ON squad_callups(match_id);

-- RLS
ALTER TABLE national_team_info ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow all" ON national_team_info FOR ALL USING (true) WITH CHECK (true);
ALTER TABLE national_matches ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow all" ON national_matches FOR ALL USING (true) WITH CHECK (true);
ALTER TABLE squad_callups ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow all" ON squad_callups FOR ALL USING (true) WITH CHECK (true);
ALTER TABLE competitions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow all" ON competitions FOR ALL USING (true) WITH CHECK (true);
ALTER TABLE competition_records ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow all" ON competition_records FOR ALL USING (true) WITH CHECK (true);

-- Vue : bilan general de l'equipe nationale
CREATE OR REPLACE VIEW v_national_team_record AS
SELECT
    team,
    COUNT(*) AS matches_played,
    SUM(CASE WHEN result = 'W' THEN 1 ELSE 0 END) AS wins,
    SUM(CASE WHEN result = 'D' THEN 1 ELSE 0 END) AS draws,
    SUM(CASE WHEN result = 'L' THEN 1 ELSE 0 END) AS losses,
    SUM(goals_for) AS total_goals_for,
    SUM(goals_against) AS total_goals_against,
    SUM(goals_for) - SUM(goals_against) AS goal_difference
FROM national_matches
GROUP BY team;

-- Vue : resultats recents
CREATE OR REPLACE VIEW v_recent_national_matches AS
SELECT * FROM national_matches
ORDER BY date DESC
LIMIT 20;

-- Vue : bilan par competition
CREATE OR REPLACE VIEW v_record_by_competition AS
SELECT
    competition,
    COUNT(*) AS matches_played,
    SUM(CASE WHEN result = 'W' THEN 1 ELSE 0 END) AS wins,
    SUM(CASE WHEN result = 'D' THEN 1 ELSE 0 END) AS draws,
    SUM(CASE WHEN result = 'L' THEN 1 ELSE 0 END) AS losses,
    SUM(goals_for) AS goals_for,
    SUM(goals_against) AS goals_against
FROM national_matches
GROUP BY competition
ORDER BY matches_played DESC;

-- Vue : bilan contre chaque adversaire
CREATE OR REPLACE VIEW v_record_by_opponent AS
SELECT
    opponent,
    COUNT(*) AS matches_played,
    SUM(CASE WHEN result = 'W' THEN 1 ELSE 0 END) AS wins,
    SUM(CASE WHEN result = 'D' THEN 1 ELSE 0 END) AS draws,
    SUM(CASE WHEN result = 'L' THEN 1 ELSE 0 END) AS losses,
    SUM(goals_for) AS goals_for,
    SUM(goals_against) AS goals_against
FROM national_matches
GROUP BY opponent
ORDER BY matches_played DESC;

-- Vue : meilleurs buteurs en selection
CREATE OR REPLACE VIEW v_national_top_scorers AS
SELECT
    p.name, p.position, p.current_club,
    SUM(sc.goals) AS total_goals,
    SUM(sc.assists) AS total_assists,
    COUNT(sc.id) AS selections,
    SUM(sc.minutes_played) AS total_minutes
FROM squad_callups sc
JOIN players p ON p.id = sc.player_id
GROUP BY p.id, p.name, p.position, p.current_club
HAVING SUM(sc.goals) > 0
ORDER BY total_goals DESC;

-- Inserer les infos de base
INSERT INTO national_team_info (team, coach, nickname, stadium, fifa_ranking, notes)
VALUES ('Mali A', 'Tom Saintfiet', 'Les Aigles', 'Stade du 26 Mars (Bamako)', 48,
        'Equipe nationale senior du Mali')
ON CONFLICT DO NOTHING;
