import os, sys
# -*- coding: utf-8 -*-
G = {}
G['Lieux, nature et objets'] = """
港|コウ|みなと|port|港:port;空港:aéroport;香港:Hong Kong
島|トウ|しま|île|島:île;半島:péninsule;列島:archipel
岸|ガン|きし|rive, côte|海岸:côte;岸:rive;対岸:rive opposée
湖|コ|みずうみ|lac|湖:lac;湖水:eau du lac;琵琶湖:lac Biwa
河|カ|かわ|fleuve|河口:embouchure;運河:canal;黄河:fleuve Jaune
谷|コク|たに|vallée|谷:vallée;渋谷:Shibuya;谷間:fond de vallée
丘|キュウ|おか|colline|丘:colline;砂丘:dune;丘陵:coteau
泉|セン|いずみ|source|温泉:source chaude;泉:source;源泉:source
林|—|—|—|—
松|ショウ|まつ|pin|松:pin;門松:décor du Nouvel An;松本:Matsumoto
竹|チク|たけ|bambou|竹:bambou;竹林:bambouseraie;爆竹:pétard
梅|バイ|うめ|prunier|梅:prunier;梅干し:prune salée;梅雨:saison des pluies
桜|オウ|さくら|cerisier|桜:cerisier;桜色:rose cerisier;夜桜:cerisiers de nuit
葉|ヨウ|は|feuille|葉:feuille;紅葉:feuillage d’automne;言葉:mot
根|コン|ね|racine|根:racine;根本:fondement;大根:radis blanc
植|ショク|う(える)|planter|植物:plante;植える:planter;植木:plante en pot
麦|バク|むぎ|blé, orge|麦:blé;小麦:froment;麦茶:thé d’orge
豆|トウ|まめ|haricot, pois|豆:haricot;大豆:soja;納豆:natto
卵|ラン|たまご|œuf|卵:œuf;卵焼き:omelette japonaise;産卵:ponte
米|—|—|—|—
鳥|—|—|—|—
犬|ケン|いぬ|chien|犬:chien;子犬:chiot;番犬:chien de garde
猫|ビョウ|ねこ|chat|猫:chat;子猫:chaton;猫舌:langue sensible au chaud
虫|チュウ|むし|insecte|虫:insecte;昆虫:insecte;虫歯:carie
貝|バイ|かい|coquillage|貝:coquillage;貝殻:coquille;貝類:coquillages
星|セイ|ほし|étoile|星:étoile;星空:ciel étoilé;火星:Mars
雲|ウン|くも|nuage|雲:nuage;雨雲:nuage de pluie;雲海:mer de nuages
雪|セツ|ゆき|neige|雪:neige;大雪:fortes chutes;雪だるま:bonhomme de neige
風|フウ|かぜ|vent|風:vent;台風:typhon;風邪:rhume
嵐|—|あらし|tempête|嵐:tempête;嵐の前:avant la tempête;砂嵐:tempête de sable
晴|セイ|は(れる)|temps clair|晴れ:beau temps;晴れる:s’éclaircir;快晴:ciel dégagé
陽|ヨウ|—|soleil, yang|太陽:soleil;陽気:gai;夕陽:soleil couchant
暖|ダン|あたた(かい)|chaud, doux|暖かい:doux;暖房:chauffage;温暖:tempéré
温|オン|あたた(かい)|tiède, chaleur|温度:température;温泉:onsen;体温:température corporelle
湿|シツ|しめ(る)|humide|湿気:humidité;湿度:taux d’humidité;湿る:s’humidifier
浴|ヨク|あ(びる)|se baigner|入浴:bain;浴衣:yukata;浴室:salle de bain
泊|ハク|と(まる)|passer la nuit|泊まる:loger;一泊:une nuit;宿泊:hébergement
宿|シュク|やど|auberge|宿:auberge;宿題:devoirs;新宿:Shinjuku
宅|タク|—|maison, domicile|自宅:chez soi;住宅:logement;宅配:livraison à domicile
庭|テイ|にわ|jardin|庭:jardin;家庭:foyer;校庭:cour d’école
壁|ヘキ|かべ|mur|壁:mur;壁紙:papier peint;城壁:remparts
窓|ソウ|まど|fenêtre|窓:fenêtre;窓口:guichet;窓際:près de la fenêtre
扉|ヒ|とびら|battant de porte|扉:porte;鉄の扉:porte de fer;開扉:ouverture
鏡|キョウ|かがみ|miroir|鏡:miroir;眼鏡:lunettes;望遠鏡:télescope
鍵|ケン|かぎ|clé|鍵:clé;合鍵:double de clé;鍵穴:serrure
袋|タイ|ふくろ|sac|袋:sac;手袋:gants;紙袋:sac en papier
箱|—|はこ|boîte|箱:boîte;郵便箱:boîte aux lettres;ごみ箱:poubelle
針|シン|はり|aiguille|針:aiguille;方針:orientation;時計の針:aiguille d’horloge
糸|シ|いと|fil|糸:fil;毛糸:laine;糸口:piste
布|フ|ぬの|tissu|布:tissu;布団:futon;財布:portefeuille
綿|メン|わた|coton|綿:coton;木綿:coton;綿菓子:barbe à papa
絹|ケン|きぬ|soie|絹:soie;絹糸:fil de soie;人絹:rayonne
紅|コウ|べに・くれない|rouge vif|紅茶:thé noir;紅葉:feuilles d’automne;口紅:rouge à lèvres
緑|リョク|みどり|vert|緑:vert;緑茶:thé vert;新緑:verdure nouvelle
茶|—|—|—|—
器|キ|うつわ|récipient, instrument|器:récipient;楽器:instrument de musique;食器:vaisselle
皿|—|さら|assiette|皿:assiette;お皿:assiette;灰皿:cendrier
瓶|ビン|—|bouteille|瓶:bouteille;花瓶:vase;瓶詰め:mis en bouteille
缶|カン|—|boîte de conserve|缶:canette;缶詰:conserve;空き缶:canette vide
灯|トウ|ひ|lampe|電灯:lampe électrique;灯り:lumière;灯台:phare
炎|エン|ほのお|flamme|炎:flamme;火炎:flammes;炎症:inflammation
煙|エン|けむり|fumée|煙:fumée;禁煙:interdit de fumer;喫煙:fait de fumer
灰|カイ|はい|cendre|灰:cendre;灰色:gris;灰皿:cendrier
""".strip().splitlines()
G['Temps, nombres et mesures'] = """
昨|—|—|—|—
未|ミ|いま(だ)|pas encore|未来:avenir;未成年:mineur;未定:non fixé
将|ショウ|まさ(に)|futur, général|将来:avenir;将軍:shogun;主将:capitaine
future|—|—|—|—
現|—|—|—|—
昔|セキ|むかし|autrefois|昔:autrefois;昔話:conte;大昔:temps très anciens
代|ダイ・タイ|か(わる)・よ|époque, remplacer|時代:époque;代わり:à la place;代表:représentant
期|—|—|—|—
際|—|—|—|—
末|—|—|—|—
最|サイ|もっと(も)|le plus|最近:récemment;最高:le meilleur;最後:dernier
初|—|—|—|—
終|—|—|—|—
単|タン|—|simple, unité|単語:mot;簡単:facile;単位:unité
複|フク|—|multiple|複雑:compliqué;複数:pluriel;重複:doublon
倍|バイ|—|double, fois|倍:fois;二倍:double;倍率:grossissement
億|オク|—|cent millions|一億:cent millions;億万長者:milliardaire;数億:centaines de millions
兆|チョウ|きざ(し)|billion, signe|一兆:mille milliards;前兆:signe avant-coureur;兆し:présage
万|—|—|—|—
種|シュ|たね|espèce, graine|種類:sorte;種:graine;品種:variété
類|ルイ|たぐい|catégorie|種類:sorte;人類:humanité;書類:documents
第|ダイ|—|ordinal|第一:premier;第二:deuxième;第三者:tiers
番|バン|—|numéro, tour|番号:numéro;番組:émission;交番:poste de police
号|ゴウ|—|numéro, nom|番号:numéro;信号:feu;記号:symbole
等|トウ|ひと(しい)|égal, classe|平等:égalité;一等:première classe;等しい:égal
段|ダン|—|marche, niveau|階段:escalier;値段:prix;段階:étape
階|カイ|—|étage|階段:escalier;二階:étage;階:étage
級|キュウ|—|classe, grade|高級:haut de gamme;上級:niveau avancé;学級:classe
位|イ|くらい|rang, place|位置:position;一位:première place;三位:troisième place
側|ソク|がわ|côté|側:côté;右側:côté droit;反対側:côté opposé
辺|ヘン|あた(り)・べ|environs|辺り:alentours;周辺:périphérie;この辺:par ici
周|シュウ|まわ(り)|tour, autour|周り:environs;一周:un tour;周囲:entourage
囲|イ|かこ(む)|entourer|囲む:encercler;周囲:alentours;範囲:étendue
範|ハン|—|modèle, limite|範囲:étendue;模範:modèle;規範:norme
限|ゲン|かぎ(る)|limite|限る:limiter;期限:échéance;制限:limite
最|—|—|—|—
以|—|—|—|—
未|—|—|—|—
各|カク|おのおの|chaque|各自:chacun;各国:chaque pays;各地:chaque région
毎|—|—|—|—
共|キョウ|とも|ensemble|共通:commun;共同:collectif;公共:public
全|—|—|—|—
他|タ|ほか|autre|他:autre;他人:autrui;その他:autres
残|—|—|—|—
余|ヨ|あま(る)|reste, surplus|余り:reste;余計:superflu;余裕:marge
""".strip().splitlines()
G['Qualités, états et divers'] = """
最|—|—|—|—
優|ユウ|やさ(しい)・すぐ(れる)|gentil, supérieur|優しい:gentil;優秀:excellent;優勝:victoire
良|—|—|—|—
悪|—|—|—|—
正|—|—|—|—
確|カク|たし(か)|certain|確か:sûrement;確認:vérification;正確:exact
的|テキ|まと|cible, -ique|目的:but;的:cible;具体的:concret
具|グ|—|outil, concret|道具:outil;具合:état;具体的:concret
体|—|—|—|—
特|—|—|—|—
別|—|—|—|—
普|フ|—|ordinaire|普通:ordinaire;普段:d’habitude;普及:diffusion
通|—|—|—|—
常|ジョウ|つね|toujours, normal|日常:quotidien;非常:extrême;常に:toujours
非|ヒ|—|non, anti|非常:urgence;非常口:sortie de secours;非難:blâme
否|ヒ|いな|nier|否定:négation;拒否:refus;賛否:pour et contre
賛|サン|—|approuver|賛成:accord;賛否:pour et contre;称賛:éloge
成|—|—|—|—
必|ヒツ|かなら(ず)|nécessairement|必要:nécessaire;必ず:sans faute;必死:désespéré
要|ヨウ|い(る)|nécessaire, essentiel|必要:nécessaire;重要:important;要点:point clé
重|—|—|—|—
軽|—|—|—|—
深|シン|ふか(い)|profond|深い:profond;深夜:nuit profonde;水深:profondeur
浅|セン|あさ(い)|peu profond|浅い:peu profond;遠浅:plage en pente douce;浅瀬:haut-fond
濃|ノウ|こ(い)|dense, foncé|濃い:foncé, fort;濃度:concentration;濃厚:riche
薄|ハク|うす(い)|mince, léger|薄い:fin;薄暗い:sombre;薄味:fadeur
厚|コウ|あつ(い)|épais|厚い:épais;厚着:vêtements chauds;厚生:bien-être
固|コ|かた(い)|dur, solide|固い:dur;固定:fixer;固体:solide
硬|コウ|かた(い)|dur|硬い:dur;硬貨:pièce de monnaie;硬直:raideur
柔|ジュウ|やわ(らかい)|souple|柔らかい:tendre;柔道:judo;柔軟:flexible
濡|—|ぬ(れる)|mouillé|濡れる:se mouiller;びしょ濡れ:trempé;濡れ衣:fausse accusation
乾|カン|かわ(く)|sec|乾く:sécher;乾杯:santé !;乾燥:sécheresse
空|—|—|—|—
満|マン|み(ちる)|plein, satisfait|満足:satisfait;満員:complet;不満:mécontentement
足|—|—|—|—
欠|ケツ|か(ける)|manquer|欠席:absence;欠点:défaut;欠ける:être ébréché
完|カン|—|complet|完全:complet;完成:achèvement;完了:fin
全|—|—|—|—
純|ジュン|—|pur|純粋:pur;単純:simple;純白:blanc pur
素|ソ・ス|もと|élémentaire, nature|素敵:charmant;素直:docile;簡素:sobre
簡|カン|—|simple|簡単:facile;簡易:simple;書簡:lettre
単|—|—|—|—
複|—|—|—|—
急|キュウ|いそ(ぐ)|urgent, rapide|急:soudain;急行:rapide;緊急:urgence
緊|キン|—|tendu|緊張:tension;緊急:urgence;緊迫:imminence
突|トツ|つ(く)|percuter, soudain|突然:soudain;突く:piquer;衝突:collision
然|ゼン・ネン|—|ainsi, naturel|自然:nature;突然:soudain;当然:naturel
偶|グウ|—|par hasard|偶然:hasard;偶数:nombre pair;配偶者:conjoint
暴|ボウ・バク|あば(れる)|violent|乱暴:brutal;暴力:violence;暴れる:se déchaîner
危|キ|あぶ(ない)|danger|危険:danger;危ない:dangereux;危機:crise
険|ケン|けわ(しい)|escarpé, danger|危険:danger;保険:assurance;冒険:aventure
保|ホ|たも(つ)|conserver|保険:assurance;保存:conservation;保つ:maintenir
安|—|—|—|—
防|ボウ|ふせ(ぐ)|prévenir|予防:prévention;防ぐ:empêcher;消防:pompiers
救|キュウ|すく(う)|sauver|救急車:ambulance;救う:sauver;救助:secours
助|ジョ|たす(ける)|aider|助ける:aider;助手:assistant;手助け:coup de main
支|シ|ささ(える)|soutenir|支える:soutenir;支払い:paiement;支店:succursale
援|エン|—|soutenir|応援:encouragement;援助:aide;支援:soutien
応|オウ|こた(える)|répondre à|応援:encouragement;反応:réaction;応じる:répondre
""".strip().splitlines()
