"""Assemble l'application : lit le contenu (src/content), les feuilles de style (src/css),
le JavaScript (src/js) et écrit ../index.html. Lancer :  python3 src/build.py"""
import os, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(HERE, 'content'))
subprocess.check_call([sys.executable, os.path.join(HERE, 'assemble.py')])
def _read(*p): return open(os.path.join(HERE, *p), encoding='utf-8').read()
def _cat_files(d, names): return ''.join(_read(d, n) for n in names)
src = _read('build', 'nojs-plus.html')
css = src[src.index('<style>')+7 : src.index('</style>')]
main = src[src.index('<main>'):]

quiz_css = _cat_files('css', ['nav.css', 'map.css', 'quiz.css'])
extra_css = _cat_files('css', ['app.css'])

search_html = _read('html', 'shell.html')

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
        lvl = 'N5' if t.startswith('N5') else 'N4' if t.startswith('N4') else 'N3' if t.startswith('N3') else None
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

import hashlib as _hl
_CAT = {'旅行': 'Voyage', '会話': 'Conversation', '敬語': 'Keigo', '語彙': 'Vocabulaire', '時間': 'Temps', '形容詞': 'Adjectifs', '道具': 'Outils', '表現': 'Expressions', '助詞': 'Particules'}
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
                elif len(hd) >= 4 and hd[1] == 'Kanji' and hd[2] == 'Kana' and hd[3].lower().startswith('romaji'):
                    for c in rows:
                        for o in range(0, len(c) - 3, 4):
                            if hd[o + 1:o + 2] == ['Kanji']: add(cat, g, c[o], c[o + 1], c[o + 2], c[o + 3])
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
from parts_bank import PB as _PARTS
def _pk(s, a):
    k = _kana(s)
    if 'なん＿＿' in k and a in ('が', 'を', 'は', 'も', 'か'): k = k.replace('なん＿＿', 'なに＿＿')
    return k
def parts_json():
    return [{'i': 'p%02d' % n, 's': s, 'a': a, 'd': d.split(','), 'fr': fr, 'n': nt, 'r': r, 'g': g, 'k': _pk(s, a)} for n, (s, a, d, fr, nt, r, g) in enumerate(_PARTS)]

_CBASE = {'本': 'ほん', '枚': 'まい', '冊': 'さつ', '台': 'だい', '個': 'こ', '着': 'ちゃく', '杯': 'はい', '人': 'にん', '匹': 'ひき', '頭': 'とう', '羽': 'わ', '皿': 'さら', '膳': 'ぜん', '切れ': 'きれ', '階': 'かい', '回': 'かい', '番': 'ばん', 'つ': 'つ', '軒': 'けん', '足': 'そく', '通': 'つう', '件': 'けん', '部': 'ぶ', '歳': 'さい', '時間': 'じかん', '分': 'ふん', '週間': 'しゅうかん', 'か月': 'かげつ', '年': 'ねん'}
_CGROUP = {'Objets courants': 'obj', 'Êtres vivants': 'viv', 'Plats & boissons': 'pla', 'Autres': 'aut', 'Objets (suite)': 'obj', 'Durées et âge': 'tmp'}
_CEXTRA = {'皿': ('sara', 'Plats servis dans une assiette', []), '膳': ('zen', 'Portions de riz ou de repas servis dans un bol (formel)', []), '切れ': ('kire', 'Tranches et morceaux coupés', ['刺身', 'チーズ']),
           'つ': ('tsu', 'Série japonaise : objets sans compteur précis, jusqu’à 10', [])}
_WGLOSS = {'ペン': 'stylo', '木': 'arbre', '道': 'route', '映画': 'film', '紙': 'feuille de papier', '写真': 'photo', 'チケット': 'ticket', '本': 'livre', 'ノート': 'cahier', '雑誌': 'magazine',
           '車': 'voiture', '自転車': 'vélo', 'パソコン': 'ordinateur', 'テレビ': 'télévision', 'りんご': 'pomme', '卵': 'œuf', 'ボタン': 'bouton', 'スーツ': 'costume', 'コート': 'manteau', 'ドレス': 'robe',
           '水': 'eau (un verre)', 'コーヒー': 'café (une tasse)', 'ラーメン': 'ramen (un bol)', '学生': 'étudiant', '客': 'client', '友達': 'ami', '猫': 'chat', '犬': 'chien', '魚': 'poisson', '虫': 'insecte',
           '馬': 'cheval', '牛': 'vache', '象': 'éléphant', 'クジラ': 'baleine', '鳥': 'oiseau', '鶏': 'poule', '刺身': 'sashimi', 'チーズ': 'fromage', '家': 'maison', '店': 'boutique', 'レストラン': 'restaurant', '靴': 'chaussures', '靴下': 'chaussettes', '手紙': 'lettre', 'メール': 'e-mail', 'はがき': 'carte postale', '事件': 'affaire', '予約': 'réservation', '資料': 'document', '新聞': 'journal'}
