-- Correction des vues pour filtrer par saison proprement

-- Vue : top buteurs (avec saison obligatoire)
CREATE OR REPLACE VIEW v_top_scorers AS
SELECT p.name, p.position, p.current_club, p.current_league, s.season,
       s.goals, s.assists,
       s.goals + s.assists AS goal_contributions,
       s.minutes, s.xg, s.goals_per90, s.matches_played, s.starts
FROM season_stats s
JOIN players p ON p.id = s.player_id
WHERE p.status != 'retired'
ORDER BY s.season DESC, s.goals DESC;

-- Vue : top passeurs
CREATE OR REPLACE VIEW v_top_assisters AS
SELECT p.name, p.position, p.current_club, p.current_league, s.season,
       s.assists, s.xag, s.assists_per90, s.minutes, s.matches_played, s.starts
FROM season_stats s
JOIN players p ON p.id = s.player_id
WHERE p.status != 'retired'
ORDER BY s.season DESC, s.assists DESC;

-- Vue : top contributions (buts + passes)
CREATE OR REPLACE VIEW v_top_contributors AS
SELECT p.name, p.position, p.current_club, p.current_league, s.season,
       s.goals, s.assists,
       s.goals + s.assists AS goal_contributions,
       s.goals_assists_per90,
       s.minutes, s.xg, s.xag, s.matches_played
FROM season_stats s
JOIN players p ON p.id = s.player_id
WHERE p.status != 'retired'
ORDER BY s.season DESC, (s.goals + s.assists) DESC;

-- Vue : resume joueur (corrigee)
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
WHERE p.status != 'retired'
GROUP BY p.id, p.name, p.position, p.detailed_position,
         p.current_club, p.current_league, p.age,
         p.nationality, p.second_nationality,
         p.height_cm, p.foot, p.market_value_display, p.status
ORDER BY total_goals DESC;

-- Vue : saisons disponibles
CREATE OR REPLACE VIEW v_available_seasons AS
SELECT DISTINCT season, COUNT(*) as nb_players
FROM season_stats
GROUP BY season
ORDER BY season DESC;
