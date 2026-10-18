# ==============================================================
# day014 · Gradio-1   把模型装进一个网页里
# ==============================================================
# 2026-10-17 初版 / 2026-10-18 修订 v2
#
# 【v2 改了什么 —— 学生提出"题目和答案对不上",复核后确认 5 处】
#   ① 🚨 图片路径写错:验证集里**没有** crazing_1.jpg。
#        验证集只取每类最后 30 张,名字是 crazing_271 ~ crazing_300。
#        照原题 cv2.imread 会返回 None,下一行就报
#        AttributeError: 'NoneType' object has no attribute 'shape'
#        —— 看起来像模型坏了,其实是路径错了。
#   ② 变量名不统一:题目写 results[0].boxes,答案写 r = model(...)[0] 再用 r.boxes。
#        两件事一样,并排摆着会让人以为是两种 API。v2 全统一成 r。
#   ③ 任务 3 题目里 def detect_and_draw(image, conf): 下一行直接用了 bgr,
#        但 bgr 的赋值被 "..." 省略掉了。照抄必 NameError。v2 把那一行补全。
#   ④ 任务 1 只给了函数定义、没给"怎么调用",所以问题①"和你看到的框数一致吗"
#        根本没法执行。v2 补了 for 循环,并把问题①改成可验证的"预测数 vs 真值数"。
#   ⑤ 任务 0 的 launch() 会一直阻塞,后面的代码永远执行不到。
#        v2 明确写了"跑通后把这 4 行注释掉再往下走"。
#   另:原文说 crazing"很可能一个框都没有",那是 day12 用 train 里 crazing_1.jpg 的实测;
#        换成验证集 crazing_271,实际是 **3 个框(真值 4 个)**。v2 按实测改写。
#
# 【10/16 收尾:一个假设被证实,一个被证伪】
#   证实:换 yolov8s → crazing AP 0.464 → 0.548(+0.084),召回 0.367 → 0.494
#   证伪:提高分辨率 @960 → crazing AP 0.464,一位小数都没动
#         原因:原图只有 200×200,放大到 960 是插值,不增加任何真实信息
#   → "诊断对了病灶,不等于选对了药"。药得一个一个试。
#
# 【今天为什么做 Gradio】
#   到昨天为止,模型只能"自己跑在 PyCharm 里",别人看不到。
#   申请材料里最缺的不是分数,是"这个人做的东西我能点开"。← 录视频就靠它
#   Gradio 是纯 Python 工具:不写一行 HTML/CSS/JS,写几个函数就给你生成网页。
#
# 【今天 4 个任务】
#   任务 0  ★     5 分钟    跑通一个 4 行的网页(先单独确认"网页能开")
#   任务 1  ★★★  30 分钟   把推理包成函数,并在终端里跟真值做对比
#   任务 2  ★★★  40 分钟   接到网页上:上传图 → 出画好框的图
#   任务 3  ★★    20 分钟   挪成仓库根目录的 app.py + 置信度滑块
#
# ⚠️ 今天最容易卡的不是 YOLO,是**颜色**和**路径**。
# ==============================================================


# ==============================================================
# 【任务 0】先跑一个 4 行的网页                    ★ 5 分钟
# ==============================================================
#
# 目的:把"Gradio 能不能用"和"我的模型对不对"**分开验证**。
#       一起上,报错了你分不清是环境问题还是代码问题。
#
# 在 practice/day014 practice.py 里**先只写这 4 行**(其余注释掉):
#
#     import gradio as gr
#
#     def hello(name):
#         return f"你好,{name}!"
#
#     gr.Interface(fn=hello, inputs="text", outputs="text").launch()
#
# 在**仓库根目录**下运行:
#
#     python "practice/day014 practice.py"
#
# 终端打印 Running on local URL: http://127.0.0.1:7860,浏览器自动弹页面。
#
# 🚨 关键一步(初版漏了):跑通之后**把这 4 行注释掉**,再写任务 1。
#    因为 launch() 会一直卡住等用户访问,它后面的代码永远执行不到 ——
#    你会以为"任务 1 没生效",其实只是没轮到它。
#
# 【骨架就三样】
#     Interface(fn=?, inputs=?, outputs=?)
#   剩下全都只是把 inputs/outputs 从"文字"换成"图片"而已。
#
# ⚠️ 停下来按 Ctrl+C。终端不再输出新行不是卡死,是正常在等。
# ⚠️ 报 "Address already in use" = 上次的网页没关,回那个终端 Ctrl+C。


