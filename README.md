# 基于深度学习的工业工件表面缺陷检测系统

基于 YOLOv11 与 OpenCV 的钢材表面缺陷检测,提供 Gradio 网页演示界面。

数据集:NEU-DET(东北大学钢材表面缺陷数据集,6 类缺陷)

## 项目结构

```
defect_detection/
├── practice/          # 第 1~4 天 Python 基础练习(day1.py ~ day4.py)
├── data/              # 数据集(不入库,见 .gitignore)
├── scripts/           # 数据集转换、训练、评估脚本
├── app.py             # Gradio 网页演示(第 17 天创建)
└── requirements.txt   # 依赖清单
```

## 快速开始

```bash
pip install -r requirements.txt
```

## 进度

- [ ] Day 1~4:Python 基础(practice/)
- [ ] Day 5~8:OpenCV 图像处理
- [ ] Day 9~16:YOLO 模型训练
- [ ] Day 17~20:Gradio 演示
- [ ] Day 21~25:文档与收尾
