#知识点:for 循环嵌套、f-string 格式化、range 左闭右开

for i in range(1, 10):
    for j in range(1, i + 1):
        print(f"{j}x{i}={i * j:<8}", end="")
    print()  # 换行

print("-" * 30)


for i in range(1, 10):
    for j in  range(9, 0, -1) :
        print(f"{j}x{i}={i * j:<16}", end="")
    print()  # 换行

    print("-" * 30)


# TODO(你的作业):把上面代码改成"倒三角"乘法表(从 9x9 开始)
# 提示:把 range(1, 10) 改成 range(9, 0, -1) 试试,观察区别

for i in range(9,0,-1):
    for j in range(1,i+1):
        print(f"{j}x{i}={i * j:<8}",end="")
    print()

print()

print(list(range(9, 0, -2)))
