import matplotlib.pyplot as plt
import seaborn as sns

from make_gamma_export_folder import COLORS, MONTH_LABELS, load_port_monthly, load_table, save_figure, short_number


def main():
    monthly = load_port_monthly()
    peak = load_table("port_peak_pressure.csv")
    latest_year = int(monthly["year"].max()) if not monthly.empty else int(peak["year"].max())
    latest = monthly[monthly["year"].eq(latest_year)].copy()
    peak_row = peak.sort_values("peak_to_average_ratio", ascending=False).iloc[0]

    fig, ax = plt.subplots(figsize=(13.333, 7.5))
    for year, frame in monthly.groupby("year"):
        if int(year) == latest_year:
            continue
        ax.plot(frame["month"], frame["passengers"], color="#CBD5E1", linewidth=1.4, alpha=0.65)
    if not latest.empty:
        ax.plot(latest["month"], latest["passengers"], color=COLORS["blue"], linewidth=3.0, marker="o", label=f"{latest_year}")
        peak_month = latest.loc[latest["passengers"].idxmax()]
        ax.scatter([peak_month["month"]], [peak_month["passengers"]], s=220, color=COLORS["red"], zorder=5)
        ax.annotate(
            f"Peak: {short_number(peak_month['passengers'], 1)} passengers",
            xy=(peak_month["month"], peak_month["passengers"]),
            xytext=(-95, 38),
            textcoords="offset points",
            arrowprops={"arrowstyle": "->", "color": COLORS["ink"]},
            fontsize=11,
            fontweight="bold",
        )
    ax.set_title("Port Seasonality and Peak-Pressure Stress", loc="left", fontsize=23, pad=18)
    ax.text(
        0.01,
        0.92,
        f"Highest measured peak-to-average ratio: {peak_row['peak_to_average_ratio']:.2f}x in {int(peak_row['year'])}",
        transform=ax.transAxes,
        fontsize=12.5,
        color=COLORS["muted"],
    )
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(MONTH_LABELS)
    ax.set_xlabel("Month")
    ax.set_ylabel("Passengers")
    ax.legend(loc="upper left")
    sns.despine(ax=ax)
    fig.subplots_adjust(left=0.10, right=0.94, top=0.82, bottom=0.14)
    save_figure(fig, "04_port_seasonality_pressure.png")


if __name__ == "__main__":
    main()