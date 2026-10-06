  /* ═══════════ QUIZ GRAMMAIRE (conjugaison + particules) ═══════════ */
  var GT = [
    { id: 'c2f', label: 'Produire la forme', cat: 'c' },
    { id: 'f2c', label: 'Reconnaître la forme', cat: 'c' },
    { id: 'p', label: 'Mot manquant', cat: 'p' },
    { id: 'pick', label: 'Quelle phrase est correcte ?', cat: 'p' },
    { id: 'role', label: 'Rôle de la particule', cat: 'p' }
  ];
  var GPG = [
    { id: 'wg', label: 'は・が' }, { id: 'nd', label: 'に・で・へ' }, { id: 'wo', label: 'を・が' }, { id: 'to', label: 'と・や・も' },
    { id: 'lm', label: 'から・まで・より' }, { id: 'cn', label: 'ので・けど・のに' }, { id: 'ds', label: 'だけ・しか・でも' },
    { id: 'sf', label: 'ね・よ・か・な' }, { id: 'ex', label: 'なら・ずつ・など・ごろ…' }, { id: 'ot', label: 'の・ながら・たら' }
  ];
  var GROLES = [
    ['Thème', 'Sujet', 'Objet direct', 'Objet d’un état (好き, わかる…)', 'Lien entre deux noms', 'Appartenance', 'Citation'],
    ['Moment précis', 'Destination', 'Direction', 'Lieu d’existence', 'Lieu de l’action', 'Lieu parcouru', 'Point de départ', 'Limite (jusqu’à)', 'Date limite', 'Moyen / instrument', 'Accompagnement', 'Destinataire'],
    ['Cause', 'Opposition (mais)', 'Pourtant (surprise, regret)', 'Condition', 'Simultanéité'],
    ['Restriction (seulement)', 'Restriction (ne… que)', 'Addition (aussi)', 'Liste complète', 'Liste d’exemples', 'Comparaison'],
    ['Question', 'Chercher l’accord', 'Informer (« je te le dis »)', 'Invitation (〜ませんか)', 'Interdiction']
  ];
  var GINC = [['Destination', 'Direction'], ['Lien entre deux noms', 'Appartenance'], ['Restriction (seulement)', 'Restriction (ne… que)'], ['Opposition (mais)', 'Pourtant (surprise, regret)']];
  function incompat(a, b) { return GINC.some(function (p) { return (p[0] === a && p[1] === b) || (p[0] === b && p[1] === a); }); }
  var GFAM = [
    { id: 'pol', label: 'Polie (ます)', f: ['Polie, présent', 'Polie, négatif', 'Polie, passé', 'Polie, passé négatif'] },
    { id: 'sim', label: 'Simple & て', f: ['Négatif simple', 'Passé simple', 'Passé négatif simple', 'Forme en て', 'て négatif'] },
    { id: 'der', label: 'Potentiel, passif, causatif', f: ['Potentiel', 'Passif', 'Causatif', 'Causatif-passif'] },
    { id: 'vol', label: 'Désir, volonté, ordre', f: ['Désidératif', 'Volitif', 'Impératif', 'Interdiction'] },
    { id: 'con', label: 'Conditionnel', f: ['Conditionnel ば', 'Conditionnel たら'] }
  ];
  var GN = [10, 25, 50, 100];
  function initGrammar(mainEl, mode) {
    var kq = 'gq_' + mode, kc = 'gqc_' + mode, ks = 'gqs_' + mode, isC = mode === 'c';
    var TT = GT.filter(function (t) { return t.cat === mode; }), TITLE = isC ? 'Quiz conjugaison' : 'Quiz particules';
    var GD = null; try { GD = JSON.parse(document.getElementById('grammar-data').textContent); } catch (e) {}
    if (!GD || !GD.verbs) return;
    var canSpeak = !!window.speechSynthesis;
    var famOf = {}; GFAM.forEach(function (f) { f.f.forEach(function (l) { famOf[l] = f.id; }); });
    var ALL = []; // éléments de base
    if (isC) GD.verbs.forEach(function (v) { Object.keys(v.f).forEach(function (l) { ALL.push({ i: 'c:' + v.v + ':' + l, c: 'c', v: v, l: l, fam: famOf[l] }); }); });
    if (!isC) GD.parts.forEach(function (p) { ALL.push({ i: 'p:' + p.i, c: 'p', p: p }); });
    var byI = {}; ALL.forEach(function (x) { byI[x.i] = x; });
    var cfg = ST[kc] || { types: TT.map(function (t) { return t.id; }), fams: GFAM.map(function (f) { return f.id; }), pg: GPG.map(function (g) { return g.id; }), n: 25, wrong: false };
    cfg.ka = false;
    if (!cfg.pg) cfg.pg = GPG.map(function (g) { return g.id; });
    if (!ST[kq]) ST[kq] = {}; if (!ST[ks]) ST[ks] = { sess: 0, q: 0, ok: 0, ty: {}, lab: {}, pt: {} };
    var Q = null;
    MIXREG[isC ? 'conj' : 'part'] = {
      label: isC ? 'Conjugaison' : 'Particules',
      count: function () { var sv = cfg; cfg = { types: TT.map(function (t) { return t.id; }), fams: GFAM.map(function (f) { return f.id; }), pg: GPG.map(function (g) { return g.id; }), n: 0, wrong: false, ka: false }; var r = avail().q; cfg = sv; return r; },
      make: function (n) { var sv = cfg; cfg = { types: TT.map(function (t) { return t.id; }), fams: GFAM.map(function (f) { return f.id; }), pg: GPG.map(function (g) { return g.id; }), n: n, wrong: false, ka: false }; var r = build(); cfg = sv; return r; },
      show: function (it, hooks, idx, total) {
        Q = { items: idx < total ? [it, it] : [it], i: 0, ok: 0, wrongList: [], t0: Date.now(), mix: hooks, mixTag: '<div class="q-tag q-tag-mix">' + (isC ? '<b>Conjugaison</b>' + (it.t === 'c2f' ? ' › ' + esc((GFAM.filter(function (f) { return f.id === byI[it.i].fam; })[0] || { label: '' }).label) : '') : '<b>Particules</b> › ' + esc((GPG.filter(function (g) { return g.id === byI[it.i].p.g; })[0] || { label: '' }).label)) + '</div>' };
        el.style.zIndex = 95; el.hidden = false; document.body.style.overflow = 'hidden';
        showQ(); ttl.textContent = 'Quiz général'; prog.textContent = idx + ' / ' + total; barI.style.width = ((idx - 1) / total * 100) + '%'; body.scrollTop = 0;
      },
      hide: function () { el.hidden = true; el.style.zIndex = ''; Q = null; paintCard(); }
    };

    var el = document.createElement('div'); el.className = 'quiz'; el.hidden = true;
    el.innerHTML = '<div class="q-top"><button class="x" type="button" aria-label="Fermer">×</button><div class="ttl">' + TITLE + '</div><div class="prog"></div></div><div class="q-bar"><i></i></div><div class="q-body"></div>';
    document.body.appendChild(el);
    var body = el.querySelector('.q-body'), prog = el.querySelector('.prog'), barI = el.querySelector('.q-bar i'), ttl = el.querySelector('.ttl');
    function $(id) { return el.querySelector('#' + id); }

    var card = document.createElement('button'); card.type = 'button'; card.className = 'quizcard';
    function wrongCount() { return Object.keys(ST[kq]).filter(function (k) { return ST[kq][k].w && byI[k]; }).length; }
    function paintCard() {
      var seen = Object.keys(ST[kq]).length, w = wrongCount();
      card.innerHTML = '<span class="qc-jp">' + (isC ? '活用' : '助詞') + '</span><span class="qc-t">' + TITLE + '<small>' + (isC ? GD.verbs.length + ' verbes · ' + ALL.length + ' formes' : GD.parts.length + ' phrases à trou') + ' · ' + (seen ? seen + ' vus' + (w ? ', ' + w + ' à revoir' : '') : 'jamais lancé') + '</small></span><span class="qc-go">›</span>';
    }
    paintCard();
    card.addEventListener('click', function () { open(true); showSetup(); });
    quizHost(mainEl).appendChild(card);
    function hideG() { el.hidden = true; document.body.style.overflow = ''; paintCard(); }
    function open(v) { if (v) { if (el.hidden) bkPush(hideG); el.hidden = false; document.body.style.overflow = 'hidden'; } else bkClose(hideG); }
    el.querySelector('.x').addEventListener('click', function () { if (Q && Q.mix) { Q.mix.quit(); return; } open(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !el.hidden && !(Q && Q.mix)) open(false); });

    function shuffle(a) { for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
    function typesFor(x) {
      if (x.c === 'p' && cfg.pg.indexOf(x.p.g) < 0) return [];
      return cfg.types.filter(function (t) { return (t === 'p' || t === 'pick' || t === 'role') ? x.c === 'p' && (t !== 'role' || x.p.r) : x.c === 'c' && cfg.fams.indexOf(x.fam) >= 0; }).filter(function (t) { return t !== 'f2c' || uniqueForm(x); });
    }
    function uniqueForm(x) { return Object.keys(x.v.f).every(function (l) { return l === x.l || x.v.f[l] !== x.v.f[x.l]; }); }
    function pool() { return ALL.filter(function (x) { return typesFor(x).length && (!cfg.wrong || (ST[kq][x.i] && ST[kq][x.i].w)); }); }
    function bucket(x) { var s = ST[kq][x.i]; if (!s) return 1; if (s.w) return 0; if (s.st >= 3) return 3; return 2; }
    function avail() { var p = pool(), q = 0; p.forEach(function (x) { q += typesFor(x).length; }); return { q: q, k: p.length }; }
    function build() {
      var p = pool(), order = shuffle(p.slice()).sort(function (a, b) { return bucket(a) - bucket(b); });
      var target = cfg.n === 0 ? avail().q : Math.min(cfg.n, avail().q), items = [], used = {}, guard = 0;
      while (items.length < target && guard++ < 10) {
        var round = [];
        order.forEach(function (x) {
          if (items.length + round.length >= target) return;
          var ok = typesFor(x).filter(function (t) { return !(used[x.i] && used[x.i][t]); }); if (!ok.length) return;
          var WT = { p: 3, role: 2, pick: 1 }, tot = ok.reduce(function (a, z) { return a + (WT[z] || 1); }, 0), rr = Math.random() * tot, t = ok[ok.length - 1];
          for (var zi = 0; zi < ok.length; zi++) { rr -= (WT[ok[zi]] || 1); if (rr < 0) { t = ok[zi]; break; } }
           (used[x.i] = used[x.i] || {})[t] = 1; round.push({ i: x.i, t: t });
        });
        if (!round.length) break; items = items.concat(shuffle(round));
      }
      return items;
    }

    function fillS(p, a) { return (cfg.ka && p.k ? p.k : p.s).replace(/（.*）/, '').replace('＿＿', a); }
    function kf(v, s) { return cfg.ka ? kfa(v, s) : s; }
    function fillK(p, a) { return (p.k || p.s).replace(/（.*）/, '').replace('＿＿', a); }
    function kfa(v, s) { for (var l in v.r) if (v.f[l] === s && v.r[l]) return v.r[l]; return v.kp && s.indexOf(v.kp) === 0 ? v.kk + s.slice(v.kp.length) : s; }
    function pshow(o) { return cfg.ka && o.k ? o.k : o.v; }
    function wrongForms(v, l) {
      var s = v.v.slice(0, -1), out = [];
      if (/en る|^groupe 1 \(en る\)/.test(v.g)) { if (l === 'Négatif simple') out.push(s + 'ない'); if (l === 'Polie, présent') out.push(s + 'ます'); if (l === 'Forme en て') out.push(s + 'て'); if (l === 'Passé simple') out.push(s + 'た'); }
      if (v.v === '行く') { if (l === 'Forme en て') out.push('行いて'); if (l === 'Passé simple') out.push('行いた'); }
      if (v.v === '食べる' && l === 'Négatif simple') out.push('食べらない');
      if (v.v === '書く' && l === 'Négatif simple') out.push('書くない');
      return out;
    }
    function options(it) {
      var x = byI[it.i];
      if (it.t === 'pick') { var bad = x.p.d[Math.floor(Math.random() * x.p.d.length)]; return shuffle([{ v: fillS(x.p, x.p.a), ok: true, k: fillK(x.p, x.p.a) }, { v: fillS(x.p, bad), ok: false, k: fillK(x.p, bad) }]); }
      if (it.t === 'role') {
        var famR = GROLES.filter(function (f) { return f.indexOf(x.p.r) >= 0; })[0] || [], outR = [{ v: x.p.r, ok: true }], sR = {}; sR[x.p.r] = 1;
        shuffle(famR.slice()).concat(shuffle([].concat.apply([], GROLES))).forEach(function (r) { if (outR.length < 4 && !sR[r] && !incompat(r, x.p.r)) { sR[r] = 1; outR.push({ v: r, ok: false }); } });
        return shuffle(outR);
      }
      if (it.t === 'p') return shuffle([{ v: x.p.a, ok: true }].concat(x.p.d.map(function (d) { return { v: d, ok: false }; })));
      var v = x.v;
      if (it.t === 'c2f') {
        var ans = v.f[x.l], seen = {}, out = [{ v: ans, ok: true, k: kfa(v, ans) }]; seen[ans] = 1;
        function add(s, vv) { if (s && !seen[s] && out.length < 4) { seen[s] = 1; out.push({ v: s, ok: false, k: kfa(vv || v, s) }); } }
        wrongForms(v, x.l).slice(0, 1).forEach(add);
        shuffle(Object.keys(v.f).filter(function (l) { return l !== x.l && famOf[l] === x.fam; })).forEach(function (l) { add(v.f[l]); });
        shuffle(ALL.filter(function (o) { return o.c === 'c' && o.l === x.l && o.v !== v && o.v.v !== 'ある'; })).forEach(function (o) { if (out.length < 4) add(o.v.f[x.l], o.v); });
        return shuffle(out);
      }
      var ans2 = x.l, s2 = {}, out2 = [{ v: ans2, ok: true }]; s2[ans2] = 1;
      var famLabels = [];
      GFAM.forEach(function (f) { if (f.id === x.fam) famLabels = f.f; });
      var cand = shuffle(famLabels.slice()).concat(shuffle(Object.keys(famOf)));
      cand.forEach(function (l) { if (out2.length < 4 && !s2[l] && v.f[l] !== v.f[x.l]) { s2[l] = 1; out2.push({ v: l, ok: false }); } });
      return shuffle(out2);
    }

    function chip(label, on, data, dis) { return '<button type="button" class="qchip' + (on ? ' on' : '') + '"' + (dis ? ' disabled' : '') + ' ' + data + '>' + label + '</button>'; }
    function toggle(arr, v) { var i = arr.indexOf(v); if (i >= 0) arr.splice(i, 1); else arr.push(v); }
    function showSetup() {
      Q = null; ttl.textContent = TITLE; prog.textContent = ''; barI.style.width = '0';
      var av = avail(); if (cfg.n !== 0 && cfg.n > av.q) cfg.n = 0;
      var hasC = cfg.types.indexOf('c2f') >= 0 || cfg.types.indexOf('f2c') >= 0, wc = wrongCount(), h = '';
      if (TT.length > 1) h += '<div class="q-sec"><h4>Types de questions</h4><div class="qchips">' + TT.map(function (t) { return chip(t.label, cfg.types.indexOf(t.id) >= 0, 'data-t="' + t.id + '"'); }).join('') + '</div></div>';
      if (!isC) h += '<div class="q-sec"><h4>Contrastes</h4><div class="qchips">' + GPG.map(function (g) { return chip(g.label, cfg.pg.indexOf(g.id) >= 0, 'data-pg="' + g.id + '"'); }).join('') + '</div></div>';
      if (isC) h += '<div class="q-sec"><h4>Formes de conjugaison</h4><div class="qchips">' + GFAM.map(function (f) { return chip(f.label, cfg.fams.indexOf(f.id) >= 0, 'data-f="' + f.id + '"', !hasC); }).join('') + '</div></div>';
      h += '<div class="q-sec"><h4>Nombre de questions</h4><div class="qchips">' + GN.filter(function (n) { return n <= av.q; }).map(function (n) { return chip(n, cfg.n === n, 'data-n="' + n + '"', n > av.q); }).join('') + chip('Tout · ' + av.q, cfg.n === 0, 'data-n="0"', av.q === 0) + '</div></div>';
      h += '<div class="q-sec"><div class="row"><span class="lab">Seulement mes ratés<small>' + (wc ? wc + ' à revoir' : 'Aucun raté pour l’instant') + '</small></span><button class="sw" type="button" id="g-wrong" role="switch" aria-checked="' + !!cfg.wrong + '"' + (wc ? '' : ' disabled') + '><i></i></button></div></div>';
      h += '<button type="button" class="mini qstat-btn" id="g-stats">📊 Statistiques</button>';
      h += '<button type="button" class="qgo" id="g-go"' + (cfg.types.length && av.q ? '' : ' disabled') + '>Lancer · ' + (cfg.n === 0 ? av.q : Math.min(cfg.n, av.q)) + ' questions</button>';
      body.innerHTML = h; body.scrollTop = 0;
    }
    function persist() { ST[kc] = cfg; save(); }
    function speakItem(x) {
      if (!canSpeak) return;
      if (x.c === 'p') speak([x.p.s.replace(/（.*）/, '').replace('＿＿', x.p.a)]);
      else speak([x.v.r[x.l] || x.v.f[x.l]]);
    }
    body.addEventListener('click', function (e) {
      var b = e.target.closest('button'); if (!b || b.disabled) return;
      var d = b.dataset;
      if (b.classList.contains('qhint')) { toggleHint(b); return; }
      if (d.t) { toggle(cfg.types, d.t); persist(); showSetup(); }
      else if (d.f) { toggle(cfg.fams, d.f); persist(); showSetup(); }
      else if (d.pg) { toggle(cfg.pg, d.pg); persist(); showSetup(); }
      else if (d.n !== undefined) { cfg.n = +d.n; persist(); showSetup(); }
      else if (b.id === 'g-wrong') { cfg.wrong = !cfg.wrong; persist(); showSetup(); }
      else if (b.id === 'g-go') { start(build()); }
      else if (b.classList.contains('qopt')) answer(b);
      else if (b.id === 'g-next') { if (Q.mix) { Q.mix.next(Q.ok > 0); return; } Q.i++; showQ(); }
      else if (b.id === 'g-say') { speakItem(byI[b.dataset.id]); }
      else if (b.id === 'g-again') { if (Q.wrongList.length) start(Q.wrongList.slice()); }
      else if (b.id === 'g-new' || b.id === 'g-back') { showSetup(); }
      else if (b.id === 'g-stats') { showStats(); }
      else if (b.id === 'g-close') { open(false); }
      else if (b.id === 'g-reset') { if (confirm('Effacer toutes les statistiques du quiz grammaire et les ratés ?')) { ST[kq] = {}; ST[ks] = { sess: 0, q: 0, ok: 0, ty: {}, lab: {}, pt: {} }; save(); showStats(); } }
    });

    function start(items) {
      if (!items.length) { toast('Aucune question disponible avec ces réglages.'); return; }
      Q = { items: items, i: 0, ok: 0, wrongList: [], t0: Date.now(), done: false }; showQ();
    }
    function vlabel(v) { return esc(cfg.ka ? v.ka : v.v) + '<small>' + esc((!cfg.ka && v.ka !== v.v ? v.ka + ' · ' : '') + v.fr + ' · ' + v.g) + '</small>'; }
    function showQ() {
      if (Q.i >= Q.items.length) return showResult();
      var it = Q.items[Q.i], x = byI[it.i], opts = options(it); Q.cur = { it: it, opts: opts, done: false };
      prog.textContent = (Q.i + 1) + ' / ' + Q.items.length; barI.style.width = (Q.i / Q.items.length * 100) + '%';
      var ask, big, hint = '', optK = function () { return opts.some(function (o) { return HK.test(o.v); }) ? hintBtn(opts.map(function (o) { return o.k; }).join('\n')) : ''; };
      if (it.t === 'c2f') { ask = 'Mets ce verbe à la forme :'; big = '<div class="q-big vq gq-verb">' + vlabel(x.v) + '</div><div class="gq-form">' + esc(x.l) + '</div>'; hint = optK(); }
      else if (it.t === 'f2c') { ask = 'Quelle est cette forme ?'; big = '<div class="q-big vq">' + esc(kf(x.v, x.v.f[x.l])) + '</div><div class="gq-sub">du verbe ' + esc(cfg.ka ? x.v.ka : x.v.v) + ' · ' + esc(x.v.fr) + '</div>'; var kk = kfa(x.v, x.v.f[x.l]); hint = hintBtn(kk !== x.v.f[x.l] ? kk : ''); }
      else if (it.t === 'pick') { ask = 'Quelle phrase est correcte ?'; big = '<div class="gq-sub gq-fr">' + esc(x.p.fr) + '</div>'; hint = optK(); }
      else if (it.t === 'role') { ask = 'Quel est le rôle de la particule en gras ?'; big = '<div class="q-big vq gq-sent">' + (function () { var pp = (cfg.ka && x.p.k ? x.p.k : x.p.s).replace(/（.*）/, '').split('＿＿'); return esc(pp[0]) + '<b class="gq-hl">' + esc(x.p.a) + '</b>' + esc(pp[1] || ''); })() + '</div><div class="gq-sub">' + esc(x.p.fr) + '</div>'; hint = hintBtn(x.p.k && HK.test(x.p.s) ? fillK(x.p, x.p.a) : ''); }
      else { ask = 'Quelle particule manque ?'; big = '<div class="q-big vq gq-sent">' + esc(cfg.ka && x.p.k ? x.p.k : x.p.s) + '</div><div class="gq-sub">' + esc(x.p.fr) + '</div>'; hint = hintBtn(x.p.k && HK.test(x.p.s) ? x.p.k : ''); }
      var short = it.t === 'p';
      body.innerHTML = '<div class="q-card">' + (Q.mixTag || '') + '<div class="q-ask">' + ask + '</div>' + big + hint + '</div><div class="q-opts' + (short ? ' gq-two' : '') + '">' +
        opts.map(function (o, i) { return '<button type="button" class="qopt vq-opt' + (short ? ' gq-pt' : '') + '" data-i="' + i + '">' + esc(pshow(o)) + '</button>'; }).join('') + '</div><div id="g-fb"></div>';
    }
    function lineOf(x) { return x.c === 'p' ? x.p.s.replace('＿＿', x.p.a).replace(/（.*）/, '') : x.v.v + ' → ' + x.l + ' : ' + x.v.f[x.l]; }
    function answer(b) {
      var cur = Q.cur; if (cur.done) return; cur.done = true;
      var o = cur.opts[+b.dataset.i], it = cur.it, x = byI[it.i], good = !!o.ok;
      body.querySelectorAll('.qopt').forEach(function (n) { var oo = cur.opts[+n.dataset.i]; n.disabled = true; if (oo.ok) n.classList.add('good'); else if (n === b) n.classList.add('bad'); });
      var st = ST[kq][x.i] || { n: 0, st: 0, w: false }; st.n++;
      if (good) { Q.ok++; st.st++; st.w = false; } else { st.st = 0; st.w = true; st.x = (st.x || 0) + 1; if (!Q.wrongList.some(function (w) { return w.i === x.i; })) Q.wrongList.push({ i: x.i, t: it.t }); }
      ST[kq][x.i] = st;
      var S = ST[ks]; S.q++; if (good) S.ok++; dayHit(good, isC ? 'c' : 'p');
      var T = S.ty[it.t] = S.ty[it.t] || { n: 0, ok: 0 }; T.n++; if (good) T.ok++;
      var K = x.c === 'p' ? (S.pt[x.p.a] = S.pt[x.p.a] || { n: 0, ok: 0 }) : (S.lab[x.l] = S.lab[x.l] || { n: 0, ok: 0 }); K.n++; if (good) K.ok++;
      save();
      var last = Q.i + 1 >= Q.items.length, h = '<div class="q-fb ' + (good ? 'good' : 'bad') + '"><div class="fbh">' + (good ? '✓ Bonne réponse' : '✗ Raté') + '</div><div class="vq-ans">';
      if (x.c === 'p') h += '<div class="vq-jp">' + esc(x.p.s.replace('＿＿', x.p.a).replace(/（.*）/, '')) + '</div><div>' + esc(x.p.fr) + '</div><div class="vq-ro">' + esc(x.p.n) + '</div>';
      else h += '<div class="vq-jp">' + esc(x.v.f[x.l]) + '</div>' + (x.v.r[x.l] ? '<div>' + esc(x.v.r[x.l]) + '</div>' : '') + '<div><b>' + esc(x.l) + '</b> de ' + esc(x.v.v) + ' (' + esc(x.v.fr) + ')</div><div class="vq-ro">' + esc(x.v.g) + '</div>';
      h += '</div><div class="fbb">' + (canSpeak ? '<button type="button" class="mini" id="g-say" data-id="' + esc(x.i) + '">🔊 Écouter</button>' : '') + '<button type="button" class="qgo" id="g-next">' + (last ? 'Voir le score' : 'Suivant') + '</button></div></div>';
      $('g-fb').innerHTML = h;
      $('g-fb').scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    }
    function showResult() {
      if (!Q.done) { Q.done = true; ST[ks].sess++; save(); }
      barI.style.width = '100%'; prog.textContent = '';
      var n = Q.items.length, pct = Math.round(Q.ok / n * 100), secs = Math.round((Date.now() - Q.t0) / 1000);
      var list = Q.wrongList.map(function (w) { var x = byI[w.i]; return '<div class="q-miss"><span>' + esc(lineOf(x)) + '<small>' + esc(x.c === 'p' ? x.p.fr : x.v.fr) + '</small></span></div>'; }).join('');
      body.scrollTop = 0; body.innerHTML = '<div class="q-score"><div class="n">' + Q.ok + '<small> / ' + n + '</small></div><div class="p">' + pct + ' % · ' + Math.floor(secs / 60) + ' min ' + (secs % 60) + ' s</div></div>' +
        (list ? '<h4 class="q-h">À revoir (' + Q.wrongList.length + ')</h4><div class="q-miss-list">' + list + '</div>' : '<p class="conj-note">Sans faute. Bravo.</p>') +
        '<div class="q-end">' + (list ? '<button type="button" class="qgo" id="g-again">Refaire les ratés</button>' : '') + '<button type="button" class="mini" id="g-new">Nouveau quiz</button><button type="button" class="mini" id="g-close">Fermer</button></div>';
    }
    function showStats() {
      Q = null; ttl.textContent = 'Statistiques'; prog.textContent = ''; barI.style.width = '0';
      var S = ST[ks], pc = function (a, b) { return b ? Math.round(a / b * 100) + ' %' : '—'; };
      function row(name, T) { var p = T.n ? Math.round(T.ok / T.n * 100) : 0; return '<div class="qs-row"><div class="qs-l"><span>' + name + '</span><span><b>' + T.n + '</b> · ' + pc(T.ok, T.n) + '</span></div><div class="qs-bar"><i style="width:' + p + '%"></i></div></div>'; }
      function sorted(map) { return Object.keys(map).filter(function (k) { return map[k].n; }).sort(function (a, b) { return (map[a].ok / map[a].n) - (map[b].ok / map[b].n) || map[b].n - map[a].n; }); }
      var h = '<div class="q-stats"><div class="qs-tiles"><div><b>' + S.sess + '</b><span>quiz terminés</span></div><div><b>' + S.q + '</b><span>questions</span></div><div><b>' + pc(S.ok, S.q) + '</b><span>de réussite</span></div></div>';
      h += qsExtra(isC ? 'c' : 'p', ST[kq], ALL.length);
      h += '<h4 class="q-h">Par type de question</h4><div class="qs-types">' + TT.map(function (t) { return row(t.label, S.ty[t.id] || { n: 0, ok: 0 }); }).join('') + '</div>';
      var sl = isC ? sorted(S.lab) : []; if (sl.length) h += '<h4 class="q-h">Formes (les plus difficiles d’abord)</h4><div class="qs-types">' + sl.map(function (k) { return row(esc(k), S.lab[k]); }).join('') + '</div>';
      var sp = !isC ? sorted(S.pt) : []; if (sp.length) h += '<h4 class="q-h">Particules (les plus difficiles d’abord)</h4><div class="qs-types">' + sp.map(function (k) { return row(esc(k), S.pt[k]); }).join('') + '</div>';
      var worst = Object.keys(ST[kq]).map(function (k) { var v = ST[kq][k]; return { i: k, x: v.x || (v.w ? 1 : 0), n: v.n }; }).filter(function (v) { return v.x > 0 && byI[v.i]; }).sort(function (a, b) { return b.x - a.x || (b.x / b.n) - (a.x / a.n); }).slice(0, 15);
      h += '<h4 class="q-h">Les plus ratés</h4>' + (worst.length ? '<div class="q-miss-list">' + worst.map(function (v) { var x = byI[v.i]; return '<div class="q-miss"><span>' + esc(lineOf(x)) + '<small>' + esc(x.c === 'p' ? x.p.fr : x.v.fr) + '</small></span><span class="qs-cnt">' + v.x + ' / ' + v.n + '</span></div>'; }).join('') + '</div>' : '<p class="conj-note">Aucun raté enregistré pour l’instant.</p>');
      h += '<div class="q-end"><button type="button" class="qgo" id="g-back">Retour</button><button type="button" class="mini" id="g-reset">Effacer les statistiques</button></div></div>';
      body.innerHTML = h; body.scrollTop = 0;
    }
  }

