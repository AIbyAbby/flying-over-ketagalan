from html import escape
import re
from pypdf import PdfReader

HEADINGS = [
    '一、一座很會遺忘的城市',
    '二、把學員的專業，當成課程的解碼器',
    '三、四段迴圈：文獻、走讀、空拍、創作',
    '四、無人機不是玩具，是三度空間視角還原過程',
    '五、作品：知識共構的具體證據',
    '六、寫在課程之後',
]
CAPTIONS = [
    ('teacher-photo-2-0.jpg', r'學員空拍作品：.*?地形自己會說話。'),
    ('teacher-photo-3-0.jpg', r'社子島頭現場走讀：.*?最大的一張教材。'),
    ('teacher-photo-4-0.jpg', r'彼此賦能：.*?學員在和平島社寮砲台空拍雞籠社'),
    ('teacher-photo-5-0.jpg', r'文獻閱讀探討：.*?雞籠社男女'),
    ('teacher-photo-6-0.jpg', r'都市街廓裡的社址指認。.*?任何遺跡可以指認。'),
    ('teacher-photo-6-1.jpg', r'遺址博物館館研析：.*?自己問題的答案。'),
    ('teacher-photo-7-0.jpg', r'展件觀察：.*?漁獵與聚落型態。'),
    ('teacher-photo-8-0.jpg', r'飛行操作：.*?哪一個河灣。'),
    ('teacher-photo-9-0.jpg', r'河濱起飛：.*?都是課程的一部分。'),
    ('teacher-photo-10-0.jpg', r'出勤紀錄：.*?汐止峰仔峙社空拍創作'),
    ('teacher-photo-10-1.jpg', r'空拍成果：.*?未被書寫的地方史。'),
    ('teacher-photo-12-0.jpg', r'創作素材蒐集：.*?學員說故事時重新相遇。'),
    ('teacher-photo-13-0.jpg', r'課程結束。沒有找回任何一個消失的社，.*?由市民親手標記的作品。'),
]
SELECTIONS = [
    ('台北是座很會遺忘的城市。', '南港社區大學與'),
    ('南港社區大學與', '社區大學的成人教育'),
    ('這一班的組成極具多元性：', '人文與教育背景的學員'),
    ('最珍貴的是原漢學員之間的對話。', '社子島頭現場走讀：'),
    ('課程的骨架是一個可以反覆運轉的迴圈：', '文獻研讀不從'),
    ('現場走讀則是把矛盾帶到地面上求證。', '都市街廓裡的社址指認。'),
    ('我們也把十三行博物館與歷史現場納入課程場域。', '遺址博物館館研析：'),
    ('課程的立場很清楚：', '且把這件事稱為'),
    ('年齡不是障礙。', '出勤紀錄：'),
    ('最後一段是創作。', '高坤燦的《'),
    ('六件作品，六種進入歷史的方法。', '創作素材蒐集：'),
    ('這門工作坊讓我更確定一件事：', '它同時回應了'),
    ('社子島頭空拍那天，', '課程結束。沒有找回'),
]

def source_text(root):
    pages=[]
    for page in PdfReader(root/'02_網站/materials/teacher.pdf').pages:
        raw=re.sub(r'^\s*\d+\s*\n', '', page.extract_text() or '')
        pages.append(''.join(raw.splitlines()).strip())
    return ''.join(pages)

def teacher_header(root):
    raw = PdfReader(root/'02_網站/materials/teacher.pdf').pages[0].extract_text() or ''
    lines = [line.strip() for line in raw.splitlines() if line.strip()]
    if lines[0] != '1' or len(lines) < 5:
        raise ValueError('Unexpected teacher PDF title block')
    return lines[1:5]

def ordered_teacher(root,write_content=True):
    text=source_text(root)
    events=[]
    for heading in HEADINGS: events.append((text.index(heading),'heading',heading))
    for filename,pattern in CAPTIONS:
        match=re.search(pattern,text)
        if not match: raise ValueError('Missing original caption: '+filename)
        events.append((match.start(),'photo',(filename,match.group())))
    events.sort(key=lambda e:e[0])
    # Every interval between headings and captions is prose, including passages
    # omitted by the former selection list. Retain the source's complete order.
    full=[]
    cursor=text.index(HEADINGS[0])
    for pos,kind,value in events:
        if pos>cursor:
            passage=text[cursor:pos].strip()
            if passage: full.append((cursor,'paragraph',passage))
        full.append((pos,kind,value))
        cursor=pos+len(value if kind=='heading' else value[1])
    if text[cursor:].strip(): full.append((cursor,'paragraph',text[cursor:].strip()))
    events=full
    title, subtitle, institution, author = teacher_header(root)
    pieces=[];markdown=['# '+title, subtitle, institution, author];opened=False
    for _,kind,value in events:
        if kind=='heading':
            if opened: pieces.append('</section>')
            i=HEADINGS.index(value)+1
            display_heading = re.sub(r'^[一二三四五六]、', '', value)
            topic, separator, detail = display_heading.partition('：')
            heading_html = ('<span class="teacher-heading-topic">'+escape(topic+separator)+'</span>'+escape(detail)) if separator else escape(display_heading)
            pieces.append(f'<section class="teacher-chapter" id="chapter-{i}"><div class="chapter-heading"><h2>{heading_html}</h2></div>')
            markdown.append('## '+value);opened=True
        elif kind=='paragraph':
            paragraphs=[];current=''
            for sentence in re.split(r'(?<=[。！？])',value):
                current+=sentence
                if len(current)>=150: paragraphs.append(current);current=''
            if current: paragraphs.append(current)
            pieces.append('<div class="chapter-reading">'+''.join('<p>'+escape(p)+'</p>' for p in paragraphs)+'</div>');markdown.append(value)
        else:
            filename,caption=value
            if filename == 'teacher-photo-6-1.jpg':
                caption = caption.removeprefix('遺址博物館館研析：')
            pieces.append(f'<figure class="teacher-photo"><img src="assets/{filename}" alt="{escape(caption)}" loading="lazy"><figcaption>{escape(caption)}</figcaption></figure>')
            markdown.append(f'![{caption}](../assets/{filename})\n\n{caption}')
    if opened: pieces.append('</section>')
    if write_content:
        (root/'02_網站/content/teacher-ordered.md').write_text('\n\n'.join(markdown)+'\n',encoding='utf-8')
    return ''.join(pieces)
