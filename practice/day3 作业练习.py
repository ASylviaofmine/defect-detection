# Day 3 练习:字符串格式化 + input 输入输出
# 对应视频:BV1qW4y1a7fU 的 p21~p28
# 规则:先自己写 15 分钟,写不出来再看文件最底部的参考答案(别一上来就翻!)

# ---------------- 任务 1:个人名片 ----------------
# 用 input() 问用户两个问题:叫什么名字?今年几岁?
# 然后打印: 你好,XXX! 你明年 N 岁。
# 提示:
#   input("问题文字") 会把用户敲进去的内容返回给你,存进变量
#   input 拿到的永远是【字符串】,年龄要加 1 就必须先用 int() 转成整数

print("mission 1:")
name=input("what is your name?")
age=int(input("what is your age?"))
n=int(age)+1
print(f"hello,{name}!And you are {n} years old next year. ")
print()

# ---------------- 任务 2:购物小票 ----------------
# 用 input() 输入商品单价和数量,计算总价
# 输出形如: 单价 12.5 x 数量 3 = 37.50 元
# 提示:
#   单价要用 float() 转,数量要用 int() 转
#   钱保留 2 位小数 → :.2f

print("mission 2:")
price=float(input("price?"))
count=int(input("how many?"))
n=price*count
print(f"{n:.2f}")
print()


# ---------------- 任务 3:对齐的名片 ----------------
# 打印出下面这种对齐效果:
# 姓名            成绩
# 张三            88.5
# 李四四          92.0
# 提示:
#   左对齐占 10 格 → :<10
#   右对齐占 6 格 → :>6
#   对齐和精度可以连用 → :>6.1f  (右对齐 6 格 + 保留 1 位小数)

print("mission 3:")
print(f"{'姓名':<10}{'成绩':>4}")
print(f"{'张三':<10}{88.5:>6.1f}")
print(f"{'李四':<10}{92.0:>6.1f}")
print()


# ---------------- 任务 4(挑战):BMI 计算器 ----------------
# 输入身高(米,如 1.75)和体重(公斤,如 68),计算 BMI 并保留 1 位小数
# 公式:BMI = 体重 ÷ 身高的平方
# 输出形如: 你的 BMI 是 22.2
# 提示:Python 里平方写作 ** ,也就是 身高 ** 2

print("mission 4:")
height=float(input("height(m)?"))
weight=float(input("weight(kg)?"))
BMI=weight/(height**2)
print(f"your BMI is {BMI:.1f}")
print(f"your BMI is {BMI:.2f}")
print()
