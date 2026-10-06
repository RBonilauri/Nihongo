import os, sys
# -*- coding: utf-8 -*-
G = {}
G['Esprit, sentiments et jugement'] = """
感|カン|—|sentiment, sentir|感じる:ressentir;感謝:remerciement;感動:émotion
情|ジョウ|なさ(け)|sentiment, situation|事情:circonstances;感情:émotion;愛情:affection
想|ソウ|—|idée, penser|予想:prévision;感想:impression;理想:idéal
念|ネン|—|pensée, souhait|残念:dommage;記念:souvenir;念のため:par précaution
思|—|—|—|—
愛|アイ|いと(しい)|amour|愛情:affection;恋愛:histoire d’amour;愛する:aimer
恋|レン|こい・こい(しい)|amour, romance|恋人:petit(e) ami(e);恋愛:romance;初恋:premier amour
幸|コウ|しあわ(せ)・さいわ(い)|bonheur|幸せ:bonheur;不幸:malheur;幸運:chance
福|フク|—|bonheur, chance|幸福:bonheur;福祉:protection sociale;福岡:Fukuoka
喜|キ|よろこ(ぶ)|joie|喜ぶ:se réjouir;喜び:joie;喜劇:comédie
怒|ド|おこ(る)・いか(り)|colère|怒る:se fâcher;怒り:colère;激怒:fureur
泣|キュウ|な(く)|pleurer|泣く:pleurer;泣き声:pleurs;号泣:sanglots
笑|ショウ|わら(う)・え(む)|rire|笑う:rire;笑顔:sourire;苦笑:rire jaune
驚|キョウ|おどろ(く)|s’étonner|驚く:être surpris;驚き:surprise;驚異:merveille
恥|チ|は(じ)・は(ずかしい)|honte|恥ずかしい:gêné;恥:honte;恥じる:avoir honte
困|コン|こま(る)|être embarrassé|困る:être embêté;困難:difficulté;困った:embêtant
苦|ク|くる(しい)・にが(い)|souffrance, amer|苦しい:pénible;苦い:amer;苦労:peine
悩|ノウ|なや(む)|se tourmenter|悩む:se tracasser;悩み:souci;苦悩:angoisse
疲|ヒ|つか(れる)|fatigue|疲れる:être fatigué;疲労:fatigue;お疲れ様:merci pour ton travail
眠|ミン|ねむ(い)・ねむ(る)|sommeil|眠い:avoir sommeil;眠る:dormir;睡眠:sommeil
夢|ム|ゆめ|rêve|夢:rêve;悪夢:cauchemar;夢中:passionné
望|ボウ|のぞ(む)|souhaiter|希望:espoir;望む:désirer;失望:déception
希|キ|—|espoir, rare|希望:espoir;希少:rare;希望者:candidat
願|ガン|ねが(う)|souhaiter, prier|お願い:s’il vous plaît;願う:souhaiter;願書:dossier de candidature
求|キュウ|もと(める)|demander, chercher|要求:exigence;求める:rechercher;求人:offre d’emploi
欲|ヨク|ほ(しい)|désir|欲しい:vouloir;食欲:appétit;欲張り:avide
信|シン|—|croire, confiance|信じる:croire;信号:feu;自信:confiance en soi
疑|ギ|うたが(う)|douter|疑問:question, doute;疑う:douter;容疑:soupçon
認|ニン|みと(める)|reconnaître|認める:admettre;確認:vérification;認識:reconnaissance
判|—|—|—|—
決|—|—|—|—
迷|メイ|まよ(う)|se perdre, hésiter|迷う:hésiter;迷子:enfant perdu;迷惑:dérangement
惑|ワク|まど(う)|se troubler|迷惑:dérangement;困惑:perplexité;誘惑:tentation
態|タイ|—|état, attitude|状態:état;態度:attitude;事態:situation
度|ド・タク|たび|degré, fois|態度:attitude;今度:la prochaine fois;速度:vitesse
性|セイ・ショウ|—|nature, sexe|性格:caractère;男性:homme;可能性:possibilité
格|カク・コウ|—|caractère, statut|性格:caractère;合格:réussite (examen);資格:qualification
好|コウ|す(き)・この(む)|aimer|好き:aimer;好物:plat préféré;友好:amitié
嫌|ケン・ゲン|きら(い)・いや|détester|嫌い:détester;嫌:déplaisant;機嫌:humeur
憎|ゾウ|にく(い)|haïr|憎い:détestable;憎む:haïr;愛憎:amour-haine
勇|ユウ|いさ(ましい)|courage|勇気:courage;勇敢:brave;勇ましい:vaillant
気|—|—|—|—
努|ド|つと(める)|s’efforcer|努力:effort;努める:s’efforcer;努めて:avec effort
励|レイ|はげ(ます)・はげ(む)|encourager|励ます:encourager;励む:s’appliquer;奨励:encouragement
誇|コ|ほこ(る)|fierté|誇り:fierté;誇る:être fier;誇張:exagération
慣|カン|な(れる)・な(らす)|s’habituer|習慣:habitude;慣れる:s’habituer;慣用句:locution
""".strip().splitlines()
G['Communication et connaissance'] = """
談|ダン|—|discuter|相談:consultation;会談:entretien;冗談:plaisanterie
論|ロン|—|théorie, débat|議論:débat;論文:thèse;結論:conclusion
説|セツ|と(く)|expliquer, théorie|説明:explication;小説:roman;説く:prêcher
紹|ショウ|—|présenter|紹介:présentation;自己紹介:se présenter;紹介状:lettre de recommandation
介|カイ|—|intermédiaire|紹介:présentation;介護:soins aux aînés;介入:intervention
伝|デン|つた(える)・つた(わる)|transmettre|伝える:transmettre;手伝う:aider;伝統:tradition
告|コク|つ(げる)|annoncer|広告:publicité;報告:rapport;告白:déclaration
報|ホウ|むく(いる)|informer, rapport|情報:information;報告:rapport;天気予報:météo
情|—|—|—|—
通|ツウ|とお(る)・かよ(う)|passer, trafic|交通:circulation;通信:communication;通訳:interprète
訳|ヤク|わけ|traduire, raison|通訳:interprète;翻訳:traduction;申し訳ない:désolé
訪|ホウ|おとず(れる)・たず(ねる)|visiter|訪問:visite;訪れる:visiter;来訪:venue
問|モン|と(う)・と(い)|question|問題:problème;質問:question;訪問:visite
題|ダイ|—|sujet, titre|問題:problème;宿題:devoirs;話題:sujet de conversation
質|シツ・シチ|—|qualité, question|質問:question;品質:qualité;性質:nature
答|トウ|こた(える)|répondre|答え:réponse;回答:réponse;返答:réplique
例|レイ|たと(える)|exemple|例えば:par exemple;例:exemple;例外:exception
示|ジ・シ|しめ(す)|montrer|指示:instruction;示す:indiquer;表示:affichage
表|—|—|—|—
現|ゲン|あらわ(れる)|apparaître, actuel|現在:présent;現金:argent liquide;表現:expression
示|—|—|—|—
語|—|—|—|—
詩|シ|—|poème|詩:poème;詩人:poète;漢詩:poème chinois
詞|シ|—|mot, parole|名詞:nom;動詞:verbe;歌詞:paroles
辞|ジ|や(める)|démissionner, mot|辞書:dictionnaire;辞める:quitter;お世辞:flatterie
典|テン|—|règle, cérémonie|辞典:dictionnaire;古典:classique;式典:cérémonie
注|チュウ|そそ(ぐ)|verser, noter|注意:attention;注文:commande;注射:piqûre
意|イ|—|sens, intention|意味:sens;意見:avis;注意:attention
味|ミ|あじ・あじ(わう)|goût, sens|意味:sens;趣味:passe-temps;味:goût
識|シキ|—|connaître, discerner|知識:connaissance;意識:conscience;常識:bon sens
知|—|—|—|—
解|カイ|と(く)・と(ける)|comprendre, résoudre|理解:compréhension;解決:résolution;解く:dénouer
覧|ラン|—|regarder|一覧:liste;展覧会:exposition;遊覧:excursion
観|カン|—|observer, vue|観光:tourisme;観察:observation;楽観:optimisme
察|—|—|—|—
調|チョウ|しら(べる)・ととの(う)|examiner, ton|調べる:enquêter;調子:forme;調査:enquête
査|サ|—|enquêter|調査:enquête;検査:examen;審査:évaluation
検|ケン|—|examiner|検査:examen;検討:étude;点検:inspection
研|ケン|と(ぐ)|aiguiser, étudier|研究:recherche;研修:formation;研ぐ:aiguiser
究|キュウ|きわ(める)|étudier à fond|研究:recherche;追究:poursuite;究極:ultime
習|—|—|—|—
訓|クン|—|enseignement, lecture kun|訓練:entraînement;訓読み:lecture japonaise;教訓:leçon
練|レン|ね(る)|s’exercer, pétrir|練習:entraînement;訓練:entraînement;洗練:raffinement
講|コウ|—|conférence, cours|講義:cours magistral;講演:conférence;講師:intervenant
演|エン|—|jouer, représenter|演奏:interprétation musicale;出演:apparition;講演:conférence
劇|ゲキ|—|théâtre, drame|劇:pièce;演劇:théâtre;喜劇:comédie
芸|ゲイ|—|art, talent|芸術:art;文芸:littérature;芸能:spectacle
術|ジュツ|すべ|technique, art|技術:technique;手術:opération;美術:beaux-arts
技|ギ|わざ|technique, habileté|技術:technique;特技:talent particulier;技:technique
""".strip().splitlines()
