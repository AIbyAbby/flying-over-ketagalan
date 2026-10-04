from pathlib import Path
from html import escape
import re
from pypdf import PdfReader

def ordered_teacher(root):
    reader=PdfReader(root/'老師.pdf')
    pages=[]
    for page in reader.pages:
        raw=page.extract_text() or ''
        raw=re.sub(r'^\s*\d+\s*\n','',raw)
        pages.append(''.join(raw.splitlines()).strip())
    # Remove photograph captions from prose; the photographs retain their
    # original sequence below. Keep the original text and paragraph order.
    captions=[
        r'學員空拍作品：.*?地形自己會說話。',
        r'社子島頭現場走讀：.*?最大的一張教材。',
        r'彼此賦能：.*?學員在和平島社寮砲台空拍雞籠社',
        r'文獻閱讀探討：.*?雞籠社男女',
        r'都市街廓裡的社址指認。.*?任何遺跡可以指認。',
        r'遺址博物館館研析：.*?自己問題的答案。',
        r'展件觀察：.*?漁獵與聚落型態。',
        r'飛行操作：.*?哪一個河灣。',
        r'河濱起飛：.*?都是課程的一部分。',
        r'出勤紀錄：.*?汐止峰仔峙社空拍創作',
        r'空拍成果：.*?未被書寫的地方史。',
        r'創作素材蒐集：.*?學員說故事時重新相遇。',
        r'課程結束。沒有找回任何一個消失的社，.*?由市民親手標記的作品。',
    ]
    text=''.join(pages)
    for caption in captions:text=re.sub(caption,'',text)
    headings=[
        '一、一座很會遺忘的城市',
        '二、把學員的專業，當成課程的解碼器',
        '三、四段迴圈：文獻、走讀、空拍、創作',
        '四、無人機不是玩具，是三度空間視角還原過程',
        '五、作品：知識共構的具體證據',
        '六、寫在課程之後',
    ]
    pictures=[
        ['teacher-photo-2-0.jpg'],
        ['teacher-photo-3-0.jpg','teacher-photo-4-0.jpg'],
        ['teacher-photo-5-0.jpg','teacher-photo-6-0.jpg','teacher-photo-6-1.jpg','teacher-photo-7-0.jpg'],
        ['teacher-photo-8-0.jpg','teacher-photo-9-0.jpg','teacher-photo-10-0.jpg','teacher-photo-10-1.jpg'],
        ['teacher-photo-12-0.jpg'],
        ['teacher-photo-13-0.jpg'],
    ]
    pieces=[]
    markdown=['# 華麗轉向：台北原民故事的知識共構教學實踐','\n作者：何懷嵩\n']
    for i,heading in enumerate(headings):
        start=text.index(heading)+len(heading)
        end=text.index(headings[i+1]) if i+1<len(headings) else len(text)
        content=text[start:end].strip()
        # Reflow complete sentences as reading paragraphs, without rewriting.
        sentences=re.split(r'(?<=[。！？])',content)
        paragraphs=[];current=''
        for sentence in sentences:
            current+=sentence
            if len(current)>=180:
                paragraphs.append(current);current=''
        if current:paragraphs.append(current)
        prose=''.join('<p>'+escape(p)+'</p>' for p in paragraphs)
        images=[]
        for filename in pictures[i]:
            im=f'<figure><img src="assets/{filename}" alt="課程的田野、空拍與同行者影像" loading="lazy"></figure>'
            images.append(im)
        # Text follows the PDF's six original sections. Their photos remain in
        # page order, including portrait images rather than forced crops.
        pieces.append(f'<article class="teacher-chapter"><div class="chapter-heading"><span class="chapter-number">{i+1:02d}</span><h2>{escape(heading[2:])}</h2></div><div class="chapter-reading">{prose}</div><div class="chapter-photos photos-{len(images)}">'+''.join(images)+'</div></article>')
        markdown.append('## '+heading+'\n\n'+'\n\n'.join(paragraphs)+'\n\n'+'\n'.join('![]('+p+')' for p in pictures[i]))
    (root/'02_網站/content/teacher-ordered.md').write_text('\n\n'.join(markdown)+'\n\n來源：老師.pdf，第1–13頁，依原章節及圖片順序整理。',encoding='utf-8')
    return '<section class="section teacher-book" id="teacher"><div class="section-heading"><span class="eyebrow">土地與記憶</span><h2>華麗轉向：<br>台北原民故事的知識共構教學實踐</h2><p class="teacher-byline">何懷嵩｜世新大學廣播電視電影學系副教授</p></div>'+''.join(pieces)+'</section>'
