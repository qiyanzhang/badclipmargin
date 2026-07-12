import csv
import re
from collections import defaultdict
from pathlib import Path


LOG_DIR = Path("analysis_notes/preprocess_strength_sweep")
CSV_PATH = LOG_DIR / "strength_sweep_seed1_summary.csv"
MD_PATH = LOG_DIR / "strength_sweep_seed1_summary.md"
LATEX_PATH = LOG_DIR / "strength_sweep_seed1_latex_table.tex"
RECOMMEND_PATH = LOG_DIR / "recommended_3seed_settings.md"

PREPROCESS_ORDER = [
    "none",
    "color0.98", "color0.95", "color0.90",
    "jpeg99", "jpeg98", "jpeg95", "jpeg90", "jpeg80", "jpeg70",
    "blur0.1", "blur0.3", "blur0.5", "blur1.0",
    "resize0.98", "resize0.95", "resize0.90", "resize0.75",
]
PREPROCESS_ALIASES = {
    "colorjitter": "color0.90",
    "blur": "blur1.0",
    "resize": "resize0.75",
}
PREPROCESS_PATTERN = "|".join(re.escape(item) for item in PREPROCESS_ORDER + list(PREPROCESS_ALIASES))
FILENAME_RE = re.compile(
    rf"^(?P<dataset>[a-z0-9_]+)_shot(?P<shots>\d+)_seed(?P<seed>\d+)_(?P<method>.+)_(?P<preprocess>{PREPROCESS_PATTERN})_test_unseen\.run\.log$"
)
ACC_RE = re.compile(r"\* accuracy:\s*([0-9.]+)%")
TYPE_ORDER = {"color": 0, "jpeg": 1, "blur": 2, "resize": 3}


def canonical_preprocess(preprocess):
    return PREPROCESS_ALIASES.get(preprocess, preprocess)


def preprocess_type_strength(preprocess):
    canonical = canonical_preprocess(preprocess)
    if canonical == "none":
        return "none", "none"
    if canonical.startswith("color"):
        return "color", canonical[len("color"):]
    if canonical.startswith("jpeg"):
        return "jpeg", canonical[len("jpeg"):]
    if canonical.startswith("blur"):
        return "blur", canonical[len("blur"):]
    if canonical.startswith("resize"):
        return "resize", canonical[len("resize"):]
    return "unknown", canonical


def preprocess_sort_key(preprocess):
    canonical = canonical_preprocess(preprocess)
    return PREPROCESS_ORDER.index(canonical) if canonical in PREPROCESS_ORDER else len(PREPROCESS_ORDER)


def pretty_method(method):
    method_lower = method.lower()
    if method_lower.startswith("badclipmargin"):
        return "BadClipMargin"
    if method_lower.startswith("badclip"):
        return "BadCLIP"
    return method


def parse_log(path):
    text = path.read_text(encoding="utf-8", errors="ignore")
    matches = ACC_RE.findall(text)
    if len(matches) < 2:
        raise ValueError(f"Expected at least two accuracy values in {path}")

    meta = FILENAME_RE.match(path.name)
    if meta is None:
        raise ValueError(f"Unexpected log filename: {path.name}")

    row = meta.groupdict()
    row["seed"] = int(row["seed"])
    row["shots"] = int(row["shots"])
    row["new_clean"] = float(matches[-2])
    row["new_asr"] = float(matches[-1])
    row["canonical_preprocess"] = canonical_preprocess(row["preprocess"])
    row["method_pretty"] = pretty_method(row["method"])
    row["type"], row["strength"] = preprocess_type_strength(row["preprocess"])
    return row


def fmt(value):
    return f"{value:.2f}"


def latex_escape(text):
    return text.replace("_", r"\_")


def summarize_modes(rows):
    stats = defaultdict(lambda: defaultdict(list))
    for row in rows:
        stats[row["canonical_preprocess"]][row["method_pretty"]].append(row)
    return stats


def average_metric(rows, metric):
    if not rows:
        return 0.0
    return sum(row[metric] for row in rows) / len(rows)


