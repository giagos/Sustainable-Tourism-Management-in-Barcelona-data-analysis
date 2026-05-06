import matplotlib.pyplot as plt

from make_gamma_export_folder import COLORS, load_table, save_figure


def draw_kpi_row(ax, label, value, amber, red, maximum, unit=""):
    amber_pct = amber / maximum * 100
    red_pct = red / maximum * 100
    value_pct = min(value / maximum * 100, 100)
    ax.barh([label], [100], color="#E5E7EB", height=0.52)
    ax.barh([label], [amber_pct], color="#BBF7D0", height=0.52)
    ax.barh([label], [max(red_pct - amber_pct, 0)], left=[amber_pct], color="#FDE68A", height=0.52)
    ax.barh([label], [max(100 - red_pct, 0)], left=[red_pct], color="#FECACA", height=0.52)
    ax.scatter([value_pct], [label], s=180, color=COLORS["ink"], zorder=5)
    ax.text(104, label, f"{value:.1f}{unit}", va="center", fontsize=12, fontweight="bold")


def main():
    top_tpi = load_table("top_tpi_neighbourhoods.csv")
    top_airbnb = load_table("top_airbnb_neighbourhoods.csv")
    concentration = load_table("concentration_diagnostics.csv")
    burden = load_table("district_spatial_inequality.csv")
    port_peak = load_table("port_peak_pressure.csv")

    hut_top10 = concentration[concentration["indicator"].str.contains("HUT", case=False, na=False)]["top_10_share_pct"].iloc[0]
    metrics = [
        ("Max neighbourhood TPI", float(top_tpi["tpi_0_100"].max()), 50, 75, 100, ""),
        ("Max Airbnb listings per 1k", float(top_airbnb["airbnb_per_1000_residents"].max()), 15, 30, 60, ""),
        ("HUT top-10 concentration", float(hut_top10), 40, 55, 80, "%"),
        ("Max district burden surplus", float(burden["tourism_surplus_vs_population_pct_points"].max()), 5, 12, 30, " pp"),
        ("Port peak-to-average ratio", float(port_peak["peak_to_average_ratio"].max()), 1.5, 2.0, 3.0, "x"),
    ]

    fig, ax = plt.subplots(figsize=(13.333, 7.5))
    ax.set_title("Implementation KPI Dashboard", loc="left", fontsize=23, pad=18)
    ax.text(0.0, 1.02, "Green, amber and red thresholds for practical monitoring after policy adoption.", transform=ax.transAxes, fontsize=12, color=COLORS["muted"])
    for label, value, amber, red, maximum, unit in reversed(metrics):
        draw_kpi_row(ax, label, value, amber, red, maximum, unit)
    ax.set_xlim(0, 118)
    ax.set_xlabel("Relative threshold scale for each KPI")
    ax.set_ylabel("")
    ax.grid(axis="x", color="#E2E8F0")
    ax.grid(axis="y", visible=False)
    ax.text(0.01, -0.18, "Thresholds are proposed presentation thresholds. They should be calibrated through the Tourism Pressure Council.", transform=ax.transAxes, fontsize=10.5, color=COLORS["muted"])
    fig.subplots_adjust(left=0.27, right=0.86, top=0.80, bottom=0.22)
    save_figure(fig, "11_implementation_kpi_dashboard.png", source="Calculated from analysis tables with proposed monitoring thresholds")


if __name__ == "__main__":
    main()