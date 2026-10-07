"""Shared static navigation and cards; no build/runtime framework required."""
from html import escape

AIR_PAGES = (
    ('fieldwork-0829.html', '01 北投社 08.29'),
    ('fieldwork-0903.html', '02 淡水與八里 09.03'),
    ('fieldwork-0905.html', '03 雞籠社與和平島 09.05'),
    ('fieldwork-0910.html', '04 基隆河流域 09.10'),
)
WORK_PAGES = {'abby.html', 'suifen.html', 'kuncan.html', 'wenjin.html', 'yuan.html'}


def render_header(filename):
    """Keep destination and disclosure separate, including on touch screens."""
    section = ('fieldwork.html' if filename in {url for url, _ in AIR_PAGES}
               else 'works.html' if filename in WORK_PAGES else filename)

    def nav_link(url, label):
        current = ' aria-current="page"' if section == url else ''
        return f'<a class="top-nav-link" href="{url}"{current}>{label}</a>'

    brand_current = ' aria-current="page"' if filename == 'index.html' else ''
    children = ''.join(
        f'<li><a href="{url}"' + (' aria-current="page"' if filename == url else '')
        + f'>{label}</a></li>' for url, label in AIR_PAGES
    )
    return (
        '<header class="site-header shared-header">'
        '<div class="header-row">'
        f'<a class="brand" href="index.html"{brand_current}>消失的原民故事</a>'
        '<div class="nav-scroll-shell">'
        '<nav class="top-nav" aria-label="主要導覽" tabindex="-1">'
        '<ul class="top-nav-list">'
        '<li>' + nav_link('intro.html', '引言') + '</li>'
        '<li>' + nav_link('teacher.html', '課程手記') + '</li>'
        '<li class="air-nav-group">' + nav_link('fieldwork.html', '空拍紀錄')
        + '<button type="button" class="air-toggle" aria-label="展開空拍紀錄子選單" '
        'aria-expanded="false" aria-controls="air-subnav"><span aria-hidden="true">▾</span></button></li>'
        '<li>' + nav_link('walks.html', '現場走讀') + '</li>'
        '<li>' + nav_link('works.html', '影音創作') + '</li>'
        '</ul></nav><span class="nav-scroll-hint" aria-hidden="true"></span></div></div>'
        '<nav id="air-subnav" class="air-subnav" aria-label="空拍紀錄子導覽" hidden>'
        '<ul>' + children + '</ul></nav></header>'
    )


def render_primary_link(url, label, class_name=''):
    return (
        f'<a class="primary-entry {escape(class_name, quote=True)}" href="{escape(url, quote=True)}">'
        f'<span>{escape(label)}</span><span class="entry-arrow" aria-hidden="true">→</span></a>'
    )


def render_section_heading(title, url, number='', subtitle='', heading_level=2):
    level = heading_level if heading_level in (2, 3) else 2
    marker = f'<span class="kicker">{escape(number)}</span>' if number else ''
    note = f'<p>{escape(subtitle)}</p>' if subtitle else ''
    return (
        '<div class="shared-section-heading"><div>' + marker
        + f'<h{level}>{escape(title)}</h{level}>' + note + '</div>'
        f'<a class="view-all" href="{escape(url, quote=True)}" aria-label="查看全部{escape(title, quote=True)}">'
        '查看全部<span class="viewall-arrow" aria-hidden="true">→</span></a></div>'
    )


def render_card(url, image, title, summary, label='', playable=False, cta=''):
    fieldwork_title_lines = {
        '兩河交會口，尋找消失的凱達格蘭': ('兩河交會口', '尋找消失的凱達格蘭'),
        '淡水河口空拍與十三行走讀': ('淡水河口', '空拍與十三行走讀'),
        '站上社寮砲台，回望雞籠社的山海': ('站上社寮砲台', '回望雞籠社的山海'),
        '沿著河尋找三個社的土地記憶': ('沿著河', '尋找三個社的土地記憶'),
    }
    title_html = '<br>'.join(escape(line) for line in fieldwork_title_lines[title]) if title in fieldwork_title_lines else escape(title)
    play = '<span class="poster-play" aria-hidden="true">▶</span>' if playable else ''
    fit = ' card-media-video' if playable else ''
    action = ('<span class="primary-entry fieldwork-card-action"><span>' + escape(cta)
              + '</span><span class="entry-arrow" aria-hidden="true">→</span></span>') if cta else (
        '<span class="card-action">' + ('觀看作品' if playable else '閱讀紀錄') + '</span>'
        '<span class="card-arrow" aria-hidden="true">→</span>')
    return (
        f'<a class="shared-card" href="{escape(url, quote=True)}">'
        f'<div class="card-media{fit}"><img src="{escape(image, quote=True)}" '
        f'alt="{escape(title, quote=True)}" loading="lazy">{play}</div>'
        '<div class="card-copy">'
        + (f'<span class="card-label">{escape(label)}</span>' if label else '')
        + f'<h3>{title_html}</h3><p>{escape(summary)}</p>'
        + action + '</div></a>'
    )


def render_intro(data, photo):
    """Do not normalize punctuation or wording in the supplied introduction."""
    body = photo(data['image'], data['image_alt'], 'intro-hero', True, show_caption=False)
    body += '<article class="intro-page wrap" aria-label="' + escape(data['title'], quote=True) + '">'
    for index, section in enumerate(data['sections']):
        level = 1 if index == 0 else 2
        body += f'<section class="intro-block"><h{level}>' + escape(section['title']) + f'</h{level}>'
        body += ''.join('<p>' + escape(p) + '</p>' for p in section['paragraphs'])
        body += '</section>'
    for section in data.get('methods', []):
        body += '<section class="intro-block intro-method"><span class="intro-method-label">' + escape(section['label']) + '</span>'
        body += '<div class="intro-method-copy"><h2>' + escape(section['title']) + '</h2>'
        body += ''.join('<p>' + escape(p) + '</p>' for p in section['paragraphs'])
        body += '</div></section>'
    if data.get('closing_image'):
        body += photo(data['closing_image'], data['closing_image_alt'], 'intro-closing-photo', show_caption=False)
    body += '<div class="intro-credits" aria-label="參與名單">'
    for row in data['credits']:
        label, text = row.split('｜', 1)
        body += '<p><strong>' + escape(label) + '</strong> ｜ ' + escape(text).replace('\n', '<br>') + '</p>'
    return body + '</div></article>'


def render_overview(title, lead, heading, cards, filename, show_breadcrumb=True, show_view_all=True):
    overview_class = ' fieldwork-overview' if filename == 'fieldwork.html' else ''
    lead_markup = ''.join('<p>' + escape(p) + '</p>' for p in lead) if isinstance(lead, list) else '<p>' + escape(lead) + '</p>'
    section_heading = render_section_heading(heading, filename + '#all-records') if show_view_all else '<div class="shared-section-heading"><h2>' + escape(heading) + '</h2></div>'
    return (
        '<div class="wrap shared-overview' + overview_class + '"><header class="page-heading">'
        + ('<a class="breadcrumb" href="index.html">首頁 /</a>' if show_breadcrumb else '')
        + f'<h1>{escape(title)}</h1>' + lead_markup + '</header>'
        '<section id="all-records">' + section_heading
        + '<div class="shared-card-grid">' + ''.join(cards) + '</div></section></div>'
    )
