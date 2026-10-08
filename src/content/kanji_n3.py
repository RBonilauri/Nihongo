import os, sys
# -*- coding: utf-8 -*-
import re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import T, P, N, H
import n3data_a, n3data_b, n3data_c, n3data_d, n3data_e

def _gl(s):  # pas de parenthèses imbriquées dans les gloses
    return s.replace('(', ', ').replace(')', '').replace('（', ', ').replace('）', '').strip(' ,')

def build(have):
    seen = set(have); groups = {}
    for m in (n3data_a, n3data_b, n3data_c, n3data_d, n3data_e):
        for g, lines in m.G.items():
            for ln in lines:
                p = ln.split('|')
                if len(p) != 5 or len(p[0]) != 1: continue
                k, on, kun, s, w = [x.strip() for x in p]
                if s in ('—', '') or w == '—' or k in seen: continue
                seen.add(k)
                ws = []
                for x in w.split(';'):
                    a = x.split(':')
                    if len(a) == 2 and k in a[0]: ws.append(f'{a[0].strip()} ({_gl(a[1])})')
                groups.setdefault(g, []).append([k, on, kun, s, ', '.join(ws)])
    return groups

def n3_sub(have):
    groups = build(have)
    total = sum(len(v) for v in groups.values())
    nc = sum(len(v) for g, v in groups.items() if not g.startswith('Compléments'))
    bl = [P(f'Les {nc} kanji du JLPT N3 élargissent le vocabulaire à la vie sociale, au travail, à l’actualité et aux sentiments. Ils sont rangés par thème ; les mots clés sont les composés les plus fréquents. Ils alimentent le quiz kanji (niveau N3) et le Quiz général. Les deux dernières rubriques (« Compléments du vocabulaire », {total - nc} kanji) regroupent des kanji plus rares (N2 et au-delà), de noms de lieux ou de plats, présents dans le vocabulaire de l’appli : ils sont aussi proposés dans le quiz kanji N3.')]
    for g, rows in groups.items():
        bl.append(H(g)); bl.append(T(['Kanji', 'On', 'Kun', 'Sens', 'Mots clés'], rows, jp=(0,), ro=()))
    return {'title': 'N3 — Liste complète', 'blocks': bl}
