"""把论文 PDF 拆成：逐页文字 + 逐页整页 PNG（160 dpi）。

用法：
    D:\\anaconda\\python.exe pdf_extract.py <论文.pdf> <输出目录>

输出：
    <输出目录>\\text.txt        每页以 "===== PAGE n =====" 分隔的文字层
    <输出目录>\\p<n>.png        每页整页图，160 dpi，坐标系供 pdf_crop.py 使用
    stdout                      页数、每页尺寸、每页嵌入位图个数（位图多的页通常有芯片照片/示波器截图）
"""
import sys
from pathlib import Path

import pymupdf

DPI = 160


def main(pdf_path: str, out_dir: str) -> None:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    doc = pymupdf.open(pdf_path)
    parts = []
    for i, page in enumerate(doc, start=1):
        parts.append(f"\n\n===== PAGE {i} =====\n")
        parts.append(page.get_text("text"))
        pix = page.get_pixmap(dpi=DPI)
        pix.save(out / f"p{i}.png")
        n_img = len(page.get_images(full=True))
        print(f"page {i}: {pix.width}x{pix.height} px @ {DPI} dpi, embedded images = {n_img}")
    (out / "text.txt").write_text("".join(parts), encoding="utf-8")
    print(f"pages = {len(doc)}, text chars = {sum(len(p) for p in parts)}")
    print(f"written to {out}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
