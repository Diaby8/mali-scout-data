"""
Operations sur la base de donnees Mali Scout Data (Supabase/PostgreSQL).
Remplace l'ancien db.py SQLite.
"""

from database.supabase_client import supabase


# ============================================
# PLAYERS
# ============================================

def add_player(name, **kwargs):
    """Ajoute un nouveau joueur."""
    data = {"name": name, **kwargs}
    result = supabase.table("players").insert(data).execute()
    return result.data[0] if result.data else None


def update_player(player_id, **kwargs):
    """Met a jour un joueur existant."""
    result = supabase.table("players").update(kwargs).eq("id", player_id).execute()
    return result.data[0] if result.data else None


def delete_player(player_id):
    """Supprime un joueur (cascade sur toutes ses stats)."""
    result = supabase.table("players").delete().eq("id", player_id).execute()
    return result.data


def get_player(player_id):
    """Retourne un joueur par ID."""
    result = supabase.table("players").select("*").eq("id", player_id).execute()
    return result.data[0] if result.data else None


def get_all_players(status=None):
    """Retourne tous les joueurs, filtre optionnel par statut."""
    query = supabase.table("players").select("*").order("name")
    if status:
        query = query.eq("status", status)
    return query.execute().data


def search_players(term):
    """Recherche un joueur par nom (partiel)."""
    result = supabase.table("players").select("*").ilike("name", f"%{term}%").order("name").execute()
    return result.data


def get_players_by_position(position):
    """Retourne les joueurs par poste."""
    result = supabase.table("players").select("*").eq("position", position).order("name").execute()
    return result.data


def get_players_by_club(club):
    """Retourne les joueurs par club."""
    result = supabase.table("players").select("*").ilike("current_club", f"%{club}%").order("name").execute()
    return result.data


def get_players_by_league(league):
    """Retourne les joueurs par ligue."""
    result = supabase.table("players").select("*").ilike("current_league", f"%{league}%").order("name").execute()
    return result.data


def upsert_player(name, fbref_id=None, **kwargs):
    """Insere ou met a jour un joueur (par fbref_id ou nom)."""
    existing = None
    if fbref_id:
        res = supabase.table("players").select("id").eq("fbref_id", fbref_id).execute()
        existing = res.data[0] if res.data else None
    if not existing:
        res = supabase.table("players").select("id").eq("name", name).execute()
        existing = res.data[0] if res.data else None

    if existing:
        return update_player(existing["id"], name=name, fbref_id=fbref_id, **kwargs)
    else:
        return add_player(name, fbref_id=fbref_id, **kwargs)


# ============================================
# CATEGORIES
# ============================================

def add_category(player_id, category):
    """Ajoute une categorie a un joueur."""
    supabase.table("player_categories").upsert(
        {"player_id": player_id, "category": category},
        on_conflict="player_id,category"
    ).execute()


def get_player_categories(player_id):
    """Retourne les categories d'un joueur."""
    result = supabase.table("player_categories").select("category").eq("player_id", player_id).execute()
    return [r["category"] for r in result.data]


def get_players_by_category(category):
    """Retourne les joueurs d'une categorie."""
    result = supabase.table("player_categories").select("player_id, players(*)").eq("category", category).execute()
    return [r["players"] for r in result.data if r.get("players")]


def get_all_categories():
    """Retourne toutes les categories."""
    result = supabase.table("player_categories").select("category").execute()
    return list(set(r["category"] for r in result.data))


# ============================================
# SEASON STATS
# ============================================

def add_season_stats(player_id, season, club=None, **stats):
    """Ajoute des stats de saison."""
    data = {"player_id": player_id, "season": season, "club": club, **stats}
    result = supabase.table("season_stats").upsert(
        data, on_conflict="player_id,season,club"
    ).execute()
    return result.data[0] if result.data else None


def get_player_season_stats(player_id):
    """Retourne toutes les stats saison d'un joueur."""
    result = supabase.table("season_stats").select("*").eq("player_id", player_id).order("season", desc=True).execute()
    return result.data


def get_latest_stats(season=None):
    """Retourne les stats de la derniere saison (ou saison specifiee)."""
    query = supabase.table("v_latest_season").select("*")
    if season:
        query = query.eq("season", season)
    return query.execute().data


def get_top_scorers(season=None, limit=10):
    """Top buteurs."""
    query = supabase.table("v_top_scorers").select("*").limit(limit)
    if season:
        query = query.eq("season", season)
    return query.execute().data


def get_top_assisters(season=None, limit=10):
    """Top passeurs."""
    query = supabase.table("v_top_assisters").select("*").limit(limit)
    if season:
        query = query.eq("season", season)
    return query.execute().data


# ============================================
# SHOOTING STATS
# ============================================

