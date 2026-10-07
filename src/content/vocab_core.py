import os, sys
# -*- coding: utf-8 -*-
# Contenu ajouté : verbes courants, lieux, maison, vêtements, météo, émotions, santé, onomatopées, pays, loisirs, panneaux
import re
import pykakasi
from content import T, P, N, H
_kks = pykakasi.kakasi()

def ro(kana, verb=False):
    s = ''.join(x['hepburn'] for x in _kks.convert(kana))
    tail = ''
    if verb and s.endswith(('ou', 'uu')): tail, s = s[-2:], s[:-2]
    for a, b in (('ou', 'ō'), ('oo', 'ō'), ('uu', 'ū'), ('aa', 'ā'), ('ii', 'ī'), ('ee', 'ē')): s = s.replace(a, b)
    return (s + tail).capitalize() if False else s + tail

def kanji_table(rows, extra=None, verb=False):
    heads = ['Kanji', 'Kana', 'Rōmaji', 'Sens'] + (['Groupe · て · ない'] if extra else [])
    out = []
    for r in rows:
        k, ka, fr = r[0], r[1], r[2]
        row = [k, ka, ro(ka, verb), fr]
        if extra: row.append(extra(r))
        out.append(row)
    return T(heads, out, jp=(0, 1), ro=(2,))

# ───────────────── VERBES ─────────────────
_GO = {'う': ('っ', 'わ'), 'つ': ('っ', 'た'), 'る': ('っ', 'ら'), 'く': ('い', 'か'), 'ぐ': ('い', 'が'), 'す': ('し', 'さ'), 'ぬ': ('ん', 'な'), 'ぶ': ('ん', 'ば'), 'む': ('ん', 'ま')}
_TE = {'う': 'て', 'つ': 'て', 'る': 'て', 'く': 'て', 'ぐ': 'で', 'す': 'て', 'ぬ': 'で', 'ぶ': 'で', 'む': 'で'}
def forms(k, g):
    """k = verbe en kanji/kana, g = 'u' (G1), 'ru' (G2), 'suru', 'irr'. Retourne (groupe, て, ない)."""
    if g == 'suru':
        base = k[:-2]; return 'する', base + 'して', base + 'しない'
    if k == '来る': return 'Irrégulier', '来て', '来ない'
    if k == 'ある': return 'G1', 'あって', 'ない'
    if g == 'ru': return 'G2', k[:-1] + 'て', k[:-1] + 'ない'
    last = k[-1]; stem = k[:-1]
    if k.endswith('行く'): return 'G1 (irrég.)', stem + 'って', stem + 'かない'
    t, a = _GO[last]
    te = stem + t + _TE[last]
    return 'G1', te, stem + a + 'ない'
def _extra(r):
    g, te, nai = forms(r[0], r[3])
    return f'{g} · {te} · {nai}'

