"""Render the supplied essay and photo collages without rewriting the prose."""
from html import escape
import hashlib
import json
from PIL import Image, ImageOps
from shared_components import render_primary_link


def collage_groups(root):
    return json.loads((root / '02_網站/content/walks-collage.json').read_text(encoding='utf-8'))['groups']


def prepare_walks_photos(root):
    """Export missing web copies only; never crop or overwrite source photographs."""
    destinations = []
    record = root / '02_網站/content/walks-photo-sources.json'
    previous = {item['src']: item for item in json.loads(record.read_text(encoding='utf-8'))} if record.exists() else {}
    for group in collage_groups(root):
        for item in group['photos']:
            source = (root / item['source']).resolve()
            target = root / '02_網站' / item['src']
            if not target.exists():
                if not source.exists():
                    raise FileNotFoundError(f"走讀照片缺少：{item['source']}")
                with Image.open(source) as image:
                    preview = ImageOps.exif_transpose(image).convert('RGB')
                    preview.thumbnail((1600, 1600), Image.Resampling.LANCZOS)
                    preview.save(target, quality=88, optimize=True)
            digest = hashlib.sha256(source.read_bytes()).hexdigest() if source.exists() else previous.get(item['src'], {}).get('sha256')
            destinations.append({'source': item['source'], 'src': item['src'], 'sha256': digest})
    serialized = json.dumps(destinations, ensure_ascii=False, indent=2) + '\n'
    if not record.exists() or record.read_text(encoding='utf-8') != serialized:
        record.write_text(serialized, encoding='utf-8')


def render_collages(root, group_id=None, panel_index=None, show_heading=True):
    body = '<div class="walks-collages">'
    for group in collage_groups(root):
        if group_id is not None and group['id'] != group_id:
            continue
        heading_id = 'walks-photos-' + group['id']
        body += (f'<section class="walks-collage-group" aria-labelledby="{heading_id}">' if show_heading else '<section class="walks-collage-group" aria-label="' + escape(group["title"], quote=True) + '照片">')
        if show_heading:
            body += f'<h2 id="{heading_id}" class="reading-container">{escape(group["title"])}</h2>'
        photos = group['photos']
        panels = group.get('panels', [{'count': min(6, len(photos) - start), 'layout': 'feature'} for start in range(0, len(photos), 6)])
        if sum(spec['count'] for spec in panels) != len(photos):
            raise ValueError('拼貼分組數量與照片不符')
        start = 0
        for number, spec in enumerate(panels):
            panel = photos[start:start + spec['count']]
            start += spec['count']
            if panel_index is not None and number != panel_index:
                continue
            focus_layout = spec['layout'] == 'focus'
            small_layout = spec['layout'] == 'small'
            classes = 'walks-collage-panel' if len(panel) >= 5 else 'walks-collage-pair'
            if small_layout:
                classes += ' collage-small-panel'
            if spec['layout'] == 'exhibits':
                classes += ' collage-exhibit-panel'
            if spec['layout'] == 'museum-mirror':
                classes += ' collage-museum-mirror'
            if spec['layout'] == 'museum-finish':
                classes += ' collage-museum-finish'
            if focus_layout:
                classes += ' collage-focus-panel'
            body += f'<div class="{classes}">'
            for index, item in enumerate(panel):
                with Image.open(root / '02_網站' / item['src']) as image:
                    width, height = image.size
                role = ' collage-feature' if index == 0 and len(panel) >= 5 and not small_layout else ''
                is_wide = not small_layout and (index == 5 or (focus_layout and index == 4))
                role += ' collage-wide' if is_wide else ''
                role += ' collage-portrait' if is_wide and height > width else ''
                role += ' collage-focus-tall' if focus_layout and index == 3 else ''
                body += f'<figure class="collage-photo{role}" style="--photo-focus:{escape(item["focus"], quote=True)}">'
                body += f'<img src="{escape(item["src"], quote=True)}" alt="{escape(item["alt"], quote=True)}" width="{width}" height="{height}" loading="lazy" decoding="async"></figure>'
            body += '</div>'
        body += '</section>'
    return body + '</div>'



def render_walks(root, photo):
    chunks = (root / '02_網站/content/walks.md').read_text(encoding='utf-8').strip().split('\n\n')
    title = chunks.pop(0).removeprefix('# ')
    body = '<article class="walks-page"><header class="walks-heading reading-container"><h1>' + escape(title) + '</h1></header>'
    section = -1
    breaks = {0: [('air', 0)], 1: [('air', 1), ('air', 2)], 2: [('museum', 0), ('museum', 1)]}
    def panels(index):
        return ''.join(render_collages(root, group, number, show_heading=False) for group, number in breaks.get(index, []))
    for chunk in chunks:
        if chunk.startswith('## '):
            if section >= 0:
                body += panels(section) + '</section>'
            section += 1
            body += '<section class="walks-section" id="walks-section-' + str(section + 1) + '"><div class="reading-container"><h2>' + escape(chunk.removeprefix('## ')) + '</h2></div>'
        elif chunk.startswith('### '):
            body += '<div class="reading-container"><h3>' + escape(chunk.removeprefix('### ')) + '</h3></div>'
        elif chunk.startswith('!['):
            import re
            match = re.fullmatch(r'!\[(.*?)\]\(\.\./(.*?)\)', chunk)
            if not match:
                raise ValueError('Unexpected walks photo markup')
            caption, src = match.groups()
            with Image.open(root / '02_網站' / src) as image:
                width, height = image.size
            body += '<div class="reading-container"><figure class="museum-photo"><img src="' + escape(src, quote=True) + '" alt="' + escape(caption, quote=True) + '" width="' + str(width) + '" height="' + str(height) + '" loading="lazy" decoding="async" style="display:block;width:100%;height:auto"><figcaption>' + escape(caption) + '</figcaption></figure></div>'
        else:
            body += '<div class="reading-container"><p>' + escape(chunk) + '</p></div>'
    body += panels(section) + '</section>'
    body += '<nav class="walks-next reading-container" aria-label="繼續探索">'
    body += render_primary_link('works.html', '觀看影音創作')
    body += '<a class="text-link" href="fieldwork.html">閱讀四次空拍紀錄 →</a></nav></article>'
    return body
