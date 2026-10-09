# Day 6 练习:文件读写、异常处理、模块
# 对应视频:BV1qW4y1a7fU 的 p81~p98(文件操作那几集必看)
# 规则:先自己写 15 分钟,写不出来再看文件最底部的参考答案(别一上来就翻!)
#
# ==============================================================
# ⏱ 今天只有 2.5 小时(10/8,压缩版节奏),这样分配:
# ==============================================================
#   0:00~0:30  补看 p51~p61(函数)          ← 你之前跳过了,今天必须补
#   0:30~1:20  看 p81~p98(文件读写/异常/模块)  ← 可跳过讲得很浅的集
#   1:20~2:50  做下面的练习
#
#   优先级(时间不够就按这个顺序砍):
#     ★★★ 必做   任务 2(读标注文件) 任务 4(自写模块)
#     ★★  推荐   任务 1  任务 3  加餐②(项目版)
#     ★   可跳   加餐①(嵌套字典,和项目无关)
#
#   为什么任务 2、4 是"必做":
#     任务 2 = 第 10/11 天读 NEU-DET 标注文件的代码,一模一样
#     任务 4 = 把代码拆成"函数 + 独立文件",10/11 的统计脚本、10/13 的
#              格式转换脚本都要这么写。不练这个,后面每天都难受。
#
#   收工标准(做到这些就算过,不必追求完美):
#     ✅ 能读出 labels_demo.txt 并统计出 12 个缺陷、四类各几个
#     ✅ 自己写的 day06_my_tools.py 能被 import 并调用成功
#     ✅ 看见过 FileNotFoundError 长什么样,并用 try/except 接住
#     ✅ Ctrl+K 提交 + Ctrl+Shift+K 推送
# ==============================================================
#
# ---------- 今天为什么重要 ----------
# 前面 5 天,你的数据都是自己在代码里手打的(scores = [88, 92...])。
# 从今天起,数据从【磁盘上的文件】里读进来 —— 这才是真实项目的起点。
#   第 10 天你会读 NEU-DET 的标注文件(每个 .txt 里一行一个缺陷),
#   今天任务 2 就是那件事的彩排,代码结构一模一样。
#
# ---------- 今天的新东西(看视频前先扫一眼) ----------
# open("路径", "r")    → 读   ;  open("路径", "w") → 写(⚠️ 会清空原有内容)
# with open("路径") as f:     → 最推荐的写法,离开缩进自动替你关闭文件
#      f.read()       一次读出全部内容(一个长字符串)
#      f.readlines()  读成列表,每个元素是一行(行尾带 \n)
#      for line in f: 一行一行读(文件大时用这个,省内存)
# 异常 try/except      → 出错时不崩溃,而是走另一条路
# 模块 import          → 把代码拆到别的 .py 文件里,再拿来用
#
# ---------- 一个必须先知道的事:相对路径从哪算起 ----------
# 代码里写的 "practice/demo_data/labels_demo.txt" 是【相对路径】,
# 它从"运行程序时所在的工作目录"算起,不是从 .py 文件所在位置算起。
# 在 PyCharm 里右键 Run,工作目录默认是【项目根目录】
# (也就是 ...\defect_detection\),所以下面这个路径能用。
# 如果报 FileNotFoundError,先怀疑路径 —— 任务 3 就是专门练这个的。





# ---------------- 任务 1:写入和读取 txt      ★★ 推荐 ----------------
# ① 用 "w" 模式,把下面三行写进 practice/demo_data/my_first_file.txt
#       第一行:我在学 Python 文件读写
#       第二行:这是第 6 天
#       第三行:今天天气不错
# ② 用 "r" 模式把它读回来,print 出来
# ③ 换成 with open(...) as f: 的写法重写一遍(推荐写法)
# 提示:
#   写文件时要自己加换行符:"\n" 不会自动加!少了它三行会挤成一行
#       f.write("第一行\n")
#   读文件两个常用方法:
#       f.read()        → 全部内容一个字符串
#       f.readlines()   → 列表,每行一个元素,行尾带 "\n"
#   ⚠️ 路径里的文件夹必须已经存在,open 不会替你创建文件夹
#      (practice/demo_data 这个文件夹我已经建好了)

print("Mission 1:")
import os
print("我现在站在:", os.getcwd())
path="practice/demo_data/my_first_file.txt"
f = open(path, "w", encoding="utf-8")
f.write("我在学 Python 文件读写\n")
f.write("这是第 6 天\n")
f.write("今天天气不错\n")
f.close()

f = open(path, "r", encoding="utf-8")
content=f.read()
f.close()
print(f"{content}")

with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()
print(lines)
print("行数:", len(lines))
print()


# ---------------- 任务 2:读真实格式的标注文件(项目彩排)   ★★★ 必做 ----------------
# 文件:practice/demo_data/labels_demo.txt
# 这是【YOLO 标注格式】,每一行的样子:
#       crazing 0.512 0.341 0.233 0.118
#       └类别┘ └────── 4 个坐标数字(先不用管)──────┘
#   一行 = 图上框出来的一个缺陷,和之前说的完全一致。
#
# 要做三件事:
#   ① 打印这个文件一共有几个缺陷(也就是几行)
#   ② 用字典统计:每个类别各出现了几次
#   ③ 打印结果(每行一个类别),并找出出现最多的类别
# 提示:
#   for line in f:                # 一行一行地读
#       parts = line.split()      # 按空格切开 → ["crazing","0.512",...]
#       name = parts[0]           # 第 0 个就是类别名
#   ⚠️ line 末尾有换行符 "\n",用 line.strip() 去掉(不然会混进统计里)
#   ⚠️ 万一文件里夹着空行,split() 会得到空列表 [],再取 [0] 就报 IndexError
#      —— 稳妥写法是先判断: if not parts: continue
#   统计字典那套直接抄 day5 的 mission 4 就行,一模一样

