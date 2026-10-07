"""Build the discussed documentary edition. Originals remain untouched."""
from pathlib import Path
from html import escape as e
import argparse, json, shutil, subprocess
from PIL import Image, ImageOps
from teacher_pages import ordered_teacher, HEADINGS, CAPTIONS, source_text, teacher_header
from shared_components import render_header, render_card, render_intro, render_overview
from walks_page import prepare_walks_photos, render_walks
import re

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--pages', nargs='+', choices=['index.html','stories.html','fieldwork.html','works.html','intro.html','walks.html','teacher.html','fieldwork-0829.html','fieldwork-0903.html','fieldwork-0905.html','fieldwork-0910.html','abby.html','suifen.html','kuncan.html','wenjin.html','yuan.html'], help='Only render these HTML filenames.')
parser.add_argument('--prepare-media', action='store_true', help='Explicitly rebuild existing photos and video posters.')
parser.add_argument('--write-content', action='store_true', help='Explicitly export legacy derived Markdown and JSON.')
args = parser.parse_args()
selected_pages = set(args.pages) if args.pages else None
built_pages = []

ROOT=Path(__file__).resolve().parent
SITE=ROOT/'02_網站'
CONTENT=SITE/'content'
CONTENT.mkdir(exist_ok=True)
CARD_SUMMARIES=json.loads((CONTENT/'card-summaries.json').read_text(encoding='utf-8'))
INTRO_DATA=json.loads((CONTENT/'intro.json').read_text(encoding='utf-8'))
TEACHER_SOURCE=source_text(ROOT)
TEACHER_CAPTIONS={name:re.search(pattern,TEACHER_SOURCE).group() for name,pattern in CAPTIONS}
if args.write_content:
 (CONTENT/'teacher-photo-captions.md').write_text('# 老師照片原文註釋\n\n'+'\n\n'.join(f'![{caption}](../assets/{name})\n\n{caption}' for name,caption in TEACHER_CAPTIONS.items())+'\n',encoding='utf-8')

