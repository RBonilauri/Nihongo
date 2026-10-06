import os, sys
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
# -*- coding: utf-8 -*-
# Contenu des nouvelles rubriques. Colonnes: dict(headers, rows, jp=[indices japonais], ro=[indices romaji])

def T(headers, rows, jp=(1,), ro=(2,)):
    return {'t': 'table', 'headers': headers, 'rows': rows, 'jp': list(jp), 'ro': list(ro)}
def P(text): return {'t': 'p', 'text': text}
def N(text): return {'t': 'note', 'text': text}
def H(text): return {'t': 'h', 'text': text}

FR3 = ['En français', '日本語', 'Rōmaji']

SECTIONS = []

# ───────────────────────── VOYAGE ─────────────────────────
SECTIONS.append({
 'id': 'voyage', 'jp': '旅行', 'label': 'Voyage', 'replace': None,
 'intro': 'Phrases de survie pour le Japon, classées par situation. La colonne française vient en premier : cache le reste et essaie de produire la phrase à voix haute.',
 'subs': [
  {'title': '自己紹介 — Se présenter', 'blocks': [
    T(FR3, [
     ['Enchanté(e) de vous rencontrer', 'はじめまして。どうぞよろしくお願いします。', 'Hajimemashite. Dōzo yoroshiku onegaishimasu.'],
     ['Je m’appelle … (poli)', 'わたしは…です。', 'Watashi wa … desu.'],
     ['Je m’appelle … (très formel)', '…と申します。', '… to mōshimasu.'],
     ['Je suis français(e)', 'フランス人です。', 'Furansujin desu.'],
     ['Je viens de France', 'フランスから来ました。', 'Furansu kara kimashita.'],
     ['J’habite à Paris', 'パリに住んでいます。', 'Pari ni sunde imasu.'],
     ['Je suis ingénieur', 'エンジニアです。', 'Enjinia desu.'],
     ['Je suis venu(e) en voyage', '旅行で来ました。', 'Ryokō de kimashita.'],
     ['C’est la première fois que je viens au Japon', '日本は初めてです。', 'Nihon wa hajimete desu.'],
     ['J’étudie le japonais', '日本語を勉強しています。', 'Nihongo o benkyō shite imasu.'],
     ['Je parle un peu japonais', '日本語を少し話せます。', 'Nihongo o sukoshi hanasemasu.'],
     ['Comment allez-vous ?', 'お元気ですか。', 'O-genki desu ka.'],
     ['Excusez-moi / Pardon / Merci (selon le contexte)', 'すみません。', 'Sumimasen.'],
     ['Merci beaucoup', 'ありがとうございます。', 'Arigatō gozaimasu.'],
     ['Je suis désolé(e)', 'ごめんなさい。', 'Gomen nasai.'],
    ]),
    N('すみません sert à tout : s’excuser, attirer l’attention d’un serveur, remercier quelqu’un qui s’est donné de la peine. C’est le mot le plus utile à connaître.'),
  ]},
  {'title': 'レストラン — Au restaurant', 'blocks': [
    T(FR3, [
     ['Deux personnes', '二人です。', 'Futari desu.'],
     ['Le menu, s’il vous plaît', 'メニューをお願いします。', 'Menyū o onegaishimasu.'],
     ['Qu’est-ce que vous recommandez ?', 'おすすめは何ですか。', 'Osusume wa nan desu ka.'],
     ['Je prends ceci', 'これをください。', 'Kore o kudasai.'],
     ['Pareil pour moi', '同じものをお願いします。', 'Onaji mono o onegaishimasu.'],
     ['De l’eau, s’il vous plaît', 'お水をお願いします。', 'O-mizu o onegaishimasu.'],
     ['Une bière pression, s’il vous plaît', '生ビールをお願いします。', 'Nama bīru o onegaishimasu.'],
     ['Y a-t-il quelque chose de non épicé ?', '辛くないものはありますか。', 'Karakunai mono wa arimasu ka.'],
     ['Je suis végétarien(ne)', 'ベジタリアンです。', 'Bejitarian desu.'],
     ['Je ne mange pas de porc', '豚肉は食べられません。', 'Butaniku wa taberaremasen.'],
     ['J’ai une allergie à …', '…のアレルギーがあります。', '… no arerugī ga arimasu.'],
     ['Y a-t-il du porc dedans ?', 'これは豚肉が入っていますか。', 'Kore wa butaniku ga haitte imasu ka.'],
     ['À emporter', '持ち帰りでお願いします。', 'Mochikaeri de onegaishimasu.'],
     ['C’était délicieux (en partant)', 'ごちそうさまでした。', 'Gochisōsama deshita.'],
     ['L’addition, s’il vous plaît', 'お会計をお願いします。', 'O-kaikei o onegaishimasu.'],
     ['On paie séparément', '別々でお願いします。', 'Betsubetsu de onegaishimasu.'],
     ['Peut-on payer par carte ?', 'カードで払えますか。', 'Kādo de haraemasu ka.'],
    ]),
    N('Avant de manger on dit いただきます (itadakimasu), après ごちそうさまでした. Pas de pourboire au Japon. Dans beaucoup de restaurants on appelle le serveur avec すみません ou un bouton sur la table.'),
  ]},
  {'title': '交通 — Transports', 'blocks': [
    T(FR3, [
     ['Où est la gare ?', '駅はどこですか。', 'Eki wa doko desu ka.'],
     ['Où sont les toilettes ?', 'トイレはどこですか。', 'Toire wa doko desu ka.'],
     ['Ce train va à Kyōto ?', 'この電車は京都に行きますか。', 'Kono densha wa Kyōto ni ikimasu ka.'],
     ['C’est quel quai pour … ?', '…は何番線ですか。', '… wa nan-ban-sen desu ka.'],
     ['Un billet pour Ōsaka, s’il vous plaît', '大阪まで一枚お願いします。', 'Ōsaka made ichimai onegaishimasu.'],
     ['Le prochain train part à quelle heure ?', '次の電車は何時ですか。', 'Tsugi no densha wa nanji desu ka.'],
     ['Combien de temps ça prend ?', 'どのくらいかかりますか。', 'Dono kurai kakarimasu ka.'],
     ['Où faut-il changer ?', 'どこで乗り換えますか。', 'Doko de norikaemasu ka.'],
     ['Je voudrais recharger ma carte (IC)', 'チャージをお願いします。', 'Chājī o onegaishimasu.'],
     ['Jusqu’ici, s’il vous plaît (taxi, adresse montrée)', 'ここまでお願いします。', 'Koko made onegaishimasu.'],
     ['Je suis perdu(e)', '道に迷いました。', 'Michi ni mayoimashita.'],
     ['Pouvez-vous me montrer sur la carte ?', '地図で教えてください。', 'Chizu de oshiete kudasai.'],
    ]),
    H('Indiquer le chemin'),
    T(['En français', '日本語', 'Rōmaji'], [
     ['tout droit', 'まっすぐ', 'massugu'],
     ['à droite / à gauche', '右 / 左', 'migi / hidari'],
     ['tourner', '曲がる', 'magaru'],
     ['près / loin', '近い / 遠い', 'chikai / tōi'],
     ['à côté de', '隣', 'tonari'],
     ['en face de', '向かい', 'mukai'],
     ['devant / derrière', '前 / 後ろ', 'mae / ushiro'],
     ['Allez tout droit, puis tournez à droite.', 'まっすぐ行って、右に曲がってください。', 'Massugu itte, migi ni magatte kudasai.'],
    ]),
    H('Mots à reconnaître en gare'),
    T(['En français', '日本語', 'Rōmaji'], [
     ['sortie / entrée', '出口 / 入口', 'deguchi / iriguchi'],
     ['portique', '改札', 'kaisatsu'],
     ['quai / point d’embarquement', '乗り場', 'noriba'],
     ['à destination de …', '…行き', '… yuki'],
     ['dernier train', '終電', 'shūden'],
     ['omnibus (s’arrête partout)', '各駅停車', 'kakueki-teisha'],
     ['rapide', '快速', 'kaisoku'],
     ['express limité', '特急', 'tokkyū'],
     ['Shinkansen', '新幹線', 'Shinkansen'],
    ]),
  ]},
  {'title': 'ホテル — Hébergement', 'blocks': [
    T(FR3, [
     ['J’ai une réservation au nom de …', '…の名前で予約しています。', '… no namae de yoyaku shite imasu.'],
     ['Le check-in, s’il vous plaît', 'チェックインをお願いします。', 'Chekkuin o onegaishimasu.'],
     ['Le check-out est à quelle heure ?', 'チェックアウトは何時ですか。', 'Chekkuauto wa nanji desu ka.'],
     ['Pouvez-vous garder mes bagages ?', '荷物を預かってもらえますか。', 'Nimotsu o azukatte moraemasu ka.'],
     ['Quel est le mot de passe du Wi-Fi ?', 'Wi-Fiのパスワードを教えてください。', 'Wai-fai no pasuwādo o oshiete kudasai.'],
     ['Le petit-déjeuner, c’est à partir de quelle heure ?', '朝食は何時からですか。', 'Chōshoku wa nanji kara desu ka.'],
     ['La climatisation ne marche pas', 'エアコンが動きません。', 'Eakon ga ugokimasen.'],
     ['Il n’y a pas d’eau chaude', 'お湯が出ません。', 'Oyu ga demasen.'],
     ['Une serviette de plus, s’il vous plaît', 'タオルをもう一枚お願いします。', 'Taoru o mō ichimai onegaishimasu.'],
     ['Pouvez-vous appeler un taxi ?', 'タクシーを呼んでもらえますか。', 'Takushī o yonde moraemasu ka.'],
     ['Je voudrais rester une nuit de plus', 'もう一泊したいです。', 'Mō ippaku shitai desu.'],
    ]),
  ]},
  {'title': '買い物 — Achats et prix', 'blocks': [
    T(FR3, [
     ['Combien ça coûte ?', 'いくらですか。', 'Ikura desu ka.'],
     ['C’est un peu cher', 'ちょっと高いです。', 'Chotto takai desu.'],
     ['Je regarde seulement', '見ているだけです。', 'Mite iru dake desu.'],
     ['Puis-je l’essayer ?', '試着してもいいですか。', 'Shichaku shite mo ii desu ka.'],
     ['Avez-vous une taille plus grande ?', 'もっと大きいサイズはありますか。', 'Motto ōkii saizu wa arimasu ka.'],
     ['Je prends celui-ci', 'これにします。', 'Kore ni shimasu.'],
     ['Je n’ai pas besoin de sac', '袋はいりません。', 'Fukuro wa irimasen.'],
     ['Pouvez-vous l’emballer comme cadeau ?', 'プレゼント用に包んでもらえますか。', 'Purezento-yō ni tsutsunde moraemasu ka.'],
     ['Peut-on payer par carte ?', 'カードは使えますか。', 'Kādo wa tsukaemasu ka.'],
     ['Est-ce qu’on peut avoir la détaxe ?', '免税できますか。', 'Menzei dekimasu ka.'],
     ['Le reçu, s’il vous plaît', 'レシートをお願いします。', 'Reshīto o onegaishimasu.'],
    ]),
    H('Lire un prix : les irrégularités'),
    T(['Montant', '日本語', 'Rōmaji'], [
     ['100 ¥', '百円', 'hyaku-en'],
     ['300 ¥', '三百円', 'sanbyaku-en'],
     ['600 ¥', '六百円', 'roppyaku-en'],
     ['800 ¥', '八百円', 'happyaku-en'],
     ['1 000 ¥', '千円', 'sen-en'],
     ['3 000 ¥', '三千円', 'sanzen-en'],
     ['8 000 ¥', '八千円', 'hassen-en'],
     ['10 000 ¥', '一万円', 'ichiman-en'],
     ['100 000 ¥', '十万円', 'jūman-en'],
     ['4 ¥ / 7 ¥ / 9 ¥', '四円 / 七円 / 九円', 'yo-en / nana-en / kyū-en'],
    ]),
    N('À retenir : 百 devient びゃく à 300 (さんびゃく), ぴゃく à 600 et 800 (ろっぴゃく, はっぴゃく). 千 devient ぜん à 3000 (さんぜん) et prend une consonne double à 8000 (はっせん). 万 ne change pas, mais 一万 garde toujours いち. Les montants à 4, 7 et 9 se lisent よ, なな, きゅう.'),
  ]},
  {'title': '緊急 — Urgences et santé', 'blocks': [
    T(FR3, [
     ['Au secours !', '助けて！', 'Tasukete!'],
     ['Appelez la police, s’il vous plaît', '警察を呼んでください。', 'Keisatsu o yonde kudasai.'],
     ['Appelez une ambulance, s’il vous plaît', '救急車を呼んでください。', 'Kyūkyūsha o yonde kudasai.'],
     ['Je ne me sens pas bien', '気分が悪いです。', 'Kibun ga warui desu.'],
     ['J’ai mal à la tête', '頭が痛いです。', 'Atama ga itai desu.'],
     ['J’ai mal au ventre', 'お腹が痛いです。', 'Onaka ga itai desu.'],
     ['J’ai de la fièvre', '熱があります。', 'Netsu ga arimasu.'],
     ['Je voudrais aller à l’hôpital', '病院に行きたいです。', 'Byōin ni ikitai desu.'],
     ['Où est la pharmacie ?', '薬局はどこですか。', 'Yakkyoku wa doko desu ka.'],
     ['J’ai perdu mon passeport', 'パスポートをなくしました。', 'Pasupōto o nakushimashita.'],
     ['On m’a volé mon sac', 'かばんを盗まれました。', 'Kaban o nusumaremashita.'],
     ['J’ai oublié mon portefeuille dans le train', '電車に財布を忘れました。', 'Densha ni saifu o wasuremashita.'],
     ['Où est l’abri d’évacuation ?', '避難所はどこですか。', 'Hinanjo wa doko desu ka.'],
    ]),
    N('Numéros d’urgence : 110 pour la police, 119 pour les pompiers et l’ambulance. Pour un séisme, suis les consignes sur place et évite les ascenseurs.'),
  ]},
  {'title': '困ったとき — Se faire comprendre', 'blocks': [
    T(FR3, [
     ['Pouvez-vous répéter, s’il vous plaît ?', 'もう一度お願いします。', 'Mō ichido onegaishimasu.'],
     ['Plus lentement, s’il vous plaît', 'もう少しゆっくりお願いします。', 'Mō sukoshi yukkuri onegaishimasu.'],
     ['Je ne comprends pas', 'わかりません。', 'Wakarimasen.'],
     ['Parlez-vous anglais ?', '英語を話せますか。', 'Eigo o hanasemasu ka.'],
     ['Comment dit-on … en japonais ?', '…は日本語で何と言いますか。', '… wa Nihongo de nan to iimasu ka.'],
     ['Que veut dire … ?', '…はどういう意味ですか。', '… wa dō iu imi desu ka.'],
     ['Pouvez-vous l’écrire ?', '書いてもらえますか。', 'Kaite moraemasu ka.'],
     ['Je cherche …', '…を探しています。', '… o sagashite imasu.'],
     ['Pouvez-vous m’aider ?', '手伝ってもらえますか。', 'Tetsudatte moraemasu ka.'],
     ['Non merci / Ça ira', '大丈夫です。', 'Daijōbu desu.'],
    ]),
    N('大丈夫です peut signifier « tout va bien » ou « non merci » selon le contexte. Pour refuser clairement, ajoute un geste de la main ou dis いりません.'),
  ]},
 ]})

