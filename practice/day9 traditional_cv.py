# Day 9 练习(10/12):传统图像检测流水线 —— 滤波 / 形态学 / 边缘检测
# ★ 今天的真正目的:亲手体会到"传统方法为什么不够用",这就是你要用深度学习的理由。
#   你项目总结、动机信里"为什么选 YOLO"那段,素材就来自今天。
#
# ==============================================================
# ⏱ 今天 2.5 小时,这样分配:
# ==============================================================
#   0:00~0:40  看视频(B 站 黑马 OpenCV 入门 BV1Fo4y1d7JL):
#                 P23 图像噪声 / P24 均值滤波 / P25 高斯滤波 / P26 中值滤波
#                 P19 连通性 / P20 膨胀与腐蚀 / P21 开闭运算
#   0:40~2:20  写下面 4 个任务
#   2:20~2:40  收工检查 + 推送 GitHub
#
#   收工标准:
#     ✅ 三种滤波的区别能说出来(哪个去麻点最好?)
#     ✅ 膨胀/腐蚀/开/闭 四个词能对上画面
#     ✅ 知道 Canny 的两个阈值是干嘛的(调大调小会怎样)
#     ✅ 任务 4 的三问能答出来(★ 这是今天最重要的产出)
#     ✅ Ctrl+K 提交 + Ctrl+Shift+K 推送
# ==============================================================
#
# ---------- 新函数速查(写的时候回来查) ----------
# cv2.blur(img, (5,5))                         → 均值滤波:取周围 5x5 的平均值
# cv2.GaussianBlur(img, (5,5), 0)              → 高斯滤波:越近的邻居权重越大(day7 用过)
# cv2.medianBlur(img, 5)                       → 中值滤波:取周围 5x5 的中位数
#                                                 ⚠️ 第二个参数是数字 5,不是 (5,5)!
# kernel = np.ones((5,5), np.uint8)            → 造一个 5x5 的核(结构元素)
# cv2.erode(img, kernel)                       → 腐蚀:白色区域被"啃瘦"
# cv2.dilate(img, kernel)                      → 膨胀:白色区域"长胖"
# cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)  → 开运算 = 先腐蚀后膨胀(去小噪点)
# cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel) → 闭运算 = 先膨胀后腐蚀(补小缺口)
# cv2.Canny(img, 阈值1, 阈值2)                  → 边缘检测,输出白底黑线(边缘是白的!)
#
# ---------- 今天的路线图 ----------
#   真实工业检测的老流程是:  去噪(滤波) → 形态学处理 → 找边缘 → 圈出缺陷
#   今天你就把这条流程亲手跑一遍,然后看看它在真实数据上到底行不行。

import cv2
import numpy as np
import os

os.makedirs("practice/out", exist_ok=True)

# ==============================================================
# 【任务 1】三种滤波,谁去麻点最好?           ★★★ 必做
# ==============================================================
# ① 读 practice/demo_images/steel_pitted.png(麻点图,满是细小噪点),转灰度
# ② 分别做三种滤波(都用 k=5):均值 cv2.blur / 高斯 GaussianBlur / 中值 medianBlur
# ③ 连原图一起,存 4 张到 practice/out/:
#      filter_none.png / filter_mean.png / filter_gauss.png / filter_median.png
# ④ 在 PyCharm 里点开对比,回答(写注释里):
#    - 哪个把"孤立的噪点"去得最干净?
#    - 哪种会把缺陷边缘也一起弄糊?
# 提示:
#   中值滤波的第二个参数写 5(不是 (5,5)),别踩这个坑
#   经验答案(先自己看,再看这句):中值滤波对"椒盐噪点"最强,而且保边最好。
#   真实产线的图噪点一旦多,第一步往往就是中值滤波。
print("任务 1:")


# ==============================================================
# 【任务 2】形态学四操作:膨胀 / 腐蚀 / 开 / 闭    ★★★ 必做
# ==============================================================
# ① 用任务 1 的中值滤波结果(或重新读 pitted 灰度图)
# ② 先造核:kernel = np.ones((5, 5), np.uint8)
# ③ 做四个操作:erode / dilate / MORPH_OPEN / MORPH_CLOSE
# ④ 存 4 张到 out/:morph_erode.png / morph_dilate.png / morph_open.png / morph_close.png
# ⑤ 回答(写注释里):开运算和"只做腐蚀"看起来像在哪?差在哪?
# 提示:
#   形态学只对"白色前景"起作用。想看清效果,可以先把图二值化:
#       _, bw = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
#   (这行我没讲,看不懂就先跳过,用原图做也能看出胖瘦变化)
#   为什么工业检测要用形态学:噪点被腐蚀啃掉,缺陷被膨胀补成完整一块,方便后面圈框。
print("任务 2:")


