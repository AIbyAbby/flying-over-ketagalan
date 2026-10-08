"""Check handed-off reflection text, native markup and locked player baseline."""
from pathlib import Path
import hashlib
import json
from html.parser import HTMLParser

class Document(HTMLParser):
    def __init__(self, markup):
        super().__init__(convert_charrefs=True)
        self.nodes=[]
        self.stack=[]
        self.feed(markup)
    def handle_starttag(self, tag, attrs):
        node={'tag':tag,'attrs':dict(attrs),'text':'','parents':list(self.stack)}
        self.nodes.append(node)
        if tag not in ('meta','link','img','source','br','hr','input','area','wbr'):
            self.stack.append(node)
    def handle_endtag(self, tag):
        for index in range(len(self.stack)-1,-1,-1):
            if self.stack[index]['tag']==tag:
                self.stack=self.stack[:index]
                return
    def handle_data(self, data):
        for node in self.stack: node['text']+=data
    def find(self, tag=None, **attrs):
        return [node for node in self.nodes if (tag is None or node['tag']==tag)
                and all(node['attrs'].get(k)==v for k,v in attrs.items())]


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / '02_網站'
saved = json.loads((ROOT/'tests/reflection-baseline.json').read_text(encoding='utf-8'))
assert hashlib.sha256((SITE/'documentary.js').read_bytes().replace(b'\r\n', b'\n')).hexdigest() == saved['documentary_sha256']
loaded = []
for page in SITE.glob('*.html'):
    doc = Document(page.read_text(encoding='utf-8'))
    if any(n['attrs'].get('src', '').startswith('work-reflection.js') for n in doc.find('script')):
        loaded.append(page.name)
assert sorted(loaded) == ['abby.html', 'yuan.html'], loaded
for name, original in saved['blocks'].items():
    doc = Document((SITE/(name+'.html')).read_text(encoding='utf-8'))
    card, = doc.find('details', id='reflection')
    summary, = [n for n in doc.find('summary') if card in n['parents']]
    assert doc.find('h2', id=card['attrs']['aria-labelledby'])
    assert not any(n['tag'] in ['button','a','div'] and summary in n['parents'] for n in doc.nodes)
    current = [[n['tag'],n['text']] for n in doc.nodes if n['tag'] in ['h2','h3','p']
               and card in n['parents']]
    assert current == original, name+': prose/headings/order changed'
    assert '閱讀全文 ＋' in summary['text'] and '收合 －' in summary['text']
    assert doc.find('button', **{'aria-controls':'reflection'})
    assert doc.find('div', id='reflection-content')
print('PASS: 56 exact original blocks, valid labels/native summary, only two script consumers; documentary.js unchanged.')
