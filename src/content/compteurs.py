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

def dates_blocks():
    """Jours du mois : 1er (ついたち) et 11 à 31, écrits « 11日 » comme sur un calendrier. Les jours 2 à 10 se lisent comme les durées (tableau « Jours (durée) »), donc pas de répétition ; ⚠ = lecture irrégulière."""
    y = {1: 'ついたち!', 14: 'じゅうよっか!', 20: 'はつか!', 24: 'にじゅうよっか!', 17: 'じゅうしちにち', 19: 'じゅうくにち', 27: 'にじゅうしちにち', 29: 'にじゅうくにち'}
    uni = ['', 'いち', 'に', 'さん', 'よん', 'ご', 'ろく', 'なな', 'はち', 'きゅう']
    def yomi(n):
        if n in y: return y[n]
        if n < 20: return 'じゅう' + uni[n - 10] + 'にち'
        if n < 30: return 'にじゅう' + uni[n - 20] + 'にち'
        return 'さんじゅう' + ('' if n == 30 else uni[n - 30]) + 'にち'
    out = [H('Les jours du mois (dates) — 1er et 11 au 31'),
           P('Sur un calendrier on écrit 1日, 11日… Du 2 au 10, la lecture est celle du tableau « Jours (durée) » ci-dessus (2日 = ふつか … 10日 = とおか). Le 1er est ついたち (≠ いちにち, « un jour »). ⚠ = lecture irrégulière : le 14 et le 24 (よっか), le 20 (はつか). Pièges : le 17 et le 27 se lisent しち (じゅうしちにち), le 19 et le 29 se lisent く (じゅうくにち). Les autres jours : chiffre + にち.')]
    days = [1] + list(range(11, 32))
    for chunk in (days[:11], days[11:]):
        row = ['%d日 %s' % (n, yomi(n).replace('!', '')) + ('⚠' if yomi(n).endswith('!') else '') for n in chunk]
        out.append(T([str(n) for n in chunk], [row], jp=(), ro=()))
    return out

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
    byou = reads('秒 (びょう) — Secondes', '秒', ['いちびょう', 'にびょう', 'さんびょう', 'よんびょう', 'ごびょう', 'ろくびょう', 'ななびょう', 'はちびょう', 'きゅうびょう', 'じゅうびょう', 'なんびょう'])
    nichi = reads('日 (にち / か) — Jours (durée)', '日', ['いちにち!', 'ふつか!', 'みっか!', 'よっか!', 'いつか!', 'むいか!', 'なのか!', 'ようか!', 'ここのか!', 'とおか!', 'なんにち'])
    dates = dates_blocks()
    temps = {'title': 'Durées et âge', 'blocks': [
        P('Compter les durées et l’âge : heures, minutes, secondes, jours, semaines, mois, années, ans. Attention aux pièges : 4 → よ (よじかん, よねん), 7 → しち ou なな, 9 → く (くじかん). Pour 20 ans : 二十歳 (はたち). Les secondes sont régulières (いち・に・さん… + びょう), mais les jours de 2 à 10 sont tous irréguliers : ふつか, みっか, よっか, いつか, むいか, なのか, ようか, ここのか, とおか (1 jour = いちにち ; le 1er du mois = ついたち).'),
        *sai, *jikan, *fun, *byou, *nichi, *shuu, *getsu, *nen,
        *dates, 
        H('Récapitulatif'),
        info([['sai', '歳', 'Âge (ans)', ''], ['jikan', '時間', 'Durée en heures', ''], ['fun', '分', 'Minutes', ''], ['byō', '秒', 'Secondes', ''], ['nichi', '日', 'Jours (durée) et jours du mois', ''],
              ['shūkan', '週間', 'Durée en semaines', ''], ['kagetsu', 'か月', 'Durée en mois', ''], ['nen', '年', 'Années', '']]),
    ]}
    return {'助数詞': [objets, temps]}
