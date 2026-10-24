"""Add the approved five works to the current edition without rebuilding unrelated content.

Run after the main edition is generated: python build_hou_shumin.py
Text source: content/hou-shumin.md. Media IDs: content/hou-shumin-media.json.
Existing works retain their body and player; only their work navigation is updated.
"""
from pathlib import Path
from html import escape as e
import json
import re
from PIL import Image
from shared_components import render_card

ROOT = Path(__file__).resolve().parent
SITE = ROOT / '02_網站'
CONTENT = SITE / 'content'
BASE = 'https://aibyabby.github.io/flying-over-ketagalan/'


def load_works():
    text = (CONTENT / 'hou-shumin.md').read_text(encoding='utf-8')
    result = []
    for media in json.loads((CONTENT / 'hou-shumin-media.json').read_text(encoding='utf-8')):
        section = re.search(r'^## ' + re.escape(media['slug']) + r'\n\n(.*?)(?=^## |\Z)', text, re.M | re.S)[1]
        parts = section.strip().split('\n\n')
        result.append(dict(media, title=parts[0].removeprefix('### '),
                           subtitle=parts[1].removeprefix('副標：'), description=parts[2],
                           short=parts[3].removeprefix('短介：'),
                           note=parts[4].removeprefix('提醒：') if len(parts) > 4 else '', author='侯淑敏'))
    return result


def img(path, alt, eager=False):
    with Image.open(SITE / path) as picture:
        width, height = picture.size
    loading = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
    return f'<img src="{e(path)}" alt="{e(alt)}" width="{width}" height="{height}" {loading} decoding="async">'


def switch(works, current):
    links = ''
    for i, w in enumerate(works, 1):
        state = ' aria-current="page"' if w['slug'] == current else ''
        links += (f'<a href="{w["slug"]}.html"{state}>' + img(w['image'], '')
                  + f'<span><strong>{i:02d} {e(w["title"])}</strong><span>{e(w["author"])}</span></span>'
                  + ('<small>目前作品</small>' if state else '') + '</a>')
    return '<details class="work-switcher"><summary>切換作品</summary><nav aria-label="作品切換">' + links + '</nav></details>'


def sequence(works, index):
    before = works[index - 1] if index else None
    after = works[index + 1] if index + 1 < len(works) else None
    def link(w, previous):
        return (f'<a href="{w["slug"]}.html"><span>{"← 上一件" if previous else "下一件 →"}</span><strong>{e(w["title"])}</strong></a>'
                if w else '<a href="works.html"><span>回到全部作品</span><strong>全部作品</strong></a>')
    page = '<nav class="final-work-sequence" aria-label="作品前後頁">' + link(before, True) + link(after, False) + '</nav>'
    bar = ('<nav class="work-action-bar" aria-label="作品快捷導覽">'
           + f'<a href="{before["slug"]+".html" if before else "works.html"}">{"← 上一件" if before else "回到全部作品"}</a>'
           + '<a href="works.html">全部作品</a>'
           + f'<a href="{after["slug"]+".html" if after else "works.html"}">{"下一件 →" if after else "回到全部作品"}</a></nav>')
    return page, bar


def work_card(w):
    is_video = w.get('kind', 'video') == 'video'
    card = render_card(w['slug']+'.html', w['image'], w['title'], w['short'], playable=is_video, stretched=True)
    if not is_video:
        card = card.replace('閱讀紀錄', '閱讀簡報')
    return card.replace('</h3>', '</h3><span class="card-label">創作者｜侯淑敏</span>', 1)


