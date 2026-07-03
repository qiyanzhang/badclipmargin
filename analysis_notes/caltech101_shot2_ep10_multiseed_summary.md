# Caltech101 2-shot ep10 Multi-seed Baseline Summary

## 1. Experimental Setting

- Dataset: Caltech101
- Training split: base / seen classes
- Testing split: base / seen and new / unseen classes
- Method: BadCLIP
- Shots: 2-shot
- Epochs: 10
- Seeds: 1, 2, 3
- Target class: face

This setting is used to evaluate whether BadCLIP's backdoor generalization becomes weaker under low-shot and limited-training-budget conditions.

## 2. Multi-seed Results

| Seed | Base Clean ACC | Base ASR | New Clean ACC | New ASR |
|---:|---:|---:|---:|---:|
| 1 | 96.5% | 98.6% | 94.2% | 92.1% |
| 2 | 96.8% | 99.1% | 88.8% | 95.7% |
| 3 | 93.0% | 97.1% | 90.3% | 91.7% |

## 3. Average Results

| Metric | Mean |
|---|---:|
| Base Clean ACC | 95.43% |
| Base ASR | 98.27% |
| New Clean ACC | 91.10% |
| New ASR | 93.17% |

## 4. Main Observation

Compared with the 16-shot setting, Caltech101 2-shot ep10 shows a clear decrease in new/unseen ASR.

- 16-shot seed1 new ASR: 99.3%
- 2-shot ep10 average new ASR: 93.17%

This indicates that BadCLIP's cross-class backdoor generalization becomes weaker under low-shot and limited-training-budget conditions.

Unlike the 1-shot ep20 setting, 2-shot ep10 does not completely collapse clean accuracy. Although clean accuracy still varies across seeds, it remains much more stable than the 1-shot case.

## 5. Comparison with 1-shot ep20

| Setting | Seed | New Clean ACC | New ASR |
|---|---:|---:|---:|
| 1-shot ep20 | 1 | 92.8% | 90.5% |
| 1-shot ep20 | 2 | 86.1% | 95.9% |
| 1-shot ep20 | 3 | 78.3% | 81.7% |
| 2-shot ep10 | 1 | 94.2% | 92.1% |
| 2-shot ep10 | 2 | 88.8% | 95.7% |
| 2-shot ep10 | 3 | 90.3% | 91.7% |

The 1-shot ep20 setting is too unstable, especially in seed3 where clean accuracy drops severely. Therefore, 1-shot is useful for analyzing low-shot sensitivity, but it is not ideal as the main method-comparison setting.

The 2-shot ep10 setting is more suitable for the main experiment because it satisfies three conditions:

1. Clean accuracy does not collapse seriously.
2. New/unseen ASR is clearly lower than the 16-shot setting.
3. The ASR decrease is observed across all three seeds.

## 6. Conclusion

Caltech101 2-shot ep10 is selected as the main low-shot experimental setting for subsequent method improvement.

The key research question becomes:

Can we improve BadCLIP's low-shot cross-class backdoor generalization by enhancing the target margin induced by the shared image-side backdoor direction and the trigger-aware prompt branch?

This motivates the next method:

Shared Direction-Prompt Margin Amplification.
