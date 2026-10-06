import os, sys
# -*- coding: utf-8 -*-
# Compléments : adjectifs, particules, keigo, expressions, temps
import re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import T, P, N, H, DATA
import vocab_core as C2
import pykakasi
_kks = pykakasi.kakasi()
FR3 = ['En français', '日本語', 'Rōmaji']

try:
    import sudachipy as _sp
    _tok = _sp.Dictionary().create(); _mode = _sp.Tokenizer.SplitMode.C
except Exception:
    _tok = None

def _kata2hira(t):
    return ''.join(chr(ord(c) - 0x60) if 'ァ' <= c <= 'ヶ' else c for c in t)

def _ro_kana(k):
    s = ''.join(x['hepburn'] for x in _kks.convert(k))
    for a, b in (('ou', 'ō'), ('uu', 'ū'), ('oo', 'ō')): s = s.replace(a, b)
    return s

def rj(jp):
    if _tok is None: return jp
    chunks = []  # [hira, proper, punct]
    prev = ''
    for m in _tok.tokenize(jp, _mode):
        surf, p, rd = m.surface(), m.part_of_speech(), m.reading_form()
        pos = p[0]
        if pos in ('補助記号', '記号'):
            chunks.append([{'。': '.', '、': ',', '？': '?', '！': '!', '「': '“', '」': '”', '…': '...', '〜': '~'}.get(surf, surf), False, True]); prev = surf; continue
        if surf == '日本': rd = 'ニホン'
        if surf == 'は' and pos == '助詞': h = 'wa'
        elif surf == 'を': h = 'o'
        elif surf == 'へ': h = 'e'
        else: h = _kata2hira(rd if rd and rd != '*' else surf)
        attach = (pos == '助動詞' and surf not in ('です', 'だ', 'でし', 'だっ', 'でしょ', 'だろ')) or (pos == '助詞' and surf in ('て', 'で', 'ば', 'ず')) or (pos == '接尾辞' and p[1] != '名詞的')
        if surf in ('た', 'ない') : attach = True
        if surf == 'で' and pos == '助詞' and p[1] != '接続助詞': attach = False
        prop = pos == '名詞' and p[1] == '固有名詞'
        if attach and chunks and not chunks[-1][2]: chunks[-1][0] += h
        else: chunks.append([h, prop, False])
        prev = surf
    out = ''
    for h, prop, punct in chunks:
        if punct: out += h if h not in ('“',) else (' ' + h if out else h); continue
        r = h if h in ('wa', 'o', 'e') else _ro_kana(h)
        if prop: r = r[:1].upper() + r[1:]
        out += ('' if (not out or out.endswith(('“', ' '))) else ' ') + r
    return (out[:1].upper() + out[1:]).strip()

def phr(rows):
    return T(FR3, [[fr, jp, rj(jp)] for fr, jp in rows], jp=(1,), ro=(2,))

def sub(title, intro, blocks):
    bl = [P(intro)] if intro else []
    return {'title': title, 'blocks': bl + blocks}

def ktab(rows):
    return C2.kanji_table(rows)

