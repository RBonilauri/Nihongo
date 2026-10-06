  /* ── état persistant ── */
  var ST = { sh: [], hist: {}, day: { d: '', n: 0, ok: 0 }, goal: 20, strk: { last: '', n: 0 }, fav: [], rec: [], su: {}, fs: 1, aid: false, showRec: true, mqc: null, kq: {}, kqc: null, kqs: { sess: 0, q: 0, ok: 0, ty: {} }, vq: {}, vqc: null, gq_c: {}, gqc_c: null, gqs_c: { sess: 0, q: 0, ok: 0, ty: {}, lab: {}, pt: {} }, cq: {}, cqc: null, cqs: { sess: 0, q: 0, ok: 0, ty: {}, ct: {} }, gq_p: {}, gqc_p: null, gqs_p: { sess: 0, q: 0, ok: 0, ty: {}, lab: {}, pt: {} }, vqs: { sess: 0, q: 0, ok: 0, ty: {}, cat: {} } };
  try { var raw0 = localStorage.getItem('jp-state'); if (raw0) { var o0 = JSON.parse(raw0); Object.keys(ST).forEach(function (k) { if (o0[k] !== undefined) ST[k] = o0[k]; }); } } catch (e) {}
  function save() { try { localStorage.setItem('jp-state', JSON.stringify(ST)); } catch (e) {} }
  /* ── objectif du jour : compte chaque réponse de quiz, série de jours consécutifs ── */
  function dkey(t) { var d = t ? new Date(t) : new Date(); return d.getFullYear() + '-' + ('0' + (d.getMonth() + 1)).slice(-2) + '-' + ('0' + d.getDate()).slice(-2); }
  function dayState() { var k = dkey(); if (!ST.day || ST.day.d !== k) ST.day = { d: k, n: 0, ok: 0 }; return ST.day; }
  function dayHit(good) {
    var D = dayState(); D.n++; if (good) D.ok++;
    ST.hist = ST.hist || {}; ST.hist[D.d] = { n: D.n, ok: D.ok }; var hk = Object.keys(ST.hist).sort(); while (hk.length > 60) delete ST.hist[hk.shift()];
    if (D.n === ST.goal) {
      var y = dkey(Date.now() - 864e5);
      ST.strk = { last: D.d, n: ST.strk.last === y ? ST.strk.n + 1 : (ST.strk.last === D.d ? ST.strk.n : 1) };
      try { toast('Objectif du jour atteint 🎉'); } catch (e) {}
    }
    save();
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


