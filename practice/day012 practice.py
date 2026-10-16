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

print(f"Mission 0:")
#   ① results.png:
#      box_loss 和 cls_loss 是不是一路下降?大概第几轮后走平?
#      (走势平了 ≈ 训练到头了,这就是"收敛")
#
#       loss 一路下降,第 60 轮后走平了 → 训练收敛
#       看 results.png:三个 loss 前 10 轮陡降,之后变缓但未停;真正判断收敛看右下角
#       mAP50:约第 40 轮起卡在 0.70~0.76 不再涨 → 已收敛。best.pt 是第 85 轮(成绩最好)


#   ② confusion_matrix.png:
#      哪两个类别最容易"互相认错"?
#      ⚠️ 这题的答案可能和直觉相反 —— 看任务 3 的提示。
#
## 混淆矩阵:格子里类与类之间很浅,但最后一列深 → 漏检多

#   ③ weights/ 里 best.pt 和 last.pt 文件大小几乎一样(都是 6.2MB),为什么?
#      (提示:同一个网络结构,权重数量相同;差别只在数值)

#best.pt 和 last.pt 用的是同一张图纸、同样多数量的数字。
#
#图纸一样 → yolov8n 的层数、每层的形状是固定的，不会变
#数字个数一样 → 都是 3,012,018 个，只是每个数字的取值不同

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

print(f"Mission 1:")
from ultralytics import YOLO
import cv2

if __name__ == "__main__":
    best = YOLO("runs/detect/yolov8n_baseline/weights/best.pt")
    r = best("data/NEU-DET/IMAGES/scratches_1.jpg",
            device=0, conf=0.25, verbose=False)[0]
    for c, cf, box in zip(r.boxes.cls, r.boxes.conf, r.boxes.xyxy):
        print(best.names[int(c)],
            round(float(cf), 3),
            [round(float(v), 1) for v in box])
    cv2.imwrite("practice/out/bestpt_scratches1.jpg", r.plot())
print()
# 要做的:
#   ① 跑通,数一数出了几个框、类别对不对、置信度多少
#   scratches：2个框，置信度：0.626、0.548
#   inclusion：4个框，置信度：0.898、0.688、0.626、0.416
#   crazing:0个框。
#   ② 打开生成的 bestpt_scratches1.jpg,肉眼确认框画在哪


#   ③ 多试 2 张:crazing_1.jpg 和 inclusion_1.jpg(你自己挑)
#inclusion_1.jpg:
if __name__ == "__main__":
    best = YOLO("runs/detect/yolov8n_baseline/weights/best.pt")
    r = best("data/NEU-DET/IMAGES/inclusion_1.jpg",
            device=0, conf=0.25, verbose=False)[0]
    for c, cf, box in zip(r.boxes.cls, r.boxes.conf, r.boxes.xyxy):
        print(best.names[int(c)],
            round(float(cf), 3),
            [round(float(v), 1) for v in box])
    cv2.imwrite("practice/out/bestpt_inclusion_1.jpg", r.plot())

#crazing_1.jpg:
if __name__ == "__main__":
    best = YOLO("runs/detect/yolov8n_baseline/weights/best.pt")
    r = best("data/NEU-DET/IMAGES/crazing_1.jpg",
            device=0, conf=0.25, verbose=False)[0]
    for c, cf, box in zip(r.boxes.cls, r.boxes.conf, r.boxes.xyxy):
        print(best.names[int(c)],
            round(float(cf), 3),
            [round(float(v), 1) for v in box])
    cv2.imwrite("practice/out/bestpt_crazing_1.jpg", r.plot())

#   ④ 把"day10 COCO 模型 vs 今天 best.pt"的对比写成 3 行注释 ——
#      这就是你文书中"fine-tuning 前后"的现场证据
#
# 【微调前后对比】同一张图,同一阈值 conf>=0.25
# day10(COCO 官方模型)   scratches_1.jpg → 0 框;conf 降到 0.01 才出 4 个"toothbrush"(置信度≤0.11)
# day12(我在 1620 张钢缺陷图上微调 26 分钟) → 2 框 scratches(0.63/0.55);inclusion_1 → 4 框(最高 0.88)
# 结论:网络结构完全没变,只是换了训练数据 —— 模型从"不认识钢缺陷"变成"能定位并分类六类缺陷"



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


print(f"Mission 2:")
#
# ② PR 曲线:patches AP 最高 0.945,crazing 最低 0.465,all classes mAP50=0.754
#    排名与混淆矩阵一致(漏检集中在 crazing) → 两个证据互相印证
# F1 曲线:读峰值处的 conf = 0.3~0.4 ,F1 = 0.7~0.8 (部署时用它当置信度门槛)
#打开 BoxF1_curve.png，找到曲线最高点，把横轴的 conf 值和纵轴的 F1 值填进去——那就是“部署时该用哪个置信度门槛”的官方答案。
##    校验:第85轮 P=0.714 R=0.699 → F1=2PR/(P+R)=0.706,与图上量级吻合
#
#F1 有个简单公式：F1 = 2×P×R ÷ (P+R)。
#第 85 轮: P=0.714, R=0.699
#F1 = 2 × 0.714 × 0.699 ÷ (0.714 + 0.699) = 0.706


# ==============================================================
# 【任务 3】解读混淆矩阵:最大的问题是"漏检"             ★★ 推荐
# ==============================================================
# confusion_matrix_normalized.png 怎么读:
#   · 纵轴 = 真实类别,横轴 = 模型判成什么
#   · 对角线格子 = 认对了的比例(= 该类的召回率)
#   · 最后一列 background = "真缺陷但模型什么都没报" = 漏检
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
#      → 最难的 crazing 恰好是"细裂纹纹理 + 小框",
#         也是框数量第二多的类(610 个)——目标小、密、淡。
#
# 【为什么这是好事】
#   问题被精确地定位成"漏检(召回率)"而不是"分类混乱"——
#   明天(10/16)调参就有了明确靶子:更大的模型 / 更小的推理尺寸 /
#   针对小目标的增强,都是冲着召回率去的。**能诊断出"哪里差",比分数本身值钱。**
#
# 要做的:把 ①②③ 用你自己的话写成 4~6 行注释(可以反驳我,只要你给出依据)。
print(f"Mission 3:")

# 混淆矩阵三件事:
# ① 对角线(认对率):scratches 0.92 最好、patches 0.88,crazing 只有 0.49 最差
# ② 类与类之间几乎全白(错分率≤0.01) → "认错类别"根本不是问题
# ③ 最右列 background(漏检)最深:crazing 漏 51%、rolled-in_scale 35%
# 结论:问题不是"分不清",而是"看不见" —— 小目标漏检,明天调参就冲它

#crazing 为什么最难？三个原因叠在一起：
#它是细裂纹纹理——淡、细、和背景对比度低
#它的框小——面积小，模型特征提取少
#它数量多（610 个框，第二多）——样本多但都难，拖累整体
