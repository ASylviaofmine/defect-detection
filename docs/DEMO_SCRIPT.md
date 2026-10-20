# Demo video — 分镜脚本与录制说明

> 目标：1 分 50 秒～2 分 10 秒，**英文旁白 + 英文硬字幕**，1920×1080。  
> 用途：README §4.5 嵌入 + 申请材料里作为"可点开的东西"。  
> 原则：**每个数字都必须能在仓库里找到出处**；失败案例要说，不要剪掉。

---

## 一、录制前准备（10 分钟，别省）

| 项       | 做法                                                                            |
| ------- | ----------------------------------------------------------------------------- |
| 关掉干扰    | 微信 / QQ / 邮件通知全关；Windows「专注助手」设为"仅闹钟"                                         |
| 清桌面     | 桌面上 `samples` 文件夹保留（要用），其它图标别入镜                                               |
| 终端字号    | 终端里 `Ctrl + 滚轮上`，调到镜头前能看清（约 18~20 号）                                          |
| 浏览器     | 缩放保持 100%，关掉书签栏（`Ctrl+Shift+B`）                                               |
| 服务先起好   | 在仓库根目录 `python app.py`，确认 <http://127.0.0.1:7860> 能打开，**别在录制中途启动**（有 23 秒无输出） |
| 预先打开的窗口 | ① `app.py` 的网页 ② README 的 §4.2 表格 ③ 终端（跑 audit 的输出）                           |
| 稿子      | 放在手机或另一块屏上；**不要**放在要录的屏幕里                                                     |
| 试录 10 秒 | 先录一段，回放确认：声音有、字看得清、没弹窗                                                        |

---

## 二、分镜表

> 英文是**照着念的**，中文只是帮你理解意思，不用念。  
> 每段单独录，录坏了只重录那一段。

### 镜头 1 ｜ 0:00–0:08 ｜ 画面：一张钢材缺陷图铺满（`docs/samples/crazing_271.jpg`）

**EN**：Every steel strip is inspected by eye before it ships. At line speed that is thousands of sheets per shift, and attention is the bottleneck.

**中**：每一条钢带出厂前都靠人眼看。按产线速度，一个班要看几千片——瓶颈是人眼能撑多久。

---

### 镜头 2 ｜ 0:08–0:16 ｜ 画面：六类对照图 `docs/figures/six_classes.png`（1356×1116，英文标签，专为视频生成）

> 展示方法：把图拖进浏览器，按 **F11** 全屏——居中且够大。录完按 F11 退出。
> 原始小图 `tools/neu_det_samples.png`（648×544，中文标签）仍在仓库里，供日常查样本用。

**EN**：NEU-DET defines six surface defect classes: crazing, inclusion, patches, pitted surface, rolled-in scale and scratches.

**中**：NEU-DET 定义了六类表面缺陷：裂纹、夹杂、斑块、麻点、氧化皮压入、划痕。

---

### 镜头 3 ｜ 0:16–0:32 ｜ 画面：`docs/figures/canny_threshold_problem.png`（1228×1002，英文标注，专为视频生成）

> 展示方法：拖进浏览器 → **F11** 全屏。上下两行对比就是论据本身，不用额外解释。
> （day9 的原始输出 `practice/out/real_canny_*.png` 是 200×200 的裸边缘图，单看没有说服力。）

**EN**：I started with Canny. One threshold floods a crazing image — 38 percent of pixels lit — or misses an inclusion at 0.6 percent. No single threshold serves six classes. That measurement is why I moved to a learned detector.

**中**：我先试了 Canny。同一个阈值，在裂纹图上点亮 38% 的像素，在夹杂图上只抓到 0.6%。一个阈值伺候不了六类缺陷——这个实测结果就是我转向深度学习的原因。

---

### 镜头 4 ｜ 0:32–0:46 ｜ 画面：终端里 `tools/audit_dataset.py` 的**已完成输出**

> ⚠️ 这个检查跑一次要 **34 秒**（要读 1800 个 XML），镜头只有 14 秒旁白，**不能现场跑**——画面会变成干等。
> 做法：**先跑完，再录屏幕上已经显示的结果。**

具体步骤：

1. 打开一个终端，**最大化**窗口，字号调到能看清（`Ctrl + 滚轮`）。
2. 先跑一次，让输出留在屏幕上：
   ```bash
   python tools/audit_dataset.py
   ```
3. 等它打印出 `体检通过 ✓  可以开训练了`，**不要清屏**。
4. 紧接着在同一个终端里录（这里必须加 `--keep-console`，否则终端会被自动最小化，audit 的输出就跟着消失了）：
   ```bash
   python tools/record_demo.py s4 --seconds 17 --keep-console
   ```
5. 倒计时结束后念旁白，鼠标**别乱动**，也不要挡住 `189 / 4189 / ✓` 那几行。

