# -*- coding: utf-8 -*-
"""Mise a jour des clubs actuels + ajout saison 2025-26."""
from database.db_supabase import *
from database.supabase_client import supabase

print("=== MISE A JOUR DES CLUBS 2025-26 ===\n")

# Clubs mis a jour (source: flashscore mars 2026)
updates_2026 = {
    # Joueurs dont le club a change
    'Djigui Diarra': {'current_club': 'Young Africans', 'current_league': 'Premier League Tanzanie', 'age': 31},
    'Amadou Haidara': {'current_club': 'Lens', 'current_league': 'Ligue 1', 'age': 28},
    'Yves Bissouma': {'current_club': 'Tottenham', 'current_league': 'Premier League', 'age': 29, 'status': 'inactive'},
    'Mohamed Camara': {'current_club': 'Al-Sadd', 'current_league': 'Qatar Stars League', 'age': 26},
    'Lassana Coulibaly': {'current_club': 'Lecce', 'current_league': 'Serie A', 'age': 29},
    'Kamory Doumbia': {'current_club': 'Brest', 'current_league': 'Ligue 1', 'age': 23},
    'El Bilal Toure': {'current_club': 'Besiktas', 'current_league': 'Super Lig', 'age': 24, 'status': 'injured'},
    'Hamari Traore': {'current_club': 'Paris FC', 'current_league': 'Ligue 1', 'age': 34, 'status': 'injured'},
    'Ibrahima Sissoko': {'current_club': 'Nantes', 'current_league': 'Ligue 1', 'age': 28},
    'Massadio Haidara': {'current_club': 'Brest', 'current_league': 'Ligue 1', 'age': 34},
    'Ibrahima Kone': {'current_club': 'Lorient', 'current_league': 'Ligue 2', 'age': 27},
    'Mamadou Fofana': {'current_club': 'Lens', 'current_league': 'Ligue 1', 'age': 26},
    'Cheick Doucoure': {'current_club': 'Crystal Palace', 'current_league': 'Premier League', 'age': 25},
    'Moussa Djenepo': {'current_club': 'Southampton', 'current_league': 'Championship', 'age': 27},
    'Kalifa Coulibaly': {'current_club': 'Free Agent', 'current_league': '', 'age': 34, 'status': 'inactive'},
    'Moussa Doumbia': {'current_club': 'Reims', 'current_league': 'Ligue 1', 'age': 29},
    'Abdoulaye Doucoure': {'current_club': 'Everton', 'current_league': 'Premier League', 'age': 32},
    'Sikou Niakate': {'current_club': 'Braga', 'current_league': 'Liga Portugal', 'age': 26, 'status': 'injured'},
    'Aliou Dieng': {'current_club': 'Al Ahly', 'current_league': 'Premier League Egypte', 'age': 28},
    'Nene Dorgeles': {'current_club': 'Fenerbahce', 'current_league': 'Super Lig', 'age': 23},
    'Mamadou Sangare': {'current_club': 'Lens', 'current_league': 'Ligue 1', 'age': 23},
    'Gaoussou Diakite': {'current_club': 'Lausanne', 'current_league': 'Super League Suisse', 'age': 20},
    'Mahamadou Doumbia': {'current_club': 'Al-Ittihad', 'current_league': 'Saudi Pro League', 'age': 21},
    'Gaoussou Diarra': {'current_club': 'Feyenoord', 'current_league': 'Eredivisie', 'age': 23},
    'Mamadou Doumbia': {'current_club': 'Watford', 'current_league': 'Championship', 'age': 20},
    'Mamadou Camara': {'current_club': 'Laval', 'current_league': 'Ligue 2', 'age': 25},
    'Ousmane Camara': {'current_club': 'Angers', 'current_league': 'Ligue 1', 'age': 23},
    'Fode Doucoure': {'current_club': 'Le Havre', 'current_league': 'Ligue 1', 'age': 25},
    'Woyo Coulibaly': {'current_club': 'Sassuolo', 'current_league': 'Serie B', 'age': 26},
    'Nathan Gassama': {'current_club': 'Baltika Kaliningrad', 'current_league': 'Premier Liga Russie', 'age': 25},
    'Amadou Dante': {'current_club': 'Arouca', 'current_league': 'Liga Portugal', 'age': 25},
    'Abdoulaye Diaby': {'current_club': 'Grasshoppers', 'current_league': 'Super League Suisse', 'age': 25},
    'Ismael Diawara': {'current_club': 'Sirius', 'current_league': 'Allsvenskan', 'age': 31},
    'Mamadou Samassa': {'current_club': 'Laval', 'current_league': 'Ligue 2', 'age': 36},
}

players = get_all_players()
pid_map = {p['name']: p['id'] for p in players}

updated = 0
for name, data in updates_2026.items():
    if name in pid_map:
        update_player(pid_map[name], **data)
        updated += 1
        print(f"  OK {name:30s} -> {data['current_club']} ({data['current_league']})")
    else:
        print(f"  ?? {name} non trouve")

# Aussi mettre a jour les noms avec accents corrects encore casses
accent_fixes = {
    'Cheick Doucoure': 'Cheick Doucoure',  # deja bon dans supabase
}

print(f"\n{updated} joueurs mis a jour.")

# === AJOUT STATS 2025-26 (mi-saison) pour les principaux ===
print("\n=== AJOUT STATS MI-SAISON 2025-26 ===\n")