# ───────────────────────── KEIGO ─────────────────────────
SECTIONS.append({
 'id': 'keigo', 'jp': '敬語', 'label': 'Keigo', 'replace': 'Keigo',
 'intro': 'Langue de politesse. En voyage, tu as surtout besoin de la reconnaître (magasins, restaurants, annonces). Pour parler, です・ます et お願いします suffisent largement.',
 'subs': [
  {'title': '三つの丁寧さ — Les 3 niveaux', 'blocks': [
    T(['Niveau', 'Rôle', 'Exemple avec « manger »'], [
     ['丁寧語 teineigo (poli)', 'Ton poli neutre, avec des inconnus. です・ます.', '食べます'],
     ['尊敬語 sonkeigo (honorifique)', 'Élève la personne dont on parle : client, supérieur, interlocuteur.', '召し上がります'],
     ['謙譲語 kenjōgo (humble)', 'Abaisse sa propre action quand elle concerne l’autre.', 'いただきます'],
    ], jp=(2,), ro=()),
    N('Règle simple : sonkeigo pour les actions de l’autre, kenjōgo pour les siennes. On n’emploie jamais le sonkeigo pour soi-même.'),
  ]},
  {'title': '特別な動詞 — Verbes spéciaux', 'blocks': [
    T(['Verbe neutre', '尊敬語 (autre)', '謙譲語 (moi)'], [
     ['いる (être)', 'いらっしゃる', 'おる'],
     ['行く (aller)', 'いらっしゃる', '参る / 伺う'],
     ['来る (venir)', 'いらっしゃる / お越しになる', '参る'],
     ['言う (dire)', 'おっしゃる', '申す / 申し上げる'],
     ['する (faire)', 'なさる', 'いたす'],
     ['食べる / 飲む', '召し上がる', 'いただく'],
     ['見る (voir)', 'ご覧になる', '拝見する'],
     ['知っている (savoir)', 'ご存じ', '存じている'],
     ['聞く (demander)', 'お聞きになる', '伺う'],
     ['会う (rencontrer)', 'お会いになる', 'お目にかかる'],
     ['あげる (donner)', '—', 'さしあげる'],
     ['くれる (donner à moi)', 'くださる', '—'],
     ['もらう (recevoir)', '—', 'いただく'],
    ], jp=(1, 2), ro=()),
    N('伺う (うかがう) veut dire « rendre visite » ou « demander » ; 参る (まいる) « aller / venir » côté humble. Dans une boutique, tu entendras souvent いらっしゃいませ (bienvenue) : c’est le sonkeigo de いらっしゃる.'),
  ]},
  {'title': 'お〜になる / お〜する — Formules générales', 'blocks': [
    T(['Forme', 'Structure', 'Exemple', 'Sens'], [
     ['Honorifique', 'お + base ます + になる', 'お読みになる', 'lire (autre)'],
     ['Honorifique (nom en する)', 'ご + nom + になる', 'ご利用になる', 'utiliser (autre)'],
     ['Humble', 'お + base ます + する', 'お持ちします', 'je porte / j’apporte'],
     ['Humble (nom en する)', 'ご + nom + する', 'ご案内します', 'je vous guide'],
     ['Demande polie', 'お + base ます + ください', 'お待ちください', 'veuillez attendre'],
     ['Demande polie (nom)', 'ご + nom + ください', 'ご確認ください', 'veuillez vérifier'],
    ], jp=(1, 2), ro=()),
    N('お s’emploie surtout avec les mots d’origine japonaise, ご avec les mots d’origine chinoise (ご案内, ご連絡). Il existe des exceptions, donc retiens les expressions courantes plutôt que la règle.'),
  ]},
  {'title': 'サービスの言葉 — Ce que tu vas entendre', 'blocks': [
    T(['Expression', '日本語', 'Rōmaji'], [
     ['Bienvenue', 'いらっしゃいませ', 'Irasshaimase'],
     ['Combien de personnes ?', '何名様ですか', 'Nan-mei-sama desu ka'],
     ['Par ici, je vous en prie', 'こちらへどうぞ', 'Kochira e dōzo'],
     ['Veuillez patienter un instant', '少々お待ちください', 'Shōshō omachi kudasai'],
     ['Merci d’avoir attendu', 'お待たせしました', 'Omatase shimashita'],
     ['Très bien (je comprends)', 'かしこまりました', 'Kashikomarimashita'],
     ['Avez-vous choisi ?', 'ご注文はお決まりですか', 'Go-chūmon wa okimari desu ka'],
     ['Ce sera tout ?', '以上でよろしいですか', 'Ijō de yoroshii desu ka'],
     ['Cela fait … yens', '…円になります', '… en ni narimasu'],
     ['Merci (à la fin)', 'ありがとうございました', 'Arigatō gozaimashita'],
     ['Revenez nous voir', 'またお越しくださいませ', 'Mata okoshi kudasaimase'],
     ['Excusez-moi (entrer, partir, déranger)', '失礼いたします', 'Shitsurei itashimasu'],
     ['Je suis confus(e) (merci / pardon)', '恐れ入ります', 'Osoreirimasu'],
     ['Toutes mes excuses', '申し訳ございません', 'Mōshiwake gozaimasen'],
    ]),
  ]},
  {'title': '旅行者のための敬語 — Ce que tu peux dire', 'blocks': [
    T(['En français', '日本語', 'Rōmaji'], [
     ['S’il vous plaît / Je vous remercie d’avance', 'お願いします / よろしくお願いします', 'Onegaishimasu / Yoroshiku onegaishimasu'],
     ['Pourrais-je avoir … ?', '…をいただけますか。', '… o itadakemasu ka.'],
     ['Puis-je … ? (poli)', '…てもよろしいですか。', '… te mo yoroshii desu ka.'],
     ['Pourriez-vous m’expliquer … ?', '…を教えていただけませんか。', '… o oshiete itadakemasen ka.'],
     ['Excusez-moi de partir avant vous', 'お先に失礼します', 'Osaki ni shitsurei shimasu'],
     ['Désolé de vous déranger', 'お手数をおかけします', 'O-tesū o okake shimasu'],
     ['Merci pour votre aide', 'ありがとうございます', 'Arigatō gozaimasu'],
    ]),
  ]},
 ]})

