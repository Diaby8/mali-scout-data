"""
Operations sur la base de donnees Mali Scout Data.
"""

import sqlite3
import os
from contextlib import contextmanager

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import DB_PATH, DATA_DIR
from database.models import SCHEMA


def init_db():
    """Cree la base et toutes les tables."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with get_conn() as conn:
        conn.executescript(SCHEMA)
    print(f"Base de donnees initialisee: {DB_PATH}")


@contextmanager
def get_conn():
    """Context manager pour la connexion SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


# --- PLAYERS ---

def upsert_player(name, fbref_id=None, fbref_url=None, birth_year=None,
                   position=None, current_club=None, current_league=None,
                   category=None, detailed_position=None, foot=None,
                   height_cm=None, market_value=None, photo_url=None):
    """Insere ou met a jour un joueur."""
    with get_conn() as conn:
        existing = None
        if fbref_id:
            existing = conn.execute(
                "SELECT id FROM players WHERE fbref_id = ?", (fbref_id,)
            ).fetchone()
        if not existing:
            existing = conn.execute(
                "SELECT id FROM players WHERE name = ?", (name,)
            ).fetchone()

        if existing:
            conn.execute("""
                UPDATE players SET
                    fbref_id = COALESCE(?, fbref_id),
                    fbref_url = COALESCE(?, fbref_url),
                    birth_year = COALESCE(?, birth_year),
                    position = COALESCE(?, position),
                    detailed_position = COALESCE(?, detailed_position),
                    current_club = COALESCE(?, current_club),
                    current_league = COALESCE(?, current_league),
                    category = COALESCE(?, category),
                    foot = COALESCE(?, foot),
                    height_cm = COALESCE(?, height_cm),
                    market_value = COALESCE(?, market_value),
                    photo_url = COALESCE(?, photo_url),
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (fbref_id, fbref_url, birth_year, position,
                  detailed_position, current_club, current_league,
                  category, foot, height_cm, market_value, photo_url,
                  existing["id"]))
            return existing["id"]
        else:
            cursor = conn.execute("""
                INSERT INTO players (name, fbref_id, fbref_url, birth_year,
                    position, detailed_position, current_club, current_league,
                    category, foot, height_cm, market_value, photo_url)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (name, fbref_id, fbref_url, birth_year,
                  position, detailed_position, current_club, current_league,
                  category, foot, height_cm, market_value, photo_url))
            return cursor.lastrowid


def get_all_players():
    """Retourne tous les joueurs."""
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM players ORDER BY name"
        ).fetchall()
        return [dict(r) for r in rows]


def get_player_by_name(name):
    """Recherche un joueur par nom (recherche partielle)."""
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM players WHERE name LIKE ?", (f"%{name}%",)
        ).fetchall()
        return [dict(r) for r in rows]


def get_player_by_id(player_id):
    """Retourne un joueur par son ID."""
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM players WHERE id = ?", (player_id,)
        ).fetchone()
        return dict(row) if row else None


# --- SEASON STATS ---

def upsert_season_stats(player_id, season, club=None, **stats):
    """Insere ou met a jour les stats d'une saison."""
    with get_conn() as conn:
        existing = conn.execute(
            "SELECT id FROM season_stats WHERE player_id = ? AND season = ? AND club = ?",
            (player_id, season, club)
        ).fetchone()

        columns = ["player_id", "season", "club"] + list(stats.keys())
        values = [player_id, season, club] + list(stats.values())

        if existing:
            set_clause = ", ".join(f"{k} = ?" for k in stats.keys())
            conn.execute(
                f"UPDATE season_stats SET {set_clause} WHERE id = ?",
                list(stats.values()) + [existing["id"]]
            )
        else:
            placeholders = ", ".join(["?"] * len(values))
            cols = ", ".join(columns)
            conn.execute(
                f"INSERT INTO season_stats ({cols}) VALUES ({placeholders})",
                values
            )


def get_player_stats(player_id):
    """Retourne toutes les stats d'un joueur."""
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM season_stats WHERE player_id = ? ORDER BY season DESC",
            (player_id,)
        ).fetchall()
        return [dict(r) for r in rows]


