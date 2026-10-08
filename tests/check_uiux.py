"""Static checks: preserve approved prose and video destinations through UI changes."""
from pathlib import Path
from urllib.parse import urlsplit
import json
from check_final_polish import Document

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / '02_網站'


def check():
    baseline = json.loads((ROOT/'tests/uiux-content-baseline.json').read_text(encoding='utf-8'))
    failures = []
    for filename, saved in baseline.items():
        path = SITE/filename
        markup = path.read_text(encoding='utf-8')
        doc = Document(markup)
        paragraphs = [n['text'] for n in doc.nodes if n['tag']=='p' and any(a['tag']=='main' for a in n['parents'])]
        # Added navigation copy is allowed, but approved prose must remain in order.
        iterator = iter(paragraphs)
        if not all(any(old == text for text in iterator) for old in saved['paragraphs']):
            failures.append(filename+': original prose/order changed')
        links = [n['attrs'].get('href') for n in doc.nodes if n['tag']=='a' and ('youtu.be/' in n['attrs'].get('href','') or 'drive.google.com/file/' in n['attrs'].get('href',''))]
        if links != saved['external_video_links']:
            failures.append(filename+': video links changed')
        videos = [(n['tag'],{k:v for k,v in n['attrs'].items() if k in ['data-youtube','data-drive','href','src']}) for n in doc.nodes if any('video-shell' in a['attrs'].get('class','').split() for a in n['parents']) and n['tag'] in ['a','button','iframe']]
        if videos != [(tag,attrs) for tag,attrs in saved['videos']]:
            failures.append(filename+': video controls/IDs changed')
        if len(doc.find('h1')) != 1:
            failures.append(filename+': expected one h1')
        if not doc.find('html',lang='zh-Hant-TW') or 'noindex' in markup.lower():
            failures.append(filename+': language/indexability changed')
        if '［聯絡方式待補］' not in markup:
            failures.append(filename+': contact placeholder missing')
        for node in doc.nodes:
            for attribute in ('src','href'):
                value=node['attrs'].get(attribute,'')
                if not value or urlsplit(value).scheme or value.startswith('//'):
                    continue
                relative=urlsplit(value).path.removeprefix('/flying-over-ketagalan/')
                target=SITE/relative if relative else path
                if not target.exists():
                    failures.append(filename+': missing '+value)
    assert not failures, '\n'.join(failures)
    print(f'PASS: {len(baseline)} pages; approved paragraphs/order, video controls/IDs, language, contact and paths preserved.')


if __name__ == '__main__':
    check()
