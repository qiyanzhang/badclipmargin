# Robustness under Selected Input Preprocessing Settings

- Setting: 2-shot base-to-new evaluation
- Seeds: 1, 2, 3
- Parsed logs: 60
- Failed logs: 0

## Per-seed Results

| Dataset | Method | Seed | Preprocess | New Clean | New ASR |
|---|---|---:|---|---:|---:|
| caltech101 | BadCLIP | 1 | none | 94.20 | 92.10 |
| caltech101 | BadCLIP | 1 | color0.90 | 94.20 | 86.40 |
| caltech101 | BadCLIP | 1 | blur0.5 | 94.40 | 90.10 |
| caltech101 | BadCLIP | 1 | jpeg70 | 93.70 | 0.00 |
| caltech101 | BadCLIP | 1 | resize0.95 | 94.50 | 19.70 |
| caltech101 | BadCLIP | 2 | none | 88.80 | 95.70 |
| caltech101 | BadCLIP | 2 | color0.90 | 88.20 | 95.30 |
| caltech101 | BadCLIP | 2 | blur0.5 | 89.60 | 95.30 |
| caltech101 | BadCLIP | 2 | jpeg70 | 88.30 | 0.30 |
| caltech101 | BadCLIP | 2 | resize0.95 | 89.60 | 28.20 |
| caltech101 | BadCLIP | 3 | none | 90.30 | 91.70 |
| caltech101 | BadCLIP | 3 | color0.90 | 91.30 | 84.20 |
| caltech101 | BadCLIP | 3 | blur0.5 | 90.50 | 93.10 |
| caltech101 | BadCLIP | 3 | jpeg70 | 89.80 | 1.30 |
| caltech101 | BadCLIP | 3 | resize0.95 | 91.20 | 42.60 |
| caltech101 | BadClipMargin | 1 | none | 93.30 | 98.30 |
| caltech101 | BadClipMargin | 1 | color0.90 | 92.60 | 97.10 |
| caltech101 | BadClipMargin | 1 | blur0.5 | 92.90 | 98.60 |
| caltech101 | BadClipMargin | 1 | jpeg70 | 92.40 | 0.40 |
| caltech101 | BadClipMargin | 1 | resize0.95 | 93.30 | 46.90 |
| caltech101 | BadClipMargin | 2 | none | 94.30 | 98.90 |
| caltech101 | BadClipMargin | 2 | color0.90 | 92.80 | 98.00 |
| caltech101 | BadClipMargin | 2 | blur0.5 | 94.10 | 98.70 |
| caltech101 | BadClipMargin | 2 | jpeg70 | 93.20 | 0.70 |
| caltech101 | BadClipMargin | 2 | resize0.95 | 94.10 | 42.90 |
| caltech101 | BadClipMargin | 3 | none | 94.80 | 98.90 |
| caltech101 | BadClipMargin | 3 | color0.90 | 94.80 | 96.00 |
| caltech101 | BadClipMargin | 3 | blur0.5 | 94.90 | 99.70 |
| caltech101 | BadClipMargin | 3 | jpeg70 | 94.00 | 0.10 |
| caltech101 | BadClipMargin | 3 | resize0.95 | 95.10 | 60.70 |
| food101 | BadCLIP | 1 | none | 90.50 | 98.00 |
| food101 | BadCLIP | 1 | color0.90 | 90.00 | 95.70 |
| food101 | BadCLIP | 1 | blur0.5 | 89.90 | 96.60 |
| food101 | BadCLIP | 1 | jpeg70 | 86.20 | 5.30 |
| food101 | BadCLIP | 1 | resize0.95 | 89.80 | 8.10 |
| food101 | BadCLIP | 2 | none | 89.50 | 95.40 |
| food101 | BadCLIP | 2 | color0.90 | 89.40 | 96.00 |
| food101 | BadCLIP | 2 | blur0.5 | 89.10 | 91.00 |
| food101 | BadCLIP | 2 | jpeg70 | 87.30 | 0.30 |
| food101 | BadCLIP | 2 | resize0.95 | 89.00 | 5.90 |
| food101 | BadCLIP | 3 | none | 88.60 | 96.60 |
| food101 | BadCLIP | 3 | color0.90 | 88.60 | 93.60 |
| food101 | BadCLIP | 3 | blur0.5 | 88.20 | 94.90 |
| food101 | BadCLIP | 3 | jpeg70 | 81.40 | 7.80 |
| food101 | BadCLIP | 3 | resize0.95 | 88.80 | 3.80 |
| food101 | BadClipMargin | 1 | none | 90.40 | 99.70 |
| food101 | BadClipMargin | 1 | color0.90 | 90.00 | 98.80 |
| food101 | BadClipMargin | 1 | blur0.5 | 89.80 | 99.40 |
| food101 | BadClipMargin | 1 | jpeg70 | 85.50 | 6.40 |
| food101 | BadClipMargin | 1 | resize0.95 | 89.90 | 8.80 |
| food101 | BadClipMargin | 2 | none | 89.10 | 95.80 |
| food101 | BadClipMargin | 2 | color0.90 | 88.80 | 96.60 |
| food101 | BadClipMargin | 2 | blur0.5 | 88.60 | 91.10 |
| food101 | BadClipMargin | 2 | jpeg70 | 87.00 | 0.40 |
| food101 | BadClipMargin | 2 | resize0.95 | 89.00 | 6.30 |
| food101 | BadClipMargin | 3 | none | 88.20 | 98.80 |
| food101 | BadClipMargin | 3 | color0.90 | 88.10 | 97.50 |
| food101 | BadClipMargin | 3 | blur0.5 | 87.60 | 98.60 |
| food101 | BadClipMargin | 3 | jpeg70 | 69.90 | 21.40 |
| food101 | BadClipMargin | 3 | resize0.95 | 87.60 | 8.30 |

