# Cross-dataset BadCLIP Mechanism Summary

## 1. Reproduction Results

| Dataset | Split | Clean ACC | ASR |
|---|---|---:|---:|
| Caltech101 | base/seen | 97.7% | 99.7% |
| Caltech101 | new/unseen | 93.7% | 99.3% |
| OxfordPets | base/seen | 93.8% | 99.3% |
| OxfordPets | new/unseen | 96.3% | 98.9% |

## 2. Backdoor Shift Analysis

| Dataset | Split | Samples | Target Attraction | PCA Top5 | Consistency |
|---|---|---:|---:|---:|---:|
| Caltech101 | base/seen | 1549 | 0.1481 | 0.3242 | 0.8378 |
| Caltech101 | new/unseen | 916 | 0.1466 | 0.2826 | 0.8469 |
| OxfordPets | base/seen | 1881 | 0.0393 | 0.4024 | 0.8040 |
| OxfordPets | new/unseen | 1788 | 0.0459 | 0.3957 | 0.8047 |

## 3. Cross-split Direction and Subspace Similarity

| Dataset | cos(base image mean, new image mean) | cos(base text mean, new text mean) | new-to-base mean cosine | new energy in base Top10 PCs | Top10 overlap |
|---|---:|---:|---:|---:|---:|
| Caltech101 | 0.9878 | 0.9986 | 0.8360 | 0.3042 | 0.6040 |
| OxfordPets | 0.9977 | 0.9999 | 0.8028 | 0.4893 | 0.9043 |

## 4. Subspace Removal Results

| Dataset | Split | Original ASR | Remove Mean | Remove Mean+PCA10 | Remove Random10 |
|---|---|---:|---:|---:|---:|
| Caltech101 | base/seen | 99.7418% | 17.5597% | 20.9167% | 99.7418% |
| Caltech101 | new/unseen | 99.3450% | 13.1004% | 19.8690% | 99.2358% |
| OxfordPets | base/seen | 99.2557% | 16.4806% | 11.5896% | 99.2026% |
| OxfordPets | new/unseen | 98.9374% | 12.8076% | 7.6622% | 98.8814% |

## 5. Subspace Keep-only Results

| Dataset | Split | Original ASR | Keep Mean | Keep Mean+PCA10 | Keep Random10 |
|---|---|---:|---:|---:|---:|
| Caltech101 | base/seen | 99.7418% | 98.5797% | 99.4835% | 11.8141% |
| Caltech101 | new/unseen | 99.3450% | 95.3057% | 96.6157% | 2.8384% |
| OxfordPets | base/seen | 99.2557% | 97.6608% | 99.4152% | 11.9617% |
| OxfordPets | new/unseen | 98.9374% | 97.0917% | 98.9933% | 7.8300% |

## 6. Prompt Branch Ablation

| Dataset | Split | bd_img+bd_prompt | bd_img+clean_prompt | clean_img+bd_prompt | keep_mean+bd_prompt | keep_mean+clean_prompt |
|---|---|---:|---:|---:|---:|---:|
| Caltech101 | base/seen | 99.7418% | 31.0523% | 11.1039% | 98.5797% | 13.1698% |
| Caltech101 | new/unseen | 99.3450% | 21.3974% | 2.6201% | 95.3057% | 4.4760% |
| OxfordPets | base/seen | 99.2557% | 95.7469% | 8.7719% | 97.6608% | 88.7294% |
| OxfordPets | new/unseen | 98.9374% | 91.8904% | 4.7539% | 97.0917% | 79.4743% |

## 7. Main Cross-dataset Observations

1. BadCLIP achieves high ASR on both Caltech101 and OxfordPets, including unseen classes.
2. In both datasets, trigger-induced image shifts are highly consistent across samples.
3. Base and new classes share nearly identical mean backdoor shift directions.
4. Removing the shared mean direction sharply reduces ASR on both seen and unseen classes.
5. Keeping only the shared mean direction is sufficient to recover high ASR.
6. Random directions do not show similar effects, indicating that the shared mean direction is a specific causal backdoor component.
7. The prompt branch amplifies target attraction, but its relative importance varies by dataset.
8. Caltech101 relies more strongly on the collaboration between shared image direction and backdoor prompt.
9. OxfordPets has a stronger image-side backdoor direction, while the prompt branch further boosts target confidence.

## 8. Refined Mechanism Claim

BadCLIP's cross-class backdoor generalization is mainly driven by a shared global backdoor direction in the CLIP image embedding space. This direction is learned from seen/base classes and transfers to unseen/new classes. It is necessary because removing it sharply reduces ASR, and it is nearly sufficient because keeping only this direction recovers high ASR. The trigger-aware prompt branch further adjusts the target-class text representation and amplifies target attraction, although the strength of this prompt-side contribution varies across datasets.

Refined idea name:

Shared Global Backdoor Direction with Trigger-Aware Prompt Amplification.
