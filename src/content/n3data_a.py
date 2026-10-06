import os, sys
# -*- coding: utf-8 -*-
# N3 : format  kanji|on|kun|sens|mot:glose;mot:glose
G = {}
G['Politique, société et droit'] = """
政|セイ・ショウ|まつりごと|politique, gouvernement|政治:politique;政府:gouvernement;行政:administration
議|ギ|—|délibération, débat|会議:réunion;議論:débat;議会:parlement
民|ミン|たみ|peuple, citoyen|国民:citoyen, peuple;民族:ethnie, peuple;市民:citoyen
連|レン|つ(れる)・つら(なる)|relier, accompagner|連絡:contact;連休:jours fériés enchaînés;連れる:emmener
対|タイ・ツイ|—|opposé, face à|反対:opposition;対話:dialogue;対象:cible
部|ブ|—|partie, section|全部:tout;部分:partie;部長:chef de service
相|ソウ・ショウ|あい|mutuel, aspect|相談:consulter;相手:partenaire;首相:Premier ministre
定|テイ・ジョウ|さだ(める)|fixer, déterminer|予定:programme;決定:décision;定食:plat du jour
首|シュ|くび|cou, chef|首都:capitale;首相:Premier ministre;手首:poignet
法|ホウ|—|loi, méthode|法律:loi;方法:méthode;文法:grammaire
制|セイ|—|système, contrôler|制度:système;制服:uniforme;規制:réglementation
治|ジ・チ|おさ(める)・なお(る)|gouverner, guérir|政治:politique;治療:traitement;自治:autonomie
務|ム|つと(める)|devoir, tâche|事務:travail de bureau;義務:obligation;業務:activité
権|ケン・ゴン|—|droit, pouvoir|権利:droit;人権:droits humains;権力:pouvoir
官|カン|—|fonctionnaire, organe|警官:policier;長官:directeur;官庁:administration
任|ニン|まか(せる)|confier, charge|責任:responsabilité;担任:professeur principal;任務:mission
係|ケイ|かか(り)・かか(わる)|rapport, responsable|関係:relation;係員:préposé;係る:concerner
関|カン|せき・かか(わる)|barrière, concerner|関係:relation;関心:intérêt;玄関:entrée
際|サイ|きわ|occasion, limite|国際:international;交際:fréquentation;実際:en réalité
参|サン|まい(る)|participer, visiter|参加:participation;参考:référence;お参り:visite au temple
加|カ|くわ(える)・くわ(わる)|ajouter, participer|参加:participation;加える:ajouter;追加:ajout
組|ソ|くみ・く(む)|assembler, groupe|組織:organisation;番組:émission;組み合わせ:combinaison
団|ダン・トン|—|groupe, rond|団体:groupe;集団:collectif;布団:futon
警|ケイ|—|avertir, police|警察:police;警告:avertissement;警官:policier
察|サツ|—|examiner, deviner|警察:police;観察:observation;診察:consultation
犯|ハン|おか(す)|crime, commettre|犯人:criminel;犯罪:crime;防犯:prévention du crime
罪|ザイ|つみ|crime, faute|犯罪:crime;有罪:coupable;罪:péché
法|—|—|—|—
裁|サイ|さば(く)・た(つ)|juger, tailler|裁判:procès;裁縫:couture;裁く:juger
判|ハン・バン|—|jugement, sceau|判断:jugement;裁判:procès;判子:cachet
訴|ソ|うった(える)|accuser, se plaindre|訴える:porter plainte;訴訟:litige;勝訴:gain de cause
規|キ|—|règle, norme|規則:règlement;規模:ampleur;定規:règle
則|ソク|—|règle, loi|規則:règlement;原則:principe;法則:loi
守|シュ・ス|まも(る)|protéger, respecter|守る:protéger;留守:absence;保守:conservation
違|イ|ちが(う)|différer, se tromper|違反:infraction;間違い:erreur;違う:être différent
反|ハン・タン|そ(る)|contraire, s’opposer|反対:opposition;違反:infraction;反応:réaction
禁|キン|—|interdire|禁止:interdiction;禁煙:non-fumeur;禁物:à éviter
止|シ|と(まる)・と(める)|arrêter, cesser|中止:annulation;禁止:interdiction;止まる:s’arrêter
許|キョ|ゆる(す)|permettre, pardonner|許可:autorisation;許す:pardonner;免許:permis
可|カ|—|possible, approuvable|可能:possible;許可:autorisation;可愛い:mignon
""".strip().splitlines()
G['Économie, entreprise et travail'] = """
経|ケイ・キョウ|へ(る)|passer, économie|経済:économie;経験:expérience;経営:gestion
済|サイ|す(む)・す(ます)|finir, régler|経済:économie;済む:être terminé;返済:remboursement
産|サン|う(む)・う(まれる)|produire, naître|生産:production;財産:fortune;お土産:souvenir
業|ギョウ|わざ|activité, métier|工業:industrie;卒業:diplôme;営業:vente
商|ショウ|あきな(う)|commerce|商品:marchandise;商店:magasin;商売:commerce
貿|ボウ|—|commerce|貿易:commerce extérieur;貿易会社:société de négoce;貿易港:port commercial
易|エキ・イ|やさ(しい)|échange, facile|貿易:commerce extérieur;容易:facile;易しい:facile
貨|カ|—|marchandise, monnaie|貨物:marchandises;通貨:monnaie;百貨店:grand magasin
費|ヒ|つい(やす)|dépense|費用:frais;食費:frais de nourriture;消費:consommation
消|ショウ|き(える)・け(す)|éteindre, disparaître|消費:consommation;消す:éteindre;消える:disparaître
資|シ|—|ressources, capital|資料:documents;資源:ressources;投資:investissement
財|ザイ・サイ|—|biens, richesse|財布:portefeuille;財産:fortune;財政:finances
投|トウ|な(げる)|jeter, investir|投票:vote;投資:investissement;投げる:lancer
銀|ギン|—|argent (métal)|銀行:banque;銀座:Ginza;銀色:argenté
鉄|テツ|—|fer|地下鉄:métro;鉄道:chemin de fer;鉄橋:pont de fer
鉱|コウ|—|minerai|鉱山:mine;鉱物:minéral;鉱石:minerai
値|チ|ね・あたい|prix, valeur|値段:prix;値上げ:hausse de prix;価値:valeur
価|カ|あたい|prix, valeur|価格:prix;物価:prix des biens;定価:prix fixe
額|ガク|ひたい|montant, front|金額:montant;額:front;総額:total
給|キュウ|—|fournir, salaire|給料:salaire;支給:versement;時給:salaire horaire
払|フツ|はら(う)|payer|支払い:paiement;払う:payer;前払い:paiement d’avance
損|ソン|そこ(なう)|perte|損害:dommage;損:perte;損得:pertes et profits
得|トク|え(る)・う(る)|obtenir, avantage|得意:fort(e) en;お得:avantageux;得る:obtenir
利|リ|き(く)|profit, avantage|便利:pratique;利用:utilisation;権利:droit
益|エキ|—|profit|利益:bénéfice;有益:utile;収益:revenu
収|シュウ|おさ(める)|recevoir, ranger|収入:revenu;領収書:reçu;回収:collecte
入|—|—|—|—
税|ゼイ|—|impôt|税金:impôt;消費税:TVA;免税:duty-free
営|エイ|いとな(む)|gérer, exploiter|営業:ouverture, vente;経営:gestion;運営:exploitation
備|ビ|そな(える)|préparer, équiper|準備:préparation;設備:équipement;予備:réserve
準|ジュン|—|standard, préparer|準備:préparation;標準:standard;水準:niveau
務|—|—|—|—
就|シュウ・ジュ|つ(く)|prendre un poste|就職:recherche d’emploi;就任:prise de fonction;成就:réalisation
職|ショク|—|emploi, profession|職業:profession;就職:entrée dans la vie active;辞職:démission
員|イン|—|membre, employé|会社員:salarié;店員:vendeur;社員:employé
課|カ|—|section, leçon|課長:chef de section;課題:devoir, enjeu;日課:routine quotidienne
長|—|—|—|—
役|ヤク・エキ|—|rôle, fonction|役割:rôle;役所:mairie;役に立つ:être utile
管|カン|くだ|tuyau, gérer|管理:gestion;水道管:conduite d’eau;血管:vaisseau
理|リ|—|raison, logique|理由:raison;料理:cuisine;管理:gestion
""".strip().splitlines()
