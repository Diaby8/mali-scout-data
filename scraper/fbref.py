"""
Scraper FBref pour les joueurs maliens.
Approche hybride:
1. Import CSV (copie depuis FBref - methode la plus fiable)
2. Scraping direct avec undetected-chromedriver (quand accessible)
"""

import time
import re
import os
import sys
import csv
import io

import pandas as pd
from bs4 import BeautifulSoup, Comment

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import FBREF_BASE, REQUEST_DELAY
from database.db import (
    init_db, upsert_player, upsert_season_stats,
    upsert_shooting_stats, upsert_passing_stats, upsert_defense_stats
)


def safe_int(val):
    try:
        return int(float(val))
    except (ValueError, TypeError):
        return None


def safe_float(val):
    try:
        return float(val)
    except (ValueError, TypeError):
        return None


def extract_fbref_id(url):
    match = re.search(r"/players/([a-f0-9]+)/", url)
    return match.group(1) if match else None


# =============================================================================
# METHODE 1 : Import CSV (la plus fiable)
# =============================================================================

def import_from_csv(csv_path: str, data_type: str = "standard"):
    """
    Importe des donnees depuis un fichier CSV exporte de FBref.

    data_type: "standard", "shooting", "passing", "defense"

    Comment utiliser:
    1. Va sur FBref (page joueur ou equipe)
    2. Clique sur "Share & Export" au-dessus du tableau
    3. Choisis "Get table as CSV (for Excel)"
    4. Colle dans un fichier .csv
    5. Lance cette fonction
    """
    df = pd.read_csv(csv_path)
    print(f"CSV charge: {len(df)} lignes, colonnes: {list(df.columns)[:10]}...")

    imported = 0
    for _, row in df.iterrows():
        name = str(row.get("Player", "")).strip()
        if not name or name == "Player":
            continue

        # Upsert joueur
        pos = str(row.get("Pos", "")) if pd.notna(row.get("Pos")) else None
        club = str(row.get("Squad", "")) if pd.notna(row.get("Squad")) else None
        league = str(row.get("Comp", "")) if pd.notna(row.get("Comp")) else None

        age_str = str(row.get("Age", ""))
        birth_year = None
        if age_str and age_str != "nan":
            age_val = safe_int(age_str.split("-")[0])
            if age_val:
                birth_year = 2025 - age_val

        pid = upsert_player(
            name=name,
            position=pos,
            current_club=club,
            current_league=league,
            birth_year=birth_year,
        )

        season = str(row.get("Season", "2024-2025"))

        if data_type == "standard":
            stats = {
                "league": league,
                "matches_played": safe_int(row.get("MP")),
                "starts": safe_int(row.get("Starts")),
                "minutes": safe_int(row.get("Min")),
                "goals": safe_int(row.get("Gls")),
                "assists": safe_int(row.get("Ast")),
                "yellow_cards": safe_int(row.get("CrdY")),
                "red_cards": safe_int(row.get("CrdR")),
                "xg": safe_float(row.get("xG")),
                "xag": safe_float(row.get("xAG")),
                "progressive_carries": safe_int(row.get("PrgC")),
                "progressive_passes": safe_int(row.get("PrgP")),
                "progressive_receives": safe_int(row.get("PrgR")),
                "goals_per90": safe_float(row.get("Gls.1") if "Gls.1" in row.index else None),
                "assists_per90": safe_float(row.get("Ast.1") if "Ast.1" in row.index else None),
                "xg_per90": safe_float(row.get("xG.1") if "xG.1" in row.index else None),
                "xag_per90": safe_float(row.get("xAG.1") if "xAG.1" in row.index else None),
            }
            stats = {k: v for k, v in stats.items() if v is not None}
            if stats:
                upsert_season_stats(pid, season, club=club, **stats)

        elif data_type == "shooting":
            stats = {
                "shots_total": safe_int(row.get("Sh")),
                "shots_on_target": safe_int(row.get("SoT")),
                "shots_on_target_pct": safe_float(row.get("SoT%")),
                "shots_per90": safe_float(row.get("Sh/90")),
                "goals_per_shot": safe_float(row.get("G/Sh")),
                "avg_shot_distance": safe_float(row.get("Dist")),
                "xg": safe_float(row.get("xG")),
                "npxg": safe_float(row.get("npxG")),
                "npxg_per_shot": safe_float(row.get("npxG/Sh")),
            }
            stats = {k: v for k, v in stats.items() if v is not None}
            if stats:
                upsert_shooting_stats(pid, season, club=club, **stats)

        elif data_type == "passing":
            stats = {
                "passes_completed": safe_int(row.get("Cmp")),
                "passes_attempted": safe_int(row.get("Att")),
                "pass_completion_pct": safe_float(row.get("Cmp%")),
                "key_passes": safe_int(row.get("KP")),
                "passes_into_final_third": safe_int(row.get("1/3")),
                "passes_into_penalty_area": safe_int(row.get("PPA")),
                "progressive_passes": safe_int(row.get("PrgP")),
            }
            stats = {k: v for k, v in stats.items() if v is not None}
            if stats:
                upsert_passing_stats(pid, season, club=club, **stats)

        elif data_type == "defense":
            stats = {
                "tackles": safe_int(row.get("Tkl")),
                "tackles_won": safe_int(row.get("TklW")),
                "interceptions": safe_int(row.get("Int")),
                "blocks": safe_int(row.get("Blocks")),
                "clearances": safe_int(row.get("Clr")),
                "errors": safe_int(row.get("Err")),
            }
            stats = {k: v for k, v in stats.items() if v is not None}
            if stats:
                upsert_defense_stats(pid, season, club=club, **stats)

        imported += 1
        print(f"  {name} ({pos}, {club}) - OK")

    print(f"\n{imported} joueurs importes!")
    return imported


