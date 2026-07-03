import argparse
import os
import sys
from types import SimpleNamespace

import numpy as np
import torch
import torch.nn.functional as F

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backdoor_attack import setup_cfg
from trainers.badclip import BadClip


def build_args(cli_args):
    opts = [
        "DATASET.NUM_SHOTS", str(cli_args.num_shots),
        "DATASET.SUBSAMPLE_CLASSES", cli_args.subsample,
    ]

    return SimpleNamespace(
        root=cli_args.root,
        output_dir=cli_args.output_dir,
        resume="",
        seed=cli_args.seed,
        source_domains=None,
        target_domains=None,
        transforms=None,
        trainer="BadClip",
        backbone="",
        head="",
        dataset_config_file=cli_args.dataset_config_file,
        config_file=cli_args.config_file,
        model_dir=cli_args.model_dir,
        load_epoch=cli_args.load_epoch,
        eval_only=False,
        no_train=False,
        opts=opts,
    )


def unwrap_model(model):
    return model.module if hasattr(model, "module") else model


def parse_batch(trainer, batch):
    if hasattr(trainer, "parse_batch_test"):
        return trainer.parse_batch_test(batch)

    if isinstance(batch, dict):
        image = batch["img"].to(trainer.device)
        label = batch["label"].to(trainer.device)
        return image, label

    image, label = batch[0].to(trainer.device), batch[1].to(trainer.device)
    return image, label


@torch.no_grad()
def encode_image(model, image):
    feat = model.image_encoder(image.type(model.dtype))
    feat = feat / feat.norm(dim=-1, keepdim=True)
    return feat.float()


@torch.no_grad()
def logits_with_feature_and_prompt_source(model, image_features_for_logits, image_features_for_prompt):
    """
    image_features_for_logits:
      参与图文相似度计算的图像特征。

    image_features_for_prompt:
      输入 prompt learner 的图像特征，用来控制 prompt 来源。
    """
    tokenized_prompts = model.tokenized_prompts
    logit_scale = model.logit_scale.exp()

    prompt_input = image_features_for_prompt.type(model.dtype)
    logits_input = image_features_for_logits.type(model.dtype)

    prompts = model.prompt_learner(prompt_input)

    logits = []
    for pts_i, imf_i in zip(prompts, logits_input):
        text_features = model.text_encoder(pts_i, tokenized_prompts)
        text_features = text_features / text_features.norm(dim=-1, keepdim=True)
        l_i = logit_scale * imf_i @ text_features.t()
        logits.append(l_i.float())

    return torch.stack(logits, dim=0)


def mean_basis(delta_i):
    m = delta_i.mean(axis=0)
    m = m / (np.linalg.norm(m) + 1e-12)
    return m[:, None].astype("float32")


def keep_delta_by_basis(clean_feat, bd_feat, basis):
    """
    只保留 backdoor shift 在 basis 上的分量。
    """
    delta = bd_feat - clean_feat
    proj = delta @ basis @ basis.t()
    feat_kept = clean_feat + proj
    feat_kept = F.normalize(feat_kept, dim=-1, eps=1e-8)
    return feat_kept


def update_target_metrics(store, name, logits, label, target):
    pred = logits.argmax(dim=1)
    target_label = torch.zeros_like(label) + target
    target_correct = (pred == target_label).float()

    target_logits = logits[:, target]
    logits_without_target = logits.clone()
    logits_without_target[:, target] = -1e9
    max_non_target = logits_without_target.max(dim=1).values
    margin = target_logits - max_non_target

    store[name]["total"] += label.numel()
    store[name]["target_correct"] += target_correct.sum().item()
    store[name]["target_margin_sum"] += margin.sum().item()
    store[name]["target_logit_sum"] += target_logits.sum().item()


