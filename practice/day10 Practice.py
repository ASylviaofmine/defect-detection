# ==============================================================
# 【任务 1】跑通官方预训练模型:它到底认识什么?    ★★★ 必做
# ==============================================================
#
# yolov8n.pt 是官方在 COCO 数据集上训好的模型。COCO 有 80 个类:
#   人、自行车、汽车、狗、猫、飞机、椅子、牙刷、香蕉……全是"日常东西"。
#   里面**没有**任何一类是"钢材表面缺陷"。
#
# 你要做的:
#   ① 导入并加载权重:
#         from ultralytics import YOLO
#         model = YOLO("yolov8n.pt")
#   ② 对这张图推理(注意 device=0 表示用显卡,不加它默认也用显卡,但写上更保险):
#         img = "data/NEU-DET/IMAGES/scratches_1.jpg"     # 划痕图
#         results = model(img, device=0, verbose=False)
#   ③ 打印:检测到几个框?类别编号→类别名是什么?置信度多少?
#         提示: r = results[0];  b = r.boxes
#               len(b)              → 框的个数
#               b.cls               → 每个框的类别编号(tensor)
#               b.conf              → 每个框的置信度
#               model.names[int(编号)] → 编号对应的类别名
#   ④ 把 conf 阈值降到 0.01 再跑一次(默认是 0.25):
#         results2 = model(img, device=0, conf=0.01, verbose=False)
#      看它开始"乱框"成什么类了。
#   ⑤ 把结论写下来(用你自己的话,别抄):
#      为什么它在钢材图上什么都框不出来?这是模型坏了,还是别的原因?
#
# 我实跑过的结果(你可以对照,但你得自己跑一遍):
#   conf>=0.25 → 0 个框
#   conf>=0.05 → 2 个框,类别都是 "toothbrush"(牙刷),置信度 0.109 / 0.05
#   conf>=0.01 → 4 个框,全是 toothbrush,置信度最低 0.017
#
# 我的答案(参考,但请先自己想):
#   模型本身没坏 —— 它确实在"看图",而且给出了它的判断。
#   问题是它脑子里的 80 个类里没有"钢缺陷",它只能硬凑一个最像的(牙刷)。
#   置信度只有 1%~10%,说明它自己也很不确定。
#   → 结论:**通用模型换不了领域。想让它认识钢缺陷,只能拿钢缺陷数据再教它一遍。**
#     这就是明天(10/14)要自己训练的原因。
print("Mission 1:")
import cv2
from ultralytics import YOLO
model = YOLO("yolov8n.pt")
img_path = "data/NEU-DET/IMAGES/scratches_1.jpg"

r=model(img_path,device=0,verbose=False)[0]
print(f"conf>=0.25:",len(r.boxes),"个框")

r2=model(img_path,device=0,conf=0.01,verbose=False)[0]
print(f"conf>=0.01:",len(r2.boxes),"个框")

for c,cf in zip(r2.boxes.cls,r2.boxes.conf):
    print(" ",model.names[int(c)],round(float(cf),3))

# ==============================================================
# 【任务 2】读懂 YOLO 标注格式:把 0~1 的比例换回像素   ★★★ 必做
# ==============================================================
#
# 打开 data/NEU-DET-yolo/train/labels/crazing_1.txt,里面只有一行:
#
#     0 0.4875 0.49 0.955 0.96
#
# 这五个数就是 YOLO 格式的"标准答案"。它们分别是:
#
#     0            ← 类别编号(0 = crazing 裂纹,见 data/NEU-DET-yolo/data.yaml)
#     0.4875       ← 框中心的 x 坐标,但**归一化了**:是"占整幅图宽度的比例"
#     0.49         ← 框中心的 y 坐标,同样归一化
#     0.955        ← 框的宽度,归一化(占图宽的 95.5%)
#     0.96         ← 框的高度,归一化
#
# ⚠️ 关键理解(今天最值钱的一句话):
#   这四个数都乘了 0~1 的"比例系数",不是像素!
#   为什么要这样?→ 因为图片可能被缩放(200×200 → 640×640),
#   用比例记录,缩放后框的位置自动还是对的;用像素记录,一缩放就全错了。
#
# 你要做的:
#   ① 图片是 200×200(scratches 那种是 200×200,crazing_1.jpg 也是 200×200)
#   ② 先把 4 个数换算成像素:
#         cx = 0.4875 * 200 = ?      框中心的 x
#         cy = 0.49   * 200 = ?
#         w  = 0.955  * 200 = ?      框的宽
#         h  = 0.96   * 200 = ?      框的高
#   ③ 再换成"左上角 + 右下角"这两个点(这是画框、也是模型输出用的格式):
#         xmin = cx - w/2
#         ymin = cy - h/2
#         xmax = cx + w/2
#         ymax = cy + h/2
#   ④ 验证:打开 data/NEU-DET/ANNOTATIONS/crazing_1.xml,
#      找到 <bndbox> 里的 xmin/ymin/xmax/ymax,和 ③ 算出来的比一比。
#      允许差 1 像素(标注工具取整会差 1)。
#
# 我实跑过的结果:
#   cx=97.5, cy=98.0, w=191.0, h=192.0
#   → xmin=2.0, ymin=2.0, xmax=193.0, ymax=194.0
#   XML 里正是 <xmin>2</xmin> <ymin>2</ymin> <xmax>193</xmax> <ymax>194</ymax>
#   完全对上 —— 说明这份 YOLO 数据和官方 VOC 是同一套框,只是换了记法。
#
# ⚠️ 两种格式对照表(背下来,以后天天用):
#   ┌──────────┬────────────────────────────┬─────────────────────────┐
#   │          │ YOLO(.txt)                │ VOC(.xml)               │
#   ├──────────┼────────────────────────────┼─────────────────────────┤
#   │ 单位     │ 归一化比例 0~1             │ 像素                     │
#   │ 一个框   │ 一行 5 个数(空格隔开)      │ <object> 块             │
#   │ 位置表示 │ 中心点 + 宽高               │ 左上角 + 右下角          │
#   │ 类别     │ 编号(0~5)                  │ 名字(crazing 文本)      │
#   └──────────┴────────────────────────────┴─────────────────────────┘
print("Mission 2:")
sentence=open("data/NEU-DET-yolo/train/labels/crazing_1.txt").read().split()
cid,cx,cy,w,h=int(sentence[0]),float(sentence[1]),float(sentence[2]),float(sentence[3]),float(sentence[4])
W=H=200
cx,cy,w,h=cx*W,cy*H,w*W,h*H
xmin,ymin=cx - w/2,cy - h/2
xmax,ymax=cx + w/2,cy + h/2
print(f"category={cid},centre={cx,cy},width={w,h},")
print(f" ➡像素框{xmin}，{ymin}-{xmax},{ymax}")


