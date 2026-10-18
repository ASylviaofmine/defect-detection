# Demo video — 分镜脚本与录制说明

> 目标：1 分 50 秒～2 分 10 秒，**英文旁白 + 英文硬字幕**，1920×1080。
> 用途：README §4.5 嵌入 + 申请材料里作为"可点开的东西"。
> 原则：**每个数字都必须能在仓库里找到出处**；失败案例要说，不要剪掉。

---

## 一、录制前准备（10 分钟，别省）

| 项 | 做法 |
| --- | --- |
| 关掉干扰 | 微信 / QQ / 邮件通知全关；Windows「专注助手」设为"仅闹钟" |
| 清桌面 | 桌面上 `samples` 文件夹保留（要用），其它图标别入镜 |
| 终端字号 | 终端里 `Ctrl + 滚轮上`，调到镜头前能看清（约 18~20 号） |
| 浏览器 | 缩放保持 100%，关掉书签栏（`Ctrl+Shift+B`） |
| 服务先起好 | 在仓库根目录 `python app.py`，确认 http://127.0.0.1:7860 能打开，**别在录制中途启动**（有 23 秒无输出） |
| 预先打开的窗口 | ① `app.py` 的网页 ② README 的 §4.2 表格 ③ 终端（跑 audit 的输出） |
| 稿子 | 放在手机或另一块屏上；**不要**放在要录的屏幕里 |
| 试录 10 秒 | 先录一段，回放确认：声音有、字看得清、没弹窗 |

---

## 二、分镜表

> 英文是**照着念的**，中文只是帮你理解意思，不用念。
> 每段单独录，录坏了只重录那一段。

### 镜头 1 ｜ 0:00–0:08 ｜ 画面：一张钢材缺陷图铺满（`docs/samples/crazing_271.jpg`）

**EN**：Every steel strip is inspected by eye before it ships. At line speed that is thousands of sheets per shift, and attention is the bottleneck.

**中**：每一条钢带出厂前都靠人眼看。按产线速度，一个班要看几千片——瓶颈是人眼能撑多久。

---

### 镜头 2 ｜ 0:08–0:16 ｜ 画面：六类对照图 `tools/neu_det_samples.png`

**EN**：NEU-DET defines six surface defect classes: crazing, inclusion, patches, pitted surface, rolled-in scale and scratches.

**中**：NEU-DET 定义了六类表面缺陷：裂纹、夹杂、斑块、麻点、氧化皮压入、划痕。

---

### 镜头 3 ｜ 0:16–0:32 ｜ 画面：day9 的 Canny 对比图（crazing 满屏 vs inclusion 几乎为零）

**EN**：I started with Canny. One threshold floods a crazing image — 38 percent of pixels lit — or misses an inclusion at 0.6 percent. No single threshold serves six classes. That measurement is why I moved to a learned detector.

**中**：我先试了 Canny。同一个阈值，在裂纹图上点亮 38% 的像素，在夹杂图上只抓到 0.6%。一个阈值伺候不了六类缺陷——这个实测结果就是我转向深度学习的原因。

---

### 镜头 4 ｜ 0:32–0:46 ｜ 画面：终端跑 `python tools/audit_dataset.py` 的输出

**EN**：Before training, I audited all 1,800 images: 4,189 boxes, labels paired one to one, every row valid. Only 27 percent hold a single defect — this is multi-instance detection.

**中**：训练前我先给 1800 张图做了体检：4189 个框、图签一一对应、每一行都合法。只有 27% 的图是单个缺陷——这是多实例检测任务。

---

### 镜头 5 ｜ 0:46–1:08 ｜ 画面：README §4.2 三组实验表格（慢慢往下滚）

**EN**：Fine-tuning YOLOv8n for a hundred epochs took 26 minutes on a laptop GPU and reached mAP 0.758. A larger backbone reached 0.766, and lifted the hardest class, crazing, from 0.46 to 0.55. Raising input resolution to 960 changed crazing by zero — the images are 200 pixels square, so there was nothing to recover.

**中**：在笔记本 GPU 上微调 YOLOv8n 一百轮，26 分钟，mAP 0.758。换更大的骨干网络到 0.766，把最难的裂纹类从 0.46 提到 0.55。但把输入分辨率提到 960，裂纹类一点没变——原图只有 200×200，没有信息可以找回来。

---

### 镜头 6 ｜ 1:08–1:35 ｜ 画面：网页 demo，拖入 `scratches_271.jpg` → 7 个框 → 滑块拉到 0.50 → 4 个框

