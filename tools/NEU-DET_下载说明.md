# NEU-DET 数据集 —— 下载与结构说明

> 记录时间:2026-10-09。数据集**不入库**(`data/` 在 .gitignore 里),换电脑时按本文档重新获取即可。

## 一、这是什么

**NEU-DET**(东北大学热轧带钢表面缺陷数据库)—— 钢材表面缺陷检测的经典公开基准集。

- 规模:**1800 张**灰度图,200×200 像素,**6 类**缺陷,**每类 300 张**
- 标注:Pascal VOC 格式 XML(bounding box),标明每个缺陷的类别与位置
- 六类缺陷:

| 序号 | 英文名 | 中文 | 说明 |
|---|---|---|---|
| 0 | crazing | 裂纹 | 表面龟裂的细网状纹路 |
| 1 | inclusion | 夹杂 | 钢中夹带异物形成的条块 |
| 2 | patches | 斑块 | 成片的颜色不均区域 |
| 3 | pitted_surface | 麻点 | 密集的小坑点 |
| 4 | rolled-in_scale | 氧化铁皮压入 | 氧化皮被轧进表面 |
| 5 | scratches | 划痕 | 直线状的刮伤 |

引用(申请材料里可写):
> K. Song, Y. Yan, "A noise robust method based on completed local binary patterns for hot-rolled steel strip surface defects", *Applied Surface Science*, vol. 285, pp. 858–864, 2013.

## 二、本地已有的两份(2026-10-09 已下好)

`defect_detection/data/` 下:

```
data/
├── NEU-DET/                       ← 【主用】官方原版,VOC 格式
│   ├── IMAGES/        1800 张 .jpg (200x200 灰度)
│   └── ANNOTATIONS/   1800 个 .xml (VOC 标注)
│
└── NEU-DET-yolo/                  ← 【兜底/对照】别人已转好的 YOLO 格式
    ├── train/images/  1620 张
    ├── train/labels/  1620 个 .txt (YOLO: 类别 cx cy w h,均为 0~1)
    ├── test/images/   180 张
    ├── test/labels/   180 个 .txt
    └── data.yaml      已写好,可直接用于 ultralytics 训练
```

- **主用 `NEU-DET/`**:10/11 统计各类缺陷数量、10/13 自己写脚本把 XML 转成 YOLO,都基于它。
- **兜底 `NEU-DET-yolo/`**:万一 10/13 的转换脚本卡住,可以直接用它开始训练,不耽误进度。

> 说明:官方原仓库把每类 5 张(共 30 张)单独放在 Validation 目录里,已合并回 `IMAGES/` / `ANNOTATIONS/`,凑齐官方完整的 1800 张。

## 三、来源

| 用途 | 来源仓库 | 备注 |
|---|---|---|
| VOC 原版 | `github.com/SprAJR/NEU-DET-Steel-Surface-Defect-Detection` | 从该仓库取 `IMAGES/` + `ANNOTATIONS/` |
| YOLO 版 | `github.com/Marfbin/NEU-DET-with-yolov8` | 从该仓库取 `data/NEU-DET/` |

官方发布页(备用,需 Google Drive 或百度网盘,提取码 `pmqx`):
http://faculty.neu.edu.cn/songkechen/zh_CN/zdylm/263270/list/index.htm

## 四、如需重新下载

```bash
cd defect_detection/data
mkdir -p _src && cd _src

# 1) VOC 原版(只取需要的目录,不拉整个仓库)
git clone --depth 1 --filter=blob:none --sparse \
  https://github.com/SprAJR/NEU-DET-Steel-Surface-Defect-Detection.git voc
cd voc && git sparse-checkout set IMAGES ANNOTATIONS Validation_Images Validation_Annotations && cd ..

# 2) YOLO 版
git clone --depth 1 --filter=blob:none --sparse \
  https://github.com/Marfbin/NEU-DET-with-yolov8.git yolo
cd yolo && git sparse-checkout set data && cd ..
```

下完后按上面「二」的目录结构整理,并把 `Validation_*` 合并进 `IMAGES/`、`ANNOTATIONS/`。