# ==============================================================
# 【任务 3】Canny 边缘检测:阈值到底管什么?    ★★★ 必做
# ==============================================================
# ① 读 practice/demo_images/steel_pitted.png 转灰度
# ② 做两次 Canny:cv2.Canny(img, 30, 100) 和 cv2.Canny(img, 100, 200)
# ③ 分别数一下"白像素"有多少个 —— 边缘在图里是【白色】的
#       np.count_nonzero(edges)  ← 数非零(白的)像素个数
# ④ 存 2 张到 out/:canny_30_100.png / canny_100_200.png,点开对比
# ⑤ 回答(写注释里):阈值调大之后,白像素变多还是变少?被"筛掉"的是哪些边缘?
# 参考数字(我实跑过):30/100 → 511 个白像素;100/200 → 208 个白像素
# 提示:
#   Canny 的两个阈值管"这条边够不够陡":越高越严格,只有特别明显的边才留。
#   阈值太低 → 全是假边缘(噪点也变边);太高 → 真边缘也被丢掉。没有万能值,只能试。
print("任务 3:")


# ==============================================================
# 【任务 4】★ 真实数据实战 + 反思(今天的核心产出)   ★★★ 必做
# ==============================================================
# 终于用上真数据了!这次不用 demo 假图,用真实 NEU-DET 的两张:
#     data/NEU-DET/IMAGES/crazing_1.jpg     (裂纹)
#     data/NEU-DET/IMAGES/inclusion_1.jpg   (夹杂)
#
# ① 两张都读进来转灰度
# ② 对两张【都用同样的参数】cv2.Canny(img, 50, 150)
# ③ 数出各自的"白像素"数量,print 出来
# ④ 存图到 out/:real_canny_crazing.png / real_canny_inclusion.png,点开看
# ⑤ 【关键】回答下面三问(写注释里):
#    ① 为什么裂纹那张的"边缘像素"比夹杂多了几十倍?
#    ② 如果缺陷本身就是"一整片细密纹理"(裂纹),边缘检测还能圈出它在哪吗?
#       —— 连成一片的边缘,你怎么区分"这是缺陷"还是"这是正常钢板纹理"?
#    ③ 所以:传统方法的死穴是什么?这跟"为什么该用 YOLO"有什么关系?
#
# 我实跑出来的数字(你的应该一致):
#     crazing_1   Canny 50/150 → 15149 个白像素  ← 占全图 38%!整张图几乎都成"边缘"了
#     inclusion_1 Canny 50/150 →   236 个白像素
#
# 提示:想说清楚第 ③ 问,可以这样组织:
#   传统方法要人手工定规则(阈值多少、多大算缺陷),而规则一变(换个光照、
#   换种钢材)就失效;深度学习是从大量样本里自己学"缺陷长什么样"。
print("任务 4:")


# ==============================================================
# 【加餐】把边缘圈成框,看它有多乱              ★ 可跳
# ==============================================================
# ① 拿任务 4 的裂纹 Canny 结果,用 cv2.findContours 找出所有"边缘块"
# ② 用 cv2.boundingRect 给每个块算外接矩形,再 cv2.rectangle 画到彩图上
# ③ 存成 out/real_box_crazing.png,看看圈出来多少个框、像不像检测结果
# 提示(这几行今天没讲,属于提前尝鲜):
#     cnts, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     for c in cnts:
#         x, y, w, h = cv2.boundingRect(c)
#         cv2.rectangle(彩色图, (x, y), (x + w, y + h), (255, 0, 0), 1)
#   我实跑过:裂纹图能找出 237 个框 —— 但你要判断:这 237 个框里,有几个是真缺陷?
#   这就是"传统方法框不准"最直观的证据。
print("加餐:")


# ==============================================================
# ==============================================================
# ================== 参考答案(先自己写,别翻!) ==================
# ==============================================================
# ==============================================================

