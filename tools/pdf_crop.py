"""按坐标从 PDF 某一页裁一张高清图（300 dpi），用来嵌进笔记。

坐标用 pdf_extract.py 生成的 160 dpi 整页图 p<n>.png 上的像素位置，
即「你在整页图上看到的位置」，脚本自动换算成 PDF 坐标。

用法：
    D:\\anaconda\\python.exe pdf_crop.py <论文.pdf> <页码> <x0> <y0> <x1> <y1> <输出.png>

例：
    D:\\anaconda\\python.exe pdf_crop.py paper.pdf 9 150 120 1200 730 "E:\\...\\assets\\Zheng-2024-table3.png"

也可以一次裁多张：把多行 "页码 x0 y0 x1 y1 输出文件名" 写进一个文本文件，然后
    D:\\anaconda\\python.exe pdf_crop.py <论文.pdf> --batch <列表.txt> <输出目录>
"""
import sys
from pathlib import Path

import pymupdf

SRC_DPI = 160   # 与 pdf_extract.py 一致
OUT_DPI = 300


def crop(doc, page_no: int, x0: float, y0: float, x1: float, y1: float, out_path: Path) -> None:
    page = doc[page_no - 1]
    k = 72.0 / SRC_DPI
    rect = pymupdf.Rect(x0 * k, y0 * k, x1 * k, y1 * k) & page.rect
    pix = page.get_pixmap(dpi=OUT_DPI, clip=rect)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    pix.save(out_path)
    print(f"page {page_no} [{x0},{y0},{x1},{y1}] -> {out_path.name} ({pix.width}x{pix.height})")


def main(argv) -> None:
    pdf = argv[1]
    doc = pymupdf.open(pdf)
    if argv[2] == "--batch":
        list_file, out_dir = Path(argv[3]), Path(argv[4])
        for line in list_file.read_text(encoding="utf-8-sig").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            p, x0, y0, x1, y1, name = line.split(maxsplit=5)
            crop(doc, int(p), float(x0), float(y0), float(x1), float(y1), out_dir / name)
    else:
        p, x0, y0, x1, y1, out = argv[2:8]
        crop(doc, int(p), float(x0), float(y0), float(x1), float(y1), Path(out))


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print(__doc__)
        sys.exit(1)
    main(sys.argv)
