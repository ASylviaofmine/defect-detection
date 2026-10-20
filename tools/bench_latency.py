"""Measure model size and single-image inference latency for the three trained runs.

Produces the deployment-characterisation table quoted in README section 4.6.

    python tools/bench_latency.py

Everything is measured on this machine: an RTX 4060 Laptop (8 GB) plus its
desktop CPU. Nothing here says anything about production edge hardware.

Method, so the numbers are reproducible and honestly labelled:

* every model is loaded and warmed up *before* any timing starts -- otherwise
  the first model in the list silently pays for CUDA context creation and
  cuDNN kernel autotuning, and reports a latency several times its true value,
* the loops are interleaved (round-robin over the three models) rather than
  run one model to completion then the next, so laptop power/thermal drift
  hits every run equally instead of only the last one,
* GPU timing brackets each call with cuda.synchronize(), since CUDA launches
  are asynchronous and `time.perf_counter()` alone would measure nothing,
* the reported figure is the median, not the mean -- a single OS hiccup
  otherwise moves the mean by tens of percent on a 50 ms operation.
"""

from __future__ import annotations

import statistics
import time
from pathlib import Path

import torch
import cv2
from ultralytics import YOLO

ROOT = Path(__file__).resolve().parent.parent

RUNS = [
    ("A", "yolov8n", 640, ROOT / "runs/detect/yolov8n_baseline/weights/best.pt"),
    ("B", "yolov8s", 640, ROOT / "runs/detect/yolov8s_640/weights/best.pt"),
    ("C", "yolov8n", 960, ROOT / "runs/detect/yolov8n_960/weights/best.pt"),
]

SAMPLE = ROOT / "docs/samples/scratches_271.jpg"
WARMUP = 8
ROUNDS_GPU = 30
ROUNDS_CPU = 8
BATCH = 8
ROUNDS_THROUGHPUT = 15


def one_call(model: YOLO, image, imgsz: int, device: str) -> float:
    """Time a single inference, in milliseconds."""
    if device == "0" and torch.cuda.is_available():
        torch.cuda.synchronize()
    t0 = time.perf_counter()
    model(image, imgsz=imgsz, device=device, verbose=False)
    if device == "0" and torch.cuda.is_available():
        torch.cuda.synchronize()
    return (time.perf_counter() - t0) * 1000


def bench(models, image, device: str, rounds: int) -> list[float]:
    """Round-robin over models so power/thermal drift is shared, not concentrated."""
    for _ in range(WARMUP):
        for _, _, imgsz, model in models:
            one_call(model, image, imgsz, device)

    samples = {tag: [] for tag, _, _, _ in models}
    for _ in range(rounds):
        for tag, _, imgsz, model in models:
            samples[tag].append(one_call(model, image, imgsz, device))
    return [statistics.median(samples[tag]) for tag, _, _, _ in models]


def bench_throughput(models, image, rounds: int) -> list[float]:
    """Batch throughput in images/second on the GPU (isolates model compute).

    Single-image latency on a desktop GPU is dominated by fixed Python, letterbox
    and NMS overhead, so two backbones of very different size land within noise
    of each other. A batch of BATCH images amortises that overhead and exposes
    the compute difference.
    """
    batch = [image] * BATCH
    for _ in range(3):
        for _, _, imgsz, model in models:
            model(batch, imgsz=imgsz, device="0", verbose=False)

    samples = {tag: [] for tag, _, _, _ in models}
    for _ in range(rounds):
        for tag, _, imgsz, model in models:
            torch.cuda.synchronize()
            t0 = time.perf_counter()
            model(batch, imgsz=imgsz, device="0", verbose=False)
            torch.cuda.synchronize()
            samples[tag].append((time.perf_counter() - t0) / BATCH)
    return [1.0 / statistics.median(samples[tag]) for tag, _, _, _ in models]


