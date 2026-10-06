# Particules et compteurs
# Exécuté par build.py dans un espace de noms partagé (variables main, css, js…).
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
