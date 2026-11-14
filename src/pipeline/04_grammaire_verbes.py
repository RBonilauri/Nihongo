# Verbes, formes conjuguées, JSON grammaire
# Exécuté par build.py dans un espace de noms partagé (variables main, css, js…).
_VERBS = {
 '食べる': ('たべる', 'manger', 'groupe 2'), '書く': ('かく', 'écrire', 'groupe 1'), 'する': ('する', 'faire', 'irrégulier'),
 '来る': ('くる', 'venir', 'irrégulier'), '行く': ('いく', 'aller', 'groupe 1 (て/た irrégulier)'), 'ある': ('ある', 'il y a (choses)', 'irrégulier'),
 '買う': ('かう', 'acheter', 'groupe 1'), '泳ぐ': ('およぐ', 'nager', 'groupe 1'), '話す': ('はなす', 'parler', 'groupe 1'), '待つ': ('まつ', 'attendre', 'groupe 1'),
 '死ぬ': ('しぬ', 'mourir', 'groupe 1'), '遊ぶ': ('あそぶ', 'jouer', 'groupe 1'), '飲む': ('のむ', 'boire', 'groupe 1'), '帰る': ('かえる', 'rentrer', 'groupe 1 (en る)'),
}
_G1MAP = {'Négatif': 'Négatif simple', 'Poli': 'Polie, présent', 'Potentiel': 'Potentiel', 'Volitif': 'Volitif', 'Impératif': 'Impératif'}
def _regru(v):  # verbe du groupe 1 en る : formes régulières
    s = v[:-1]
    return {'Négatif simple': s + 'らない', 'Polie, présent': s + 'ります', 'Forme en て': s + 'って', 'Passé simple': s + 'った', 'Volitif': s + 'ろう'}
def grammar_json(html):
    soup = _BS(html, 'html.parser'); verbs = {}
    def getv(v, fr=None, g=None, ka=None):
        if v not in verbs:
            info = _VERBS.get(v)
            verbs[v] = {'v': v, 'ka': (info[0] if info else ka), 'fr': (info[1] if info else fr), 'g': (info[2] if info else g), 'f': {}}
        return verbs[v]
    strip = lambda t: _re.sub(r'\s*[(（][^)）]*[)）]', '', t).strip()
    for d in soup.select('details.sub'):
        t = d.summary.get_text(' ', strip=True)
        for tb in d.select('table'):
            hd = [th.get_text(' ', strip=True) for th in tb.select('thead th')]
            rows = [[td.get_text(' ', strip=True) for td in tr.find_all(['td', 'th'], recursive=False)] for tr in tb.select('tbody tr')]
            if t.startswith('活用表') and hd[:2] == ['Forme', '食べる (G2)']:
                names = [strip(_re.sub(r'\s*\(.*', '', h)) for h in hd[1:]]
                for r in rows:
                    if r[0] == 'Dictionnaire': continue
                    for k, nm in enumerate(names):
                        c = strip(r[k + 1])
                        if c and c != '—': getv(nm)['f'][r[0]] = c
            elif t.startswith('活用表') and hd[:2] == ['Finale', 'Exemple']:
                for r in rows:
                    v = r[1]; vv = getv(v)
                    for k, h in enumerate(hd[2:7]):
                        vv['f'][_G1MAP[h]] = r[k + 2]
                    te, ta = [x.strip() for x in r[7].split('/')]
                    vv['f']['Forme en て'] = te; vv['f']['Passé simple'] = ta
            elif t.startswith('基本') and hd[:2] == ['Verbe', 'Lecture'] and 'Négatif (ない)' in hd:
                for r in rows:
                    vv = getv(r[0], r[2], 'groupe 1 (en る)', r[1]); vv['f'].update(_regru(r[0])); vv['f']['Négatif simple'] = r[3]
    # lectures des formes
    for vv in verbs.values():
        def rd(x, vv=vv):
            if not _re.search(r'[一-鿿]', x): return ''
            m = _re.match(r'[一-鿿]+', vv['v'])
            if vv['v'] != '来る' and m and x.startswith(m.group()):
                okuri = vv['v'][len(m.group()):]; kp = vv['ka'][:len(vv['ka']) - len(okuri)]
                return kp + x[len(m.group()):]
            return _reading(x)
        vv['r'] = {k: rd(x) for k, x in vv['f'].items()}
        mm = _re.match(r'[一-鿿]+', vv['v'])
        if mm and vv['v'] != '来る':
            okuri = vv['v'][len(mm.group()):]; vv['kp'] = mm.group(); vv['kk'] = vv['ka'][:len(vv['ka']) - len(okuri)]
    return verbs

