import os, sys
# -*- coding: utf-8 -*-
# Compléments : vocabulaire thématique, temps, géographie, culture
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import T, P, N, H
import vocab_core as C2
from adjectifs_keigo import phr, sub, ktab, HAVE

ECOLE = [
 ('授業', 'じゅぎょう', 'Cours, leçon'), ('宿題', 'しゅくだい', 'Devoirs'), ('試験', 'しけん', 'Examen'), ('成績', 'せいせき', 'Résultats scolaires'), ('先輩', 'せんぱい', 'Aîné (école, travail)'),
 ('後輩', 'こうはい', 'Cadet, junior'), ('同級生', 'どうきゅうせい', 'Camarade de classe'), ('留学生', 'りゅうがくせい', 'Étudiant étranger'), ('教科書', 'きょうかしょ', 'Manuel scolaire'), ('黒板', 'こくばん', 'Tableau noir'),
 ('図書館', 'としょかん', 'Bibliothèque'), ('入学', 'にゅうがく', 'Entrée à l’école'), ('卒業', 'そつぎょう', 'Fin d’études, diplôme'), ('専攻', 'せんこう', 'Spécialité'), ('論文', 'ろんぶん', 'Mémoire, article'),
 ('会議', 'かいぎ', 'Réunion'), ('資料', 'しりょう', 'Documents'), ('書類', 'しょるい', 'Dossier, papiers'), ('上司', 'じょうし', 'Supérieur'), ('部下', 'ぶか', 'Subordonné'),
 ('同僚', 'どうりょう', 'Collègue'), ('社長', 'しゃちょう', 'Président (société)'), ('部長', 'ぶちょう', 'Chef de service'), ('課長', 'かちょう', 'Chef de section'), ('社員', 'しゃいん', 'Employé'),
 ('給料', 'きゅうりょう', 'Salaire'), ('残業', 'ざんぎょう', 'Heures supplémentaires'), ('出張', 'しゅっちょう', 'Déplacement professionnel'), ('休暇', 'きゅうか', 'Congé'), ('面接', 'めんせつ', 'Entretien d’embauche'),
 ('履歴書', 'りれきしょ', 'CV'), ('契約', 'けいやく', 'Contrat'), ('取引先', 'とりひきさき', 'Partenaire commercial'), ('名刺', 'めいし', 'Carte de visite'), ('締め切り', 'しめきり', 'Date limite'),
 ('予算', 'よさん', 'Budget'), ('売上', 'うりあげ', 'Chiffre d’affaires'), ('会社員', 'かいしゃいん', 'Salarié'), ('アルバイト', 'アルバイト', 'Job étudiant, temps partiel'), ('在宅勤務', 'ざいたくきんむ', 'Télétravail'),
]
SHIZEN = [
 ('山脈', 'さんみゃく', 'Chaîne de montagnes'), ('火山', 'かざん', 'Volcan'), ('滝', 'たき', 'Cascade'), ('森', 'もり', 'Forêt'), ('砂浜', 'すなはま', 'Plage de sable'), ('海岸', 'かいがん', 'Côte'),
 ('湖', 'みずうみ', 'Lac'), ('島', 'しま', 'Île'), ('半島', 'はんとう', 'Péninsule'), ('谷', 'たに', 'Vallée'), ('丘', 'おか', 'Colline'), ('草原', 'そうげん', 'Prairie'),
 ('砂漠', 'さばく', 'Désert'), ('温泉', 'おんせん', 'Source thermale'), ('洞窟', 'どうくつ', 'Grotte'), ('崖', 'がけ', 'Falaise'), ('岩', 'いわ', 'Rocher'), ('石', 'いし', 'Pierre'),
 ('土', 'つち', 'Terre, sol'), ('砂', 'すな', 'Sable'), ('泥', 'どろ', 'Boue'), ('波', 'なみ', 'Vague'), ('潮', 'しお', 'Marée, eau de mer'), ('風景', 'ふうけい', 'Paysage'),
 ('景色', 'けしき', 'Vue, panorama'), ('自然', 'しぜん', 'Nature'), ('環境', 'かんきょう', 'Environnement'), ('地震', 'じしん', 'Séisme'), ('津波', 'つなみ', 'Tsunami'), ('台風', 'たいふう', 'Typhon'),
 ('雷', 'かみなり', 'Tonnerre, foudre'), ('虹', 'にじ', 'Arc-en-ciel'), ('霧', 'きり', 'Brouillard'), ('露', 'つゆ', 'Rosée'), ('朝焼け', 'あさやけ', 'Aube rougeoyante'), ('夕焼け', 'ゆうやけ', 'Crépuscule rougeoyant'),
 ('桜', 'さくら', 'Cerisier'), ('紅葉', 'もみじ', 'Érable, feuilles rouges'), ('竹', 'たけ', 'Bambou'), ('松', 'まつ', 'Pin'), ('梅', 'うめ', 'Prunier japonais'),
]
SPORT = [
 ('運動', 'うんどう', 'Exercice, sport'), ('試合', 'しあい', 'Match'), ('選手', 'せんしゅ', 'Joueur, athlète'), ('チーム', 'チーム', 'Équipe'), ('応援', 'おうえん', 'Encouragement, soutien'), ('勝つ', 'かつ', 'Gagner'),
 ('負ける', 'まける', 'Perdre'), ('引き分け', 'ひきわけ', 'Match nul'), ('野球', 'やきゅう', 'Baseball'), ('サッカー', 'サッカー', 'Football'), ('テニス', 'テニス', 'Tennis'), ('水泳', 'すいえい', 'Natation'),
 ('柔道', 'じゅうどう', 'Judo'), ('空手', 'からて', 'Karaté'), ('剣道', 'けんどう', 'Kendo'), ('相撲', 'すもう', 'Sumo'), ('マラソン', 'マラソン', 'Marathon'), ('スキー', 'スキー', 'Ski'),
 ('スノーボード', 'スノーボード', 'Snowboard'), ('登山', 'とざん', 'Alpinisme'), ('ジョギング', 'ジョギング', 'Jogging'), ('ヨガ', 'ヨガ', 'Yoga'), ('ゴルフ', 'ゴルフ', 'Golf'), ('卓球', 'たっきゅう', 'Tennis de table'),
 ('バスケットボール', 'バスケットボール', 'Basket-ball'), ('バレーボール', 'バレーボール', 'Volley-ball'), ('自転車', 'じてんしゃ', 'Vélo'), ('体操', 'たいそう', 'Gymnastique'), ('練習', 'れんしゅう', 'Entraînement'), ('優勝', 'ゆうしょう', 'Victoire (championnat)'),
]
MUSIQUE = [
 ('音楽', 'おんがく', 'Musique'), ('歌手', 'かしゅ', 'Chanteur'), ('曲', 'きょく', 'Morceau'), ('歌詞', 'かし', 'Paroles'), ('楽器', 'がっき', 'Instrument'), ('ギター', 'ギター', 'Guitare'),
 ('ピアノ', 'ピアノ', 'Piano'), ('ドラム', 'ドラム', 'Batterie'), ('コンサート', 'コンサート', 'Concert'), ('映画', 'えいが', 'Film'), ('監督', 'かんとく', 'Réalisateur'), ('俳優', 'はいゆう', 'Acteur'),
 ('女優', 'じょゆう', 'Actrice'), ('漫画', 'まんが', 'Manga'), ('アニメ', 'アニメ', 'Anime'), ('小説', 'しょうせつ', 'Roman'), ('雑誌', 'ざっし', 'Magazine'), ('新聞', 'しんぶん', 'Journal'),
 ('ニュース', 'ニュース', 'Informations'), ('番組', 'ばんぐみ', 'Émission'), ('絵', 'え', 'Dessin, tableau'), ('写真', 'しゃしん', 'Photo'), ('芸術', 'げいじゅつ', 'Art'), ('展覧会', 'てんらんかい', 'Exposition'),
 ('劇場', 'げきじょう', 'Théâtre'), ('歌舞伎', 'かぶき', 'Kabuki'), ('能', 'のう', 'Théâtre nô'), ('落語', 'らくご', 'Conte comique rakugo'), ('書道', 'しょどう', 'Calligraphie'), ('茶道', 'さどう', 'Cérémonie du thé'),
]
IT = [
 ('携帯電話', 'けいたいでんわ', 'Téléphone portable'), ('スマホ', 'スマホ', 'Smartphone'), ('パソコン', 'パソコン', 'Ordinateur'), ('画面', 'がめん', 'Écran'), ('充電', 'じゅうでん', 'Charge'), ('電池', 'でんち', 'Pile, batterie'),
 ('電源', 'でんげん', 'Alimentation'), ('インターネット', 'インターネット', 'Internet'), ('メール', 'メール', 'E-mail'), ('アプリ', 'アプリ', 'Application'), ('ウェブサイト', 'ウェブサイト', 'Site web'), ('検索', 'けんさく', 'Recherche'),
 ('パスワード', 'パスワード', 'Mot de passe'), ('ログイン', 'ログイン', 'Connexion'), ('ダウンロード', 'ダウンロード', 'Téléchargement'), ('ファイル', 'ファイル', 'Fichier'), ('保存', 'ほぞん', 'Enregistrer'), ('削除', 'さくじょ', 'Supprimer'),
 ('送信', 'そうしん', 'Envoi'), ('受信', 'じゅしん', 'Réception'), ('添付', 'てんぷ', 'Pièce jointe'), ('返信', 'へんしん', 'Réponse (message)'), ('通話', 'つうわ', 'Appel'), ('留守番電話', 'るすばんでんわ', 'Répondeur'),
 ('カメラ', 'カメラ', 'Appareil photo'), ('動画', 'どうが', 'Vidéo'), ('音量', 'おんりょう', 'Volume'), ('設定', 'せってい', 'Réglages'), ('接続', 'せつぞく', 'Connexion (réseau)'), ('電波', 'でんぱ', 'Signal, ondes'),
 ('無料', 'むりょう', 'Gratuit'), ('有料', 'ゆうりょう', 'Payant'), ('利用', 'りよう', 'Utilisation'), ('登録', 'とうろく', 'Inscription'), ('個人情報', 'こじんじょうほう', 'Données personnelles'),
]
CUISINE = [
 ('包丁', 'ほうちょう', 'Couteau de cuisine'), ('まな板', 'まないた', 'Planche à découper'), ('鍋', 'なべ', 'Casserole, marmite'), ('フライパン', 'フライパン', 'Poêle'), ('炊飯器', 'すいはんき', 'Cuiseur à riz'), ('電子レンジ', 'でんしレンジ', 'Micro-ondes'),
 ('冷蔵庫', 'れいぞうこ', 'Réfrigérateur'), ('皿', 'さら', 'Assiette'), ('茶碗', 'ちゃわん', 'Bol à riz'), ('箸', 'はし', 'Baguettes'), ('スプーン', 'スプーン', 'Cuillère'), ('フォーク', 'フォーク', 'Fourchette'),
 ('ナイフ', 'ナイフ', 'Couteau (table)'), ('コップ', 'コップ', 'Verre'), ('醤油', 'しょうゆ', 'Sauce soja'), ('味噌', 'みそ', 'Miso'), ('砂糖', 'さとう', 'Sucre'), ('塩', 'しお', 'Sel'),
 ('酢', 'す', 'Vinaigre'), ('胡椒', 'こしょう', 'Poivre'), ('油', 'あぶら', 'Huile'), ('出汁', 'だし', 'Bouillon dashi'), ('味', 'あじ', 'Goût'), ('味付け', 'あじつけ', 'Assaisonnement'),
 ('切る', 'きる', 'Couper'), ('焼く', 'やく', 'Griller'), ('煮る', 'にる', 'Mijoter'), ('茹でる', 'ゆでる', 'Bouillir'), ('揚げる', 'あげる', 'Frire'), ('炒める', 'いためる', 'Faire sauter'),
 ('蒸す', 'むす', 'Cuire à la vapeur'), ('混ぜる', 'まぜる', 'Mélanger'), ('加える', 'くわえる', 'Ajouter'), ('材料', 'ざいりょう', 'Ingrédients'), ('分量', 'ぶんりょう', 'Quantité'), ('レシピ', 'レシピ', 'Recette'),
 ('弱火', 'よわび', 'Feu doux'), ('強火', 'つよび', 'Feu vif'), ('中火', 'ちゅうび', 'Feu moyen'),
]
QUANT = [
 ('全部', 'ぜんぶ', 'Tout'), ('半分', 'はんぶん', 'Moitié'), ('少し', 'すこし', 'Un peu'), ('たくさん', 'たくさん', 'Beaucoup'), ('ちょっと', 'ちょっと', 'Un peu, un instant'), ('全然', 'ぜんぜん', 'Pas du tout (avec négatif)'),
 ('大体', 'だいたい', 'À peu près'), ('約', 'やく', 'Environ'), ('ほとんど', 'ほとんど', 'Presque tout'), ('ぜひ', 'ぜひ', 'Absolument, sans faute'), ('全体', 'ぜんたい', 'Ensemble'), ('部分', 'ぶぶん', 'Partie'),
 ('一部', 'いちぶ', 'Une partie'), ('残り', 'のこり', 'Reste'), ('合計', 'ごうけい', 'Total'), ('平均', 'へいきん', 'Moyenne'), ('割合', 'わりあい', 'Proportion'), ('パーセント', 'パーセント', 'Pour cent'),
 ('倍', 'ばい', 'Fois, double'), ('以上', 'いじょう', 'Au moins, plus de'), ('以下', 'いか', 'Au plus, moins de'), ('未満', 'みまん', 'Moins de (strict)'), ('以内', 'いない', 'En moins de, dans la limite'), ('ずつ', 'ずつ', 'Chacun, par'),
 ('余り', 'あまり', 'Reste, pas très'), ('足りる', 'たりる', 'Suffire'), ('十分', 'じゅうぶん', 'Suffisamment'), ('多め', 'おおめ', 'Un peu plus que d’habitude'), ('少なめ', 'すくなめ', 'Un peu moins'), ('同じ', 'おなじ', 'Même'),
]
RELATION = [
 ('恋人', 'こいびと', 'Petit(e) ami(e)'), ('彼氏', 'かれし', 'Petit ami'), ('彼女', 'かのじょ', 'Petite amie, elle'), ('夫婦', 'ふうふ', 'Couple marié'), ('主人', 'しゅじん', 'Mon mari'), ('家内', 'かない', 'Mon épouse'),
 ('義父', 'ぎふ', 'Beau-père'), ('義母', 'ぎぼ', 'Belle-mère'), ('孫', 'まご', 'Petit-enfant'), ('親戚', 'しんせき', 'Parent (famille élargie)'), ('従兄弟', 'いとこ', 'Cousin'), ('叔父', 'おじ', 'Oncle'),
 ('叔母', 'おば', 'Tante'), ('甥', 'おい', 'Neveu'), ('姪', 'めい', 'Nièce'), ('双子', 'ふたご', 'Jumeaux'), ('隣人', 'りんじん', 'Voisin'), ('近所', 'きんじょ', 'Voisinage'),
 ('知り合い', 'しりあい', 'Connaissance'), ('親友', 'しんゆう', 'Meilleur ami'), ('客', 'きゃく', 'Client, invité'), ('大家', 'おおや', 'Propriétaire (logement)'), ('同居', 'どうきょ', 'Cohabitation'), ('留守', 'るす', 'Absence'),
 ('お見合い', 'おみあい', 'Rencontre arrangée'), ('結婚式', 'けっこんしき', 'Mariage (cérémonie)'), ('葬式', 'そうしき', 'Funérailles'), ('誕生日', 'たんじょうび', 'Anniversaire'), ('お祝い', 'おいわい', 'Célébration, cadeau'), ('プレゼント', 'プレゼント', 'Cadeau'),
]
MAGASIN = [
 ('売り場', 'うりば', 'Rayon'), ('レジ', 'レジ', 'Caisse'), ('試着室', 'しちゃくしつ', 'Cabine d’essayage'), ('サイズ', 'サイズ', 'Taille'), ('色違い', 'いろちがい', 'Autre couleur'), ('割引', 'わりびき', 'Remise'),
 ('値段', 'ねだん', 'Prix'), ('税込', 'ぜいこみ', 'Taxe incluse'), ('税抜', 'ぜいぬき', 'Hors taxe'), ('免税', 'めんぜい', 'Détaxe'), ('領収書', 'りょうしゅうしょ', 'Reçu'), ('レシート', 'レシート', 'Ticket de caisse'),
 ('返品', 'へんぴん', 'Retour de marchandise'), ('交換', 'こうかん', 'Échange'), ('在庫', 'ざいこ', 'Stock'), ('新商品', 'しんしょうひん', 'Nouveau produit'), ('限定', 'げんてい', 'Édition limitée'), ('お土産', 'おみやげ', 'Souvenir'),
 ('包装', 'ほうそう', 'Emballage'), ('袋', 'ふくろ', 'Sac'), ('会計', 'かいけい', 'Paiement, addition'), ('現金', 'げんきん', 'Espèces'), ('小銭', 'こぜに', 'Petite monnaie'), ('お釣り', 'おつり', 'Monnaie rendue'),
 ('ポイントカード', 'ポイントカード', 'Carte de fidélité'), ('営業時間', 'えいぎょうじかん', 'Horaires'), ('定休日', 'ていきゅうび', 'Jour de fermeture'), ('開店', 'かいてん', 'Ouverture'), ('閉店', 'へいてん', 'Fermeture'), ('セール', 'セール', 'Soldes'),
]
BAGAGE = [
 ('荷物', 'にもつ', 'Bagages'), ('切符', 'きっぷ', 'Billet'), ('改札', 'かいさつ', 'Portillon'), ('ホーム', 'ホーム', 'Quai'), ('乗り換え', 'のりかえ', 'Correspondance'), ('終電', 'しゅうでん', 'Dernier train'),
 ('始発', 'しはつ', 'Premier train'), ('各駅停車', 'かくえきていしゃ', 'Omnibus'), ('急行', 'きゅうこう', 'Express'), ('特急', 'とっきゅう', 'Rapide limité'), ('新幹線', 'しんかんせん', 'Shinkansen'), ('指定席', 'していせき', 'Place réservée'),
 ('自由席', 'じゆうせき', 'Place libre'), ('片道', 'かたみち', 'Aller simple'), ('往復', 'おうふく', 'Aller-retour'), ('定期券', 'ていきけん', 'Abonnement'), ('運賃', 'うんちん', 'Tarif du transport'), ('遅れ', 'おくれ', 'Retard'),
 ('運休', 'うんきゅう', 'Suspension de service'), ('出発', 'しゅっぱつ', 'Départ'), ('到着', 'とうちゃく', 'Arrivée'), ('時刻表', 'じこくひょう', 'Horaires de train'), ('路線図', 'ろせんず', 'Plan du réseau'), ('出口', 'でぐち', 'Sortie'),
 ('入口', 'いりぐち', 'Entrée'), ('乗車', 'じょうしゃ', 'Montée dans un véhicule'), ('下車', 'げしゃ', 'Descente'), ('次の駅', 'つぎのえき', 'Prochaine station'), ('予約', 'よやく', 'Réservation'), ('座席', 'ざせき', 'Siège'),
 ('手荷物', 'てにもつ', 'Bagage à main'), ('スーツケース', 'スーツケース', 'Valise'), ('リュック', 'リュック', 'Sac à dos'), ('地図', 'ちず', 'Carte, plan'), ('パスポート', 'パスポート', 'Passeport'), ('ビザ', 'ビザ', 'Visa'),
]
CULTURE = [
 ('神社', 'じんじゃ', 'Sanctuaire shintoïste'), ('お寺', 'おてら', 'Temple bouddhiste'), ('鳥居', 'とりい', 'Portique de sanctuaire'), ('賽銭', 'さいせん', 'Offrande d’argent'), ('お守り', 'おまもり', 'Porte-bonheur'), ('おみくじ', 'おみくじ', 'Oracle papier'),
 ('着物', 'きもの', 'Kimono'), ('浴衣', 'ゆかた', 'Yukata'), ('帯', 'おび', 'Ceinture de kimono'), ('下駄', 'げた', 'Sandales en bois'), ('畳', 'たたみ', 'Tatami'), ('布団', 'ふとん', 'Futon'),
 ('障子', 'しょうじ', 'Cloison en papier'), ('襖', 'ふすま', 'Porte coulissante'), ('縁側', 'えんがわ', 'Véranda'), ('庭園', 'ていえん', 'Jardin'), ('茶室', 'ちゃしつ', 'Salon de thé'), ('抹茶', 'まっちゃ', 'Thé vert en poudre'),
 ('花見', 'はなみ', 'Admirer les cerisiers'), ('花火', 'はなび', 'Feu d’artifice'), ('祭り', 'まつり', 'Festival'), ('神輿', 'みこし', 'Sanctuaire portatif'), ('盆踊り', 'ぼんおどり', 'Danse d’été du Obon'), ('正月', 'しょうがつ', 'Nouvel An'),
 ('初詣', 'はつもうで', 'Première visite de l’an'), ('お盆', 'おぼん', 'Fête des morts (août)'), ('七五三', 'しちごさん', 'Fête des 3, 5 et 7 ans'), ('成人式', 'せいじんしき', 'Cérémonie de passage à l’âge adulte'), ('武士', 'ぶし', 'Samouraï'), ('侍', 'さむらい', 'Samouraï'),
 ('忍者', 'にんじゃ', 'Ninja'), ('天皇', 'てんのう', 'Empereur'), ('将軍', 'しょうぐん', 'Shogun'), ('城', 'しろ', 'Château'), ('浮世絵', 'うきよえ', 'Estampe ukiyo-e'), ('俳句', 'はいく', 'Haïku'),
]
PREF = [
 ('北海道', 'ほっかいどう', 'Hokkaidō · Sapporo'), ('青森', 'あおもり', 'Aomori (Tōhoku)'), ('岩手', 'いわて', 'Iwate (Tōhoku)'), ('宮城', 'みやぎ', 'Miyagi · Sendai'), ('秋田', 'あきた', 'Akita (Tōhoku)'),
 ('山形', 'やまがた', 'Yamagata (Tōhoku)'), ('福島', 'ふくしま', 'Fukushima (Tōhoku)'), ('茨城', 'いばらき', 'Ibaraki (Kantō)'), ('栃木', 'とちぎ', 'Tochigi · Nikkō'), ('群馬', 'ぐんま', 'Gunma (Kantō)'),
 ('埼玉', 'さいたま', 'Saitama (Kantō)'), ('千葉', 'ちば', 'Chiba · Narita'), ('東京', 'とうきょう', 'Tōkyō (capitale)'), ('神奈川', 'かながわ', 'Kanagawa · Yokohama'), ('新潟', 'にいがた', 'Niigata (Chūbu)'),
 ('富山', 'とやま', 'Toyama (Chūbu)'), ('石川', 'いしかわ', 'Ishikawa · Kanazawa'), ('福井', 'ふくい', 'Fukui (Chūbu)'), ('山梨', 'やまなし', 'Yamanashi · Mont Fuji'), ('長野', 'ながの', 'Nagano (Alpes)'),
 ('岐阜', 'ぎふ', 'Gifu · Takayama'), ('静岡', 'しずおか', 'Shizuoka · Mont Fuji'), ('愛知', 'あいち', 'Aichi · Nagoya'), ('三重', 'みえ', 'Mie · Ise'), ('滋賀', 'しが', 'Shiga · lac Biwa'),
 ('京都', 'きょうと', 'Kyōto'), ('大阪', 'おおさか', 'Ōsaka'), ('兵庫', 'ひょうご', 'Hyōgo · Kōbe'), ('奈良', 'なら', 'Nara'), ('和歌山', 'わかやま', 'Wakayama · Kōya-san'),
 ('鳥取', 'とっとり', 'Tottori (Chūgoku)'), ('島根', 'しまね', 'Shimane (Chūgoku)'), ('岡山', 'おかやま', 'Okayama (Chūgoku)'), ('広島', 'ひろしま', 'Hiroshima · Miyajima'), ('山口', 'やまぐち', 'Yamaguchi (Chūgoku)'),
 ('徳島', 'とくしま', 'Tokushima (Shikoku)'), ('香川', 'かがわ', 'Kagawa (Shikoku)'), ('愛媛', 'えひめ', 'Ehime (Shikoku)'), ('高知', 'こうち', 'Kōchi (Shikoku)'), ('福岡', 'ふくおか', 'Fukuoka (Kyūshū)'),
 ('佐賀', 'さが', 'Saga (Kyūshū)'), ('長崎', 'ながさき', 'Nagasaki (Kyūshū)'), ('熊本', 'くまもと', 'Kumamoto (Kyūshū)'), ('大分', 'おおいた', 'Ōita · Beppu'), ('宮崎', 'みやざき', 'Miyazaki (Kyūshū)'),
 ('鹿児島', 'かごしま', 'Kagoshima (Kyūshū)'), ('沖縄', 'おきなわ', 'Okinawa'),
]
REGIONS = [
 ('北海道地方', 'ほっかいどうちほう', 'Région de Hokkaidō (nord)'), ('東北地方', 'とうほくちほう', 'Région du Tōhoku (nord-est)'), ('関東地方', 'かんとうちほう', 'Région du Kantō (Tōkyō)'),
 ('中部地方', 'ちゅうぶちほう', 'Région du Chūbu (centre)'), ('近畿地方', 'きんきちほう', 'Région du Kinki (Kyōto, Ōsaka)'), ('中国地方', 'ちゅうごくちほう', 'Région du Chūgoku (ouest)'),
 ('四国地方', 'しこくちほう', 'Région du Shikoku'), ('九州地方', 'きゅうしゅうちほう', 'Région du Kyūshū (sud-ouest)'), ('本州', 'ほんしゅう', 'Honshū, l’île principale'),
 ('四国', 'しこく', 'Île de Shikoku'), ('九州', 'きゅうしゅう', 'Île de Kyūshū'), ('日本海', 'にほんかい', 'Mer du Japon'), ('太平洋', 'たいへいよう', 'Océan Pacifique'),
 ('関西', 'かんさい', 'Kansai (région d’Ōsaka)'), ('関東', 'かんとう', 'Kantō (région de Tōkyō)'), ('富士山', 'ふじさん', 'Mont Fuji'),
]

