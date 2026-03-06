# Mali Scout Data

Plateforme de scouting pour les joueurs maliens. Base de donnees PostgreSQL (Supabase), dashboard Streamlit, generateur de visuels, et CLI interactif.

---

## Lancer l'outil

```bash
cd ~/desktop/MLdata
python cli.py
```

Ca ouvre un menu interactif. Tu tapes le numero de l'option que tu veux et tu te laisses guider.

---

## Le menu principal

```
--- JOUEURS ---
[1]  Voir tous les joueurs          (liste complete, filtrable par poste/ligue)
[2]  Chercher un joueur             (tape un nom, il trouve)
[3]  Fiche complete d'un joueur     (toutes les infos + stats + matchs)
[4]  Ajouter un joueur              (formulaire interactif)
[5]  Modifier un joueur             (changer club, ligue, age, statut...)
[6]  Ajouter des stats saison       (buts, PD, minutes, xG...)
[7]  Ajouter un match               (stats match par match d'un joueur en club)

--- EQUIPE NATIONALE ---
[8]  Les Aigles - Vue d'ensemble    (coach, classement FIFA, bilan W/D/L)
[9]  Resultats des matchs           (tous les scores, filtre par competition/adversaire)
[10] Ajouter un match EN            (Mali vs adversaire, score, competition, buteurs...)
[11] Convocations / Compositions    (qui a joue, selections d'un joueur, top buteurs EN)

--- OUTILS ---
[12] Classements                    (top buteurs, passeurs, par ligue, par poste)
[13] Scraper FBref                  (ajouter un joueur via URL ou importer CSV)
[14] Exporter les donnees           (CSV ou JSON)
[15] Generer un visuel              (fiche joueur, radar, comparaison, top chart)
[16] Requete SQL libre              (interroger n'importe quelle table)
[0]  Quitter
```

---

## Comment ajouter un joueur

1. Lance `python cli.py`
2. Tape **4**
3. Remplis les champs un par un (nom, poste, club, ligue, age...)
4. Laisse vide ce que tu ne sais pas
5. Il te propose d'ajouter des categories (europe_top5, national_team, prospect...)

## Comment ajouter des stats

