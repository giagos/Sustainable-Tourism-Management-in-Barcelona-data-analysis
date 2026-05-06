# Barcelona Sustainable Tourism Pressure Analysis

**Author:** Ioannis Kapetankis  
**Assignment:** Sustainable Tourism Management  
**Project title:** A Data-Driven Critical Appraisal of Sustainable Tourism Management in Barcelona: Tourism Pressure, Spatial Inequality and Policy Effectiveness

This repository contains a reproducible data-analysis project examining whether Barcelona's sustainable tourism policies reduce measurable tourism pressure or mainly document and administer it. The analysis combines tourism accommodation, port passenger, electricity, environmental metadata and population-denominator data to build neighbourhood and district-level evidence for sustainable tourism management.

## Contents

- [Barcelona Sustainable Tourism Pressure Analysis](#barcelona-sustainable-tourism-pressure-analysis)
  - [Contents](#contents)
  - [Project Overview](#project-overview)
  - [Research Question](#research-question)
  - [Repository Guide](#repository-guide)
  - [Main Outputs](#main-outputs)
    - [Selected Figures](#selected-figures)
    - [Selected Tables](#selected-tables)
  - [Key Indicators](#key-indicators)
  - [How To Run The Notebook](#how-to-run-the-notebook)
  - [Data Sources](#data-sources)
  - [Academic Framework](#academic-framework)
  - [Limitations](#limitations)
  - [Author Note](#author-note)

## Project Overview

The project creates a structured evidence base for assessing tourism pressure in Barcelona. It loads all prepared datasets, profiles data quality, standardises geography, adds population denominators, aggregates indicators to neighbourhood and district level, and produces formal tables plus watermarked figures for academic use.

The final analysis focuses on four linked questions:

1. Where is tourism pressure concentrated in Barcelona?
2. Which neighbourhoods face the strongest accommodation pressure relative to resident population?
3. Do port and resource-use indicators suggest seasonal or citywide pressure beyond accommodation alone?
4. What does the evidence imply for sustainable tourism policy effectiveness?

## Research Question

> To what extent do Barcelona's sustainable tourism policies reduce measurable tourism pressure, rather than merely documenting or administratively managing it?

## Repository Guide

| Path | Purpose |
|---|---|
| [notebooks/barcelona_tourism_sustainability_analysis.ipynb](notebooks/barcelona_tourism_sustainability_analysis.ipynb) | Main analysis notebook with data loading, profiling, indicators, maps, charts and summary tables. |
| [Data/](Data/) | Raw, prepared and catalogued datasets used for the analysis. |
| [Data/catalog/dataset_manifest.csv](Data/catalog/dataset_manifest.csv) | File inventory for downloaded datasets. |
| [Data/catalog/preparation_report.csv](Data/catalog/preparation_report.csv) | Preparation status and validation report. |
| [outputs/tables/](outputs/tables/) | Exported CSV tables for the assignment evidence base. |
| [outputs/figures/](outputs/figures/) | Exported watermarked figures, maps and trend charts. |
| [scripts/prepare_datasets.py](scripts/prepare_datasets.py) | Dataset preparation script. |
| [scripts/download_datasets.ps1](scripts/download_datasets.ps1) | Dataset download script. |

## Main Outputs

The notebook exports formal tables and figures that can be used directly in the Sustainable Tourism Management assignment.

### Selected Figures

| Figure | File |
|---|---|
| Tourism Pressure Index map | [outputs/figures/04_tpi_choropleth.png](outputs/figures/04_tpi_choropleth.png) |
| Airbnb pressure map | [outputs/figures/05_airbnb_pressure_choropleth.png](outputs/figures/05_airbnb_pressure_choropleth.png) |
| HUT pressure map | [outputs/figures/06_hut_pressure_choropleth.png](outputs/figures/06_hut_pressure_choropleth.png) |
| Policy-priority typology map | [outputs/figures/07_policy_priority_typology_map.png](outputs/figures/07_policy_priority_typology_map.png) |
| District spatial inequality chart | [outputs/figures/10_district_spatial_inequality.png](outputs/figures/10_district_spatial_inequality.png) |
| DPSIR policy-effectiveness matrix | [outputs/figures/22_dpsir_policy_effectiveness_chain.png](outputs/figures/22_dpsir_policy_effectiveness_chain.png) |

<details>
<summary><strong>Open the complete figure list</strong></summary>

- [01_tpi_top_neighbourhoods.png](outputs/figures/01_tpi_top_neighbourhoods.png)
- [02_airbnb_pressure_top_neighbourhoods.png](outputs/figures/02_airbnb_pressure_top_neighbourhoods.png)
- [03_hut_pressure_top_neighbourhoods.png](outputs/figures/03_hut_pressure_top_neighbourhoods.png)
- [04_tpi_choropleth.png](outputs/figures/04_tpi_choropleth.png)
- [05_airbnb_pressure_choropleth.png](outputs/figures/05_airbnb_pressure_choropleth.png)
- [06_hut_pressure_choropleth.png](outputs/figures/06_hut_pressure_choropleth.png)
- [07_policy_priority_typology_map.png](outputs/figures/07_policy_priority_typology_map.png)
- [08_hut_vs_airbnb_scatter.png](outputs/figures/08_hut_vs_airbnb_scatter.png)
- [09_tpi_component_heatmap.png](outputs/figures/09_tpi_component_heatmap.png)
- [10_district_spatial_inequality.png](outputs/figures/10_district_spatial_inequality.png)
- [11_district_pressure_heatmap.png](outputs/figures/11_district_pressure_heatmap.png)
- [12_concentration_lorenz_curve.png](outputs/figures/12_concentration_lorenz_curve.png)
- [13_airbnb_room_type_by_district.png](outputs/figures/13_airbnb_room_type_by_district.png)
- [14_port_recovery_and_cruise_share.png](outputs/figures/14_port_recovery_and_cruise_share.png)
- [15_port_monthly_seasonality_heatmap.png](outputs/figures/15_port_monthly_seasonality_heatmap.png)
- [16_port_peak_pressure_ratio.png](outputs/figures/16_port_peak_pressure_ratio.png)
- [17_electricity_consumption_index.png](outputs/figures/17_electricity_consumption_index.png)
- [19_hut_quarterly_trend.png](outputs/figures/19_hut_quarterly_trend.png)
- [20_air_quality_monitoring_coverage.png](outputs/figures/20_air_quality_monitoring_coverage.png)
- [21_policy_priority_summary.png](outputs/figures/21_policy_priority_summary.png)
- [22_dpsir_policy_effectiveness_chain.png](outputs/figures/22_dpsir_policy_effectiveness_chain.png)

</details>

### Selected Tables

| Table | File |
|---|---|
| Dataset inventory | [outputs/tables/dataset_inventory.csv](outputs/tables/dataset_inventory.csv) |
| Analysis dataset overview | [outputs/tables/analysis_dataset_overview.csv](outputs/tables/analysis_dataset_overview.csv) |
| Top TPI neighbourhoods | [outputs/tables/top_tpi_neighbourhoods.csv](outputs/tables/top_tpi_neighbourhoods.csv) |
| District pressure summary | [outputs/tables/district_pressure_summary.csv](outputs/tables/district_pressure_summary.csv) |
| District spatial inequality | [outputs/tables/district_spatial_inequality.csv](outputs/tables/district_spatial_inequality.csv) |
| Policy evidence scorecard | [outputs/tables/policy_evidence_scorecard.csv](outputs/tables/policy_evidence_scorecard.csv) |

## Key Indicators

The analysis builds a composite Tourism Pressure Index using standardised components available at neighbourhood level:

- Airbnb listings per 1,000 residents
- Entire-home Airbnb listings per 1,000 residents
- HUT licences per 1,000 residents
- HUT places per 1,000 residents
- Recent Airbnb review activity per 1,000 residents
- Mean platform availability

Additional supporting indicators include:

- Port passenger recovery and peak-month pressure
- Electricity-consumption index as a resource-use proxy
- Air-quality monitoring coverage
- District tourism-unit surplus compared with resident-population share
- Policy-priority typology for neighbourhood targeting

## How To Run The Notebook

1. Open [notebooks/barcelona_tourism_sustainability_analysis.ipynb](notebooks/barcelona_tourism_sustainability_analysis.ipynb).
2. Use a Python environment with the required analysis libraries installed.
3. Run the notebook cells from top to bottom.
4. Review exported tables in [outputs/tables/](outputs/tables/).
5. Review exported figures in [outputs/figures/](outputs/figures/).

Core Python libraries used by the notebook:

```text
pandas
numpy
matplotlib
seaborn
tabulate
```

## Data Sources

The project uses prepared datasets from:

- Barcelona Open Data BCN
- Inside Airbnb Barcelona
- Port de Barcelona passenger traffic data
- Official Barcelona population-denominator data

The data preparation summary is available in [Data/catalog/preparation_summary.json](Data/catalog/preparation_summary.json), and the full local data catalogue is available in [Data/catalog/dataset_manifest.csv](Data/catalog/dataset_manifest.csv).

## Academic Framework

The analysis is structured around sustainable tourism management concepts, including:

- Triple Bottom Line: social, environmental and economic dimensions
- DPSIR: driving forces, pressures, state, impacts and responses
- Carrying capacity as a multidimensional policy question
- Policy-effectiveness chain: claim, mechanism, indicator, observed result, limitation and recommendation

<details>
<summary><strong>How the evidence supports the assignment argument</strong></summary>

The project separates measurement from policy effectiveness. It shows that Barcelona can document tourism pressure at neighbourhood and district level, but policy success requires evidence of pressure reduction over time. The Tourism Pressure Index, concentration diagnostics and policy-priority typology help identify where sustainable tourism management needs targeted intervention rather than only citywide monitoring.

</details>

## Limitations

- The Tourism Pressure Index is an available-data indicator, not a causal proof of policy success.
- Inside Airbnb data reflects platform listings and should be compared with official registers where available.
- Port passenger data is citywide and does not show exact visitor movement within neighbourhoods.
- Electricity data is treated as a resource-use proxy because it is not fully harmonised to neighbourhood boundaries.
- Air-quality files provide monitoring metadata, not a complete pollutant time-series analysis.

## Author Note

This repository was prepared by **Ioannis Kapetankis** for a **Sustainable Tourism Management** assignment on Barcelona tourism pressure, spatial inequality and policy effectiveness.