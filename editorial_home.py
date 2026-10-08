"""Chapter-based homepage using the agreed story-first reading sequence."""
from html import escape
from pathlib import Path
from PIL import Image
from shared_components import render_card, render_section_heading, render_primary_link, render_seo, render_header, render_footer

OPENING = [
    '我們原以為，自己已經很熟悉這座城市。',
    '熟悉上班途中經過的橋，熟悉假日散步的河堤，也熟悉那些說了無數次的地名。直到跟著老師翻開古地圖，才發現熟悉的街道之下，還有一層我們未曾細讀的往事。北投、關渡、錫口、八里，那些日常用來辨認方向的名字，開始帶著問題回到眼前：在今日的道路與樓房出現以前，人們如何沿河往來，又如何在水岸安頓生活？',
    '這是「消失的原民故事」計畫的起點。南港社區大學與臺北市原住民族部落大學攜手開設工作坊，由何懷嵩老師帶領我們，透過文獻、走讀、空拍與影像創作，探尋凱達格蘭族留在臺北及周邊地區的歷史線索。參與的人來自不同背景，各自帶著人生經驗，也帶著對這片生活之地的好奇。',
]

METHODS = [
    ('文獻', '從字裡讀見來處', '翻開古地圖與歷史記載，辨讀社名、水路與聚落線索。資料裡的差異，也成為我們出發時帶著的問題。'),
    ('走讀', '把問題帶到現場', '跟著老師走向河岸、街巷與展場，對照山勢、地形與文物，讓紙上的名字與眼前的風景逐漸相連。'),
    ('空拍', '換一個高度觀看', '飛越歷史，記錄土地。空拍機緩緩升起，鏡頭沿著水路前行，將河灣、山勢與聚落收進視野。我們以空中影像對照古地圖，在今日的風景裡，探尋先民生活的線索。'),
    ('創作', '讓發現長成故事', '整理照片、剪輯影片，將文獻線索、現場觀察與創作想像編織成作品，留下每個人理解地方的方式。'),
]


def render_entry():
    """Keep the public root URL as a static entry to the introduction."""
    return '''<!doctype html>
<html lang="zh-Hant-TW">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="refresh" content="0; url=intro.html">
''' + render_seo('index.html', '消失的原民故事') + '''
<link rel="stylesheet" href="magazine.css?v=uiux-1">
<link rel="stylesheet" href="reading-layout.css?v=uiux-1">
<link rel="stylesheet" href="uiux-fonts.css?v=uiux-1">
<link rel="stylesheet" href="uiux-polish.css?v=uiux-1">
<title>消失的原民故事</title>
<script src="documentary.js?v=6" defer></script>
</head>
<body id="top" class="inner"><a class="skip" href="#main">跳到主要內容</a>''' + render_header('index.html') + '''
<main id="main" class="wrap"><header class="page-heading">
<h1>消失的原民故事</h1>
<p>''' + render_primary_link('intro.html', '閱讀引言') + '''</p>
</header></main>
<noscript><p class="redirect-note">若未自動跳轉，請<a href="intro.html">閱讀引言</a>。</p></noscript>
''' + render_footer() + '''</body></html>
'''

def paragraphs(items):
    return ''.join('<p>'+escape(p).replace('\n','<br>')+'</p>' for p in items)

def chapter(number, title, items, image, photo, link='', label='閱讀故事', image_caption='', primary=False, all_url=''):
    destination = all_url or ('fieldwork.html' if link.startswith('fieldwork-') else link)
    heading = render_section_heading(title, destination) if destination else '<h2>'+escape(title)+'</h2>'
    content = '<section class="journal-chapter"><div class="journal-copy"><span class="journal-number">'+escape(number)+'</span>'+heading+'<div class="journal-reading">'+paragraphs(items)+'</div>'
    if link:
        content += (render_primary_link(link, label, 'journal-link ui-control') if primary else '<a class="journal-link ui-control" href="'+escape(link)+'">'+escape(label)+'</a>')
    return content+'</div>'+photo(image,image_caption,'journal-picture')+'</section>'

