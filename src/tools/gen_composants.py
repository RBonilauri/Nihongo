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
VARS = {'亻': '人', '氵': '水', '扌': '手', '忄': '心', '犭': '犬', '刂': '刀', '礻': '示', '衤': '衣', '灬': '火', '罒': '网', '攵': '攴'}   # variantes de radical = même radical
VF = {'人': '亻', '水': '氵', '手': '扌', '心': '忄', '犬': '犭', '刀': '刂', '示': '礻', '衣': '衤', '火': '灬', '网': '罒', '攴': '攵', '艸': '艹', '辵': '辶', '邑': '阝', '阜': '阝'}  # forme prise par le radical dans un kanji
def disp(c): return DISP.get(c, c)
FULL = set(r[0] for r in db.execute('select literal from character'))   # vrais kanji (KANJIDIC2), pas les variantes de radical ni les traits
_js = open(os.path.join(HERE, 'js', '08b-kanji-details.js'), encoding='utf-8').read()
NAMED = KSET | set(re.findall(r"'(.)': '", re.search(r'var KRN = \{(.*?)\};', _js, re.S).group(1)))   # éléments qu'on sait nommer
res = {}
for k in KS:
    R = chr(0x2F00 + rad[k] - 1) if k in rad else ''
    R = disp(unicodedata.normalize('NFKC', R)) if R else ''
    if R == k: R = ''
    if k in rad and (rad[k] <= 6 or R not in NAMED): R = ''   # radicaux-traits (一 丨 丶 丿 乙 亅) et radicaux sans nom : aucun intérêt
    lv = leaves(k); form = R
    for c in lv:                       # forme du radical telle qu'elle apparaît dans le kanji (ex. 水 → 氵)
        if c == R: form = R; break
        if R and VF.get(R) == c: form = c
    comps = []
    for c in lv:
        c = disp(c)
        if c != k and c in FULL and c in NAMED and c != '一' and c != R and c != form and VARS.get(c) != R and c not in comps: comps.append(c)
    # éléments : 1 à 4 kanji complets distincts, radical exclu (il est affiché à part), sinon on n'affiche rien (trop fin / atomique)
    comps = comps if 1 <= len(comps) <= 4 else []
    if R or comps: res[k] = [form, ''.join(comps)] + ([R] if R and form != R else [])
json.dump(res, open(os.path.join(HERE, 'data', 'kanji_composants.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'), sort_keys=True)
print(len(KS), 'kanji ;', len(res), 'avec données ;', sum(1 for v in res.values() if v[1]), 'avec composants ;', sum(1 for v in res.values() if v[0]), 'avec radical')