def new_page(w, works, template):
    title = e(w['title'])
    doc = re.sub(r'<title>.*?</title>', '<title>'+title+'｜消失的原民故事</title>', template, count=1)
    for name, value in [('description', w['short']), ('og:title', w['title']+'｜消失的原民故事'),
                        ('og:description', w['short']), ('og:url', BASE+w['slug']+'.html'),
                        ('twitter:title', w['title']+'｜消失的原民故事'), ('twitter:description', w['short'])]:
        doc = re.sub(r'(<meta (?:name|property)="'+re.escape(name)+r'" content=")[^"]*(")',
                     lambda m: m[1]+e(value, quote=True)+m[2], doc)
    doc = re.sub(r'(<link rel="canonical" href=")[^"]*', lambda m: m[1]+BASE+w['slug']+'.html', doc)
    route = ('<div class="content-route wrap"><nav class="final-breadcrumb" aria-label="麵包屑">'
             '<a href="index.html">首頁</a><span aria-hidden="true">／</span><a href="works.html">影音創作</a>'
             '<span aria-hidden="true">／</span><span aria-current="page">'+title+'</span></nav>'
             + switch(works, w['slug'])+'</div>')
    body = (route+'<header class="article-heading wrap work-heading"><h1>'+title+'</h1>'
            '<p class="article-lead">'+e(w['subtitle'])+'</p><p class="work-author">創作者｜侯淑敏</p></header>'
            '<article class="work-reading wrap"><div class="work-introduction"><p>'+e(w['description'])+'</p></div>')
    source = f'https://drive.google.com/file/d/{w["id"]}/view'
    if w['kind'] == 'video':
        body += (f'<div class="video-shell" data-video="{w["id"]}" data-title="{title}">'
                 + img(w['image'], '', True)
                 + f'<button type="button" class="play-button play-button--icon ui-control" aria-label="播放作品：{title}">'
                   '<span class="play-icon" aria-hidden="true">▶</span></button></div>'
                   '<p class="drive-viewing-hint"><span class="drive-hint-standard">手機觀看建議另開影片。</span>'
                   '<span class="drive-hint-line" aria-hidden="true">若在 LINE 內無法播放，請改用手機瀏覽器開啟。</span></p>')
    else:
        body += (f'<div class="video-shell"><iframe src="https://drive.google.com/file/d/{w["id"]}/preview" '
                   f'title="{title}・簡報" loading="lazy" allowfullscreen></iframe></div>')
        # No video-shell: the existing player script binds buttons in video shells only.
        body = body.replace('<div class="video-shell"><iframe', '<div class="presentation-shell"><iframe')
    body += (f'<p class="player-fallback-row"><a class="player-fallback" href="{source}" target="_blank" rel="noopener">'
             + ('在雲端觀看影片 ↗' if w['kind'] == 'video' else '另開簡報閱讀 ↗')+'</a></p></article>')
    body += ('<section class="other-works wrap"><div class="section-heading"><span class="kicker">沿著作品繼續閱讀</span>'
             '<h2>侯淑敏的其他作品</h2></div><div class="shared-card-grid">'
             + ''.join(work_card(other) for other in works if other.get('author') == '侯淑敏' and other['slug'] != w['slug'])
             + '</div></section>')
    seq, bar = sequence(works, next(i for i, item in enumerate(works) if item['slug'] == w['slug']))
    doc = re.sub(r'<main id="main">.*?</main>', lambda _: '<main id="main">'+body+seq+'</main>', doc, count=1, flags=re.S)
    doc = re.sub(r'<nav class="work-action-bar".*?</nav>', lambda _: bar, doc, count=1, flags=re.S)
    # Use the approved touch fallback on new pages without altering old players.
    if 'drive-viewing-hint.js' not in doc:
        doc = doc.replace('</head>', '<link rel="stylesheet" href="drive-viewing-hint.css?v=20261023-1"><script src="drive-viewing-hint.js?v=20261023-1" defer></script></head>')
    doc = re.sub(r'drive-viewing-hint\.css\?v=[^"\s]+', 'drive-viewing-hint.css?v=20261024-1', doc)
    if w['kind'] == 'presentation':
        doc = doc.replace('</head>', '<style>.presentation-shell{aspect-ratio:16/9}.presentation-shell iframe{width:100%;height:100%;border:0}</style></head>')
    return doc


