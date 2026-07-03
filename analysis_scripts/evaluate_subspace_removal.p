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
def logits_with_given_image_features(model, image_features_for_logits, image_features_for_prompt):
    """
    用指定的 image feature 算 logits。

    image_features_for_logits:
      真正参与图文相似度计算的图像特征。

    image_features_for_prompt:
      输入 prompt learner 的图像特征。
      这里我们默认用 backdoor image feature，保持 BadCLIP 的 trigger-aware prompt 响应不变。
    """
    tokenized_prompts = model.tokenized_prompts
    logit_scale = model.logit_scale.exp()

    prompts = model.prompt_learner(image_features_for_prompt)

    logits = []
    for pts_i, imf_i in zip(prompts, image_features_for_logits):
        text_features = model.text_encoder(pts_i, tokenized_prompts)
        text_features = text_features / text_features.norm(dim=-1, keepdim=True)
        l_i = logit_scale * imf_i @ text_features.t()
        logits.append(l_i.float())

    logits = torch.stack(logits, dim=0)
    return logits


def pca_basis(delta_i, k):
    x = delta_i - delta_i.mean(axis=0, keepdims=True)
    _, _, vh = np.linalg.svd(x, full_matrices=False)
    return vh[:k].T.astype("float32")


def mean_basis(delta_i):
    m = delta_i.mean(axis=0)
    m = m / (np.linalg.norm(m) + 1e-12)
    return m[:, None].astype("float32")


def random_basis(dim, k, seed=1):
    rng = np.random.default_rng(seed)
    a = rng.normal(size=(dim, k)).astype("float32")
    q, _ = np.linalg.qr(a)
    return q[:, :k].astype("float32")


def ablate_delta_by_basis(clean_feat, bd_feat, basis):
    """
    只去掉 backdoor shift delta_i 在 basis 上的分量：
      delta_i = f(x+trigger) - f(x)
      delta_i_removed = delta_i - Proj_basis(delta_i)
      f_removed = normalize(f(x) + delta_i_removed)

    这样比直接从 f(x+trigger) 上去掉方向更合理，
    因为我们只消除 trigger 引入的漂移分量，而尽量保留原图语义。
    """
    delta = bd_feat - clean_feat
    proj = delta @ basis @ basis.t()
    delta_removed = delta - proj
    feat_removed = clean_feat + delta_removed
    feat_removed = F.normalize(feat_removed, dim=-1, eps=1e-8)
    return feat_removed


def update_metrics(store, name, logits, label, target):
    pred = logits.argmax(dim=1)

    target_label = torch.zeros_like(label) + target
    correct_target = (pred == target_label).float()

    target_logits = logits[:, target]
    logits_without_target = logits.clone()
    logits_without_target[:, target] = -1e9
    max_non_target = logits_without_target.max(dim=1).values
    margin = target_logits - max_non_target

    store[name]["total"] += label.numel()
    store[name]["target_correct"] += correct_target.sum().item()
    store[name]["target_margin_sum"] += margin.sum().item()
    store[name]["target_logit_sum"] += target_logits.sum().item()


def update_clean_metrics(store, logits, label):
    pred = logits.argmax(dim=1)
    correct = (pred == label).float()
    store["clean"]["total"] += label.numel()
    store["clean"]["correct"] += correct.sum().item()


