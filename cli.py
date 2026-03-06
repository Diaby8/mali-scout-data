"""
Mali Scout Data - Interface Interactive
Usage: python cli.py
"""

import sys
import os
import json
import csv
from datetime import datetime

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.text import Text
from rich.columns import Columns
from rich import box

from database.db_supabase import *
from database.supabase_client import supabase

console = Console()

# Couleurs Mali
VERT = "#14B53A"
OR = "#FCD116"
ROUGE = "#CE1126"


def banner():
    console.clear()
    console.print(Panel(
        Text("MALI SCOUT DATA", style=f"bold {OR}", justify="center"),
        subtitle="Base de scouting des joueurs maliens",
        border_style=VERT,
        box=box.DOUBLE,
        padding=(1, 4),
    ))
    console.print()


def menu_principal():
    """Menu principal."""
    while True:
        banner()
        summary = get_db_summary()
        console.print(f"  [bold]{summary.get('players', 0)}[/bold] joueurs | "
                      f"[bold]{summary.get('season_stats', 0)}[/bold] stats saison | "
                      f"[bold]{summary.get('match_stats', 0)}[/bold] stats match\n")

        options = [
            ("", "[bold white]--- JOUEURS ---[/bold white]"),
            ("1", "Voir tous les joueurs"),
            ("2", "Chercher un joueur"),
            ("3", "Fiche complete d'un joueur"),
            ("4", "Ajouter un joueur"),
            ("5", "Modifier un joueur"),
            ("6", "Ajouter des stats saison"),
            ("7", "Ajouter un match"),
            ("", ""),
            ("", "[bold white]--- EQUIPE NATIONALE ---[/bold white]"),
            ("8", "Les Aigles - Vue d'ensemble"),
            ("9", "Resultats des matchs"),
            ("10", "Ajouter un match equipe nationale"),
            ("11", "Convocations / Compositions"),
            ("12", "Joueurs par categorie EN (A, U23, U20, U17, binationaux)"),
            ("13", "Historique des coachs"),
            ("", ""),
            ("", "[bold white]--- OUTILS ---[/bold white]"),
            ("14", "Classements (top buteurs, passeurs...)"),
            ("15", "Scraper FBref (chercher des joueurs)"),
            ("16", "Exporter les donnees"),
            ("17", "Generer un visuel"),
            ("18", "Requete SQL libre"),
            ("0", "Quitter"),
        ]

        table = Table(show_header=False, box=box.SIMPLE, border_style=VERT)
        table.add_column(style=f"bold {OR}", width=4)
        table.add_column()
        for num, label in options:
            if num == "":
                table.add_row("", label)
            else:
                table.add_row(f"[{num}]", label)
        console.print(table)

        valid = [str(i) for i in range(19)]
        choix = Prompt.ask("\nChoix", choices=valid, default="0")

        actions = {
            "1": page_joueurs,
            "2": page_recherche,
            "3": page_fiche_joueur,
            "4": page_ajouter_joueur,
            "5": page_modifier_joueur,
            "6": page_ajouter_stats,
            "7": page_ajouter_match,
            "8": page_equipe_nationale,
            "9": page_resultats_nationaux,
            "10": page_ajouter_match_national,
            "11": page_convocations,
            "12": page_categories_en,
            "13": page_historique_coachs,
            "14": page_classements,
            "15": page_scraper,
            "16": page_exporter,
            "17": page_visuel,
            "18": page_sql,
            "0": lambda: sys.exit(0),
        }

        if choix in actions:
            try:
                actions[choix]()
            except KeyboardInterrupt:
                continue
            except Exception as e:
                console.print(f"\n[red]Erreur: {e}[/red]")
                Prompt.ask("\nAppuie sur Entree pour continuer")


# ============================================
# 1. VOIR TOUS LES JOUEURS
# ============================================

def page_joueurs():
    banner()
    console.print("[bold]Tous les joueurs[/bold]\n")

    players = get_all_players()
    if not players:
        console.print("[dim]Aucun joueur dans la base.[/dim]")
        Prompt.ask("\nAppuie sur Entree")
        return

    # Filtre optionnel
    filtre = Prompt.ask(
        "Filtrer par [dim](poste/ligue/club/mali_a/u23/u20/u17/binational/tous)[/dim]",
        default="tous"
    )

    nt_filter_map = {"mali_a": "mali_a", "u23": "mali_u23", "u20": "mali_u20",
                     "u17": "mali_u17", "binational": "binational"}

    if filtre.upper() in ("GK", "DF", "MF", "FW"):
        players = [p for p in players if p.get("position") == filtre.upper()]
    elif filtre.lower() in nt_filter_map:
        players = [p for p in players if p.get("nt_status") == nt_filter_map[filtre.lower()]]
    elif filtre.lower() != "tous":
        players = [p for p in players if
                   filtre.lower() in (p.get("current_league") or "").lower() or
                   filtre.lower() in (p.get("current_club") or "").lower()]

    afficher_joueurs(players)
    Prompt.ask("\nAppuie sur Entree")


def afficher_joueurs(players):
    """Affiche une liste de joueurs dans un tableau."""
    table = Table(
        title=f"{len(players)} joueurs",
        box=box.ROUNDED,
        border_style=VERT,
        header_style=f"bold {OR}",
    )
    table.add_column("ID", style="dim", width=4)
    table.add_column("Nom", style="bold white", min_width=20)
    table.add_column("Poste", width=6)
    table.add_column("Club", min_width=15)
    table.add_column("Ligue", min_width=14)
    table.add_column("Age", width=4)
    table.add_column("EN", width=12)
    table.add_column("Statut", width=8)

    poste_colors = {"GK": "yellow", "DF": "blue", "MF": "green", "FW": "red"}
    nt_colors = {
        "mali_a": "bold green", "mali_u23": "cyan", "mali_u20": "blue",
        "mali_u17": "magenta", "binational": "yellow", "never_called": "dim",
        "retired_intl": "dim red",
    }
    nt_labels = {
        "mali_a": "Mali A", "mali_u23": "U23", "mali_u20": "U20",
        "mali_u17": "U17", "binational": "Binational", "never_called": "-",
        "retired_intl": "Retraite",
    }

    for p in players:
        poste = p.get("position", "?")
        color = poste_colors.get(poste, "white")
        statut = p.get("status", "active")
        statut_style = "green" if statut == "active" else "red" if statut == "injured" else "dim"
        nt = p.get("nt_status", "") or ""
        nt_style = nt_colors.get(nt, "dim")
        nt_label = nt_labels.get(nt, nt or "?")

        table.add_row(
            str(p["id"]),
            p.get("name", "?"),
            f"[{color}]{poste}[/{color}]",
            p.get("current_club", "?"),
            p.get("current_league", "?"),
            str(p.get("age", "?")),
            f"[{nt_style}]{nt_label}[/{nt_style}]",
            f"[{statut_style}]{statut}[/{statut_style}]",
        )
    console.print(table)


# ============================================
# 2. CHERCHER UN JOUEUR
# ============================================

def page_recherche():
    banner()
    console.print("[bold]Recherche de joueur[/bold]\n")
    terme = Prompt.ask("Nom du joueur")
    resultats = search_players(terme)

    if not resultats:
        console.print(f"\n[dim]Aucun resultat pour '{terme}'[/dim]")
    else:
        afficher_joueurs(resultats)

    Prompt.ask("\nAppuie sur Entree")


# ============================================
# 3. FICHE COMPLETE
# ============================================