def build():
    additions = load_works()
    old = json.loads((CONTENT / 'works.json').read_text(encoding='utf-8'))
    featured = next(w for w in additions if w['slug'] == 'shumin-jinniang')
    remaining = [w for w in additions if w['slug'] != featured['slug']]
    additions = [featured] + remaining
    group = dict(featured, slug='shumin')
    works = old + [group]
    individual_works = old + additions
    template = (SITE / 'suifen.html').read_text(encoding='utf-8')
    template = re.sub(r'<link rel="stylesheet" href="work-fonts-extra\.css\?v=[^"]+">', '', template)
    if 'class="site-header final-header"' not in template:
        raise RuntimeError('需要目前正式版的導覽模板；停止，避免套回舊版版面。')
    for w in additions:
        doc = new_page(w, individual_works, template)
        doc = re.sub(r'<details class="work-switcher">.*?</details>', lambda _: switch(works, 'shumin'), doc, count=1, flags=re.S)
        seq, bar = sequence(works, len(works)-1)
        doc = re.sub(r'<nav class="final-work-sequence".*?</nav>', lambda _: seq, doc, count=1, flags=re.S)
        doc = re.sub(r'<nav class="work-action-bar".*?</nav>', lambda _: bar, doc, count=1, flags=re.S)
        (SITE / (w['slug']+'.html')).write_text(doc, encoding='utf-8')
    # Like the existing multi-work creator pages, show all five works inline.
    hub = new_page(group, works, template)
    sections = ''
    for w in remaining:
        individual = (SITE / (w['slug']+'.html')).read_text(encoding='utf-8')
        article = re.search(r'<article class="work-reading wrap">(.*?)</article>', individual, re.S)[1]
        sections += ('<section class="interview wrap" id="'+w['slug']+'">'
                     '<header class="article-heading work-heading shumin-work-heading"><h2>'+e(w['title'])+'</h2>'
                     '<p class="article-lead">'+e(w['subtitle'])+'</p>'
                     '<p class="work-author">創作者｜侯淑敏</p></header>'+article+'</section>')
    hub = re.sub(r'<section class="other-works wrap">.*?</section>', lambda _: sections, hub, count=1, flags=re.S)
    hub = hub.replace('</head>', '<link rel="stylesheet" href="shumin-layout.css?v=20261023-1"></head>')
    if 'presentation-shell iframe' not in hub:
        hub = hub.replace('</head>', '<style>.presentation-shell{aspect-ratio:16/9}.presentation-shell iframe{width:100%;height:100%;border:0}</style></head>')
    (SITE / 'shumin.html').write_text(hub, encoding='utf-8')
    overview_path = SITE / 'works.html'
    overview = overview_path.read_text(encoding='utf-8')
    # Keep the approved main title, subtitle and byline together on this creator card.
    suifen = next(w for w in old if w['slug'] == 'suifen')
    def format_suifen(match):
        card = match[0]
        if 'href="suifen.html"' not in card:
            return card
        card = re.sub(r'<p class="card-subtitle">.*?</p>', '', card, flags=re.S)
        card = card.replace('</h3>', '</h3><p class="card-subtitle">'+e(suifen['subtitle'])+'</p>', 1)
        return card
    overview = re.sub(r'<article class="shared-card work-card">.*?</article>', format_suifen, overview, flags=re.S)
    overview = re.sub(r'<!-- hou-featured:start -->.*?<!-- hou-featured:end -->', '', overview, flags=re.S)
    block = '<!-- hou-shumin:start -->'+work_card(group)+'<!-- hou-shumin:end -->'
    if '<!-- hou-shumin:start -->' in overview:
        overview = re.sub(r'<!-- hou-shumin:start -->.*?<!-- hou-shumin:end -->', lambda _: block, overview, flags=re.S)
    else:
        anchor = '</div></section></div><nav class="final-sequence"'
        if overview.count(anchor) != 1:
            raise RuntimeError('作品總覽結構不符，停止避免誤插入。')
        overview = overview.replace(anchor, block+anchor, 1)
    overview_path.write_text(overview, encoding='utf-8')
    for i, w in enumerate(old):
        path = SITE / (w['slug']+'.html')
        doc = path.read_text(encoding='utf-8')
        doc = re.sub(r'<details class="work-switcher">.*?</details>', lambda _: switch(works, w['slug']), doc, count=1, flags=re.S)
        seq, bar = sequence(works, next(j for j, item in enumerate(works) if item['slug'] == w['slug']))
        doc = re.sub(r'<nav class="final-work-sequence".*?</nav>', lambda _: seq, doc, count=1, flags=re.S)
        doc = re.sub(r'<nav class="work-action-bar".*?</nav>', lambda _: bar, doc, count=1, flags=re.S)
        path.write_text(doc, encoding='utf-8')
    # Added glyphs use the same families/weights without changing original font subsets.
    for w in works + additions + [{'slug': 'works'}]:
        path = SITE / (w['slug']+'.html')
        doc = path.read_text(encoding='utf-8')
        if 'work-fonts-extra.css' not in doc:
            doc = doc.replace('</head>', '<link rel="stylesheet" href="work-fonts-extra.css?v=20261023-2"></head>')
        doc = re.sub(r'work-fonts-extra\.css\?v=[^"\s]+', 'work-fonts-extra.css?v=20261023-2', doc)
        path.write_text(doc, encoding='utf-8')
    sitemap = SITE / 'sitemap.xml'
    xml = sitemap.read_text(encoding='utf-8')
    for w in additions + [group]:
        url = BASE+w['slug']+'.html'
        if '<loc>'+url+'</loc>' not in xml:
            xml = xml.replace('</urlset>', '<url><loc>'+url+'</loc></url>\n</urlset>')
    sitemap.write_text(xml, encoding='utf-8')
    print('已集中五件作品於侯淑敏頁，總覽為 Abby 後的一張卡片。')


if __name__ == '__main__':
    build()