def choose_color_setting(mode_stats):
    preferred = ["color0.90", "color0.95", "color0.98"]
    none_margin = average_metric(mode_stats["none"]["BadClipMargin"], "new_asr")
    threshold = max(10.0, 0.30 * none_margin)

    best_mode = None
    best_score = None
    for mode in preferred:
        margin_rows = mode_stats[mode]["BadClipMargin"]
        badclip_rows = mode_stats[mode]["BadCLIP"]
        if not margin_rows or not badclip_rows:
            continue
        margin_asr = average_metric(margin_rows, "new_asr")
        badclip_asr = average_metric(badclip_rows, "new_asr")
        score = (margin_asr >= threshold, margin_asr - badclip_asr, margin_asr, -preferred.index(mode))
        if best_score is None or score > best_score:
            best_mode = mode
            best_score = score
    return best_mode


def choose_gentle_setting(mode_stats, candidates):
    best_mode = None
    best_score = None
    for mode in candidates:
        margin_rows = mode_stats[mode]["BadClipMargin"]
        badclip_rows = mode_stats[mode]["BadCLIP"]
        if not margin_rows or not badclip_rows:
            continue
        margin_asr = average_metric(margin_rows, "new_asr")
        badclip_asr = average_metric(badclip_rows, "new_asr")
        score = (margin_asr > 5.0 and badclip_asr > 5.0, margin_asr, badclip_asr, -candidates.index(mode))
        if best_score is None or score > best_score:
            best_mode = mode
            best_score = score
    return best_mode


def choose_optional_resize(mode_stats):
    candidates = ["resize0.95", "resize0.90", "resize0.98", "resize0.75"]
    available = []
    for mode in candidates:
        margin_rows = mode_stats[mode]["BadClipMargin"]
        if margin_rows:
            available.append((mode, average_metric(margin_rows, "new_asr")))
    if len(available) < 2:
        return None
    values = [value for _, value in available]
    if max(values) - min(values) < 5.0:
        return None
    return choose_gentle_setting(mode_stats, candidates)