def init_store(method_names):
    return {
        name: {
            "total": 0,
            "target_correct": 0,
            "target_margin_sum": 0.0,
            "target_logit_sum": 0.0,
        }
        for name in method_names
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--model-dir", required=True)
    parser.add_argument("--subspace-npz", required=True)
    parser.add_argument("--load-epoch", type=int, default=10)
    parser.add_argument("--subsample", default="new", choices=["base", "new", "all"])
    parser.add_argument("--num-shots", type=int, default=16)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--max-batches", type=int, default=0)
    parser.add_argument("--out", required=True)

    parser.add_argument(
        "--dataset-config-file",
        default="configs/datasets/caltech101.yaml",
    )
    parser.add_argument(
        "--config-file",
        default="configs/trainers/BadClip/vit_b16_c4_ep10_batch1_ctxv1_init.yaml",
    )
    parser.add_argument(
        "--output-dir",
        default="output/analysis_prompt_ablation",
    )

    cli_args = parser.parse_args()
    os.makedirs(os.path.dirname(cli_args.out), exist_ok=True)

    print(f"Loading subspace source: {cli_args.subspace_npz}")
    subspace_data = np.load(cli_args.subspace_npz, allow_pickle=True)
    base_delta_i = subspace_data["delta_i"].astype("float32")

    args = build_args(cli_args)
    cfg = setup_cfg(args)

    print("Building BadClip trainer...")
    trainer = BadClip(cfg)

    print(f"Loading model from: {cli_args.model_dir}")
    trainer.load_model(cli_args.model_dir, epoch=cli_args.load_epoch)

    model = unwrap_model(trainer.model)
    model.eval()

    target = int(model.trigger.target)
    target_name = model.prompt_learner.classnames[target]

    print(f"Target index: {target}")
    print(f"Target name: {target_name}")
    print(f"Evaluate split: {cli_args.subsample}")

    mean_b = torch.from_numpy(mean_basis(base_delta_i)).to(trainer.device).float()

    method_names = [
        "clean_img_clean_prompt",
        "bd_img_bd_prompt",
        "bd_img_clean_prompt",
        "clean_img_bd_prompt",
        "keep_mean_bd_prompt",
        "keep_mean_clean_prompt",
    ]

    store = init_store(method_names)

    loader = trainer.test_loader

    for batch_idx, batch in enumerate(loader):
        if cli_args.max_batches > 0 and batch_idx >= cli_args.max_batches:
            break

        image, label = parse_batch(trainer, batch)
        image = image.to(trainer.device)
        label = label.to(trainer.device)

        clean_image = image
        bd_image = model.trigger(image.clone())

        clean_feat = encode_image(model, clean_image)
        bd_feat = encode_image(model, bd_image)
        keep_mean_feat = keep_delta_by_basis(clean_feat, bd_feat, mean_b)

        logits_clean_clean = logits_with_feature_and_prompt_source(
            model, clean_feat, clean_feat
        )
        logits_bd_bd = logits_with_feature_and_prompt_source(
            model, bd_feat, bd_feat
        )
        logits_bd_clean = logits_with_feature_and_prompt_source(
            model, bd_feat, clean_feat
        )
        logits_clean_bd = logits_with_feature_and_prompt_source(
            model, clean_feat, bd_feat
        )
        logits_keep_mean_bd = logits_with_feature_and_prompt_source(
            model, keep_mean_feat, bd_feat
        )
        logits_keep_mean_clean = logits_with_feature_and_prompt_source(
            model, keep_mean_feat, clean_feat
        )

        update_target_metrics(store, "clean_img_clean_prompt", logits_clean_clean, label, target)
        update_target_metrics(store, "bd_img_bd_prompt", logits_bd_bd, label, target)
        update_target_metrics(store, "bd_img_clean_prompt", logits_bd_clean, label, target)
        update_target_metrics(store, "clean_img_bd_prompt", logits_clean_bd, label, target)
        update_target_metrics(store, "keep_mean_bd_prompt", logits_keep_mean_bd, label, target)
        update_target_metrics(store, "keep_mean_clean_prompt", logits_keep_mean_clean, label, target)

        if (batch_idx + 1) % 5 == 0:
            print(f"Processed batches: {batch_idx + 1}")

    lines = []
    lines.append("# Prompt Branch Ablation Evaluation")
    lines.append("")
    lines.append(f"subsample: {cli_args.subsample}")
    lines.append(f"subspace_source: {cli_args.subspace_npz}")
    lines.append(f"target_index: {target}")
    lines.append(f"target_name: {target_name}")
    lines.append("")
    lines.append("## Target prediction rate under different image/prompt combinations")
    lines.append("method,target_rate,target_margin_mean,target_logit_mean,total")

    rows = []
    for name in method_names:
        total = store[name]["total"]
        target_rate = store[name]["target_correct"] / max(total, 1) * 100
        margin_mean = store[name]["target_margin_sum"] / max(total, 1)
        target_logit_mean = store[name]["target_logit_sum"] / max(total, 1)

        line = f"{name},{target_rate:.4f},{margin_mean:.6f},{target_logit_mean:.6f},{total}"
        lines.append(line)
        rows.append((name, target_rate, margin_mean, target_logit_mean, total))

    with open(cli_args.out, "w") as f:
        f.write("\n".join(lines))

    csv_path = cli_args.out.replace(".summary.txt", ".csv")
    with open(csv_path, "w") as f:
        f.write("method,target_rate,target_margin_mean,target_logit_mean,total\n")
        for name, target_rate, margin_mean, target_logit_mean, total in rows:
            f.write(f"{name},{target_rate:.4f},{margin_mean:.6f},{target_logit_mean:.6f},{total}\n")

    print("\n".join(lines))
    print("")
    print(f"Saved summary to: {cli_args.out}")
    print(f"Saved csv to: {csv_path}")


if __name__ == "__main__":
    main()