def page_fiche_joueur():
    banner()
    console.print("[bold]Fiche joueur[/bold]\n")

    # Choix du joueur
    player_id = choisir_joueur()
    if not player_id:
        return

    profile = get_player_full_profile(player_id)
    if not profile:
        console.print("[red]Joueur introuvable.[/red]")
        Prompt.ask("\nAppuie sur Entree")
        return

    banner()
    # En-tete
    console.print(Panel(
        f"[bold {OR}]{profile['name']}[/bold {OR}]\n"
        f"{profile.get('position', '?')} | {profile.get('detailed_position', '')}",
        border_style=VERT,
        box=box.DOUBLE,
    ))

    # Infos
    infos = Table(show_header=False, box=box.SIMPLE, border_style="dim")
    infos.add_column(style=f"bold {OR}", width=16)
    infos.add_column()
    infos.add_row("Club", profile.get("current_club", "?"))
    infos.add_row("Ligue", profile.get("current_league", "?"))
    infos.add_row("Age", str(profile.get("age", "?")))
    infos.add_row("Taille", f"{profile.get('height_cm', '?')} cm")
    infos.add_row("Pied", profile.get("foot", "?") or "?")
    infos.add_row("Nationalite", profile.get("nationality", "Mali"))
    if profile.get("second_nationality"):
        infos.add_row("2e nationalite", profile["second_nationality"])
    infos.add_row("Valeur", profile.get("market_value_display", "?") or "?")
    infos.add_row("Statut", profile.get("status", "active"))
    nt = profile.get("nt_status", "") or ""
    nt_labels = {"mali_a": "Mali A", "mali_u23": "U23", "mali_u20": "U20", "mali_u17": "U17",
                 "binational": "Binational", "never_called": "Jamais appele", "retired_intl": "Retraite intl"}
    infos.add_row("Equipe nationale", nt_labels.get(nt, nt or "?"))
    if profile.get("intl_caps"):
        infos.add_row("Selections", str(profile["intl_caps"]))
    if profile.get("intl_goals"):
        infos.add_row("Buts en sel.", str(profile["intl_goals"]))
    if profile.get("categories"):
        infos.add_row("Categories", ", ".join(profile["categories"]))
    if profile.get("notes"):
        infos.add_row("Notes", profile["notes"])
    console.print(infos)

    # Stats saison
    if profile.get("season_stats"):
        console.print(f"\n[bold {OR}]Stats par saison[/bold {OR}]")
        st = Table(box=box.SIMPLE_HEAVY, border_style=VERT, header_style=f"bold {OR}")
        st.add_column("Saison")
        st.add_column("Club")
        st.add_column("MJ", justify="right")
        st.add_column("Buts", justify="right", style="bold")
        st.add_column("PD", justify="right")
        st.add_column("Min", justify="right")
        st.add_column("xG", justify="right")
        st.add_column("xAG", justify="right")
        for s in profile["season_stats"]:
            st.add_row(
                s.get("season", ""), s.get("club", ""),
                str(s.get("matches_played", 0)), str(s.get("goals", 0)),
                str(s.get("assists", 0)), str(s.get("minutes", 0)),
                f"{s.get('xg', 0) or 0:.1f}", f"{s.get('xag', 0) or 0:.1f}",
            )
        console.print(st)

    # Derniers matchs
    if profile.get("matches"):
        console.print(f"\n[bold {OR}]Derniers matchs[/bold {OR}]")
        mt = Table(box=box.SIMPLE_HEAVY, border_style=VERT, header_style=f"bold {OR}")
        mt.add_column("Date")
        mt.add_column("Adversaire")
        mt.add_column("Comp.")
        mt.add_column("Min", justify="right")
        mt.add_column("Buts", justify="right", style="bold")
        mt.add_column("PD", justify="right")
        mt.add_column("Note", justify="right")
        for m in profile["matches"][:10]:
            mt.add_row(
                m.get("date", ""), m.get("opponent", ""), m.get("competition", ""),
                str(m.get("minutes_played", "")), str(m.get("goals", 0)),
                str(m.get("assists", 0)), str(m.get("rating") or ""),
            )
        console.print(mt)

    # Transferts
    if profile.get("transfers"):
        console.print(f"\n[bold {OR}]Transferts[/bold {OR}]")
        for t in profile["transfers"]:
            console.print(f"  {t.get('date', '?')} : {t.get('club_from', '?')} -> {t.get('club_to', '?')} ({t.get('transfer_fee_display', '?')})")

    # Blessures
    if profile.get("injuries"):
        console.print(f"\n[bold {OR}]Blessures[/bold {OR}]")
        for i in profile["injuries"]:
            console.print(f"  {i.get('start_date', '?')} - {i.get('end_date', '?')} : {i.get('injury_type', '?')}")

    Prompt.ask("\nAppuie sur Entree")


# ============================================
# 4. AJOUTER UN JOUEUR
# ============================================

def page_ajouter_joueur():
    banner()
    console.print("[bold]Ajouter un joueur[/bold]\n")

    nom = Prompt.ask("Nom complet")
    if not nom:
        return

    position = Prompt.ask("Poste", choices=["GK", "DF", "MF", "FW"])

    console.print("\n[dim]Remplis ce que tu sais, laisse vide sinon[/dim]\n")

    detailed = Prompt.ask("Poste detaille [dim](ex: MC, AD, DC, AG...)[/dim]", default="")
    club = Prompt.ask("Club actuel", default="")
    league = Prompt.ask("Ligue", default="")
    age = Prompt.ask("Age", default="")
    birth_year = Prompt.ask("Annee de naissance", default="")
    nationality = Prompt.ask("Nationalite", default="Mali")
    second_nat = Prompt.ask("2e nationalite [dim](France, etc.)[/dim]", default="")
    foot = Prompt.ask("Pied [dim](left/right/both)[/dim]", default="")
    height = Prompt.ask("Taille (cm)", default="")
    value = Prompt.ask("Valeur marchande [dim](ex: 5M, 500K)[/dim]", default="")
    nt_status = Prompt.ask("Statut EN [dim](mali_a/mali_u23/mali_u20/mali_u17/binational/never_called/retired_intl)[/dim]", default="")
    intl_caps = Prompt.ask("Selections internationales", default="")
    intl_goals = Prompt.ask("Buts en selection", default="")
    notes = Prompt.ask("Notes", default="")

    kwargs = {"position": position}
    if detailed:
        kwargs["detailed_position"] = detailed
    if club:
        kwargs["current_club"] = club
    if league:
        kwargs["current_league"] = league
    if age:
        kwargs["age"] = int(age)
    if birth_year:
        kwargs["birth_year"] = int(birth_year)
    if nationality:
        kwargs["nationality"] = nationality
    if second_nat:
        kwargs["second_nationality"] = second_nat
    if foot and foot in ("left", "right", "both"):
        kwargs["foot"] = foot
    if height:
        kwargs["height_cm"] = int(height)
    if value:
        kwargs["market_value_display"] = value
    if nt_status and nt_status in ("mali_a", "mali_u23", "mali_u20", "mali_u17", "binational", "never_called", "retired_intl"):
        kwargs["nt_status"] = nt_status
    if intl_caps:
        kwargs["intl_caps"] = int(intl_caps)
    if intl_goals:
        kwargs["intl_goals"] = int(intl_goals)
    if notes:
        kwargs["notes"] = notes

    console.print(f"\n[dim]Ajout de {nom}...[/dim]")
    result = add_player(nom, **kwargs)

    if result:
        console.print(f"\n[bold green]Joueur ajoute : {result['name']} (ID: {result['id']})[/bold green]")

        # Categorie
        if Confirm.ask("\nAjouter des categories ?", default=False):
            console.print("[dim]Categories possibles: europe_top5, europe_other, mali_ligue1, afrique, national_team, u23, u20, prospect, diaspora[/dim]")
            cats = Prompt.ask("Categories [dim](separees par des virgules)[/dim]")
            for cat in cats.split(","):
                cat = cat.strip()
                if cat:
                    add_category(result["id"], cat)
                    console.print(f"  + {cat}")
    else:
        console.print("[red]Erreur lors de l'ajout.[/red]")

    Prompt.ask("\nAppuie sur Entree")


# ============================================
# 5. MODIFIER UN JOUEUR
# ============================================

def page_modifier_joueur():
    banner()
    console.print("[bold]Modifier un joueur[/bold]\n")

    player_id = choisir_joueur()
    if not player_id:
        return

    player = get_player(player_id)
    if not player:
        console.print("[red]Joueur introuvable.[/red]")
        Prompt.ask("\nAppuie sur Entree")
        return

    console.print(f"\nModification de [bold]{player['name']}[/bold]")
    console.print("[dim]Laisse vide pour ne pas modifier[/dim]\n")

    fields = [
        ("name", "Nom", player.get("name", "")),
        ("position", "Poste (GK/DF/MF/FW)", player.get("position", "")),
        ("detailed_position", "Poste detaille", player.get("detailed_position", "")),
        ("current_club", "Club", player.get("current_club", "")),
        ("current_league", "Ligue", player.get("current_league", "")),
        ("age", "Age", player.get("age", "")),
        ("foot", "Pied (left/right/both)", player.get("foot", "")),
        ("height_cm", "Taille (cm)", player.get("height_cm", "")),
        ("market_value_display", "Valeur marchande", player.get("market_value_display", "")),
        ("status", "Statut (active/injured/retired/inactive)", player.get("status", "")),
        ("nt_status", "Statut EN (mali_a/mali_u23/mali_u20/mali_u17/binational/never_called/retired_intl)", player.get("nt_status", "")),
        ("intl_caps", "Selections internationales", player.get("intl_caps", "")),
        ("intl_goals", "Buts en selection", player.get("intl_goals", "")),
        ("notes", "Notes", player.get("notes", "")),
    ]

    updates = {}
    for key, label, current in fields:
        val = Prompt.ask(f"{label} [dim]({current or '?'})[/dim]", default="")
        if val:
            if key in ("age", "height_cm", "intl_caps", "intl_goals"):
                updates[key] = int(val)
            else:
                updates[key] = val

    if updates:
        result = update_player(player_id, **updates)
        if result:
            console.print(f"\n[bold green]Joueur mis a jour : {result['name']}[/bold green]")
        else:
            console.print("[red]Erreur.[/red]")
    else:
        console.print("\n[dim]Aucune modification.[/dim]")

    Prompt.ask("\nAppuie sur Entree")


# ============================================
# 6. AJOUTER DES STATS SAISON
# ============================================