V = {}
V['Vie quotidienne'] = [
 ('起きる', 'おきる', 'Se lever, se réveiller', 'ru'), ('寝る', 'ねる', 'Dormir, se coucher', 'ru'), ('食べる', 'たべる', 'Manger', 'ru'), ('飲む', 'のむ', 'Boire', 'u'),
 ('洗う', 'あらう', 'Laver', 'u'), ('着る', 'きる', 'Porter (haut du corps)', 'ru'), ('履く', 'はく', 'Porter (chaussures, pantalon)', 'u'), ('脱ぐ', 'ぬぐ', 'Enlever (vêtement, chaussures)', 'u'),
 ('使う', 'つかう', 'Utiliser', 'u'), ('開ける', 'あける', 'Ouvrir (quelque chose)', 'ru'), ('閉める', 'しめる', 'Fermer (quelque chose)', 'ru'), ('作る', 'つくる', 'Faire, fabriquer', 'u'),
 ('持つ', 'もつ', 'Tenir, avoir sur soi', 'u'), ('置く', 'おく', 'Poser, déposer', 'u'), ('取る', 'とる', 'Prendre', 'u'), ('待つ', 'まつ', 'Attendre', 'u'),
 ('立つ', 'たつ', 'Se lever, être debout', 'u'), ('座る', 'すわる', 'S’asseoir', 'u'), ('歩く', 'あるく', 'Marcher', 'u'), ('走る', 'はしる', 'Courir', 'u'),
 ('泳ぐ', 'およぐ', 'Nager', 'u'), ('遊ぶ', 'あそぶ', 'Jouer, s’amuser', 'u'), ('休む', 'やすむ', 'Se reposer, s’absenter', 'u'), ('働く', 'はたらく', 'Travailler', 'u'),
 ('住む', 'すむ', 'Habiter', 'u'), ('生まれる', 'うまれる', 'Naître', 'ru'), ('生きる', 'いきる', 'Vivre', 'ru'), ('死ぬ', 'しぬ', 'Mourir', 'u'),
]
V['Déplacements'] = [
 ('行く', 'いく', 'Aller', 'u'), ('来る', 'くる', 'Venir', 'irr'), ('帰る', 'かえる', 'Rentrer chez soi', 'u'), ('出る', 'でる', 'Sortir, partir', 'ru'),
 ('入る', 'はいる', 'Entrer', 'u'), ('着く', 'つく', 'Arriver', 'u'), ('出かける', 'でかける', 'Sortir (de chez soi)', 'ru'), ('乗る', 'のる', 'Monter (dans un transport)', 'u'),
 ('降りる', 'おりる', 'Descendre (d’un transport)', 'ru'), ('乗り換える', 'のりかえる', 'Changer (de train)', 'ru'), ('通る', 'とおる', 'Passer par', 'u'), ('渡る', 'わたる', 'Traverser', 'u'),
 ('曲がる', 'まがる', 'Tourner', 'u'), ('止まる', 'とまる', 'S’arrêter', 'u'), ('止める', 'とめる', 'Arrêter, garer', 'ru'), ('迷う', 'まよう', 'Se perdre, hésiter', 'u'),
 ('戻る', 'もどる', 'Revenir en arrière', 'u'), ('向かう', 'むかう', 'Se diriger vers', 'u'), ('急ぐ', 'いそぐ', 'Se dépêcher', 'u'), ('並ぶ', 'ならぶ', 'Faire la queue, s’aligner', 'u'),
 ('泊まる', 'とまる', 'Loger, passer la nuit', 'u'), ('運ぶ', 'はこぶ', 'Transporter', 'u'),
]
V['Communication'] = [
 ('言う', 'いう', 'Dire', 'u'), ('話す', 'はなす', 'Parler', 'u'), ('聞く', 'きく', 'Écouter, demander', 'u'), ('聞こえる', 'きこえる', 'Être audible, entendre', 'ru'),
 ('答える', 'こたえる', 'Répondre', 'ru'), ('伝える', 'つたえる', 'Transmettre, faire savoir', 'ru'), ('頼む', 'たのむ', 'Demander, commander', 'u'), ('断る', 'ことわる', 'Refuser', 'u'),
 ('謝る', 'あやまる', 'S’excuser', 'u'), ('笑う', 'わらう', 'Rire, sourire', 'u'), ('泣く', 'なく', 'Pleurer', 'u'), ('歌う', 'うたう', 'Chanter', 'u'),
 ('読む', 'よむ', 'Lire', 'u'), ('書く', 'かく', 'Écrire', 'u'), ('見る', 'みる', 'Regarder, voir', 'ru'), ('見える', 'みえる', 'Être visible, se voir', 'ru'),
 ('見せる', 'みせる', 'Montrer', 'ru'), ('会う', 'あう', 'Rencontrer', 'u'), ('呼ぶ', 'よぶ', 'Appeler', 'u'), ('送る', 'おくる', 'Envoyer', 'u'),
 ('教える', 'おしえる', 'Enseigner, indiquer', 'ru'), ('習う', 'ならう', 'Apprendre (auprès de quelqu’un)', 'u'), ('覚える', 'おぼえる', 'Mémoriser, retenir', 'ru'), ('忘れる', 'わすれる', 'Oublier', 'ru'),
 ('思い出す', 'おもいだす', 'Se rappeler', 'u'), ('数える', 'かぞえる', 'Compter', 'ru'), ('間違える', 'まちがえる', 'Se tromper', 'ru'),
]
V['Donner, recevoir, échanger'] = [
 ('あげる', 'あげる', 'Donner (à quelqu’un d’autre)', 'ru'), ('もらう', 'もらう', 'Recevoir', 'u'), ('くれる', 'くれる', 'Donner (à moi / à mon cercle)', 'ru'), ('貸す', 'かす', 'Prêter', 'u'),
 ('借りる', 'かりる', 'Emprunter', 'ru'), ('返す', 'かえす', 'Rendre', 'u'), ('渡す', 'わたす', 'Remettre, tendre', 'u'), ('買う', 'かう', 'Acheter', 'u'),
 ('売る', 'うる', 'Vendre', 'u'), ('払う', 'はらう', 'Payer', 'u'), ('探す', 'さがす', 'Chercher', 'u'), ('見つける', 'みつける', 'Trouver', 'ru'),
 ('見つかる', 'みつかる', 'Être trouvé', 'u'), ('なくす', 'なくす', 'Perdre (un objet)', 'u'), ('落とす', 'おとす', 'Faire tomber, perdre', 'u'), ('拾う', 'ひろう', 'Ramasser', 'u'),
 ('捨てる', 'すてる', 'Jeter', 'ru'), ('手伝う', 'てつだう', 'Aider', 'u'), 
]
V['Esprit et sentiments'] = [
 ('思う', 'おもう', 'Penser, trouver que', 'u'), ('考える', 'かんがえる', 'Réfléchir', 'ru'), ('知る', 'しる', 'Connaître, apprendre', 'u'), ('分かる', 'わかる', 'Comprendre', 'u'),
 ('信じる', 'しんじる', 'Croire, faire confiance', 'ru'), ('決める', 'きめる', 'Décider', 'ru'), ('選ぶ', 'えらぶ', 'Choisir', 'u'), ('困る', 'こまる', 'Être embêté, en difficulté', 'u'),
 ('驚く', 'おどろく', 'Être surpris', 'u'), ('喜ぶ', 'よろこぶ', 'Se réjouir', 'u'), ('楽しむ', 'たのしむ', 'Profiter, s’amuser', 'u'), ('疲れる', 'つかれる', 'Être fatigué', 'ru'),
 ('慣れる', 'なれる', 'S’habituer', 'ru'), ('間に合う', 'まにあう', 'Arriver à temps', 'u'), ('足りる', 'たりる', 'Suffire', 'ru'), ('要る', 'いる', 'Avoir besoin de', 'u'),
 ('気をつける', 'きをつける', 'Faire attention', 'ru'), ('比べる', 'くらべる', 'Comparer', 'ru'),
]
V['Objets, changements, états'] = [
 ('入れる', 'いれる', 'Mettre dedans', 'ru'), ('出す', 'だす', 'Sortir, remettre, envoyer', 'u'), ('付ける', 'つける', 'Allumer, fixer, mettre', 'ru'), ('消す', 'けす', 'Éteindre, effacer', 'u'),
 ('切る', 'きる', 'Couper', 'u'), ('押す', 'おす', 'Pousser, appuyer', 'u'), ('引く', 'ひく', 'Tirer', 'u'), ('壊れる', 'こわれる', 'Se casser', 'ru'),
 ('壊す', 'こわす', 'Casser', 'u'), ('直す', 'なおす', 'Réparer, corriger', 'u'), ('治る', 'なおる', 'Guérir', 'u'), ('落ちる', 'おちる', 'Tomber', 'ru'),
 ('始まる', 'はじまる', 'Commencer (intransitif)', 'u'), ('始める', 'はじめる', 'Commencer (transitif)', 'ru'), ('終わる', 'おわる', 'Se terminer', 'u'), ('続ける', 'つづける', 'Continuer (transitif)', 'ru'),
 ('続く', 'つづく', 'Continuer (intransitif)', 'u'), ('変える', 'かえる', 'Changer (transitif)', 'ru'), ('変わる', 'かわる', 'Changer (intransitif)', 'u'), ('増える', 'ふえる', 'Augmenter', 'ru'),
 ('減る', 'へる', 'Diminuer', 'u'), ('かかる', 'かかる', 'Coûter, prendre (du temps)', 'u'), ('掛ける', 'かける', 'Accrocher, passer (un appel)', 'ru'), ('ある', 'ある', 'Il y a (chose), exister', 'u'),
]
V['Cuisine et météo'] = [
 ('焼く', 'やく', 'Griller, cuire', 'u'), ('煮る', 'にる', 'Mijoter', 'ru'), ('茹でる', 'ゆでる', 'Faire bouillir (à l’eau)', 'ru'), ('炒める', 'いためる', 'Faire sauter', 'ru'),
 ('揚げる', 'あげる', 'Frire', 'ru'), ('混ぜる', 'まぜる', 'Mélanger', 'ru'), ('温める', 'あたためる', 'Réchauffer', 'ru'), ('冷やす', 'ひやす', 'Refroidir', 'u'),
 ('降る', 'ふる', 'Tomber (pluie, neige)', 'u'), ('吹く', 'ふく', 'Souffler (vent)', 'u'), ('晴れる', 'はれる', 'S’éclaircir, faire beau', 'ru'), ('曇る', 'くもる', 'Se couvrir', 'u'),
 ('咲く', 'さく', 'Fleurir', 'u'),
]
# verbes en する (nom + する)
SURU = [
 ('勉強する', 'べんきょうする', 'Étudier'), ('散歩する', 'さんぽする', 'Se promener'), ('運転する', 'うんてんする', 'Conduire'), ('予約する', 'よやくする', 'Réserver'),
 ('心配する', 'しんぱいする', 'S’inquiéter'), ('質問する', 'しつもんする', 'Poser une question'), ('電話する', 'でんわする', 'Téléphoner'), ('掃除する', 'そうじする', 'Nettoyer'),
 ('洗濯する', 'せんたくする', 'Faire la lessive'), ('料理する', 'りょうりする', 'Cuisiner'), ('旅行する', 'りょこうする', 'Voyager'), ('結婚する', 'けっこんする', 'Se marier'),
 ('練習する', 'れんしゅうする', 'S’entraîner'), ('準備する', 'じゅんびする', 'Préparer'), ('説明する', 'せつめいする', 'Expliquer'), ('利用する', 'りようする', 'Utiliser (un service)'),
 ('紹介する', 'しょうかいする', 'Présenter'), ('案内する', 'あんないする', 'Guider, accompagner'), ('出発する', 'しゅっぱつする', 'Partir (départ)'), ('到着する', 'とうちゃくする', 'Arriver (arrivée)'),
 ('注文する', 'ちゅうもんする', 'Commander'), ('確認する', 'かくにんする', 'Vérifier'), ('連絡する', 'れんらくする', 'Contacter'), ('参加する', 'さんかする', 'Participer'),
 ('相談する', 'そうだんする', 'Consulter, demander conseil'), ('約束する', 'やくそくする', 'Promettre, convenir'), ('招待する', 'しょうたいする', 'Inviter'), ('買い物する', 'かいものする', 'Faire des achats'),
]
# ── Verbes supplémentaires ──
_NEW = {}
_NEW['Verbes de base essentiels'] = [
 ('いる', 'いる', 'Être, se trouver (êtres animés)', 'ru'), ('なる', 'なる', 'Devenir', 'u'), ('できる', 'できる', 'Pouvoir, être possible', 'ru'), ('行う', 'おこなう', 'Effectuer, tenir (événement)', 'u'),
 ('違う', 'ちがう', 'Être différent, être faux', 'u'), ('合う', 'あう', 'Convenir, être juste', 'u'), ('似る', 'にる', 'Ressembler', 'ru'), ('似合う', 'にあう', 'Aller bien (vêtement, personne)', 'u'),
 ('残る', 'のこる', 'Rester', 'u'), ('残す', 'のこす', 'Laisser, ne pas finir', 'u'), ('含む', 'ふくむ', 'Inclure, contenir', 'u'), ('含める', 'ふくめる', 'Inclure (dans un total)', 'ru'),
 ('分ける', 'わける', 'Diviser, partager', 'ru'), ('合わせる', 'あわせる', 'Ajuster, faire coïncider', 'ru'), ('役に立つ', 'やくにたつ', 'Être utile', 'u'), ('気づく', 'きづく', 'Remarquer, s’apercevoir', 'u'),
 ('感じる', 'かんじる', 'Ressentir', 'ru'), ('当たる', 'あたる', 'Toucher, tomber juste', 'u'), ('起こる', 'おこる', 'Se produire', 'u'), ('起こす', 'おこす', 'Réveiller, provoquer', 'u'),
 ('決まる', 'きまる', 'Être décidé', 'u'), ('済む', 'すむ', 'Être terminé, suffire', 'u'), ('済ませる', 'すませる', 'Terminer, régler', 'ru'), ('従う', 'したがう', 'Suivre, obéir à', 'u'),
]
_NEW['Corps, santé et soins'] = [
 ('磨く', 'みがく', 'Se brosser (dents), polir', 'u'), ('浴びる', 'あびる', 'Prendre (une douche), recevoir', 'ru'), ('拭く', 'ふく', 'Essuyer', 'u'), ('眠る', 'ねむる', 'Dormir, s’endormir', 'u'),
 ('覚める', 'さめる', 'S’éveiller, se dissiper', 'ru'), ('太る', 'ふとる', 'Grossir', 'u'), ('痩せる', 'やせる', 'Maigrir', 'ru'), ('育つ', 'そだつ', 'Grandir', 'u'),
 ('育てる', 'そだてる', 'Élever, cultiver', 'ru'), ('倒れる', 'たおれる', 'S’effondrer, tomber', 'ru'), ('酔う', 'よう', 'Être ivre, avoir le mal des transports', 'u'), ('吐く', 'はく', 'Vomir, cracher', 'u'),
 ('痛む', 'いたむ', 'Faire mal', 'u'), ('産む', 'うむ', 'Mettre au monde', 'u'), ('亡くなる', 'なくなる', 'Décéder', 'u'), ('温まる', 'あたたまる', 'Se réchauffer', 'u'),
 ('冷える', 'ひえる', 'Se refroidir, avoir froid', 'ru'), ('乾く', 'かわく', 'Sécher, avoir soif', 'u'), ('乾かす', 'かわかす', 'Faire sécher', 'u'), ('濡れる', 'ぬれる', 'Être mouillé', 'ru'),
]
_NEW['Gestes et manipulations'] = [
 ('折る', 'おる', 'Plier, casser (os, branche)', 'u'), ('破る', 'やぶる', 'Déchirer', 'u'), ('破れる', 'やぶれる', 'Se déchirer', 'ru'), ('割る', 'わる', 'Casser (verre, œuf)', 'u'),
 ('割れる', 'われる', 'Se briser', 'ru'), ('曲げる', 'まげる', 'Plier, courber', 'ru'), ('倒す', 'たおす', 'Renverser, abattre', 'u'), ('投げる', 'なげる', 'Lancer', 'ru'),
 ('打つ', 'うつ', 'Frapper, taper (clavier)', 'u'), ('叩く', 'たたく', 'Frapper, taper', 'u'), ('蹴る', 'ける', 'Donner un coup de pied', 'u'), ('掴む', 'つかむ', 'Saisir', 'u'),
 ('握る', 'にぎる', 'Serrer, empoigner', 'u'), ('引っ張る', 'ひっぱる', 'Tirer fort', 'u'), ('回す', 'まわす', 'Faire tourner', 'u'), ('回る', 'まわる', 'Tourner, faire le tour', 'u'),
 ('動く', 'うごく', 'Bouger, fonctionner', 'u'), ('動かす', 'うごかす', 'Déplacer, actionner', 'u'), ('並べる', 'ならべる', 'Aligner, disposer', 'ru'), ('片付ける', 'かたづける', 'Ranger, débarrasser', 'ru'),
 ('掃く', 'はく', 'Balayer', 'u'), ('干す', 'ほす', 'Étendre, faire sécher', 'u'), ('畳む', 'たたむ', 'Plier (linge)', 'u'), ('敷く', 'しく', 'Étendre, mettre au sol (futon)', 'u'),
 ('貼る', 'はる', 'Coller, afficher', 'u'), ('塗る', 'ぬる', 'Peindre, étaler (crème)', 'u'), ('縫う', 'ぬう', 'Coudre', 'u'), ('包む', 'つつむ', 'Emballer, envelopper', 'u'),
 ('結ぶ', 'むすぶ', 'Nouer, relier', 'u'), ('測る', 'はかる', 'Mesurer', 'u'), ('積む', 'つむ', 'Empiler, charger', 'u'), ('乗せる', 'のせる', 'Poser sur, embarquer', 'ru'),
 ('下ろす', 'おろす', 'Retirer (argent), déposer, descendre', 'u'), ('繋ぐ', 'つなぐ', 'Relier, connecter', 'u'), ('繋がる', 'つながる', 'Être connecté', 'u'), ('切れる', 'きれる', 'Se couper, être épuisé', 'ru'),
 ('外す', 'はずす', 'Enlever, retirer', 'u'), ('外れる', 'はずれる', 'Se détacher, rater', 'ru'), ('取れる', 'とれる', 'Se détacher, pouvoir être pris', 'ru'), ('取り替える', 'とりかえる', 'Remplacer, échanger', 'ru'),
 ('隠す', 'かくす', 'Cacher', 'u'), ('隠れる', 'かくれる', 'Se cacher', 'ru'), ('広げる', 'ひろげる', 'Déplier, étaler', 'ru'), ('広がる', 'ひろがる', 'S’étendre, se répandre', 'u'),
 ('離す', 'はなす', 'Lâcher, séparer', 'u'), ('離れる', 'はなれる', 'S’éloigner', 'ru'), ('近づく', 'ちかづく', 'S’approcher', 'u'), ('向く', 'むく', 'Se tourner vers', 'u'),
]
_NEW['Études, travail et activités'] = [
 ('学ぶ', 'まなぶ', 'Apprendre, étudier', 'u'), ('調べる', 'しらべる', 'Chercher (une info), vérifier', 'ru'), ('試す', 'ためす', 'Essayer, tester', 'u'), ('写す', 'うつす', 'Copier, photographier', 'u'),
 ('描く', 'かく', 'Dessiner, peindre', 'u'), ('進む', 'すすむ', 'Avancer', 'u'), ('進める', 'すすめる', 'Faire avancer', 'ru'), ('勧める', 'すすめる', 'Recommander, conseiller', 'ru'),
 ('上がる', 'あがる', 'Monter, augmenter', 'u'), ('下がる', 'さがる', 'Descendre, baisser', 'u'), ('上げる', 'あげる', 'Lever, augmenter', 'ru'), ('下げる', 'さげる', 'Baisser, abaisser', 'ru'),
 ('届く', 'とどく', 'Parvenir, arriver (colis)', 'u'), ('届ける', 'とどける', 'Livrer, remettre', 'ru'), ('集まる', 'あつまる', 'Se rassembler', 'u'), ('集める', 'あつめる', 'Collecter, rassembler', 'ru'),
 ('遅れる', 'おくれる', 'Être en retard', 'ru'), ('頑張る', 'がんばる', 'Se donner du mal, tenir bon', 'u'), ('諦める', 'あきらめる', 'Abandonner, renoncer', 'ru'), ('勝つ', 'かつ', 'Gagner', 'u'),
 ('負ける', 'まける', 'Perdre (match), faire une remise', 'ru'), ('誘う', 'さそう', 'Inviter, proposer de venir', 'u'), ('招く', 'まねく', 'Inviter, convier', 'u'), ('祝う', 'いわう', 'Fêter, féliciter', 'u'),
 ('贈る', 'おくる', 'Offrir (cadeau)', 'u'), ('飛ぶ', 'とぶ', 'Voler, sauter', 'u'), ('登る', 'のぼる', 'Gravir, escalader', 'u'), ('滑る', 'すべる', 'Glisser, skier', 'u'),
 ('釣る', 'つる', 'Pêcher', 'u'), ('踊る', 'おどる', 'Danser', 'u'), ('弾く', 'ひく', 'Jouer (piano, guitare)', 'u'), ('撮る', 'とる', 'Prendre (une photo)', 'u'),
 ('勤める', 'つとめる', 'Travailler pour (une entreprise)', 'ru'), ('辞める', 'やめる', 'Quitter, arrêter', 'ru'), ('引っ越す', 'ひっこす', 'Déménager', 'u'), ('通う', 'かよう', 'Fréquenter, faire la navette', 'u'),
 ('建てる', 'たてる', 'Construire', 'ru'), ('建つ', 'たつ', 'Être construit', 'u'),
]
_NEW['Services, voyage et argent'] = [
 ('預ける', 'あずける', 'Confier, déposer (bagages)', 'ru'), ('預かる', 'あずかる', 'Garder en dépôt', 'u'), ('受け取る', 'うけとる', 'Recevoir, réceptionner', 'u'), ('受ける', 'うける', 'Passer (examen), subir', 'ru'),
 ('申し込む', 'もうしこむ', 'S’inscrire, faire une demande', 'u'), ('払い戻す', 'はらいもどす', 'Rembourser', 'u'), ('取り消す', 'とりけす', 'Annuler', 'u'), ('延ばす', 'のばす', 'Reporter, prolonger', 'u'),
 ('延びる', 'のびる', 'Être reporté, se prolonger', 'ru'), ('確かめる', 'たしかめる', 'S’assurer, vérifier', 'ru'), ('寄る', 'よる', 'Passer (chez, par)', 'u'), ('立ち寄る', 'たちよる', 'Faire un détour, s’arrêter', 'u'),
 ('支払う', 'しはらう', 'Régler (un paiement)', 'u'), ('稼ぐ', 'かせぐ', 'Gagner (de l’argent)', 'u'), ('貯める', 'ためる', 'Économiser, épargner', 'ru'), ('余る', 'あまる', 'Rester, être en trop', 'u'),
 ('足す', 'たす', 'Ajouter', 'u'), ('売れる', 'うれる', 'Se vendre', 'ru'), ('売り切れる', 'うりきれる', 'Être épuisé', 'ru'), ('混む', 'こむ', 'Être bondé', 'u'),
 ('空く', 'すく', 'Se vider, être peu fréquenté', 'u'), ('開く', 'あく', 'S’ouvrir', 'u'), ('閉まる', 'しまる', 'Se fermer', 'u'), ('訪れる', 'おとずれる', 'Visiter, se rendre à', 'ru'),
 ('迎える', 'むかえる', 'Accueillir', 'ru'), ('見送る', 'みおくる', 'Raccompagner, dire au revoir', 'u'), ('流行る', 'はやる', 'Être à la mode, se répandre', 'u'), ('下りる', 'おりる', 'Descendre, être accordé (permis)', 'ru'),
 ('お願いする', 'おねがいする', 'Demander (poli)', 'suru'),
]
_NEW['Relations et sentiments'] = [
 ('嫌う', 'きらう', 'Détester', 'u'), ('怒る', 'おこる', 'Se fâcher', 'u'), ('叱る', 'しかる', 'Gronder', 'u'), ('褒める', 'ほめる', 'Féliciter, louer', 'ru'),
 ('頼る', 'たよる', 'Compter sur', 'u'), ('許す', 'ゆるす', 'Pardonner, autoriser', 'u'), ('認める', 'みとめる', 'Admettre, reconnaître', 'ru'), ('疑う', 'うたがう', 'Douter, soupçonner', 'u'),
 ('願う', 'ねがう', 'Souhaiter', 'u'), ('祈る', 'いのる', 'Prier, espérer', 'u'), ('怖がる', 'こわがる', 'Avoir peur', 'u'), ('悲しむ', 'かなしむ', 'Être triste', 'u'),
 ('悩む', 'なやむ', 'Se tracasser, hésiter', 'u'), ('出会う', 'であう', 'Rencontrer (par hasard)', 'u'), ('別れる', 'わかれる', 'Se séparer, se quitter', 'ru'), ('付き合う', 'つきあう', 'Sortir avec, fréquenter', 'u'),
 ('尋ねる', 'たずねる', 'Demander (une question)', 'ru'), ('知らせる', 'しらせる', 'Informer', 'ru'), ('伝わる', 'つたわる', 'Se transmettre', 'u'), ('話し合う', 'はなしあう', 'Discuter ensemble', 'u'),
 ('叫ぶ', 'さけぶ', 'Crier', 'u'), ('黙る', 'だまる', 'Se taire', 'u'), ('眺める', 'ながめる', 'Contempler', 'ru'), ('盗む', 'ぬすむ', 'Voler (dérober)', 'u'),
 ('騙す', 'だます', 'Tromper', 'u'), ('逃げる', 'にげる', 'S’enfuir', 'ru'), ('追う', 'おう', 'Poursuivre', 'u'), ('追いかける', 'おいかける', 'Courir après', 'ru'),
 ('捕まえる', 'つかまえる', 'Attraper', 'ru'), ('守る', 'まもる', 'Protéger, respecter', 'u'), ('助ける', 'たすける', 'Sauver, aider', 'ru'), ('避ける', 'さける', 'Éviter', 'ru'),
 ('防ぐ', 'ふせぐ', 'Empêcher, prévenir', 'u'),
]
_NEW['Nature et phénomènes'] = [
 ('鳴る', 'なる', 'Sonner, retentir', 'u'), ('鳴く', 'なく', 'Crier (animal)', 'u'), ('光る', 'ひかる', 'Briller', 'u'), ('燃える', 'もえる', 'Brûler', 'ru'),
 ('燃やす', 'もやす', 'Brûler (transitif)', 'u'), ('溶ける', 'とける', 'Fondre', 'ru'), ('沸く', 'わく', 'Bouillir', 'u'), ('沸かす', 'わかす', 'Faire bouillir', 'u'),
 ('凍る', 'こおる', 'Geler', 'u'), ('積もる', 'つもる', 'S’accumuler (neige)', 'u'), ('流れる', 'ながれる', 'Couler, s’écouler', 'ru'), ('流す', 'ながす', 'Faire couler, évacuer', 'u'),
 ('浮かぶ', 'うかぶ', 'Flotter', 'u'), ('沈む', 'しずむ', 'Couler, se coucher (soleil)', 'u'), ('消える', 'きえる', 'Disparaître, s’éteindre', 'ru'), ('現れる', 'あらわれる', 'Apparaître', 'ru'),
 ('揺れる', 'ゆれる', 'Trembler, osciller', 'ru'), ('震える', 'ふるえる', 'Trembler (de froid, de peur)', 'ru'),
]
_have = {r[0] for rows in V.values() for r in rows} | {r[0] for r in SURU}
_dup = []
_front = {}
for _t, _rows in _NEW.items():
    _keep = []
    for r in _rows:
        if r[0] in _have: _dup.append(r[0]); continue
        _have.add(r[0]); _keep.append(r)
    _front[_t] = _keep
