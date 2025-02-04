# Demographic Report System

## Overview
The **Demographic Report System** is designed to analyze sociometric data and generate demographic reports based on a sociogram. The system allows filtering and visualization of cadet performance across various demographic categories, comparing current and historical data.

## Features
- **Data Integration**: Merges sociometric and sociogram data.
- **Demographic Filtering**: Enables analysis by specific subgroups.
- **Statistical Analysis**: Computes averages and trends across various demographic categories.
- **Graphical Reports**: Generates bar graphs and pie charts.
- **Historical Comparisons**: Supports year-over-year performance comparisons.
- **Automated Word Report Generation**: Outputs demographic reports in DOCX format.

## Project Structure
```
Demographic_Report/
│── main.py                  # Entry point for running demographic analysis
│── demographic_report.py     # Core module for generating reports
│── constants.py              # Contains category mappings and output paths
│── SocioLinker.py            # Links sociometric and sociogram data
│── DocxHelper.py             # Handles Word report generation
```

## Dependencies
To run the system, the following Python packages are required:
- `pandas`
- `numpy`
- `matplotlib`
- `plotly`
- `openpyxl`
- `python-docx`


## Running the System
1. **Prepare Data**: Place input Excel files in the `data/` directory.
2. **Run the Main Analysis**:
   ```sh
   python main.py --title "Demographic Report" --sociometry-path "path/to/stats.xlsx" --sociogram-path "path/to/sociogram.xlsx"
   ```
3. **Optional Parameters**:
   - To filter by a specific column (for example here the column 5 is the column representing the מחלקה):
     ```sh
     --filter-column 5 --filter-name "רמה מחלקתית"
     ```
   - To include previous year data:
     ```sh
     --old-socio-path "path/to/last_year_stats.xlsx"
     ```

## Output
- **Bar Graphs**: Comparing demographic group performance.
- **Pie Charts**: Distribution of demographic attributes.
- **Word Reports**: Structured demographic reports with visualizations.

## Future Improvements
- Enhance visualization capabilities with interactive dashboards.
- Automate data validation and anomaly detection.
- Expand demographic filters for more granular analysis.

## Contributors
- Developed as part of the Talpiot evaluation system.
- Developed by Ben Hillel from מ"ד 

