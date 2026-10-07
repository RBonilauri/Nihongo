# -*- coding: utf-8 -*-
# Exemples de phrases pour les verbes courants du vocabulaire.
# Une ligne par verbe :  verbe | début de phrase japonais | verbe français (infinitif) | complément français | sujet (vide = « je ») | complément à la forme négative | options
# Options : E = pas de « en cours », D = pas de « souhait » (たい), P = imparfait à la place du passé composé,
#           T = présent avec ている (知っています), U = présent et négatif avec ている (似ています).
# Le japonais = début + verbe conjugué ; le français est conjugué par le moteur de js/04-traduction-formes.js.
RAW = """
いる|庭に犬が|être|dans le jardin|Le chien|||EP
なる|医者に|devenir|médecin||||
できる|ピアノが|pouvoir|jouer du piano||||ED
行う|会議を|tenir|une réunion|On|de réunion||
違う|この答えは|être|faux|La réponse|||EP
合う|このサイズは|convenir|à ma taille|Cette taille|||E
似る|母に|ressembler|à sa mère|Ma sœur|||UEP
似合う|その服は|aller|bien à Yuki|Cette robe|||E
残る|ケーキが|rester|dans la boîte|Un gâteau|||E
残す|ご飯を|laisser|du riz|||de riz|
含む|この値段は|inclure|la taxe|Ce prix|la taxe||E
含める|税金を|inclure|la taxe dans le total||||
分ける|ケーキを|partager|le gâteau en quatre||||
合わせる|時計を|régler|la montre sur l’heure||||
役に立つ|この辞書は|être|très utile|Ce dictionnaire|||E
気づく|間違いに|remarquer|l’erreur|||l’erreur|D
感じる|寒さを|ressentir|le froid||||
当たる|くじが|tomber|juste|Le ticket|||E
起こる|地震が|se produire||Un séisme|||E
起こす|弟を|réveiller|mon petit frère||||
決まる|予定が|être|décidé|Le programme|||E
済む|用事が|être|terminé|Mon affaire|||E
済ませる|買い物を|terminer|mes courses||||
従う|ルールに|suivre|les règles||||
起きる|六時に|se lever|à six heures||||
寝る|十一時に|se coucher|à onze heures||||
食べる|寿司を|manger|des sushis||des sushis|
飲む|お茶を|boire|du thé||de thé|
洗う|手を|se laver|les mains||||
着る|シャツを|mettre|une chemise||de chemise|
履く|靴を|mettre|mes chaussures||||
脱ぐ|靴を|enlever|mes chaussures||||
使う|スマホを|utiliser|mon téléphone||||
開ける|窓を|ouvrir|la fenêtre||||
閉める|ドアを|fermer|la porte||||
作る|料理を|préparer|le dîner||||
持つ|かばんを|porter|un sac||de sac|T
置く|本を|poser|le livre sur la table||||
取る|塩を|prendre|le sel||||
待つ|駅で友達を|attendre|mon ami à la gare||||
立つ|入口の前に|se tenir|devant l’entrée||||
座る|椅子に|s’asseoir|sur la chaise||||
歩く|公園を|marcher|dans le parc||||
走る|朝、川の近くを|courir|près de la rivière||||
泳ぐ|海で|nager|dans la mer||||
遊ぶ|公園で|jouer|dans le parc||||
休む|ここで|se reposer|ici||||
働く|会社で|travailler|dans une entreprise||||
住む|東京に|habiter|à Tokyo||||T
生まれる|京都で|naître|à Kyoto|Mon ami|||DE
生きる|百歳まで|vivre|jusqu’à cent ans||||
死ぬ|その花は|mourir|bientôt|Cette fleur|||DE
行く|学校へ|aller|à l’école||||
来る|友達が|venir|chez moi|Mon ami|||D
帰る|七時に家へ|rentrer|à sept heures||||
出る|八時に家を|sortir|de la maison à huit heures||||
入る|部屋に|entrer|dans la chambre||||
着く|駅に|arriver|à la gare||||
出かける|友達と|sortir|avec mes amis||||
乗る|電車に|prendre|le train||le train|
降りる|次の駅で|descendre|à la prochaine station||||
乗り換える|新宿で|changer|de train à Shinjuku||||
通る|橋を|passer|par le pont||||
渡る|道を|traverser|la rue||||
曲がる|角を右に|tourner|à droite au coin||||
止まる|電車が|s’arrêter|à la gare|Le train|||
止める|車を|garer|la voiture||||
迷う|道に|se perdre|en chemin||||
戻る|ホテルに|retourner|à l’hôtel||||
向かう|空港へ|se diriger|vers l’aéroport||||
急ぐ|駅へ|se dépêcher|d’aller à la gare||||
並ぶ|店の前に|faire|la queue devant le magasin||||
泊まる|ホテルに|loger|à l’hôtel||||
運ぶ|荷物を|porter|les bagages||||
言う|「ありがとう」と|dire|merci||||
話す|先生と|parler|avec le professeur||||
聞く|音楽を|écouter|de la musique||de musique|
聞こえる|鳥の声が|entendre|les oiseaux||||ED
答える|質問に|répondre|à la question||||
伝える|メッセージを|transmettre|le message||||
頼む|コーヒーを|commander|un café||de café|
断る|誘いを|refuser|l’invitation||||
謝る|友達に|s’excuser|auprès de mon ami||||
笑う|大きな声で|rire|à haute voix||||
泣く|映画を見て|pleurer|devant le film||||
歌う|カラオケで|chanter|au karaoké||||
読む|新聞を|lire|le journal||||
書く|手紙を|écrire|une lettre||de lettre|
見る|映画を|regarder|un film||de film|
見える|山が|voir|la montagne||||ED
見せる|写真を|montrer|la photo à mon ami||||
会う|駅で友達に|rencontrer|mon ami à la gare||||
呼ぶ|タクシーを|appeler|un taxi||de taxi|
送る|友達にメールを|envoyer|un e-mail à mon ami||d’e-mail|
教える|友達に日本語を|enseigner|le japonais à mon ami||||
習う|先生に日本語を|apprendre|le japonais||||
覚える|新しい言葉を|retenir|les nouveaux mots||||
忘れる|財布を|oublier|mon portefeuille||||
思い出す|昔のことを|se rappeler|le passé||||
数える|お金を|compter|l’argent||||
間違える|道を|se tromper|de chemin||||
あげる|友達にプレゼントを|offrir|un cadeau à mon ami||de cadeau|
もらう|友達にプレゼントを|recevoir|un cadeau de mon ami||de cadeau|
くれる|友達が私にプレゼントを|offrir|un cadeau|Mon ami|de cadeau||
貸す|友達にペンを|prêter|un stylo à mon ami||de stylo|
借りる|図書館で本を|emprunter|un livre à la bibliothèque||de livre|
返す|図書館に本を|rendre|le livre à la bibliothèque||||
渡す|先生に書類を|remettre|le dossier au professeur||||
買う|お土産を|acheter|des souvenirs||de souvenirs|
売る|古い本を|vendre|de vieux livres||de vieux livres|
払う|現金で|payer|en espèces||||
探す|鍵を|chercher|mes clés||||
見つける|鍵を|trouver|mes clés||||
見つかる|鍵が|trouver|ses clés|Mon ami|||ED
なくす|財布を|perdre|mon portefeuille||||
落とす|スマホを|faire|tomber mon téléphone||||
拾う|財布を|ramasser|un portefeuille||de portefeuille|
捨てる|ごみを|jeter|les ordures||||
手伝う|母の料理を|aider|ma mère à cuisiner||||
思う|日本は面白いと|penser|que le Japon est intéressant||||
考える|将来のことを|réfléchir|à mon avenir||||
知る|あの人を|connaître|cette personne||||T
分かる|答えが|comprendre|la réponse||||E
信じる|友達を|croire|mon ami||||
決める|行く日を|décider|du jour du départ||||
選ぶ|お土産を|choisir|un souvenir||de souvenir|
困る|道が分からなくて|être|embarrassé||||
驚く|ニュースを聞いて|être|surpris||||
喜ぶ|合格して|se réjouir|d’avoir réussi||||
楽しむ|旅行を|profiter|du voyage||||
疲れる|仕事で|être|fatigué||||
慣れる|日本の生活に|s’habituer|à la vie au Japon||||
間に合う|電車に|arriver|à temps pour le train||||
足りる|お金が|suffire|pour acheter ça|L’argent|||E
要る|傘が|avoir|besoin d’un parapluie||de parapluie|E
気をつける|足元に|faire|attention où je marche||||
比べる|二つの店の値段を|comparer|les prix des deux magasins||||
入れる|砂糖をコーヒーに|mettre|du sucre dans le café||de sucre|
出す|ごみを|jeter|les ordures||||
付ける|電気を|allumer|la lumière||||
消す|テレビを|éteindre|la télévision||||
切る|紙を|couper|le papier||||
押す|ボタンを|appuyer|sur le bouton||||
引く|ドアを|tirer|la porte||||
壊れる|時計が|se casser|net|La montre|||E
壊す|おもちゃを|casser|le jouet||||
直す|自転車を|réparer|mon vélo||||
治る|風邪が|guérir|vite|Mon rhume|||E
落ちる|葉が|tomber|des arbres|Les feuilles|||E
始まる|授業が|commencer|à neuf heures|Le cours|||
始める|勉強を|commencer|à étudier||||
終わる|仕事が|finir|à six heures|Le travail|||
続ける|日本語の勉強を|continuer|d’étudier le japonais||||
続く|雨が|continuer|toute la semaine|La pluie|||
変える|予定を|changer|mon programme||||
変わる|天気が|changer|vite|Le temps|||
増える|観光客が|augmenter|chaque année|Les touristes|||E
減る|人が|diminuer|dans le quartier|Le nombre d’habitants|||E
かかる|ここから駅まで十分|prendre|dix minutes|Le trajet|||E
掛ける|友達に電話を|passer|un coup de fil à mon ami||de coup de fil|
ある|机の上に本が|être|sur le bureau|Le livre|||EP
焼く|魚を|griller|du poisson||de poisson|
煮る|野菜を|mijoter|des légumes||de légumes|
茹でる|卵を|faire|bouillir des œufs||d’œufs|
炒める|野菜を|faire|sauter des légumes||de légumes|
揚げる|天ぷらを|frire|des tempuras||de tempuras|
混ぜる|卵と砂糖を|mélanger|les œufs et le sucre||||
温める|スープを|réchauffer|la soupe||||
冷やす|ビールを|refroidir|la bière||||
降る|雨が|tomber|toute la journée|La pluie|||
吹く|強い風が|souffler|fort|Le vent|||
晴れる|明日は|faire|beau|Le ciel|||E
曇る|空が|se couvrir|de nuages|Le ciel|||E
咲く|桜が|fleurir|au printemps|Les cerisiers|||
磨く|毎晩、歯を|se brosser|les dents||||
浴びる|夜、シャワーを|prendre|une douche||de douche|
拭く|テーブルを|essuyer|la table||||
眠る|ぐっすり|dormir|profondément||||
覚める|朝、目が|se réveiller|tôt||||
太る|最近|grossir|||||E
痩せる|運動して|maigrir|||||E
育つ|子どもが|grandir|vite|L’enfant|||E
育てる|庭で野菜を|cultiver|des légumes dans le jardin||de légumes|
倒れる|木が|tomber|pendant la tempête|L’arbre|||
酔う|電車で|avoir|mal au cœur||||
吐く|白い息を|souffler|de la buée||||
痛む|歯が|faire|mal|Ma dent|||
産む|鳥が卵を|pondre|des œufs|L’oiseau|d’œufs||
亡くなる|祖父が|décéder||Mon grand-père|||DE
温まる|部屋が|se réchauffer|doucement|La pièce|||
冷える|体が|avoir|froid||||E
乾く|洗濯物が|sécher|vite|Le linge|||
乾かす|髪を|sécher|mes cheveux||||
濡れる|雨で|être|mouillé||||
折る|紙を|plier|une feuille de papier||de feuille|
破る|手紙を|déchirer|la lettre||||
破れる|紙が|se déchirer|facilement|Le papier|||
割る|卵を|casser|un œuf||d’œuf|
割れる|コップが|se briser|net|Le verre|||
曲げる|針金を|plier|le fil de fer||||
倒す|木を|abattre|un arbre||d’arbre|
投げる|ボールを|lancer|la balle||||
打つ|キーボードを|taper|sur le clavier||||
叩く|ドアを|frapper|à la porte||||
蹴る|ボールを|donner|un coup de pied dans le ballon||||
掴む|手すりを|saisir|la rampe||||
握る|手を|serrer|la main||||
引っ張る|ロープを|tirer|sur la corde||||
回す|ハンドルを|tourner|le volant||||
回る|地球は太陽の周りを|tourner|autour du soleil|La Terre|||ED
動く|機械が|fonctionner|sans problème|La machine|||
動かす|車を|déplacer|la voiture||||
並べる|本を棚に|ranger|les livres sur l’étagère||||
片付ける|部屋を|ranger|ma chambre||||
掃く|庭を|balayer|le jardin||||
干す|洗濯物を|étendre|le linge||||
畳む|服を|plier|mes vêtements||||
敷く|布団を|étendre|le futon||||
貼る|ポスターを|coller|une affiche||d’affiche|
塗る|クリームを|appliquer|de la crème||de crème|
縫う|ボタンを|coudre|un bouton||de bouton|
包む|プレゼントを|emballer|un cadeau||de cadeau|
結ぶ|ひもを|nouer|la ficelle||||
測る|体温を|mesurer|ma température||||
積む|荷物を|charger|les bagages||||
乗せる|荷物を棚に|poser|les bagages sur l’étagère||||
下ろす|銀行でお金を|retirer|de l’argent à la banque||d’argent|
繋ぐ|ケーブルを|brancher|le câble||||
繋がる|電話が|être|connecté|L’appel|||E
切れる|電池が|se vider|bientôt|La pile|||
外す|眼鏡を|enlever|mes lunettes||||
外れる|ボタンが|se détacher|tout seul|Le bouton|||
取れる|ボタンが|se détacher|du manteau|Le bouton|||
取り替える|電池を|remplacer|les piles||||
隠す|プレゼントを|cacher|le cadeau||||
隠れる|ドアの後ろに|se cacher|derrière la porte||||
広げる|地図を|déplier|la carte||||
広がる|噂が|se répandre|vite|La rumeur*|||
離す|手を|lâcher|la main||||
離れる|駅から|s’éloigner|de la gare||||
近づく|駅に|s’approcher|de la gare||||
向く|窓の方を|se tourner|vers la fenêtre||||
学ぶ|大学で歴史を|étudier|l’histoire à l’université||||
調べる|インターネットで|chercher|sur Internet||||
試す|新しい方法を|essayer|une nouvelle méthode||de nouvelle méthode|
写す|ノートを|copier|le cahier||||
描く|絵を|dessiner|un tableau||de tableau|
進む|計画が|avancer|régulièrement|Le projet|||
進める|仕事を|faire|avancer le travail||||
勧める|友達にこの店を|recommander|ce magasin à mon ami||||
上がる|物価が|monter|chaque année|Les prix|||E
下がる|気温が|baisser|la nuit|La température|||
上げる|手を|lever|la main||||
下げる|値段を|baisser|le prix||||
届く|荷物が|arriver|vite|Le colis|||
届ける|荷物を|livrer|le colis||||
集まる|みんなが駅に|se rassembler|devant la gare|Tout le monde|||
集める|切手を|collectionner|les timbres||||
遅れる|電車が|avoir|du retard|Le train|||
頑張る|試験のために|se donner|du mal pour l’examen||||
諦める|夢を|abandonner|mon rêve||||
勝つ|試合に|gagner|le match||||
負ける|試合に|perdre|le match||||
誘う|友達を|inviter|mon ami au cinéma||||
招く|友達を|inviter|mon ami à dîner||||
祝う|友達の誕生日を|fêter|l’anniversaire de mon ami||||
贈る|母に花を|offrir|des fleurs à ma mère||de fleurs|
飛ぶ|鳥が|voler|dans le ciel|L’oiseau|||
登る|山に|gravir|la montagne||||
滑る|冬、スキーで|skier|dans les Alpes||||
釣る|川で魚を|pêcher|du poisson dans la rivière||de poisson|
踊る|祭りで|danser|à la fête||||
弾く|ピアノを|jouer|du piano||||
撮る|写真を|prendre|une photo||de photo|
勤める|銀行に|travailler|dans une banque||||
辞める|会社を|quitter|mon entreprise||||
引っ越す|大阪へ|déménager|à Osaka||||
通う|大学に|aller|à l’université||||
建てる|家を|construire|une maison||de maison|
建つ|新しい駅が|être|construit|Une nouvelle gare|||EP
預ける|荷物を|laisser|mes bagages à la consigne||||
預かる|荷物を|garder|vos bagages||||
受け取る|荷物を|recevoir|le colis||||
受ける|試験を|passer|l’examen||||
申し込む|ツアーに|s’inscrire|au circuit||||
払い戻す|チケットを|rembourser|le billet||||
取り消す|予約を|annuler|la réservation||||
延ばす|出発を|reporter|le départ||||
延びる|会議が|être|reporté|La réunion|||EP
確かめる|時間を|vérifier|l’heure||||
寄る|帰りに店に|passer|au magasin en rentrant||||
立ち寄る|帰りに本屋に|passer|à la librairie en rentrant||||
支払う|カードで|payer|par carte||||
稼ぐ|アルバイトで|gagner|de l’argent||d’argent|
貯める|毎月お金を|économiser|de l’argent||d’argent|
余る|お金が|rester||L’argent|||E
足す|砂糖を|ajouter|du sucre||de sucre|
売れる|この本は|se vendre|facilement|Ce livre|||
売り切れる|チケットが|être|épuisé|Les billets|||E
混む|電車が|être|bondé|Le train|||E
空く|電車が|être|vide|Le train|||E
開く|店が|ouvrir|à dix heures|Le magasin|||
閉まる|店が|fermer|à neuf heures|Le magasin|||
訪れる|京都を|visiter|Kyoto||||
迎える|友達を|accueillir|mon ami à l’aéroport||||
見送る|友達を|dire|au revoir à mon ami||||
流行る|この歌が|être|à la mode|Cette chanson|||E
下りる|許可が|être|accordé|Le permis|||EP
お願いする|店員に|demander|de l’aide au vendeur||||
嫌う|うそをつく人を|détester|les menteurs||||
怒る|先生が|se fâcher|contre l’élève|Le professeur|||
叱る|子どもを|gronder|l’enfant||||
褒める|友達を|féliciter|mon ami||||
頼る|友達に|compter|sur mon ami||||
許す|友達を|pardonner|à mon ami||||
認める|自分の間違いを|admettre|mon erreur||||
疑う|その話を|douter|de cette histoire||||
願う|みんなの幸せを|souhaiter|le bonheur de tous||||
祈る|神社で|prier|au sanctuaire||||
怖がる|犬を|avoir|peur des chiens||||
悲しむ|別れを|être|triste de la séparation||||
悩む|将来のことで|se tracasser|pour l’avenir||||
出会う|旅行先で友達に|rencontrer|un ami en voyage||||
別れる|駅で友達と|se séparer|de mon ami à la gare||||
付き合う|友達と|sortir|avec mon ami||||
尋ねる|道を|demander|le chemin||||
知らせる|友達に時間を|informer|mon ami de l’heure||||
伝わる|気持ちが|se transmettre|bien|Ses sentiments|||E
話し合う|友達と計画を|discuter|du plan avec mon ami||||
叫ぶ|大きな声で|crier|très fort||||
黙る|会議で|se taire|pendant la réunion||||
眺める|海を|contempler|la mer||||
盗む|財布を|voler|un portefeuille||de portefeuille|
騙す|人を|tromper|les gens||||
逃げる|犬が|s’enfuir|dans le jardin|Le chien|||
追う|犬が猫を|poursuivre|le chat|Le chien|||
追いかける|犬を|courir|après le chien||||
捕まえる|虫を|attraper|un insecte||d’insecte|
守る|約束を|tenir|ma promesse||||
助ける|友達を|aider|mon ami||||
避ける|混む時間を|éviter|les heures de pointe||||
防ぐ|事故を|éviter|l’accident||||
鳴る|電話が|sonner|souvent|Le téléphone|||
鳴く|猫が|miauler|dans la nuit|Le chat|||
光る|星が|briller|dans le ciel|Les étoiles|||
燃える|火が|brûler|fort|Le feu|||
燃やす|ごみを|brûler|les déchets||||
溶ける|氷が|fondre|vite|La glace|||
沸く|お湯が|bouillir|vite|L’eau|||
沸かす|お湯を|faire|bouillir de l’eau||d’eau|
凍る|川が|geler|en hiver|La rivière|||
積もる|雪が|s’accumuler|sur la route|La neige|||
流れる|川が|couler|doucement|La rivière|||
流す|水を|évacuer|l’eau||||
浮かぶ|ボートが|flotter|sur l’eau|Le bateau|||
沈む|太陽が|se coucher|à l’ouest|Le soleil|||
消える|電気が|s’éteindre|tout à coup|La lumière*|||
現れる|月が|apparaître|derrière les nuages|La lune|||
揺れる|地震で家が|trembler|fort|La maison|||
震える|寒くて|trembler|de froid||||
勉強する|日本語を|étudier|le japonais||||
散歩する|公園を|se promener|dans le parc||||
運転する|車を|conduire|une voiture||de voiture|
予約する|ホテルを|réserver|un hôtel||d’hôtel|
心配する|友達のことを|s’inquiéter|pour mon ami||||
質問する|先生に|poser|une question au professeur||de question|
電話する|友達に|téléphoner|à mon ami||||
掃除する|部屋を|nettoyer|ma chambre||||
洗濯する|週末に|faire|la lessive||||
料理する|夕食を|cuisiner|le dîner||||
旅行する|日本を|voyager|au Japon||||
結婚する|恋人と|se marier|avec ma compagne||||T
練習する|毎日ピアノを|s’entraîner|au piano||||
準備する|旅行の|préparer|le voyage||||
説明する|友達に|expliquer|la règle à mon ami||||
利用する|電車を|utiliser|le train||||
紹介する|友達を|présenter|mon ami||||
案内する|観光客を|guider|les touristes||||
出発する|八時に|partir|tôt le matin||||
到着する|空港に|arriver|à l’aéroport||||
注文する|ラーメンを|commander|un ramen||de ramen|
確認する|予約を|vérifier|la réservation||||
連絡する|友達に|contacter|mon ami||||
参加する|会議に|participer|à la réunion||||
相談する|先生に|demander|conseil au professeur||||
約束する|友達と|promettre|à mon ami de venir||||
招待する|友達を|inviter|mon ami à la fête||||
買い物する|デパートで|faire|des achats au grand magasin||d’achats||
"""
PATCH = """
来る|友達が家に|venir|chez moi|Mon ami|||D
生まれる|病院で赤ちゃんが|naître|à l’hôpital|Un bébé|||DE
死ぬ|魚が|mourir|dans l’aquarium|Le poisson|||DE
合う|この靴は|convenir|à mon pied|Cette chaussure|||E
似合う|そのコートは|aller|bien|Ce manteau|||EP
当たる|くじが|gagner|un prix||x||
決まる|予定が|être|décidé|Le programme|||E
済む|用事が|être|terminée|Mon affaire|||E
違う|この答えは|être|fausse|La réponse|||EP
見つかる|鍵が|être|retrouvée|La clé|||E
降る|雨が|pleuvoir||Il|||
晴れる|空が|se dégager||Le ciel|||E
曇る|空が|se couvrir|de nuages|Le ciel|||E
落ちる|りんごが|tomber|de l’arbre|Le fruit|||E
壊れる|おもちゃが|se casser||Le jouet|||E
咲く|桜が|fleurir|au printemps|Le cerisier|||
増える|観光客が|augmenter|chaque année|Le nombre de touristes|||E
上がる|物価が|monter|chaque année|Le prix|||E
光る|星が|briller|dans le ciel|Une étoile|||
売り切れる|チケットが|être|épuisé|Le billet|||E
建つ|新しい建物が|être|construit|Un nouveau bâtiment|||EP
延びる|予定が|être|reporté|Le rendez-vous|||EP
切れる|糸が|se couper||Le fil|||E
伝わる|気持ちが|être|compris|Le message|||E
温まる|部屋が|se réchauffer|doucement|La pièce*|||
積もる|雪が|s’accumuler|sur la route|La neige*|||
通る|橋を|emprunter|le pont||||
寄る|帰りに店に|faire|un saut au magasin||x||
立ち寄る|帰りに本屋に|faire|un détour par la librairie||x||
思う|日本は面白いと|trouver|le Japon intéressant|||ED
住む|東京に|habiter|à Tokyo||||U
持つ|かばんを|porter|un sac||x|U
結婚する|恋人と|se marier|avec ma compagne||||U
くれる|友達が私にプレゼントを|offrir|un cadeau pour moi|Mon ami|x||
遅れる|電車が|avoir|du retard|Le train|x||
出会う|旅行先で友達に|rencontrer|un ami en voyage||x||
疲れる|仕事で|être|fatigué|||ED
驚く|ニュースを聞いて|être|surpris|||ED
困る|道が分からなくて|être|embarrassé|||ED
酔う|電車で|avoir|mal au cœur|||ED
冷える|体が|avoir|froid|||ED
濡れる|雨で|être|mouillé|||ED
悲しむ|別れを|être|triste de la séparation|||ED
怖がる|犬を|avoir|peur des chiens|||ED
悩む|将来のことで|se tracasser|pour l’avenir||||D
起きる|早く|se lever|tôt||||
寝る|早く|se coucher|tôt||||
帰る|家へ|rentrer|chez moi||||
出る|家を|sortir|de la maison||||
走る|川の近くを|courir|près de la rivière||||
置く|机の上に本を|poser|le livre sur la table||||
洗濯する||faire|la lessive||||
準備する|夕食を|préparer|le dîner||||
出発する|朝早く|partir|tôt le matin|||E
始まる|九時に授業が|commencer|à neuf heures|Le cours|||E
終わる|六時に仕事が|finir|à six heures|Le travail|||E
開く|十時に店が|ouvrir|à dix heures|Le magasin|||E
閉まる|九時に店が|fermer|à neuf heures|Le magasin|||E
掛ける|友達に電話を|passer|un coup de fil à mon ami||x||
"""
import re as _re
def _norm(k, pre, fv, comp, subj, neg, o):
    # neg non vide : le complément est de type « un/des/du … » → forme négative automatique (de / d’)
    n = ''
    if neg:
        n = _re.sub(r'^(un|une|des|du)\s+', 'de ', comp)
        n = _re.sub(r'^de la\s+', 'de ', n)
        n = _re.sub(r'^de ([aeiouyhéèêâîôû])', r'd’\1', n)
        n = _re.sub(r'^de l’', 'd’', n)
    return {'p': pre, 'v': fv, 'c': comp, 's': subj, 'n': n, 'o': o}
def frames():
    out = {}
    for blk in (RAW, PATCH):
        for ln in blk.strip().splitlines():
            p = ln.split('|')
            p += [''] * (6 - len(p))
            k, pre, fv, comp, subj = p[:5]
            neg, o = '', ''
            for f in p[5:]:
                if _re.fullmatch('[EDPTU]+', f): o += f
                elif f: neg = f
            out[k] = _norm(k, pre, fv, comp, subj, neg, o)
    return out
