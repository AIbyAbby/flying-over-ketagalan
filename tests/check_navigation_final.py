"""Independent structural acceptance for the approved navigation changes."""
from pathlib import Path
from lxml import html
import argparse, hashlib, json, re, subprocess

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / '02_網站'
WORKS = ['suifen', 'kuncan', 'wenjin', 'yuan', 'abby']
MAIN = ['intro', 'teacher', 'fieldwork', 'walks', 'works']

def has_class(node, cls):
    return cls in node.get('class', '').split()

def check(phase):
    issues = []
    pages = {p.stem: html.fromstring(p.read_text(encoding='utf-8')) for p in SITE.glob('*.html')}
    def require(ok, message):
        if not ok: issues.append(message)
    for slug, doc in pages.items():
        markup=(SITE/(slug+'.html')).read_text(encoding='utf-8')
        original=subprocess.check_output(['git','show','ef8ca87:02_網站/'+slug+'.html'],cwd=ROOT).decode('utf-8').replace('\r\n','\n')
        player_pattern=r'<div\b[^>]*class="[^"]*\bvideo-shell\b[^"]*"[^>]*>.*?</div>'
        require(re.findall(player_pattern,markup,re.S)==re.findall(player_pattern,original,re.S),f'{slug}: player differs from task starting commit')
        olddoc=html.fromstring(original)
        def prose(d): return [''.join(n.itertext()) for n in d.xpath('//main//p|//main//h1|//main//h2|//main//h3') if not n.xpath('ancestor::nav')]
        iterator=iter(prose(doc))
        require(all(any(text==candidate for candidate in iterator) for text in prose(olddoc)),f'{slug}: starting prose/order changed')
        cards = doc.xpath('//*[@class]')
        cards = [n for n in cards if has_class(n, 'shared-card') or has_class(n, 'intro-method') or has_class(n, 'entry')]
        for i, card in enumerate(cards):
            links = card.xpath('.//a[@href]')
            require(card.tag != 'a' and len(links) == 1 and bool(links[0].xpath('ancestor::h3')), f'{slug}: card {i} must have one title link')
        if slug in WORKS:
            require(len(doc.xpath('//a[@class="player-fallback"]')) == 1, f'{slug}: verified fallback missing')
        if phase >= 2:
            require(len(doc.xpath('//header[@class="site-header final-header"]')) == 1, f'{slug}: header')
            require(len(doc.xpath('//details[@class="site-menu"]')) == 1, f'{slug}: menu')
            nav = doc.xpath('//nav[@class="desktop-navigation"]/a')
            require([a.get('href').split('/')[-1] for a in nav] == [s+'.html' for s in MAIN], f'{slug}: nav order')
            require(not doc.xpath('//*[@class="air-toggle"]|//*[@id="air-subnav"]'), f'{slug}: old dropdown remains')
            require(bool(doc.xpath('//body[@id="top"]//a[@href="#top"]')), f'{slug}: top')
            require(bool(doc.xpath('//a[@class="skip"]')), f'{slug}: skip')
            require(bool(doc.xpath('//link[@rel="canonical"]')), f'{slug}: canonical')
            for prop in ['og:title','og:description','og:type','og:url','og:locale','og:image']:
                require(len(doc.xpath(f'//meta[@property="{prop}"]')) == 1, f'{slug}: {prop}')
        if phase >= 3:
            if slug in MAIN: require(bool(doc.xpath('//nav[@class="final-sequence"]')), f'{slug}: page sequence')
            if slug in WORKS:
                require(bool(doc.xpath('//nav[@class="work-action-bar"]')), f'{slug}: action bar')
                switch = doc.xpath('//details[@class="work-switcher"]')
                require(len(switch) == 1 and [a.get('href') for a in switch[0].xpath('.//a')] == [s+'.html' for s in WORKS], f'{slug}: switch order')
                require(bool(doc.xpath('//nav[@class="final-work-sequence"]')), f'{slug}: work sequence')
                index=WORKS.index(slug)
                expected=[(WORKS[index-1] if index else 'works')+'.html','works.html',(WORKS[index+1] if index<4 else 'works')+'.html']
                require([a.get('href') for a in doc.xpath('//nav[@class="work-action-bar"]/a')]==expected,f'{slug}: previous/next endpoints')
                require(markup.index('class="work-switcher"')<markup.index('class="video-shell'),f'{slug}: switcher before content')
                require(bool(doc.xpath('//nav[@class="final-breadcrumb"]/a[@href="index.html"]')),f'{slug}: homepage route missing')
            if slug=='fieldwork':
                require(len(doc.xpath('//nav[@class="fieldwork-local-nav wrap"]/a'))==4,'four activities reachable within three clicks')
    original_js=subprocess.check_output(['git','show','ef8ca87:02_網站/documentary.js'],cwd=ROOT).replace(b'\r\n',b'\n')
    require((SITE/'documentary.js').read_bytes().replace(b'\r\n',b'\n')==original_js,'documentary.js changed')
    print(json.dumps({'phase':phase, 'pages':len(pages), 'failures':issues}, ensure_ascii=False, indent=2))
    assert not issues

if __name__ == '__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--phase',type=int,default=3)
    check(parser.parse_args().phase)