# ───────────────────────── PRONONCIATION ─────────────────────────
SECTIONS.append({
 'id': 'hatsuon', 'jp': '発音', 'label': 'Prononciation', 'replace': None,
 'intro': 'La base de l’oral. Pour un francophone, les trois priorités sont : la durée des voyelles, les consonnes doubles (っ), puis seulement l’accent de hauteur.',
 'subs': [
  {'title': '母音 — Les 5 voyelles', 'blocks': [
    T(['Kana', 'Rōmaji', 'Approximation française', 'Piège'], [
     ['あ', 'a', '« a » de papa', 'Bouche bien ouverte, toujours la même'],
     ['い', 'i', '« i » de midi', 'Sans glisser vers « ii »'],
     ['う', 'u', '« ou » écrasé', 'Lèvres non arrondies, plus relâché que « ou »'],
     ['え', 'e', '« é » ouvert', 'Ne glisse pas en « eille »'],
     ['お', 'o', '« o » fermé', 'Ne devient pas « au » ni « ô » diphtongué'],
    ], jp=(0,), ro=(1,)),
    N('Chaque voyelle reste pure et ne bouge pas pendant la prononciation, contrairement à l’anglais et au français qui diphtonguent souvent.'),
  ]},
  {'title': '子音 — Consonnes pièges', 'blocks': [
    T(['Son', 'Kana', 'Comment le dire', 'Erreur fréquente'], [
     ['r', 'ら り る れ ろ', 'Un seul petit coup de langue derrière les dents du haut, entre r, l et d', 'Rouler le r ou dire un « l » anglais'],
     ['fu', 'ふ', 'Souffle léger entre les deux lèvres, entre « f » et « h »', 'Dire un « f » français avec les dents'],
     ['tsu', 'つ', '« ts » + u', 'Dire « tou » ou « sou »'],
     ['shi', 'し', 'Comme « chi » en français', 'Dire « si »'],
     ['chi', 'ち', 'Comme « tchi »', 'Dire « chi »'],
     ['ji', 'じ', 'Comme « dji »', 'Dire « ji » à la française'],
     ['g', 'が行', 'Toujours dur (g de gare)', 'Dire « j » devant e/i'],
     ['hi', 'ひ', 'Souffle plus palatal, proche du « ch » allemand de ich', 'Dire « chi »'],
    ], jp=(1,), ro=(0,)),
    H('Le ん se prononce selon ce qui suit'),
    T(['Devant', 'Son', 'Exemple'], [
     ['b, m, p', 'm', 'さんぽ (sampo)'],
     ['k, g', 'ng', 'ぎんこう (ginkō)'],
     ['fin de mot', 'nasale', 'ほん (hon)'],
    ], jp=(2,), ro=()),
  ]},
  {'title': '拍 — Voyelles longues et っ', 'blocks': [
    P('Le japonais compte en mores (拍, haku) : chaque kana vaut un temps, et une voyelle longue en vaut deux. Allonger ou raccourcir change le mot.'),
    T(['Court', 'Long', 'Sens'], [
     ['おばさん obasan', 'おばあさん obāsan', 'tante / grand-mère'],
     ['おじさん ojisan', 'おじいさん ojīsan', 'oncle / grand-père'],
     ['ゆき yuki', 'ゆうき yūki', 'neige / courage'],
     ['ビル biru', 'ビール bīru', 'immeuble / bière'],
     ['ここ koko', 'こうこう kōkō', 'ici / lycée'],
     ['とる toru', 'とおる tōru', 'prendre / passer'],
    ], jp=(0, 1), ro=()),
    H('La consonne double っ'),
    T(['Simple', 'Double', 'Sens'], [
     ['きて kite', 'きって kitte', 'viens / timbre'],
     ['かこ kako', 'かっこ kakko', 'passé / parenthèses'],
     ['さか saka', 'さっか sakka', 'pente / écrivain'],
    ], jp=(0, 1), ro=()),
    H('Le ん compte pour un temps'),
    T(['Sans ん', 'Avec ん', 'Sens'], [
     ['かじ kaji', 'かんじ kanji', 'incendie / caractère'],
     ['きねん kinen', 'きんえん kin’en', 'commémoration / interdit de fumer'],
    ], jp=(0, 1), ro=()),
    N('Pour te contrôler : tape le rythme avec la main en comptant une more par kana. おばあさん fait 5 temps (o-ba-a-sa-n), おばさん en fait 4.'),
  ]},
  {'title': '高低アクセント — Accent de hauteur', 'blocks': [
    P('Le japonais standard ne marque pas l’accent par la force mais par la hauteur : chaque mot a un schéma de syllabes hautes et basses. Ce qui compte, c’est l’endroit où la voix descend.'),
    T(['Type', 'Schéma', 'Exemple'], [
     ['平板 heiban (plat)', 'bas puis haut, sans descente', '端 はし (bord) ; 飴 あめ (bonbon)'],
     ['頭高 atamadaka', 'haut puis descente dès la 1re more', '箸 はし (baguettes) ; 雨 あめ (pluie)'],
     ['尾高 odaka', 'haut jusqu’à la fin, la descente apparaît sur la particule', '橋 はし (pont)'],
    ], jp=(2,), ro=()),
    N('Les trois « はし » se distinguent uniquement par la hauteur : 箸 は↓し, 橋 はし↓(が), 端 はし(が) sans descente. Dans le Kansai (Ōsaka, Kyōto), les schémas sont souvent inversés.'),
    N('Priorité raisonnable : travaille d’abord les longueurs et les っ, puis écoute et répète. Le dictionnaire en ligne OJAD (ojad.jp) donne l’accent de chaque mot et des formes de verbes.'),
    H('Intonation des questions'),
    T(['Phrase', 'Intonation'], [
     ['食べますか。 Tabemasu ka.', 'La voix monte sur か'],
     ['食べます。 Tabemasu.', 'La voix reste plate ou descend'],
     ['そうですか。 Sō desu ka.', 'Descendante : « Ah, je vois » ; montante : « Vraiment ? »'],
    ], jp=(0,), ro=()),
  ]},
  {'title': '母音の無声化 — Voyelles sourdes', 'blocks': [
    P('Les voyelles い et う entre deux consonnes sourdes, ou en fin de mot après une consonne sourde, sont souvent à peine prononcées. C’est ce qui donne le son typique du japonais parlé.'),
    T(['Mot', 'Lu comme', 'Remarque'], [
     ['です desu', '« des »', 'Le u final disparaît presque'],
     ['ます masu', '« mas »', 'Idem pour toutes les formes en ます'],
     ['すき suki', '« ski »', 'Le u entre s et k est sourd'],
     ['ありがとうございます', '« arigatō gozaimas »', 'Le u final est avalé'],
     ['きます kimasu', '« kimas »', 'Le i entre k et m reste net, seul le u final tombe'],
     ['ひと hito', '« hto »', 'Le i entre h et t est sourd'],
    ], jp=(0,), ro=()),
    N('Ne les omets pas par réflexe : écoute un natif dire です et ます puis imite. Ça donne tout de suite un rythme plus naturel.'),
  ]},
 ]})

