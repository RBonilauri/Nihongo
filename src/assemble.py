import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, 'build'); os.makedirs(BUILD, exist_ok=True)
sys.path.insert(0, os.path.join(HERE, 'content'))
import html, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import SECTIONS
from bs4 import BeautifulSoup
E = html.escape

def table(b):
    h = '<div class="scroll-x"><table class="particle-grid"><thead><tr>' + ''.join(f'<th>{E(x)}</th>' for x in b['headers']) + '</tr></thead><tbody>'
    for r in b['rows']:
        h += '<tr>'
        for i, c in enumerate(r):
            cls = ' class="jp-cell"' if i in b['jp'] else (' class="ro-cell"' if i in b['ro'] else '')
            h += f'<td{cls}>{E(c)}</td>'
        h += '</tr>'
    return h + '</tbody></table></div>'

def blocks(bs):
    out = ''
    for b in bs:
        if b['t'] == 'table': out += table(b)
        elif b['t'] == 'p': out += f'<p class="conj-intro">{E(b["text"])}</p>'
        elif b['t'] == 'note': out += f'<p class="conj-note">{E(b["text"])}</p>'
        elif b['t'] == 'h': out += f'<div class="section-title">{E(b["text"])}</div>'
    return out

def section(sec):
    h = f'<details class="sec" name="sec"><summary><span class="jp">{E(sec["jp"])}</span><span class="lbl">{E(sec["label"])}</span></summary><div class="sec-body"><p class="conj-intro">{E(sec["intro"])}</p>'
    for sub in sec['subs']:
        h += f'<details class="sub" name="sub-{sec["id"]}"><summary>{E(sub["title"])}</summary><div class="sub-body">{blocks(sub["blocks"])}</div></details>'
    return h + '</div></details>'

src = open(os.path.join(HERE, 'base', 'japonais-nojs.html'), encoding='utf-8').read()
i = src.index('<main>')
head, main = src[:i], src[i:]
soup = BeautifulSoup(main, 'html.parser')
secs = soup.select('main > details.sec')
last = secs[-1]
for sec in SECTIONS:
    frag = BeautifulSoup(section(sec), 'html.parser')
    node = frag.find('details')
    if sec['replace']:
        old = [d for d in secs if sec['replace'] in d.summary.get_text()][0]
        old.replace_with(node)
    elif sec.get('after'):
        anchor = [d for d in secs if sec['after'] in d.summary.get_text()][0]
        anchor.insert_after(node)
    else:
        last.insert_after(node); last = node
from content import EXTRA_SUBS
for key, subs in EXTRA_SUBS.items():
    target = [d for d in soup.select('main > details.sec') if d.summary.get_text().strip().startswith(key)][0]
    body = target.select_one(':scope > .sec-body')
    name = target.select_one('details.sub')['name']
    for sub in subs:
        fr = BeautifulSoup(f'<details class="sub" name="{name}"><summary>{E(sub["title"])}</summary><div class="sub-body">{blocks(sub["blocks"])}</div></details>', 'html.parser')
        body.append(fr.find('details'))
css_add = '''
  .jp-cell { font-family: 'Noto Serif JP', serif; font-size: 1.05em; color: var(--red); min-width: 9rem; }
  .ro-cell { color: var(--muted); font-size: .8em; min-width: 8rem; }
  .aid-hide .ro-cell { filter: blur(6px); cursor: pointer; }
  .aid-hide .ro-cell.rv { filter: none; }
'''
head = head.replace('</style>', css_add + '</style>', 1)
open(os.path.join(BUILD, 'nojs-plus.html'), 'w', encoding='utf-8').write(head + str(soup))
print('ok', len(SECTIONS))
