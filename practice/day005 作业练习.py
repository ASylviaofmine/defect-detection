# Day 5 练习:数据容器(列表 / 元组 / 字符串 / 字典)
# 对应视频:BV1qW4y1a7fU 的 p62~p80
# 规则:先自己写 15 分钟,写不出来再看文件最底部的参考答案(别一上来就翻!)

# ---------- 今天的新东西(看视频前先扫一眼,有个印象就行) ----------
# 列表 list:   用 [] 装一串东西,可以增删改     list = [1, 2, 3]
# 元组 tuple:  用 () 装一串东西,定了就不能改   point = (10, 20)
#              → 适合存"本来就不该变"的数据:坐标、图像尺寸、类别名称表
# 字符串 str:  本质也是一串字符,所以列表的很多技巧它也能用("hello"[0] → "h")
# 字典 dict:   键值对,靠【名字】找东西          {"crazing": 4}
#              → 列表像排号座位(靠 0/1/2 找),字典像电话簿(靠名字找)
#
# 索引从 0 开始;负数索引从后往前数(-1 是最后一个)
# 切片 [开始:结束:步长],和 range 一样是【左闭右开】
# 切片不改变原列表(复制一份给你);sort() 会改变原列表
#
# 为什么今天这章对你项目特别重要:
#   数据集里 每个缺陷类别名、每张图的文件路径、标注框的四个坐标——
#   全都是用列表和字典装起来的。第 10 天分析数据集,用的就是今天的工具箱。

# ---------------- 任务 1:列表基础 ----------------
# 先照抄这一行:
#     classes = ["crazing[0]", "inclusion[1]", "patches[2]"]
# 然后依次做下面 7 件事,每做完一件就 print 出来看看结果:
#   ① 在末尾追加 "rolled"            → 用 .append()
#   ② 在下标 1 的位置插入 "pitted"    → 用 .insert(1, "pitted")
#   ③ 删掉 "inclusion"               → 用 .remove("inclusion")
#   ④ 打印整个列表,再打印它的长度     → print(classes) / len(classes)
#   ⑤ 用索引取出第 1 个和第 3 个元素   → classes[0] / classes[2]
#   ⑥ 用负数索引取出最后一个元素       → classes[-1]
#   ⑦ 判断 "crazing" 在不在列表里      → "crazing" in classes
# 提示:
#   索引从 0 开始:第 1 个是 [0],第 2 个是 [1],第 3 个是 [2]
#   [-1] 是最后一个,[-2] 是倒数第二个
#   in 的结果是 True / False


print("Mission 1:")
classes=["crazing","inclusion","patches"]
classes.append("rolled")
print(classes)
#.append()在末尾追加
classes.insert(1,"pitted")
print(classes)
#.insert():在下标为几的地方中插一个。
classes.remove("inclusion")
print(classes)
#.remove():删掉
#remove 删的是内容，重复元素只删第一个
print(classes)
print(len(classes))
print(classes[0], classes[2])
print(classes[-1])#倒数第一格是什么
print(classes[-2])#倒数第二格是什么
print("crazing" in classes)#in 是"按名字问在不在"
print()

# ---------------- 任务 2:遍历统计(不许用内置函数) ----------------
# 这是第 10 天要用的核心技能:遍历一批数据,把统计量算出来
# 先照抄这一行:
#     defects_per_image = [3, 0, 5, 2, 8, 1, 0, 4, 6, 2]
# 意思是"10 张图,每张图里各有几个缺陷"
# 只用 for 循环和 if,手算出这 5 个数并打印:
#   ① 缺陷总数
#   ② 平均每张图几个缺陷(保留 2 位小数)
#   ③ 最多的一张有几个
#   ④ 最少的一张有几个
#   ⑤ 有几张图是"零缺陷"(完全合格)
# 提示——固定套路(叫"累加器",是编程里最常见的模式):
#     total = 0                     # ① 先准备一个空篮子
#     for n in defects_per_image:   # ② 一个一个拿出来
#         total = total + n         # ③ 扔进篮子
#   这个模式今天要写 5 遍,写完你就再也忘不掉了
#   求最大:先设 biggest = defects_per_image[0],遍历时遇到更大的就更新它
#   求最小:同理,用 < 判断
#   零缺陷计数:遍历时 if n == 0: 计数加 1
#   ⚠️ sum() / max() / min() 都能一行搞定,但【今天不许用】——
#      先用循环自己算一遍,你才知道那几个内置函数内部在干什么

