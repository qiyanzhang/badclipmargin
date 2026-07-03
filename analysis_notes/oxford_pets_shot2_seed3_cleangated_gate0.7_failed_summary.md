# OxfordPets 2-shot ep10 Clean-Gated gate=0.7 Seed3 Summary

## Setting

- Dataset: OxfordPets
- Shots: 2-shot
- Epochs: 10
- Seed: 3
- Method: BadClipCleanGatedMargin
- lambda_min: 0.0
- lambda_max: 0.2
- margin_m: 5.0
- margin_scale: 2.0
- warmup_epochs: 3
- clean_gate_threshold: 0.7
- clean_gate_temp: 0.5

## Result Comparison

| Method | Base Clean ACC | Base ASR | New Clean ACC | New ASR |
|---|---:|---:|---:|---:|
| Fixed BadClipMargin lambda=0.1,m=5.0 | 88.2% | 97.2% | 93.7% | 94.2% |
| Clean-Gated threshold=1.0 | 87.0% | 97.4% | 77.7% | 96.0% |
| Clean-Gated threshold=0.7 | 82.8% | 98.2% | 77.0% | 90.5% |

## Observation

Lowering clean_gate_threshold from 1.0 to 0.7 does not recover new clean accuracy on seed3. It also reduces new ASR.

This suggests that clean gating based only on training clean loss is not sufficient to preserve unseen-class clean accuracy.

## Next Step

Move to a direct clean-preserving margin design:

- Backdoored images should have target-class logit larger than non-target logits.
- Clean images should have their true-class logit larger than the target-class logit.

This directly prevents clean samples from being overly attracted to the target class.