## Mean ± Std Results

| Dataset | Method | Preprocess | New Clean | New ASR |
|---|---|---|---:|---:|
| caltech101 | BadCLIP | none | 91.10±2.79 | 93.17±2.20 |
| caltech101 | BadCLIP | color0.90 | 91.23±3.00 | 88.63±5.88 |
| caltech101 | BadCLIP | blur0.5 | 91.50±2.55 | 92.83±2.61 |
| caltech101 | BadCLIP | jpeg70 | 90.60±2.79 | 0.53±0.68 |
| caltech101 | BadCLIP | resize0.95 | 91.77±2.50 | 30.17±11.58 |
| caltech101 | BadClipMargin | none | 94.13±0.76 | 98.70±0.35 |
| caltech101 | BadClipMargin | color0.90 | 93.40±1.22 | 97.03±1.00 |
| caltech101 | BadClipMargin | blur0.5 | 93.97±1.01 | 99.00±0.61 |
| caltech101 | BadClipMargin | jpeg70 | 93.20±0.80 | 0.40±0.30 |
| caltech101 | BadClipMargin | resize0.95 | 94.17±0.90 | 50.17±9.34 |
| food101 | BadCLIP | none | 89.53±0.95 | 96.67±1.30 |
| food101 | BadCLIP | color0.90 | 89.33±0.70 | 95.10±1.31 |
| food101 | BadCLIP | blur0.5 | 89.07±0.85 | 94.17±2.87 |
| food101 | BadCLIP | jpeg70 | 84.97±3.14 | 4.47±3.82 |
| food101 | BadCLIP | resize0.95 | 89.20±0.53 | 5.93±2.15 |
| food101 | BadClipMargin | none | 89.23±1.11 | 98.10±2.04 |
| food101 | BadClipMargin | color0.90 | 88.97±0.96 | 97.63±1.11 |
| food101 | BadClipMargin | blur0.5 | 88.67±1.10 | 96.37±4.58 |
| food101 | BadClipMargin | jpeg70 | 80.80±9.47 | 9.40±10.82 |
| food101 | BadClipMargin | resize0.95 | 88.83±1.16 | 7.80±1.32 |

## Mean Changes Relative to None

| Dataset | Method | Preprocess | Δ New Clean | Δ New ASR |
|---|---|---|---:|---:|
| caltech101 | BadCLIP | color0.90 | +0.13 | -4.53 |
| caltech101 | BadCLIP | blur0.5 | +0.40 | -0.33 |
| caltech101 | BadCLIP | jpeg70 | -0.50 | -92.63 |
| caltech101 | BadCLIP | resize0.95 | +0.67 | -63.00 |
| caltech101 | BadClipMargin | color0.90 | -0.73 | -1.67 |
| caltech101 | BadClipMargin | blur0.5 | -0.17 | +0.30 |
| caltech101 | BadClipMargin | jpeg70 | -0.93 | -98.30 |
| caltech101 | BadClipMargin | resize0.95 | +0.03 | -48.53 |
| food101 | BadCLIP | color0.90 | -0.20 | -1.57 |
| food101 | BadCLIP | blur0.5 | -0.47 | -2.50 |
| food101 | BadCLIP | jpeg70 | -4.57 | -92.20 |
| food101 | BadCLIP | resize0.95 | -0.33 | -90.73 |
| food101 | BadClipMargin | color0.90 | -0.27 | -0.47 |
| food101 | BadClipMargin | blur0.5 | -0.57 | -1.73 |
| food101 | BadClipMargin | jpeg70 | -8.43 | -88.70 |
| food101 | BadClipMargin | resize0.95 | -0.40 | -90.30 |
