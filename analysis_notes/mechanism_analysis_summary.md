# BadCLIP Mechanism Analysis Summary

## 1. Reproduction Results

| Split | Clean ACC | ASR |
|---|---:|---:|
| base/seen | 97.7% | 99.7% |
| new/unseen | 93.7% | 99.3% |

## 2. Backdoor Shift Analysis

| Split | Samples | Align Mean | Target Attraction | Delta I Norm | Delta T Norm | PCA Top3 | PCA Top5 | Consistency |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| base/seen | 1549 | 0.1082 | 0.1481 | 0.8083 | 0.7218 | 0.2501 | 0.3242 | 0.8378 |
| new/unseen | 916 | 0.0990 | 0.1466 | 0.7638 | 0.7175 | 0.1998 | 0.2826 | 0.8469 |

## 3. Cross-split Subspace Analysis

| Metric | Value |
|---|---:|
| cos(base_image_mean_dir, new_image_mean_dir) | 0.9878 |
| cos(base_text_mean_dir, new_text_mean_dir) | 0.9986 |
| new_delta_i cosine to base_image_mean_dir | 0.8360 |
| base_delta_i cosine to new_image_mean_dir | 0.8289 |
| new energy in base Top10 PCs | 0.3042 |
| base-new Top10 subspace overlap | 0.6040 |

## 4. Subspace Removal Results

| Split | Original ASR | Remove Mean | Remove PCA10 | Remove Random10 |
|---|---:|---:|---:|---:|
| base/seen | 99.7418% | 17.5597% | 97.4177% | 99.7418% |
| new/unseen | 99.3450% | 13.1004% | 97.1616% | 99.2358% |

## 5. Subspace Keep-only Results

| Split | Original ASR | Keep Mean | Keep PCA10 | Keep Mean+PCA10 | Keep Random10 |
|---|---:|---:|---:|---:|---:|
| base/seen | 99.7418% | 98.5797% | 49.1930% | 99.4835% | 11.8141% |
| new/unseen | 99.3450% | 95.3057% | 16.2664% | 96.6157% | 2.8384% |

## 6. Prompt Branch Ablation

| Split | clean_img+clean_prompt | bd_img+bd_prompt | bd_img+clean_prompt | clean_img+bd_prompt | keep_mean+bd_prompt | keep_mean+clean_prompt |
|---|---:|---:|---:|---:|---:|---:|
| base/seen | 8.3925% | 99.7418% | 31.0523% | 11.1039% | 98.5797% | 13.1698% |
| new/unseen | 0.0000% | 99.3450% | 21.3974% | 2.6201% | 95.3057% | 4.4760% |

## 7. Main Observations

1. BadCLIP induces highly consistent image-feature shifts across samples.
2. The mean backdoor shift directions on base and new classes are almost identical.
3. Removing the shared mean backdoor direction causes ASR to drop sharply on both base and new classes.
4. Keeping only the shared mean backdoor direction is sufficient to recover high ASR.
5. Random directions do not show similar effects, indicating that the shared mean direction is a specific causal backdoor component.
6. The trigger-aware prompt branch is also necessary: keeping the mean direction with clean prompt leads to low target rate, while keeping the mean direction with backdoor prompt recovers high target rate.
7. Therefore, BadCLIP's attack is driven by the collaboration between a shared global image-side backdoor direction and a trigger-aware prompt-side target alignment.

## 8. Current Conclusion

BadCLIP's cross-class backdoor generalization is mainly driven by a shared global backdoor direction in the CLIP image embedding space. This direction is learned from base classes but transfers to unseen classes. It is necessary because removing it sharply reduces ASR, and it is nearly sufficient because keeping only this direction can recover high ASR. However, the direction must cooperate with the trigger-aware backdoor prompt; otherwise, the attack effect is much weaker.

A more accurate framing of the idea is:

Shared Global Backdoor Direction with Trigger-Aware Prompt Amplification.

中文表述为：

带有触发器感知 Prompt 放大的全局共享后门方向。
