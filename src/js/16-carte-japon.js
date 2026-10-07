  var REGK = { hok: 'ほっかいどう', toh: 'とうほく', kan: 'かんとう', chu: 'ちゅうぶ', kin: 'きんき', chg: 'ちゅうごく', shi: 'しこく', kyu: 'きゅうしゅう・おきなわ' };
  /* ── carte du Japon ── */
  var JPM = null, JPCOL = ['#e69f00', '#56b4e9', '#009e73', '#f0e442', '#0072b2', '#d55e00', '#cc79a7', '#9a9a9a'];
  function jpm() {
    if (JPM !== null) return JPM;
    try { JPM = JSON.parse(document.getElementById('map-data').textContent); } catch (e) { JPM = false; }
    if (JPM) { JPM.by = {}; JPM.p.forEach(function (o) { JPM.by[o.n] = o; }); JPM.ids = Object.keys(JPM.reg); }
    return JPM;
  }
  var JPREG = { '北海道地方': 'hok', '東北地方': 'toh', '関東地方': 'kan', '関東': 'kan', '中部地方': 'chu', '近畿地方': 'kin', '関西': 'kin', '中国地方': 'chg', '四国地方': 'shi', '四国': 'shi', '九州地方': 'kyu', '九州': 'kyu' };
  function jpSet(jp) {
    var M = jpm(); if (!M) return null;
    if (M.by[jp]) return [jp];
    if (JPREG[jp]) return M.p.filter(function (o) { return o.r === JPREG[jp] && (jp !== '九州' || o.n !== '沖縄'); }).map(function (o) { return o.n; });
    if (jp === '本州') return M.p.filter(function (o) { return o.r !== 'hok' && o.r !== 'shi' && o.r !== 'kyu'; }).map(function (o) { return o.n; });
    return null;
  }
  function jpPaths(on, cls) {
    var M = jpm(), set = {}; (on || []).forEach(function (n) { set[n] = 1; });
    return M.p.map(function (o) { return '<path class="' + cls + (set[o.n] ? ' jm-on' : '') + '" data-n="' + o.n + '" d="' + o.d + '"/>'; }).join('');
  }
  function jpFrame(M) { var f = M.frame; return '<rect class="jm-fr" x="' + f[0] + '" y="' + f[1] + '" width="' + f[2] + '" height="' + f[3] + '"/>'; }
  function jpMiniSet(set, cls) {
    var M = jpm();
    return '<div class="' + cls + '"><svg viewBox="' + M.vb.join(' ') + '" role="img" aria-label="Carte du Japon">' + jpPaths(set, 'jm-p') + jpFrame(M) + '</svg></div>';
  }
  function jpMini(x) {
    var set = jpSet(x.jp); if (!set) return '';
    var M = jpm(), o = M.by[x.jp], line = '';
    if (o) line = '<div class="vq-reg"><b>Région</b> · ' + esc(M.reg[o.r][0]) + ' · ' + esc(M.reg[o.r][1]) + '</div>';
    return line + jpMiniSet(set, 'jm-mini');
  }
  function jpMapInit() {
    var host = document.querySelector('.jpmap-host'); if (!host || host.firstChild) return;
    var M = jpm(); if (!M) return;
    var legend = M.ids.map(function (r, i) { return '<button type="button" class="jm-chip" data-r="' + r + '"><i style="background:' + JPCOL[i] + '"></i>' + esc(M.reg[r][0]) + '</button>'; }).join('');
    var paths = M.p.map(function (o) { return '<path class="jm-p" data-n="' + o.n + '" data-r="' + o.r + '" style="fill:' + JPCOL[M.ids.indexOf(o.r)] + '" d="' + o.d + '"/>'; }).join('');
    var labels = M.ids.map(function (r) {
      var mem = M.p.filter(function (o) { return o.r === r && o.n !== '沖縄'; }), cx = 0, cy = 0;
      mem.forEach(function (o) { cx += o.c[0]; cy += o.c[1]; }); cx /= mem.length; cy /= mem.length;
      return '<text class="jm-t" x="' + cx.toFixed(0) + '" y="' + cy.toFixed(0) + '">' + esc(M.reg[r][0].split('・')[0]) + '</text>';
    }).join('');
    host.innerHTML = '<div class="jm-leg">' + legend + '</div><div class="jm-box"><svg class="jm-svg" viewBox="' + M.vb.join(' ') + '">' + paths + jpFrame(M) + '<g class="jm-lab">' + labels + '</g><text class="jm-sl" id="jm-sl" x="0" y="0"></text></svg>' +
      '<div class="jm-zb"><button type="button" data-z="in" aria-label="Zoom avant">+</button><button type="button" data-z="out" aria-label="Zoom arrière">−</button><button type="button" data-z="0" aria-label="Réinitialiser">⟲</button></div></div>' +
      '<div class="jm-card" id="jm-card"><p class="jm-hint">Touche une préfecture ou une région.</p></div>';
    var svg = host.querySelector('.jm-svg'), card = host.querySelector('#jm-card'), sl = host.querySelector('#jm-sl');
    var base = M.vb.slice(), vb = M.vb.slice(), moved = false, ptrs = {}, last = null, selR = null, selN = null;
    function setVb() { svg.setAttribute('viewBox', vb.join(' ')); svg.classList.toggle('jm-z', vb[2] < base[2] - 1); svg.style.setProperty('--lf', (vb[2] / base[2]).toFixed(3)); }
    function clamp() { vb[0] = Math.min(Math.max(vb[0], base[0]), base[0] + base[2] - vb[2]); vb[1] = Math.min(Math.max(vb[1], base[1]), base[1] + base[3] - vb[3]); }
    function toSvg(px, py) { var r = svg.getBoundingClientRect(); return [vb[0] + (px - r.left) / r.width * vb[2], vb[1] + (py - r.top) / r.height * vb[3]]; }
    function zoomAt(f, c) {
      var w = vb[2] * f; if (w > base[2]) w = base[2]; if (w < base[2] / 8) w = base[2] / 8;
      f = w / vb[2]; vb[0] = c[0] - (c[0] - vb[0]) * f; vb[1] = c[1] - (c[1] - vb[1]) * f; vb[2] = w; vb[3] *= f; clamp(); setVb();
    }
    function paint() {
      svg.querySelectorAll('.jm-p').forEach(function (p) {
        p.classList.toggle('jm-sel', p.dataset.n === selN);
        p.classList.toggle('jm-dim', !!selR && p.dataset.r !== selR);
      });
      host.querySelectorAll('.jm-chip').forEach(function (c) { c.classList.toggle('on', c.dataset.r === selR); });
      var p = selN && svg.querySelector('.jm-p[data-n="' + selN + '"]'); if (p) p.parentNode.insertBefore(p, svg.querySelector('.jm-fr'));
      if (selN) { var o = M.by[selN]; sl.textContent = selN; sl.setAttribute('x', o.c[0]); sl.setAttribute('y', o.c[1]); } else sl.textContent = '';
    }
    function showPref(n) {
      var o = M.by[n], r = M.reg[o.r]; selN = n; selR = o.r; paint();
      card.innerHTML = '<div class="jm-h"><span class="jm-k">' + esc(o.n) + '</span><span class="jm-ka">' + esc(o.k) + '</span><span class="jm-ro">' + esc(o.ro) + '</span></div>' +
        '<div class="jm-l"><b>Région</b> ' + esc(r[0]) + ' (' + esc(REGK[o.r] || '') + ') · ' + esc(r[1]) + '</div><div class="jm-l"><b>Chef-lieu</b> ' + esc(o.cap) + (o.cap !== o.capk ? ' (' + esc(o.capk) + ')' : '') + ' · ' + esc(o.capr) + '</div>' +
        '<div class="jm-l"><b>À retenir</b> ' + esc(o.sp) + '</div>' + (window.speechSynthesis ? '<button type="button" class="mini jm-say" data-t="' + esc(o.k) + '">🔊 Écouter</button>' : '');
    }
    function showReg(r) {
      selR = r; selN = null; paint(); var m = M.p.filter(function (o) { return o.r === r; });
      card.innerHTML = '<div class="jm-h"><span class="jm-k">' + esc(M.reg[r][0]) + '</span><span class="jm-ka">' + esc(REGK[r] || '') + '</span><span class="jm-ro">' + esc(M.reg[r][1]) + '</span></div>' +
        '<div class="jm-l"><b>' + m.length + ' préfecture' + (m.length > 1 ? 's' : '') + '</b></div><div class="jm-ps">' + m.map(function (o) { return '<button type="button" class="jm-pb" data-n="' + o.n + '"><span>' + esc(o.n) + '</span><small>' + esc(o.ro) + '</small></button>'; }).join('') + '</div>';
    }
    svg.addEventListener('click', function (e) { if (moved) { moved = false; return; } var p = e.target.closest && e.target.closest('.jm-p'); if (p) showPref(p.dataset.n); });
    host.addEventListener('click', function (e) {
      var t = e.target.closest('button'); if (!t) return;
      if (t.dataset.z) { if (t.dataset.z === 'in') zoomAt(.6, [vb[0] + vb[2] / 2, vb[1] + vb[3] / 2]); else if (t.dataset.z === 'out') zoomAt(1 / .6, [vb[0] + vb[2] / 2, vb[1] + vb[3] / 2]); else { vb = base.slice(); setVb(); selN = null; selR = null; paint(); card.innerHTML = '<p class="jm-hint">Touche une préfecture ou une région.</p>'; } }
      else if (t.classList.contains('jm-chip')) { if (selR === t.dataset.r && !selN) { selR = null; paint(); card.innerHTML = '<p class="jm-hint">Touche une préfecture ou une région.</p>'; } else showReg(t.dataset.r); }
      else if (t.classList.contains('jm-pb')) showPref(t.dataset.n);
      else if (t.classList.contains('jm-say')) speak([t.dataset.t]);
    });
    svg.addEventListener('wheel', function (e) { e.preventDefault(); zoomAt(e.deltaY < 0 ? .8 : 1.25, toSvg(e.clientX, e.clientY)); }, { passive: false });
    svg.addEventListener('pointerdown', function (e) { ptrs[e.pointerId] = [e.clientX, e.clientY]; last = null; moved = false; });
    svg.addEventListener('pointermove', function (e) {
      if (!ptrs[e.pointerId]) return;
      var ids = Object.keys(ptrs), prev = ptrs[e.pointerId];
      if (ids.length === 2) {
        var o = ptrs[ids.filter(function (i) { return +i !== e.pointerId; })[0]], d0 = Math.hypot(prev[0] - o[0], prev[1] - o[1]), d1 = Math.hypot(e.clientX - o[0], e.clientY - o[1]);
        ptrs[e.pointerId] = [e.clientX, e.clientY]; if (d0 > 0 && d1 > 0) { zoomAt(d0 / d1, toSvg((e.clientX + o[0]) / 2, (e.clientY + o[1]) / 2)); moved = true; }
      } else if (ids.length === 1 && svg.classList.contains('jm-z')) {
        var r = svg.getBoundingClientRect(), dx = e.clientX - prev[0], dy = e.clientY - prev[1];
        if (Math.abs(dx) + Math.abs(dy) > 0) { if (Math.abs(dx) + Math.abs(dy) > 3 || moved) { moved = true; vb[0] -= dx / r.width * vb[2]; vb[1] -= dy / r.height * vb[3]; clamp(); setVb(); ptrs[e.pointerId] = [e.clientX, e.clientY]; } }
      }
    });
    var up = function (e) { delete ptrs[e.pointerId]; }; svg.addEventListener('pointerup', up); svg.addEventListener('pointercancel', up); svg.addEventListener('pointerleave', up);
  }
