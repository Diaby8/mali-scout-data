# -*- coding: utf-8 -*-
"""Correction massive de tous les joueurs - Mars 2026.
Sources: Transfermarkt, Footmercato, FBref (croisees par 5 agents de recherche).
"""
from database.db_supabase import get_all_players, update_player
from database.supabase_client import supabase

print("=== CORRECTION MASSIVE - MARS 2026 ===")
print("Sources: Transfermarkt + Footmercato + FBref\n")

players = get_all_players()
pid_map = {p['name']: p['id'] for p in players}

# ============================================================
# 1. MISES A JOUR DES CLUBS ET INFOS (verifie par web)
# ============================================================
updates = {
    # --- BATCH 1 : Joueurs top ---
    'Amadou Haidara': {
        'current_club': 'Lens', 'current_league': 'Ligue 1',
        'age': 28, 'height_cm': 178, 'foot': 'right', 'nationality': 'Mali',
        'status': 'active'
    },
    'Mohamed Camara': {
        'current_club': 'Al-Sadd', 'current_league': 'Qatar Stars League',
        'age': 26, 'height_cm': 173, 'foot': 'right', 'nationality': 'Mali',
        'status': 'active'
    },
    'Kamory Doumbia': {
        'current_club': 'Brest', 'current_league': 'Ligue 1',
        'position': 'MF', 'age': 23, 'height_cm': 170, 'foot': 'right',
        'nationality': 'Mali', 'status': 'active'
    },
    'El Bilal Toure': {
        'current_club': 'Besiktas', 'current_league': 'Super Lig',
        'age': 24, 'height_cm': 185, 'foot': 'both', 'nationality': 'Mali',
        'status': 'active'
    },
    'Lassana Coulibaly': {
        'current_club': 'Lecce', 'current_league': 'Serie A',
        'age': 29, 'height_cm': 183, 'foot': 'right', 'nationality': 'Mali',
        'status': 'active'
    },
    'Cheick Doucoure': {
        'current_club': 'Crystal Palace', 'current_league': 'Premier League',
        'age': 26, 'height_cm': 180, 'foot': 'right', 'nationality': 'Mali',
        'status': 'injured'  # blesse genou/achille depuis jan 2025
    },
    'Nene Dorgeles': {
        'current_club': 'Fenerbahce', 'current_league': 'Super Lig',
        'position': 'FW', 'age': 23, 'height_cm': 174, 'foot': 'right',
        'nationality': 'Mali', 'status': 'active'
    },
    'Aliou Dieng': {
        'current_club': 'Al Ahly', 'current_league': 'Premier League Egypte',
        'age': 28, 'height_cm': 184, 'foot': 'right', 'nationality': 'Mali',
        'status': 'active'  # pre-contrat Valencia ete 2026
    },
    'Moussa Diarra': {
        'current_club': 'Anderlecht', 'current_league': 'Jupiter Pro League',
        'age': 25, 'height_cm': 185, 'foot': 'left', 'nationality': 'Mali',
        'status': 'active'  # pret d'Alaves depuis jan 2026
    },

    # --- BATCH 2 ---
    'Ibrahima Kone': {
        'current_club': 'UD Almeria', 'current_league': 'LaLiga2',
        'age': 26, 'height_cm': 190, 'foot': 'left', 'nationality': 'Mali',
        'status': 'active'
    },
    'Moussa Doumbia': {
        'current_club': 'Free Agent', 'current_league': '',
        'age': 31, 'height_cm': 173, 'foot': 'right', 'nationality': 'Mali',
        'status': 'inactive'  # ex-Sochaux, libre depuis juil 2025
    },
    'Hamari Traore': {
        'current_club': 'Paris FC', 'current_league': 'Ligue 1',
        'age': 34, 'height_cm': 175, 'foot': 'right', 'nationality': 'Mali',
        'status': 'injured'  # genou depuis jan 2026
    },
    'Massadio Haidara': {
        'current_club': 'Kocaelispor', 'current_league': 'Super Lig',
        'age': 33, 'height_cm': 179, 'foot': 'left', 'nationality': 'Mali',
        'second_nationality': 'France', 'status': 'active'
    },
    'Ibrahima Sissoko': {
        'current_club': 'Nantes', 'current_league': 'Ligue 1',
        'age': 28, 'height_cm': 193, 'foot': 'right', 'nationality': 'Mali',
        'second_nationality': 'France', 'status': 'active'
    },
    'Mamadou Sangare': {
        'current_club': 'Lens', 'current_league': 'Ligue 1',
        'age': 23, 'height_cm': 181, 'foot': 'left', 'nationality': 'Mali',
        'status': 'active'
    },
    'Fousseni Diabate': {
        'current_club': 'Kasimpasa', 'current_league': 'Super Lig',
        'age': 30, 'height_cm': 178, 'foot': 'left', 'nationality': 'Mali',
        'second_nationality': 'France', 'status': 'active'
    },
    'Gaoussou Diarra': {
        'current_club': 'Feyenoord', 'current_league': 'Eredivisie',
        'age': 23, 'height_cm': 183, 'foot': 'right', 'nationality': 'Mali',
        'status': 'injured'  # cheville depuis dec 2025
    },
    'Mamadou Doumbia': {
        'current_club': 'Watford', 'current_league': 'Championship',
        'age': 20, 'height_cm': 192, 'foot': 'left', 'nationality': 'Mali',
        'status': 'active'
    },
    'Adama Traore Malouda': {
        'current_club': 'Genclerbirligi', 'current_league': 'Super Lig',
        'age': 30, 'height_cm': 178, 'foot': 'left', 'nationality': 'Mali',
        'status': 'active'
    },

    # --- BATCH 3 ---
    'Mahamadou Doumbia': {
        'current_club': 'Al-Ittihad', 'current_league': 'Saudi Pro League',
        'age': 21, 'height_cm': 186, 'foot': 'right', 'nationality': 'Mali',
        'status': 'active'
    },
    'Gaoussou Diakite': {
        'current_club': 'Lausanne-Sport', 'current_league': 'Super League Suisse',
        'position': 'FW', 'age': 20, 'height_cm': 182, 'foot': 'right',
        'nationality': 'Mali', 'status': 'active'
    },
    'Woyo Coulibaly': {
        'current_club': 'Sassuolo', 'current_league': 'Serie A',
        'age': 26, 'height_cm': 182, 'foot': 'both', 'nationality': 'Mali',
        'second_nationality': 'France', 'status': 'active'
    },
    'Sikou Niakate': {
        'current_club': 'Braga', 'current_league': 'Liga Portugal',
        'age': 26, 'height_cm': 186, 'foot': 'left', 'nationality': 'Mali',
        'second_nationality': 'France', 'status': 'injured'
    },
    'Nathan Gassama': {
        'current_club': 'Baltika Kaliningrad', 'current_league': 'Premier Liga Russie',
        'age': 25, 'height_cm': 192, 'foot': 'left', 'nationality': 'Mali',
        'second_nationality': 'France', 'status': 'active'
    },
    'Amadou Dante': {
        'current_club': 'Arouca', 'current_league': 'Liga Portugal',
        'age': 25, 'height_cm': 178, 'foot': 'left', 'nationality': 'Mali',
        'status': 'active'
    },
    'Abdoulaye Diaby': {
        'current_club': 'Grasshoppers', 'current_league': 'Super League Suisse',
        'age': 25, 'height_cm': 198, 'foot': 'right', 'nationality': 'Mali',
        'status': 'active'
    },
    'Ismael Diawara': {
        'current_club': 'Sirius', 'current_league': 'Allsvenskan',
        'age': 31, 'height_cm': 194, 'foot': 'right', 'nationality': 'Mali',
        'second_nationality': 'Suede', 'status': 'active'
    },
    'Mamadou Samassa': {
        'current_club': 'Laval', 'current_league': 'Ligue 2',
        'age': 36, 'height_cm': 198, 'foot': 'right', 'nationality': 'Mali',
        'second_nationality': 'France', 'status': 'active'
    },
    'Mamadou Camara': {
        'current_club': 'Laval', 'current_league': 'Ligue 2',
        'age': 25, 'height_cm': 189, 'foot': 'right', 'nationality': 'Mali',
        'second_nationality': 'France', 'status': 'active'
    },

    # --- BATCH 4 ---
    'Ousmane Camara': {
        'current_club': 'Angers', 'current_league': 'Ligue 1',
        'age': 23, 'height_cm': 197, 'foot': 'right', 'nationality': 'Mali',
        'second_nationality': 'France', 'status': 'active'
    },
    'Fode Doucoure': {
        'current_club': 'Le Havre', 'current_league': 'Ligue 1',
        'age': 25, 'height_cm': 172, 'foot': 'right', 'nationality': 'Mali',
        'status': 'active'
    },
    'Mamadou Fofana DF': {
        'current_club': 'New England Revolution', 'current_league': 'MLS',
        'age': 28, 'height_cm': 186, 'foot': 'both', 'nationality': 'Mali',
        'status': 'active'
    },
    'Moussa Marega': {
        'current_club': 'Al-Diraiyah FC', 'current_league': 'Saudi First Division',
        'age': 34, 'height_cm': 183, 'foot': 'right', 'nationality': 'Mali',
        'second_nationality': 'France', 'status': 'injured'
    },
    'Molla Wague': {
        'current_club': 'Isola Capo Rizzuto', 'current_league': 'Eccellenza Italie',
        'age': 35, 'height_cm': 191, 'foot': 'right', 'nationality': 'Mali',
        'second_nationality': 'France', 'status': 'active'
    },
    'Daouda Guindo': {
        'current_club': 'Brest', 'current_league': 'Ligue 1',
        'age': 23, 'height_cm': 183, 'foot': 'left', 'nationality': 'Mali',
        'status': 'active'
    },
    'Cheick Tidiane Diabate': {
        'current_club': 'Free Agent', 'current_league': '',
        'age': 37, 'height_cm': 194, 'foot': 'right', 'nationality': 'Mali',
        'status': 'retired'  # sans club depuis 3 ans
    },
    'Kalifa Coulibaly': {
        'current_club': 'Free Agent', 'current_league': '',
        'age': 34, 'height_cm': 197, 'foot': 'right', 'nationality': 'Mali',
        'second_nationality': 'France', 'status': 'inactive'
    },
    'Yacouba Sylla': {
        'current_club': 'Free Agent', 'current_league': '',
        'age': 35, 'height_cm': 184, 'foot': 'right', 'nationality': 'Mali',
        'second_nationality': 'France', 'status': 'inactive'
    },
    'Youssouf Koita': {
        'current_club': 'AS Real Bamako', 'current_league': 'Ligue 1 Mali',
        'age': 25, 'height_cm': 187, 'foot': 'right', 'nationality': 'Mali',
        'status': 'active'
    },

    # --- BATCH 5 ---
    'Djigui Diarra': {
        'current_club': 'Young Africans', 'current_league': 'Premier League Tanzanie',
        'age': 31, 'height_cm': 180, 'foot': 'right', 'nationality': 'Mali',
        'status': 'active'
    },
    'Cheick Traore': {
        'current_club': 'Paris 13 Atletico', 'current_league': 'National',
        'age': 30, 'height_cm': 175, 'foot': 'right', 'nationality': 'Mali',
        'second_nationality': 'France', 'status': 'active'
    },
    'Ibrahima Cisse': {
        'current_club': 'FC Aarau', 'current_league': 'Challenge League Suisse',
        'position': 'DF', 'age': 25, 'height_cm': 196, 'foot': 'right',
        'nationality': 'Mali', 'second_nationality': 'France', 'status': 'active'
    },
    'Ousmane Diallo': {
        'current_club': 'Renaissance Zemamra', 'current_league': 'Botola Pro Maroc',
        'position': 'DF', 'age': 26, 'height_cm': 181, 'foot': 'left',
        'nationality': 'Mali', 'status': 'active'
    },
    'Lassana Ndiaye': {
        'current_club': 'Free Agent', 'current_league': '',
        'position': 'FW', 'age': 25, 'nationality': 'Mali',
        'status': 'inactive'
    },

    # --- Joueurs non verifiables en ligne (ligues locales) - garder tels quels mais enrichir ---
    'Lassana Fane': {
        'current_club': 'Free Agent', 'current_league': '',
        'status': 'retired'  # reconverti entraineur adjoint Djoliba
    },
}

