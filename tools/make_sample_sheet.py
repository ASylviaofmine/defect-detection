"""生成一张"六类缺陷对照图":每类挑 1 张样本拼在一起,方便肉眼认缺陷。
数据来自 data/NEU-DET/IMAGES(官方 VOC 版)。

运行:
    python tools/make_sample_sheet.py                       # 默认 200px 单元、中文标签
    python tools/make_sample_sheet.py --cell 420 --lang en \
        --out docs/figures/six_classes.png                  # 录视频用的大图、英文标签
"""
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ap = argparse.ArgumentParser()
ap.add_argument("--cell", type=int, default=200, help="每张样本的边长(源图 200,放大用 LANCZOS)")
ap.add_argument("--lang", choices=["zh", "en"], default="zh", help="标签语言")
ap.add_argument("--out", default=None, help="输出路径,默认 tools/neu_det_samples.png")
args = ap.parse_args()

ROOT = Path(__file__).resolve().parent.parent
IMG_DIR = ROOT / "data" / "NEU-DET" / "IMAGES"
OUT = Path(args.out) if args.out else Path(__file__).resolve().parent / "neu_det_samples.png"
OUT = OUT if OUT.is_absolute() else ROOT / OUT

CLASSES = [
    ("crazing", "Crazing 裂纹", "Crazing"),
    ("inclusion", "Inclusion 夹杂", "Inclusion"),
    ("patches", "Patches 斑块", "Patches"),
    ("pitted_surface", "Pitted Surface 麻点", "Pitted surface"),
    ("rolled-in_scale", "Rolled-in Scale 氧化皮", "Rolled-in scale"),
    ("scratches", "Scratches 划痕", "Scratches"),
]

CELL = args.cell
PAD = max(12, CELL // 17)
LABEL_H = max(34, CELL // 6)
COLS = 3
LABEL_SIZE = max(18, CELL // 12)
TITLE_SIZE = max(22, CELL // 9)

# 尽量用中文字体,找不到就退回默认字体
FONT_PATH = None
for fp in [r"C:\Windows\Fonts\msyh.ttc", r"C:\Windows\Fonts\simhei.ttf"]:
    try:
        ImageFont.truetype(fp, 18)
        FONT_PATH = fp
        break
    except Exception:
        continue

def load(size):
    if FONT_PATH:
        return ImageFont.truetype(FONT_PATH, size)
    return ImageFont.load_default()

font = load(LABEL_SIZE)
tfont = load(TITLE_SIZE)

rows = (len(CLASSES) + COLS - 1) // COLS
W = COLS * CELL + (COLS + 1) * PAD
H = rows * (CELL + LABEL_H) + (rows + 1) * PAD + TITLE_SIZE + 18

sheet = Image.new("RGB", (W, H), (255, 255, 255))
draw = ImageDraw.Draw(sheet)

title = ("NEU-DET — six surface defect classes (200×200 greyscale)"
         if args.lang == "en" else "NEU-DET 六类钢材表面缺陷样本 (200x200)")
draw.text((PAD, 10), title, fill=(20, 20, 20), font=tfont)

for i, (cls, zh_label, en_label) in enumerate(CLASSES):
    # 找该类第一张图
    cands = sorted(IMG_DIR.glob(f"{cls}_*.jpg"))
    if not cands:
        print(f"[警告] 没找到 {cls} 的图片")
        continue
    img = Image.open(cands[0]).convert("RGB")
    if CELL != img.width:
        img = img.resize((CELL, CELL), Image.LANCZOS)
    r, c = divmod(i, COLS)
    x = PAD + c * (CELL + PAD)
    y = TITLE_SIZE + 18 + PAD + r * (CELL + LABEL_H + PAD)
    sheet.paste(img, (x, y))
    draw.rectangle([x, y, x + CELL - 1, y + CELL - 1], outline=(180, 180, 180))
    label = en_label if args.lang == "en" else zh_label
    draw.text((x + 2, y + CELL + LABEL_H // 5), label, fill=(180, 30, 30), font=font)
    print(f"  {cls:16s} <- {cands[0].name}")

OUT.parent.mkdir(parents=True, exist_ok=True)
sheet.save(OUT)
print(f"\n已生成: {OUT}  ({sheet.width}x{sheet.height})")
