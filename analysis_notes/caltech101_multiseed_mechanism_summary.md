# Caltech101 Multi-seed Mechanism Summary

## 1. Original Reproduction Results

| Seed | Split | Clean ACC | ASR |
|---:|---|---:|---:|
| 1 | base/seen | 97.7% | 99.7% |
| 1 | new/unseen | 93.7% | 99.3% |
| 2 | base/seen | 97.5% | 99.9% |
| 2 | new/unseen | 94.8% | 99.6% |
| 3 | base/seen | 97.6% | 100.0% |
| 3 | new/unseen | 95.3% | 99.2% |

## 2. Alignment Results on New Split

| Seed | Target Attraction | PCA Top5 | Consistency |
|---:|---:|---:|---:|
| 1 | 0.1466 | 0.2826 | 0.8469 |
| 2 | 0.0654 | 0.2698 | 0.8565 |
| 3 | 0.1081 | 0.3527 | 0.7659 |

## 3. Cross-split Direction Similarity

| Seed | cos(base image mean, new image mean) | cos(base text mean, new text mean) | new-to-base mean cosine | new energy in base Top10 PCs | Top10 overlap |
|---:|---:|---:|---:|---:|---:|
| 1 | 0.9878 | 0.9986 | 0.8360 | 0.3042 | 0.6040 |
| 2 | 0.9874 | 0.9999 | 0.8455 | 0.2469 | 0.4857 |
| 3 | 0.9834 | 0.9994 | 0.7518 | 0.3776 | 0.6268 |

## 4. Causal Removal and Keep-only Results on New Split

| Seed | Original ASR | Remove Mean | Remove Mean+PCA10 | Remove Random10 | Keep Mean | Keep Mean+PCA10 | Keep Random10 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 99.35% | 13.10% | 19.87% | 99.24% | 95.31% | 96.62% | 2.84% |
| 2 | 99.56% | 25.98% | 19.54% | 99.35% | 96.62% | 97.05% | 1.86% |
| 3 | 99.24% | 0.98% | 0.66% | 98.91% | 92.03% | 98.25% | 0.00% |

## 5. Conclusion

Across three random seeds, BadCLIP consistently achieves high ASR on unseen classes. The trigger-induced image shift remains highly consistent across samples and the mean backdoor direction transfers from base classes to new classes.

Removing the shared mean direction sharply reduces ASR, while keeping only this direction recovers most of the attack success. Random directions do not show similar effects. These results confirm that the shared global backdoor direction is a stable causal component of BadCLIP's cross-class backdoor generalization.