COURSES=[
 dict(key='0829',date='08.29',place='北投社',title='兩河交會口，尋找消失的凱達格蘭',cover='0829-0080',
 intro='''來到社子島頭，河風迎面而來。淡水河與基隆河在此交會，我們攤開古地圖，找到「干豆門」的位置，再抬頭望向對岸，關渡就在不遠處。

紙上的地名，第一次和腳下的土地產生了連結。

我們辨認山勢與水道，試著把幾百年前的地景，放回今天的視線裡。當空拍機離開地面，河道、沙洲和遠山從另一個角度展現出完整的輪廓。

也就在這個時候，一個問題浮現出來：

北投社的人，當年為什麼選擇在這裡生活？

也許答案並不複雜。\n水，是生活的依靠，也是往來的方向。

站在兩條河交會的地方，我們看見的不只是地理位置，也開始理解一個聚落與土地之間最初的關係。''',
 short='從社子島頭出發，在河流交會處重新觀看土地。',
 photos=[('0829-0080','沿著河面望向遠方，水路、河岸與山勢在同一個視野裡展開。'),('0829-0042','一起走到現場，讓課堂上的地名有了眼前的風景。'),('0829-0110','水道穿過河岸植被，空拍讓細小的地景關係變得清楚。')]),
 dict(key='0903',date='09.03',place='淡水與八里',title='淡水河口空拍與十三行走讀',cover='0903-0047',
 intro='''河口的風帶著海的氣息。

淡水與八里隔著河相望，如今淡江大橋橫跨其間，讓兩岸的往來變得便利。只是站在水岸時，我們仍不免想到：橋出現以前，人們又是如何渡過這段水路？

這一天，我們在觀海路尾進行空拍。

附近屬於管制空域，飛行前必須仔細確認範圍；起飛之後，也只能朝河面方向前進。有限的飛行路線，反而讓我們更專注於兩岸之間的水域。

結束飛行後，我們前往八里十三行一帶走讀。

高處看到的是開闊的河口，走進遺址與展場，視線則落在一件件細小的遺物上。從遼闊的地景，到留下生活痕跡的物件，時間忽然有了不同的尺度。

原來，一條河的兩岸，不只是空間上的分隔。

渡河、往來與交流，也讓水面成為連結生活的一條路。''',
 short='從河口兩岸的空拍，到十三行展場裡的生活線索。',
 photos=[('0903-0014','從空中看向河口，海岸、港灣與水面的尺度一起展開。'),('0903-0047','淡江大橋跨過河面，當代建設與河口地形相互映照。'),('0903-0029','鏡頭轉向海岸，陸地與水域的交界成為另一條閱讀路徑。')]),
 dict(key='0905',date='09.05',place='雞籠社與和平島',title='站上社寮砲台，回望雞籠社的山海',cover='0905-0005',
 intro='''和平島的風，帶著明顯的海味。

我們來到社寮砲台附近，從山勢望向港灣與水道，再回頭尋找古地圖上的「雞籠社」。地圖裡的聚落畫在山海之間，而今天的景象，已經有了截然不同的面貌。

於是，我們開始一處一處辨認。

大家輪流操作空拍機，也交換彼此的看法。從地面看是一座島，換個高度觀看，山、港與海的位置關係便更加清楚。

有些歷史不會留下完整的遺址，甚至只剩下一個名稱。

但一個名字能留到今天，本身就是一條線索。

透過空拍，也讓那個久遠的「雞籠社」，在今天的山海之間重新被看見。''',
 short='走進和平島，從岩岸、港口與聚落觀看雞籠社。',
 photos=[('0905-0005','和平島的海岸與岩層，在高處呈現出不同於地面的尺度。'),('0905-0015','貼著海岸觀看，岩壁、浪花與沿岸步道彼此交錯。'),('0905-0023','從海岸轉向城市，水道、港口與街廓形成層層地景。')]),
 dict(key='0910',date='09.10',place='基隆河流域',title='沿著河尋找三個社的土地記憶',cover='0910-0054',
 intro='''峰仔峙社、錫口社、塔塔悠社。

三個名字，分布在基隆河流域。這一天，我們從汐止出發，沿著河岸尋找它們曾經所在的位置，也停留在舊社橋與可以眺望河谷的高處。

城市裡的道路、建築與橋梁不斷改變，河谷的走向卻仍然清楚。

拍攝前，我們先確認附近的飛行空域。國道三號就在周邊，路線必須避開管制範圍。完成確認後，才開始從高處觀看這片河域。

當視野拉開，河灣的形狀變得明顯，地圖上的三個社名，也開始和地形有了關係。

這一天沒有追著一座遺跡尋找答案，而是順著河的方向，把幾個名字重新串在一起。

原來，地方的記憶不一定藏在一棟老建築裡。

有時，它就在一段河道、一個轉彎，以及一個仍然被記得的名字裡。''',
 short='沿基隆河辨認河灣、街廓與歷史聚落的關係。',
 photos=[('0910-0054','河面、橋梁與城市並置，空拍帶來更完整的觀看。'),('0910-0024','河岸植被與住宅向兩側延伸，水路仍在城市之間流動。'),('0910-0048','鏡頭循著河灣轉彎，地形與城市的關係逐漸清楚。')]),
]
WORKS=json.loads((CONTENT/'works.json').read_text(encoding='utf-8'))
ACTIVITY_MEDIA=json.loads((CONTENT/'activity-media.json').read_text(encoding='utf-8')) if (CONTENT/'activity-media.json').exists() else {}
for course in COURSES:
 if course['key'] in ACTIVITY_MEDIA:
  course['photos']=[(Path(p['src']).stem.removeprefix('flight-'),p['caption']) for p in ACTIVITY_MEDIA[course['key']]['photos']]