_GO = {'う': 'わいえお', 'く': 'かきけこ', 'ぐ': 'がぎげご', 'す': 'さしせそ', 'つ': 'たちてと', 'ぬ': 'なにねの', 'ぶ': 'ばびべぼ', 'む': 'まみめも', 'る': 'らりれろ'}
_TE = {'う': ('って', 'った'), 'つ': ('って', 'った'), 'る': ('って', 'った'), 'く': ('いて', 'いた'), 'ぐ': ('いで', 'いだ'), 'す': ('して', 'した'), 'ぬ': ('んで', 'んだ'), 'ぶ': ('んで', 'んだ'), 'む': ('んで', 'んだ')}
_HON = ('いらっしゃる', 'なさる', 'くださる', 'おっしゃる', 'ござる')
_NOCJ = {'ある', 'できる', '分かる', 'わかる', '見える', 'みえる', '聞こえる', 'きこえる', '要る'}
def gen_forms(s, ty):
    """19 formes du quiz à partir d'un verbe (kanji ou kana) et de son type u/ru/suru."""
    L = s[-1]; st = s[:-1]; pre = s[:-2]
    if ty == 'suru':
        a = i = pre + 'し'; te = pre + 'して'; ta = pre + 'した'; pot = pre + 'できる'; pas = pre + 'される'; cau = pre + 'させる'; vol = pre + 'しよう'; imp = pre + 'しろ'; ba = pre + 'すれば'
        caup = pre + 'させられる'
    elif ty == 'ru':
        a = i = st; te = st + 'て'; ta = st + 'た'; pot = pas = st + 'られる'; cau = st + 'させる'; vol = st + 'よう'; imp = st + 'ろ'; ba = st + 'れば'; caup = st + 'させられる'
    else:
        g = _GO[L]; a = st + g[0]; i = st + g[1]; e = st + g[2]; o = st + g[3]
        t = _TE[L]
        if s.endswith(('行く', 'いく')) and not s.endswith(('生きる',)): t = ('って', 'った')
        te = st + t[0]; ta = st + t[1]; pot = e + 'る'; pas = a + 'れる'; cau = a + 'せる'; vol = o + 'う'; imp = e; ba = e + 'ば'
        caup = a + 'せられる'
        if s.endswith(_HON): i = st + 'い'; imp = st + 'い'; te = st + 'って'; ta = st + 'った'
    n1 = lambda v: v[:-1] + 'ない'
    return {
        'Polie, présent': i + 'ます', 'Polie, négatif': i + 'ません', 'Polie, passé': i + 'ました', 'Polie, passé négatif': i + 'ませんでした',
        'Négatif simple': a + 'ない', 'Passé simple': ta, 'Passé négatif simple': a + 'なかった', 'Forme en て': te, 'て négatif': a + 'ないで',
        'Désidératif': i + 'たい', 'Potentiel': pot, 'Passif': pas, 'Causatif': cau, 'Causatif-passif': caup,
        'Volitif': vol, 'Impératif': imp, 'Interdiction': s + 'な', 'Conditionnel ば': ba, 'Conditionnel たら': ta + 'ら'}
def add_all_verbs(verbs, html):
    soup = _BS(html, 'html.parser'); n = 0; seen = set(verbs)
    for d in soup.select('details.cjd'):
        k, ka, ty = d['data-k'], d['data-ka'], d['data-t']
        if k in seen or k in _NOCJ or ka in _NOCJ or ty == 'irr': continue
        tr = d.find_parent('tr'); td = tr.find_all('td', recursive=False)
        fr = td[3].get_text(' ', strip=True)
        f = gen_forms(k, ty); r = gen_forms(ka, ty) if k != ka else {x: '' for x in f}
        gl = {'u': 'groupe 1', 'ru': 'groupe 2', 'suru': 'する-verbe'}[ty]
        v = {'v': k, 'ka': ka, 'fr': fr, 'g': gl, 'f': f, 'r': r}
        m = _re.match(r'^([一-鿿々]+)([぀-ゟ]*)$', k)
        if m and k != ka and ka.endswith(m.group(2)): v['kp'] = m.group(1); v['kk'] = ka[:len(ka) - len(m.group(2))]
        verbs[k] = v; seen.add(k); n += 1
    print('verbes ajoutés au quiz conj', n)
_GV = grammar_json(main)
add_all_verbs(_GV, main)
if '来る' in _GV:   # le lecteur automatique donne きさせる : le causatif de 来る se lit こさせる
    _GV['来る']['r'].update({'Causatif': 'こさせる', 'Causatif-passif': 'こさせられる'})

