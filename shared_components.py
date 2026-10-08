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


def render_card(url, image, title, summary, label='', playable=False, cta='', stretched=False):
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
    opening = '<article class="shared-card work-card">' if stretched else f'<a class="shared-card" href="{escape(url, quote=True)}">'
    heading = (f'<a class="stretched-link" href="{escape(url, quote=True)}">{title_html}</a>' if stretched else title_html)
    return (
        opening
        + f'<div class="card-media{fit}"><img src="{escape(image, quote=True)}" '
        f'alt="{escape(title, quote=True)}" loading="lazy">{play}</div>'
        '<div class="card-copy">'
        + (f'<span class="card-label">{escape(label)}</span>' if label else '')
        + f'<h3>{heading}</h3><p>{escape(summary)}</p>'
        + action + ('</div></article>' if stretched else '</div></a>')
    )


def render_intro(data, photo):
    """Render the approved introduction and its four reading destinations."""
    body = photo(data['image'], data['image_alt'], 'intro-hero', True, show_caption=False)
    body += '<article class="intro-page wrap" aria-label="' + escape(data['title'], quote=True) + '">'
    def methods():
        result = '<section class="intro-destinations" aria-labelledby="intro-destinations-title">'
        result += '<h2 id="intro-destinations-title">' + escape(data['methods_heading']) + '</h2>'
        for item in data.get('methods', []):
            result += '<div class="intro-block intro-method"><span class="intro-method-label" aria-hidden="true">' + escape(item['label']) + '</span>'
            result += '<div class="intro-method-copy">'
            result += ''.join('<p>' + escape(p) + '</p>' for p in item['paragraphs'])
            result += '</div></div>'
        return result + '</section>'
    for index, section in enumerate(data['sections']):
        level = 1 if index == 0 else 2
        kind = ' intro-opening' if index == 0 else (' intro-thanks' if index == len(data['sections']) - 1 else ' intro-making')
        body += '<section class="intro-block' + kind + '"><h' + str(level) + '>' + escape(section['title']) + '</h' + str(level) + '>'
        body += ''.join('<p>' + escape(p) + '</p>' for p in section['paragraphs'])
        if index == len(data['sections']) - 1:
            body += '<p class="intro-signature">— Abby 陳翠碧</p>'
        body += '</section>'
        if index + 1 == data.get('methods_after', 1):
            body += methods()
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


PUBLIC_BASE = 'https://aibyabby.github.io/flying-over-ketagalan/'
PAGE_DESCRIPTIONS = {
    'index.html': '消失的原民故事，保存一段共同學習與創作的記憶。從老師的課程手記、四次空拍到現場走讀與同學影音作品，循著水路、文獻和古地名，重新認識生活的土地。',
    'intro.html': '從老師的手記出發，整理課程中的空拍、走讀與影音創作。這篇引言記下網站緣起、各分頁的內容與一路同行的感謝，讓老師與同學共同留下的學習記憶持續被看見。',
    'teacher.html': '閱讀何懷嵩老師的課程手記，從文獻與古地圖走向走讀、空拍及影音創作。文章與現場照片保留課程設計、師生討論與知識共構的過程，重新探問臺北原民故事。',
    'fieldwork.html': '四次空拍，從北投社、淡水與八里、雞籠社與和平島，走向基隆河流域。點進各次紀錄，觀看空拍影片、現場照片與當時的通告單，回望我們一起出訪的風景。',
    'walks.html': '從空拍現場的操作與交流，到十三行博物館的展件與空間，照片留下同學共同走讀的身影。跟著現場紀錄回望課堂之外的觀看、討論，以及彼此陪伴的學習時刻。',
    'works.html': '收藏同學以空拍、走讀、文獻與 AI 情境影像完成的影音創作。每件作品呈現不同的觀察和敘事方式，也保留部分創作者的過程分享，邀請老師與同學慢慢欣賞。',
    'stories.html': '從課程手記出發，串起四次田野空拍與同學的影音作品。這份故事目錄整理老師的教學敘述、沿河而行的現場紀錄與各自寫成的故事，留下土地與影像的共同記憶。',
    'fieldwork-0829.html': '八月二十九日走訪北投社，在社子島頭觀看淡水河與基隆河交會，對望關渡宮與關渡大橋。空拍影片、現場照片及完整通告單，記錄這次從河流讀回土地的出訪。',
    'fieldwork-0903.html': '九月三日走訪淡水與八里，從空中觀看淡水河口、兩岸與淡江大橋，再走進十三行一帶。空拍影片、照片與完整通告單，留下河口景觀與現場走讀的學習紀錄。',
    'fieldwork-0905.html': '九月五日走訪雞籠社與和平島，從社寮砲台附近觀看海岸、港灣及山勢，對照古地圖的聚落線索。空拍影片、照片與完整通告單，保存這次山海之間的共同出訪。',
    'fieldwork-0910.html': '九月十日沿基隆河流域，尋找峰仔峙社、錫口社與塔塔悠社的土地記憶。空拍影片、現場照片和完整通告單，記錄河灣、橋梁與城市之間仍可辨認的歷史線索。',
    'abby.html': 'Abby 陳翠碧以課程空拍、走讀照片與古地圖編織空拍奇遇記，讓現代水岸與歷史情境相遇。頁面收錄影片、配音功課與創作之路，分享反覆觀看、聆聽和修改的過程。',
    'suifen.html': '張穗芬從北投保德宮與十三行博物館的線索出發，探尋凱達格蘭族的遺跡。透過今日地景、文物及古地圖重新辨認土地記憶，並以創作訪談分享自己的觀察與思考。',
    'kuncan.html': '高坤燦帶著「凱達格蘭族，你在哪裡？」的提問，從空中觀看淡水河、社子島與基隆河流域。作品將當代街廓與歷史社名相互對照，循著河灣追尋聚落留下的記憶。',
    'wenjin.html': '黃文津走進十三行，從干欄家屋、陶罐、古地圖與河口景觀，觀看人與土地的生活線索。影音作品串連展件、歷史材料及今日風景，在細節之間重讀凱達格蘭的故事。',
    'yuan.html': '傅玉安以一六三二年的西班牙神父報告為線索，透過 AI 影像重新想像島嶼北方的聚落與水路。頁面收錄凱達格蘭1632與創作之路，分享史料、聲音及剪輯間的取捨。',
    '404.html': '這個頁面目前找不到，歡迎回到消失的原民故事引言，繼續閱讀老師的課程手記、空拍紀錄、現場走讀與同學影音創作，循著網站導覽尋找想觀看的內容與學習記憶。',
}
MAIN_SEQUENCE = (('intro.html', '引言'), ('teacher.html', '課程手記'),
                 ('fieldwork.html', '空拍紀錄'), ('walks.html', '現場走讀'), ('works.html', '影音創作'))


