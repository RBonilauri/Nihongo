# -*- coding: utf-8 -*-
# Deuxième phrase d'exemple de chaque verbe : sens ou contexte différent de la première (verbes_exemples.py).
# Même format de ligne : verbe | début JP | verbe FR | complément FR | sujet | négation | options
RAW = """
いる|私は家に|être|à la maison||||EP
なる|有名に|devenir|célèbre||||
できる|宿題が|pouvoir|finir mes devoirs||||ED
行う|試験を|passer|l’examen|On|d’examen|
違う|私の意見は彼と|être|différente de la sienne|Mon opinion|||EP
合う|計算が|être|juste|Le calcul||E|
似る|私は父に|ressembler|à mon père||||UEP
似合う|赤い帽子が彼女に|aller|bien|Ce chapeau rouge||EP
残る|お金が少し|rester||Un peu d’argent|||E
残す|メモを|laisser|un mot|||de mot|
含む|このスープは野菜を|contenir|des légumes|Cette soupe|de légumes|E
含める|送料も|inclure|les frais de port dans le prix||||
分ける|ごみを|trier|les déchets||||
合わせる|手を|joindre|les mains||||
役に立つ|この地図は旅行で|être|utile en voyage|Cette carte||E
気づく|電気が消えているのに|remarquer|que la lumière est éteinte||||D
感じる|風を|sentir|le vent||||
当たる|宝くじに|gagner|à la loterie||||
起こる|事故が|arriver||Un accident|||E
起こす|問題を|causer|un problème|||de problème|
決まる|会議の日が|être|fixée|La date de la réunion||E
済む|仕事が|être|fini|Mon travail||E
済ませる|宿題を|finir|mes devoirs|||
従う|先生の指示に|suivre|les consignes du professeur||||
起きる|朝六時に|se lever|à six heures|||
寝る|夜十一時に|se coucher|à onze heures|||
食べる|朝ご飯を|prendre|le petit-déjeuner||de petit-déjeuner|
飲む|薬を|prendre|des médicaments||de médicaments|
洗う|車を|laver|la voiture||||
着る|スーツを|mettre|un costume||de costume|
履く|ズボンを|mettre|un pantalon||de pantalon|
脱ぐ|コートを|enlever|mon manteau||||
使う|お金を|dépenser|de l’argent||d’argent|
開ける|ドアを|ouvrir|la porte||||
閉める|カーテンを|fermer|les rideaux||||
作る|友達を|se faire|des amis||d’amis|
持つ|夢を|avoir|un rêve||de rêve|U
置く|鍵をテーブルの上に|poser|la clé sur la table||||
取る|写真を|prendre|une photo||de photo|
待つ|バスを|attendre|le bus||||
立つ|窓の近くに|se tenir|près de la fenêtre||||
座る|ソファに|s’asseoir|sur le canapé||||
歩く|駅まで|marcher|jusqu’à la gare||||
走る|毎朝|courir|tous les matins||||
泳ぐ|プールで|nager|à la piscine||||
遊ぶ|友達と|jouer|avec mes amis||||
休む|風邪で会社を|s’absenter|du travail à cause d’un rhume||||
働く|病院で|travailler|à l’hôpital||||
住む|大阪に|habiter|à Osaka||||U
生まれる|北海道で|naître|à Hokkaido||||DE
生きる|楽しく|vivre|heureux||||
死ぬ|花が|mourir|faute d’eau|La fleur*|||DE
行く|仕事に|aller|au travail||||
来る|春が|arriver||Le printemps|||DE
帰る|国に|rentrer|dans mon pays||||
出る|会議に|assister|à la réunion||||
入る|大学に|entrer|à l’université||||
着く|空港に|arriver|à l’aéroport||||
出かける|買い物に|sortir|pour faire des courses||||
乗る|バスに|prendre|le bus||||
降りる|電車を|descendre|du train||||
乗り換える|地下鉄に|changer|pour le métro||||
通る|トンネルを|traverser|le tunnel||||
渡る|橋を|traverser|le pont||||
曲がる|次の角を左に|tourner|à gauche au prochain coin||||
止まる|時計が|s’arrêter|à midi|La montre*||E
止める|エンジンを|couper|le moteur||||
迷う|どの服にするか|hésiter|entre deux vêtements||||
戻る|席に|retourner|à ma place||||
向かう|会社へ|se rendre|au bureau||||
急ぐ|仕事を|se presser|pour finir le travail||||
並ぶ|窓の前に花瓶が|être|posé près de la fenêtre|Le vase|||EP
泊まる|友達の家に|dormir|chez un ami||||
運ぶ|机を|déplacer|la table||||
言う|本当のことを|dire|la vérité||||
話す|電話で母と|parler|à ma mère au téléphone||||
聞く|先生に|demander|au professeur||||
聞こえる|電車の音が|entendre|le bruit du train||||ED
答える|電話に|répondre|au téléphone||||
伝える|気持ちを|exprimer|mes sentiments||||
頼む|友達に手伝いを|demander|de l’aide à mon ami||d’aide à mon ami|
断る|仕事を|refuser|ce travail||||
謝る|先生に|s’excuser|auprès du professeur||||
笑う|冗談を聞いて|rire|en entendant la blague||||
泣く|悲しくて|pleurer|de tristesse||||
歌う|大きな声で|chanter|à haute voix||||
読む|漫画を|lire|un manga||de manga|
書く|名前を|écrire|mon nom||||
見る|テレビを|regarder|la télévision||||
見える|星が|voir|les étoiles||||ED
見せる|パスポートを|montrer|mon passeport||||
会う|先生に|rencontrer|le professeur||||
呼ぶ|友達を|inviter|mon ami||||
送る|荷物を|envoyer|un colis||de colis|
教える|道を|indiquer|le chemin||||
習う|ピアノを|apprendre|le piano||||
覚える|漢字を|apprendre|des kanji par cœur||||
忘れる|約束を|oublier|le rendez-vous||||
思い出す|友達の名前を|se souvenir|du nom de mon ami||||
数える|星を|compter|les étoiles||||
"""
RAW += """
間違える|答えを|se tromper|dans la réponse||||
あげる|母に花を|offrir|des fleurs à ma mère||de fleurs à ma mère|
もらう|母から手紙を|recevoir|une lettre de ma mère||de lettre de ma mère|
くれる|先生が私に本を|prêter|un livre|Mon professeur|de livre|
貸す|友達にお金を|prêter|de l’argent à mon ami||d’argent à mon ami|
借りる|友達から傘を|emprunter|un parapluie à mon ami||de parapluie à mon ami|
返す|友達に傘を|rendre|le parapluie à mon ami||||
渡す|友達に鍵を|donner|la clé à mon ami||||
買う|パンを|acheter|du pain||de pain|
売る|野菜を|vendre|des légumes||de légumes|
払う|税金を|payer|les impôts||||
探す|仕事を|chercher|du travail||de travail|
見つける|いい店を|trouver|un bon magasin||de bon magasin|
見つかる|答えが|être|trouvée|La réponse||E
なくす|自信を|perdre|confiance||de confiance|
落とす|コップを|faire|tomber un verre||||
拾う|タクシーを|prendre|un taxi dans la rue||de taxi dans la rue|
捨てる|古い服を|jeter|de vieux vêtements||de vieux vêtements|
手伝う|友達の引っ越しを|aider|mon ami à déménager||||
思う|明日は雨だと|penser|qu’il pleuvra demain||||ED
考える|いい方法を|chercher|une bonne méthode||de bonne méthode|
知る|その事実を|apprendre|ce fait||||
分かる|日本語が|comprendre|le japonais||||E
信じる|神を|croire|en Dieu||||
決める|新しい仕事を|choisir|un nouveau travail||de nouveau travail|
選ぶ|好きな色を|choisir|ma couleur préférée||||
困る|お金がなくて|être|en difficulté||||ED
驚く|大きな音に|sursauter|au grand bruit||||ED
喜ぶ|プレゼントをもらって|se réjouir|de recevoir un cadeau||||
楽しむ|音楽を|profiter|de la musique||||
疲れる|歩きすぎて|être|épuisé d’avoir trop marché||||ED
慣れる|早起きに|s’habituer|à me lever tôt||||
間に合う|会議に|arriver|à temps à la réunion||||
足りる|時間が|suffire|pour finir|Le temps||E
要る|パスポートが|avoir|besoin d’un passeport||besoin d’un passeport|E
気をつける|健康に|faire|attention à ma santé||||
比べる|去年と今年を|comparer|cette année et l’an dernier||||
入れる|財布にお金を|mettre|de l’argent dans mon portefeuille||d’argent dans mon portefeuille|
出す|宿題を|rendre|mes devoirs||||
付ける|名前を|donner|un nom||de nom|
消す|電気を|éteindre|la lumière||||
切る|髪を|couper|mes cheveux||||
押す|ベルを|sonner|à la porte||||
引く|辞書を|chercher|dans le dictionnaire||||
壊れる|時計が|tomber|en panne|La montre*||E
壊す|健康を|ruiner|ma santé||||
直す|間違いを|corriger|l’erreur||||
治る|けがが|guérir|doucement|Ma blessure||E
落ちる|試験に|échouer|à l’examen||||
始まる|映画が|commencer|à huit heures|Le film||E
始める|新しい仕事を|commencer|un nouveau travail||de nouveau travail|
終わる|授業が|finir|à midi|Le cours||E
続ける|運動を|continuer|le sport||||
続く|道がまっすぐ|continuer|tout droit|La route||
変える|髪の色を|changer|la couleur de mes cheveux||||
変わる|信号が|changer|au vert|Le feu||
増える|体重が|augmenter||Mon poids||E
減る|雨が|diminuer|en hiver|La pluie||E
かかる|時間が|prendre|beaucoup de temps|Cela|beaucoup de temps|E
掛ける|眼鏡を|mettre|mes lunettes||||
ある|駅の近くに銀行が|être|près de la gare|La banque||EP
焼く|パンを|faire|griller du pain||de pain|
煮る|肉を|faire|mijoter de la viande||de viande|
茹でる|パスタを|faire|cuire des pâtes||de pâtes|
炒める|ご飯を|faire|sauter du riz||de riz|
揚げる|鶏肉を|faire|frire du poulet||de poulet|
混ぜる|絵の具を|mélanger|les peintures||||
温める|手を|réchauffer|mes mains||||
冷やす|頭を|refroidir|ma tête||||
降る|雪が|neiger||Il|||
吹く|笛を|jouer|de la flûte||||
晴れる|霧が|se dissiper|vite|Le brouillard||E
曇る|鏡が|s’embuer||Le miroir||E
咲く|庭で花が|fleurir|dans le jardin|Une fleur||
磨く|靴を|cirer|mes chaussures||||
浴びる|朝、日光を|prendre|le soleil du matin||de soleil du matin|
拭く|窓を|essuyer|la fenêtre||||
眠る|八時間|dormir|huit heures||||
覚める|夢から|se réveiller|d’un rêve||||
太る|食べすぎて|grossir|à force de trop manger||||E
痩せる|病気で|maigrir|à cause de la maladie||||E
育つ|ここで|grandir|ici||||E
育てる|子どもを|élever|mes enfants||||
倒れる|道で|s’évanouir|dans la rue||||
酔う|お酒に|être|saoul||||ED
吐く|ため息を|pousser|un soupir||de soupir|
痛む|胃が|faire|mal|Mon estomac||
産む|赤ちゃんを|mettre|un bébé au monde||de bébé au monde|
亡くなる|おばあさんが|décéder||Ma grand-mère*|||DE
温まる|体が|se réchauffer|près du feu|Mon corps||
冷える|夜は|faire|froid la nuit|Il|||ED
乾く|喉が|avoir|soif||||ED
乾かす|洗濯物を|faire|sécher le linge||||
濡れる|雨に|se faire|mouiller par la pluie||||ED
折る|腕を|se casser|le bras||||
破る|記録を|battre|un record||de record|
破れる|ズボンが|se déchirer|au genou|Mon pantalon||
割る|皿を|casser|une assiette||d’assiette|
割れる|氷が|se briser|sous mon poids|La glace||
曲げる|膝を|plier|les genoux||||
"""
RAW += """
倒す|敵を|battre|l’adversaire||d’adversaire|
投げる|石を|jeter|une pierre||de pierre|
打つ|釘を|enfoncer|un clou||de clou|
叩く|太鼓を|battre|le tambour||||
蹴る|誘いを|refuser|l’invitation sèchement||||
掴む|チャンスを|saisir|l’occasion||||
握る|ペンを|tenir|un stylo||de stylo|
引っ張る|友達の腕を|tirer|sur le bras de mon ami||||
回す|コマを|faire|tourner une toupie||||
回る|時計の針が|tourner|dans le sens horaire|L’aiguille|||ED
動く|体が|bouger|facilement|Mon corps||
動かす|体を|bouger|mon corps||||
並べる|皿を|disposer|les assiettes sur la table||||
片付ける|おもちゃを|ranger|les jouets||||
掃く|玄関を|balayer|l’entrée||||
干す|布団を|faire|sécher la couette au soleil||||
畳む|傘を|fermer|mon parapluie||||
敷く|地図を|étaler|la carte sur la table||||
貼る|切手を|coller|un timbre||de timbre|
塗る|壁を|peindre|le mur||||
縫う|スカートを|coudre|une jupe||de jupe|
包む|お弁当を|envelopper|le bento dans un tissu||||
結ぶ|ネクタイを|nouer|ma cravate||||
測る|長さを|mesurer|la longueur||||
積む|経験を|accumuler|de l’expérience||d’expérience|
乗せる|子どもを車に|faire|monter l’enfant dans la voiture||||
下ろす|荷物を|déposer|les bagages||||
繋ぐ|手を|tenir|la main de mon enfant||||
繋がる|インターネットが|se connecter||Internet|||E
切れる|電話が|être|coupée|La communication||E
外す|席を|quitter|ma place un instant||||
外れる|予想が|se tromper|complètement|La prévision*||E
取れる|疲れが|partir|après le bain|La fatigue*||E
取り替える|シャツを|changer|de chemise||||
隠す|秘密を|cacher|un secret||de secret|
隠れる|月が雲に|se cacher|derrière les nuages|La lune*||
広げる|腕を|ouvrir|grand les bras||||
広がる|火事が|se propager|dans la ville|L’incendie||
離す|犬を|lâcher|le chien||||
離れる|家を|quitter|ma maison||||
近づく|試験が|s’approcher|à grands pas|L’examen||E
向く|右を|regarder|à droite||||
学ぶ|経験から|apprendre|de l’expérience||||
調べる|辞書で言葉を|chercher|un mot dans le dictionnaire||||
試す|新しい靴を|essayer|de nouvelles chaussures||de nouvelles chaussures|
写す|黒板を|copier|le tableau||||
描く|地図を|dessiner|une carte||de carte|
進む|時計が|avancer|de cinq minutes|Ma montre||
進める|時計を|avancer|ma montre||||
勧める|医者が運動を|conseiller|de faire du sport|Le médecin||
上がる|成績が|s’améliorer||Mon niveau|||E
下がる|熱が|baisser|enfin|Ma fièvre||E
上げる|声を|élever|la voix||||
下げる|頭を|baisser|la tête||||
届く|手が棚に|atteindre|l’étagère||||
届ける|花を|livrer|des fleurs||de fleurs|
集まる|客が|venir|en nombre|La clientèle*||
集める|友達からお金を|collecter|de l’argent auprès de mes amis||d’argent auprès de mes amis|
遅れる|会議に|être|en retard à la réunion||||
頑張る|毎日|s’appliquer|tous les jours||||
諦める|タバコを|arrêter|de fumer||||
勝つ|ゲームに|gagner|la partie||||
負ける|誘惑に|céder|à la tentation||||
誘う|友達を食事に|inviter|mon ami à manger||||
招く|結婚式に友達を|inviter|mon ami au mariage||||
祝う|結婚を|fêter|le mariage||||
贈る|賞を|décerner|un prix||de prix|
飛ぶ|飛行機で東京へ|voler|en avion jusqu’à Tokyo||||
登る|木に|grimper|à un arbre||||
滑る|雪の上で|glisser|sur la neige||||
釣る|海で|pêcher|en mer||||
踊る|音楽に合わせて|danser|en rythme||||
弾く|ギターを|jouer|de la guitare||||
撮る|ビデオを|filmer|une vidéo||de vidéo|
勤める|郵便局に|travailler|à la poste||||
辞める|タバコを|arrêter|de fumer||||
引っ越す|新しい家に|déménager|dans une nouvelle maison||||
通う|ジムに|aller|à la salle de sport||||
建てる|ビルを|construire|un immeuble||d’immeuble|
建つ|駅の前にホテルが|être|construit devant la gare|Un hôtel||EP
預ける|子どもを友達に|confier|mon enfant à un ami||||
預かる|友達の猫を|garder|le chat de mon ami||||
受け取る|給料を|toucher|mon salaire||||
受ける|面接を|passer|un entretien||d’entretien|
申し込む|コースに|s’inscrire|à un cours||||
払い戻す|代金を|rembourser|le prix||||
取り消す|発言を|retirer|ses paroles||||
延ばす|髪を|laisser|pousser mes cheveux||||
延びる|ひげが|pousser|vite|Ma barbe*||
確かめる|予約を|vérifier|la réservation||||
寄る|道の端に|se ranger|sur le bord de la route||||
立ち寄る|友達の家に|faire|un saut chez mon ami||de saut chez mon ami|
支払う|税金を|payer|les impôts||||
稼ぐ|生活費を|gagner|de quoi vivre||||
貯める|ポイントを|accumuler|des points||de points|
余る|時間が|rester||Le temps|||E
足す|二に三を|ajouter|trois à deux||||
売れる|新商品が|se vendre|très vite|Le nouveau produit||
売り切れる|今日の弁当が|être|épuisé|Le bento du jour||E
混む|道が|être|embouteillée|La route||E
"""
RAW += """
空く|おなかが|avoir|faim|||ED
開く|ドアが|s’ouvrir||La porte*||E
閉まる|ドアが|se fermer||La porte*||E
訪れる|春が|arriver||Le printemps|||E
迎える|新しい年を|accueillir|la nouvelle année||||
見送る|機会を|laisser|passer l’occasion||||
流行る|風邪が|se répandre||Le rhume|||E
下りる|幕が|tomber|à la fin du spectacle|Le rideau||EP
お願いする|友達に|demander|un service à mon ami||de service à mon ami|
嫌う|雨を|détester|la pluie||||
怒る|母が|se fâcher|à cause du bruit|Ma mère*||
叱る|犬を|gronder|le chien||||
褒める|料理を|complimenter|la cuisine||||
頼る|地図に|se fier|à la carte||||
許す|ミスを|pardonner|l’erreur||||
認める|彼の才能を|reconnaître|son talent||||
疑う|自分の目を|douter|de ses yeux||||
願う|平和を|souhaiter|la paix||||
祈る|試験の合格を|prier|pour réussir l’examen||||
怖がる|暗闇を|avoir|peur du noir||||ED
悲しむ|友達の死を|être|triste de la mort de mon ami||||ED
悩む|進路のことで|hésiter|sur mon orientation||||D
出会う|大学で恋人と|rencontrer|ma compagne à l’université||||
別れる|彼氏と|se séparer|de mon petit ami||||
付き合う|買い物に|accompagner|mon ami faire des courses||||
尋ねる|名前を|demander|le nom||||
知らせる|結果を|annoncer|le résultat||||
伝わる|意味が|être|compris|Le sens||E
話し合う|問題について|discuter|du problème||||
叫ぶ|助けを|appeler|à l’aide||||
黙る|何も言わずに|rester|silencieux||||
眺める|空を|regarder|le ciel||||
盗む|時間を|voler|du temps||de temps|
騙す|目を|tromper|les yeux||||
逃げる|火事から|fuir|l’incendie||||
追う|夢を|poursuivre|mon rêve||||
追いかける|猫を|courir|après le chat||||
捕まえる|タクシーを|héler|un taxi||de taxi|
守る|秘密を|garder|un secret||de secret|
助ける|子どもを|sauver|l’enfant||||
避ける|人混みを|éviter|la foule||||
防ぐ|風邪を|prévenir|le rhume||||
鳴る|ベルが|sonner||La sonnette||
鳴く|鳥が|chanter|le matin|Un oiseau||
光る|ライトが|briller|dans le noir|La lumière||
燃える|紙が|brûler|vite|Le papier||
燃やす|枯れ葉を|brûler|des feuilles mortes||de feuilles mortes|
溶ける|雪が|fondre|au soleil|La neige||
沸く|お風呂が|être|chaud|Le bain||E
沸かす|お茶のお湯を|faire|chauffer l’eau du thé||||
凍る|池が|geler|en hiver|L’étang||
積もる|ほこりが|s’accumuler|sur l’étagère|La poussière*||
流れる|涙が|couler|sur ma joue|Une larme*||
流す|トイレの水を|tirer|la chasse d’eau||||
浮かぶ|いい考えが|venir|à l’esprit|Une bonne idée*|||E
沈む|船が|couler|en mer|Le bateau||
消える|痛みが|disparaître|doucement|La douleur||
現れる|効果が|se faire|sentir|L’effet||
揺れる|カーテンが|bouger|au vent|Le rideau||
震える|手が|trembler|de peur|Ma main||
勉強する|図書館で|étudier|à la bibliothèque||||
散歩する|犬と|se promener|avec mon chien||||
運転する|夜、|conduire|la nuit||||
予約する|レストランを|réserver|un restaurant||de restaurant|
心配する|試験のことを|s’inquiéter|pour l’examen||||
質問する|電話で|poser|une question par téléphone||de question par téléphone|
電話する|会社に|téléphoner|à l’entreprise||||
掃除する|窓を|nettoyer|les fenêtres||||
洗濯する|日曜日に|faire|la lessive le dimanche||||
料理する|朝ご飯を|cuisiner|le petit-déjeuner||||
旅行する|一人で|voyager|seul||||
結婚する|二十五歳で|se marier|à vingt-cinq ans||||U
練習する|毎日|s’entraîner|tous les jours||||
準備する|旅行の|préparer|le voyage||||
説明する|先生に理由を|expliquer|la raison au professeur||||
利用する|図書館を|utiliser|la bibliothèque||||
紹介する|私の家族を|présenter|ma famille||||
案内する|町を|faire|visiter la ville||||
出発する|八時に|partir|à huit heures||||
到着する|予定より早く|arriver|plus tôt que prévu||||
注文する|飲み物を|commander|des boissons||de boissons|
確認する|メールを|vérifier|mes e-mails||||
連絡する|毎週母に|contacter|ma mère chaque semaine||||
参加する|祭りに|participer|à la fête||||
相談する|医者に|consulter|le médecin||||
約束する|七時に|promettre|d’être là à sept heures||||
招待する|家に友達を|inviter|mon ami chez moi||||
買い物する|ネットで|faire|des achats sur Internet||d’achats sur Internet|
"""

import re as _re
from verbes_exemples import _norm

def frames():
    out = {}
    for ln in RAW.strip().splitlines():
        if not ln.strip(): continue
        p = ln.split('|'); p += [''] * (6 - len(p))
        k, pre, fv, comp, subj = p[:5]
        neg, o = '', ''
        for f in p[5:]:
            if _re.fullmatch('[EDPTU]+', f): o += f
            elif f: neg = f
        out[k] = _norm(k, pre, fv, comp, subj, neg, o)
    return out
