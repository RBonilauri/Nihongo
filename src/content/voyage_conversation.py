import os, sys
# -*- coding: utf-8 -*-
# Compléments : voyage, conversation, vocabulaire thématique, temps, géographie
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import T, P, N, H
import vocab_core as C2
from adjectifs_keigo import phr, sub, ktab, HAVE

VOY = {}
VOY['空港 — Aéroport et douane'] = ('À l’arrivée, au départ et en transit.', [
 ('Où est l’enregistrement ?', 'チェックインカウンターはどこですか。'), ('Voici mon passeport', 'パスポートです。'), ('Je suis ici pour du tourisme', '観光で来ました。'),
 ('Je reste une semaine', '一週間滞在します。'), ('Je loge à l’hôtel…', '〜ホテルに泊まります。'), ('Je n’ai rien à déclarer', '申告するものはありません。'),
 ('Où est la livraison des bagages ?', '荷物の受け取りはどこですか。'), ('Ma valise n’est pas arrivée', 'スーツケースが出てきません。'), ('Où est la porte d’embarquement ?', '搭乗口はどこですか。'),
 ('À quelle heure est l’embarquement ?', '搭乗は何時からですか。'), ('Mon vol est annulé', 'フライトがキャンセルになりました。'), ('Je voudrais changer de vol', '便を変更したいのですが。'),
 ('Où puis-je changer de l’argent ?', '両替はどこでできますか。'), ('Où est le train pour le centre-ville ?', '市内へ行く電車はどこですか。'), ('Où est la consigne ?', '荷物預かり所はどこですか。'),
 ('Où prendre le bus pour l’hôtel ?', 'ホテル行きのバスはどこから出ますか。'),
])
VOY['タクシー — Taxi'] = ('Pour se faire conduire sans parler beaucoup.', [
 ('Pouvez-vous m’emmener à cette adresse ?', 'この住所までお願いします。'), ('À la gare de Tokyo, s’il vous plaît', '東京駅までお願いします。'), ('Combien de temps faut-il ?', 'どのくらいかかりますか。'),
 ('C’est combien environ ?', 'いくらぐらいですか。'), ('Arrêtez-vous ici, s’il vous plaît', 'ここで止めてください。'), ('Tournez à gauche au feu', '次の信号を左に曲がってください。'),
 ('Pouvez-vous attendre ?', '待っていただけますか。'), ('Je peux payer par carte ?', 'カードで払えますか。'), ('Gardez la monnaie', 'お釣りはいりません。'),
 ('Ouvrez le coffre, s’il vous plaît', 'トランクを開けてください。'), ('Pourriez-vous m’aider avec mes bagages ?', '荷物を入れてもらえますか。'), ('Je suis pressé(e)', '急いでいます。'),
])
VOY['コンビニ — Konbini et supermarché'] = ('Les gestes et phrases de la caisse, dans les magasins ouverts 24 h.', [
 ('Voulez-vous un sac ?', '袋はご利用ですか。'), ('Je n’ai pas besoin de sac', '袋はいりません。'), ('Pouvez-vous le réchauffer ?', '温めてもらえますか。'),
 ('Des baguettes, s’il vous plaît', 'お箸をください。'), ('Où est le rayon des boissons ?', '飲み物はどこにありますか。'), ('Avez-vous un distributeur ?', 'ATMはありますか。'),
 ('Je voudrais payer en espèces', '現金で払います。'), ('Je paie par carte', 'カードでお願いします。'), ('C’est un cadeau (emballage)', 'プレゼント用に包んでください。'),
 ('Où sont les toilettes ?', 'お手洗いはどこですか。'), ('Avez-vous du Wi‑Fi gratuit ?', '無料のWi‑Fiはありますか。'), ('C’est en promotion ?', 'セール中ですか。'),
 ('Est-ce hors taxes ?', '免税できますか。'), ('Puis-je goûter ?', '試食してもいいですか。'), ('Ça se garde combien de temps ?', '賞味期限はいつまでですか。'),
])
VOY['銀行・郵便 — Banque, poste et colis'] = ('Pour l’argent, le courrier et les envois.', [
 ('Je voudrais changer des euros en yens', 'ユーロを円に両替したいです。'), ('Quel est le taux de change ?', '為替レートはいくらですか。'), ('Où est le distributeur ?', 'ATMはどこですか。'),
 ('Ma carte est avalée', 'カードが出てきません。'), ('Je voudrais retirer de l’argent', 'お金をおろしたいです。'), ('Je voudrais envoyer ce colis en France', 'この荷物をフランスに送りたいです。'),
 ('Combien de temps ça met ?', 'どのくらいかかりますか。'), ('Par avion ou par bateau ?', '航空便ですか、船便ですか。'), ('Combien coûte un timbre pour la France ?', 'フランスまで切手はいくらですか。'),
 ('Je voudrais envoyer ceci par coursier', 'これを宅配便で送りたいです。'), ('Pouvez-vous écrire l’adresse ?', '住所を書いてください。'), ('Je voudrais un reçu', '領収書をください。'),
 ('Remplissez ce formulaire', 'この用紙に記入してください。'),
])
VOY['携帯・ネット — Téléphone, SIM et Wi‑Fi'] = ('Pour rester connecté pendant le voyage.', [
 ('Où acheter une carte SIM ?', 'SIMカードはどこで買えますか。'), ('Quel est le mot de passe du Wi‑Fi ?', 'Wi‑Fiのパスワードは何ですか。'), ('Ma batterie est presque vide', 'バッテリーがもうすぐなくなります。'),
 ('Puis-je charger mon téléphone ici ?', 'ここで充電してもいいですか。'), ('Pouvez-vous me prêter un chargeur ?', '充電器を貸してもらえますか。'), ('Le signal est mauvais', '電波が悪いです。'),
 ('Pouvez-vous m’appeler un taxi ?', 'タクシーを呼んでもらえますか。'), ('Pouvez-vous prendre une photo de nous ?', '写真を撮ってもらえますか。'), ('Je peux photographier ?', '写真を撮ってもいいですか。'),
 ('Je voudrais louer un pocket Wi‑Fi', 'ポケットWi‑Fiを借りたいです。'), ('J’ai perdu mon téléphone', '携帯電話をなくしました。'), ('Comment on dit… en japonais ?', '〜は日本語で何と言いますか。'),
 ('Pouvez-vous le traduire ?', '翻訳してもらえますか。'),
])
VOY['病院・薬局 — Médecin et pharmacie'] = ('Complète « Urgences et santé » pour une consultation ordinaire.', [
 ('Je ne me sens pas bien', '体の調子が悪いです。'), ('J’ai de la fièvre', '熱があります。'), ('J’ai mal à la tête', '頭が痛いです。'),
 ('J’ai mal au ventre', 'お腹が痛いです。'), ('J’ai la nausée', '吐き気がします。'), ('J’ai la diarrhée', '下痢をしています。'),
 ('Je tousse beaucoup', '咳がよく出ます。'), ('J’ai mal à la gorge', '喉が痛いです。'), ('Je suis allergique à…', '〜アレルギーがあります。'),
 ('Depuis quand avez-vous ces symptômes ?', 'いつから症状がありますか。'), ('Je prends ces médicaments', 'この薬を飲んでいます。'), ('Avez-vous une assurance ?', '保険に入っていますか。'),
 ('Pouvez-vous me prescrire un médicament ?', '薬を出してもらえますか。'), ('Combien de fois par jour ?', '一日何回飲みますか。'), ('Avant ou après le repas ?', '食前ですか、食後ですか。'),
 ('Je voudrais un médicament contre le rhume', '風邪薬がほしいです。'), ('Je suis enceinte', '妊娠しています。'),
])
VOY['観光 — Visites, billets et photos'] = ('Musées, temples, châteaux et attractions.', [
 ('Un billet adulte, s’il vous plaît', '大人一枚お願いします。'), ('Deux entrées, s’il vous plaît', '二枚ください。'), ('Quelles sont les heures d’ouverture ?', '営業時間は何時から何時までですか。'),
 ('À quelle heure ferme-t-on ?', '何時に閉まりますか。'), ('Y a-t-il une visite guidée ?', 'ガイドツアーはありますか。'), ('Y a-t-il un guide en anglais ?', '英語のガイドはいますか。'),
 ('Est-ce qu’il y a un tarif étudiant ?', '学生割引はありますか。'), ('Où est l’entrée ?', '入口はどこですか。'), ('Y a-t-il un plan en français ?', 'フランス語の地図はありますか。'),
 ('C’est interdit de photographier ?', '撮影禁止ですか。'), ('Où est la sortie ?', '出口はどこですか。'), ('C’est ouvert le lundi ?', '月曜日は開いていますか。'),
 ('Combien de temps faut-il pour la visite ?', '見学にどのくらいかかりますか。'), ('Je voudrais réserver une visite', '見学を予約したいです。'), ('Où est le meilleur point de vue ?', '一番いい景色が見える場所はどこですか。'),
 ('Comment prier au temple ?', 'お参りの仕方を教えてください。'), ('Je voudrais un omamori (porte-bonheur)', 'お守りをください。'),
])
VOY['居酒屋・カラオケ — Izakaya, bar et karaoké'] = ('Sortir le soir : commander, trinquer, chanter.', [
 ('Une table pour trois personnes', '三名です。'), ('Pouvons-nous nous asseoir au comptoir ?', 'カウンター席でもいいですか。'), ('Une bière pression pour commencer', 'とりあえず生ビールをお願いします。'),
 ('Santé !', '乾杯！'), ('Que recommandez-vous ?', 'おすすめは何ですか。'), ('Un autre, s’il vous plaît', 'もう一杯お願いします。'),
 ('Je voudrais de l’eau', 'お水をください。'), ('C’est une formule à volonté (nomihōdai) ?', '飲み放題ですか。'), ('Pouvons-nous partager ?', 'シェアしてもいいですか。'),
 ('Pouvez-vous nous apporter l’addition ?', 'お会計をお願いします。'), ('On paie séparément', '別々でお願いします。'), ('C’est moi qui offre', '私がおごります。'),
 ('Pour combien de temps le karaoké ?', '何時間ですか。'), ('Quelle chanson voulez-vous chanter ?', '何を歌いますか。'), ('Je ne chante pas bien', '歌が下手です。'),
 ('Je ne bois pas d’alcool', 'お酒は飲めません。'),
])
VOY['道案内 — Demander et comprendre son chemin'] = ('Pour trouver un lieu et comprendre les indications.', [
 ('Excusez-moi, où est… ?', 'すみません、〜はどこですか。'), ('Je cherche la gare', '駅を探しています。'), ('C’est loin d’ici ?', 'ここから遠いですか。'),
 ('Combien de minutes à pied ?', '歩いて何分ですか。'), ('Allez tout droit', 'まっすぐ行ってください。'), ('Tournez à droite au feu', '信号を右に曲がってください。'),
 ('C’est au coin', '角にあります。'), ('C’est en face de la banque', '銀行の向かいにあります。'), ('C’est à côté du konbini', 'コンビニの隣にあります。'),
 ('C’est derrière l’immeuble', 'ビルの後ろにあります。'), ('Traversez la rue', '道を渡ってください。'), ('Prenez la deuxième rue à gauche', '二つ目の角を左に曲がってください。'),
 ('Pouvez-vous me le montrer sur la carte ?', '地図で見せてもらえますか。'), ('Je suis perdu(e)', '道に迷いました。'), ('Quelle est la station la plus proche ?', '一番近い駅はどこですか。'),
 ('C’est par là ?', 'こちらですか。'), ('Vous pouvez y aller à pied', '歩いて行けます。'),
])
VOY['予約 — Réserver, annuler, confirmer'] = ('Au téléphone ou sur place : hôtel, restaurant, spectacle, train.', [
 ('Je voudrais réserver pour ce soir', '今夜予約したいのですが。'), ('Pour deux personnes à 19 h', '二名で七時にお願いします。'), ('Au nom de Dupont', 'デュポンの名前でお願いします。'),
 ('Avez-vous de la place demain ?', '明日、空いていますか。'), ('Je voudrais annuler ma réservation', '予約をキャンセルしたいです。'), ('Je voudrais changer la date', '日付を変更したいです。'),
 ('C’est complet ?', '満席ですか。'), ('Y a-t-il des frais d’annulation ?', 'キャンセル料はかかりますか。'), ('Je voudrais une chambre non-fumeur', '禁煙の部屋をお願いします。'),
 ('Pouvez-vous envoyer une confirmation ?', '確認のメールをいただけますか。'), ('Nous serons en retard de 30 minutes', '三十分遅れます。'), ('Je voudrais réserver une place côté fenêtre', '窓側の席を予約したいです。'),
 ('Je voudrais réserver un billet de Shinkansen', '新幹線の切符を予約したいです。'),
])
VOY['洗濯・生活 — Lessive, laverie et petits services'] = ('Vie pratique pendant un long séjour.', [
 ('Où est la laverie ?', 'コインランドリーはどこですか。'), ('Comment fonctionne cette machine ?', 'この機械の使い方を教えてください。'), ('Combien de temps pour le séchage ?', '乾燥にどのくらいかかりますか。'),
 ('Pouvez-vous faire le pressing ?', 'クリーニングをお願いできますか。'), ('Quand sera-ce prêt ?', 'いつできますか。'), ('Je voudrais un autre oreiller', '枕をもう一つください。'),
 ('Pouvez-vous nettoyer la chambre ?', '部屋を掃除してもらえますか。'), ('Je n’ai pas d’eau chaude', 'お湯が出ません。'), ('La climatisation ne marche pas', 'エアコンが動きません。'),
 ('Où jeter les ordures ?', 'ごみはどこに捨てますか。'), ('Y a-t-il un sèche-cheveux ?', 'ドライヤーはありますか。'), ('Le bruit est trop fort', '音がうるさいです。'),
])
VOY['祭り・行事 — Fêtes, festivals et saisons'] = ('Pour comprendre et parler des événements japonais.', [
 ('Il y a un festival aujourd’hui ?', '今日はお祭りがありますか。'), ('C’est à quelle heure ?', '何時からですか。'), ('Les cerisiers sont-ils en fleur ?', '桜は咲いていますか。'),
 ('Quand est la meilleure période pour les feuilles rouges ?', '紅葉はいつがきれいですか。'), ('Je voudrais voir un feu d’artifice', '花火を見たいです。'), ('Je voudrais mettre un yukata', '浴衣を着てみたいです。'),
 ('Où acheter un omikuji (oracle) ?', 'おみくじはどこで引けますか。'), ('Qu’est-ce que c’est que ce plat de fête ?', 'この行事の食べ物は何ですか。'), ('C’est une tradition ancienne', '古い伝統です。'),
 ('On fait un pique-nique sous les cerisiers', 'お花見をします。'), ('Il y a beaucoup de monde', '人がたくさんいます。'), ('Je voudrais faire un vœu', 'お願いごとをします。'),
])

