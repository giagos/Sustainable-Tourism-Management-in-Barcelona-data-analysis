import pandas as pd

from make_gamma_export_folder import GAMMA_DIR, ROOT, ensure_gamma_dir


FIGURES = [
    ("01_executive_evidence_dashboard.png", "Opening evidence", "Five headline KPI cards for Barcelona tourism pressure.", "Analysis tables", "Pressure is measurable and concentrated."),
    ("02_top_tpi_neighbourhoods_bar.png", "TPI ranking", "Top 10 neighbourhoods by Tourism Pressure Index.", "top_tpi_neighbourhoods.csv", "Pressure is spatially uneven."),
    ("03_district_pressure_burden.png", "District burden", "Population share compared with tourism-accommodation share.", "district_spatial_inequality.csv", "Some districts carry more tourism units than population share."),
    ("04_port_seasonality_pressure.png", "Port seasonality", "Monthly port passenger pressure and peak stress.", "Port passenger prepared data", "Annual totals hide peak-month stress."),
    ("05_tourism_pressure_calendar_heatmap.png", "Pressure calendar", "Monthly heatmap of accommodation and port pressure proxies.", "Inside Airbnb calendar and port data", "Timing matters for governance triggers."),
    ("06_stakeholder_power_exposure_matrix.png", "Stakeholder analysis", "Decision power versus pressure exposure.", "Conceptual scoring from analysis evidence", "High-exposure residents need stronger influence."),
    ("07_stakeholder_conflict_matrix.png", "Conflict analysis", "Conflict intensity between major stakeholder groups.", "Conceptual stakeholder analysis", "Participation design must handle predictable conflicts."),
    ("08_participation_gap_table.png", "Participation gap", "Stakeholder interests, influence gaps and missing mechanisms.", "Conceptual table linked to indicators", "Evidence should trigger specific participation mechanisms."),
    ("09_tpi_triggered_governance_model.png", "Governance model", "Data to threshold to stakeholder action to policy response.", "TPI indicator logic", "TPI can be used as a governance trigger."),
    ("10_barcelona_tourism_pressure_council.png", "Council proposal", "Proposed participatory governance body.", "A2 governance design", "Monitoring needs an accountable participation body."),
    ("11_implementation_kpi_dashboard.png", "Implementation KPIs", "Monitoring dashboard with green, amber and red thresholds.", "Analysis tables and proposed thresholds", "Policy follow-up needs operational thresholds."),
    ("12_pressure_adjusted_tourism_value_index.png", "Adjusted value", "Conceptual index discounting tourism value by local pressure.", "district_pressure_summary.csv", "High tourism value should be adjusted by local pressure."),
    ("13_data_sources_table.png", "Data sources", "Clean visual table of datasets, variables, years and slide use.", "analysis_dataset_overview.csv", "The presentation is grounded in reproducible sources."),
    ("existing_01_tpi_choropleth_simplified.png", "Existing map", "Presentation re-export of the TPI choropleth.", "Existing analysis figure", "The spatial pattern supports neighbourhood targeting."),
    ("existing_02_hut_vs_airbnb_pressure_scatter.png", "Existing scatter", "Presentation re-export of the HUT versus Airbnb scatterplot.", "Existing analysis figure", "HUT and Airbnb pressures overlap but are not identical."),
    ("existing_03_policy_matrix_clean.png", "Existing policy matrix", "Presentation re-export of the policy matrix.", "Existing analysis figure", "Evidence connects directly to policy recommendations."),
    ("existing_04_stakeholder_matrix_clean.png", "Existing stakeholder figure", "Presentation re-export of the stakeholder matrix/table.", "Gamma stakeholder assets", "Participation must be tied to measurable pressure."),
]


def main():
    ensure_gamma_dir()
    rows = []
    for file_name, slide, caption, source, key_message in FIGURES:
        rows.append(
            {
                "figure_file": file_name,
                "slide": slide,
                "caption": caption,
                "source": source,
                "key_message": key_message,
                "exists": (GAMMA_DIR / file_name).exists(),
            }
        )
    index = pd.DataFrame(rows)
    path = GAMMA_DIR / "14_figure_index.csv"
    index.to_csv(path, index=False, encoding="utf-8-sig")
    print(f"Exported {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()