# ───────────── ADJECTIFS EN い ─────────────
ADJ_I = {
 'Taille, forme, distance': [
  ('太い', 'ふとい', 'Gros, épais (objet long)'), ('細い', 'ほそい', 'Fin, mince'), ('厚い', 'あつい', 'Épais (livre, mur)'), ('薄い', 'うすい', 'Mince, léger (goût)'),
  ('深い', 'ふかい', 'Profond'), ('浅い', 'あさい', 'Peu profond'), ('低い', 'ひくい', 'Bas, petit (taille)'), ('近い', 'ちかい', 'Proche'),
  ('遠い', 'とおい', 'Loin'), ('多い', 'おおい', 'Nombreux, abondant'), ('少ない', 'すくない', 'Peu nombreux'), ('丸い', 'まるい', 'Rond'),
  ('細かい', 'こまかい', 'Fin, détaillé, menu'), ('激しい', 'はげしい', 'Violent, intense'), ('濃い', 'こい', 'Fort, foncé, dense'), ('偉い', 'えらい', 'Éminent, admirable'),
 ],
 'Goût, toucher et sensations': [
  ('甘い', 'あまい', 'Sucré, doux'), ('辛い', 'からい', 'Épicé, piquant'), ('苦い', 'にがい', 'Amer'), ('酸っぱい', 'すっぱい', 'Acide'),
  ('しょっぱい', 'しょっぱい', 'Salé'), ('美味しい', 'おいしい', 'Délicieux'), ('不味い', 'まずい', 'Mauvais (au goût)'), ('硬い', 'かたい', 'Dur'),
  ('柔らかい', 'やわらかい', 'Mou, tendre'), ('臭い', 'くさい', 'Qui sent mauvais'), ('温かい', 'あたたかい', 'Chaud (agréable), tiède'), ('暖かい', 'あたたかい', 'Doux (météo)'),
  ('涼しい', 'すずしい', 'Frais (agréable)'), ('蒸し暑い', 'むしあつい', 'Chaud et humide'), ('眩しい', 'まぶしい', 'Éblouissant'), ('明るい', 'あかるい', 'Clair, lumineux, gai'),
  ('暗い', 'くらい', 'Sombre, triste'), ('うるさい', 'うるさい', 'Bruyant, agaçant'), ('騒がしい', 'さわがしい', 'Bruyant, agité'), ('汚い', 'きたない', 'Sale'),
  ('痒い', 'かゆい', 'Qui démange'), ('だるい', 'だるい', 'Mou, sans énergie'), ('眠たい', 'ねむたい', 'Somnolent'), ('苦しい', 'くるしい', 'Pénible, oppressant'),
 ],
 'Jugement et qualité': [
  ('悪い', 'わるい', 'Mauvais'), ('凄い', 'すごい', 'Incroyable, formidable'), ('素晴らしい', 'すばらしい', 'Magnifique'), ('正しい', 'ただしい', 'Correct, juste'),
  ('詳しい', 'くわしい', 'Détaillé, bien informé'), ('珍しい', 'めずらしい', 'Rare, inhabituel'), ('欲しい', 'ほしい', 'Vouloir (objet)'), ('若い', 'わかい', 'Jeune'),
  ('強い', 'つよい', 'Fort'), ('弱い', 'よわい', 'Faible'), ('早い', 'はやい', 'Tôt, précoce'), ('速い', 'はやい', 'Rapide'),
  ('遅い', 'おそい', 'Lent, tardif'), ('賢い', 'かしこい', 'Intelligent, malin'), ('厳しい', 'きびしい', 'Sévère, strict'), ('面白い', 'おもしろい', 'Intéressant, drôle'),
  ('つまらない', 'つまらない', 'Ennuyeux, sans intérêt'), ('我慢強い', 'がまんづよい', 'Patient, endurant'), ('危ない', 'あぶない', 'Dangereux'), ('細長い', 'ほそながい', 'Long et étroit'), ('細かい', 'こまかい', 'Minutieux'),
  ('ずるい', 'ずるい', 'Rusé, injuste'), ('酷い', 'ひどい', 'Terrible, cruel'), ('怪しい', 'あやしい', 'Suspect'), ('忙しい', 'いそがしい', 'Occupé'),
 ],
 'Caractère et sentiments': [
  ('優しい', 'やさしい', 'Gentil, doux'), ('可愛い', 'かわいい', 'Mignon, adorable'), ('格好いい', 'かっこいい', 'Classe, beau (garçon)'), ('恥ずかしい', 'はずかしい', 'Honteux, gêné'),
  ('羨ましい', 'うらやましい', 'Envieux, enviable'), ('懐かしい', 'なつかしい', 'Nostalgique'), ('寂しい', 'さびしい', 'Seul, triste'), ('悔しい', 'くやしい', 'Frustré, rageant'),
  ('恋しい', 'こいしい', 'Qui manque (être aimé)'), ('惜しい', 'おしい', 'Dommage, regrettable'), ('辛い', 'つらい', 'Pénible, dur à vivre'), ('親しい', 'したしい', 'Proche, intime'),
  ('頼もしい', 'たのもしい', 'Fiable, rassurant'), ('たくましい', 'たくましい', 'Robuste, solide'), ('図々しい', 'ずうずうしい', 'Effronté'), ('可哀想', 'かわいそう', 'Pauvre, à plaindre'),
  ('嬉しい', 'うれしい', 'Heureux (tout de suite)'), ('楽しい', 'たのしい', 'Amusant'), ('うらやましい', 'うらやましい', 'Digne d’envie'), ('怖い', 'こわい', 'Effrayant'),
 ],
}
ADJ_NA = {
 'Qualité et valeur': [
  ('素敵', 'すてき', 'Charmant, superbe'), ('立派', 'りっぱ', 'Magnifique, remarquable'), ('派手', 'はで', 'Voyant, flashy'), ('地味', 'じみ', 'Discret, sobre'),
  ('贅沢', 'ぜいたく', 'Luxueux, dispendieux'), ('豊か', 'ゆたか', 'Riche, abondant'), ('盛ん', 'さかん', 'Florissant, actif'), ('新鮮', 'しんせん', 'Frais'),
  ('清潔', 'せいけつ', 'Propre, hygiénique'), ('不潔', 'ふけつ', 'Sale, malpropre'), ('快適', 'かいてき', 'Confortable, agréable'), ('素朴', 'そぼく', 'Simple, rustique'),
  ('適当', 'てきとう', 'Approprié, approximatif'), ('十分', 'じゅうぶん', 'Suffisant'), ('完全', 'かんぜん', 'Complet, parfait'), ('特別', 'とくべつ', 'Spécial'),
  ('普通', 'ふつう', 'Ordinaire, normal'), ('正確', 'せいかく', 'Exact, précis'), ('確か', 'たしか', 'Sûr, certain'), ('明らか', 'あきらか', 'Évident'),
 ],
 'Caractère et attitude': [
  ('真面目', 'まじめ', 'Sérieux, consciencieux'), ('正直', 'しょうじき', 'Honnête'), ('素直', 'すなお', 'Docile, franc'), ('熱心', 'ねっしん', 'Appliqué, passionné'),
  ('頑固', 'がんこ', 'Têtu'), ('器用', 'きよう', 'Habile (de ses mains)'), ('不器用', 'ぶきよう', 'Maladroit'), ('意地悪', 'いじわる', 'Méchant, taquin'),
  ('積極的', 'せっきょくてき', 'Actif, proactif'), ('消極的', 'しょうきょくてき', 'Passif, réservé'), ('わがまま', 'わがまま', 'Égoïste, capricieux'), ('のんき', 'のんき', 'Insouciant'),
  ('生意気', 'なまいき', 'Insolent'), ('冷静', 'れいせい', 'Calme, posé'), ('勤勉', 'きんべん', 'Travailleur'), 
 ],
 'États, situations et jugements': [
  ('自由', 'じゆう', 'Libre'), ('無理', 'むり', 'Impossible, excessif'), ('必要', 'ひつよう', 'Nécessaire'), ('不要', 'ふよう', 'Inutile'),
  ('簡単', 'かんたん', 'Simple, facile'), ('複雑', 'ふくざつ', 'Compliqué'), ('安全', 'あんぜん', 'Sûr, sécurisé'), ('危険', 'きけん', 'Dangereux'),
  ('健康', 'けんこう', 'En bonne santé'), ('丈夫', 'じょうぶ', 'Solide, robuste'), ('平気', 'へいき', 'Tranquille, indifférent'), ('心配', 'しんぱい', 'Inquiet'),
  ('残念', 'ざんねん', 'Dommage'), ('幸せ', 'しあわせ', 'Heureux'), ('不幸', 'ふこう', 'Malheureux'), ('楽', 'らく', 'Facile, confortable'),
  ('変', 'へん', 'Bizarre'), ('大丈夫', 'だいじょうぶ', 'Pas de souci, ça va'), ('駄目', 'だめ', 'Nul, interdit, raté'), ('無駄', 'むだ', 'Inutile, gaspillé'),
  ('自然', 'しぜん', 'Naturel'), ('不自然', 'ふしぜん', 'Peu naturel'), ('急', 'きゅう', 'Soudain, urgent'), ('確実', 'かくじつ', 'Certain, sûr'),
  ('手軽', 'てがる', 'Facile, pratique'), ('色々', 'いろいろ', 'Divers, variés'), ('様々', 'さまざま', 'Varié'), ('同じ', 'おなじ', 'Même'),
  ('別', 'べつ', 'Autre, séparé'), ('妙', 'みょう', 'Étrange'), ('孤独', 'こどく', 'Solitaire'), ('退屈', 'たいくつ', 'Ennuyeux, ennui'),
  ('嫌', 'いや', 'Désagréable, pas envie'), ('面倒', 'めんどう', 'Pénible, embêtant'), ('邪魔', 'じゃま', 'Gênant, dérangeant'), ('失礼', 'しつれい', 'Impoli, grossier'),
  ('無事', 'ぶじ', 'Sain et sauf'), ('主', 'おも', 'Principal'), ('特殊', 'とくしゅ', 'Particulier, spécial'), ('可能', 'かのう', 'Possible'),
 ],
}