CONV = {}
CONV['世間話 — Parler de tout et de rien'] = ('Les sujets qui lancent une conversation avec un inconnu.', [
 ('Il fait beau aujourd’hui, n’est-ce pas ?', '今日はいい天気ですね。'), ('Il fait vraiment chaud', '本当に暑いですね。'), ('Il pleut beaucoup ces temps-ci', '最近、雨が多いですね。'),
 ('Vous habitez par ici ?', 'この近くにお住まいですか。'), ('Vous travaillez dans quoi ?', 'お仕事は何をされていますか。'), ('Vous avez des frères et sœurs ?', 'ご兄弟はいますか。'),
 ('J’adore la cuisine japonaise', '日本料理が大好きです。'), ('C’est ma première fois au Japon', '日本は初めてです。'), ('Vous parlez très bien japonais !', '日本語がお上手ですね。'),
 ('Je suis encore débutant', 'まだまだ初心者です。'), ('Ça fait un mois que j’apprends', '一か月前から勉強しています。'), ('Quel est votre plat préféré ?', '好きな食べ物は何ですか。'),
 ('Vous avez voyagé en France ?', 'フランスに行ったことがありますか。'), ('Votre week-end s’est bien passé ?', '週末はどうでしたか。'),
])
CONV['意見 — Donner son avis, être d’accord ou non'] = ('Exprimer opinion, nuance et désaccord poliment.', [
 ('À mon avis…', '私の意見では、〜です。'), ('Je pense que c’est bien', 'いいと思います。'), ('Je ne pense pas que…', '〜とは思いません。'),
 ('Je suis tout à fait d’accord', '全くその通りだと思います。'), ('Je suis d’accord avec vous', 'あなたに賛成です。'), ('Je ne suis pas d’accord', '私は反対です。'),
 ('C’est un peu différent', 'ちょっと違うと思います。'), ('Je comprends, mais…', 'わかりますが、〜。'), ('Ça dépend des cas', '場合によります。'),
 ('C’est intéressant', '面白いですね。'), ('C’est difficile à dire', '難しいですね。'), ('Je n’ai pas d’opinion', '特に意見はありません。'),
 ('Je préfère le thé au café', 'コーヒーより紅茶のほうが好きです。'), ('Les deux sont bien', 'どちらもいいですね。'), ('C’est une bonne idée', 'それはいい考えですね。'),
])
CONV['聞き返す — Faire répéter, clarifier'] = ('Pour ne pas rester bloqué quand on ne comprend pas.', [
 ('Pardon ?', 'えっ？'), ('Pouvez-vous répéter ?', 'もう一度お願いします。'), ('Pouvez-vous parler plus lentement ?', 'もう少しゆっくり話してください。'),
 ('Je n’ai pas compris', 'わかりませんでした。'), ('Qu’est-ce que ça veut dire ?', 'どういう意味ですか。'), ('Comment ça s’écrit ?', 'どう書きますか。'),
 ('Pouvez-vous l’écrire ?', '書いてもらえますか。'), ('Comment on prononce ce kanji ?', 'この漢字はどう読みますか。'), ('Je ne connais pas ce mot', 'この言葉を知りません。'),
 ('Vous voulez dire… ?', '〜ということですか。'), ('Est-ce correct ?', 'これで合っていますか。'), ('Pouvez-vous le dire en anglais ?', '英語で言ってもらえますか。'),
 ('Je ne parle pas bien le japonais', '日本語があまり話せません。'), ('Pouvez-vous m’expliquer simplement ?', '簡単に説明してもらえますか。'),
])
CONV['褒める・感謝 — Compliments, remerciements, excuses'] = ('Pour être chaleureux et poli.', [
 ('C’est délicieux !', 'とてもおいしいです。'), ('C’est magnifique !', '素晴らしいですね。'), ('Votre maison est très belle', 'すてきなお宅ですね。'),
 ('Merci beaucoup pour tout', 'いろいろありがとうございます。'), ('Merci de votre accueil', 'おもてなしありがとうございました。'), ('Je vous suis très reconnaissant(e)', 'とても感謝しています。'),
 ('Je suis désolé(e) de vous avoir dérangé', 'ご迷惑をおかけしてすみません。'), ('Pardonnez-moi', '申し訳ありません。'), ('Ce n’est pas grave', '気にしないでください。'),
 ('Ce n’est rien', 'どういたしまして。'), ('Excusez mon impolitesse', '失礼しました。'), ('Merci pour le cadeau', 'プレゼントをありがとうございます。'),
 ('Ça me fait très plaisir', 'とても嬉しいです。'), ('Vous êtes très gentil', 'ご親切にありがとうございます。'),
])
CONV['誘う — Inviter, accepter, refuser'] = ('Proposer une sortie et répondre sans froisser.', [
 ('Voulez-vous dîner ensemble ?', '一緒に夕食を食べませんか。'), ('Vous êtes libre samedi ?', '土曜日は空いていますか。'), ('Allons au cinéma', '映画を見に行きましょう。'),
 ('Ça vous dit de venir ?', '行きませんか。'), ('Avec plaisir !', 'ぜひ行きたいです。'), ('Hélas, je ne suis pas libre ce jour-là', 'あいにくその日は都合が悪いです。'),
 ('Une autre fois, peut-être', 'また今度お願いします。'), ('Où et à quelle heure ?', 'どこで何時ですか。'), ('On se retrouve devant la gare', '駅の前で会いましょう。'),
 ('J’invite', '私がご馳走します。'), ('Je vais voir', '考えておきます。'), ('Merci de l’invitation', 'お誘いありがとうございます。'),
 ('Je regrette de ne pas pouvoir venir', '行けなくて残念です。'), ('Prévenez-moi', '知らせてください。'),
])
CONV['自分のこと — Parler de soi et de la France'] = ('Présenter son quotidien, ses goûts, son pays.', [
 ('Je viens de France', 'フランスから来ました。'), ('Je vis à Paris', 'パリに住んでいます。'), ('Je suis ingénieur', 'エンジニアです。'),
 ('Je travaille dans l’informatique', 'IT関係の仕事をしています。'), ('J’apprends le japonais depuis un an', '一年前から日本語を勉強しています。'), ('Mon rêve est de parler japonais', '日本語が話せるようになるのが夢です。'),
 ('Paris est une grande ville', 'パリは大きい町です。'), ('La France est célèbre pour le vin', 'フランスはワインで有名です。'), ('Le fromage français est très bon', 'フランスのチーズはとてもおいしいです。'),
 ('J’adore cuisiner', '料理をするのが好きです。'), ('Je joue du piano', 'ピアノを弾きます。'), ('J’ai un chat', '猫を飼っています。'),
 ('Je suis allé(e) à Kyoto l’année dernière', '去年、京都に行きました。'), ('J’ai l’intention de revenir au Japon', 'また日本に来るつもりです。'),
])
CONV['電話 — Au téléphone'] = ('Pour téléphoner sans voir l’interlocuteur.', [
 ('Allô ?', 'もしもし。'), ('Ici M. Dupont', 'デュポンです。'), ('Puis-je parler à M. Sato ?', '佐藤さんをお願いします。'),
 ('Un instant, s’il vous plaît', '少々お待ちください。'), ('Il n’est pas là', '今おりません。'), ('Voulez-vous laisser un message ?', 'ご伝言はありますか。'),
 ('Je rappelle plus tard', 'またかけ直します。'), ('Vous vous êtes trompé de numéro', '番号が違います。'), ('Pouvez-vous parler plus fort ?', '少しお声が遠いです。'),
 ('La ligne est mauvaise', '電話の調子が悪いです。'), ('Pouvez-vous me rappeler ?', 'かけ直してもらえますか。'), ('Merci de votre appel', 'お電話ありがとうございました。'),
])

def voy_conv_subs():
    v = [sub(t, i[0], [phr(i[1])]) for t, i in VOY.items()]
    c = [sub(t, i[0], [phr(i[1])]) for t, i in CONV.items()]
    return {'旅行': v, '会話': c}
