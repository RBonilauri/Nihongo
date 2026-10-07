
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
      'Potentiel': function (o) { return [Q('Je peux ' + o.inf1), Q('Être capable de ' + o.inf)]; },
      'Passif': function (o) { return o.c && !o.pr && !o.rest ? [Q('Être ' + o.c.pp + ' (par quelqu’un)')] : ['Subir l’action de « ' + o.inf + ' »']; },
      'Causatif': function (o) { return [Q('Faire ' + o.inf + ' (qqn)'), Q('Laisser ' + o.inf)]; },
      'Causatif-passif': function (o) { return [Q('Être forcé de ' + o.inf)]; },
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
      ok: function (fr) { return !!get(fr); },
      sent: sent,
      exact: function (fr) { var o = get(fr); return !!(o && o.c); }
    };
  })();
