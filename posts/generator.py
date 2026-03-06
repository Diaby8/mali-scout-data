"""
Generateur de visuels pour les reseaux sociaux.
Fiches joueurs, radars, comparaisons - aux couleurs du Mali.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import COLORS, POSTS_OUTPUT

GREEN = COLORS["green"]
GOLD = COLORS["gold"]
RED = COLORS["red"]
BG = COLORS["bg_dark"]
BG2 = COLORS["bg_card"]
WHITE = COLORS["white"]


def _ensure_output():
    os.makedirs(POSTS_OUTPUT, exist_ok=True)


def create_player_card(player_name, club, position, stats, output_path=None):
    """Genere une fiche joueur visuelle."""
    _ensure_output()
    output_path = output_path or POSTS_OUTPUT

    fig, ax = plt.subplots(figsize=(8, 10))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis("off")

    # Bandes drapeau Mali
    ax.axhspan(10.5, 12, color=GREEN, alpha=0.9)
    ax.axhspan(10.0, 10.5, color=GOLD, alpha=0.9)
    ax.axhspan(9.7, 10.0, color=RED, alpha=0.9)

    # Nom
    ax.text(5, 11.2, player_name.upper(), fontsize=28, fontweight="bold",
            color=WHITE, ha="center", va="center", fontfamily="sans-serif")

    # Club | Poste
    ax.text(5, 10.25, f"{club}  |  {position}", fontsize=14,
            color=BG, ha="center", va="center", fontweight="bold")

    # Stats en grille
    stat_keys = list(stats.keys())
    stat_vals = list(stats.values())
    cols = min(len(stat_keys), 3)

    for i, (key, val) in enumerate(zip(stat_keys, stat_vals)):
        row = i // cols
        col = i % cols
        x = 1.5 + col * 3.5
        y = 8.5 - row * 2.5

        circle = plt.Circle((x, y), 0.8, color=GREEN, alpha=0.2)
        ax.add_patch(circle)

        ax.text(x, y + 0.1, str(val), fontsize=24, fontweight="bold",
                color=GOLD, ha="center", va="center")
        ax.text(x, y - 1.0, key, fontsize=11,
                color=WHITE, ha="center", va="center", alpha=0.8)

    # Footer
    ax.text(5, 0.5, "MALI SCOUT DATA", fontsize=10, color=WHITE,
            ha="center", va="center", alpha=0.4, fontstyle="italic")

    filepath = os.path.join(output_path,
                            f"{player_name.replace(' ', '_').lower()}_card.png")
    fig.savefig(filepath, dpi=150, bbox_inches="tight",
                facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close(fig)
    return filepath


def create_radar_chart(player_name, categories, values, max_val=100.0,
                       output_path=None):
    """Genere un radar chart pour un joueur."""
    _ensure_output()
    output_path = output_path or POSTS_OUTPUT

    N = len(categories)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    values_plot = values + [values[0]]
    angles += [angles[0]]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    ax.plot(angles, values_plot, color=GOLD, linewidth=2)
    ax.fill(angles, values_plot, color=GREEN, alpha=0.3)
    ax.scatter(angles[:-1], values, color=GOLD, s=80, zorder=5)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=10, color=WHITE, fontweight="bold")
    ax.set_ylim(0, max_val)
    ax.set_yticks([])
    ax.spines["polar"].set_color(WHITE)
    ax.spines["polar"].set_alpha(0.3)
    ax.grid(color=WHITE, alpha=0.1)

    ax.set_title(player_name.upper(), fontsize=20, fontweight="bold",
                 color=WHITE, pad=30)

    filepath = os.path.join(output_path,
                            f"{player_name.replace(' ', '_').lower()}_radar.png")
    fig.savefig(filepath, dpi=150, bbox_inches="tight",
                facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close(fig)
    return filepath


def create_comparison(player1, stats1, player2, stats2, output_path=None):
    """Genere un visuel comparatif entre 2 joueurs."""
    _ensure_output()
    output_path = output_path or POSTS_OUTPUT

    categories = list(stats1.keys())
    vals1 = list(stats1.values())
    vals2 = list(stats2.values())

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    x = np.arange(len(categories))
    width = 0.35

    bars1 = ax.bar(x - width/2, vals1, width, label=player1,
                   color=GREEN, alpha=0.85, edgecolor="white", linewidth=0.5)
    bars2 = ax.bar(x + width/2, vals2, width, label=player2,
                   color=GOLD, alpha=0.85, edgecolor="white", linewidth=0.5)

    for bar in bars1:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                f"{bar.get_height():.0f}", ha="center", va="bottom",
                color=WHITE, fontsize=10, fontweight="bold")
    for bar in bars2:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                f"{bar.get_height():.0f}", ha="center", va="bottom",
                color=WHITE, fontsize=10, fontweight="bold")

    ax.set_xticks(x)
    ax.set_xticklabels(categories, color=WHITE, fontsize=11, fontweight="bold")
    ax.tick_params(axis="y", colors=WHITE)
    ax.legend(fontsize=12, loc="upper right",
              facecolor=BG, edgecolor=WHITE, labelcolor=WHITE)
    ax.spines["bottom"].set_color(WHITE)
    ax.spines["left"].set_color(WHITE)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_title(f"{player1} vs {player2}", fontsize=18, fontweight="bold",
                 color=WHITE, pad=15)

    safe = f"compare_{player1}_{player2}".replace(" ", "_").lower()
    filepath = os.path.join(output_path, f"{safe}.png")
    fig.savefig(filepath, dpi=150, bbox_inches="tight",
                facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close(fig)
    return filepath


def create_top_chart(title, players, values, stat_name, output_path=None):
    """Genere un classement top N joueurs."""
    _ensure_output()
    output_path = output_path or POSTS_OUTPUT

    fig, ax = plt.subplots(figsize=(10, max(4, len(players) * 0.8)))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    y = np.arange(len(players))
    colors = [GREEN if i == 0 else GOLD if i < 3 else WHITE for i in range(len(players))]
    alphas = [0.9 if i < 3 else 0.6 for i in range(len(players))]

    bars = ax.barh(y, values, color=colors, alpha=0.8, edgecolor=BG, height=0.6)

    for i, (bar, val) in enumerate(zip(bars, values)):
        ax.text(bar.get_width() + max(values)*0.02, bar.get_y() + bar.get_height()/2,
                f" {val}", va="center", color=WHITE, fontsize=12, fontweight="bold")

    ax.set_yticks(y)
    ax.set_yticklabels(players, color=WHITE, fontsize=12, fontweight="bold")
    ax.invert_yaxis()
    ax.set_xlabel(stat_name, color=WHITE, fontsize=12)
    ax.tick_params(axis="x", colors=WHITE)
    ax.spines["bottom"].set_color(WHITE)
    ax.spines["left"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.set_title(title, fontsize=18, fontweight="bold", color=GOLD, pad=15)

    # Footer
    fig.text(0.5, 0.02, "MALI SCOUT DATA", ha="center",
             fontsize=9, color=WHITE, alpha=0.4, fontstyle="italic")

    safe = title.replace(" ", "_").lower()[:40]
    filepath = os.path.join(output_path, f"{safe}.png")
    fig.savefig(filepath, dpi=150, bbox_inches="tight",
                facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close(fig)
    return filepath


def generate_tweet_text(player_name, stats, hashtags=None):
    """Genere un texte de tweet avec les stats d'un joueur."""
    if hashtags is None:
        hashtags = ["#Mali", "#Football", "#ScoutData", "#Aigles"]

    lines = [f"{player_name.upper()}\n"]
    for k, v in stats.items():
        lines.append(f"{k}: {v}")
    lines.append("")
    lines.append(" ".join(hashtags))
    return "\n".join(lines)


if __name__ == "__main__":
    # Test
    card = create_player_card(
        "Amadou Haidara", "RB Leipzig", "Milieu",
        {"Matchs": 28, "Buts": 5, "Passes D.": 7, "xG": 4.2, "Tacles": 45, "Min": 2300}
    )
    print(f"Card: {card}")

    radar = create_radar_chart(
        "Amadou Haidara",
        ["Tir", "Passe", "Dribble", "Defense", "Physique", "Vision"],
        [72, 78, 65, 80, 85, 75]
    )
    print(f"Radar: {radar}")

    comp = create_comparison(
        "Haidara", {"Buts": 5, "Passes D.": 7, "Tacles": 45, "xG": 4.2},
        "Bissouma", {"Buts": 3, "Passes D.": 4, "Tacles": 62, "xG": 2.8},
    )
    print(f"Compare: {comp}")

    top = create_top_chart(
        "Top 5 Buteurs Maliens 2024-25",
        ["El Bilal Toure", "Sekou Koita", "Amadou Haidara", "Moussa Djenepo", "Adama Traore"],
        [12, 9, 5, 4, 3], "Buts"
    )
    print(f"Top: {top}")