def page_ajouter_stats():
    banner()
    console.print("[bold]Ajouter des stats saison[/bold]\n")

    player_id = choisir_joueur()
    if not player_id:
        return

    player = get_player(player_id)
    console.print(f"\nStats pour [bold]{player['name']}[/bold]\n")

    season = Prompt.ask("Saison [dim](ex: 2024-25)[/dim]")
    club = Prompt.ask("Club", default=player.get("current_club", ""))
    league = Prompt.ask("Ligue", default=player.get("current_league", ""))

    console.print("\n[dim]Remplis ce que tu as (0 si pas de donnees)[/dim]\n")

    stats = {}
    stat_fields = [
        ("matches_played", "Matchs joues", int),
        ("starts", "Titularisations", int),
        ("minutes", "Minutes", int),
        ("goals", "Buts", int),
        ("assists", "Passes decisives", int),
        ("goals_pens", "Buts hors penalties", int),
        ("pens_made", "Penalties marques", int),
        ("pens_att", "Penalties tires", int),
        ("yellow_cards", "Cartons jaunes", int),
        ("red_cards", "Cartons rouges", int),
        ("xg", "xG", float),
        ("xag", "xAG", float),
        ("progressive_carries", "Carries progressives", int),
        ("progressive_passes", "Passes progressives", int),
    ]

    for key, label, typ in stat_fields:
        val = Prompt.ask(f"  {label}", default="")
        if val:
            stats[key] = typ(val)

    if league:
        stats["league"] = league

    # Calculer per90 si on a les minutes
    if stats.get("minutes") and stats["minutes"] > 0:
        full_90s = stats["minutes"] / 90
        if "goals" in stats:
            stats["goals_per90"] = round(stats["goals"] / full_90s, 2)
        if "assists" in stats:
            stats["assists_per90"] = round(stats["assists"] / full_90s, 2)
        if "goals" in stats and "assists" in stats:
            stats["goals_assists"] = stats["goals"] + stats["assists"]
            stats["goals_assists_per90"] = round(stats["goals_assists"] / full_90s, 2)
        stats["full_90s"] = round(full_90s, 1)

    result = add_season_stats(player_id, season, club, **stats)
    if result:
        console.print(f"\n[bold green]Stats ajoutees pour {player['name']} ({season})[/bold green]")
    else:
        console.print("[red]Erreur.[/red]")

    Prompt.ask("\nAppuie sur Entree")


# ============================================
# 7. AJOUTER UN MATCH
# ============================================

def page_ajouter_match():
    banner()
    console.print("[bold]Ajouter un match[/bold]\n")

    player_id = choisir_joueur()
    if not player_id:
        return

    player = get_player(player_id)
    console.print(f"\nMatch pour [bold]{player['name']}[/bold]\n")

    date = Prompt.ask("Date [dim](YYYY-MM-DD)[/dim]")
    opponent = Prompt.ask("Adversaire")
    competition = Prompt.ask("Competition [dim](ex: Ligue 1, CAN, UCL)[/dim]", default="")
    home_away = Prompt.ask("Dom/Ext", choices=["home", "away", "neutral"], default="home")
    result_match = Prompt.ask("Resultat [dim](ex: 2-1)[/dim]", default="")
    started = Confirm.ask("Titulaire ?", default=True)

    console.print("\n[dim]Stats du match[/dim]\n")

    stats = {}
    match_fields = [
        ("minutes_played", "Minutes jouees", int),
        ("goals", "Buts", int),
        ("assists", "Passes dec.", int),
        ("shots", "Tirs", int),
        ("shots_on_target", "Tirs cadres", int),
        ("key_passes", "Passes cles", int),
        ("tackles", "Tacles", int),
        ("interceptions", "Interceptions", int),
        ("dribbles_completed", "Dribbles reussis", int),
        ("dribbles_attempted", "Dribbles tentes", int),
        ("rating", "Note [dim](ex: 7.2)[/dim]", float),
    ]

    for key, label, typ in match_fields:
        val = Prompt.ask(f"  {label}", default="")
        if val:
            stats[key] = typ(val)

    yellow = Confirm.ask("  Carton jaune ?", default=False)
    red = Confirm.ask("  Carton rouge ?", default=False)

    stats["competition"] = competition
    stats["home_away"] = home_away
    stats["result"] = result_match
    stats["started"] = started
    stats["yellow_card"] = yellow
    stats["red_card"] = red

    add_match_stats(player_id, date, opponent, **stats)
    console.print(f"\n[bold green]Match ajoute : {player['name']} vs {opponent} ({date})[/bold green]")

    Prompt.ask("\nAppuie sur Entree")


# ============================================
# 8. EQUIPE NATIONALE - VUE D'ENSEMBLE
# ============================================

def page_equipe_nationale():
    banner()
    console.print(Panel(
        f"[bold {OR}]LES AIGLES DU MALI[/bold {OR}]",
        border_style=VERT, box=box.DOUBLE,
    ))

    # Infos generales
    info = get_national_team_info()
    if info:
        infos = Table(show_header=False, box=box.SIMPLE, border_style="dim")
        infos.add_column(style=f"bold {OR}", width=20)
        infos.add_column()
        infos.add_row("Surnom", info.get("nickname", "Les Aigles"))
        infos.add_row("Coach", info.get("coach", "?"))
        infos.add_row("Coach adjoint", info.get("assistant_coach", "?") or "?")
        infos.add_row("Capitaine", info.get("captain", "?") or "?")
        infos.add_row("Stade", info.get("stadium", "?") or "?")
        infos.add_row("Classement FIFA", str(info.get("fifa_ranking", "?") or "?"))
        infos.add_row("Classement CAF", str(info.get("caf_ranking", "?") or "?"))
        infos.add_row("Confederation", info.get("confederation", "CAF"))
        console.print(infos)

    # Bilan general
    record = get_national_record()
    if record:
        r = record[0]
        console.print(f"\n[bold {OR}]Bilan general[/bold {OR}]")
        bilan = Table(box=box.ROUNDED, border_style=VERT, header_style=f"bold {OR}")
        bilan.add_column("MJ", justify="right")
        bilan.add_column("V", justify="right", style="green bold")
        bilan.add_column("N", justify="right", style="yellow")
        bilan.add_column("D", justify="right", style="red")
        bilan.add_column("BP", justify="right")
        bilan.add_column("BC", justify="right")
        bilan.add_column("Diff", justify="right", style="bold")
        bilan.add_row(
            str(r.get("matches_played", 0)), str(r.get("wins", 0)),
            str(r.get("draws", 0)), str(r.get("losses", 0)),
            str(r.get("total_goals_for", 0)), str(r.get("total_goals_against", 0)),
            str(r.get("goal_difference", 0)),
        )
        console.print(bilan)

    # Bilan par competition
    by_comp = get_record_by_competition()
    if by_comp:
        console.print(f"\n[bold {OR}]Bilan par competition[/bold {OR}]")
        ct = Table(box=box.ROUNDED, border_style=VERT, header_style=f"bold {OR}")
        ct.add_column("Competition", min_width=25)
        ct.add_column("MJ", justify="right")
        ct.add_column("V", justify="right", style="green")
        ct.add_column("N", justify="right", style="yellow")
        ct.add_column("D", justify="right", style="red")
        ct.add_column("BP", justify="right")
        ct.add_column("BC", justify="right")
        for c in by_comp:
            ct.add_row(
                c.get("competition", "?"), str(c.get("matches_played", 0)),
                str(c.get("wins", 0)), str(c.get("draws", 0)), str(c.get("losses", 0)),
                str(c.get("goals_for", 0)), str(c.get("goals_against", 0)),
            )
        console.print(ct)

    # Derniers matchs
    matches = get_national_matches(limit=5)
    if matches:
        console.print(f"\n[bold {OR}]5 derniers matchs[/bold {OR}]")
        afficher_matchs_nationaux(matches)

    # Meilleurs buteurs en selection
    scorers = get_national_top_scorers()
    if scorers:
        console.print(f"\n[bold {OR}]Meilleurs buteurs en selection[/bold {OR}]")
        st = Table(box=box.ROUNDED, border_style=VERT, header_style=f"bold {OR}")
        st.add_column("#", width=3)
        st.add_column("Nom", style="bold")
        st.add_column("Poste")
        st.add_column("Club")
        st.add_column("Buts", justify="right", style=f"bold {OR}")
        st.add_column("PD", justify="right")
        st.add_column("Sel.", justify="right")
        for i, s in enumerate(scorers, 1):
            st.add_row(
                str(i), s.get("name", ""), s.get("position", ""),
                s.get("current_club", ""), str(s.get("total_goals", 0)),
                str(s.get("total_assists", 0)), str(s.get("selections", 0)),
            )
        console.print(st)

    # Modifier les infos
    if Confirm.ask("\nModifier les infos de l'equipe ?", default=False):
        console.print("[dim]Laisse vide pour ne pas modifier[/dim]\n")
        coach = Prompt.ask("Coach", default="")
        captain = Prompt.ask("Capitaine", default="")
        ranking = Prompt.ask("Classement FIFA", default="")
        caf_rank = Prompt.ask("Classement CAF", default="")

        updates = {}
        if coach:
            updates["coach"] = coach
        if captain:
            updates["captain"] = captain
        if ranking:
            updates["fifa_ranking"] = int(ranking)
        if caf_rank:
            updates["caf_ranking"] = int(caf_rank)

        if updates:
            update_national_team_info(**updates)
            console.print(f"[bold green]Infos mises a jour.[/bold green]")

    Prompt.ask("\nAppuie sur Entree")


