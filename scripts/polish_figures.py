from __future__ import annotations

import textwrap
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
TABLES_DIR = ROOT / "outputs" / "tables"
FIGURES_DIR = ROOT / "outputs" / "figures"
WATERMARK_TEXT = "Barcelona Open Data BCN, Port de Barcelona and Inside Airbnb | Created by Ioannis Kapetankis"

sns.set_theme(style="whitegrid", context="talk")
mpl.rcParams.update({
    "axes.titlesize": 14,
    "axes.titleweight": "bold",
    "axes.labelsize": 11,
    "savefig.dpi": 240,
})


def add_watermark(fig: mpl.figure.Figure) -> None:
    fig.text(
        0.995,
        0.008,
        WATERMARK_TEXT,
        ha="right",
        va="bottom",
        fontsize=8,
        color="#374151",
        alpha=0.86,
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.72, "pad": 2.0},
    )


def finish_figure(fig: mpl.figure.Figure, filename: str) -> Path:
    add_watermark(fig)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    path = FIGURES_DIR / filename
    fig.savefig(path, dpi=240, bbox_inches="tight")
    plt.close(fig)
    return path


def polish_port_recovery() -> Path:
    port_recovery = pd.read_csv(TABLES_DIR / "port_recovery_index.csv")
    port_recovery["year"] = pd.to_numeric(port_recovery["year"], errors="coerce")
    port_recovery["passengers"] = pd.to_numeric(port_recovery["passengers"], errors="coerce")
    port_recovery["passenger_index"] = pd.to_numeric(port_recovery["passenger_index"], errors="coerce")
    base_year = int(port_recovery.loc[port_recovery["passenger_index"].sub(100).abs().idxmin(), "year"])

    fig, ax1 = plt.subplots(figsize=(9, 5.6))
    ax2 = ax1.twinx()
    ax2.bar(
        port_recovery["year"],
        port_recovery["passengers"] / 1_000_000,
        color="#D1D5DB",
        width=0.55,
        label="Annual passengers",
    )
    sns.lineplot(
        data=port_recovery,
        x="year",
        y="passenger_index",
        marker="o",
        ax=ax1,
        color="#3B6FB6",
        linewidth=2.4,
        label="Recovery index",
    )
    ax1.axhline(100, color="#6B7280", linestyle="--", linewidth=1)
    ax1.set_title(f"Port passenger recovery: index and annual scale (base year {base_year}=100)", loc="left")
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Passenger index")
    ax2.set_ylabel("Annual passengers (millions)")
    ax1.legend(loc="upper left", fontsize=8)
    ax2.legend(loc="upper right", fontsize=8)
    return finish_figure(fig, "14_port_recovery_and_cruise_share.png")


def polish_dpsir_chain() -> Path:
    fig, ax = plt.subplots(figsize=(13.2, 6.2))
    ax.axis("off")
    panels = [
        ("Driving forces", "Platform listings, HUT stock, port arrivals", "#DBEAFE"),
        ("Pressures", "Per-resident intensity, concentration, monthly peaks", "#FEF3C7"),
        ("State", "TPI hotspots and district tourism surplus", "#FCE7F3"),
        ("Impacts", "Housing pressure risk, crowding, resource-use proxy", "#EDE9FE"),
        ("Responses", "Target caps and enforcement; add environmental observations", "#DCFCE7"),
    ]
    box_width = 0.174
    for idx, (stage, body, color) in enumerate(panels):
        x0 = 0.035 + idx * 0.192
        rect = mpl.patches.FancyBboxPatch(
            (x0, 0.32),
            box_width,
            0.40,
            boxstyle="round,pad=0.012,rounding_size=0.018",
            facecolor=color,
            edgecolor="#374151",
            linewidth=0.9,
        )
        ax.add_patch(rect)
        ax.text(x0 + box_width / 2, 0.60, stage, ha="center", va="center", fontsize=10.5, weight="bold", color="#111827")
        ax.text(
            x0 + box_width / 2,
            0.455,
            textwrap.fill(body, width=24),
            ha="center",
            va="center",
            fontsize=8.4,
            linespacing=1.25,
            color="#374151",
        )
        if idx < len(panels) - 1:
            ax.annotate(
                "",
                xy=(x0 + box_width + 0.024, 0.515),
                xytext=(x0 + box_width + 0.008, 0.515),
                arrowprops={"arrowstyle": "->", "color": "#374151", "linewidth": 1.3},
            )
    ax.text(
        0.035,
        0.20,
        "Reading for the assignment: evidence is strongest for spatial pressure and concentration; causal environmental outcomes need additional observation data.",
        ha="left",
        va="center",
        fontsize=9.2,
        color="#374151",
        transform=ax.transAxes,
    )
    ax.set_title("DPSIR policy-effectiveness chain for Barcelona sustainable tourism", loc="left", pad=10)
    return finish_figure(fig, "22_dpsir_policy_effectiveness_chain.png")


if __name__ == "__main__":
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    written = [polish_port_recovery(), polish_dpsir_chain()]
    for path in written:
        print(path.relative_to(ROOT))
