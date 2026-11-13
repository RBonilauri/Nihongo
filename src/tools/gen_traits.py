#!/usr/bin/env python3
"""Traits, fréquence et radical (classique, 1-214) de chaque kanji de l'appli, d'après KANJIDIC2 (jamdict.db).
Usage : python3 src/tools/gen_traits.py <jamdict.db>  →  src/data/kanji_traits.json  {kanji: [traits, rang de fréquence (0 = hors 2500), n° radical]}"""
import json, re, sqlite3, sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
h = open(os.path.join(os.path.dirname(ROOT), 'index.html'), encoding='utf-8').read()
kd = json.loads(re.search(r'id="kanji-data">(.*?)</script>', h, re.S).group(1).replace('<\\/', '</'))
db = sqlite3.connect(sys.argv[1])
rad = dict(db.execute("select c.literal, r.value from character c join radical r on r.cid=c.ID where r.rad_type='classical'").fetchall())
out = {}; miss = []
for e in kd:
    r = db.execute("select stroke_count, freq from character where literal=?", (e['k'],)).fetchone()
    if not r or not r[0]: miss.append(e['k']); continue
    out[e['k']] = [int(r[0]), int(r[1] or 0), int(rad.get(e['k'], 0))]
json.dump(out, open(os.path.join(ROOT, 'data', 'kanji_traits.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print(len(out), 'kanji ; sans données :', miss[:10], ' ; sans radical :', sum(1 for v in out.values() if not v[2]), ' ; avec fréquence :', sum(1 for v in out.values() if v[1]))
