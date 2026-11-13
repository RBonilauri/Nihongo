# Traits (n), rang de fréquence (q, absent si hors des 2 500 plus fréquents), numéro (r) et glyphe (rg) du radical classique, pour les modes d'affichage des listes de kanji.
_kd = _json.loads(_KJ)
_tr = _json.load(open(os.path.join(HERE, 'data', 'kanji_traits.json'), encoding='utf-8'))
_rl = [x['g'] for x in _json.load(open(os.path.join(HERE, 'data', 'radicaux.json'), encoding='utf-8')) if not x.get('p')][:214]
for _e in _kd:
    _t = _tr.get(_e['k'])
    if _t:
        _e['n'] = _t[0]
        if _t[1]: _e['q'] = _t[1]
        if _t[2]: _e['r'] = _t[2]; _e['rg'] = _rl[_t[2] - 1]
_KJ = _json.dumps(_kd, ensure_ascii=False, separators=(',', ':'))