def import_from_paste(pasted_text: str, data_type: str = "standard"):
    """
    Importe depuis du texte colle (format CSV de FBref).
    Utile pour le dashboard Streamlit.
    """
    # Sauvegarder en fichier temporaire
    tmp_path = os.path.join(os.path.dirname(__file__), "..", "data", "_temp_import.csv")
    with open(tmp_path, "w", encoding="utf-8") as f:
        f.write(pasted_text)
    result = import_from_csv(tmp_path, data_type)
    os.remove(tmp_path)
    return result


# =============================================================================
# METHODE 2 : Scraping direct (quand FBref est accessible)
# =============================================================================

def _get_driver():
    """Cree un driver Chrome non-detecte."""
    try:
        import undetected_chromedriver as uc
        options = uc.ChromeOptions()
        options.add_argument("--window-size=1920,1080")
        driver = uc.Chrome(options=options, version_main=145)
        return driver
    except Exception as e:
        print(f"Erreur creation driver: {e}")
        print("Installe undetected-chromedriver: pip install undetected-chromedriver")
        return None


def _wait_cloudflare(driver, timeout=30):
    """Attend que Cloudflare soit passe."""
    start = time.time()
    while time.time() - start < timeout:
        title = driver.title.lower()
        if "instant" not in title and "just a moment" not in title and "500" not in title:
            return True
        time.sleep(1)
    return False


def _fetch_soup(driver, url):
    """Charge une page via Selenium."""
    print(f"  Chargement: {url}")
    driver.get(url)
    if not _wait_cloudflare(driver):
        print(f"  ERREUR: page non chargee ({driver.title})")
        return None
    time.sleep(REQUEST_DELAY)
    return BeautifulSoup(driver.page_source, "lxml")


def _parse_table(soup, table_id):
    """Parse un tableau FBref (direct ou dans les commentaires HTML)."""
    table = soup.find("table", {"id": table_id})
    if table is None:
        comments = soup.find_all(string=lambda text: isinstance(text, Comment))
        for comment in comments:
            if table_id in str(comment):
                csoup = BeautifulSoup(str(comment), "lxml")
                table = csoup.find("table", {"id": table_id})
                if table:
                    break
    if table is None:
        return None
    df = pd.read_html(str(table))[0]
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[-1] if col[-1] != "" else col[-2] for col in df.columns]
    return df


