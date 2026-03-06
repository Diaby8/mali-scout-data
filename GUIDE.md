# MALI SCOUT DATA - Guide Complet

## Table des matieres
1. [Vue d'ensemble du projet](#1-vue-densemble)
2. [Comment scraper les donnees](#2-comment-scraper)
3. [Importer les donnees dans la base](#3-importer-les-donnees)
4. [Creer des visualisations](#4-creer-des-visualisations)
5. [Publier sur Twitter](#5-publier-sur-twitter)
6. [Routine quotidienne](#6-routine-quotidienne)
7. [Ajouter de nouvelles sources](#7-nouvelles-sources)
8. [Structure du projet](#8-structure-du-projet)

---

## 1. Vue d'ensemble

Ce projet te permet de :
- Collecter les stats de tous les joueurs maliens depuis plusieurs sources
- Stocker tout dans une base de donnees locale (SQLite)
- Generer des visuels pro pour Twitter/Instagram
- Suivre les performances au fil du temps

### Lancer le dashboard
```bash
cd C:\Users\DiabyDIAKITE\Desktop\MLdata
streamlit run app.py
```
Ouvre http://localhost:8501 dans ton navigateur.

---

## 2. Comment scraper les donnees

### Source 1 : FBref (stats avancees - xG, passes, defense)

FBref est LA meilleure source pour les stats avancees (StatsBomb data).
Cloudflare bloque les scripts automatiques, donc on fait un copier-coller manuel.

#### Methode CSV (la plus fiable)

**Etape 1 : Trouver le joueur**
- Va sur https://fbref.com
- Dans la barre de recherche, tape le nom du joueur (ex: "Amadou Haidara")
- Clique sur son profil

**Etape 2 : Copier les stats**
- Descends jusqu'au tableau "Standard Stats" (ou Shooting, Passing, Defense)
- Au-dessus du tableau, clique sur "Share & Export"
- Clique sur "Get table as CSV (for Excel)"
- Un bloc de texte apparait : SELECTIONNE TOUT et COPIE (Ctrl+A, Ctrl+C)

**Etape 3 : Importer**
- Ouvre le dashboard (streamlit run app.py)
- Va dans "Importer des donnees" > onglet "CSV FBref"
- Choisis le type de stats (standard, shooting, passing, defense)
- Colle le texte dans la zone
- Clique "Importer"

**OU en ligne de commande :**
```bash
# Sauvegarde le CSV dans un fichier
# Puis importe-le
python scraper/fbref.py --csv data/mon_fichier.csv --type standard
python scraper/fbref.py --csv data/tirs.csv --type shooting
python scraper/fbref.py --csv data/passes.csv --type passing
python scraper/fbref.py --csv data/defense.csv --type defense
```

#### Pages FBref utiles

| Page | URL | Ce qu'on y trouve |
|------|-----|-------------------|
| Joueur individuel | fbref.com/en/players/ID/Nom | Toutes les stats par saison |
| Equipe nationale Mali | fbref.com/en/squads/0f29b73a/Mali-Men-Stats | Effectif + stats NT |
| Ligue 1 francaise | fbref.com/en/comps/13/stats/Ligue-1-Stats | Tous les joueurs L1 |
| Premier League | fbref.com/en/comps/9/stats/Premier-League-Stats | Tous les joueurs PL |
| Bundesliga | fbref.com/en/comps/20/stats/Bundesliga-Stats | Tous les joueurs BuLi |
| Serie A | fbref.com/en/comps/11/stats/Serie-A-Stats | Tous les joueurs Serie A |

**Astuce** : Sur les pages de ligue, tu peux filtrer par nationalite dans le tableau.
Cherche les joueurs avec "MLI" dans la colonne Nation.

#### Quels tableaux copier sur FBref

| Tableau | Type (--type) | Stats contenues |
|---------|---------------|-----------------|
| Standard Stats | standard | Matchs, buts, passes D, xG, xAG, minutes |
| Shooting | shooting | Tirs, tirs cadres, xG, npxG, distance |
| Passing | passing | Passes completes, %, passes cles, progressives |
| Defense | defense | Tacles, interceptions, blocks, degagements |
| Possession | (a venir) | Touches, dribbles, progressive carries |

---

### Source 2 : Transfermarkt (valeurs marchandes, transferts)

**Methode manuelle :**
1. Va sur https://www.transfermarkt.com
2. Cherche le joueur
3. Note sa valeur marchande, son club, sa duree de contrat
4. Ajoute-le manuellement dans le dashboard > "Ajout manuel"

**Pages utiles :**
- Equipe nationale : transfermarkt.com/mali/startseite/verein/15776
- Joueurs par valeur : trie par "Market value"

---

### Source 3 : Sofascore (notes de match, stats en temps reel)

**Methode manuelle :**
1. Va sur https://www.sofascore.com
2. Cherche un match ou un joueur
3. Tu trouves : note du match, touches, duels, passes, etc.
4. Utilise "Ajout manuel" dans le dashboard

**Ideal pour :** les stats post-match (rating, duels gagnes, etc.)

---

### Source 4 : FotMob (stats de match detaillees)

**Methode :**
1. Va sur https://www.fotmob.com
2. Cherche le joueur
3. Tu as ses stats par match et par saison
4. Copie les donnees manuellement

---

## 3. Importer les donnees dans la base

### Via le dashboard (recommande)
1. Lance `streamlit run app.py`
2. Va dans "Importer des donnees"
3. 3 options :
   - **CSV FBref** : colle un CSV copie depuis FBref
   - **Ajout manuel** : entre les stats a la main
   - **Scraping** : tente le scraping automatique (pas toujours fiable)

### Via le terminal
```bash
# Initialiser la base avec les 20 joueurs connus
python scraper/fbref.py

# Importer un CSV
python scraper/fbref.py --csv data/standard_stats.csv --type standard

# Ajouter un joueur en Python
python -c "
from scraper.fbref import add_player_manual
add_player_manual(
    name='Nouveau Joueur',
    position='MF',
    club='FC Bamako',
    season='2024-2025',
    goals=5,
    assists=3,
    matches=20,
    minutes=1500,
    xg=4.2
)
"
```

### Verifier la base
```bash
python -c "
from database.db import get_db_summary, get_all_players
print(get_db_summary())
for p in get_all_players():
    print(f\"{p['name']} - {p['position']} - {p['current_club']}\")
"
```

---

## 4. Creer des visualisations

### Via le dashboard
1. Va dans "Generateur de Posts"
2. Choisis le type :
   - **Fiche Joueur** : carte avec stats principales
   - **Radar Chart** : profil du joueur en araignee
   - **Comparaison** : 2 joueurs cote a cote
   - **Top Performers** : classement top N
3. Remplis les champs
4. Clique "Generer"
5. Telecharge l'image

### Via le terminal (Python)
```python
from posts.generator import (
    create_player_card,
    create_radar_chart,
    create_comparison,
    create_top_chart,
    generate_tweet_text
)

# Fiche joueur
create_player_card(
    "Amadou Haidara",
    "RB Leipzig",       # club
    "Milieu",           # poste
    {"Matchs": 28, "Buts": 5, "PD": 7, "xG": 4.2}
)

# Radar chart (valeurs de 0 a 100)
create_radar_chart(
    "Amadou Haidara",
    ["Tir", "Passe", "Dribble", "Defense", "Physique", "Vision"],
    [72, 78, 65, 80, 85, 75]
)

# Comparaison
create_comparison(
    "Haidara", {"Buts": 5, "PD": 7, "Tacles": 45},
    "Bissouma", {"Buts": 3, "PD": 4, "Tacles": 62}
)

# Top performers
create_top_chart(
    "Top 5 Buteurs Maliens 2024-25",
    ["El Bilal Toure", "Sekou Koita", "Haidara", "Djenepo", "Traore"],
    [12, 9, 5, 4, 3],
    "Buts"
)

# Texte de tweet
tweet = generate_tweet_text(
    "Amadou Haidara",
    {"Matchs": 28, "Buts": 5, "PD": 7},
    hashtags=["#Mali", "#Aigles", "#Bundesliga"]
)
print(tweet)
```

Les images sont sauvegardees dans `posts/output/`.

### Personnaliser les couleurs
Edite `config.py` pour changer les couleurs :
```python
COLORS = {
    "green": "#14B53A",   # Vert du drapeau
    "gold": "#FCD116",    # Or du drapeau
    "red": "#CE1126",     # Rouge du drapeau
    "bg_dark": "#1a1a2e", # Fond sombre
    "bg_card": "#16213e", # Fond des cartes
    "white": "#FFFFFF",
}
```

---

## 5. Publier sur Twitter

### Pour l'instant (manuel)
1. Genere ton visuel via le dashboard
2. Telecharge l'image
3. Copie le texte de tweet genere
4. Poste sur Twitter manuellement

### Bientot (automatique)
On va integrer l'API Twitter (X) pour poster directement depuis le dashboard.
Il faudra :
1. Creer un compte developpeur sur https://developer.twitter.com
2. Generer des cles API
3. Les ajouter dans un fichier `.env`

---

## 6. Routine quotidienne

### Le matin (10-15 min)
1. Ouvre FBref, Sofascore ou FotMob
2. Regarde si des joueurs maliens ont joue la veille
3. Copie les stats mises a jour
4. Importe dans le dashboard

### Le post (5-10 min)
1. Ouvre le dashboard > "Generateur de Posts"
2. Choisis un angle :
   - **Apres un match** : fiche joueur avec stats du match
   - **Fin de semaine** : comparaison de 2 joueurs
   - **Lundi** : top performers de la semaine
   - **Mercato** : fiche d'un joueur qui change de club
3. Genere le visuel + tweet
4. Poste sur Twitter

### Idees de contenu recurrent
| Jour | Type de post | Exemple |
|------|-------------|---------|
| Lundi | Top performers du week-end | "Top 5 Maliens ce week-end" |
| Mardi | Analyse tactique | Radar chart d'un joueur |
| Mercredi | Comparaison | "Haidara vs Bissouma" |
| Jeudi | Decouverte | Fiche d'un jeune talent |
| Vendredi | Preview week-end | Joueurs a suivre |
| Samedi | Live / post-match | Stats immediates |
| Dimanche | Recap | Bilan de la journee |

---

## 7. Ajouter de nouvelles sources

### Ajouter un joueur a la liste
Edite `scraper/fbref.py`, dans la liste `MALI_PLAYERS_FBREF` :
```python
MALI_PLAYERS_FBREF = [
    # ... joueurs existants ...
    {"name": "Nouveau Joueur", "url": "/en/players/ID/Nom-Joueur", "pos": "MF"},
]
```
Pour trouver l'ID FBref : va sur la page du joueur, l'URL contient `/players/XXXXX/`.

### Creer un nouveau type de visuel
Edite `posts/generator.py` et ajoute une nouvelle fonction :
```python
def create_mon_visuel(data, output_path=None):
    # Utilise matplotlib comme les autres fonctions
    fig, ax = plt.subplots(figsize=(10, 8))
    # ... ton code ...
    fig.savefig(filepath, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return filepath
```

### Structure de la base de donnees
La base contient ces tables :

**players** : infos de base
- name, position, current_club, current_league, birth_year, fbref_url

**season_stats** : stats par saison
- goals, assists, matches_played, minutes, xg, xag, progressive_carries, etc.

**shooting_stats** : stats de tir
- shots_total, shots_on_target, xg, npxg, goals_per_shot, etc.

**passing_stats** : stats de passes
- passes_completed, pass_completion_pct, key_passes, progressive_passes, etc.

**defense_stats** : stats defensives
- tackles, interceptions, blocks, clearances, etc.

**transfers** : historique transferts
- club_from, club_to, transfer_fee, market_value

**national_team** : stats en selection
- competition, matches, goals, assists, minutes

---

## 8. Structure du projet

```
MLdata/
├── config.py              # Configuration (chemins, couleurs, URLs)
├── app.py                 # Dashboard Streamlit (interface web)
├── requirements.txt       # Dependances Python
├── GUIDE.md               # Ce guide
│
├── database/
│   ├── models.py          # Schema SQL (tables)
│   └── db.py              # Operations base de donnees
│
├── scraper/
│   └── fbref.py           # Import CSV + scraping FBref
│
├── analytics/
│   └── (a venir)          # Calculs avances, classements
│
├── posts/
│   ├── generator.py       # Generation de visuels
│   └── output/            # Images generees
│
└── data/
    └── mali_scout.db      # Base de donnees SQLite
```

### Commandes utiles
```bash
# Lancer le dashboard
streamlit run app.py

# Initialiser la base
python scraper/fbref.py

# Importer des stats CSV
python scraper/fbref.py --csv data/fichier.csv --type standard

# Tester les visuels
python posts/generator.py

# Voir le contenu de la base
python -c "from database.db import get_db_summary; print(get_db_summary())"
```

---

## Conseils

1. **Commence petit** : importe 5-10 joueurs avec leurs stats, fais tes premiers posts
2. **Sois regulier** : un post par jour vaut mieux que 10 posts puis rien
3. **Qualite > Quantite** : verifie toujours tes stats avant de poster
4. **Engage ta communaute** : pose des questions, fais des sondages
5. **Source tes donnees** : mentionne toujours "Source: FBref/StatsBomb" dans tes posts
6. **Sauvegarde** : fais un `git push` regulier pour ne rien perdre
