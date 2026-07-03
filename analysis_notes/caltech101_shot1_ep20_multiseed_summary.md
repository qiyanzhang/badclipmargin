# Caltech101 1-shot ep20 Multi-seed Baseline Summary

| Seed | Base Clean ACC | Base ASR | New Clean ACC | New ASR |
|---:|---:|---:|---:|---:|
| 1 | 96.3% | 98.2% | 92.8% | 90.5% |
| 2 | 96.1% | 98.5% | 86.1% | 95.9% |
| 3 | 87.5% | 92.8% | 78.3% | 81.7% |

## Observation

The 1-shot ep20 setting shows strong seed sensitivity. In seed1, unseen ASR decreases to 90.5% while clean accuracy remains high. In seed2, unseen ASR is higher but unseen clean accuracy drops to 86.1%. In seed3, both clean accuracy and ASR drop substantially.

This indicates that the extremely low-shot setting affects not only backdoor generalization but also clean classification generalization. Therefore, 1-shot ep20 is useful for analyzing low-shot instability, but it may not be ideal as the main method-comparison setting.
