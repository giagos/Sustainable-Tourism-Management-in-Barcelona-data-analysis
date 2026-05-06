import math

import matplotlib.pyplot as plt
from matplotlib.patches import Circle

from make_gamma_export_folder import COLORS, save_figure, wrap_text


def main():
    fig, ax = plt.subplots(figsize=(13.333, 7.5))
    ax.axis("off")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    fig.text(0.055, 0.92, "Barcelona Tourism Pressure Council", fontsize=24, fontweight="bold", color=COLORS["ink"])
    fig.text(0.055, 0.865, "Proposed participatory governance body for evidence review and policy triggers.", fontsize=12.5, color=COLORS["muted"])

    center = (0.50, 0.48)
    central = Circle(center, 0.14, facecolor=COLORS["blue"], edgecolor="white", linewidth=2.5)
    ax.add_patch(central)
    ax.text(center[0], center[1], "Tourism\nPressure\nCouncil", ha="center", va="center", fontsize=17, fontweight="bold", color="white")

    nodes = [
        ("Residents\nand neighbourhoods", COLORS["red"]),
        ("District\ncouncils", COLORS["orange"]),
        ("City tourism\noffice", COLORS["blue"]),
        ("Port\nauthority", COLORS["teal"]),
        ("Hotels and\nlicensed sector", COLORS["purple"]),
        ("Platform data\nliaison", COLORS["pink"]),
        ("Environmental\nNGOs", COLORS["green"]),
        ("Academic\ndata lab", COLORS["amber"]),
    ]
    radius = 0.34
    for idx, (label, color) in enumerate(nodes):
        angle = math.radians(90 - idx * 360 / len(nodes))
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        ax.plot([center[0], x], [center[1], y], color="#94A3B8", linewidth=1.8, zorder=1)
        node = Circle((x, y), 0.085, facecolor="white", edgecolor=color, linewidth=2.2, zorder=2)
        ax.add_patch(node)
        ax.text(x, y, label, ha="center", va="center", fontsize=10.5, fontweight="bold", color=color, zorder=3)

    ax.text(0.08, 0.10, wrap_text("Mandate: review red/amber pressure indicators, publish minutes, recommend policy response, and track whether pressure is reduced or displaced.", 92), fontsize=11.2, color=COLORS["muted"])
    save_figure(fig, "10_barcelona_tourism_pressure_council.png", source="Conceptual participation design for A2")


if __name__ == "__main__":
    main()