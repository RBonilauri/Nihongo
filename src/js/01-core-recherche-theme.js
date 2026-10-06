
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
        index.push({ el: el, path: path, sec: sec, sub: sub, text: txt, norm: fold(txt) + (el.dataset && el.dataset.ro ? ' ' + fold(el.dataset.ro) : '') });
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
  var results = [], drBody = document.getElementById('dr-body');
  function setRes(v) { box.hidden = !v; drBody.hidden = v; }
  function run() {
    var raw = q.value.trim(); clr.hidden = !raw;
    if (!raw) { setRes(false); box.innerHTML = ''; return; }
    var toks = fold(raw).split(/\s+/).filter(Boolean).map(function (t) { var k = r2k(t); return k && k !== t ? [t, k] : [t]; });
    var hits = [];
    for (var i = 0; i < index.length; i++) {
      var it = index[i], ok = true, score = 0;
      for (var j = 0; j < toks.length; j++) { var p = -1; for (var a = 0; a < toks[j].length; a++) { var pa = it.norm.indexOf(toks[j][a]); if (pa >= 0 && (p < 0 || pa < p)) p = pa; } if (p < 0) { ok = false; break; } score += p === 0 ? 3 : 1; }
      if (!ok) continue;
      if (it.el.tagName === 'SUMMARY' || it.el.classList.contains('section-title')) score += 4;
      score -= Math.min(it.text.length, 400) / 200;
      hits.push({ it: it, s: score });
    }
    hits.sort(function (a, b) { return b.s - a.s; });
    var flat = []; toks.forEach(function (t) { t.forEach(function (x) { flat.push(x); }); });
    results = hits.slice(0, 60).map(function (h) { return h.it; });
    var html = '<div class="count">' + hits.length + ' résultat' + (hits.length > 1 ? 's' : '') + (hits.length > 60 ? ' (60 affichés)' : '') + '</div>';
    if (!results.length) html += '<div class="empty">Aucun résultat pour « ' + esc(raw) + ' ». Essaie un seul mot, en français ou en japonais.</div>';
    results.forEach(function (it, k) {
      html += '<button class="res" data-k="' + k + '"><span class="path">' + esc(it.path) + '</span><span class="snip">' + snippet(it, flat) + '</span></button>';
    });
    box.innerHTML = html; setRes(true);
  }
  function go(it) {
    setRes(false); closeNav();
    setTimeout(function () {
      navOpen(it.sec, it.sub);
      var el = it.el; setTimeout(function () { el.classList.remove('flash'); void el.offsetWidth; el.classList.add('flash'); el.scrollIntoView({ block: 'center' }); }, 80);
      setTimeout(function () { el.classList.remove('flash'); }, 2600);
    }, 160);
  }
  box.addEventListener('click', function (e) { var b = e.target.closest('.res'); if (b) go(results[+b.dataset.k]); });
  var t; q.addEventListener('input', function () { clearTimeout(t); t = setTimeout(run, 90); });
  q.addEventListener('focus', function () { if (q.value.trim() && results.length) setRes(true); });
  q.addEventListener('keydown', function (e) { if (e.key === 'Enter' && results[0]) go(results[0]); if (e.key === 'Escape') { q.value = ''; run(); } });
  clr.addEventListener('click', function () { q.value = ''; run(); q.focus(); });
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
    document.body.classList.add('nav-open'); drawer.setAttribute('aria-hidden', 'false'); menuBtn.setAttribute('aria-expanded', 'true');
    if (focusSearch) setTimeout(function () { q.focus(); }, 240);
  }
  function closeNav() { bkClose(hideNav); }
  function hideNav() { document.body.classList.remove('nav-open'); drawer.setAttribute('aria-hidden', 'true'); menuBtn.setAttribute('aria-expanded', 'false'); q.blur(); }
  menuBtn.addEventListener('click', function () { document.body.classList.contains('nav-open') ? closeNav() : openNav(false); });
  document.getElementById('dr-close').addEventListener('click', closeNav);
  document.getElementById('scrim').addEventListener('click', closeNav);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && document.body.classList.contains('nav-open')) closeNav(); });