def adj_subs(have):
    mine = set()
    def dedup(d):
        out = {}
        for t, rows in d.items():
            keep = []
            for r in rows:
                if r[0] in have or (r[0], r[1]) in mine: continue
                mine.add((r[0], r[1])); keep.append(r)
            if keep: out[t] = keep
        return out
    ai, an = dedup(ADJ_I), dedup(ADJ_NA)
    bi, bn = [], []
    for t, rows in ai.items(): bi += [H(t), ktab(rows)]
    for t, rows in an.items(): bn += [H(t), ktab(rows)]
    ni, nn = sum(len(v) for v in ai.values()), sum(len(v) for v in an.values())
    return [
      sub('い形容詞 — Adjectifs en い, liste étendue', f'{ni} adjectifs en い de plus, rangés par thème. Ils se conjuguent tous comme 大きい (voir « Vue d’ensemble »), sauf いい / よい.', bi),
      sub('な形容詞 — Adjectifs en な, liste étendue', f'{nn} adjectifs en な de plus. Devant un nom : forme + な (素敵な人) ; en fin de phrase : forme + だ / です.', bn),
    ]

HAVE = set(open(os.path.join(DATA, 'have_vocab.txt'), encoding='utf-8').read().split('\n'))

# ───────────── KEIGO ─────────────
KEIGO_VERBS = [
 ('いらっしゃる', 'いらっしゃる', 'Être, aller, venir (respectueux)'), ('おっしゃる', 'おっしゃる', 'Dire (respectueux)'), ('なさる', 'なさる', 'Faire (respectueux)'),
 ('召し上がる', 'めしあがる', 'Manger, boire (respectueux)'), ('ご覧になる', 'ごらんになる', 'Voir (respectueux)'), ('くださる', 'くださる', 'Donner à moi (respectueux)'),
 ('お休みになる', 'おやすみになる', 'Se reposer, dormir (respectueux)'), ('お亡くなりになる', 'おなくなりになる', 'Décéder (respectueux)'),
 ('参る', 'まいる', 'Aller, venir (humble)'), ('伺う', 'うかがう', 'Visiter, demander, écouter (humble)'), ('申す', 'もうす', 'Dire (humble)'),
 ('申し上げる', 'もうしあげる', 'Dire (très humble)'), ('いたす', 'いたす', 'Faire (humble)'), ('いただく', 'いただく', 'Manger, recevoir (humble)'),
 ('拝見する', 'はいけんする', 'Voir (humble)'), ('存じる', 'ぞんじる', 'Savoir, penser (humble)'), ('存じ上げる', 'ぞんじあげる', 'Connaître quelqu’un (humble)'),
 ('お目にかかる', 'おめにかかる', 'Rencontrer (humble)'), ('差し上げる', 'さしあげる', 'Donner (humble)'), ('承知する', 'しょうちする', 'Comprendre, accepter (humble)'),
 ('お待ちする', 'おまちする', 'Attendre (humble)'), ('お届けする', 'おとどけする', 'Livrer, apporter (humble)'), ('お持ちする', 'おもちする', 'Porter (humble)'),
 ('ございます', 'ございます', 'Il y a, c’est (très poli)'), ('おる', 'おる', 'Être (humble)'),
]
KEIGO_P1 = [
 ('Je suis à votre service (mot de bienvenue)', 'いらっしゃいませ。ご用件をお伺いします。'), ('Puis-je vous aider ?', 'いかがなさいましたか。'),
 ('Veuillez entrer', 'どうぞお入りください。'), ('Veuillez vous asseoir', 'どうぞおかけください。'), ('Merci de votre visite', 'ご来店ありがとうございます。'),
 ('Désolé de vous avoir fait attendre', 'お待たせして申し訳ございません。'), ('Je vais vérifier', '確認いたします。'), ('Un instant, je vous prie', '少々お待ちいただけますか。'),
 ('Je vous en prie / Pas de quoi', 'とんでもないです。'), ('Je comprends parfaitement', '承知いたしました。'), ('Je vais le noter', '承りました。'),
 ('Comment puis-je vous appeler ?', 'お名前をお伺いしてもよろしいですか。'), ('Quel est votre numéro de téléphone ?', 'お電話番号を教えていただけますか。'),
 ('Vos papiers, s’il vous plaît', 'パスポートを拝見してもよろしいでしょうか。'), ('Voici votre monnaie', 'お釣りでございます。'), ('Voici votre reçu', 'こちらがレシートでございます。'),
 ('Nous sommes fermés aujourd’hui', '本日は休業しております。'), ('C’est complet', '満席でございます。'), ('Nous n’en avons plus', '品切れでございます。'), ('Je regrette, c’est impossible', '申し訳ございませんが、できかねます。'),
 ('Veuillez patienter à cet endroit', 'こちらでお待ちください。'), ('Attention à la marche', 'お足元にご注意ください。'), ('Merci de votre compréhension', 'ご理解のほどお願いいたします。'),
 ('Nous vous souhaitons un bon séjour', 'どうぞごゆっくりお過ごしください。'), ('Faites attention en rentrant', 'お気をつけてお帰りください。'),
]
KEIGO_P2 = [
 ('Je vous contacte au sujet de…', '〜の件でご連絡いたしました。'), ('Pardon de vous déranger', 'お忙しいところ恐れ入ります。'), ('Je vous remercie de votre aide', 'お力添えありがとうございます。'),
 ('Merci pour votre réponse', 'ご返信ありがとうございます。'), ('Veuillez excuser mon retard', '遅くなり申し訳ございません。'), ('Je vous prie de m’excuser', 'お詫び申し上げます。'),
 ('Je vous en suis reconnaissant(e)', '感謝申し上げます。'), ('Je compte sur vous', 'よろしくお願い申し上げます。'), ('Pourriez-vous me confirmer ?', 'ご確認いただけますでしょうか。'),
 ('Merci de bien vouloir répondre', 'ご返事をお願いいたします。'), ('Je souhaiterais prendre rendez-vous', 'お会いしたいのですが、ご都合はいかがでしょうか。'),
 ('Quand seriez-vous disponible ?', 'ご都合のよろしい日時を教えてください。'), ('Je suis disponible demain', '明日でしたら大丈夫です。'), ('Je vous rappellerai', 'こちらからお電話いたします。'),
 ('Veuillez transmettre mes salutations', 'よろしくお伝えください。'), ('Je suis bien en retard dans ma réponse', 'ご連絡が遅くなりました。'),
 ('Allô, ici M. Tanaka', 'もしもし、田中と申します。'), ('Puis-je parler à M. Sato ?', '佐藤様はいらっしゃいますか。'), ('Il est absent pour le moment', 'ただいま席を外しております。'),
 ('Souhaitez-vous laisser un message ?', '伝言をお預かりしましょうか。'), ('Je rappellerai plus tard', 'また後ほどお電話いたします。'), ('Pardon, je n’ai pas entendu', 'お電話が少々遠いようです。'),
 ('C’est une erreur de numéro', '番号をお間違えのようです。'), ('Merci de votre appel', 'お電話ありがとうございました。'),
]

