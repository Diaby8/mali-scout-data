"""
Mali National Football Team (Les Aigles) - Head Coaches History

Data compiled from multiple web sources (March 2026):
- Wikipedia (en + fr)
- Transfermarkt
- National-Football-Teams.com
- CAF Online
- FEMAFOOT (Malian Football Federation)
- Various sports news outlets

Format:
    (coach_name, start_date, end_date, nationality, wins, draws, losses, notable_achievements)

Notes:
- W/D/L = None when stats could not be verified from reliable sources
- Dates use 'YYYY-MM' or 'YYYY-MM-DD' when known, 'YYYY' otherwise
- Caretaker/interim coaches are marked with '(interim)' in their name
- Focus is on coaches from 2000 onwards, with select earlier coaches included
"""

MALI_COACHES_HISTORY = [
    # ==================== PRE-2000 (selected notable coaches) ====================

    (
        'Kidian Diallo',
        '1982', '1989',
        'Malian',
        None, None, None,
        'Longest-serving Malian coach in the early era'
    ),
    (
        'Karl-Heinz Weigang',
        '1990', '1994',
        'German',
        None, None, None,
        'Experienced international coach; also managed Ghana, Gabon, Vietnam'
    ),

    # ==================== 2000 ONWARDS (detailed) ====================

    (
        'Romano Matte',
        '2000-07', '2001-06',
        'Italian',
        None, None, None,
        'Contract July 2000 - June 2001'
    ),
    (
        'Henryk Kasperczak',  # 1st stint
        '2001-07', '2002-02',
        'Polish',
        7, 4, 2,
        'AFCON 2002: 4th place (semi-finalist, host country Mali); 13 matches total'
    ),
    (
        'Christian Dalger',
        '2002-03', '2003-09',
        'French',
        6, 0, 5,
        'Qualified Mali for AFCON 2004; 2002: 2W 3L, 2003: 4W 2L'
    ),
    (
        'Henri Stambouli',
        '2003-09', '2004-03',
        'French',
        None, None, None,
        'AFCON 2004: 4th place (semi-finalist); ~8 matches, 2.00 pts/match'
    ),
    (
        'Alain Moizan',
        '2004-04', '2004-07',
        'French',
        None, None, None,
        'Short interim tenure after Stambouli'
    ),
    (
        'Mamadou Keita',
        '2004-08', '2005-02',
        'Malian',
        None, None, None,
        'Malian football legend (d. 2008); brief tenure'
    ),
    (
        'Pierre Lechantre',
        '2005-03', '2006-07',
        'French',
        None, None, None,
        'Previously led Cameroon to AFCON 2000 title; limited success with Mali'
    ),
    (
        'Jean-Francois Jodar',
        '2006-07', '2008-03',
        'French',
        None, None, None,
        'Led Mali through 2008 AFCON qualifiers and tournament'
    ),
    (
        'Stephen Keshi',
        '2008-04', '2010-01',
        'Nigerian',
        None, None, None,
        'AFCON 2010: group stage exit; sacked Jan 2010. Later won AFCON 2013 with Nigeria'
    ),
    (
        'Alain Giresse',  # 1st stint
        '2010-02', '2012-05',
        'French',
        None, None, None,
        'AFCON 2012: 3rd place; left due to contract dispute with federation'
    ),
    (
        'Amadou Pathe Diallo (interim)',
        '2012-05', '2012-07',
        'Malian',
        None, None, None,
        'Caretaker between Giresse and Carteron'
    ),
    (
        'Patrice Carteron',
        '2012-07', '2013-05',
        'French',
        None, None, None,
        'AFCON 2013: 3rd place; Mali reached highest FIFA ranking (23rd, June 2013)'
    ),
    (
        'Henryk Kasperczak',  # 2nd stint
        '2014-01', '2015-03',
        'Polish',
        None, None, None,
        'AFCON 2015: quarter-finals; dismissed March 2015'
    ),
    (
        'Alain Giresse',  # 2nd stint
        '2015-03', '2017-09',
        'French',
        None, None, None,
        'AFCON 2017: group stage; resigned Sept 2017 after WC qualifier draw vs Morocco'
    ),
    (
        'Mohamed Magassouba',
        '2017-09', '2022-04',
        'Malian',
        16, None, None,
        'Interim 2017-2019, permanent Oct 2019. AFCON 2019: R16. '
        'AFCON 2021: R16. Best defense in WCQ (0 goals conceded, 5W 1D). '
        '36 matches, 16 wins (44% win rate). Fired April 2022'
    ),
    (
        'Eric Sekou Chelle',
        '2022-05', '2024-06-13',
        'Franco-Malian',
        14, None, None,
        'AFCON 2023 (Jan 2024): quarter-finals (topped group ahead of South Africa). '
        '26 matches, 14 wins (54% win rate). Dismissed June 2024 after poor WCQ results. '
        'Later appointed Nigeria coach'
    ),
    (
        'Tom Saintfiet',
        '2024-08-29', 'present',
        'Belgian',
        9, 7, 3,
        'AFCON 2025 qualifying: 1st in Group I (4W 2D, best defense in Africa). '
        'AFCON 2025: quarter-finals (unbeaten until QF loss 0-1 vs Senegal). '
        '19 matches: 9W 7D 3L. Contract until Aug 2026. '
        'Previously led Gambia to first-ever AFCON (2021 QF)'
    ),
]


