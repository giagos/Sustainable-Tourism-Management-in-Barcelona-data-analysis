import matplotlib.pyplot as plt
import seaborn as sns

from make_gamma_export_folder import COLORS, load_table, save_figure


def main():
    data = load_table("top_tpi_neighbourhoods.csv").head(10).copy()
    data["label"] = data["neighbourhood_name"] + " | " + data["district_name"]
    data = data.sort_values("tpi_0_100", ascending=True)

    fig, ax = plt.subplots(figsize=(13.333, 7.5))
    colors = sns.color_palette("rocket", n_colors=len(data))
    ax.barh(data["label"], data["tpi_0_100"], color=colors)
    ax.set_title("Top 10 Neighbourhoods by Tourism Pressure Index", loc="left", fontsize=23, pad=18)
    ax.set_xlabel("Tourism Pressure Index (0-100)")
    ax.set_ylabel("")
    ax.set_xlim(0, max(105, data["tpi_0_100"].max() * 1.12))
    for y_pos, value in enumerate(data["tpi_0_100"]):
        ax.text(value + 1.2, y_pos, f"{value:.1f}", va="center", fontsize=11, fontweight="bold", color=COLORS["ink"])
    sns.despine(ax=ax, left=True)
    fig.subplots_adjust(left=0.28, right=0.93, top=0.83, bottom=0.16)
    save_figure(fig, "02_top_tpi_neighbourhoods_bar.png")


if __name__ == "__main__":
    main()