WORK_COPY={
 'abby':('當空拍機升空遠眺，社子島與淡水河在鏡頭下展開，開啟了一場穿越時空的奇幻旅程。Abby 從實體空拍課堂出發，將當代水岸實景與生成式 AI 敘事無縫銜接。從時光漩渦地圖到古老水澤，獨木舟上的凝望、大屯山硫穴的蒸騰煙嵐，逐步拼湊出十七世紀凱達格蘭族與山川共生的生活樣貌。這場奇遇不僅記錄了探索土地的熱情，更以科技之眼重新凝視歷史，喚醒深埋在台北盆地地層下的原鄉記憶。','當空拍機升離河岸，現代地景交疊出四百年前的部落記憶。跟著 Abby 乘上時空獨木舟，在空拍與情境創作之間，展開一場重返凱達格蘭的奇遇。'),
 'suifen':('搭上現代捷運穿梭台北，我們熟悉的都會街廓，能否成為尋訪平埔記憶的時光路徑？張穗芬帶著田野踏查的視角，從北投保德宮刻著「平埔社」的古石雕出發，一路延伸至十三行博物館的陶罐工藝與干欄聚落。影片將今日地景、文獻地圖與史前生活模型細膩疊合，帶領觀者放慢腳步，在日常風景中辨認凱達格蘭族的身世痕跡。當聚落已然隱沒，這些留存的物件與線索，正為我們拼湊出未曾斷裂的土地記憶。','每天穿梭的現代城市，還藏著哪些未曾細讀的平埔線索？跟著張穗芬搭上捷運走訪遺址與博物館，在日常風景的縫隙中，重新辨認凱達格蘭的歷史痕跡。'),
 'kuncan':('「凱達格蘭族，你在哪裡？」高坤燦以一句真切探問作為航道，操縱空拍機掠過淡水河、社子島、基隆河灣直至汐止與松山。鏡頭從高空俯瞰當代高樓林立的繁華街廓，又在峰仔峙社與錫口社的古老河曲前駐足停留。作品將今日清晰的水路航道，與歷史文獻、地名源流深情疊合，追索隱沒在水泥叢林下的聚落紋理。當聚落的身影已隨歲月模糊，河流的彎折與名字的餘音，正持續為我們指引尋回根源的方向。','當聚落的樣貌隱入都會，我們還能循著什麼找到它？高坤燦帶著「你在哪裡」的真切提問，以空拍鏡頭穿過淡水河與基隆河，追尋這片土地最初的輪廓。'),
 'wenjin':('一座住屋、一件陶罐與一張古地圖，究竟能為我們拼湊出多少過往生活的線索？黃文津帶著踏查視角走進八里十三行，將博物館裡的干欄家屋、出土工藝與乾隆古地圖緊密疊合。鏡頭凝視著專注製陶的族人身影，在開闊的淡水河口與觀音山色之間，尋找人與土地依存的深刻脈絡。當聚落日常隨歲月隱沒，這些被用心留存的碎片，正重新喚醒這片土地最初的文明足跡，讓古老深邃的海洋靈魂再次對當代說話。','一件出土文物與古地圖，究竟能接起怎樣的生活輪廓？跟著黃文津在住屋、展件與歷史材料之間停留，從零散的細節中，讀回人與土地依存的深刻記憶。'),
 'yuan':('1632年的夜裡，燭火微光映著木桌。遠渡而來的西班牙神父提起羽毛筆，在手記裡記下島嶼北方的山勢、水路與聚落。傅玉安以歷史文獻為起點，運用生成式 AI 重構十七世紀的時空場景。神父的筆尖穿過雞籠社與淡水河口，記錄下往來水上的獨木舟、帆船運載的硫磺，以及族人最初開口說出的詞彙。邀請你藉由異鄉人的凝視，重新走進四百年前凱達格蘭族的生活：當歷史只留下片語，我們如何讓過往重新對我們說話？','十七世紀的微光下，西班牙神父在手記寫下北台灣的水路與聚落。傅玉安以歷史文獻為底，在影像中重現凱達格蘭族四百年前的生活剪影與相遇。'),
}
WORK_SOURCES={
 'abby':'空拍奇遇記 Abby.mp4',
 'suifen':'2026_探尋凱達格蘭族的遺跡_張穗芬.mp4',
 'kuncan':'凱達格蘭族的故事-坤燦.mp4',
 'wenjin':'凱達格蘭族的故事-黃文津.mp4',
 'yuan':'凱達格蘭1632-玉安.mov',
}

def first_frame(source, name):
 """Use the first decoded frame, including an intentional black opening."""
 target=SITE/'assets'/name
 if not args.prepare_media:
  if target.exists(): return 'assets/'+name
  raise FileNotFoundError(f'缺少現有媒體：{target}；請明確使用 --prepare-media 建立。')
 if not source.exists():
  if target.exists(): return 'assets/'+name
  raise FileNotFoundError(source)
 if not target.exists() or source.stat().st_mtime_ns>target.stat().st_mtime_ns:
  ffmpeg=shutil.which('ffmpeg')
  if not ffmpeg: raise RuntimeError('建立影片第一畫面封面需要 FFmpeg')
  subprocess.run([ffmpeg,'-hide_banner','-loglevel','error','-y','-i',str(source),
                  '-map','0:v:0','-frames:v','1','-vf',"scale=min(1280\\,iw):-2",'-q:v','2',str(target)],check=True)
 return 'assets/'+name

for w in WORKS:
 w['description'],w['short']=WORK_COPY[w['slug']]
 w['image']=first_frame(ROOT/WORK_SOURCES[w['slug']],w['slug']+'-first-frame.jpg')
INTERVIEW_POSTER=first_frame(ROOT/'穗芬談消失的台北原住民故事創作思維.mp4','suifen-interview-first-frame.jpg')
for key,media in ACTIVITY_MEDIA.items():
 media['video']['poster']=first_frame(SITE/media['video']['src'],'fieldwork-'+key+'-first-frame.jpg')

def save_md(name,title,paragraphs):
 if args.write_content:
  (CONTENT/name).write_text('# '+title+'\n\n'+'\n\n'.join(paragraphs)+'\n',encoding='utf-8')

