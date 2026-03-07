"""
Exploratory Data Analysis Script
=================================
Impact of Weather Conditions on Sales - Business Analytics Project

Generates 10 publication-quality charts and saves them to charts/ folder.
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
warnings.filterwarnings('ignore')

# ─── Style Setup ────────────────────────────────────────────────────────────
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
COLORS = {
    'primary': '#2196F3',
    'secondary': '#FF9800',
    'accent': '#4CAF50',
    'danger': '#F44336',
    'purple': '#9C27B0',
    'teal': '#009688',
    'winter': '#42A5F5',
    'spring': '#66BB6A',
    'summer': '#FFA726',
    'autumn': '#EF5350'
}
SEASON_COLORS = [COLORS['winter'], COLORS['spring'], COLORS['summer'], COLORS['autumn']]
SEASON_ORDER = ['Winter', 'Spring', 'Summer', 'Autumn']

# Create output directory
os.makedirs('charts', exist_ok=True)

# Load data
print("Loading merged dataset...")
df = pd.read_csv('merged_sales_weather.csv', parse_dates=['DATE'])
print(f"Loaded {len(df)} rows\n")

# ─── Chart 1: Daily Total Sales Time Series ─────────────────────────────────
print("Chart 1: Daily Total Sales Time Series...")
fig, ax = plt.subplots(figsize=(14, 5))
ax.plot(df['DATE'], df['Total_Sales'], color=COLORS['primary'], alpha=0.4, linewidth=0.8)
# 30-day rolling average
rolling = df['Total_Sales'].rolling(window=30, center=True).mean()
ax.plot(df['DATE'], rolling, color=COLORS['danger'], linewidth=2, label='30-Day Moving Avg')
ax.set_xlabel('Date', fontsize=12)
ax.set_ylabel('Total Units Sold', fontsize=12)
ax.set_title('Daily Total Sales (2014–2018)', fontsize=14, fontweight='bold')
ax.legend(fontsize=11)
plt.tight_layout()
plt.savefig('charts/01_daily_sales_timeseries.png', dpi=150)
plt.close()

# ─── Chart 2: Monthly Average Sales ─────────────────────────────────────────
print("Chart 2: Monthly Average Sales...")
monthly = df.groupby('Month')['Total_Sales'].mean()
month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(month_names, monthly.values, color=[
    COLORS['winter'], COLORS['winter'], COLORS['winter'],
    COLORS['spring'], COLORS['spring'], COLORS['spring'],
    COLORS['summer'], COLORS['summer'], COLORS['summer'],
    COLORS['autumn'], COLORS['autumn'], COLORS['autumn']
], edgecolor='white', linewidth=1.5)
ax.set_xlabel('Month', fontsize=12)
ax.set_ylabel('Avg Daily Sales (Units)', fontsize=12)
ax.set_title('Average Daily Sales by Month', fontsize=14, fontweight='bold')
for bar, val in zip(bars, monthly.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
            f'{val:.0f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
plt.tight_layout()
plt.savefig('charts/02_monthly_avg_sales.png', dpi=150)
plt.close()

# ─── Chart 3: Sales by Season (Boxplot) ─────────────────────────────────────
print("Chart 3: Sales by Season Boxplot...")
fig, ax = plt.subplots(figsize=(8, 6))
season_data = [df[df['Season'] == s]['Total_Sales'].values for s in SEASON_ORDER]
bp = ax.boxplot(season_data, labels=SEASON_ORDER, patch_artist=True,
                medianprops=dict(color='black', linewidth=2))
for patch, color in zip(bp['boxes'], SEASON_COLORS):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)
ax.set_ylabel('Total Units Sold', fontsize=12)
ax.set_title('Sales Distribution by Season', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('charts/03_sales_by_season_boxplot.png', dpi=150)
plt.close()

# ─── Chart 4: Sales by Day of Week ──────────────────────────────────────────
print("Chart 4: Sales by Day of Week...")
day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
day_sales = df.groupby('DayOfWeek')['Total_Sales'].mean()
fig, ax = plt.subplots(figsize=(10, 5))
colors_dow = [COLORS['primary']] * 5 + [COLORS['accent']] * 2
ax.bar(day_names, day_sales.values, color=colors_dow, edgecolor='white', linewidth=1.5)
ax.set_ylabel('Avg Daily Sales (Units)', fontsize=12)
ax.set_title('Average Sales by Day of Week', fontsize=14, fontweight='bold')
ax.axhline(y=day_sales.mean(), color=COLORS['danger'], linestyle='--', alpha=0.7, label='Overall Mean')
ax.legend()
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig('charts/04_sales_by_day_of_week.png', dpi=150)
plt.close()

# ─── Chart 5: Temperature Distribution ──────────────────────────────────────
print("Chart 5: Temperature Distribution...")
fig, ax = plt.subplots(figsize=(10, 5))
ax.hist(df['Avg_Temp'], bins=40, color=COLORS['secondary'], edgecolor='white',
        alpha=0.8, density=True)
df['Avg_Temp'].plot.kde(ax=ax, color=COLORS['danger'], linewidth=2, label='KDE')
ax.set_xlabel('Average Temperature (°C)', fontsize=12)
ax.set_ylabel('Density', fontsize=12)
ax.set_title('Distribution of Daily Average Temperature', fontsize=14, fontweight='bold')
ax.legend()
plt.tight_layout()
plt.savefig('charts/05_temperature_distribution.png', dpi=150)
plt.close()

# ─── Chart 6: Rainfall Distribution ─────────────────────────────────────────
print("Chart 6: Rainfall Distribution...")
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
# Rain frequency
rain_pct = df['Is_Rainy'].value_counts(normalize=True) * 100
axes[0].pie([rain_pct.get(0, 0), rain_pct.get(1, 0)],
            labels=['No Rain', 'Rain'], autopct='%1.1f%%',
            colors=[COLORS['primary'], COLORS['teal']],
            startangle=90, textprops={'fontsize': 12})
axes[0].set_title('Rainy vs Non-Rainy Days', fontsize=13, fontweight='bold')

# Rainfall amount (only rainy days)
rainy_days = df[df['Is_Rainy'] == 1]['Rainfall']
if len(rainy_days) > 0:
    axes[1].hist(rainy_days, bins=30, color=COLORS['teal'], edgecolor='white', alpha=0.8)
    axes[1].set_xlabel('Rainfall (mm)', fontsize=12)
    axes[1].set_ylabel('Count', fontsize=12)
    axes[1].set_title('Rainfall Distribution (Rainy Days Only)', fontsize=13, fontweight='bold')
else:
    axes[1].text(0.5, 0.5, 'No rainfall data', ha='center', va='center', fontsize=14)
    axes[1].set_title('Rainfall Distribution', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('charts/06_rainfall_distribution.png', dpi=150)
plt.close()

# ─── Chart 7: Sales vs Temperature Scatter ──────────────────────────────────
print("Chart 7: Sales vs Temperature Scatter...")
fig, ax = plt.subplots(figsize=(10, 6))
scatter = ax.scatter(df['Avg_Temp'], df['Total_Sales'], c=df['Month'], cmap='coolwarm',
                      alpha=0.5, s=20, edgecolors='none')
# Trend line
z = np.polyfit(df['Avg_Temp'].dropna(), df.loc[df['Avg_Temp'].notna(), 'Total_Sales'], 1)
p = np.poly1d(z)
x_line = np.linspace(df['Avg_Temp'].min(), df['Avg_Temp'].max(), 100)
ax.plot(x_line, p(x_line), color=COLORS['danger'], linewidth=2.5, linestyle='--',
        label=f'Trend (slope={z[0]:.2f})')
cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label('Month', fontsize=11)
ax.set_xlabel('Average Temperature (°C)', fontsize=12)
ax.set_ylabel('Total Units Sold', fontsize=12)
ax.set_title('Sales vs Temperature', fontsize=14, fontweight='bold')
ax.legend(fontsize=11)
plt.tight_layout()
plt.savefig('charts/07_sales_vs_temperature.png', dpi=150)
plt.close()

# ─── Chart 8: Sales vs Rainfall Scatter ─────────────────────────────────────
print("Chart 8: Sales vs Rainfall...")
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# Scatter
axes[0].scatter(df['Rainfall'], df['Total_Sales'], alpha=0.4, s=20,
                color=COLORS['teal'], edgecolors='none')
if df['Rainfall'].max() > 0:
    z2 = np.polyfit(df['Rainfall'], df['Total_Sales'], 1)
    p2 = np.poly1d(z2)
    x2 = np.linspace(0, df['Rainfall'].max(), 100)
    axes[0].plot(x2, p2(x2), color=COLORS['danger'], linewidth=2.5, linestyle='--')
axes[0].set_xlabel('Rainfall (mm)', fontsize=12)
axes[0].set_ylabel('Total Units Sold', fontsize=12)
axes[0].set_title('Sales vs Rainfall', fontsize=13, fontweight='bold')

# Bar comparison: rainy vs non-rainy
rain_comp = df.groupby('Is_Rainy')['Total_Sales'].mean()
axes[1].bar(['Non-Rainy', 'Rainy'], rain_comp.values,
            color=[COLORS['primary'], COLORS['teal']], edgecolor='white', linewidth=1.5)
for i, v in enumerate(rain_comp.values):
    axes[1].text(i, v + 5, f'{v:.0f}', ha='center', fontweight='bold', fontsize=12)
axes[1].set_ylabel('Avg Daily Sales', fontsize=12)
axes[1].set_title('Avg Sales: Rainy vs Non-Rainy Days', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('charts/08_sales_vs_rainfall.png', dpi=150)
plt.close()

# ─── Chart 9: Correlation Heatmap ───────────────────────────────────────────
print("Chart 9: Correlation Heatmap...")
corr_cols = ['Total_Sales', 'Sales_B1', 'Sales_B2', 'Sales_B3', 'Sales_B4',
             'Avg_Temp', 'Min_Temp', 'Max_Temp', 'Rainfall', 'Wind_Speed',
             'IsWeekend', 'Total_Promos']
corr_available = [c for c in corr_cols if c in df.columns]
corr_matrix = df[corr_available].corr()

fig, ax = plt.subplots(figsize=(12, 9))
mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)
sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f', cmap='RdBu_r',
            center=0, square=True, linewidths=0.5, ax=ax,
            cbar_kws={'shrink': 0.8},
            annot_kws={'size': 9})
ax.set_title('Correlation Matrix: Sales & Weather Variables', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('charts/09_correlation_heatmap.png', dpi=150)
plt.close()

# ─── Chart 10: Monthly Temp vs Sales Dual Axis ──────────────────────────────
print("Chart 10: Monthly Temperature vs Sales...")
monthly_data = df.groupby('Month').agg({
    'Total_Sales': 'mean',
    'Avg_Temp': 'mean'
}).reset_index()

fig, ax1 = plt.subplots(figsize=(10, 5))
ax2 = ax1.twinx()

ax1.bar(month_names, monthly_data['Total_Sales'], color=COLORS['primary'],
        alpha=0.6, label='Avg Sales', edgecolor='white', linewidth=1.5)
ax2.plot(month_names, monthly_data['Avg_Temp'], color=COLORS['danger'],
         linewidth=3, marker='o', markersize=8, label='Avg Temp')

ax1.set_xlabel('Month', fontsize=12)
ax1.set_ylabel('Avg Daily Sales (Units)', fontsize=12, color=COLORS['primary'])
ax2.set_ylabel('Avg Temperature (°C)', fontsize=12, color=COLORS['danger'])
ax1.set_title('Monthly Sales vs Temperature', fontsize=14, fontweight='bold')

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=11)
plt.tight_layout()
plt.savefig('charts/10_monthly_temp_vs_sales.png', dpi=150)
plt.close()

# ─── Chart 11 (Bonus): Category-wise Sales by Season ────────────────────────
print("Chart 11: Category Sales by Season...")
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
categories = [('Sales_B1', 'Category B1'), ('Sales_B2', 'Category B2'),
              ('Sales_B3', 'Category B3'), ('Sales_B4', 'Category B4')]
for ax, (col, title) in zip(axes.flat, categories):
    season_cat = df.groupby('Season')[col].mean().reindex(SEASON_ORDER)
    ax.bar(SEASON_ORDER, season_cat.values, color=SEASON_COLORS, edgecolor='white', linewidth=1.5)
    ax.set_title(title, fontsize=13, fontweight='bold')
    ax.set_ylabel('Avg Daily Sales')
    for i, v in enumerate(season_cat.values):
        ax.text(i, v + 1, f'{v:.0f}', ha='center', fontsize=10, fontweight='bold')
plt.suptitle('Average Sales by Season per Product Category', fontsize=15, fontweight='bold', y=1.01)
plt.tight_layout()
plt.savefig('charts/11_category_sales_by_season.png', dpi=150)
plt.close()

print(f"\n✅ All charts saved to charts/ folder!")
print(f"   Generated {len(os.listdir('charts'))} charts")
