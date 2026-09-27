# Day 2 练习:列表、字典、循环、条件
# 规则:先自己写,写不出来再看文件最底部的参考答案(先挣扎 15 分钟再看!)

# ---------------- 任务 1:成绩统计 ----------------
# 打印这组成绩的:最高分、最低分、平均分(平均分保留 1 位小数)
scores = [88, 92, 79, 93, 85, 61, 74, 99, 82, 70]
# 提示:max()、min()、sum()/len()、f"{x:.1f}" 可以保留1位小数


# ---------------- 任务 2:找规律(FizzBuzz) ----------------
# 打印 1~30 的数字,但是:
#   能被 3 整除 → 打印 "Fizz"
#   能被 5 整除 → 打印 "Buzz"
#   能同时被 3 和 5 整除 → 打印 "FizzBuzz"
#   其余 → 打印数字本身
# 提示:先判断 % 15 == 0(同时整除),再判断 % 3、% 5,顺序不能反


# ---------------- 任务 3:词频统计(项目真实技能!) ----------------
# 统计这句话里每个单词出现的次数,打印出出现 >= 2 次的单词和次数
text = "yolo detect defect defect steel yolo steel steel model detect yolo"
# 提示:
#   text.split() 会把句子切成单词列表
#   用字典统计:如果单词已在字典里,次数+1;不在,次数设为 1
#   最后用 for 遍历字典,只打印次数 >= 2 的

# ==================== 参考答案(做完再看!) ====================
# 任务 1:
# print("最高分:", max(scores))
# print("最低分:", min(scores))
# print(f"平均分: {sum(scores) / len(scores):.1f}")

# 任务 2:
# for n in range(1, 31):
#     if n % 15 == 0:
#         print("FizzBuzz")
#     elif n % 3 == 0:
#         print("Fizz")
#     elif n % 5 == 0:
#         print("Buzz")
#     else:
#         print(n)

# 任务 3:
# counts = {}
# for word in text.split():
#     if word in counts:
#         counts[word] += 1
#     else:
#         counts[word] = 1
# for word, n in counts.items():
#     if n >= 2:
#         print(word, "出现了", n, "次")