def _cat(rows):
    return [r for r in rows if r[0] not in HAVE]

def vocab_subs():
    def mk(title, intro, rows):
        rows = _cat(rows)
        return sub(title, intro, [C2.kanji_table(rows)])
    return [
      mk('学校 — École, études et travail de bureau', 'Vocabulaire de l’école, de l’université et de l’entreprise.', ECOLE),
      mk('自然 — Paysages et phénomènes naturels', 'Relief, eau, végétation, séismes et saisons : pour lire un guide ou comprendre la météo.', SHIZEN),
      mk('スポーツ — Sports et compétition', 'Les sports les plus pratiqués ou regardés au Japon, et le vocabulaire du match.', SPORT),
      mk('芸術 — Musique, cinéma, médias et arts', 'Culture, divertissement, médias et arts traditionnels.', MUSIQUE),
      mk('IT — Téléphone, ordinateur et internet', 'Pour parler technologie : appareils, réseau, applications.', IT),
      mk('料理 — Ustensiles, assaisonnements et gestes de cuisine', 'Vocabulaire de cuisine : cuisiner, lire une recette, comprendre un menu.', CUISINE),
      mk('量 — Quantités, parties et proportions', 'Dire « tout », « un peu », « au moins », « environ ».', QUANT),
      mk('人間関係 — Famille élargie et relations', 'Proches, voisins, couple et événements de la vie.', RELATION),
      mk('店 — Magasins, caisse et achats', 'Se repérer dans un magasin et comprendre la caisse.', MAGASIN),
      mk('旅行用語 — Billets, trains et bagages', 'Mots à connaître pour se déplacer en train, bus et avion.', BAGAGE),
      mk('文化 — Traditions, temples et fêtes', 'Mots de la culture japonaise : religion, vêtement, habitat, fêtes, histoire.', CULTURE),
    ]

