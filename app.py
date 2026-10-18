"""Steel surface defect detection — Gradio web demo.

Fine-tuned YOLOv8s on NEU-DET (6 classes), mAP@50 = 0.766.

Run from the repository root:

    python app.py

Then open http://127.0.0.1:7860

Note: the web page is served by *this* Python process. Closing the terminal
(or Ctrl+C) takes the page down; run `python app.py` again to bring it back.
"""

import cv2
import gradio as gr
from pathlib import Path
from ultralytics import YOLO

# ---------------------------------------------------------------------------
# Paths -- resolved from this file, so the demo works no matter which
# directory python is started from. (Relative paths are resolved against the
# *current working directory*, not the script's location -- that difference
# caused a "data.yaml does not exist" error earlier in this project.)
# ---------------------------------------------------------------------------
ROOT = Path(__file__).parent
WEIGHT = ROOT / "runs" / "detect" / "yolov8s_640" / "weights" / "best.pt"
SAMPLES = ROOT / "docs" / "samples"

assert WEIGHT.exists(), f"权重不存在: {WEIGHT}\n请先在仓库根目录执行训练,或检查路径。"

# Loaded once at import time. If this were inside the callback, every click
# would re-read 22 MB from disk (~2-3 s) before doing any work.
model = YOLO(str(WEIGHT))

CLASS_ZH = {
    "crazing": "裂纹",
    "inclusion": "夹杂",
    "patches": "斑块",
    "pitted_surface": "麻点",
    "rolled-in_scale": "氧化皮压入",
    "scratches": "划痕",
}


def detect(image, conf):
    """Run detection and return (annotated RGB image, one-line summary).

    Args:
        image: RGB uint8 array from Gradio (H, W, 3)
        conf:  minimum confidence, 0.05-0.95
    """
    if image is None:
        raise gr.Error("请先上传一张图片,或点下方示例图。")

    # Gradio hands us RGB; OpenCV and Ultralytics expect BGR. Skipping this
    # does not raise -- it silently swaps the red and blue channels, which the
    # model tolerates poorly and the output looks wrong.
    bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    result = model(bgr, conf=conf, verbose=False)[0]
    boxes = result.boxes
    n = len(boxes)

    if n == 0:
        summary = f"未检测到缺陷(conf ≥ {conf:.2f})"
    else:
        counts = {}
        for cls_id in boxes.cls:
            name = result.names[int(cls_id)]
            counts[name] = counts.get(name, 0) + 1
        detail = " · ".join(
            f"{CLASS_ZH.get(k, k)} × {v}" for k, v in sorted(counts.items(), key=lambda kv: -kv[1])
        )
        summary = f"检测到 {n} 个缺陷框 — {detail}"

    # result.plot() returns a BGR image with boxes drawn on it.
    annotated = result.plot()
    return cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB), summary


demo = gr.Interface(
    fn=detect,
    inputs=[
        gr.Image(type="numpy", label="上传缺陷图片 (Upload)", height=320),
        gr.Slider(minimum=0.05, maximum=0.95, value=0.25, step=0.05,
                  label="置信度阈值 (confidence threshold)"),
    ],
    outputs=[
        gr.Image(type="numpy", label="检测结果 (Detection)", height=320),
        gr.Textbox(label="统计 (Summary)"),
    ],
    examples=[
        [str(SAMPLES / "crazing_271.jpg"), 0.25],
        [str(SAMPLES / "scratches_271.jpg"), 0.25],
        [str(SAMPLES / "inclusion_271.jpg"), 0.25],
    ],
    title="钢材表面缺陷检测 / Steel Surface Defect Detection",
    description=(
        "YOLOv8s fine-tuned on NEU-DET · 6 classes · mAP@50 **0.766** · "
        "trained on 1620 images in 52 min (RTX 4060 Laptop). "
        "Drag a 200×200 greyscale strip image in, or click an example below."
    ),
    flagging_mode="never",
)

if __name__ == "__main__":
    demo.launch()
