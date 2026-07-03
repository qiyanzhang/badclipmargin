# BadClipMargin Hyperparameter Ablation: Paper Table

| Dataset | Method / Param | Base Clean | Base ASR | New Clean | New ASR |
|---|---|---:|---:|---:|---:|
| Caltech101 | BadCLIP | 95.43 | 98.27 | 91.10 | 93.17 |
| Caltech101 | BadClipMargin λ=0.2,m=5 | 96.77 | 99.70 | 94.13 | 98.70 |
| Caltech101 | BadClipMargin λ=0.5,m=5 | 95.83 | 99.80 | 92.30 | 99.03 |
| OxfordPets | BadCLIP | 84.23 | 95.07 | 87.03 | 90.63 |
| OxfordPets | BadClipMargin λ=0.1,m=5 | 83.83 | 97.03 | 91.53 | 94.63 |
| OxfordPets | BadClipMargin λ=0.2,m=5 | 74.70 | 98.37 | 64.33 | 94.63 |

## Takeaway

For Caltech101, λ=0.2,m=5 achieves the best clean-ASR trade-off. Although λ=0.5,m=5 slightly improves New ASR, it reduces New Clean.

For OxfordPets, λ=0.2,m=5 causes severe clean accuracy degradation without improving New ASR. Therefore, λ=0.1,m=5 is selected as the main configuration.

Overall, the results show that target-margin amplification is effective, but overly strong margin weights can hurt clean performance.