# ───────────── PARTICULES (suite) ─────────────
PART_X = [
 ('Si… (condition, conseil)', '時間があるなら、来てください。'), ('Quant à… (changement de sujet)', '果物なら、りんごが好きです。'), ('… et autres choses (liste libre)', '肉とか魚とか野菜を買いました。'),
 ('Chacun, à chaque fois (quantité)', '一人ずつ入ってください。'), ('… etc. (liste non exhaustive)', '本や雑誌などを読みます。'), ('Des choses comme… (dédain)', 'お酒なんか飲みません。'),
 ('C’est précisément… (insistance)', 'これこそ私が探していたものです。'), ('Même (cas extrême, négatif)', '水すら飲めませんでした。'), ('Même moi / Moi aussi (justification)', '私だって行きたいです。'),
 ('Vers (approximation de temps)', '三時ごろ来ます。'), ('En plus (raison empilée)', '安いし、おいしいし、よく行きます。'), ('Même si… (concession)', '雨が降っても、行きます。'),
 ('Tantôt… tantôt…', '朝は食べたり食べなかったりします。'), ('Au sujet de… ', '日本の文化について勉強しています。'), ('Envers, à l’égard de…', '先生に対して失礼です。'),
 ('Selon, grâce à…', '電車の遅れによって、遅刻しました。'), ('En tant que…', '観光客として来ました。'), ('Selon… (source d’info)', '天気予報によると、明日は雨です。'),
 ('Pour… (but)', '健康のために歩きます。'), ('Appelé, nommé…', '「さくら」という花が好きです。'), ('Comme, du genre… ', '日本のような国に住みたいです。'),
 ('Pendant que (durée)', '食べている間に電話が来ました。'), ('Sans… (nég.)', '何も言わずに帰りました。'), ('Dès que…', '着いたらすぐ電話します。'),
 ('Chaque… (à chaque fois)', '会うたびに話します。'), ('Que ce soit… ou…', '電車でもバスでも行けます。'), ('Tout… (entier)', '一日中雨でした。'),
 ('Au cours de… / Dans le cadre de…', '旅行中に写真を撮りました。'), ('Environ (quantité)', '千円ぐらいです。'), ('Plus… que (comparaison)', '東京は京都より大きいです。'),
 ('Le plus… (superlatif)', '日本で富士山がいちばん高いです。'), ('Aussi… que… (équivalence)', 'これは あれ ほど高くないです。'),
]

