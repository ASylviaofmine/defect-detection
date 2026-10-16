# Day 1 练习:Python 基础
# 任务 1:跑通环境(直接运行本文件)
# 任务 2:看懂下面的九九乘法表代码,然后自己默写一遍

print("hello, 我开始学 Python 了")
print("今天的日期是:2026-09-21")
print("-" * 30)

# 九九乘法表(标准答案)
# 知识点:for 循环嵌套、f-string 格式化、range 左闭右开

for i in range(1, 10):
    for j in range(1, i + 1):
        print(f"{j}x{i}={i * j:<4}", end="")
    print()  # 换行

print("-" * 30)

# TODO(你的作业):把上面代码改成"倒三角"乘法表(从 9x9 开始)
# 提示:把 range(1, 10) 改成 range(9, 0, -1) 试试,观察区别

for i in range(1, 10):
    for j in  range(9, 0, -1) :
        print(f"{j}x{i}={i * j:<4}", end="")
    print()  # 换行

    print("-" * 30)

print("hello,i will start to study python today.")
print("today is 2026.09.27")