> 操作节奏：拖进去 → 停 2 秒（让人看清 7 个框）→ 慢慢拉滑块 → 点 Submit → 停 2 秒（4 个框）

**EN**：Here it is running. This image has four defects. At the default threshold the model reports seven; at 0.50 it reports exactly four. The trade-off between missing a defect and raising a false alarm is visible, not hidden.

**中**：这是它在跑。这张图实际有 4 个缺陷。默认阈值下模型报了 7 个，把阈值提到 0.50 正好报 4 个。"漏检"和"误报"之间的取舍，是可以看见的，不是藏起来的。

---

### 镜头 7 ｜ 1:35–1:50 ｜ 画面：同一个网页，拖入 `crazing_271.jpg` → 只有 3 个低置信度框

**EN**：On the hardest class it finds only three weak boxes. I show this on purpose: the failure mode is misses, not wrong labels.

**中**：在最难的那类上，它只报出 3 个把握不大的框。我是故意放这段的——它的失败方式是"漏"，不是"认错"。

---

### 镜头 8 ｜ 1:50–2:05 ｜ 画面：README 的 Limitations 章节，滚到结尾

**EN**：All of this was measured on 180 images from one acquisition setup — a benchmark result, not a production estimate. Next: a held-out test protocol and edge latency.

**中**：这些数字都来自同一台设备拍的 180 张图——是基准成绩，不是产线估计。下一步是做独立测试集和边缘设备延迟测试。

---

### 镜头 9 ｜ 2:05–2:12 ｜ 画面：GitHub 仓库首页

**EN**：The data audit, training scripts and failure analysis are all in the repository.

**中**：数据体检脚本、训练脚本和失败分析，都在仓库里。

---

## 三、怎么录（Windows，不用装软件）

1. **按 `Win + G`** → 出现 Xbox Game Bar → 点左上角的"录制"圆点（或 `Win + Alt + R` 直接开始/停止）。
2. 第一次用会问"这是游戏吗"——选**是**，就能录任何窗口。
3. 录完的文件在 `C:\Users\<你>\Videos\Captures\`。
4. **每段单独录**，文件名按 `s1` `s2` … 存，剪起来最快。
5. 想指定只录某个窗口：`Win + G` → 设置 → 捕获 → 勾选"仅录制所选窗口"。

> 如果 Win+G 录不了（部分教育版），备选：PowerPoint → 插入 → 屏幕录制（能导出 mp4）。

## 四、剪与字幕（剪映专业版，免费）

1. 新建项目 → 导入 9 段 → 按顺序拖到时间线 → 剪掉每段开头结尾的空白（每段前留 0.3 秒）。
2. **字幕**：选"文本 → 智能字幕 → 识别字幕"（英文识别），再逐条改错字。改完导出时要**勾选"烧录到视频"**。
3. 音量：旁白拉到 -3 dB 左右；如果录进了键盘声，用"降噪"。
4. 导出：1080p / 30fps / mp4。

## 五、发布与挂链接

1. 上传到 **B 站**（或 YouTube 设为 Unlisted）。
2. 标题：`Steel Surface Defect Detection — YOLOv8 on NEU-DET (2 min demo)`
3. 简介里放仓库地址：`https://github.com/ASylviaofmine/defect-detection`
4. 把视频链接写进 README §4.5：

```markdown
▶ [2-minute demo (video)](https://www.bilibili.com/video/xxxxx)
```

---

## 六、容易翻车的 6 个点

1. **中途才启动服务** → 前 23 秒黑屏无输出（`import torch` 10.8 s + 首张推理 8.9 s）。先起好再录。
2. **终端字号太小** → 手机上看不清。宁大勿小。
3. **念稿太快** → 英文旁白比中文慢，每句之间停半秒，剪的时候好切。
4. **滑块一下拉到底** → 观众看不清"7 变 4"的过程。慢慢拉，停 1 秒再点 Submit。
5. **只放成功案例** → 看起来像作业。镜头 7 那段（crazing 只有 3 个弱框）必须留。
6. **忘了关通知** → 弹窗出现一次就得重录整段。

---

## 七、万一英文念不顺

退而求其次：**中文旁白 + 英文硬字幕**。评审看的是内容，字幕一样能读。但英文旁白在申请里是加分项——如果能念，就念。

判断标准：**先完整念一遍镜头 5**（最长那段）。如果卡超过两次，就换中文旁白，别硬撑。