print("--- Mise a jour des joueurs ---\n")
updated = 0
not_found = 0
for name, data in updates.items():
    if name in pid_map:
        try:
            update_player(pid_map[name], **data)
            updated += 1
            club = data.get('current_club', '?')
            league = data.get('current_league', '')
            status = data.get('status', 'active')
            extra = f" [{status}]" if status != 'active' else ""
            print(f"  OK {name:30s} -> {club} ({league}){extra}")
        except Exception as e:
            print(f"  ERR {name}: {e}")
    else:
        not_found += 1
        print(f"  ?? {name} non trouve")

print(f"\n{updated} joueurs mis a jour, {not_found} non trouves.")

# ============================================================
# 2. MAMADOU FOFANA (ID 17) - doublon avec Mamadou Fofana DF (ID 87)
# Le vrai Mamadou Fofana malien est defenseur au New England Revolution
# ID 17 est une erreur (jamais joue a Lens en tant que MF)
# ============================================================
print("\n--- Correction doublon Mamadou Fofana ---")
fofana_mf_id = pid_map.get('Mamadou Fofana')
if fofana_mf_id:
    # Supprimer les stats liees a ce doublon
    supabase.table('season_stats').delete().eq('player_id', fofana_mf_id).execute()
    supabase.table('transfers').delete().eq('player_id', fofana_mf_id).execute()
    supabase.table('players').delete().eq('id', fofana_mf_id).execute()
    print(f"  Supprime 'Mamadou Fofana' (ID {fofana_mf_id}) - doublon de 'Mamadou Fofana DF' (ID {pid_map.get('Mamadou Fofana DF')})")

