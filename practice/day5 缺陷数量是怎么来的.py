# 这个文件回答一个问题:
#     defects_per_image = [3, 0, 5, 2, 8, 1, 0, 4, 6, 2]
# 这 10 个数字到底从哪来的?

# 下面这个列表,假装是"已经打开过的 10 张图"。
# 每一行 = 一张图;行里面的每个英文单词 = 这张图上框出来的一个缺陷。
#   crazing    裂纹
#   inclusion  夹杂
#   patches    斑块
#   rolled     轧制氧化皮
# 空的 [] 表示这张图干干净净、一个缺陷都没有(合格品)。
defects_by_image = [
    ["crazing", "inclusion", "patches"],                                                          # 图 1
    [],                                                                                            # 图 2
    ["crazing", "crazing", "rolled", "patches", "inclusion"],                                      # 图 3
    ["rolled", "patches"],                                                                         # 图 4
    ["crazing", "crazing", "inclusion", "inclusion", "patches", "patches", "rolled", "rolled"],    # 图 5
    ["crazing"],                                                                                    # 图 6
    [],                                                                                             # 图 7
    ["inclusion", "patches", "rolled", "crazing"],                                                 # 图 8
    ["crazing", "crazing", "inclusion", "patches", "rolled", "rolled"],                            # 图 9
    ["inclusion", "patches"],                                                                      # 图 10
]

# ============ 关键一步:数出每张图有几个缺陷 ============
# len() 你 day5 任务 1 已经用过了 —— 它数"这个列表里有几样东西"。
# 这里数的不是数字,而是一堆"缺陷的名字",数出来的个数就是缺陷个数。
defects_per_image = []
for one_image in defects_by_image:
    defects_per_image.append(len(one_image))

print("每张图的缺陷个数:", defects_per_image)
print()

# 核对一下:和任务 2 里那个列表是不是一模一样?
print("和任务 2 给的列表一样吗?", defects_per_image == [3, 0, 5, 2, 8, 1, 0, 4, 6, 2])
print()

# ============ 顺便看看:哪一类缺陷最多? ============
# 这段就是 day5 任务 4 要写的代码,也是第 10 天分析真实数据集时要做的事。
counts = {}
for one_image in defects_by_image:
    for name in one_image:
        if name in counts:
            counts[name] = counts[name] + 1
        else:
            counts[name] = 1

print("四类缺陷各出现多少个:")
for name, n in counts.items():
    print(f"  {name}: {n} 个")

total = 0
for n in counts.values():
    total = total + n
print(f"  合计: {total} 个")


# ============ 第 10 天会变成什么样? ============
# 上面那个 defects_by_image 是我手打的假数据。
# 第 10 天,你会写一段代码,把数据集里真实的标注文件一个一个读进来:
#
#     对每个标注文件:
#         打开它
#         一行一行读,每一行代表图上的一个缺陷框
#         把这些框装进一个列表
#
# 读出来的东西和上面长得一模一样 —— 只不过那时候不再是我编的,
# 而是 NEU-DET 数据集里 1800 张真实钢材图片上的真实缺陷。
#
# 所以:数字是假的,逻辑是真的。你现在练的循环 + 累加器,
# 第 10 天一个字都不用改。
