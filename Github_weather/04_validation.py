#!/usr/bin/env python3
"""
Statistical Validation and Baseline Comparison
Author: Emma Dobbin
Date: December 2025

Validates BCI performance and compares against baseline methods.
"""

import pandas as pd
import numpy as np
from scipy.stats import pearsonr
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, confusion_matrix
from sklearn.preprocessing import StandardScaler

def partial_correlation(x, y, control):
    """
    Calculate partial correlation between x and y, controlling for z
    """
    # Residualize x and y against control
    x_resid = x - np.polyval(np.polyfit(control, x, 1), control)
    y_resid = y - np.polyval(np.polyfit(control, y, 1), control)
    
    # Correlation of residuals
    r, p = pearsonr(x_resid, y_resid)
    return r, p

def validate_bci(bci_data_file):
    """
    Run statistical validation on BCI results
    
    Parameters:
    -----------
    bci_data_file : str
        CSV file with BCI calculations
    """
    print("="*80)
    print("BCI STATISTICAL VALIDATION")
    print("="*80)
    
    df = pd.read_csv(bci_data_file)
    
    print(f"\nDataset: n={len(df)} timesteps")
    print(f"Storms: {df['storm'].nunique()}")
    print(f"Date range: {df['valid_time'].min()} to {df['valid_time'].max()}")
    
    # Basic correlations
    print(f"\n{'='*80}")
    print("CORRELATION ANALYSIS")
    print('='*80)
    
    corr_spread, p_spread = pearsonr(df['model_std'], df['mean_error'])
    corr_bci, p_bci = pearsonr(df['BCI'], df['mean_error'])
    
    print(f"\nCorrelation with forecast error:")
    print(f"  Ensemble spread: r = {corr_spread:.3f}, p = {p_spread:.6f}")
    print(f"  BCI: r = {corr_bci:.3f}, p = {p_bci:.6f}")
    
    # Partial correlation (controlling for spread)
    partial_r, partial_p = partial_correlation(
        df['BCI'].values,
        df['mean_error'].values,
        df['model_std'].values
    )
    
    print(f"\nPartial correlation (controlling for spread):")
    print(f"  r = {partial_r:.3f}, p = {partial_p:.6f}")
    
    if partial_p < 0.001:
        print("  *** HIGHLY SIGNIFICANT (p < 0.001)")
    elif partial_p < 0.01:
        print("  ** VERY SIGNIFICANT (p < 0.01)")
    elif partial_p < 0.05:
        print("  * SIGNIFICANT (p < 0.05)")
    else:
        print("  NOT SIGNIFICANT")
    
    # Per-storm analysis
    print(f"\n{'='*80}")
    print("PER-STORM STATISTICS")
    print('='*80)
    
    storm_stats = df.groupby('storm').agg({
        'BCI': ['mean', 'std'],
        'model_std': 'mean',
        'mean_error': 'mean',
        'valid_time': 'count'
    }).round(3)
    storm_stats.columns = ['BCI_mean', 'BCI_std', 'Spread', 'Error', 'N']
    print(f"\n{storm_stats.sort_values('N', ascending=False)}")
    
    return df

def baseline_comparison(bci_data_file):
    """
    Compare BCI against baseline approaches
    
    Parameters:
    -----------
    bci_data_file : str
        CSV file with BCI calculations
    """
    print("\n" + "="*80)
    print("BASELINE COMPARISON")
    print("="*80)
    
    df = pd.read_csv(bci_data_file)
    
    # Define high-error events (top 25%)
    error_threshold = df['mean_error'].quantile(0.75)
    df['high_error'] = (df['mean_error'] > error_threshold).astype(int)
    
    print(f"\nHigh-error threshold: {error_threshold:.2f}°C")
    print(f"High-error events: {df['high_error'].sum()} / {len(df)} ({df['high_error'].sum()/len(df)*100:.1f}%)")
    
    # Prepare features
    X_spread = df[['model_std']].values
    X_bci = df[['BCI']].values
    X_combined = df[['model_std', 'BCI']].values
    
    # Normalize for equal weighting
    scaler = StandardScaler()
    X_combined_norm = scaler.fit_transform(X_combined)
    
    y = df['high_error'].values
    
    results = []
    
    print(f"\nModel Performance (AUC for high-error detection):")
    print("-" * 60)
    
    # Model 1: Spread only
    lr = LogisticRegression(random_state=42, max_iter=1000)
    lr.fit(X_spread, y)
    auc = roc_auc_score(y, lr.predict_proba(X_spread)[:, 1])
    print(f"  Spread only:              AUC = {auc:.3f}")
    results.append({'Model': 'Spread only', 'AUC': auc})
    
    # Model 2: BCI only
    lr = LogisticRegression(random_state=42, max_iter=1000)
    lr.fit(X_bci, y)
    auc = roc_auc_score(y, lr.predict_proba(X_bci)[:, 1])
    print(f"  BCI only:                 AUC = {auc:.3f}")
    results.append({'Model': 'BCI only', 'AUC': auc})
    
    # Model 3: Equal weights (normalized)
    lr = LogisticRegression(random_state=42, max_iter=1000)
    lr.fit(X_combined_norm, y)
    auc = roc_auc_score(y, lr.predict_proba(X_combined_norm)[:, 1])
    print(f"  Spread + BCI (equal):     AUC = {auc:.3f}")
    results.append({'Model': 'Spread + BCI (equal)', 'AUC': auc})
    
    # Model 4: Learned weights
    lr = LogisticRegression(random_state=42, max_iter=1000)
    lr.fit(X_combined, y)
    auc = roc_auc_score(y, lr.predict_proba(X_combined)[:, 1])
    print(f"  Spread + BCI (learned):   AUC = {auc:.3f}")
    print(f"    Learned weights: Spread={lr.coef_[0][0]:.2f}, BCI={lr.coef_[0][1]:.2f}")
    results.append({'Model': 'Spread + BCI (learned)', 'AUC': auc})
    
    results_df = pd.DataFrame(results)
    
    print(f"\n{'='*80}")
    print("SUMMARY")
    print('='*80)
    print(f"\n{results_df.to_string(index=False)}")
    
    # Save results
    results_df.to_csv('../results/baseline_comparison.csv', index=False)
    print(f"\n✓ Saved: ../results/baseline_comparison.csv")
    
    return results_df

if __name__ == '__main__':
    # Run validation
    df = validate_bci('../results/bci_validation.csv')
    
    # Run baseline comparison
    baseline_comparison('../results/bci_validation.csv')
