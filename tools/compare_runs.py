# -*- coding: utf-8 -*-
"""
对比多个训练实验的结果,输出一张 markdown 对比表。

AI 辅助脚本(见 README §8 的 AI 使用声明)。

用法(在 defect_detection 目录下):
    python tools/compare_runs.py yolov8n_baseline yolov8s_640 yolov8n_960

它会做三件事:
  1. 从每个实验的 results.csv 里读出:最佳轮次、mAP50、mAP50-95、P、R、总耗时
  2. 用每个实验的 weights/best.pt 在验证集上重跑一次评估,拿到【每一类】的 AP
  3. 打印一张 markdown 表,并保存到 runs/compare_report.md

为什么要单独写这个脚本?
  训练日志里的 results.csv 只有"总体指标",没有"每一类"。
  但要判断调参有没有治好 crazing,必须看 crazing 那一类的 AP/召回 ——
  所以只能拿 best.pt 重新评估一次。
"""
import csv
import sys
from pathlib import Path

RUNS_DIR = Path("runs/detect")


def read_results_csv(run_dir):
    """从 results.csv 读出总体指标(取 mAP50 最高那一轮,和 best.pt 对应)。"""
    rows = list(csv.DictReader(open(run_dir / "results.csv", encoding="utf-8")))
    if not rows:
        return None
    best = max(rows, key=lambda r: float(r["metrics/mAP50(B)"]))
    return {
        "epoch": int(best["epoch"]),
        "mAP50": float(best["metrics/mAP50(B)"]),
        "mAP50-95": float(best["metrics/mAP50-95(B)"]),
        "P": float(best["metrics/precision(B)"]),
        "R": float(best["metrics/recall(B)"]),
        "minutes": float(rows[-1]["time"]) / 60,
        "seconds_per_epoch": float(rows[-1]["time"]) / len(rows),
    }


def read_args(run_dir):
    """从 args.yaml 里读出这组实验用的模型和 imgsz(方便填表)。"""
    info = {"model": "-", "imgsz": "-", "epochs": "-"}
    p = run_dir / "args.yaml"
    if not p.exists():
        return info
    for line in p.read_text(encoding="utf-8").splitlines():
        for k in info:
            if line.startswith(f"{k}:"):
                info[k] = line.split(":", 1)[1].strip().strip("'")
    return info


def main(run_names):
    from ultralytics import YOLO  # 放在函数里,只有真要评估时才耗时导入

    rows = []
    per_class = {}
    names = None

    for run in run_names:
        run_dir = RUNS_DIR / run
        if not (run_dir / "weights" / "best.pt").exists():
            print(f"[跳过] {run}:找不到 weights/best.pt")
            continue

        args = read_args(run_dir)
        stats = read_results_csv(run_dir)

        # 用 best.pt 在验证集上重新评估一次,拿每一类的指标
        model = YOLO(str(run_dir / "weights" / "best.pt"))
        m = model.val(data="data/NEU-DET-yolo/data.yaml", split="val",
                      device=0, verbose=False)
        names = m.names
        per_class[run] = {
            "ap50": list(m.box.ap50),
            "p": list(m.box.p),
            "r": list(m.box.r),
        }

        rows.append((run, args, stats))
        print(f"[完成] {run}: mAP50={stats['mAP50']:.3f} 用时 {stats['minutes']:.1f} 分钟")

    if not rows:
        print("没有任何可对比的实验。")
        return

    lines = []
    lines.append("# 训练实验对比\n")
    lines.append(f"对比实验数:{len(rows)}\n")

    lines.append("## 总体指标(取每组实验 mAP50 最高的那一轮)\n")
    lines.append("| 实验 | 模型 | imgsz | 最佳轮次 | mAP@50 | mAP@50-95 | Precision | Recall | 总耗时 | 秒/轮 |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for run, args, s in rows:
        lines.append(
            f"| `{run}` | {args['model']} | {args['imgsz']} | {s['epoch']} | "
            f"**{s['mAP50']:.3f}** | {s['mAP50-95']:.3f} | {s['P']:.3f} | {s['R']:.3f} | "
            f"{s['minutes']:.1f} min | {s['seconds_per_epoch']:.1f} |"
        )

    key = "crazing"
    idx = [i for i, n in (names or {}).items() if n == key]
    if idx:
        i = idx[0]
        lines.append(f"\n## 重点类别 `{key}` 的对比(今天的靶子)\n")
        lines.append("| 实验 | AP@50 | Precision | Recall |")
        lines.append("| --- | --- | --- | --- |")
        for run, _, _ in rows:
            d = per_class[run]
            lines.append(f"| `{run}` | **{d['ap50'][i]:.3f}** | {d['p'][i]:.3f} | {d['r'][i]:.3f} |")

    lines.append("\n## 六类 AP@50 全表\n")
    header = "| 实验 | " + " | ".join(names[i] for i in sorted(names)) + " |"
    lines.append(header)
    lines.append("| --- " * (len(names) + 1) + "|")
    for run, _, _ in rows:
        cells = " | ".join(f"{v:.3f}" for v in per_class[run]["ap50"])
        lines.append(f"| `{run}` | {cells} |")

    report = "\n".join(lines)
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    out = RUNS_DIR / "compare_report.md"
    out.write_text(report, encoding="utf-8")

    print("\n" + report)
    print(f"\n已保存到 {out}")


if __name__ == "__main__":
    main(sys.argv[1:] or ["yolov8n_baseline"])
