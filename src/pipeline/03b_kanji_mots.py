# Mots clés des listes de kanji (après le vocabulaire)
import json as _json
# Mots clés : lecture (ruby) au-dessus de chaque mot, et « ＋ » pour afficher les mots supplémentaires
import html as _hh
_WRE = _re.compile(r'([^\s,、()（）]+)\s*[（(]([^)）]*)[)）]')
def _kwcell(txt):
    base, _, more = _hh.unescape(txt).partition(' ＋ ')
    def one(m):
        w, g = m.group(1), m.group(2)
        rd = _reading(w) if _HASK.search(w) else ''
        wh = ('<ruby>' + _hh.escape(w) + '<rt>' + _hh.escape(rd) + '</rt></ruby>') if rd and rd != w else _hh.escape(w)
        return '<span class="kw">' + wh + ' <small>(' + _hh.escape(g) + ')</small></span>'
    out = ' '.join(one(m) for m in _WRE.finditer(base))
    if more.strip():
        out += ' <details class="kmore"><summary title="Plus d’exemples" aria-label="Plus d’exemples"></summary>' + ' '.join(one(m) for m in _WRE.finditer(more)) + '</details>'
    return '<div class="kws">' + out + '</div>'
# lectures du vocabulaire (plus fiables : 一日 = ついたち, 七日 = なのか…) prioritaires sur Sudachi
_vk = {}
for _x in _vall:
    if _x.get('kk') and _x['jp'] not in _vk: _vk[_x['jp']] = _x['kk'].split('・')[0]
_kd = _json.loads(_KJ)
for _k in _kd:
    for _w in _k['kw']:
        if _w[0] in _vk: _w[1] = _vk[_w[0]]
_KJ = _json.dumps(_kd, ensure_ascii=False, separators=(',', ':'))
_reading0 = _reading
def _reading(w): return _vk.get(w) or _reading0(w)
main = _re.sub(r'(<td data-label="Mots clés">)(.*?)(</td>)', lambda m: m.group(1) + _kwcell(m.group(2)) + m.group(3), main)