if _dup: print('verbes déjà présents (ignorés):', _dup)
_base = dict(V); V.clear()
V['Verbes de base essentiels'] = _front.pop('Verbes de base essentiels')
V.update(_base); V.update(_front)

def verbs_blocks():
    bl = [P('Tableau de référence : pour chaque verbe, son groupe, sa forme en て et sa forme négative simple (ない). Les verbes sont rangés par thème. Ces verbes forment la rubrique « Verbes du quotidien » du quiz vocabulaire.'),
          N('Pièges : 帰る, 入る, 走る, 切る, 知る, 要る, 減る ressemblent à des verbes du groupe 2 (en いる/える) mais sont du groupe 1. 行く fait 行って (et non 行いて). 開ける/開く, 始める/始まる, 変える/変わる : le premier est transitif (on fait l’action), le second intransitif (ça se produit).')]
    for theme, rows in V.items():
        bl.append(H(theme)); bl.append(kanji_table(rows, _extra, verb=True))
    bl.append(H('Nom + する (verbes composés)'))
    bl.append(P('Beaucoup de verbes se forment en ajoutant する à un nom. Ils se conjuguent tous comme する : しない, して, します, した…'))
    rows = [(k, ka, fr, 'suru') for k, ka, fr in SURU]
    bl.append(kanji_table(rows, _extra, verb=True))
    return bl

