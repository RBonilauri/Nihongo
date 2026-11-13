# Phrases d'exemple : ajoute la phrase en kana (3e élément) à chaque exemple contenant des kanji.
# Exécuté par build.py dans un espace de noms partagé ; après les données JSON (_KJ, _VJ, _CJ), avant l'assemblage.
_YU = {1: 'ついたち', 2: 'ふつか', 3: 'みっか', 4: 'よっか', 5: 'いつか', 6: 'むいか', 7: 'なのか', 8: 'ようか', 9: 'ここのか', 10: 'とおか', 14: 'じゅうよっか', 20: 'はつか', 24: 'にじゅうよっか'}
_UN = ['', 'いち', 'に', 'さん', 'よん', 'ご', 'ろく', 'なな', 'はち', 'きゅう']
def _jour(n):
    if n in _YU: return _YU[n]
    if n in (17, 27): return ('じゅう' if n < 20 else 'にじゅう') + 'しちにち'
    if n in (19, 29): return ('じゅう' if n < 20 else 'にじゅう') + 'くにち'
    if n < 20: return 'じゅう' + _UN[n - 10] + 'にち'
    if n < 30: return 'にじゅう' + _UN[n - 20] + 'にち'
    return 'さんじゅう' + ('' if n == 30 else _UN[n - 30]) + 'にち'
