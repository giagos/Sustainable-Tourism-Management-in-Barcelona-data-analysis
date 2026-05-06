import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from make_gamma_export_folder import COLORS, load_table, save_figure


def main():
    data = load_table("district_spatial_inequality.csv").copy()
    data = data.sort_values("tourism_surplus_vs_population_pct_points", ascending=True)
    y = np.arange(len(data))

    fig, ax = plt.subplots(figsize=(13.333, 7.5))
    ax.barh(y - 0.18, data["population_share_pct"], height=0.34, color="#93C5FD", label="Resident population share")
    ax.barh(y + 0.18, data["tourism_unit_share_pct"], height=0.34, color="#F97316", label="Tourism-unit share")
    ax.set_yticks(y)
    ax.set_yticklabels(data["district_name"])
    ax.set_title("District Pressure Burden: Population Share vs Tourism-Accommodation Share", loc="left", fontsize=21, pad=18)
    ax.set_xlabel("Share of city total (%)")
    ax.set_ylabel("")
    ax.legend(loc="lower right", frameon=True)
    for idx, row in enumerate(data.itertuples()):
        surplus = row.tourism_surplus_vs_population_pct_points
        color = COLORS["red"] if surplus > 0 else COLORS["blue"]
        ax.text(max(row.population_share_pct, row.tourism_unit_share_pct) + 0.7, idx, f"{surplus:+.1f} pp", va="center", color=color, fontsize=10.5, fontweight="bold")
    sns.despine(ax=ax, left=True)
    fig.subplots_adjust(left=0.19, right=0.91, top=0.82, bottom=0.15)
    save_figure(fig, "03_district_pressure_burden.png")


if __name__ == "__main__":
    main()