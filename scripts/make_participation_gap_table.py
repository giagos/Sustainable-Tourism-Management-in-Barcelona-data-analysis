import matplotlib.pyplot as plt
import pandas as pd

from make_gamma_export_folder import COLORS, GAMMA_DIR, ensure_gamma_dir, save_figure, wrap_text


def participation_rows():
    return pd.DataFrame(
        [
            ["Residents", "housing affordability, crowding, liveability", "Very high", "Low-medium", "binding neighbourhood trigger hearings", "TPI and tourism units per 1,000 residents"],
            ["Neighbourhood NGOs", "environment, public space, equity", "High", "Medium", "formal evidence-review seat", "district surplus vs population share"],
            ["Municipality", "policy coordination and enforcement", "High", "High", "transparent threshold dashboard", "red/amber/green KPI breaches"],
            ["Hotels", "regulated visitor economy", "Medium", "High", "shared mitigation commitments", "licensed accommodation concentration"],
            ["Platforms", "short-term rental revenues", "Medium", "High", "mandatory data-sharing protocol", "platform listings per 1,000 residents"],
            ["Port authority", "visitor flows and cruise scheduling", "Medium", "High", "peak-pressure scheduling review", "monthly peak-to-average ratio"],
            ["Tourists", "access and experience quality", "Low-medium", "Low", "visitor information and demand-shifting tools", "seasonal pressure calendar"],
        ],
        columns=["Stakeholder", "Interest", "Pressure exposure", "Current influence", "Missing mechanism", "Indicator"],
    )


def main():
    ensure_gamma_dir()
    data = participation_rows()
    data.to_csv(GAMMA_DIR / "08_participation_gap_table.csv", index=False, encoding="utf-8-sig")
    wrapped = data.copy()
    widths = [14, 24, 14, 14, 25, 27]
    for col, width in zip(wrapped.columns, widths):
        wrapped[col] = wrapped[col].map(lambda value: wrap_text(value, width))

    fig, ax = plt.subplots(figsize=(13.333, 7.5))
    ax.axis("off")
    fig.text(0.04, 0.94, "Participation Gap Table", fontsize=23, fontweight="bold", color=COLORS["ink"])
    fig.text(0.04, 0.895, "Where pressure evidence should trigger stronger stakeholder participation mechanisms.", fontsize=12, color=COLORS["muted"])
    table = ax.table(cellText=wrapped.values, colLabels=wrapped.columns, cellLoc="left", loc="center", bbox=[0.02, 0.06, 0.96, 0.78])
    table.auto_set_font_size(False)
    table.set_fontsize(8.2)
    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor("#D8DEE9")
        if row == 0:
            cell.set_facecolor(COLORS["blue"])
            cell.set_text_props(color="white", weight="bold")
            cell.set_height(0.075)
        else:
            cell.set_facecolor("#FFFFFF" if row % 2 else "#F8FAFC")
            cell.set_height(0.106)
    save_figure(fig, "08_participation_gap_table.png", source="Conceptual table linked to analysis indicators")


if __name__ == "__main__":
    main()