# ───────────── TEMPS ─────────────
DUREE = [
 ('Une minute', '一分'), ('Cinq minutes', '五分'), ('Dix minutes', '十分'), ('Une demi-heure', '三十分 / 半時間'), ('Une heure', '一時間'), ('Deux heures', '二時間'),
 ('Trois heures', '三時間'), ('Une demi-journée', '半日'), ('Un jour', '一日'), ('Trois jours', '三日間'), ('Une semaine', '一週間'), ('Deux semaines', '二週間'),
 ('Un mois', '一か月'), ('Trois mois', '三か月'), ('Six mois', '半年'), ('Un an', '一年'), ('Deux ans', '二年'), ('Dix ans', '十年'),
]
AGE = [
 ('J’ai vingt ans', '二十歳です。'), ('J’ai trente ans', '三十歳です。'), ('J’ai trente-cinq ans', '三十五歳です。'), ('Quel âge avez-vous ? (poli)', '何歳ですか。'),
 ('Quel âge avez-vous ? (très poli)', 'おいくつですか。'), ('Il a huit ans', '八歳です。'), ('Elle a trois ans', '三歳です。'), ('Mon père a soixante ans', '父は六十歳です。'),
 ('Ma fille a un an', '娘は一歳です。'), ('Nous avons le même âge', '同い年です。'), ('Je suis né en 1990', '一九九〇年に生まれました。'), ('Je suis plus âgé que lui', '彼より年上です。'),
]
FERIES = [
 ('Nouvel An (1er janvier)', '元日', 'がんじつ'), ('Fête de la majorité (2e lundi de janvier)', '成人の日', 'せいじんのひ'), ('Journée de la fondation (11 février)', '建国記念の日', 'けんこくきねんのひ'),
 ('Équinoxe de printemps', '春分の日', 'しゅんぶんのひ'), ('Journée Shōwa (29 avril)', '昭和の日', 'しょうわのひ'), ('Fête de la Constitution (3 mai)', '憲法記念日', 'けんぽうきねんび'),
 ('Journée de la verdure (4 mai)', 'みどりの日', 'みどりのひ'), ('Fête des enfants (5 mai)', 'こどもの日', 'こどものひ'), ('Journée de la mer (3e lundi de juillet)', '海の日', 'うみのひ'),
 ('Journée de la montagne (11 août)', '山の日', 'やまのひ'), ('Fête du respect des aînés (3e lundi de septembre)', '敬老の日', 'けいろうのひ'), ('Équinoxe d’automne', '秋分の日', 'しゅうぶんのひ'),
 ('Journée du sport (2e lundi d’octobre)', 'スポーツの日', 'スポーツのひ'), ('Fête de la culture (3 novembre)', '文化の日', 'ぶんかのひ'), ('Fête du travail (23 novembre)', '勤労感謝の日', 'きんろうかんしゃのひ'),
 ('Anniversaire de l’empereur (23 février)', '天皇誕生日', 'てんのうたんじょうび'), ('Golden Week', 'ゴールデンウィーク', 'ゴールデンウィーク'), ('Veille du Nouvel An', '大晦日', 'おおみそか'),
 ('Saint-Valentin', 'バレンタインデー', 'バレンタインデー'), ('Fête des filles (3 mars)', 'ひな祭り', 'ひなまつり'), ('Fête des étoiles (7 juillet)', '七夕', 'たなばた'),
]
def temps_subs():
    jours = [(f'{n}', jp) for n, jp in [(1, 'ついたち'), (2, 'ふつか'), (3, 'みっか'), (4, 'よっか'), (5, 'いつか'), (6, 'むいか'), (7, 'なのか'), (8, 'ようか'), (9, 'ここのか'), (10, 'とおか'),
        (11, 'じゅういちにち'), (12, 'じゅうににち'), (13, 'じゅうさんにち'), (14, 'じゅうよっか'), (15, 'じゅうごにち'), (16, 'じゅうろくにち'), (17, 'じゅうしちにち'), (18, 'じゅうはちにち'),
        (19, 'じゅうくにち'), (20, 'はつか'), (21, 'にじゅういちにち'), (22, 'にじゅうににち'), (23, 'にじゅうさんにち'), (24, 'にじゅうよっか'), (25, 'にじゅうごにち'), (26, 'にじゅうろくにち'),
        (27, 'にじゅうしちにち'), (28, 'にじゅうはちにち'), (29, 'にじゅうくにち'), (30, 'さんじゅうにち'), (31, 'さんじゅういちにち')]]
    kj = {1: '一日', 2: '二日', 3: '三日', 4: '四日', 5: '五日', 6: '六日', 7: '七日', 8: '八日', 9: '九日', 10: '十日', 14: '十四日', 20: '二十日', 24: '二十四日'}
    def k(n):
        if n in kj: return kj[n]
        s = {11: '十一', 12: '十二', 13: '十三', 15: '十五', 16: '十六', 17: '十七', 18: '十八', 19: '十九', 21: '二十一', 22: '二十二', 23: '二十三', 25: '二十五', 26: '二十六', 27: '二十七', 28: '二十八', 29: '二十九', 30: '三十', 31: '三十一'}[n]
        return s + '日'
    jours_tab = C2.kanji_table([(k(int(n)), kana, f'Le {n}') for n, kana in jours])
    return [
      sub('日付 — Les 31 jours du mois', 'Les jours du mois ont des lectures irrégulières de 1 à 10, puis 14, 20 et 24. Les autres se lisent : nombre + にち.', [jours_tab]),
      sub('期間 — Durées', 'Dire combien de temps. Rappel : 〜時間 (heures), 〜日 / 〜日間 (jours), 〜週間 (semaines), 〜か月 (mois), 〜年 (années).', [phr_dur()]),
      sub('年齢 — Âge et naissance', 'Parler de l’âge : 〜歳 (さい), avec les cas particuliers 一歳 (いっさい), 八歳 (はっさい), 二十歳 (はたち).', [phr(AGE)]),
      sub('祝日 — Jours fériés et fêtes', 'Les jours fériés japonais et les événements de l’année. Les dates marquées « lundi » changent chaque année.', [C2.kanji_table([(jp, ka, fr) for fr, jp, ka in FERIES])]),
    ]

