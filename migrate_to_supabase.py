"""
Migration des donnees SQLite vers Supabase.
Execute une seule fois apres avoir cree les tables dans Supabase.
"""

import sqlite3
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY") or os.getenv("SUPABASE_ANON_KEY")
DB_PATH = os.path.join(os.path.dirname(__file__), "data", "mali_scout.db")


def migrate():
    print("=== Migration SQLite -> Supabase ===\n")

    if not os.path.exists(DB_PATH):
        print(f"Base SQLite introuvable: {DB_PATH}")
        return

    sb = create_client(SUPABASE_URL, SUPABASE_KEY)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    # Migrer les joueurs
    players = conn.execute("SELECT * FROM players").fetchall()
    print(f"Joueurs a migrer: {len(players)}")

    migrated = 0
    for p in players:
        data = {
            "name": p["name"],
            "fbref_id": p["fbref_id"],
            "fbref_url": p["fbref_url"],
            "birth_year": p["birth_year"],
            "birth_date": p["birth_date"],
            "position": p["position"],
            "detailed_position": p["detailed_position"],
            "current_club": p["current_club"],
            "current_league": p["current_league"],
            "nationality": p["nationality"] or "Mali",
            "second_nationality": p["second_nationality"],
            "foot": None,  # pas de validation dans SQLite
            "height_cm": p["height_cm"],
            "market_value_display": p["market_value"],
            "contract_until": p["contract_until"],
            "photo_url": p["photo_url"],
            "status": "active",
        }
        # Nettoyer les None
        data = {k: v for k, v in data.items() if v is not None}

        try:
            sb.table("players").upsert(data, on_conflict="fbref_id").execute()
            migrated += 1
            print(f"  OK: {p['name']}")
        except Exception as e:
            print(f"  ERREUR {p['name']}: {e}")

    print(f"\n{migrated}/{len(players)} joueurs migres.")

    # Migrer les categories
    try:
        categories = conn.execute("SELECT * FROM player_categories").fetchall()
        if categories:
            print(f"\nCategories a migrer: {len(categories)}")
            for c in categories:
                # Trouver le nouveau player_id
                old_player = conn.execute("SELECT name FROM players WHERE id = ?", (c["player_id"],)).fetchone()
                if old_player:
                    new_player = sb.table("players").select("id").eq("name", old_player["name"]).execute()
                    if new_player.data:
                        sb.table("player_categories").upsert(
                            {"player_id": new_player.data[0]["id"], "category": c["category"]},
                            on_conflict="player_id,category"
                        ).execute()
    except Exception as e:
        print(f"Categories: {e}")

    # Migrer les stats saison
    tables_to_migrate = [
        ("season_stats", "player_id,season,club"),
        ("shooting_stats", "player_id,season,club"),
        ("passing_stats", "player_id,season,club"),
        ("defense_stats", "player_id,season,club"),
        ("match_stats", "player_id,date,opponent"),
        ("national_team", "player_id,season,competition"),
    ]

    for table, conflict_key in tables_to_migrate:
        try:
            rows = conn.execute(f"SELECT * FROM {table}").fetchall()
            if rows:
                print(f"\n{table}: {len(rows)} lignes a migrer")
                for r in rows:
                    row_data = dict(r)
                    old_pid = row_data.pop("player_id")
                    row_data.pop("id", None)

                    old_player = conn.execute("SELECT name FROM players WHERE id = ?", (old_pid,)).fetchone()
                    if old_player:
                        new_player = sb.table("players").select("id").eq("name", old_player["name"]).execute()
                        if new_player.data:
                            row_data["player_id"] = new_player.data[0]["id"]
                            row_data = {k: v for k, v in row_data.items() if v is not None}
                            sb.table(table).upsert(row_data, on_conflict=conflict_key).execute()
        except Exception as e:
            print(f"{table}: {e}")

    conn.close()
    print("\n=== Migration terminee ! ===")


if __name__ == "__main__":
    migrate()
