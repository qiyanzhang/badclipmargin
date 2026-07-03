# OxfordPets 2-shot ep10 BadClipEMADirectionMargin Seed3 Summary

## Setting

- Dataset: OxfordPets
- Shots: 2-shot
- Epochs: 10
- Seed: 3
- Method: BadClipEMADirectionMargin
- lambda_margin: 0.1
- margin_m: 5.0
- lambda_dir: 0.05
- dir_ema_momentum: 0.99

## Result Comparison

| Method | Base Clean ACC | Base ASR | New Clean ACC | New ASR |
|---|---:|---:|---:|---:|
| Fixed BadClipMargin lambda=0.1,m=5.0 | 88.2% | 97.2% | 93.7% | 94.2% |
| Batch-level BadClipDirectionMargin | 86.8% | 98.6% | 80.4% | 96.8% |
| BadClipEMADirectionMargin lambda_dir=0.05 | 86.5% | 98.2% | 87.3% | 94.1% |

## Observation

The EMA direction loss is no longer close to zero, which confirms that the EMA shared direction constraint is active under the batch-size-1 setting.

Compared with batch-level direction loss, EMA direction substantially improves new clean accuracy.

However, compared with the fixed BadClipMargin lambda=0.1 baseline, EMA direction still hurts new clean accuracy while providing almost no new ASR gain.

## Conclusion

EMA shared direction is a valid mechanism, but lambda_dir=0.05 is too strong for OxfordPets seed3.

Next, test a weaker direction weight:

lambda_dir = 0.02
