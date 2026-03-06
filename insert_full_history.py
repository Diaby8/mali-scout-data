# -*- coding: utf-8 -*-
"""Insert full verified match history + coaches for Mali national team.
Source: national-football-teams.com (verified March 2026)."""
from database.supabase_client import supabase

print("=== INSERTION HISTORIQUE COMPLET MATCHS + COACHS ===\n")

# ============================================
# MATCHS 2015-2023 (2024-2026 deja inseres)
# ============================================

matches = [
    # === 2019 ===
    ('2015-01-14', 'Afrique du Sud', 0, 3, 'L', 'Amical'),
    ('2015-01-20', 'Cameroun', 1, 1, 'D', 'CAN 2015 - Phase de groupes'),
    ('2015-01-24', 'Cote d Ivoire', 1, 1, 'D', 'CAN 2015 - Phase de groupes'),
    ('2015-01-28', 'Guinee', 1, 1, 'D', 'CAN 2015 - Phase de groupes'),
    ('2015-03-25', 'Gabon', 3, 4, 'L', 'Amical'),
    ('2015-03-31', 'Ghana', 1, 1, 'D', 'Amical'),
    ('2015-06-06', 'Libye', 2, 2, 'D', 'Amical'),
    ('2015-06-13', 'Soudan du Sud', 2, 0, 'W', 'Qualif CAN 2017'),
    ('2015-06-20', 'Guinee-Bissau', 1, 1, 'D', 'Qualif CHAN 2016'),
    ('2015-07-05', 'Guinee-Bissau', 3, 1, 'W', 'Qualif CHAN 2016'),
    ('2015-09-06', 'Benin', 1, 1, 'D', 'Qualif CAN 2017'),
    ('2015-10-09', 'Burkina Faso', 4, 1, 'W', 'Amical'),
    ('2015-10-18', 'Mauritanie', 2, 1, 'W', 'Qualif CHAN 2016'),
    ('2015-10-24', 'Mauritanie', 1, 1, 'D', 'Qualif CHAN 2016'),
    ('2015-11-14', 'Botswana', 1, 2, 'L', 'Qualif CM 2018'),
    ('2015-11-17', 'Botswana', 2, 0, 'W', 'Qualif CM 2018'),

    # === 2016 ===
    ('2016-01-19', 'Ouganda', 2, 2, 'D', 'CHAN 2016 - Phase de groupes'),
    ('2016-01-23', 'Zimbabwe', 1, 0, 'W', 'CHAN 2016 - Phase de groupes'),
    ('2016-01-27', 'Zambie', 0, 0, 'D', 'CHAN 2016 - Phase de groupes'),
    ('2016-01-31', 'Tunisie', 2, 1, 'W', 'CHAN 2016 - Quarts de finale'),
    ('2016-02-04', 'Cote d Ivoire', 1, 0, 'W', 'CHAN 2016 - Demi-finale'),
    ('2016-02-07', 'RD Congo', 0, 3, 'L', 'CHAN 2016 - Finale'),
    ('2016-03-25', 'Guinee Equatoriale', 1, 0, 'W', 'Qualif CAN 2017'),
    ('2016-03-28', 'Guinee Equatoriale', 1, 0, 'W', 'Qualif CAN 2017'),
    ('2016-05-27', 'Nigeria', 0, 1, 'L', 'Amical'),
    ('2016-06-04', 'Soudan du Sud', 3, 0, 'W', 'Qualif CAN 2017'),
    ('2016-09-04', 'Benin', 5, 2, 'W', 'Qualif CAN 2017'),
    ('2016-10-08', 'Cote d Ivoire', 1, 3, 'L', 'Qualif CM 2018'),
    ('2016-11-12', 'Gabon', 0, 0, 'D', 'Qualif CM 2018'),

    # === 2017 ===
    ('2017-01-07', 'Burkina Faso', 1, 2, 'L', 'Amical'),
    ('2017-01-17', 'Egypte', 0, 0, 'D', 'CAN 2017 - Phase de groupes'),
    ('2017-01-21', 'Ghana', 0, 1, 'L', 'CAN 2017 - Phase de groupes'),
    ('2017-01-25', 'Ouganda', 1, 1, 'D', 'CAN 2017 - Phase de groupes'),
    ('2017-06-10', 'Gabon', 2, 1, 'W', 'Qualif CAN 2019'),
    ('2017-07-15', 'Gambie', 0, 0, 'D', 'Qualif CHAN 2018'),
    ('2017-07-22', 'Gambie', 4, 0, 'W', 'Qualif CHAN 2018'),
    ('2017-08-06', 'Senegal', 1, 1, 'D', 'Amical'),
    ('2017-08-12', 'Mauritanie', 2, 2, 'D', 'Qualif CHAN 2018'),
    ('2017-08-19', 'Mauritanie', 0, 1, 'L', 'Qualif CHAN 2018'),
    ('2017-09-01', 'Maroc', 0, 6, 'L', 'Qualif CM 2018'),
    ('2017-09-05', 'Maroc', 0, 0, 'D', 'Qualif CM 2018'),
    ('2017-10-06', 'Cote d Ivoire', 0, 0, 'D', 'Qualif CM 2018'),
    ('2017-11-11', 'Gabon', 0, 0, 'D', 'Qualif CM 2018'),

    # === 2018 ===
    ('2018-03-23', 'Japon', 1, 1, 'D', 'Amical'),
    ('2018-09-09', 'Soudan du Sud', 3, 0, 'W', 'Qualif CAN 2019'),
    ('2018-10-12', 'Burundi', 0, 0, 'D', 'Qualif CAN 2019'),
    ('2018-10-16', 'Burundi', 1, 1, 'D', 'Qualif CAN 2019'),
    ('2018-11-17', 'Gabon', 1, 0, 'W', 'Qualif CAN 2019'),

    # === 2019 ===
    ('2019-03-23', 'Soudan du Sud', 3, 0, 'W', 'Qualif CAN 2019'),
    ('2019-03-26', 'Senegal', 1, 2, 'L', 'Amical'),
    ('2019-06-14', 'Cameroun', 1, 1, 'D', 'Amical'),
    ('2019-06-16', 'Algerie', 2, 3, 'L', 'Amical'),
    ('2019-06-24', 'Mauritanie', 4, 1, 'W', 'CAN 2019 - Phase de groupes'),
    ('2019-06-28', 'Tunisie', 1, 1, 'D', 'CAN 2019 - Phase de groupes'),
    ('2019-07-02', 'Angola', 0, 1, 'L', 'CAN 2019 - Phase de groupes'),
    ('2019-07-08', 'Cote d Ivoire', 0, 1, 'L', 'CAN 2019 - Huitiemes de finale'),
    ('2019-07-27', 'Guinee-Bissau', 4, 0, 'W', 'Qualif CHAN 2020'),
    ('2019-09-05', 'Arabie Saoudite', 1, 1, 'D', 'Amical'),
    ('2019-09-21', 'Mauritanie', 0, 0, 'D', 'Qualif CHAN 2020'),
    ('2019-10-13', 'Afrique du Sud', 1, 2, 'L', 'Amical'),
    ('2019-10-20', 'Mauritanie', 2, 0, 'W', 'Qualif CHAN 2020'),
    ('2019-11-14', 'Guinee', 2, 2, 'D', 'Qualif CAN 2022'),
    ('2019-11-17', 'Tchad', 2, 0, 'W', 'Qualif CAN 2022'),

    # === 2020 ===
    ('2020-10-09', 'Ghana', 3, 0, 'W', 'Amical'),
    ('2020-11-13', 'Namibie', 1, 0, 'W', 'Qualif CAN 2022'),
    ('2020-11-17', 'Namibie', 2, 1, 'W', 'Qualif CAN 2022'),

    # === 2021 ===
    # CHAN 2020 (joue en 2021)
    ('2021-01-16', 'Burkina Faso', 1, 0, 'W', 'CHAN 2020 - Phase de groupes'),
    ('2021-01-20', 'Cameroun', 1, 1, 'D', 'CHAN 2020 - Phase de groupes'),
    ('2021-01-24', 'Zimbabwe', 1, 0, 'W', 'CHAN 2020 - Phase de groupes'),
    ('2021-01-30', 'Congo', 0, 0, 'D', 'CHAN 2020 - Quarts de finale'),
    ('2021-02-03', 'Guinee', 0, 0, 'D', 'CHAN 2020 - Demi-finale'),
    ('2021-02-07', 'Maroc', 0, 2, 'L', 'CHAN 2020 - Finale'),
    # Qualif CAN 2022
    ('2021-03-24', 'Guinee', 0, 1, 'L', 'Qualif CAN 2022'),
    ('2021-03-28', 'Tchad', 3, 0, 'W', 'Qualif CAN 2022'),
    # Amicaux
    ('2021-06-06', 'Algerie', 0, 1, 'L', 'Amical'),
    ('2021-06-11', 'RD Congo', 1, 1, 'D', 'Amical'),
    ('2021-06-15', 'Tunisie', 0, 1, 'L', 'Amical'),
    # Qualif CM 2022
    ('2021-09-01', 'Rwanda', 1, 0, 'W', 'Qualif CM 2022'),
    ('2021-09-06', 'Ouganda', 0, 0, 'D', 'Qualif CM 2022'),
    ('2021-10-07', 'Kenya', 5, 0, 'W', 'Qualif CM 2022'),
    ('2021-10-10', 'Kenya', 1, 0, 'W', 'Qualif CM 2022'),
    ('2021-11-11', 'Rwanda', 3, 0, 'W', 'Qualif CM 2022'),
    ('2021-11-14', 'Ouganda', 1, 0, 'W', 'Qualif CM 2022'),

    # === 2022 ===
    # CAN 2022 (Cameroun)
    ('2022-01-12', 'Tunisie', 1, 0, 'W', 'CAN 2022 - Phase de groupes'),
    ('2022-01-16', 'Gambie', 1, 1, 'D', 'CAN 2022 - Phase de groupes'),
    ('2022-01-20', 'Mauritanie', 2, 0, 'W', 'CAN 2022 - Phase de groupes'),
    ('2022-01-26', 'Guinee Equatoriale', 0, 0, 'D', 'CAN 2022 - Huitiemes de finale'),
    # Qualif CM 2022 - Barrages
    ('2022-03-25', 'Tunisie', 0, 1, 'L', 'Qualif CM 2022 - Barrage'),
    ('2022-03-29', 'Tunisie', 0, 0, 'D', 'Qualif CM 2022 - Barrage'),
    # Qualif CAN 2023
    ('2022-06-04', 'Congo', 4, 0, 'W', 'Qualif CAN 2023'),
    ('2022-06-09', 'Soudan du Sud', 3, 1, 'W', 'Qualif CAN 2023'),
    # Qualif CHAN 2022
    ('2022-08-27', 'Sierra Leone', 2, 1, 'W', 'Qualif CHAN 2022'),
    ('2022-09-03', 'Sierra Leone', 2, 0, 'W', 'Qualif CHAN 2022'),
    # Amicaux
    ('2022-09-23', 'Zambie', 1, 0, 'W', 'Amical'),
    ('2022-09-26', 'Zambie', 0, 0, 'D', 'Amical'),
    ('2022-11-16', 'Algerie', 1, 1, 'D', 'Amical'),

    # === 2023 ===
    # CHAN 2022 (joue en 2023)
    ('2023-01-16', 'Angola', 3, 3, 'D', 'CHAN 2022 - Phase de groupes'),
    ('2023-01-24', 'Mauritanie', 0, 1, 'L', 'CHAN 2022 - Phase de groupes'),
    # Qualif CAN 2023
    ('2023-03-24', 'Gambie', 2, 0, 'W', 'Qualif CAN 2023'),
    ('2023-03-28', 'Gambie', 0, 1, 'L', 'Qualif CAN 2023'),
    ('2023-06-18', 'Congo', 2, 0, 'W', 'Qualif CAN 2023'),
    ('2023-09-08', 'Soudan du Sud', 4, 0, 'W', 'Qualif CAN 2023'),
    # Amicaux
    ('2023-09-12', 'Cote d Ivoire', 0, 0, 'D', 'Amical'),
    ('2023-10-13', 'Ouganda', 1, 0, 'W', 'Amical'),
    ('2023-10-17', 'Arabie Saoudite', 3, 1, 'W', 'Amical'),
    # Qualif CM 2026
    ('2023-11-17', 'Tchad', 3, 1, 'W', 'Qualif CM 2026'),
    ('2023-11-20', 'Centrafrique', 1, 1, 'D', 'Qualif CM 2026'),
]

