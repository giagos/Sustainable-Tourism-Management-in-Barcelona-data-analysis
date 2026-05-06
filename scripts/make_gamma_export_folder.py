from pathlib import Path
import re
import textwrap

import matplotlib as mpl
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "outputs"
TABLES_DIR = OUTPUT_DIR / "tables"
FIGURES_DIR = OUTPUT_DIR / "figures"
GAMMA_DIR = OUTPUT_DIR / "gamma_assets"
PREPARED_DIR = ROOT / "Data" / "prepared"

WIDE_FIGSIZE = (13.333, 7.5)
DPI = 220
MONTH_LABELS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
CREATOR_WATERMARK = "Created by Ioannis Kapetankis"

COLORS = {
    "bg": "#F8FAFC",
    "panel": "#FFFFFF",
    "ink": "#111827",
    "muted": "#64748B",
    "line": "#CBD5E1",
    "blue": "#2563EB",
    "teal": "#0F766E",
    "green": "#16A34A",
    "amber": "#D97706",
    "orange": "#EA580C",
    "red": "#B91C1C",
    "purple": "#7C3AED",
    "pink": "#BE185D",
}


def setup_style():
    sns.set_theme(style="whitegrid", context="talk")
    mpl.rcParams.update(
        {
            "figure.facecolor": COLORS["bg"],
            "axes.facecolor": COLORS["panel"],
            "axes.edgecolor": COLORS["line"],
            "axes.labelcolor": COLORS["ink"],
            "xtick.color": COLORS["muted"],
            "ytick.color": COLORS["muted"],
            "text.color": COLORS["ink"],
            "axes.titleweight": "bold",
            "font.family": "DejaVu Sans",
            "savefig.facecolor": COLORS["bg"],
        }
    )


def ensure_gamma_dir():
    GAMMA_DIR.mkdir(parents=True, exist_ok=True)
    return GAMMA_DIR


def load_table(filename):
    path = TABLES_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Missing required table: {path}")
    return pd.read_csv(path)


def save_figure(fig, filename, source="Barcelona tourism sustainability analysis outputs"):
    ensure_gamma_dir()
    fig.set_size_inches(*WIDE_FIGSIZE)
    footer = f"{source} | {CREATOR_WATERMARK}"
    fig.text(
        0.985,
        0.018,
        footer,
        ha="right",
        va="bottom",
        fontsize=8.5,
        color=COLORS["muted"],
        bbox={"facecolor": COLORS["bg"], "edgecolor": "none", "alpha": 0.82, "pad": 2.0},
    )
    path = GAMMA_DIR / filename
    fig.savefig(path, dpi=DPI)
    plt.close(fig)
    print(f"Exported {path.relative_to(ROOT)}")
    return path


def wrap_text(value, width):
    return "\n".join(textwrap.wrap(str(value), width=width, break_long_words=False))


def short_number(value, decimals=1):
    if pd.isna(value):
        return "n/a"
    value = float(value)
    if abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.{decimals}f}M"
    if abs(value) >= 1_000:
        return f"{value / 1_000:.{decimals}f}k"
    return f"{value:.{decimals}f}"


def pct(value, decimals=1):
    return "n/a" if pd.isna(value) else f"{float(value):.{decimals}f}%"


def to_number(series):
    text = series.astype("string").str.strip()
    text = text.str.replace("\u00a0", "", regex=False)
    text = text.str.replace(r"[^0-9,\.\-]", "", regex=True)
    comma_decimal = text.str.contains(",", na=False) & ~text.str.contains(r"\.\d{1,3}$", na=False)
    text = text.where(~comma_decimal, text.str.replace(".", "", regex=False).str.replace(",", ".", regex=False))
    text = text.where(comma_decimal, text.str.replace(",", "", regex=False))
    return pd.to_numeric(text, errors="coerce")


def standardize_columns(frame):
    frame = frame.copy()
    frame.columns = [re.sub(r"_+", "_", re.sub(r"[^0-9a-zA-Z]+", "_", str(col)).strip("_").lower()) for col in frame.columns]
    return frame


def first_existing(columns, candidates):
    lookup = {str(col).lower(): col for col in columns}
    for candidate in candidates:
        if candidate in lookup:
            return lookup[candidate]
    return None


def read_csv_any(path, **kwargs):
    for encoding in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            return pd.read_csv(path, encoding=encoding, encoding_errors="replace", sep=None, engine="python", on_bad_lines="skip", **kwargs)
        except Exception:
            continue
    return pd.read_csv(path, encoding="latin-1", encoding_errors="replace", on_bad_lines="skip", **kwargs)


