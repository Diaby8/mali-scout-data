"""
Schema de la base de donnees Mali Scout Data.
Toutes les tables et leur creation.
"""

SCHEMA = """
-- Joueurs : infos de base
CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    fbref_id TEXT UNIQUE,
    fbref_url TEXT,
    transfermarkt_url TEXT,
    sofascore_id TEXT,
    birth_year INTEGER,
    birth_date TEXT,
    position TEXT,
    detailed_position TEXT,
    current_club TEXT,
    current_league TEXT,
    nationality TEXT DEFAULT 'Mali',
    second_nationality TEXT,
    foot TEXT,
    height_cm INTEGER,
    market_value TEXT,
    contract_until TEXT,
    category TEXT DEFAULT 'senior',
    photo_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Categories de joueurs (pour organiser et filtrer)
CREATE TABLE IF NOT EXISTS player_categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL,
    category TEXT NOT NULL,
    FOREIGN KEY (player_id) REFERENCES players(id),
    UNIQUE(player_id, category)
);
-- Categories possibles:
-- 'europe_top5' : joue dans un top 5 ligue europeenne
-- 'europe_other' : joue en Europe hors top 5
-- 'mali_ligue1' : joue en Ligue 1 malienne
-- 'afrique' : joue dans un autre pays africain
-- 'national_team' : selectionne en equipe nationale A
-- 'u23' : equipe nationale U23 / Espoirs
-- 'u20' : equipe nationale U20
-- 'prospect' : jeune talent a suivre
-- 'diaspora' : ne en France/Europe, eligible Mali

-- Stats par saison (standard)
CREATE TABLE IF NOT EXISTS season_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL,
    season TEXT NOT NULL,
    club TEXT,
    league TEXT,
    age INTEGER,
    matches_played INTEGER DEFAULT 0,
    starts INTEGER DEFAULT 0,
    minutes INTEGER DEFAULT 0,
    goals INTEGER DEFAULT 0,
    assists INTEGER DEFAULT 0,
    goals_pens INTEGER DEFAULT 0,
    pens_made INTEGER DEFAULT 0,
    pens_att INTEGER DEFAULT 0,
    yellow_cards INTEGER DEFAULT 0,
    red_cards INTEGER DEFAULT 0,
    xg REAL,
    xag REAL,
    progressive_carries INTEGER,
    progressive_passes INTEGER,
    progressive_receives INTEGER,
    goals_per90 REAL,
    assists_per90 REAL,
    xg_per90 REAL,
    xag_per90 REAL,
    source TEXT DEFAULT 'fbref',
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (player_id) REFERENCES players(id),
    UNIQUE(player_id, season, club)
);

-- Stats de tir
CREATE TABLE IF NOT EXISTS shooting_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL,
    season TEXT NOT NULL,
    club TEXT,
    shots_total INTEGER,
    shots_on_target INTEGER,
    shots_on_target_pct REAL,
    shots_per90 REAL,
    goals_per_shot REAL,
    avg_shot_distance REAL,
    shots_free_kicks INTEGER,
    xg REAL,
    npxg REAL,
    npxg_per_shot REAL,
    xg_net REAL,
    source TEXT DEFAULT 'fbref',
    FOREIGN KEY (player_id) REFERENCES players(id),
    UNIQUE(player_id, season, club)
);

-- Stats de passes
CREATE TABLE IF NOT EXISTS passing_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL,
    season TEXT NOT NULL,
    club TEXT,
    passes_completed INTEGER,
    passes_attempted INTEGER,
    pass_completion_pct REAL,
    passes_total_distance INTEGER,
    passes_progressive_distance INTEGER,
    short_passes_completed INTEGER,
    short_passes_attempted INTEGER,
    medium_passes_completed INTEGER,
    medium_passes_attempted INTEGER,
    long_passes_completed INTEGER,
    long_passes_attempted INTEGER,
    key_passes INTEGER,
    passes_into_final_third INTEGER,
    passes_into_penalty_area INTEGER,
    crosses_into_penalty_area INTEGER,
    progressive_passes INTEGER,
    source TEXT DEFAULT 'fbref',
    FOREIGN KEY (player_id) REFERENCES players(id),
    UNIQUE(player_id, season, club)
);

-- Stats defensives
CREATE TABLE IF NOT EXISTS defense_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL,
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
    clearances INTEGER,
    errors INTEGER,
    source TEXT DEFAULT 'fbref',
    FOREIGN KEY (player_id) REFERENCES players(id),
    UNIQUE(player_id, season, club)
);

-- Infos mercato / transferts
CREATE TABLE IF NOT EXISTS transfers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL,
    season TEXT,
    date TEXT,
    club_from TEXT,
    club_to TEXT,
    transfer_fee TEXT,
    market_value TEXT,
    source TEXT DEFAULT 'manual',
    FOREIGN KEY (player_id) REFERENCES players(id)
);

-- Equipe nationale : convocations / matchs
CREATE TABLE IF NOT EXISTS national_team (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL,
    season TEXT,
    competition TEXT,
    matches INTEGER DEFAULT 0,
    goals INTEGER DEFAULT 0,
    assists INTEGER DEFAULT 0,
    minutes INTEGER DEFAULT 0,
    source TEXT DEFAULT 'fbref',
    FOREIGN KEY (player_id) REFERENCES players(id),
    UNIQUE(player_id, season, competition)
);

-- Stats de match (pour le suivi des performances recentes)
CREATE TABLE IF NOT EXISTS match_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    competition TEXT,
    opponent TEXT,
    home_away TEXT,
    result TEXT,
    minutes_played INTEGER,
    goals INTEGER DEFAULT 0,
    assists INTEGER DEFAULT 0,
    shots INTEGER,
    shots_on_target INTEGER,
    passes_completed INTEGER,
    passes_attempted INTEGER,
    key_passes INTEGER,
    tackles INTEGER,
    interceptions INTEGER,
    dribbles_completed INTEGER,
    dribbles_attempted INTEGER,
    fouls_committed INTEGER,
    fouls_drawn INTEGER,
    yellow_card INTEGER DEFAULT 0,
    red_card INTEGER DEFAULT 0,
    rating REAL,
    source TEXT DEFAULT 'manual',
    FOREIGN KEY (player_id) REFERENCES players(id),
    UNIQUE(player_id, date, opponent)
);

-- Suivi des valeurs marchandes dans le temps
CREATE TABLE IF NOT EXISTS market_value_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    value_euros INTEGER,
    source TEXT DEFAULT 'transfermarkt',
    FOREIGN KEY (player_id) REFERENCES players(id)
);

-- Index pour les recherches rapides
CREATE INDEX IF NOT EXISTS idx_players_name ON players(name);
CREATE INDEX IF NOT EXISTS idx_players_club ON players(current_club);
CREATE INDEX IF NOT EXISTS idx_players_category ON players(category);
CREATE INDEX IF NOT EXISTS idx_player_categories ON player_categories(category);
CREATE INDEX IF NOT EXISTS idx_season_stats_player ON season_stats(player_id);
CREATE INDEX IF NOT EXISTS idx_season_stats_season ON season_stats(season);
CREATE INDEX IF NOT EXISTS idx_match_stats_player ON match_stats(player_id);
CREATE INDEX IF NOT EXISTS idx_match_stats_date ON match_stats(date);
"""
