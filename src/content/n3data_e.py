# -*- coding: utf-8 -*-
from kanji_ajouts import N3 as _A
from kanji_compl import N3 as _B
G = {g: t.strip().split("\n") for D in (_A, _B) for g, t in D.items()}
