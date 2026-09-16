# 论文阅读 · AI 填写提示词（复制下面整块，改前两行）

```
论文 PDF：<Zotero 路径，例如 E:\Zotero\storage\XXXX\xxx.pdf>
文件名：论文阅读<年份>-<第一作者名>.md

请按下面的规矩把这篇论文读透，用我的模板填一份笔记。

【路径】
- 模板：E:\Transimpedance Amplifier(TIA)\论文阅读模板.md（先完整读一遍，按最新版填，含 Q3b / Q26b / Q26c / A16–A18）
- 笔记存到：E:\Transimpedance Amplifier(TIA)\Transimpedance Amplifier(TIA)\
- 配图存到：同目录下的 assets\，文件名前缀「<第一作者>-<年份>-」，笔记里用 ![[文件名]] 嵌入
- 参考风格：同目录下「Ai填写的论文阅读.md」和「论文阅读2024-Xiaoxiao Zheng.md」
- 注意：我说的 E:\笔记\ 就是 E:\Transimpedance Amplifier(TIA)\，不要去找 E:\笔记

【读 PDF 的方法】（PATH 里的 python 是 Windows 商店空壳，别用；poppler 没装；PDF 工具服务器没配目录）
- 用 Anaconda 的 Python：D:\anaconda\python.exe，已装 pymupdf（import pymupdf）
- 文字层：doc[i].get_text() 逐页抽，存成 txt 再读
- 图表：doc[i].get_pixmap(dpi=160) 存 PNG 看全页，关键图用 clip=fitz.Rect(...) 按 dpi=300 裁出来，再用 Read 工具看图
- 用 PowerShell 或 Read/Write 工具处理中文路径，Bash 会把中文路径弄成乱码
- 必须亲眼看到：末页对比表、系统框图、核心电路图、器件尺寸表、各档性能表、噪声/频响/线性度测试图、功耗分解。看不到的格子标「⚠️ 图未提取」，不要编

【填写规矩】
1. 从上往下填全部问题，中文。每个「答：」都要有内容，论文没说的写「未说明」，不猜
2. 所有你自己推的数字标【我算的】，读图读出来的数字标【读图】，论文原话用引号引英文原文
3. Q16 手抄图留空，但把三处该标注的内容写好供我抄的时候填
4. Q11–Q15 先按电路图 + 器件尺寸自己估（gm、Cgs、Ao、Rin、极点位置），再对作者，写清「差在」哪
5. Q17–Q20 至少复现三个数：B4 噪声自洽（先算 (I_rms / i_n)^2 是不是恰好等于 f-3dB，判断密度是不是换算值）、B5 灵敏度反推、以及功耗/DR/FoM 这类加法。每个都列公式和中间值
6. 口径核对是重点，每个都要给证据：Z_T 是单级还是整链（用 GBW 反推 R_F 能不能成立）、噪声是密度还是积分值、噪声在什么直流/背景条件下测的、带宽是电学还是光学、C_d 是板上电容还是真 PD、MDS 是几个 σ
7. 找它的漏洞：噪声模型漏了哪个器件、图和图之间对不上的地方（比如小信号响应和大信号钳位矛盾）、FoM 里故意没放的量。找到了在 Q22/Q23 和第八节里单独讲
8. 第八节写「给我的三条即时结论」：① 这篇对我 TIA/dToF 主线真正有用的一件事 ② 哪些数不能直接抄进总表、要打星号 ③ 可以变成选题种子的洞
9. A 组、B 组表全部填，B 组注明口径（整链/单级），并跟已有笔记里的论文横向比一句

【模板本身】
如果模板缺了这篇论文才暴露出来的字段，直接改模板，新问题用 Q<n>b 后缀编号、新字段接在 A 组末尾，不要改旧编号

【最后】
- 用 Bash/PowerShell 验证一遍笔记里所有 ![[...]] 指向的图片文件存在
- 回复里告诉我：三个最要紧的结论、哪些数是你读图读的需要我复核、模板改了什么
```

---

## 备注

- 第一次用这个提示词是 2026-09-16，Zheng 2024 那篇。当时踩的坑：Bash 处理中文路径乱码（用 PowerShell 或 Read 工具）；一开始没找到 Anaconda（在 D:\anaconda，不在 PATH），绕去用 Node 的 pdfjs + mupdf 包才读到图；之后已把 pymupdf 装进 D:\anaconda 的 base 环境，直接用即可。
- 另一条路：把 `E:\Zotero\storage` 加进 `C:\Users\86186\.pdf-tools\config.json` 的 `allowedDirectories` 并重启，PDF 工具服务器就能直接读文字和渲染页面。
