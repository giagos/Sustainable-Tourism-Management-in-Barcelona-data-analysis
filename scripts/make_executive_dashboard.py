import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from make_gamma_export_folder import COLORS, load_table, pct, save_figure, short_number, wrap_text


def draw_card(ax, xy, width, height, title, value, note, color):
    x, y = xy
    ax.add_patch(
        Rectangle((x, y), width, height, transform=ax.transAxes, facecolor=COLORS["panel"], edgecolor="#D8DEE9", linewidth=1.4)
    )
    ax.add_patch(Rectangle((x, y + height - 0.035), width, 0.035, transform=ax.transAxes, facecolor=color, edgecolor=color))
    ax.text(x + 0.025, y + height - 0.078, wrap_text(title, 18), transform=ax.transAxes, fontsize=9.3, fontweight="bold", color=COLORS["muted"], va="top", linespacing=0.9)
    ax.text(x + 0.025, y + 0.112, value, transform=ax.transAxes, fontsize=20.0, fontweight="bold", color=color, va="center")
    ax.text(x + 0.025, y + 0.022, wrap_text(note, 28), transform=ax.transAxes, fontsize=7.3, color=COLORS["muted"], va="bottom", linespacing=0.96)


def main():
    top_tpi = load_table("top_tpi_neighbourhoods.csv")
    top_airbnb = load_table("top_airbnb_neighbourhoods.csv")
    concentration = load_table("concentration_diagnostics.csv")
    port_peak = load_table("port_peak_pressure.csv")

    tpi_max = top_tpi.iloc[0]
    tpi_second = top_tpi.iloc[1]
    airbnb_max = top_airbnb.iloc[0]
    hut_concentration = concentration[concentration["indicator"].str.contains("HUT", case=False, na=False)].iloc[0]
    port_peak_row = port_peak.sort_values("peak_to_average_ratio", ascending=False).iloc[0]

    cards = [
        (
            "Max neighbourhood TPI",
            short_number(tpi_max["tpi_0_100"], 1),
            f"{tpi_max['neighbourhood_name']} ({tpi_max['district_name']})",
            COLORS["red"],
        ),
        (
            "Second TPI hotspot",
            short_number(tpi_second["tpi_0_100"], 1),
            f"{tpi_second['neighbourhood_name']} ({tpi_second['district_name']})",
            COLORS["orange"],
        ),
        (
            "Airbnb intensity",
            short_number(airbnb_max["airbnb_per_1000_residents"], 1),
            "listings per 1,000 residents",
            COLORS["blue"],
        ),
        (
            "HUT top-10 concentration",
            pct(hut_concentration["top_10_share_pct"], 1),
            "share of licences in top 10 neighbourhoods",
            COLORS["purple"],
        ),
        (
            "Port peak stress",
            f"{port_peak_row['peak_to_average_ratio']:.2f}x",
            f"peak / average month, {int(port_peak_row['year'])}",
            COLORS["teal"],
        ),
    ]

    fig, ax = plt.subplots(figsize=(13.333, 7.5))
    ax.axis("off")
    fig.text(0.055, 0.92, "Barcelona Tourism Pressure Evidence Dashboard", fontsize=24, fontweight="bold", color=COLORS["ink"])
    fig.text(
        0.055,
        0.865,
        "Opening evidence slide for A2: the strongest measurable signals from the analysis pipeline.",
        fontsize=12.5,
        color=COLORS["muted"],
    )

    positions = [(0.055, 0.55), (0.37, 0.55), (0.685, 0.55), (0.20, 0.21), (0.515, 0.21)]
    for position, card in zip(positions, cards):
        draw_card(ax, position, 0.26, 0.25, *card)

    save_figure(fig, "01_executive_evidence_dashboard.png")


if __name__ == "__main__":
    main()