# ───────────── EXPRESSIONS ─────────────
GRAMM2 = [
 ('Je suis en train de…', '今、ご飯を食べています。'), ('C’est déjà fait / J’ai fini par…', '宿題を全部やってしまいました。'), ('Je le fais d’avance', 'ホテルを予約しておきます。'),
 ('C’est déjà écrit / préparé', '窓が開けてあります。'), ('Je viens de…', '今、起きたばかりです。'), ('Il se trouve que… (après avoir fait)', '食べたところです。'),
 ('Facile à… / Difficile à…', 'このペンは書きやすいです。'), ('Difficile à…', 'この漢字は覚えにくいです。'), ('Trop… (excès)', '食べすぎました。'),
 ('J’ai l’air de… / On dirait que…', '雨が降りそうです。'), ('Je crois que… (opinion)', '日本は面白いと思います。'), ('On dit que…', '明日は雪が降るそうです。'),
 ('Si je faisais… (hypothèse)', 'お金があれば、旅行します。'), ('Si… (quand ça arrive)', '春になると、桜が咲きます。'), ('Il faut absolument…', 'パスポートを持って行かなければなりません。'),
 ('Pas besoin de…', '急がなくてもいいです。'), ('On a le droit de…', 'ここで写真を撮ってもいいです。'), ('Il est interdit de…', 'ここで泳いではいけません。'),
 ('Je veux que tu…', '先生に来てほしいです。'), ('Je veux essayer de…', '日本料理を作ってみたいです。'), ('Je pense faire…', '来年日本へ行くつもりです。'),
 ('J’ai décidé de…', '毎日勉強することにしました。'), ('Il est prévu que…', '来月、引っ越すことになりました。'), ('J’ai l’habitude de…', '毎朝コーヒーを飲むことにしています。'),
 ('Je m’habitue à…', '日本の生活に慣れてきました。'), ('Je peux désormais…', '日本語が話せるようになりました。'), ('Autant que possible…', 'できるだけ早く来てください。'),
 ('Quand je suis revenu…', '帰ってきたら、雨が降っていました。'), ('Avant de… / Après avoir…', '寝る前に、歯を磨きます。'), ('Après avoir mangé…', '食べた後で、散歩します。'),
 ('Sans même…', '何も食べずに出かけました。'), ('Au lieu de…', 'バスの代わりに電車で行きます。'), ('Même si je… (opposition)', '勉強したのに、わかりません。'),
 ('À cause de…', '雨のせいで、遅れました。'), ('Grâce à…', 'あなたのおかげで、助かりました。'), ('Chaque fois que…', '日本に行くたびに、買い物をします。'),
]
DAILY = [
 ('Bon appétit (avant de manger)', 'いただきます。'), ('Merci pour le repas', 'ごちそうさまでした。'), ('Je pars (en quittant la maison)', 'いってきます。'),
 ('Bonne journée (à celui qui part)', 'いってらっしゃい。'), ('Je suis rentré', 'ただいま。'), ('Bon retour', 'おかえりなさい。'),
 ('Je suis désolé de partir avant vous', 'お先に失礼します。'), ('Merci pour votre travail', 'お疲れ様です。'), ('Prenez soin de vous (maladie)', 'お大事に。'),
 ('Félicitations !', 'おめでとうございます。'), ('Bonne année !', 'あけましておめでとうございます。'), ('Bon anniversaire !', 'お誕生日おめでとうございます。'),
 ('Courage ! (encouragement)', '頑張ってください。'), ('Faites de votre mieux', 'ベストを尽くしてください。'), ('Bonne chance !', '幸運を祈ります。'),
 ('Ça fait longtemps !', 'お久しぶりです。'), ('Enchanté (première rencontre)', 'はじめまして。どうぞよろしくお願いします。'), ('Excusez-moi de vous déranger', 'お邪魔します。'),
 ('Merci d’être venu', 'お越しいただきありがとうございます。'), ('Faites comme chez vous', 'どうぞごゆっくり。'), ('Je ne me suis pas bien exprimé', 'うまく言えなくてすみません。'),
 ('Bien sûr !', 'もちろんです。'), ('Évidemment', '当たり前です。'), ('Pas du tout', '全然違います。'), ('C’est ça !', 'その通りです。'),
 ('Je vous laisse faire', 'お任せします。'), ('Ça dépend', '場合によります。'), ('Ça m’est égal', 'どちらでもいいです。'),
 ('Je suis occupé en ce moment', '今ちょっと忙しいです。'), ('Bonne idée !', 'いい考えですね。'), ('Quel dommage !', '残念ですね。'),
 ('J’ai de la chance', 'ラッキーでした。'), ('Pas mal !', '悪くないですね。'), ('Je suis épuisé(e)', 'もうくたくたです。'), ('J’ai faim', 'お腹がすきました。'),
 ('J’ai soif', '喉が渇きました。'), ('J’ai sommeil', '眠いです。'), ('J’ai froid', '寒いです。'), ('J’ai chaud', '暑いです。'),
]
IDIOMS = [
 ('Sept fois tomber, huit fois se relever', '七転び八起き。'), ('Ce qui est fait est fait (aucun regret)', '後悔先に立たず。'), ('Parler est d’argent, se taire est d’or', '沈黙は金。'),
 ('Une fois par un hasard : une rencontre unique', '一期一会。'), ('Vaut mieux tard que jamais', '遅くてもやらないよりはまし。'), ('Les voyages forment la jeunesse', '可愛い子には旅をさせよ。'),
 ('À force de patience (persévérance)', '継続は力なり。'), ('Voir une fois vaut cent entendre', '百聞は一見にしかず。'), ('Tomber du ciel (très soudain)', '突然のことです。'),
 ('Un seul mot : tout est dit (en un coup)', '一石二鳥。'), ('Deux oiseaux d’un coup de pierre', '一石二鳥です。'), ('Un cœur, un esprit', '以心伝心。'),
 ('Aller doucement va loin', '急がば回れ。'), ('Le singe tombe aussi des arbres', '猿も木から落ちる。'), ('Le silence est parfois la meilleure réponse', '言わぬが花。'),
]

