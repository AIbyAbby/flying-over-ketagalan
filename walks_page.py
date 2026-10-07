"""Render the supplied photo essay from its Markdown source, without rewriting prose."""
from html import escape
from pathlib import Path
import json
from PIL import Image, ImageOps
from shared_components import render_primary_link


def prepare_walks_photos(root):
    """Export only missing web copies; preserve all five originals."""
    sources = sorted((root / '十三行').glob('*.jpg'))
    expected = ('261003_1', '261003_2', '261003_3', '261003_7', '261004_4')
    record = root / '02_網站/content/walks-photo-sources.json'
    previous = {item['src']: item['source'] for item in json.loads(record.read_text(encoding='utf-8'))} if record.exists() else {}
    destinations = []
    for suffix in expected:
        relative = f'assets/walks-museum-{suffix}.jpg'
        target = root / '02_網站' / relative
        source = next((p for p in sources if p.stem.endswith(suffix)), None)
        if not target.exists():
            if source is None:
                raise FileNotFoundError(f'十三行照片缺少：{suffix}')
            with Image.open(source) as image:
                preview = ImageOps.exif_transpose(image).convert('RGB')
                preview.thumbnail((1600, 1600), Image.Resampling.LANCZOS)
                preview.save(target, quality=88, optimize=True)
        destinations.append({'source': str(source.relative_to(root)) if source else previous[relative], 'src': relative})
    serialized = json.dumps(destinations, ensure_ascii=False, indent=2) + '\n'
    if not record.exists() or record.read_text(encoding='utf-8') != serialized:
        record.write_text(serialized, encoding='utf-8')


def render_walks(root, photo):
    chunks = (root / '02_網站/content/walks.md').read_text(encoding='utf-8').strip().split('\n\n')
    title = chunks.pop(0).removeprefix('# ')
    body = '<article class="walks-page"><header class="walks-heading reading-container">'
    body += '<span class="kicker">走讀紀錄・課程心得</span><h1>' + escape(title) + '</h1>'
    body += '</header>'
    section = -1
    paragraph = 0
    for chunk in chunks:
        if chunk.startswith('## '):
            if section >= 0:
                body += '</section>'
            section += 1
            paragraph = 0
            heading = chunk.removeprefix('## ')
            parts = heading.split('｜', 1)
            body += f'<section class="walks-section" id="walks-section-{section + 1}">'
            body += '<div class="reading-container"><h2>' + escape(parts[0])
            if len(parts) == 2:
                body += '<span class="walks-heading-detail">' + escape(parts[1]) + '</span>'
            body += '</h2></div>'
            continue
        paragraph += 1
        body += '<div class="reading-container"><p>' + escape(chunk) + '</p></div>'
        if section == 0 and paragraph == 2:
            body += photo('assets/flight-0829-0048.jpg', '兩側河水環抱島身，住屋沿著狹長的土地安頓', 'walks-photo media-container')
        if section == 0 and paragraph == 4:
            body += photo('assets/flight-0905-0030.jpg', '和平島｜同行者在山坡高處共同觀看港灣', 'walks-photo media-container')
        if section == 0 and paragraph == 7:
            body += '<div class="walks-gallery media-container" aria-label="十三行博物館參訪照片">'
            for suffix, caption in [
                ('261003_1', '十三行博物館｜展場裡的講解與交流'),
                ('261003_2', '十三行博物館｜用鏡頭記錄展場內容'),
                ('261003_3', '十三行博物館｜停下腳步，細看展示內容'),
            ]:
                body += photo(f'assets/walks-museum-{suffix}.jpg', caption, 'walks-gallery-photo walks-photo-' + suffix.replace('_', '-'))
            body += '</div><div class="walks-gallery walks-gallery-pair media-container">'
            for suffix, caption in [
                ('261003_7', '十三行博物館｜留下參訪的身影'),
                ('261004_4', '十三行博物館｜觀看復原的生活情境'),
            ]:
                body += photo(f'assets/walks-museum-{suffix}.jpg', caption, 'walks-gallery-photo walks-photo-' + suffix.replace('_', '-'))
            body += '</div>'
        if section == 1 and paragraph == 2:
            body += photo('assets/flight-0829-0042.jpg', '一起走到河岸的夥伴，把共同的發現留在合影裡', 'walks-photo media-container')
    body += '</section><nav class="walks-next reading-container" aria-label="繼續探索">'
    body += render_primary_link('works.html', '看看同學的影音創作')
    body += '<a class="text-link" href="fieldwork.html">閱讀四次空拍紀錄 →</a></nav></article>'
    return body
