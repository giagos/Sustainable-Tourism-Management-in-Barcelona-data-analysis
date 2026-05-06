import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from make_gamma_export_folder import COLORS, load_table, normalize_0_100, save_figure


def main():
    district = load_table("district_pressure_summary.csv").copy()
    district["tourism_units"] = district["listings"] + district["hut_licenses"]
    district["gross_value_index"] = normalize_0_100(district["tourism_units"]).fillna(0)
    district["pressure_penalty"] = np.clip(district["mean_tpi_0_100"] / 100 * 0.70, 0, 0.70)
    district["pressure_adjusted_value_index"] = district["gross_value_index"] * (1 - district["pressure_penalty"])
    plot = district.sort_values("gross_value_index", ascending=True)

    fig, ax = plt.subplots(figsize=(13.333, 7.5))
    y = np.arange(len(plot))
    ax.barh(y + 0.18, plot["gross_value_index"], height=0.34, color="#93C5FD", label="Gross tourism value proxy")
    ax.barh(y - 0.18, plot["pressure_adjusted_value_index"], height=0.34, color=COLORS["red"], label="Pressure-adjusted value")
    ax.set_yticks(y)
    ax.set_yticklabels(plot["district_name"])
    ax.set_title("Pressure-Adjusted Tourism Value Index", loc="left", fontsize=23, pad=18)
    ax.text(0.0, 1.02, "Concept: tourism value should be discounted where neighbourhood pressure is high.", transform=ax.transAxes, fontsize=12, color=COLORS["muted"])
    ax.set_xlabel("Index (highest gross tourism-unit district = 100)")
    ax.set_ylabel("")
    ax.legend(loc="lower right")
    sns.despine(ax=ax, left=True)
    fig.subplots_adjust(left=0.20, right=0.93, top=0.80, bottom=0.15)
    save_figure(fig, "12_pressure_adjusted_tourism_value_index.png", source="Conceptual index from district accommodation units and mean TPI")


if __name__ == "__main__":
    main()