# Day 7 练习(10/9):OpenCV-1 —— 读图、灰度化、缩放、保存、高斯滤波
# 规则:先自己写 15 分钟,写不出来再看文件最底部的参考答案(别一上来就翻!)
#
# ==============================================================
# ⏱ 今天 2.5 小时,这样分配:
# ==============================================================
#   0:00~0:50  看视频:B 站随便挑一个播放量高的「OpenCV 入门」,
#              只看"读图/灰度/缩放/滤波"那 1/3 就行,后面别贪
#   0:50~2:20  做下面的练习
#   2:20~2:50  收工检查 + 推送 GitHub
#
#   优先级(时间不够就按这个顺序砍):
#     ★★★ 必做   任务 1(读图看数字)  任务 2(灰度化+保存)  任务 4(高斯滤波)
#     ★★  推荐   任务 3(缩放)  任务 5(像素统计)
#     ★   可跳   加餐(数暗像素)
#
#   收工标准(做到这些就算过,不必追求完美):
#     ✅ 能说出"一张 200x200 灰度图 = 200 行 x 200 列的数字表格"
#     ✅ 灰度化后的图保存成功,文件比彩色版小
#     ✅ 高斯滤波前后的两张图对比过,能说出区别
#     ✅ Ctrl+K 提交 + Ctrl+Shift+K 推送
# ==============================================================
#
# ---------- 先说三件开场必须知道的事 ----------
#
# ① 环境已经装好了(我检查过:OpenCV 5.0.0),今天不用 pip,直接写代码。
#
# ② ⚠️ practice/demo_images/ 里的图是【合成的假图】,不是真实数据!
#    是我按"钢板长什么样"用代码画出来的(生成脚本在 tools/make_demo_images.py)。
#    真实的 NEU-DET 缺陷图在 10/11 才下载。这样安排的原因:今天先把
#    图像处理的"手感"练出来,不被下载问题卡住。
#    真实 NEU-DET 的图就是 200x200 的灰度图,所以示例图也按这个尺寸做。
#
# ③ OpenCV 里颜色顺序是 BGR 不是 RGB!(历史原因,记住就行)
#    所以 cv2.imread 读进来的彩色图,第 0 个通道是蓝色、1 绿色、2 红色。
#
# ---------- 今天最重要的一个观念 ----------
# 前面 6 天你处理的数据是"数字列表"。今天开始,数据变成"图片"。
# 但在电脑眼里,图片仍然是数字:
#   彩色图 = 一个三维表格:200 行 x 200 列 x 3 个通道(蓝/绿/红各一个数,0~255)
#   灰度图 = 一个二维表格:200 行 x 200 列(每个格子一个数,0 黑 ~ 255 白)
# 图像处理 = 对这一大堆数字做运算。想通这一点,后面所有函数都不神秘。
#
# ---------- 新函数速查(写的时候回来查) ----------
# cv2.imread("路径")                    → 读图,得到一个大表格(numpy 数组)
#                                         ⚠️ 路径错了不报错,静默返回 None —— 经典坑!
# cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) → 彩色转灰度
# cv2.resize(img, (宽, 高))             → 缩放 ⚠️ 参数顺序是 (宽, 高),和 shape 的 (高, 宽) 相反!
# cv2.GaussianBlur(img, (k, k), 0)      → 高斯模糊;k 是滤波核大小,必须是奇数(3/5/7/15...)
# cv2.imwrite("路径", img)              → 保存图片,成功返回 True
# img.shape                             → (高, 宽) 或 (高, 宽, 3)
# img[y, x]                             → 取第 y 行第 x 列那【一个像素】的值 ⚠️ 先行后列!

import cv2
import numpy as np

# ---------------- 任务 1:读一张图,亲眼看看"图片是数字"      ★★★ 必做 ----------------
# ① 用 cv2.imread 读 practice/demo_images/steel_scratch.png(划痕图)
# ② print 它的 shape 和 dtype
# ③ print img[0, 0] 和 img[100, 100](两个像素的值)
# ④ 思考题(把答案写在注释里):一张 200x200 的灰度图一共存了多少个数?
# 提示:
#   如果 print 出 None,99% 是路径错了 —— 从工作目录 defect_detection 算起
# print("Mission 1:")


