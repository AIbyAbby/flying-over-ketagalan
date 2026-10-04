from pathlib import Path
from html import escape
from pypdf import PdfReader

FIELD_EXCERPTS={
 '0829': [('水文交匯與古地景','聚焦基隆河與淡水河交會口，對望關渡宮與「干豆門」歷史咽喉，對照河口地景的古今變遷。'),('凱達格蘭生活想像','結合河口濕地與蘆葦景觀，構思平埔族凱達格蘭社群昔日倚水而居、漁獵遊牧的生活情境，作為後續合成地圖與虛擬人視覺化素材。'),('生態指認','涵蓋關渡水鳥保護區的動態生態影像，豐富在地田野資料庫。')],
 '0903': [('生活空間的影像素材','本計畫旨在透過影像重建凱達格蘭社群（淡水社、八里社、北投社遷居路線）的歷史生活空間想像，並提供後製合成地圖與虛擬人物疊加之素材。'),('淡水河口意象與淡江大橋','三鏡頭切換（24mm 廣角呈現河口宏觀氣勢、70mm/166mm 中長焦壓縮淡江大橋與河口對岸八里觀音山的空間關聯）。'),('淡水社生活區域與老街','記錄舊時聚落與現代河岸交錯的空間感；走訪鼻頭街捕捉傳統聚落紋理與地形起伏。')],
 '0905': [('計畫主題','重構凱達格蘭族（雞籠社）歷史居住想像、空間變遷與當代海岸地景敘事。'),('移動方式','定點集合＋彈性串聯八尺門、正濱漁港與和平橋周邊狹窄巷弄。'),('核心拍攝重點','為後續歷史合成地圖（Map Compositing）與虛擬歷史人物／社群想像（Virtual Avatar / Spatial Visualizations）累積豐富的空間素材。')],
 '0910': [('河岸與水尾灣','基隆河岸汐止段與水尾灣園區：記錄河道演變與原住民族沿河墾殖、建聚之地形空間。'),('聚落與城市地景','新社舊社橋與社後地區：探尋「峰仔峙社」歷史聚落核心，對比當代都市地景與昔日平埔族群社址。'),('地理想像與延伸場域','原住民公園與小南港山：從小南港山高位俯瞰基隆河彎道與平原全景，建立峰仔峙社群生活空間的地理想像與空間軸線。')]
}

def field_excerpt(key):
 # Exact transcriptions of selected first-page passages; spelling and punctuation
 # normalized only where the scan breaks lines. No private contact details.
 body=''.join(f'<div><h3>{escape(h)}</h3><p>{escape(t)}</p></div>' for h,t in FIELD_EXCERPTS[key])
 return '<section class="pdf-excerpts">'+body+'</section>'

def teacher_excerpts(root):
 reader=PdfReader(root/'老師.pdf')
 selections=[
 (0,'一、一座很會遺忘的城市','台北是座很會遺忘的城市。','南港社區大學與'),
 (3,'文獻、走讀、空拍與創作','課程的骨架是一個可以反覆運轉的迴圈：','文獻研讀不从'),
 (6,'空拍，讓地形自己說話','課程的立場很清楚：','且把這件事'),
 (11,'寫在課程之後','這門工作坊讓我更確定一件事：','它同時回應')
 ]
 figures=['teacher-photo-2-0.jpg','teacher-photo-3-0.jpg','teacher-photo-10-1.jpg','teacher-photo-13-0.jpg']
 parts=[]
 for i,(p,h,start,end) in enumerate(selections):
  text=reader.pages[p].extract_text() or ''
  text=text[text.index(start):]
  # These selections follow complete original paragraphs, not generated prose.
  if i==1:end='文獻研讀不從'
  if end in text:text=text[:text.index(end)]
  if i==2:text=text.split('課程的立場很清楚：',1)[1];text='課程的立場很清楚：'+text
  text=''.join(text.splitlines()).strip()
  parts.append(f'<article class="original-excerpt"><div><h3>{escape(h)}</h3><p>{escape(text)}</p></div><figure><img src="assets/{figures[i]}" alt="課程中的空拍、走讀與學員現場紀錄" loading="lazy"></figure></article>')
  (root/'02_網站/content'/f'teacher-excerpt-{p+1}.md').write_text(f'# {h}\n\n{text}\n\n來源：老師.pdf，第 {p+1} 頁。\n',encoding='utf-8')
 return '<section class="section original-reading"><div class="section-heading"><span class="eyebrow">尋找消失的原民故事</span><h2>從城市的日常，<br>讀回土地的記憶。</h2><p>地名仍在，故事卻逐漸遠去。從文獻的線索走入街廓與水岸，再讓空中的視野與地面的經驗相互對照，這是一段師生共同認識土地的過程。</p></div>'+''.join(parts)+'</section>'

def archive_dates():
 dates=['08.27','08.29','09.03','09.05','09.10','09.12']
 cards=''.join(f'<span>{d}<small>第 {i+1} 次課程</small></span>' for i,d in enumerate(dates))
 return '<section class="section course-overview"><div class="section-heading"><span class="eyebrow">六堂課的足跡 / 2026</span><h2>從老師的陳述，走進田野與影像。</h2><p>六個上課日，串起文獻、現場、空拍與學員作品。沿著河灣與聚落，辨認曾經的生活；把地面上的疑問帶到空中，也把鏡頭裡的發現帶回彼此的討論。</p></div><div class="course-dates">'+cards+'</div><a class="text-link" href="fieldwork.html">沿著課程的足跡，走進現場 →</a></section>'