def add_shooting_stats(player_id, season, club=None, **stats):
    data = {"player_id": player_id, "season": season, "club": club, **stats}
    return supabase.table("shooting_stats").upsert(data, on_conflict="player_id,season,club").execute().data


def get_player_shooting_stats(player_id):
    return supabase.table("shooting_stats").select("*").eq("player_id", player_id).order("season", desc=True).execute().data


# ============================================
# PASSING STATS
# ============================================

def add_passing_stats(player_id, season, club=None, **stats):
    data = {"player_id": player_id, "season": season, "club": club, **stats}
    return supabase.table("passing_stats").upsert(data, on_conflict="player_id,season,club").execute().data


def get_player_passing_stats(player_id):
    return supabase.table("passing_stats").select("*").eq("player_id", player_id).order("season", desc=True).execute().data


# ============================================
# DEFENSE STATS
# ============================================

def add_defense_stats(player_id, season, club=None, **stats):
    data = {"player_id": player_id, "season": season, "club": club, **stats}
    return supabase.table("defense_stats").upsert(data, on_conflict="player_id,season,club").execute().data


def get_player_defense_stats(player_id):
    return supabase.table("defense_stats").select("*").eq("player_id", player_id).order("season", desc=True).execute().data


# ============================================
# POSSESSION STATS
# ============================================

def add_possession_stats(player_id, season, club=None, **stats):
    data = {"player_id": player_id, "season": season, "club": club, **stats}
    return supabase.table("possession_stats").upsert(data, on_conflict="player_id,season,club").execute().data


def get_player_possession_stats(player_id):
    return supabase.table("possession_stats").select("*").eq("player_id", player_id).order("season", desc=True).execute().data


# ============================================
# GOALKEEPER STATS
# ============================================

def add_goalkeeper_stats(player_id, season, club=None, **stats):
    data = {"player_id": player_id, "season": season, "club": club, **stats}
    return supabase.table("goalkeeper_stats").upsert(data, on_conflict="player_id,season,club").execute().data


def get_player_gk_stats(player_id):
    return supabase.table("goalkeeper_stats").select("*").eq("player_id", player_id).order("season", desc=True).execute().data


# ============================================
# MATCH STATS
# ============================================

def add_match_stats(player_id, date, opponent, **stats):
    data = {"player_id": player_id, "date": date, "opponent": opponent, **stats}
    return supabase.table("match_stats").upsert(data, on_conflict="player_id,date,opponent").execute().data


def get_player_matches(player_id, limit=20):
    return supabase.table("match_stats").select("*").eq("player_id", player_id).order("date", desc=True).limit(limit).execute().data


def get_recent_matches(days=7):
    from datetime import datetime, timedelta
    since = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    result = supabase.table("match_stats").select("*, players(name, position, current_club)").gte("date", since).order("date", desc=True).execute()
    return result.data


# ============================================
# TRANSFERS
# ============================================

def add_transfer(player_id, club_from, club_to, **kwargs):
    data = {"player_id": player_id, "club_from": club_from, "club_to": club_to, **kwargs}
    return supabase.table("transfers").insert(data).execute().data


def get_player_transfers(player_id):
    return supabase.table("transfers").select("*").eq("player_id", player_id).order("date", desc=True).execute().data


# ============================================
# NATIONAL TEAM
# ============================================

def add_national_team_stats(player_id, season, competition, **stats):
    data = {"player_id": player_id, "season": season, "competition": competition, **stats}
    return supabase.table("national_team").upsert(data, on_conflict="player_id,season,competition").execute().data


def get_player_national_stats(player_id):
    return supabase.table("national_team").select("*").eq("player_id", player_id).order("season", desc=True).execute().data


# ============================================
# MARKET VALUE
# ============================================

def add_market_value(player_id, date, value_euros, source="transfermarkt"):
    data = {"player_id": player_id, "date": date, "value_euros": value_euros, "source": source}
    return supabase.table("market_value_history").insert(data).execute().data


def get_market_value_history(player_id):
    return supabase.table("market_value_history").select("*").eq("player_id", player_id).order("date", desc=True).execute().data


# ============================================
# INJURIES
# ============================================

def add_injury(player_id, injury_type, start_date=None, end_date=None, **kwargs):
    data = {"player_id": player_id, "injury_type": injury_type, "start_date": start_date, "end_date": end_date, **kwargs}
    return supabase.table("injuries").insert(data).execute().data


def get_player_injuries(player_id):
    return supabase.table("injuries").select("*").eq("player_id", player_id).order("start_date", desc=True).execute().data


# ============================================
# AWARDS
# ============================================

def add_award(player_id, title, **kwargs):
    data = {"player_id": player_id, "title": title, **kwargs}
    return supabase.table("awards").insert(data).execute().data