# ============================================
# 9. RESULTATS DES MATCHS NATIONAUX
# ============================================

def afficher_matchs_nationaux(matches):
    """Affiche une liste de matchs nationaux."""
    mt = Table(box=box.ROUNDED, border_style=VERT, header_style=f"bold {OR}")
    mt.add_column("Date", width=12)
    mt.add_column("Competition", min_width=18)
    mt.add_column("Adversaire", min_width=15)
    mt.add_column("Score", justify="center", width=7)
    mt.add_column("R", justify="center", width=3)
    mt.add_column("Lieu")

    for m in matches:
        gf = m.get("goals_for", 0)
        ga = m.get("goals_against", 0)
        result = m.get("result", "?")
        result_style = "green bold" if result == "W" else "red bold" if result == "L" else "yellow bold"
        score = f"{gf} - {ga}"

        venue = m.get("venue", "") or ""
        if m.get("home_away") == "away":
            venue = f"(ext) {venue}"

        penalty = m.get("penalty_shootout", "")
        if penalty:
            score += f" ({penalty} tab)"

        mt.add_row(
            m.get("date", ""), m.get("competition", ""),
            m.get("opponent", ""), score,
            f"[{result_style}]{result}[/{result_style}]",
            venue,
        )
    console.print(mt)


def page_resultats_nationaux():
    banner()
    console.print("[bold]Resultats Equipe Nationale[/bold]\n")

    options = [
        ("1", "Tous les matchs (recents)"),
        ("2", "Filtrer par competition"),
        ("3", "Bilan contre un adversaire"),
    ]

    for num, label in options:
        console.print(f"  [{OR}][{num}][/{OR}] {label}")

    choix = Prompt.ask("\nChoix", choices=["1", "2", "3"])

    if choix == "1":
        limit = IntPrompt.ask("Nombre de matchs", default=20)
        matches = get_national_matches(limit=limit)
        if matches:
            console.print(f"\n[bold]{len(matches)} derniers matchs[/bold]\n")
            afficher_matchs_nationaux(matches)

            # Stats rapides
            wins = sum(1 for m in matches if m.get("result") == "W")
            draws = sum(1 for m in matches if m.get("result") == "D")
            losses = sum(1 for m in matches if m.get("result") == "L")
            gf = sum(m.get("goals_for", 0) for m in matches)
            ga = sum(m.get("goals_against", 0) for m in matches)
            console.print(f"\n  Bilan: [green]{wins}V[/green] [yellow]{draws}N[/yellow] [red]{losses}D[/red] | {gf} BP - {ga} BC")
        else:
            console.print("[dim]Aucun match enregistre.[/dim]")

    elif choix == "2":
        comp = Prompt.ask("Competition [dim](ex: CAN, Qualif CM, Amical)[/dim]")
        matches = get_national_matches_by_competition(comp)
        if matches:
            console.print(f"\n[bold]{comp} - {len(matches)} matchs[/bold]\n")
            afficher_matchs_nationaux(matches)
        else:
            console.print(f"[dim]Aucun match pour '{comp}'.[/dim]")

    elif choix == "3":
        adversaire = Prompt.ask("Adversaire [dim](ex: Senegal, Cote d'Ivoire)[/dim]")
        record = get_record_by_opponent()
        found = [r for r in record if adversaire.lower() in r.get("opponent", "").lower()]
        if found:
            for r in found:
                console.print(f"\n[bold]Mali vs {r['opponent']}[/bold]")
                console.print(f"  Matchs: {r['matches_played']}")
                console.print(f"  Victoires: [green]{r['wins']}[/green]")
                console.print(f"  Nuls: [yellow]{r['draws']}[/yellow]")
                console.print(f"  Defaites: [red]{r['losses']}[/red]")
                console.print(f"  Buts: {r['goals_for']} - {r['goals_against']}")

            # Afficher les matchs
            matches = get_national_matches(limit=100)
            opponent_matches = [m for m in matches if adversaire.lower() in m.get("opponent", "").lower()]
            if opponent_matches:
                console.print()
                afficher_matchs_nationaux(opponent_matches)
        else:
            console.print(f"[dim]Aucun match contre '{adversaire}'.[/dim]")

    Prompt.ask("\nAppuie sur Entree")


# ============================================
# 10. AJOUTER UN MATCH EQUIPE NATIONALE
# ============================================

def page_ajouter_match_national():
    banner()
    console.print("[bold]Ajouter un match de l'Equipe Nationale[/bold]\n")

    date = Prompt.ask("Date [dim](YYYY-MM-DD)[/dim]")
    opponent = Prompt.ask("Adversaire")
    competition = Prompt.ask("Competition [dim](ex: CAN 2025, Qualif CM 2026, Amical)[/dim]")
    round_match = Prompt.ask("Tour [dim](ex: Poules, 1/4 finale, Finale)[/dim]", default="")
    home_away = Prompt.ask("Dom/Ext", choices=["home", "away", "neutral"], default="home")
    venue = Prompt.ask("Stade", default="")
    city = Prompt.ask("Ville", default="")

    goals_for = IntPrompt.ask("Buts Mali")
    goals_against = IntPrompt.ask(f"Buts {opponent}")

    penalty = Prompt.ask("Tirs au but [dim](ex: 4-3, ou vide)[/dim]", default="")
    coach = Prompt.ask("Coach", default="")
    attendance = Prompt.ask("Spectateurs [dim](ou vide)[/dim]", default="")
    notes = Prompt.ask("Notes", default="")

    kwargs = {"competition": competition, "home_away": home_away, "team": "Mali A"}
    if round_match:
        kwargs["round"] = round_match
    if venue:
        kwargs["venue"] = venue
    if city:
        kwargs["city"] = city
    if penalty:
        kwargs["penalty_shootout"] = penalty
    if coach:
        kwargs["coach"] = coach
    if attendance:
        kwargs["attendance"] = int(attendance)
    if notes:
        kwargs["notes"] = notes

    result = add_national_match(date, opponent, goals_for, goals_against, **kwargs)

    res_text = "Victoire" if goals_for > goals_against else "Defaite" if goals_for < goals_against else "Nul"
    res_color = "green" if goals_for > goals_against else "red" if goals_for < goals_against else "yellow"

    console.print(f"\n[bold {res_color}]Match ajoute : Mali {goals_for} - {goals_against} {opponent} ({res_text})[/bold {res_color}]")

    # Ajouter les buteurs ?
    if Confirm.ask("\nAjouter les performances des joueurs ?", default=False):
        while True:
            console.print()
            player_id = choisir_joueur()
            if not player_id:
                break

            player = get_player(player_id)
            console.print(f"\n[bold]{player['name']}[/bold]")

            started = Confirm.ask("  Titulaire ?", default=True)
            minutes = Prompt.ask("  Minutes jouees", default="90")
            goals = Prompt.ask("  Buts", default="0")
            assists = Prompt.ask("  Passes dec.", default="0")
            yellow = Confirm.ask("  Carton jaune ?", default=False)
            red = Confirm.ask("  Carton rouge ?", default=False)
            rating = Prompt.ask("  Note [dim](ex: 7.5)[/dim]", default="")

            # Trouver l'ID du match qu'on vient d'ajouter
            match = supabase.table("national_matches").select("id").eq("date", date).eq("opponent", opponent).execute()
            match_id = match.data[0]["id"] if match.data else None

            callup_data = {
                "started": started,
                "minutes_played": int(minutes),
                "goals": int(goals),
                "assists": int(assists),
                "yellow_card": yellow,
                "red_card": red,
                "competition": competition,
                "date": date,
            }
            if rating:
                callup_data["rating"] = float(rating)

            add_squad_callup(player_id, match_id, **callup_data)
            console.print(f"  [green]OK[/green]")

            if not Confirm.ask("\nAjouter un autre joueur ?", default=True):
                break

    Prompt.ask("\nAppuie sur Entree")


# ============================================
# 11. CONVOCATIONS
# ============================================