def init_store(method_names):
    store = {
        "clean": {
            "total": 0,
            "correct": 0,
        }
    }

    for name in method_names:
        store[name] = {
            "total": 0,
            "target_correct": 0,
            "target_margin_sum": 0.0,
            "target_logit_sum": 0.0,
        }

    return store


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
        default="output/analysis_subspace_removal",
    )

    cli_args = parser.parse_args()
    os.makedirs(os.path.dirname(cli_args.out), exist_ok=True)

    print(f"Loading subspace source: {cli_args.subspace_npz}")
    subspace_data = np.load(cli_args.subspace_npz, allow_pickle=True)
    base_delta_i = subspace_data["delta_i"].astype("float32")
    dim = base_delta_i.shape[1]

    basis_np = {
        "remove_mean": mean_basis(base_delta_i),
        "remove_pca1": pca_basis(base_delta_i, 1),
        "remove_pca3": pca_basis(base_delta_i, 3),
        "remove_pca5": pca_basis(base_delta_i, 5),
        "remove_pca10": pca_basis(base_delta_i, 10),
        "remove_random1": random_basis(dim, 1, seed=cli_args.seed),
        "remove_random3": random_basis(dim, 3, seed=cli_args.seed),
        "remove_random5": random_basis(dim, 5, seed=cli_args.seed),
        "remove_random10": random_basis(dim, 10, seed=cli_args.seed),
    }

    method_names = ["original_backdoor"] + list(basis_np.keys())

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

    basis_torch = {
        name: torch.from_numpy(basis).to(trainer.device).float()
        for name, basis in basis_np.items()
    }

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

        # 干净分类 sanity check
        clean_logits = logits_with_given_image_features(
            model,
            clean_feat,
            clean_feat,
        )
        update_clean_metrics(store, clean_logits, label)

        # 原始后门 ASR sanity check
        original_bd_logits = logits_with_given_image_features(
            model,
            bd_feat,
            bd_feat,
        )
        update_metrics(store, "original_backdoor", original_bd_logits, label, target)

        # 子空间去除后再分类
        for name, basis in basis_torch.items():
            removed_feat = ablate_delta_by_basis(clean_feat, bd_feat, basis)

            # 这里 prompt 仍然使用 bd_feat，隔离“图像侧后门漂移子空间”的作用
            removed_logits = logits_with_given_image_features(
                model,
                removed_feat,
                bd_feat,
            )
            update_metrics(store, name, removed_logits, label, target)

        if (batch_idx + 1) % 5 == 0:
            print(f"Processed batches: {batch_idx + 1}")

    lines = []
    lines.append("# Backdoor Subspace Removal Evaluation")
    lines.append("")
    lines.append(f"subsample: {cli_args.subsample}")
    lines.append(f"subspace_source: {cli_args.subspace_npz}")
    lines.append(f"target_index: {target}")
    lines.append(f"target_name: {target_name}")
    lines.append("")

    clean_total = store["clean"]["total"]
    clean_acc = store["clean"]["correct"] / max(clean_total, 1) * 100
    lines.append("## Clean sanity check")
    lines.append(f"clean_total: {clean_total}")
    lines.append(f"clean_acc: {clean_acc:.4f}")
    lines.append("")

    lines.append("## Backdoor ASR after removing image-shift subspace")
    lines.append("method,ASR,target_margin_mean,target_logit_mean,total")

    result_rows = []
    for name in method_names:
        total = store[name]["total"]
        asr = store[name]["target_correct"] / max(total, 1) * 100
        margin_mean = store[name]["target_margin_sum"] / max(total, 1)
        target_logit_mean = store[name]["target_logit_sum"] / max(total, 1)

        line = f"{name},{asr:.4f},{margin_mean:.6f},{target_logit_mean:.6f},{total}"
        lines.append(line)
        result_rows.append((name, asr, margin_mean, target_logit_mean, total))

    with open(cli_args.out, "w") as f:
        f.write("\n".join(lines))

    csv_path = cli_args.out.replace(".summary.txt", ".csv")
    with open(csv_path, "w") as f:
        f.write("method,ASR,target_margin_mean,target_logit_mean,total\n")
        for name, asr, margin_mean, target_logit_mean, total in result_rows:
            f.write(f"{name},{asr:.4f},{margin_mean:.6f},{target_logit_mean:.6f},{total}\n")

    print("\n".join(lines))
    print("")
    print(f"Saved summary to: {cli_args.out}")
    print(f"Saved csv to: {csv_path}")


if __name__ == "__main__":
    main()

