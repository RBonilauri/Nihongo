  /* ═══════════ QUIZ COMPTEURS ═══════════ */
  var CT = [
    { id: 'rd', label: 'Lecture (三本 → さんぼん)' },
    { id: 'ear', label: '🔊 Écoute → écriture' },
    { id: 'ct', label: 'Choisir le compteur (猫 → 匹)' },
    { id: 'us', label: 'À quoi sert ce compteur ?' }
  ];
  var CG = [
    { id: 'obj', label: 'Objets' }, { id: 'viv', label: 'Êtres vivants' }, { id: 'pla', label: 'Plats' },
    { id: 'aut', label: 'Étages, fois, rang' }, { id: 'tsu', label: 'Série つ' }, { id: 'tmp', label: 'Durées et âge' }
  ];
  var CSINO = { '一': 'いち', '二': 'に', '三': 'さん', '四': 'よん', '五': 'ご', '六': 'ろく', '七': 'なな', '八': 'はち', '九': 'きゅう', '十': 'じゅう', '何': 'なん', '1': 'いち', '2': 'に', '3': 'さん', '4': 'よん', '5': 'ご', '6': 'ろく', '7': 'なな', '8': 'はち', '9': 'きゅう', '10': 'じゅう' };
  var CN = [10, 25, 50, 100, 150, 200];
  function initCounters(mainEl) {
    var CD = null; try { CD = JSON.parse(document.getElementById('counter-data').textContent); } catch (e) {}
    if (!CD || !CD.reads) return;
    var canSpeak = !!window.speechSynthesis;
    var cinfo = {}; CD.counters.forEach(function (c) { cinfo[c.k] = c; });
    var types = CT.filter(function (t) { return canSpeak || t.id !== 'ear'; });
    var ALL = [];
    CD.reads.forEach(function (r) { ALL.push({ i: 'r:' + r.k, kind: 'r', g: r.g, r: r }); });
    CD.counters.forEach(function (c) {
      if (c.k !== 'つ') ALL.push({ i: 'c:' + c.k, kind: 'c', g: c.g, c: c });
      c.ex.forEach(function (w) { ALL.push({ i: 'w:' + w[0], kind: 'w', g: c.g, c: c, w: w }); });
    });
    var byI = {}; ALL.forEach(function (x) { byI[x.i] = x; });
    var cfg = ST.cqc || { types: types.map(function (t) { return t.id; }), groups: CG.map(function (g) { return g.id; }), n: 25, wrong: false };
    if (ST.cqc && ST.cqc.groups && ST.cqc.groups.indexOf('tmp') < 0 && !ST.cqc.g2) { ST.cqc.groups.push('tmp'); ST.cqc.g2 = 1; }
    cfg.ka = false;
    cfg.types = cfg.types.filter(function (t) { return types.some(function (u) { return u.id === t; }); }); if (!cfg.types.length) cfg.types = types.map(function (t) { return t.id; });
    if (!ST.cq) ST.cq = {}; if (!ST.cqs) ST.cqs = { sess: 0, q: 0, ok: 0, ty: {}, ct: {} };
    var Q = null;
    MIXREG['compt'] = {
      label: 'Compteurs',
      count: function () { var sv = cfg; cfg = { types: types.map(function (t) { return t.id; }), groups: CG.map(function (g) { return g.id; }), n: 0, wrong: false, ka: false }; var r = avail().q; cfg = sv; return r; },
      make: function (n) { var sv = cfg; cfg = { types: types.map(function (t) { return t.id; }), groups: CG.map(function (g) { return g.id; }), n: n, wrong: false, ka: false }; var r = build(); cfg = sv; return r; },
      show: function (it, hooks, idx, total) {
        Q = { items: idx < total ? [it, it] : [it], i: 0, ok: 0, wrongList: [], t0: Date.now(), mix: hooks, mixTag: '<div class="q-tag q-tag-mix">' + '<b>Compteurs</b> › ' + esc((CG.filter(function (g) { return g.id === byI[it.i].g; })[0] || { label: '' }).label) + '</div>' };
        el.style.zIndex = 95; el.hidden = false; document.body.style.overflow = 'hidden';
        showQ(); ttl.textContent = 'Quiz général'; prog.textContent = idx + ' / ' + total; barI.style.width = ((idx - 1) / total * 100) + '%'; body.scrollTop = 0;
      },
      hide: function () { el.hidden = true; el.style.zIndex = ''; Q = null; paintCard(); }
    };

    var el = document.createElement('div'); el.className = 'quiz'; el.hidden = true;
    el.innerHTML = '<div class="q-top"><button class="x" type="button" aria-label="Fermer">×</button><div class="ttl">Quiz compteurs</div><div class="prog"></div></div><div class="q-bar"><i></i></div><div class="q-body"></div>';
    document.body.appendChild(el);
    var body = el.querySelector('.q-body'), prog = el.querySelector('.prog'), barI = el.querySelector('.q-bar i'), ttl = el.querySelector('.ttl');
    function $(id) { return el.querySelector('#' + id); }

    var card = document.createElement('button'); card.type = 'button'; card.className = 'quizcard';
    function wrongCount() { return Object.keys(ST.cq).filter(function (k) { return ST.cq[k].w && byI[k]; }).length; }
    function paintCard() {
      var seen = Object.keys(ST.cq).length, w = wrongCount();
      card.innerHTML = '<span class="qc-jp">助数詞</span><span class="qc-t">Quiz compteurs<small>' + CD.counters.length + ' compteurs · ' + CD.reads.length + ' lectures · ' + (seen ? seen + ' vus' + (w ? ', ' + w + ' à revoir' : '') : 'jamais lancé') + '</small></span><span class="qc-go">›</span>';
    }
    paintCard();
    card.addEventListener('click', function () { open(true); showSetup(); });
    quizHost(mainEl).appendChild(card);
    function hideC() { el.hidden = true; document.body.style.overflow = ''; paintCard(); }
    function open(v) { if (v) { if (el.hidden) bkPush(hideC); el.hidden = false; document.body.style.overflow = 'hidden'; } else bkClose(hideC); }
    el.querySelector('.x').addEventListener('click', function () { if (Q && Q.mix) { Q.mix.quit(); return; } open(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !el.hidden && !(Q && Q.mix)) open(false); });

    function shuffle(a) { for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
    function typesFor(x) {
      if (cfg.groups.indexOf(x.g) < 0) return [];
      var want = x.kind === 'r' ? ['rd', 'ear'] : x.kind === 'w' ? ['ct'] : ['us'];
      return cfg.types.filter(function (t) { return want.indexOf(t) >= 0 && (t !== 'ear' || (x.r.c !== '階' && x.r.c !== '回')); });
    }
    function pool() { return ALL.filter(function (x) { return typesFor(x).length && (!cfg.wrong || (ST.cq[x.i] && ST.cq[x.i].w)); }); }
    function bucket(x) { var s = ST.cq[x.i]; if (!s) return 1; if (s.w) return 0; if (s.st >= 3) return 3; return 2; }
    function avail() { var p = pool(), q = 0; p.forEach(function (x) { q += typesFor(x).length; }); return { q: q, k: p.length }; }
    function build() {
      var p = pool(), order = shuffle(p.slice()).sort(function (a, b) { return bucket(a) - bucket(b); });
      var target = cfg.n === 0 ? avail().q : Math.min(cfg.n, avail().q), items = [], used = {}, guard = 0;
      while (items.length < target && guard++ < 10) {
        var round = [];
        order.forEach(function (x) {
          if (items.length + round.length >= target) return;
          var ok = typesFor(x).filter(function (t) { return !(used[x.i] && used[x.i][t]); }); if (!ok.length) return;
          var t = ok[Math.floor(Math.random() * ok.length)]; (used[x.i] = used[x.i] || {})[t] = 1; round.push({ i: x.i, t: t });
        });
        if (!round.length) break; items = items.concat(shuffle(round));
      }
      return items;
    }

    function options(it) {
      var x = byI[it.i], out = [], seen = {};
      function add(v, ok, k) { if (v && !seen[v] && out.length < 4) { seen[v] = 1; out.push({ v: v, ok: !!ok, k: k }); } }
      if (it.t === 'rd' || it.t === 'ear') {
        var r = x.r, same = CD.reads.filter(function (o) { return o.c === r.c && o !== r; }), cross = CD.reads.filter(function (o) { return o.c !== r.c && o.g === r.g && o.n === r.n; });
        var key = it.t === 'rd' ? 'y' : 'k';
        add(r[key], true);
        function okc(o) { return it.t === 'rd' || o.y !== r.y; }
        if (it.t === 'rd') { var base = cinfo[r.c] && cinfo[r.c].b, sn = CSINO[r.n]; if (base && sn && sn + base !== r.y) add(sn + base, false); }
        shuffle(same.filter(okc)).slice(0, 2).forEach(function (o) { add(o[key], false); });
        shuffle(cross.filter(okc)).forEach(function (o) { add(o[key], false); });
        shuffle(same.filter(okc)).forEach(function (o) { add(o[key], false); });
        shuffle(CD.reads.filter(function (o) { return o !== r && okc(o); })).forEach(function (o) { add(o[key], false); });
      } else if (it.t === 'ct') {
        add(x.c.k, true, x.c.b);
        shuffle(CD.counters.filter(function (c) { return c.k !== x.c.k && c.k !== 'つ' && c.g === x.c.g; })).forEach(function (c) { add(c.k, false, c.b); });
        shuffle(CD.counters.filter(function (c) { return c.k !== x.c.k && c.k !== 'つ'; })).forEach(function (c) { add(c.k, false, c.b); });
      } else {
        add(x.c.u, true);
        shuffle(CD.counters.filter(function (c) { return c.k !== x.c.k && c.k !== 'つ' && c.g === x.c.g; })).forEach(function (c) { add(c.u, false); });
        shuffle(CD.counters.filter(function (c) { return c.k !== x.c.k && c.k !== 'つ'; })).forEach(function (c) { add(c.u, false); });
      }
      return shuffle(out);
    }

    function chip(label, on, data, dis) { return '<button type="button" class="qchip' + (on ? ' on' : '') + '"' + (dis ? ' disabled' : '') + ' ' + data + '>' + label + '</button>'; }
    function toggle(arr, v) { var i = arr.indexOf(v); if (i >= 0) arr.splice(i, 1); else arr.push(v); }
    function showSetup() {
      Q = null; ttl.textContent = 'Quiz compteurs'; prog.textContent = ''; barI.style.width = '0';
      var av = avail(); if (cfg.n !== 0 && cfg.n > av.q) cfg.n = 0;
      var wc = wrongCount(), h = '';
      h += '<div class="q-sec"><h4>Catégories</h4><div class="qchips">' + CG.map(function (g) { return chip(g.label, cfg.groups.indexOf(g.id) >= 0, 'data-g="' + g.id + '"'); }).join('') + '</div></div>';
      h += '<div class="q-sec"><h4>Types de questions</h4><div class="qchips">' + types.map(function (t) { return chip(t.label, cfg.types.indexOf(t.id) >= 0, 'data-t="' + t.id + '"'); }).join('') + '</div></div>';
      h += '<div class="q-sec"><h4>Nombre de questions</h4><div class="qchips">' + CN.filter(function (n) { return n <= av.q; }).map(function (n) { return chip(n, cfg.n === n, 'data-n="' + n + '"'); }).join('') + chip('Tout · ' + av.q, cfg.n === 0, 'data-n="0"', av.q === 0) + '</div></div>';
      h += '<div class="q-sec"><div class="row"><span class="lab">Seulement mes ratés<small>' + (wc ? wc + ' à revoir' : 'Aucun raté pour l’instant') + '</small></span><button class="sw" type="button" id="k-wrong" role="switch" aria-checked="' + !!cfg.wrong + '"' + (wc ? '' : ' disabled') + '><i></i></button></div></div>';
      h += '<button type="button" class="mini qstat-btn" id="k-stats">📊 Statistiques</button>';
      h += '<button type="button" class="qgo" id="k-go"' + (cfg.types.length && cfg.groups.length && av.q ? '' : ' disabled') + '>Lancer · ' + (cfg.n === 0 ? av.q : Math.min(cfg.n, av.q)) + ' questions</button>';
      body.innerHTML = h;
    }
    function persist() { ST.cqc = cfg; save(); }
    function sayText(x) { return x.kind === 'r' ? x.r.y : ''; }
    body.addEventListener('click', function (e) {
      var b = e.target.closest('button'); if (!b || b.disabled) return;
      var d = b.dataset;
      if (b.classList.contains('qhint')) { toggleHint(b); return; }
      if (d.g) { toggle(cfg.groups, d.g); persist(); showSetup(); }
      else if (d.t) { toggle(cfg.types, d.t); persist(); showSetup(); }
      else if (d.n !== undefined) { cfg.n = +d.n; persist(); showSetup(); }
      else if (b.id === 'k-wrong') { cfg.wrong = !cfg.wrong; persist(); showSetup(); }
      else if (b.id === 'k-go') { start(build()); }
      else if (b.classList.contains('qopt')) answer(b);
      else if (b.id === 'k-next') { if (Q.mix) { Q.mix.next(Q.ok > 0); return; } Q.i++; showQ(); }
      else if (b.id === 'k-say') { var t = sayText(byI[b.dataset.id]); if (t && canSpeak) speak([t]); }
      else if (b.id === 'k-replay') { var t2 = sayText(byI[Q.cur.it.i]); if (t2 && canSpeak) speak([t2]); }
      else if (b.id === 'k-again') { if (Q.wrongList.length) start(Q.wrongList.slice()); }
      else if (b.id === 'k-new' || b.id === 'k-back') { showSetup(); }
      else if (b.id === 'k-stats') { showStats(); }
      else if (b.id === 'k-close') { open(false); }
      else if (b.id === 'k-reset') { if (confirm('Effacer toutes les statistiques du quiz compteurs et les ratés ?')) { ST.cq = {}; ST.cqs = { sess: 0, q: 0, ok: 0, ty: {}, ct: {} }; save(); showStats(); } }
    });

    function start(items) {
      if (!items.length) { toast('Aucune question disponible avec ces réglages.'); return; }
      Q = { items: items, i: 0, ok: 0, wrongList: [], t0: Date.now(), done: false }; showQ();
    }
    function counterOf(x) { return x.kind === 'r' ? x.r.c : x.c.k; }
    function showQ() {
      if (Q.i >= Q.items.length) return showResult();
      var it = Q.items[Q.i], x = byI[it.i], opts = options(it); Q.cur = { it: it, opts: opts, done: false };
      prog.textContent = (Q.i + 1) + ' / ' + Q.items.length; barI.style.width = (Q.i / Q.items.length * 100) + '%';
      var ask, big, hint = '';
      if (it.t === 'rd') { ask = 'Comment se lit ?'; big = '<div class="q-big vq">' + esc(x.r.k) + '</div>'; }
      else if (it.t === 'ear') { ask = 'Écoute, puis choisis l’écriture'; big = '<button type="button" class="qgo vq-ear" id="k-replay">🔊 Réécouter</button>'; }
      else if (it.t === 'ct') { ask = 'Quel compteur pour :'; big = '<div class="q-big vq">' + esc(x.w[0]) + '</div><div class="gq-sub">' + esc(x.w[1]) + '</div>'; hint = hintBtn(HK.test(x.w[0]) || opts.some(function (o) { return HK.test(o.v); }) ? (x.w[2] || x.w[0]) + '\n' + opts.map(function (o) { return o.k || o.v; }).join(' · ') : ''); }
      else { ask = 'À quoi sert ce compteur ?'; big = '<div class="q-big vq">' + esc(x.c.k) + '</div><div class="gq-sub">' + esc(x.c.ro) + '</div>'; hint = hintBtn(HK.test(x.c.k) ? x.c.b : ''); }
      body.innerHTML = '<div class="q-card">' + (Q.mixTag || '') + '<div class="q-ask">' + ask + '</div>' + big + hint + '</div><div class="q-opts' + (it.t === 'ct' || it.t === 'ear' ? ' gq-two' : '') + '">' +
        opts.map(function (o, i) { return '<button type="button" class="qopt vq-opt' + (it.t === 'ct' || it.t === 'ear' ? ' gq-pt' : '') + '" data-i="' + i + '">' + esc(cfg.ka && o.k ? o.k : o.v) + '</button>'; }).join('') + '</div><div id="k-fb"></div>';
      if (it.t === 'ear' && canSpeak) setTimeout(function () { speak([x.r.y]); }, 150);
    }
    function lineOf(x) { return x.kind === 'r' ? x.r.k + ' → ' + x.r.y : x.kind === 'w' ? x.w[0] + ' → ' + x.c.k : x.c.k + ' : ' + x.c.u; }
    function answer(b) {
      var cur = Q.cur; if (cur.done) return; cur.done = true;
      var o = cur.opts[+b.dataset.i], it = cur.it, x = byI[it.i], good = !!o.ok;
      body.querySelectorAll('.qopt').forEach(function (n) { var oo = cur.opts[+n.dataset.i]; n.disabled = true; if (oo.ok) n.classList.add('good'); else if (n === b) n.classList.add('bad'); });
      var st = ST.cq[x.i] || { n: 0, st: 0, w: false }; st.n++;
      if (good) { Q.ok++; st.st++; st.w = false; } else { st.st = 0; st.w = true; st.x = (st.x || 0) + 1; if (!Q.wrongList.some(function (w) { return w.i === x.i; })) Q.wrongList.push({ i: x.i, t: it.t }); }
      ST.cq[x.i] = st;
      var S = ST.cqs; S.q++; if (good) S.ok++; dayHit(good);
      var T = S.ty[it.t] = S.ty[it.t] || { n: 0, ok: 0 }; T.n++; if (good) T.ok++;
      var K = S.ct[counterOf(x)] = S.ct[counterOf(x)] || { n: 0, ok: 0 }; K.n++; if (good) K.ok++;
      save();
      var last = Q.i + 1 >= Q.items.length, c = x.kind === 'r' ? cinfo[x.r.c] : x.c;
      var h = '<div class="q-fb ' + (good ? 'good' : 'bad') + '"><div class="fbh">' + (good ? '✓ Bonne réponse' : '✗ Raté') + '</div><div class="vq-ans">';
      if (x.kind === 'r') h += '<div class="vq-jp">' + esc(x.r.k) + '</div><div>' + esc(x.r.y) + (x.r.irr ? ' ⚠ irrégulier' : '') + '</div>';
      else if (x.kind === 'w') h += '<div class="vq-jp">' + esc(x.w[0]) + ' → ' + esc(x.c.k) + '</div><div>' + esc(x.w[1]) + '</div>';
      else h += '<div class="vq-jp">' + esc(x.c.k) + '</div><div>' + esc(x.c.u) + '</div>';
      if (c) {
        h += '<div class="vq-ro"><b>' + esc(c.k) + '</b> (' + esc(c.ro) + ') : ' + esc(c.u) + '</div>';
        var row = CD.reads.filter(function (r) { return r.c === c.k; }).map(function (r) { return esc(r.k) + ' ' + esc(r.y) + (r.irr ? '⚠' : ''); }).join(' · ');
        if (row) h += '<div class="vq-ro cq-row">' + row + '</div>';
      }
      h += '</div><div class="fbb">' + (canSpeak && x.kind === 'r' ? '<button type="button" class="mini" id="k-say" data-id="' + esc(x.i) + '">🔊 Écouter</button>' : '') + '<button type="button" class="qgo" id="k-next">' + (last ? 'Voir le score' : 'Suivant') + '</button></div></div>';
      $('k-fb').innerHTML = h;
      $('k-fb').scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    }
    function showResult() {
      if (!Q.done) { Q.done = true; ST.cqs.sess++; save(); }
      barI.style.width = '100%'; prog.textContent = '';
      var n = Q.items.length, pct = Math.round(Q.ok / n * 100), secs = Math.round((Date.now() - Q.t0) / 1000);
      var list = Q.wrongList.map(function (w) { var x = byI[w.i]; return '<div class="q-miss"><span>' + esc(lineOf(x)) + '</span></div>'; }).join('');
      body.innerHTML = '<div class="q-score"><div class="n">' + Q.ok + '<small> / ' + n + '</small></div><div class="p">' + pct + ' % · ' + Math.floor(secs / 60) + ' min ' + (secs % 60) + ' s</div></div>' +
        (list ? '<h4 class="q-h">À revoir (' + Q.wrongList.length + ')</h4><div class="q-miss-list">' + list + '</div>' : '<p class="conj-note">Sans faute. Bravo.</p>') +
        '<div class="q-end">' + (list ? '<button type="button" class="qgo" id="k-again">Refaire les ratés</button>' : '') + '<button type="button" class="mini" id="k-new">Nouveau quiz</button><button type="button" class="mini" id="k-close">Fermer</button></div>';
    }
    function showStats() {
      Q = null; ttl.textContent = 'Statistiques'; prog.textContent = ''; barI.style.width = '0';
      var S = ST.cqs, pc = function (a, b) { return b ? Math.round(a / b * 100) + ' %' : '—'; };
      function row(name, T) { var p = T.n ? Math.round(T.ok / T.n * 100) : 0; return '<div class="qs-row"><div class="qs-l"><span>' + name + '</span><span><b>' + T.n + '</b> · ' + pc(T.ok, T.n) + '</span></div><div class="qs-bar"><i style="width:' + p + '%"></i></div></div>'; }
      var cts = Object.keys(S.ct).filter(function (k) { return S.ct[k].n; }).sort(function (a, b) { return (S.ct[a].ok / S.ct[a].n) - (S.ct[b].ok / S.ct[b].n) || S.ct[b].n - S.ct[a].n; });
      var h = '<div class="q-stats"><div class="qs-tiles"><div><b>' + S.sess + '</b><span>quiz terminés</span></div><div><b>' + S.q + '</b><span>questions</span></div><div><b>' + pc(S.ok, S.q) + '</b><span>de réussite</span></div></div>';
      h += '<h4 class="q-h">Par type de question</h4><div class="qs-types">' + CT.map(function (t) { return row(t.label, S.ty[t.id] || { n: 0, ok: 0 }); }).join('') + '</div>';
      if (cts.length) h += '<h4 class="q-h">Par compteur (les plus difficiles d’abord)</h4><div class="qs-types">' + cts.map(function (k) { return row(esc(k) + (cinfo[k] ? ' · ' + esc(cinfo[k].ro) : ''), S.ct[k]); }).join('') + '</div>';
      var worst = Object.keys(ST.cq).map(function (k) { var v = ST.cq[k]; return { i: k, x: v.x || (v.w ? 1 : 0), n: v.n }; }).filter(function (v) { return v.x > 0 && byI[v.i]; }).sort(function (a, b) { return b.x - a.x || (b.x / b.n) - (a.x / a.n); }).slice(0, 15);
      h += '<h4 class="q-h">Les plus ratés</h4>' + (worst.length ? '<div class="q-miss-list">' + worst.map(function (v) { return '<div class="q-miss"><span>' + esc(lineOf(byI[v.i])) + '</span><span class="qs-cnt">' + v.x + ' / ' + v.n + '</span></div>'; }).join('') + '</div>' : '<p class="conj-note">Aucun raté enregistré pour l’instant.</p>');
      h += '<div class="q-end"><button type="button" class="qgo" id="k-back">Retour</button><button type="button" class="mini" id="k-reset">Effacer les statistiques</button></div></div>';
      body.innerHTML = h;
    }
  }

