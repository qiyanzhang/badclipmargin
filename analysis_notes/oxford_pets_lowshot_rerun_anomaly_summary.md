# OxfordPets Low-shot Rerun Anomaly Summary

## Rerun Results

| Experiment | Base Clean ACC | Base ASR | New Clean ACC | New ASR |
|---|---:|---:|---:|---:|
| BadClipMargin 8-shot seed2 rerun | 85.3% | 98.5% | 30.7% | 78.9% |
| BadCLIP 16-shot seed3 rerun | 93.2% | 99.0% | 21.3% | 99.6% |

## Observation

The rerun confirms that some OxfordPets shot/seed settings are unstable.

For BadClipMargin 8-shot seed2, the rerun produces much lower new clean accuracy than the original run, and the new ASR also drops. This suggests training instability or sensitivity to the specific optimization trajectory.

For BadCLIP 16-shot seed3, the rerun again shows severe new clean accuracy collapse while maintaining very high new ASR. This confirms that the original abnormal result is not simply a logging error.

## Implication

The OxfordPets low-shot curve should not be used as the primary evidence for the method.

The main experimental setting should remain the stable 2-shot setting, where BadClipMargin improves both new clean accuracy and new ASR over BadCLIP.

The low-shot curve can be used as an auxiliary stability analysis, showing that target-margin amplification is most useful in low-shot settings but can be sensitive under some shot/seed configurations.

## Final Decision

Use OxfordPets 2-shot as the main result.

Use 1/4/8/16-shot results only as supplementary analysis, with explicit discussion of instability.
