# NYC Yellow Taxi BI Project

This project looks at NYC Yellow Taxi trips from January to March 2025 and turns the raw trip records into business-friendly analysis. The goal is not to build a model. The goal is to understand demand, revenue, geography, payment behavior, trip efficiency, and the impact of the January 5 CBD congestion fee.

The notebooks are written in the order they should be run.

## Project Flow

1. `Pre-Process.ipynb`
   - Reviews the raw taxi data for data quality issues.
   - Checks dates, distances, passenger counts, fare fields, locations, and other validity rules.

2. `02_feature_engineering.ipynb`
   - Builds the analytical dataset.
   - Uses `Data/project_master_clean.parquet` as the taxi trip input.
   - Adds useful fields like pickup hour, pickup day, pickup month, trip duration, tip percent, average speed, pickup/dropoff boroughs, zones, service zones, and CBD period.
   - Saves the main analytical file locally as:
     `Data/processed/analytical/analytical.parquet`

3. `03_univariate_eda.ipynb`
   - Looks at one variable at a time.
   - Covers trip volume, distance, duration, fares, total amounts, passenger counts, payment types, and rate codes.

4. `04_bivariate_eda.ipynb`
   - Looks at relationships between two variables.
   - Covers hour vs demand, weekday vs demand, geography vs trips/revenue, payment type vs tip behavior, distance vs total amount, and borough-level metrics.

5. `05_multivariate_eda.ipynb`
   - Looks at deeper operational patterns using several variables together.
   - Covers time x geography x demand, geography x payment x revenue, distance x duration x total amount, month x hour x borough, CBD fee pre/post Jan 5, revenue concentration, and efficiency/outlier patterns.
   - Keeps the charts and tables inside the notebook, like the other EDA notebooks.


## How to Run

Use the project virtual environment if available:

```powershell
.\.venv\Scripts\python.exe
```

Open the notebooks in Jupyter and run them in this order:

```text
Pre-Process.ipynb
02_feature_engineering.ipynb
03_univariate_eda.ipynb
04_bivariate_eda.ipynb
05_multivariate_eda.ipynb
```

The feature engineering notebook expects `Data/project_master_clean.parquet` to exist. The EDA notebooks expect `Data/processed/analytical/analytical.parquet` to exist.

## Notes

- The CBD congestion fee starts to matter after January 5, 2025, so the multivariate notebook treats that as a separate business topic.
