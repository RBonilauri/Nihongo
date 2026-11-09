"""Génère src/data/radicaux.json et la rubrique « Radicaux » (cartes, ordre de Kangxi, variantes à part) dans src/base/japonais-nojs.html.
Sources : Kanji Alive (CC-BY 4.0, kanjialive/kanji-data-media) pour noms japonais, traits et position ; table de Kangxi (Unicode) pour les 214 radicaux ;
kanji fréquents tirés des listes de l'appli (src/data/kanji_composants.json). Usage : python3 src/tools/gen_radicaux.py"""
import os, re, sys, csv, json, collections, unicodedata
HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.insert(0, os.path.join(HERE, 'content')); sys.path.insert(0, os.path.join(HERE, 'data'))
from kanji_master import ROWS
from radicaux_lectures import LECT, ORIG, NEW_JA, NEW_FR
N = lambda c: unicodedata.normalize('NFKC', c)
INFO = {r[0]: (r[3], int(r[6][1])) for r in ROWS}
CP = json.load(open(os.path.join(HERE, 'data', 'kanji_composants.json'), encoding='utf-8'))
js = open(os.path.join(HERE, 'js', '08b-kanji-details.js'), encoding='utf-8').read()
KRN = dict(re.findall(r"'(.)': '([^']*)'", re.search(r"var KRN = \{(.*?)\};", js, re.S).group(1)))
KA = {}
for r in csv.DictReader(open(os.path.join(HERE, 'data', 'kanjialive_radicaux.csv'), encoding='utf-8')): KA[N(r['radical'])] = r
fr1 = lambda s: re.split(r'[,;，、/]', s)[0].strip()
def frname(g): return NEW_FR.get(g) or (INFO[g][0].split(',')[0].strip() if g in INFO else KRN.get(g, ''))
TAB = [6, 23, 31, 34, 23, 29, 20, 9, 11, 8, 6, 4, 4, 2, 1, 2, 1]
STROKES = [s for s, n in enumerate(TAB, 1) for _ in range(n)]
POS = {'へん': 'à gauche (へん)', 'つくり': 'à droite (つくり)', 'かんむり': 'en haut (かんむり)', 'あし': 'en bas (あし)', 'たれ': 'en haut à gauche (たれ)', 'にょう': 'en bas à gauche (にょう)', 'かまえ': 'autour (かまえ)'}
# variantes : (glyphe, radical de Kangxi, clé Kanji Alive, nom japonais de secours, traits de secours, position de secours)
VAR = [('氺', '水', '氺', 'したみず', 5, ''), ('氵', '水', '⺡', 'さんずい', 3, 'へん'), ('灬', '火', '⺣', 'れっか・れんが', 4, 'あし'),
       ('忄', '心', '⺖', 'りっしんべん', 3, 'へん'), ('⺗', '心', None, 'したごころ', 4, 'あし'), ('亻', '人', '⺅', 'にんべん', 2, 'へん'), ('𠆢', '人', '𠆢', 'ひとやね', 2, 'かんむり'),
       ('扌', '手', '⺘', 'てへん', 3, 'へん'), ('刂', '刀', '⺉', 'りっとう', 2, 'つくり'), ('犭', '犬', '⺨', 'けものへん', 3, 'へん'), ('礻', '示', '⺭', 'しめすへん', 4, 'へん'),
       ('衤', '衣', '⻂', 'ころもへん', 5, 'へん'), ('艹', '艸', '⺾', 'くさかんむり', 3, 'かんむり'), ('辶', '辵', '⻌', 'しんにょう・しんにゅう', 3, 'にょう'),
       ('阝', '阜', '⻖', 'こざとへん', 3, 'へん'), ('阝', '邑', '⻏', 'おおざと', 3, 'つくり'), ('罒', '网', '⺫', 'あみがしら', 5, 'かんむり'), ('攵', '攴', '⺙', 'ぼくづくり・のぶん', 4, 'つくり'),
       ('耂', '老', '⺹', 'おいかんむり', 4, 'かんむり'), ('月', '肉', None, 'にくづき', 4, ''), ('王', '玉', None, 'おうへん・たまへん', 4, 'へん'), ('牜', '牛', None, 'うしへん', 4, 'へん'),
       ('⺌', '小', '⺌', 'しょうかんむり', 3, 'かんむり'), ('尣', '尢', '⺐', 'だいのまげあし', 3, '')]