def load_port_monthly():
    paths = sorted((PREPARED_DIR / "port_barcelona" / "passenger_traffic").glob("*.csv"))
    frames = []
    for path in paths:
        frame = standardize_columns(read_csv_any(path))
        frame["source_file"] = path.name
        frames.append(frame)
    if not frames:
        return pd.DataFrame(columns=["year", "month", "passengers"])
    data = pd.concat(frames, ignore_index=True, sort=False)
    year_col = first_existing(data.columns, ["man_any_servei_id", "any", "year"])
    month_col = first_existing(data.columns, ["man_mes_servei_id", "month", "mes"])
    passenger_col = first_existing(data.columns, ["man_par_passatgers", "passatgers", "passengers"])
    if not (year_col and month_col and passenger_col):
        return pd.DataFrame(columns=["year", "month", "passengers"])
    raw_month = to_number(data[month_col])
    data["year"] = to_number(data[year_col]).astype("Int64")
    data["month"] = raw_month.where(raw_month <= 100, raw_month.mod(100)).astype("Int64")
    data["passengers"] = to_number(data[passenger_col])
    return (
        data.dropna(subset=["year", "month", "passengers"])
        .groupby(["year", "month"], as_index=False)["passengers"]
        .sum()
        .sort_values(["year", "month"])
    )


def load_airbnb_calendar_monthly():
    paths = sorted((PREPARED_DIR / "inside_airbnb").glob("*/calendar.csv"))
    if not paths:
        return pd.DataFrame(columns=["month", "booked_nights"])
    path = paths[0]
    try:
        frame = pd.read_csv(path, usecols=["date", "available"], dtype={"available": "string"})
    except Exception:
        frame = read_csv_any(path)
        frame = standardize_columns(frame)
        if not {"date", "available"}.issubset(frame.columns):
            return pd.DataFrame(columns=["month", "booked_nights"])
        frame = frame[["date", "available"]]
    frame["date"] = pd.to_datetime(frame["date"], errors="coerce")
    available = frame["available"].astype("string").str.lower().isin(["t", "true", "yes", "y", "1"])
    frame["booked_nights"] = (~available).astype(int)
    frame["month"] = frame["date"].dt.month
    return frame.dropna(subset=["month"]).groupby("month", as_index=False)["booked_nights"].sum()


def normalize_0_100(series):
    numeric = pd.to_numeric(series, errors="coerce")
    if numeric.notna().sum() == 0 or numeric.max() == numeric.min():
        return pd.Series(np.nan, index=series.index)
    return (numeric - numeric.min()) / (numeric.max() - numeric.min()) * 100


def reframe_existing_figure(source_path, filename, title=None):
    if not source_path.exists():
        print(f"Skipped missing existing figure: {source_path.relative_to(ROOT)}")
        return None
    image = mpimg.imread(source_path)
    fig = plt.figure(figsize=WIDE_FIGSIZE, facecolor=COLORS["bg"])
    ax = fig.add_axes([0.045, 0.08, 0.91, 0.82])
    ax.imshow(image)
    ax.axis("off")
    if title:
        fig.text(0.055, 0.94, title, ha="left", va="center", fontsize=22, fontweight="bold", color=COLORS["ink"])
    return save_figure(fig, filename, source="Re-exported from existing analysis figure")


def copy_existing_figures():
    ensure_gamma_dir()
    mappings = [
        (FIGURES_DIR / "04_tpi_choropleth.png", "existing_01_tpi_choropleth_simplified.png", "Tourism Pressure Index map"),
        (FIGURES_DIR / "08_hut_vs_airbnb_scatter.png", "existing_02_hut_vs_airbnb_pressure_scatter.png", "HUT and Airbnb pressure scatter"),
        (FIGURES_DIR / "22_dpsir_policy_effectiveness_chain.png", "existing_03_policy_matrix_clean.png", "Policy-effectiveness matrix"),
    ]
    exported = [reframe_existing_figure(source, filename, title) for source, filename, title in mappings]
    stakeholder_source = GAMMA_DIR / "06_stakeholder_power_exposure_matrix.png"
    if not stakeholder_source.exists():
        stakeholder_source = GAMMA_DIR / "08_participation_gap_table.png"
    if stakeholder_source.exists():
        exported.append(reframe_existing_figure(stakeholder_source, "existing_04_stakeholder_matrix_clean.png", "Stakeholder matrix/table"))
    return [path for path in exported if path is not None]


def draw_threshold_bar(ax, label, value, amber, red, maximum, unit=""):
    ax.barh([label], [maximum], color="#E5E7EB", height=0.52)
    ax.barh([label], [min(amber, maximum)], color="#BBF7D0", height=0.52)
    ax.barh([label], [max(min(red, maximum) - amber, 0)], left=[amber], color="#FDE68A", height=0.52)
    ax.barh([label], [max(maximum - red, 0)], left=[red], color="#FECACA", height=0.52)
    ax.scatter([min(value, maximum)], [label], s=180, color=COLORS["ink"], zorder=5)
    ax.text(maximum * 1.02, label, f"{value:.1f}{unit}", va="center", fontsize=12, fontweight="bold")


setup_style()


def main():
    ensure_gamma_dir()
    copy_existing_figures()
    print(f"Gamma export folder ready: {GAMMA_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()