def page_convocations():
    banner()
    console.print("[bold]Convocations / Compositions[/bold]\n")

    options = [
        ("1", "Voir les selections d'un joueur"),
        ("2", "Composition d'un match"),
        ("3", "Meilleurs buteurs en selection"),
    ]

    for num, label in options:
        console.print(f"  [{OR}][{num}][/{OR}] {label}")

    choix = Prompt.ask("\nChoix", choices=["1", "2", "3"])

    if choix == "1":
        player_id = choisir_joueur()
        if player_id:
            player = get_player(player_id)
            callups = get_player_callups(player_id)
            console.print(f"\n[bold]{player['name']}[/bold] - Selections\n")

            if callups:
                ct = Table(box=box.ROUNDED, border_style=VERT, header_style=f"bold {OR}")
                ct.add_column("Date")
                ct.add_column("Competition")
                ct.add_column("Titu.", justify="center")
                ct.add_column("Min", justify="right")
                ct.add_column("Buts", justify="right", style="bold")
                ct.add_column("PD", justify="right")
                ct.add_column("Note", justify="right")

                total_goals = 0
                total_assists = 0
                total_mins = 0

                for c in callups:
                    match_info = c.get("national_matches", {}) or {}
                    opponent = match_info.get("opponent", "")
                    comp = c.get("competition", "") or match_info.get("competition", "")

                    titu = "X" if c.get("started") else ""
                    goals = c.get("goals", 0) or 0
                    assists = c.get("assists", 0) or 0
                    mins = c.get("minutes_played", 0) or 0

                    total_goals += goals
                    total_assists += assists
                    total_mins += mins

                    display_date = c.get("date", "") or match_info.get("date", "")

                    ct.add_row(
                        display_date,
                        f"{comp} vs {opponent}" if opponent else comp,
                        titu, str(mins), str(goals), str(assists),
                        str(c.get("rating", "")) if c.get("rating") else "",
                    )

                console.print(ct)
                console.print(f"\n  Total: {len(callups)} selections | {total_goals} buts | {total_assists} PD | {total_mins} min")
            else:
                console.print("[dim]Aucune selection enregistree.[/dim]")

    elif choix == "2":
        matches = get_national_matches(limit=20)
        if matches:
            console.print("\n[bold]Matchs recents :[/bold]\n")
            for m in matches:
                gf = m.get("goals_for", 0)
                ga = m.get("goals_against", 0)
                console.print(f"  [dim]ID {m['id']}[/dim] | {m['date']} | Mali {gf}-{ga} {m['opponent']} ({m.get('competition', '')})")

            match_id = IntPrompt.ask("\nID du match")
            callups = supabase.table("squad_callups").select("*, players(name, position)").eq("match_id", match_id).order("started", desc=True).execute().data

            if callups:
                ct = Table(title="Composition", box=box.ROUNDED, border_style=VERT, header_style=f"bold {OR}")
                ct.add_column("Nom", style="bold")
                ct.add_column("Poste")
                ct.add_column("Titu.", justify="center")
                ct.add_column("Min", justify="right")
                ct.add_column("Buts", justify="right")
                ct.add_column("PD", justify="right")
                ct.add_column("CJ", justify="center")
                ct.add_column("CR", justify="center")
                ct.add_column("Note", justify="right")

                for c in callups:
                    p = c.get("players", {}) or {}
                    ct.add_row(
                        p.get("name", "?"), p.get("position", "?"),
                        "X" if c.get("started") else "",
                        str(c.get("minutes_played", "")),
                        str(c.get("goals", 0)), str(c.get("assists", 0)),
                        "Y" if c.get("yellow_card") else "",
                        "R" if c.get("red_card") else "",
                        str(c.get("rating", "")) if c.get("rating") else "",
                    )
                console.print(ct)
            else:
                console.print("[dim]Aucune composition enregistree pour ce match.[/dim]")
        else:
            console.print("[dim]Aucun match enregistre.[/dim]")

    elif choix == "3":
        scorers = get_national_top_scorers()
        if scorers:
            st = Table(title="Meilleurs buteurs en selection", box=box.ROUNDED, border_style=VERT, header_style=f"bold {OR}")
            st.add_column("#", width=3)
            st.add_column("Nom", style="bold")
            st.add_column("Poste")
            st.add_column("Club")
            st.add_column("Buts", justify="right", style=f"bold {OR}")
            st.add_column("PD", justify="right")
            st.add_column("Sel.", justify="right")
            st.add_column("Minutes", justify="right")
            for i, s in enumerate(scorers, 1):
                st.add_row(
                    str(i), s.get("name", ""), s.get("position", ""),
                    s.get("current_club", ""), str(s.get("total_goals", 0)),
                    str(s.get("total_assists", 0)), str(s.get("selections", 0)),
                    str(s.get("total_minutes", 0)),
                )
            console.print(st)
        else:
            console.print("[dim]Aucune donnee. Ajoute des matchs avec les performances des joueurs.[/dim]")

    Prompt.ask("\nAppuie sur Entree")


# ============================================
# 12. JOUEURS PAR CATEGORIE EN
# ============================================

def page_categories_en():
    banner()
    console.print(Panel(
        f"[bold {OR}]JOUEURS PAR CATEGORIE EN[/bold {OR}]",
        border_style=VERT, box=box.DOUBLE,
    ))

    categories = [
        ("1", "mali_a", "Mali A (equipe senior)"),
        ("2", "mali_u23", "Mali U23 (Espoirs)"),
        ("3", "mali_u20", "Mali U20"),
        ("4", "mali_u17", "Mali U17"),
        ("5", "binational", "Binationaux (pourraient choisir le Mali)"),
        ("6", "never_called", "Jamais appeles"),
        ("7", "retired_intl", "Retraites internationaux"),
        ("8", "all", "Vue complete par categorie"),
    ]

    for num, _, label in categories:
        console.print(f"  [{OR}][{num}][/{OR}] {label}")

    choix = Prompt.ask("\nChoix", choices=[str(i) for i in range(1, 9)])

    players = get_all_players()

    if choix == "8":
        _afficher_toutes_categories(players)
    elif choix == "1":
        _afficher_mali_a(players)
    else:
        nt_key = categories[int(choix) - 1][1]
        filtered = [p for p in players if p.get("nt_status") == nt_key]
        if filtered:
            _afficher_groupe_en(filtered, categories[int(choix) - 1][2])
        else:
            console.print(f"\n[dim]Aucun joueur dans cette categorie.[/dim]")

    Prompt.ask("\nAppuie sur Entree")


def _afficher_mali_a(players):
    """Affiche les joueurs Mali A avec sous-filtres."""
    mali_a = [p for p in players if p.get("nt_status") == "mali_a"]
    if not mali_a:
        console.print("[dim]Aucun joueur Mali A.[/dim]")
        return

    console.print(f"\n[bold {OR}]MALI A[/bold {OR}] - {len(mali_a)} joueurs\n")

    options = [
        ("1", "Tous les Mali A"),
        ("2", "Appeles recemment (< 2 ans)"),
        ("3", "Plus appeles depuis 2+ ans"),
        ("4", "Par poste (GK / DF / MF / FW)"),
        ("5", "Par ligue"),
        ("6", "Top selections / buteurs EN"),
    ]
    for num, label in options:
        console.print(f"  [{OR}][{num}][/{OR}] {label}")

    sub = Prompt.ask("\nChoix", choices=["1", "2", "3", "4", "5", "6"], default="1")

    # Recuperer les dernieres convocations pour chaque joueur
    callups = {}
    try:
        res = supabase.table("squad_callups").select("player_id, date").order("date", desc=True).execute()
        for c in res.data:
            pid = c["player_id"]
            if pid not in callups:
                callups[pid] = c["date"]
    except Exception:
        pass

    # Date limite : 2 ans en arriere
    from datetime import timedelta
    two_years_ago = (datetime.now() - timedelta(days=730)).strftime("%Y-%m-%d")

    if sub == "1":
        _afficher_groupe_en(mali_a, "MALI A - Tous")

    elif sub == "2":
        recent = [p for p in mali_a if callups.get(p["id"], "9999") >= two_years_ago]
        if not recent:
            # Si pas de data squad_callups, filtrer par age/status comme fallback
            console.print("[dim]Pas de donnees de convocations. Affichage des joueurs actifs de moins de 33 ans.[/dim]\n")
            recent = [p for p in mali_a if p.get("status") == "active" and (p.get("age") or 99) < 33]
        _afficher_groupe_en(recent, f"MALI A - Appeles recemment ({len(recent)} joueurs)")

    elif sub == "3":
        old = [p for p in mali_a if callups.get(p["id"], "0000") < two_years_ago]
        if not old and not callups:
            console.print("[dim]Pas de donnees de convocations. Affichage des joueurs 33+ ans ou inactifs.[/dim]\n")
            old = [p for p in mali_a if (p.get("age") or 0) >= 33 or p.get("status") in ("inactive", "retired")]
        _afficher_groupe_en(old, f"MALI A - Plus appeles depuis 2+ ans ({len(old)} joueurs)")

    elif sub == "4":
        poste_names = {"GK": "GARDIENS", "DF": "DEFENSEURS", "MF": "MILIEUX", "FW": "ATTAQUANTS"}
        for pos in ("GK", "DF", "MF", "FW"):
            group = [p for p in mali_a if p.get("position") == pos]
            if group:
                console.print(f"\n[bold {OR}]{poste_names[pos]}[/bold {OR}] ({len(group)})")
                table = Table(box=box.SIMPLE, border_style=VERT, show_header=False)
                table.add_column(width=25, style="bold")
                table.add_column(width=20)
                table.add_column(width=20)
                table.add_column(width=5, justify="right")
                table.add_column(width=8, justify="right")
                for p in sorted(group, key=lambda x: x.get("age") or 99):
                    caps = p.get("intl_caps", 0) or 0
                    caps_str = f"{caps} sel." if caps else ""
                    table.add_row(
                        p["name"],
                        p.get("current_club", "?"),
                        p.get("current_league", "?"),
                        str(p.get("age", "?")),
                        caps_str,
                    )
                console.print(table)

    elif sub == "5":
        leagues = {}
        for p in mali_a:
            lg = p.get("current_league") or "Inconnue"
            leagues.setdefault(lg, []).append(p)
        for lg, pls in sorted(leagues.items(), key=lambda x: -len(x[1])):
            console.print(f"\n[bold {OR}]{lg}[/bold {OR}] ({len(pls)})")
            for p in pls:
                caps = p.get("intl_caps", 0) or 0
                caps_str = f" | {caps} sel." if caps else ""
                console.print(f"  {p.get('position', '?'):4s} {p['name']:25s} {p.get('current_club', '?'):20s} age {p.get('age', '?')}{caps_str}")

    elif sub == "6":
        # Trier par selections puis par buts
        by_caps = sorted(mali_a, key=lambda x: -(x.get("intl_caps") or 0))
        console.print(f"\n[bold {OR}]Par nombre de selections[/bold {OR}]")
        table = Table(box=box.ROUNDED, border_style=VERT, header_style=f"bold {OR}")
        table.add_column("#", width=3)
        table.add_column("Nom", style="bold", min_width=22)
        table.add_column("Poste", width=5)
        table.add_column("Club", min_width=18)
        table.add_column("Age", width=4, justify="right")
        table.add_column("Sel.", width=5, justify="right", style=f"bold {OR}")
        table.add_column("Buts EN", width=7, justify="right")
        for i, p in enumerate(by_caps, 1):
            caps = p.get("intl_caps", 0) or 0
            goals = p.get("intl_goals", 0) or 0
            if caps == 0 and goals == 0:
                continue
            table.add_row(
                str(i), p["name"], p.get("position", "?"),
                p.get("current_club", "?"),
                str(p.get("age", "?")),
                str(caps), str(goals),
            )
        console.print(table)


