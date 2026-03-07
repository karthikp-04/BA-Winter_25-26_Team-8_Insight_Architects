"""
Data Preparation Script
=======================
Impact of Weather Conditions on Sales - Business Analytics Project

This script:
1. Loads the UCI Hierarchical Sales Data
2. Loads the Meteostat weather data (export.xlsx)
3. Aggregates daily sales totals (overall + per category)
4. Handles missing weather values
5. Engineers temporal features (month, day of week, season, weekend)
6. Merges and exports the final dataset
"""

import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore')

# ─── Configuration ───────────────────────────────────────────────────────────
SALES_FILE = 'hierarchical_sales_data.csv'
WEATHER_FILE = 'export.xlsx'
OUTPUT_FILE = 'merged_sales_weather.csv'

# ─── 1. Load Sales Data ─────────────────────────────────────────────────────
print("=" * 60)
print("STEP 1: Loading Sales Data")
print("=" * 60)

sales_df = pd.read_csv(SALES_FILE)
sales_df['DATE'] = pd.to_datetime(sales_df['DATE'])

# Identify quantity columns by category
qty_b1 = [c for c in sales_df.columns if c.startswith('QTY_B1_')]
qty_b2 = [c for c in sales_df.columns if c.startswith('QTY_B2_')]
qty_b3 = [c for c in sales_df.columns if c.startswith('QTY_B3_')]
qty_b4 = [c for c in sales_df.columns if c.startswith('QTY_B4_')]
all_qty = qty_b1 + qty_b2 + qty_b3 + qty_b4

# Aggregate daily sales
sales_df['Total_Sales'] = sales_df[all_qty].sum(axis=1)
sales_df['Sales_B1'] = sales_df[qty_b1].sum(axis=1)
sales_df['Sales_B2'] = sales_df[qty_b2].sum(axis=1)
sales_df['Sales_B3'] = sales_df[qty_b3].sum(axis=1)
sales_df['Sales_B4'] = sales_df[qty_b4].sum(axis=1)

# Promotion columns
promo_cols = [c for c in sales_df.columns if c.startswith('PROMO_')]
sales_df['Total_Promos'] = sales_df[promo_cols].sum(axis=1)

# Keep only aggregated columns
sales_agg = sales_df[['DATE', 'Total_Sales', 'Sales_B1', 'Sales_B2',
                       'Sales_B3', 'Sales_B4', 'Total_Promos']].copy()

print(f"  Sales data loaded: {len(sales_agg)} rows")
print(f"  Date range: {sales_agg['DATE'].min().date()} to {sales_agg['DATE'].max().date()}")
print(f"  Avg daily total sales: {sales_agg['Total_Sales'].mean():.1f} units")
print()

# ─── 2. Load Weather Data ───────────────────────────────────────────────────
print("=" * 60)
print("STEP 2: Loading Weather Data")
print("=" * 60)

weather_df = pd.read_excel(WEATHER_FILE)
weather_df.columns = weather_df.columns.str.strip().str.lower()
weather_df['date'] = pd.to_datetime(weather_df['date'])

print(f"  Weather data loaded: {len(weather_df)} rows")
print(f"  Date range: {weather_df['date'].min().date()} to {weather_df['date'].max().date()}")
print(f"  Missing values before cleaning:")
for col in ['tavg', 'tmin', 'tmax', 'prcp', 'wspd']:
    if col in weather_df.columns:
        print(f"    {col}: {weather_df[col].isnull().sum()} nulls")
print()

# ─── 3. Clean Weather Data ──────────────────────────────────────────────────
print("=" * 60)
print("STEP 3: Cleaning Weather Data")
print("=" * 60)

# Fill precipitation NaN with 0 (assume no rain if not recorded)
if 'prcp' in weather_df.columns:
    weather_df['prcp'] = weather_df['prcp'].fillna(0.0)
else:
    weather_df['prcp'] = 0.0

# Interpolate temperature and wind speed
for col in ['tavg', 'tmin', 'tmax', 'wspd']:
    if col in weather_df.columns:
        weather_df[col] = weather_df[col].interpolate(method='linear')
        weather_df[col] = weather_df[col].bfill().ffill()

# Compute temperature range
if 'tmin' in weather_df.columns and 'tmax' in weather_df.columns:
    weather_df['temp_range'] = weather_df['tmax'] - weather_df['tmin']

# Create rain flag
weather_df['is_rainy'] = (weather_df['prcp'] > 0).astype(int)

# Create temperature category
weather_df['temp_category'] = pd.cut(
    weather_df['tavg'],
    bins=[-np.inf, 5, 15, 25, np.inf],
    labels=['Cold (<5°C)', 'Cool (5-15°C)', 'Warm (15-25°C)', 'Hot (>25°C)']
)

