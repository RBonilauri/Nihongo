
(function () {
  document.documentElement.classList.add('js');
  var q = document.getElementById('q'), clr = document.getElementById('clr'), box = document.getElementById('results');
  function fold(s) {
    var o = '';
    for (var i = 0; i < s.length; i++) {
      var c = s.charAt(i), code = c.charCodeAt(0);
      if (code >= 0x30A1 && code <= 0x30F6) { o += String.fromCharCode(code - 0x60); continue; }
      var n = c.normalize('NFD').charAt(0).toLowerCase();
      o += n || c;
    }
    return o;
  }
  var UNIT = 'tr, li, p, .group-card, .conj-ex-card, .te-card, .distinction-card, .fs-group, .conj-note, .sd-row, .conj-form-header, details.ex-answer, .section-title, .ex-list, .kanji-card, .cec-sentence';
  var index = [], subMap = {};
  function build() {
    var secs = document.querySelectorAll('details.sec');
    secs.forEach(function (sec, si) {
      sec.dataset.i = si;
      var secLabel = sec.querySelector(':scope > summary .lbl').textContent.trim();
      var jp = sec.querySelector(':scope > summary .jp').textContent.trim();
      function add(el, path, sec, sub) {
        var txt = (el.tagName === 'TR' ? Array.prototype.map.call(el.children, function (c) { return c.textContent.replace(/\s+/g, ' ').trim(); }).filter(Boolean).join(' · ') : el.textContent).replace(/\s+/g, ' ').trim();
        if (txt.length < 2) return;
        index.push({ el: el, path: path, sec: sec, sj: jp, sub: sub, text: txt, norm: fold(txt) + (el.dataset && el.dataset.ro ? ' ' + fold(el.dataset.ro) : '') });
      }
      add(sec.querySelector(':scope > summary'), jp + ' ' + secLabel, sec, null);
      var scope = function (root, path, sub) {
        var cands = Array.prototype.slice.call(root.querySelectorAll(UNIT));
        cands.forEach(function (el) {
          if (el.querySelector(UNIT)) return; // keep leaf-most units only
          add(el, path, sec, sub);
        });
      };
      var subs = sec.querySelectorAll(':scope > .sec-body > details.sub');
      subs.forEach(function (d, sj) {
        var lbl = d.querySelector(':scope > summary').textContent.trim();
        var path = secLabel + ' › ' + lbl;
        d.dataset.id = 's' + si + '-' + sj; subMap[path] = { sec: sec, sub: d, id: path, title: lbl, secLabel: secLabel };
        add(d.querySelector(':scope > summary'), path, sec, d);
        scope(d, path, d);
      });
      // content of the section outside sub-pages
      var body = sec.querySelector(':scope > .sec-body');
      Array.prototype.slice.call(body.children).forEach(function (ch) {
        if (ch.matches('details.sub')) return;
        if (ch.matches(UNIT) && !ch.querySelector(UNIT)) add(ch, secLabel, sec, null);
        else scope(ch, secLabel, null);
      });
    });
  }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function snippet(it, toks) {
    var t = it.text, n = it.norm, pos = -1;
    for (var i = 0; i < toks.length; i++) { var p = n.indexOf(toks[i]); if (p >= 0 && (pos < 0 || p < pos)) pos = p; }
    var start = Math.max(0, pos - 40), end = Math.min(t.length, start + 150);
    var seg = t.slice(start, end), segN = n.slice(start, end), marks = [];
    toks.forEach(function (tk) { var from = 0, p; while ((p = segN.indexOf(tk, from)) >= 0) { marks.push([p, p + tk.length]); from = p + tk.length; } });
    marks.sort(function (a, b) { return a[0] - b[0]; });
    var out = '', cur = 0;
    marks.forEach(function (m) { if (m[0] < cur) { if (m[1] > cur) { out += '<mark>' + esc(seg.slice(cur, m[1])) + '</mark>'; cur = m[1]; } return; }
      out += esc(seg.slice(cur, m[0])) + '<mark>' + esc(seg.slice(m[0], m[1])) + '</mark>'; cur = m[1]; });
    out += esc(seg.slice(cur));
    return (start > 0 ? '… ' : '') + out + (end < t.length ? ' …' : '');
  }
  var results = [], cur = null, shown = 40, shint = document.getElementById('shint'), scopesEl = document.getElementById('scopes');
  function setRes(v) { box.hidden = !v; if (shint) shint.hidden = v; }
  /* mots uniques de l'index (pour la correction d'une faute de frappe) */
  var vocabW = null;
  function lev1(a, b) { // vrai si distance d'édition ≤ 1
    var la = a.length, lb = b.length; if (Math.abs(la - lb) > 1) return false;
    var i = 0; while (i < la && i < lb && a.charAt(i) === b.charAt(i)) i++;
    if (la === lb) return a.slice(i + 1) === b.slice(i + 1) || (a.charAt(i) === b.charAt(i + 1) && a.charAt(i + 1) === b.charAt(i) && a.slice(i + 2) === b.slice(i + 2));
    return la > lb ? a.slice(i + 1) === b.slice(i) : b.slice(i + 1) === a.slice(i);
  }
  function fixTok(t) {
    if (!vocabW) { var m = {}; index.forEach(function (it) { (it.norm.match(/[a-z0-9]{4,}/g) || []).forEach(function (w) { m[w] = (m[w] || 0) + 1; }); }); vocabW = Object.keys(m).sort(function (a, b) { return m[b] - m[a]; }); }
    var out = []; for (var i = 0; i < vocabW.length && out.length < 6; i++) if (lev1(t, vocabW[i])) out.push(vocabW[i]);
    return out;
  }
  function altTok(t) { // variantes : kana (romaji), singulier français
    var a = [t], k = r2k(t); if (k && k !== t) a.push(k);
    if (t.length >= 4 && /[sx]$/.test(t)) a.push(t.slice(0, -1));
    return a;
  }
  function search(toks) {
    var hits = [];
    for (var i = 0; i < index.length; i++) {
      var it = index[i], ok = true, score = 0;
      for (var j = 0; j < toks.length; j++) {
        var p = -1, ws = false;
        for (var a = 0; a < toks[j].length; a++) {
          var tk = toks[j][a], pa = it.norm.indexOf(tk);
          if (pa >= 0 && (p < 0 || pa < p)) p = pa;
          if (pa >= 0 && !ws) { var q0 = pa; while (q0 >= 0) { if (q0 === 0 || !/[a-z0-9]/.test(it.norm.charAt(q0 - 1))) { ws = true; break; } q0 = it.norm.indexOf(tk, q0 + 1); } }
        }
        if (p < 0) { ok = false; break; }
        score += (ws ? 1.5 : 0) - Math.min(p, 200) / 400;
      }
      if (!ok) continue;
      if (it.el.tagName === 'SUMMARY' || it.el.classList.contains('section-title')) score += 4;
      score -= Math.min(it.text.length, 400) / 200;
      hits.push({ it: it, s: score });
    }
    hits.sort(function (a, b) { return b.s - a.s; });
    return hits;
  }
  function renderHist() {
    var h = document.getElementById('shist'), l = (ST.sh || []);
    if (!h) return;
    if (!l.length || q.value.trim()) { h.hidden = true; return; }
    h.innerHTML = '<div class="count">Recherches récentes <button type="button" class="shx" data-x="1">effacer</button></div>' + l.map(function (w, i) { return '<button type="button" class="chip" data-w="' + i + '">' + esc(w) + '</button>'; }).join('');
    h.hidden = false;
  }
  function remember(w) { w = w.trim(); if (w.length < 2) return; ST.sh = [w].concat((ST.sh || []).filter(function (x) { return x !== w; })).slice(0, 6); save(); }
  function scopeList() {
    var o = [], seen = {};
    index.forEach(function (it) { if (!seen[it.sj]) { seen[it.sj] = 1; o.push({ j: it.sj, l: it.sec.querySelector(':scope > summary .lbl').textContent.trim() }); } });
    return o;
  }
  function renderScopes(counts) {
    if (!scopesEl) return;
    var sc = ST.ss || '', tot = counts ? Object.keys(counts).reduce(function (a, k) { return a + counts[k]; }, 0) : 0;
    var h = '<button type="button" class="chip' + (sc ? '' : ' on') + '" data-sc="">Tout' + (counts ? ' <small>' + tot + '</small>' : '') + '</button>';
    scopeList().forEach(function (s) {
      var n = counts ? (counts[s.j] || 0) : null;
      h += '<button type="button" class="chip' + (sc === s.j ? ' on' : '') + (n === 0 && sc !== s.j ? ' zero' : '') + '" data-sc="' + esc(s.j) + '">' + esc(s.l) + (n !== null ? ' <small>' + n + '</small>' : '') + '</button>';
    });
    scopesEl.innerHTML = h;
    var on = scopesEl.querySelector('.on'); if (on && on.scrollIntoView && scopesEl.scrollWidth > scopesEl.clientWidth) scopesEl.scrollLeft = Math.max(0, on.offsetLeft - 40);
  }
  function paint() {
    if (!cur) return;
    var hits = cur.hits, raw = cur.raw, sc = ST.ss || '';
    results = hits.slice(0, shown).map(function (h) { return h.it; });
    var scLbl = ''; if (sc) { var f = scopeList().filter(function (s) { return s.j === sc; })[0]; scLbl = f ? f.l : sc; }
    var html = '<div class="count">' + hits.length + ' résultat' + (hits.length > 1 ? 's' : '') + (sc ? ' dans « ' + esc(scLbl) + ' »' : '') + '</div>';
    if (cur.fixed && results.length) html += '<div class="empty">Aucun résultat exact pour « ' + esc(raw) + ' » — résultats proches.</div>';
    if (!results.length) html += '<div class="empty">Aucun résultat pour « ' + esc(raw) + ' »' + (sc ? ' dans cette rubrique' + (cur.total ? ' (' + cur.total + ' dans les autres : touche « Tout »)' : '') : '') + '. Essaie un seul mot, en français, en romaji ou en japonais.</div>';
    results.forEach(function (it, k) {
      html += '<button class="res" data-k="' + k + '"><span class="path">' + esc(it.path) + '</span><span class="snip">' + snippet(it, cur.flat) + '</span></button>';
    });
    if (hits.length > shown) html += '<button type="button" class="res more" data-more="1">Afficher plus (' + (hits.length - shown) + ')</button>';
    box.innerHTML = html; setRes(true);
  }
  function run() {
    var raw = q.value.trim(); clr.hidden = !raw; shown = 40;
    if (!raw) { cur = null; setRes(false); box.innerHTML = ''; renderScopes(null); renderHist(); return; }
    renderHist();
    var toks = fold(raw).replace(/\b(?:l|d|j|qu|c|s|t|m)['’]/g, '').split(/\s+/).filter(Boolean).map(altTok);
    var hits = search(toks), fixed = '';
    if (!hits.length) {
      var t2 = toks.map(function (alts) { var base = alts[0]; if (base.length < 4 || !/^[a-z0-9]+$/.test(base)) return alts; var f = fixTok(base); return f.length ? alts.concat(f) : alts; });
      var h2 = search(t2);
      if (h2.length) { hits = h2; toks = t2; fixed = 1; }
    }
    var counts = {}; hits.forEach(function (h) { counts[h.it.sj] = (counts[h.it.sj] || 0) + 1; });
    var sc = ST.ss || '', all = hits.length;
    if (sc) hits = hits.filter(function (h) { return h.it.sj === sc; });
    var flat = []; toks.forEach(function (t) { t.forEach(function (x) { flat.push(x); }); });
    cur = { hits: hits, raw: raw, flat: flat, fixed: fixed, total: all - hits.length, counts: counts };
    renderScopes(counts); paint();
  }
  function go(it) {
    remember(q.value); q.blur();
    navOpen(it.sec, it.sub);
    var el = it.el; setTimeout(function () { el.classList.remove('flash'); void el.offsetWidth; el.classList.add('flash'); el.scrollIntoView({ block: 'center' }); }, 120);
    setTimeout(function () { el.classList.remove('flash'); }, 2800);
  }
  box.addEventListener('click', function (e) { var b = e.target.closest('.res'); if (!b) return; if (b.dataset.more) { shown += 40; paint(); return; } go(results[+b.dataset.k]); });
  scopesEl.addEventListener('click', function (e) { var b = e.target.closest('.chip'); if (!b) return; ST.ss = b.dataset.sc || ''; save(); shown = 40; if (q.value.trim()) run(); else renderScopes(null); });
  var t; q.addEventListener('input', function () { clearTimeout(t); t = setTimeout(run, 90); });
  q.addEventListener('keydown', function (e) { if (e.key === 'Enter' && results[0]) go(results[0]); if (e.key === 'Escape') { q.value = ''; run(); } });
  clr.addEventListener('click', function () { q.value = ''; run(); q.focus(); });
  document.getElementById('shist').addEventListener('click', function (e) {
    var b = e.target.closest('button'); if (!b) return;
    if (b.dataset.x) { ST.sh = []; save(); renderHist(); return; }
    q.value = (ST.sh || [])[+b.dataset.w] || ''; run(); q.focus();
  });
  // thème : clair (défaut) / sombre / auto
  var root = document.documentElement, meta = document.querySelector('meta[name="theme-color"]'), seg = document.getElementById('seg-theme');
  function getPref() { try { return localStorage.getItem('jp-theme') || 'light'; } catch (e) { return 'light'; } }
  function applyTheme(p) {
    if (p === 'auto') root.removeAttribute('data-theme'); else root.setAttribute('data-theme', p);
    seg.querySelectorAll('button').forEach(function (b) { b.setAttribute('aria-pressed', b.dataset.t === p ? 'true' : 'false'); });
    var dark = p === 'dark' || (p === 'auto' && matchMedia('(prefers-color-scheme: dark)').matches);
    if (meta) meta.setAttribute('content', dark ? '#17130f' : '#1c1510');
  }
  applyTheme(getPref());
  seg.addEventListener('click', function (e) { var b = e.target.closest('button'); if (!b) return; try { localStorage.setItem('jp-theme', b.dataset.t); } catch (er) {} applyTheme(b.dataset.t); });

  // bouton retour du téléphone : ferme la surcouche ouverte au lieu de quitter la page
  var BK = [], bkSkip = 0;
  function bkPush(fn) { BK.push(fn); try { history.pushState({ bk: 1 }, ''); } catch (e) {} }
  function bkClose(fn) {
    fn(); var i = BK.lastIndexOf(fn); if (i < 0) return;
    var top = i === BK.length - 1; BK.splice(i, 1);
    if (top) { bkSkip++; try { history.back(); } catch (e) { bkSkip--; } }
  }
  window.addEventListener('popstate', function () {
    if (bkSkip > 0) { bkSkip--; return; }
    var fn = BK.pop(); if (fn) { fn(); return; }
    if (NAV.length > 1) { NAV.pop(); pushed = Math.max(0, pushed - 1); navRender(); }
  });
  // menu latéral
  var drawer = document.getElementById('drawer'), menuBtn = document.getElementById('menu');
  function openNav(focusSearch) {
    if (!document.body.classList.contains('nav-open')) bkPush(hideNav);
    renderHist(); document.body.classList.add('nav-open'); drawer.setAttribute('aria-hidden', 'false'); menuBtn.setAttribute('aria-expanded', 'true');
    if (focusSearch) setTimeout(function () { q.focus(); }, 240);
  }
  function closeNav() { bkClose(hideNav); }
  function hideNav() { document.body.classList.remove('nav-open'); drawer.setAttribute('aria-hidden', 'true'); menuBtn.setAttribute('aria-expanded', 'false'); q.blur(); }
  menuBtn.addEventListener('click', function () { document.body.classList.contains('nav-open') ? closeNav() : openNav(false); });
  document.getElementById('dr-close').addEventListener('click', closeNav);
  document.getElementById('scrim').addEventListener('click', closeNav);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && document.body.classList.contains('nav-open')) closeNav(); });

