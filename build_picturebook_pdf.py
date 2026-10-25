"""Preserve the 24 original slide pages as a PDF and a native HTML reading gallery."""
from pathlib import Path
import argparse
import json
import subprocess
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image, ImageOps, ImageDraw
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent
SITE = ROOT / '02_網站'


def build(source):
    images = SITE / 'assets/shumin-picturebook-pages'
    images.mkdir(exist_ok=True)
    output = SITE / 'materials/shumin-picturebook.pdf'
    output.parent.mkdir(exist_ok=True)
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(source),
                    '-vf', 'select=eq(mod(n\\,120)\\,60)', '-fps_mode', 'vfr', '-q:v', '2',
                    str(images / 'page-%02d.jpg')], check=True)
    pages = sorted(images.glob('page-*.jpg'))
    assert len(pages) == 24, f'Expected 24 stable slide pages; got {len(pages)}'
    # One identical, symmetric crop for every page, preserving the outermost text.
    crop = (48, 48, 1872, 1032)
    for page in pages:
        with Image.open(page) as picture:
            assert picture.size == (1920, 1080)
            trimmed = picture.crop(crop)
        trimmed.save(page, quality=95, subsampling=0)
    width, height = 1824, 984
    pdf = canvas.Canvas(str(output), pagesize=(width/2, height/2), pageCompression=1)
    pdf.setTitle('《秀朗尪姨‧金娘傳奇》故事繪本')
    pdf.setAuthor('侯淑敏')
    pdf.setSubject('依原影片頁面順序保存的圖文繪本；畫面文字非可搜尋文字層。')
    for i, page in enumerate(pages, 1):
        with Image.open(page) as picture:
            assert picture.size == (width, height)
        pdf.bookmarkPage(f'page-{i}')
        pdf.addOutlineEntry(f'Page {i:02d}', f'page-{i}', level=0)
        pdf.drawImage(ImageReader(str(page)), 0, 0, width=width/2, height=height/2)
        pdf.showPage()
    pdf.save()
    reader = PdfReader(output)
    assert len(reader.pages) == 24
    manifest = {'pdf': 'materials/shumin-picturebook.pdf', 'pages': [str(p.relative_to(SITE)).replace('\\', '/') for p in pages],
                'page_count': 24, 'source_id': '111qvYNDHvsmGtVBa3raUzu4Qm7ezSA7D',
                'source_times_seconds': [2 + i * 4 for i in range(24)], 'text_mode': 'original-frame-image',
                'uniform_crop_pixels': {'left':48,'right':48,'top':48,'bottom':48}, 'page_image_size':[width,height]}
    (SITE / 'content/shumin-picturebook-pdf.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    sheet = Image.new('RGB', (1600, 6*245), 'white')
    draw = ImageDraw.Draw(sheet)
    for i, page in enumerate(pages):
        x, y = (i % 4)*400, (i//4)*245
        with Image.open(page) as picture:
            sheet.paste(ImageOps.contain(picture, (400,225)), (x,y+20))
        draw.text((x+6,y+4), f'Page {i+1:02d} / {2+i*4}s', fill='black')
    (ROOT/'scratch').mkdir(exist_ok=True)
    sheet.save(ROOT/'scratch/picturebook-pdf-pages.jpg')
    print(f'PDF: {len(reader.pages)} pages, {output.stat().st_size} bytes')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    build(parser.parse_args().source)
