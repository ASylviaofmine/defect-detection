"""生成一张"六类缺陷对照图":每类挑 1 张样本拼在一起,方便肉眼认缺陷。
数据来自 data/NEU-DET/IMAGES(官方 VOC 版)。
运行: python tools/make_sample_sheet.py
输出: tools/neu_det_samples.png
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
IMG_DIR = ROOT / "data" / "NEU-DET" / "IMAGES"
OUT = Path(__file__).resolve().parent / "neu_det_samples.png"

CLASSES = [
    ("crazing", "Crazing 裂纹"),
    ("inclusion", "Inclusion 夹杂"),
    ("patches", "Patches 斑块"),
    ("pitted_surface", "Pitted Surface 麻点"),
    ("rolled-in_scale", "Rolled-in Scale 氧化皮"),
    ("scratches", "Scratches 划痕"),
]

CELL = 200      # 图片本身 200x200
PAD = 12
LABEL_H = 34
COLS = 3

# 尽量用中文字体,找不到就退回默认字体
font = None
for fp in [r"C:\Windows\Fonts\msyh.ttc", r"C:\Windows\Fonts\simhei.ttf"]:
    try:
        font = ImageFont.truetype(fp, 18)
        break
    except Exception:
        continue
if font is None:
    font = ImageFont.load_default()

rows = (len(CLASSES) + COLS - 1) // COLS
W = COLS * CELL + (COLS + 1) * PAD
H = rows * (CELL + LABEL_H) + (rows + 1) * PAD + 40

sheet = Image.new("RGB", (W, H), (255, 255, 255))
draw = ImageDraw.Draw(sheet)

title = "NEU-DET 六类钢材表面缺陷样本 (200x200)"
try:
    tfont = ImageFont.truetype(r"C:\Windows\Fonts\msyh.ttc", 22)
except Exception:
    tfont = font
draw.text((PAD, 10), title, fill=(20, 20, 20), font=tfont)

for i, (cls, label) in enumerate(CLASSES):
    # 找该类第一张图
    cands = sorted(IMG_DIR.glob(f"{cls}_*.jpg"))
    if not cands:
        print(f"[警告] 没找到 {cls} 的图片")
        continue
    img = Image.open(cands[0]).convert("RGB")
    r, c = divmod(i, COLS)
    x = PAD + c * (CELL + PAD)
    y = 40 + PAD + r * (CELL + LABEL_H + PAD)
    sheet.paste(img, (x, y))
    draw.rectangle([x, y, x + CELL - 1, y + CELL - 1], outline=(180, 180, 180))
    draw.text((x + 2, y + CELL + 6), label, fill=(180, 30, 30), font=font)
    print(f"  {cls:16s} <- {cands[0].name}")

sheet.save(OUT)
print(f"\n已生成: {OUT}  ({sheet.width}x{sheet.height})")