# ───────────────── LIEUX ─────────────────
LIEUX = [
 ('駅', 'えき', 'Gare, station'), ('空港', 'くうこう', 'Aéroport'), ('港', 'みなと', 'Port'), ('バス停', 'バスてい', 'Arrêt de bus'), ('交番', 'こうばん', 'Poste de police de quartier'),
 ('警察署', 'けいさつしょ', 'Commissariat'), ('郵便局', 'ゆうびんきょく', 'Bureau de poste'), ('銀行', 'ぎんこう', 'Banque'), ('病院', 'びょういん', 'Hôpital'), ('薬局', 'やっきょく', 'Pharmacie'),
 ('大使館', 'たいしかん', 'Ambassade'), ('市役所', 'しやくしょ', 'Mairie'), ('図書館', 'としょかん', 'Bibliothèque'), ('博物館', 'はくぶつかん', 'Musée (histoire, sciences)'), ('美術館', 'びじゅつかん', 'Musée d’art'),
 ('動物園', 'どうぶつえん', 'Zoo'), ('水族館', 'すいぞくかん', 'Aquarium'), ('公園', 'こうえん', 'Parc'), ('神社', 'じんじゃ', 'Sanctuaire shintoïste'), ('お寺', 'おてら', 'Temple bouddhiste'),
 ('城', 'しろ', 'Château'), ('映画館', 'えいがかん', 'Cinéma'), ('学校', 'がっこう', 'École'), ('大学', 'だいがく', 'Université'), ('会社', 'かいしゃ', 'Entreprise'),
 ('市場', 'いちば', 'Marché'), ('商店街', 'しょうてんがい', 'Rue commerçante'), ('デパート', 'デパート', 'Grand magasin'), ('スーパー', 'スーパー', 'Supermarché'), ('コンビニ', 'コンビニ', 'Supérette ouverte 24 h'),
 ('本屋', 'ほんや', 'Librairie'), ('花屋', 'はなや', 'Fleuriste'), ('パン屋', 'パンや', 'Boulangerie'), ('魚屋', 'さかなや', 'Poissonnerie'), ('八百屋', 'やおや', 'Marchand de légumes'),
 ('喫茶店', 'きっさてん', 'Café, salon de thé'), ('居酒屋', 'いざかや', 'Izakaya (bar à tapas)'), ('食堂', 'しょくどう', 'Cantine, restaurant simple'), ('旅館', 'りょかん', 'Auberge traditionnelle'), ('民宿', 'みんしゅく', 'Chambre d’hôtes'),
 ('駐車場', 'ちゅうしゃじょう', 'Parking'), ('お手洗い', 'おてあらい', 'Toilettes'), ('交差点', 'こうさてん', 'Carrefour'), ('信号', 'しんごう', 'Feu de signalisation'), ('橋', 'はし', 'Pont'),
 ('道', 'みち', 'Chemin, rue'), ('角', 'かど', 'Coin (de rue)'), ('横断歩道', 'おうだんほどう', 'Passage piéton'), ('出口', 'でぐち', 'Sortie'), ('入口', 'いりぐち', 'Entrée'),
]
MAISON = [
 ('家', 'いえ', 'Maison (bâtiment)'), ('部屋', 'へや', 'Pièce, chambre'), ('玄関', 'げんかん', 'Entrée (où l’on enlève ses chaussures)'), ('台所', 'だいどころ', 'Cuisine'), ('風呂', 'ふろ', 'Bain, salle de bain'),
 ('寝室', 'しんしつ', 'Chambre à coucher'), ('窓', 'まど', 'Fenêtre'), ('ドア', 'ドア', 'Porte'), ('階段', 'かいだん', 'Escalier'), ('鍵', 'かぎ', 'Clé'),
 ('机', 'つくえ', 'Bureau, table de travail'), ('椅子', 'いす', 'Chaise'), ('ベッド', 'ベッド', 'Lit'), ('布団', 'ふとん', 'Futon'), ('電気', 'でんき', 'Électricité, lumière'),
 ('冷蔵庫', 'れいぞうこ', 'Réfrigérateur'), ('電子レンジ', 'でんしレンジ', 'Four à micro-ondes'), ('洗濯機', 'せんたくき', 'Machine à laver'), ('エアコン', 'エアコン', 'Climatisation'), ('テレビ', 'テレビ', 'Télévision'),
 ('携帯', 'けいたい', 'Téléphone portable'), ('充電器', 'じゅうでんき', 'Chargeur'), ('財布', 'さいふ', 'Portefeuille'), ('傘', 'かさ', 'Parapluie'), ('鞄', 'かばん', 'Sac'),
 ('時計', 'とけい', 'Montre, horloge'), ('眼鏡', 'めがね', 'Lunettes'), ('新聞', 'しんぶん', 'Journal'), ('手紙', 'てがみ', 'Lettre'), ('荷物', 'にもつ', 'Bagages'),
 ('タオル', 'タオル', 'Serviette'), ('石鹸', 'せっけん', 'Savon'), ('歯ブラシ', 'はブラシ', 'Brosse à dents'), ('薬', 'くすり', 'Médicament'), ('ゴミ', 'ゴミ', 'Déchets, poubelle'),
]
FUKU = [
 ('服', 'ふく', 'Vêtements'), ('洋服', 'ようふく', 'Vêtements occidentaux'), ('着物', 'きもの', 'Kimono'), ('浴衣', 'ゆかた', 'Yukata (kimono d’été)'), ('シャツ', 'シャツ', 'Chemise'),
 ('Tシャツ', 'Tシャツ', 'T-shirt'), ('セーター', 'セーター', 'Pull'), ('上着', 'うわぎ', 'Veste'), ('コート', 'コート', 'Manteau'), ('ズボン', 'ズボン', 'Pantalon'),
 ('スカート', 'スカート', 'Jupe'), ('ワンピース', 'ワンピース', 'Robe'), ('下着', 'したぎ', 'Sous-vêtements'), ('靴', 'くつ', 'Chaussures'), ('靴下', 'くつした', 'Chaussettes'),
 ('帽子', 'ぼうし', 'Chapeau, casquette'), ('手袋', 'てぶくろ', 'Gants'), ('マフラー', 'マフラー', 'Écharpe'), ('ネクタイ', 'ネクタイ', 'Cravate'), ('サイズ', 'サイズ', 'Taille'),
 ('大きい', 'おおきい', 'Grand'), ('小さい', 'ちいさい', 'Petit'), ('長い', 'ながい', 'Long'), ('短い', 'みじかい', 'Court'), ('きつい', 'きつい', 'Serré'), ('ゆるい', 'ゆるい', 'Large, lâche'),
]
TENKI = [
 ('天気', 'てんき', 'Météo, temps'), ('晴れ', 'はれ', 'Beau temps'), ('曇り', 'くもり', 'Nuageux'), ('雨', 'あめ', 'Pluie'), ('雪', 'ゆき', 'Neige'),
 ('風', 'かぜ', 'Vent'), ('台風', 'たいふう', 'Typhon'), ('雷', 'かみなり', 'Tonnerre, orage'), ('霧', 'きり', 'Brouillard'), ('地震', 'じしん', 'Tremblement de terre'),
 ('津波', 'つなみ', 'Tsunami'), ('暑い', 'あつい', 'Chaud (météo)'), ('寒い', 'さむい', 'Froid (météo)'), ('涼しい', 'すずしい', 'Frais, agréable'), ('暖かい', 'あたたかい', 'Doux, tiède'),
 ('蒸し暑い', 'むしあつい', 'Chaud et humide'), ('湿度', 'しつど', 'Humidité'), ('気温', 'きおん', 'Température de l’air'), ('梅雨', 'つゆ', 'Saison des pluies'), ('天気予報', 'てんきよほう', 'Prévisions météo'),
 ('春', 'はる', 'Printemps'), ('夏', 'なつ', 'Été'), ('秋', 'あき', 'Automne'), ('冬', 'ふゆ', 'Hiver'), ('桜', 'さくら', 'Cerisier en fleurs'),
 ('紅葉', 'こうよう', 'Feuilles d’automne rougies'), ('花火', 'はなび', 'Feu d’artifice'), ('空', 'そら', 'Ciel'), ('太陽', 'たいよう', 'Soleil'), ('月', 'つき', 'Lune'),
]
KIMOCHI = [
 ('嬉しい', 'うれしい', 'Heureux, content'), ('楽しい', 'たのしい', 'Amusant, agréable'), ('悲しい', 'かなしい', 'Triste'), ('寂しい', 'さびしい', 'Seul, nostalgique'), ('怖い', 'こわい', 'Effrayant, avoir peur'),
 ('恥ずかしい', 'はずかしい', 'Gêné, honteux'), ('心配', 'しんぱい', 'Inquiétude'), ('緊張', 'きんちょう', 'Tension, trac'), ('安心', 'あんしん', 'Soulagement, tranquillité'), ('残念', 'ざんねん', 'Dommage'),
 ('眠い', 'ねむい', 'Avoir sommeil'), ('疲れた', 'つかれた', 'Fatigué'), ('お腹がすいた', 'おなかがすいた', 'Avoir faim'), ('喉が渇いた', 'のどがかわいた', 'Avoir soif'), ('忙しい', 'いそがしい', 'Occupé'),
 ('暇', 'ひま', 'Libre, désœuvré'), ('退屈', 'たいくつ', 'Ennuyeux, s’ennuyer'), ('面白い', 'おもしろい', 'Intéressant, drôle'), ('つまらない', 'つまらない', 'Ennuyeux, sans intérêt'), ('びっくり', 'びっくり', 'Surpris'),
 ('怒る', 'おこる', 'Se fâcher'), ('好き', 'すき', 'Aimer'), ('嫌い', 'きらい', 'Ne pas aimer'), ('大好き', 'だいすき', 'Adorer'), ('大丈夫', 'だいじょうぶ', 'Ça va, pas de problème'),
]
SHOJO = [
 ('症状', 'しょうじょう', 'Symptôme'), ('熱', 'ねつ', 'Fièvre'), ('咳', 'せき', 'Toux'), ('くしゃみ', 'くしゃみ', 'Éternuement'), ('鼻水', 'はなみず', 'Nez qui coule'),
 ('頭痛', 'ずつう', 'Mal de tête'), ('腹痛', 'ふくつう', 'Mal de ventre'), ('吐き気', 'はきけ', 'Nausée'), ('下痢', 'げり', 'Diarrhée'), ('めまい', 'めまい', 'Vertige'),
 ('風邪', 'かぜ', 'Rhume'), ('インフルエンザ', 'インフルエンザ', 'Grippe'), ('怪我', 'けが', 'Blessure'), ('骨折', 'こっせつ', 'Fracture'), ('捻挫', 'ねんざ', 'Entorse'),
 ('やけど', 'やけど', 'Brûlure'), ('アレルギー', 'アレルギー', 'Allergie'), ('医者', 'いしゃ', 'Médecin'), ('看護師', 'かんごし', 'Infirmier, infirmière'), ('救急車', 'きゅうきゅうしゃ', 'Ambulance'),
 ('保険', 'ほけん', 'Assurance'), ('診察', 'しんさつ', 'Consultation'), ('処方箋', 'しょほうせん', 'Ordonnance'), ('痛み止め', 'いたみどめ', 'Antidouleur'), ('目薬', 'めぐすり', 'Collyre'),
 ('絆創膏', 'ばんそうこう', 'Pansement'), ('マスク', 'マスク', 'Masque'), ('体温', 'たいおん', 'Température corporelle'), ('入院', 'にゅういん', 'Hospitalisation'), ('具合が悪い', 'ぐあいがわるい', 'Ne pas se sentir bien'),
]
KUNI = [
 ('日本', 'にほん', 'Japon'), ('フランス', 'フランス', 'France'), ('アメリカ', 'アメリカ', 'États-Unis'), ('イギリス', 'イギリス', 'Royaume-Uni'), ('ドイツ', 'ドイツ', 'Allemagne'),
 ('イタリア', 'イタリア', 'Italie'), ('スペイン', 'スペイン', 'Espagne'), ('ベルギー', 'ベルギー', 'Belgique'), ('スイス', 'スイス', 'Suisse'), ('カナダ', 'カナダ', 'Canada'),
 ('中国', 'ちゅうごく', 'Chine'), ('韓国', 'かんこく', 'Corée du Sud'), ('台湾', 'たいわん', 'Taïwan'), ('タイ', 'タイ', 'Thaïlande'), ('インド', 'インド', 'Inde'),
 ('ブラジル', 'ブラジル', 'Brésil'), ('オーストラリア', 'オーストラリア', 'Australie'), ('ヨーロッパ', 'ヨーロッパ', 'Europe'), ('アジア', 'アジア', 'Asie'), ('外国', 'がいこく', 'Pays étranger'),
 ('外国人', 'がいこくじん', 'Étranger'), ('日本人', 'にほんじん', 'Japonais(e)'), ('フランス人', 'フランスじん', 'Français(e)'), ('日本語', 'にほんご', 'Langue japonaise'), ('フランス語', 'フランスご', 'Langue française'),
 ('英語', 'えいご', 'Anglais'), ('中国語', 'ちゅうごくご', 'Chinois'), ('韓国語', 'かんこくご', 'Coréen'),
]
SHUMI = [
 ('趣味', 'しゅみ', 'Passe-temps'), ('音楽', 'おんがく', 'Musique'), ('映画', 'えいが', 'Film'), ('本', 'ほん', 'Livre'), ('漫画', 'まんが', 'Manga'),
 ('アニメ', 'アニメ', 'Animé'), ('ゲーム', 'ゲーム', 'Jeu vidéo'), ('写真', 'しゃしん', 'Photo'), ('料理', 'りょうり', 'Cuisine (action de cuisiner)'), ('旅行', 'りょこう', 'Voyage'),
 ('登山', 'とざん', 'Alpinisme, randonnée'), ('釣り', 'つり', 'Pêche'), ('キャンプ', 'キャンプ', 'Camping'), ('スポーツ', 'スポーツ', 'Sport'), ('サッカー', 'サッカー', 'Football'),
 ('野球', 'やきゅう', 'Baseball'), ('テニス', 'テニス', 'Tennis'), ('水泳', 'すいえい', 'Natation'), ('スキー', 'スキー', 'Ski'), ('柔道', 'じゅうどう', 'Judo'),
 ('剣道', 'けんどう', 'Kendo'), ('相撲', 'すもう', 'Sumo'), ('ギター', 'ギター', 'Guitare'), ('ピアノ', 'ピアノ', 'Piano'), ('カラオケ', 'カラオケ', 'Karaoké'),
 ('温泉', 'おんせん', 'Source chaude'), ('買い物', 'かいもの', 'Courses, shopping'), ('散歩', 'さんぽ', 'Promenade'), ('読書', 'どくしょ', 'Lecture (loisir)'), ('園芸', 'えんげい', 'Jardinage'),
]
ONOMA = [
 ('わくわく', 'わくわく', 'Être excité, impatient', 'わくわくします。'), ('どきどき', 'どきどき', 'Cœur qui bat (nervosité, émotion)', '緊張してどきどきします。'), ('ぺらぺら', 'ぺらぺら', 'Parler couramment une langue', '日本語がぺらぺらです。'),
 ('ぐっすり', 'ぐっすり', 'Dormir profondément', 'ぐっすり寝ました。'), ('ゆっくり', 'ゆっくり', 'Lentement, tranquillement', 'ゆっくり休んでください。'), ('のんびり', 'のんびり', 'Se détendre, sans se presser', 'のんびり過ごします。'),
 ('ぴったり', 'ぴったり', 'Parfaitement ajusté', 'このサイズはぴったりです。'), ('たっぷり', 'たっぷり', 'En abondance', 'たっぷり食べました。'), ('しっかり', 'しっかり', 'Solidement, correctement', 'しっかり勉強します。'),
 ('はっきり', 'はっきり', 'Clairement', 'はっきり言ってください。'), ('そろそろ', 'そろそろ', 'Bientôt, il est temps de', 'そろそろ行きましょう。'), ('だんだん', 'だんだん', 'Peu à peu', 'だんだん寒くなります。'),
 ('どんどん', 'どんどん', 'De plus en plus vite, sans cesse', 'どんどん増えています。'), ('ぺこぺこ', 'ぺこぺこ', 'Avoir très faim', 'お腹がぺこぺこです。'), ('ふわふわ', 'ふわふわ', 'Moelleux, léger', 'ふわふわのパンケーキです。'),
 ('さくさく', 'さくさく', 'Croustillant (tempura, biscuit)', 'さくさくの天ぷらです。'), ('もちもち', 'もちもち', 'Moelleux et élastique (mochi)', 'もちもちした食感です。'), ('とろとろ', 'とろとろ', 'Fondant, onctueux', 'とろとろの卵です。'),
 ('ぴりぴり', 'ぴりぴり', 'Piquant (épicé)', '少しぴりぴりします。'), ('ごろごろ', 'ごろごろ', 'Paresser; gronder (tonnerre)', '家でごろごろします。'), ('ぐるぐる', 'ぐるぐる', 'Tourner en rond', '頭がぐるぐるします。'),
 ('ざあざあ', 'ざあざあ', 'Pleuvoir à verse', '雨がざあざあ降っています。'), ('ぽつぽつ', 'ぽつぽつ', 'Quelques gouttes', '雨がぽつぽつ降ってきました。'), ('ぎりぎり', 'ぎりぎり', 'De justesse', 'ぎりぎり間に合いました。'),
 ('うろうろ', 'うろうろ', 'Rôder, errer', '駅の前でうろうろしました。'), ('ちゃんと', 'ちゃんと', 'Correctement, comme il faut', 'ちゃんと説明します。'), ('きっと', 'きっと', 'Sûrement', 'きっと大丈夫です。'),
 ('ずっと', 'ずっと', 'Tout le temps; de loin', 'ずっと待っています。'), ('ちょうど', 'ちょうど', 'Juste, exactement', 'ちょうどいいです。'), ('やっと', 'やっと', 'Enfin, après effort', 'やっと着きました。'),
 ('うっかり', 'うっかり', 'Par inattention', 'うっかり忘れました。'), ('そっくり', 'そっくり', 'Tout à fait semblable', '父にそっくりです。'), ('にこにこ', 'にこにこ', 'Sourire (aimablement)', 'にこにこ笑っています。'),
]
def onoma_table():
    rows = [[k, ka, ro(ka), fr, ex] for k, ka, fr, ex in ONOMA]
    return T(['Kanji', 'Kana', 'Rōmaji', 'Sens', 'Exemple'], rows, jp=(0, 1, 4), ro=(2,))

