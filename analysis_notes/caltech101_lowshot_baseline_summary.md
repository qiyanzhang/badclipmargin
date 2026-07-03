# Caltech101 Low-shot BadCLIP Baseline Summary

## 1. Original 16-shot Baseline

| Setting | Split | Clean ACC | ASR |
|---|---|---:|---:|
| 16-shot ep10 | base/seen | 97.7% | 99.7% |
| 16-shot ep10 | new/unseen | 93.7% | 99.3% |

## 2. Low-shot Baselines

| Setting | Split | Clean ACC | ASR |
|---|---|---:|---:|
| 4-shot ep10 | base/seen | 97.4% | 99.5% |
| 4-shot ep10 | new/unseen | 92.9% | 97.4% |
| 2-shot ep10 | base/seen | 96.5% | 98.6% |
| 2-shot ep10 | new/unseen | 94.2% | 92.1% |
| 2-shot ep20 | base/seen | 97.1% | 99.5% |
| 2-shot ep20 | new/unseen | 93.0% | 97.4% |

## 3. Current Observation

The 2-shot ep10 setting reduces unseen ASR from 99.3% to 92.1%, while clean accuracy remains high.
However, increasing the training epochs to 20 improves unseen ASR to 97.4%, indicating that the ep10 degradation is partially due to insufficient optimization.

Therefore, 1-shot should be evaluated next to find a more challenging low-shot setting.

## 4. 1-shot ep10 Baseline

| Setting | Split | Clean ACC | ASR |
|---|---|---:|---:|
| 1-shot ep10 | base/seen | 96.1% | 96.8% |
| 1-shot ep10 | new/unseen | 92.8% | 87.2% |

## 5. Observation after 1-shot ep10

The 1-shot ep10 setting substantially reduces unseen ASR to 87.2%, while clean accuracy remains 92.8%.
This suggests that 1-shot is a more challenging setting than 2-shot and may be suitable for method improvement.
However, an ep20 control experiment is still needed to check whether longer training can recover the ASR.

## 6. 1-shot ep20 Baseline

| Setting | Split | Clean ACC | ASR |
|---|---|---:|---:|
| 1-shot ep20 | base/seen | 96.3% | 98.2% |
| 1-shot ep20 | new/unseen | 92.8% | 90.5% |

## 7. Low-shot Conclusion

Compared with 16-shot, the 1-shot setting substantially reduces unseen ASR while keeping clean accuracy relatively stable.

Increasing training epochs from 10 to 20 only improves unseen ASR from 87.2% to 90.5%, which is still much lower than the 16-shot unseen ASR of 99.3% and the 2-shot ep20 unseen ASR of 97.4%.

Therefore, 1-shot is a suitable challenging setting for analyzing and improving BadCLIP's cross-class backdoor generalization.

## 8. 1-shot ep20 Seed2 Result

| Setting | Split | Clean ACC | ASR |
|---|---|---:|---:|
| 1-shot ep20 seed2 | base/seen | 96.1% | 98.5% |
| 1-shot ep20 seed2 | new/unseen | 86.1% | 95.9% |

Observation: Compared with seed1, seed2 obtains higher unseen ASR but lower unseen clean accuracy, indicating that the 1-shot setting is sensitive to seed and training sample selection.

## 9. Caltech101 2-shot ep10 Multi-seed Result

| Seed | Base Clean ACC | Base ASR | New Clean ACC | New ASR |
|---:|---:|---:|---:|---:|
| 1 | 96.5% | 98.6% | 94.2% | 92.1% |
| 2 | 96.8% | 99.1% | 88.8% | 95.7% |
| 3 | 93.0% | 97.1% | 90.3% | 91.7% |

Average results:

| Metric | Mean |
|---|---:|
| Base Clean ACC | 95.43% |
| Base ASR | 98.27% |
| New Clean ACC | 91.10% |
| New ASR | 93.17% |

Observation:

The 2-shot ep10 setting shows a consistent decrease in new/unseen ASR compared with the 16-shot setting, while avoiding the severe clean accuracy collapse observed in the 1-shot ep20 setting. Therefore, Caltech101 2-shot ep10 is selected as the main low-shot setting for subsequent method improvement.

## 10. BadClipMargin Multi-seed Result on Caltech101 2-shot ep10

| Method | Seed | Base Clean ACC | Base ASR | New Clean ACC | New ASR |
|---|---:|---:|---:|---:|---:|
| BadCLIP | 1 | 96.5% | 98.6% | 94.2% | 92.1% |
| BadCLIP | 2 | 96.8% | 99.1% | 88.8% | 95.7% |
| BadCLIP | 3 | 93.0% | 97.1% | 90.3% | 91.7% |
| BadClipMargin | 1 | 96.7% | 99.8% | 92.0% | 98.6% |
| BadClipMargin | 2 | 95.8% | 99.7% | 90.9% | 99.0% |
| BadClipMargin | 3 | 95.0% | 99.9% | 94.0% | 99.5% |

Average results:

| Method | Base Clean Avg | Base ASR Avg | New Clean Avg | New ASR Avg |
|---|---:|---:|---:|---:|
| BadCLIP | 95.43% | 98.27% | 91.10% | 93.17% |
| BadClipMargin | 95.83% | 99.80% | 92.30% | 99.03% |

Observation:

BadClipMargin improves new/unseen average ASR by 5.86 percentage points, from 93.17% to 99.03%, while maintaining or slightly improving clean accuracy. This validates target margin amplification as an effective solution for low-shot BadCLIP generalization.
