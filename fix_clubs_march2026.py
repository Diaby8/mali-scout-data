# -*- coding: utf-8 -*-
"""Correction des clubs - Mars 2026 (donnees verifiees via web)."""
from database.db_supabase import get_all_players, update_player
from database.supabase_client import supabase

print("=== CORRECTION DES CLUBS - MARS 2026 ===\n")
print("Sources: Transfermarkt, Flashscore, Wikipedia, clubs officiels\n")

players = get_all_players()
pid_map = {p['name']: p['id'] for p in players}

# Corrections verifiees par recherche web (mars 2026)
corrections = {
    # --- TRANSFERTS CONFIRMES ---
    'Abdoulaye Doucoure': {
        'current_club': 'NEOM', 'current_league': 'Saudi Pro League', 'age': 33,
        'status': 'active'
    },
    'Boubacar Traore': {
        'current_club': 'Metz', 'current_league': 'Ligue 2', 'age': 24,
        'status': 'active'  # pret de Wolves
    },
    'Diadie Samassekou': {
        'current_club': 'Houston Dynamo', 'current_league': 'MLS', 'age': 29,
        'status': 'active'
    },
    'Fode Ballo-Toure': {
        'current_club': 'Metz', 'current_league': 'Ligue 2', 'age': 29,
        'status': 'active'
    },
    'Boubacar Kiki Kouyate': {
        'current_club': 'Antwerp', 'current_league': 'Jupiter Pro League', 'age': 29,
        'status': 'active'
    },
    'Sekou Koita': {
        'current_club': 'Genclerbirligi', 'current_league': 'Super Lig', 'age': 25,
        'status': 'active'  # pret de CSKA Moscou
    },
    'Adama Traore': {
        'current_club': 'Amedspor', 'current_league': '1. Lig Turquie', 'age': 30,
        'status': 'active'
    },
    'Ibrahim Mounkoro': {
        'current_club': 'TP Mazembe', 'current_league': 'Linafoot RDC', 'age': 35,
        'status': 'active'
    },
    'Moussa Djenepo': {
        'current_club': 'Esteghlal', 'current_league': 'Persian Gulf Pro League', 'age': 27,
        'status': 'active'
    },
    'Falaye Sacko': {
        'current_club': 'Neftchi Baku', 'current_league': 'Premier League Azerbaidjan', 'age': 29,
        'status': 'active'
    },
    'Amadou Diawara': {
        'current_club': 'Leganes', 'current_league': 'La Liga', 'age': 28,
        'status': 'active'
    },
    'Moussa Sissako': {
        'current_club': 'FK IMT Belgrad', 'current_league': 'Super Liga Serbie', 'age': 25,
        'status': 'active'
    },
    'Modibo Sagnan': {
        'current_club': 'Caykur Rizespor', 'current_league': 'Super Lig', 'age': 27,
        'status': 'active'  # pret de Montpellier
    },
    'Kevin Zohi': {
        'current_club': 'Torreense', 'current_league': 'Liga Portugal 2', 'age': 27,
        'status': 'active'
    },
    'Daouda Peeters': {
        'current_club': 'Las Vegas Lights', 'current_league': 'USL Championship', 'age': 27,
        'status': 'active'
    },
    'Abdoulay Diaby': {
        'current_club': 'Al-Batin', 'current_league': 'Saudi First Division', 'age': 34,
        'status': 'active'
    },
    'Lassine Sinayoko': {
        'current_club': 'Auxerre', 'current_league': 'Ligue 1', 'age': 24,
        'status': 'active'  # confirme, toujours a Auxerre
    },
    'Yves Bissouma': {
        'current_club': 'Tottenham', 'current_league': 'Premier League', 'age': 29,
        'status': 'active'  # confirme, contrat expire juin 2026
    },
    'Cheick Oumar Konate': {
        'current_club': 'AE Kifisia', 'current_league': 'Super League Grece', 'age': 23,
        'status': 'active'  # pret de Clermont
    },
    'Salif Coulibaly': {
        'current_club': 'Horoya AC', 'current_league': 'Ligue 1 Guinee', 'age': 33,
        'status': 'active'
    },
    'Sekou Kone': {
        'current_club': 'Lausanne-Sport', 'current_league': 'Super League Suisse', 'age': 20,
        'status': 'active'  # pret de Manchester United
    },
    'Abdoulaye Toure': {
        'current_club': 'Le Havre', 'current_league': 'Ligue 1', 'age': 31,
        'status': 'active'
    },
    'Hadi Sacko': {
        'current_club': 'Adanaspor', 'current_league': '1. Lig Turquie', 'age': 31,
        'status': 'active'
    },
    'Youssouf Kone': {
        'current_club': 'Free Agent', 'current_league': '', 'age': 30,
        'status': 'inactive'  # libre depuis mars 2025 (ex-JSK)
    },
    'Oumar Gonzalez': {
        'current_club': 'Free Agent', 'current_league': '', 'age': 27,
        'status': 'inactive'  # libre depuis juillet 2025
    },
    # Moussa Kone (Dortmund II) -> introuvable en 2025-26, probablement parti
    'Moussa Kone': {
        'current_club': 'Inconnu', 'current_league': '', 'age': 25,
        'status': 'inactive'
    },
}

