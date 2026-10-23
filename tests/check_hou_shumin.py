"""Acceptance of the additional works, including routes and original-player preservation."""
import json
import re
import subprocess
from pathlib import Path
from lxml import html

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / '02_網站'
OLD = ['suifen', 'kuncan', 'wenjin', 'yuan', 'abby']
NEW = ['shumin-fude', 'shumin-map', 'shumin-riverside', 'shumin-jinniang', 'shumin-belief']


def check():
    overview = html.parse(str(SITE / 'works.html'))
    cards = overview.xpath('//article[contains(concat(" ",@class," ")," work-card ")]')
    assert len(cards) == 10, f'作品卡應為 10 件，目前 {len(cards)}'
    assert cards[0].xpath('.//a[@class="stretched-link"]/@href') == ['shumin-jinniang.html'], '金娘傳奇應為第一件'
    for slug in NEW:
        assert len(overview.xpath(f'//a[@class="stretched-link"][@href="{slug}.html"]')) == 1
    all_slugs = ['shumin-jinniang'] + OLD + [s for s in NEW if s != 'shumin-jinniang']
    ids = json.loads((SITE / 'content/hou-shumin-media.json').read_text(encoding='utf-8'))
    for slug in all_slugs:
        doc = html.parse(str(SITE / (slug + '.html')))
        assert [a.get('href') for a in doc.xpath('//details[@class="work-switcher"]//a')] == [s+'.html' for s in all_slugs], slug
        index = all_slugs.index(slug)
        previous = all_slugs[index-1]+'.html' if index else 'works.html'
        following = all_slugs[index+1]+'.html' if index+1 < len(all_slugs) else 'works.html'
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
            assert 'AI 生成圖片' in ''.join(doc.xpath('//main//text()'))
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
    print('PASS: 10 作品卡；10 頁切換導覽；4 部影片與 1 份簡報；來源連結、圖片與目前位置')


if __name__ == '__main__':
    check()