def intro_parts(value):
 return [part.strip() for part in value.split('\n\n') if part.strip()]

def intro_lead(value):
 return intro_parts(value)[0]

def photo(src,caption='',cls='',priority=False,show_caption=True):
 caption=TEACHER_CAPTIONS.get(Path(src).name,caption)
 path=SITE/src
 with Image.open(path) as image: width,height=image.size
 loading='fetchpriority="high"' if priority else 'loading="lazy"'
 return f'<figure class="{cls}"><img src="{src}" width="{width}" height="{height}" alt="{e(caption)}" {loading}>'+ (f'<figcaption>{e(caption)}</figcaption>' if caption and show_caption else '')+'</figure>'

def row(url,image,label,title,intro,short,playable=False):
 caption=TEACHER_CAPTIONS.get(Path(image).name)
 picture=photo(image,caption) if caption else f'<img src="{image}" alt="{e(title)}" loading="lazy">'
 if playable: picture='<div class="work-poster">'+picture+'<span class="poster-play" aria-hidden="true">▶</span></div>'
 action='觀看作品' if playable else '閱讀故事'
 return f'<a class="entry" href="{url}"><div class="entry-image">{picture}</div><div class="entry-copy"><h3>{e(title)}</h3><span class="kicker">{e(label)}</span><p class="desktop-intro">{e(intro_lead(intro))}</p><p class="mobile-intro">{e(short)}</p><span class="entry-link">{action}</span></div></a>'

def legacy_body(html):
 # Old prose retains its established formatting; new components keep their arrows.
 protected=[]
 def protect(match):
  protected.append(match[0]); return f'__SHARED_{len(protected)-1}__'
 html=re.sub(r'<a class="(?:shared-card|primary-entry)\b.*?</a>|<span class="viewall-arrow".*?</span>',protect,html,flags=re.S)
 for old,new in [('老師的敘述','土地的記憶'),('老師的陳述','土地的記憶'),('故事總覽','故事目錄'),('田野與空拍','沿河而行'),('四堂田野與空拍紀實','沿河而行'),('同學作品','鏡頭裡的故事')]:
  html=html.replace(old,new)
 html=html.replace('四堂沿河而行紀實','沿河而行')
 html=re.sub(r'<div class="cover-lines".*?</div>','',html)
 html=html.replace('<span class="title-dot">。</span>','')
 html=re.sub(r'<span aria-hidden="true">[↗→←↑↓]</span>','',html)
 html=re.sub(r'[↗→←↑↓]','',html)
 html=html.replace('aria-label="回到頁首">','aria-label="回到頁首">回到頁首')
 def clean_heading(match):
  return match[1]+re.sub(r'[，、：。？！?！・‧]','',match[2])+match[3]
 html=re.sub(r'(<h[1-3][^>]*>)(.*?)(</h[1-3]>)',clean_heading,html,flags=re.S)
 html=re.sub(r'(<nav\b[^>]*>)(.*?)(</nav>)',lambda m:m[1]+re.sub(r'[，、：。？！?！・‧]','',m[2])+m[3],html,flags=re.S)
 html=html.replace('華麗轉向：','華麗轉向 ').replace('田野・空拍・創作紀實','文獻 走讀 空拍 創作')
 html=html.replace('<span>文獻 走讀 空拍 創作</span>','<span class="brand-subtitle"><span>飛越歷史</span> <span>紀錄土地</span></span>')
 html=html.replace('首頁 /','卷首 /')
 html=html.replace('閱讀老師、田野與鏡頭裡的故事','翻閱土地與影像的故事')
 html=html.replace('閱讀老師、田野與同學作品','翻閱土地與影像的故事')
 html=html.replace('原民故事</h1>','原民故事</h1>')
 for i,component in enumerate(protected): html=html.replace(f'__SHARED_{i}__',component)
 return html