IDIOMS = [
 ('Sept fois à terre, huit fois debout (ne jamais abandonner)', '七転び八起き。'), ('Inutile de regretter après coup', '後悔先に立たず。'), ('Le silence est d’or', '沈黙は金。'),
 ('Une rencontre, une chance unique', '一期一会。'), ('La persévérance fait la force', '継続は力なり。'), ('Voir une fois vaut mieux que cent fois entendre', '百聞は一見にしかず。'),
 ('Faire d’une pierre deux coups', '一石二鳥。'), ('Se comprendre sans parler', '以心伝心。'), ('Mieux vaut le détour que la précipitation', '急がば回れ。'),
 ('Même le singe tombe de l’arbre (tout le monde se trompe)', '猿も木から落ちる。'), ('Autant de personnes, autant de goûts', '十人十色。'), ('Le gâteau plutôt que la fleur (l’utile avant le beau)', '花より団子。'),
 ('La pratique vaut mieux que la théorie', '習うより慣れよ。'), ('Mieux vaut prévenir que guérir', '備えあれば憂いなし。'), ('Ne jamais oublier son esprit de débutant', '初心忘るべからず。'),
 ('Les petits ruisseaux font les grandes rivières', '塵も積もれば山となる。'), ('Deux têtes valent mieux qu’une', '三人寄れば文殊の知恵。'), ('L’appréhension est pire que l’action', '案ずるより産むが易し。'),
]
GRAMM2 = [(a, b.replace('これは あれ ほど', 'これはあれほど')) for a, b in GRAMM2]
GRAMM2 = [(('Je viens de… (à l’instant)' if a.startswith('Il se trouve') else a), b) for a, b in GRAMM2]

