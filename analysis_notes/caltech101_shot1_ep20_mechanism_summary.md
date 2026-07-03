# Caltech101 1-shot ep20 Mechanism Summary

## 1. Baseline Performance

| Setting | Split | Clean ACC | ASR |
|---|---|---:|---:|
| 1-shot ep20 | base/seen | 96.3% | 98.2% |
| 1-shot ep20 | new/unseen | 92.8% | 90.5% |

Compared with 16-shot, the 1-shot setting substantially reduces unseen ASR while keeping clean accuracy stable.

## 2. Alignment Results

| Split | Align Mean | Target Attraction | Delta-I Norm | Delta-T Norm | PCA Top5 | Consistency |
|---|---:|---:|---:|---:|---:|---:|
| base/seen | 0.1280 | 0.1078 | 0.6475 | 0.4588 | 0.3247 | 0.8407 |
| new/unseen | 0.1384 | 0.0953 | 0.6150 | 0.4494 | 0.2891 | 0.8486 |

The shared direction remains stable, but the image-shift norm and target attraction are weaker than in the 16-shot setting.

## 3. Cross-split Direction Transfer

| Metric | Value |
|---|---:|
| cos(base image mean, new image mean) | 0.9894 |
| cos(base text mean, new text mean) | 0.9998 |
| new-to-base mean cosine | 0.8393 |
| new energy in base Top10 PCs | 0.3269 |
| Top10 subspace overlap | 0.6418 |

The shared backdoor direction transfers well from base classes to new classes.

## 4. Removal and Keep-only Results

| Original ASR | Remove Mean | Remove PCA10 | Remove Random10 | Keep Mean | Keep Mean+PCA10 | Keep Random10 |
|---:|---:|---:|---:|---:|---:|---:|
| 90.50% | 14.41% | 57.64% | 89.19% | 85.92% | 86.46% | 14.96% |

Removing the shared mean direction largely destroys the attack, while keeping only the mean direction recovers most of the attack success.

## 5. Prompt Ablation Results

| Method | Target Rate | Target Margin |
|---|---:|---:|
| clean_img_clean_prompt | 0.11% | -8.59 |
| bd_img_bd_prompt | 90.50% | 4.17 |
| bd_img_clean_prompt | 7.31% | -4.31 |
| clean_img_bd_prompt | 11.46% | -3.70 |
| keep_mean_bd_prompt | 85.92% | 3.23 |
| keep_mean_clean_prompt | 4.91% | -4.76 |

The image-side backdoor direction or the backdoor prompt alone is insufficient. The attack mainly arises from the interaction between the shared image-side backdoor direction and the trigger-aware prompt.

## 6. Conclusion

In the 1-shot ep20 setting, BadCLIP still learns a highly transferable shared backdoor direction. However, this direction alone is not sufficient under clean prompts. The attack relies on the synergy between the shared image-side direction and the trigger-aware prompt branch.

This suggests that improving low-shot BadCLIP should not only enforce direction consistency, but also strengthen the target margin induced by the shared direction and its amplification through the prompt branch.
