# Données JSON du vocabulaire
# Exécuté par build.py dans un espace de noms partagé (variables main, css, js…).
import hashlib as _hl
_CAT = {'旅行': 'Voyage', '会話': 'Conversation', '敬語': 'Keigo', '語彙': 'Vocabulaire', '常用': 'Vocabulaire', '時間': 'Temps', '形容詞': 'Adjectifs', '道具': 'Outils', '表現': 'Expressions', '助詞': 'Particules'}
def vocab_json(html):
    soup = _BS(html, 'html.parser'); out = []; seen = set()
    def add(cat, g, fr, jp, ka, ro):
        fr = _re.sub(r'\s+', ' ', fr).strip(); jp = _re.sub(r'\s+', ' ', jp).strip()
        if not fr or not jp or len(jp) > 45 or len(fr) > 70 or (fr, jp) in seen: return
        if jp.startswith('〜') or fr.startswith('-'): return
        seen.add((fr, jp))
        out.append({'i': _hl.md5((fr + '|' + jp).encode()).hexdigest()[:6], 'c': cat, 'g': g, 'fr': fr, 'jp': jp, 'ka': ka if ka and ka != jp else '', 'kk': (ka if ka and ka != jp else (_kana(jp) if _HASK.search(jp) else '')), 'ro': ro or ''})
    for sec in soup.select('details.sec'):
        head = sec.summary.get_text(' ', strip=True).split()[0]
        cat = _CAT.get(head)
        if not cat: continue
        for d in sec.select('details.sub'):
            cat = _CAT.get(head)
            g = cat + ':' + d.summary.get_text(' ', strip=True).split()[0]
            isv = (cat == 'Vocabulaire' and g.endswith(':動詞'))
            for tb in d.select('table'):
                if isv:
                    hh = tb.find_previous('div', class_='section-title'); cat, g = 'Verbes', 'Verbes:' + (hh.get_text(strip=True) if hh else 'Divers')
                else: cat = _CAT.get(head)
                hd = [th.get_text(strip=True) for th in tb.select('thead th')]
                rows = [[td.get_text(' ', strip=True) for td in tr.find_all(['td', 'th'], recursive=False)] for tr in tb.select('tbody tr')]
                if len(hd) >= 3 and hd[1] in ('日本語', 'Japonais') and hd[2].lower().startswith(('rōmaji', 'romaji')):
                    for c in rows:
                        if len(c) >= 3: add(cat, g, c[3] if hd[0] == 'Structure' and len(c) > 3 else c[0], c[1], '', c[2])
                elif len(hd) >= 4 and hd[1] in ('Kanji', '日本語') and hd[2] == 'Kana' and hd[3].lower().startswith(('romaji', 'rōmaji')):
                    for c in rows:
                        for o in range(0, len(c) - 3, 4):
                            if hd[o + 1:o + 2] in (['Kanji'], ['日本語']): add(cat, g, c[o], c[o + 1], c[o + 2], c[o + 3])
                elif hd[:2] == ['日本語', 'Sens'] and cat in ('Particules', 'Expressions'):
                    for c in rows:
                        if len(c) >= 2 and not _re.search(r'[A-Za-z]{4,}', c[0]): add(cat, g, c[1], c[0], '', '')
                elif hd[:2] == ['Kanji', 'Kana'] and len(hd) >= 4 and hd[3] == 'Sens':
                    for c in rows:
                        if len(c) >= 4: add(cat, g, c[3], c[0], c[1], c[2])
    cats = {}
    for x in out: cats[x['c']] = cats.get(x['c'], 0) + 1
    print('vocab', len(out), cats)
    return _json.dumps(out, ensure_ascii=False, separators=(',', ':'))
_VJ = vocab_json(main)

