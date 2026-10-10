  /* ── état persistant ── */
  var ST = { ss: '', gq: {}, gqc: null, gqs: { sess: 0, q: 0, ok: 0, ty: {}, rg: {} }, qh: {}, sh: [], hist: {}, day: { d: '', n: 0, ok: 0 }, goal: 20, rc: { cnt: {}, seed: 0, run: 0, bestRun: 0, bestStrk: 0, bd: { p: 0, n: 0, d: '' }, big: { n: 0, d: '' }, days: -1, spd: {} }, strk: { last: '', n: 0 }, fav: [], rec: [], su: {}, rv: {}, chart: 'bar', range: '7', mapl: 'k', fs: 1, aid: false, silent: false, trip: { d: '', s: '', show: true }, showRec: true, mqc: null, kq: {}, kqc: null, kqs: { sess: 0, q: 0, ok: 0, ty: {} }, vq: {}, vqc: null, gq_c: {}, gqc_c: null, gqs_c: { sess: 0, q: 0, ok: 0, ty: {}, lab: {}, pt: {} }, cq: {}, cqc: null, cqs: { sess: 0, q: 0, ok: 0, ty: {}, ct: {} }, gq_p: {}, gqc_p: null, gqs_p: { sess: 0, q: 0, ok: 0, ty: {}, lab: {}, pt: {} }, vqs: { sess: 0, q: 0, ok: 0, ty: {}, cat: {} } };
  try { var raw0 = localStorage.getItem('jp-state'); if (raw0) { var o0 = JSON.parse(raw0); Object.keys(ST).forEach(function (k) { if (o0[k] !== undefined) ST[k] = o0[k]; }); } } catch (e) {}
  /* ── records : compteurs cumulés (survivent aux remises à zéro des quiz), initialisés avec l'existant ── */
  (function () {
    var R = ST.rc = ST.rc || {}; R.cnt = R.cnt || {}; R.spd = R.spd || {}; R.bd = R.bd || { p: 0, n: 0, d: '' }; R.big = R.big || { n: 0, d: '' };
    if (!(R.days >= 0)) R.days = Object.keys(ST.hist || {}).filter(function (k) { return ST.hist[k].n > 0; }).length;
    ['run', 'bestRun', 'bestStrk'].forEach(function (k) { R[k] = R[k] || 0; });
    if (!R.seed) { var m = { k: 'kqs', v: 'vqs', c: 'gqs_c', p: 'gqs_p', n: 'cqs', g: 'gqs' }; Object.keys(m).forEach(function (k) { R.cnt[k] = (ST[m[k]] && ST[m[k]].q) || 0; }); R.seed = 1; }
  })();
  var _AB = [];
  /* ── « plus ratés » : classement par erreurs cumulées, partagé par tous les quiz ── */
  function missCnt(v) { return (v && (v.x || (v.w ? 1 : 0))) || 0; }
  function missKeys(items, valid) {
    items = items || {};
    return Object.keys(items).filter(function (k) { return missCnt(items[k]) > 0 && (!valid || valid(k)); }).sort(function (a, b) {
      var A = items[a], B = items[b], xa = missCnt(A), xb = missCnt(B); return xb - xa || (xb / (B.n || 1)) - (xa / (A.n || 1)) || (B.n || 0) - (A.n || 0);
    });
  }
  function missFix(cfg, items, wc, valid) {
    var hc = missKeys(items, valid).length;
    if (!hc) { cfg.wrong = false; cfg.top = 0; }
    else if (cfg.wrong) { if (cfg.top > 0 && cfg.top > hc) cfg.top = 'all'; if (!cfg.top && !wc) cfg.top = 'all'; }
    return hc;
  }
  function missSet(cfg, items, valid) {
    if (!cfg.wrong || !cfg.top) return null;
    var ks = missKeys(items, valid), set = {}; (cfg.top === 'all' ? ks : ks.slice(0, cfg.top)).forEach(function (k) { set[k] = 1; }); return set;
  }
  function missPass(cfg, items, id, ts) { if (!cfg.wrong) return true; if (ts) return !!ts[id]; return !!(items[id] && items[id].w); }
  function missUi(cfg, items, wc, valid) {
    var hc = missKeys(items, valid).length, opts = [];
    if (wc) opts.push([0, 'En cours · ' + wc]);
    [10, 25, 50, 100].forEach(function (n) { if (hc >= n) opts.push([n, 'Top ' + n]); });
    opts.push(['all', 'Tout l’historique · ' + hc]);
    var cur = cfg.top || 0;
    return '<div class="qmiss"><small>Cibler : ' + (cur === 0 ? 'les ratés pas encore corrigés' : cur === 'all' ? 'tout ce que tu as déjà raté' : 'les ' + cur + ' plus ratés (erreurs cumulées)') + '</small><div class="qchips">' +
      opts.map(function (o) { return '<button type="button" class="qchip' + (cur === o[0] ? ' on' : '') + '" data-top="' + o[0] + '">' + o[1] + '</button>'; }).join('') + '</div></div>';
  }
  function missTop(cfg, v) { cfg.top = v === 'all' ? 'all' : +v; if (cfg.top > 0) cfg.n = cfg.top; }
  function save() { try { localStorage.setItem('jp-state', JSON.stringify(ST)); } catch (e) {} }
  /* ── objectif du jour : compte chaque réponse de quiz, série de jours consécutifs ── */
  function dkey(t) { var d = t ? new Date(t) : new Date(); return d.getFullYear() + '-' + ('0' + (d.getMonth() + 1)).slice(-2) + '-' + ('0' + d.getDate()).slice(-2); }
  function dayState() { var k = dkey(); if (!ST.day || ST.day.d !== k) ST.day = { d: k, n: 0, ok: 0 }; return ST.day; }
  /* records : total par type, séries, meilleur % et plus grosse journée, jours d'étude, temps pour enchaîner 10/25/50/100 questions (≥ 80 % de réussite, pause max 60 s) */
  var SPD_N = [10, 25, 50, 100];
  function rcHit(good, key, D) {
    var R = ST.rc, now = Date.now();
    if (key) R.cnt[key] = (R.cnt[key] || 0) + 1;
    R.run = good ? (R.run || 0) + 1 : 0; if (R.run > R.bestRun) R.bestRun = R.run;
    if (D.n >= 10) { var p = Math.round(D.ok * 1000 / D.n) / 10; if (p > R.bd.p || (p === R.bd.p && D.n > R.bd.n)) R.bd = { p: p, n: D.n, d: D.d }; }
    if (_AB.length && now - _AB[_AB.length - 1].t > 60000) _AB = [];
    _AB.push({ t: now, g: good ? 1 : 0 }); if (_AB.length > 100) _AB.shift();
    if (D.n === 1) R.days++;
    if (D.n > R.big.n) R.big = { n: D.n, d: D.d };
    SPD_N.forEach(function (N) {
      if (_AB.length < N) return;
      var w = _AB.slice(-N), ok = w.reduce(function (a, e) { return a + e.g; }, 0);
      if (ok / N < 0.8) return;
      var sec = Math.round((w[N - 1].t - w[0].t) * N / (N - 1) / 100) / 10, b = R.spd[N];   /* durée estimée des N questions */
      if (b && !b.t && b.s) b.t = Math.round(b.s * N * 10) / 10;
      if (sec > 0 && (!b || !b.t || sec < b.t)) R.spd[N] = { t: sec, d: D.d };
    });
  }
  function dayHit(good, key) {
    var D = dayState(); D.n++; if (good) D.ok++;
    rcHit(good, key, D);
    if (key) { var QH = ST.qh = ST.qh || {}, H1 = QH[key] = QH[key] || {}, e = H1[D.d] = H1[D.d] || { n: 0, ok: 0 }; e.n++; if (good) e.ok++; var hk1 = Object.keys(H1).sort(); while (hk1.length > 60) delete H1[hk1.shift()]; }
    ST.hist = ST.hist || {}; ST.hist[D.d] = { n: D.n, ok: D.ok }; var hk = Object.keys(ST.hist).sort(); while (hk.length > 60) delete ST.hist[hk.shift()];
    if (D.n === ST.goal) {
      var y = dkey(Date.now() - 864e5);
      ST.strk = { last: D.d, n: ST.strk.last === y ? ST.strk.n + 1 : (ST.strk.last === D.d ? ST.strk.n : 1) };
      if (ST.strk.n > ST.rc.bestStrk) ST.rc.bestStrk = ST.strk.n;
      try { toast('Objectif du jour atteint 🎉'); } catch (e) {}
    }
    save();
  }
  /* ── compte à rebours du voyage (date réglable, avion comme barre de progression) ── */
  function ymd(t) { var d = new Date(t); return d.getFullYear() + '-' + ('0' + (d.getMonth() + 1)).slice(-2) + '-' + ('0' + d.getDate()).slice(-2); }
  function dayNum(k) { var a = String(k).split('-'); return Math.round(Date.UTC(+a[0], +a[1] - 1, +a[2]) / 864e5); }
  var PLANE = '<svg class="tr-plane" viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path fill="currentColor" d="M21 16v-2l-8-5V3.5a1.5 1.5 0 0 0-3 0V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5z" transform="rotate(90 12 12)"/></svg>';
  function tripCard() {
    var T = ST.trip || {}; if (!T.show) return '';
    if (!T.d) return '<div class="ntrip"><div class="tr-h"><b>Voyage au Japon</b></div><p class="tr-s">Choisis ta date de départ pour lancer le compte à rebours.</p><button type="button" class="mini" data-act="trip-set">Choisir la date</button></div>';
    var today = dayNum(ymd(Date.now())), end = dayNum(T.d), start = dayNum(T.s || ymd(Date.now())), left = end - today;
    if (left < 0) return '';
    var span = Math.max(1, end - start), f = Math.max(0, Math.min(1, (today - start) / span)), pct = Math.round(f * 100);
    var dt = new Date(T.d + 'T12:00:00').toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' });
    var big = left === 0 ? 'C’est aujourd’hui !' : 'J-' + left;
    var sub = left === 0 ? 'Bon voyage !' : (left === 1 ? 'jour avant le départ' : 'jours avant le départ');
    return '<div class="ntrip"><div class="tr-h"><b>Voyage au Japon</b><span>' + dt + '</span></div><div class="tr-n"><b>' + big + '</b><small>' + sub + '</small></div>' +
      '<div class="tr-bar" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="' + pct + '"><i style="width:' + pct + '%"></i><span style="left:' + pct + '%">' + PLANE + '</span></div>' +
      '<small class="tr-s">' + pct + ' % du chemin parcouru</small></div>';
  }
  function dayCard() {
    var D = dayState(), g = ST.goal, p = Math.min(100, Math.round(D.n * 100 / g)), y = dkey(Date.now() - 864e5);
    var s = (ST.strk.last === D.d || ST.strk.last === y) ? ST.strk.n : 0;
    return '<div class="nday"><div class="nd-h"><b>Objectif du jour</b><span>' + Math.min(D.n, g) + ' / ' + g + (D.n >= g ? ' ✓' : '') + '</span></div><div class="nd-bar" role="progressbar" aria-valuenow="' + p + '" aria-valuemin="0" aria-valuemax="100"><i style="width:' + p + '%"></i></div><small>' + (D.n ? D.ok + ' bonnes réponses sur ' + D.n + ' · ' : 'Réponds à ' + g + ' questions pour valider la journée · ') + (s ? '🔥 ' + s + ' jour' + (s > 1 ? 's' : '') + ' de suite' : 'pas encore de série') + '</small></div>';
  }
  function rvCount() { return Object.keys(ST.rv || {}).length; }
  function rvCard() {
    var ks = Object.keys(ST.rv || {}); if (!ks.length) return '';
    var by = {}; ks.forEach(function (k) { var id = ST.rv[k].id; by[id] = (by[id] || 0) + 1; });
    var chips = Object.keys(by).filter(function (id) { return subMap[id]; }).map(function (id) { return '<button type="button" class="rv-c" data-act="rv-sub" data-id="' + esc(id) + '">' + esc(subMap[id].title) + ' <b>' + by[id] + '</b></button>'; }).join('');
    return '<div class="nrv"><div class="rv-h"><b>🔖 Fiches à revoir</b><span>' + ks.length + ' fiche' + (ks.length > 1 ? 's' : '') + '</span></div>' + (chips ? '<div class="rv-l">' + chips + '</div>' : '') + '<button type="button" class="ngo" data-act="rv-all">Réviser mes ' + ks.length + ' fiche' + (ks.length > 1 ? 's' : '') + '</button></div>';
  }
  function toast(msg, action, fn) {
    var t = document.createElement('div'); t.className = 'toast'; t.setAttribute('role', 'status');
    t.innerHTML = '<span>' + esc(msg) + '</span>' + (action ? '<button>' + esc(action) + '</button>' : '');
    if (action) t.querySelector('button').addEventListener('click', function () { fn(); t.remove(); });
    document.body.appendChild(t); setTimeout(function () { t.remove(); }, action ? 12000 : 2600);
  }
  function openTo(rec) { navOpen(rec.sec, rec.sub); }

  /* ── favoris & récents ── */
  var home = document.createElement('div'); home.className = 'home';
  function chip(id) { var r = subMap[id]; if (!r) return ''; return '<button class="chip" data-id="' + esc(id) + '"><small>' + esc(r.secLabel) + '</small>' + esc(r.title) + '</button>'; }
  function renderHome() {
    var f = ST.fav.filter(function (id) { return subMap[id]; }), r = ST.rec.filter(function (id) { return subMap[id]; });
    var h = '';
    if (f.length) h += '<h3>★ Favoris</h3><div class="chips">' + f.map(chip).join('') + '</div>';
    if (r.length && ST.showRec) h += '<h3>Récents</h3><div class="chips">' + r.map(chip).join('') + '</div>';
    home.innerHTML = h;
  }
  home.addEventListener('click', function (e) { var c = e.target.closest('.chip'); if (c) openTo(subMap[c.dataset.id]); });
  function syncFavButtons() { document.querySelectorAll('.fav').forEach(function (b) { var on = ST.fav.indexOf(b.dataset.id) >= 0; b.classList.toggle('on', on); b.textContent = on ? '★' : '☆'; b.setAttribute('aria-pressed', on ? 'true' : 'false'); }); }
  document.addEventListener('toggle', function (e) {
    var d = e.target; if (!d.matches || !d.matches('details.sub') || !d.open) return;
    var id = Object.keys(subMap).filter(function (k) { return subMap[k].sub === d; })[0]; if (!id) return;
    ST.rec = [id].concat(ST.rec.filter(function (x) { return x !== id; })).slice(0, 3); save(); renderHome();
  }, true);



  /* anti-indices : retire les parenthèses contenant du japonais, qui donneraient la réponse */
  function noJpHint(s) { return String(s).replace(/\s*[（(][^）)]*[぀-ヿ㐀-鿿][^）)]*[）)]/g, '').replace(/\s+/g, ' ').trim(); }
