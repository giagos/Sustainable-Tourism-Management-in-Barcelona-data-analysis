import matplotlib.pyplot as plt
import pandas as pd

from make_gamma_export_folder import COLORS, GAMMA_DIR, ensure_gamma_dir, load_table, save_figure, short_number, wrap_text


SLIDE_USE = {
    "Inside Airbnb listings": "TPI, Airbnb intensity, stakeholder exposure",
    "Inside Airbnb calendar": "monthly accommodation pressure calendar",
    "Inside Airbnb reviews": "use-intensity component",
    "HUT licences": "licensed accommodation pressure",
    "Port passengers": "seasonality and peak stress",
    "Electricity consumption": "resource-use proxy",
    "Air quality stations": "environmental monitoring coverage",
    "Population denominators": "per-resident pressure denominators",
}


def year_range(row):
    dates = [row.get("date_min"), row.get("date_max")]
    years = []
    for value in dates:
        year = pd.to_datetime(value, errors="coerce")
        if pd.notna(year):
            years.append(str(year.year))
    if not years:
        return "metadata / snapshot"
    return "-".join([years[0], years[-1]]) if len(set(years)) > 1 else years[0]


def main():
    ensure_gamma_dir()
    overview = load_table("analysis_dataset_overview.csv")
    keep = overview[overview["dataset"].isin(SLIDE_USE)].copy()
    table = pd.DataFrame(
        {
            "Dataset": keep["dataset"],
            "Rows": keep["rows"].map(lambda value: short_number(value, 1)),
            "Years": keep.apply(year_range, axis=1),
            "Key variables": keep["column_names"].map(lambda value: ", ".join(str(value).split(", ")[:5])),
            "Slide use": keep["dataset"].map(SLIDE_USE),
        }
    )
    table.to_csv(GAMMA_DIR / "13_data_sources_table.csv", index=False, encoding="utf-8-sig")
    wrapped = table.copy()
    widths = [20, 8, 15, 30, 30]
    for col, width in zip(wrapped.columns, widths):
        wrapped[col] = wrapped[col].map(lambda value: wrap_text(value, width))

    fig, ax = plt.subplots(figsize=(13.333, 7.5))
    ax.axis("off")
    fig.text(0.04, 0.94, "Data Sources Used in the A2 Evidence Slides", fontsize=23, fontweight="bold", color=COLORS["ink"])
    fig.text(0.04, 0.895, "Technical source inventory linking datasets to slide-level evidence.", fontsize=12, color=COLORS["muted"])
    visual_table = ax.table(cellText=wrapped.values, colLabels=wrapped.columns, cellLoc="left", loc="center", bbox=[0.03, 0.06, 0.94, 0.78])
    visual_table.auto_set_font_size(False)
    visual_table.set_fontsize(8.4)
    for (row, col), cell in visual_table.get_celld().items():
        cell.set_edgecolor("#D8DEE9")
        if row == 0:
            cell.set_facecolor(COLORS["teal"])
            cell.set_text_props(color="white", weight="bold")
            cell.set_height(0.075)
        else:
            cell.set_facecolor("#FFFFFF" if row % 2 else "#F8FAFC")
            cell.set_height(0.092)
    save_figure(fig, "13_data_sources_table.png", source="Analysis dataset overview table")


if __name__ == "__main__":
    main()