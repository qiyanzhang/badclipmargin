# Main Results with Mean ± Std

- Shot: 2
- Seeds: [1, 2, 3]
- Std is computed across three random seeds.
- Caltech101 BadCLIP baseline is filled from verified per-seed records because the corresponding run logs are not stored under the unified log names.

## Per-seed Results

| Dataset | Seed | Method | Base Clean | Base ASR | New Clean | New ASR |
|---|---:|---|---:|---:|---:|---:|
| Caltech101 | 1 | BadCLIP | 96.5 | 98.6 | 94.2 | 92.1 |
| Caltech101 | 2 | BadCLIP | 96.8 | 99.1 | 88.8 | 95.7 |
| Caltech101 | 3 | BadCLIP | 93.0 | 97.1 | 90.3 | 91.7 |
| Caltech101 | 1 | BadClipMargin | 96.3 | 99.7 | 93.3 | 98.3 |
| Caltech101 | 2 | BadClipMargin | 97.2 | 99.7 | 94.3 | 98.9 |
| Caltech101 | 3 | BadClipMargin | 96.8 | 99.7 | 94.8 | 98.9 |
| OxfordPets | 1 | BadCLIP | 81.5 | 90.9 | 86.6 | 82.6 |
| OxfordPets | 2 | BadCLIP | 85.1 | 97.6 | 91.4 | 98.1 |
| OxfordPets | 3 | BadCLIP | 86.1 | 96.7 | 83.1 | 91.2 |
| OxfordPets | 1 | BadClipMargin | 80.2 | 97.0 | 90.4 | 94.6 |
| OxfordPets | 2 | BadClipMargin | 83.1 | 96.9 | 90.5 | 95.1 |
| OxfordPets | 3 | BadClipMargin | 88.2 | 97.2 | 93.7 | 94.2 |
| Food101 | 1 | BadCLIP | 89.6 | 98.5 | 90.5 | 98.0 |
| Food101 | 2 | BadCLIP | 88.8 | 96.2 | 89.5 | 95.4 |
| Food101 | 3 | BadCLIP | 88.1 | 98.3 | 88.6 | 96.6 |
| Food101 | 1 | BadClipMargin | 89.1 | 99.7 | 90.4 | 99.7 |
| Food101 | 2 | BadClipMargin | 89.2 | 97.1 | 89.1 | 95.8 |
| Food101 | 3 | BadClipMargin | 88.6 | 99.4 | 88.2 | 98.8 |

## Mean ± Std Results

| Dataset | Method | Base Clean | Base ASR | New Clean | New ASR |
|---|---|---:|---:|---:|---:|
| Caltech101 | BadCLIP | 95.43±2.11 | 98.27±1.04 | 91.10±2.79 | 93.17±2.20 |
| Caltech101 | BadClipMargin | 96.77±0.45 | 99.70±0.00 | 94.13±0.76 | 98.70±0.35 |
| OxfordPets | BadCLIP | 84.23±2.42 | 95.07±3.64 | 87.03±4.17 | 90.63±7.77 |
| OxfordPets | BadClipMargin | 83.83±4.05 | 97.03±0.15 | 91.53±1.88 | 94.63±0.45 |
| Food101 | BadCLIP | 88.83±0.75 | 97.67±1.27 | 89.53±0.95 | 96.67±1.30 |
| Food101 | BadClipMargin | 88.97±0.32 | 98.73±1.42 | 89.23±1.11 | 98.10±2.04 |

## Improvement Based on Mean Values

| Dataset | Δ Base Clean | Δ Base ASR | Δ New Clean | Δ New ASR |
|---|---:|---:|---:|---:|
| Caltech101 | +1.33 | +1.43 | +3.03 | +5.53 |
| OxfordPets | -0.40 | +1.97 | +4.50 | +4.00 |
| Food101 | +0.13 | +1.07 | -0.30 | +1.43 |