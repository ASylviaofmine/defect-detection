# ---------------- 任务 1:读一张图,亲眼看看"图片是数字"      ★★★ 必做 ----------------
# ① 用 cv2.imread 读 practice/demo_images/steel_scratch.png(划痕图)
# ② print 它的 shape 和 dtype
# ③ print img[0, 0] 和 img[100, 100](两个像素的值)
# ④ 思考题(把答案写在注释里):一张 200x200 的灰度图一共存了多少个数?
# 提示:
#   如果 print 出 None,99% 是路径错了 —— 从工作目录 defect_detection 算起


print("Mission 1:")
import cv2
import numpy as np
img = cv2.imread("practice/demo_images/steel_scratch.png", cv2.IMREAD_GRAYSCALE)
print("shape:", img.shape)
print("dtype:", img.dtype)
print("img[0][0]:",img[0][0])
print("img[100][100]:",img[100][100])

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


print("Mission 2:")
color = cv2.imread("practice/demo_images/color_part.png")
gray = cv2.cvtColor(color, cv2.COLOR_BGR2GRAY)
print("彩色shape:", color.shape)   # (200, 200, 3)
print("灰色shape:", gray.shape)    # (200, 200) -> 第三维没了
# 输出一律写进 practice/out/,不要写回素材目录(会覆盖原图)
cv2.imwrite("practice/out/gray_color_part.png", gray)
print("保存成功？", gray is not None)   # is not None = 不是空的 = 存进去了

# ---------------- 任务 3:缩放      ★★ 推荐 ----------------
# ① 读 steel_clean.png,缩成原来的一半(高宽各除以 2),print 新 shape
# ② 再把它拉伸成 800x800(会变形,没关系,看到效果就行),保存到 practice/out/big.png
# ③ print 原来 shape 和 800x800 的 shape,算一算像素总数变成了几倍
# 提示:
#   cv2.resize 的第二个参数是 (宽, 高) —— 故意和 shape 的 (高, 宽) 相反,记住这个坑
#   为什么要会缩放?10/12 用 YOLO 时,图片会被统一缩放到 640x640 再喂给模型,
#   今天先手动体验一次


print("Mission 3:")


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


print("Mission 4:")
img = cv2.imread("practice/demo_images/steel_pitted.png", cv2.IMREAD_GRAYSCALE)
b5 = cv2.GaussianBlur(img, (5, 5), 0)
b15 = cv2.GaussianBlur(img, (15, 15), 0)
cv2.imwrite("practice/out/blur_0.png", img)
cv2.imwrite("practice/out/blur_5.png", b5)
cv2.imwrite("practice/out/blur_15.png", b15)
print("已保存三张图,可在文件树里点开对比")
# 观察:k=5 时麻点基本消失;k=15 时整张图发糊、轧制纹路也被抹掉。
# 结论:模糊抹掉的是"细小变化"(噪点),但缺陷的边缘同样会变糊,所以 k 不是越大越好。

# ---------------- 任务 5:像素统计 —— 检测的雏形      ★★ 推荐 ----------------
# ① 分别读 steel_clean.png 和 steel_inclusion.png,转灰度
# ② 用 np.mean / np.min / np.max 打印两张图的平均亮度、最暗值、最亮值
# ③ 观察:含缺陷那张的 min 是不是明显更小?为什么?
# 提示:
#   想通了 ③ 你就懂了缺陷检测最朴素的原理:缺陷的地方亮度异常(特别暗或特别亮),
#   只要"某个像素的数值异常",它就可能是缺陷 —— 明天的 Canny、后天的 YOLO,
#   都是把这句大白话升级成更聪明、更稳的算法


print("Mission 5:")


# ---------------- 加餐:数一数"异常像素"有几个      ★ 可跳 ----------------
# ① 读 steel_inclusion.png 转灰度,算出平均值 avg
# ② 用 for 循环(不许用别的函数)数出:亮度低于 avg-40 的像素有几个
# ③ 再除以总像素数,算出异常占比(百分比,保留 2 位)
# 这就是 day5"循环统计"的老套路,只不过数的东西从"列表里的数"换成了"图里的像素"
# 提示:
#   两层 for,img.shape 是 (200, 200) -> for i in range(h): for j in range(w):
#   200x200 = 4 万次循环,Python 也就几秒钟,跑得动
# print("Bonus:")