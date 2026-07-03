# OxfordPets 2-shot ep10 Seed1 BadCLIP vs BadClipMargin Summary

## Setting

- Dataset: OxfordPets
- Shots: 2-shot
- Epochs: 10
- Seed: 1
- Baseline: BadCLIP
- Method: BadClipMargin
- lambda_margin: 0.2
- margin_m: 5.0

## Results

| Method | Base Clean ACC | Base ASR | New Clean ACC | New ASR |
|---|---:|---:|---:|---:|
| BadCLIP | 81.5% | 90.9% | 86.6% | 82.6% |
| BadClipMargin lambda=0.2,m=5.0 | 75.7% | 97.4% | 90.3% | 95.2% |

## Observation

BadClipMargin substantially improves new/unseen ASR on OxfordPets 2-shot ep10, increasing it from 82.6% to 95.2%. New clean accuracy also improves from 86.6% to 90.3%.

However, base clean accuracy drops from 81.5% to 75.7%, suggesting that the margin objective may affect base-class clean performance on OxfordPets. More seeds are needed to determine whether this is a stable trend or a seed-specific fluctuation.

## Next Step

Run seed2 and seed3 for both BadCLIP and BadClipMargin. If BadClipMargin consistently improves new ASR while base clean drops, then test a milder setting such as lambda=0.1,m=5.0.