# ───────────────────────── CONVERSATION ─────────────────────────
SECTIONS.append({
 'id': 'kaiwa', 'jp': '会話', 'label': 'Conversation', 'replace': None,
 'intro': 'Les petits mots qui font parler naturellement : réactions, hésitations, connecteurs, accord et refus polis, et les structures qui servent tous les jours.',
 'subs': [
  {'title': '相づち — Réactions', 'blocks': [
    T(['En français', '日本語', 'Rōmaji', 'Quand'], [
     ['Oui, je vous suis', 'はい / ええ', 'Hai / Ee', 'Pendant que l’autre parle'],
     ['Ah, je vois', 'そうですか', 'Sō desu ka', 'Réception d’une information'],
     ['Ah d’accord, c’est comme ça', 'そうなんですか', 'Sō nan desu ka', 'Un peu plus vivant'],
     ['Je vois, effectivement', 'なるほど', 'Naruhodo', 'Compréhension'],
     ['Vraiment ?', 'ほんとうですか', 'Hontō desu ka', 'Surprise, version polie'],
     ['Ah tiens ! (surprise)', 'へえ', 'Hē', 'Neutre à familier'],
     ['C’est vrai / Tout à fait', 'そうですね', 'Sō desu ne', 'Acquiescement'],
     ['Génial !', 'すごい', 'Sugoi', 'Admiration, tous registres'],
     ['Ça a l’air bien', 'いいですね', 'Ii desu ne', 'Réaction positive'],
     ['Ça doit être dur', '大変ですね', 'Taihen desu ne', 'Compassion'],
     ['Quel dommage', '残念ですね', 'Zannen desu ne', 'Regret'],
     ['Sérieux ? (familier)', 'まじで', 'Maji de', 'Entre amis uniquement'],
     ['Oups / Ça craint (familier)', 'やばい', 'Yabai', 'Peut être positif ou négatif'],
    ], jp=(1,), ro=(2,)),
    N('Les Japonais approuvent souvent d’un はい ou d’un signe de tête pendant que l’autre parle. Cela veut dire « je t’écoute », pas « je suis d’accord ».'),
  ]},
  {'title': 'つなぎ言葉 — Hésitations', 'blocks': [
    T(['En français', '日本語', 'Rōmaji'], [
     ['Euh… (je réfléchis)', 'えーと', 'Ēto'],
     ['Euh… (je vais demander ou interrompre poliment)', 'あのう', 'Anō'],
     ['Voyons… (avant de répondre)', 'そうですねえ', 'Sō desu nē'],
     ['Disons… (j’atténue)', 'まあ', 'Mā'],
     ['Un peu… (refus doux)', 'ちょっと…', 'Chotto…'],
     ['Hmm', 'うーん', 'Ūn'],
    ]),
    N('Utiliser えーと et そうですねえ te laisse du temps pour construire ta phrase. Les Japonais s’en servent constamment, donc ça ne fait pas hésitant.'),
  ]},
  {'title': '接続詞 — Connecteurs', 'blocks': [
    T(['En français', '日本語', 'Rōmaji', 'Registre'], [
     ['d’abord', 'まず', 'mazu', 'neutre'],
     ['ensuite', 'それから', 'sorekara', 'neutre'],
     ['et puis', 'そして', 'soshite', 'neutre'],
     ['de plus', 'それに', 'soreni', 'oral'],
     ['mais', 'でも', 'demo', 'oral'],
     ['cependant', 'しかし', 'shikashi', 'écrit, formel'],
     ['mais (familier)', 'だけど / けど', 'dakedo / kedo', 'familier'],
     ['donc / c’est pourquoi', 'だから', 'dakara', 'oral'],
     ['alors / du coup', 'それで', 'sorede', 'oral'],
     ['alors, bon (pour conclure)', 'じゃあ', 'jā', 'oral'],
     ['au fait', 'ところで', 'tokorode', 'neutre'],
     ['par exemple', 'たとえば', 'tatoeba', 'neutre'],
     ['en somme', 'つまり', 'tsumari', 'neutre'],
     ['enfin / pour finir', '最後に', 'saigo ni', 'neutre'],
    ], jp=(1,), ro=(2,)),
  ]},
  {'title': '同意・断り — Accord et refus polis', 'blocks': [
    T(['En français', '日本語', 'Rōmaji'], [
     ['D’accord / Pas de problème', 'いいですよ', 'Ii desu yo'],
     ['Avec plaisir', 'ぜひ', 'Zehi'],
     ['Je ne sais pas encore', 'まだわかりません', 'Mada wakarimasen'],
     ['Je vais y réfléchir (souvent un refus doux)', '考えておきます', 'Kangaete okimasu'],
     ['C’est un peu difficile (refus)', 'ちょっと難しいです', 'Chotto muzukashii desu'],
     ['J’ai déjà quelque chose ce jour-là', 'その日は予定があります', 'Sono hi wa yotei ga arimasu'],
     ['Non merci', '結構です', 'Kekkō desu'],
     ['Je ne suis pas tout à fait de cet avis', 'ちょっと違うと思います', 'Chotto chigau to omoimasu'],
    ]),
    N('Au Japon, un non direct est rare. Des réponses comme ちょっと…, 考えておきます ou 難しいですね sont généralement des refus. Fais de même pour décliner sans froisser.'),
  ]},
  {'title': '文型 — Structures utiles', 'blocks': [
    T(['Structure', '日本語', 'Rōmaji', 'Sens'], [
     ['〜ませんか (inviter)', '一緒に行きませんか。', 'Issho ni ikimasen ka.', 'Et si on y allait ensemble ?'],
     ['〜ましょう (proposer)', '食べましょう。', 'Tabemashō.', 'Mangeons.'],
     ['〜たいです (désir)', '日本の料理を食べたいです。', 'Nihon no ryōri o tabetai desu.', 'Je veux manger de la cuisine japonaise.'],
     ['〜てもいいですか (permission)', '写真を撮ってもいいですか。', 'Shashin o totte mo ii desu ka.', 'Puis-je prendre une photo ?'],
     ['〜てください (demander)', '見せてください。', 'Misete kudasai.', 'Montrez-moi, s’il vous plaît.'],
     ['〜ていただけませんか (demande polie)', '教えていただけませんか。', 'Oshiete itadakemasen ka.', 'Pourriez-vous m’indiquer… ?'],
     ['〜と思います (opinion)', 'おいしいと思います。', 'Oishii to omoimasu.', 'Je pense que c’est bon.'],
     ['〜ことがあります (expérience)', '日本に行ったことがあります。', 'Nihon ni itta koto ga arimasu.', 'Je suis déjà allé au Japon.'],
     ['〜つもりです (intention)', '来年日本に行くつもりです。', 'Rainen Nihon ni iku tsumori desu.', 'Je compte aller au Japon l’an prochain.'],
     ['〜ほうがいいです (conseil)', '早く寝たほうがいいです。', 'Hayaku neta hō ga ii desu.', 'Il vaut mieux dormir tôt.'],
     ['〜から (raison)', '疲れたから、休みます。', 'Tsukareta kara, yasumimasu.', 'Je suis fatigué, donc je me repose.'],
    ], jp=(1,), ro=(2,)),
  ]},
  {'title': '会話を続ける — Relancer la conversation', 'blocks': [
    T(['En français', '日本語', 'Rōmaji'], [
     ['Et vous ?', 'あなたは？ / …さんは？', 'Anata wa? / …san wa?'],
     ['Vous venez d’où ?', 'ご出身はどちらですか。', 'Go-shusshin wa dochira desu ka.'],
     ['Que faites-vous dans la vie ?', 'お仕事は何ですか。', 'O-shigoto wa nan desu ka.'],
     ['Quel est votre passe-temps ?', '趣味は何ですか。', 'Shumi wa nan desu ka.'],
     ['Depuis combien de temps étudiez-vous le japonais ?', '日本語はどのくらい勉強していますか。', 'Nihongo wa dono kurai benkyō shite imasu ka.'],
     ['Vous êtes déjà allé à … ?', '…に行ったことがありますか。', '… ni itta koto ga arimasu ka.'],
     ['Qu’avez-vous préféré au Japon ?', '日本で何が一番よかったですか。', 'Nihon de nani ga ichiban yokatta desu ka.'],
     ['(On te complimente) Vous parlez bien japonais !', '日本語がお上手ですね。', 'Nihongo ga o-jōzu desu ne.'],
     ['(Réponse modeste) Pas du tout, je débute', 'いえいえ、まだまだです。', 'Ie ie, mada mada desu.'],
    ]),
  ]},
 ]})