def scrape_player_page(driver, player_url: str, player_name: str = ""):
    """
    Scrape la page FBref d'un joueur individuel.
    Retourne un dict avec toutes les infos.
    """
    soup = _fetch_soup(driver, player_url)
    if soup is None:
        return None

    info = {"url": player_url, "name": player_name}

    # Meta
    h1 = soup.find("h1")
    if h1:
        info["name"] = h1.get_text(strip=True)

    meta = soup.find("div", {"id": "meta"})
    if meta:
        for p in meta.find_all("p"):
            text = p.get_text(strip=True)
            if "Position:" in text:
                info["position"] = text.split("Position:")[-1].split("▪")[0].strip()
            if "Club:" in text:
                info["club"] = text.split("Club:")[-1].strip()

    # Tables de stats
    for table_id, key in [
        ("stats_standard_dom_lg", "standard"),
        ("stats_shooting_dom_lg", "shooting"),
        ("stats_passing_dom_lg", "passing"),
        ("stats_defense_dom_lg", "defense"),
    ]:
        df = _parse_table(soup, table_id)
        if df is not None:
            info[key] = df

    return info


def scrape_player_and_save(driver, player_url: str, player_name: str = ""):
    """Scrape un joueur et sauvegarde en DB."""
    info = scrape_player_page(driver, player_url, player_name)
    if info is None:
        return None

    name = info.get("name", player_name)
    fbref_id = extract_fbref_id(player_url)

    pid = upsert_player(
        name=name,
        fbref_id=fbref_id,
        fbref_url=player_url,
        position=info.get("position"),
        current_club=info.get("club"),
    )

    # Standard stats
    std = info.get("standard")
    if std is not None and "Season" in std.columns:
        for _, row in std.iterrows():
            season = str(row.get("Season", "")).strip()
            if not season or season == "Season":
                continue
            club = str(row.get("Squad", "")) if pd.notna(row.get("Squad")) else None
            stats = {
                "league": str(row.get("Comp", "")) if pd.notna(row.get("Comp")) else None,
                "matches_played": safe_int(row.get("MP")),
                "starts": safe_int(row.get("Starts")),
                "minutes": safe_int(row.get("Min")),
                "goals": safe_int(row.get("Gls")),
                "assists": safe_int(row.get("Ast")),
                "yellow_cards": safe_int(row.get("CrdY")),
                "red_cards": safe_int(row.get("CrdR")),
                "xg": safe_float(row.get("xG")),
                "xag": safe_float(row.get("xAG")),
            }
            stats = {k: v for k, v in stats.items() if v is not None}
            if stats:
                upsert_season_stats(pid, season, club=club, **stats)

    print(f"  {name} sauvegarde (id={pid})")
    return pid


# =============================================================================
# METHODE 3 : Liste de joueurs maliens connus
# =============================================================================

