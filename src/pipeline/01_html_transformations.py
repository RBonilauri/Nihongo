# Transformations du HTML de base : furigana/romaji, empilement, conjugaison inline
# Exécuté par build.py dans un espace de noms partagé (variables main, css, js…).
from bs4 import BeautifulSoup as _BS
def unsplit_tables(html):
    """Tableaux en deux blocs côte à côte (8 colonnes : heures, mois, jours du mois) → 4 colonnes
    empilées : plus de défilement horizontal sur téléphone."""
    soup = _BS(html, 'html.parser')
    for t in soup.select('table'):
        hs = t.select('thead th')
        h = [x.get_text(strip=True) for x in hs]
        if len(h) != 8 or h[:4] != h[4:]: continue
        for x in hs[4:]: x.extract()
        body = t.find('tbody')
        rows = body.find_all('tr'); lefts, rights, notes = [], [], []
        for tr in rows:
            c = tr.find_all('td', recursive=False)
            if len(c) == 8:
                lefts.append(c[:4])
                if any(x.get_text(strip=True) for x in c[4:]): rights.append(c[4:])
            elif len(c) == 5 and c[4].get('colspan'):
                lefts.append(c[:4]); notes.append(c[4])
            else: lefts.append(c)
        for tr in rows: tr.extract()
        for cells in lefts + rights:
            tr = soup.new_tag('tr')
            for x in cells: tr.append(x.extract())
            body.append(tr)
        for x in notes:
            tr = soup.new_tag('tr'); x['colspan'] = '4'; tr.append(x.extract()); body.append(tr)
    return str(soup)
main = unsplit_tables(main)
def stackify(html):
    soup = _BS(html, 'html.parser')
    n = 0
    for t in soup.select('table'):
        heads = [h.get_text(' ', strip=True) for h in t.select('thead th')]
        if not (4 <= len(heads) <= 5 or heads == ['日本語', 'Sens', 'Pourquoi']): continue
        if not heads[0] or heads[0].isdigit() or heads[0] == 'Base': continue
        t['class'] = (t.get('class') or []) + ['stack'] + (['stack-kanji'] if heads[0] == 'Kanji' and len(heads) >= 4 else [])
        for tr in t.select('tbody tr'):
            for i, td in enumerate(tr.find_all('td', recursive=False)):
                if i < len(heads): td['data-label'] = heads[i]
        n += 1
    print('stacked tables', n)
    return str(soup)

import pykakasi as _pk, re as _re
_kks = _pk.kakasi()
_KANA = _re.compile(r'[぀-ヿー]+')
def add_romaji(html):
    soup = _BS(html, 'html.parser'); n = 0
    for t in soup.select('table'):
        heads = ' '.join(h.get_text(' ', strip=True) for h in t.select('thead th')).lower()
        if 'romaji' in heads or 'rōmaji' in heads: continue
        for tr in t.select('tbody tr'):
            runs = _KANA.findall(tr.get_text(' ', strip=True))
            if not runs: continue
            seen = []; 
            for r in runs:
                ro = ''.join(x['hepburn'] for x in _kks.convert(r))
                if ro and ro not in seen: seen.append(ro)
            if not seen: continue
            v = ' '.join(seen)
            short = _re.sub(r'ou', 'o', _re.sub(r'oo', 'o', _re.sub(r'uu', 'u', v)))
            tr['data-ro'] = v if short == v else v + ' ' + short
            n += 1
    print('rows with romaji', n)
    return str(soup)
