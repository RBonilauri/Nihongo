# Phrases d'exemple des connecteurs (2 emplois différents par connecteur)
# clé = texte français de la 1re colonne du tableau « 接続詞 — Connecteurs »
EX = {
 'd’abord': [('まず、手を洗ってください。', 'Tout d’abord, lavez-vous les mains.'), ('まず、自己紹介をします。', 'D’abord, je vais me présenter.')],
 'ensuite': [('朝ごはんを食べて、それから学校に行きます。', 'Je prends mon petit-déjeuner, ensuite je vais à l’école.'), ('まっすぐ行って、それから右に曲がってください。', 'Allez tout droit, puis tournez à droite.')],
 'et puis': [('東京に行きました。そして、京都にも行きました。', 'Je suis allé à Tokyo. Et puis je suis aussi allé à Kyoto.'), ('この町は静かで、そして安全です。', 'Cette ville est calme, et sûre.')],
 'de plus': [('この店は安いです。それに、おいしいです。', 'Ce restaurant est bon marché. De plus, c’est bon.'), ('今日は雨です。それに、風も強いです。', 'Aujourd’hui il pleut. En plus, le vent est fort.')],
 'mais': [('行きたいです。でも、お金がありません。', 'J’ai envie d’y aller. Mais je n’ai pas d’argent.'), ('日本語は難しいです。でも、おもしろいです。', 'Le japonais est difficile. Mais c’est passionnant.')],
 'cependant': [('計画は良かったです。しかし、時間が足りませんでした。', 'Le plan était bon. Cependant, le temps a manqué.'), ('日本は小さい国です。しかし、人口は多いです。', 'Le Japon est un petit pays. Cependant, sa population est nombreuse.')],
 'mais (familier)': [('高いけど、買います。', 'C’est cher, mais je l’achète.'), ('行きたかったけど、行けなかった。', 'Je voulais y aller, mais je n’ai pas pu.')],
 'donc / c’est pourquoi': [('雨です。だから、傘を持っていきます。', 'Il pleut. Donc j’emporte un parapluie.'), ('昨日は疲れていました。だから、早く寝ました。', 'J’étais fatigué hier. C’est pourquoi je me suis couché tôt.')],
 'alors / du coup': [('電車が止まりました。それで、遅れました。', 'Le train s’est arrêté. Du coup, je suis arrivé en retard.'), ('それで、どうなりましたか。', 'Et alors, qu’est-ce qui s’est passé ?')],
 'alors, bon (pour conclure)': [('じゃあ、行きましょう。', 'Bon, allons-y.'), ('「コーヒーは苦手です。」「じゃあ、お茶はどうですか。」', '« Je n’aime pas trop le café. » « Alors, que diriez-vous d’un thé ? »')],
 'au fait': [('ところで、田中さんは元気ですか。', 'Au fait, Tanaka-san va bien ?'), ('ところで、今何時ですか。', 'Au fait, quelle heure est-il ?')],
 'par exemple': [('日本の食べ物、たとえば、寿司が好きです。', 'J’aime la cuisine japonaise, par exemple les sushis.'), ('たとえば、明日はどうですか。', 'Par exemple, demain, ça vous irait ?')],
 'en somme': [('つまり、行きたくないんですね。', 'En somme, tu n’as pas envie d’y aller, n’est-ce pas ?'), ('父の兄、つまり伯父は医者です。', 'Le frère de mon père, c’est-à-dire mon oncle, est médecin.')],
 'enfin / pour finir': [('最後に、ありがとうございました。', 'Pour finir, merci beaucoup.'), ('最後に、もう一度確認します。', 'Enfin, je vérifie encore une fois.')],
}

# lectures corrigées à la main quand l'automatique se trompe
KANA = {
 '今日は雨です。それに、風も強いです。': 'きょうはあめです。それに、かぜもつよいです。',
 '日本は小さい国です。しかし、人口は多いです。': 'にほんはちいさいくにです。しかし、じんこうはおおいです。',
 '電車が止まりました。それで、遅れました。': 'でんしゃがとまりました。それで、おくれました。',
 '日本の食べ物、たとえば、寿司が好きです。': 'にほんのたべもの、たとえば、すしがすきです。',
 '「コーヒーは苦手です。」「じゃあ、お茶はどうですか。」': '「コーヒーはにがてです。」「じゃあ、おちゃはどうですか。」',
}