def _afficher_groupe_en(players, titre):
    """Affiche un groupe de joueurs EN avec details."""
    console.print(f"\n[bold {OR}]{titre}[/bold {OR}]\n")
    table = Table(box=box.ROUNDED, border_style=VERT, header_style=f"bold {OR}")
    table.add_column("#", width=3, style="dim")
    table.add_column("Nom", style="bold", min_width=22)
    table.add_column("Poste", width=5)
    table.add_column("Club", min_width=18)
    table.add_column("Ligue", min_width=16)
    table.add_column("Age", width=4, justify="right")
    table.add_column("Sel.", width=5, justify="right")
    table.add_column("Buts", width=5, justify="right")
    table.add_column("Statut", width=8)
    table.add_column("2e nat.", width=10)

    poste_order = {"GK": 0, "DF": 1, "MF": 2, "FW": 3}
    sorted_players = sorted(players, key=lambda x: (poste_order.get(x.get("position", ""), 9), x.get("name", "")))

    for i, p in enumerate(sorted_players, 1):
        statut = p.get("status", "active")
        statut_style = "green" if statut == "active" else "red" if statut == "injured" else "dim"
        poste = p.get("position", "?")
        poste_colors = {"GK": "yellow", "DF": "blue", "MF": "green", "FW": "red"}
        pc = poste_colors.get(poste, "white")
        caps = p.get("intl_caps", 0) or 0
        goals = p.get("intl_goals", 0) or 0

        table.add_row(
            str(i),
            p["name"],
            f"[{pc}]{poste}[/{pc}]",
            p.get("current_club", "?"),
            p.get("current_league", "?"),
            str(p.get("age", "?")),
            str(caps) if caps else "",
            str(goals) if goals else "",
            f"[{statut_style}]{statut}[/{statut_style}]",
            p.get("second_nationality", "") or "",
        )
    console.print(table)


def _afficher_toutes_categories(players):
    """Affiche tous les joueurs groupes par categorie EN."""
    nt_config = [
        ("mali_a", "MALI A", "bold green"),
        ("mali_u23", "U23", "cyan"),
        ("mali_u20", "U20", "blue"),
        ("mali_u17", "U17", "magenta"),
        ("binational", "BINATIONAUX", "yellow"),
        ("never_called", "JAMAIS APPELES", "dim"),
        ("retired_intl", "RETRAITES INTERNATIONAUX", "dim red"),
    ]
    total_shown = 0
    for nt_key, nt_label, style in nt_config:
        group = [p for p in players if p.get("nt_status") == nt_key]
        if not group:
            continue
        total_shown += len(group)
        console.print(f"\n[{style}]{'=' * 50}[/{style}]")
        console.print(f"[bold {style}]  {nt_label} ({len(group)} joueurs)[/bold {style}]")
        console.print(f"[{style}]{'=' * 50}[/{style}]")

        poste_order = {"GK": 0, "DF": 1, "MF": 2, "FW": 3}
        group.sort(key=lambda x: (poste_order.get(x.get("position", ""), 9), x.get("name", "")))

        for p in group:
            poste = p.get("position", "?")
            caps = p.get("intl_caps", 0) or 0
            goals = p.get("intl_goals", 0) or 0
            club = p.get("current_club", "?")
            league = p.get("current_league", "")
            age = p.get("age", "?")
            second_nat = p.get("second_nationality", "")

            extras = []
            if caps:
                extras.append(f"{caps} sel.")
            if goals:
                extras.append(f"{goals}G")
            if second_nat:
                extras.append(f"[dim]({second_nat})[/dim]")
            extras_str = " | " + " ".join(extras) if extras else ""

            statut = p.get("status", "active")
            statut_icon = "[green]●[/green]" if statut == "active" else "[red]●[/red]" if statut == "injured" else "[dim]○[/dim]"

            console.print(f"  {statut_icon} {poste:4s} {p['name']:25s} {club:20s} {league:20s} {age}{extras_str}")

    # Sans categorie
    no_cat = [p for p in players if not p.get("nt_status")]
    if no_cat:
        console.print(f"\n[dim]{'=' * 50}[/dim]")
        console.print(f"[dim]  SANS CATEGORIE ({len(no_cat)} joueurs)[/dim]")
        for p in no_cat:
            console.print(f"  [dim]? {p.get('position', '?'):4s} {p['name']:25s} {p.get('current_club', '?')}[/dim]")

    console.print(f"\n[bold]Total: {total_shown} joueurs categorises[/bold]")


# ============================================
# 13. HISTORIQUE DES COACHS
# ============================================

def page_historique_coachs():
    banner()
    console.print(Panel(
        f"[bold {OR}]HISTORIQUE DES COACHS - LES AIGLES[/bold {OR}]",
        border_style=VERT, box=box.DOUBLE,
    ))

    # Lire les coachs depuis la table
    try:
        result = supabase.table("coaches_history").select("*").order("start_date", desc=True).execute()
        coaches = result.data
    except Exception:
        coaches = []

    if coaches:
        table = Table(box=box.ROUNDED, border_style=VERT, header_style=f"bold {OR}")
        table.add_column("Coach", style="bold", min_width=20)
        table.add_column("Nationalite", width=15)
        table.add_column("Debut", width=12)
        table.add_column("Fin", width=12)
        table.add_column("MJ", justify="right", width=4)
        table.add_column("V", justify="right", style="green", width=4)
        table.add_column("N", justify="right", style="yellow", width=4)
        table.add_column("D", justify="right", style="red", width=4)
        table.add_column("Resultat majeur", min_width=20)

        for c in coaches:
            end = c.get("end_date", "") or "en poste"
            table.add_row(
                c.get("name", "?"),
                c.get("nationality", "?"),
                c.get("start_date", "?"),
                end,
                str(c.get("matches", 0) or ""),
                str(c.get("wins", 0) or ""),
                str(c.get("draws", 0) or ""),
                str(c.get("losses", 0) or ""),
                c.get("achievements", "") or "",
            )
        console.print(table)

        # Bilan par coach depuis les matchs
        console.print(f"\n[bold {OR}]Bilan calcule depuis les matchs enregistres[/bold {OR}]")
        matches = supabase.table("national_matches").select("coach, result").not_.is_("coach", "null").execute().data
        if matches:
            coach_stats = {}
            for m in matches:
                c = m["coach"]
                if c not in coach_stats:
                    coach_stats[c] = {"mj": 0, "w": 0, "d": 0, "l": 0}
                coach_stats[c]["mj"] += 1
                if m["result"] == "W":
                    coach_stats[c]["w"] += 1
                elif m["result"] == "D":
                    coach_stats[c]["d"] += 1
                elif m["result"] == "L":
                    coach_stats[c]["l"] += 1

            for coach, s in sorted(coach_stats.items(), key=lambda x: -x[1]["mj"]):
                console.print(f"  {coach:25s} | {s['mj']}MJ [green]{s['w']}V[/green] [yellow]{s['d']}N[/yellow] [red]{s['l']}D[/red]")
    else:
        console.print("[dim]Aucun historique de coach enregistre.[/dim]")
        console.print("[dim]Utilise Supabase SQL Editor pour creer la table coaches_history.[/dim]")

    # Option d'ajout
    if Confirm.ask("\nAjouter un coach ?", default=False):
        name = Prompt.ask("Nom du coach")
        nationality = Prompt.ask("Nationalite", default="")
        start = Prompt.ask("Date debut (YYYY-MM-DD)")
        end = Prompt.ask("Date fin (YYYY-MM-DD ou vide si en poste)", default="")
        achievements = Prompt.ask("Resultats majeurs", default="")

        data = {"name": name, "start_date": start}
        if nationality:
            data["nationality"] = nationality
        if end:
            data["end_date"] = end
        if achievements:
            data["achievements"] = achievements

        try:
            supabase.table("coaches_history").insert(data).execute()
            console.print(f"[bold green]Coach {name} ajoute.[/bold green]")
        except Exception as e:
            console.print(f"[red]Erreur: {e}[/red]")

    Prompt.ask("\nAppuie sur Entree")