MALI_PLAYERS_FBREF = [
    # ===== GARDIENS =====
    {"name": "Djigui Diarra", "url": "/en/players/9428b460/Djigui-Diarra", "pos": "GK",
     "club": "Stade Malien", "categories": ["national_team", "mali_ligue1"]},
    {"name": "Ibrahim Mounkoro", "url": "/en/players/f04f3e76/Ibrahim-Mounkoro", "pos": "GK",
     "club": "Hatayspor", "categories": ["national_team", "europe_other"]},

    # ===== DEFENSEURS =====
    {"name": "Hamari Traore", "url": "/en/players/a19444db/Hamari-Traore", "pos": "DF",
     "club": "Rennes", "categories": ["national_team", "europe_top5"]},
    {"name": "Massadio Haidara", "url": "/en/players/0caf3cd2/Massadio-Haidara", "pos": "DF",
     "club": "Lens", "categories": ["national_team", "europe_top5"]},
    {"name": "Boubacar Kiki Kouyate", "url": "/en/players/dba98bb7/Boubacar-Kouyate", "pos": "DF",
     "club": "Metz", "categories": ["national_team", "europe_top5"]},
    {"name": "Falaye Sacko", "url": "/en/players/7e33bbe5/Falaye-Sacko", "pos": "DF",
     "club": "Vitoria Guimaraes", "categories": ["national_team", "europe_other"]},
    {"name": "Kamory Doumbia", "url": "/en/players/6984c7c0/Kamory-Doumbia", "pos": "DF",
     "club": "Reims", "categories": ["national_team", "europe_top5"]},
    {"name": "Fodé Ballo-Touré", "url": "/en/players/db943aa5/Fode-Ballo-Toure", "pos": "DF",
     "club": "AC Milan", "categories": ["national_team", "europe_top5", "diaspora"]},
    {"name": "Kévin Zohi", "url": "/en/players/91c7a7f8/Kevin-Zohi", "pos": "DF",
     "club": "Metz", "categories": ["europe_top5", "diaspora"]},

    # ===== MILIEUX =====
    {"name": "Amadou Haidara", "url": "/en/players/3c529cfb/Amadou-Haidara", "pos": "MF",
     "club": "RB Leipzig", "categories": ["national_team", "europe_top5"]},
    {"name": "Yves Bissouma", "url": "/en/players/8a139f03/Yves-Bissouma", "pos": "MF",
     "club": "Tottenham", "categories": ["national_team", "europe_top5"]},
    {"name": "Diadié Samassekou", "url": "/en/players/31891baa/Diadie-Samassekou", "pos": "MF",
     "club": "Hoffenheim", "categories": ["national_team", "europe_top5"]},
    {"name": "Mohamed Camara", "url": "/en/players/9ce6e6a0/Mohamed-Camara", "pos": "MF",
     "club": "AS Monaco", "categories": ["national_team", "europe_top5"]},
    {"name": "Lassana Coulibaly", "url": "/en/players/5d519e33/Lassana-Coulibaly", "pos": "MF",
     "club": "Salernitana", "categories": ["national_team", "europe_top5"]},
    {"name": "Cheick Doucouré", "url": "/en/players/af3b4b65/Cheick-Doucoure", "pos": "MF",
     "club": "Crystal Palace", "categories": ["national_team", "europe_top5"]},
    {"name": "Makan Dioumassi", "url": "/en/players/e0a4eac5/Makan-Dioumassi", "pos": "MF",
     "club": "Djoliba", "categories": ["mali_ligue1"]},
    {"name": "Mamadou Fofana", "url": "/en/players/dd7d1f03/Mamadou-Fofana", "pos": "MF",
     "club": "Lens", "categories": ["europe_top5", "prospect"]},

    # ===== ATTAQUANTS =====
    {"name": "Moussa Djenepo", "url": "/en/players/2f4f2570/Moussa-Djenepo", "pos": "FW",
     "club": "Southampton", "categories": ["national_team", "europe_top5"]},
    {"name": "Adama Traore", "url": "/en/players/98358a45/Adama-Traore", "pos": "FW",
     "club": "Hatayspor", "categories": ["national_team", "europe_other"]},
    {"name": "Kalifa Coulibaly", "url": "/en/players/c2b53093/Kalifa-Coulibaly", "pos": "FW",
     "club": "Nantes", "categories": ["national_team", "europe_top5"]},
    {"name": "Moussa Doumbia", "url": "/en/players/8ca26b29/Moussa-Doumbia", "pos": "FW",
     "club": "Reims", "categories": ["national_team", "europe_top5"]},
    {"name": "Sékou Koita", "url": "/en/players/d65a0df1/Sekou-Koita", "pos": "FW",
     "club": "RB Salzburg", "categories": ["national_team", "europe_other"]},
    {"name": "El Bilal Touré", "url": "/en/players/3e2b97e6/El-Bilal-Toure", "pos": "FW",
     "club": "Atalanta", "categories": ["national_team", "europe_top5"]},
    {"name": "Lassine Sinayoko", "url": "/en/players/bf459c7c/Lassine-Sinayoko", "pos": "FW",
     "club": "Auxerre", "categories": ["national_team", "europe_top5"]},
    {"name": "Abdoul Karim Koné", "url": "/en/players/ca1f8a82/Abdoul-Karim-Kone", "pos": "FW",
     "club": "Djoliba", "categories": ["mali_ligue1", "national_team"]},
    {"name": "Ibrahima Kone", "url": "/en/players/02d80a44/Ibrahima-Kone", "pos": "FW",
     "club": "Lorient", "categories": ["national_team", "europe_top5"]},
    {"name": "Kamory Doumbia", "url": "/en/players/15ca4ebb/Kamory-Doumbia-att", "pos": "FW",
     "club": "Stade de Reims", "categories": ["europe_top5", "prospect"]},
]


