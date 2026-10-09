"""Read-only checks for the static deliverable; no browser or external requests."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from xml.etree import ElementTree
import json
import re
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / '02_網站'
PROSE_EXPECTATIONS = json.loads((ROOT / 'tests/approved-prose-expectations.json').read_text(encoding='utf-8'))['pages']


def approved_copy(markup, page_name):
    """Apply only the explicitly approved copy and intro heading removals."""
    if page_name == 'fieldwork-0829.html':
        for original, revised in (
            ('水道穿過蘆葦草澤，讓人想起倚水而居的日子',
             '水道穿過河岸植被，空拍讓細小的地景關係變得清楚'),
            ('看著快艇在水面劃開白浪、水道穿過蘆葦草澤',
             '看著快艇在水面劃開白浪、水道在河岸綠意間蜿蜒'),
        ):
            markup = markup.replace(original, revised)
    if page_name == 'intro.html':
        markup = markup.replace(
            '謝謝懷嵩老師。每次出發前，他都細心準備通告單；到了現場，照顧同學的學習與安全，讓沒有空拍機的人也有操作機會。老師的用心延續到課後，整理空拍照片、影片與課堂資料，讓我們創作時能查找素材、回顧所學。',
            '謝謝懷嵩老師，從行前準備到現場教學，始終用心照顧每位同學，讓大家都有學習與操作的機會。課後還細心整理空拍素材與課堂資料，讓我們能持續創作、回顧所學，感謝您的付出與陪伴！',
        )
        markup = re.sub(r'(<div class="intro-method-copy">)<h3>.*?</h3>', r'\1', markup, flags=re.S)
    return markup


class Document(HTMLParser):
    def __init__(self, markup):
        super().__init__(convert_charrefs=True)
        self.nodes = []
        self.stack = []
        self.feed(markup)

    def handle_starttag(self, tag, attrs):
        node = {'tag': tag, 'attrs': dict(attrs), 'text': '', 'parents': list(self.stack)}
        self.nodes.append(node)
        if tag not in ('meta', 'link', 'img', 'source', 'br', 'hr', 'input', 'area', 'wbr'):
            self.stack.append(node)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i]['tag'] == tag:
                self.stack = self.stack[:i]
                return

    def handle_data(self, data):
        for node in self.stack:
            node['text'] += data

    def find(self, tag=None, **attrs):
        return [n for n in self.nodes if (tag is None or n['tag'] == tag)
                and all(n['attrs'].get(k) == v for k, v in attrs.items())]


def check():
    failures = []
    pending_player_images = []
    descriptions = []
    pages = sorted(SITE.glob('*.html'))
    for path in pages:
        markup = path.read_text(encoding='utf-8')
        doc = Document(markup)
        def require(condition, detail):
            if not condition:
                failures.append(path.name + ': ' + detail)
        require(doc.find('html', lang='zh-Hant-TW'), '缺少繁體臺灣 lang')
        require(doc.find('body', id='top'), '缺少頁首錨點')
        require(doc.find('main', id='main'), '缺少主要內容錨點')
        require(doc.find('a', href='#main', **{'class':'skip'}), '缺少跳到內容連結')
        require(doc.find('a', href='#top', **{'class':'back-top ui-control'}), '回到頁首錨點錯誤')
        require('［聯絡方式待補］' not in markup, '已核准移除的聯絡方式佔位不應恢復')
        description = doc.find('meta', name='description')
        require(len(description) == 1, 'description 數量錯誤')
        if description:
            value = description[0]['attrs']['content']
            descriptions.append(value)
            require(60 <= len(value) <= 80, 'description 非 60–80 字')
        for property_name in ('og:title', 'og:description', 'og:type', 'og:url', 'og:locale', 'og:image'):
            require(len(doc.find('meta', property=property_name)) == 1, '缺少或重複 ' + property_name)
        require(doc.find('meta', name='twitter:card', content='summary_large_image'), '缺少 Twitter card')
        require('noindex' not in markup.lower(), '不應有 noindex')
        require(doc.find('details', **{'class':'site-menu'}), '缺少原生網站選單')
        require(doc.find('summary', role='button', **{'aria-controls':'site-menu-panel', 'aria-expanded':'false'}), '選單開關屬性錯誤')
        require(not doc.find('button', **{'class':'air-toggle'}) and not doc.find(id='air-subnav'), '舊空拍下拉不應恢復')
        desktop = doc.find('nav', **{'class':'desktop-navigation'})
        menu_links = [n for n in doc.find('a') if desktop and desktop[0] in n['parents']]
        require([n['attrs'].get('href','').rsplit('/',1)[-1] for n in menu_links] == ['intro.html','teacher.html','fieldwork.html','walks.html','works.html'], '主導覽順序錯誤')
        ids = [n['attrs']['id'] for n in doc.nodes if 'id' in n['attrs']]
        require(len(ids) == len(set(ids)), '重複 id')
        for node in doc.nodes:
            for attr in ('src', 'href'):
                value = node['attrs'].get(attr, '')
                if not value or urlsplit(value).scheme or value.startswith('//'):
                    continue
                url = urlsplit(value)
                local_path = unquote(url.path)
                if local_path.startswith('/flying-over-ketagalan/'):
                    local_path = local_path.removeprefix('/flying-over-ketagalan/')
                target = path.parent / local_path if local_path else path
                require(target.exists(), '本機連結不存在 ' + value)
                if url.fragment and target.suffix == '.html' and target.exists():
                    target_doc = doc if target == path else Document(target.read_text(encoding='utf-8'))
                    require(target_doc.find(id=unquote(url.fragment)), '錨點不存在 ' + value)
            if node['tag'] == 'img':
                attrs = node['attrs']
                player = any('video-shell' in p['attrs'].get('class', '').split() for p in node['parents'])
                if player:
                    pending_player_images.append(path.name + ': ' + attrs['src'])
                    continue
                require('width' in attrs and 'height' in attrs, '非播放器圖片缺少尺寸 ' + attrs['src'])
                require(attrs.get('decoding') == 'async', '圖片缺少 decoding ' + attrs['src'])
                require(attrs.get('loading') == 'lazy' or attrs.get('fetchpriority') == 'high', '圖片載入優先級錯誤')
                require(bool(attrs.get('alt')), '圖片缺少有效 alt')
            if node['tag'] == 'source' and 'srcset' in node['attrs']:
                for candidate in node['attrs']['srcset'].split(','):
                    image_name, declared_width = candidate.strip().split()
                    image_path = SITE / image_name
                    require(image_path.exists(), 'srcset 圖片不存在')
                    if image_path.exists():
                        with Image.open(image_path) as image:
                            require(image.width == int(declared_width.removesuffix('w')), 'srcset 寬度描述與圖檔不符 ' + image_name)
        if path.name == 'works.html':
            cards = doc.find('article', **{'class':'shared-card work-card'})
            require(len(cards) == 5, '作品卡片不是五張 article')
            for card in cards:
                links = [n for n in doc.find('a', **{'class':'stretched-link'}) if card in n['parents']]
                require(len(links) == 1 and any(p['tag'] == 'h3' for p in links[0]['parents']), '卡片連結不在 h3')
                require(not any(n['tag'] == 'p' and any(p['tag'] == 'a' for p in n['parents']) for n in doc.nodes if card in n['parents']), '簡介被連結包覆')
        if path.name == '404.html':
            for node in doc.nodes:
                for attr in ('href','src'):
                    value=node['attrs'].get(attr,'')
                    if value and not urlsplit(value).scheme and not value.startswith('#'):
                        require(value.startswith('/flying-over-ketagalan/'), '404 深層網址的資源/連結不能用相對路徑')
        baseline = ROOT / 'tmp/final-polish-baseline' / path.name
        if baseline.exists():
            approved_baseline = approved_copy(baseline.read_text(encoding='utf-8'), path.name)
            old = Document(approved_baseline)
            def original_prose(d):
                return [n['text'] for n in d.nodes if n['tag'] in ('p','h1','h2','h3') and any(p['tag']=='main' for p in n['parents'])]
            original, updated = PROSE_EXPECTATIONS.get(path.name, original_prose(old)), original_prose(doc)
            if path.name != 'index.html':
                iterator = iter(updated)
                require(all(any(text == candidate for candidate in iterator) for text in original), '原文文字或段落順序改變')
            pattern = r'<section\b[^>]*class="[^"]*\bactivity-film\b[^"]*"[^>]*>.*?</section>|<div\b[^>]*class="[^"]*\bvideo-shell\b[^"]*"[^>]*>.*?</div>'
            require(re.findall(pattern, markup, re.S) == re.findall(pattern, approved_baseline, re.S), '播放器 HTML 被改動（含核准的引言例外）')
    assert len(descriptions) == len(set(descriptions)), 'description 重複'
    sitemap = ElementTree.parse(SITE/'sitemap.xml')
    urls = [n.text for n in sitemap.findall('.//{*}loc')]
    assert {u.rsplit('/',1)[-1] for u in urls} == {p.name for p in pages}, 'sitemap 漏頁'
    with Image.open(SITE/'assets/og-cover.jpg') as image:
        assert image.size == (1200,630), 'OG 圖片尺寸錯誤'
    with Image.open(SITE/'apple-touch-icon.png') as image:
        assert image.size == (180,180), 'Apple icon 尺寸錯誤'
    baseline_js=ROOT/'tmp/final-polish-baseline/documentary.js'
    if baseline_js.exists():
        assert (SITE/'documentary.js').read_bytes() == baseline_js.read_bytes(), '影片 JS 必須保持原樣'
    report = {'pages':len(pages), 'failures':failures, 'player_images_awaiting_approval':pending_player_images}
    print(json.dumps(report,ensure_ascii=False,indent=2))
    assert not failures, '靜態驗證未通過'


if __name__ == '__main__':
    check()