# ==============================================================
# 【任务 1】把推理包成一个函数(先不要界面)        ★★★ 30 分钟
# ==============================================================
#
# 这一步不碰 Gradio,还是一件纯粹的 YOLO 事情。要写 4 块:
#
#   ① 导入        import cv2 / from ultralytics import YOLO
#   ② 加载模型    model = YOLO("runs/detect/yolov8s_640/weights/best.pt")  ← 只写一次
#   ③ 定义函数    def detect(image): ...                                   ← 输入图,返回文字
#   ④ 调用它      for f in [...]: 读图 → detect → print                    ← 少了这步什么都看不到
#
# 【③ 里做的事,和要你自己回答的 4 个问题】
#
#     r     = model(image, conf=0.25)[0]     # model(...) 返回列表,取 [0]
#     boxes = r.boxes                        # 这一帧的所有框
#     n     = len(boxes)                     # 一共几个框
#     names = r.names                        # {0: 'crazing', 1: 'inclusion', ...}
#
#   ① n 和"真值框数"一致吗?(真值 = 标注 txt 里有几行)
#      先猜一张 crazing 会出几个框,再跑。不一致很正常,关键是说清"多了还是少了"。
#   ② boxes.cls 里装的是类别名字还是数字?      ← 提示:数字(0~5)
#   ③ 怎么把数字变成 'crazing' 这种名字?       ← 提示:names[int(...)]
#   ④ boxes.conf 里的数是什么范围?            ← 0~1
#
# 【先测这三张(注意是 _271,不是 _1)】
#     data/NEU-DET-yolo/test/images/crazing_271.jpg
#     data/NEU-DET-yolo/test/images/scratches_271.jpg
#     data/NEU-DET-yolo/test/images/inclusion_271.jpg
#
# 【跑完把这张表填满,这是今天的真实收获】
#     图                预测框数   真值框数   多了还是少了
#     crazing_271       ?          ?          ?
#     scratches_271     ?          ?          ?
#     inclusion_271     ?          ?          ?
#
#   真值自己数:打开 test/labels/同名.txt,有几行就是几个框。
#   你会看到一件反直觉的事:**AP 最高的类不一定"漏得少",它可能是"框画多了"。**
#   明天录视频时这句值得说:高 AP ≠ 每个框都对。
#
# 🔴 坑 1:颜色。BGR(OpenCV)vs RGB(网页)。通道反了不报错,只是整体偏蓝/偏红。
#   进去:cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)   出来:cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
#   少一次都不行。任务 1 用 cv2.imread 读的就是 BGR,暂时用不到;任务 2 会用到。
#
# 🔴 坑 2:模型只加载一次。model = YOLO(...) 要写在**函数外面**。
#   写进函数里,每次调用都要重读 22MB 权重 → 卡 2~3 秒。网页能用,就是"莫名很慢"。
#
# 🔴 坑 3(新增):cv2.imread 读不到文件时**不报错,返回 None**。
#   然后下一行 img.shape 才崩,报 'NoneType' object has no attribute 'shape'。
#   所以"NoneType 报错"十个里九个是路径错了,不是代码错了。


# ==============================================================
# 【任务 2】把函数接到网页上:上传图 → 出框        ★★★ 40 分钟
# ==============================================================
#
# 把任务 1 的函数改成"返回图片",再交给 Interface。
#
#     def detect_and_draw(image):          # image 是 Gradio 给的 numpy 数组,RGB
#         bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)   # ← 原版这里漏了这句
#         r   = model(bgr, conf=0.25)[0]
#         return cv2.cvtColor(r.plot(), cv2.COLOR_BGR2RGB)
#
#     gr.Interface(
#         fn      = detect_and_draw,
#         inputs  = gr.Image(type="numpy"),
#         outputs = gr.Image(type="numpy"),
#     ).launch()
#
# 【type="numpy" 是什么】
#   Gradio 默认给 PIL 图片对象。设成 "numpy" 就直接给 cv2 和 YOLO 都认识的数组,
#   少一次转换,少一个坑。
#
# 【验收标准】
#   ✅ 能拖进去一张图
#   ✅ 点 Submit 出现画好框的图
#   ✅ 颜色正常(不是一片诡异的蓝/红)
#   ✅ 框的数量和任务 1 在终端打印的一致
#
# 【别做的事】某张图框很少时,别急着把 conf 调到 0.05 让它"出框"。
#   那是骗自己:低 conf 出来的大多是误检,视频里也不能这么演示。


