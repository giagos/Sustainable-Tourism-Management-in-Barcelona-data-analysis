import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from make_gamma_export_folder import COLORS, save_figure, wrap_text


def box(ax, x, y, w, h, title, body, color):
    ax.add_patch(Rectangle((x, y), w, h, transform=ax.transAxes, facecolor="white", edgecolor=color, linewidth=2.0))
    ax.add_patch(Rectangle((x, y + h - 0.045), w, 0.045, transform=ax.transAxes, facecolor=color, edgecolor=color))
    ax.text(x + 0.018, y + h - 0.075, title, transform=ax.transAxes, fontsize=10.8, fontweight="bold", color=color, va="top")
    ax.text(x + 0.018, y + h - 0.128, wrap_text(body, 31), transform=ax.transAxes, fontsize=7.7, color=COLORS["ink"], va="top", linespacing=0.92)


def arrow(ax, start, end):
    ax.annotate("", xy=end, xytext=start, xycoords=ax.transAxes, textcoords=ax.transAxes, arrowprops={"arrowstyle": "->", "linewidth": 2.2, "color": COLORS["ink"]})


def main():
    fig, ax = plt.subplots(figsize=(13.333, 7.5))
    ax.axis("off")
    fig.text(0.055, 0.92, "TPI-Triggered Governance Model", fontsize=24, fontweight="bold", color=COLORS["ink"])
    fig.text(0.055, 0.865, "A data-driven loop that converts tourism pressure evidence into participatory policy response.", fontsize=12.5, color=COLORS["muted"])

    boxes = [
        (0.06, 0.52, 0.20, 0.24, "1. Data inputs", "Airbnb, HUT licences, port passengers, population and environmental proxies.", COLORS["blue"]),
        (0.30, 0.52, 0.20, 0.24, "2. TPI thresholds", "Green: monitor. Amber: district review. Red: stakeholder action.", COLORS["amber"]),
        (0.54, 0.52, 0.20, 0.24, "3. Stakeholder action", "Residents, NGOs, municipality, hotels, platforms and port review evidence.", COLORS["purple"]),
        (0.78, 0.52, 0.17, 0.24, "4. Policy response", "Licensing, enforcement, port scheduling and demand shifting.", COLORS["red"]),
        (0.34, 0.15, 0.32, 0.20, "5. Monitoring feedback", "Dashboard checks whether pressure falls, moves or creates conflicts.", COLORS["teal"]),
    ]
    for args in boxes:
        box(ax, *args)
    arrow(ax, (0.265, 0.64), (0.30, 0.64))
    arrow(ax, (0.505, 0.64), (0.54, 0.64))
    arrow(ax, (0.745, 0.64), (0.78, 0.64))
    arrow(ax, (0.865, 0.52), (0.63, 0.33))
    arrow(ax, (0.34, 0.27), (0.16, 0.52))
    save_figure(fig, "09_tpi_triggered_governance_model.png", source="Conceptual governance model built from TPI indicators")


if __name__ == "__main__":
    main()