# ---------------- 任务 2:灰度化 + 保存      ★★★ 必做 ----------------
# ① 读 practice/demo_images/color_part.png(彩色图)
# ② 用 cvtColor 转灰度,print 转换前后的 shape(3 个数字 -> 2 个数字)
# ③ 把灰度图保存到 practice/out/gray_color_part.png
# ④ 在 PyCharm 左侧文件树里点开两张图对比,肉眼看看差别
# 提示:
#   practice/out/ 文件夹我已经建好了。程序员的写法是用下面这行自动建,
#   想练 day6 学的 os 模块可以自己加上:
#       import os
#       os.makedirs("practice/out", exist_ok=True)
#   为什么彩色转灰度有意义?真实 NEU-DET 数据全是灰度图,
#   颜色对检测没帮助,去掉它数据量少 2/3,还排除干扰。
# print("Mission 2:")


# ---------------- 任务 3:缩放      ★★ 推荐 ----------------
# ① 读 steel_clean.png,缩成原来的一半(高宽各除以 2),print 新 shape
# ② 再把它拉伸成 800x800(会变形,没关系,看到效果就行),保存到 practice/out/big.png
# ③ print 原来 shape 和 800x800 的 shape,算一算像素总数变成了几倍
# 提示:
#   cv2.resize 的第二个参数是 (宽, 高) —— 故意和 shape 的 (高, 宽) 相反,记住这个坑
#   为什么要会缩放?10/12 用 YOLO 时,图片会被统一缩放到 640x640 再喂给模型,
#   今天先手动体验一次
# print("Mission 3:")


# ---------------- 任务 4:高斯滤波(去噪)      ★★★ 必做 ----------------
# ① 读 steel_pitted.png(麻点图),转灰度
# ② 做 3 个版本:原图、GaussianBlur(k=5)、GaussianBlur(k=15),全存到 practice/out/
#    文件名:blur_0.png / blur_5.png / blur_15.png
# ③ 在 PyCharm 里点开对比,回答(写注释里):
#    - k=5 时麻点怎么了?
#    - k=15 时划痕/边缘还清楚吗?这说明"模糊"是把什么变没了、什么也变没了?
# 提示:
#   k 必须是奇数!写 (4,4) 会直接报错,亲手试一次印象更深(试完改回 5)
#   为什么这很重要:10/10 的 Canny 边缘检测对噪点极其敏感 ——
#   一堆噪点会被它当成一堆假边缘。所以真实流程永远是"先滤波、再找边缘"。
# print("Mission 4:")


# ---------------- 任务 5:像素统计 —— 检测的雏形      ★★ 推荐 ----------------
# ① 分别读 steel_clean.png 和 steel_inclusion.png,转灰度
# ② 用 np.mean / np.min / np.max 打印两张图的平均亮度、最暗值、最亮值
# ③ 观察:含缺陷那张的 min 是不是明显更小?为什么?
# 提示:
#   想通了 ③ 你就懂了缺陷检测最朴素的原理:缺陷的地方亮度异常(特别暗或特别亮),
#   只要"某个像素的数值异常",它就可能是缺陷 —— 明天的 Canny、后天的 YOLO,
#   都是把这句大白话升级成更聪明、更稳的算法
# print("Mission 5:")


# ---------------- 加餐:数一数"异常像素"有几个      ★ 可跳 ----------------
# ① 读 steel_inclusion.png 转灰度,算出平均值 avg
# ② 用 for 循环(不许用别的函数)数出:亮度低于 avg-40 的像素有几个
# ③ 再除以总像素数,算出异常占比(百分比,保留 2 位)
# 这就是 day5"循环统计"的老套路,只不过数的东西从"列表里的数"换成了"图里的像素"
# 提示:
#   两层 for,img.shape 是 (200, 200) -> for i in range(h): for j in range(w):
#   200x200 = 4 万次循环,Python 也就几秒钟,跑得动
# print("Bonus:")

# ==============================================================
# ==============================================================
# ================== 参考答案(先自己写,别翻!) ==================
# ==============================================================
# ==============================================================