VKA = {'月': '⺝'}
cards = []   # dict(g, p, n, t, m, pos, kj, num)
par = {}
for i in range(214):
    g = N(chr(0x2F00 + i)); par[g] = i + 1
    ka = KA.get(g)
    ja = (ka['rad_name_ja'] if ka and ka['rad_name_ja'] else None) or LECT.get(g) or ORIG.get(g) or NEW_JA.get(g) or ''
    cards.append(dict(g=g, p='', n=ja, t=STROKES[i], m=frname(g), pos=(ka['rad_position_ja'] if ka else ''), num=i + 1, src='ka' if ka else 'main'))
for g, p, key, ja, st, pos in VAR:
    ka = KA.get(key) if key else None
    cards.append(dict(g=g, p=p, n=(ka['rad_name_ja'] if ka and ka['rad_name_ja'] else ja), t=int(ka['rad_stroke']) if ka and ka['rad_stroke'].isdigit() else st, m=frname(p), pos=(ka['rad_position_ja'] if ka and ka['rad_position_ja'] else pos), num=par[p] + 0.5, src='ka' if ka else 'main'))
# kanji fréquents (N5 d'abord) : kanji dont le radical affiché est ce glyphe (et ce parent pour les variantes)
bykey = collections.defaultdict(list)
for k, v in CP.items():
    if not v[0]: continue
    bykey[(v[0], v[2] if len(v) > 2 else '')].append(k)
for c in cards:
    ks = sorted(bykey.get((c['g'], c['p']), []), key=lambda k: (-INFO[k][1], k))[:4]
    c['kj'] = [(k, fr1(INFO[k][0])) for k in ks]
cards.sort(key=lambda c: (c['num'], c['p'] != ''))
for c in cards: c['n'] = c['n'] or ''
json.dump([{k: c[k] for k in ('g', 'p', 'n', 't', 'm', 'pos', 'src')} for c in cards], open(os.path.join(HERE, 'data', 'radicaux.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
def card(c):
    tag = '<span class="rtag">variante de %s</span>' % c['p'] if c['p'] else ''
    pp = POS.get(re.split(r'[,、 ]+', c['pos'])[0]) if c['pos'] else None
    pos = ' · Position : %s' % pp if pp else ''
    kj = ''.join('<span class="rkj"><b>%s</b>%s</span>' % (k, m) for k, m in c['kj']) or '<span class="rkj"><i>—</i></span>'
    return ('<div class="rcard" data-g="%s" data-p="%s" data-n="%s" data-m="%s"><div class="rg"><b>%s</b>%s</div><div class="ri"><div class="rt">%s</div><div class="rm">Nom : <b>%s</b></div><div class="rm">Traits : %s%s</div><div class="rk">%s</div></div></div>'
            % (c['g'], c['p'], c['n'], c['m'], c['g'], tag, c['m'][:1].upper() + c['m'][1:], c['n'] or '—', c['t'], pos, kj))
out, last = [], None
for c in cards:
    if c['t'] != last and not c['p']:
        last = c['t']; out.append('<div class="rhead">%d trait%s</div>' % (last, 's' if last > 1 else ''))
    out.append(card(c))
block = ('<!-- RAD-AUTO -->\n<div class="section-title">Tous les radicaux — ordre de Kangxi</div>\n<p style="font-size:0.78rem;color:var(--muted);line-height:1.8;margin-bottom:1rem">Les 214 radicaux et leurs variantes (formes prises dans un kanji, signalées « variante de … »). Noms japonais, traits et position : Kanji Alive (CC-BY 4.0) ; kanji fréquents : listes N5 à N1 de l\'appli.</p>\n<div class="rlist">\n' + '\n'.join(out) + '\n</div>\n<!-- /RAD-AUTO -->')
P = os.path.join(HERE, 'base', 'japonais-nojs.html'); h = open(P, encoding='utf-8').read()
OLD = '<div class="section-title">Radicaux essentiels à connaître</div>'
if OLD in h:      # 1re génération : on remplace l'ancien tableau (et l'ancien bloc auto) par les cartes
    a = h.index(OLD); e = h.index('</div></details>', h.index('<!-- /RAD-AUTO -->') if '<!-- /RAD-AUTO -->' in h else a)
    h = h[:a] + block + '\n' + h[e:]
else:
    h = re.sub(r'<!-- RAD-AUTO -->.*?<!-- /RAD-AUTO -->', lambda m: block, h, flags=re.S)
open(P, 'w', encoding='utf-8').write(h)
print(len(cards), 'cartes ;', sum(1 for c in cards if not c['n']), 'sans nom ;', sum(1 for c in cards if not c['kj']), 'sans kanji')