print("Mission 2:")
defects_per_image = [3, 0, 5, 2, 8, 1, 0, 4, 6, 2]
total=0
biggest = defects_per_image[0]
smallest = defects_per_image[0]
zero_count=0
for n in defects_per_image:
    total=total+n
    if n>biggest:
        biggest = n
    if n<smallest:
        smallest = n
    if n==0:
        zero_count+=1
average=total/len(defects_per_image)
print(f"缺陷总数：{total}")
print(f"平均每张：{average:.2f}")
print(f"最多的一张有：{biggest}")
print(f"最少的一张有：{smallest}")
print(f"零缺陷的有：{zero_count}")
print()

# ---------------- 任务 3:排序与切片 ----------------
# 还是用上一题那个列表
#   ① 升序排序并打印           → .sort()
#   ② 降序排序并打印           → .sort(reverse=True)
#   ③ 取前 3 个                → [0:3] 或简写成 [:3]
#   ④ 取后 3 个                → [-3:]
#   ⑤ 反转整个列表并打印        → [::-1]
#   ⑥ 每隔一个取一个(下标 0、2、4…) → [::2]
# 提示:
#   切片 [开始:结束:步长] 和 range 一样是【左闭右开】——[0:3] 取到的是下标 0、1、2
#   [::-1] 是经典写法:开始和结束都留空,步长写 -1,意思就是"从头到尾倒着走"
#   ⚠️ 对比着看:sort() 改变原来的列表;切片不改变原列表,只是复制一份给你

print("Mission 3:")
num= [3, 0, 5, 2, 8, 1, 0, 4, 6, 2]
num.sort()
print(f"升序：{num}")
num.sort(reverse=True)
print(f"降序：{num}")

num= [3, 0, 5, 2, 8, 1, 0, 4, 6, 2]
print(f"{list(num[0:3])}")
print(f"{list(num[-3:])}")
print(f"{list(num[::-1])}")
print(f"{list(num[::2])}")
print()


# ---------------- 任务 4(项目实战):统计每类缺陷有多少个 ----------------
# 这题就是第 10 天分析 NEU-DET 数据集时你要写的代码,一模一样
# 先照抄这两行:
#     labels = ["crazing", "inclusion", "patches", "crazing", "rolled",
#               "inclusion", "crazing", "patches", "rolled", "crazing"]
#   ① 用字典统计每个类别出现了多少次(直接套用 day2 词频统计那套)
#   ② 遍历字典,每个类别打印一行,形如:  crazing 出现 4 次
#   ③ 找出出现次数最多的类别,打印:  出现最多的是 crazing
# 提示:
#   ① 的骨架(和 day2 一模一样,只是把"单词"换成"缺陷类别"):
#         counts = {}
#         for name in labels:
#             if name in counts:
#                 ...
#             else:
#                 ...
#   ② 同时取出键和值 → for name, n in counts.items():
#   ③ 找最大:先设 top_name = None、top_n = 0,然后遍历字典,
#      遇到 n > top_n 就同时更新这两个变量
#      —— 和任务 2 找最大值完全同一个思路,只是这次比较的是"值"

print("Mission 4:")
labels = ["crazing", "inclusion", "patches", "crazing", "rolled",
            "inclusion", "crazing", "patches", "rolled", "crazing"]
counts={}
for name in labels:
    if name in counts:
        counts[name]+=1
    else:
        counts[name]=1
for name, n in counts.items():
    print(f"{name} : {n} times")

most_name=None
most_n=0
for name, m in counts.items():
    if m>most_n:
        most_name=name
        most_n=m
print(f"出现最多的是 {most_name}，共 {most_n} 次")


# ---------------- 加餐(选做):嵌套字典 ----------------
# 字典里面还能再放字典,这是项目里组织复杂数据的常见方式
#     students = {
#         "张三": {"语文": 88, "数学": 95},
#         "李四": {"语文": 92, "数学": 79},
#     }
# 遍历打印每个人的每一科成绩,以及他的总分
# 提示:
#     for name, scores in students.items():
#         # 这里的 scores 本身又是一个字典,可以对它再 .items() 遍历一次
#         for subject, mark in scores.items():
#             ...