def extra_subs():
    adj = adj_subs(set(HAVE))
    return {
      '形容詞': adj,
      '助詞': [sub('その他 — Autres particules et locutions', 'Particules secondaires et locutions de liaison qui reviennent tout le temps : なら, とか, ずつ, など, について, によって…', [phr(PART_X)])],
      '敬語': [
        sub('尊敬語・謙譲語 — Verbes honorifiques et humbles, suite', 'Les verbes spéciaux de keigo au-delà des plus courants. 尊敬語 = respectueux (élève l’autre), 謙譲語 = humble (abaisse soi-même).', [C2.kanji_table(KEIGO_VERBS)]),
        sub('サービス・接客 — Vocabulaire de service, suite', 'Phrases entendues dans les magasins, hôtels, restaurants et administrations.', [phr(KEIGO_P1)]),
        sub('ビジネス・電話 — Affaires, e-mails et téléphone', 'Formules formelles pour écrire, téléphoner ou prendre rendez-vous.', [phr(KEIGO_P2)]),
      ],
      '表現': [
        sub('文型・続き — Structures de phrase, suite', 'Structures grammaticales du quotidien en phrases complètes : N5 à N3.', [phr(GRAMM2)]),
        sub('日常 — Expressions du quotidien', 'Formules toutes faites et réactions : à dire à voix haute, telles quelles.', [phr(DAILY)]),
        sub('ことわざ — Proverbes et dictons', 'Les proverbes japonais les plus connus (四字熟語 et phrases).', [phr(IDIOMS)]),
      ],
    }

