import matplotlib.pyplot as plt
import pandas as pd

from make_gamma_export_folder import COLORS, save_figure


def stakeholder_data():
    return pd.DataFrame(
        [
            {"stakeholder": "Residents", "power": 4.0, "exposure": 9.2, "group": "high exposure"},
            {"stakeholder": "Neighbourhood NGOs", "power": 5.0, "exposure": 8.4, "group": "high exposure"},
            {"stakeholder": "Municipality", "power": 9.0, "exposure": 7.1, "group": "decision maker"},
            {"stakeholder": "Platforms", "power": 8.2, "exposure": 5.8, "group": "market actor"},
            {"stakeholder": "Hotels", "power": 7.0, "exposure": 5.2, "group": "market actor"},
            {"stakeholder": "Port authority", "power": 7.3, "exposure": 4.6, "group": "infrastructure"},
            {"stakeholder": "Local businesses", "power": 5.5, "exposure": 6.2, "group": "local economy"},
            {"stakeholder": "Tourists", "power": 2.4, "exposure": 3.9, "group": "users"},
        ]
    )


def main():
    data = stakeholder_data()
    palette = {
        "high exposure": COLORS["red"],
        "decision maker": COLORS["blue"],
        "market actor": COLORS["purple"],
        "infrastructure": COLORS["teal"],
        "local economy": COLORS["amber"],
        "users": COLORS["green"],
    }

    fig, ax = plt.subplots(figsize=(13.333, 7.5))
    ax.axvspan(0, 5, ymin=0.5, ymax=1, color="#FEE2E2", alpha=0.35)
    ax.axvspan(5, 10, ymin=0.5, ymax=1, color="#DBEAFE", alpha=0.35)
    ax.axhline(5, color=COLORS["line"], linewidth=1.4)
    ax.axvline(5, color=COLORS["line"], linewidth=1.4)
    for _, row in data.iterrows():
        ax.scatter(row["power"], row["exposure"], s=520, color=palette[row["group"]], edgecolor="white", linewidth=2.0, zorder=3)
        ax.annotate(row["stakeholder"], (row["power"], row["exposure"]), xytext=(8, 5), textcoords="offset points", fontsize=11, fontweight="bold")
    ax.text(2.5, 9.6, "High exposure\nlow formal power", ha="center", va="top", fontsize=12, color=COLORS["red"], fontweight="bold")
    ax.text(7.5, 9.6, "High power\nhigh responsibility", ha="center", va="top", fontsize=12, color=COLORS["blue"], fontweight="bold")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_xlabel("Decision power")
    ax.set_ylabel("Pressure exposure")
    ax.set_title("Stakeholder Power-Exposure Matrix", loc="left", fontsize=23, pad=18)
    fig.subplots_adjust(left=0.10, right=0.94, top=0.82, bottom=0.14)
    save_figure(fig, "06_stakeholder_power_exposure_matrix.png", source="Conceptual stakeholder scoring based on analysed pressure evidence")


if __name__ == "__main__":
    main()