def phr_dur():
    from adjectifs_keigo import rj
    rows = [(fr, jp) for fr, jp in DUREE]
    return T(['En français', '日本語', 'Rōmaji'], [[fr, jp, rj(jp)] for fr, jp in rows], jp=(1,), ro=(2,))

def all_subs():
    return {'語彙': vocab_subs(), '時間': temps_subs()}


# ───────────── GÉOGRAPHIE ─────────────
def geo_section():
    import json
    from content import T, DATA
    from adjectifs_keigo import sub
    M = json.load(open(os.path.join(DATA, 'japanmap.json'), encoding='utf-8'))
    pk = {a: b for a, b, c in PREF}
    rows = [(o['n'], o['k'], 'Région ' + M['reg'][o['r']][1] + ' · chef-lieu ' + o['capr']) for o in M['p']]
    order = {n: i for i, (n, _, _) in enumerate(PREF)}
    rows.sort(key=lambda r: order[r[0]])
    reg_rows = []
    for r, (jp, ro) in M['reg'].items():
        reg_rows.append([jp + ('地方' if r not in ('hok',) and False else ''), ro, '・'.join(o['n'] for o in M['p'] if o['r'] == r)])
    return {'id': 'chiri', 'jp': '地理', 'label': 'Géographie', 'replace': None, 'after': '時間',
      'intro': 'Les 47 préfectures et les 8 régions du Japon, avec une carte interactive et un quiz dédié (Quiz géographie, aussi dans le Quiz général).',
      'subs': [
        sub('地図 — Carte interactive du Japon', 'Touche une préfecture pour voir son nom en japonais, son chef-lieu et ce qu’il faut en retenir. Touche une région pour en voir toutes les préfectures. Les boutons + et − zooment, et tu peux déplacer la carte une fois zoomée.', [{'t': 'p', 'text': '[[JPMAP]]'}]),
        sub('都道府県 — Les 47 préfectures', 'Chaque préfecture avec sa lecture, sa région et son chef-lieu.', [C2.kanji_table(rows)]),
        sub('地方 — Les 8 régions', 'Les régions et les préfectures qui les composent.', [T(['Région', 'Rōmaji', 'Préfectures'], reg_rows, jp=(0, 2), ro=(1,))]),
        sub('島と海 — Îles, mers et grandes zones', 'Îles principales, mers et zones souvent citées (Kansai, Kantō…).', [C2.kanji_table([r for r in REGIONS if not r[0].endswith('地方')])]),
      ]}
