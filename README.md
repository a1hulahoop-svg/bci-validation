# Bias-Coherence Index (BCI) Validation

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18079447.svg)](https://doi.org/10.5281/zenodo.18079447)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository contains code and documentation for the Bias-Coherence Index (BCI), a computationally efficient diagnostic for detecting systematic bias consensus in ensemble weather forecasts.

**Manuscript:** Dobbin, E. (2026). Bias-Coherence Index: Diagnosing Ensemble Consensus in Extratropical Cyclone Temperature Forecasts. *Weather and Forecasting* (submitted).

---

## Overview

Ensemble spread is the primary uncertainty metric in operational forecasting, but it can fail when models exhibit systematic bias consensus—situations where ensembles "agree but are wrong together." BCI addresses this gap by quantifying inter-model bias consensus independent of ensemble dispersion.

### Key Features

- ✅ **Computationally efficient:** ~0.001 seconds per forecast time
- ✅ **Interpretable formulation:** Geometric mean of bias consensus (φ) and error stability (ρ)
- ✅ **Operationally validated:** 1,218 forecasts across 14 UK extratropical cyclones
- ✅ **Strong performance:** 46% AUC improvement over spread-alone baseline
- ✅ **Open source:** MIT licensed, fully reproducible

---

## Results Summary

**Validation Dataset:**
- **n = 1,218** forecast-observation pairs
- **4 locations:** West Bromwich, London, Edinburgh, Dublin (UK/Ireland)
- **14 storms:** Major extratropical cyclones (2021-2024)
- **Models:** ECMWF + CMC ensembles (20 members total)
- **Variable:** 2-meter temperature
- **Lead times:** 0-24 hours

**Key Findings:**
- **Partial correlation:** r = -0.534 (p < 10⁻⁹⁰) controlling for spread
- **High-error detection:** AUC = 0.880 (combined), vs 0.603 (spread-only)
- **Improvement:** +46% relative to spread-alone baseline
- **Geographic consistency:** Mean BCI 0.689-0.748 across all locations

---

## Installation

### Requirements

```bash
python >= 3.8
numpy >= 1.20
pandas >= 1.3
scipy >= 1.7
scikit-learn >= 1.0
matplotlib >= 3.4
seaborn >= 0.11
```

### Setup

```bash
# Clone repository
git clone https://github.com/a1hulahoop-svg/bci-validation.git
cd bci-validation

# Install dependencies
pip install -r requirements.txt
```

---

## Usage

### Quick Start

Calculate BCI for your ensemble forecasts:

```python
import numpy as np
from bci_calculator import calculate_bci

# Your ensemble data
ensemble_forecasts = np.array([...])  # Shape: (n_members, n_times)
observations = np.array([...])         # Shape: (n_times,)

# Calculate BCI
bci_values = calculate_bci(ensemble_forecasts, observations)

print(f"Mean BCI: {bci_values.mean():.3f}")
```

### Full Validation Pipeline

Reproduce manuscript results:

```bash
# 1. Download TIGGE data (requires ECMWF account)
python download_tigge_data.py --storms storms_list.txt --locations locations.csv

# 2. Download observations
python download_observations.py --locations locations.csv --dates dates.txt

# 3. Calculate BCI with optimized parameters
python recalculate_bci_optimized.py

# 4. Generate figures
python generate_figures_optimized.py

# 5. Run sensitivity analysis
python sensitivity_analysis.py
```

---

## BCI Formulation

BCI combines two components via geometric mean:

```
BCI = √(φ × ρ)
```

Where:

**φ (Bias Consensus):** Directional agreement + magnitude consistency
```
φ = 0.7 × directional_agreement + 0.3 × magnitude_consistency
```
- `directional_agreement = max(n_positive_bias, n_negative_bias) / n_members`
- `magnitude_consistency = 1 / (1 + CV)` where `CV = σ_bias / |μ_bias|`
- Clipped to [0.3, 1.0]

**ρ (Error Stability):** Spread-skill consistency
```
ρ = min(ensemble_spread / RMSE, 1.0)
```
- Clipped to [0.3, 1.0]

**Parameter Selection:**
- 70/30 weighting chosen via cross-validated sensitivity analysis
- Geometric mean ensures both components contribute
- Clipping prevents extreme values

---

## Repository Structure

```
bci-validation/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── LICENSE                            # MIT license
│
├── scripts/
│   ├── recalculate_bci_optimized.py  # Main BCI calculation
│   ├── generate_figures_optimized.py # Create manuscript figures
│   ├── sensitivity_analysis.py       # Parameter optimization
│   ├── download_tigge_data.py        # Fetch TIGGE ensembles
│   └── download_observations.py      # Fetch Open-Meteo data
│
├── src/
│   ├── bci_calculator.py             # Core BCI functions
│   └── validation_utils.py           # Helper functions
│
├── data/
│   ├── storms_list.txt               # UK cyclone names & dates
│   ├── locations.csv                 # Station coordinates
│   └── README_data.md                # Data documentation
│
├── results/
│   ├── figures/                      # Manuscript figures
│   ├── tables/                       # Summary statistics
│   └── sensitivity/                  # Parameter tests
│
└── docs/
    ├── METHODOLOGY.md                # Detailed methods
    └── VALIDATION.md                 # Validation procedures
```

---

## Data Sources

### TIGGE Ensemble Forecasts

- **Source:** ECMWF TIGGE Archive (https://apps.ecmwf.int/datasets/data/tigge/)
- **Models:** ECMWF (10 members), CMC (10 members)
- **Variable:** 2-meter temperature
- **Temporal resolution:** 3-hourly forecasts
- **Spatial resolution:** Nearest grid point to station
- **Access:** Requires free ECMWF account

### Observations

- **Source:** Open-Meteo Archive (https://open-meteo.com/)
- **Variable:** 2-meter temperature (hourly)
- **Stations:** 
  - West Bromwich: 52.52°N, 1.98°W
  - London: 51.51°N, 0.13°W
  - Edinburgh: 55.95°N, 3.19°W
  - Dublin: 53.35°N, 6.26°W
- **Access:** Publicly available, no account required

### UK Extratropical Cyclones (2021-2024)

Storm names and dates documented in `data/storms_list.txt`:
- Arwen, Malik, Dudley, Eunice, Franklin, Noa, Babet
- Ciarán, Debi, Fergus, Gerrit, Henk, Isha, Jocelyn

---

## Reproducing Results

### Step 1: Download Data

**Note:** Full TIGGE download requires ~300 MB storage and 6-10 hours depending on connection.

```bash
# TIGGE ensemble forecasts
python scripts/download_tigge_data.py

# Observations
python scripts/download_observations.py
```

### Step 2: Calculate BCI

```bash
python scripts/recalculate_bci_optimized.py
```

**Output:**
- `bci_validation_OPTIMIZED_all_locations.csv` (1,218 timesteps)
- `BCI_Old_vs_New_Comparison.csv` (summary statistics)

### Step 3: Generate Figures

```bash
python scripts/generate_figures_optimized.py
```

**Output:**
- `Figure1_Partial_Correlation_OPTIMIZED.png`
- `Figure2_ROC_Curves_OPTIMIZED.png`
- `Figure3_BCI_Distribution_OPTIMIZED.png`

### Step 4: Sensitivity Analysis

```bash
python scripts/sensitivity_analysis.py
```

**Output:**
- `BCI_Sensitivity_Analysis.png`
- `BCI_Sensitivity_Summary.csv`

---

## Performance Metrics

| Metric | Value | Description |
|--------|-------|-------------|
| Partial correlation | r = -0.534 | BCI vs error (controlling for spread) |
| Significance | p < 10⁻⁹⁰ | Extremely significant |
| AUC (spread only) | 0.603 | Baseline discrimination |
| AUC (BCI only) | 0.246 | BCI alone (poor) |
| AUC (combined) | 0.880 | Spread + BCI (excellent) |
| Improvement | +46% | Relative to spread-only |
| Computation time | ~0.001s | Per forecast time |

---

## Citation

If you use this code or methodology, please cite:

```bibtex
@article{dobbin2026bci,
  title={Bias-Coherence Index: Diagnosing Ensemble Consensus in Extratropical Cyclone Temperature Forecasts},
  author={Dobbin, Emma},
  journal={Weather and Forecasting},
  year={2026},
  note={Submitted}
}
```

**Temporary citation:** Dobbin, E. (2026). BCI validation code and data. GitHub repository, https://github.com/a1hulahoop-svg/bci-validation

---

## Extensions & Future Work

The current validation demonstrates proof-of-concept for:
- 2 models (ECMWF + CMC)
- 2-meter temperature
- 0-24 hour lead times
- UK/Ireland extratropical cyclones

**Planned extensions:**
- [ ] Additional models (UKMO, NCEP, JMA)
- [ ] Longer lead times (24-120 hours)
- [ ] Additional variables (wind speed, precipitation)
- [ ] Global validation across climate regimes
- [ ] Real-time operational implementation

**Contributions welcome!** See `CONTRIBUTING.md` for guidelines.

---

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 Emma Dobbin, CGT Group Ltd

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## Contact

**Emma Dobbin**  
Director and Founder  
CGT Group Ltd  
Belfast, Northern Ireland, UK  

- Email: contact@cgtheory.com
- GitHub: [@a1hulahoop-svg](https://github.com/a1hulahoop-svg)

---

## Acknowledgments

- **ECMWF** for providing TIGGE archive access
- **Open-Meteo** for observational temperature data
- **UK Met Office** for storm naming and documentation
- Weather and Forecasting reviewers for constructive feedback

---

## Version History

- **v1.0.0** (January 2026) - Initial release with manuscript submission
  - ECMWF + CMC validation (n=1,218)
  - Parameter optimization (70/30 weighting)
  - Four UK/Ireland locations
  - 14 extratropical cyclones (2021-2024)

---

**Last Updated:** January 2026  
**Status:** Active development  
**DOI:** Pending publication