> 想在画面上更干净：另开一个终端（Windows Terminal）跑录制命令，让 PyCharm 的"运行"标签页显示 audit 输出。这样录制终端会被自动最小化，画面里只剩结果。

**EN**：Before training, I audited all 1,800 images: 4,189 boxes, labels paired one to one, every row valid. Of the 1,620 training images, only 452 — 28 percent — hold a single defect. This is multi-instance detection, not one box per image.

**中**：训练前我先给 1800 张图做了体检：4189 个框、图签一一对应、每一行都合法。1620 张训练图里，只有 452 张、也就是 28%，是单个缺陷——这是多实例检测，不是一图一框。

---

### 镜头 5 ｜ 0:46–1:08 ｜ 画面：`docs/figures/metrics_4_2.html`（拖进浏览器 + F11，与镜头 2/3 同一套操作）

> **素材出处：`docs/figures/metrics_4_2.html`** —— 录屏专用单页，内容与 README §4.2（第 122–147 行）**一字不差**，字号为 1080p 调好，一屏放得下，不用找行号。
> 为什么不直接拍 README：PyCharm 的**预览模式没有行号**，§4.2 的表有 10 列、在预览里又小又挤，还要防着别滚进 §4.3 的大图——不稳定因素太多。

具体步骤：

1. 资源管理器里把 `docs/figures/metrics_4_2.html` **拖进浏览器** → **F11** 全屏。
2. 开录：`python tools/record_demo.py s5 --seconds 25`
3. 倒计时结束后念旁白，按下面的节奏轻轻滚动（页面结构：上=三行数据表，下=confirmed / refuted 两张卡）：

| 时间 | 画面 | 旁白进度 |
| --- | --- | --- |
| 0–10 s | 停在顶部表格，`A / B / C` 三行全在画面里 | "…26 minutes … mAP 0.758 … 0.766" |
| 10–17 s | 慢滚到下方两张卡，绿边 **CONFIRMED** 卡 | "lifted the hardest class, crazing, from 0.46 to 0.55" |
| 17–25 s | 停在橙边 **REFUTED** 卡（"200 × 200 … nothing to recover"） | "changed crazing by zero … nothing to recover" |

> 备选（方案 B）：PyCharm 打开 `README.md` → 预览模式 → 预览字号调到 20~22 → 滚到标题 "4.2 Quantitative metrics (measured)"。需要最大化窗口（表格 10 列），且**只滚到 `Source of truth: runs/detect/compare_report.md` 那行就停**，再往下是 §4.3 的全屏大图。

**EN**：Fine-tuning YOLOv8n for a hundred epochs took 26 minutes on a laptop GPU and reached mAP 0.758. A larger backbone reached 0.766, and lifted the hardest class, crazing, from 0.46 to 0.55. Raising input resolution to 960 changed crazing by zero — the images are 200 pixels square, so there was nothing to recover.

**中**：在笔记本 GPU 上微调 YOLOv8n 一百轮，26 分钟，mAP 0.758。换更大的骨干网络到 0.766，把最难的裂纹类从 0.46 提到 0.55。但把输入分辨率提到 960，裂纹类一点没变——原图只有 200×200，没有信息可以找回来。

---

### 镜头 6 ｜ 1:08–1:35 ｜ 画面：网页 demo，拖入 `docs/samples/scratches_271.jpg` → 7 个框 → 滑块拉到 0.50 → 4 个框

> **素材出处：`docs/samples/scratches_271.jpg`**（也是页面下方**第 2 个示例图**，点它比拖拽更稳，见下面的备选方案）。
> **实测数字（刚复核过）**：conf 0.25 → **7 框**（0.76 / 0.70 / 0.66 / 0.51 / 0.34 / 0.30 / 0.28）；conf 0.50 → **4 框**（0.76 / 0.70 / 0.66 / 0.51）。真值也是 4 个。
> 顺手能讲的一个点：第 4 个框 0.51、第 5 个 0.34，**中间有断档**——阈值 0.50 正好落在缝里，所以不是"硬凑"出来的 4。

**录制前必须做完（否则 30 秒里会有一段死等）**

1. 在 `defect_detection` 目录起服务：`python app.py`
2. **等约 25 秒**（torch 10.8 s + ultralytics 3.4 s），看到 `Running on local URL: http://127.0.0.1:7860` 再往下。
3. 浏览器打开 `http://127.0.0.1:7860`，**先把图拖进去点一次 Submit 热身**——首次推理要 8.9 秒，之后 0.05 秒。热身完清掉结果（图片框右上角 × ），保持空页面待录。
4. 浏览器**最大化**，再按 `Ctrl` + `=` 放大 2~3 档，让两栏内容占满画面（默认宽度只占中间一窄条）。

