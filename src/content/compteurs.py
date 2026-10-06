import os, sys
# -*- coding: utf-8 -*-
# Compléments : compteurs (objets, durées, âge)
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import T, P, N, H

def reads(label, k, forms):
    """forms: liste de 10 (+ ?) lectures kana ; ⚠ si irrégulière (dernier élément = lecture de 何)"""
    heads = [str(i) for i in range(1, 11)] + ['?']
    row = []
    for i, f in enumerate(forms):
        n = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '何'][i]
        irr = f.endswith('!')
        row.append(f'{n}{k} {f.rstrip("!")}' + ('⚠' if irr else ''))
    return H(label), T(heads, [row], jp=(), ro=())

def info(rows):
    return T(['Compteur', 'Kanji', 'S’utilise pour', 'Exemples'], rows, jp=(1,), ro=(0,))

def counters_subs():
    ken = reads('軒 (けん) — Maisons et boutiques', '軒', ['いっけん!', 'にけん', 'さんげん!', 'よんけん', 'ごけん', 'ろっけん!', 'ななけん', 'はっけん!', 'きゅうけん', 'じゅっけん!', 'なんげん!'])
    soku = reads('足 (そく) — Paires de chaussures', '足', ['いっそく!', 'にそく', 'さんぞく!', 'よんそく', 'ごそく', 'ろくそく', 'ななそく', 'はっそく!', 'きゅうそく', 'じゅっそく!', 'なんぞく!'])
    tsuu = reads('通 (つう) — Lettres et messages', '通', ['いっつう!', 'につう', 'さんつう', 'よんつう', 'ごつう', 'ろくつう', 'ななつう', 'はっつう!', 'きゅうつう', 'じゅっつう!', 'なんつう'])
    kken = reads('件 (けん) — Affaires, dossiers, cas', '件', ['いっけん!', 'にけん', 'さんけん', 'よんけん', 'ごけん', 'ろっけん!', 'ななけん', 'はっけん!', 'きゅうけん', 'じゅっけん!', 'なんけん'])
    bu = reads('部 (ぶ) — Exemplaires, parties', '部', ['いちぶ', 'にぶ', 'さんぶ', 'よんぶ', 'ごぶ', 'ろくぶ', 'ななぶ', 'はちぶ', 'きゅうぶ', 'じゅうぶ', 'なんぶ'])
    objets = {'title': 'Objets (suite)', 'blocks': [
        P('Compteurs supplémentaires pour les maisons, chaussures, lettres, dossiers et exemplaires. ⚠ = lecture irrégulière.'),
        *ken, *soku, *tsuu, *kken, *bu,
        H('Récapitulatif'),
        info([['ken', '軒', 'Maisons, immeubles, boutiques', '家、店、レストラン'], ['soku', '足', 'Paires de chaussures, chaussettes', '靴、靴下'],
              ['tsū', '通', 'Lettres, e-mails, documents', '手紙、メール、はがき'], ['ken', '件', 'Affaires, cas, dossiers, réservations', '事件、予約'],
              ['bu', '部', 'Exemplaires (journaux, documents)', '資料、新聞']]),
    ]}
    sai = reads('歳 (さい) — Âge', '歳', ['いっさい!', 'にさい', 'さんさい', 'よんさい', 'ごさい', 'ろくさい', 'ななさい', 'はっさい!', 'きゅうさい', 'じゅっさい!', 'なんさい'])
    jikan = reads('時間 (じかん) — Heures (durée)', '時間', ['いちじかん', 'にじかん', 'さんじかん', 'よじかん!', 'ごじかん', 'ろくじかん', 'ななじかん!', 'はちじかん', 'くじかん!', 'じゅうじかん', 'なんじかん'])
    fun = reads('分 (ふん / ぷん) — Minutes', '分', ['いっぷん!', 'にふん', 'さんぷん!', 'よんぷん!', 'ごふん', 'ろっぷん!', 'ななふん', 'はっぷん!', 'きゅうふん', 'じゅっぷん!', 'なんぷん!'])
    shuu = reads('週間 (しゅうかん) — Semaines', '週間', ['いっしゅうかん!', 'にしゅうかん', 'さんしゅうかん', 'よんしゅうかん', 'ごしゅうかん', 'ろくしゅうかん', 'ななしゅうかん', 'はっしゅうかん!', 'きゅうしゅうかん', 'じゅっしゅうかん!', 'なんしゅうかん'])
    getsu = reads('か月 (かげつ) — Mois (durée)', 'か月', ['いっかげつ!', 'にかげつ', 'さんかげつ', 'よんかげつ', 'ごかげつ', 'ろっかげつ!', 'ななかげつ', 'はっかげつ!', 'きゅうかげつ', 'じゅっかげつ!', 'なんかげつ'])
    nen = reads('年 (ねん) — Années', '年', ['いちねん', 'にねん', 'さんねん', 'よねん!', 'ごねん', 'ろくねん', 'しちねん!', 'はちねん', 'くねん!', 'じゅうねん', 'なんねん'])
    temps = {'title': 'Durées et âge', 'blocks': [
        P('Compter les durées et l’âge : heures, minutes, semaines, mois, années, ans. Attention aux pièges : 4 → よ (よじかん, よねん), 7 → しち ou なな, 9 → く (くじかん). Pour 20 ans : 二十歳 (はたち).'),
        *sai, *jikan, *fun, *shuu, *getsu, *nen,
        H('Récapitulatif'),
        info([['sai', '歳', 'Âge (ans)', ''], ['jikan', '時間', 'Durée en heures', ''], ['fun', '分', 'Minutes', ''],
              ['shūkan', '週間', 'Durée en semaines', ''], ['kagetsu', 'か月', 'Durée en mois', ''], ['nen', '年', 'Années', '']]),
    ]}
    return {'助数詞': [objets, temps]}
