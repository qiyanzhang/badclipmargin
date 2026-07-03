# OxfordPets 2-shot ep10 BadClipMargin lambda=0.1,m=5.0 Multi-seed Summary

## 1. Setting

- Dataset: OxfordPets
- Shots: 2-shot
- Epochs: 10
- Seeds: 1, 2, 3
- Baseline: BadCLIP
- Method: BadClipMargin
- lambda_margin: 0.1
- margin_m: 5.0

## 2. Main Results

| Method | Seed | Base Clean ACC | Base ASR | New Clean ACC | New ASR |
|---|---:|---:|---:|---:|---:|
| BadCLIP | 1 | 81.5% | 90.9% | 86.6% | 82.6% |
| BadCLIP | 2 | 85.1% | 97.6% | 91.4% | 98.1% |
| BadCLIP | 3 | 86.1% | 96.7% | 83.1% | 91.2% |
| BadClipMargin lambda=0.1,m=5.0 | 1 | 80.2% | 97.0% | 90.4% | 94.6% |
| BadClipMargin lambda=0.1,m=5.0 | 2 | 83.1% | 96.9% | 90.5% | 95.1% |
| BadClipMargin lambda=0.1,m=5.0 | 3 | 88.2% | 97.2% | 93.7% | 94.2% |

## 3. Average Results

| Method | Base Clean Avg | Base ASR Avg | New Clean Avg | New ASR Avg |
|---|---:|---:|---:|---:|
| BadCLIP | 84.23% | 95.07% | 87.03% | 90.63% |
| BadClipMargin lambda=0.1,m=5.0 | 83.83% | 97.03% | 91.53% | 94.63% |

## 4. Improvement over BadCLIP

| Metric | Improvement |
|---|---:|
| Base Clean ACC | -0.40% |
| Base ASR | +1.96% |
| New Clean ACC | +4.50% |
| New ASR | +4.00% |

## 5. Comparison with lambda=0.2,m=5.0

| Method | Base Clean Avg | Base ASR Avg | New Clean Avg | New ASR Avg |
|---|---:|---:|---:|---:|
| BadClipMargin lambda=0.2,m=5.0 | 74.70% | 98.37% | 64.33% | 94.63% |
| BadClipMargin lambda=0.1,m=5.0 | 83.83% | 97.03% | 91.53% | 94.63% |

lambda=0.2,m=5.0 improves ASR but severely hurts clean accuracy on OxfordPets.

lambda=0.1,m=5.0 achieves the same average new ASR as lambda=0.2,m=5.0, while substantially improving clean accuracy.

## 6. Conclusion

For OxfordPets 2-shot ep10, lambda=0.1,m=5.0 is a better margin setting than lambda=0.2,m=5.0.

BadClipMargin improves low-shot backdoor generalization on OxfordPets, but the dataset is more sensitive to the strength of margin amplification than Caltech101.

Therefore, OxfordPets can be used as the second dataset, with lambda=0.1,m=5.0 as the main setting.
