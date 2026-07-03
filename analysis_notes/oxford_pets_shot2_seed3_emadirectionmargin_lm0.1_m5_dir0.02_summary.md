# OxfordPets 2-shot ep10 BadClipEMADirectionMargin lambda_dir=0.02 Seed3 Summary

## Setting

- Dataset: OxfordPets
- Shots: 2-shot
- Epochs: 10
- Seed: 3
- Method: BadClipEMADirectionMargin
- lambda_margin: 0.1
- margin_m: 5.0
- lambda_dir: 0.02
- dir_ema_momentum: 0.99

## Result Comparison

| Method | Base Clean ACC | Base ASR | New Clean ACC | New ASR |
|---|---:|---:|---:|---:|
| Fixed BadClipMargin lambda=0.1,m=5.0 | 88.2% | 97.2% | 93.7% | 94.2% |
| BadClipEMADirectionMargin lambda_dir=0.05 | 86.5% | 98.2% | 87.3% | 94.1% |
| BadClipEMADirectionMargin lambda_dir=0.02 | 85.8% | 98.7% | 82.4% | 97.8% |

## Observation

The EMA direction loss is active and no longer close to zero, indicating that the cross-batch shared direction constraint works under the batch-size-1 setting.

However, reducing lambda_dir from 0.05 to 0.02 does not recover new clean accuracy. Instead, it further increases new ASR while decreasing new clean accuracy.

This suggests that EMA shared-direction alignment strengthens the backdoor direction, but it may also over-attract unseen clean samples toward the target class.

## Conclusion

EMA shared-direction margin is useful as a mechanism validation: stronger shared direction leads to stronger ASR.

However, it is not suitable as the final main method because it hurts unseen clean accuracy.

The final main method should remain fixed BadClipMargin, while EMA direction can be reported as an exploratory mechanism-driven variant.
