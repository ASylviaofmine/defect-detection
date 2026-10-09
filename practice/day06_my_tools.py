def count_lines(path):
    """数一个文件有多少行,返回行数"""
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    return len(lines)


def count_classes(path):
    """统计每类缺陷各出现几次,返回字典"""
    counts = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.split()
            if not parts:
                continue
            name = parts[0]
            if name in counts:
                counts[name] += 1
            else:
                counts[name] = 1
    return counts
