# ==============================================================
# day012 · YOLO-3   读懂训练结果 + 用 best.pt 推理
# ==============================================================
# 2026-10-15   建议总时长:约 2.5 小时(不含推送)
#
# 【昨天的成果,先摆在这里】
#   训练已完成:100 轮,26.3 分钟,best mAP50 = 0.758(第 85 轮)
#   产物在 runs/detect/yolov8n_baseline/
#
# 【今天 4 个任务】
#   任务 0  ★★★ 补昨天 day11 的任务 4:把结果解读写成注释(30 分钟)
#   任务 1  ★★★ 用 best.pt 推理:和 day10 那次"0 个框"正面对比(30 分钟)
#   任务 2  ★★   看懂 4 张曲线图:PR / F1 / P / R + mAP50 vs mAP50-95(40 分钟)
#   任务 3  ★★   解读混淆矩阵:最大的问题不是"认错"而是"漏检"(30 分钟)
#   收工     我来回填 README 的 Results + 你推送 GitHub
#
# 【今天产出什么素材】
#   · "微调前 vs 微调后"的同一张图对比 —— 文书里最直观的证据
#   · "模型几乎不认错类,但漏检一半裂纹" —— 这是明天调参的靶子
# ==============================================================


# ==============================================================
# 【任务 0】补昨天 day11 的任务 4                        ★★★ 必做
# ==============================================================
# 打开 runs/detect/yolov8n_baseline/ 下的两张图,把答案写成注释
# 加到 day011practice.py 的末尾(Mission 4 部分):
#
#   ① results.png:
#      box_loss 和 cls_loss 是不是一路下降?大概第几轮后走平?
#      (走势平了 ≈ 训练到头了,这就是"收敛")
#
#   ② confusion_matrix.png:
#      哪两个类别最容易"互相认错"?
#      ⚠️ 这题的答案可能和直觉相反 —— 看任务 3 的提示。
#
#   ③ weights/ 里 best.pt 和 last.pt 文件大小几乎一样(都是 6.2MB),为什么?
#      (提示:同一个网络结构,权重数量相同;差别只在数值)
#
#   ④ 把 ①② 的答案写成两行注释留在 day011practice.py 里。


# ==============================================================
# 【任务 1】用 best.pt 推理 —— 见证微调的威力           ★★★ 必做
# ==============================================================
#
# 还记得 day10 吗?COCO 预训练的 yolov8n.pt 在 scratches_1.jpg 上:
#     conf >= 0.25  →  0 个框
#     conf >= 0.01  →  4 个框,全是"toothbrush",置信度 0.017~0.109
#
# 现在换成你自己训练出来的 best.pt,同样的图、同样的阈值,看会发生什么。
#
# 代码骨架(写在你的 day012practice.py 里;⚠️ 训练推理都记得包 main 保护):
#
#     from ultralytics import YOLO
#     import cv2
#
#     if __name__ == "__main__":
#         best = YOLO("runs/detect/yolov8n_baseline/weights/best.pt")
#         r = best("data/NEU-DET/IMAGES/scratches_1.jpg",
#                  device=0, conf=0.25, verbose=False)[0]
#         for c, cf, box in zip(r.boxes.cls, r.boxes.conf, r.boxes.xyxy):
#             print(best.names[int(c)],
#                   round(float(cf), 3),
#                   [round(float(v), 1) for v in box])
#         cv2.imwrite("practice/out/bestpt_scratches1.jpg", r.plot())
#
# 要做的:
#   ① 跑通,数一数出了几个框、类别对不对、置信度多少
#   ② 打开生成的 bestpt_scratches1.jpg,肉眼确认框画在哪
#   ③ 多试 2 张:crazing_1.jpg 和 inclusion_1.jpg(你自己挑)
#   ④ 把"day10 COCO 模型 vs 今天 best.pt"的对比写成 3 行注释 ——
#      这就是你文书中"fine-tuning 前后"的现场证据
#
# 【r.plot() 是什么】
#   day10 你是拿 cv2.rectangle 手动画框;其实 ultralytics 自带了:
#   r.plot() 返回"已经画好框和标签"的图(numpy 数组),直接 imwrite 即可。
#
# 【我实跑的结果(2026-10-15,conf>=0.25)】
#   scratches_1.jpg → 2 框,全是 scratches,置信度 0.63 / 0.55
#                     (day10 同图同阈值:0 框)
#   inclusion_1.jpg → 4 框,全是 inclusion,置信度 0.90 / 0.69 / 0.63 / 0.42
#                     (day10:同图只会出"toothbrush",置信度 ≤ 0.11)
#   crazing_1.jpg   → 0 框!
#                     ← 别慌,这不是坏了:混淆矩阵里 crazing 召回率只有 0.49,
#                        单张图测出来和整体指标完全吻合。crazing 就是明天的靶子。


