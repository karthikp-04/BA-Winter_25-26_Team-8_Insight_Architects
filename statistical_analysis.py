"""
Statistical & Regression Analysis Script
=========================================
Impact of Weather Conditions on Sales - Business Analytics Project

Performs:
1. Correlation analysis with p-values
2. ANOVA: Sales across seasons
3. T-test: Rainy vs Non-rainy days
4. OLS Regression: Sales ~ weather + temporal variables
5. Residual diagnostics
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import pearsonr, f_oneway, ttest_ind
import statsmodels.api as sm
from statsmodels.formula.api import ols
import os
import warnings
warnings.filterwarnings('ignore')

os.makedirs('charts', exist_ok=True)

# ─── Load Data ──────────────────────────────────────────────────────────────
print("Loading merged dataset...")
df = pd.read_csv('merged_sales_weather.csv', parse_dates=['DATE'])
print(f"Loaded {len(df)} rows\n")

# ═══════════════════════════════════════════════════════════════════════════
# 1. CORRELATION ANALYSIS WITH P-VALUES
# ═══════════════════════════════════════════════════════════════════════════
print("=" * 70)
print("1. CORRELATION ANALYSIS")
print("=" * 70)

weather_vars = ['Avg_Temp', 'Min_Temp', 'Max_Temp', 'Rainfall', 'Wind_Speed', 'Temp_Range']
sales_vars = ['Total_Sales', 'Sales_B1', 'Sales_B2', 'Sales_B3', 'Sales_B4']
available_weather = [c for c in weather_vars if c in df.columns]
available_sales = [c for c in sales_vars if c in df.columns]

print(f"\n{'Weather Variable':<20} {'Sales Variable':<15} {'Pearson r':>10} {'p-value':>12} {'Significance':>15}")
print("-" * 72)

for wvar in available_weather:
    for svar in available_sales:
        mask = df[[wvar, svar]].dropna()
        if len(mask) > 2:
            r, p = pearsonr(mask[wvar], mask[svar])
            sig = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else 'ns'
            if svar == 'Total_Sales':  # Only print total sales for brevity
                print(f"{wvar:<20} {svar:<15} {r:>10.4f} {p:>12.6f} {sig:>15}")

print("\n  Significance: *** p<0.001, ** p<0.01, * p<0.05, ns = not significant")

# ═══════════════════════════════════════════════════════════════════════════
# 2. ANOVA: SALES ACROSS SEASONS
# ═══════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("2. ANOVA: SALES ACROSS SEASONS")
print("=" * 70)

seasons = ['Winter', 'Spring', 'Summer', 'Autumn']
season_groups = [df[df['Season'] == s]['Total_Sales'].dropna().values for s in seasons]
season_groups = [g for g in season_groups if len(g) > 0]

if len(season_groups) >= 2:
    f_stat, p_val = f_oneway(*season_groups)
    print(f"\n  F-statistic: {f_stat:.4f}")
    print(f"  p-value: {p_val:.6f}")
    print(f"  Result: {'Significant difference' if p_val < 0.05 else 'No significant difference'} "
          f"in sales across seasons (alpha=0.05)")

    print(f"\n  {'Season':<12} {'Mean':>8} {'Std':>8} {'Count':>6}")
    print("  " + "-" * 38)
    for s in seasons:
        data = df[df['Season'] == s]['Total_Sales']
        if len(data) > 0:
            print(f"  {s:<12} {data.mean():>8.1f} {data.std():>8.1f} {len(data):>6}")

# ═══════════════════════════════════════════════════════════════════════════
# 3. T-TEST: RAINY VS NON-RAINY DAYS
# ═══════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("3. T-TEST: RAINY VS NON-RAINY DAYS")
print("=" * 70)

rainy = df[df['Is_Rainy'] == 1]['Total_Sales'].dropna()
not_rainy = df[df['Is_Rainy'] == 0]['Total_Sales'].dropna()

if len(rainy) > 1 and len(not_rainy) > 1:
    t_stat, p_val = ttest_ind(rainy, not_rainy, equal_var=False)
    print(f"\n  Rainy days:     n={len(rainy):>5}, mean={rainy.mean():.1f}, std={rainy.std():.1f}")
    print(f"  Non-rainy days: n={len(not_rainy):>5}, mean={not_rainy.mean():.1f}, std={not_rainy.std():.1f}")
    print(f"\n  t-statistic: {t_stat:.4f}")
    print(f"  p-value: {p_val:.6f}")
    print(f"  Result: {'Significant difference' if p_val < 0.05 else 'No significant difference'} "
          f"between rainy and non-rainy days (alpha=0.05)")
    print(f"  Effect: {'Higher' if rainy.mean() > not_rainy.mean() else 'Lower'} sales on rainy days")
else:
    print("\n  Insufficient rainy day data for t-test.")
    print(f"  Rainy days: {len(rainy)}, Non-rainy days: {len(not_rainy)}")

# ═══════════════════════════════════════════════════════════════════════════
# 4. T-TEST: WEEKEND VS WEEKDAY
# ═══════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("4. T-TEST: WEEKEND VS WEEKDAY SALES")
print("=" * 70)

weekend = df[df['IsWeekend'] == 1]['Total_Sales'].dropna()
weekday = df[df['IsWeekend'] == 0]['Total_Sales'].dropna()

t_stat, p_val = ttest_ind(weekend, weekday, equal_var=False)
print(f"\n  Weekend:  n={len(weekend):>5}, mean={weekend.mean():.1f}, std={weekend.std():.1f}")
print(f"  Weekday:  n={len(weekday):>5}, mean={weekday.mean():.1f}, std={weekday.std():.1f}")
print(f"\n  t-statistic: {t_stat:.4f}")
print(f"  p-value: {p_val:.6f}")
print(f"  Result: {'Significant difference' if p_val < 0.05 else 'No significant difference'} "
      f"between weekend and weekday sales (alpha=0.05)")

# ═══════════════════════════════════════════════════════════════════════════
# 5. OLS REGRESSION
# ═══════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("5. OLS REGRESSION: Total_Sales ~ Weather + Temporal Variables")
print("=" * 70)

# Prepare features
reg_df = df[['Total_Sales', 'Avg_Temp', 'Rainfall', 'Wind_Speed',
             'IsWeekend', 'Total_Promos', 'Season']].dropna().copy()

# Create season dummies
season_dummies = pd.get_dummies(reg_df['Season'], prefix='Season', drop_first=True)
for col in season_dummies.columns:
    season_dummies[col] = season_dummies[col].astype(float)
reg_df = pd.concat([reg_df.drop('Season', axis=1), season_dummies], axis=1)
reg_df = reg_df.apply(pd.to_numeric, errors='coerce').dropna()

# Define X and y
y = reg_df['Total_Sales']
X = reg_df.drop('Total_Sales', axis=1)
X = sm.add_constant(X)

# Fit OLS model
model = sm.OLS(y, X).fit()

print(f"\n{model.summary()}")

print(f"\n  Key Metrics:")
print(f"  R-squared:     {model.rsquared:.4f}")
print(f"  Adj R-squared: {model.rsquared_adj:.4f}")
print(f"  F-statistic:   {model.fvalue:.4f}")
print(f"  Prob (F):      {model.f_pvalue:.6f}")

print(f"\n  Significant Predictors (p < 0.05):")
for var in model.pvalues.index:
    if model.pvalues[var] < 0.05 and var != 'const':
        print(f"    {var}: coef={model.params[var]:.4f}, p={model.pvalues[var]:.6f}")

# ─── Residual Diagnostics ───────────────────────────────────────────────────
print("\n  Generating residual diagnostics plot...")
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Residuals vs Fitted
residuals = model.resid
fitted = model.fittedvalues
axes[0, 0].scatter(fitted, residuals, alpha=0.3, s=10, color='#2196F3')
axes[0, 0].axhline(y=0, color='red', linestyle='--')
axes[0, 0].set_xlabel('Fitted Values')
axes[0, 0].set_ylabel('Residuals')
axes[0, 0].set_title('Residuals vs Fitted', fontweight='bold')

# Normal Q-Q plot
sm.qqplot(residuals, line='45', ax=axes[0, 1], markerfacecolor='#2196F3', alpha=0.3)
axes[0, 1].set_title('Normal Q-Q Plot', fontweight='bold')

# Histogram of residuals
axes[1, 0].hist(residuals, bins=40, color='#2196F3', edgecolor='white', alpha=0.8, density=True)
x_kde = np.linspace(residuals.min(), residuals.max(), 100)
axes[1, 0].plot(x_kde, stats.norm.pdf(x_kde, residuals.mean(), residuals.std()),
                color='red', linewidth=2)
axes[1, 0].set_xlabel('Residuals')
axes[1, 0].set_ylabel('Density')
axes[1, 0].set_title('Distribution of Residuals', fontweight='bold')

# Scale-Location
std_residuals = residuals / residuals.std()
axes[1, 1].scatter(fitted, np.sqrt(np.abs(std_residuals)), alpha=0.3, s=10, color='#2196F3')
axes[1, 1].set_xlabel('Fitted Values')
axes[1, 1].set_ylabel('√|Standardized Residuals|')
axes[1, 1].set_title('Scale-Location', fontweight='bold')

plt.suptitle('Regression Diagnostic Plots', fontsize=15, fontweight='bold', y=1.01)
plt.tight_layout()
plt.savefig('charts/12_regression_diagnostics.png', dpi=150)
plt.close()

# ─── Coefficient Plot ────────────────────────────────────────────────────────
print("  Generating coefficient plot...")
coef_df = pd.DataFrame({
    'Variable': model.params.index,
    'Coefficient': model.params.values,
    'StdErr': model.bse.values,
    'p_value': model.pvalues.values
})
coef_df = coef_df[coef_df['Variable'] != 'const'].sort_values('Coefficient')

fig, ax = plt.subplots(figsize=(10, 6))
colors = ['#4CAF50' if p < 0.05 else '#BDBDBD' for p in coef_df['p_value']]
ax.barh(coef_df['Variable'], coef_df['Coefficient'], color=colors,
        edgecolor='white', linewidth=1.5)
ax.axvline(x=0, color='red', linestyle='--', alpha=0.7)
ax.set_xlabel('Coefficient Value', fontsize=12)
ax.set_title('Regression Coefficients\n(Green = Significant at p<0.05)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('charts/13_regression_coefficients.png', dpi=150)
plt.close()

print("\nStatistical analysis complete!")
print(f"   Diagnostic charts saved to charts/ folder")
