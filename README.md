# Bias-Coherence Index (BCI) - Validation Code

**Complementary Diagnostic for Ensemble Forecast Uncertainty**

Emma Dobbin, CGT Group

**Note:** All code and data files are in the `Github_weather/` directory.

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.PENDING.svg)](https://zenodo.org/doi/PENDING)

## Summary

The Bias-Coherence Index (BCI) captures inter-model bias consensus - orthogonal to ensemble spread - for improved uncertainty quantification in limited multi-model ensembles.

**Key Result**: Partial correlation r = 0.528 (p < 0.000001) on n=156 timesteps from 14 UK extratropical cyclones using real TIGGE operational forecasts (ECMWF + CMC).

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Download TIGGE data (requires ECMWF API key)
python code/01_download_tigge.py

# Extract forecasts from GRIB files
python code/02_extract_forecasts.py

# Calculate BCI
python code/03_calculate_bci.py

# Run validation
python code/04_validation.py
```

## Dataset

- **14 UK extratropical cyclones** (2021-2024)
- **Models**: ECMWF + CMC ensemble forecasts (TIGGE archive)
- **Location**: West Bromwich, UK (52.51°N, 1.99°W)
- **Variable**: 2-meter temperature
- **Lead times**: 0-24 hours
- **Sample size**: n=156 matched forecast-observation pairs

## Results

### Model Performance (AUC for high-error detection)

| Model | AUC |
|-------|-----|
| **Spread + BCI (equal weights)** | **0.850** |
| Spread + BCI (learned weights) | 0.803 |
| Spread only | 0.775 |
| BCI only | 0.745 |

### Statistical Validation

- **Partial correlation** (controlling for spread): r = 0.528, p < 0.000001
- **Orthogonality confirmed**: BCI provides independent information
- **Cross-storm generalization**: Validated across 14 independent events

## BCI Formulation

```
BCI = √(φ × ρ)
```

Where:
- **φ (phi)**: Bias-adjusted consensus - directional agreement in forecast errors
- **ρ (rho)**: Error pattern stability - temporal coherence in residuals

## Repository Structure

```
bci-validation/
├── code/
│   ├── 01_download_tigge.py       # TIGGE data acquisition
│   ├── 02_extract_forecasts.py    # GRIB processing
│   ├── 03_calculate_bci.py        # BCI computation
│   └── 04_validation.py           # Statistical validation
├── data/
│   ├── matched_forecasts.csv      # Processed forecast-observation pairs
│   └── ensemble_forecasts.csv     # Individual ensemble members
├── results/
│   ├── bci_validation.csv         # Full BCI results (n=156)
│   └── baseline_comparison.csv    # Model performance comparison
├── docs/
│   └── manuscript.pdf             # Full manuscript
├── requirements.txt
└── README.md
```

## Installation

```bash
git clone https://github.com/emmad obbin/bci-validation.git
cd bci-validation
pip install -r requirements.txt
```

### Requirements

- Python 3.8+
- pandas, numpy, scipy
- xarray, cfgrib (for GRIB files)
- scikit-learn (for validation)
- ecmwf-api-client (for TIGGE download)

## Usage

### Using Pre-Processed Data

```python
import pandas as pd

# Load BCI validation results
df = pd.read_csv('results/bci_validation.csv')

# Analyze BCI behavior
print(df[['storm', 'BCI', 'model_std', 'mean_error']].head())
```

### Computing BCI from Scratch

```python
from code.calculate_bci import calculate_bci

# Ensemble forecasts and observation
ensemble = [10.5, 11.2, 10.8, 11.0]  # Member forecasts
observation = 12.5  # Observed temperature

# Calculate BCI
bci, phi, rho = calculate_bci(ensemble, observation)
print(f"BCI: {bci:.3f}")
```

## Citation

```bibtex
@article{dobbin2025bci,
  title={Bias-Coherence Index: A Complementary Diagnostic for 
         Ensemble Temperature Forecast Uncertainty Quantification},
  author={Dobbin, Emma},
  journal={Weather and Forecasting},
  year={2025},
  note={Submitted}
}
```

## License

MIT License - See LICENSE file

## Data Availability

- **TIGGE data**: Available from ECMWF (https://apps.ecmwf.int/datasets/data/tigge/)
- **Observation data**: From Open-Meteo Archive (https://open-meteo.com/)
- **Processed data**: Included in this repository under `data/`

## Reproducibility

All analysis can be reproduced from scratch using the provided scripts. Pre-processed data is included for convenience.

## Limitations

This is a **proof-of-concept validation** with known limitations:
- Single location (West Bromwich, UK Midlands)
- Single variable (2m temperature)
- Short lead times (0-24 hours)
- Limited ensemble size (10 members per model)
- High-impact storm selection

Broader validation across variables, locations, and forecast horizons is needed.

## Contact

Emma Dobbin - contact@cgtheory.com

## Acknowledgments

TIGGE data courtesy of ECMWF and participating centers. Observation data from Open-Meteo.

---

**Note**: This is honest, transparent science. All code and data are provided for independent verification and replication.
