  /* ═══════════ QUIZ GÉOGRAPHIE ═══════════ */
  var GTY = [
    { id: 'map', label: 'Repérer sur la carte' },
    { id: 'reg', label: 'Quelle région ?' },
    { id: 'cap', label: 'Chef-lieu' },
    { id: 'c2p', label: 'Chef-lieu → préfecture' },
    { id: 'rd', label: 'Lecture du nom' },
    { id: 'rmap', label: 'Régions sur la carte' },
    { id: 'ear', label: '🔊 Écoute → préfecture' }
  ];
  function initGeo(mainEl) {
    var M = jpm(); if (!M) return;
    var canSpeak = !!window.speechSynthesis;
    var types = GTY.filter(function (t) { return canSpeak || t.id !== 'ear'; });
    var ALL = M.p.map(function (o) { return { i: 'g:' + o.n, k: 'p', o: o, r: o.r }; }).concat(M.ids.map(function (r) { return { i: 'r:' + r, k: 'r', r: r }; }));
    var byI = {}; ALL.forEach(function (x) { byI[x.i] = x; });
    var GN2 = [10, 25, 50, 100];
    var cfg = ST.gqc || { regs: M.ids.slice(), types: types.map(function (t) { return t.id; }), n: 25, wrong: false };
    cfg.types = cfg.types.filter(function (t) { return types.some(function (u) { return u.id === t; }); }); if (!cfg.types.length) cfg.types = types.map(function (t) { return t.id; });
    if (!ST.gq) ST.gq = {};
    var Q = null;
    var rl = function (r) { return M.reg[r][0] + ' · ' + M.reg[r][1]; };
    function shuffle(a) { for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
    function elig(x, t) {
      if (x.k === 'r') return t === 'rmap';
      if (t === 'rmap') return false;
      if ((t === 'cap' || t === 'c2p') && x.o.cap === x.o.n) return false;
      return true;
    }
    function pool() { return ALL.filter(function (x) { return cfg.regs.indexOf(x.r) >= 0 && (!cfg.wrong || (ST.gq[x.i] && ST.gq[x.i].w)); }); }
    function countAvail() { var q = 0, p = pool(); p.forEach(function (x) { q += cfg.types.filter(function (t) { return elig(x, t); }).length; }); return { q: q, k: p.length }; }
    function bucket(x) { var s = ST.gq[x.i]; if (!s) return 1; if (s.w) return 0; if (s.st >= 3) return 3; return 2; }
    function build() {
      var order = shuffle(pool().slice()).sort(function (a, b) { return bucket(a) - bucket(b); }), av = countAvail().q;
      var target = cfg.n === 0 ? av : Math.min(cfg.n, av), items = [], used = {}, guard = 0;
      while (items.length < target && guard++ < 20) {
        var round = [];
        order.forEach(function (x) {
          if (items.length + round.length >= target) return;
          var ok = cfg.types.filter(function (t) { return elig(x, t) && !(used[x.i] && used[x.i][t]); }); if (!ok.length) return;
          var t = ok[Math.floor(Math.random() * ok.length)]; (used[x.i] = used[x.i] || {})[t] = 1; round.push({ i: x.i, t: t });
        });
        if (!round.length) break; items = items.concat(shuffle(round));
      }
      return items;
    }
    MIXREG['geo'] = {
      label: 'Géographie',
      count: function () { var sv = cfg; cfg = { regs: M.ids.slice(), types: types.map(function (t) { return t.id; }), n: 0, wrong: false }; var r = countAvail().q; cfg = sv; return r; },
      make: function (n) { var sv = cfg; cfg = { regs: M.ids.slice(), types: types.map(function (t) { return t.id; }), n: n, wrong: false }; var r = build(); cfg = sv; return r; },
      show: function (it, hooks, idx, total) {
        Q = { items: idx < total ? [it, it] : [it], i: 0, ok: 0, wrongList: [], t0: Date.now(), mix: hooks, mixTag: '<div class="q-tag q-tag-mix"><b>Géographie</b></div>' };
        el.style.zIndex = 95; el.hidden = false; document.body.style.overflow = 'hidden';
        showQ(); ttl.textContent = 'Quiz général'; prog.textContent = idx + ' / ' + total; barI.style.width = ((idx - 1) / total * 100) + '%'; body.scrollTop = 0;
      },
      hide: function () { el.hidden = true; el.style.zIndex = ''; Q = null; paintCard(); }
    };
    var el = document.createElement('div'); el.className = 'quiz'; el.hidden = true;
    el.innerHTML = '<div class="q-top"><button class="x" type="button" aria-label="Fermer">×</button><div class="ttl">Quiz géographie</div><div class="prog"></div></div><div class="q-bar"><i></i></div><div class="q-body"></div>';
    document.body.appendChild(el);
    var body = el.querySelector('.q-body'), prog = el.querySelector('.prog'), barI = el.querySelector('.q-bar i'), ttl = el.querySelector('.ttl');
    function $(id) { return el.querySelector('#' + id); }
    var card = document.createElement('button'); card.type = 'button'; card.className = 'quizcard';
    function wrongCount() { return Object.keys(ST.gq).filter(function (k) { return ST.gq[k].w && byI[k]; }).length; }
    function paintCard() {
      var seen = Object.keys(ST.gq).length, w = wrongCount();
      card.innerHTML = '<span class="qc-jp">地理</span><span class="qc-t">Quiz géographie<small>47 préfectures · 8 régions · cartes · ' + (seen ? seen + ' vus' + (w ? ', ' + w + ' à revoir' : '') : 'jamais lancé') + '</small></span><span class="qc-go">›</span>';
    }
    paintCard();
    card.addEventListener('click', function () { open(true); showSetup(); });
    quizHost(mainEl).appendChild(card);
    function hideG() { el.hidden = true; document.body.style.overflow = ''; paintCard(); }
    function open(v) { if (v) { if (el.hidden) bkPush(hideG); el.hidden = false; document.body.style.overflow = 'hidden'; } else bkClose(hideG); }
    el.querySelector('.x').addEventListener('click', function () { if (Q && Q.mix) { Q.mix.quit(); return; } open(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !el.hidden && !(Q && Q.mix)) open(false); });

    function chip(label, on, data, dis) { return '<button type="button" class="qchip' + (on ? ' on' : '') + '"' + (dis ? ' disabled' : '') + ' ' + data + '>' + label + '</button>'; }
    function toggle(arr, v) { var i = arr.indexOf(v); if (i >= 0) arr.splice(i, 1); else arr.push(v); }
    function persist() { ST.gqc = cfg; save(); }
    function showSetup() {
      Q = null; ttl.textContent = 'Quiz géographie'; prog.textContent = ''; barI.style.width = '0';
      var av = countAvail(); if (cfg.n !== 0 && cfg.n > av.q) cfg.n = 0;
      var wc = wrongCount(), h = '';
      h += '<div class="q-sec"><h4>Régions</h4><div class="qchips">' + M.ids.map(function (r) { return chip(esc(M.reg[r][0]) + ' · ' + M.p.filter(function (o) { return o.r === r; }).length, cfg.regs.indexOf(r) >= 0, 'data-r="' + r + '"'); }).join('') + '</div></div>';
      h += '<div class="q-sec"><h4>Types de questions</h4><div class="qchips">' + types.map(function (t) { return chip(t.label, cfg.types.indexOf(t.id) >= 0, 'data-t="' + t.id + '"'); }).join('') + '</div></div>';
      h += '<div class="q-sec"><h4>Nombre de questions</h4><div class="qchips">' + GN2.filter(function (n) { return n <= av.q; }).map(function (n) { return chip(n, cfg.n === n, 'data-n="' + n + '"'); }).join('') + chip('Tout · ' + av.q, cfg.n === 0, 'data-n="0"', av.q === 0) + '</div></div>';
      h += '<div class="q-sec"><div class="row"><span class="lab">Seulement mes ratés<small>' + (wc ? wc + ' à revoir' : 'Aucun raté pour l’instant') + '</small></span><button class="sw" type="button" id="g-wrong" role="switch" aria-checked="' + !!cfg.wrong + '"' + (wc ? '' : ' disabled') + '><i></i></button></div></div>';
      h += '<button type="button" class="mini qstat-btn" id="g-stats">📊 Statistiques</button>';
      h += '<button type="button" class="qgo" id="g-go"' + (cfg.regs.length && cfg.types.length && av.q ? '' : ' disabled') + '>Lancer · ' + (cfg.n === 0 ? av.q : Math.min(cfg.n, av.q)) + ' questions</button>';
      body.innerHTML = h; body.scrollTop = 0;
    }
    function showStats() {
      Q = null; ttl.textContent = 'Statistiques'; prog.textContent = ''; barI.style.width = '0';
      var S = ST.gqs || { sess: 0, q: 0, ok: 0, ty: {}, rg: {} }, pc = function (a, b) { return b ? Math.round(a / b * 100) + ' %' : '—'; };
      function row(name, T) { T = T || { n: 0, ok: 0 }; var p = T.n ? Math.round(T.ok / T.n * 100) : 0; return '<div class="qs-row"><div class="qs-l"><span>' + name + '</span><span><b>' + T.n + '</b> · ' + pc(T.ok, T.n) + '</span></div><div class="qs-bar"><i style="width:' + p + '%"></i></div></div>'; }
      var h = '<div class="q-stats"><div class="qs-tiles"><div><b>' + S.sess + '</b><span>quiz terminés</span></div><div><b>' + S.q + '</b><span>questions</span></div><div><b>' + pc(S.ok, S.q) + '</b><span>de réussite</span></div></div>';
      h += qsExtra('g', ST.gq, ALL.length);
      h += '<h4 class="q-h">Par type de question</h4><div class="qs-types">' + GTY.map(function (t) { return row(esc(t.label), (S.ty || {})[t.id]); }).join('') + '</div>';
      h += '<h4 class="q-h">Par région</h4><div class="qs-types">' + M.ids.map(function (r) { return row(esc(M.reg[r][0]), (S.rg || {})[r]); }).join('') + '</div>';
      var worst = Object.keys(ST.gq).map(function (k) { var v = ST.gq[k]; return { k: k, x: v.x || (v.w ? 1 : 0), n: v.n }; }).filter(function (v) { return v.x > 0 && byI[v.k]; }).sort(function (a, b) { return b.x - a.x || (b.x / b.n) - (a.x / a.n); }).slice(0, 15);
      h += '<h4 class="q-h">Les plus ratés</h4>';
      h += worst.length ? '<div class="q-miss-list">' + worst.map(function (v) { var x = byI[v.k]; return '<div class="q-miss"><span class="vq-mj">' + esc(x.k === 'r' ? M.reg[x.r][0] : x.o.n) + '</span><span>' + esc(x.k === 'r' ? M.reg[x.r][1] : x.o.ro) + '</span><span class="qs-cnt">' + v.x + ' / ' + v.n + '</span></div>'; }).join('') + '</div>' : '<p class="conj-note">Aucun raté pour l’instant.</p>';
      h += '<div class="q-end"><button type="button" class="qgo" id="g-back">Retour</button><button type="button" class="mini" id="g-reset">Effacer les statistiques</button></div></div>';
      body.innerHTML = h; body.scrollTop = 0;
    }
    function pickPrefs(x, n, key) {
      var others = M.p.filter(function (o) { return o.n !== x.o.n; }), same = shuffle(others.filter(function (o) { return o.r === x.o.r; })), rest = shuffle(others.filter(function (o) { return o.r !== x.o.r; }));
      var out = [], seen = {}; seen[x.o[key]] = 1;
      same.slice(0, 2).concat(rest).concat(same.slice(2)).forEach(function (o) { if (out.length < n && !seen[o[key]]) { seen[o[key]] = 1; out.push(o); } });
      return out;
    }
    function options(it) {
      var x = byI[it.i], t = it.t, out;
      if (t === 'rmap') out = [{ v: rl(x.r), ok: true }].concat(shuffle(M.ids.filter(function (r) { return r !== x.r; })).slice(0, 3).map(function (r) { return { v: rl(r), ok: false }; }));
      else if (t === 'reg') out = [{ v: rl(x.o.r), ok: true }].concat(shuffle(M.ids.filter(function (r) { return r !== x.o.r; })).slice(0, 3).map(function (r) { return { v: rl(r), ok: false }; }));
      else if (t === 'cap') out = [{ v: x.o.cap, ok: true }].concat(pickPrefs(x, 3, 'cap').map(function (o) { return { v: o.cap, ok: false }; }));
      else if (t === 'rd') out = [{ v: x.o.k, ok: true }].concat(pickPrefs(x, 3, 'k').map(function (o) { return { v: o.k, ok: false }; }));
      else out = [{ v: x.o.n, ok: true }].concat(pickPrefs(x, 3, 'n').map(function (o) { return { v: o.n, ok: false }; }));
      return shuffle(out);
    }
    function setOf(x) { return x.k === 'r' ? M.p.filter(function (o) { return o.r === x.r; }).map(function (o) { return o.n; }) : [x.o.n]; }
    function sayG(x) { if (canSpeak) speak([x.k === 'r' ? M.reg[x.r][0] : x.o.k]); }
    function start(items) {
      if (!items.length) { toast('Aucune question disponible avec ces réglages.'); return; }
      Q = { items: items, i: 0, ok: 0, wrongList: [], t0: Date.now(), done: false }; showQ();
    }
    function showQ() {
      if (Q.i >= Q.items.length) return showResult();
      var it = Q.items[Q.i], x = byI[it.i], opts = options(it); Q.cur = { it: it, opts: opts, done: false };
      prog.textContent = (Q.i + 1) + ' / ' + Q.items.length; barI.style.width = (Q.i / Q.items.length * 100) + '%';
      var ask, big;
      if (it.t === 'map') { ask = 'Quelle est cette préfecture ?'; big = jpMiniSet(setOf(x), 'jm-quiz'); }
      else if (it.t === 'rmap') { ask = 'Quelle est cette région ?'; big = jpMiniSet(setOf(x), 'jm-quiz'); }
      else if (it.t === 'reg') { ask = 'Dans quelle région se trouve cette préfecture ?'; big = '<div class="q-big word vq">' + esc(x.o.n) + '</div>'; }
      else if (it.t === 'cap') { ask = 'Quel est le chef-lieu de cette préfecture ?'; big = '<div class="q-big word vq">' + esc(x.o.n) + '</div>'; }
      else if (it.t === 'c2p') { ask = 'De quelle préfecture est-ce le chef-lieu ?'; big = '<div class="q-big word vq">' + esc(x.o.cap) + '</div>'; }
      else if (it.t === 'rd') { ask = 'Comment se lit ce nom ?'; big = '<div class="q-big word vq">' + esc(x.o.n) + '</div>'; }
      else { ask = 'Écoute, puis choisis la préfecture'; big = '<button type="button" class="qgo vq-ear" id="g-replay">🔊 Réécouter</button>'; }
      body.innerHTML = '<div class="q-card">' + (Q.mixTag || '<div class="q-tag">Géographie</div>') + '<div class="q-ask">' + ask + '</div>' + big + '</div><div class="q-opts">' +
        opts.map(function (o, i) { return '<button type="button" class="qopt vq-opt" data-i="' + i + '">' + esc(o.v) + '</button>'; }).join('') + '</div><div id="g-fb"></div>';
      if (it.t === 'ear') setTimeout(function () { sayG(x); }, 150);
    }
    function answerHtml(x) {
      if (x.k === 'r') {
        var m = M.p.filter(function (o) { return o.r === x.r; });
        return '<div class="vq-ans"><div class="vq-jp">' + esc(M.reg[x.r][0]) + '</div><div class="vq-ro">' + esc(M.reg[x.r][1]) + '</div><div>' + m.map(function (o) { return esc(o.n); }).join('・') + '</div></div>';
      }
      var o = x.o;
      return '<div class="vq-ans"><div class="vq-jp">' + esc(o.n) + '</div><div>' + esc(o.k) + '</div><div class="vq-ro">' + esc(o.ro) + '</div>' +
        '<div><b>Région</b> · ' + esc(rl(o.r)) + '</div><div><b>Chef-lieu</b> · ' + esc(o.cap) + (o.cap !== o.capk ? ' (' + esc(o.capk) + ')' : '') + ' · ' + esc(o.capr) + '</div></div>';
    }
    function answer(b) {
      var cur = Q.cur; if (cur.done) return; cur.done = true;
      var o = cur.opts[+b.dataset.i], it = cur.it, x = byI[it.i], good = !!o.ok;
      body.querySelectorAll('.qopt').forEach(function (n) { var oo = cur.opts[+n.dataset.i]; n.disabled = true; if (oo.ok) n.classList.add('good'); else if (n === b) n.classList.add('bad'); });
      var st = ST.gq[x.i] || { n: 0, st: 0, w: false }; st.n++;
      dayHit(good, 'g');
      var GS = ST.gqs = ST.gqs || { sess: 0, q: 0, ok: 0, ty: {}, rg: {} }; GS.q++; if (good) GS.ok++;
      var GT0 = GS.ty[it.t] = GS.ty[it.t] || { n: 0, ok: 0 }; GT0.n++; if (good) GT0.ok++;
      var rk0 = x.k === 'r' ? x.r : x.o.r, GR = (GS.rg = GS.rg || {})[rk0] = (GS.rg[rk0] || { n: 0, ok: 0 }); GR.n++; if (good) GR.ok++;
      if (good) { Q.ok++; st.st++; st.w = false; } else { st.st = 0; st.w = true; st.x = (st.x || 0) + 1; if (!Q.wrongList.some(function (w) { return w.i === x.i; })) Q.wrongList.push({ i: x.i, t: it.t }); }
      ST.gq[x.i] = st; save();
      var last = Q.i + 1 >= Q.items.length;
      $('g-fb').innerHTML = '<div class="q-fb ' + (good ? 'good' : 'bad') + '"><div class="fbh">' + (good ? '✓ Bonne réponse' : '✗ Raté') + '</div>' + answerHtml(x) + (it.t === 'map' || it.t === 'rmap' ? '' : jpMiniSet(setOf(x), 'jm-mini')) +
        '<div class="fbb">' + (canSpeak ? '<button type="button" class="mini" id="g-say" data-id="' + x.i + '">🔊 Écouter</button>' : '') + '<button type="button" class="qgo" id="g-next">' + (last ? 'Voir le score' : 'Suivant') + '</button></div></div>';
      $('g-fb').scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    }
    function showResult() {
      if (!Q.done) { Q.done = true; (ST.gqs = ST.gqs || { sess: 0, q: 0, ok: 0, ty: {}, rg: {} }).sess++; save(); }
      barI.style.width = '100%'; prog.textContent = '';
      var n = Q.items.length, pct = Math.round(Q.ok / n * 100), secs = Math.round((Date.now() - Q.t0) / 1000);
      var list = Q.wrongList.map(function (w) { var x = byI[w.i]; return '<div class="q-miss"><span class="vq-mj">' + esc(x.k === 'r' ? M.reg[x.r][0] : x.o.n) + '</span><span>' + esc(x.k === 'r' ? M.reg[x.r][1] : x.o.ro) + '<small>' + esc(x.k === 'r' ? '' : rl(x.o.r)) + '</small></span></div>'; }).join('');
      body.scrollTop = 0; body.innerHTML = '<div class="q-score"><div class="n">' + Q.ok + '<small> / ' + n + '</small></div><div class="p">' + pct + ' % · ' + Math.floor(secs / 60) + ' min ' + (secs % 60) + ' s</div></div>' +
        (list ? '<h4 class="q-h">À revoir (' + Q.wrongList.length + ')</h4><div class="q-miss-list">' + list + '</div>' : '<p class="conj-note">Sans faute. Bravo.</p>') +
        '<div class="q-end">' + (list ? '<button type="button" class="qgo" id="g-again">Refaire les ratés</button>' : '') + '<button type="button" class="mini" id="g-new">Nouveau quiz</button><button type="button" class="mini" id="g-close">Fermer</button></div>';
    }
    body.addEventListener('click', function (e) {
      var b = e.target.closest('button'); if (!b || b.disabled) return;
      var d = b.dataset;
      if (d.r) { toggle(cfg.regs, d.r); persist(); showSetup(); }
      else if (d.t) { toggle(cfg.types, d.t); persist(); showSetup(); }
      else if (d.n !== undefined) { cfg.n = +d.n; persist(); showSetup(); }
      else if (b.id === 'g-wrong') { cfg.wrong = !cfg.wrong; persist(); showSetup(); }
      else if (b.id === 'g-go') { start(build()); }
      else if (b.id === 'g-stats') { showStats(); }
      else if (b.id === 'g-back') { showSetup(); }
      else if (b.id === 'g-reset') { if (confirm('Effacer toutes les statistiques du quiz géographie et les ratés ?')) { ST.gq = {}; ST.gqs = { sess: 0, q: 0, ok: 0, ty: {}, rg: {} }; if (ST.qh) delete ST.qh.g; save(); showStats(); } }
      else if (b.classList.contains('qopt')) answer(b);
      else if (b.id === 'g-next') { if (Q.mix) { Q.mix.next(Q.ok > 0); return; } Q.i++; showQ(); }
      else if (b.id === 'g-say') { sayG(byI[d.id]); }
      else if (b.id === 'g-replay') { sayG(byI[Q.cur.it.i]); }
      else if (b.id === 'g-again') { if (Q.wrongList.length) start(Q.wrongList.slice()); }
      else if (b.id === 'g-new') { showSetup(); }
      else if (b.id === 'g-close') { open(false); }
    });
  }