# ==============================================================
# 【任务 2】看懂 4 张曲线图                              ★★ 推荐
# ==============================================================
# runs/detect/yolov8n_baseline/ 下有 4 张曲线图,全部来自那 180 张验证图:
#
#   BoxPR_curve.png   —— PR 曲线(最重要)
#       横轴 Recall(查全率):图上真实的缺陷,我找出来了多少
#       纵轴 Precision(查准率):我报出来的框,有多少是真的
#       这两个天生互相牵制:门槛(conf)调低 → 查全升但误报多;
#       门槛调高 → 查准升但漏检多。曲线下面积 = AP,所有类平均 = mAP。
#
#   BoxF1_curve.png   —— F1 曲线
#       F1 = 精确率和召回率的调和平均,越高越好。
#       曲线峰值对应的横轴 conf,就是"推荐的置信度阈值"。
#       读图任务:找到这个峰值点,记下 (conf, F1) —— 部署时就用它。
#
#   BoxP_curve / BoxR_curve —— 单看 P 或 R 随阈值怎么变,了解取舍用。
#
# 【mAP50 vs mAP50-95,别再混】
#   mAP50:   预测框和真值框重叠够 50% 就算对 → 宽松,数值高
#   mAP50-95:重叠 50%、60% … 95% 各算一次取平均 → 严格,数值低
#   你的:0.758 vs 0.411 —— 都正常,不是模型哪里坏了。
#
# 要做的:打开 BoxF1_curve.png,写下峰值处的 conf 和 F1 值(两行注释)。


# ==============================================================
# 【任务 3】解读混淆矩阵:最大的问题是"漏检"             ★★ 推荐
# ==============================================================
# confusion_matrix_normalized.png 怎么读:
#   ⚠️ 这版 ultralytics 的布局和教科书相反(源码 metrics.py 593 行):
#      横轴 X = True(真实类别),纵轴 Y = Predicted(模型判成什么),按列归一化
#   · 对角线格子 = 该类的召回率(判对的比例)
#   · 最后一行 Predicted=background = "真缺陷但模型什么都没报" = 各类漏检率
#
# 【我读出来的三个事实(你复核后写进自己的结论)】
#
#   ① 对角线:scratches 0.92 > patches 0.88 > inclusion 0.73 >
#      pitted_surface 0.72 > rolled-in_scale 0.65 > crazing 0.49
#
#   ② 类与类之间的混淆几乎为 0(全部 ≤ 0.01)!
#      → **"认错类别"根本不是问题**。这推翻了"模型会把它认成别的缺陷"的直觉。
#
#   ③ 损失全在最后一行(漏检):
#      crazing 51% 直接没报、rolled-in_scale 35%、pitted_surface 28%
#      (自检:对角线 = 1 − 漏检率,0.49=1−0.51 ✓ 0.73=1−0.27 ✓ 0.92=1−0.08 ✓)
#      → 最难的 crazing 恰好是"细裂纹纹理 + 小框",
#         也是框数量第二多的类(610 个)——目标小、密、淡。
#
# 【为什么这是好事】
#   问题被精确地定位成"漏检(召回率)"而不是"分类混乱"——
#   明天(10/16)调参就有了明确靶子:更大的模型 / 更小的推理尺寸 /
#   针对小目标的增强,都是冲着召回率去的。**能诊断出"哪里差",比分数本身值钱。**
#
# 要做的:把 ①②③ 用你自己的话写成 4~6 行注释(可以反驳我,只要你给出依据)。


# ==============================================================
# 【收工】
#   1. day011practice.py 补完任务 4 + day012practice.py 写完
#   2. 我把今天的数字回填进 README 的 Results(不再 pending!)
#   3. 你 git add + commit + push(看明天的绿方块)
# ==============================================================


# ==============================================================
#             ↓↓↓  参考答案    ↓↓↓
# ==============================================================
# ⚠️ 先自己写!写不出来再看,看完要重写一遍,别只抄。

if False:  # ← 抄的时候换成 if __name__ == "__main__":
    from ultralytics import YOLO
    import cv2

    best = YOLO("runs/detect/yolov8n_baseline/weights/best.pt")

    # ---------- 任务 1:三张图推理对比 ----------
    for name in ["scratches_1", "crazing_1", "inclusion_1"]:
        r = best(f"data/NEU-DET/IMAGES/{name}.jpg",
                 device=0, conf=0.25, verbose=False)[0]
        print(f"\n{name}: {len(r.boxes)} boxes (conf>=0.25)")
        for c, cf, box in zip(r.boxes.cls, r.boxes.conf, r.boxes.xyxy):
            print("   ", best.names[int(c)],
                  round(float(cf), 3),
                  [round(float(v), 1) for v in box])
        cv2.imwrite(f"practice/out/bestpt_{name}.jpg", r.plot())

    # ---------- 结果解读参考 ----------
    # day10(COCO 预训练,同图同阈值):scratches_1 → 0 框(0.01 才出 4 个 toothbrush)
    # day12(微调后):                 scratches_1 → 出 scratches 框,置信度大幅提高
    # 同一张图、同一个网络结构,唯一区别是:在 1620 张钢缺陷图上练了 26 分钟。
    # 这就是迁移学习:不是从零学"什么是缺陷",而是把"会找物体"的本事
    # 挪到"找钢缺陷"这个新任务上。
