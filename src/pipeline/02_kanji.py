# Lectures (Sudachi) et données JSON des kanji
# Exécuté par build.py dans un espace de noms partagé (variables main, css, js…).
import json as _json
from sudachipy import dictionary as _sd, tokenizer as _st
_tk = _sd.Dictionary().create(); _mode = _st.Tokenizer.SplitMode.C
def _kata2hira(t): return ''.join(chr(ord(c) - 0x60) if 'ァ' <= c <= 'ヶ' else c for c in t)
_OVR = {'四月':'しがつ','七月':'しちがつ','九月':'くがつ','三百':'さんびゃく','日本':'にほん','日本海':'にほんかい','明日':'あした','山道':'やまみち','富士山':'ふじさん','一目':'ひとめ','言う':'いう','何時':'なんじ','何曜日':'なんようび','何か':'なにか','一回':'いっかい','川沿い':'かわぞい','何人':'なんにん','何枚':'なんまい'}
_SKIP = {'お正月節'}
def _reading(w):
    if w in _OVR: return _OVR[w]
    return _kata2hira(''.join(x.reading_form() for x in _tk.tokenize(w, _mode)))
_HASK = _re.compile(r'[一-鿿々]')
_JPRUN = _re.compile(r'[぀-ヿ㐀-鿿ー々]+|[^぀-ヿ㐀-鿿ー々]+')
def _kana(t):
    out = []
    for m in _JPRUN.finditer(t):
        seg = m.group()
        if not _HASK.search(seg): out.append(seg); continue
        for tok in _tk.tokenize(seg, _st.Tokenizer.SplitMode.A):
            sf = tok.surface()
            if sf in _OVR: out.append(_OVR[sf])
            elif _HASK.search(sf):
                r = _kata2hira(tok.reading_form()); out.append(r if r and r != 'キゴウ' else sf)
            else: out.append(sf)
    r = ''.join(out)
    for x, y in (('ななじ', 'しちじ'), ('ぶかい', 'ふかい'), ('きゅうじ', 'くじ'), ('よんじ', 'よじ'), ('よんがつ', 'しがつ'), ('わたくし', 'わたし'), ('つらくない', 'からくない'), ('なんが', 'なにが'), ('なんを', 'なにを'), ('いちはく', 'いっぱく'), ('いれますか', 'はいれますか')): r = r.replace(x, y)
    return r
def kanji_json(html):
    soup = _BS(html, 'html.parser'); data = []; wordcache = {}
    for d in soup.select('details.sub'):
        t = d.summary.get_text(' ', strip=True)
        lvl = 'N5' if t.startswith('N5') else 'N4' if t.startswith('N4') else 'N3' if t.startswith('N3') else 'N2' if t.startswith('N2') else None
        if not lvl or 'Liste' not in t: continue
        for gi, tb in enumerate(d.select('table.stack-kanji')):
            for tr in tb.select('tbody tr'):
                c = [td.get_text(' ', strip=True) for td in tr.find_all('td', recursive=False)]
                if len(c) < 4 or not c[0]: continue
                kw = []
                for mm in _re.finditer(r'([^\s,、()（）]+)\s*[（(]([^)）]*)[)）]', c[4] if len(c) > 4 else ''):
                    w, g = mm.group(1), mm.group(2)
                    if len(w) < 2 or w in _SKIP: continue
                    kw.append([w, _reading(w), g])
                clean = lambda x: None if x in ('', '—', '-', '–') else x
                data.append({'k': c[0], 'l': lvl, 'g': lvl + str(gi), 'on': clean(c[1]), 'kun': clean(c[2]), 's': c[3], 'kw': kw})
    print('kanji', len(data), 'words', sum(len(x['kw']) for x in data))
    return _json.dumps(data, ensure_ascii=False, separators=(',', ':'))
_KJ = kanji_json(main)

