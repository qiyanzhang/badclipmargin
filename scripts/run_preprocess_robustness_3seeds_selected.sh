#!/bin/bash
export CUDA_VISIBLE_DEVICES=${CUDA_VISIBLE_DEVICES:-0}

set -euo pipefail

cd "$(dirname "$0")/.."

DATA=/mnt/disk3/zhuangrenwei/zqy/badclip_exp/data
CFG=vit_b16_c4_ep10_batch1_ctxv1_init
SHOTS=2
LOAD_EPOCH=10
SUBSAMPLE=new
LOG_DIR=analysis_notes/preprocess_robustness_3seeds_selected
OUTPUT_ROOT=output/preprocess_robustness_3seeds_selected
SEEDS=(${SEED_LIST:-1 2 3})
PREPROCESS_LIST=("none" "color0.90" "blur0.5" "jpeg70" "resize0.95")

mkdir -p "${LOG_DIR}"
mkdir -p "${OUTPUT_ROOT}"

find_model_dir() {
    local dataset="$1"
    local trainer="$2"
    local preferred_dir="$3"
    local seed="$4"

    if [[ -d "${preferred_dir}" ]]; then
        echo "${preferred_dir}"
        return 0
    fi

    echo "[WARN] Preferred model dir not found: ${preferred_dir}"
    echo "[INFO] Candidate directories:"
    find output/train_seen -type d | grep -i "${dataset}" | grep -i "${trainer}" | grep "seed${seed}" || true
    return 1
}

run_eval() {
    local dataset="$1"
    local seed="$2"
    local trainer="$3"
    local method_tag="$4"
    local dataset_cfg="$5"
    local model_dir="$6"
    local preprocess="$7"
    local output_dir="$8"
    shift 8
    local -a env_args=("$@")

    local log_file="${LOG_DIR}/${dataset}_shot${SHOTS}_seed${seed}_${method_tag}_${preprocess}_test_unseen.run.log"

    if [[ -f "${log_file}" ]]; then
        echo "[SKIP] ${log_file}"
        return 0
    fi

    echo "[RUN] dataset=${dataset} seed=${seed} trainer=${trainer} preprocess=${preprocess}"

    env BADCLIP_PREPROCESS="${preprocess}" "${env_args[@]}" \
        python -m backdoor_attack \
        --root "${DATA}" \
        --seed "${seed}" \
        --trainer "${trainer}" \
        --dataset-config-file "${dataset_cfg}" \
        --config-file "configs/trainers/BadClip/${CFG}.yaml" \
        --output-dir "${output_dir}" \
        --model-dir "${model_dir}" \
        --load-epoch "${LOAD_EPOCH}" \
        --eval-only \
        DATASET.NUM_SHOTS "${SHOTS}" \
        DATASET.SUBSAMPLE_CLASSES "${SUBSAMPLE}" \
        2>&1 | tee "${log_file}"
}

for seed in "${SEEDS[@]}"; do
    caltech_badclip_dir="$(find_model_dir \
        "caltech101" \
        "BadClip" \
        "output/train_seen/caltech101/shots_2/BadClip/${CFG}/seed${seed}" \
        "${seed}" || true)"

    caltech_margin_dir="$(find_model_dir \
        "caltech101" \
        "BadClipMargin" \
        "output/train_seen/caltech101/shots_2/BadClipMargin/${CFG}_lm0.2_m5/seed${seed}" \
        "${seed}" || true)"

    food_badclip_dir="$(find_model_dir \
        "food101" \
        "BadClip" \
        "output/train_seen/food101/shots_2/BadClip/${CFG}/seed${seed}" \
        "${seed}" || true)"

    food_margin_dir="$(find_model_dir \
        "food101" \
        "BadClipMargin" \
        "output/train_seen/food101/shots_2/BadClipMargin/${CFG}_lm0.1_m5/seed${seed}" \
        "${seed}" || true)"

    for preprocess in "${PREPROCESS_LIST[@]}"; do
        if [[ -n "${caltech_badclip_dir}" ]]; then
            run_eval \
                "caltech101" \
                "${seed}" \
                "BadClip" \
                "badclip" \
                "configs/datasets/caltech101.yaml" \
                "${caltech_badclip_dir}" \
                "${preprocess}" \
                "${OUTPUT_ROOT}/caltech101/shots_${SHOTS}/BadClip/${CFG}/seed${seed}/${preprocess}"
        fi

        if [[ -n "${caltech_margin_dir}" ]]; then
            run_eval \
                "caltech101" \
                "${seed}" \
                "BadClipMargin" \
                "badclipmargin_lm0.2_m5" \
                "configs/datasets/caltech101.yaml" \
                "${caltech_margin_dir}" \
                "${preprocess}" \
                "${OUTPUT_ROOT}/caltech101/shots_${SHOTS}/BadClipMargin/${CFG}_lm0.2_m5/seed${seed}/${preprocess}" \
                "BADCLIP_MARGIN_LAMBDA=0.2" \
                "BADCLIP_MARGIN_M=5.0"
        fi

        if [[ -n "${food_badclip_dir}" ]]; then
            run_eval \
                "food101" \
                "${seed}" \
                "BadClip" \
                "badclip" \
                "configs/datasets/food101.yaml" \
                "${food_badclip_dir}" \
                "${preprocess}" \
                "${OUTPUT_ROOT}/food101/shots_${SHOTS}/BadClip/${CFG}/seed${seed}/${preprocess}"
        fi

        if [[ -n "${food_margin_dir}" ]]; then
            run_eval \
                "food101" \
                "${seed}" \
                "BadClipMargin" \
                "badclipmargin_lm0.1_m5" \
                "configs/datasets/food101.yaml" \
                "${food_margin_dir}" \
                "${preprocess}" \
                "${OUTPUT_ROOT}/food101/shots_${SHOTS}/BadClipMargin/${CFG}_lm0.1_m5/seed${seed}/${preprocess}" \
                "BADCLIP_MARGIN_LAMBDA=0.1" \
                "BADCLIP_MARGIN_M=5.0"
        fi
    done
done