if False:
    # ---------- 任务 1 ----------
    img = cv2.imread("practice/demo_images/steel_scratch.png", cv2.IMREAD_GRAYSCALE)
    print("Mission 1:")
    print("shape =", img.shape)     # (200, 200) -> 高 200 行,宽 200 列
    print("dtype =", img.dtype)     # uint8:无符号 8 位整数,只能存 0~255
    print("img[0, 0] =", img[0, 0])
    print("img[100, 100] =", img[100, 100])
    # 思考题:200 x 200 = 40000 个数。彩色图再 x3 = 120000 个。
    # (实测:img[0,0]=114,img[100,100]=113。你算出的数若差一两个,是版本差异,正常)
    # 若 print None:路径不对。确认你是在 defect_detection 根目录运行。

    # ---------- 任务 2 ----------
    color = cv2.imread("practice/demo_images/color_part.png")
    gray = cv2.cvtColor(color, cv2.COLOR_BGR2GRAY)
    print("Mission 2:")
    print("彩色 shape:", color.shape)   # (200, 200, 3)
    print("灰度 shape:", gray.shape)    # (200, 200) -> 第三维没了
    cv2.imwrite("practice/out/gray_color_part.png", gray)
    print("保存成功?", gray is not None)
    # 文件树里对比:彩色原图 48KB 左右,灰度图 13KB 左右 -> 信息少了,文件变小

    # ---------- 任务 3 ----------
    img = cv2.imread("practice/demo_images/steel_clean.png", cv2.IMREAD_GRAYSCALE)
    half = cv2.resize(img, (img.shape[1] // 2, img.shape[0] // 2))   # (宽, 高)
    print("Mission 3:")
    print("原 shape:", img.shape, "-> 一半:", half.shape)            # (200,200) -> (100,100)
    big = cv2.resize(img, (800, 800))
    cv2.imwrite("practice/out/big.png", big)
    print("800x800 的像素总数是原来的", (800 * 800) // (200 * 200), "倍")   # 16 倍

    # ---------- 任务 4 ----------
    img = cv2.imread("practice/demo_images/steel_pitted.png", cv2.IMREAD_GRAYSCALE)
    b5 = cv2.GaussianBlur(img, (5, 5), 0)
    b15 = cv2.GaussianBlur(img, (15, 15), 0)
    cv2.imwrite("practice/out/blur_0.png", img)
    cv2.imwrite("practice/out/blur_5.png", b5)
    cv2.imwrite("practice/out/blur_15.png", b15)
    print("Mission 4:已保存三张图,去文件树里点开对比")
    # - k=5:麻点基本消失(小噪点被周围的平均数"抹平"了)
    # - k=15:连轧制纹路都被抹掉,整张图发糊 —— 模糊抹掉的是"细小变化",
    #   但缺陷的边缘也会变糊,所以 k 不是越大越好,要挑一个"去噪但保边"的值

    # ---------- 任务 5 ----------
    clean = cv2.cvtColor(cv2.imread("practice/demo_images/steel_clean.png"), cv2.COLOR_BGR2GRAY)
    inc = cv2.cvtColor(cv2.imread("practice/demo_images/steel_inclusion.png"), cv2.COLOR_BGR2GRAY)
    print("Mission 5:")
    print(f"clean: mean={np.mean(clean):.1f}  min={np.min(clean)}  max={np.max(clean)}")
    print(f"inclusion: mean={np.mean(inc):.1f}  min={np.min(inc)}  max={np.max(inc)}")
    # 参考输出(大致):clean min=96  /  inclusion min=44
    # 缺陷处特别暗,所以 min 被拉低了一大截 —— 这就是"数值异常 = 可能是缺陷"

    # ---------- 加餐 ----------
    img = cv2.cvtColor(cv2.imread("practice/demo_images/steel_inclusion.png"), cv2.COLOR_BGR2GRAY)
    avg = np.mean(img)
    count = 0
    h, w = img.shape
    for i in range(h):
        for j in range(w):
            if img[i, j] < avg - 40:
                count += 1
    print("Bonus:")
    print(f"平均亮度 {avg:.1f},异常像素 {count} 个,占比 {count / (h * w) * 100:.2f}%")
    # 参考输出(实测):平均亮度 113.6,异常像素 542 个,占比 1.35%
    # (数不一定和你完全一样,量级对就行)
