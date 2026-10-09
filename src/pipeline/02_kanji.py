# Lectures (Sudachi) et données JSON des kanji
# Exécuté par build.py dans un espace de noms partagé (variables main, css, js…).
import json as _json
from sudachipy import dictionary as _sd, tokenizer as _st
_tk = _sd.Dictionary().create(); _mode = _st.Tokenizer.SplitMode.C
def _kata2hira(t): return ''.join(chr(ord(c) - 0x60) if 'ァ' <= c <= 'ヶ' else c for c in t)
_OVR = {'四月':'しがつ','七月':'しちがつ','九月':'くがつ','三百':'さんびゃく','日本':'にほん','日本海':'にほんかい','明日':'あした','山道':'やまみち','富士山':'ふじさん','一目':'ひとめ','言う':'いう','何時':'なんじ','何曜日':'なんようび','何か':'なにか','一回':'いっかい','川沿い':'かわぞい','何人':'なんにん','何枚':'なんまい'}
_OVR.update({'俺ん家':'おれんち','一兆': 'いっちょう', '一冊': 'いっさつ', '一匹': 'いっぴき', '一周': 'いっしゅう', '一拍': 'いっぱく', '一晩': 'ひとばん', '一杯': 'いっぱい', '一歳': 'いっさい', '一泊': 'いっぱく', '一等': 'いっとう', '一羽': 'いちわ', '一軒': 'いっけん', '一週間': 'いっしゅうかん', '一階': 'いっかい', '二日酔い': 'ふつかよい', '勉強机': 'べんきょうづくえ', '十歳': 'じゅっさい', '四角形': 'しかくけい', '四畳半': 'よじょうはん', '塵取り': 'ちりとり', '搭乗口': 'とうじょうぐち', '故里': 'ふるさと', '昔風': 'むかしふう', '栃の実': 'とちのみ', '榎茸': 'えのきたけ', '水道管': 'すいどうかん', '水餃子': 'すいぎょうざ', '登山口': 'とざんぐち', '第一章': 'だいいっしょう', '紅生姜': 'べにしょうが', '綺麗好き': 'きれいずき', '綿菓子': 'わたがし', '羊肉': 'ようにく', '芋焼酎': 'いもじょうちゅう', '茨の道': 'いばらのみち', '蛙跳び': 'かえるとび', '貿易会社': 'ぼうえきがいしゃ', '足踏み': 'あしぶみ', '込む': 'こむ', '運動靴': 'うんどうぐつ', '門扉': 'もんぴ', '高原': 'こうげん', '高峰': 'こうほう', '鶏小屋': 'にわとりごや', '三匹': 'さんびき', '三千円': 'さんぜんえん', '三時頃': 'さんじごろ', '八千円': 'はっせんえん', '八歳': 'はっさい', '八百円': 'はっぴゃくえん', '六百円': 'ろっぴゃくえん', '九千八百円': 'きゅうせんはっぴゃくえん', '日暮れ頃': 'ひぐれごろ'})
_OVR.update(_RDG)
_SKIP = {'お正月節'}
def _reading(w):
    if w in _OVR: return _OVR[w]
    return _kata2hira(''.join(x.reading_form() for x in _tk.tokenize(w, _mode)))
_HASK = _re.compile(r'[一-鿿々]')
_JPRUN = _re.compile(r'[぀-ヿ㐀-鿿ー々]+|[^぀-ヿ㐀-鿿ー々]+')
def _kana(t):
    if t in _OVR: return _OVR[t]
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
        lvl = 'N5' if t.startswith('N5') else 'N4' if t.startswith('N4') else 'N3' if t.startswith('N3') else 'N2' if t.startswith('N2') else 'N1' if t.startswith('N1') else None
        if not lvl or 'Liste' not in t: continue
        for gi, tb in enumerate(d.select('table.stack-kanji')):
            for tr in tb.select('tbody tr'):
                c = [td.get_text(' ', strip=True) for td in tr.find_all('td', recursive=False)]
                if len(c) < 4 or not c[0]: continue
                kw = []
                for mm in _re.finditer(r'([^\s,、()（）]+)\s*[（(]([^)）]*)[)）]', (c[4] if len(c) > 4 else '').replace(' ＋ ', ', ')):
                    w, g = mm.group(1), mm.group(2)
                    if len(w) < 2 or w in _SKIP: continue
                    kw.append([w, _reading(w), g])
                clean = lambda x: None if x in ('', '—', '-', '–') else x
                data.append({'k': c[0], 'l': lvl, 'g': lvl + str(gi), 'on': clean(c[1]), 'kun': clean(c[2]), 's': c[3], 'kw': kw})
    print('kanji', len(data), 'words', sum(len(x['kw']) for x in data))
    return _json.dumps(data, ensure_ascii=False, separators=(',', ':'))
_KJ = kanji_json(main)

