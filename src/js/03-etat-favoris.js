  /* ── état persistant ── */
  var ST = { ss: '', gq: {}, gqc: null, gqs: { sess: 0, q: 0, ok: 0, ty: {}, rg: {} }, qh: {}, sh: [], hist: {}, day: { d: '', n: 0, ok: 0 }, goal: 20, strk: { last: '', n: 0 }, fav: [], rec: [], su: {}, fs: 1, aid: false, silent: false, trip: { d: '', s: '', show: true }, showRec: true, mqc: null, kq: {}, kqc: null, kqs: { sess: 0, q: 0, ok: 0, ty: {} }, vq: {}, vqc: null, gq_c: {}, gqc_c: null, gqs_c: { sess: 0, q: 0, ok: 0, ty: {}, lab: {}, pt: {} }, cq: {}, cqc: null, cqs: { sess: 0, q: 0, ok: 0, ty: {}, ct: {} }, gq_p: {}, gqc_p: null, gqs_p: { sess: 0, q: 0, ok: 0, ty: {}, lab: {}, pt: {} }, vqs: { sess: 0, q: 0, ok: 0, ty: {}, cat: {} } };
  try { var raw0 = localStorage.getItem('jp-state'); if (raw0) { var o0 = JSON.parse(raw0); Object.keys(ST).forEach(function (k) { if (o0[k] !== undefined) ST[k] = o0[k]; }); } } catch (e) {}
  function save() { try { localStorage.setItem('jp-state', JSON.stringify(ST)); } catch (e) {} }
  /* ── objectif du jour : compte chaque réponse de quiz, série de jours consécutifs ── */
  function dkey(t) { var d = t ? new Date(t) : new Date(); return d.getFullYear() + '-' + ('0' + (d.getMonth() + 1)).slice(-2) + '-' + ('0' + d.getDate()).slice(-2); }
  function dayState() { var k = dkey(); if (!ST.day || ST.day.d !== k) ST.day = { d: k, n: 0, ok: 0 }; return ST.day; }
  function dayHit(good, key) {
    var D = dayState(); D.n++; if (good) D.ok++;
    if (key) { var QH = ST.qh = ST.qh || {}, H1 = QH[key] = QH[key] || {}, e = H1[D.d] = H1[D.d] || { n: 0, ok: 0 }; e.n++; if (good) e.ok++; var hk1 = Object.keys(H1).sort(); while (hk1.length > 60) delete H1[hk1.shift()]; }
    ST.hist = ST.hist || {}; ST.hist[D.d] = { n: D.n, ok: D.ok }; var hk = Object.keys(ST.hist).sort(); while (hk.length > 60) delete ST.hist[hk.shift()];
    if (D.n === ST.goal) {
      var y = dkey(Date.now() - 864e5);
      ST.strk = { last: D.d, n: ST.strk.last === y ? ST.strk.n + 1 : (ST.strk.last === D.d ? ST.strk.n : 1) };
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