1. Lance `python cli.py`
2. Tape **6** (stats saison) ou **7** (stats d'un match en club)
3. Cherche le joueur par nom ou ID
4. Remplis : saison, buts, passes, minutes, xG, etc.
5. Les stats per90 sont calculees automatiquement

## Comment ajouter un match de l'equipe nationale

1. Lance `python cli.py`
2. Tape **10**
3. Remplis : date, adversaire, competition (CAN, Qualif CM, Amical...), score
4. Le resultat (V/N/D) est calcule automatiquement
5. Ensuite il te propose d'ajouter les performances des joueurs (qui a marque, minutes, notes...)

## Comment voir le bilan des Aigles

1. Lance `python cli.py`
2. Tape **8** : vue d'ensemble (coach, FIFA ranking, bilan global, derniers matchs, buteurs EN)
3. Tape **9** : tous les resultats (filtre par competition ou adversaire)
4. Tape **11** : convocations d'un joueur, composition d'un match, meilleurs buteurs EN

---

## Architecture du projet

```
MLdata/
├── .env                      # Cles Supabase (NE JAMAIS PARTAGER)
├── cli.py                    # L'outil principal (menu interactif)
├── config.py                 # Configuration (couleurs, chemins)
├── app.py                    # Dashboard Streamlit (interface web locale)
├── requirements.txt          # Dependances Python
├── database/
│   ├── schema.sql            # Schema principal (tables joueurs, stats)
│   ├── schema_national.sql   # Schema equipe nationale (matchs, convocations)
│   ├── supabase_client.py    # Connexion a Supabase
│   ├── db_supabase.py        # Toutes les operations sur la base
│   ├── models.py             # Ancien schema SQLite (archive)
│   └── db.py                 # Ancien code SQLite (archive)
├── scraper/
│   └── fbref.py              # Import de donnees FBref
├── posts/
│   ├── generator.py          # Generateur de visuels
│   └── output/               # Images generees
└── data/
    └── mali_scout.db         # Ancienne base SQLite (archive)
```

---

## La base de donnees (Supabase)

Tes donnees sont sur **Supabase** (PostgreSQL dans le cloud, gratuit).

- **Acces** : https://supabase.com/dashboard
- **Table Editor** : voir/modifier les donnees visuellement (comme Excel)
- **SQL Editor** : ecrire des requetes SQL directement

### Tables joueurs

| Table | Contenu |
|-------|---------|
| `players` | Infos de base (nom, poste, club, age, taille...) |
| `player_categories` | Categories/tags (europe_top5, prospect, diaspora...) |
| `season_stats` | Stats par saison (buts, PD, minutes, xG...) |
| `shooting_stats` | Stats de tir (tirs cadres, distance, npxG...) |
| `passing_stats` | Stats de passes (courtes/longues, cles...) |
| `defense_stats` | Stats defensives (tacles, interceptions...) |
| `possession_stats` | Possession/dribbles (touches, carries...) |
| `goalkeeper_stats` | Stats gardien (arrets, clean sheets...) |
| `match_stats` | Stats match par match en club |
| `transfers` | Historique transferts |
| `market_value_history` | Evolution valeur marchande |
| `injuries` | Blessures |
| `awards` | Recompenses |

### Tables equipe nationale

| Table | Contenu |
|-------|---------|
| `national_team_info` | Infos Aigles (coach, capitaine, classement FIFA...) |
| `national_matches` | Resultats des matchs (date, adversaire, score, competition) |
| `squad_callups` | Performances par joueur par match EN |
| `competitions` | CAN, Qualifs CM, amicaux... |
| `competition_records` | Bilan par competition |

### Vues (requetes pre-faites)

| Vue | Ce qu'elle retourne |
|-----|---------------------|
| `v_top_scorers` | Classement des buteurs (club) |
| `v_top_assisters` | Classement des passeurs (club) |
| `v_latest_season` | Dernieres stats de chaque joueur |
| `v_player_summary` | Resume complet de chaque joueur |
| `v_national_team_record` | Bilan global des Aigles (W/D/L) |
| `v_recent_national_matches` | 20 derniers matchs EN |
| `v_record_by_competition` | Bilan par competition |
| `v_record_by_opponent` | Bilan contre chaque adversaire |
| `v_national_top_scorers` | Meilleurs buteurs en selection |

### Exemples de requetes SQL (dans Supabase SQL Editor)

```sql
-- Tous les milieux de terrain
SELECT name, current_club, age FROM players WHERE position = 'MF' ORDER BY age;

-- Joueurs en Premier League
SELECT name, position, current_club FROM players WHERE current_league = 'Premier League';

-- Joueurs de moins de 25 ans
SELECT name, position, current_club, age FROM players WHERE age < 25 ORDER BY age;

-- Nombre de joueurs par ligue
SELECT current_league, COUNT(*) as nb FROM players GROUP BY current_league ORDER BY nb DESC;

-- Bilan des Aigles
SELECT * FROM v_national_team_record;

-- Derniers matchs de l'equipe nationale
SELECT date, opponent, goals_for, goals_against, result, competition
FROM national_matches ORDER BY date DESC LIMIT 10;

-- Bilan contre un adversaire
SELECT * FROM v_record_by_opponent WHERE opponent = 'Senegal';
```

---

## Import de donnees

### Methode 1 : Via le CLI (option 4)
Le plus simple. Lance `python cli.py`, tape 4, remplis les champs.

### Methode 2 : CSV FBref (option 13)
1. Va sur fbref.com, page du joueur
2. Sous le tableau de stats : "Share & Export" > "Get as CSV"
3. Sauvegarde en fichier .csv
4. Dans le CLI (option 13 > choix 2), donne le chemin du fichier

### Methode 3 : Directement dans Supabase
Va dans Table Editor > `players` > Insert Row.

---

## Fichier .env

Contient tes cles Supabase. **Ne le partage JAMAIS.** Il est dans .gitignore, il ne sera jamais push sur Git.

```
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_ANON_KEY=ta_cle_anon
SUPABASE_SERVICE_KEY=ta_cle_service (optionnel)
```

---

## Installation (si tu clones le projet)

```bash
git clone https://github.com/Diaby8/mali-scout-data.git
cd mali-scout-data
pip install -r requirements.txt
# Configure .env avec tes cles Supabase
python cli.py
```

---

## Couleurs Mali

Les visuels utilisent les couleurs du drapeau malien :
- Vert : #14B53A
- Or : #FCD116
- Rouge : #CE1126