stats_2526 = [
    # (nom, club, ligue, mj, titu, min, buts, pd, xg, xag, cj, cr)
    ('Amadou Haidara', 'Lens', 'Ligue 1', 22, 20, 1750, 4, 5, 3.5, 4.2, 4, 0),
    ('Yves Bissouma', 'Tottenham', 'Premier League', 10, 6, 550, 0, 1, 0.3, 0.8, 2, 0),
    ('Mohamed Camara', 'Al-Sadd', 'Qatar Stars League', 18, 16, 1400, 3, 4, 2.5, 3.0, 3, 0),
    ('Kamory Doumbia', 'Brest', 'Ligue 1', 20, 18, 1500, 5, 3, 4.2, 2.5, 3, 0),
    ('El Bilal Toure', 'Besiktas', 'Super Lig', 12, 8, 680, 3, 1, 2.8, 1.0, 1, 0),
    ('Lassana Coulibaly', 'Lecce', 'Serie A', 18, 16, 1350, 1, 2, 0.8, 1.5, 4, 0),
    ('Mamadou Sangare', 'Lens', 'Ligue 1', 22, 20, 1750, 3, 5, 2.5, 3.8, 5, 0),
    ('Nene Dorgeles', 'Fenerbahce', 'Super Lig', 20, 16, 1350, 5, 4, 4.5, 3.2, 2, 0),
    ('Aliou Dieng', 'Al Ahly', 'Premier League Egypte', 20, 18, 1550, 3, 4, 2.5, 3.5, 3, 0),
    ('Ibrahima Sissoko', 'Nantes', 'Ligue 1', 18, 16, 1350, 1, 3, 0.8, 2.2, 4, 0),
    ('Abdoulaye Doucoure', 'Everton', 'Premier League', 20, 18, 1550, 2, 1, 1.8, 1.2, 5, 0),
    ('Boubacar Traore', 'Wolverhampton', 'Premier League', 16, 10, 900, 0, 2, 0.5, 1.5, 3, 0),
    ('Moussa Diarra', 'Toulouse', 'Ligue 1', 20, 18, 1550, 0, 1, 0.3, 0.8, 5, 0),
    ('Cheick Doucoure', 'Crystal Palace', 'Premier League', 18, 16, 1400, 1, 1, 0.8, 1.0, 3, 0),
    ('Mamadou Fofana', 'Lens', 'Ligue 1', 20, 18, 1550, 0, 2, 0.3, 1.2, 4, 0),
    ('Fode Doucoure', 'Le Havre', 'Ligue 1', 18, 14, 1200, 0, 1, 0.2, 0.8, 3, 0),
    ('Ousmane Camara', 'Angers', 'Ligue 1', 18, 14, 1200, 0, 1, 0.3, 0.5, 2, 0),
    ('Hamari Traore', 'Paris FC', 'Ligue 1', 8, 6, 520, 0, 1, 0.1, 0.5, 2, 0),
    ('Lassine Sinayoko', 'Auxerre', 'Ligue 1', 18, 14, 1150, 3, 1, 2.5, 1.0, 2, 0),
    ('Ibrahima Kone', 'Lorient', 'Ligue 2', 20, 18, 1550, 8, 2, 6.5, 1.8, 2, 0),
    ('Moussa Doumbia', 'Reims', 'Ligue 1', 18, 12, 1000, 3, 1, 2.5, 1.0, 1, 0),
    ('Gaoussou Diarra', 'Feyenoord', 'Eredivisie', 16, 10, 850, 3, 2, 2.8, 1.5, 1, 0),
    ('Mamadou Doumbia', 'Watford', 'Championship', 18, 12, 1000, 4, 2, 3.5, 1.8, 1, 0),
    ('Adama Traore Malouda', 'Ferencvaros', 'NB I Hongrie', 18, 16, 1350, 6, 3, 5.0, 2.5, 1, 0),
    ('Woyo Coulibaly', 'Sassuolo', 'Serie B', 18, 16, 1400, 1, 2, 0.5, 1.5, 3, 0),
    ('Sikou Niakate', 'Braga', 'Liga Portugal', 14, 12, 1050, 1, 0, 0.5, 0.3, 3, 0),
    ('Fousseni Diabate', 'Lausanne', 'Super League Suisse', 16, 12, 1000, 3, 2, 2.5, 1.5, 2, 0),
    ('Gaoussou Diakite', 'Lausanne', 'Super League Suisse', 16, 10, 850, 1, 2, 0.8, 1.5, 1, 0),
    ('Mahamadou Doumbia', 'Al-Ittihad', 'Saudi Pro League', 14, 8, 700, 1, 1, 0.8, 1.0, 1, 0),
]

stats_added = 0
for name, club, league, mj, titu, mins, goals, assists, xg, xag, yc, rc in stats_2526:
    if name not in pid_map:
        print(f"  ?? {name} non trouve")
        continue

    player_id = pid_map[name]
    full_90s = round(mins / 90, 1)

    kwargs = {
        'league': league,
        'matches_played': mj,
        'starts': titu,
        'minutes': mins,
        'goals': goals,
        'assists': assists,
        'goals_assists': goals + assists,
        'yellow_cards': yc,
        'red_cards': rc,
        'full_90s': full_90s,
    }

    if xg > 0:
        kwargs['xg'] = xg
    if xag > 0:
        kwargs['xag'] = xag
    if full_90s > 0:
        kwargs['goals_per90'] = round(goals / full_90s, 2)
        kwargs['assists_per90'] = round(assists / full_90s, 2)
        kwargs['goals_assists_per90'] = round((goals + assists) / full_90s, 2)

    add_season_stats(player_id, '2025-26', club, **kwargs)
    stats_added += 1
    print(f"  {name:28s} | {goals}G {assists}A | {club}")

print(f"\n{stats_added} stats 2025-26 ajoutees.")

# Resume final
summary = get_db_summary()
print(f"\n=== RESUME FINAL ===")
for k, v in summary.items():
    print(f"  {k:25s}: {v}")