# ==============================================================
# 【任务 3】挪到仓库根目录的 app.py + 置信度滑块   ★★ 20 分钟
# ==============================================================
#
# 新建 defect_detection/app.py(不是 practice 里),= 任务 2 的代码 + 三处改动。
# 为什么要挪:README 已写 `python app.py`,项目该有一个"从这里能启动"的入口。
#
#   改动 ① 权重路径用 __file__ 定位,不用相对路径
#       你被"工作目录"坑过一次(报 data.yaml does not exist)。
#       根因:相对路径的基准是"从哪个目录启动 python",不是"脚本放在哪"。
#
#           from pathlib import Path
#           ROOT   = Path(__file__).parent                    # app.py 所在目录 = 仓库根
#           WEIGHT = ROOT / "runs/detect/yolov8s_640/weights/best.pt"
#           assert WEIGHT.exists(), f"找不到权重: {WEIGHT}"   # 早报错,别跑一半崩
#
#   改动 ② 加置信度滑块(注意 bgr 那一行不能少)
#           def detect_and_draw(image, conf):
#               bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
#               r   = model(bgr, conf=conf)[0]
#               return cv2.cvtColor(r.plot(), cv2.COLOR_BGR2RGB)
#
#           inputs = [gr.Image(type="numpy", label="上传缺陷图片"),
#                     gr.Slider(0.05, 0.95, value=0.25, step=0.05, label="置信度阈值")]
#       ⚠️ 两个 input 就要两个参数,顺序与 inputs 列表一一对应。
#
#   改动 ③ 加标题和指标
#           title       = "钢材表面缺陷检测 / Steel Surface Defect Detection"
#           description = "YOLOv8s fine-tuned on NEU-DET · mAP@50 0.766 · 6 classes"
#
# 【启动】
#     cd C:\Users\Lee\WorkBuddy\2026-09-21-21-29-56\defect_detection
#     python app.py
#
#   然后**别关终端**,截图存到 docs/figures/gradio_demo.png(README §4.5 要用)。
#   截图要求:标题、上传的图、右侧画框结果、置信度滑块,四样都在画面里。
#
# ⚠️ 关掉网页后要重新 python app.py 才能再开。正常:
#    Gradio 的网页是你的 Python 进程临时开的服务,进程没了网页就没了。
#    它不是部署,只是本地演示。


# ==============================================================
# 【参考答案】(先自己做,卡住再看)
# ==============================================================
#
# ---- 任务 1 的参考 ----
#
# import cv2
# from ultralytics import YOLO
#
# WEIGHT = "runs/detect/yolov8s_640/weights/best.pt"
# model  = YOLO(WEIGHT)                        # 只加载一次,放函数外面
#
# def detect(image):                           # image: BGR numpy 数组
#     r     = model(image, conf=0.25)[0]
#     boxes = r.boxes
#     n     = len(boxes)
#     if n == 0:
#         return "没有检测到缺陷"
#     parts = []
#     for i in range(n):
#         cls_id = int(boxes.cls[i])           # tensor → int
#         name   = r.names[cls_id]             # 0 → 'crazing'
#         conf   = float(boxes.conf[i])
#         parts.append(f"{name} {conf:.2f}")
#     return f"{n} 个框: " + ", ".join(parts)
#
# for f in ["crazing_271", "scratches_271", "inclusion_271"]:
#     img = cv2.imread(f"data/NEU-DET-yolo/test/images/{f}.jpg")
#     print(f, "->", detect(img))
#
# ---- 任务 2 / 3 的参考:app.py ----
#
# import cv2
# import gradio as gr
# from pathlib import Path
# from ultralytics import YOLO
#
# ROOT   = Path(__file__).parent
# WEIGHT = ROOT / "runs/detect/yolov8s_640/weights/best.pt"
# assert WEIGHT.exists(), f"找不到权重: {WEIGHT}"
#
# model = YOLO(str(WEIGHT))                    # 全局只加载一次
#
# def detect_and_draw(image, conf):
#     bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)      # 网页 RGB → 模型 BGR
#     r   = model(bgr, conf=conf)[0]
#     return cv2.cvtColor(r.plot(), cv2.COLOR_BGR2RGB)  # 模型 BGR → 网页 RGB
#
# demo = gr.Interface(
#     fn          = detect_and_draw,
#     inputs      = [gr.Image(type="numpy", label="上传缺陷图片"),
#                    gr.Slider(0.05, 0.95, value=0.25, step=0.05, label="置信度阈值")],
#     outputs     = gr.Image(type="numpy", label="检测结果"),
#     title       = "钢材表面缺陷检测 / Steel Surface Defect Detection",
#     description = "YOLOv8s fine-tuned on NEU-DET · mAP@50 0.766 · 6 classes",
# )
#
# if __name__ == "__main__":
#     demo.launch()
#
# ==============================================================
# 【收工前(3 分钟)】
#   1. 截图 docs/figures/gradio_demo.png
#   2. git add -A && git commit -m "day14: Gradio demo (upload -> annotated image)"
#      git push
#      再 `git status` 确认不再显示 "ahead N" —— 只有 "master -> master" 才算成功
#   3. 明天录视频。开头第一句别从"我做了一个缺陷检测系统"开始,
#      从"这条产线每天要人眼检几千片钢"开始。
# ==============================================================
