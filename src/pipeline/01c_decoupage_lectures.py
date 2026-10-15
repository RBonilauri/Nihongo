# Découpage de la lecture d'un mot par kanji (ex. 満室 / まんしつ → まん|しつ), pour l'ampoule 💡 des quiz.
# Table des lectures : src/data/kanji_lectures.json (KANJIDIC2, hiragana ; « stem.okurigana » pour les kun).
# Exécuté par build.py avant 02_kanji.py (même espace de noms). Un mot dont la lecture ne s'aligne pas
# sur des lectures connues (jukujikun : 今日, 大人…) n'a pas de découpage → pas d'ampoule.
import json as _j2, os as _o2
_LECT = _j2.load(open(_o2.path.join(HERE, 'data', 'kanji_lectures.json'), encoding='utf-8'))
_EXTRA = {'日': ['に', 'び'], '時': ['と'], '計': ['け'], '人': ['り', 'ん'], '本': ['ぽん'], '上': ['うわ', 'じょう'], '下': ['した'], '何': ['なん', 'なに'], '大': ['おお', 'おと'], '手': ['て'],
          '気': ['け'], '屋': ['や'], '母': ['かあ'], '父': ['とう'], '兄': ['にい'], '姉': ['ねえ'], '真': ['ま'], '生': ['お'], '木': ['こ'], '子': ['こ'], '小': ['こ', 'お'], '川': ['がわ'], '一': ['ひと'], '二': ['ふた']}
_RENDAKU = dict(zip('かきくけこさしすせそたちつてとはひふへほ', 'がぎぐげござじずぜぞだぢづでどばびぶべぼ'))
_HANDAKU = dict(zip('はひふへほ', 'ぱぴぷぺぽ'))
_RENYO = dict(zip('るくぐすつぬぶむう', 'りきぎしちにびみい'))
_KANJI_RE = _re.compile(r'[一-鿿々]')
def _expand(r):
    """une lecture KANJIDIC → formes utilisables dans un mot : « わ.る » → わ, わり, わる…"""
    if '.' not in r: return [r]
    st, ok = r.split('.', 1); out = [st, st + ok]
    if ok: out += [st + ok[:-1], st + ok[:-1] + _RENYO.get(ok[-1], '')]
    return [x for x in out if x]
def _variants(r):
    out = {r: 0}
    if r[0] in _RENDAKU: out.setdefault(_RENDAKU[r[0]] + r[1:], 1)
    if r[0] in _HANDAKU: out.setdefault(_HANDAKU[r[0]] + r[1:], 1)
    if len(r) > 1 and r[-1] in 'つくちき':
        for v, c in list(out.items()): out.setdefault(v[:-1] + 'っ', c + 1)
    return out
_RCACHE = {}
def _readings_of(c):
    if c not in _RCACHE:
        d = {}
        for tok in _LECT.get(c, '').split():
            for f in _expand(tok): d.setdefault(f, 0)
        for f in _EXTRA.get(c, []): d.setdefault(f, 2)
        _RCACHE[c] = d
    return _RCACHE[c]
def _align(word, rd):
    """liste des lectures, une par kanji du mot (dans l'ordre), ou None si l'alignement échoue."""
    n, m = len(word), len(rd); INF = 10 ** 6; memo = {}
    def go(i, j):
        if (i, j) in memo: return memo[(i, j)]
        if i == n: res = (0, ()) if j == m else (INF, ())
        else:
            c = word[i]
            if not _KANJI_RE.match(c):
                h = _kata2hira(c); res = (INF, ())
                if j < m and (rd[j] == h or (c == 'ー' and rd[j] in 'あいうえおー')):
                    r = go(i + 1, j + 1); res = r if r[0] >= INF else (r[0], r[1])
            else:
                best = (INF, ()); cands = _readings_of(word[i - 1] if c == '々' and i else c)
                if not cands: cands = {}
                for base, bc in cands.items():
                    for v, cost in _variants(base).items():
                        if rd.startswith(v, j):
                            r = go(i + 1, j + len(v))
                            if r[0] < INF and r[0] + cost + bc < best[0]: best = (r[0] + cost + bc, (v,) + r[1])
                res = best
        memo[(i, j)] = res; return res
    cost, segs = go(0, 0)
    return list(segs) if cost < INF else None
def _seg(word, rd):
    """chaîne « seg|seg » (un segment par kanji), '' si impossible."""
    if not rd or not _KANJI_RE.search(word): return ''
    a = _align(word, rd)
    return '|'.join(a) if a else ''
