"""Configuration centrale du projet Mali Scout Data."""

import os

# Chemins
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "mali_scout.db")
POSTS_OUTPUT = os.path.join(BASE_DIR, "posts", "output")

# Scraping
REQUEST_DELAY = 4  # secondes entre chaque requete FBref
SELENIUM_HEADLESS = True

# FBref URLs
FBREF_BASE = "https://fbref.com"
MALI_NT_URL = f"{FBREF_BASE}/en/squads/0f29b73a/Mali-Men-Stats"

# Couleurs Mali (pour les visuels)
COLORS = {
    "green": "#14B53A",
    "gold": "#FCD116",
    "red": "#CE1126",
    "bg_dark": "#1a1a2e",
    "bg_card": "#16213e",
    "white": "#FFFFFF",
}