print(f"Insertion de {len(matches)} matchs (2015-2023)...\n")

added = 0
skipped = 0
for date, opponent, gf, ga, result, comp in matches:
    # Check if already exists
    existing = supabase.table('national_matches').select('id').eq('date', date).eq('opponent', opponent).execute()
    if existing.data:
        skipped += 1
        continue

    data = {
        'date': date,
        'opponent': opponent,
        'goals_for': gf,
        'goals_against': ga,
        'result': result,
        'competition': comp,
        'team': 'Mali A',
    }
    try:
        supabase.table('national_matches').insert(data).execute()
        added += 1
        print(f"  {date} | Mali {gf}-{ga} {opponent:20s} | {comp}")
    except Exception as e:
        print(f"  ERR {date} vs {opponent}: {e}")

print(f"\n{added} matchs ajoutes, {skipped} deja existants.")

# ============================================
# TOTAL MATCHS
# ============================================
total = supabase.table('national_matches').select('id', count='exact').execute()
print(f"Total matchs dans la base: {total.count}")

# ============================================
# HISTORIQUE DES COACHS (verifie)
# ============================================
print("\n=== INSERTION HISTORIQUE DES COACHS ===\n")

# Creer la table si elle n'existe pas
# (doit etre fait via SQL Editor dans Supabase)