**录制**

5. 开录：`python tools/record_demo.py s6 --seconds 30`
6. 倒计时结束后按节奏操作：

| 时间 | 操作 | 旁白进度 |
| --- | --- | --- |
| 0–6 s | 把 `scratches_271.jpg` 拖进左上"上传"框（**别拖到地址栏**），点 **Submit** | "Here it is running…"（先让 7 个框出现在画面上） |
| 6–9 s | 手离开鼠标，停住 | "This image has four defects. At the default threshold the model reports seven" |
| 9–20 s | 把滑块从 0.25 **慢慢**拖到 0.50（画面数字跟着变） | "…at 0.50 it reports exactly four" |
| 20–22 s | 点 **Submit** | 停半秒 |
| 22–30 s | 手离开鼠标，停在结果页（4 个框 + 下方 Summary 文字） | "The trade-off between missing a defect and raising a false alarm is visible, not hidden." |

> ⚠️ **滑块改完必须再点一次 Submit**，Gradio 不会自动重跑。这是最容易录废的一步。
> ⚠️ 端口 7860 若被占（以前踩过）：`netstat -ano | findstr :7860` 查到 PID 后 `taskkill /PID <pid> /F`，再重启 `python app.py`。
> 备选（更稳、少 3 秒拖拽风险）：直接点页面下方**第 2 个示例图**（就是 `scratches_271.jpg`），Gradio 会自动填入并跑到 7 框；然后拉滑块 + Submit。缺点是不如"拖入"像真人在用。

**EN**：Here it is running. This image has four defects. At the default threshold the model reports seven; at 0.50 it reports exactly four. The trade-off between missing a defect and raising a false alarm is visible, not hidden.

**中**：这是它在跑。这张图实际有 4 个缺陷。默认阈值下模型报了 7 个，把阈值提到 0.50 正好报 4 个。"漏检"和"误报"之间的取舍，是可以看见的，不是藏起来的。

---

### 镜头 7 ｜ 1:35–1:50 ｜ 画面：同一个网页，拖入 `docs/samples/crazing_271.jpg` → 只有 3 个低置信度框

> **素材出处：`docs/samples/crazing_271.jpg`**（页面下方**第 1 个示例图**）。
> **实测数字**：conf **0.25 → 3 框**，置信度 **0.47 / 0.29 / 0.26**（三个都不高，两个低于 0.3）；标签文件里真值是 **4 框**，所以这是**漏了 1 个**，不是认错类。
> **这一镜不用重启服务**——`app.py` 一直开着，浏览器别关，画面才和镜头 6 连续。

**⚠️ 录之前第一件事：把滑块拉回 0.25。**
镜头 6 录完滑块停在 **0.50**，而 `crazing_271` 在 0.50 下输出 **0 个框**（实测）。忘了这一步，画面会显示"未检测到缺陷"，和旁白 "three weak boxes" 直接矛盾，整段作废。

**步骤**

1. 浏览器回到 `http://127.0.0.1:7860`（确认还是同一个窗口、缩放没变）。
2. 清空上一镜的 images：图片框右上角 **×**；**滑块拖回 0.25**。
3. 开录：`python tools/record_demo.py s7 --seconds 18`
4. 倒计时结束后：

| 时间 | 操作 | 旁白进度 |
| --- | --- | --- |
| 0–5 s | 拖入 `crazing_271.jpg` → 点 **Submit** | "On the hardest class…" |
| 5–10 s | 手离开鼠标，停住，让 3 个框和框上的 0.47 / 0.29 / 0.26 入镜 | "…it finds only three weak boxes." |
| 10–18 s | 不动。想再强调就把鼠标移到下方 Summary（"裂纹 × 3"） | "I show this on purpose: the failure mode is misses, not wrong labels." |

> 想更有说服力但**不建议开口说**：真值是 4 框。口头提"four"而画面上只有 3 个框，观众反而找不到依据——这个数字留给 §4.3 的每类 AP 表和混淆矩阵去支撑。

**EN**：On the hardest class it finds only three weak boxes. I show this on purpose: the failure mode is misses, not wrong labels.

**中**：在最难的那类上，它只报出 3 个把握不大的框。我是故意放这段的——它的失败方式是"漏"，不是"认错"。

---

### 镜头 8 ｜ 1:50–2:05 ｜ 画面：`docs/figures/limitations_5.html`（拖进浏览器 + F11，与镜头 5 同一套操作）

> **素材出处：`docs/figures/limitations_5.html`** —— 录屏专用单页，内容与 README §5（9 条 Limitations）一字不差，**一屏放得下，不用滚动**。旁白点到的条目（1 小数据集 / 3 单一采集设备 / 5 无独立测试集 / 8 无边缘端延迟）有蓝色高亮条。
> 为什么不直接拍 README：预览模式没有行号、字号小、9 条超过一屏必须滚——15 秒里滚这么密的技术文本，观众一个字都读不进。

