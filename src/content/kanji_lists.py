# -*- coding: utf-8 -*-
# Génère les cinq listes de kanji (N5, N4, N3, N2, N1) à partir de kanji_master.ROWS.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import T, P, H
import kanji_master

INTRO = {
 'N5': 'Les {n} kanji du JLPT N5 sont les plus fondamentaux — chiffres, temps, nature, famille, corps, directions. Ils réapparaissent dans des centaines de mots composés et forment la base de tout le reste.',
 'N4': 'Les {n} kanji du JLPT N4 couvrent le quotidien éducatif, professionnel et social — verbes essentiels, émotions, saisons, corps, ville. Maîtriser le N4 permet de lire des textes simples et des panneaux.',
 'N3': 'Les {n} kanji du JLPT N3 élargissent le vocabulaire à la vie sociale, au travail, à l’actualité et aux sentiments. Ils sont rangés par thème ; les mots clés sont les composés les plus fréquents.',
 'N2': 'Les {n} kanji du JLPT N2 prolongent le N3 : vocabulaire du travail, de la société, des médias et de la vie pratique. Ils sont rangés par thème ; les mots clés sont les composés les plus utiles.',
 'N1': 'Les {n} kanji de cette liste couvrent le JLPT N1 et au-delà : kanji de la presse, du droit, de la science et de la littérature, puis kanji plus rares (noms de lieux, de plats, de personnes). Ils sont rangés par thème ; les mots clés sont les composés les plus courants.',
}

def _sub(lv):
    rows = [r for r in kanji_master.ROWS if r[6] == lv]
    groups = {}
    for k, on, kun, s, kw, th, _, mx in rows: groups.setdefault(th, []).append([k, on, kun, s, kw + (' ＋ ' + mx if mx else '')])
    txt = INTRO[lv].format(n=len(rows)) + ' Ils alimentent le quiz kanji (niveau ' + lv + ') et le Quiz général.'
    bl = [P(txt)]
    for g in groups:
        bl.append(H(g)); bl.append(T(['Kanji', 'On', 'Kun', 'Sens', 'Mots clés'], groups[g], jp=(0,), ro=()))
    return {'title': lv + ' — Liste complète (' + str(len(rows)) + ')', 'blocks': bl}

def subs(): return [_sub(l) for l in ('N5', 'N4', 'N3', 'N2', 'N1')]
