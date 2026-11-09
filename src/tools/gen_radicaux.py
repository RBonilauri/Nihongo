"""Génère le tableau « Autres radicaux » de la rubrique Kanji > Radicaux et le branche dans src/base/japonais-nojs.html.
Les radicaux = ceux utilisés dans le menu « Composants » (src/data/kanji_composants.json). Usage : python3 src/tools/gen_radicaux.py"""
import os, re, sys, json, collections
HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.insert(0, os.path.join(HERE, 'content')); sys.path.insert(0, os.path.join(HERE, 'data'))
from kanji_master import ROWS
from radicaux_lectures import LECT
CP = json.load(open(os.path.join(HERE, 'data', 'kanji_composants.json'), encoding='utf-8'))
js = open(os.path.join(HERE, 'js', '08b-kanji-details.js'), encoding='utf-8').read()
KRN = dict(re.findall(r"'(.)': '([^']*)'", re.search(r"var KRN = \{(.*?)\};", js, re.S).group(1)))
INFO = {r[0]: (r[3], r[6]) for r in ROWS}
def name(c): return re.split(r'[,;，、]', INFO[c][0])[0].strip() if c in INFO else KRN[c]
P = os.path.join(HERE, 'base', 'japonais-nojs.html'); h = open(P, encoding='utf-8').read()
# 1) variantes ajoutées aux lignes existantes ; ⻌→辶 ; 钅 et 飠 (jamais utilisés) retirés
for a, b in (('氵', '氵／水'), ('亻', '亻／人'), ('扌', '扌／手'), ('⻌', '辶'), ('金／钅', '金'), ('食／飠', '食')):
    h = h.replace('>%s</td>' % a, '>%s</td>' % b, 1)   # idempotent : a n'existe plus après le 1er passage (les cellules d'origine sont uniques)
rub = set(''.join(re.findall(r'color:var\(--red\)">([^<]+)</td>', h[h.index('Radicaux essentiels'):(h.index('<!-- RAD-AUTO -->') if '<!-- RAD-AUTO -->' in h else h.index('筆順 — Traits'))])).replace('／', ''))
PAIRS = {'犭': '犭／犬', '犬': '犭／犬', '礻': '礻／示', '示': '礻／示'}
cnt = collections.Counter(v[0] for v in CP.values() if v[0])
assoc = collections.defaultdict(list)
for k, v in CP.items():
    if v[0]: assoc[PAIRS.get(v[0], v[0])].append(k)
rows, seen = [], set()
for g, n in sorted(((PAIRS.get(k, k), cnt[k]) for k in cnt if k not in rub), key=lambda t: -t[1]):
    if g in seen: continue
    seen.add(g)
    n = sum(cnt[c] for c in g.replace('／', ''))
    ks = sorted(assoc[g], key=lambda k: ({'N5': 0, 'N4': 1, 'N3': 2, 'N2': 3, 'N1': 4}[INFO[k][1]], k))[:5]
    first = g.split('／')[0]
    sens = name(first)
    lect = LECT[g if g in LECT else first]
    assoc_s = ', '.join('%s (%s)' % (k, name(k) if False else re.split(r'[,;，、/]', INFO[k][0])[0].strip()) for k in ks)
    rows.append((n, '<tr><td style="font-family:\'Noto Serif JP\',serif;font-size:1.6rem;color:var(--red)">%s</td><td style="font-size:0.82rem">%s</td><td style="font-size:0.82rem">%s</td><td style="font-size:0.82rem">%s</td></tr>' % (g, lect, sens, assoc_s)))
rows.sort(key=lambda t: -t[0])
block = ('<!-- RAD-AUTO -->\n<div class="section-title">Autres radicaux — classés par fréquence dans les kanji de l\'appli</div>\n<p style="font-size:0.78rem;color:var(--muted);line-height:1.8;margin-bottom:1rem">Tous les radicaux affichés dans « Composants » après une réponse de quiz kanji. Les kanji associés sont tirés des listes N5 à N1.</p>\n<div class="scroll-x"><table class="particle-grid">\n<thead><tr><th>Radical</th><th>Lecture</th><th>Sens</th><th>Kanji associés</th></tr></thead>\n<tbody>\n' + '\n'.join(r for _, r in rows) + '\n</tbody>\n</table></div>\n<!-- /RAD-AUTO -->')
if '<!-- RAD-AUTO -->' in h: h = re.sub(r'<!-- RAD-AUTO -->.*?<!-- /RAD-AUTO -->', lambda m: block, h, flags=re.S)
else:
    i = h.index('筆順 — Traits'); j = h.rindex('</div></details>', 0, i)
    h = h[:j] + block + '\n' + h[j:]
open(P, 'w', encoding='utf-8').write(h)
print(len(rows), 'lignes ajoutées')
