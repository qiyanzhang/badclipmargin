# OxfordPets 2-shot ep10 BadCLIP vs BadClipMargin lambda=0.2,m=5.0 Summary

## 1. Setting

- Dataset: OxfordPets
- Shots: 2-shot
- Epochs: 10
- Seeds: 1, 2, 3
- Baseline: BadCLIP
- Method: BadClipMargin
- lambda_margin: 0.2
- margin_m: 5.0

## 2. Multi-seed Results

| Method | Seed | Base Clean ACC | Base ASR | New Clean ACC | New ASR |
|---|---:|---:|---:|---:|---:|
| BadCLIP | 1 | 81.5% | 90.9% | 86.6% | 82.6% |
| BadCLIP | 2 | 85.1% | 97.6% | 91.4% | 98.1% |
| BadCLIP | 3 | 86.1% | 96.7% | 83.1% | 91.2% |
| BadClipMargin | 1 | 75.7% | 97.4% | 90.3% | 95.2% |
| BadClipMargin | 2 | 66.2% | 99.0% | 46.9% | 89.8% |
| BadClipMargin | 3 | 82.2% | 98.7% | 55.8% | 98.9% |

## 3. Average Results

| Method | Base Clean Avg | Base ASR Avg | New Clean Avg | New ASR Avg |
|---|---:|---:|---:|---:|
| BadCLIP | 84.23% | 95.07% | 87.03% | 90.63% |
| BadClipMargin lambda=0.2,m=5.0 | 74.70% | 98.37% | 64.33% | 94.63% |

## 4. Observation

BadClipMargin lambda=0.2,m=5.0 improves ASR on OxfordPets, but it causes severe clean accuracy degradation, especially on seed2 and seed3.

This suggests that the margin objective is too strong for OxfordPets. Unlike Caltech101, OxfordPets is more sensitive to target-margin amplification, so a milder margin setting is required.

## 5. Next Step

Run a weaker setting on OxfordPets:

lambda_margin = 0.1
margin_m = 5.0

First test seed2, because seed2 shows the most severe clean accuracy collapse. If seed2 clean accuracy recovers while ASR remains competitive, then run seed1 and seed3.
