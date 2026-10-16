"""
数据集体检工具 —— 训练之前必须跑一遍。

训练报错里 80% 都是数据问题(路径、图片标签对不上、标签格式错),
但 pylov8 的报错信息通常含糊。先在这里查清楚,再开训练。

用法:
    python tools/audit_dataset.py
"""

import os
import sys
from collections import Counter

ROOT = "data/NEU-DET-yolo"
CLASS_NAMES = {0: "crazing", 1: "inclusion", 2: "patches",
               3: "pitted_surface", 4: "rolled-in_scale", 5: "scratches"}


def jpeg_size(path):
    """不依赖第三方库,直接从 JPEG 文件头读出 (宽, 高)。"""
    with open(path, "rb") as f:
        data = f.read()
    i = 2
    while i < len(data) - 9:
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker in (0xC0, 0xC1, 0xC2, 0xC3):
            h = int.from_bytes(data[i + 5:i + 7], "big")
            w = int.from_bytes(data[i + 7:i + 9], "big")
            return w, h
        if marker == 0xD8 or 0xD0 <= marker <= 0xD9:
            i += 2
            continue
        i += 2 + int.from_bytes(data[i + 2:i + 4], "big")
    return None


def pick(iterable, n=3):
    items = sorted(iterable)
    return items[:n]


def audit_split(root, split):
    idir = os.path.join(root, split, "images")
    ldir = os.path.join(root, split, "labels")
    if not os.path.isdir(idir) or not os.path.isdir(ldir):
        print(f"[{split}] 目录不存在: {idir} / {ldir}")
        return False

    imgs = {os.path.splitext(f)[0] for f in os.listdir(idir)}
    labs = {os.path.splitext(f)[0] for f in os.listdir(ldir)}

    print(f"[{split}]  图片 {len(imgs)} 张   标签 {len(labs)} 个")
    ok = True

    only_img, only_lab = imgs - labs, labs - imgs
    if only_img:
        ok = False
        print(f"  ✗ 有图无标签: {len(only_img)} 个,例如 {pick(only_img)}")
    if only_lab:
        ok = False
        print(f"  ✗ 有标签无图: {len(only_lab)} 个,例如 {pick(only_lab)}")
    if not only_img and not only_lab:
        print("  ✓ 图片与标签一一对应")

    lines_per_file = Counter()
    cls_counter = Counter()
    problems = []
    for name in os.listdir(ldir):
        raw = open(os.path.join(ldir, name)).read()
        lines = [ln for ln in raw.replace("\r", "").split("\n") if ln.strip()]
        lines_per_file[len(lines)] += 1
        for ln in lines:
            parts = ln.split()
            if len(parts) != 5:
                problems.append((name, f"字段数={len(parts)} 应为 5"))
                continue
            try:
                cid = int(parts[0])
                vals = [float(x) for x in parts[1:]]
            except ValueError:
                problems.append((name, "存在非数字"))
                continue
            cls_counter[cid] += 1
            if cid not in CLASS_NAMES:
                problems.append((name, f"类别编号越界 {cid}"))
            if any(v < 0 or v > 1 for v in vals):
                problems.append((name, f"坐标越界 {vals}"))
            if vals[2] <= 0 or vals[3] <= 0:
                problems.append((name, f"宽或高为 0 {vals}"))

    print(f"  每个标签文件的行数分布: {dict(sorted(lines_per_file.items()))}")
    print("  类别分布:")
    total = sum(cls_counter.values())
    for cid in sorted(cls_counter):
        n = cls_counter[cid]
        print(f"    {cid} {CLASS_NAMES.get(cid, '?'):<16} {n:>4} 个框  ({n / total * 100:5.1f}%)")

    if problems:
        ok = False
        print(f"  ✗ 异常 {len(problems)} 处,例如 {problems[:3]}")
    else:
        print("  ✓ 标签格式全部合法(每行 5 个字段 / 类别 0~5 / 坐标 0~1)")

    sample = os.listdir(idir)[:5]
    sizes = Counter(jpeg_size(os.path.join(idir, f)) for f in sample)
    print(f"  抽查 {len(sample)} 张图片尺寸: {dict(sizes)}")
    return ok


def main():
    if not os.path.isdir(ROOT):
        print(f"找不到 {ROOT} —— 请先按 tools/NEU-DET_下载说明.md 准备好数据集")
        return 1
    print(f"体检目录: {ROOT}\n")
    results = [audit_split(ROOT, s) for s in ("train", "test")]
    print()
    print("=" * 56)
    print("体检通过 ✓  可以开训练了" if all(results)
          else "发现问题 ✗  先修数据,别急着开训练")
    print("=" * 56)
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
