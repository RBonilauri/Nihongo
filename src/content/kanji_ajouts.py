# -*- coding: utf-8 -*-
# Kanji manquants par rapport aux listes JLPT de référence (KANJIDIC : anciens niveaux 4 et 3 ; N3 usuel).
# Format : kanji|on|kun|sens|mot:glose;mot:glose
N5 = {
'Lieux, directions et déplacements': """
駅|エキ|—|gare|駅前:devant la gare;駅員:employé de gare;東京駅:gare de Tokyo
店|テン|みせ|magasin|店員:vendeur;書店:librairie;喫茶店:café
""",
'Qualités et couleurs': """
少|ショウ|すく(ない)・すこ(し)|peu|少し:un peu;少ない:peu nombreux;少年:garçon
多|タ|おお(い)|nombreux, beaucoup|多い:nombreux;多分:probablement;多数:majorité
""",
}
N4 = {
'Lieux et ville': """
世|セ・セイ|よ|monde, génération|世界:monde;世話:soin, aide;世の中:société
京|キョウ・ケイ|—|capitale|東京:Tokyo;京都:Kyoto;上京:monter à la capitale
住|ジュウ|す(む)|habiter|住所:adresse;住む:habiter;住民:habitant
堂|ドウ|—|grande salle|食堂:cantine;講堂:amphithéâtre;本堂:salle principale
場|ジョウ|ば|lieu|場所:endroit;会場:salle;駐車場:parking
所|ショ|ところ|endroit|場所:endroit;住所:adresse;事務所:bureau
界|カイ|—|monde, limite|世界:monde;境界:frontière;業界:secteur
県|ケン|—|préfecture|県庁:préfecture;県立:départemental;神奈川県:préfecture de Kanagawa
都|ト・ツ|みやこ|capitale|東京都:métropole de Tokyo;都会:grande ville;京都:Kyoto
門|モン|かど|portail|正門:porte principale;専門:spécialité;門:portail
""",
'Éducation et travail': """
事|ジ|こと|chose, affaire|仕事:travail;事故:accident;大事:important
仕|シ|つか(える)|servir, faire|仕事:travail;仕方:manière;仕度:préparatifs
力|リョク・リキ|ちから|force|力:force;体力:endurance;努力:effort
売|バイ|う(る)|vendre|売る:vendre;売店:kiosque;販売:vente
工|コウ・ク|—|travail manuel, industrie|工場:usine;工事:travaux;大工:charpentier
""",
'Corps et santé': """
体|タイ|からだ|corps|体育:éducation physique;体温:température;全体:ensemble
""",
'Émotions et caractère': """
心|シン|こころ|cœur, esprit|心配:inquiétude;安心:soulagement;中心:centre
""",
'Mouvements et actions physiques': """
持|ジ|も(つ)|tenir, posséder|持つ:tenir;気持ち:sentiment;お金持ち:riche
発|ハツ・ホツ|—|partir, émettre|出発:départ;発音:prononciation;発見:découverte
""",
'Pensée, communication et apprentissage': """
文|ブン・モン|ふみ|phrase, écrit|文章:texte;作文:rédaction;文化:culture
漢|カン|—|Chine, Han|漢字:kanji;漢方:médecine chinoise;漢語:mot sino-japonais
自|ジ・シ|みずか(ら)|soi-même|自分:soi-même;自転車:vélo;自由:liberté
英|エイ|—|Angleterre, brillant|英語:anglais;英国:Royaume-Uni;英会話:conversation anglaise
""",
'Temps et saisons': """
去|キョ・コ|さ(る)|partir, passé|去年:l’an dernier;過去:passé;去る:quitter
""",
'Objets et vie quotidienne': """
便|ベン・ビン|たよ(り)|commodité, courrier|便利:pratique;郵便:poste;不便:peu pratique
台|ダイ・タイ|—|support, compteur de machines|台所:cuisine;台風:typhon;三台:trois véhicules
用|ヨウ|もち(いる)|utiliser, usage|用事:chose à faire;利用:utilisation;用意:préparatifs
""",
'Nourriture et nature': """
料|リョウ|—|frais, matière|料理:cuisine;料金:tarif;無料:gratuit
洋|ヨウ|—|océan, occidental|洋服:vêtement occidental;西洋:Occident;洋食:cuisine occidentale
菜|サイ|な|légume|野菜:légume;菜食:végétarisme;白菜:chou chinois
飯|ハン|めし|riz cuit, repas|ご飯:riz, repas;朝ご飯:petit-déjeuner;夕飯:dîner
""",
'Famille et relations': """
私|シ|わたし・わたくし|je, privé|私:je;私立:privé;私物:affaires personnelles
""",
'Qualités et mesures': """
低|テイ|ひく(い)|bas|低い:bas;最低:minimum;低下:baisse
真|シン|ま|vrai, exact|写真:photo;真ん中:milieu;真面目:sérieux
短|タン|みじか(い)|court|短い:court;短所:défaut;短期:court terme
""",
}
# N3 : nouvelles rubriques (même format que n3data_*.py)
N3 = {}
N3['Société et institutions'] = """
局|キョク|—|bureau, situation|郵便局:poste;結局:finalement;薬局:pharmacie
席|セキ|—|siège, place|席:siège;出席:présence;満席:complet
争|ソウ|あらそ(う)|se disputer, lutter|戦争:guerre;競争:concurrence;争う:se disputer
王|オウ|—|roi|王様:roi;王子:prince;女王:reine
約|ヤク|—|promesse, environ|約束:promesse;予約:réservation;約:environ
責|セキ|せ(める)|responsabilité, blâmer|責任:responsabilité;責める:blâmer;責務:devoir
容|ヨウ|—|contenu, forme|内容:contenu;容易:facile;美容:esthétique
件|ケン|くだん|affaire, cas|事件:incident;条件:condition;件名:objet
内|ナイ・ダイ|うち|intérieur|案内:guide;内容:contenu;国内:national
式|シキ|—|cérémonie, formule|結婚式:mariage;卒業式:remise des diplômes;方式:méthode
実|ジツ|み・みの(る)|réel, fruit|実は:en fait;事実:fait;現実:réalité
面|メン|おもて・つら|visage, surface|面白い:intéressant;場面:scène;表面:surface
害|ガイ|—|dommage|被害:dégâts;害虫:nuisible;公害:pollution
居|キョ|い(る)|être, résider|居間:séjour;居酒屋:izakaya;住居:logement
与|ヨ|あた(える)|donner|与える:donner;関与:implication;給与:salaire
和|ワ|やわ(らぐ)・なご(やか)|paix, japonais|平和:paix;和食:cuisine japonaise;和室:pièce à tatami
原|ゲン|はら|origine, plaine|原因:cause;原則:principe;高原:plateau
因|イン|よ(る)|cause|原因:cause;要因:facteur;因果:cause et effet
神|シン・ジン|かみ|dieu, esprit|神:dieu;神社:sanctuaire shinto;精神:esprit
祖|ソ|—|ancêtre|祖父:grand-père;祖母:grand-mère;祖先:ancêtres
"""
N3['Actions et mouvements'] = """
掛|—|か(ける)・か(かる)|accrocher, suspendre|掛ける:accrocher;出掛ける:sortir;掛かる:coûter
戻|レイ|もど(る)|revenir|戻る:revenir;戻す:remettre;払い戻し:remboursement
頼|ライ|たの(む)・たよ(る)|demander, se fier|頼む:demander;信頼:confiance;頼る:compter sur
向|コウ|む(く)・む(かう)|se tourner vers|向かう:se diriger;方向:direction;向き:orientation
鳴|メイ|な(く)・な(る)|crier, sonner|鳴る:sonner;悲鳴:cri;鳴く:chanter
記|キ|しる(す)|noter|記事:article;日記:journal intime;記念:souvenir
勤|キン・ゴン|つと(める)|travailler pour|勤める:travailler;通勤:trajet domicile-travail;出勤:aller au travail
直|チョク・ジキ|なお(す)・ただ(ちに)|réparer, direct|直す:corriger;正直:honnête;直接:directement
断|ダン|ことわ(る)・た(つ)|refuser, couper|断る:refuser;判断:jugement;中断:interruption
呼|コ|よ(ぶ)|appeler|呼ぶ:appeler;呼吸:respiration;点呼:appel
破|ハ|やぶ(る)・やぶ(れる)|déchirer|破る:déchirer;破片:fragment;破壊:destruction
捕|ホ|つか(まえる)|attraper|捕まえる:attraper;逮捕:arrestation;捕る:capturer
放|ホウ|はな(す)・はな(つ)|libérer, lâcher|放送:diffusion;放す:lâcher;解放:libération
落|ラク|お(ちる)・お(とす)|tomber|落ちる:tomber;落とす:laisser tomber;落語:rakugo
置|チ|お(く)|poser|置く:poser;位置:position;装置:dispositif
探|タン|さが(す)・さぐ(る)|chercher|探す:chercher;探検:exploration;探偵:détective
寄|キ|よ(る)|s’approcher, passer|寄る:passer par;寄付:don;年寄り:personne âgée
留|リュウ・ル|と(める)・と(まる)|rester|留学:études à l’étranger;留守:absence;留学生:étudiant étranger
取|シュ|と(る)|prendre|取る:prendre;取り消す:annuler;受け取る:recevoir
申|シン|もう(す)|dire, humble|申す:dire, humble;申し込み:inscription;申請:demande
吸|キュウ|す(う)|aspirer|吸う:aspirer, fumer;呼吸:respiration;吸収:absorption
刻|コク|きざ(む)|graver, heure|時刻:heure;深刻:grave;遅刻:retard
戦|セン|いくさ・たたか(う)|guerre, combattre|戦争:guerre;戦う:combattre;作戦:stratégie
吹|スイ|ふ(く)|souffler|吹く:souffler;吹雪:tempête de neige;吹奏楽:orchestre d’harmonie
込|—|こ(む)・こ(める)|entrer, mettre dedans|込む:être bondé;申し込む:s’inscrire;見込み:prévision
割|カツ|わ(る)・わり|diviser|割る:casser;割合:proportion;役割:rôle
登|トウ・ト|のぼ(る)|grimper|登る:grimper;登山:alpinisme;登録:inscription
抱|ホウ|だ(く)・いだ(く)|serrer, porter|抱く:serrer;抱える:porter;抱負:aspiration
付|フ|つ(く)・つ(ける)|attacher|付く:s’attacher;受付:réception;気付く:remarquer
除|ジョ・ジ|のぞ(く)|exclure, enlever|除く:exclure;掃除:ménage;削除:suppression
招|ショウ|まね(く)|inviter|招待:invitation;招く:inviter;招待状:carton d’invitation
配|ハイ|くば(る)|distribuer, inquiétude|心配:inquiétude;配達:livraison;配る:distribuer
盗|トウ|ぬす(む)|voler|盗む:voler;盗難:vol;強盗:cambriolage
遊|ユウ・ユ|あそ(ぶ)|jouer|遊ぶ:jouer;遊園地:parc d’attractions;遊び:jeu
浮|フ|う(く)・う(かぶ)|flotter|浮く:flotter;浮かぶ:venir à l’esprit;浮気:infidélité
流|リュウ・ル|なが(れる)|couler|流れる:couler;交流:échange;流行:mode
過|カ|す(ぎる)・す(ごす)|dépasser, passer|過ぎる:dépasser;過去:passé;通過:passage
"""
N3['Qualités, états et notions'] = """
存|ソン・ゾン|—|exister, savoir|存在:existence;保存:conserver;存じる:savoir, humble
貧|ヒン・ビン|まず(しい)|pauvre|貧しい:pauvre;貧乏:pauvreté;貧困:misère
由|ユ・ユウ|よし|raison, origine|理由:raison;自由:liberté;経由:via
富|フ・フウ|と(む)・とみ|riche, abondant|豊富:abondant;富む:être riche;富士山:mont Fuji
途|ト|—|route, chemin|途中:en chemin;用途:usage;途端:à l’instant où
皆|カイ|みな|tous|皆:tout le monde;皆さん:tout le monde, poli;皆様:chers tous
絶|ゼツ|た(える)・た(つ)|couper, extrême|絶対:absolument;絶える:s’éteindre;絶好:idéal
適|テキ|—|approprié|適当:approprié;快適:confortable;適切:adéquat
在|ザイ|あ(る)|exister, se trouver|現在:actuellement;存在:existence;在宅:à la maison
偉|イ|えら(い)|grand, remarquable|偉い:remarquable;偉大:grandiose;偉人:grand homme
更|コウ|さら・ふ(ける)|encore plus, renouveler|更新:mise à jour;更に:de plus;今更:à présent
能|ノウ|—|capacité, noh|能力:capacité;可能:possible;才能:talent
美|ビ|うつく(しい)|beau|美しい:beau;美術:beaux-arts;美味しい:délicieux
程|テイ|ほど|degré, mesure|程度:degré;日程:programme;先程:tout à l’heure
静|セイ・ジョウ|しず(か)|calme|静か:calme;静止:immobile;安静:repos
頂|チョウ|いただ(く)・いただき|sommet, recevoir|頂く:recevoir, humble;山頂:sommet;頂上:sommet
供|キョウ・ク|とも・そな(える)|accompagner, offrir|子供:enfant;提供:fournir;お供:accompagnateur
似|ジ|に(る)|ressembler|似る:ressembler;似合う:aller bien;真似:imitation
互|ゴ|たが(い)|mutuel|お互い:mutuellement;相互:réciproque;互いに:l’un l’autre
雑|ザツ・ゾウ|—|mélangé, divers|雑誌:magazine;複雑:compliqué;雑談:bavardage
列|レツ|—|rang, file|行列:file d’attente;列車:train;列島:archipel
果|カ|は(たす)・は(て)|fruit, résultat|結果:résultat;果物:fruit;果たす:accomplir
恐|キョウ|おそ(れる)|craindre|恐れる:craindre;恐縮:être confus;恐怖:peur
幾|キ|いく|combien|幾つ:combien;幾ら:combien, prix;幾日:combien de jours
誤|ゴ|あやま(る)|se tromper|誤解:malentendu;誤る:se tromper;誤字:faute de caractère
精|セイ|—|esprit, raffiné|精神:esprit;精一杯:de son mieux;精密:précis
君|クン|きみ|toi, seigneur|君:tu, familier;君たち:vous;君主:monarque
婚|コン|—|mariage|結婚:mariage;婚約:fiançailles;離婚:divorce
舞|ブ|ま(う)・まい|danser|舞う:danser;舞台:scène;歌舞伎:kabuki
活|カツ|—|vivant, actif|生活:vie quotidienne;活動:activité;活発:actif
"""
N3['Nature, lieux et objets'] = """
球|キュウ|たま|balle, sphère|野球:baseball;地球:Terre;電球:ampoule
機|キ|はた|machine, occasion|機会:occasion;飛行機:avion;機械:machine
礼|レイ|—|salut, politesse|失礼:impoli;お礼:remerciement;礼儀:politesse
杯|ハイ|さかずき|verre, coupe|乾杯:santé;一杯:un verre;杯:coupe
徒|ト|—|élève, disciple|生徒:élève;信徒:fidèle;徒歩:à pied
緒|ショ・チョ|お|fil, début|一緒:ensemble;情緒:atmosphère;緒:cordon
路|ロ|じ|route|道路:route;線路:voie ferrée;路地:ruelle
座|ザ|すわ(る)|s’asseoir, place|座る:s’asseoir;座席:siège;銀座:Ginza
園|エン|その|jardin, parc|公園:parc;動物園:zoo;幼稚園:maternelle
予|ヨ|あらかじ(め)|à l’avance|予約:réservation;予定:programme;予報:prévisions
船|セン|ふね・ふな|bateau|船:bateau;汽船:vapeur;船便:envoi par bateau
処|ショ|—|traiter, lieu|処理:traitement;対処:gérer;処分:élimination
積|セキ|つ(む)・つ(もる)|accumuler|積む:empiler;面積:superficie;積極的:actif
暮|ボ|く(らす)・く(れる)|vivre, tomber la nuit|暮らす:vivre;夕暮れ:crépuscule;年の暮れ:fin d’année
候|コウ|そうろう|climat, saison|天候:temps;気候:climat;候補:candidat
横|オウ|よこ|côté, horizontal|横:côté;横断:traversée;横浜:Yokohama
晩|バン|—|soir|今晩:ce soir;毎晩:chaque soir;晩ご飯:dîner
御|ギョ・ゴ|おん・お|honorifique|御飯:riz, repas;御礼:remerciements;御中:Messieurs
景|ケイ|—|paysage, vue|景色:paysage;景気:conjoncture;背景:arrière-plan
束|ソク|たば|botte, lier|約束:promesse;花束:bouquet;束ねる:lier
靴|カ|くつ|chaussure|靴:chaussure;靴下:chaussette;運動靴:baskets
"""
