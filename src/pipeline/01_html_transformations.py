# Transformations du HTML de base : furigana/romaji, empilement, conjugaison inline
# Exécuté par build.py dans un espace de noms partagé (variables main, css, js…).
from bs4 import BeautifulSoup as _BS
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
            d = soup.new_tag('details', attrs={'class': 'cjd', 'data-k': k, 'data-ka': ka, 'data-t': ty})
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
    print('conjugaisons', n)
    return str(soup)
main = _re.sub(r'<p class="conj-intro">\[\[JPMAP\]\]</p>', '<div class="jpmap-host"></div>', main)
main = conjify(main)

