# Impact of Weather Conditions on Sales

A comprehensive business analytics project examining the relationship between external atmospheric conditions and retail performance.

## Project Overview
This study integrates hierarchical sales data from a physical grocery store (2014-2018) with real-world weather observations from Meteostat (Italy). Using Python and Business Analytics techniques, we quantify how temperature, rainfall, and seasonality drive consumer behavior.

## Repository Structure
- `data_preparation.py`: Cleaning and merging sales + weather datasets.
- `eda_analysis.py`: Generation of 11 exploratory visualizations.
- `statistical_analysis.py`: Correlation matrices, ANOVA, T-tests, and OLS Regression.
- `export_for_dashboard.py`: Pre-processes results for web visualization.
- `dashboard/`: Interactive HTML/JS dashboard using Chart.js.
- `charts/`: Folder containing high-resolution PNG charts.
- `business_insights.md`: key findings and strategic recommendations.

## How to Run
1. **Requirements**: `pip install -r requirements.txt`
2. **Execute Full Pipeline**:
   - `python data_preparation.py`
   - `python eda_analysis.py`
   - `python statistical_analysis.py`
   - `python export_for_dashboard.py`
3. **View Dashboard**:
   - Open locally: `dashboard/index.html` in any modern web browser
   - Or view online: [Interactive Dashboard](https://karthikp-04.github.io/BA-Winter_25-26_Team-8_Insight_Architects/dashboard/)

## Analytical Techniques
- **Exploratory Data Analysis (EDA)**: Time series analysis, distribution mapping, and bivariate plotting.
- **Hypothesis Testing**: T-tests for weekend vs. weekday and rainy vs. non-rainy impact.
- **Predictive Modeling**: Ordinary Least Squares (OLS) regression to isolate weather-driven demand variance.

## 

## Team 8
- CB.SC.U4CSE23522
- CB.SC.U4CSE23551
- CB.EN.U4CCE23004
*23CSE452-Business Analytics*
