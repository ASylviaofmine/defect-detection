# 累加器追踪:把"看不见的中间过程"打印出来
#
# 为什么写这个文件:
#   任务 2 那段代码,写完只给你 5 个最终结果(31 / 3.1 / 8 / 0 / 2),
#   中间的 10 圈循环发生了什么,屏幕上完全看不到 —— 这就是"看不懂"的根源。
#   这个文件把每一圈的 4 个篮子的值都打出来,你就能看见数据是怎么一点点攒起来的。
#
# 用法:右键 Run,盯着表格看,看完再回头读你的代码,就通了。

defects_per_image = [3, 0, 5, 2, 8, 1, 0, 4, 6, 2]

# ===== 第一步:开跑之前,先把 4 个篮子摆好 =====
total = 0                        # 累加篮子,里面装"到目前为止一共多少个缺陷"
biggest = defects_per_image[0]   # 最大篮子,先装第一个数(3),等下有更大的就换掉
smallest = defects_per_image[0]  # 最小篮子,先装第一个数(3),等下有更小的就换掉
zero_count = 0                   # 计数篮子,数"有几张图是 0"

print("=" * 72)
print(f"开跑前:  total={total}   biggest={biggest}   smallest={smallest}   zero_count={zero_count}")
print("=" * 72)

# ===== 第二步:一圈一圈地走,每圈打印一次,看篮子怎么变 =====
round_no = 0
for n in defects_per_image:
    round_no = round_no + 1
    print(f"\n--- 第 {round_no} 圈:n 拿到的是 {n} ---")

    # 动作 1:累加 —— 把 n 加进 total
    old_total = total
    total = total + n
    print(f"  ① total:    {old_total} + {n} = {total}")

    # 动作 2:挑战最大
    if n > biggest:
        print(f"  ② biggest:  {n} > {biggest}? 成立 → 换成 {n}")
        biggest = n
    else:
        print(f"  ② biggest:  {n} > {biggest}? 不成立 → 不动,还是 {biggest}")

    # 动作 3:挑战最小
    if n < smallest:
        print(f"  ③ smallest: {n} < {smallest}? 成立 → 换成 {n}")
        smallest = n
    else:
        print(f"  ③ smallest: {n} < {smallest}? 不成立 → 不动,还是 {smallest}")

    # 动作 4:是不是 0
    if n == 0:
        zero_count = zero_count + 1
        print(f"  ④ zero_count: n 是 0 → 记一个,现在是 {zero_count}")
    else:
        print(f"  ④ zero_count: n 不是 0 → 不动,还是 {zero_count}")

    print(f"  【本圈结束】 total={total}  biggest={biggest}  smallest={smallest}  zero_count={zero_count}")

# ===== 第三步:循环结束,篮子已经装满了,现在才能用 =====
print("\n" + "=" * 72)
print("10 圈走完,4 个篮子的最终结果:")
print(f"  total      = {total}      ← 总数 = 31")
print(f"  biggest    = {biggest}      ← 最多的那张")
print(f"  smallest   = {smallest}      ← 最少的那张")
print(f"  zero_count = {zero_count}      ← 零缺陷的图有几张")
print("=" * 72)

# 平均分必须等循环跑完才能算,因为 total 要 10 个数全加完才是 31
average = total / len(defects_per_image)
print(f"\n平均分在循环【外面】算: {total} / {len(defects_per_image)} = {average}")
print(f"留 2 位小数就是: {average:.2f}  ← 你代码里写的是 average 没加 :.2f,所以打出来是 3.1")

print("\n" + "=" * 72)
print("自己做三个小实验(改一行,Run 一次,看结果):")
print("=" * 72)
print("""
实验 1:把 smallest = defects_per_image[0] 改成 smallest = 0
        再跑一次,看看 smallest 最后是多少?为什么变成 0 了?
        (提示:任何数都不小于 0,所以最小的那个 if 永远不成立)

实验 2:把 total = total + n 改成 total = n
        看看 total 最后是多少?会变成列表里最后一个数(2)
        (因为每圈都把之前的值覆盖掉了,没有"攒"起来)

实验 3:把两个 if 改成 if / else 看看 ——
        写成 else 之后,一个数只能触发其中一个判断,统计会变少
""")