def page(filename,title,body,home=False,legacy=True):
 if selected_pages is not None and filename not in selected_pages:
  return
 if legacy:
  body=legacy_body(body)
  title=legacy_body(title)
 body=re.sub(r'(<h[123]\b[^>]*>)沿著河尋找三個社的土地記憶(</h[123]>)',r'\1沿著河<br>尋找三個社的土地記憶\2',body)
 styles='<link rel="stylesheet" href="magazine.css?v=16">'
 if filename=='teacher.html':styles='<link rel="stylesheet" href="magazine.css?v=17">'
 if filename=='walks.html':styles+='<link rel="stylesheet" href="walks.css?v=1">'
 body_class=('home' if home else 'inner') + (' teacher-page' if filename=='teacher.html' else '')
 if filename.startswith('fieldwork-'): body_class+=' field-page'
 if filename in {'abby.html','suifen.html','kuncan.html','wenjin.html','yuan.html'}: body_class+=' work-page'
 if home: styles+='<link rel="stylesheet" href="editorial-home.css?v=7">'
 styles+='<link rel="stylesheet" href="reading-layout.css?v=1">'
 html=f'''<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="循著凱達格蘭的足跡，留下田野、空拍與創作的共同記憶。"><meta name="theme-color" content="#234f56"><title>{e(title)}｜消失的原民故事</title><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;600;700;800;900&family=Noto+Serif+TC:wght@400;500;600;700&display=swap" rel="stylesheet">{styles}<script src="documentary.js?v=5" defer></script></head>
<body class="{body_class}"><a class="skip" href="#main">跳到主要內容</a>{render_header(filename)}<main id="main">{body}</main><footer class="site-footer compact-footer"><a class="back-top ui-control" href="#main" aria-label="回到頁首">回到頁首</a></footer></body></html>'''
 (SITE/filename).write_text(html,encoding='utf-8')
 built_pages.append(filename)

# Web-sized copies; retain originals and photographic content.
for p in sorted((ROOT/'tmp/source-photos').glob('*.jpg')) if args.prepare_media else []:
 with Image.open(p) as im:
  im=im.convert('RGB');im.thumbnail((1800,1800));im.save(SITE/'assets'/('flight-'+p.stem+'.jpg'),quality=88,optimize=True)

HOME_PARAGRAPHS=[
 '北投、關渡、八里、錫口——有些名字，我們每天經過，卻未必知道它們曾經承載的故事。老師帶著文獻與古地圖，我們帶著各自的經驗，一起走向凱達格蘭族曾經生活的地方。',
 '從河岸與街廓，到十三行博物館的展場，我們在眼前的風景裡尋找線索。當空拍機升起，河灣、山勢與聚落的關係有了不同的尺度；回到地面，這些發現又成為彼此對話、各自創作的起點。',
 '這裡留下老師的敘述、四次田野與空拍紀實，以及同學們用影像寫成的故事。我們把一起走過、看過、思索過的片刻留在這裡，也邀請你循著這些足跡，重新觀看這片土地。',
]
save_md('home.md','消失的原民故事',HOME_PARAGRAPHS)
hero='''<section class="cover"><img class="cover-photo" src="assets/flight-0829-0080.jpg" alt="課程實際空拍的河面、河岸與山勢" fetchpriority="high"><div class="cover-lines" aria-hidden="true"><span></span><span></span><i></i></div><div class="cover-copy"><span class="kicker">循著凱達格蘭的足跡</span><h1>消失的<br>原民故事<span class="title-dot">。</span></h1><p>從地面走讀，到空中的觀看。<br>把土地的記憶，寫進我們的鏡頭。</p><a class="cover-button" href="works.html">走進故事 <span aria-hidden="true">↗</span></a></div><div class="cover-bottom"><span>田野・空拍・創作紀實</span><a href="#beginning">往下閱讀 ↓</a></div></section>'''
home_intro='<section class="home-intro wrap" id="beginning"><div class="intro-heading"><span class="kicker">我們一起出發尋找</span><h2>名字留了下來，<br>故事去了哪裡？</h2><div class="intro-index"><span>文獻</span><span>田野</span><span>空拍</span><span>創作</span></div></div><div class="intro-reading">'+''.join('<p>'+e(p)+'</p>' for p in HOME_PARAGRAPHS)+'<a class="text-link" href="works.html">沿著足跡，走進故事 ↗</a></div></section>'
home_close='<section class="home-close">'+photo('assets/teacher-photo-13-0.jpg','','home-group')+'<div><span class="kicker">共同留下的記憶</span><h2>同一片土地，<br>不同的觀看。</h2><a class="cover-button" href="works.html">閱讀老師、田野與同學作品 ↗</a></div></section>'
from editorial_home import render_entry
if selected_pages is None or 'index.html' in selected_pages:
 (SITE/'index.html').write_text(render_entry(),encoding='utf-8')
 built_pages.append('index.html')