HYOSHIKI = [
 ('出口', 'でぐち', 'Sortie'), ('入口', 'いりぐち', 'Entrée'), ('非常口', 'ひじょうぐち', 'Sortie de secours'), ('禁煙', 'きんえん', 'Interdit de fumer'), ('喫煙', 'きつえん', 'Zone fumeurs'),
 ('禁止', 'きんし', 'Interdit'), ('立入禁止', 'たちいりきんし', 'Accès interdit'), ('撮影禁止', 'さつえいきんし', 'Photos interdites'), ('土足禁止', 'どそくきんし', 'Interdit de garder ses chaussures'), ('駐車禁止', 'ちゅうしゃきんし', 'Stationnement interdit'),
 ('営業中', 'えいぎょうちゅう', 'Ouvert (en service)'), ('準備中', 'じゅんびちゅう', 'Fermé (en préparation)'), ('営業時間', 'えいぎょうじかん', 'Horaires d’ouverture'), ('定休日', 'ていきゅうび', 'Jour de fermeture régulier'), ('休業', 'きゅうぎょう', 'Fermé (congé)'),
 ('本日休業', 'ほんじつきゅうぎょう', 'Fermé aujourd’hui'), ('貸切', 'かしきり', 'Privatisé, réservé'), ('満席', 'まんせき', 'Complet (places assises)'), ('空席', 'くうせき', 'Place libre'), ('満室', 'まんしつ', 'Complet (chambres)'),
 ('空室', 'くうしつ', 'Chambre disponible'), ('使用中', 'しようちゅう', 'Occupé (toilettes)'), ('故障中', 'こしょうちゅう', 'En panne'), ('工事中', 'こうじちゅう', 'En travaux'), ('通行止め', 'つうこうどめ', 'Route barrée'),
 ('押す', 'おす', 'Pousser'), ('引く', 'ひく', 'Tirer'), ('危険', 'きけん', 'Danger'), ('注意', 'ちゅうい', 'Attention'), ('徐行', 'じょこう', 'Ralentir'),
 ('無料', 'むりょう', 'Gratuit'), ('有料', 'ゆうりょう', 'Payant'), ('割引', 'わりびき', 'Réduction'), ('税込', 'ぜいこみ', 'TTC'), ('税抜', 'ぜいぬき', 'Hors taxe'),
 ('免税', 'めんぜい', 'Détaxe'), ('現金', 'げんきん', 'Espèces'), ('お釣り', 'おつり', 'Monnaie rendue'), ('領収書', 'りょうしゅうしょ', 'Reçu, facture'), ('現金のみ', 'げんきんのみ', 'Espèces uniquement'),
 ('受付', 'うけつけ', 'Accueil, réception'), ('案内所', 'あんないじょ', 'Bureau d’information'), ('会計', 'かいけい', 'Caisse, addition'), ('予約', 'よやく', 'Réservation'), ('要予約', 'ようよやく', 'Réservation obligatoire'),
 ('開館', 'かいかん', 'Ouverture (musée, salle)'), ('閉館', 'へいかん', 'Fermeture (musée, salle)'), ('開店', 'かいてん', 'Ouverture (magasin)'), ('閉店', 'へいてん', 'Fermeture (magasin)'), ('本日', 'ほんじつ', 'Aujourd’hui (formel)'),
 ('切符売り場', 'きっぷうりば', 'Guichet de billets'), ('改札口', 'かいさつぐち', 'Portillons'), ('乗り場', 'のりば', 'Quai, point d’embarquement'), ('乗り換え', 'のりかえ', 'Correspondance'), ('各駅停車', 'かくえきていしゃ', 'Omnibus (s’arrête partout)'),
 ('急行', 'きゅうこう', 'Express'), ('特急', 'とっきゅう', 'Express limité'), ('快速', 'かいそく', 'Rapide'), ('指定席', 'していせき', 'Place réservée'), ('自由席', 'じゆうせき', 'Place non réservée'),
 ('片道', 'かたみち', 'Aller simple'), ('往復', 'おうふく', 'Aller-retour'), ('大人', 'おとな', 'Adulte'), ('子供', 'こども', 'Enfant'), ('男', 'おとこ', 'Homme (toilettes)'),
 ('女', 'おんな', 'Femme (toilettes)'), ('お手洗い', 'おてあらい', 'Toilettes'), ('非常ボタン', 'ひじょうボタン', 'Bouton d’urgence'), ('手荷物', 'てにもつ', 'Bagages à main'), ('忘れ物', 'わすれもの', 'Objets perdus'),
]