# ==============================================================
# 【任务 3】把你算出来的框画到图上,亲眼验证    ★★★ 必做
# ==============================================================
#
# 任务 2 是"纸面计算",这一步是"眼见为实"。如果框画出来正好套住那片裂纹,
# 说明你前面所有换算都对了;如果画歪了,说明某一步搞错了。
#
# 你要做的:
#   ① 读图:  img = cv2.imread("data/NEU-DET-yolo/train/images/crazing_1.jpg")
#   ② 用任务 2 算出的 (xmin, ymin, xmax, ymax) 画框:
#            cv2.rectangle(img, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (0, 0, 255), 2)
#      坐标必须是**整数**(像素没有小数),所以用 int() 包一下
#   ③ 存到 practice/out/label_vis_crazing1.png
#   ④ 在 PyCharm 里点开看(展开 practice → out → 双击)
#
# 提示(day9 刚学过的画图):
#   颜色: 红色 = (0, 0, 255)   ← 注意 OpenCV 是 BGR 顺序,不是 RGB!
#   线宽: 2
#
# 加练(愿意就做,30 秒):
#   换成 inclusion_1 再画一次,确认不同类别的框也画得对。

print("Mission 3:")
img = cv2.imread("data/NEU-DET-yolo/train/images/crazing_1.jpg")
cv2.rectangle(img, (int(xmin), int(ymin)), (int(xmax), int(ymax)), ( 0, 0, 255),2)
cv2.imwrite("practice/out/label_vis_crazing1.png",img)
print(f"save!")

# ==============================================================
# 【任务 4】看懂模型的"输出对象"    ★★ 推荐
# ==============================================================
#
# 这一步是为了 10/16 做准备 —— 那天你要"整理量化指标":算 mAP、统计各类准确率。
# 那些指标全都来自模型输出对象里的这几样东西。
#
# 用任务 1 的 conf=0.01 那次结果(results2),把下面这些打印出来:
#
#   r = results2[0]
#   print(r.orig_shape)          # 原图尺寸 (高, 宽)
#   print(r.boxes.xyxy)          # 每个框的像素坐标: [左上x, 左上y, 右下x, 右下y]
#   print(r.boxes.cls)           # 每个框的类别编号
#   print(r.boxes.conf)          # 每个框的置信度
#   print(r.boxes.data)          # 上面三样拼在一起的一张大表(每行一个框)
#
# ⚠️ 坑:xyxy / cls / conf 都是 PyTorch 张量(tensor),不是 list。
#   想当普通数字用,要转一下:
#       .cpu().numpy()      → 变成 numpy 数组
#       .tolist()           → 变成 Python 列表
#   比如: print(r.boxes.xyxy.cpu().numpy())
#   (现在都在 CPU/GPU 上,区别不明显;但训练时张量在显卡里,
#    不 .cpu() 直接拿去打印/画图会报错,这个习惯现在就养起来。)
#
# 然后再做一件事:用 r.plot() 出一张"画好框的图",存下来
#       vis = r.plot()                      # 返回一张带框的图(numpy 数组)
#       cv2.imwrite("practice/out/pred_raw.png", vis)
#   打开看看:它把牙刷框在哪儿了?—— 你会发现那个框跟"缺陷"毫无关系,
#   这就是任务 1 结论的"眼见为实"版本。
print("Mission 4:")
print("orig_shape=",r2.orig_shape)
print("xyxy=",r2.boxes.xyxy.cpu().numpy())
print("cls=",r2.boxes.cls.cpu().numpy())
print("conf=",r2.boxes.conf.cpu().numpy())
print("data=")
print(r2.boxes.data.cpu().numpy())
cv2.imwrite("practice/out/pred_raw.png",r2.plot())
print(f"save!")