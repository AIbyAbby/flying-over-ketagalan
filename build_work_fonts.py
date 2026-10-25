"""Supplement existing font subsets with new work characters; existing glyphs stay untouched.

Pass full, licensed Noto TC variable fonts using --sans and --serif.
"""
from pathlib import Path
import argparse
from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from lxml import html

ROOT = Path(__file__).resolve().parent
SITE = ROOT / '02_網站'


def build(sans, serif):
    text = ''.join(html.fromstring(p.read_text(encoding='utf-8')).text_content()
                   for p in SITE.glob('shumin-*.html'))
    # Include punctuation and Roman numerals too; the menu icon is intentionally a symbol.
    required = {ord(c) for c in text if ord(c) >= 32 and c != '☰'}
    rules = ['/* 補足新增作品用字；沿用原字體與字重，unicode-range 不覆蓋既有字。 */']
    for family, weight, source in [('NotoSansTC', 400, sans), ('NotoSansTC', 700, sans), ('NotoSerifTC', 700, serif)]:
        name = f'{family}-{weight}'
        original = TTFont(SITE / f'assets/fonts/{name}-site.woff2')
        missing = required - set(original.getBestCmap())
        if not missing:
            continue
        font = TTFont(source)
        assert missing <= set(font.getBestCmap()), f'{family}: 原始字型仍有缺字'
        instantiateVariableFont(font, {'wght': weight}, inplace=True, updateFontNames=True)
        options = subset.Options()
        worker = subset.Subsetter(options=options)
        worker.populate(unicodes=missing)
        worker.subset(font)
        font.flavor = 'woff2'
        filename = name+'-works-extra.woff2'
        font.save(SITE / 'assets/fonts' / filename)
        unicode_range = ','.join(f'U+{code:X}' for code in sorted(missing))
        family_name = 'Noto Sans TC' if family == 'NotoSansTC' else 'Noto Serif TC'
        rules.append(f'@font-face{{font-family:"{family_name}";src:url("assets/fonts/{filename}?v=20261025-2") format("woff2");font-style:normal;font-weight:{weight};font-display:swap;unicode-range:{unicode_range}}}')
        print(f'{filename}: {len(missing)} 個補字，{(SITE / "assets/fonts" / filename).stat().st_size} bytes')
    (SITE / 'work-fonts-extra.css').write_text('\n'.join(rules)+'\n', encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sans', type=Path, required=True)
    parser.add_argument('--serif', type=Path, required=True)
    args = parser.parse_args()
    build(args.sans, args.serif)
