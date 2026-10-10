# Day 8 练习(10/11):NEU-DET 真实数据集 —— 认缺陷 + 写统计脚本
# 规则:先自己写 15 分钟,写不出来再看文件最底部的参考答案(别一上来就翻!)
#
# ==============================================================
# ⏱ 今天 2.5 小时,这样分配:
# ==============================================================
#   0:00~0:30  认六类缺陷(看 tools/neu_det_samples.png + 翻 IMAGES 里的真图)
#   0:30~2:00  写下面的统计脚本
#   2:00~2:30  收工检查 + 推送 GitHub
#
#   收工标准:
#     ✅ 能说出六类缺陷的中文名和长相特征
#     ✅ 统计脚本跑出正确结果(六类各 300 张,共 1800 张)
#     ✅ 想通一件事:为什么"正好各 300 张"这件事本身值得写进项目总结
#     ✅ Ctrl+K 提交 + Ctrl+Shift+K 推送
# ==============================================================
#
# ---------- 开场:今天的数据是真的 ----------
#
# 前 7 天用的都是练习数据(12 行的 labels_demo.txt、合成的假图)。
# 今天开始,你用 10/9 已经下好的【真实 NEU-DET 数据集】,位置在:
#
#   data/NEU-DET/IMAGES/        1800 张真图(200x200 灰度 jpg)
#   data/NEU-DET/ANNOTATIONS/   1800 个 XML 标注(VOC 格式)
#
# ---------- 先认识 VOC 标注长什么样 ----------
#
# 打开 data/NEU-DET/ANNOTATIONS/crazing_1.xml,你会看到:
#
#   <annotation>
#       <filename>crazing_1.jpg</filename>
#       <size><width>200</width><height>200</height></size>
#       <object>
#           <name>crazing</name>              ← 缺陷类别就在这
#           <bndbox>
#               <xmin>2</xmin><ymin>2</ymin>      ← 框的左上角
#               <xmax>193</xmax><ymax>194</ymax>  ← 框的右下角
#           </bndbox>
#       </object>
#   </annotation>
#
# 一个 XML 就是一个"缺陷"的档案:类别 + 框住它的矩形位置。
# 【重要】有的图里有多个缺陷,就会有多个 <object> 段。这是 10/13 转换脚本的关键。
#
# ---------- 今天的核心思想:你已经写过两遍了 ----------
#
# 数"每类出现几次"这个逻辑,你在 day5 mission4 和 day6 任务2 各写过一次。
# 今天只是把数据源从"12 行假数据"换成"1800 个真文件"。
# 而且——day6 你不是把函数抽到 day06_my_tools.py 了吗?今天正好 import 它来用!
# 这就是"模块化"的真实回报:不用重写第四遍。

import os

XML_DIR = "data/NEU-DET/ANNOTATIONS"      # 标注目录
IMG_DIR = "data/NEU-DET/IMAGES"           # 图片目录

# ---------------- 任务 1:先摸清目录里有什么      ★★★ 必做 ----------------
# ① 用 os.listdir(XML_DIR) 拿到所有文件名,print 前 5 个看看
# ② print 一共有多少个 xml 文件、多少个 jpg 文件
# ③ 思考题(写在注释里):两者数量应该相等吗?为什么?
# 提示:
#   os.listdir 返回的是一个列表(day5 学过的那种),里面是文件名字符串
#   想数"jpg 有几个",可以用 for 循环 + 字符串 endswith(".jpg") 判断(day3 学过 str)
print("Mission 1:")


# ---------------- 任务 2:从文件名切出类别      ★★★ 必做 ----------------
# 文件名长这样:crazing_1.xml / pitted_surface_1.xml / rolled-in_scale_1.xml
# 目标:从 "pitted_surface_1.xml" 里切出 "pitted_surface"
# ① 拿一个文件名,用字符串方法去掉 ".xml" 后缀
# ② 再用 split("_") 切分,观察切出来几段
# ③ ⚠️ 关键坑:pitted_surface_1.xml 切出来是 ['pitted','surface','1'] ——
#    "pitted_surface" 自己就带下划线!所以不能简单取 [0]。
#    想清楚:哪一部分是数字(编号),剩下的拼起来就是类别名?
# ④ 写出一个能正确处理全部六类的切法,print 几个结果验证
# 提示:
#   判断"某段是不是数字"可以用 str.isdigit(),比如 "123".isdigit() 是 True
print("Mission 2:")


# ---------------- 任务 3:统计六类各多少张      ★★★ 必做 ----------------
# 目标:遍历 XML_DIR 里全部文件名,输出一个字典,形如:
#   {'crazing': 300, 'inclusion': 300, ...}
# ① 用任务 2 写好的切类别逻辑
# ② 用 day5/day6 那种"字典计数"套路累加
# ③ 打印结果,应该六类都是 300
# 提示:
#   你也可以试试 import day06_my_tools,但注意它里面的 count_classes 是
#   按"每行第一个空格前的词"切的(为 YOLO 的 txt 设计),对 XML 文件名不适用。
#   所以这里【自己写】更合适 —— 理解这一点,你就懂了"为什么函数不能无脑复用"。
print("Mission 3:")