main = stackify(main)
import json as _json, verbes_exemples as _vx
_EX = _vx.frames()
nex = [0]
def conjify(html):
    soup = _BS(html, 'html.parser'); n = 0
    for t in soup.select('table'):
        heads = [h.get_text(' ', strip=True) for h in t.select('thead th')]
        if len(heads) != 5 or not heads[4].startswith('Groupe'): continue
        for tr in t.select('tbody tr'):
            td = tr.find_all('td', recursive=False)
            if len(td) < 5: continue
            k, ka, txt = td[0].get_text(strip=True), td[1].get_text(strip=True), td[4].get_text(' ', strip=True)
            g = txt.split('·')[0].strip()
            ty = 'suru' if g.startswith('する') else 'irr' if g.startswith('Irr') else 'ru' if g.startswith('G2') else 'u'
            cls = td[4].get('class')
            td[4].clear()
            d = soup.new_tag('details', attrs={'class': 'cjd', 'data-k': k, 'data-ka': ka, 'data-t': ty, 'data-fr': td[3].get_text(' ', strip=True)})
            sm = soup.new_tag('summary')
            parts = [x.strip() for x in txt.split('·')]
            i1 = soup.new_tag('span', attrs={'class': 'cj-info'})
            gs = soup.new_tag('b', attrs={'class': 'cj-g'}); gs.string = parts[0]; i1.append(gs)
            for x in parts[1:]:
                sp = soup.new_tag('span'); sp.string = x; i1.append(sp)
            bt = soup.new_tag('span', attrs={'class': 'cj-btn'}); bt.string = 'Conjuguer'
            sm.append(i1); sm.append(bt)
            d.append(sm); d.append(soup.new_tag('div', attrs={'class': 'cjb'}))
            td[4].append(d); n += 1
            fr_ = _EX.get(k)
            if fr_:
                pk = ''.join(x['hira'] for x in _kks.convert(fr_['p'])) if fr_['p'] else ''
                ex = soup.new_tag('details', attrs={'class': 'exd', 'data-k': k, 'data-ka': ka, 'data-t': ty, 'data-ex': _json.dumps([fr_['p'], pk, fr_['v'], fr_['c'], fr_['s'], fr_['n'], fr_['o']], ensure_ascii=False, separators=(',', ':'))})
                sm2 = soup.new_tag('summary'); lb = soup.new_tag('span', attrs={'class': 'ex-l'}); lb.string = 'Phrases d’exemple'; bt2 = soup.new_tag('span', attrs={'class': 'cj-btn'}); bt2.string = 'Exemple'
                sm2.append(lb); sm2.append(bt2); ex.append(sm2); ex.append(soup.new_tag('div', attrs={'class': 'exb'}))
                td[4].append(ex); nex[0] += 1
    print('conjugaisons', n, 'exemples', nex[0])
    return str(soup)
main = _re.sub(r'<p class="conj-intro">\[\[JPMAP\]\]</p>', '<div class="jpmap-host"></div>', main)
main = conjify(main)
def foldify(html):
    """Verbes courants : chaque thème (Vie quotidienne, Déplacements…) devient un bloc repliable."""
    soup = _BS(html, 'html.parser'); n = 0
    sub = [d for d in soup.select('details.sub') if d.summary.get_text().startswith('動詞 — Verbes courants')]
    if not sub: return html
    body = sub[0].select_one('.sub-body')
    for h in list(body.select(':scope > .section-title')):
        grp = soup.new_tag('details', attrs={'class': 'vgrp'})
        sm = soup.new_tag('summary'); t = soup.new_tag('span', attrs={'class': 'vg-t'}); t.string = h.get_text(' ', strip=True); sm.append(t)
        grp.append(sm)
        nxt = h.find_next_sibling(); moved = []
        while nxt is not None and 'section-title' not in (nxt.get('class') or []):
            moved.append(nxt); nxt = nxt.find_next_sibling()
        h.insert_before(grp); h.extract()
        for m in moved: grp.append(m.extract())
        cnt = len(grp.select('details.cjd'))
        c = soup.new_tag('span', attrs={'class': 'vg-n'}); c.string = str(cnt) + ' verbes'; sm.append(c); n += 1
    print('thèmes repliables', n)
    return str(soup)
main = foldify(main)

