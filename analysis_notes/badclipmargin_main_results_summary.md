# BadClipMargin Main Experimental Results Summary

## 1. Method

BadClipMargin adds a target-margin amplification loss to the original BadCLIP objective.

The goal is to make the target-class logit of backdoored images exceed the largest non-target logit by a sufficient margin. This encourages the shared backdoor direction to cross the target decision boundary more stably, especially under low-shot settings.

## 2. Caltech101 2-shot ep10 Results

| Method | Margin Setting | Base Clean Avg | Base ASR Avg | New Clean Avg | New ASR Avg |
|---|---|---:|---:|---:|---:|
| BadCLIP | - | 95.43% | 98.27% | 91.10% | 93.17% |
| BadClipMargin | lambda=0.2,m=5.0 | 96.77% | 99.70% | 94.13% | 98.70% |

## 3. OxfordPets 2-shot ep10 Results

| Method | Margin Setting | Base Clean Avg | Base ASR Avg | New Clean Avg | New ASR Avg |
|---|---|---:|---:|---:|---:|
| BadCLIP | - | 84.23% | 95.07% | 87.03% | 90.63% |
| BadClipMargin | lambda=0.1,m=5.0 | 83.83% | 97.03% | 91.53% | 94.63% |

## 4. Main Observations

BadClipMargin improves low-shot new-class ASR on both Caltech101 and OxfordPets.

On Caltech101, lambda=0.2,m=5.0 provides the best clean-ASR trade-off.

On OxfordPets, lambda=0.2,m=5.0 is too strong and hurts clean accuracy, while lambda=0.1,m=5.0 provides a better trade-off.

This indicates that the margin objective is effective across datasets, but the optimal strength is dataset-sensitive.

## 5. Mechanism Summary

Mechanism analyses on both datasets show that BadClipMargin preserves the shared image-side backdoor direction learned by BadCLIP.

Removing the mean direction almost disables the attack, while keeping only the mean direction preserves most of the ASR.

Compared with BadCLIP, BadClipMargin increases target attraction and target margin, showing that it strengthens the target-discriminative ability of the shared backdoor direction rather than creating a new attack mechanism.

## 6. Current Conclusion

BadClipMargin addresses the low-shot bottleneck of BadCLIP by amplifying the target-boundary crossing ability of the shared image-side backdoor direction.

It improves low-shot cross-class backdoor generalization while maintaining a reasonable clean-ASR trade-off.
