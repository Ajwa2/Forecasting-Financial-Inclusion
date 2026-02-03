# Forecasting Financial Inclusion in Ethiopia

## Project Overview

This project focuses on forecasting financial inclusion in Ethiopia using machine learning techniques.

## Running the notebooks and dashboard

1. Install dependencies:

```bash
pip install -r requirements.txt
pip install streamlit plotly
```

2. Reproduce forecasts (Task 4): open and run `notebooks/task4_forecast.ipynb` in Jupyter — this will write `reports/forecasts_task4.csv`.

3. Dashboard (Task 5): prototype in notebook `notebooks/task5_dashboard.ipynb`. To run the Streamlit app:

```bash
streamlit run dashboard/app.py
```

The Streamlit app reads `reports/forecasts_task4.csv` and provides interactive exploration and CSV download.

Notes: notebooks and the app expect the processed Excel at `data/processed/ethiopia_fi_unified_data_enriched.xlsx` and a `reports` folder writable by the user.