# ───────────────── NOMBRES, PRIX ─────────────────
BIGN = [
 ('百', 'ひゃく', '100'), ('二百', 'にひゃく', '200'), ('三百', 'さんびゃく', '300'), ('四百', 'よんひゃく', '400'), ('五百', 'ごひゃく', '500'),
 ('六百', 'ろっぴゃく', '600'), ('七百', 'ななひゃく', '700'), ('八百', 'はっぴゃく', '800'), ('九百', 'きゅうひゃく', '900'),
 ('千', 'せん', '1 000'), ('二千', 'にせん', '2 000'), ('三千', 'さんぜん', '3 000'), ('四千', 'よんせん', '4 000'), ('五千', 'ごせん', '5 000'),
 ('六千', 'ろくせん', '6 000'), ('七千', 'ななせん', '7 000'), ('八千', 'はっせん', '8 000'), ('九千', 'きゅうせん', '9 000'),
 ('一万', 'いちまん', '10 000'), ('二万', 'にまん', '20 000'), ('五万', 'ごまん', '50 000'), ('十万', 'じゅうまん', '100 000'), ('百万', 'ひゃくまん', '1 000 000'),
 ('千万', 'せんまん', '10 000 000'), ('一億', 'いちおく', '100 000 000'),
]
MIX = [
 ('三万五千', 'さんまんごせん', '35 000'), ('十二万', 'じゅうにまん', '120 000'), ('二十五万', 'にじゅうごまん', '250 000'), ('百五十万', 'ひゃくごじゅうまん', '1 500 000'),
 ('二百万', 'にひゃくまん', '2 000 000'), ('一万二千五百', 'いちまんにせんごひゃく', '12 500'), ('八万八千', 'はちまんはっせん', '88 000'), ('千二百', 'せんにひゃく', '1 200'),
]
PRIX = [
 ('百八円', 'ひゃくはちえん', '108 ¥'), ('三百三十円', 'さんびゃくさんじゅうえん', '330 ¥'), ('四百八十円', 'よんひゃくはちじゅうえん', '480 ¥'), ('六百五十円', 'ろっぴゃくごじゅうえん', '650 ¥'),
 ('八百円', 'はっぴゃくえん', '800 ¥'), ('千八十円', 'せんはちじゅうえん', '1 080 ¥'), ('千五百円', 'せんごひゃくえん', '1 500 ¥'), ('三千三百円', 'さんぜんさんびゃくえん', '3 300 ¥'),
 ('四千八百円', 'よんせんはっぴゃくえん', '4 800 ¥'), ('六千円', 'ろくせんえん', '6 000 ¥'), ('八千八百円', 'はっせんはっぴゃくえん', '8 800 ¥'), ('九千八百円', 'きゅうせんはっぴゃくえん', '9 800 ¥'),
 ('一万二千円', 'いちまんにせんえん', '12 000 ¥'), ('二万五千円', 'にまんごせんえん', '25 000 ¥'), ('五万八千円', 'ごまんはっせんえん', '58 000 ¥'), ('十万円', 'じゅうまんえん', '100 000 ¥'),
]
def num_blocks():
    br = lambda rows: [[k, ka, ro(ka), fr] for k, ka, fr in rows]
    return [
     P('Le japonais ne compte pas par milliers mais par万 (まん) = 10 000. On pense donc en « 10 000 » : 10万 = 100 000, 100万 = 1 000 000, 1 000万 = 10 millions, puis 億 (おく) = 100 millions. Pour lire un grand nombre, regroupe-le par 4 chiffres en partant de la droite : 3 5000 → 3万 5千.'),
     T(['Kanji', 'Kana', 'Rōmaji', 'Sens'], br(BIGN), jp=(0, 1), ro=(2,)),
     N('Les lectures irrégulières à connaître par cœur : 300 さんびゃく, 600 ろっぴゃく, 800 はっぴゃく, 3 000 さんぜん, 8 000 はっせん. 10 000 se dit toujours いちまん (jamais まん seul), alors que 100 et 1 000 se disent seuls : ひゃく, せん.'),
     H('Nombres composés'),
     T(['Kanji', 'Kana', 'Rōmaji', 'Sens'], br(MIX), jp=(0, 1), ro=(2,)),
     H('Âge, année, pourcentage, téléphone'),
     T(['En français', '日本語', 'Rōmaji'], [
       ['20 ans', '二十歳（はたち）', 'Hatachi'], ['1 an (âge)', '一歳', 'Issai'], ['8 ans', '八歳', 'Hassai'], ['10 ans', '十歳', 'Jussai'], ['Quel âge ?', '何歳ですか。', 'Nansai desu ka.'],
       ['L’année 2027', '二千二十七年', 'Nisen nijūnana-nen'], ['100 %', '百パーセント', 'Hyaku pāsento'], ['50 %', '五十パーセント', 'Gojuppāsento'], ['La moitié', '半分', 'Hanbun'],
       ['Un tiers', '三分の一', 'Sanbun no ichi'], ['Numéro de téléphone', '電話番号', 'Denwa bangō'], ['0 (zéro)', 'ゼロ / れい', 'Zero / Rei'],
       ['Dans un numéro, le trait d’union se dit « no »', '〇九〇の一二三四の五六七八', 'Zero-kyū-zero no ichi-ni-san-yon no go-roku-nana-hachi'],
     ], jp=(1,), ro=(2,)),
     N('Pour les numéros de téléphone, on lit chiffre par chiffre : 4 se dit よん ou し (mais pas dans les numéros, on préfère よん) et 7 se dit なな. 0 se dit ゼロ ou れい.'),
    ]
