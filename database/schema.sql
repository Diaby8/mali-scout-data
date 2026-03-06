-- ============================================
-- MALI SCOUT DATA - Schema PostgreSQL (Supabase)
-- ============================================

-- Joueurs : infos de base
CREATE TABLE IF NOT EXISTS players (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    fbref_id TEXT UNIQUE,
    fbref_url TEXT,
    transfermarkt_url TEXT,
    sofascore_id TEXT,
    birth_date DATE,
    birth_year INTEGER,
    age INTEGER,
    position TEXT,
    detailed_position TEXT,
    current_club TEXT,
    current_league TEXT,
    nationality TEXT DEFAULT 'Mali',
    second_nationality TEXT,
    foot TEXT CHECK (foot IN ('left', 'right', 'both')),
    height_cm INTEGER,
    weight_kg INTEGER,
    market_value_euros INTEGER,
    market_value_display TEXT,
    contract_until TEXT,
    agent TEXT,
    photo_url TEXT,
    status TEXT DEFAULT 'active' CHECK (status IN ('active', 'injured', 'retired', 'inactive')),
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Categories de joueurs
CREATE TABLE IF NOT EXISTS player_categories (
    id SERIAL PRIMARY KEY,
    player_id INTEGER NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    category TEXT NOT NULL,
    UNIQUE(player_id, category)
);

-- Stats par saison (standard)
CREATE TABLE IF NOT EXISTS season_stats (
    id SERIAL PRIMARY KEY,
    player_id INTEGER NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    season TEXT NOT NULL,
    club TEXT,
    league TEXT,
    age INTEGER,
    matches_played INTEGER DEFAULT 0,
    starts INTEGER DEFAULT 0,
    minutes INTEGER DEFAULT 0,
    full_90s REAL,
    goals INTEGER DEFAULT 0,
    assists INTEGER DEFAULT 0,
    goals_assists INTEGER DEFAULT 0,
    goals_pens INTEGER DEFAULT 0,
    pens_made INTEGER DEFAULT 0,
    pens_att INTEGER DEFAULT 0,
    yellow_cards INTEGER DEFAULT 0,
    red_cards INTEGER DEFAULT 0,
    xg REAL,
    xag REAL,
    npxg REAL,
    progressive_carries INTEGER,
    progressive_passes INTEGER,
    progressive_receives INTEGER,
    goals_per90 REAL,
    assists_per90 REAL,
    goals_assists_per90 REAL,
    xg_per90 REAL,
    xag_per90 REAL,
    source TEXT DEFAULT 'fbref',
    scraped_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(player_id, season, club)
);

-- Stats de tir
CREATE TABLE IF NOT EXISTS shooting_stats (
    id SERIAL PRIMARY KEY,
    player_id INTEGER NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    season TEXT NOT NULL,
    club TEXT,
    shots_total INTEGER,
    shots_on_target INTEGER,
    shots_on_target_pct REAL,
    shots_per90 REAL,
    goals_per_shot REAL,
    goals_per_shot_on_target REAL,
    avg_shot_distance REAL,
    shots_free_kicks INTEGER,
    xg REAL,
    npxg REAL,
    npxg_per_shot REAL,
    xg_net REAL,
    npxg_net REAL,
    source TEXT DEFAULT 'fbref',
    UNIQUE(player_id, season, club)
);

-- Stats de passes
CREATE TABLE IF NOT EXISTS passing_stats (
    id SERIAL PRIMARY KEY,
    player_id INTEGER NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    season TEXT NOT NULL,
    club TEXT,
    passes_completed INTEGER,
    passes_attempted INTEGER,
    pass_completion_pct REAL,
    passes_total_distance INTEGER,
    passes_progressive_distance INTEGER,
    short_passes_completed INTEGER,
    short_passes_attempted INTEGER,
    short_pass_pct REAL,
    medium_passes_completed INTEGER,
    medium_passes_attempted INTEGER,
    medium_pass_pct REAL,
    long_passes_completed INTEGER,
    long_passes_attempted INTEGER,
    long_pass_pct REAL,
    assists INTEGER,
    xag REAL,
    xa REAL,
    key_passes INTEGER,
    passes_into_final_third INTEGER,
    passes_into_penalty_area INTEGER,
    crosses_into_penalty_area INTEGER,
    progressive_passes INTEGER,
    source TEXT DEFAULT 'fbref',
    UNIQUE(player_id, season, club)
);

-- Stats defensives
CREATE TABLE IF NOT EXISTS defense_stats (
    id SERIAL PRIMARY KEY,
    player_id INTEGER NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    season TEXT NOT NULL,
    club TEXT,
    tackles INTEGER,
    tackles_won INTEGER,
    tackles_def_3rd INTEGER,
    tackles_mid_3rd INTEGER,
    tackles_att_3rd INTEGER,
    challenges_lost INTEGER,
    blocks INTEGER,
    shots_blocked INTEGER,
    passes_blocked INTEGER,
    interceptions INTEGER,
    tackles_interceptions INTEGER,
    clearances INTEGER,
    errors INTEGER,
    source TEXT DEFAULT 'fbref',
    UNIQUE(player_id, season, club)
);

-- Stats de possession / dribble
CREATE TABLE IF NOT EXISTS possession_stats (
    id SERIAL PRIMARY KEY,
    player_id INTEGER NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    season TEXT NOT NULL,
    club TEXT,
    touches INTEGER,
    touches_def_pen INTEGER,
    touches_def_3rd INTEGER,
    touches_mid_3rd INTEGER,
    touches_att_3rd INTEGER,
    touches_att_pen INTEGER,
    take_ons_attempted INTEGER,
    take_ons_succeeded INTEGER,
    take_ons_pct REAL,
    carries INTEGER,
    carries_total_distance INTEGER,
    carries_progressive_distance INTEGER,
    progressive_carries INTEGER,
    carries_into_final_third INTEGER,
    carries_into_penalty_area INTEGER,
    miscontrols INTEGER,
    dispossessed INTEGER,
    passes_received INTEGER,
    progressive_passes_received INTEGER,
    source TEXT DEFAULT 'fbref',
    UNIQUE(player_id, season, club)
);

-- Stats gardien
CREATE TABLE IF NOT EXISTS goalkeeper_stats (
    id SERIAL PRIMARY KEY,
    player_id INTEGER NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    season TEXT NOT NULL,
    club TEXT,
    matches_played INTEGER,
    starts INTEGER,
    minutes INTEGER,
    goals_against INTEGER,
    goals_against_per90 REAL,
    shots_on_target_against INTEGER,
    saves INTEGER,
    save_pct REAL,
    wins INTEGER,
    draws INTEGER,
    losses INTEGER,
    clean_sheets INTEGER,
    clean_sheet_pct REAL,
    pens_faced INTEGER,
    pens_allowed INTEGER,
    pens_saved INTEGER,
    post_shot_xg REAL,
    psxg_net REAL,
    source TEXT DEFAULT 'fbref',
    UNIQUE(player_id, season, club)
);

-- Transferts / mercato
CREATE TABLE IF NOT EXISTS transfers (
    id SERIAL PRIMARY KEY,
    player_id INTEGER NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    season TEXT,
    date DATE,
    club_from TEXT,
    club_to TEXT,
    transfer_fee_euros INTEGER,
    transfer_fee_display TEXT,
    transfer_type TEXT CHECK (transfer_type IN ('transfer', 'loan', 'loan_return', 'free', 'youth')),
    source TEXT DEFAULT 'manual'
);

-- Equipe nationale
CREATE TABLE IF NOT EXISTS national_team (
    id SERIAL PRIMARY KEY,
    player_id INTEGER NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    team TEXT DEFAULT 'Mali A',
    season TEXT,
    competition TEXT,
    matches INTEGER DEFAULT 0,
    goals INTEGER DEFAULT 0,
    assists INTEGER DEFAULT 0,
    minutes INTEGER DEFAULT 0,
    yellow_cards INTEGER DEFAULT 0,
    red_cards INTEGER DEFAULT 0,
    source TEXT DEFAULT 'manual',
    UNIQUE(player_id, season, competition)
);

-- Stats par match (suivi performances recentes)
CREATE TABLE IF NOT EXISTS match_stats (
    id SERIAL PRIMARY KEY,
    player_id INTEGER NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    competition TEXT,
    matchday INTEGER,
    opponent TEXT,
    home_away TEXT CHECK (home_away IN ('home', 'away', 'neutral')),
    result TEXT,
    started BOOLEAN,
    minutes_played INTEGER,
    goals INTEGER DEFAULT 0,
    assists INTEGER DEFAULT 0,
    shots INTEGER,
    shots_on_target INTEGER,
    xg REAL,
    xag REAL,
    passes_completed INTEGER,
    passes_attempted INTEGER,
    key_passes INTEGER,
    tackles INTEGER,
    interceptions INTEGER,
    dribbles_completed INTEGER,
    dribbles_attempted INTEGER,
    fouls_committed INTEGER,
    fouls_drawn INTEGER,
    yellow_card BOOLEAN DEFAULT FALSE,
    red_card BOOLEAN DEFAULT FALSE,
    rating REAL,
    source TEXT DEFAULT 'manual',
    UNIQUE(player_id, date, opponent)
);

-- Historique valeur marchande
CREATE TABLE IF NOT EXISTS market_value_history (
    id SERIAL PRIMARY KEY,
    player_id INTEGER NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    value_euros INTEGER,
    source TEXT DEFAULT 'transfermarkt'
);

-- Blessures
CREATE TABLE IF NOT EXISTS injuries (
    id SERIAL PRIMARY KEY,
    player_id INTEGER NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    injury_type TEXT NOT NULL,
    start_date DATE,
    end_date DATE,
    matches_missed INTEGER,
    notes TEXT
);

-- Recompenses / distinctions
CREATE TABLE IF NOT EXISTS awards (
    id SERIAL PRIMARY KEY,
    player_id INTEGER NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    competition TEXT,
    season TEXT,
    date DATE
);

-- Logs d'import (tracer ce qui a ete importe)
CREATE TABLE IF NOT EXISTS import_logs (
    id SERIAL PRIMARY KEY,
    import_type TEXT,
    source TEXT,
    records_count INTEGER,
    status TEXT,
    details TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================
-- INDEX pour les recherches rapides
-- ============================================
CREATE INDEX IF NOT EXISTS idx_players_name ON players(name);
CREATE INDEX IF NOT EXISTS idx_players_club ON players(current_club);
CREATE INDEX IF NOT EXISTS idx_players_position ON players(position);
CREATE INDEX IF NOT EXISTS idx_players_status ON players(status);
CREATE INDEX IF NOT EXISTS idx_player_categories_cat ON player_categories(category);
CREATE INDEX IF NOT EXISTS idx_season_stats_player ON season_stats(player_id);
CREATE INDEX IF NOT EXISTS idx_season_stats_season ON season_stats(season);
CREATE INDEX IF NOT EXISTS idx_shooting_stats_player ON shooting_stats(player_id);
CREATE INDEX IF NOT EXISTS idx_passing_stats_player ON passing_stats(player_id);
CREATE INDEX IF NOT EXISTS idx_defense_stats_player ON defense_stats(player_id);
CREATE INDEX IF NOT EXISTS idx_match_stats_player ON match_stats(player_id);
CREATE INDEX IF NOT EXISTS idx_match_stats_date ON match_stats(date);
CREATE INDEX IF NOT EXISTS idx_national_team_player ON national_team(player_id);
CREATE INDEX IF NOT EXISTS idx_transfers_player ON transfers(player_id);

-- ============================================
-- FONCTION : mise a jour automatique de updated_at
-- ============================================
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER players_updated_at
    BEFORE UPDATE ON players
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();

-- ============================================
-- VUES utiles (requetes pre-faites)
-- ============================================

-- Vue : derniere saison de chaque joueur
CREATE OR REPLACE VIEW v_latest_season AS
SELECT DISTINCT ON (s.player_id)
    p.name, p.position, p.current_club, p.current_league, s.*
FROM season_stats s
JOIN players p ON p.id = s.player_id
ORDER BY s.player_id, s.season DESC;

-- Vue : top buteurs saison en cours
CREATE OR REPLACE VIEW v_top_scorers AS
SELECT p.name, p.position, p.current_club, s.season, s.goals, s.assists,
       s.goals + s.assists AS goal_contributions, s.minutes, s.xg,
       s.goals_per90, s.matches_played
FROM season_stats s
JOIN players p ON p.id = s.player_id
WHERE p.status = 'active'
ORDER BY s.goals DESC;

-- Vue : top passeurs
CREATE OR REPLACE VIEW v_top_assisters AS
SELECT p.name, p.position, p.current_club, s.season, s.assists, s.xag,
       s.assists_per90, s.minutes, s.matches_played
FROM season_stats s
JOIN players p ON p.id = s.player_id
WHERE p.status = 'active'
ORDER BY s.assists DESC;

-- Vue : resume joueur (toutes stats combinees)
CREATE OR REPLACE VIEW v_player_summary AS
SELECT
    p.id, p.name, p.position, p.detailed_position,
    p.current_club, p.current_league, p.age,
    p.nationality, p.second_nationality,
    p.height_cm, p.foot, p.market_value_display,
    p.status,
    COUNT(DISTINCT ss.season) AS seasons_tracked,
    COALESCE(SUM(ss.matches_played), 0) AS total_matches,
    COALESCE(SUM(ss.goals), 0) AS total_goals,
    COALESCE(SUM(ss.assists), 0) AS total_assists,
    COALESCE(SUM(ss.minutes), 0) AS total_minutes
FROM players p
LEFT JOIN season_stats ss ON p.id = ss.player_id
GROUP BY p.id, p.name, p.position, p.detailed_position,
         p.current_club, p.current_league, p.age,
         p.nationality, p.second_nationality,
         p.height_cm, p.foot, p.market_value_display, p.status
ORDER BY p.name;

-- ============================================
-- DISABLE RLS (projet personnel, pas besoin)
-- ============================================
ALTER TABLE players ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow all" ON players FOR ALL USING (true) WITH CHECK (true);
ALTER TABLE player_categories ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow all" ON player_categories FOR ALL USING (true) WITH CHECK (true);
ALTER TABLE season_stats ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow all" ON season_stats FOR ALL USING (true) WITH CHECK (true);
ALTER TABLE shooting_stats ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow all" ON shooting_stats FOR ALL USING (true) WITH CHECK (true);
ALTER TABLE passing_stats ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow all" ON passing_stats FOR ALL USING (true) WITH CHECK (true);
ALTER TABLE defense_stats ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow all" ON defense_stats FOR ALL USING (true) WITH CHECK (true);
ALTER TABLE possession_stats ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow all" ON possession_stats FOR ALL USING (true) WITH CHECK (true);
ALTER TABLE goalkeeper_stats ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow all" ON goalkeeper_stats FOR ALL USING (true) WITH CHECK (true);
ALTER TABLE transfers ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow all" ON transfers FOR ALL USING (true) WITH CHECK (true);
ALTER TABLE national_team ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow all" ON national_team FOR ALL USING (true) WITH CHECK (true);
ALTER TABLE match_stats ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow all" ON match_stats FOR ALL USING (true) WITH CHECK (true);
ALTER TABLE market_value_history ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow all" ON market_value_history FOR ALL USING (true) WITH CHECK (true);
ALTER TABLE injuries ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow all" ON injuries FOR ALL USING (true) WITH CHECK (true);
ALTER TABLE awards ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow all" ON awards FOR ALL USING (true) WITH CHECK (true);
ALTER TABLE import_logs ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow all" ON import_logs FOR ALL USING (true) WITH CHECK (true);
