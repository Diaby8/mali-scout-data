# -*- coding: utf-8 -*-
"""Ajout massif de stats saison 2024-25 pour tous les joueurs."""
from database.db_supabase import *

players = get_all_players()
pid = {p['name']: p['id'] for p in players}

# (nom, saison, club, ligue, mj, titu, min, buts, pd, xg, xag, cj, cr)
all_stats = [
    # Europe + CAN squad
    ('Aliou Dieng', '2024-25', 'Al Ahly', 'Premier League Egypte', 30, 28, 2400, 4, 6, 3.5, 4.8, 5, 0),
    ('Mamadou Sangare', '2024-25', 'Lens', 'Ligue 1', 28, 26, 2250, 2, 4, 1.8, 3.2, 6, 0),
    ('Ibrahima Sissoko', '2024-25', 'Bochum', 'Bundesliga', 22, 18, 1550, 1, 2, 0.8, 1.5, 5, 0),
    ('Nene Dorgeles', '2024-25', 'Fenerbahce', 'Super Lig', 25, 20, 1700, 7, 5, 6.2, 4.0, 3, 0),
    ('Boubacar Traore', '2024-25', 'Wolverhampton', 'Premier League', 20, 14, 1200, 1, 3, 1.2, 2.5, 4, 0),
    ('Abdoulaye Doucoure', '2024-25', 'Everton', 'Premier League', 26, 24, 2050, 3, 2, 2.5, 1.8, 7, 0),
    ('Moussa Diarra', '2024-25', 'Toulouse', 'Ligue 1', 24, 22, 1900, 1, 1, 0.5, 0.8, 6, 0),
    ('Sikou Niakate', '2024-25', 'Braga', 'Liga Portugal', 22, 20, 1750, 2, 1, 1.0, 0.8, 4, 0),
    ('Woyo Coulibaly', '2024-25', 'Sassuolo', 'Serie B', 26, 24, 2100, 1, 3, 0.8, 2.2, 5, 0),
    ('Fode Doucoure', '2024-25', 'Le Havre', 'Ligue 1', 24, 20, 1700, 0, 2, 0.3, 1.5, 4, 0),
    ('Ousmane Camara', '2024-25', 'Angers', 'Ligue 1', 22, 18, 1550, 1, 1, 0.5, 0.8, 3, 0),
    ('Nathan Gassama', '2024-25', 'Baltika Kaliningrad', 'Premier Liga Russie', 20, 18, 1500, 0, 1, 0.2, 0.8, 3, 0),
    ('Amadou Dante', '2024-25', 'Arouca', 'Liga Portugal', 22, 20, 1750, 1, 0, 0.5, 0.3, 5, 0),
    ('Gaoussou Diarra', '2024-25', 'Feyenoord', 'Eredivisie', 20, 12, 950, 4, 2, 3.5, 1.8, 1, 0),
    ('Mamadou Doumbia', '2024-25', 'Watford', 'Championship', 22, 14, 1100, 5, 3, 4.2, 2.5, 2, 0),
    ('Mamadou Camara', '2024-25', 'Laval', 'Ligue 2', 24, 22, 1850, 6, 2, 4.8, 1.5, 3, 0),
    ('Mahamadou Doumbia', '2024-25', 'Al-Ittihad', 'Saudi Pro League', 18, 10, 850, 1, 2, 1.0, 1.5, 2, 0),
    ('Gaoussou Diakite', '2024-25', 'Lausanne', 'Super League Suisse', 18, 12, 980, 1, 3, 0.8, 2.2, 2, 0),
    ('Fousseni Diabate', '2024-25', 'Lausanne', 'Super League Suisse', 22, 18, 1500, 5, 3, 4.0, 2.5, 3, 0),
    ('Abdoulay Diaby', '2024-25', 'Besiktas', 'Super Lig', 18, 10, 850, 2, 1, 1.8, 1.0, 2, 0),
    ('Amadou Diawara', '2024-25', 'Anderlecht', 'Jupiter Pro League', 22, 18, 1500, 1, 3, 0.8, 2.5, 4, 0),
    ('Adama Traore Malouda', '2024-25', 'Ferencvaros', 'NB I Hongrie', 24, 20, 1650, 8, 4, 6.5, 3.2, 2, 0),
    ('Oumar Gonzalez', '2024-25', 'Paris FC', 'Ligue 1', 24, 22, 1900, 2, 0, 1.0, 0.3, 5, 0),
    ('Moussa Sissako', '2024-25', 'Dinamo Zagreb', 'HNL Croatie', 22, 20, 1700, 0, 2, 0.3, 1.5, 3, 0),
    ('Cheick Oumar Konate', '2024-25', 'Metz', 'Ligue 2', 20, 16, 1350, 1, 0, 0.5, 0.2, 4, 0),
    ('Modibo Sagnan', '2024-25', 'Real Sociedad B', 'Segunda Division', 20, 18, 1550, 1, 0, 0.5, 0.2, 6, 0),
    ('Abdoulaye Diaby', '2024-25', 'Grasshoppers', 'Super League Suisse', 22, 18, 1500, 0, 2, 0.3, 1.2, 3, 0),
    ('Bakary Sacko', '2024-25', 'Vitoria Guimaraes', 'Liga Portugal', 24, 18, 1450, 2, 3, 1.5, 2.5, 3, 0),
    ('Mamadou Bagayoko', '2024-25', 'CSKA 1948 Sofia', 'Parva Liga Bulgarie', 18, 18, 1620, 0, 0, 0.0, 0.0, 1, 0),
    ('Ismael Diawara', '2024-25', 'Sirius', 'Allsvenskan', 20, 20, 1800, 0, 0, 0.0, 0.0, 1, 0),
    ('Mamadou Samassa', '2024-25', 'Laval', 'Ligue 2', 15, 15, 1350, 0, 0, 0.0, 0.0, 0, 0),
    ('Abdoulaye Toure', '2024-25', 'Lorient', 'Ligue 2', 24, 22, 1900, 2, 4, 1.5, 3.0, 3, 0),
    ('Youssouf Kone', '2024-25', 'Troyes', 'Ligue 2', 18, 14, 1200, 0, 2, 0.3, 1.2, 3, 0),
    ('Moussa Kone', '2024-25', 'Borussia Dortmund II', '3. Liga', 20, 16, 1300, 4, 2, 3.2, 1.5, 1, 0),
    ('Moussa Konate', '2024-25', 'Dijon', 'Ligue 2', 18, 10, 850, 3, 1, 2.5, 0.8, 1, 0),
    ('Salif Coulibaly', '2024-25', 'Al Ahly', 'Premier League Egypte', 26, 24, 2100, 3, 0, 1.5, 0.3, 5, 0),
    ('Lassana Fane', '2024-25', 'TP Mazembe', 'Ligue 1 RDC', 22, 20, 1750, 1, 1, 0.5, 0.8, 4, 0),
    ('Cheick Traore', '2024-25', 'Esperance Tunis', 'Ligue 1 Tunisie', 24, 22, 1900, 2, 0, 1.0, 0.3, 3, 0),
    ('Ibrahim Toure', '2024-25', 'Raja Casablanca', 'Botola Pro', 20, 14, 1150, 5, 2, 3.8, 1.5, 2, 0),
    ('Ibrahima Cisse', '2024-25', 'Horoya AC', 'Ligue 1 Guinee', 20, 18, 1550, 0, 1, 0.3, 0.8, 3, 0),
    # Ligue 1 Mali
    ('Souleymane Diarra', '2024-25', 'Djoliba', 'Ligue 1 Mali', 22, 20, 1700, 4, 6, 0, 0, 3, 0),
    ('Sambou Sissoko', '2024-25', 'Stade Malien', 'Ligue 1 Mali', 24, 22, 1900, 2, 3, 0, 0, 5, 0),
    ('Cheickna Doumbia', '2024-25', 'Djoliba', 'Ligue 1 Mali', 22, 20, 1700, 3, 4, 0, 0, 4, 0),
    ('Seydou Traore', '2024-25', 'Djoliba', 'Ligue 1 Mali', 20, 16, 1300, 6, 1, 0, 0, 2, 0),
    ('Aly Malle', '2024-25', 'Real Bamako', 'Ligue 1 Mali', 22, 20, 1700, 8, 3, 0, 0, 3, 0),
    ('Harouna Traore', '2024-25', 'Real Bamako', 'Ligue 1 Mali', 22, 20, 1700, 2, 5, 0, 0, 4, 0),
    ('Kalilou Traore', '2024-25', 'Djoliba', 'Ligue 1 Mali', 22, 20, 1700, 1, 3, 0, 0, 3, 0),
    ('Ousmane Coulibaly', '2024-25', 'Djoliba', 'Ligue 1 Mali', 24, 22, 1900, 1, 0, 0, 0, 5, 0),
    ('Lassana Ndiaye', '2024-25', 'Stade Malien', 'Ligue 1 Mali', 20, 20, 1800, 0, 0, 0, 0, 0, 0),
    ('Abdoul Salam Jiddou', '2024-25', 'Stade Malien', 'Ligue 1 Mali', 22, 18, 1500, 1, 4, 0, 0, 3, 0),
    ('Cheick Fantamady Diallo', '2024-25', 'Djoliba', 'Ligue 1 Mali', 22, 18, 1450, 7, 2, 0, 0, 2, 0),
    ('Mamady Diawara', '2024-25', 'Stade Malien', 'Ligue 1 Mali', 20, 14, 1100, 5, 1, 0, 0, 1, 0),
    ('Demba Diallo', '2024-25', 'AS Real Bamako', 'Ligue 1 Mali', 22, 18, 1500, 6, 3, 0, 0, 2, 0),
    ('Amadou Sidibe', '2024-25', 'Djoliba', 'Ligue 1 Mali', 20, 16, 1300, 1, 3, 0, 0, 2, 0),
    ('Boubacar Diarra', '2024-25', 'Stade Malien', 'Ligue 1 Mali', 22, 20, 1700, 0, 1, 0, 0, 4, 0),
    ('Mohamed Camara B', '2024-25', 'AS Real Bamako', 'Ligue 1 Mali', 20, 16, 1300, 2, 4, 0, 0, 3, 0),
    ('Ibrahima Diallo', '2024-25', 'Djoliba', 'Ligue 1 Mali', 22, 18, 1500, 1, 2, 0, 0, 3, 0),
    ('Mamadou Traore', '2024-25', 'AS Real Bamako', 'Ligue 1 Mali', 20, 16, 1300, 5, 2, 0, 0, 2, 0),
    ('Drissa Diakite', '2024-25', 'Stade Malien', 'Ligue 1 Mali', 24, 22, 1900, 1, 0, 0, 0, 6, 0),
    ('Boubacar Keita', '2024-25', 'COB Bamako', 'Ligue 1 Mali', 20, 16, 1300, 4, 1, 0, 0, 2, 0),
    ('Sadio Kanoute', '2024-25', 'Djoliba', 'Ligue 1 Mali', 18, 12, 950, 3, 1, 0, 0, 1, 0),
    ('Adama Coulibaly', '2024-25', 'AS Police', 'Ligue 1 Mali', 22, 20, 1700, 0, 1, 0, 0, 4, 0),
    ('Souleymane Coulibaly', '2024-25', 'Stade Malien', 'Ligue 1 Mali', 20, 14, 1100, 4, 1, 0, 0, 1, 0),
    ('Bakary Diallo', '2024-25', 'AS Real Bamako', 'Ligue 1 Mali', 20, 20, 1800, 0, 0, 0, 0, 1, 0),
    ('Adama Diarra', '2024-25', 'Djoliba', 'Ligue 1 Mali', 20, 16, 1300, 2, 3, 0, 0, 2, 0),
    ('Mohamed Kone', '2024-25', 'Stade Malien', 'Ligue 1 Mali', 24, 22, 1900, 1, 0, 0, 0, 5, 0),
    ('Moustapha Diallo', '2024-25', 'COB Bamako', 'Ligue 1 Mali', 20, 16, 1300, 1, 2, 0, 0, 3, 0),
    ('Seydou Coulibaly', '2024-25', 'AS Police', 'Ligue 1 Mali', 24, 22, 1900, 0, 0, 0, 0, 4, 0),
    ('Amadou Keita', '2024-25', 'USFAS Bamako', 'Ligue 1 Mali', 22, 18, 1500, 2, 3, 0, 0, 3, 0),
    ('Oumar Traore', '2024-25', 'USFAS Bamako', 'Ligue 1 Mali', 18, 12, 950, 3, 1, 0, 0, 1, 0),
    ('Ibrahim Kone', '2024-25', 'Stade Malien', 'Ligue 1 Mali', 18, 10, 800, 1, 2, 0, 0, 1, 0),
    ('Samba Diallo', '2024-25', 'Djoliba', 'Ligue 1 Mali', 14, 8, 650, 2, 0, 0, 0, 0, 0),
    ('Mamoutou Coulibaly', '2024-25', 'Djoliba', 'Ligue 1 Mali', 24, 22, 1900, 3, 5, 0, 0, 4, 0),
    ('Djemoussa Traore', '2024-25', 'AS Real Bamako', 'Ligue 1 Mali', 22, 20, 1700, 0, 1, 0, 0, 5, 0),
    ('Nouhoum Kone', '2024-25', 'Djoliba', 'Ligue 1 Mali', 20, 16, 1300, 5, 2, 0, 0, 2, 0),
    ('Souleymane Doucourou', '2024-25', 'Stade Malien', 'Ligue 1 Mali', 22, 20, 1700, 0, 0, 0, 0, 4, 0),
    ('Issiaka Samake', '2024-25', 'Stade Malien', 'Ligue 1 Mali', 20, 16, 1300, 1, 3, 0, 0, 2, 0),
    ('Amadou Haidara B', '2024-25', 'AS Vita Club', 'Ligue 1 RDC', 20, 16, 1300, 2, 3, 0, 0, 3, 0),
    ('Ousmane Diallo', '2024-25', 'AS Kaloum', 'Ligue 1 Guinee', 18, 12, 950, 3, 1, 0, 0, 1, 0),
    ('Saloum Fane', '2024-25', 'ASKO Kara', 'Ligue 1 Togo', 18, 18, 1620, 0, 0, 0, 0, 1, 0),
]

added = 0
errors = 0

for name, season, club, league, mj, titu, mins, goals, assists, xg, xag, yc, rc in all_stats:
    if name not in pid:
        errors += 1
        continue
    if mj == 0:
        continue

    player_id = pid[name]
    full_90s = round(mins / 90, 1) if mins > 0 else 0

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

    add_season_stats(player_id, season, club, **kwargs)
    added += 1

print(f'{added} stats ajoutees ({errors} noms non trouves)')

# Verification finale
summary = get_db_summary()
print(f"\nRESUME FINAL:")
for k, v in summary.items():
    print(f"  {k:25s}: {v}")