def get_latest_stats():
    """Retourne les dernieres stats de chaque joueur."""
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT p.name, p.position, p.current_club, s.*
            FROM season_stats s
            JOIN players p ON p.id = s.player_id
            WHERE s.season = (
                SELECT MAX(s2.season) FROM season_stats s2
                WHERE s2.player_id = s.player_id
            )
            ORDER BY p.name
        """).fetchall()
        return [dict(r) for r in rows]


# --- SHOOTING STATS ---

def upsert_shooting_stats(player_id, season, club=None, **stats):
    """Insere ou met a jour les stats de tir."""
    with get_conn() as conn:
        existing = conn.execute(
            "SELECT id FROM shooting_stats WHERE player_id = ? AND season = ? AND club = ?",
            (player_id, season, club)
        ).fetchone()

        columns = ["player_id", "season", "club"] + list(stats.keys())
        values = [player_id, season, club] + list(stats.values())

        if existing:
            set_clause = ", ".join(f"{k} = ?" for k in stats.keys())
            conn.execute(
                f"UPDATE shooting_stats SET {set_clause} WHERE id = ?",
                list(stats.values()) + [existing["id"]]
            )
        else:
            placeholders = ", ".join(["?"] * len(values))
            cols = ", ".join(columns)
            conn.execute(
                f"INSERT INTO shooting_stats ({cols}) VALUES ({placeholders})",
                values
            )


# --- PASSING STATS ---

def upsert_passing_stats(player_id, season, club=None, **stats):
    """Insere ou met a jour les stats de passes."""
    with get_conn() as conn:
        existing = conn.execute(
            "SELECT id FROM passing_stats WHERE player_id = ? AND season = ? AND club = ?",
            (player_id, season, club)
        ).fetchone()

        columns = ["player_id", "season", "club"] + list(stats.keys())
        values = [player_id, season, club] + list(stats.values())

        if existing:
            set_clause = ", ".join(f"{k} = ?" for k in stats.keys())
            conn.execute(
                f"UPDATE passing_stats SET {set_clause} WHERE id = ?",
                list(stats.values()) + [existing["id"]]
            )
        else:
            placeholders = ", ".join(["?"] * len(values))
            cols = ", ".join(columns)
            conn.execute(
                f"INSERT INTO passing_stats ({cols}) VALUES ({placeholders})",
                values
            )


# --- DEFENSE STATS ---

def upsert_defense_stats(player_id, season, club=None, **stats):
    """Insere ou met a jour les stats defensives."""
    with get_conn() as conn:
        existing = conn.execute(
            "SELECT id FROM defense_stats WHERE player_id = ? AND season = ? AND club = ?",
            (player_id, season, club)
        ).fetchone()

        columns = ["player_id", "season", "club"] + list(stats.keys())
        values = [player_id, season, club] + list(stats.values())

        if existing:
            set_clause = ", ".join(f"{k} = ?" for k in stats.keys())
            conn.execute(
                f"UPDATE defense_stats SET {set_clause} WHERE id = ?",
                list(stats.values()) + [existing["id"]]
            )
        else:
            placeholders = ", ".join(["?"] * len(values))
            cols = ", ".join(columns)
            conn.execute(
                f"INSERT INTO defense_stats ({cols}) VALUES ({placeholders})",
                values
            )


# --- STATS COMBINÉES ---

def get_player_full_profile(player_id):
    """Retourne le profil complet d'un joueur avec toutes ses stats."""
    player = get_player_by_id(player_id)
    if not player:
        return None

    with get_conn() as conn:
        season = conn.execute(
            "SELECT * FROM season_stats WHERE player_id = ? ORDER BY season DESC",
            (player_id,)
        ).fetchall()

        shooting = conn.execute(
            "SELECT * FROM shooting_stats WHERE player_id = ? ORDER BY season DESC",
            (player_id,)
        ).fetchall()

        passing = conn.execute(
            "SELECT * FROM passing_stats WHERE player_id = ? ORDER BY season DESC",
            (player_id,)
        ).fetchall()

        defense = conn.execute(
            "SELECT * FROM defense_stats WHERE player_id = ? ORDER BY season DESC",
            (player_id,)
        ).fetchall()

    player["season_stats"] = [dict(r) for r in season]
    player["shooting_stats"] = [dict(r) for r in shooting]
    player["passing_stats"] = [dict(r) for r in passing]
    player["defense_stats"] = [dict(r) for r in defense]
    return player


