# Caltech101 Target Sensitivity: Target 1/2, 2-shot, 3 Seeds

## Per-seed Results

| Target | Name | Seed | Method | Base Clean | Base ASR | New Clean | New ASR |
|---:|---|---:|---|---:|---:|---:|---:|
| 1 | leopard | 1 | BadCLIP | 95.0 | 99.5 | 87.0 | 95.0 |
| 1 | leopard | 1 | BadClipMargin | 92.5 | 99.9 | 87.2 | 99.6 |
| 1 | leopard | 2 | BadCLIP | 96.1 | 98.8 | 92.0 | 97.9 |
| 1 | leopard | 2 | BadClipMargin | 95.5 | 99.9 | 92.2 | 99.6 |
| 1 | leopard | 3 | BadCLIP | 94.4 | 97.2 | 92.7 | 95.7 |
| 1 | leopard | 3 | BadClipMargin | 93.5 | 99.5 | 89.7 | 99.1 |
| 2 | motorbike | 1 | BadCLIP | 96.5 | 99.4 | 93.8 | 97.1 |
| 2 | motorbike | 1 | BadClipMargin | 92.8 | 100.0 | 93.4 | 99.3 |
| 2 | motorbike | 2 | BadCLIP | 96.1 | 99.4 | 91.8 | 96.7 |
| 2 | motorbike | 2 | BadClipMargin | 97.0 | 100.0 | 92.9 | 99.9 |
| 2 | motorbike | 3 | BadCLIP | 95.7 | 98.9 | 92.9 | 97.7 |
| 2 | motorbike | 3 | BadClipMargin | 95.4 | 99.8 | 92.5 | 99.2 |

## Mean over 3 Seeds

| Target | Name | Method | Base Clean | Base ASR | New Clean | New ASR |
|---:|---|---|---:|---:|---:|---:|
| 1 | leopard | BadCLIP | 95.17 | 98.50 | 90.57 | 96.20 |
| 1 | leopard | BadClipMargin | 93.83 | 99.77 | 89.70 | 99.43 |
| 2 | motorbike | BadCLIP | 96.10 | 99.23 | 92.83 | 97.17 |
| 2 | motorbike | BadClipMargin | 95.07 | 99.93 | 92.93 | 99.47 |

## Improvement: BadClipMargin - BadCLIP

| Target | Name | Delta Base Clean | Delta Base ASR | Delta New Clean | Delta New ASR |
|---:|---|---:|---:|---:|---:|
| 1 | leopard | -1.33 | +1.27 | -0.87 | +3.23 |
| 2 | motorbike | -1.03 | +0.70 | +0.10 | +2.30 |

## Notes

- Target 1 is leopard.
- Target 2 is motorbike.
- The last two accuracy values in each log are parsed as Clean ACC and ASR.
