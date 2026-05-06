import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from make_gamma_export_folder import COLORS, save_figure


def main():
    groups = ["Residents", "Platforms", "Hotels", "Port", "Municipality", "NGOs", "Tourists"]
    values = [
        [0, 9, 7, 6, 6, 2, 5],
        [9, 0, 5, 3, 7, 8, 2],
        [7, 5, 0, 4, 4, 5, 2],
        [6, 3, 4, 0, 5, 6, 3],
        [6, 7, 4, 5, 0, 4, 2],
        [2, 8, 5, 6, 4, 0, 4],
        [5, 2, 2, 3, 2, 4, 0],
    ]
    matrix = pd.DataFrame(values, index=groups, columns=groups)

    fig, ax = plt.subplots(figsize=(13.333, 7.5))
    sns.heatmap(matrix, cmap="Reds", vmin=0, vmax=10, annot=True, fmt="d", linewidths=1.0, linecolor="white", cbar_kws={"label": "Conflict intensity (0-10)"}, ax=ax)
    ax.set_title("Stakeholder Conflict Matrix", loc="left", fontsize=23, pad=18)
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.tick_params(axis="x", rotation=0)
    fig.subplots_adjust(left=0.16, right=0.92, top=0.82, bottom=0.16)
    save_figure(fig, "07_stakeholder_conflict_matrix.png", source="Conceptual stakeholder conflict assessment for A2 participation analysis")


if __name__ == "__main__":
    main()