overview='''<div class="wrap"><header class="page-heading"><a class="breadcrumb" href="index.html">首頁 /</a><span class="kicker">故事總覽</span><h1>每一次出發，<br>都有一條走進故事的路。</h1><p>從老師的敘述出發，沿著四次田野的足跡，<br class="desktop-break">看見同學們如何把土地與記憶，轉化成自己的作品。</p></header><nav class="category-nav" aria-label="內容分類"><a href="#teacher">老師的敘述</a><a href="#fieldwork">田野與空拍</a><a href="#works">同學作品</a></nav>'''
overview+='<section class="entry-section" id="teacher"><div class="list-heading"><span>01</span><div><span class="kicker">故事的起點</span><h2>老師的敘述</h2></div></div>'+row('teacher.html','assets/teacher-photo-3-0.jpg','何懷嵩・課程設計手記','華麗轉向：台北原民故事的知識共構教學實踐','一座很會遺忘的城市，如何重新讀回土地的記憶？老師從課程的起點寫起，留下文獻、走讀、空拍與創作之間，師生共同建立理解的過程。','從文獻走向現場，讀回土地與人的記憶。')+'</section>'
overview+='<section class="entry-section" id="fieldwork"><div class="list-heading"><span>02</span><div><span class="kicker">一起走過的現場</span><h2>四堂田野與空拍紀實</h2></div></div>'
for c in COURSES: overview+=row(f'fieldwork-{c["key"]}.html',f'assets/flight-{c["cover"]}.jpg',c['date']+'・'+c['place'],c['title'],c['intro'],c['short'])
overview+='</section><section class="entry-section" id="works"><div class="list-heading"><span>03</span><div><span class="kicker">各自寫成的故事</span><h2>同學作品</h2></div></div>'
for w in WORKS: overview+=row(w['slug']+'.html',w['image'],w['author']+'・'+w['duration'],w['title'],w['description'],w['short'],playable=True)
overview+='</section></div>'
page('stories.html','故事總覽',overview)
FIELDWORK_OVERVIEW=json.loads((CONTENT/'fieldwork-overview.json').read_text(encoding='utf-8'))
air_cards=[render_card(f'fieldwork-{c["key"]}.html',f'assets/flight-{c["cover"]}.jpg',c['title'],FIELDWORK_OVERVIEW['cards'][c['key']]['summary'],label=f'{c["place"]}｜{c["date"]}',cta=FIELDWORK_OVERVIEW['cards'][c['key']]['cta']) for c in COURSES]
page('fieldwork.html','空拍紀錄',render_overview('空拍紀錄',FIELDWORK_OVERVIEW['lead'],'四次出發',air_cards,'fieldwork.html',show_breadcrumb=False,show_view_all=False),legacy=False)
work_cards=[render_card(w['slug']+'.html',w['image'],w['title'],CARD_SUMMARIES[w['slug']],label=w['author']+'｜'+w['duration'],playable=True) for w in WORKS]
page('works.html','影音創作',render_overview('影音創作','從共同走過的土地，長出各自觀看與敘說的方式。','鏡頭裡的故事',work_cards,'works.html',show_breadcrumb=False,show_view_all=False),legacy=False)
# Retain the supplied full-resolution photograph and export a web-sized copy.
intro_source=ROOT/INTRO_DATA['image_source']
intro_target=SITE/INTRO_DATA['image']
if args.prepare_media and intro_source.exists():
 with Image.open(intro_source) as source:
  preview=ImageOps.exif_transpose(source)
  preview.thumbnail((2560,2560),Image.Resampling.LANCZOS)
  preview.convert('RGB').save(intro_target,quality=90,optimize=True)
elif not intro_target.exists():
 raise FileNotFoundError(f'引言照片不存在：{intro_source}')
closing_source=ROOT/INTRO_DATA['closing_image_source'] if INTRO_DATA.get('closing_image_source') else None
if closing_source:
 closing_target=SITE/INTRO_DATA['closing_image']
 if args.prepare_media and closing_source.exists():
  with Image.open(closing_source) as source:
   preview=ImageOps.exif_transpose(source)
   preview.thumbnail((2560,2560),Image.Resampling.LANCZOS)
   preview.convert('RGB').save(closing_target,quality=90,optimize=True)
 elif not closing_target.exists():
  raise FileNotFoundError(f'引言結尾圖片不存在：{closing_source}')
page('intro.html','引言',render_intro(INTRO_DATA,photo),legacy=False)
if selected_pages is None or 'walks.html' in selected_pages:
 prepare_walks_photos(ROOT)
 page('walks.html','現場走讀',render_walks(ROOT,photo),legacy=False)

teacher_title,teacher_subtitle,teacher_institution,teacher_author=teacher_header(ROOT)
teacher_title_intro,teacher_title_separator,teacher_title_main=teacher_title.partition('：')
teacher_title_markup='<span class="teacher-title-intro">'+e(teacher_title_intro)+'</span><span class="teacher-title-main">'+e(teacher_title_main)+'</span>'
teacher_heading='<header class="article-heading wrap"><h1>'+teacher_title_markup+'</h1><p class="article-lead">'+e(teacher_subtitle.removeprefix('——'))+'</p><div class="teacher-byline"><p>'+e(teacher_institution)+'</p><p>'+e(teacher_author)+'</p></div></header>'
teacher_body=ordered_teacher(ROOT,write_content=args.write_content)
page('teacher.html',teacher_title,teacher_heading+'<article class="teacher-article">'+teacher_body+'</article>',legacy=False)