updated = 0
not_found = 0
for name, data in corrections.items():
    if name in pid_map:
        update_player(pid_map[name], **data)
        updated += 1
        club = data['current_club']
        league = data.get('current_league', '')
        print(f"  OK {name:30s} -> {club} ({league})")
    else:
        not_found += 1
        print(f"  ?? {name} non trouve dans la base")

print(f"\n{updated} joueurs corriges, {not_found} non trouves.")

# === AJOUT TRANSFERTS HISTORIQUES ===
print("\n=== AJOUT TRANSFERTS HISTORIQUES ===\n")

transfers_data = [
    # (nom, date, club_depart, club_arrivee, type, fee)
    ('Abdoulaye Doucoure', '2025-08-15', 'Everton', 'NEOM', 'Free Transfer', None),
    ('Boubacar Traore', '2025-07-24', 'Wolverhampton', 'Metz', 'Loan', None),
    ('Diadie Samassekou', '2025-08-23', 'Hoffenheim', 'Houston Dynamo', 'Free Transfer', None),
    ('Fode Ballo-Toure', '2025-01-21', 'AC Milan', 'Metz', 'Free Transfer', None),
    ('Boubacar Kiki Kouyate', '2025-08-12', 'Montpellier', 'Antwerp', 'Free Transfer', None),
    ('Sekou Koita', '2025-08-20', 'CSKA Moscow', 'Genclerbirligi', 'Loan', None),
    ('Adama Traore', '2025-07-01', 'Hull City', 'Amedspor', 'Transfer', None),
    ('Ibrahim Mounkoro', '2024-01-01', 'Hatayspor', 'TP Mazembe', 'Transfer', None),
    ('Moussa Djenepo', '2025-08-20', 'Standard Liege', 'Esteghlal', 'Transfer', None),
    ('Falaye Sacko', '2025-08-10', 'Montpellier', 'Neftchi Baku', 'Free Transfer', None),
    ('Amadou Diawara', '2025-07-31', 'Anderlecht', 'Leganes', 'Free Transfer', None),
    ('Modibo Sagnan', '2025-08-02', 'Montpellier', 'Caykur Rizespor', 'Loan', None),
    ('Kevin Zohi', '2025-08-02', 'Metz', 'Torreense', 'Transfer', None),
    ('Daouda Peeters', '2025-02-19', 'Free Agent', 'Las Vegas Lights', 'Free Transfer', None),
    ('Abdoulay Diaby', '2025-09-10', 'Free Agent', 'Al-Batin', 'Free Transfer', None),
    ('Cheick Oumar Konate', '2026-01-08', 'Clermont', 'AE Kifisia', 'Loan', None),
    ('Sekou Kone', '2026-02-02', 'Manchester United', 'Lausanne-Sport', 'Loan', None),
]

transfers_added = 0
for name, date, from_club, to_club, transfer_type, fee in transfers_data:
    if name not in pid_map:
        print(f"  ?? {name} non trouve")
        continue
    player_id = pid_map[name]
    try:
        data = {
            'player_id': player_id,
            'date': date,
            'from_club': from_club,
            'to_club': to_club,
            'transfer_type': transfer_type,
        }
        if fee:
            data['fee'] = fee
        supabase.table('transfers').insert(data).execute()
        transfers_added += 1
        print(f"  {name:28s} | {from_club} -> {to_club} ({transfer_type})")
    except Exception as e:
        print(f"  ERR {name}: {e}")

print(f"\n{transfers_added} transferts ajoutes.")

# Resume
from database.db_supabase import get_db_summary
summary = get_db_summary()
print(f"\n=== RESUME BASE ===")
for k, v in summary.items():
    print(f"  {k:25s}: {v}")