coaches = [
    {
        'name': 'Mohamed Magassouba',
        'nationality': 'Mali',
        'start_date': '2017-09',
        'end_date': '2022-04',
        'team': 'Mali A',
        'matches': 36,
        'wins': 16,
        'achievements': 'Interim 2017-19, permanent oct 2019. CAN 2019 - 8emes, CHAN 2020 - Finaliste, CAN 2022 - 8emes. Meilleure defense en qualifs CM (0 but encaisse)',
    },
    {
        'name': 'Eric Sekou Chelle',
        'nationality': 'Mali/France',
        'start_date': '2022-05',
        'end_date': '2024-06-13',
        'team': 'Mali A',
        'matches': 26,
        'wins': 14,
        'achievements': 'CAN 2024 - Quarts de finale (1er du groupe devant Afrique du Sud). 54% de victoires. Limoge apres mauvais resultats en qualifs CM 2026',
    },
    {
        'name': 'Tom Saintfiet',
        'nationality': 'Belgique',
        'start_date': '2024-08-29',
        'end_date': None,
        'team': 'Mali A',
        'matches': 19,
        'wins': 9,
        'draws': 7,
        'losses': 3,
        'achievements': 'Qualif CAN 2025 reussie (1er du groupe I). CAN 2025 - Quarts de finale (invaincu jusqu en QF, defaite 0-1 vs Senegal). Contrat jusqu aout 2026',
    },
]

try:
    coaches_added = 0
    for c in coaches:
        # Check if exists
        existing = supabase.table('coaches_history').select('id').eq('name', c['name']).eq('start_date', c['start_date']).execute()
        if existing.data:
            continue
        supabase.table('coaches_history').insert(c).execute()
        coaches_added += 1
        end_str = c['end_date'] or 'en poste'
        print(f"  {c['name']:25s} | {c['start_date']} - {end_str} | {c.get('achievements', '')}")

    print(f"\n{coaches_added} coachs ajoutes.")
except Exception as e:
    print(f"\nERREUR: {e}")
    print("La table coaches_history n'existe pas encore.")
    print("Execute ce SQL dans Supabase SQL Editor:")
    print("  -> Voir database/schema_coaches.sql")
