# 生成"假的"钢材表面示例图,给 day7(OpenCV-1)练习用。
# ⚠️ 这些图是【合成】的,不是真实数据。真实的 NEU-DET 图片在 10/11 才下载。
# 之所以先合成:① 保证今天一定能跑起来,不被网络卡住;② 缺陷位置/类型我自己控制,方便你对照。
#
# 真实 NEU-DET 图片尺寸就是 200x200 灰度图,所以这里也按 200x200 生成。

import os
import numpy as np
import cv2

OUT_DIR = os.path.join("practice", "demo_images")
os.makedirs(OUT_DIR, exist_ok=True)

rng = np.random.default_rng(42)  # 固定随机种子,保证每次生成的图一样


def steel_base(h=200, w=200, mean=115, streak=10):
    """造一张'钢板表面':底色 + 噪点 + 横向轧制纹路"""
    img = rng.normal(mean, 8, (h, w)).astype(np.float32)      # 底色 + 细噪点
    rows = np.sin(np.linspace(0, np.pi * 6, h))[:, None] * streak
    img = img + rows                                          # 横向条带(轧制留下的)
    img = cv2.GaussianBlur(img, (3, 3), 0)                    # 轻微平滑,更像真实表面
    return np.clip(img, 0, 255).astype(np.uint8)


def add_scratch(img, p1, p2, thickness=2, darken=55):
    """划痕:一条比周围暗的细线"""
    out = img.copy()
    cv2.line(out, p1, p2, int(np.clip(img.mean() - darken, 0, 255)), thickness, cv2.LINE_AA)
    out = cv2.GaussianBlur(out, (3, 3), 0)
    return out


def add_patch(img, center, axes, darken=35, angle=0):
    """斑块:一块比周围暗的椭圆区域"""
    out = img.copy()
    val = int(np.clip(img.mean() - darken, 0, 255))
    cv2.ellipse(out, center, axes, angle, 0, 360, val, -1)
    out = cv2.GaussianBlur(out, (5, 5), 0)
    return out


def add_pits(img, n=40, darken=45):
    """麻点:一堆又小又暗的点"""
    out = img.copy()
    val = int(np.clip(img.mean() - darken, 0, 255))
    xs = rng.integers(15, 185, n)
    ys = rng.integers(15, 185, n)
    for x, y in zip(xs, ys):
        cv2.circle(out, (int(x), int(y)), int(rng.integers(1, 3)), val, -1)
    out = cv2.GaussianBlur(out, (3, 3), 0)
    return out


def add_inclusion(img, n=12, darken=70):
    """夹杂:几处不规则的深色小块"""
    out = img.copy()
    val = int(np.clip(img.mean() - darken, 0, 255))
    xs = rng.integers(20, 180, n)
    ys = rng.integers(20, 180, n)
    for x, y in zip(xs, ys):
        axes = (int(rng.integers(3, 7)), int(rng.integers(2, 5)))
        cv2.ellipse(out, (int(x), int(y)), axes, int(rng.integers(0, 180)), 0, 360, val, -1)
    out = cv2.GaussianBlur(out, (5, 5), 0)
    return out


# ---------------- 五张图 ----------------
imgs = {}
imgs["clean"] = steel_base()
imgs["scratch"] = add_scratch(steel_base(), (30, 150), (175, 60), thickness=2)
imgs["patches"] = add_patch(steel_base(), (105, 95), (45, 30), angle=25)
imgs["pitted"] = add_pits(steel_base())
imgs["inclusion"] = add_inclusion(steel_base())

for name, im in imgs.items():
    cv2.imwrite(os.path.join(OUT_DIR, f"steel_{name}.png"), im)
    print(f"steel_{name}.png  shape={im.shape}  mean={im.mean():.1f}  min={im.min()}  max={im.max()}")

# ---------------- 一张彩色的(专门给"灰度化"用) ----------------
# 真实 NEU-DET 是灰度图,但你得先亲眼看见"彩色 -> 灰度"的变化,
# 所以额外造一张彩色工件图:蓝色金属底 + 棕色锈斑。
h = w = 200
color = np.zeros((h, w, 3), np.uint8)
color[:, :] = (170, 110, 60)                                  # BGR:偏蓝的金属色
color = np.clip(color.astype(np.float32) + rng.normal(0, 6, (h, w, 3)), 0, 255).astype(np.uint8)
cv2.circle(color, (70, 80), 35, (45, 70, 140), -1)            # BGR:棕色(锈斑)
cv2.line(color, (140, 20), (185, 175), (30, 40, 200), 3, cv2.LINE_AA)  # BGR:红色(划痕)
color = cv2.GaussianBlur(color, (3, 3), 0)
cv2.imwrite(os.path.join(OUT_DIR, "color_part.png"), color)
print(f"color_part.png    shape={color.shape}  (3 个数字 = 彩色)")

print("\n全部写入:", os.path.abspath(OUT_DIR))