# ───────── Voyage : situations ciblées ─────────
SECTIONS[0]['subs'] += [
 {'title': '鉄道 — Train et Shinkansen', 'blocks': [
   T(FR3, [
    ['Un billet de Shinkansen pour Kyōto, s’il vous plaît', '京都まで新幹線の切符をお願いします。', 'Kyōto made Shinkansen no kippu o onegaishimasu.'],
    ['Une place réservée, s’il vous plaît', '指定席をお願いします。', 'Shiteiseki o onegaishimasu.'],
    ['Une place non réservée', '自由席をお願いします。', 'Jiyūseki o onegaishimasu.'],
    ['Place non-fumeur', '禁煙席をお願いします。', 'Kin’enseki o onegaishimasu.'],
    ['Aller simple / aller-retour', '片道 / 往復', 'katamichi / ōfuku'],
    ['Puis-je utiliser le JR Pass ?', 'JRパスは使えますか。', 'Jeiāru pasu wa tsukaemasu ka.'],
    ['Ce train s’arrête à … ?', 'この電車は…に止まりますか。', 'Kono densha wa … ni tomarimasu ka.'],
    ['Quelle est la prochaine gare ?', '次の駅はどこですか。', 'Tsugi no eki wa doko desu ka.'],
    ['Où est la voiture n° 5 ?', '五号車はどこですか。', 'Gogōsha wa doko desu ka.'],
    ['Le train est en retard ?', '電車は遅れていますか。', 'Densha wa okurete imasu ka.'],
    ['J’ai oublié un objet dans le train', '電車に忘れ物をしました。', 'Densha ni wasuremono o shimashita.'],
    ['Où puis-je acheter un bento de gare ?', '駅弁はどこで買えますか。', 'Ekiben wa doko de kaemasu ka.'],
   ]),
   H('Mots utiles'),
   T(['En français', '日本語', 'Rōmaji'], [
    ['billet', '切符', 'kippu'],
    ['correspondance', '乗り換え', 'norikae'],
    ['première classe (Green Car)', 'グリーン車', 'gurīn-sha'],
    ['agent de gare', '駅員', 'eki-in'],
    ['objets trouvés', '忘れ物', 'wasuremono'],
    ['retard', '遅延', 'chien'],
    ['service supprimé', '運休', 'unkyū'],
    ['quai', 'ホーム', 'hōmu'],
    ['numéro de quai', '番線', 'bansen'],
   ]),
 ]},
 {'title': '温泉 — Onsen et ryokan', 'blocks': [
   T(FR3, [
    ['Où est l’onsen ?', '温泉はどこですか。', 'Onsen wa doko desu ka.'],
    ['Quel est le prix d’entrée ?', '入浴料はいくらですか。', 'Nyūyokuryō wa ikura desu ka.'],
    ['Où est le vestiaire ?', '脱衣所はどこですか。', 'Datsuijo wa doko desu ka.'],
    ['Puis-je louer une serviette ?', 'タオルを借りられますか。', 'Taoru o kariraremasu ka.'],
    ['Avez-vous un bain privé à réserver ?', '貸切風呂はありますか。', 'Kashikiri-buro wa arimasu ka.'],
    ['J’ai un tatouage. Puis-je entrer ?', 'タトゥーがありますが、入れますか。', 'Tatū ga arimasu ga, hairemasu ka.'],
    ['À quelle heure est le dîner ?', '夕食は何時ですか。', 'Yūshoku wa nanji desu ka.'],
    ['À quelle heure est le petit-déjeuner ?', '朝食は何時ですか。', 'Chōshoku wa nanji desu ka.'],
    ['Pouvez-vous préparer le futon ?', '布団を敷いてもらえますか。', 'Futon o shiite moraemasu ka.'],
   ]),
   H('Mots à reconnaître'),
   T(['En français', '日本語', 'Rōmaji'], [
    ['bain pour hommes', '男湯', 'otokoyu'],
    ['bain pour femmes', '女湯', 'onnayu'],
    ['bain en plein air', '露天風呂', 'rotenburo'],
    ['vestiaire', '脱衣所', 'datsuijo'],
    ['yukata (kimono léger)', '浴衣', 'yukata'],
    ['auberge traditionnelle', '旅館', 'ryokan'],
   ]),
   N('Règles d’usage : se laver et se rincer à fond avant d’entrer dans le bain. La serviette ne va pas dans l’eau, on la pose sur la tête ou au bord. On entre nu. Beaucoup d’onsen refusent encore les tatouages visibles, mais certains les acceptent avec un patch ou dans un bain privé : demande avant.'),
 ]},
 {'title': 'ハイキング — Randonnée et nature', 'blocks': [
   T(FR3, [
    ['Quel est le parcours le plus facile ?', '一番簡単なコースはどれですか。', 'Ichiban kantan na kōsu wa dore desu ka.'],
    ['Combien de temps faut-il pour monter ?', '登るのにどのくらいかかりますか。', 'Noboru no ni dono kurai kakarimasu ka.'],
    ['Le sentier est-il ouvert ?', '登山道は開いていますか。', 'Tozandō wa aite imasu ka.'],
    ['Y a-t-il des ours par ici ?', 'このあたりにクマは出ますか。', 'Kono atari ni kuma wa demasu ka.'],
    ['Où est le refuge ?', '山小屋はどこですか。', 'Yamagoya wa doko desu ka.'],
    ['Peut-on remplir sa gourde quelque part ?', '水を補給できる場所はありますか。', 'Mizu o hokyū dekiru basho wa arimasu ka.'],
    ['Quel temps fera-t-il demain ?', '明日の天気はどうですか。', 'Ashita no tenki wa dō desu ka.'],
    ['Faisons une pause', '少し休みましょう。', 'Sukoshi yasumimashō.'],
    ['Je me suis foulé la cheville', '足首をひねりました。', 'Ashikubi o hinerimashita.'],
   ]),
   H('Mots à reconnaître'),
   T(['En français', '日本語', 'Rōmaji'], [
    ['montagne', '山', 'yama'],
    ['sommet', '頂上', 'chōjō'],
    ['départ du sentier', '登山口', 'tozanguchi'],
    ['cascade', '滝', 'taki'],
    ['lac', '湖', 'mizūmi'],
    ['forêt', '森', 'mori'],
    ['danger', '危険', 'kiken'],
    ['passage interdit', '通行止め', 'tsūkōdome'],
    ['ours', '熊 / クマ', 'kuma'],
   ]),
   N('Au Japon, les ours sont une vraie question en montagne. Beaucoup de sentiers ont des cloches à agiter. Les panneaux 熊出没注意 (kuma shutsubotsu chūi) signalent une zone à ours.'),
 ]},
]

