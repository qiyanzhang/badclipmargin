# Target Sensitivity Table for Paper

| Target | Name | Method | Base Clean | Base ASR | New Clean | New ASR |
|---:|---|---|---:|---:|---:|---:|
| 1 | leopard | BadCLIP | 95.17 | 98.50 | 90.57 | 96.20 |
| 1 | leopard | BadClipMargin | 93.83 | 99.77 | 89.70 | 99.43 |
| 2 | motorbike | BadCLIP | 96.10 | 99.23 | 92.83 | 97.17 |
| 2 | motorbike | BadClipMargin | 95.07 | 99.93 | 92.93 | 99.47 |

## Improvement

| Target | Name | Delta Base Clean | Delta Base ASR | Delta New Clean | Delta New ASR |
|---:|---|---:|---:|---:|---:|
| 1 | leopard | -1.33 | +1.27 | -0.87 | +3.23 |
| 2 | motorbike | -1.03 | +0.70 | +0.10 | +2.30 |

## Takeaway

BadClipMargin improves unseen-class ASR across additional target classes, showing that the method is not restricted to the original face target. The improvement comes with a mild Base Clean trade-off, while New Clean remains largely stable.