_KN = '〇一二三四五六七八九'
def _knum(n):
    n = int(n)
    if n < 10: return _KN[n]
    if n < 20: return '十' + (_KN[n - 10] if n > 10 else '')
    if n < 100: return _KN[n // 10] + '十' + (_KN[n % 10] if n % 10 else '')
    return ''.join(_KN[int(c)] for c in str(n))
_kd = _json.loads(_KJ); _vd = _json.loads(_VJ); _cd = _json.loads(_CJ)
# Lectures de référence de l'appli (mot → lecture), sans ambiguïté : elles priment sur l'analyseur (qui se trompe sur nombres + compteurs : いちぽん, ろくひゃく, よんか…)
_MAN = {'三十日': 'さんじゅうにち', '三十一日': 'さんじゅういちにち', '二十日': 'はつか', '十日': 'とおか', '一日': 'いちにち', '二十歳': 'はたち', '七五三': 'しちごさん', '何日': 'なんにち'}
_GOLD = {}; _CONF = set()
def _addgold(w, r):
    r = (r or '').strip()
    if len(w) < 2 or not _HASK.search(w) or not r or _re.search('[・/、,（(]', r): return
    if w in _GOLD and _GOLD[w] != r: _CONF.add(w)      # deux lectures différentes selon les listes : ambigu, on laisse l'analyseur trancher
    _GOLD[w] = r
for _r in _cd.get('reads', []): _addgold(_r['k'], _r['y'].replace('!', ''))
for _e in _kd:
    for _w in _e.get('kw', []): _addgold(_w[0], _w[1])
for _x in _vd:
    if _x.get('jp') and _x.get('ka'): _addgold(_x['jp'], _x['ka'])
for _w in _CONF: _GOLD.pop(_w, None)
_GOLD.update(_MAN)
_GMAX = max(len(k) for k in _GOLD)
def _kana_g(t, own=None):
    """kana d'une phrase : lectures de référence d'abord (plus long d'abord), analyseur Sudachi pour le reste"""
    if own and own[0] in t:        # le mot illustré par la phrase garde sa lecture de la liste, même si une expression plus longue le contient
        i = t.index(own[0])
        return _kana_g(t[:i]) + own[1] + _kana_g(t[i + len(own[0]):], own if own[0] in t[i + len(own[0]):] else None)
    out = []; i = 0; buf = ''
    def flush():
        nonlocal buf
        if buf: out.append(_kana(buf)); buf = ''
    while i < len(t):
        for n in range(min(_GMAX, len(t) - i), 0, -1):
            seg = t[i:i + n]
            r = _GOLD.get(seg) if n > 1 else None
            if r: flush(); out.append(r); i += n; break
        else:
            buf += t[i]; i += 1
    flush()
    return ''.join(out)
_ISO = {'米': 'こめ', '箱': 'はこ'}      # mot isolé : l'analyseur donne べい / ばこ
def _own_stem(w, r):
    """verbe ou adjectif conjugué dans la phrase : (partie en kanji, sa lecture) si le mot finit par des kana repris à l'identique dans la lecture"""
    m = _re.match(r'^([一-鿿々]+)([぀-ゟ]+)$', w)
    if m and r.endswith(m.group(2)) and len(r) > len(m.group(2)): return (m.group(1), r[:-len(m.group(2))])
    return None
_SOV = _json.load(open(os.path.join(HERE, 'data', 'phrases_kana_corrections.json'), encoding='utf-8'))   # corrections manuelles {phrase: kana}
def _sk(jp, own=None):
    """phrase en hiragana ('' si la phrase n'a pas de kanji ou si la conversion n'apporte rien)"""
    if not _HASK.search(jp): return ''
    if jp in _SOV: return _SOV[jp]
    t = _re.sub(r'(\d{1,2})日', lambda m: _jour(int(m.group(1))), jp)      # jours du mois : lecture de calendrier
    t = _re.sub(r'\d+', lambda m: _knum(m.group()), t)
    t = _re.sub(r'(?<=[日年秒])間', 'かん', t)                      # 三日間, 五年間 : かん (et non ま)
    t = _re.sub(r'(?<=[日年月分秒歳])後', 'ご', t)                # 二日後, 三年後 : ご (et non あと)
    t = _re.sub(r'(?<=[日年月])前', 'まえ', t)
    if own and own[0] not in t and _own_stem(*own): own = _own_stem(*own)
    t = _re.sub('(?<![一-鿿々])米(?![一-鿿々])|(?:(?<=[のをはがにでもといおその、。])|^)箱(?![一-鿿々])', lambda m: '\1' + _ISO[m.group()] + '\1', t)
    k = _kana_g(t, own).replace('\1', '')
    return k if k and k != jp and not _HASK.search(k) else ''
for _e in _kd:
    for _w in _e.get('kw', []):
        if len(_w) > 4 and _w[4] and len(_w[4]) == 2:
            _o = (_w[0], _w[1].split('・')[0].strip()) if _w[0] in _w[4][0] else None
            _w[4] = [_w[4][0], _w[4][1], _sk(_w[4][0], _o)]
_KJ = _json.dumps(_kd, ensure_ascii=False, separators=(',', ':'))
for _x in _vd:
    if _x.get('ex') and len(_x['ex']) == 2:
        _o = (_x['jp'], _x['ka'].split('・')[0].strip()) if _x.get('ka') and _x['jp'] in _x['ex'][0] else None
        _x['ex'] = [_x['ex'][0], _x['ex'][1], _sk(_x['ex'][0], _o)]
_VJ = _json.dumps(_vd, ensure_ascii=False, separators=(',', ':'))
_RY = {'r:' + _r['k']: (_r['k'], _r['y'].replace('!', '')) for _r in _cd.get('reads', [])}
for _k, _l in _cd.get('exs', {}).items():
    _cd['exs'][_k] = [[e[0], e[1], _sk(e[0], _RY.get(_k))] for e in _l]
_CJ = _json.dumps(_cd, ensure_ascii=False, separators=(',', ':'))
print('phrases en kana : kanji', sum(1 for e in _kd for w in e.get('kw', []) if len(w) > 4 and w[4] and len(w[4]) > 2 and w[4][2]), '· vocabulaire', sum(1 for x in _vd if x.get('ex') and len(x['ex']) > 2 and x['ex'][2]), '· compteurs', sum(1 for l in _cd.get('exs', {}).values() for e in l if e[2]))