# ── Sous-partie ajoutée à la section 助詞 (Particules) ──
def _tw(rows): return T(['日本語', 'Sens', 'Pourquoi'], rows, jp=(0,), ro=())
EXTRA_SUBS = {'助詞': [{
 'title': '使い分け — Quand choisir laquelle',
 'blocks': [
  P('Les erreurs les plus fréquentes viennent de paires de particules proches. Pour chaque paire : la règle, des exemples côte à côte et le piège à retenir.'),
  H('は ou が ?'),
  P('は pose le thème : ce dont on parle, une information connue. が désigne le sujet précis : une information nouvelle, la réponse à « qui ? / quoi ? », ou ce qui existe ou se produit.'),
  _tw([
   ['私は田中です。', 'Moi, je suis Tanaka.', 'は : on présente le thème « moi ».'],
   ['誰が田中さんですか。', 'Qui est Tanaka ?', 'が : mot interrogatif sujet.'],
   ['あの人が田中さんです。', 'C’est cette personne, Tanaka.', 'が : réponse à « qui ? », information nouvelle.'],
   ['雨が降っています。', 'Il pleut.', 'が : phénomène observé, constat.'],
   ['今日は雨が降っています。', 'Aujourd’hui, il pleut.', 'は : thème « aujourd’hui » ; が : sujet « pluie ».'],
  ]),
  N('Piège : un mot interrogatif sujet (誰, 何, どれ, いつ…) prend が, jamais は.'),
  H('に ou で ?'),
  P('に marque un point : arrivée, existence, moment précis, personne visée. で marque le cadre d’une action : où elle se déroule, avec quoi, comment.'),
  _tw([
   ['公園に猫がいます。', 'Il y a un chat dans le parc.', 'に : lieu d’existence (いる / ある).'],
   ['公園で遊びます。', 'Je joue dans le parc.', 'で : lieu où se déroule l’action.'],
   ['東京に住んでいます。', 'J’habite à Tokyo.', 'に : 住む → lieu de résidence.'],
   ['家でご飯を食べます。', 'Je mange à la maison.', 'で : lieu de l’action 食べる.'],
   ['電車で行きます。', 'J’y vais en train.', 'で : moyen de transport.'],
   ['電車に乗ります。', 'Je monte dans le train.', 'に : 乗る se construit avec に.'],
   ['会議は三階であります。', 'La réunion se tient au 3e étage.', 'で : un événement a lieu quelque part.'],
  ]),
  N('Piège : ある / いる → に pour ce qui existe (本があります), mais で pour un événement (パーティーがあります → 公園で).'),
  H('へ ou に ?'),
  P('Avec 行く, 来る, 帰る, へ et に sont interchangeables pour la destination ; へ insiste sur la direction. に est obligatoire pour un moment précis, un destinataire ou l’existence : là, へ est impossible.'),
  _tw([
   ['日本へ行きます。', 'Je vais au Japon.', 'へ : direction (に possible aussi).'],
   ['日本に行きます。', 'Je vais au Japon.', 'に : destination, ton neutre.'],
   ['七時に起きます。', 'Je me lève à sept heures.', 'に : heure précise (へ impossible).'],
   ['友達にあげます。', 'Je le donne à un ami.', 'に : destinataire (へ impossible).'],
  ]),
  N('へ s’écrit avec le kana へ mais se lit « e ».'),
  H('を ou が ?'),
  P('を marque l’objet direct d’une action. Mais les verbes et adjectifs d’état, de goût, de désir ou de capacité prennent が : 好き, 嫌い, 上手, 下手, ほしい, わかる, できる, ある, いる.'),
  _tw([
   ['水を飲みます。', 'Je bois de l’eau.', 'を : objet direct d’un verbe d’action.'],
   ['犬が好きです。', 'J’aime les chiens.', 'が : 好き prend が.'],
   ['日本語がわかります。', 'Je comprends le japonais.', 'が : わかる prend が.'],
   ['車がほしいです。', 'Je veux une voiture.', 'が : ほしい prend が.'],
   ['料理ができます。', 'Je sais cuisiner.', 'が : できる prend が.'],
   ['水が飲みたいです。', 'Je veux boire de l’eau.', 'Avec 〜たい : が ou を, les deux existent.'],
   ['公園を散歩します。', 'Je me promène dans le parc.', 'を : lieu parcouru (散歩する, 歩く, 渡る).'],
  ]),
  H('と, や, も'),
  P('と relie une liste complète, ou signifie « avec ». や donne des exemples parmi d’autres (souvent avec など). も signifie « aussi » et remplace は, が ou を ; après に ou で, il s’ajoute (にも, でも).'),
  _tw([
   ['りんごとみかんを買いました。', 'J’ai acheté des pommes et des mandarines.', 'と : liste complète, rien d’autre.'],
   ['りんごやみかんを買いました。', 'J’ai acheté des pommes, des mandarines…', 'や : exemples, il y en avait d’autres.'],
   ['友達と行きます。', 'J’y vais avec un ami.', 'と : avec, accompagnement.'],
   ['私も行きます。', 'Moi aussi, j’y vais.', 'も : remplace は ou が.'],
   ['日本にも行きました。', 'Je suis aussi allé au Japon.', 'も s’ajoute à に.'],
   ['コーヒーも紅茶も飲みません。', 'Je ne bois ni café ni thé.', 'A も B も + négatif : ni A ni B.'],
  ]),
  H('から ou ので ?'),
  P('から donne une raison plus subjective ; elle peut terminer la phrase (« Pourquoi ? — Parce que… »). ので est plus objectif et plus doux, souvent poli. Avec un nom : 雨なので, mais 雨だから.'),
  _tw([
   ['疲れたから、休みます。', 'Je suis fatigué, donc je me repose.', 'から : cause, point de vue personnel.'],
   ['雨なので、行きません。', 'Comme il pleut, je n’y vais pas.', 'ので : cause objective, nom + な + ので.'],
   ['「どうして休みますか。」「疲れたからです。」', '« Pourquoi te reposes-tu ? » « Parce que je suis fatigué. »', 'から : peut conclure la phrase.'],
   ['駅から歩きます。', 'Je marche depuis la gare.', 'から : aussi point de départ.'],
  ]),
  H('けど, が, のに'),
  P('けど (familier) et が (plus soutenu) opposent deux idées : « mais ». のに exprime la surprise ou le regret : « alors que, et pourtant ». Après のに, on ne peut pas faire une demande ni un ordre.'),
  _tw([
   ['高いけど、買います。', 'C’est cher, mais je l’achète.', 'けど : mais, ton neutre ou familier.'],
   ['行きたいが、時間がありません。', 'Je veux y aller, mais je n’ai pas le temps.', 'が : mais, ton plus formel ou écrit.'],
   ['薬を飲んだのに、まだ痛いです。', 'J’ai pris un médicament, et pourtant j’ai encore mal.', 'のに : surprise, déception.'],
   ['すみませんが、駅はどこですか。', 'Excusez-moi, où est la gare ?', 'が : introduction polie d’une question.'],
  ]),
  H('だけ, しか, ばかり'),
  P('だけ = seulement (neutre, verbe affirmatif). しか = ne… que, toujours avec un verbe négatif, avec une idée de manque. ばかり = presque toujours la même chose, souvent un reproche.'),
  _tw([
   ['一つだけください。', 'Un seul, s’il vous plaît.', 'だけ : seulement, neutre.'],
   ['千円しかありません。', 'Je n’ai que mille yens.', 'しか + négatif : c’est peu.'],
   ['漫画ばかり読んでいます。', 'Il ne lit que des mangas.', 'ばかり : toujours pareil, reproche possible.'],
   ['一度も行ったことがありません。', 'Je n’y suis jamais allé, pas une fois.', '数 + も + négatif : pas même…'],
  ]),
  H('まで ou までに'),
  P('まで indique jusqu’à quand dure une action continue. までに donne la date limite d’une action ponctuelle : « avant, au plus tard ».'),
  _tw([
   ['五時まで働きます。', 'Je travaille jusqu’à cinq heures.', 'まで : durée continue.'],
   ['五時までに来てください。', 'Venez avant cinq heures.', 'までに : date limite, action ponctuelle.'],
   ['朝から晩まで働きます。', 'Je travaille du matin au soir.', 'から … まで : de … à …'],
  ]),
  H('ね, よ, か, な'),
  P('Particules finales : ね cherche l’accord, よ informe ou insiste, か pose une question, な est un monologue ou une interdiction (forme du dictionnaire + な).'),
  _tw([
   ['今日は暑いですね。', 'Il fait chaud, hein ?', 'ね : chercher l’accord.'],
   ['この電車は新宿に行きますよ。', 'Ce train va à Shinjuku, je vous assure.', 'よ : informer, affirmer.'],
   ['行きますか。', 'Vous y allez ?', 'か : question.'],
   ['いい天気だな。', 'Quel beau temps.', 'な : monologue, ton familier masculin.'],
   ['行くな。', 'N’y va pas !', 'Forme du dictionnaire + な : interdiction brutale.'],
  ]),
 ]}]}

# contenu supplémentaire
import vocab_core
EXTRA_SUBS['語彙'] = vocab_core.SUBS_VOCAB
EXTRA_SUBS['時間'] = vocab_core.SUBS_TEMPS
EXTRA_SUBS['表現'] = vocab_core.EXPR_SUBS
EXTRA_SUBS['会話'] = vocab_core.KAIWA_SUBS

import kanji_n3
EXTRA_SUBS['漢字'] = [kanji_n3.n3_sub(open(os.path.join(DATA, 'have_kanji.txt'), encoding='utf-8').read())]

import adjectifs_keigo, voyage_conversation, vocab_themes
def _merge(d):
    for k, v in d.items(): EXTRA_SUBS.setdefault(k, []).extend(v)
_merge(adjectifs_keigo.extra_subs()); _merge(voyage_conversation.voy_conv_subs()); _merge(vocab_themes.all_subs())
import compteurs
_merge(compteurs.counters_subs())

SECTIONS.append(vocab_themes.geo_section())