# ============================================
# 14. CLASSEMENTS
# ============================================

def page_classements():
    banner()
    console.print("[bold]Classements[/bold]\n")

    options = [
        ("1", "Top buteurs"),
        ("2", "Top passeurs"),
        ("3", "Joueurs par ligue"),
        ("4", "Joueurs par poste"),
        ("5", "Resume de tous les joueurs"),
    ]

    for num, label in options:
        console.print(f"  [{OR}][{num}][/{OR}] {label}")

    choix = Prompt.ask("\nChoix", choices=["1", "2", "3", "4", "5"])

    if choix == "1":
        # Afficher saisons disponibles
        seasons = supabase.table("v_available_seasons").select("*").execute().data
        if seasons:
            console.print(f"\n[dim]Saisons disponibles: {', '.join(s['season'] + ' (' + str(s['nb_players']) + ' joueurs)' for s in seasons)}[/dim]")
        season = Prompt.ask("Saison", default="2025-26")
        data = get_top_scorers(season=season, limit=20)
        if data:
            table = Table(title=f"Top Buteurs {season}", box=box.ROUNDED, border_style=VERT, header_style=f"bold {OR}")
            table.add_column("#", width=3)
            table.add_column("Nom", style="bold")
            table.add_column("Club")
            table.add_column("Ligue")
            table.add_column("Buts", justify="right", style=f"bold {OR}")
            table.add_column("PD", justify="right")
            table.add_column("G+A", justify="right", style="bold")
            table.add_column("xG", justify="right")
            table.add_column("MJ", justify="right")
            for i, d in enumerate(data, 1):
                table.add_row(
                    str(i), d.get("name", ""), d.get("current_club", ""),
                    d.get("current_league", ""),
                    str(d.get("goals", 0)), str(d.get("assists", 0)),
                    str(d.get("goal_contributions", 0)), f"{d.get('xg', 0) or 0:.1f}",
                    str(d.get("matches_played", 0)),
                )
            console.print(table)
        else:
            console.print("[dim]Pas de stats disponibles. Ajoute des stats saison d'abord.[/dim]")

    elif choix == "2":
        seasons = supabase.table("v_available_seasons").select("*").execute().data
        if seasons:
            console.print(f"\n[dim]Saisons disponibles: {', '.join(s['season'] for s in seasons)}[/dim]")
        season = Prompt.ask("Saison", default="2025-26")
        data = get_top_assisters(season=season, limit=20)
        if data:
            table = Table(title=f"Top Passeurs {season}", box=box.ROUNDED, border_style=VERT, header_style=f"bold {OR}")
            table.add_column("#", width=3)
            table.add_column("Nom", style="bold")
            table.add_column("Club")
            table.add_column("Ligue")
            table.add_column("PD", justify="right", style=f"bold {OR}")
            table.add_column("xAG", justify="right")
            table.add_column("PD/90", justify="right")
            table.add_column("MJ", justify="right")
            for i, d in enumerate(data, 1):
                table.add_row(
                    str(i), d.get("name", ""), d.get("current_club", ""),
                    d.get("current_league", ""),
                    str(d.get("assists", 0)), f"{d.get('xag', 0) or 0:.1f}",
                    f"{d.get('assists_per90', 0) or 0:.2f}",
                    str(d.get("matches_played", 0)),
                )
            console.print(table)
        else:
            console.print("[dim]Pas de stats disponibles.[/dim]")

    elif choix == "3":
        players = get_all_players()
        leagues = {}
        for p in players:
            lg = p.get("current_league") or "Inconnue"
            leagues.setdefault(lg, []).append(p)

        for lg, pls in sorted(leagues.items(), key=lambda x: -len(x[1])):
            console.print(f"\n[bold {OR}]{lg}[/bold {OR}] ({len(pls)} joueurs)")
            for p in pls:
                console.print(f"  {p.get('position', '?'):4s} {p['name']:25s} {p.get('current_club', '?')}")

    elif choix == "4":
        players = get_all_players()
        postes = {"GK": [], "DF": [], "MF": [], "FW": []}
        for p in players:
            pos = p.get("position", "?")
            if pos in postes:
                postes[pos].append(p)

        poste_names = {"GK": "Gardiens", "DF": "Defenseurs", "MF": "Milieux", "FW": "Attaquants"}
        for pos, pls in postes.items():
            console.print(f"\n[bold {OR}]{poste_names[pos]}[/bold {OR}] ({len(pls)})")
            for p in pls:
                console.print(f"  {p['name']:25s} {p.get('current_club', '?'):20s} {p.get('current_league', '?')}")

    elif choix == "5":
        data = get_player_summary()
        if data:
            table = Table(title="Resume joueurs", box=box.ROUNDED, border_style=VERT, header_style=f"bold {OR}")
            table.add_column("Nom", style="bold")
            table.add_column("Poste")
            table.add_column("Club")
            table.add_column("Saisons", justify="right")
            table.add_column("MJ", justify="right")
            table.add_column("Buts", justify="right")
            table.add_column("PD", justify="right")
            for d in data:
                table.add_row(
                    d.get("name", ""), d.get("position", ""),
                    d.get("current_club", ""),
                    str(d.get("seasons_tracked", 0)),
                    str(d.get("total_matches", 0)),
                    str(d.get("total_goals", 0)),
                    str(d.get("total_assists", 0)),
                )
            console.print(table)

    Prompt.ask("\nAppuie sur Entree")


# ============================================
# 9. SCRAPER FBREF
# ============================================

def page_scraper():
    banner()
    console.print("[bold]Scraper FBref[/bold]\n")

    options = [
        ("1", "Chercher un joueur sur FBref (par URL)"),
        ("2", "Importer un CSV FBref"),
        ("3", "Scraper les joueurs connus"),
    ]

    for num, label in options:
        console.print(f"  [{OR}][{num}][/{OR}] {label}")

    choix = Prompt.ask("\nChoix", choices=["1", "2", "3"])

    if choix == "1":
        console.print("\n[dim]Va sur fbref.com, cherche le joueur, copie l'URL de sa page[/dim]")
        console.print("[dim]Exemple: https://fbref.com/en/players/abc123/Player-Name[/dim]\n")
        url = Prompt.ask("URL FBref du joueur")
        nom = Prompt.ask("Nom du joueur")
        position = Prompt.ask("Poste", choices=["GK", "DF", "MF", "FW"])
        club = Prompt.ask("Club actuel", default="")
        league = Prompt.ask("Ligue", default="")

        # Extraire fbref_id de l'URL
        fbref_id = None
        if "/players/" in url:
            parts = url.split("/players/")
            if len(parts) > 1:
                fbref_id = parts[1].split("/")[0]

        kwargs = {"position": position, "fbref_url": url}
        if fbref_id:
            kwargs["fbref_id"] = fbref_id
        if club:
            kwargs["current_club"] = club
        if league:
            kwargs["current_league"] = league

        result = upsert_player(nom, **kwargs)
        if result:
            console.print(f"\n[bold green]Joueur ajoute/mis a jour : {result['name']} (ID: {result['id']})[/bold green]")

    elif choix == "2":
        console.print("\n[bold]Import CSV FBref[/bold]\n")
        console.print("[dim]1. Va sur la page FBref du joueur[/dim]")
        console.print("[dim]2. Sous le tableau de stats, clique 'Share & Export' > 'Get as CSV'[/dim]")
        console.print("[dim]3. Copie tout le texte CSV[/dim]")
        console.print("[dim]4. Colle-le dans un fichier .csv[/dim]\n")

        filepath = Prompt.ask("Chemin du fichier CSV")
        stat_type = Prompt.ask("Type de stats", choices=["standard", "shooting", "passing", "defense"], default="standard")

        if os.path.exists(filepath):
            try:
                import pandas as pd
                df = pd.read_csv(filepath)
                console.print(f"\n[dim]{len(df)} lignes trouvees[/dim]")
                console.print(f"[dim]Colonnes: {', '.join(df.columns[:10])}...[/dim]")

                player_id = choisir_joueur()
                if player_id:
                    imported = 0
                    for _, row in df.iterrows():
                        season = str(row.get("Season", ""))
                        club = str(row.get("Squad", ""))
                        if not season:
                            continue

                        if stat_type == "standard":
                            stats = {}
                            col_map = {
                                "MP": "matches_played", "Starts": "starts", "Min": "minutes",
                                "Gls": "goals", "Ast": "assists", "G-PK": "goals_pens",
                                "PK": "pens_made", "PKatt": "pens_att",
                                "CrdY": "yellow_cards", "CrdR": "red_cards",
                                "xG": "xg", "xAG": "xag",
                                "PrgC": "progressive_carries", "PrgP": "progressive_passes",
                            }
                            for csv_col, db_col in col_map.items():
                                if csv_col in row and pd.notna(row[csv_col]):
                                    try:
                                        stats[db_col] = float(row[csv_col]) if '.' in str(row[csv_col]) else int(row[csv_col])
                                    except (ValueError, TypeError):
                                        pass
                            add_season_stats(player_id, season, club, **stats)
                            imported += 1

                    console.print(f"\n[bold green]{imported} lignes importees[/bold green]")
            except Exception as e:
                console.print(f"[red]Erreur: {e}[/red]")
        else:
            console.print(f"[red]Fichier introuvable: {filepath}[/red]")

    elif choix == "3":
        console.print("\n[dim]Lancement du scraper FBref...[/dim]")
        try:
            from scraper.fbref import scrape_all_players
            scrape_all_players(max_players=5)
            console.print("[bold green]Scraping termine.[/bold green]")
        except ImportError:
            console.print("[red]Le scraper n'est pas configure pour Supabase. Utilise l'import CSV.[/red]")
        except Exception as e:
            console.print(f"[red]Erreur: {e}[/red]")

    Prompt.ask("\nAppuie sur Entree")


