# Dataset Layout

This folder is organized for reproducible tourism and sustainability analysis.

## Structure

- `raw/inside_airbnb/`: Airbnb snapshot files grouped by city snapshot and section.
- `raw/barcelona_open_data/`: Barcelona open-data files grouped by dataset id.
- `raw/port_barcelona/passenger_traffic/`: Port of Barcelona passenger traffic CSV files.
- `prepared/`: Validated and decompressed files ready for analysis.
- `catalog/dataset_manifest.csv`: Inventory of every downloaded file, source URL, resolved URL, and saved path.
- `catalog/preparation_report.csv`: File-level extraction and validation status for every dataset.
- `catalog/preparation_summary.json`: Summary counts for the preparation run.

## Labeling Rules

- Inside Airbnb files keep their published filenames.
- Port of Barcelona files keep their published filenames.
- Barcelona open-data files are saved as `resource_<resource-id>__<resolved-filename>` so the original CKAN resource id remains visible even when the download URL is generic.

## Re-download

Run the downloader from the workspace root:

```powershell
.\scripts\download_datasets.ps1
```

## Prepare For Analysis

Validate and extract the raw downloads into the prepared analysis folder:

```powershell
c:/python314/python.exe .\scripts\prepare_datasets.py
```