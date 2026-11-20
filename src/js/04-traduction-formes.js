
  /* ── traduction française approximative des formes verbales ──
     Principe : on conjugue le verbe français (sens du verbe japonais) pour quelques formes de base,
     puis on les insère dans des tournures types. Si le verbe est inconnu, repli sur l'infinitif seul. */
  var FRV = (function () {
    var VOW = /^[aeiouyàâäéèêëîïôöûùüœh]/i;
    // irréguliers : [je (présent), participe passé, auxiliaire 'a'/'e', nous (impératif), impératif tu]
    var IRR = {
      'être': ['suis', 'été', 'a', 'soyons', 'sois'], 'avoir': ['ai', 'eu', 'a', 'ayons', 'aie'], 'aller': ['vais', 'allé', 'e', 'allons', 'va'],
      'faire': ['fais', 'fait', 'a', 'faisons'], 'venir': ['viens', 'venu', 'e', 'venons'], 'voir': ['vois', 'vu', 'a', 'voyons'],
      'prendre': ['prends', 'pris', 'a', 'prenons'], 'pouvoir': ['peux', 'pu', 'a', null], 'vouloir': ['veux', 'voulu', 'a', 'voulons', 'veuille'],
      'savoir': ['sais', 'su', 'a', 'sachons', 'sache'], 'devoir': ['dois', 'dû', 'a', 'devons'], 'dire': ['dis', 'dit', 'a', 'disons'],
      'lire': ['lis', 'lu', 'a', 'lisons'], 'mettre': ['mets', 'mis', 'a', 'mettons'], 'partir': ['pars', 'parti', 'e', 'partons'],
      'sortir': ['sors', 'sorti', 'e', 'sortons'], 'dormir': ['dors', 'dormi', 'a', 'dormons'], 'ouvrir': ['ouvre', 'ouvert', 'a', 'ouvrons'],
      'courir': ['cours', 'couru', 'a', 'courons'], 'boire': ['bois', 'bu', 'a', 'buvons'], 'croire': ['crois', 'cru', 'a', 'croyons'],
      'vivre': ['vis', 'vécu', 'a', 'vivons'], 'suivre': ['suis', 'suivi', 'a', 'suivons'], 'rire': ['ris', 'ri', 'a', 'rions'],
      'plaire': ['plais', 'plu', 'a', 'plaisons'], 'battre': ['bats', 'battu', 'a', 'battons'], 'mourir': ['meurs', 'mort', 'e', 'mourons'],
      'naître': ['nais', 'né', 'e', 'naissons'], 'tenir': ['tiens', 'tenu', 'a', 'tenons'], 'asseoir': ['assieds', 'assis', 'a', 'asseyons'],
      'fuir': ['fuis', 'fui', 'a', 'fuyons'], 'sentir': ['sens', 'senti', 'a', 'sentons'], 'servir': ['sers', 'servi', 'a', 'servons'],
      'offrir': ['offre', 'offert', 'a', 'offrons'], 'couvrir': ['couvre', 'couvert', 'a', 'couvrons'], 'cueillir': ['cueille', 'cueilli', 'a', 'cueillons'],
      'bouillir': ['bous', 'bouilli', 'a', 'bouillons'], 'valoir': ['vaux', 'valu', 'a', 'valons'], 'vaincre': ['vaincs', 'vaincu', 'a', 'vainquons'],
      'coudre': ['couds', 'cousu', 'a', 'cousons'], 'résoudre': ['résous', 'résolu', 'a', 'résolvons'], 'inclure': ['inclus', 'inclus', 'a', 'incluons'],
      'frire': ['fris', 'frit', 'a', null], 'pleuvoir': ['pleus', 'plu', 'a', null], 'taire': ['tais', 'tu', 'a', 'taisons'], 'suffire': ['suffis', 'suffi', 'a', 'suffisons'],
      'cuire': ['cuis', 'cuit', 'a', 'cuisons'], 'paraître': ['parais', 'paru', 'a', 'paraissons'], 'connaître': ['connais', 'connu', 'a', 'connaissons']
    };
    // composés : dérivés d'un irréguliers (préfixe + base)
    var BASES = ['prendre', 'mettre', 'venir', 'tenir', 'faire', 'voir', 'dire', 'lire', 'courir', 'couvrir', 'offrir', 'partir', 'sortir', 'sentir', 'servir', 'dormir', 'battre', 'vivre', 'suivre', 'croire', 'plaire', 'cueillir', 'boire', 'cuire', 'paraître', 'connaître', 'naître', 'mourir', 'devoir', 'savoir', 'asseoir', 'valoir'];
    var AUX_E = { 'aller': 1, 'venir': 1, 'partir': 1, 'sortir': 1, 'mourir': 1, 'naître': 1, 'arriver': 1, 'entrer': 1, 'rentrer': 1, 'monter': 1, 'descendre': 1, 'tomber': 1, 'rester': 1, 'retourner': 1, 'décéder': 1, 'devenir': 1, 'revenir': 1, 'parvenir': 1, 'repartir': 1, 'ressortir': 1 };
    var GRAVE = { 'acheter': 1, 'racheter': 1, 'geler': 1, 'congeler': 1, 'peler': 1, 'modeler': 1, 'marteler': 1, 'ciseler': 1, 'démanteler': 1 };
    var CONS = '[bcdfghjklmnpqrstvwxz]';
    function lowFirst(s) { return s.charAt(0).toLowerCase() + s.slice(1); }
    function cap(s) { return s.charAt(0).toUpperCase() + s.slice(1); }

    // renvoie {pres, pp, aux, nous, imp} pour un infinitif, ou null si inconnu
    function conj(v) {
      var t = IRR[v], i, b;
      if (!t && /cevoir$/.test(v)) { var s0 = v.slice(0, -6); return { pres: s0 + 'çois', pp: s0 + 'çu', aux: 'a', nous: s0 + 'cevons', imp: s0 + 'çois' }; }
      if (!t) for (i = 0; i < BASES.length && !t; i++) { b = BASES[i]; if (v.length > b.length && v.slice(-b.length) === b) { var pre = v.slice(0, -b.length), tb = IRR[b]; t = [pre + tb[0], pre + tb[1], tb[2] === 'e' ? 'a' : tb[2], tb[3] ? pre + tb[3] : null, tb[4] ? pre + tb[4] : null]; if (AUX_E[v]) t[2] = 'e'; else if (b !== 'venir' && b !== 'partir' && b !== 'sortir' && b !== 'mourir' && b !== 'naître') t[2] = 'a'; } }
      if (t) return { pres: t[0], pp: t[1], aux: AUX_E[v] ? 'e' : t[2], nous: t[3], imp: t[4] || t[0] };
      var st = v.slice(0, -2), r;
      if (/er$/.test(v)) {
        st = v.slice(0, -2); var p = st;
        if (/(el|et)$/.test(st) && !GRAVE[v]) p = st + st.slice(-1);                      // appeler → appelle, jeter → jette
        else if (/é[bcdfgpt][lr]$/.test(st)) p = st.replace(/é([bcdfgpt][lr])$/, 'è$1');                                   // régler → règle
        else if (/é(ch|gl|tr)$/.test(st)) p = st.replace(/é(ch|gl|tr)$/, 'è$1');                                 // sécher → sèche
        else if (new RegExp('[eé]' + CONS + '$').test(st) && !/(ll|tt)$/.test(st)) p = st.replace(new RegExp('[eé](' + CONS + ')$'), 'è$1'); // lever → lève
        else if (/[ou]yer$/.test(v) || /ayer$/.test(v)) p = st.slice(0, -1) + 'i';       // nettoyer → nettoie, payer → paie
        var nous = /ger$/.test(v) ? st + 'eons' : /cer$/.test(v) ? st.slice(0, -1) + 'çons' : st + 'ons';
        return { pres: p + 'e', pp: st + 'é', aux: AUX_E[v] ? 'e' : 'a', nous: nous, imp: p + 'e' };
      }
      if (/oir$/.test(v)) {
        if (/cevoir$/.test(v)) { st = v.slice(0, -6); return { pres: st + 'çois', pp: st + 'çu', aux: 'a', nous: st + 'cevons', imp: st + 'çois' }; }
        return null;
      }
      if (/uire$/.test(v)) { st = v.slice(0, -2); return { pres: st + 's', pp: st + 't', aux: 'a', nous: st + 'sons', imp: st + 's' }; }
      if (/crire$/.test(v)) { st = v.slice(0, -2); return { pres: st + 's', pp: st + 't', aux: 'a', nous: st + 'vons', imp: st + 's' }; }
      if (/indre$/.test(v)) { st = v.slice(0, -5); return { pres: st + 'ins', pp: st + 'int', aux: 'a', nous: st + 'ignons', imp: st + 'ins' }; }
      if (/aître$/.test(v)) { st = v.slice(0, -5); return { pres: st + 'ais', pp: st + 'u', aux: 'a', nous: st + 'aissons', imp: st + 'ais' }; }
      if (/dre$/.test(v)) { st = v.slice(0, -2); return { pres: st + 's', pp: st + 'u', aux: AUX_E[v] ? 'e' : 'a', nous: st + 'ons', imp: st + 's' }; }
      if (/ir$/.test(v)) { st = v.slice(0, -2); return { pres: st + 'is', pp: st + 'i', aux: 'a', nous: st + 'issons', imp: st + 'is' }; }
      return null;
    }

    function parse(fr) {
      var s = (fr || '').replace(/\(.*?\)/g, '').split(/[,;\/]/)[0].trim(); if (!s) return null;
      s = s.replace(/\s+(sur|à|de|en|dans|avec|pour|par|vers|après|contre|chez)$/i, '').trim();
      var pr = false, m = s.match(/^(se\s+|s['’])(.+)$/i); if (m) { pr = true; s = m[2]; }
      var w = s.split(/\s+/), v = w[0].toLowerCase(); if (!/(er|ir|re|oir)$/.test(v) || /^(il|elle|on)$/.test(v)) return null;
      var o = { pr: pr, v: v, rest: w.slice(1).join(' ').toLowerCase(), c: conj(v) };
      o.R = o.rest ? ' ' + o.rest : '';
      o.inf = (pr ? (VOW.test(v) ? 's’' : 'se ') : '') + v + o.R;                // se lever
      o.inf1 = (pr ? (VOW.test(v) ? 'm’' : 'me ') : '') + v + o.R;                // me lever
      if (o.c) {
        var c = o.c, R = o.R;
        var je = function (p) { return (pr ? (VOW.test(p) ? 'Je m’' : 'Je me ') : (VOW.test(p) ? 'J’' : 'Je ')) + p + R; };
        o.J = je(c.pres);
        o.JN = (pr ? (VOW.test(c.pres) ? 'Je ne m’' : 'Je ne me ') : (VOW.test(c.pres) ? 'Je n’' : 'Je ne ')) + c.pres + ' pas' + R;
        var e = pr || c.aux === 'e';
        o.PC = (pr ? 'Je me suis ' : e ? 'Je suis ' : 'J’ai ') + c.pp + R;
        o.PCN = (pr ? 'Je ne me suis pas ' : e ? 'Je ne suis pas ' : 'Je n’ai pas ') + c.pp + R;
        o.FUT = (e ? 'serai' : 'aurai');
        o.IMP = cap(c.imp) + (pr ? '-toi' : '') + R;
        o.IMPN = (pr ? 'Ne ' + (VOW.test(c.imp) ? 't’' : 'te ') : (VOW.test(c.imp) ? 'N’' : 'Ne ')) + c.imp + ' pas' + R;
        o.NOUS = c.nous ? cap(c.nous) + (pr ? '-nous' : '') + R : null;
        o.PPR = (pr ? (VOW.test(c.pres) ? 'me' : 'me') : '');
      }
      return o;
    }


    /* ── phrases complètes (exemples des verbes) ── */
    var SP3 = { 'être': 'est', 'avoir': 'a', 'aller': 'va', 'pouvoir': 'peut', 'vouloir': 'veut', 'valoir': 'vaut' };
    var IMPST = { 'être': 'ét', 'avoir': 'av', 'pouvoir': 'pouv', 'savoir': 'sav', 'vouloir': 'voul', 'devoir': 'dev', 'pleuvoir': 'pleuv' };
    function third(p, v) {
      if (SP3[v]) return SP3[v];
      if (/aître$/.test(v)) return p.replace(/ais$/, 'aît');
      if (/[eé]$/.test(p)) return p;
      if (/x$/.test(p)) return p.slice(0, -1) + 't';
      if (/[dt]s$/.test(p) && !/^(vois|dis|lis|suis|vis|ris|fuis)$/.test(p)) return p.slice(0, -1);
      if (/s$/.test(p)) return p.slice(0, -1) + 't';
      return p;
    }
    function elide(tokens) {
      var out = '';
      tokens.filter(Boolean).forEach(function (t, i, a) {
        var nx = a[i + 1];
        if (nx && /^(je|ne|me|se|te)$/.test(t) && VOW.test(nx)) { out += t.charAt(0) + '’'; }
        else out += t + (nx ? ' ' : '');
      });
      return out;
    }
    // renvoie la phrase française, ou null si le verbe n’est pas conjugable
    function sent(fv, comp, negc, subj, tense) {
      var o = get(fv); if (!o || !o.c) return null;
      var fem = /\*$/.test(subj || ''); subj = (subj || '').replace(/\*$/, '');
      var je = !subj, S = je ? 'je' : subj, c = o.c, pr = o.pr, e = pr || c.aux === 'e';
      var refl = pr ? (je ? 'me' : 'se') : '';
      var pres = je ? c.pres : third(c.pres, o.v);
      var pp = c.pp + (fem && e && !/s$/.test(c.pp) ? 'e' : '');
      var ax = e ? (je ? 'suis' : 'est') : (je ? 'ai' : 'a');
      var cm = comp || '', ng = negc || comp || '';
      var imp = null;
      if (IMPST[o.v] || c.nous) imp = (IMPST[o.v] || c.nous.replace(/ons$/, '')) + (je ? 'ais' : 'ait');
      var T = {
        pres: [S, refl, pres, cm],
        neg: [S, 'ne', refl, pres, 'pas', ng],
        pc: [S, refl, ax, pp, cm],
        pcneg: [S, 'ne', refl, ax, 'pas', pp, ng],
        imp: imp ? [S, refl, imp, cm] : null,
        impneg: imp ? [S, 'ne', refl, imp, 'pas', ng] : null,
        en: [S, je ? 'suis' : 'est', 'en train de', pr ? (je ? 'me' : 'se') : '', o.v, cm],
        des: je ? [S, 'veux', pr ? 'me' : '', o.v, cm] : null
      }[tense];
      if (!T) return null;
      var r = elide(T); r = r.charAt(0).toUpperCase() + r.slice(1);
      return r.replace(/\s+/g, ' ').replace(/\bde ([aeiouyéèêhœ])/g, function (m, x) { return 'd’' + x; }).replace(/ de d’/g, ' d’') + '.';
    }


    /* ── phrase modèle par forme : cadre japonais (avant / après la forme) + phrase française ──
       Cadres génériques, choisis pour rester grammaticaux avec n’importe quel verbe (sujet « je » ou sans agent) ;
       la phrase française vient du même moteur de conjugaison. null si la forme n’a pas de cadre. */
    var KF = { '今日は': 'きょうは', '明日': 'あした', '明日は': 'あしたは', '昨日': 'きのう', '昨日は': 'きのうは', '私は': 'わたしは', 'あなたに': 'あなたに', '弟に': 'おとうとに', 'ここでは': 'ここでは', 'あの時は': 'あのときは', 'これは': 'これは', 'まず': 'まず', '出かけました': 'でかけました', '休みます': 'やすみます', '電話します': 'でんわします', '電話': 'でんわ', 'びっくりしました': 'びっくりしました', 'なりました': 'なりました', '買います': 'かいます', '人': 'ひと', '思っています': 'おもっています', '時々': 'ときどき', '今': 'いま', '休みの日は': 'やすみのひは', '寝たりします': 'ねたりします', '怒られます': 'おこられます', '元気になります': 'げんきになります', '一緒に': 'いっしょに', '私が': 'わたしが' };
    function kanaOf(t) { var o = t; Object.keys(KF).sort(function (a, b) { return b.length - a.length; }).forEach(function (k) { o = o.split(k).join(KF[k]); }); return o; }
    function te2(o) { return o.inf.replace(/^s’/, 't’').replace(/^se /, 'te '); }
    var VF = {   // [avant, après, fr(o)]
      'Négatif simple': ['今日は', '。', function (o) { return 'Aujourd’hui, ' + lowFirst(o.JN) + '.'; }],
      'Polie, présent': ['明日', '。', function (o) { return 'Demain, je vais ' + o.inf1 + '.'; }],
      'Polie, négatif': ['明日は', '。', function (o) { return 'Demain, ' + lowFirst(o.JN) + '.'; }],
      'Polie, passé': ['昨日', '。', function (o) { return 'Hier, ' + lowFirst(o.PC) + '.'; }],
      'Polie, passé négatif': ['昨日は', '。', function (o) { return 'Hier, ' + lowFirst(o.PCN) + '.'; }],
      'Passé simple': ['昨日', '。', function (o) { return 'Hier, ' + lowFirst(o.PC) + '.'; }],
      'Passé négatif simple': ['昨日は', '。', function (o) { return 'Hier, ' + lowFirst(o.PCN) + '.'; }],
      'Forme en て': ['まず', '、それから休みます。', function (o) { return 'D’abord, ' + lowFirst(o.J) + ', puis je me repose.'; }],
      'て négatif': ['', '、出かけました。', function (o) { return 'Je suis sorti sans ' + o.inf + '.'; }],
      'Désidératif': ['私は', '。', function (o) { return 'Je veux ' + o.inf1 + '.'; }],
      'Désidératif négatif': ['私は', '。', function (o) { return 'Je ne veux pas ' + o.inf1 + '.'; }],
      'Désidératif passé': ['私は', '。', function (o) { return 'Je voulais ' + o.inf1 + '.'; }],
      'Désidératif passé négatif': ['私は', '。', function (o) { return 'Je ne voulais pas ' + o.inf1 + '.'; }],
      'Potentiel': ['私は', '。', function (o) { return 'Je peux ' + o.inf1 + '.'; }],
      'Passif': ['', 'ことがあります。', function (o) { return 'Il m’arrive de subir l’action de « ' + o.inf + ' ».'; }],
      'Causatif': ['弟に', 'ことがあります。', function (o) { return 'Il m’arrive de faire ' + (o.v + o.R) + ' (qqn).'; }],
      'Causatif-passif': ['', 'ことがあります。', function (o) { return 'Il m’arrive d’être forcé de ' + o.inf + '.'; }],
      'Volitif': ['', 'と思っています。', function (o) { return 'J’envisage de ' + o.inf1 + '.'; }],
      'Impératif': ['', '！', function (o) { return (o.c ? o.IMP : cap(o.inf)) + ' !'; }],
      'Interdiction': ['ここでは', '。', function (o) { return 'Ici, ' + (o.c ? lowFirst(o.IMPN) : 'ne pas ' + o.inf) + ' !'; }],
      'Conditionnel ば': ['', 'いいです。', function (o) { return 'Il suffit de ' + o.inf + '.'; }],
      'Conditionnel たら': ['', '、電話します。', function (o) { return o.c ? 'Quand ' + (o.c.aux === 'e' || o.pr ? (o.pr ? 'je me serai ' : 'je serai ') : 'j’aurai ') + o.c.pp + o.R + ', je t’appelle.' : 'Quand on aura ' + o.inf + ', je t’appelle.'; }],
      'Potentiel négatif': ['私は', '。', function (o) { return 'Je ne peux pas ' + o.inf1 + '.'; }],
      'Potentiel passé': ['昨日は', '。', function (o) { return 'Hier, j’ai pu ' + o.inf1 + '.'; }],
      'Potentiel poli': ['私は', '。', function (o) { return 'Je peux ' + o.inf1 + '.'; }],
      'Potentiel poli négatif': ['私は', '。', function (o) { return 'Je ne peux pas ' + o.inf1 + '.'; }],
      'Passif négatif': ['', 'ことはありません。', function (o) { return 'Il ne m’arrive jamais de subir l’action de « ' + o.inf + ' ».'; }],
      'Passif passé': ['', 'ことがあります。', function (o) { return 'J’ai déjà subi l’action de « ' + o.inf + ' ».'; }],
      'Passif poli': ['時々', '。', function (o) { return 'Parfois, je subis l’action de « ' + o.inf + ' ».'; }],
      'Passif poli négatif': ['めったに', '。', function (o) { return 'Je ne subis presque jamais l’action de « ' + o.inf + ' ».'; }],
      'Causatif négatif': ['弟に', 'ことがあります。', function (o) { return 'Il m’arrive de ne pas faire ' + (o.v + o.R) + ' (qqn).'; }],
      'Causatif passé': ['弟に', 'ことがあります。', function (o) { return 'Il m’est arrivé de faire ' + (o.v + o.R) + ' (qqn).'; }],
      'Causatif poli': ['時々、弟に', '。', function (o) { return 'Parfois, je fais ' + o.inf + ' (qqn).'; }],
      'Causatif poli négatif': ['弟には', '。', function (o) { return 'Je ne fais pas ' + o.inf + ' (qqn).'; }],
      'Causatif-passif négatif': ['', 'ことがあります。', function (o) { return 'Il m’arrive de ne pas être forcé de ' + o.inf + '.'; }],
      'Causatif-passif passé': ['', 'ことがあります。', function (o) { return 'Il m’est arrivé d’être forcé de ' + o.inf + '.'; }],
      'Causatif-passif poli': ['時々', '。', function (o) { return 'Parfois, je suis forcé de ' + o.inf + '.'; }],
      'Causatif-passif poli négatif': ['めったに', '。', function (o) { return 'Je ne suis presque jamais forcé de ' + o.inf + '.'; }],
      'En cours': ['今', '。', function (o) { return 'En ce moment, je suis en train de ' + o.inf1 + '.'; }],
      'En cours négatif': ['今', '。', function (o) { return 'En ce moment, je ne suis pas en train de ' + o.inf1 + '.'; }],
      'En cours passé': ['昨日', '。', function (o) { return 'Hier, j’étais en train de ' + o.inf1 + '.'; }],
      'En cours passé négatif': ['昨日は', '。', function (o) { return 'Hier, je n’étais pas en train de ' + o.inf1 + '.'; }],
      'Demande': ['', '。', function (o) { return 'Je vous prie de ' + o.inf.replace(/^s’/, 'vous ').replace(/^se /, 'vous ') + '.'; }],
      'Demande négatif': ['', '。', function (o) { return 'Je vous prie de ne pas ' + o.inf.replace(/^s’/, 'vous ').replace(/^se /, 'vous ') + '.'; }],
      'Obligation': ['私は', '。', function (o) { return 'Je dois ' + o.inf1 + '.'; }],
      'Absence d’obligation': ['私は', '。', function (o) { return 'Je n’ai pas besoin de ' + o.inf1 + '.'; }],
      'Obligation orale': ['私は', '。', function (o) { return 'Je dois ' + o.inf1 + '.'; }],
      'Si négatif': ['', '、怒られます。', function (o) { return o.c ? 'Si ' + lowFirst(o.JN) + ', je me fais gronder.' : null; }],
      'Quand négatif': ['', '、電話します。', function (o) { return o.c ? 'Si ' + lowFirst(o.PCN) + ', je t’appelle.' : null; }],
      'Conditionnel と': ['', '、元気になります。', function (o) { return o.c ? 'Quand ' + lowFirst(o.J) + ', je me sens bien.' : null; }],
      'Conditionnel なら': ['', '、これがいいです。', function (o) { return 'Si c’est pour ' + o.inf1 + ', ceci est mieux.'; }],
      'Invitation': ['一緒に', '。', function (o) { return o.c && o.NOUS ? o.NOUS + ' ensemble !' : null; }],
      'Proposition': ['私が', '。', function (o) { return 'Dois-je ' + o.inf1 + ' ?'; }],
      'Ordre poli': ['', '！', function (o) { return (o.c ? o.IMP : cap(o.inf)) + ' !'; }],
      'Énumération': ['休みの日は', '、寝たりします。', function (o) { return o.c ? 'Les jours de congé, ' + lowFirst(o.J) + ', ou je dors.' : null; }],
      'Énumération négatif': ['休みの日は', '、寝たりします。', function (o) { return 'Les jours de congé, il m’arrive de ne pas ' + o.inf1 + ' et de dormir.'; }],
      'Regret': ['', '。', function (o) { return 'J’aurais dû ' + o.inf1 + '.'; }],
      'Regret négatif': ['', '。', function (o) { return 'Je n’aurais pas dû ' + o.inf1 + '.'; }],
      'Souhait sur autrui (てほしい)': ['あなたに', '。', function (o) { return 'Je voudrais que tu le fasses (' + o.inf + ').'; }],
      'Souhait sur autrui négatif (ないでほしい)': ['あなたに', '。', function (o) { return 'Je voudrais que tu ne le fasses pas (' + o.inf + ').'; }],
      'Souhait sur autrui négatif (てほしくない)': ['あなたに', '。', function (o) { return 'Je ne veux pas que tu le fasses (' + o.inf + ').'; }],
      'Souhait sur autrui passé (てほしかった)': ['あなたに', '。', function (o) { return 'J’aurais voulu que tu le fasses (' + o.inf + ').'; }],
      'Souhait sur autrui passé négatif (ないでほしかった)': ['あなたに', '。', function (o) { return 'J’aurais voulu que tu ne le fasses pas (' + o.inf + ').'; }]
    };
    function adjFr(fr) { var s = (fr || '').replace(/\(.*?\)/g, '').split(/[\/,;]/)[0].trim(); return s ? lowFirst(s) : ''; }
    var AF = {
      'Adjectif négatif': ['これは', '。', function (a) { return 'Ce n’est pas ' + a + '.'; }],
      'Adjectif passé': ['あの時は', '。', function (a) { return 'À ce moment-là, c’était ' + a + '.'; }],
      'Adjectif passé négatif': ['あの時は', '。', function (a) { return 'À ce moment-là, ce n’était pas ' + a + '.'; }],
      'Adjectif en て': ['これは', '、びっくりしました。', function (a) { return 'Comme c’est ' + a + ', j’ai été surpris.'; }],
      'Adverbe': ['', 'なりました。', function (a) { return 'C’est devenu ' + a + '.'; }],
      'Adjectif poli': ['これは', '。', function (a) { return 'C’est ' + a + '.'; }],
      'Adjectif poli négatif': ['これは', '。', function (a) { return 'Ce n’est pas ' + a + '.'; }],
      'Adjectif poli passé': ['あの時は', '。', function (a) { return 'À ce moment-là, c’était ' + a + '.'; }],
      'Adjectif poli passé négatif': ['あの時は', '。', function (a) { return 'À ce moment-là, ce n’était pas ' + a + '.'; }],
      'Adjectif condition': ['', '、買います。', function (a) { return 'Si c’est ' + a + ', j’achète.'; }]
    };
    var cache = {};
    function get(fr) { if (!(fr in cache)) cache[fr] = parse(fr); return cache[fr]; }
    var Q = function (s) { return '« ' + s + ' »'; };
    // formes : renvoie un tableau de tournures
    var F = {
      'Polie, présent': function (o) { return o.c ? [Q(o.J), Q('Je vais ' + o.inf1)] : [o.inf + ' (présent, poli)']; },
      'Polie, négatif': function (o) { return o.c ? [Q(o.JN)] : ['ne pas ' + o.inf + ' (poli)']; },
      'Polie, passé': function (o) { return o.c ? [Q(o.PC)] : [o.inf + ' au passé (poli)']; },
      'Polie, passé négatif': function (o) { return o.c ? [Q(o.PCN)] : ['ne pas ' + o.inf + ' au passé (poli)']; },
      'Négatif simple': function (o) { return o.c ? [Q(o.JN), Q('Ne pas ' + o.inf)] : ['ne pas ' + o.inf]; },
      'Passé simple': function (o) { return o.c ? [Q(o.PC)] : [o.inf + ' au passé']; },
      'Passé négatif simple': function (o) { return o.c ? [Q(o.PCN)] : ['ne pas ' + o.inf + ' au passé']; },
      'Forme en て': function (o) { return o.c ? [Q('… et ' + o.inf), Q(o.IMP + ', s’il te plaît')] : [o.inf + ', puis… / s’il vous plaît']; },
      'て négatif': function (o) { return [Q('Sans ' + o.inf)]; },
      'Désidératif': function (o) { return [Q('Je veux ' + o.inf1), Q('J’aimerais ' + o.inf1)]; },
      'Désidératif passé': function (o) { return [Q('Je voulais ' + o.inf1)]; },
      'Désidératif passé négatif': function (o) { return [Q('Je ne voulais pas ' + o.inf1)]; },
      'Souhait sur autrui (てほしい)': function (o) { return [Q('Je voudrais que tu… (' + o.inf + ')')]; },
      'Souhait sur autrui négatif (ないでほしい)': function (o) { return [Q('Je voudrais que tu ne… pas (' + o.inf + ')')]; },
      'Souhait sur autrui négatif (てほしくない)': function (o) { return [Q('Je ne veux pas que tu… (' + o.inf + ')')]; },
      'Souhait sur autrui passé (てほしかった)': function (o) { return [Q('J’aurais voulu que tu… (' + o.inf + ')')]; },
      'Souhait sur autrui passé négatif (ないでほしかった)': function (o) { return [Q('J’aurais voulu que tu ne… pas (' + o.inf + ')')]; },
      'Potentiel': function (o) { return [Q('Je peux ' + o.inf1), Q('Être capable de ' + o.inf)]; },
      'Passif': function (o) { return o.c && !o.pr && !o.rest ? [Q('Être ' + o.c.pp + ' (par quelqu’un)')] : ['Subir l’action de « ' + o.inf + ' »']; },
      'Causatif': function (o) { return [Q('Faire ' + o.inf + ' (qqn)'), Q('Laisser ' + o.inf)]; },
      'Causatif-passif': function (o) { return [Q('Être forcé de ' + o.inf)]; },
      'Potentiel passé': function (o) { return [Q('J’ai pu ' + o.inf1)]; },
      'Potentiel poli': function (o) { return [Q('Je peux ' + o.inf1) + ' (poli)']; },
      'Potentiel poli négatif': function (o) { return [Q('Je ne peux pas ' + o.inf1) + ' (poli)']; },
      'Passif négatif': function (o) { return ['Ne pas subir l’action de « ' + o.inf + ' »']; },
      'Passif passé': function (o) { return ['Avoir subi l’action de « ' + o.inf + ' »']; },
      'Passif poli': function (o) { return ['Subir l’action de « ' + o.inf + ' » (poli)']; },
      'Passif poli négatif': function (o) { return ['Ne pas subir l’action de « ' + o.inf + ' » (poli)']; },
      'Causatif négatif': function (o) { return [Q('Ne pas faire ' + (o.v + o.R) + ' (qqn)'), Q('Ne pas laisser ' + o.inf)]; },
      'Causatif passé': function (o) { return [Q('Avoir fait ' + o.inf + ' (qqn)'), Q('Avoir laissé ' + o.inf)]; },
      'Causatif poli': function (o) { return [Q('Faire ' + o.inf + ' (qqn)') + ' (poli)']; },
      'Causatif poli négatif': function (o) { return [Q('Ne pas faire ' + (o.v + o.R) + ' (qqn)') + ' (poli)']; },
      'Causatif-passif négatif': function (o) { return [Q('Ne pas être forcé de ' + o.inf)]; },
      'Causatif-passif passé': function (o) { return [Q('Avoir été forcé de ' + o.inf)]; },
      'Causatif-passif poli': function (o) { return [Q('Être forcé de ' + o.inf) + ' (poli)']; },
      'Causatif-passif poli négatif': function (o) { return [Q('Ne pas être forcé de ' + o.inf) + ' (poli)']; },
      'En cours passé': function (o) { return [Q('J’étais en train de ' + o.inf1)]; },
      'En cours passé négatif': function (o) { return [Q('Je n’étais pas en train de ' + o.inf1)]; },
      'Obligation': function (o) { return [Q('Il faut ' + o.inf)]; },
      'Absence d’obligation': function (o) { return [Q('Pas besoin de ' + o.inf)]; },
      'Obligation orale': function (o) { return [Q('Il faut ' + o.inf) + ' (oral)']; },
      'Conditionnel と': function (o) { return o.c ? [Q('Dès que ' + lowFirst(o.J))] : ['dès que l’on ' + o.inf]; },
      'Conditionnel なら': function (o) { return ['si l’on ' + o.inf + ' (hypothèse : « dans ce cas… »)']; },
      'Invitation': function (o) { return o.c && o.NOUS ? [Q(o.NOUS + ' !')] : [o.inf + ', faisons… (invitation polie)']; },
      'Proposition': function (o) { return ['« Voulez-vous que je… ? » (' + o.inf + ')']; },
      'Ordre poli': function (o) { return o.c ? [Q(o.IMP + ' !') + ' (ordre ferme mais poli)'] : [o.inf + ' ! (ordre ferme mais poli)']; },
      'Énumération': function (o) { return ['tantôt ' + o.inf + ', tantôt… (énumération)']; },
      'Énumération négatif': function (o) { return ['tantôt ne pas ' + o.inf + ', tantôt… (énumération)']; },
      'Regret': function (o) { return [Q('J’aurais dû ' + o.inf1)]; },
      'Regret négatif': function (o) { return [Q('Je n’aurais pas dû ' + o.inf1)]; },
      'Volitif': function (o) { var a = [Q('Je vais ' + o.inf1)]; if (o.c && o.NOUS) a.unshift(Q(o.NOUS + ' !')); return a; },
      'Impératif': function (o) { return o.c ? [Q(o.IMP + ' !')] : [o.inf + ' ! (ordre)']; },
      'Interdiction': function (o) { return o.c ? [Q('Ne pas ' + o.inf + ' !'), Q(o.IMPN + ' !')] : [Q('Ne pas ' + o.inf + ' !')]; },
      'Conditionnel ば': function (o) { return o.c ? [Q('Si ' + lowFirst(o.J))] : ['si l’on ' + o.inf]; },
      'Conditionnel たら': function (o) { return o.c ? [Q('Si ' + lowFirst(o.PC)), Q('Quand ' + (o.c.aux === 'e' || o.pr ? (o.pr ? 'je me serai ' : 'je serai ') : (VOW.test(o.c.pp) ? 'j’aurai ' : 'j’aurai ')) + o.c.pp + o.R)] : ['quand on aura ' + o.inf]; },
      // variantes utilisées par la fiche « Conjuguer »
      'DICO': function (o) { return [o.inf + (o.c ? ' · ' + Q(o.J) : '')]; },
      'Désidératif négatif': function (o) { return [Q('Je ne veux pas ' + o.inf1)]; },
      'Potentiel négatif': function (o) { return [Q('Je ne peux pas ' + o.inf1)]; },
      'Si négatif': function (o) { return o.c ? [Q('Si ' + lowFirst(o.JN))] : ['si l’on ne ' + o.inf + ' pas']; },
      'Quand négatif': function (o) { return o.c ? [Q('Si ' + lowFirst(o.PCN))] : ['si l’on n’a pas ' + o.inf]; },
      'En cours': function (o) { return [Q('Je suis en train de ' + o.inf1)]; },
      'En cours négatif': function (o) { return [Q('Je ne suis pas en train de ' + o.inf1)]; },
      'Demande': function (o) { return o.c ? [Q(o.IMP + ', s’il vous plaît')] : [o.inf + ', s’il vous plaît']; },
      'Demande négatif': function (o) { return o.c ? [Q(o.IMPN + ', s’il vous plaît')] : ['ne pas ' + o.inf + ', s’il vous plaît']; }
    };
    return {
      // variantes de traduction pour (sens français du verbe, forme) ; [] si on ne sait pas
      tr: function (fr, label) { var o = get(fr), f = F[label]; if (!o || !f) return []; try { return f(o); } catch (e) { return []; } },
      // phrase modèle d’une forme : {pre, post, preK, postK, fr} ou null
      exf: function (fr, label, adj) {
        var t, f;
        if (adj) { t = AF[label]; f = adjFr(fr); if (!t || !f) return null; return { pre: t[0], post: t[1], preK: kanaOf(t[0]), postK: kanaOf(t[1]), fr: t[2](f) }; }
        t = VF[label]; var o = get(fr); if (!t) return null;
        try { f = o ? t[2](o) : null; } catch (e) { f = null; }
        if (!f) return null;
        if (o && !o.c) return null;
        return { pre: t[0], post: t[1], preK: kanaOf(t[0]), postK: kanaOf(t[1]), fr: f.replace(/\b([dD])e ([aeiouyéèêhœ])/g, '$1’$2') };
      },
      ok: function (fr) { return !!get(fr); },
      sent: sent,
      exact: function (fr) { var o = get(fr); return !!(o && o.c); }
    };
  })();