print("Mission 2:")
path="practice/demo_data/labels_demo.txt"
counts={}
total_lines = 0
f=open(path, "r", encoding="utf-8")
for line in f:
    parts = line.strip().split()
    if not parts:
        continue
    name=parts[0]
    total_lines+=1
    if name in counts:
        counts[name]+=1
    else:
        counts[name]=1
f.close()

print(f"缺陷总数：{total_lines}")
print(f"缺陷总数：{counts}")
for name,n in counts.items():
    print(f"{name}出现{n}次")
print()

most_name=None
most_n=0
for name,n in counts.items():
    if n>most_n:
        most_name=name
        most_n=n
print(f"{most_name}出现次数最多，有{most_n}次")


# ---------------- 任务 3:异常处理(出错也不崩)   ★★ 推荐 ----------------
# ① 先不加任何处理,直接读一个【不存在】的文件:
#       practice/demo_data/no_such_file.txt
#    跑一次,把报错信息看清楚 —— 记住 FileNotFoundError 这个名字
# ② 用 try / except 包起来:文件找不到时打印 "文件没找到,请检查路径"
# ③ 再加一步:except 之后打印一句 "程序继续运行,没有崩溃",
#    感受 try/except 的意义 —— 程序活下来了
# 提示:
#   try:
#       ...可能出错的代码...
#   except FileNotFoundError:
#       ...出错时做什么...
#   ⚠️ try 里面【只放】可能出错的那几行;不要把所有代码都塞进去
#   ⚠️ 加了 try 之后程序不会崩,但错误也"看不见"了 ——
#      实际项目里要在 except 里 print 出来,不然出了问题你都不知道

print("Mission 3:")

try:
    path = "practice/demo_data/no_such_file.txt"
    f = open(path, "r", encoding="utf-8")
    f.close()
    print(f"{f}")
except FileNotFoundError:
    print("文件没找到,请检查路径")
print("程序继续运行,没有崩溃")
print()


# ---------------- 任务 4:自己写一个模块         ★★★ 必做 ----------------
# ① 在 practice 文件夹下【新建一个文件】day06_my_tools.py,里面写一个函数:
#
#       def count_lines(path):
#           """数一个文件有多少行,返回行数"""      ← 这行叫文档字符串
#           你自己写
#
# ② 回到本文件,import 它,数出 labels_demo.txt 有多少行并打印
# ③ 再给 day06_my_tools.py 加一个函数 count_classes(path),
#    把任务 2 的统计逻辑搬进去,返回一个字典 {类别: 次数}
#    (这样以后别的脚本也能直接用,不用重写)
# 提示:
#   import my_tools                        → 用 my_tools.count_lines("路径")
#   from my_tools import count_lines       → 直接用 count_lines("路径")
#   ⚠️ day06_my_tools.py 必须和 day6.py 放在同一个文件夹(practice/)
#   ⚠️ 改了 day06_my_tools.py 之后,day6.py 要重新 Run 才会加载新代码
#   ⚠️ 函数里的变量名尽量和外面不冲突:函数内部叫 counts 没问题,
#      但如果你在外面也定义了 counts,函数里那个是另一个(这叫"作用域")

print("Mission 4:")
import day06_my_tools
n = day06_my_tools.count_lines("practice/demo_data/labels_demo.txt")
print("行数(缺陷总数):", n)
result = day06_my_tools.count_classes("practice/demo_data/labels_demo.txt")
print(result)
print()


# ---------------- 加餐(时间够再做,不够就跳) ----------------
# ① ★ 可跳 —— day5 欠的那道:遍历嵌套字典
#    为什么可以跳:嵌套字典不需要专门刷题。加餐②本身就是嵌套结构(字典套字典),
#    练了②就等于练了①;以后读 JSON 配置文件时还会自然碰上,那时学更省力。
#
#       students = {"张三": {"语文": 88, "数学": 95},
#                   "李四": {"语文": 92, "数学": 79}}
#    打印每个人的每一科成绩,以及他的总分
#   提示:外层 for 拿到的是"内层的那个字典",对它再 .items() 遍历一次
#
# ② ★★ 推荐(项目版,第 10 天真实要用的结构):统计"每张图里每类缺陷各几个"
#    数据:
#       data = [("img1", "crazing"), ("img1", "patches"), ("img1", "crazing"),
#               ("img2", "rolled"),
#               ("img3", "inclusion"), ("img3", "inclusion"), ("img3", "crazing")]
#    要打印成:
#       img1: crazing 2 个, patches 1 个
#       img2: rolled 1 个
#       img3: inclusion 2 个, crazing 1 个
#   提示:
#       result[img] = {}          # 第一次见到这张图,先给它建一个空的内层字典
#       result[img][cls] += 1     # 两层方括号:先按图名找,再按类别找
#   为什么这个结构重要:真实数据集就是"图 → 这张图上有哪些缺陷"的嵌套关系,
#   以后统计"平均每张图几个缺陷""哪张图最脏"全靠它。