# ============================================================
# 3. BAKARY SACKO (ID 47) - doublon de Falaye Sacko (ID 6)
# ============================================================
print("\n--- Correction doublon Bakary Sacko ---")
sacko_id = pid_map.get('Bakary Sacko')
if sacko_id:
    supabase.table('season_stats').delete().eq('player_id', sacko_id).execute()
    supabase.table('transfers').delete().eq('player_id', sacko_id).execute()
    supabase.table('players').delete().eq('id', sacko_id).execute()
    print(f"  Supprime 'Bakary Sacko' (ID {sacko_id}) - doublon de 'Falaye Sacko' (ID {pid_map.get('Falaye Sacko')})")

# ============================================================
# 4. SIDY SARR - Senegalais, pas malien -> supprimer
# ============================================================
print("\n--- Suppression joueurs non maliens ---")
sarr_id = pid_map.get('Sidy Sarr')
if sarr_id:
    supabase.table('season_stats').delete().eq('player_id', sarr_id).execute()
    supabase.table('transfers').delete().eq('player_id', sarr_id).execute()
    supabase.table('players').delete().eq('id', sarr_id).execute()
    print(f"  Supprime 'Sidy Sarr' (ID {sarr_id}) - joueur senegalais, pas malien")

# MOUSSA KONATE - Senegalais, pas malien
konate_id = pid_map.get('Moussa Konate')
if konate_id:
    supabase.table('season_stats').delete().eq('player_id', konate_id).execute()
    supabase.table('transfers').delete().eq('player_id', konate_id).execute()
    supabase.table('players').delete().eq('id', konate_id).execute()
    print(f"  Supprime 'Moussa Konate' (ID {konate_id}) - joueur senegalais, pas malien")