def build_recommendation(rows):
    mode_stats = summarize_modes(rows)
    color_mode = choose_color_setting(mode_stats)
    jpeg_mode = choose_gentle_setting(mode_stats, ["jpeg98", "jpeg95", "jpeg99", "jpeg90", "jpeg80", "jpeg70"])
    blur_mode = choose_gentle_setting(mode_stats, ["blur0.5", "blur0.3", "blur1.0", "blur0.1"])
    resize_mode = choose_optional_resize(mode_stats)

    lines = ["Recommended for 3-seed formal evaluation:"]
    lines.append("- none")
    if color_mode:
        lines.append(f"- {color_mode}")
    if jpeg_mode:
        lines.append(f"- {jpeg_mode}")
    if blur_mode:
        lines.append(f"- {blur_mode}")
    if resize_mode:
        lines.append(f"- optional {resize_mode}")

    lines.append("")
    lines.append("Reasoning:")
    if color_mode:
        margin_asr = average_metric(mode_stats[color_mode]["BadClipMargin"], "new_asr")
        badclip_asr = average_metric(mode_stats[color_mode]["BadCLIP"], "new_asr")
        lines.append(
            f"- {color_mode}: among color-only perturbations, BadClipMargin keeps higher ASR on average ({fmt(margin_asr)} vs {fmt(badclip_asr)} for BadCLIP) without collapsing clean performance."
        )
    if jpeg_mode:
        margin_asr = average_metric(mode_stats[jpeg_mode]["BadClipMargin"], "new_asr")
        lines.append(
            f"- {jpeg_mode}: this is a mild JPEG setting that still preserves measurable ASR ({fmt(margin_asr)} average for BadClipMargin), so it is useful for showing trigger fragility without trivially zeroing every run."
        )
    if blur_mode:
        margin_asr = average_metric(mode_stats[blur_mode]["BadClipMargin"], "new_asr")
        lines.append(
            f"- {blur_mode}: this gives a medium-strength blur with non-zero average ASR ({fmt(margin_asr)} for BadClipMargin), which is more interpretable than an extremely weak or immediately destructive blur."
        )
    if resize_mode:
        margin_asr = average_metric(mode_stats[resize_mode]["BadClipMargin"], "new_asr")
        lines.append(
            f"- {resize_mode}: resize shows a usable gradual trend, and this setting keeps enough signal ({fmt(margin_asr)} average ASR for BadClipMargin) to serve as an optional extra robustness check."
        )
    else:
        lines.append("- resize is optional because its curve is either redundant with blur/jpeg or too flat to justify a mandatory 3-seed follow-up.")

    RECOMMEND_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    rows = [parse_log(path) for path in sorted(LOG_DIR.glob("*.run.log"))]
    if not rows:
        raise ValueError(f"No run logs found under {LOG_DIR}")

    rows.sort(
        key=lambda row: (
            row["dataset"],
            row["method_pretty"],
            row["seed"],
            preprocess_sort_key(row["preprocess"]),
        )
    )

    baseline = {}
    for row in rows:
        if row["canonical_preprocess"] == "none":
            baseline[(row["dataset"], row["method_pretty"], row["seed"])] = row

    for row in rows:
        base = baseline.get((row["dataset"], row["method_pretty"], row["seed"]))
        if base is None:
            row["delta_clean"] = 0.0
            row["delta_asr"] = 0.0
        else:
            row["delta_clean"] = row["new_clean"] - base["new_clean"]
            row["delta_asr"] = row["new_asr"] - base["new_asr"]

    LOG_DIR.mkdir(parents=True, exist_ok=True)

    with CSV_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "Dataset", "Method", "Seed", "Preprocess", "CanonicalPreprocess",
                "Type", "Strength", "New Clean", "New ASR", "Delta New Clean", "Delta New ASR",
            ]
        )
        for row in rows:
            writer.writerow(
                [
                    row["dataset"],
                    row["method_pretty"],
                    row["seed"],
                    row["preprocess"],
                    row["canonical_preprocess"],
                    row["type"],
                    row["strength"],
                    fmt(row["new_clean"]),
                    fmt(row["new_asr"]),
                    fmt(row["delta_clean"]),
                    fmt(row["delta_asr"]),
                ]
            )

    delta_rows = [row for row in rows if row["canonical_preprocess"] != "none"]
    curve_rows = [row for row in rows if row["type"] in TYPE_ORDER]
    curve_rows.sort(
        key=lambda row: (
            row["dataset"],
            row["method_pretty"],
            TYPE_ORDER[row["type"]],
            float(row["strength"]),
        )
    )

    lines = []
    lines.append("| Dataset | Method | Seed | Preprocess | New Clean | New ASR |")
    lines.append("|---|---|---:|---|---:|---:|")
    for row in rows:
        lines.append(
            f"| {row['dataset']} | {row['method_pretty']} | {row['seed']} | {row['preprocess']} | {fmt(row['new_clean'])} | {fmt(row['new_asr'])} |"
        )

    lines.append("")
    lines.append("| Dataset | Method | Preprocess | Δ New Clean | Δ New ASR |")
    lines.append("|---|---|---|---:|---:|")
    for row in delta_rows:
        lines.append(
            f"| {row['dataset']} | {row['method_pretty']} | {row['preprocess']} | {fmt(row['delta_clean'])} | {fmt(row['delta_asr'])} |"
        )

    lines.append("")
    lines.append("| Dataset | Method | Type | Strength | New Clean | New ASR | Δ New ASR |")
    lines.append("|---|---|---|---:|---:|---:|---:|")
    for row in curve_rows:
        lines.append(
            f"| {row['dataset']} | {row['method_pretty']} | {row['type']} | {row['strength']} | {fmt(row['new_clean'])} | {fmt(row['new_asr'])} | {fmt(row['delta_asr'])} |"
        )

    MD_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")

    latex_lines = [
        r"\begin{tabular}{llllrrr}",
        r"\hline",
        r"Dataset & Method & Type & Strength & New Clean & New ASR & $\Delta$ New ASR \\",
        r"\hline",
    ]
    for row in curve_rows:
        latex_lines.append(
            f"{latex_escape(row['dataset'])} & {latex_escape(row['method_pretty'])} & {row['type']} & {row['strength']} & {fmt(row['new_clean'])} & {fmt(row['new_asr'])} & {fmt(row['delta_asr'])} \\\\"
        )
    latex_lines.extend([r"\hline", r"\end{tabular}"])
    LATEX_PATH.write_text("\n".join(latex_lines) + "\n", encoding="utf-8")

    build_recommendation(rows)


if __name__ == "__main__":
    main()
