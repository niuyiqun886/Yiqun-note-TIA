# 论文阅读 · AI 操作手册 + 启动提示词

> 这份文件是给 AI 看的完整操作流程。2026-09-16 读 Zheng 2024 那篇时实际走的就是下面这些步骤，脚本已固化在 `tools\` 里，照做即可复现同样质量的笔记。
> 人只需要复制最下面「启动提示词」那几行，改 PDF 路径和文件名。

---

## 0. 环境事实（先读，别再探测）

| 项 | 事实 |
|---|---|
| Python | `D:\anaconda\python.exe`（3.13），已装 `pymupdf`。**PATH 里的 `python`/`python3` 是 Windows 商店空壳，运行无输出，不要用** |
| 脚本 | `E:\Transimpedance Amplifier(TIA)\tools\pdf_extract.py`、`pdf_crop.py`（用法见第 2 步） |
| 模板 | `E:\Transimpedance Amplifier(TIA)\论文阅读模板.md` |
| 笔记目录 | `E:\Transimpedance Amplifier(TIA)\Transimpedance Amplifier(TIA)\` |
| 图片目录 | 笔记目录下的 `assets\` |
| 风格参考 | 笔记目录下 `论文阅读2024-Xiaoxiao Zheng.md`（最新、最完整）、`Ai填写的论文阅读.md` |
| 路径别名 | 用户说的 `E:\笔记\` 就是 `E:\Transimpedance Amplifier(TIA)\`，磁盘上没有 `E:\笔记` |
| 中文路径 | Bash 会把中文路径弄成乱码。**跑命令用 PowerShell，读写文件用 Read / Write / Edit 工具** |
| 临时文件 | 放 scratchpad，不要放笔记目录 |
| 没有的东西 | poppler / pdftoppm 没装；PDF 工具 MCP 服务器的 allowedDirectories 是空的，用不了 |

---

## 1. 读模板和风格参考（5 分钟）

1. Read 完整读一遍 `论文阅读模板.md`，记住当前版本有哪些问题（含 Q3b / Q26b / Q26c / A16–A18 / B4 陷阱）。
2. Read 一遍 `论文阅读2024-Xiaoxiao Zheng.md`，看清三件事：每个问题答到什么深度、【我算的】/【读图】标记怎么用、图片怎么嵌（`![[Zheng2024-xxx.png]]`）。
3. 从文件名取「第一作者-年份」作为图片前缀，例如 `Zheng2024-`。

---

## 2. 拆 PDF：文字 + 整页图（2 分钟）

```powershell
$py  = "D:\anaconda\python.exe"
$t   = "E:\Transimpedance Amplifier(TIA)\tools"
$pdf = "<论文 PDF 完整路径>"
$out = "<scratchpad>\paper"
& $py "$t\pdf_extract.py" $pdf $out
```

得到 `$out\text.txt`（每页以 `===== PAGE n =====` 分隔）和 `$out\p1.png … pN.png`（160 dpi 整页图，1360×1760 左右）。stdout 会打印每页嵌入位图个数，位图多的页通常是芯片照片 / 示波器截图 / 实物图。

---

## 3. 读论文（这是主要时间）

**3a. 先读全文文字**：Read `text.txt`。一次读完，公式会被拆成碎行，凭上下文拼。记下每张图、每张表在第几页。

**3b. 再逐页看图**：用 Read 工具打开 `p<n>.png`。**表格和电路图在文字层里是没有的，只能看图**。至少要亲眼看到：

- 末页对比表（Table 对比表）——逐列抄数
- 系统框图（PD → 输出整链）
- 核心电路图（TIA 那张）+ 器件尺寸表（如果有）
- 直流消除 / AGC / 补偿等创新点的电路图
- 各档性能表
- 频响图、噪声测试截图、线性度 / DR 图、功耗分解图
- 测试台框图（判断电学还是光学）

看图时读数：曲线上的 −3 dB 点、最低测试点、拐点。**读出来的数字在笔记里标【读图】**。

**3c. 看不清的局部**：用 `pdf_crop.py` 按坐标裁 300 dpi 小图再看（坐标就是你在 160 dpi 整页图上看到的像素位置，四边各留 10–20 px 余量）：

```powershell
& $py "$t\pdf_crop.py" $pdf <页码> <x0> <y0> <x1> <y1> "<scratchpad>\zoom.png"
```

---

## 4. 裁图进笔记库（5 分钟）

把要嵌进笔记的图一次性裁出来，直接存到 `assets\`。写一个列表文件（每行 `页码 x0 y0 x1 y1 文件名`，用 Write 工具写，UTF-8），然后批量裁：

```powershell
& $py "$t\pdf_crop.py" $pdf --batch "<scratchpad>\crops.txt" "E:\Transimpedance Amplifier(TIA)\Transimpedance Amplifier(TIA)\assets"
```

列表示例（Zheng 2024 那篇实际用的坐标，供估位置参考；A4 双栏论文左栏约 x 100–680，右栏约 x 690–1250）：

```
3  100 110  680 460  Zheng2024-fig02_block_diagram.png
4  100 110  680 650  Zheng2024-fig04_DCSF-TIA.png
4  100 690  680 900  Zheng2024-table1_device_sizes.png
4  690 110 1250 470  Zheng2024-fig05_dc-SFP.png
7  690 370 1250 730  Zheng2024-fig13_freq_resp_SCR.png
8  100 110  680 410  Zheng2024-fig15_dc_lf_response.png
8  100 870  680 1060 Zheng2024-table2_gain_modes.png
9  150 120 1200 740  Zheng2024-table3_comparison.png
```

裁完 Read 几张确认没裁掉边。通常 10–14 张：对比表、框图、核心电路、创新点电路、尺寸表、性能表、频响、噪声、DR/线性度、功耗。

---

## 5. 核算数字（10 分钟，写笔记之前做）

用 Python 或 node 把下面这些算一遍，结果直接进 Q17–Q20 和 B 组：

```
dB → Ω：10^(dB/20)
B4 陷阱：(I_n,rms / i_n,密度)^2 是否 = f-3dB（=砖墙换算；是的话密度列标「换算值」，再按 1.11×f-3dB 和 π/2×f-3dB 重算）
每一档都验：nA_rms / sqrt(BW) 是否等于表里的 pA/√Hz
它给的输入折合噪声公式：代它的数重算一遍，看用的是差分还是单端、×2 还是 ×√2
功耗加法：电流 × 电压；分解各项求和是否等于总功耗；核心放大器电流 × 电压 ≈ TIA 功耗则辅助环路功耗可忽略
DR：20·log(Imax/Imin)；单档 DR 从图上读端点算
FoM：按它的公式代数，看用的 Gain 是哪个值
B5：MDS / I_n,rms = 几个 σ；若 MDS 是正弦幅度再 ÷√2
R_F 噪声下限：R_F ≥ 4kT / i_n^2
口径反推：若 Z_T 全在 TIA 单级，R_F·C_d 极点和 BW 要求的 GBW 是多少；超过 20–30 GHz（0.18 μm）就说明 Z_T 是整链
器件估算：由尺寸表和偏置估 g_m（√(2μC_ox(W/L)I)）、C_gs（⅔·W·L·C_ox，0.18 μm 取 8.6 fF/μm²）、A_v 各级
FMCW / dToF 特有：拍频 kHz/m、高通角对应最近距离、被消除直流的散粒噪声 √(2qI)、消除电流源的 4kTγg_m
```

**每一个我算的数都在笔记里标【我算的】并给公式和中间值。**

---

## 6. 写笔记（30–40 分钟）

文件：`E:\Transimpedance Amplifier(TIA)\Transimpedance Amplifier(TIA)\论文阅读<年份>-<第一作者名>.md`，用 Write 工具一次写完。结构 = 模板全部章节，逐题填。规矩：

1. 顶部三行声明：AI 填写、哪些图看到了 / 没看到、【我算的】要复核。
2. **每个「答：」都有内容**。论文没说的写「未说明」，不猜；能给证据的「未说明」要给证据（例如：为什么判断 Z_T 是整链）。
3. 论文原话用引号引英文；自己推的标【我算的】；从图上读的标【读图】。
4. **Q3 末页对比表逐列过**：它每一列排第几、赢的到底是哪一列。**Q3b** 写它的 FoM 分子分母各有什么、故意漏了什么。
5. **Q11–Q15 先猜后对**：按电路图 + 器件尺寸自己估 g_m / C_gs / A_o / R_in / 极点 / 噪声主项，再写作者怎么说，再写「差在」。
6. **Q13 专门查噪声模型漏了谁**（消除电流源、被消除电流的散粒噪声、后级、缓冲）。
7. **Q16 手抄图留空**，但把三处该标注的内容写好。
8. **Q17–Q20 至少复现三个数**（第 5 步的结果），每个给公式、中间值、结论勾选框。
9. **Q22 / Q23** 写它回避的问题和图与图之间对不上的地方；Q23 分「电路一侧 / 噪声口径一侧 / 系统一侧」，标出哪条最值钱。
10. **六 口径核对** 全答，含 Q26b（噪声在什么直流 / 背景条件下测的）、Q26c（电学还是光学、C_d 是板上电容还是真 PD）。
11. **七 A 组 A1–A18 全填**，要打星号的格子在「注意」列写 🚩 和原因；B 组注明整链 / 单级口径，并跟已有笔记里的论文横向比一句。
12. **八 给用户的三条即时结论**：① 对 TIA/dToF 主线真正有用的一件事 ② 哪些数不能直接抄进总表 ③ 可以变成选题种子的洞。
13. 图片嵌入用 `![[<前缀>-xxx.png]]`，放在对应问题下面。

---

## 7. 模板要不要改（5 分钟）

如果这篇论文暴露了模板没覆盖的字段（例如低频截止、直流处理、测试条件），直接 Edit 模板：新问题用 `Q<n>b` 后缀，新字段接在 A 组末尾，B 组补注意事项。**不改旧编号**，旧笔记引用不会断。

---

## 8. 验证 + 汇报（3 分钟）

```powershell
$f = "<笔记完整路径>"; $a = "E:\Transimpedance Amplifier(TIA)\Transimpedance Amplifier(TIA)\assets"
$t = Get-Content $f -Raw -Encoding UTF8
[regex]::Matches($t, '!\[\[([^\]]+)\]\]') | % { $n = $_.Groups[1].Value; "$(Test-Path (Join-Path $a $n))  $n" }
```

全部 True 才算完。最后回复用户：三个最要紧的结论、哪些数是【读图】需要复核、模板改了什么、笔记和图片存在哪。

---

## 启动提示词（复制这块，改前两行）

```
论文 PDF：<E:\Zotero\storage\XXXX\xxx.pdf>
文件名：论文阅读<年份>-<第一作者名>.md

先完整读 E:\Transimpedance Amplifier(TIA)\论文阅读-AI提示词.md，那是操作手册。
然后严格按手册第 0–8 步执行，把这篇论文读透、用模板填一份笔记、配图裁进 assets、验证后汇报。
环境事实已在手册第 0 节，不要再探测 Python 和路径。
```

---

## 备注

- 2026-09-16 第一次做（Zheng 2024）。当时没找到 Anaconda 绕去用 Node 的 pdfjs + mupdf 包，pdfjs 渲染有几页段错误；之后装了 pymupdf 并固化成 `tools\` 两个脚本，上面流程是用脚本重跑验证过的。
- 另一条路：把 `E:\Zotero\storage` 加进 `C:\Users\86186\.pdf-tools\config.json` 的 `allowedDirectories` 并重启，PDF 工具 MCP 就能直接读；目前没配。
