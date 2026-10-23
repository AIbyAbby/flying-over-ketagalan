"""New work text must not fall back to a different CJK font."""
from pathlib import Path
from fontTools.ttLib import TTFont
from lxml import html

SITE = Path(__file__).resolve().parents[1] / '02_網站'


def check():
    pages = list(SITE.glob('shumin-*.html'))
    text = ''.join(html.fromstring(p.read_text(encoding='utf-8')).text_content() for p in pages)
    required = {ord(c) for c in text if ord(c) >= 32 and c != '☰'}
    for face in ['NotoSansTC-400', 'NotoSansTC-700', 'NotoSerifTC-700']:
        fonts = list((SITE / 'assets/fonts').glob(face+'-*.woff2'))
        covered = set().union(*(set(TTFont(p).getBestCmap()) for p in fonts))
        missing = required - covered
        assert not missing, face+' 缺字：'+''.join(chr(c) for c in sorted(missing))
    for name in ['works', 'suifen', 'kuncan', 'wenjin', 'yuan', 'abby'] + [p.stem for p in pages]:
        assert 'work-fonts-extra.css' in (SITE / (name+'.html')).read_text(encoding='utf-8'), name
    print('PASS: 新增文字的正文及粗體、標題三套字型均無缺字；所有作品導覽已載入補字。')


if __name__ == '__main__':
    check()
