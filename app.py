"""
Mali Scout Data - Dashboard Streamlit
Interface complete pour le scouting des joueurs maliens.
"""

import streamlit as st
import pandas as pd
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import COLORS, DB_PATH
from database.db import (
    init_db, get_all_players, get_player_by_name, get_player_by_id,
    get_player_stats, get_latest_stats, get_db_summary,
    get_player_full_profile, upsert_player, upsert_season_stats
)
from posts.generator import (
    create_player_card, create_radar_chart, create_comparison,
    create_top_chart, generate_tweet_text
)
from scraper.fbref import import_from_paste, add_player_manual, MALI_PLAYERS_FBREF

# --- Config ---
st.set_page_config(
    page_title="Mali Scout Data",
    page_icon="\U0001F1F2\U0001F1F1",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Init DB ---
init_db()

# --- CSS ---
st.markdown(f"""
<style>
    .main-header {{
        background: linear-gradient(90deg, {COLORS['green']} 0%, {COLORS['gold']} 50%, {COLORS['red']} 100%);
        padding: 3px;
        border-radius: 10px;
        margin-bottom: 20px;
    }}
    .main-header-inner {{
        background: {COLORS['bg_dark']};
        padding: 15px;
        border-radius: 8px;
        text-align: center;
    }}
    .main-header-inner h1 {{
        color: {COLORS['gold']};
        margin: 0;
        font-size: 2em;
    }}
    .main-header-inner p {{
        color: {COLORS['white']};
        opacity: 0.7;
        margin: 0;
    }}
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div class="main-header">
    <div class="main-header-inner">
        <h1>MALI SCOUT DATA</h1>
        <p>Scouting & analyse des joueurs maliens</p>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("", [
    "Dashboard",
    "Fiche Joueur",
    "Comparaison",
    "Generateur de Posts",
    "Importer des donnees",
])

# Afficher resume DB dans sidebar
summary = get_db_summary()
st.sidebar.markdown("---")
st.sidebar.markdown(f"**Base de donnees**")
st.sidebar.markdown(f"Joueurs: **{summary['joueurs']}**")
st.sidebar.markdown(f"Stats saison: **{summary['stats_saison']}**")


# =============================================================================
# DASHBOARD
# =============================================================================
if page == "Dashboard":
    st.header("Vue d'ensemble")

    players = get_all_players()
    if not players:
        st.warning("Base vide. Va dans **Importer des donnees** pour commencer.")
        st.stop()

    players_df = pd.DataFrame(players)

    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Joueurs", len(players_df))
    with col2:
        positions = players_df["position"].value_counts()
        st.metric("Postes", len(positions))
    with col3:
        clubs = players_df["current_club"].dropna().nunique()
        st.metric("Clubs", clubs)
    with col4:
        st.metric("Stats en base", summary["stats_saison"])

    # Tableau joueurs
    st.subheader("Effectif")
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        pos_options = ["Tous"] + sorted(players_df["position"].dropna().unique().tolist())
        pos_filter = st.selectbox("Filtrer par poste", pos_options)
    with col_f2:
        search = st.text_input("Rechercher un joueur")

    display_df = players_df[["name", "position", "current_club", "current_league", "birth_year"]].copy()
    display_df.columns = ["Joueur", "Poste", "Club", "Ligue", "Annee naiss."]

    if pos_filter != "Tous":
        display_df = display_df[display_df["Poste"] == pos_filter]
    if search:
        display_df = display_df[display_df["Joueur"].str.contains(search, case=False, na=False)]

    st.dataframe(display_df, use_container_width=True, hide_index=True)

    # Stats si disponibles
    latest = get_latest_stats()
    if latest:
        st.subheader("Dernieres stats")
        stats_df = pd.DataFrame(latest)
        show_cols = ["name", "position", "current_club", "season", "matches_played",
                     "goals", "assists", "minutes", "xg", "xag"]
        show_cols = [c for c in show_cols if c in stats_df.columns]
        if show_cols:
            st.dataframe(stats_df[show_cols].rename(columns={
                "name": "Joueur", "position": "Poste", "current_club": "Club",
                "season": "Saison", "matches_played": "MJ", "goals": "Buts",
                "assists": "PD", "minutes": "Min", "xg": "xG", "xag": "xAG"
            }), use_container_width=True, hide_index=True)


# =============================================================================
# FICHE JOUEUR
# =============================================================================
elif page == "Fiche Joueur":
    st.header("Fiche Joueur")

    players = get_all_players()
    if not players:
        st.warning("Aucun joueur en base.")
        st.stop()

    player_names = [p["name"] for p in players]
    selected = st.selectbox("Selectionne un joueur", player_names)

    player = [p for p in players if p["name"] == selected][0]
    profile = get_player_full_profile(player["id"])

    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader(player["name"])
        st.write(f"**Poste:** {player.get('position', 'N/A')}")
        st.write(f"**Club:** {player.get('current_club', 'N/A')}")
        st.write(f"**Ligue:** {player.get('current_league', 'N/A')}")
        if player.get("birth_year"):
            st.write(f"**Annee de naissance:** {player['birth_year']}")
        if player.get("fbref_url"):
            st.markdown(f"[Voir sur FBref]({player['fbref_url']})")

    with col2:
        if profile and profile.get("season_stats"):
            stats = profile["season_stats"]
            if stats:
                last = stats[0]  # Plus recente
                metrics = {}
                if last.get("matches_played") is not None:
                    metrics["Matchs"] = last["matches_played"]
                if last.get("goals") is not None:
                    metrics["Buts"] = last["goals"]
                if last.get("assists") is not None:
                    metrics["Passes D."] = last["assists"]
                if last.get("minutes") is not None:
                    metrics["Minutes"] = last["minutes"]
                if last.get("xg") is not None:
                    metrics["xG"] = round(last["xg"], 1)
                if last.get("xag") is not None:
                    metrics["xAG"] = round(last["xag"], 1)

                if metrics:
                    cols = st.columns(len(metrics))
                    for i, (label, val) in enumerate(metrics.items()):
                        with cols[i]:
                            st.metric(label, val)

    # Historique
    if profile and profile.get("season_stats"):
        st.subheader("Historique par saison")
        hist_df = pd.DataFrame(profile["season_stats"])
        show_cols = ["season", "club", "league", "matches_played", "goals",
                     "assists", "minutes", "xg", "xag", "yellow_cards"]
        show_cols = [c for c in show_cols if c in hist_df.columns]
        st.dataframe(hist_df[show_cols].rename(columns={
            "season": "Saison", "club": "Club", "league": "Ligue",
            "matches_played": "MJ", "goals": "Buts", "assists": "PD",
            "minutes": "Min", "xg": "xG", "xag": "xAG",
            "yellow_cards": "CJ"
        }), use_container_width=True, hide_index=True)

    # Generer fiche visuelle
    if st.button("Generer fiche visuelle"):
        stats_vis = {}
        if profile and profile.get("season_stats"):
            last = profile["season_stats"][0]
            for k, label in [("matches_played", "Matchs"), ("goals", "Buts"),
                             ("assists", "PD"), ("minutes", "Min"),
                             ("xg", "xG"), ("xag", "xAG")]:
                if last.get(k) is not None:
                    stats_vis[label] = last[k] if isinstance(last[k], int) else round(last[k], 1)

        fp = create_player_card(
            player["name"],
            player.get("current_club", "N/A"),
            player.get("position", "N/A"),
            stats_vis or {"Info": "Pas de stats"}
        )
        st.image(fp, caption=f"Fiche de {player['name']}")
        with open(fp, "rb") as f:
            st.download_button("Telecharger la fiche", f,
                               file_name=os.path.basename(fp), mime="image/png")


# =============================================================================
# COMPARAISON
# =============================================================================
elif page == "Comparaison":
    st.header("Comparaison de joueurs")

    players = get_all_players()
    if len(players) < 2:
        st.warning("Il faut au moins 2 joueurs en base.")
        st.stop()

    names = [p["name"] for p in players]
    col1, col2 = st.columns(2)
    with col1:
        p1_name = st.selectbox("Joueur 1", names, key="cmp1")
    with col2:
        p2_name = st.selectbox("Joueur 2", names,
                               index=min(1, len(names)-1), key="cmp2")

    if p1_name == p2_name:
        st.warning("Selectionne deux joueurs differents.")
        st.stop()

    p1 = [p for p in players if p["name"] == p1_name][0]
    p2 = [p for p in players if p["name"] == p2_name][0]
    prof1 = get_player_full_profile(p1["id"])
    prof2 = get_player_full_profile(p2["id"])

    has_stats = (prof1 and prof1.get("season_stats") and
                 prof2 and prof2.get("season_stats"))

    if has_stats:
        s1 = prof1["season_stats"][0]
        s2 = prof2["season_stats"][0]

        stat_options = ["goals", "assists", "matches_played", "minutes",
                        "xg", "xag", "yellow_cards"]
        available = [s for s in stat_options
                     if s1.get(s) is not None and s2.get(s) is not None]

        selected_stats = st.multiselect("Stats a comparer", available, default=available[:4])

        if selected_stats:
            labels = {
                "goals": "Buts", "assists": "PD", "matches_played": "MJ",
                "minutes": "Min", "xg": "xG", "xag": "xAG",
                "yellow_cards": "CJ"
            }

            comp_data = {labels.get(s, s): [s1.get(s, 0), s2.get(s, 0)]
                         for s in selected_stats}
            comp_df = pd.DataFrame(comp_data, index=[p1_name, p2_name]).T
            st.dataframe(comp_df, use_container_width=True)

            if st.button("Generer visuel comparatif"):
                stats1 = {labels.get(s, s): float(s1.get(s, 0)) for s in selected_stats}
                stats2 = {labels.get(s, s): float(s2.get(s, 0)) for s in selected_stats}
                fp = create_comparison(p1_name, stats1, p2_name, stats2)
                st.image(fp)
                with open(fp, "rb") as f:
                    st.download_button("Telecharger", f,
                                       file_name=os.path.basename(fp), mime="image/png")
    else:
        st.info("Importe des stats pour pouvoir comparer les joueurs.")


# =============================================================================
# GENERATEUR DE POSTS
# =============================================================================
elif page == "Generateur de Posts":
    st.header("Generateur de Posts Twitter")

    post_type = st.selectbox("Type de post", [
        "Fiche Joueur",
        "Radar Chart",
        "Comparaison",
        "Top Performers"
    ])

    players = get_all_players()
    names = [p["name"] for p in players]

    if post_type == "Fiche Joueur":
        player_name = st.selectbox("Joueur", names)
        player = [p for p in players if p["name"] == player_name][0]
        profile = get_player_full_profile(player["id"])

        custom_stats = st.checkbox("Stats personnalisees")
        if custom_stats:
            col1, col2, col3 = st.columns(3)
            with col1:
                matchs = st.number_input("Matchs", 0, 100, 0)
                buts = st.number_input("Buts", 0, 100, 0)
            with col2:
                pd_val = st.number_input("Passes D.", 0, 100, 0)
                minutes = st.number_input("Minutes", 0, 10000, 0)
            with col3:
                xg = st.number_input("xG", 0.0, 50.0, 0.0, step=0.1)
                xag = st.number_input("xAG", 0.0, 50.0, 0.0, step=0.1)
            stats = {"Matchs": matchs, "Buts": buts, "PD": pd_val,
                     "Min": minutes, "xG": xg, "xAG": xag}
            stats = {k: v for k, v in stats.items() if v > 0}
        else:
            stats = {}
            if profile and profile.get("season_stats"):
                last = profile["season_stats"][0]
                for k, label in [("matches_played", "Matchs"), ("goals", "Buts"),
                                 ("assists", "PD"), ("xg", "xG")]:
                    if last.get(k) is not None:
                        stats[label] = last[k] if isinstance(last[k], int) else round(last[k], 1)

        if st.button("Generer") and stats:
            fp = create_player_card(player_name,
                                    player.get("current_club", "N/A"),
                                    player.get("position", "N/A"), stats)
            st.image(fp)

            tweet = generate_tweet_text(player_name, stats)
            st.text_area("Texte du tweet", tweet, height=150)
            with open(fp, "rb") as f:
                st.download_button("Telecharger", f, file_name=os.path.basename(fp))

    elif post_type == "Radar Chart":
        player_name = st.selectbox("Joueur", names)
        st.info("Entre les valeurs de 0 a 100 pour chaque categorie")

        categories = st.text_input("Categories (virgules)",
                                   "Tir,Passe,Dribble,Defense,Physique,Vision")
        values_str = st.text_input("Valeurs (virgules)", "70,75,65,80,85,70")

        if st.button("Generer"):
            cats = [c.strip() for c in categories.split(",")]
            vals = [float(v.strip()) for v in values_str.split(",")]
            if len(cats) == len(vals):
                fp = create_radar_chart(player_name, cats, vals)
                st.image(fp)
                with open(fp, "rb") as f:
                    st.download_button("Telecharger", f, file_name=os.path.basename(fp))
            else:
                st.error("Nombre de categories et valeurs different!")

    elif post_type == "Comparaison":
        col1, col2 = st.columns(2)
        with col1:
            p1 = st.selectbox("Joueur 1", names, key="post_p1")
        with col2:
            p2 = st.selectbox("Joueur 2", names, index=min(1, len(names)-1), key="post_p2")

        stat_labels = st.text_input("Stats (virgules)", "Buts,PD,Tacles,xG")
        col1, col2 = st.columns(2)
        with col1:
            v1 = st.text_input(f"Valeurs {p1}", "5,7,45,4.2")
        with col2:
            v2 = st.text_input(f"Valeurs {p2}", "3,4,62,2.8")

        if st.button("Generer"):
            labels = [l.strip() for l in stat_labels.split(",")]
            vals1 = [float(v.strip()) for v in v1.split(",")]
            vals2 = [float(v.strip()) for v in v2.split(",")]
            s1 = dict(zip(labels, vals1))
            s2 = dict(zip(labels, vals2))
            fp = create_comparison(p1, s1, p2, s2)
            st.image(fp)
            with open(fp, "rb") as f:
                st.download_button("Telecharger", f, file_name=os.path.basename(fp))

    elif post_type == "Top Performers":
        title = st.text_input("Titre", "Top 5 Buteurs Maliens 2024-25")
        stat_name = st.text_input("Stat", "Buts")
        players_input = st.text_area("Joueurs et valeurs (un par ligne: Nom,Valeur)",
                                     "El Bilal Toure,12\nSekou Koita,9\nAmadou Haidara,5")

        if st.button("Generer"):
            lines = [l.strip() for l in players_input.strip().split("\n") if l.strip()]
            names_list = [l.split(",")[0].strip() for l in lines]
            vals = [float(l.split(",")[1].strip()) for l in lines]
            fp = create_top_chart(title, names_list, vals, stat_name)
            st.image(fp)

            tweet = f"{title}\n\n"
            for i, (n, v) in enumerate(zip(names_list, vals), 1):
                tweet += f"{i}. {n} - {v:.0f} {stat_name}\n"
            tweet += "\n#Mali #Football #ScoutData"
            st.text_area("Texte du tweet", tweet, height=200)
            with open(fp, "rb") as f:
                st.download_button("Telecharger", f, file_name=os.path.basename(fp))


# =============================================================================
# IMPORTER DES DONNEES
# =============================================================================
elif page == "Importer des donnees":
    st.header("Importer des donnees")

    tab1, tab2, tab3 = st.tabs(["CSV FBref", "Ajout manuel", "Scraping"])

    # --- TAB 1: CSV ---
    with tab1:
        st.subheader("Importer depuis FBref (CSV)")
        st.markdown("""
        **Comment faire:**
        1. Va sur [FBref](https://fbref.com) - page d'un joueur ou d'une equipe
        2. Trouve le tableau de stats voulu
        3. Clique sur **Share & Export** au-dessus du tableau
        4. Choisis **Get table as CSV (for Excel)**
        5. Copie tout le texte et colle-le ci-dessous
        """)

        data_type = st.selectbox("Type de stats",
                                 ["standard", "shooting", "passing", "defense"],
                                 key="csv_type")

        csv_text = st.text_area("Colle le CSV ici", height=200, key="csv_paste")

        if st.button("Importer le CSV") and csv_text.strip():
            try:
                count = import_from_paste(csv_text, data_type)
                st.success(f"{count} joueurs importes!")
                st.rerun()
            except Exception as e:
                st.error(f"Erreur: {e}")

        # Upload fichier
        uploaded = st.file_uploader("Ou uploade un fichier CSV", type=["csv"])
        if uploaded:
            csv_path = os.path.join("data", uploaded.name)
            with open(csv_path, "wb") as f:
                f.write(uploaded.read())
            st.success(f"Fichier sauvegarde: {csv_path}")
            if st.button("Importer le fichier"):
                from scraper.fbref import import_from_csv
                count = import_from_csv(csv_path, data_type)
                st.success(f"{count} joueurs importes!")

    # --- TAB 2: Manuel ---
    with tab2:
        st.subheader("Ajouter un joueur manuellement")

        col1, col2 = st.columns(2)
        with col1:
            m_name = st.text_input("Nom du joueur")
            m_pos = st.selectbox("Poste", ["GK", "DF", "MF", "FW"])
            m_club = st.text_input("Club actuel")
        with col2:
            m_season = st.text_input("Saison", "2024-2025")
            m_goals = st.number_input("Buts", 0, 100, 0)
            m_assists = st.number_input("Passes decisives", 0, 100, 0)

        col3, col4 = st.columns(2)
        with col3:
            m_matches = st.number_input("Matchs joues", 0, 100, 0)
            m_minutes = st.number_input("Minutes", 0, 10000, 0)
        with col4:
            m_xg = st.number_input("xG", 0.0, 50.0, 0.0, step=0.1)
            m_xag = st.number_input("xAG", 0.0, 50.0, 0.0, step=0.1)

        if st.button("Ajouter le joueur") and m_name:
            add_player_manual(
                m_name, m_pos, m_club, m_season,
                goals=m_goals or None,
                assists=m_assists or None,
                matches=m_matches or None,
                minutes=m_minutes or None,
                xg=m_xg or None,
                xag=m_xag or None,
            )
            st.success(f"{m_name} ajoute!")
            st.rerun()

    # --- TAB 3: Scraping ---
    with tab3:
        st.subheader("Scraping FBref")
        st.info("Le scraping direct de FBref peut etre bloque par Cloudflare. "
                "L'import CSV est plus fiable.")

        st.markdown("**Joueurs pre-configures:**")
        for p in MALI_PLAYERS_FBREF:
            st.markdown(f"- {p['name']} ({p['pos']})")

        if st.button("Tenter le scraping"):
            st.warning("Le scraping necessite Chrome et peut prendre du temps. "
                       "Lance cette commande dans le terminal:\n\n"
                       "`python scraper/fbref.py --scrape --max 3`")
