"""Génère src/data/kanji_composants.json : {kanji: [radical_kangxi, "composants"]}.
Sources : CJKVI-IDS (décomposition, src/data/ids_cjkvi.txt) et KANJIDIC2 (radical classique, via jamdict-data).
Usage : python3 src/tools/gen_composants.py <jamdict.db>"""
import sys, re, json, sqlite3, unicodedata, os
HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.insert(0, os.path.join(HERE, 'content'))
from kanji_master import ROWS
KS = [r[0] for r in ROWS]; KSET = set(KS)
IDS = {}
for l in open(os.path.join(HERE, 'data', 'ids_cjkvi.txt'), encoding='utf-8'):
    p = l.rstrip('\n').split('\t')
    if len(p) >= 3 and not p[0].startswith('#'):
        IDS.setdefault(p[1], re.sub(r'\$\([A-Z]+\)|\[[A-Z]+\]', '', p[2]))
OPS = set('⿰⿱⿲⿳⿴⿵⿶⿷⿸⿹⿺⿻⿼⿽⿾⿿㇯')
def isid(c):
    return ('一' <= c <= '鿿') or ('⺀' <= c <= '⻳') or ('⼀' <= c <= '⿕') or ('㐀' <= c <= '䶿')
def leaves(c, top=True, depth=0):
    s = IDS.get(c)
    if not s or s == c or (not top and c in KSET) or depth > 4: return [c]
    out = []
    for ch in s:
        if ch in OPS: continue
        out += leaves(ch, False, depth + 1)
    return out
db = sqlite3.connect(sys.argv[1]); rad = {}
for ch, v in db.execute("select c.literal, r.value from character c join radical r on r.cid=c.ID where r.rad_type='classical'"): rad[ch] = int(v)
# formes affichées : variante usuelle du radical ; traits seuls sans signification propre écartés des éléments
DISP = {'辵': '辶', '⻌': '辶', '艸': '艹', '⺾': '艹'}
TRAITS = set('丿丶丨乚乀丷乛乁⺊龴龶㐄㐅㔾丱亅')
def disp(c): return DISP.get(c, c)
res = {}
for k in KS:
    R = chr(0x2F00 + rad[k] - 1) if k in rad else ''
    R = disp(unicodedata.normalize('NFKC', R)) if R else ''
    if R == k: R = ''
    comps = []
    for c in leaves(k):
        c = disp(c)
        if c != k and isid(c) and c not in TRAITS and c not in comps: comps.append(c)
    # composants : 2 à 4 éléments distincts, sinon on n'affiche rien (trop fin / atomique)
    comps = comps if 2 <= len(comps) <= 4 else []
    if R or comps: res[k] = [R, ''.join(comps)]
json.dump(res, open(os.path.join(HERE, 'data', 'kanji_composants.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'), sort_keys=True)
print(len(KS), 'kanji ;', len(res), 'avec données ;', sum(1 for v in res.values() if v[1]), 'avec composants ;', sum(1 for v in res.values() if v[0]), 'avec radical')