def get_player_awards(player_id):
    return supabase.table("awards").select("*").eq("player_id", player_id).execute().data


# ============================================
# FULL PROFILE
# ============================================

def get_player_full_profile(player_id):
    """Retourne le profil complet d'un joueur avec toutes ses stats."""
    player = get_player(player_id)
    if not player:
        return None

    player["categories"] = get_player_categories(player_id)
    player["season_stats"] = get_player_season_stats(player_id)
    player["shooting_stats"] = get_player_shooting_stats(player_id)
    player["passing_stats"] = get_player_passing_stats(player_id)
    player["defense_stats"] = get_player_defense_stats(player_id)
    player["possession_stats"] = get_player_possession_stats(player_id)
    player["gk_stats"] = get_player_gk_stats(player_id)
    player["matches"] = get_player_matches(player_id)
    player["transfers"] = get_player_transfers(player_id)
    player["national_team"] = get_player_national_stats(player_id)
    player["market_values"] = get_market_value_history(player_id)
    player["injuries"] = get_player_injuries(player_id)
    player["awards"] = get_player_awards(player_id)
    return player


# ============================================
# SUMMARY / STATS GLOBALES
# ============================================

def get_db_summary():
    """Resume de la base de donnees."""
    tables = ["players", "season_stats", "shooting_stats", "passing_stats",
              "defense_stats", "possession_stats", "match_stats", "transfers",
              "national_team"]
    summary = {}
    for table in tables:
        result = supabase.table(table).select("id", count="exact").execute()
        summary[table] = result.count
    return summary


def get_player_summary():
    """Vue resume de tous les joueurs."""
    return supabase.table("v_player_summary").select("*").execute().data


# ============================================
# IMPORT LOG
# ============================================

def log_import(import_type, source, records_count, status="success", details=None):
    data = {"import_type": import_type, "source": source,
            "records_count": records_count, "status": status, "details": details}
    return supabase.table("import_logs").insert(data).execute().data


# ============================================
# EQUIPE NATIONALE
# ============================================

def get_national_team_info(team="Mali A"):
    """Infos generales sur l'equipe nationale."""
    result = supabase.table("national_team_info").select("*").eq("team", team).execute()
    return result.data[0] if result.data else None


def update_national_team_info(team="Mali A", **kwargs):
    """Met a jour les infos de l'equipe nationale."""
    return supabase.table("national_team_info").update(kwargs).eq("team", team).execute().data


def add_national_match(date, opponent, goals_for, goals_against, **kwargs):
    """Ajoute un match de l'equipe nationale."""
    # Calculer le resultat automatiquement
    if goals_for > goals_against:
        result = "W"
    elif goals_for < goals_against:
        result = "L"
    else:
        result = "D"
    data = {"date": date, "opponent": opponent, "goals_for": goals_for,
            "goals_against": goals_against, "result": result, **kwargs}
    return supabase.table("national_matches").upsert(data, on_conflict="date,opponent,team").execute().data


def get_national_matches(limit=20):
    """Retourne les derniers matchs."""
    return supabase.table("national_matches").select("*").order("date", desc=True).limit(limit).execute().data


def get_national_matches_by_competition(competition):
    """Matchs d'une competition."""
    return supabase.table("national_matches").select("*").ilike("competition", f"%{competition}%").order("date", desc=True).execute().data


def get_national_record():
    """Bilan general W/D/L."""
    return supabase.table("v_national_team_record").select("*").execute().data


def get_record_by_competition():
    """Bilan par competition."""
    return supabase.table("v_record_by_competition").select("*").execute().data


def get_record_by_opponent():
    """Bilan par adversaire."""
    return supabase.table("v_record_by_opponent").select("*").execute().data


def get_national_top_scorers():
    """Meilleurs buteurs en selection."""
    return supabase.table("v_national_top_scorers").select("*").execute().data


def add_squad_callup(player_id, match_id=None, **kwargs):
    """Ajoute une convocation/performance en selection."""
    data = {"player_id": player_id, "match_id": match_id, **kwargs}
    return supabase.table("squad_callups").upsert(data, on_conflict="player_id,match_id").execute().data


def get_player_callups(player_id):
    """Convocations d'un joueur."""
    return supabase.table("squad_callups").select("*, national_matches(*)").eq("player_id", player_id).order("date", desc=True).execute().data


def add_competition(name, year, **kwargs):
    """Ajoute une competition."""
    data = {"name": name, "year": year, **kwargs}
    return supabase.table("competitions").upsert(data, on_conflict="name,year").execute().data


def get_competitions():
    """Liste toutes les competitions."""
    return supabase.table("competitions").select("*").order("year", desc=True).execute().data