def render_home(root, courses, works, photo, summaries):
    site = root/'02_網站'
    source = root.parent/'金色時光城市河谷與歷史幽影.png'
    target = site/'assets/home-golden-river.jpg'
    if not target.exists():
        with Image.open(source) as im:
            im.convert('RGB').save(target, quality=94, optimize=True)
    body = '<div class="editorial-journal"><header class="journal-opening" id="origins"><span class="journal-number">循著凱達格蘭的足跡</span><h1>消失的原民故事</h1><p class="journal-subtitle"><span>從地面走讀，從空中的觀看</span><span>把土地的記憶寫進我們的鏡頭</span></p><div class="journal-opening-actions">'+render_primary_link('fieldwork.html','走進四次空拍紀錄')+'<a class="journal-link" href="walks.html">看看我們一起走過的地方 →</a></div><div class="journal-reading">'+paragraphs(OPENING)+'</div><nav class="journal-contents" aria-label="首頁章節"><a href="#origins">故事緣起</a><a href="#course-notes">課程手記</a><a href="#journeys">四次出發</a><a href="#creations">影像創作</a></nav></header>'
    method_html='<section class="journal-methods" aria-label="我們如何進行這個計畫">'
    for term,title,description in METHODS:
        method_html+='<div class="journal-method"><span class="method-mark">'+term+'</span><h2>'+title+'</h2><p>'+description+'</p></div>'
    method_html+='</section>'
    body=body.replace('<nav class="journal-contents"',method_html+'<nav class="journal-contents"')
    body += photo('assets/home-golden-river.jpg','','journal-picture journal-opening-picture',True)
    body += '<div id="course-notes">'+chapter('01　課程手記','循著名字走向土地',[
        '出發以前，我們先學著閱讀。古地圖上的河道、文獻裡不盡相同的社名，以及歷史圖像中由他人描繪的面貌，都需要細細辨認。有些資料讓輪廓漸漸清楚，有些卻帶來更多疑問。',
        '老師引領我們把問題帶到現場，讓紙頁上的記載，與眼前的山勢、水路和街廓彼此對照。不同背景的同行者，也將自己的經驗帶進討論。一個地名，因此有了更多理解的入口。',
    ],'assets/flight-0905-0030.jpg',photo,'teacher.html','閱讀何懷嵩老師的課程手記',image_caption='和平島｜同行者在山坡高處共同觀看港灣')+'</div>'
    body += chapter('02　觀看的轉向','當鏡頭升起',[
        '當空拍機緩緩升起，被建築遮住的河灣展開了，原本分散的兩岸也連成一幅完整的風景。我們開始試著從水路理解這座城市：哪裡可以靠岸，哪裡通往更遠的地方，山與河如何牽引人們生活的方向。',
        '空拍機彷彿成了一部穿越時光的機器。鏡頭拍下當下，思緒卻循著文獻與地形，往更早的年代伸展。當橋梁尚未橫跨水面，當街道還沒有今日的模樣，曾在這裡生活的人，會從怎樣的角度看見河岸與天空？',
        '這些想像成為創作的起點，也提醒我們繼續查找、比對，分辨哪些已有依據，哪些仍有待追問。',
    ],'assets/home-0829-0077.jpg',photo,image_caption='關渡河岸｜水路、山勢與城市在空中視野裡相接', all_url='fieldwork.html')
    body += '<section id="journeys" class="journal-section-heading"><span class="journal-number">03　田野與空拍</span>'+render_section_heading('四次出發的風景','fieldwork.html')+'<p>循著水路與古地名<br>從河口走向海岸 再讀回城市的來處</p></section>'
    home_covers={'0829':'home-0829-0083.jpg','0903':'flight-0903-0017.jpg','0905':'flight-0905-0022.jpg','0910':'flight-0910-0046.jpg'}
    for i,c in enumerate(courses,1):
        body += chapter(f'{i:02d}　{c["date"]}　{c["place"]}',c['title'],c['intro'].split('\n\n')[:1],
                        'assets/'+home_covers[c['key']],photo,f'fieldwork-{c["key"]}.html','走進這次沿河而行',
                        image_caption=c['date']+' '+c['place']+'｜現場影像', primary=True)
    body += '<section id="creations" class="journal-works"><div class="journal-copy"><span class="journal-number">04　影像創作</span>'+render_section_heading('把觀看寫成故事','works.html')+'<div class="journal-reading">'+paragraphs([
        '回到課堂，照片、影片與討論逐漸長成各自的作品。有人從古地名出發，有人凝視博物館中的展件，也有人讓實拍畫面與歷史情境的創作相遇。我們在彼此的敘述裡，看見了自己未曾留意的細節。',
    ])+'</div></div><div class="journal-work-grid shared-card-grid">'
    for w in works:
        body += render_card(w['slug']+'.html', w['image'], w['title'], summaries[w['slug']], label=w['author'], playable=True)
    body += '</div></section>'
    body += chapter('05　寫在旅程之後','讓土地的記憶繼續被看見',[
        '這裡收錄的，是一段一起學習觀看的旅程。「消失」是我們對那些逐漸被忽略的故事所提出的追問。當我們願意停下腳步，重新讀一個名字、看一段河流，熟悉的城市，也就有了更深的來處。',
    ],'assets/flight-0905-0035.jpg',photo,'works.html','觀看影音創作',image_caption='和平島｜雲霧中的海岸與遠方島嶼')
    return body+'</div>'