for idx,c in enumerate(COURSES):
 lead=''.join('<p>'+e(part).replace('\n','<br>')+'</p>' for part in intro_parts(c['intro']))
 body=f'<header class="article-heading wrap"><span class="kicker">{c["date"]}・{c["place"]}</span><h1>{c["title"]}</h1><div class="article-lead">{lead}</div></header>'
 body+=photo(f'assets/flight-{c["cover"]}.jpg','','field-cover',True)
 body+='<article class="field-article wrap"><div class="reading-block"><span class="kicker">這一次，為何出發</span><h2>把老師提出的問題，<br>帶到眼前的土地。</h2>'
 paragraphs=intro_parts(c['intro'])
 notice=(CONTENT/('notice-'+c['key']+'.md')).read_text(encoding='utf-8')
 for passage in notice.strip().split('\n\n'):
  if passage.startswith('# '):
   body+='<p class="document-title">'+e(passage[2:])+'</p>'
  elif passage.startswith('### '): body+='<h3>'+e(passage[4:])+'</h3>'
  elif passage.startswith('## '): body+='<h2>'+e(passage[3:])+'</h2>'
  else: body+='<p>'+e(passage)+'</p>'
  paragraphs.append(passage)
 body+='</div><section class="scene-section"><div class="section-heading"><span class="kicker">鏡頭裡的現場</span><h2>換一個高度，<br>重新觀看。</h2></div><div class="scene-grid">'
 for p,caption in c['photos']:
  body+=photo('assets/flight-'+p+'.jpg',caption,'scene-photo');paragraphs += [f'![{caption}](../assets/flight-{p}.jpg)',caption]
 body+='</div></section>'
 if c['key'] in ACTIVITY_MEDIA:
  clip=ACTIVITY_MEDIA[c['key']]['video']
  film_title=clip.get('title',c['place'].replace('・',' ')+'空拍紀實')
  body+='<section class="activity-film"><div class="section-heading"><span class="kicker">兩分鐘空拍紀實</span><p class="film-location">拍攝地點｜'+e(clip['location'])+'</p><h2>'+e(film_title)+'</h2></div>'
  body+=f'<video controls playsinline preload="none" poster="{clip["poster"]}" aria-label="{e(film_title)} 兩分鐘空拍影片"><source src="{clip["src"]}" type="video/mp4">您的瀏覽器無法播放此影片，<a href="{clip["src"]}">開啟空拍影片</a>。</video>'
  body+=f'<a class="film-open" href="{clip["src"]}"><span aria-hidden="true">▶</span> 開啟空拍影片</a>'
  if 'music' in clip and clip['music'].get('source_type')=='user_provided':
   pass
  elif 'music' in clip:
   score=clip['music']
   body+=f'<p class="music-credit">配樂 <a href="{e(score["page"])}">{e(score["title"])}</a> — Kevin MacLeod（incompetech.com）<br><a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a> 節錄與淡入淡出</p>'
  body+='</section>'
  paragraphs+=['## '+film_title,'拍攝地點｜'+clip['location'],f'影片：[{c["date"]}兩分鐘空拍](../{clip["src"]})']
 maps=sorted((SITE/'assets').glob('notice-'+c['key']+'-map-*.jpg'))
 if maps:
  body+='<section class="document-maps"><h2>在地圖上讀回風景</h2>'
  for mp in maps: body+=photo('assets/'+mp.name,'田野通告中的地景與空域參考圖','source-map')
  body+='</section>'
 if c['key']=='0903':
  museum='我們也把十三行博物館與歷史現場納入課程場域。十三行的展櫃裡，專注看著鎮館之寶的人面陶罐，反覆思索藝術美感在凱達格蘭人生活中的可能，那些被復原的生活情境模型，在走讀之後看起來完全不一樣了，學員不再是觀眾，而是帶著問題來對照答案的人。同一組展件，第一次看是知識，第二次看是證據。'
  caption='遺址博物館館研析：走讀之後再回到展場，學員看的不是展示，而是自己問題的答案。'
  body+='<section class="museum-story"><div class="reading-block"><span class="kicker">從地景，回到生活的線索</span><h2>在十三行，<br>讓看過的土地與展件相遇。</h2><p>'+e(museum)+'</p></div>'+photo('assets/teacher-photo-6-1.jpg',caption,'museum-photo')+'</section>'
  paragraphs+=['## 在十三行，讓看過的土地與展件相遇。',museum,caption]
 body+='</article><nav class="next-story wrap" aria-label="繼續閱讀">'
 body+='<a href="fieldwork.html">← 四堂紀實</a>'
 if idx<3:
  nxt=COURSES[idx+1];body+=f'<a href="fieldwork-{nxt["key"]}.html">下一次出發：{nxt["place"]} →</a>'
 else:body+='<a href="works.html">看見同學的作品 →</a>'
 body+='</nav>'
 save_md('fieldwork-'+c['key']+'.md',c['date']+' '+c['place']+'｜'+c['title'],paragraphs)
 page('fieldwork-'+c['key']+'.html',c['place']+'・'+c['title'],body)

