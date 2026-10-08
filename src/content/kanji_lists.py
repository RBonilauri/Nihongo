# -*- coding: utf-8 -*-
# Génère les quatre listes de kanji (N5, N4, N3, N2) à partir de kanji_master.ROWS.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import T, P, H
import kanji_master

INTRO = {
 'N5': 'Les {n} kanji du JLPT N5 sont les plus fondamentaux — chiffres, temps, nature, famille, corps, directions. Ils réapparaissent dans des centaines de mots composés et forment la base de tout le reste.',
 'N4': 'Les {n} kanji du JLPT N4 couvrent le quotidien éducatif, professionnel et social — verbes essentiels, émotions, saisons, corps, ville. Maîtriser le N4 permet de lire des textes simples et des panneaux.',
 'N3': 'Les {n} kanji du JLPT N3 élargissent le vocabulaire à la vie sociale, au travail, à l’actualité et aux sentiments. Ils sont rangés par thème ; les mots clés sont les composés les plus fréquents.',
 'N2': 'Les {n} kanji de cette liste prolongent le N3 : {a} kanji du JLPT N2, puis {b} kanji plus rares (niveau N1 et au-delà), rangés dans les rubriques « Au-delà du N2 » : noms de lieux, de plats, d’animaux, mots du vocabulaire de l’appli. Ils sont classés par thème.',
}

def _sub(lv):
    rows = [r for r in kanji_master.ROWS if r[6] == lv]
    groups = {}
    for k, on, kun, s, kw, th, _ in rows: groups.setdefault(th, []).append([k, on, kun, s, kw])
    beyond = sum(len(v) for g, v in groups.items() if g.startswith('Au-delà'))
    txt = INTRO[lv].format(n=len(rows), a=len(rows) - beyond, b=beyond) + ' Ils alimentent le quiz kanji (niveau ' + lv + ') et le Quiz général.'
    bl = [P(txt)]
    for g in sorted(groups, key=lambda g: g.startswith('Au-delà')) if lv == 'N2' else groups:
        bl.append(H(g)); bl.append(T(['Kanji', 'On', 'Kun', 'Sens', 'Mots clés'], groups[g], jp=(0,), ro=()))
    return {'title': lv + ' — Liste complète (' + str(len(rows)) + ')', 'blocks': bl}

def subs(): return [_sub(l) for l in ('N5', 'N4', 'N3', 'N2')]