# Traductions complètes (pour que chaque question de quiz ait une seule bonne réponse)
PART_X = [
 ('Si tu as le temps, viens. (なら)', '時間があるなら、来てください。'), ('Pour les fruits, j’aime les pommes. (なら)', '果物なら、りんごが好きです。'), ('J’ai acheté de la viande, du poisson, des légumes… (とか)', '肉とか魚とか野菜を買いました。'),
 ('Entrez une personne à la fois. (ずつ)', '一人ずつ入ってください。'), ('Je lis des livres, des magazines, etc. (など)', '本や雑誌などを読みます。'), ('Moi, l’alcool ou ce genre de chose, je n’en bois pas. (なんか)', 'お酒なんか飲みません。'),
 ('C’est justement ce que je cherchais. (こそ)', 'これこそ私が探していたものです。'), ('Je n’ai même pas pu boire de l’eau. (すら)', '水すら飲めませんでした。'), ('Moi aussi, je veux y aller ! (だって)', '私だって行きたいです。'),
 ('Je viens vers trois heures. (ごろ)', '三時ごろ来ます。'), ('C’est bon marché, c’est bon, alors j’y vais souvent. (し)', '安いし、おいしいし、よく行きます。'), ('Même s’il pleut, j’y vais. (ても)', '雨が降っても、行きます。'),
 ('Le matin, je mange ou je ne mange pas, selon les jours. (たり)', '朝は食べたり食べなかったりします。'), ('J’étudie la culture japonaise. (について)', '日本の文化について勉強しています。'), ('C’est impoli envers le professeur. (に対して)', '先生に対して失礼です。'),
 ('J’ai été en retard à cause du retard du train. (によって)', '電車の遅れによって、遅刻しました。'), ('Je suis venu en tant que touriste. (として)', '観光客として来ました。'), ('Selon la météo, il pleuvra demain. (によると)', '天気予報によると、明日は雨です。'),
 ('Je marche pour ma santé. (のために)', '健康のために歩きます。'), ('J’aime la fleur appelée « sakura ». (という)', '「さくら」という花が好きです。'), ('Je voudrais vivre dans un pays comme le Japon. (ような)', '日本のような国に住みたいです。'),
 ('Pendant que je mangeais, j’ai eu un appel. (間に)', '食べている間に電話が来ました。'), ('Il est rentré sans rien dire. (ずに)', '何も言わずに帰りました。'), ('Dès que tu arrives, appelle-moi. (たらすぐ)', '着いたらすぐ電話します。'),
 ('Chaque fois qu’on se voit, on parle. (たびに)', '会うたびに話します。'), ('On peut y aller en train ou en bus. (でも)', '電車でもバスでも行けます。'), ('Il a plu toute la journée. (中)', '一日中雨でした。'),
 ('J’ai pris des photos pendant le voyage. (中に)', '旅行中に写真を撮りました。'), ('C’est environ mille yens. (ぐらい)', '千円ぐらいです。'), ('Tōkyō est plus grand que Kyōto. (より)', '東京は京都より大きいです。'),
 ('Le mont Fuji est la plus haute montagne du Japon. (いちばん)', '日本で富士山がいちばん高いです。'), ('Ce n’est pas aussi cher que ça. (ほど)', 'これはあれほど高くないです。'),
]
GRAMM2 = [
 ('Je suis en train de manger. (ている)', '今、ご飯を食べています。'), ('J’ai fini tous mes devoirs. (てしまう)', '宿題を全部やってしまいました。'), ('Je réserve l’hôtel à l’avance. (ておく)', 'ホテルを予約しておきます。'),
 ('La fenêtre est ouverte (quelqu’un l’a ouverte). (てある)', '窓が開けてあります。'), ('Je viens de me réveiller. (たばかり)', '今、起きたばかりです。'), ('Je viens de manger. (たところ)', '食べたところです。'),
 ('Ce stylo est facile à écrire. (やすい)', 'このペンは書きやすいです。'), ('Ce kanji est difficile à retenir. (にくい)', 'この漢字は覚えにくいです。'), ('J’ai trop mangé. (すぎる)', '食べすぎました。'),
 ('On dirait qu’il va pleuvoir. (そう)', '雨が降りそうです。'), ('Je trouve que le Japon est intéressant. (と思う)', '日本は面白いと思います。'), ('On dit qu’il neigera demain. (そうだ)', '明日は雪が降るそうです。'),
 ('Si j’avais de l’argent, je voyagerais. (ば)', 'お金があれば、旅行します。'), ('Quand le printemps arrive, les cerisiers fleurissent. (と)', '春になると、桜が咲きます。'), ('Il faut apporter son passeport. (なければならない)', 'パスポートを持って行かなければなりません。'),
 ('Pas besoin de se dépêcher. (なくてもいい)', '急がなくてもいいです。'), ('On a le droit de prendre des photos ici. (てもいい)', 'ここで写真を撮ってもいいです。'), ('Il est interdit de nager ici. (てはいけない)', 'ここで泳いではいけません。'),
 ('Je voudrais que le professeur vienne. (てほしい)', '先生に来てほしいです。'), ('Je voudrais essayer de faire de la cuisine japonaise. (てみる)', '日本料理を作ってみたいです。'), ('J’ai l’intention d’aller au Japon l’année prochaine. (つもり)', '来年日本へ行くつもりです。'),
 ('J’ai décidé d’étudier tous les jours. (ことにする)', '毎日勉強することにしました。'), ('Il a été décidé que je déménage le mois prochain. (ことになる)', '来月、引っ越すことになりました。'), ('Je fais en sorte de boire du café chaque matin. (ことにしている)', '毎朝コーヒーを飲むことにしています。'),
 ('Je me suis habitué à la vie au Japon. (てきた)', '日本の生活に慣れてきました。'), ('Je peux maintenant parler japonais. (ようになる)', '日本語が話せるようになりました。'), ('Venez le plus tôt possible. (できるだけ)', 'できるだけ早く来てください。'),
 ('En rentrant, il pleuvait. (たら)', '帰ってきたら、雨が降っていました。'), ('Avant de dormir, je me brosse les dents. (前に)', '寝る前に、歯を磨きます。'), ('Après avoir mangé, je me promène. (た後で)', '食べた後で、散歩します。'),
 ('Il est sorti sans rien manger. (ずに)', '何も食べずに出かけました。'), ('J’y vais en train plutôt qu’en bus. (の代わりに)', 'バスの代わりに電車で行きます。'), ('J’ai étudié, mais je ne comprends pas. (のに)', '勉強したのに、わかりません。'),
 ('Je suis en retard à cause de la pluie. (せい)', '雨のせいで、遅れました。'), ('Grâce à vous, j’ai été sauvé. (おかげ)', 'あなたのおかげで、助かりました。'), ('Chaque fois que je vais au Japon, je fais du shopping. (たびに)', '日本に行くたびに、買い物をします。'),
]