def video(video_id,image,title,button='播放作品'):
 return f'<div class="video-shell" data-video="{video_id}"><img src="{image}" alt="{e(title)}影片封面" loading="lazy"><button type="button" class="play-button ui-control" aria-label="{e(button+'：'+title)}"><span class="play-icon" aria-hidden="true">▶</span>{button}</button></div><div class="video-links"><a href="https://drive.google.com/file/d/{video_id}/view" target="_blank" rel="noopener">在雲端開啟影片 ↗</a></div>'

for w in WORKS:
 body=f'<header class="article-heading wrap work-heading"><a class="breadcrumb" href="works.html">故事總覽 / 同學作品</a><span class="kicker">{w["author"]}・{w["duration"]}</span><h1>{w["title"]}</h1><p class="article-lead">{w["subtitle"]}</p></header><article class="work-reading wrap"><div class="work-introduction"><span class="kicker">這件作品的出發點</span><p>{w["description"]}</p></div>'+video(w['id'],w['image'],w['title'])+'</article>'
 if w['slug']=='abby':
  voiceover_intro='<p>十三行人究竟是不是凱達格蘭族的祖先？走進十三行博物館，Abby 從田野走讀中拍下的展件影像出發，結合語音敘事與情境音效，完成這份富有探索精神的配音成果。</p><p>透過《番社采風圖》的歷史圖說、一比一復原的干欄式住屋、細緻拍印的幾何陶罐紋樣，以及火塘邊的生活日常，將靜態的照片轉化為生動的歷史漫遊。這不只是一次課堂作業，更是讓走讀足跡有了聲音，讓沉睡千年的考古記憶在當代重新甦醒。</p>'
  voiceover_shell='<div class="video-shell" data-youtube="S2_Z2z-UeqE"><img src="assets/abby-voiceover-first-frame.jpg" alt="十三行人真的是凱達格蘭族的祖先嗎影片封面" loading="lazy"><button type="button" class="play-button ui-control" aria-label="播放作品：十三行人真的是凱達格蘭族的祖先嗎？"><span class="play-icon" aria-hidden="true">▶</span>播放作品</button></div><div class="video-links"><a href="https://youtu.be/S2_Z2z-UeqE" target="_blank" rel="noopener">在 YouTube 開啟影片 </a></div>'
  body+=f'<section class="interview wrap"><div class="work-introduction work-secondary"><span class="kicker">走讀配音功課・4 分 17 秒</span><h2>十三行人真的是凱達格蘭族的祖先嗎？</h2>{voiceover_intro}</div>{voiceover_shell}</section>'
 if w['slug']=='suifen':
  body+='<section class="interview wrap"><div class="section-heading"><span class="kicker">聽創作者說</span><h2>穗芬談創作思維</h2><p>從作品回到創作的過程，聽穗芬分享自己的觀看與思考。</p></div>'+video('1Uxapk_yIMfmXcGxE9QF9Vz7gEEVUsIFz',INTERVIEW_POSTER,'穗芬談創作思維','播放創作分享')+'</section>'
 body+='<section class="other-works wrap"><div class="section-heading"><span class="kicker">還有另一種觀看</span><h2>繼續走進其他作品</h2></div>'
 for v in WORKS:
  if v['slug']!=w['slug']:body+=row(v['slug']+'.html',v['image'],v['author'],v['title'],v['description'],v['short'],playable=True)
 body+='</section>'
 save_md(w['slug']+'.md',w['title'],['作者：'+w['author'],w['subtitle'],w['description'],'影片：https://drive.google.com/file/d/'+w['id']+'/view'])
 page(w['slug']+'.html',w['title'],body)

if args.write_content:
 (CONTENT/'works.json').write_text(json.dumps(WORKS,ensure_ascii=False,indent=2),encoding='utf-8')
 (CONTENT/'fieldwork.json').write_text(json.dumps(COURSES,ensure_ascii=False,indent=2),encoding='utf-8')
(SITE/'.nojekyll').touch()
print('Built '+str(len(built_pages))+' pages: '+', '.join(built_pages))