# ---------------- 任务 4:把结果整理成一张表      ★★ 推荐 ----------------
# ① 把六类按固定顺序排好(别用字典的原始顺序,那样每次跑可能不一样)
# ② 用 f-string 对齐输出(day3 学的 :<15 那种),像这样:
#      crazing           300   16.7%
#      inclusion         300   16.7%
#      ...
#      ------------------------------
#      总计             1800  100.0%
# ③ 计算每类占比(百分比保留 1 位小数)
# 提示:
#   固定顺序可以写个列表:names = ["crazing", "inclusion", ...]
#   然后 for name in names: 依次取出数量,这样表格顺序永远一致
print("Mission 4:")


# ---------------- 任务 5:思考题(不写代码,写注释)      ★★ 推荐 ----------------
# 你统计出来会发现:六类【正好都是 300 张】。请回答(写在下面的注释里):
# ① 这说明这个数据集"平衡"还是"不平衡"?
# ② 真实工厂产线上,六种缺陷会一样多吗?哪种可能罕见得多?
# ③ 如果真实数据里"划痕 1000 张、裂纹只有 20 张",训练出来的模型会有什么毛病?
#    (提示:模型见多了谁,就更会认谁)
#
# 这三问的答案,就是你项目总结里"类别不平衡"那一节的素材。
# 面试/动机信里能聊出这一层,说明你不是"跑通了代码",而是"理解了问题"。
print("Mission 5:")


# ==============================================================
# ==============================================================
# ================== 参考答案(先自己写,别翻!) ==================
# ==============================================================
# ==============================================================

if False:
    # ---------- 任务 1 ----------
    import os
    files = os.listdir("data/NEU-DET/ANNOTATIONS")
    print("Mission 1:")
    print("前5个:", files[:5])
    xml_n = len([f for f in files if f.endswith(".xml")])
    img_n = len([f for f in os.listdir("data/NEU-DET/IMAGES") if f.endswith(".jpg")])
    print(f"xml 文件 {xml_n} 个, jpg 文件 {img_n} 个")
    # 应该相等(都是 1800):一个 XML 对应一张图,多一个少一个说明数据有问题。

    # ---------- 任务 2 ----------
    print("Mission 2:")
    name = "pitted_surface_1.xml"
    stem = name.replace(".xml", "")          # "pitted_surface_1"
    parts = stem.split("_")                  # ['pitted', 'surface', '1']
    print("切分结果:", parts)
    # 关键:最后一段是编号(数字),前面所有段拼起来才是类别
    cls_parts = [p for p in parts if not p.isdigit()]
    cls = "_".join(cls_parts)
    print("类别 =", cls)                      # pitted_surface
    # 抽查几个:
    for t in ["crazing_1.xml", "rolled-in_scale_27.xml", "scratches_300.xml"]:
        stem = t.replace(".xml", "")
        cls = "_".join([p for p in stem.split("_") if not p.isdigit()])
        print(f"  {t:28s} -> {cls}")

    # ---------- 任务 3 ----------
    print("Mission 3:")
    counts = {}
    for f in os.listdir("data/NEU-DET/ANNOTATIONS"):
        if not f.endswith(".xml"):
            continue
        stem = f.replace(".xml", "")
        cls = "_".join([p for p in stem.split("_") if not p.isdigit()])
        if cls in counts:
            counts[cls] += 1
        else:
            counts[cls] = 1
    print(counts)
    # 预期:{'crazing': 300, 'inclusion': 300, 'patches': 300,
    #        'pitted_surface': 300, 'rolled-in_scale': 300, 'scratches': 300}

    # ---------- 任务 4 ----------
    print("Mission 4:")
    names = ["crazing", "inclusion", "patches",
             "pitted_surface", "rolled-in_scale", "scratches"]
    total = sum(counts.values())
    print(f"{'类别':<18}{'数量':>6}{'占比':>9}")
    print("-" * 34)
    for n in names:
        c = counts[n]
        print(f"{n:<18}{c:>6}{c / total * 100:>8.1f}%")
    print("-" * 34)
    print(f"{'总计':<18}{total:>6}{100.0:>8.1f}%")
    # 输出示例:
    #   类别                 数量      占比
    #   crazing             300    16.7%
    #   ...
    #   总计               1800   100.0%

    # ---------- 任务 5(答案要点) ----------
    # ① 平衡。每类完全一样多,是官方为了"公平比较算法"特意配平的。
    # ② 不一样。真实产线上"划痕/氧化皮"这种常见,某些缺陷可能几千张里才几例。
    # ③ 模型会"偏科":见多了的类认得准,罕见的类经常漏检或认错(哪怕它更危险)。
    #    解决办法就是后面的招:数据增强、类别权重、重采样 —— 这就是"调优"的切入点了。
