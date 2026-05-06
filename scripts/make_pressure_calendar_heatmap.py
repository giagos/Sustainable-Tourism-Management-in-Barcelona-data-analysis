import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from make_gamma_export_folder import COLORS, MONTH_LABELS, load_airbnb_calendar_monthly, load_port_monthly, normalize_0_100, save_figure


def main():
    rows = []
    labels = []

    airbnb = load_airbnb_calendar_monthly()
    if not airbnb.empty:
        airbnb = airbnb.set_index("month").reindex(range(1, 13))
        rows.append(normalize_0_100(airbnb["booked_nights"]).to_numpy())
        labels.append("Airbnb booked-night proxy")

    port = load_port_monthly()
    if not port.empty:
        latest_year = int(port["year"].max())
        port_latest = port[port["year"].eq(latest_year)].set_index("month").reindex(range(1, 13))
        rows.append(normalize_0_100(port_latest["passengers"]).to_numpy())
        labels.append(f"Port passengers ({latest_year})")

    if not rows:
        matrix = pd.DataFrame([[0] * 12], index=["No monthly source available"], columns=MONTH_LABELS)
    else:
        matrix = pd.DataFrame(rows, index=labels, columns=MONTH_LABELS)

    fig, ax = plt.subplots(figsize=(13.333, 7.5))
    sns.heatmap(
        matrix,
        cmap="YlOrRd",
        linewidths=1.2,
        linecolor="#FFFFFF",
        vmin=0,
        vmax=100,
        cbar_kws={"label": "Normalised monthly pressure (0-100)"},
        ax=ax,
    )
    ax.set_title("Tourism Pressure Calendar Heatmap", loc="left", fontsize=23, pad=18)
    ax.set_xlabel("Month")
    ax.set_ylabel("")
    ax.text(
        0.01,
        -0.20,
        "Airport passenger data is not present in the prepared sources, so the calendar uses available accommodation and port proxies.",
        transform=ax.transAxes,
        fontsize=10.5,
        color=COLORS["muted"],
    )
    fig.subplots_adjust(left=0.22, right=0.92, top=0.80, bottom=0.26)
    save_figure(fig, "05_tourism_pressure_calendar_heatmap.png")


if __name__ == "__main__":
    main()