**步骤**

1. 把 `docs/figures/limitations_5.html` 拖进浏览器 → **F11** 全屏。
2. 开录：`python tools/record_demo.py s8 --seconds 18`
3. 倒计时结束后念旁白。**全程不需要动鼠标**——让画面完全静止，这 15 秒是"诚实时刻"，越稳越好：

| 时间 | 画面 | 旁白进度 |
| --- | --- | --- |
| 0–12 s | 静止在第 1 条（高亮："…an upper bound for this benchmark, not a production estimate"） | "All of this was measured on a 180-image validation split from one acquisition setup — a benchmark result, not a production estimate." |
| 12–18 s | 鼠标轻移到底部斜体一行（"Next: an independent held-out test protocol, and latency on production edge hardware."） | "Next: a held-out test protocol and edge latency." |

> 旁白里 "180 images" 比 README 第 1 条的 "1800 images" 容易听混——**说的是验证集 180 张**，不是数据集 1800 张，所以 EN 已写成 "a 180-image validation split"。念的时候 180 后面稍微停半拍。
> 高亮条是画面提示，不需要在旁白里解释。

**EN**：All of this was measured on a 180-image validation split from one acquisition setup — a benchmark result, not a production estimate. Next: a held-out test protocol and edge latency.

**中**：这些数字都来自同一台设备拍的 180 张验证图——是基准成绩，不是产线估计。下一步是做独立测试集和边缘设备延迟测试。

---

### 镜头 9 ｜ 2:05–2:12 ｜ 画面：GitHub 仓库首页

**EN**：The data audit, training scripts and failure analysis are all in the repository.

**中**：数据体检脚本、训练脚本和失败分析，都在仓库里。

---

## 三、怎么录（用仓库自带的 `tools/record_demo.py`）

> **为什么不用 Win+G：** 本机实测 Game Bar 的麦克风链路有故障——界面显示 Mic On、设备也选对了，但导出的音轨是数字静音（`mean_volume -91 dB`）。用 ffmpeg 直采同一支麦克风是 `-18 dB`，说明麦克风本身正常，问题在 Game Bar 采集层。
> `tools/record_demo.py` 用 ffmpeg 同录屏幕 + 麦克风，**录完自动报告音量 dB**，不会再出现"录了 20 分钟才发现没声音"。

### 一次性的准备（只做一次）

```bash
cd C:\Users\Lee\WorkBuddy\2026-09-21-21-29-56\defect_detection
pip install --user imageio-ffmpeg          # 已装过可跳过
python tools/record_demo.py --list         # 确认能看到「麦克风阵列 (Realtek(R) Audio)」
```

### 每一段的标准流程

1. **摆好画面**：切到这一段要录的窗口，`F11` 让浏览器全屏。
2. **最小化所有不该入镜的窗口**（WorkBuddy 聊天窗、微信、资源管理器）——录的是整个桌面。
3. 在终端运行下面对应的命令。
4. 看到 `3... 2... 1...` 时**准备好讲话**；终端会自动最小化，不进画面。
5. 按旁白念，同时做动作。
6. 到时间自动停止，终端弹回，显示 `✓ 音量 -2x dB` —— 看到这个才算成功。

### 九段视频的命令（时长已含 3 秒余量）

```bash
python tools/record_demo.py s1 --seconds 11
python tools/record_demo.py s2 --seconds 11
python tools/record_demo.py s3 --seconds 19
python tools/record_demo.py s4 --seconds 17 --keep-console   # audit 输出要留在屏幕上,不能让终端最小化
python tools/record_demo.py s5 --seconds 25
python tools/record_demo.py s6 --seconds 30
python tools/record_demo.py s7 --seconds 18
python tools/record_demo.py s8 --seconds 18
python tools/record_demo.py s9 --seconds 10
```

文件输出到 `C:\Users\Lee\Videos\Captures\s1.mp4` …… `s9.mp4`。

### 录完自检

每段录完都会打印一行，三种情况：

| 输出 | 含义 | 处理 |
| --- | --- | --- |
| `✓ 音量 -20 dB` | 正常 | 继续下一段 |
| `⚠ 音量 -91 dB` | 静音 | 重录；先确认没有别的程序占用麦克风 |
| `⚠ 音量 -3 dB` | 太响/爆音 | 离电脑远一点重录 |

想回看某段：直接双击 `Videos\Captures\sN.mp4`。分辨率是屏幕原生的 2560×1600，30 fps。

> 不想用脚本、坚持用 Win+G 也可以，但**录完必须播一遍确认有人声**——本机已经证明它会静默产出无声文件。

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
