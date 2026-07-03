# Caltech101 Target Sensitivity: 2-shot Seed1

## Target Mapping

| Target index | Target name |
|---:|---|
| 0 | face |
| 1 | leopard |
| 2 | motorbike |

## Results

| Target | Target name | Method | Base Clean | Base ASR | New Clean | New ASR |
|---:|---|---|---:|---:|---:|---:|
| 0 | face | BadCLIP | 96.5 | 98.6 | 94.2 | 92.1 |
| 0 | face | BadClipMargin | 96.3 | 99.7 | 93.3 | 98.3 |
| 1 | leopard | BadCLIP | 95.0 | 99.5 | 87.0 | 95.0 |
| 1 | leopard | BadClipMargin | 92.5 | 99.9 | 87.2 | 99.6 |
| 2 | motorbike | BadCLIP | 96.5 | 99.4 | 93.8 | 97.1 |
| 2 | motorbike | BadClipMargin | 92.8 | 100.0 | 93.4 | 99.3 |

## Improvement

| Target | Target name | Delta Base Clean | Delta Base ASR | Delta New Clean | Delta New ASR |
|---:|---|---:|---:|---:|---:|
| 0 | face | -0.2 | +1.1 | -0.9 | +6.2 |
| 1 | leopard | -2.5 | +0.4 | +0.2 | +4.6 |
| 2 | motorbike | -3.7 | +0.6 | -0.4 | +2.2 |

## Conclusion

BadClipMargin consistently improves New ASR across three target classes, including face, leopard, and motorbike. This suggests that the method is not tied to a single target class. New Clean remains largely stable, while Base Clean may decrease for some targets, indicating a clean-ASR trade-off.