def prix_blocks():
    return [
     P('Ce que tu entends et lis à la caisse, au guichet et dans les distributeurs. Le yen s’écrit 円 et se prononce えん ; le prix précède toujours 円 : 三百円 = 300 yens.'),
     T(['Prix', '日本語', 'Rōmaji'], [[fr, k, ro(ka)] for k, ka, fr in PRIX], jp=(1,), ro=(2,)),
     N('Pièges : 4 yens se dit よえん (et non よんえん), 7 yens ななえん ou しちえん. Les centaines et les milliers irréguliers (300, 600, 800, 3 000, 8 000) se retrouvent partout dans les prix.'),
     H('Pièces et billets'),
     T(['En français', '日本語', 'Rōmaji'], [
       ['Pièce de 1 yen', '一円玉', 'Ichien-dama'], ['Pièce de 5 yens', '五円玉', 'Goen-dama'], ['Pièce de 10 yens', '十円玉', 'Jūen-dama'], ['Pièce de 50 yens', '五十円玉', 'Gojūen-dama'],
       ['Pièce de 100 yens', '百円玉', 'Hyakuen-dama'], ['Pièce de 500 yens', '五百円玉', 'Gohyakuen-dama'], ['Billet de 1 000 yens', '千円札', 'Sen’en-satsu'],
       ['Billet de 5 000 yens', '五千円札', 'Gosen’en-satsu'], ['Billet de 10 000 yens', '一万円札', 'Ichiman’en-satsu'], ['Petite monnaie', '小銭', 'Kozeni'],
     ], jp=(1,), ro=(2,)),
     H('À la caisse et au change'),
     T(['En français', '日本語', 'Rōmaji'], [
       ['C’est combien ?', 'いくらですか。', 'Ikura desu ka.'], ['C’est combien en tout ?', '全部でいくらですか。', 'Zenbu de ikura desu ka.'], ['C’est TTC ?', '税込みですか。', 'Zeikomi desu ka.'],
       ['Je paie en espèces', '現金で払います。', 'Genkin de haraimasu.'], ['Puis-je payer par carte ?', 'カードで払えますか。', 'Kādo de haraemasu ka.'], ['Espèces uniquement', '現金のみです。', 'Genkin nomi desu.'],
       ['Le reçu, s’il vous plaît', 'レシートをお願いします。', 'Reshīto o onegaishimasu.'], ['Une facture au nom de …, s’il vous plaît', '領収書をお願いします。', 'Ryōshūsho o onegaishimasu.'],
       ['Pouvez-vous faire un prix ?', 'もう少し安くなりますか。', 'Mō sukoshi yasuku narimasu ka.'], ['Je voudrais changer de l’argent', '両替したいです。', 'Ryōgae shitai desu.'],
       ['Où est le distributeur ?', 'ATMはどこですか。', 'ēchīemu wa doko desu ka.'], ['Je voudrais recharger ma carte', 'チャージをお願いします。', 'Chāji o onegaishimasu.'],
       ['C’est un peu cher', 'ちょっと高いです。', 'Chotto takai desu.'], ['C’est bon marché', '安いですね。', 'Yasui desu ne.'],
     ], jp=(1,), ro=(2,)),
    ]