# Désir (〜たい) à quatre temps et souhait sur autrui (〜てほしい), dérivés des formes déjà présentes
_LH = 'Souhait sur autrui '
_TAI_HOSHII = [
    ('Désidératif négatif', 'Désidératif', lambda s: s[:-1] + 'くない'),
    ('Désidératif passé', 'Désidératif', lambda s: s[:-1] + 'かった'),
    ('Désidératif passé négatif', 'Désidératif', lambda s: s[:-1] + 'くなかった'),
    (_LH + '(てほしい)', 'Forme en て', lambda s: s + 'ほしい'),
    (_LH + 'négatif (ないでほしい)', 'て négatif', lambda s: s + 'ほしい'),
    (_LH + 'négatif (てほしくない)', 'Forme en て', lambda s: s + 'ほしくない'),
    (_LH + 'passé (てほしかった)', 'Forme en て', lambda s: s + 'ほしかった'),
    (_LH + 'passé négatif (ないでほしかった)', 'て négatif', lambda s: s + 'ほしかった'),
]
def add_tai_hoshii(verbs):
    n = 0
    for vv in verbs.values():
        f, r = vv['f'], vv['r']
        d, nd = f.get('Désidératif'), f.get('て négatif')
        if not d or not d.endswith('たい') or not f.get('Forme en て') or not nd or not nd.endswith('ないで'): continue
        for lab, src, fn in _TAI_HOSHII:
            f[lab] = fn(f[src]); r[lab] = fn(r[src]) if r.get(src) else ''
        n += 1
    print('verbes avec formes たい (4 temps) et てほしい (5 formes)', n)
add_tai_hoshii(_GV)

# Adjectifs en い / en な et です : mêmes mécanismes que les verbes (une entrée par adjectif, 10 formes), tirés du vocabulaire
import json as _jsA
_ADJ_NA = {'好き', '嫌い', '大好き', '上手', '下手', '得意', '苦手', '有名', '静か', '賑やか', '便利', '不便', '親切', '丁寧', '大切', '大変', '元気', '暇', '真剣', '不思議', 'きれい', '可哀想'}
_ADJ_SKIP = {'うらやましい', '主'}
_ADJ_FR = {'好き': 'Apprécié (aimer)', '嫌い': 'Détesté (détester)', '大好き': 'Adoré (adorer)', '眠い': 'Somnolent (avoir sommeil)'}
_ADJ_IRR = ('格好いい', 'かっこいい')       # いい → よ- pour toutes les formes conjuguées
def gen_adj(s, ty):
    if ty == 'i':
        st = s[:-2] + 'よ' if s in _ADJ_IRR else s[:-1]
        return {'Adjectif négatif': st + 'くない', 'Adjectif passé': st + 'かった', 'Adjectif passé négatif': st + 'くなかった', 'Adjectif en て': st + 'くて',
                'Adverbe': st + 'く', 'Adjectif poli': s + 'です', 'Adjectif poli négatif': st + 'くないです', 'Adjectif poli passé': st + 'かったです',
                'Adjectif poli passé négatif': st + 'くなかったです', 'Adjectif condition': st + 'かったら'}
    return {'Adjectif négatif': s + 'じゃない', 'Adjectif passé': s + 'だった', 'Adjectif passé négatif': s + 'じゃなかった', 'Adjectif en て': s + 'で',
            'Adverbe': s + 'に', 'Adjectif poli': s + 'です', 'Adjectif poli négatif': s + 'じゃありません', 'Adjectif poli passé': s + 'でした',
            'Adjectif poli passé négatif': s + 'じゃありませんでした', 'Adjectif condition': s + 'だったら'}
def add_adjectives(verbs):
    n = 0
    for e in _jsA.loads(_VJ):
        if e['c'] != 'Adjectifs' or e['g'] not in ('Adjectifs:い形容詞', 'Adjectifs:な形容詞', 'Adjectifs:Listes'): continue
        jp = e['jp'].strip()
        if jp in verbs or jp in _ADJ_SKIP or not jp or ' ' in jp or '/' in jp: continue
        ty = 'na' if (e['g'] == 'Adjectifs:な形容詞' or jp in _ADJ_NA) else 'i'
        if ty == 'i' and not jp.endswith('い'): continue
        ka = (e.get('ka') or e.get('kk') or jp).strip()
        if _re.search(r'[一-鿿]', ka) or ' ' in ka: ka = jp
        f = gen_adj(jp, ty); r = gen_adj(ka, ty) if ka != jp else {}
        fr = _re.sub(r'\s*⚠.*$', '', _re.sub(r'\s+', ' ', e['fr']).strip()); fr = _ADJ_FR.get(jp) or fr[:1].upper() + fr[1:]
        verbs[jp] = {'v': jp, 'ka': ka, 'fr': fr, 'g': 'adjectif en ' + ('な' if ty == 'na' else 'い'), 'adj': 1, 'f': f,
                     'r': {l: (r[l] if r and _re.search(r'[一-鿿]', f[l]) else '') for l in f}}
        n += 1
    print('adjectifs ajoutés au quiz conj', n)
add_adjectives(_GV)
