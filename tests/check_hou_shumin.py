"""Acceptance of the additional works, including routes and original-player preservation."""
import json
import re
import subprocess
from pathlib import Path
from lxml import html

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / '02_網站'
OLD = ['suifen', 'kuncan', 'wenjin', 'yuan', 'abby']
NEW = ['shumin-fude', 'shumin-map', 'shumin-riverside', 'shumin-jinniang', 'shumin-picturebook', 'shumin-belief']


def check():
    overview = html.parse(str(SITE / 'works.html'))
    cards = overview.xpath('//article[contains(concat(" ",@class," ")," work-card ")]')
    assert len(cards) == 6, f'創作者卡應為 6 張，目前 {len(cards)}'
    creator_slugs = OLD + ['shumin']
    assert [c.xpath('.//a[@class="stretched-link"]/@href')[0] for c in cards] == [s+'.html' for s in creator_slugs]
    for slug in NEW:
        assert not overview.xpath(f'//a[@class="stretched-link"][@href="{slug}.html"]'), '不可拆成五張總覽卡'
    all_slugs = OLD + NEW + ['shumin']
    ids = json.loads((SITE / 'content/hou-shumin-media.json').read_text(encoding='utf-8'))
    for slug in all_slugs:
        doc = html.parse(str(SITE / (slug + '.html')))
        assert [a.get('href') for a in doc.xpath('//details[@class="work-switcher"]//a')] == [s+'.html' for s in creator_slugs], slug
        index = creator_slugs.index(slug) if slug in OLD else len(creator_slugs)-1
        previous = creator_slugs[index-1]+'.html' if index else 'works.html'
        following = creator_slugs[index+1]+'.html' if index+1 < len(creator_slugs) else 'works.html'
        assert doc.xpath('//nav[@class="work-action-bar"]/a/@href') == [previous, 'works.html', following], slug
        for nav in doc.xpath('//nav'):
            assert len(nav.xpath('.//*[@aria-current="page"]')) <= 1, slug
        if slug not in NEW:
            continue
        assert '侯淑敏' in ''.join(doc.xpath('//p[@class="work-author"]/text()'))
        assert len(doc.xpath('//h1')) == 1
        assert len(doc.xpath('//div[@class="work-introduction"]/p')) >= 1
        item = next(w for w in ids if w['slug'] == slug)
        source = f'https://drive.google.com/file/d/{item["id"]}/view'
        assert doc.xpath(f'//a[@class="player-fallback"][@href="{source}"]'), slug
        if item['kind'] == 'video':
            assert doc.xpath(f'//div[@class="video-shell"][@data-video="{item["id"]}"]'), slug
        else:
            assert not doc.xpath('//div[@class="video-shell"]'), '簡報不可當影片'
            assert doc.xpath('//iframe[@title="平埔族秀朗社的靈魂信仰與祭儀・簡報"]')
            assert '作品形式｜圖像簡報' not in ''.join(doc.xpath('//main//text()'))
            assert '原簡報註明' not in ''.join(doc.xpath('//main//text()'))
        for img in doc.xpath('//img[@src]'):
            assert (SITE / img.get('src')).is_file(), img.get('src')
        for a in doc.xpath('//a[@href]'):
            href = a.get('href')
            if not href.startswith(('https:', 'http:', '#')):
                assert (SITE / href.split('#')[0]).exists(), href
    # The only permitted changes to old work pages are the three work navigation regions.
    regions = [r'<details class="work-switcher">.*?</details>',
               r'<nav class="final-work-sequence".*?</nav>',
               r'<nav class="work-action-bar".*?</nav>']
    for slug in OLD:
        original = subprocess.check_output(['git', 'show', f'HEAD:02_網站/{slug}.html'], cwd=ROOT).decode('utf-8')
        current = (SITE / (slug+'.html')).read_text(encoding='utf-8')
        for region in regions:
            original = re.sub(region, '', original, flags=re.S)
            current = re.sub(region, '', current, flags=re.S)
        font_link = r'<link rel="stylesheet" href="work-fonts-extra\.css\?v=[^"]+">'
        original = re.sub(font_link, '', original)
        current = re.sub(font_link, '', current)
        assert original.replace('\r\n', '\n') == current.replace('\r\n', '\n'), slug+'：既有內容被改動'
    for filename in ['documentary.js', 'navigation-final.js', 'drive-viewing-hint.js']:
        tracked = subprocess.check_output(['git', 'ls-tree', '--name-only', 'HEAD', '--', f'02_網站/{filename}'], cwd=ROOT)
        if not tracked.strip():
            continue  # A newly added helper has no previously published version to preserve.
        original = subprocess.check_output(['git', 'show', f'HEAD:02_網站/{filename}'], cwd=ROOT)
        assert original.replace(b'\r\n', b'\n') == (SITE / filename).read_bytes().replace(b'\r\n', b'\n'), filename
    hub = html.parse(str(SITE / 'shumin.html'))
    expected = [next(w['id'] for w in ids if w['slug']==s) for s in ['shumin-jinniang','shumin-picturebook','shumin-fude','shumin-map','shumin-riverside']]
    assert hub.xpath('//div[@class="video-shell"]/@data-video') == expected
    assert len(hub.xpath('//div[@class="presentation-shell"]/iframe')) == 1
    assert len(hub.xpath('//a[@class="player-fallback"]')) == 6
    assert hub.xpath('//h1/text()') == ['秀朗尪姨・金娘傳奇Ⅰ']
    print('PASS: 6 張創作者卡；侯淑敏在 Abby 後；六件作品同頁，金娘第一、繪本第二；導覽與原文保留')


if __name__ == '__main__':
    check()
