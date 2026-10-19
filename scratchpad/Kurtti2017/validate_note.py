import json
import re
from pathlib import Path
import pymupdf

root = Path(r'E:\Transimpedance Amplifier(TIA)')
note = root / 'Transimpedance Amplifier(TIA)' / '论文阅读2017-Kurtti.md'
assets = note.parent / 'assets'
template = root / '论文阅读模板.md'
t = note.read_text(encoding='utf-8')
tp = template.read_text(encoding='utf-8')
questions = re.findall(r'^\*\*(Q\d+[a-z]?)\.', t, re.M)
template_questions = re.findall(r'^\*\*(Q\d+[a-z]?)\.', tp, re.M)
assert len(questions) == len(set(questions)), 'duplicate question'
assert set(questions) == set(template_questions), (set(template_questions) - set(questions), set(questions) - set(template_questions))
for letter, n in [('A', 21), ('B', 7)]:
    rows = re.findall(r'^\| (' + letter + r'\d+) \|', t, re.M)
    assert rows == [f'{letter}{i}' for i in range(1, n + 1)], rows
chunks = re.split(r'^\*\*(Q\d+[a-z]?)\..*$', t, flags=re.M)
for i in range(1, len(chunks), 2):
    assert chunks[i + 1].strip(), chunks[i]
for q in range(11, 16):
    section = chunks[chunks.index(f'Q{q}') + 1]
    for label in ['我猜：', '作者：', '差在：']:
        assert label in section, (q, label)
assert not re.search(r'答：[ \t]*\n(?:[ \t]*\n)*(?:---|\*\*Q|$)', t)
assert '手抄图位置：留空' in t
assert t.count('$$') % 2 == 0
assert '\ufffd' not in t
refs = re.findall(r'!\[\[([^\]]+)\]\]', t)
checks = []
for ref in refs:
    p = assets / ref
    assert p.is_file(), str(p)
    pix = pymupdf.Pixmap(str(p))
    assert pix.width > 200 and pix.height > 200
    checks.append({'file': ref, 'exists': True, 'width': pix.width, 'height': pix.height})
assert len(set(refs)) == 17
created_assets = {p.name for p in assets.glob('Kurtti2017-*.png')}
assert created_assets == set(refs), created_assets.symmetric_difference(set(refs))
report = {'note': str(note), 'characters': len(t), 'lines': len(t.splitlines()),
          'questions': questions, 'A_rows': 21, 'B_rows': 7,
          'image_references': len(refs), 'unique_images': len(set(refs)),
          'all_images_exist_and_decode': True, 'image_checks': checks,
          'missing_template_questions': [], 'empty_answers': [],
          'Q11_to_Q15_all_have_three_parts': True, 'hand_drawing_space_preserved': True}
Path(__file__).with_name('validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(report, ensure_ascii=False, indent=2))