def get_db_summary():
    """Retourne un resume de la base de donnees."""
    with get_conn() as conn:
        players = conn.execute("SELECT COUNT(*) as c FROM players").fetchone()["c"]
        stats = conn.execute("SELECT COUNT(*) as c FROM season_stats").fetchone()["c"]
        shooting = conn.execute("SELECT COUNT(*) as c FROM shooting_stats").fetchone()["c"]
        passing = conn.execute("SELECT COUNT(*) as c FROM passing_stats").fetchone()["c"]
        defense = conn.execute("SELECT COUNT(*) as c FROM defense_stats").fetchone()["c"]
    return {
        "joueurs": players,
        "stats_saison": stats,
        "stats_tir": shooting,
        "stats_passes": passing,
        "stats_defense": defense,
    }


# --- CATEGORIES ---

def add_player_category(player_id, category):
    """Ajoute une categorie a un joueur."""
    with get_conn() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO player_categories (player_id, category) VALUES (?, ?)",
            (player_id, category)
        )


def get_players_by_category(category):
    """Retourne tous les joueurs d'une categorie."""
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT p.* FROM players p
            JOIN player_categories pc ON p.id = pc.player_id
            WHERE pc.category = ?
            ORDER BY p.name
        """, (category,)).fetchall()
        return [dict(r) for r in rows]


def get_player_categories(player_id):
    """Retourne les categories d'un joueur."""
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT category FROM player_categories WHERE player_id = ?",
            (player_id,)
        ).fetchall()
        return [r["category"] for r in rows]


def get_all_categories():
    """Retourne toutes les categories existantes."""
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT DISTINCT category FROM player_categories ORDER BY category"
        ).fetchall()
        return [r["category"] for r in rows]


# --- MATCH STATS ---

def add_match_stats(player_id, date, opponent, competition=None,
                    home_away=None, result=None, **stats):
    """Ajoute les stats d'un match."""
    with get_conn() as conn:
        existing = conn.execute(
            "SELECT id FROM match_stats WHERE player_id = ? AND date = ? AND opponent = ?",
            (player_id, date, opponent)
        ).fetchone()

        columns = ["player_id", "date", "opponent", "competition",
                    "home_away", "result"] + list(stats.keys())
        values = [player_id, date, opponent, competition,
                  home_away, result] + list(stats.values())

        if existing:
            set_clause = ", ".join(f"{k} = ?" for k in stats.keys())
            if set_clause:
                conn.execute(
                    f"UPDATE match_stats SET competition=?, home_away=?, result=?, {set_clause} WHERE id = ?",
                    [competition, home_away, result] + list(stats.values()) + [existing["id"]]
                )
        else:
            placeholders = ", ".join(["?"] * len(values))
            cols = ", ".join(columns)
            conn.execute(
                f"INSERT INTO match_stats ({cols}) VALUES ({placeholders})",
                values
            )


def get_player_matches(player_id, limit=20):
    """Retourne les derniers matchs d'un joueur."""
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM match_stats WHERE player_id = ? ORDER BY date DESC LIMIT ?",
            (player_id, limit)
        ).fetchall()
        return [dict(r) for r in rows]


def get_recent_performances(days=7):
    """Retourne les performances des N derniers jours."""
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT p.name, p.position, p.current_club, m.*
            FROM match_stats m
            JOIN players p ON p.id = m.player_id
            WHERE m.date >= date('now', ? || ' days')
            ORDER BY m.date DESC
        """, (f"-{days}",)).fetchall()
        return [dict(r) for r in rows]


# --- MARKET VALUE ---

def add_market_value(player_id, date, value_euros, source="transfermarkt"):
    """Ajoute une valeur marchande historique."""
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO market_value_history (player_id, date, value_euros, source) VALUES (?, ?, ?, ?)",
            (player_id, date, value_euros, source)
        )


def get_market_value_history(player_id):
    """Retourne l'historique de valeur marchande d'un joueur."""
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM market_value_history WHERE player_id = ? ORDER BY date DESC",
            (player_id,)
        ).fetchall()
        return [dict(r) for r in rows]


if __name__ == "__main__":
    init_db()
    print("Tables creees avec succes.")
    print(f"Base: {DB_PATH}")
