#!/usr/bin/env python3
"""
Calculate Bias-Coherence Index (BCI)
Author: Emma Dobbin
Date: December 2025

Computes BCI from ensemble forecasts and observations.
BCI = √(φ × ρ) where:
- φ: Bias-adjusted consensus (directional agreement)
- ρ: Error pattern stability (temporal coherence)
"""

import pandas as pd
import numpy as np

def calculate_bci_component_phi(ensemble_members, observation):
    """
    Calculate phi: Bias-adjusted consensus
    
    Measures directional agreement in forecast biases
    
    Parameters:
    -----------
    ensemble_members : array-like
        Ensemble member forecasts
    observation : float
        Observed value
        
    Returns:
    --------
    phi : float
        Bias consensus score [0.3, 1.0]
    """
    biases = ensemble_members - observation
    
    # Directional agreement
    n_positive = np.sum(biases > 0)
    n_negative = np.sum(biases < 0)
    directional_agreement = max(n_positive, n_negative) / len(biases)
    
    # Magnitude consistency
    bias_std = np.std(biases)
    bias_mean = np.abs(np.mean(biases))
    
    if bias_mean > 0.01:
        cv = bias_std / bias_mean
        magnitude_consistency = 1 / (1 + cv)
    else:
        magnitude_consistency = 0.8  # Default for near-zero bias
    
    # Combined phi
    phi = 0.5 * directional_agreement + 0.5 * magnitude_consistency
    phi = np.clip(phi, 0.3, 1.0)
    
    return phi

def calculate_bci_component_rho(spread, error):
    """
    Calculate rho: Error pattern stability
    
    Simplified version using spread-skill ratio as proxy
    
    Parameters:
    -----------
    spread : float
        Ensemble standard deviation
    error : float
        Forecast error magnitude
        
    Returns:
    --------
    rho : float
        Stability score [0.3, 1.0]
    """
    if error > 0.1:
        spread_skill_ratio = min(spread / error, 1.0)
    else:
        spread_skill_ratio = 1.0
    
    rho = np.clip(spread_skill_ratio, 0.3, 1.0)
    
    return rho

def calculate_bci(ensemble_members, observation, spread=None, error=None):
    """
    Calculate complete BCI
    
    Parameters:
    -----------
    ensemble_members : array-like
        Ensemble member forecasts
    observation : float
        Observed value
    spread : float, optional
        Pre-computed ensemble spread
    error : float, optional
        Pre-computed forecast error
        
    Returns:
    --------
    bci : float
        Bias-Coherence Index [~0.3, ~1.0]
    phi : float
        Phi component
    rho : float
        Rho component
    """
    # Calculate phi from ensemble-observation relationship
    phi = calculate_bci_component_phi(ensemble_members, observation)
    
    # Calculate rho from spread-error relationship
    if spread is None:
        spread = np.std(ensemble_members)
    if error is None:
        error = np.abs(np.mean(ensemble_members) - observation)
    
    rho = calculate_bci_component_rho(spread, error)
    
    # BCI is geometric mean
    bci = np.sqrt(phi * rho)
    
    return bci, phi, rho

def process_validation_data(matched_forecasts_file, ensemble_forecasts_file, output_file):
    """
    Calculate BCI for all timesteps in validation dataset
    
    Parameters:
    -----------
    matched_forecasts_file : str
        CSV with matched forecast-observation pairs
    ensemble_forecasts_file : str
        CSV with individual ensemble member forecasts
    output_file : str
        Output CSV path
    """
    print("="*80)
    print("CALCULATING BCI FOR VALIDATION DATASET")
    print("="*80)
    
    # Load data
    matched_df = pd.read_csv(matched_forecasts_file)
    ensemble_df = pd.read_csv(ensemble_forecasts_file)
    
    ensemble_df['valid_time'] = pd.to_datetime(ensemble_df['valid_time'])
    matched_df['valid_time'] = pd.to_datetime(matched_df['valid_time'])
    
    print(f"\nProcessing {len(matched_df)} timesteps...")
    
    results = []
    
    for idx, row in matched_df.iterrows():
        storm = row['storm']
        vt = row['valid_time']
        obs = row['obs_temperature']
        spread = row['model_std']
        error = row['mean_error']
        
        # Get ensemble members
        members = ensemble_df[
            (ensemble_df['storm'] == storm) &
            (ensemble_df['valid_time'] == vt)
        ]['temperature'].values
        
        if len(members) < 4:
            continue
        
        # Calculate BCI
        bci, phi, rho = calculate_bci(members, obs, spread, error)
        
        results.append({
            'storm': storm,
            'valid_time': vt,
            'obs_temperature': obs,
            'model_mean': row['model_mean'],
            'model_std': spread,
            'mean_error': error,
            'phi': phi,
            'rho': rho,
            'BCI': bci,
            'n_members': len(members)
        })
    
    # Save results
    results_df = pd.DataFrame(results)
    results_df.to_csv(output_file, index=False)
    
    print(f"\n✓ BCI calculated for {len(results_df)} timesteps")
    print(f"✓ Saved: {output_file}")
    
    # Summary statistics
    print(f"\nBCI Statistics:")
    print(f"  Mean: {results_df['BCI'].mean():.3f}")
    print(f"  Std: {results_df['BCI'].std():.3f}")
    print(f"  Range: {results_df['BCI'].min():.3f} - {results_df['BCI'].max():.3f}")
    
    print(f"\nPhi Statistics:")
    print(f"  Mean: {results_df['phi'].mean():.3f}")
    
    print(f"\nRho Statistics:")
    print(f"  Mean: {results_df['rho'].mean():.3f}")
    
    return results_df

if __name__ == '__main__':
    # Example usage
    process_validation_data(
        matched_forecasts_file='../data/matched_forecasts.csv',
        ensemble_forecasts_file='../data/ensemble_forecasts.csv',
        output_file='../results/bci_validation.csv'
    )
