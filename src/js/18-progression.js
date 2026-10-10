
  /* ═══════════ PAGE « MA PROGRESSION » ═══════════ */
  var RANGES = { '7': '7 derniers jours', '15': '15 derniers jours', '30': '30 derniers jours', 'month': 'Mois en cours' };
  function rangeKey() { return RANGES[ST.range] ? ST.range : '7'; }
  function rangeTitle() { var k = rangeKey(); return k === 'month' ? 'Mois de ' + new Date().toLocaleDateString('fr-FR', { month: 'long' }) : RANGES[k]; }
  function buildDays(H) {
    var DN = ['dim', 'lun', 'mar', 'mer', 'jeu', 'ven', 'sam'], k = rangeKey(), now = new Date(), list = [], out = { days: [], mx: 1, n: 0, ok: 0 };
    if (k === 'month') { var last = new Date(now.getFullYear(), now.getMonth() + 1, 0).getDate(); for (var d = 1; d <= last; d++) list.push({ t: new Date(now.getFullYear(), now.getMonth(), d, 12).getTime(), f: d > now.getDate() }); }
    else { var N = +k; for (var i = N - 1; i >= 0; i--) list.push({ t: Date.now() - i * 864e5, f: false }); }
    list.forEach(function (e, idx) {
      var dt = new Date(e.t), v = e.f ? { n: 0, ok: 0 } : (H[dkey(e.t)] || { n: 0, ok: 0 });
      out.mx = Math.max(out.mx, v.n); out.n += v.n; out.ok += v.ok;
      out.days.push({ l: list.length > 8 ? String(dt.getDate()) : DN[dt.getDay()], n: v.n, ok: v.ok, f: e.f, today: !e.f && (k === 'month' ? dt.getDate() === now.getDate() : idx === list.length - 1) });
    });
    return out;
  }
  /* graphique des 7 jours : barres ou points reliés (réglage ST.chart) */
  function chartHtml(days, mx) {
    var N = days.length, dense = N > 8, step = N > 20 ? 5 : N > 8 ? 3 : 1;
    function lab(d, i, cls) { var show = !dense || i % step === 0 || i === N - 1 && (N - 1) % step > 1 || d.today; return '<span class="pg-l' + (cls || '') + '">' + (show ? d.l : '') + '</span>'; }
    if (ST.chart !== 'line') return '<div class="pg-bars' + (dense ? ' dense' : '') + '">' + days.map(function (d, i) { return '<div class="pg-d' + (d.today ? ' today' : '') + (d.f ? ' fut' : '') + '"><span class="pg-n">' + (d.n && (!dense || d.today || d.n === mx) ? d.n : '') + '</span><div class="pg-col"><i style="height:' + (d.n * 78 / mx) + '%"></i></div>' + lab(d, i, '') + '</div>'; }).join('') + '</div>';
    var pt = days.map(function (d, i) { return { x: (i + .5) * 100 / N, y: 100 - d.n * 78 / mx, d: d, i: i }; }), live = pt.filter(function (q) { return !q.d.f; });
    return '<div class="pg-line' + (dense ? ' dense' : '') + '"><div class="pg-plot"><svg viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true"><polyline vector-effect="non-scaling-stroke" points="' + live.map(function (q) { return q.x.toFixed(1) + ',' + q.y.toFixed(1); }).join(' ') + '"/></svg>' +
      live.map(function (q) { return '<span class="pg-pt' + (q.d.today ? ' today' : '') + '" style="left:' + q.x.toFixed(1) + '%;top:' + q.y.toFixed(1) + '%"></span>' + (q.d.n && (!dense || q.d.today || q.d.n === mx) ? '<span class="pg-pn" style="left:' + q.x.toFixed(1) + '%;top:' + q.y.toFixed(1) + '%">' + q.d.n + '</span>' : ''); }).join('') + '</div>' +
      '<div class="pg-axis">' + pt.map(function (q) { return lab(q.d, q.i, q.d.today ? ' today' : ''); }).join('') + '</div></div>';
  }
  function statsHtml() {
    function J(id) { try { return JSON.parse(document.getElementById(id).textContent); } catch (e) { return null; } }
    var KD = J('kanji-data') || [], VD = J('vocab-data') || [], GD = J('grammar-data') || { verbs: [], parts: [] }, MD = J('map-data') || { p: [] }, CD = J('counter-data') || { counters: [] };
    var vById = {}; VD.forEach(function (x) { vById[x.i] = x; });
    var QZ = [
      { n: 'Kanji', ic: '漢', it: ST.kq, s: ST.kqs, tot: KD.length },
      { n: 'Vocabulaire & phrases', ic: '語', it: ST.vq, s: ST.vqs, tot: VD.length },
      { n: 'Conjugaison', ic: '動', it: ST.gq_c, s: ST.gqs_c, tot: 0 },
      { n: 'Particules', ic: '助', it: ST.gq_p, s: ST.gqs_p, tot: GD.parts.length },
      { n: 'Compteurs', ic: '数', it: ST.cq, s: ST.cqs, tot: 0 },
      { n: 'Géographie', ic: '地', it: ST.gq, s: ST.gqs, tot: MD.p.length + (MD.ids ? MD.ids.length : 0) + (J('geo-words') || []).length }
    ];
    var tq = 0, tok = 0;
    var cards = QZ.map(function (z) {
      var it = z.it || {}, ks = Object.keys(it), seen = ks.length, mast = 0, wr = 0;
      ks.forEach(function (k) { var v = it[k]; if (v.w) wr++; else if (v.st >= 3) mast++; });
      var q = (z.s && z.s.q) || 0, ok = (z.s && z.s.ok) || 0;
      if (!z.s) { ks.forEach(function (k) { q += it[k].n || 0; ok += (it[k].n || 0) - (it[k].x || 0); }); }
      tq += q; tok += ok;
      var pct = q ? Math.round(ok * 100 / q) : 0, tot = z.tot && z.tot >= seen ? z.tot : 0;
      var den = tot || Math.max(seen, 1);
      return '<div class="pg-card"><div class="pg-h"><span class="pg-i">' + z.ic + '</span><b>' + esc(z.n) + '</b><span class="pg-p">' + (q ? pct + ' % de réussite' : 'pas encore joué') + '</span></div>' +
        '<div class="pg-bar" title="maîtrisés / à revoir / en cours"><i class="m" style="width:' + (mast * 100 / den) + '%"></i><i class="w" style="width:' + (wr * 100 / den) + '%"></i><i class="o" style="width:' + (Math.max(0, seen - mast - wr) * 100 / den) + '%"></i></div>' +
        '<div class="pg-k"><span><b>' + seen + '</b>' + (tot ? ' / ' + tot : '') + ' vus</span><span><b>' + mast + '</b> maîtrisés</span><span><b>' + wr + '</b> à revoir</span><span><b>' + q + '</b> réponses</span></div></div>';
    }).join('');
    // 7 derniers jours
    var H = ST.hist || {}, DN = ['dim', 'lun', 'mar', 'mer', 'jeu', 'ven', 'sam'], BD = buildDays(H), days = BD.days, mx = BD.mx;
    var week = chartHtml(days, mx);
    var QK = [['k', 'Kanji', '漢'], ['v', 'Vocabulaire', '語'], ['c', 'Conjugaison', '動'], ['p', 'Particules', '助'], ['n', 'Compteurs', '数'], ['g', 'Géographie', '地']];
    var detail = QK.map(function (z) {
      var QH = (ST.qh || {})[z[0]] || {}, QD = buildDays(QH), dd = QD.days, m2 = QD.mx, n7 = QD.n, ok7 = QD.ok;
      return '<div class="pg-sub"><div class="pg-h"><span class="pg-i">' + z[2] + '</span><b>' + esc(z[1]) + '</b><span class="pg-p">' + (n7 ? n7 + ' réponses · ' + Math.round(ok7 * 100 / n7) + ' %' : 'aucune sur la période') + '</span></div>' +
        '<div class="pg-week pg-mini">' + chartHtml(dd, m2) + '</div></div>';
    }).join('');
    var wk = days.reduce(function (a, d) { return a + d.n; }, 0), act = Object.keys(H).filter(function (k) { return H[k].n > 0; }).length;
    var D = dayState(), y = dkey(Date.now() - 864e5), strk = (ST.strk.last === D.d || ST.strk.last === y) ? ST.strk.n : 0;
    // points faibles (kanji + vocabulaire)
    var weak = [];
    Object.keys(ST.kq || {}).forEach(function (k) { var v = ST.kq[k]; if (v.x > 0) weak.push({ x: v.x, n: v.n, t: k, d: (KD.filter(function (z) { return z.k === k; })[0] || {}).s || '' }); });
    Object.keys(ST.vq || {}).forEach(function (k) { var v = ST.vq[k], w = vById[k]; if (v.x > 0 && w) weak.push({ x: v.x, n: v.n, t: w.jp || w.fr, d: w.jp ? w.fr : '' }); });
    weak.sort(missSort);
    var wh = weak.map(function (w) { return '<li><span class="pg-wt">' + esc(w.t) + '</span><span class="pg-wd">' + esc(w.d) + '</span><span class="pg-wx">' + w.x + '/' + w.n + ' ratés</span></li>'; });
    return '<div class="pg"><div class="pg-sum"><div><b>' + tq + '</b><small>réponses</small></div><div><b>' + (tq ? Math.round(tok * 100 / tq) : 0) + ' %</b><small>réussite</small></div><div><b>' + act + '</b><small>jours actifs</small></div><div><b>' + strk + '</b><small>série 🔥</small></div></div>' +
      '<h3 class="pg-t">' + esc(rangeTitle()) + ' <small>' + wk + ' réponses</small></h3><div class="pg-week">' + week + '</div>' +
      '<details class="pg-det"><summary>Détails par quiz</summary>' + detail + '</details>' +
      '<h3 class="pg-t">Par quiz</h3>' + cards +
      '<div class="pg-leg"><i class="m"></i> maîtrisés (3 bonnes d’affilée) <i class="w"></i> à revoir <i class="o"></i> en cours</div>' +
      '<h3 class="pg-t">Points faibles</h3>' + (wh.length ? missBlock(wh, 'pg-weak', 'ul')  : '<p class="pg-empty">Rien à signaler pour l’instant : les mots ratés apparaîtront ici.</p>') + '</div>';
  }


  /* ═══════════ PAGE « RECORDS » ═══════════ */
  /* coupes : part des éléments de la catégorie maîtrisés (3 bonnes réponses d'affilée) */
  var CUPS = [
    { n: 'Bronze', min: 10, c: '#b87333' }, { n: 'Argent', min: 25, c: '#aab2bd' },
    { n: 'Or', min: 50, c: '#e0b13a' }, { n: 'Platine', min: 80, c: '#5cc8d8' }
  ];
  function cupSvg(c, off) {
    return '<svg class="rc-cup' + (off ? ' off' : '') + '" viewBox="0 0 24 24" width="30" height="30" aria-hidden="true"><path d="M6 3h12v6a6 6 0 0 1-12 0z" fill="' + c + '" stroke="' + c + '" stroke-width="1.2" stroke-linejoin="round"/><path d="M6 5H3v2a3 3 0 0 0 3 3M18 5h3v2a3 3 0 0 1-3 3M12 15v3M9 18h6M8 21h8" fill="none" stroke="' + c + '" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  }
  function cupFor(m, tot) {
    var pct = tot ? m * 100 / tot : 0, cur = -1; CUPS.forEach(function (c, i) { if (pct >= c.min) cur = i; });
    var nx = CUPS[cur + 1];
    return { pct: pct, cur: cur >= 0 ? CUPS[cur] : null, next: nx || null, left: nx ? Math.max(1, Math.ceil(nx.min * tot / 100 - m - 1e-9)) : 0 };
  }
  function fpct(p) { return (p >= 10 || p === 0 ? String(Math.round(p)) : String(Math.round(p * 10) / 10).replace('.', ',')); }
  function recordsHtml() {
    var R = ST.rc || {}, cnt = R.cnt || {}, D = dayState(), y = dkey(Date.now() - 864e5);
    var curStrk = (ST.strk.last === D.d || ST.strk.last === y) ? ST.strk.n : 0, bestStrk = Math.max(R.bestStrk || 0, curStrk);
    var bd = R.bd || { p: 0, n: 0, d: '' }, H = ST.hist || {};
    Object.keys(H).forEach(function (k) { var v = H[k]; if (v.n >= 10) { var p = Math.round(v.ok * 1000 / v.n) / 10; if (p > bd.p || (p === bd.p && v.n > bd.n)) bd = { p: p, n: v.n, d: k }; } });
    function J(id) { try { return JSON.parse(document.getElementById(id).textContent); } catch (e) { return null; } }
    var KD = J('kanji-data') || [], VD = J('vocab-data') || [], GD = J('grammar-data') || { verbs: [], parts: [] }, MD = J('map-data') || { p: [] }, CD = J('counter-data') || { counters: [], reads: [] };
    var nC = (CD.reads || []).length; (CD.counters || []).forEach(function (c) { if (c.k !== 'つ') nC++; nC += (c.ex || []).length; });
    var nV = 0; GD.verbs.forEach(function (v) { nV += Object.keys(v.f || {}).length; });
    var T = [['k', 'Kanji', '漢', ST.kq, KD.length], ['v', 'Vocabulaire & phrases', '語', ST.vq, VD.length], ['c', 'Conjugaison', '動', ST.gq_c, nV], ['p', 'Particules', '助', ST.gq_p, GD.parts.length], ['n', 'Compteurs', '数', ST.cq, nC], ['g', 'Géographie', '地', ST.gq, MD.p.length + (MD.ids ? MD.ids.length : 0) + (J('geo-words') || []).length]];
    var tot = 0, mTot = 0, nTot = 0;
    T.forEach(function (t) { var it = t[3] || {}, m = 0; Object.keys(it).forEach(function (k) { if (!it[k].w && it[k].st >= 3) m++; }); t.m = Math.min(m, t[4]); tot += cnt[t[0]] || 0; mTot += t.m; nTot += t[4]; });
    function fd(k) { return k ? new Date(k + 'T12:00:00').toLocaleDateString('fr-FR', { day: 'numeric', month: 'short', year: 'numeric' }) : ''; }
    function fs(n) { return String(n).replace('.', ','); }
    var tc = cupFor(mTot, nTot);
    var h = '<div class="pg rc"><div class="rc-hero">' + cupSvg(tc.cur ? tc.cur.c : '#8a8378', !tc.cur) + '<div><b>' + tot.toLocaleString('fr-FR') + '</b><small>réponses au total · ' + fpct(tc.pct) + ' % maîtrisé' + (tc.cur ? ' · coupe ' + tc.cur.n.toLowerCase() : '') + '</small></div></div>';
    h += '<h3 class="pg-t">Par type de quiz <small>la coupe suit la part d’éléments maîtrisés (3 bonnes réponses d’affilée)</small></h3>';
    T.forEach(function (t) {
      var n = cnt[t[0]] || 0, c = cupFor(t.m, t[4]);
      h += '<div class="rc-row"><span class="pg-i">' + t[2] + '</span><div class="rc-m"><b>' + esc(t[1]) + '</b><small>' + fpct(c.pct) + ' % maîtrisé · ' + (c.next ? 'encore ' + c.left.toLocaleString('fr-FR') + ' pour la coupe ' + c.next.n.toLowerCase() : 'palier maximum atteint') + '</small></div><span class="rc-n">' + n.toLocaleString('fr-FR') + '</span>' + cupSvg(c.cur ? c.cur.c : '#8a8378', !c.cur) + '</div>';
    });
    h += '<div class="pg-leg rc-leg">' + CUPS.map(function (c) { return cupSvg(c.c).replace('width="30" height="30"', 'width="16" height="16"') + ' ' + c.n.toLowerCase() + ' ' + c.min + ' %'; }).join(' · ') + '</div>';
    h += '<h3 class="pg-t">Séries</h3><div class="rc-grid">' +
      '<div><b>🔥 ' + bestStrk + '</b><small>jour' + (bestStrk > 1 ? 's' : '') + ' de suite (record)</small></div>' +
      '<div><b>✔ ' + (R.bestRun || 0) + '</b><small>bonnes réponses d’affilée</small></div></div>';
    h += '<h3 class="pg-t">Meilleure journée</h3><div class="rc-grid one"><div>' + (bd.p ? '<b>' + fs(bd.p) + ' %</b><small>' + bd.n + ' réponses · ' + fd(bd.d) + '</small>' : '<b>—</b><small>joue au moins 10 questions dans la journée</small>') + '</div></div>';
    h += '<h3 class="pg-t">Rapidité <small>moyenne par question, ≥ 80 % de bonnes réponses</small></h3><div class="rc-spd">';
    SPD_N.forEach(function (N) {
      var b = (R.spd || {})[N];
      h += '<div><small>' + N + ' questions</small>' + (b ? '<b>' + fs(b.s) + ' s</b><small>' + fd(b.d) + '</small>' : '<b>—</b><small>à battre</small>') + '</div>';
    });
    h += '</div><p class="pg-empty">La rapidité se mesure sur des questions enchaînées sans pause de plus d’une minute.</p></div>';
    return h;
  }

  /* bloc commun aux écrans « Statistiques » de chaque quiz : avancement, 7 jours, tendance */
  function qsExtra(key, items, total) {
    items = items || {};
    var ks = Object.keys(items), seen = ks.length, mast = 0, wr = 0;
    ks.forEach(function (k) { var v = items[k]; if (v.w) wr++; else if (v.st >= 3) mast++; });
    var tot = total && total >= seen ? total : 0, den = tot || Math.max(seen, 1);
    var QH = (ST.qh || {})[key] || {}, DN = ['dim', 'lun', 'mar', 'mer', 'jeu', 'ven', 'sam'], days = [], mx = 1, n7 = 0, ok7 = 0, nP = 0, okP = 0;
    for (var i = 13; i >= 0; i--) {
      var t = Date.now() - i * 864e5, v = QH[dkey(t)] || { n: 0, ok: 0 };
      if (i < 7) { days.push({ l: DN[new Date(t).getDay()], n: v.n, today: i === 0 }); mx = Math.max(mx, v.n); n7 += v.n; ok7 += v.ok; } else { nP += v.n; okP += v.ok; }
    }
    var p7 = n7 ? Math.round(ok7 * 100 / n7) : null, pP = nP ? Math.round(okP * 100 / nP) : null, trend = '';
    if (p7 !== null && pP !== null) { var d = p7 - pP; trend = d > 1 ? '↗ +' + d + ' points' : d < -1 ? '↘ ' + d + ' points' : '→ stable'; trend += ' vs semaine précédente'; }
    var h = '<h4 class="q-h">Mon avancement</h4><div class="pg-card"><div class="pg-bar"><i class="m" style="width:' + (mast * 100 / den) + '%"></i><i class="w" style="width:' + (wr * 100 / den) + '%"></i><i class="o" style="width:' + (Math.max(0, seen - mast - wr) * 100 / den) + '%"></i></div>' +
      '<div class="pg-k"><span><b>' + seen + '</b>' + (tot ? ' / ' + tot : '') + ' vus</span><span><b>' + mast + '</b> maîtrisés</span><span><b>' + wr + '</b> à revoir</span>' + (tot ? '<span><b>' + Math.round(mast * 100 / tot) + ' %</b> maîtrisé</span>' : '') + '</div>' +
      '<div class="pg-leg"><i class="m"></i> maîtrisés (3 bonnes d’affilée) <i class="w"></i> à revoir <i class="o"></i> en cours</div></div>';
    h += '<h4 class="q-h">7 derniers jours' + (n7 ? ' · ' + n7 + ' réponses' + (p7 !== null ? ' · ' + p7 + ' %' : '') : '') + '</h4><div class="pg-week pg-mini">' +
      chartHtml(days, mx) + '</div>';
    if (trend) h += '<p class="pg-trend">' + trend + '</p>';
    return h;
  }

  /* classement des « plus ratés » : erreurs décroissantes, puis taux d'erreur, puis nb d'essais */
  function missSort(a, b) { return b.x - a.x || (b.x / b.n) - (a.x / a.n) || b.n - a.n; }
  /* 5 premiers visibles, le reste dans un menu déroulant */
  function missBlock(rows, cls, tag) {
    cls = cls || 'q-miss-list'; tag = tag || 'div';
    var top = '<' + tag + ' class="' + cls + '">' + rows.slice(0, 5).join('') + '</' + tag + '>';
    if (rows.length <= 5) return top;
    return top + '<details class="q-more"><summary>Voir les ' + (rows.length - 5) + ' autres</summary><' + tag + ' class="' + cls + '">' + rows.slice(5).join('') + '</' + tag + '></details>';
  }