def counters_json(html):
    soup = _BS(html, 'html.parser'); reads = []; info = {}
    for sec in soup.select('details.sec'):
        if not sec.summary.get_text().startswith('助数詞'): continue
        for d in sec.select('details.sub'):
            t = d.summary.get_text(' ', strip=True); g = _CGROUP.get(t)
            for tb in d.select('table'):
                hd = [th.get_text(' ', strip=True) for th in tb.select('thead th')]
                rows = [[td.get_text(' ', strip=True) for td in tr.find_all(['td', 'th'], recursive=False)] for tr in tb.select('tbody tr')]
                if t == 'Principes' and hd[:3] == ['Chiffre', 'Sino-japonais', 'Japonais classique']:
                    for r in rows:
                        k, y = r[2].split(' ')[:2]; reads.append({'k': k, 'y': y, 'c': 'つ', 'g': 'tsu', 'n': r[0], 'irr': 0})
                elif g and hd[:1] == ['Compteur']:
                    for r in rows:
                        info[r[1]] = {'ro': r[0], 'u': r[2].replace('superlatiif', 'superlatif'), 'ex': [w.strip() for w in r[3].split('、') if w.strip() and '＝' not in w]}
                elif g and hd and (hd[0] in ('1', 'N°1')):
                    for cell in rows[0]:
                        m = _re.match(r'^(\S+)\s+(\S+?)(⚠)?$', cell)
                        if not m: continue
                        k, y, irr = m.group(1), m.group(2), bool(m.group(3))
                        mm = _re.match(r'^([一二三四五六七八九十何]+)(.+)$', k)
                        reads.append({'k': k, 'y': y, 'c': mm.group(2), 'g': g, 'n': mm.group(1), 'irr': int(irr)})
    for k, (ro, u, ex) in _CEXTRA.items(): info.setdefault(k, {'ro': ro, 'u': u, 'ex': ex})
    gmap = {}
    for r in reads: gmap[r['c']] = r['g']
    counters = []
    for k, v in info.items():
        if k not in gmap or k == 'つ': continue
        ex = [[w, _WGLOSS[w], (_reading(w) if _HASK.search(w) else w)] for w in v['ex'] if w in _WGLOSS]
        counters.append({'k': k, 'ro': v['ro'], 'u': v['u'], 'g': gmap[k], 'b': _CBASE[k], 'ex': ex})
    counters.append({'k': 'つ', 'ro': 'tsu', 'u': _CEXTRA['つ'][1], 'g': 'tsu', 'b': 'つ', 'ex': []})
    print('compteurs', len(counters), 'lectures', len(reads), 'mots', sum(len(c['ex']) for c in counters))
    return _json.dumps({'reads': reads, 'counters': counters}, ensure_ascii=False, separators=(',', ':'))
_CJ = counters_json(main)
_GJ = _json.dumps({'verbs': list(_GV.values()), 'parts': parts_json()}, ensure_ascii=False, separators=(',', ':'))
print('grammar verbs', len(_GV), 'forms', sum(len(v['f']) for v in _GV.values()), 'parts', len(_PARTS))

main = add_romaji(main)
main = search_html + main
# searchbar must sit after the header so it sticks at the very top of main: keep as first child

js = _cat_files('js', sorted(f for f in os.listdir(os.path.join(HERE, 'js')) if f.endswith('.js')))

head = '''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Japonais Référence</title>
<meta name="theme-color" content="#1c1510">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="日本語">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<script>try{var t=localStorage.getItem("jp-theme");document.documentElement.setAttribute("data-theme",t==="dark"||t==="light"?t:(t==="auto"?"":"light"));if(!document.documentElement.getAttribute("data-theme"))document.documentElement.removeAttribute("data-theme")}catch(e){document.documentElement.setAttribute("data-theme","light")}</script>
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="icon" type="image/png" href="icon-192.png">
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@400;700&family=DM+Mono:wght@300;400;500&display=swap" rel="stylesheet">
<style>
html { -webkit-text-size-adjust: 100%; }
body { margin: 0; padding-top: env(safe-area-inset-top, 0px); padding-bottom: env(safe-area-inset-bottom, 0px); }
''' + css + extra_css + quiz_css + '''</style>
</head>
<body>
''' 
html = head + main + '\n<script type="application/json" id="kanji-data">' + _KJ.replace('</', '<\\/') + '</script>\n<script type="application/json" id="vocab-data">' + _VJ.replace('</', '<\\/') + '</script>\n<script type="application/json" id="grammar-data">' + _GJ.replace('</', '<\\/') + '</script>\n<script type="application/json" id="map-data">' + open(os.path.join(HERE, 'data', 'japanmap.json'), encoding='utf-8').read().replace('</', '<\\/') + '</script>\n<script type="application/json" id="counter-data">' + _CJ.replace('</', '<\\/') + '</script>\n<script>' + js + '</script>\n</body>\n</html>\n'
open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(html)
print(len(html))