# ============================================
# 10. EXPORTER
# ============================================

def page_exporter():
    banner()
    console.print("[bold]Exporter les donnees[/bold]\n")

    options = [
        ("1", "Tous les joueurs (CSV)"),
        ("2", "Tous les joueurs (JSON)"),
        ("3", "Stats saison (CSV)"),
        ("4", "Profil complet d'un joueur (JSON)"),
    ]

    for num, label in options:
        console.print(f"  [{OR}][{num}][/{OR}] {label}")

    choix = Prompt.ask("\nChoix", choices=["1", "2", "3", "4"])
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if choix == "1":
        players = get_all_players()
        filepath = f"export_joueurs_{timestamp}.csv"
        if players:
            with open(filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=players[0].keys())
                writer.writeheader()
                writer.writerows(players)
            console.print(f"\n[bold green]Exporte: {filepath} ({len(players)} joueurs)[/bold green]")

    elif choix == "2":
        players = get_all_players()
        filepath = f"export_joueurs_{timestamp}.json"
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(players, f, ensure_ascii=False, indent=2, default=str)
        console.print(f"\n[bold green]Exporte: {filepath} ({len(players)} joueurs)[/bold green]")

    elif choix == "3":
        data = get_latest_stats()
        filepath = f"export_stats_{timestamp}.csv"
        if data:
            with open(filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            console.print(f"\n[bold green]Exporte: {filepath} ({len(data)} lignes)[/bold green]")
        else:
            console.print("[dim]Pas de stats a exporter.[/dim]")

    elif choix == "4":
        player_id = choisir_joueur()
        if player_id:
            profile = get_player_full_profile(player_id)
            filepath = f"export_{profile['name'].replace(' ', '_').lower()}_{timestamp}.json"
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(profile, f, ensure_ascii=False, indent=2, default=str)
            console.print(f"\n[bold green]Exporte: {filepath}[/bold green]")

    Prompt.ask("\nAppuie sur Entree")


# ============================================
# 11. GENERER UN VISUEL
# ============================================

def page_visuel():
    banner()
    console.print("[bold]Generer un visuel[/bold]\n")

    options = [
        ("1", "Fiche joueur (card)"),
        ("2", "Radar chart"),
        ("3", "Comparaison deux joueurs"),
        ("4", "Top buteurs (classement visuel)"),
    ]

    for num, label in options:
        console.print(f"  [{OR}][{num}][/{OR}] {label}")

    choix = Prompt.ask("\nChoix", choices=["1", "2", "3", "4"])

    try:
        from posts.generator import generate_player_card, generate_radar_chart, generate_comparison, generate_top_chart

        if choix == "1":
            player_id = choisir_joueur()
            if player_id:
                profile = get_player_full_profile(player_id)
                if profile and profile.get("season_stats"):
                    path = generate_player_card(profile)
                    console.print(f"\n[bold green]Visuel genere: {path}[/bold green]")
                else:
                    console.print("[dim]Ce joueur n'a pas de stats. Ajoute des stats d'abord.[/dim]")

        elif choix == "2":
            player_id = choisir_joueur()
            if player_id:
                profile = get_player_full_profile(player_id)
                if profile and profile.get("season_stats"):
                    path = generate_radar_chart(profile)
                    console.print(f"\n[bold green]Radar genere: {path}[/bold green]")
                else:
                    console.print("[dim]Pas de stats pour ce joueur.[/dim]")

        elif choix == "3":
            console.print("Joueur 1:")
            id1 = choisir_joueur()
            console.print("Joueur 2:")
            id2 = choisir_joueur()
            if id1 and id2:
                p1 = get_player_full_profile(id1)
                p2 = get_player_full_profile(id2)
                if p1 and p2:
                    path = generate_comparison(p1, p2)
                    console.print(f"\n[bold green]Comparaison generee: {path}[/bold green]")

        elif choix == "4":
            season = Prompt.ask("Saison", default="2024-25")
            data = get_top_scorers(season=season, limit=5)
            if data:
                path = generate_top_chart(data, f"Top 5 buteurs maliens {season}")
                console.print(f"\n[bold green]Top chart genere: {path}[/bold green]")
            else:
                console.print("[dim]Pas de stats pour cette saison.[/dim]")

    except ImportError as e:
        console.print(f"[red]Module manquant: {e}[/red]")
    except Exception as e:
        console.print(f"[red]Erreur: {e}[/red]")

    Prompt.ask("\nAppuie sur Entree")


# ============================================
# 12. REQUETE SQL LIBRE
# ============================================

def page_sql():
    banner()
    console.print("[bold]Requete SQL libre[/bold]\n")
    console.print("[dim]Tu peux aussi utiliser le SQL Editor sur supabase.com pour des requetes plus complexes.[/dim]")
    console.print("[dim]Ici tu peux interroger les tables via l'API Supabase.[/dim]\n")

    console.print(f"[bold {OR}]Tables disponibles:[/bold {OR}]")
    tables = ["players", "season_stats", "shooting_stats", "passing_stats",
              "defense_stats", "possession_stats", "goalkeeper_stats",
              "match_stats", "transfers", "national_team", "injuries", "awards"]
    for t in tables:
        console.print(f"  - {t}")

    console.print(f"\n[bold {OR}]Vues disponibles:[/bold {OR}]")
    vues = ["v_top_scorers", "v_top_assisters", "v_latest_season", "v_player_summary"]
    for v in vues:
        console.print(f"  - {v}")

    console.print()
    table_name = Prompt.ask("Table ou vue a interroger")

    # Filtre optionnel
    filtre_col = Prompt.ask("Filtrer par colonne [dim](ou vide)[/dim]", default="")
    filtre_val = ""
    if filtre_col:
        filtre_val = Prompt.ask(f"Valeur pour {filtre_col}")

    limit = IntPrompt.ask("Nombre max de resultats", default=20)

    try:
        query = supabase.table(table_name).select("*").limit(limit)
        if filtre_col and filtre_val:
            query = query.ilike(filtre_col, f"%{filtre_val}%")

        result = query.execute()

        if result.data:
            table = Table(box=box.ROUNDED, border_style=VERT, header_style=f"bold {OR}")
            keys = list(result.data[0].keys())
            # Limiter les colonnes affichees
            if len(keys) > 12:
                keys = keys[:12]
            for k in keys:
                table.add_column(k, max_width=20, overflow="ellipsis")
            for row in result.data:
                table.add_row(*[str(row.get(k, ""))[:20] for k in keys])
            console.print(table)
            console.print(f"\n[dim]{len(result.data)} resultats[/dim]")
        else:
            console.print("[dim]Aucun resultat.[/dim]")
    except Exception as e:
        console.print(f"[red]Erreur: {e}[/red]")

    Prompt.ask("\nAppuie sur Entree")


# ============================================
# UTILITAIRES
# ============================================

def choisir_joueur():
    """Permet de choisir un joueur par recherche ou ID."""
    choix = Prompt.ask("Nom du joueur ou ID [dim](ou 'liste' pour tout voir)[/dim]")

    if choix.lower() == "liste":
        players = get_all_players()
        afficher_joueurs(players)
        choix = Prompt.ask("\nID du joueur")

    # Si c'est un nombre, c'est un ID
    if choix.isdigit():
        return int(choix)

    # Sinon, recherche par nom
    resultats = search_players(choix)
    if not resultats:
        console.print(f"[dim]Aucun joueur trouve pour '{choix}'[/dim]")
        return None
    elif len(resultats) == 1:
        console.print(f"  -> {resultats[0]['name']} (ID: {resultats[0]['id']})")
        return resultats[0]["id"]
    else:
        afficher_joueurs(resultats)
        id_choisi = Prompt.ask("\nID du joueur")
        return int(id_choisi) if id_choisi.isdigit() else None


if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        console.print("\n[dim]Au revoir.[/dim]")