def scrape_known_players(max_players=None):
    """Scrape les joueurs maliens connus depuis la liste."""
    init_db()
    driver = _get_driver()
    if driver is None:
        return

    players = MALI_PLAYERS_FBREF[:max_players] if max_players else MALI_PLAYERS_FBREF

    try:
        for p in players:
            url = FBREF_BASE + p["url"]
            pid = upsert_player(name=p["name"], position=p["pos"],
                                fbref_url=url,
                                fbref_id=extract_fbref_id(url))
            try:
                scrape_player_and_save(driver, url, p["name"])
            except Exception as e:
                print(f"  ERREUR {p['name']}: {e}")
            time.sleep(REQUEST_DELAY)
    finally:
        try:
            driver.quit()
        except Exception:
            pass

    from database.db import get_db_summary
    summary = get_db_summary()
    print(f"\n=== Resultat ===")
    print(f"  Joueurs: {summary['joueurs']}")
    print(f"  Stats saison: {summary['stats_saison']}")


# =============================================================================
# METHODE 4 : Ajout manuel rapide
# =============================================================================

def add_player_manual(name, position, club, season="2024-2025",
                      goals=None, assists=None, matches=None,
                      minutes=None, xg=None, xag=None):
    """Ajoute un joueur manuellement avec ses stats de base."""
    pid = upsert_player(name=name, position=position, current_club=club)
    stats = {
        "goals": goals, "assists": assists,
        "matches_played": matches, "minutes": minutes,
        "xg": xg, "xag": xag,
    }
    stats = {k: v for k, v in stats.items() if v is not None}
    if stats:
        upsert_season_stats(pid, season, club=club, **stats)
    print(f"Joueur ajoute: {name} (id={pid})")
    return pid


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="FBref Scraper Mali")
    parser.add_argument("--csv", type=str, help="Importer un CSV FBref")
    parser.add_argument("--type", type=str, default="standard",
                        choices=["standard", "shooting", "passing", "defense"],
                        help="Type de stats du CSV")
    parser.add_argument("--scrape", action="store_true",
                        help="Scraper les joueurs connus")
    parser.add_argument("--max", type=int, default=None,
                        help="Nombre max de joueurs")
    parser.add_argument("--init-db", action="store_true",
                        help="Initialiser la base de donnees")
    args = parser.parse_args()

    if args.init_db:
        init_db()

    if args.csv:
        init_db()
        import_from_csv(args.csv, args.type)
    elif args.scrape:
        scrape_known_players(args.max)
    else:
        # Par defaut: initialiser la DB avec les joueurs connus (sans scraping)
        init_db()
        from database.db import add_player_category
        for p in MALI_PLAYERS_FBREF:
            url = FBREF_BASE + p["url"]
            pid = upsert_player(
                name=p["name"],
                position=p["pos"],
                fbref_url=url,
                fbref_id=extract_fbref_id(url),
                current_club=p.get("club"),
                category=p.get("categories", ["senior"])[0],
            )
            for cat in p.get("categories", []):
                add_player_category(pid, cat)
        from database.db import get_db_summary, get_all_categories
        summary = get_db_summary()
        cats = get_all_categories()
        print(f"Base initialisee avec {summary['joueurs']} joueurs")
        print(f"Categories: {', '.join(cats)}")
        print("Utilise --csv pour importer des stats ou --scrape pour scraper FBref")