if False:
    # ---------- 任务 1 ----------
    import cv2, numpy as np
    img = cv2.imread("practice/demo_images/steel_pitted.png", cv2.IMREAD_GRAYSCALE)
    mean = cv2.blur(img, (5, 5))
    gauss = cv2.GaussianBlur(img, (5, 5), 0)
    median = cv2.medianBlur(img, 5)          # ← 注意是数字 5
    print("任务 1:")
    cv2.imwrite("practice/out/filter_none.png", img)
    cv2.imwrite("practice/out/filter_mean.png", mean)
    cv2.imwrite("practice/out/filter_gauss.png", gauss)
    cv2.imwrite("practice/out/filter_median.png", median)
    print("四张图已存到 practice/out/,去对比")
    # 结论:中值滤波去"孤立麻点"最干净,且缺陷边缘保留最好;
    #       均值/高斯会把边界一起抹糊(它们是"加权平均",边界也被平均掉了)。

    # ---------- 任务 2 ----------
    kernel = np.ones((5, 5), np.uint8)
    src = cv2.medianBlur(img, 5)
    er = cv2.erode(src, kernel, iterations=1)
    di = cv2.dilate(src, kernel, iterations=1)
    op = cv2.morphologyEx(src, cv2.MORPH_OPEN, kernel)
    cl = cv2.morphologyEx(src, cv2.MORPH_CLOSE, kernel)
    print("任务 2:")
    cv2.imwrite("practice/out/morph_erode.png", er)
    cv2.imwrite("practice/out/morph_dilate.png", di)
    cv2.imwrite("practice/out/morph_open.png", op)
    cv2.imwrite("practice/out/morph_close.png", cl)
    # 开运算 ≈ 腐蚀的效果(细小的亮点被抹掉了),但开运算之后整体亮度/大小更接近原图,
    # 因为它腐蚀完又膨胀回来了 —— 差别在于"被抹掉的小东西不会长回来"。

    # ---------- 任务 3 ----------
    e1 = cv2.Canny(img, 30, 100)
    e2 = cv2.Canny(img, 100, 200)
    print("任务 3:")
    print("30/100 ->", int(np.count_nonzero(e1)), "白像素")    # 511
    print("100/200 ->", int(np.count_nonzero(e2)), "白像素")   # 208
    cv2.imwrite("practice/out/canny_30_100.png", e1)
    cv2.imwrite("practice/out/canny_100_200.png", e2)
    # 阈值调大 → 白像素变少。被筛掉的是"不够陡"的弱边缘(噪点、纹理的细微起伏)。

    # ---------- 任务 4 ----------
    crazing = cv2.imread("data/NEU-DET/IMAGES/crazing_1.jpg", cv2.IMREAD_GRAYSCALE)
    inclusion = cv2.imread("data/NEU-DET/IMAGES/inclusion_1.jpg", cv2.IMREAD_GRAYSCALE)
    ec = cv2.Canny(crazing, 50, 150)
    ei = cv2.Canny(inclusion, 50, 150)
    print("任务 4:")
    print("crazing_1   ->", int(np.count_nonzero(ec)), "白像素")     # 15149
    print("inclusion_1 ->", int(np.count_nonzero(ei)), "白像素")     # 236
    cv2.imwrite("practice/out/real_canny_crazing.png", ec)
    cv2.imwrite("practice/out/real_canny_inclusion.png", ei)
    # ① 裂纹本身就是"一整片细密纹理",每条纹路都是一条边,所以边缘像素爆炸
    #    (15149 / 40000 = 38%,整张图都是"边缘")。
    # ② 不能。边缘连成一片时,没法知道哪块边缘属于缺陷 —— 它在整张图上到处都是。
    # ③ 传统方法的死穴:规则是人手工定的(阈值、大小),换个光照/钢材就失效;
    #    而且它只找到"边缘",不懂"什么是缺陷"。YOLO 是直接从大量样本里学
    #    "缺陷长什么样、通常在哪",所以对纹理型缺陷也稳。

    # ---------- 加餐 ----------
    color = cv2.imread("data/NEU-DET/IMAGES/crazing_1.jpg")     # 读彩色好画蓝框
    cnts, _ = cv2.findContours(ec, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(color, (x, y), (x + w, y + h), (255, 0, 0), 1)
    print("加餐:共画出", len(cnts), "个框")     # 实跑:237 个
    cv2.imwrite("practice/out/real_box_crazing.png", color)