def render_seo(filename, title):
    description = escape(PAGE_DESCRIPTIONS[filename], quote=True)
    canonical = PUBLIC_BASE + ('intro.html' if filename == 'index.html' else filename)
    image = ('assets/' + filename.removesuffix('.html') + '-first-frame.jpg'
             if filename in WORK_PAGES else 'assets/og-cover.jpg')
    width, height = (1280, 720) if filename in WORK_PAGES else (1200, 630)
    full_title = '消失的原民故事' if filename == 'index.html' else title + '｜消失的原民故事'
    return (f'<meta name="description" content="{description}">'
            f'<link rel="canonical" href="{canonical}">'
            f'<meta property="og:title" content="{escape(full_title, quote=True)}">'
            f'<meta property="og:description" content="{description}">'
            '<meta property="og:type" content="website">'
            f'<meta property="og:url" content="{PUBLIC_BASE + filename}">'
            '<meta property="og:locale" content="zh_TW">'
            f'<meta property="og:image" content="{PUBLIC_BASE + image}">'
            f'<meta property="og:image:width" content="{width}"><meta property="og:image:height" content="{height}">'
            '<meta property="og:image:alt" content="消失的原民故事・土地與影像的學習記憶">'
            '<meta name="twitter:card" content="summary_large_image">'
            f'<meta name="twitter:title" content="{escape(full_title, quote=True)}">'
            f'<meta name="twitter:description" content="{description}">'
            f'<meta name="twitter:image" content="{PUBLIC_BASE + image}">'
            '<link rel="icon" href="favicon.ico" sizes="16x16 32x32 48x48">'
            '<link rel="apple-touch-icon" href="apple-touch-icon.png" sizes="180x180">')


def render_page_sequence(filename):
    pages = [page for page, _ in MAIN_SEQUENCE]
    if filename not in pages:
        return ''
    index = pages.index(filename)
    links = []
    for offset, label, relation in ((-1, '上一頁', 'prev'), (1, '下一頁', 'next')):
        if 0 <= index + offset < len(pages):
            url, title = MAIN_SEQUENCE[index + offset]
            links.append(f'<a class="sequence-{relation}" href="{url}" rel="{relation}"><span>{label}</span> {title}</a>')
    return '<nav class="page-sequence" aria-label="篇章前後頁">' + ''.join(links) + '</nav>'


def render_footer():
    return ('<footer class="site-footer compact-footer">'
            '<a class="back-top ui-control" href="#top" aria-label="回到頁首">回到頁首</a>'
            '<p class="copyright">本站所有作品、照片與文字，著作權屬原創作者。'
            '如需撤下或更正，請聯繫：<strong class="contact-placeholder">［聯絡方式待補］</strong></p></footer>')
