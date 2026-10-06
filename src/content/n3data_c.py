import os, sys
# -*- coding: utf-8 -*-
G = {}
G['Actions et mouvements'] = """
動|ドウ|うご(く)・うご(かす)|bouger|動く:bouger;運動:sport;自動車:voiture
運|ウン|はこ(ぶ)|transporter, sort|運転:conduite;運ぶ:transporter;運動:exercice
働|ドウ|はたら(く)|travailler|働く:travailler;労働:travail;共働き:double revenu
労|ロウ|—|peine, travail|労働:travail;苦労:peine;疲労:fatigue
押|オウ|お(す)|pousser|押す:pousser;押し入れ:placard;押さえる:maintenir
引|イン|ひ(く)|tirer|引く:tirer;引っ越し:déménagement;引き出し:tiroir
拾|シュウ・ジュウ|ひろ(う)|ramasser|拾う:ramasser;収拾:règlement;拾い物:trouvaille
捨|シャ|す(てる)|jeter|捨てる:jeter;切り捨て:arrondi inférieur;取捨:tri
抜|バツ|ぬ(く)・ぬ(ける)|arracher|抜く:retirer;抜ける:se détacher;選抜:sélection
投|—|—|—|—
打|ダ|う(つ)|frapper|打つ:frapper;打ち合わせ:réunion préparatoire;打撃:coup
倒|トウ|たお(れる)・たお(す)|renverser|倒れる:tomber;倒す:abattre;面倒:ennui
折|セツ|お(る)・お(れる)|plier, casser|折る:plier;右折:virage à droite;骨折:fracture
曲|キョク|ま(がる)・ま(げる)|courber, morceau|曲がる:tourner;曲:morceau;作曲:composition
回|—|—|—|—
乗|—|—|—|—
越|エツ|こ(える)・こ(す)|franchir|越える:franchir;引っ越す:déménager;追い越す:dépasser
超|チョウ|こ(える)|dépasser|超える:dépasser;超特急:train ultra-rapide;超過:excédent
追|ツイ|お(う)|poursuivre|追う:poursuivre;追加:ajout;追い越す:dépasser
逃|トウ|に(げる)・のが(す)|s’enfuir|逃げる:fuir;逃す:laisser échapper;逃亡:fuite
迎|ゲイ|むか(える)|accueillir|迎える:accueillir;迎え:accueil;歓迎:bienvenue
送|—|—|—|—
返|—|—|—|—
届|—|—|—|—
訪|—|—|—|—
着|—|—|—|—
到|トウ|—|arriver|到着:arrivée;到達:atteindre;周到:minutieux
達|タツ|—|atteindre, pluriel|友達:ami;発達:développement;配達:livraison
進|シン|すす(む)・すす(める)|avancer|進む:avancer;進歩:progrès;前進:progression
退|タイ|しりぞ(く)|reculer, se retirer|退院:sortie d’hôpital;退職:départ à la retraite;早退:départ anticipé
残|ザン|のこ(る)・のこ(す)|rester|残る:rester;残業:heures sup;残念:dommage
続|ゾク|つづ(く)・つづ(ける)|continuer|続く:continuer;続ける:poursuivre;連続:suite
加|—|—|—|—
増|ゾウ|ふ(える)・ふ(やす)|augmenter|増える:augmenter;増加:accroissement;増やす:accroître
減|ゲン|へ(る)・へ(らす)|diminuer|減る:diminuer;減少:baisse;軽減:allègement
省|ショウ・セイ|はぶ(く)・かえり(みる)|économiser, ministère|省略:abrégé;反省:réflexion;外務省:ministère des Affaires étrangères
略|リャク|—|abréger|省略:omission;略す:abréger;戦略:stratégie
変|ヘン|か(わる)・か(える)|changer, étrange|変:étrange;変化:changement;大変:difficile
替|タイ|か(える)|remplacer|替える:remplacer;両替:change;交替:alternance
換|カン|か(える)|échanger|交換:échange;換気:aération;乗り換え:correspondance
交|コウ|まじ(わる)・か(わす)|croiser, échanger|交通:circulation;交番:poste de police;交差点:carrefour
差|サ|さ(す)|différence, tendre|差:écart;交差点:carrefour;時差:décalage horaire
比|ヒ|くら(べる)|comparer|比べる:comparer;比較:comparaison;比例:proportion
並|ヘイ|なら(ぶ)・なら(べる)|aligner|並ぶ:faire la queue;並べる:aligner;並木:rangée d’arbres
続|—|—|—|—
構|コウ|かま(える)|structure, soin|結構:très bien;構造:structure;構わない:peu importe
造|ゾウ|つく(る)|fabriquer|製造:fabrication;構造:structure;造る:construire
製|セイ|—|fabriquer|製品:produit;日本製:fabriqué au Japon;製造:fabrication
建|ケン・コン|た(てる)・た(つ)|construire|建物:bâtiment;建築:architecture;建てる:construire
築|チク|きず(く)|bâtir|建築:architecture;新築:construction neuve;築く:ériger
設|セツ|もう(ける)|établir|設備:équipement;設計:conception;建設:construction
計|—|—|—|—
試|—|—|—|—
測|ソク|はか(る)|mesurer|測る:mesurer;予測:prévision;観測:observation
量|リョウ|はか(る)|quantité|量:quantité;大量:grande quantité;測量:arpentage
乱|ラン|みだ(れる)|désordre|乱暴:violent;混乱:confusion;乱れる:se dérégler
混|コン|ま(ざる)・こ(む)|mélanger, bondé|混む:être bondé;混雑:affluence;混ぜる:mélanger
""".strip().splitlines()
G['Personnes, corps et vie'] = """
員|—|—|—|—
彼|ヒ|かれ・かの|il, lui|彼:il, petit ami;彼女:elle, petite amie;彼ら:eux
婦|フ|—|femme mariée|夫婦:couple;主婦:femme au foyer;婦人:dame
夫|フ・フウ|おっと|mari|夫:mon mari;夫婦:couple;夫人:Madame
妻|サイ|つま|épouse|妻:mon épouse;夫妻:M. et Mme;愛妻:épouse chérie
主|シュ|ぬし・おも|maître, principal|主人:mari, maître;主婦:femme au foyer;主な:principal
客|キャク・カク|—|client, invité|お客さん:client;乗客:passager;観光客:touriste
師|シ|—|maître, professionnel|医師:médecin;教師:enseignant;美容師:coiffeur
者|シャ|もの|personne|学者:savant;記者:journaliste;若者:jeune
歳|サイ・セイ|—|âge, ans|二十歳:vingt ans;歳:âge;万歳:vive
若|ジャク|わか(い)|jeune|若い:jeune;若者:jeunes;若干:quelque peu
老|ロウ|お(いる)・ふ(ける)|vieux|老人:personne âgée;老後:retraite;年老いる:vieillir
童|ドウ|わらべ|enfant|児童:enfant;童話:conte;童謡:chanson enfantine
児|ジ・ニ|—|enfant|児童:enfant;育児:éducation d’un enfant;小児科:pédiatrie
育|イク|そだ(てる)・そだ(つ)|élever, grandir|教育:éducation;育てる:élever;体育:éducation physique
産|—|—|—|—
命|メイ・ミョウ|いのち|vie, ordre|生命:vie;運命:destin;命令:ordre
死|シ|し(ぬ)|mourir|死ぬ:mourir;死亡:décès;死体:cadavre
亡|ボウ・モウ|な(くなる)|mort, disparaître|死亡:décès;亡くなる:décéder;滅亡:chute
殺|サツ・サイ|ころ(す)|tuer|殺す:tuer;殺人:meurtre;自殺:suicide
傷|ショウ|きず・いた(む)|blessure|傷:blessure;傷つく:être blessé;負傷:blessure
負|フ|ま(ける)・お(う)|perdre, porter|負ける:perdre;勝負:match;負担:charge
勝|ショウ|か(つ)・まさ(る)|gagner|勝つ:gagner;勝利:victoire;優勝:victoire (championnat)
敗|ハイ|やぶ(れる)|échouer|失敗:échec;敗北:défaite;勝敗:victoire ou défaite
失|シツ|うしな(う)|perdre|失敗:échec;失礼:impolitesse;失う:perdre
成|セイ・ジョウ|な(る)・な(す)|devenir, réussir|成功:réussite;成長:croissance;完成:achèvement
功|コウ|—|mérite, succès|成功:réussite;功績:mérite;年功:ancienneté
病|—|—|—|—
患|カン|わずら(う)|souffrir de|患者:patient;急患:urgence;患部:partie malade
康|コウ|—|santé, paix|健康:santé;小康:accalmie;康:paix
健|ケン|すこ(やか)|robuste|健康:santé;保健:hygiène;健全:sain
療|リョウ|—|soigner|治療:traitement;医療:soins médicaux;療養:convalescence
症|ショウ|—|symptôme|症状:symptôme;花粉症:rhume des foins;熱中症:coup de chaleur
状|ジョウ|—|état, lettre|状態:état;症状:symptôme;年賀状:carte de vœux
胃|イ|—|estomac|胃:estomac;胃腸:appareil digestif;胃薬:médicament pour l’estomac
腸|チョウ|—|intestin|腸:intestin;胃腸:digestion;大腸:gros intestin
肩|ケン|かた|épaule|肩:épaule;肩こり:épaules raides;双肩:les deux épaules
胸|キョウ|むね|poitrine|胸:poitrine;胸元:décolleté;度胸:cran
腕|ワン|うで|bras|腕:bras;腕時計:montre;腕前:habileté
指|シ|ゆび・さ(す)|doigt, indiquer|指:doigt;指定:désignation;指輪:bague
髪|ハツ|かみ|cheveux|髪:cheveux;髪の毛:cheveu;散髪:coupe de cheveux
毛|モウ|け|poil, cheveu|毛:poil;毛糸:laine;羊毛:laine de mouton
顔|—|—|—|—
姿|シ|すがた|silhouette|姿:silhouette;姿勢:posture;後ろ姿:vu de dos
""".strip().splitlines()
