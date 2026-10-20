"""Build the "one threshold cannot serve all classes" figure.

Three panels per defect class:
    original | Canny edges (50/150) | edges overlaid in red on the original

The point of the figure is the number, not the pretty picture: the same
threshold that lights up 38 % of a crazing image finds 236 pixels (0.6 %) on an
inclusion image. That measurement is the argument for a learned detector.

Run:  python tools/make_canny_figure.py
Out:  docs/figures/canny_threshold_problem.png
"""

from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
IMG_DIR = ROOT / "data" / "NEU-DET" / "IMAGES"
OUT = ROOT / "docs" / "figures" / "canny_threshold_problem.png"

CELL = 380
PAD = 22
TITLE_H = 64
LABEL_H = 56
LO, HI = 50, 150

CLASSES = [("crazing", "Crazing"), ("inclusion", "Inclusion")]


def panel_strip(gray: np.ndarray):
    """original | edges | edges drawn in red on the original"""
    edges = cv2.Canny(gray, LO, HI)

    original = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    edge_view = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    overlay = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    overlay[edges > 0] = (0, 0, 255)          # BGR red

    panels = []
    for p in (original, edge_view, overlay):
        if p.shape[0] != CELL:
            p = cv2.resize(p, (CELL, CELL), interpolation=cv2.INTER_LANCZOS4)
        panels.append(p)

    ratio = np.count_nonzero(edges) / edges.size
    return panels, np.count_nonzero(edges), ratio


def main() -> None:
    rows = []
    for cls, label in CLASSES:
        files = sorted(IMG_DIR.glob(f"{cls}_*.jpg"))
        if not files:
            raise SystemExit(f"找不到 {cls} 的图片,检查 {IMG_DIR}")
        gray = cv2.imread(str(files[0]), cv2.IMREAD_GRAYSCALE)
        panels, count, ratio = panel_strip(gray)
        rows.append((label, panels, count, ratio))
        print(f"{cls:12s} {count:6d} 个边缘像素 / {gray.size} = {ratio*100:.1f}%")

    n_cols = 3
    width = n_cols * CELL + (n_cols + 1) * PAD
    height = TITLE_H + len(rows) * (CELL + LABEL_H + PAD) + PAD

    canvas = np.full((height, width, 3), 255, np.uint8)

    cv2.putText(canvas, "One Canny threshold (50/150) on two defect classes",
                (PAD, 42), cv2.FONT_HERSHEY_SIMPLEX, 1.05, (25, 25, 25), 2, cv2.LINE_AA)

    for i, (label, panels, count, ratio) in enumerate(rows):
        y = TITLE_H + i * (CELL + LABEL_H + PAD)
        for j, p in enumerate(panels):
            x = PAD + j * (CELL + PAD)
            canvas[y:y + CELL, x:x + CELL] = p
            cv2.rectangle(canvas, (x, y), (x + CELL, y + CELL), (185, 185, 185), 1)

        caption = (f"{label}: {count:,} edge pixels = {ratio*100:.1f}% of the image")
        cv2.putText(canvas, caption, (PAD, y + CELL + 38),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.85, (30, 30, 200), 2, cv2.LINE_AA)

    cv2.putText(canvas, "original", (PAD + 8, TITLE_H - 8),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (110, 110, 110), 1, cv2.LINE_AA)
    cv2.putText(canvas, "Canny edges", (PAD + (CELL + PAD) + 8, TITLE_H - 8),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (110, 110, 110), 1, cv2.LINE_AA)
    cv2.putText(canvas, "edges in red", (PAD + 2 * (CELL + PAD) + 8, TITLE_H - 8),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (110, 110, 110), 1, cv2.LINE_AA)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(OUT), canvas)
    print(f"\n已生成: {OUT}  ({canvas.shape[1]}x{canvas.shape[0]})")


if __name__ == "__main__":
    main()