# ============================================================
# 5. JOUEURS NON VERIFIABLES - marquer comme non confirmes
# ============================================================
print("\n--- Joueurs non verifiables (ligues locales) ---")
unverifiable = ['Amadou Haidara B', 'Ibrahim Toure', 'Saloum Fane']
for name in unverifiable:
    if name in pid_map:
        print(f"  ?? {name} (ID {pid_map[name]}) - non trouvable en ligne, donnees non confirmees")

# ============================================================
# 6. AJOUT TRANSFERTS HISTORIQUES (nouveaux)
# ============================================================
print("\n--- Ajout transferts ---")
new_transfers = [
    ('Moussa Diarra', '2024-07-01', 'Toulouse', 'Alaves', 'transfer', '2024-25'),
    ('Moussa Diarra', '2026-01-15', 'Alaves', 'Anderlecht', 'loan', '2025-26'),
    ('Ibrahima Kone', '2023-08-01', 'Lorient', 'UD Almeria', 'transfer', '2023-24'),
    ('Massadio Haidara', '2025-07-03', 'Brest', 'Kocaelispor', 'free', '2025-26'),
    ('Fousseni Diabate', '2025-09-08', 'Lausanne', 'Kasimpasa', 'free', '2025-26'),
    ('Adama Traore Malouda', '2025-08-15', 'Ferencvaros', 'Genclerbirligi', 'transfer', '2025-26'),
    ('Daouda Guindo', '2025-08-26', 'RB Salzburg', 'Brest', 'free', '2025-26'),
    ('Youssouf Koita', '2025-08-05', 'Djoliba AC', 'AS Real Bamako', 'free', '2025-26'),
    ('Ibrahima Cisse', '2026-01-15', 'Schalke 04', 'FC Aarau', 'free', '2025-26'),
    ('Cheick Traore', '2025-07-17', 'Al-Faisaly', 'Paris 13 Atletico', 'free', '2025-26'),
    ('Ousmane Diallo', '2025-07-26', 'Djoliba AC', 'Renaissance Zemamra', 'transfer', '2025-26'),
    ('Mamadou Sangare', '2025-08-20', 'Rapid Vienne', 'Lens', 'transfer', '2025-26'),
    ('Ibrahima Sissoko', '2026-01-12', 'VfL Bochum', 'Nantes', 'transfer', '2025-26'),
    ('Amadou Dante', '2025-07-01', 'Sturm Graz', 'Arouca', 'transfer', '2025-26'),
    ('Gaoussou Diarra', '2025-07-04', 'Istanbulspor', 'Feyenoord', 'transfer', '2025-26'),
    ('Moussa Marega', '2024-08-04', 'Free Agent', 'Al-Diraiyah FC', 'free', '2024-25'),
    ('Ousmane Camara', '2022-08-16', 'Free Agent', 'Angers', 'free', '2022-23'),
    ('Fode Doucoure', '2025-07-22', 'Red Star FC', 'Le Havre', 'free', '2025-26'),
]

t_added = 0
for name, date, cf, ct, tt, season in new_transfers:
    if name not in pid_map:
        continue
    try:
        supabase.table('transfers').insert({
            'player_id': pid_map[name],
            'date': date,
            'club_from': cf,
            'club_to': ct,
            'transfer_type': tt,
            'season': season,
            'source': 'web_verified'
        }).execute()
        t_added += 1
        print(f"  {name:28s} | {cf} -> {ct}")
    except Exception as e:
        print(f"  ERR {name}: {e}")

print(f"\n{t_added} transferts ajoutes.")

# ============================================================
# RESUME FINAL
# ============================================================
from database.db_supabase import get_db_summary
summary = get_db_summary()
print(f"\n=== RESUME FINAL ===")
for k, v in summary.items():
    print(f"  {k:25s}: {v}")
