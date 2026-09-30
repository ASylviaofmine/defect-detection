# ---------------- 任务 1:成绩统计 ----------------
# 打印这组成绩的:最高分、最低分、平均分(平均分保留 1 位小数)
scores = [88, 92, 79, 93, 85, 61, 74, 99, 82, 70]
# 提示:
# max()、
# min()、
# sum()/len()、f"{x:.1f}" 可以保留1位、5位小数，保留整数；

#任务 1:
print("mission 1：")
print("最高分:", max(scores))
print("最低分:", min(scores))
print(f"平均分: {sum(scores) / len(scores):.1f}")
print(f"平均分: {sum(scores) / len(scores):.0f}")
print(f"平均分: {sum(scores) / len(scores):.5f}")

print()


# ---------------- 任务 2:找规律(FizzBuzz) ----------------
# 打印 1~30 的数字,但是:
#   能被 3 整除 → 打印 "Fizz"
#   能被 5 整除 → 打印 "Buzz"
#   能同时被 3 和 5 整除 → 打印 "FizzBuzz"
#   其余 → 打印数字本身
# 提示:先判断 % 15 == 0(同时整除),再判断 % 3、% 5,顺序不能反
#mission 2
#num(range(1,1,30))

# 任务 2:
print("mission 2：")
for n in range(1, 31):
#n 依次取 1、2、3……30。为什么不是 31？
# 因为 range 是左闭右开，到 31 前一格停
    if n % 15 == 0:
    #n % 3 == 0 and n % 5 == 0
    #% 是取余数
    #== 是判断相等（双等号！）。单等号 = 是赋值，别混。
    #"余数是 0" = "能被整除"
        print("FizzBuzz")
    elif n % 3 == 0:
    #elif 就是 else if 的缩写。意思是"上面那个条件不成立的话，再看看这个"。
        print("Fizz")
    elif n % 5 == 0:
        print("Buzz")
    else:
        print(n)

print()

# ---------------- 任务 3:词频统计(项目真实技能!)IMPORTANT ----------------
# 统计这句话里每个单词出现的次数,打印出出现 >= 2 次的单词和次数
text = "yolo detect defect defect steel yolo steel steel model detect yolo"
# 提示:
#   text.split() 会把句子切成单词列表
#   用字典统计:如果单词已在字典里,次数+1;不在,次数设为 1
#   最后用 for 遍历字典,只打印次数 >= 2 的

#？？？

# 任务 3:
print("mission 3：")
counts = {}
for word in text.split():
#text.split() 把句子按空格切成单词列表：
    if word in counts:
    #in 在这里判断"这个单词是否已经是字典里的一个键"。
    #
    #这一步为什么必须有 if 判断？
    # 因为 counts[word] += 1 的前提是"这个键已经存在"。
    # 如果直接对不存在的键做加法，Python 会报 KeyError（查无此键）。
    # 所以先用 in 探一下路——这是字典累加的固定套路，记住这个"先判断、再加一"的模式。
        counts[word] += 1
        #+= 是简写，等价于 counts[word] = counts[word] + 1。
    else:
        counts[word] = 1
for word, n in counts.items():
    # 一次把字典里每一对"键和值"​同时拿出来，所以左边能写两个变量 word, n 来接（这叫"拆包"）。
    # 如果只写 for word in counts:，你只能拿到单词，拿不到次数。
    if n >= 2:

         print(word, "出现了", n, "次")