# ==================== AFCON RESULTS SUMMARY ====================
MALI_AFCON_RESULTS = {
    2002: {'finish': '4th place', 'coach': 'Henryk Kasperczak', 'note': 'Host country. Lost SF to Cameroon 0-3, 3rd place match lost to Nigeria 0-1'},
    2004: {'finish': '4th place', 'coach': 'Henri Stambouli', 'note': 'Lost SF, lost 3rd place match to Nigeria'},
    2008: {'finish': 'Group stage / 1st round', 'coach': 'Jean-Francois Jodar', 'note': ''},
    2010: {'finish': 'Group stage', 'coach': 'Stephen Keshi', 'note': 'Keshi sacked after tournament'},
    2012: {'finish': '3rd place', 'coach': 'Alain Giresse', 'note': 'Best result at the time'},
    2013: {'finish': '3rd place', 'coach': 'Patrice Carteron', 'note': 'Beat Ghana 3-1 in 3rd place match. Lost SF to Nigeria 1-4'},
    2015: {'finish': 'Quarter-finals', 'coach': 'Henryk Kasperczak', 'note': ''},
    2017: {'finish': 'Group stage', 'coach': 'Alain Giresse', 'note': ''},
    2019: {'finish': 'Round of 16', 'coach': 'Mohamed Magassouba', 'note': 'Lost R16 to Ivory Coast'},
    2021: {'finish': 'Round of 16', 'coach': 'Mohamed Magassouba', 'note': 'Tournament held Jan-Feb 2022'},
    2023: {'finish': 'Quarter-finals', 'coach': 'Eric Chelle', 'note': 'Tournament held Jan-Feb 2024. Topped group. Lost QF to Ivory Coast in extra time'},
    2025: {'finish': 'Quarter-finals', 'coach': 'Tom Saintfiet', 'note': 'Lost QF 0-1 to Senegal. Unbeaten in group + R16'},
}


if __name__ == '__main__':
    print("=" * 100)
    print("MALI NATIONAL FOOTBALL TEAM - HEAD COACHES HISTORY")
    print("=" * 100)
    print()
    print(f"{'Coach':<35} {'Tenure':<25} {'Nationality':<15} {'W':>3} {'D':>3} {'L':>3}  Notable Achievements")
    print("-" * 140)
    for coach in MALI_COACHES_HISTORY:
        name, start, end, nat, w, d, l, achievements = coach
        tenure = f"{start} - {end}"
        w_str = str(w) if w is not None else '-'
        d_str = str(d) if d is not None else '-'
        l_str = str(l) if l is not None else '-'
        # Truncate achievements for display
        ach_short = achievements[:60] + '...' if len(achievements) > 60 else achievements
        print(f"{name:<35} {tenure:<25} {nat:<15} {w_str:>3} {d_str:>3} {l_str:>3}  {ach_short}")

    print()
    print("=" * 100)
    print("MALI AT AFCON - RESULTS SUMMARY")
    print("=" * 100)
    print()
    for year, data in sorted(MALI_AFCON_RESULTS.items()):
        print(f"  AFCON {year}: {data['finish']:<20} Coach: {data['coach']:<25} {data['note']}")