def main() -> None:
    if not SAMPLE.exists():
        raise SystemExit(f"sample image missing: {SAMPLE}")
    image = cv2.imread(str(SAMPLE))
    if image is None:
        raise SystemExit(f"could not read {SAMPLE}")

    print("Loading all checkpoints first, so no model pays a one-off CUDA cost ...")
    models = []
    for tag, name, imgsz, weight in RUNS:
        if not weight.exists():
            print(f"  {tag} MISSING {weight}")
            continue
        models.append((tag, name, imgsz, YOLO(str(weight))))
    if not models:
        raise SystemExit("no checkpoints found -- run training first")

    gpu_ok = torch.cuda.is_available()
    print(f"GPU available: {gpu_ok}"
          + (f"  ({torch.cuda.get_device_name(0)})" if gpu_ok else "  -- GPU column skipped"))
    print(f"CPU threads: {torch.get_num_threads()}")
    print()

    gpu_ms = bench(models, image, "0", ROUNDS_GPU) if gpu_ok else [float("nan")] * len(models)
    cpu_ms = bench(models, image, "cpu", ROUNDS_CPU)
    fps = bench_throughput(models, image, ROUNDS_THROUGHPUT) if gpu_ok else [float("nan")] * len(models)

    header = (f"{'Run':<4}{'Model':<10}{'imgsz':>6}{'Params':>10}{'Size':>9}"
              f"{'GPU ms':>9}{'CPU ms':>9}{'img/s b' + str(BATCH):>10}")
    print(header)
    print("-" * len(header))

    rows = []
    for (tag, name, imgsz, model), g_ms, c_ms, f in zip(models, gpu_ms, cpu_ms, fps):
        params = sum(p.numel() for p in model.model.parameters())
        weight = next(w for t, _, _, w in RUNS if t == tag)
        size_mb = weight.stat().st_size / 1024 / 1024
        print(f"{tag:<4}{name:<10}{imgsz:>6}{params / 1e6:>9.2f}M{size_mb:>8.1f}M"
              f"{g_ms:>9.1f}{c_ms:>9.1f}{f:>10.1f}")
        rows.append((tag, name, imgsz, params, size_mb, g_ms, c_ms, f))

    print()
    print("Sanity checks (these must hold, otherwise the measurement is suspect):")
    by_tag = {r[0]: r for r in rows}
    if "A" in by_tag and "B" in by_tag:
        a, b = by_tag["A"], by_tag["B"]
        print(f"  params      yolov8n {a[3] / 1e6:.2f}M < yolov8s {b[3] / 1e6:.2f}M  -> "
              f"{'OK' if a[3] < b[3] else 'SUSPECT'}")
        print(f"  CPU latency yolov8n {a[6]:.1f} < yolov8s {b[6]:.1f} ms     -> "
              f"{'OK, n is faster' if a[6] < b[6] else 'SUSPECT, n should be faster'}")
        print(f"  GPU batch-1 yolov8n {a[5]:.1f} vs yolov8s {b[5]:.1f} ms   -> "
              f"{'within noise, as expected (overhead-dominated)' if abs(a[5] - b[5]) < 0.3 * max(a[5], b[5]) else 'n and s differ more than expected'}")
        print(f"  GPU throughput yolov8n {a[7]:.1f} vs yolov8s {b[7]:.1f} img/s -> "
              f"{'OK, n is faster' if a[7] > b[7] else 'SUSPECT, n should be faster'}")
    if "A" in by_tag and "C" in by_tag:
        a, c = by_tag["A"], by_tag["C"]
        print(f"  yolov8n@640 vs @960 GPU latency: {a[5]:.1f} vs {c[5]:.1f} ms -> "
              f"{'OK, 960 is slower' if c[5] > a[5] else 'SUSPECT, 960 should be slower'}")

    print()
    print("Markdown for README section 4.6:")
    print()
    print("| Run | Model | imgsz | Params | Weight file | Latency, GPU (batch 1) | "
          f"Latency, CPU (batch 1) | Throughput, GPU (batch {BATCH}) |")
    print("| --- | ----- | ----- | ------ | ----------- | ---------------------- | "
          "---------------------- | -------------------------------- |")
    for tag, name, imgsz, params, size_mb, g_ms, c_ms, f in rows:
        gpu = f"{g_ms:.1f} ms" if g_ms == g_ms else "n/a"
        tput = f"{f:.0f} img/s" if f == f else "n/a"
        print(f"| {tag} | `{name}` | {imgsz} | {params / 1e6:.2f} M | "
              f"{size_mb:.1f} MB | {gpu} | {c_ms:.1f} ms | {tput} |")


if __name__ == "__main__":
    main()