# Rename columns for clarity
weather_clean = weather_df[['date', 'tavg', 'tmin', 'tmax', 'prcp', 'wspd',
                             'temp_range', 'is_rainy', 'temp_category']].copy()
weather_clean.columns = ['DATE', 'Avg_Temp', 'Min_Temp', 'Max_Temp', 'Rainfall',
                          'Wind_Speed', 'Temp_Range', 'Is_Rainy', 'Temp_Category']

print(f"  Missing values after cleaning:")
for col in weather_clean.columns:
    nulls = weather_clean[col].isnull().sum()
    if nulls > 0:
        print(f"    {col}: {nulls} nulls")
if weather_clean.isnull().sum().sum() == 0:
    print("    None — all clean!")
print()

# ─── 4. Add Temporal Features ───────────────────────────────────────────────
print("=" * 60)
print("STEP 4: Adding Temporal Features")
print("=" * 60)

# We'll add these to the merged dataframe
def add_temporal_features(df):
    df['Year'] = df['DATE'].dt.year
    df['Month'] = df['DATE'].dt.month
    df['DayOfWeek'] = df['DATE'].dt.dayofweek  # 0=Mon, 6=Sun
    df['DayName'] = df['DATE'].dt.day_name()
    df['IsWeekend'] = (df['DayOfWeek'] >= 5).astype(int)
    
    # Season mapping (Northern Hemisphere / Italy)
    season_map = {12: 'Winter', 1: 'Winter', 2: 'Winter',
                  3: 'Spring', 4: 'Spring', 5: 'Spring',
                  6: 'Summer', 7: 'Summer', 8: 'Summer',
                  9: 'Autumn', 10: 'Autumn', 11: 'Autumn'}
    df['Season'] = df['Month'].map(season_map)
    
    # Month name for charts
    df['MonthName'] = df['DATE'].dt.strftime('%b')
    
    return df

print("  Temporal features: Year, Month, DayOfWeek, DayName, IsWeekend, Season")
print()

# ─── 5. Merge Datasets ─────────────────────────────────────────────────────
print("=" * 60)
print("STEP 5: Merging Sales and Weather Data")
print("=" * 60)

merged_df = pd.merge(sales_agg, weather_clean, on='DATE', how='inner')
merged_df = add_temporal_features(merged_df)

# Sort by date
merged_df = merged_df.sort_values('DATE').reset_index(drop=True)

print(f"  Merged dataset: {len(merged_df)} rows x {len(merged_df.columns)} columns")
print(f"  Date range: {merged_df['DATE'].min().date()} to {merged_df['DATE'].max().date()}")
print(f"  Columns: {list(merged_df.columns)}")
print()

# ─── 6. Summary Statistics ──────────────────────────────────────────────────
print("=" * 60)
print("STEP 6: Summary Statistics")
print("=" * 60)

print("\n--- Sales Statistics ---")
for col in ['Total_Sales', 'Sales_B1', 'Sales_B2', 'Sales_B3', 'Sales_B4']:
    print(f"  {col}: mean={merged_df[col].mean():.1f}, "
          f"std={merged_df[col].std():.1f}, "
          f"min={merged_df[col].min()}, max={merged_df[col].max()}")

print("\n--- Weather Statistics ---")
for col in ['Avg_Temp', 'Rainfall', 'Wind_Speed']:
    print(f"  {col}: mean={merged_df[col].mean():.1f}, "
          f"std={merged_df[col].std():.1f}, "
          f"min={merged_df[col].min():.1f}, max={merged_df[col].max():.1f}")

print(f"\n  Rainy days: {merged_df['Is_Rainy'].sum()} "
      f"({merged_df['Is_Rainy'].mean()*100:.1f}%)")
print(f"  Weekend days: {merged_df['IsWeekend'].sum()} "
      f"({merged_df['IsWeekend'].mean()*100:.1f}%)")

print("\n--- Sales by Season ---")
season_stats = merged_df.groupby('Season')['Total_Sales'].agg(['mean', 'std', 'count'])
for season in ['Winter', 'Spring', 'Summer', 'Autumn']:
    if season in season_stats.index:
        row = season_stats.loc[season]
        print(f"  {season}: mean={row['mean']:.1f}, std={row['std']:.1f}, n={int(row['count'])}")

# ─── 7. Save Output ────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 7: Saving Merged Dataset")
print("=" * 60)

merged_df.to_csv(OUTPUT_FILE, index=False)
print(f"  Saved to: {OUTPUT_FILE}")
print(f"  File size: {os.path.getsize(OUTPUT_FILE) / 1024:.1f} KB")
print("\n✅ Data preparation complete!")