# ───────────────── GRAMMAIRE : donner/recevoir, probabilité ─────────────────
def _g3(rows): return T(['日本語', 'Sens', 'Pourquoi'], rows, jp=(0,), ro=())
JUJU = [
 P('Le japonais distingue qui donne et qui reçoit, et choisit le verbe selon le point de vue. Trois verbes de base, qui se retrouvent aussi après un verbe en て pour dire « faire un service ».'),
 _g3([
  ['私は友達にプレゼントをあげました。', 'J’ai offert un cadeau à un ami.', 'あげる : je donne à quelqu’un d’autre.'],
  ['友達が私にプレゼントをくれました。', 'Un ami m’a offert un cadeau.', 'くれる : quelqu’un me donne à moi (ou à mon cercle).'],
  ['私は友達にプレゼントをもらいました。', 'J’ai reçu un cadeau d’un ami.', 'もらう : je reçois ; on peut aussi dire 友達からもらう.'],
  ['母が妹に本をあげました。', 'Ma mère a donné un livre à ma sœur.', 'Entre tiers : あげる (si aucun des deux n’est « moi »).'],
 ]),
 N('くれる s’emploie seulement quand le receveur est moi ou mon entourage proche. Si tu donnes toi-même, c’est あげる. Pour quelqu’un de très respecté : さしあげる (humble, donner) et いただく (humble, recevoir) ; くださる (honorifique, donner).'),
 H('Après un verbe en て : rendre un service'),
 _g3([
  ['手伝ってあげます。', 'Je t’aide (je te rends service).', 'てあげる : je fais pour toi. Peut sembler condescendant avec un supérieur.'],
  ['手伝ってくれました。', 'Il m’a aidé.', 'てくれる : quelqu’un fait pour moi.'],
  ['手伝ってもらいました。', 'Je me suis fait aider.', 'てもらう : je demande ou obtiens que quelqu’un fasse.'],
  ['写真を撮ってもらえますか。', 'Pourriez-vous me prendre en photo ?', 'てもらえますか : demande polie, très courante.'],
  ['写真を撮っていただけませんか。', 'Pourriez-vous avoir la gentillesse de me prendre en photo ?', 'ていただけませんか : encore plus poli.'],
  ['駅まで連れて行ってくれました。', 'Il m’a accompagné jusqu’à la gare.', 'Reconnaissance : くれる exprime « il l’a fait pour moi ».'],
 ]),
 N('Piège : en français on dit « j’ai demandé à ma sœur de m’aider » ; en japonais on préfère 妹に手伝ってもらいました (je me suis fait aider par ma sœur). On remercie en présentant l’aide comme un cadeau reçu.'),
]
SURYO = [
 P('Pour exprimer l’apparence, la probabilité ou le ouï-dire, plusieurs formules se ressemblent. Chacune a sa nuance : on ne peut pas les échanger librement.'),
 _g3([
  ['おいしそうです。', 'Ça a l’air bon.', 'そうです (apparence) : radical du verbe ou de l’adjectif + そう. Jugement sur ce qu’on voit.'],
  ['雨が降りそうです。', 'Il va sans doute pleuvoir.', 'Verbe : radical en ます + そう : ce qui va se produire.'],
  ['雨が降るそうです。', 'On dit qu’il va pleuvoir.', 'そうです (ouï-dire) : forme simple + そうです. Information entendue.'],
  ['誰もいないようです。', 'Il semble qu’il n’y ait personne.', 'ようです : impression fondée sur des indices observés.'],
  ['誰もいないみたいです。', 'On dirait qu’il n’y a personne.', 'みたいです : même sens que ようです, plus oral.'],
  ['彼は来ないらしいです。', 'Il paraît qu’il ne viendra pas.', 'らしい : information indirecte, rapportée ou déduite.'],
  ['日本らしい料理です。', 'C’est un plat typiquement japonais.', 'Après un nom : らしい = « typique de ».'],
  ['明日は雨でしょう。', 'Demain, il pleuvra probablement.', 'でしょう : probabilité, ton de prévision météo.'],
  ['遅れるかもしれません。', 'Je serai peut-être en retard.', 'かもしれません : possibilité (environ 30-50 %).'],
  ['もう着いているはずです。', 'Il doit déjà être arrivé.', 'はずです : déduction logique, attente fondée sur une raison.'],
  ['彼は日本人に違いありません。', 'C’est sûrement un Japonais.', 'に違いありません : forte conviction.'],
 ]),
 N('Piège : おいしそうです (« ça a l’air bon », avant de goûter) et おいしいそうです (« on dit que c’est bon ») ne se disent pas pareil. Pour いい, on dit よさそう ; pour ない, なさそう.'),
]
MSG = [
 P('Messages, SMS, LINE et e-mails : les formules courtes pour réserver, prévenir d’un retard ou confirmer. Ton poli par défaut ; entre amis on enlève です・ます.'),
 T(['En français', '日本語', 'Rōmaji'], [
  ['Merci de votre réponse', 'ご返信ありがとうございます。', 'Go-henshin arigatō gozaimasu.'],
  ['Je voudrais réserver pour deux personnes', '二名で予約をお願いしたいです。', 'Ni-mei de yoyaku o onegai shitai desu.'],
  ['Je voudrais confirmer ma réservation', '予約を確認したいです。', 'Yoyaku o kakunin shitai desu.'],
  ['Je voudrais annuler ma réservation', '予約をキャンセルしたいです。', 'Yoyaku o kyanseru shitai desu.'],
  ['Pourriez-vous répondre en anglais ?', '英語で返信していただけますか。', 'Eigo de henshin shite itadakemasu ka.'],
  ['Je vous remercie par avance (fin de message)', 'どうぞよろしくお願いいたします。', 'Dōzo yoroshiku onegai itashimasu.'],
  ['Je suis en retard', '少し遅れます。', 'Sukoshi okuremasu.'],
  ['Désolé d’être en retard', '遅れてすみません。', 'Okurete sumimasen.'],
  ['J’arrive à 7 h', '七時に着きます。', 'Shichi-ji ni tsukimasu.'],
  ['Je suis devant la gare', '駅の前にいます。', 'Eki no mae ni imasu.'],
  ['OK, compris (poli)', '了解しました。', 'Ryōkai shimashita.'],
  ['OK (entre amis)', '了解。', 'Ryōkai.'],
  ['Merci ! (entre amis)', 'ありがとう！', 'Arigatō!'],
  ['Désolé (entre amis)', 'ごめん。', 'Gomen.'],
  ['À demain', 'また明日。', 'Mata ashita.'],
  ['Bonne nuit', 'おやすみなさい。', 'Oyasumi nasai.'],
  ['Je suis bien arrivé(e)', '無事に着きました。', 'Buji ni tsukimashita.'],
  ['Fais attention à toi / Bon voyage', '気をつけてね。', 'Ki o tsukete ne.'],
 ], jp=(1,), ro=(2,)),
 N('Dans les messages, (笑) ou w signifie « lol », 草 est l’équivalent d’un rire moqueur et les stickers LINE remplacent souvent une phrase. Un message d’hôtel ou de restaurant se termine toujours par よろしくお願いします.'),
]
def _vocab_sub(title, rows, intro=None):
    bl = [P(intro)] if intro else []
    bl.append(kanji_table(rows)); return {'title': title, 'blocks': bl}

SUBS_VOCAB = [
 _vocab_sub('場所 — Lieux en ville', LIEUX, 'Les lieux qu’on cherche, qu’on demande et qu’on lit sur les panneaux.'),
 _vocab_sub('家 — Maison et objets', MAISON, 'Objets du quotidien, hébergement et affaires de voyage.'),
 _vocab_sub('服 — Vêtements', FUKU),
 _vocab_sub('天気 — Météo et saisons', TENKI),
 _vocab_sub('気持ち — Émotions et états', KIMOCHI, 'Pour dire comment tu te sens : adjectifs en い, mots en な et quelques verbes.'),
 _vocab_sub('症状 — Santé et symptômes', SHOJO, 'À compléter avec la rubrique Voyage › Urgences et santé, qui contient les phrases complètes.'),
 _vocab_sub('趣味 — Loisirs', SHUMI),
 {'title': '擬音語 — Onomatopées et adverbes expressifs', 'blocks': [P('Les mots expressifs sont partout à l’oral : ils décrivent les sons, les textures, les sensations. Les plus fréquents, avec un exemple.'), onoma_table()]},
 _vocab_sub('標識 — Panneaux et affichages', HYOSHIKI, 'À lire sans traduction : portes, magasins, gares, caisses. Les mêmes mots sont dans le quiz vocabulaire.'),
]
SUBS_TEMPS = [
 {'title': '大きな数 — Grands nombres', 'blocks': num_blocks()},
 {'title': 'お金 — Prix et argent', 'blocks': prix_blocks()},
]
EXPR_SUBS = [
 {'title': '授受 — あげる・もらう・くれる', 'blocks': JUJU},
 {'title': '推量・伝聞 — そう・よう・らしい・はず', 'blocks': SURYO},
]
KAIWA_SUBS = [{'title': 'メッセージ — SMS, LINE et e-mails', 'blocks': MSG}]
