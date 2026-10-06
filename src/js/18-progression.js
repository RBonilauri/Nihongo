
  /* ═══════════ PAGE « MA PROGRESSION » ═══════════ */
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
      { n: 'Géographie', ic: '地', it: ST.gq, s: ST.gqs, tot: MD.p.length }
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
    var days = [], mx = 1, H = ST.hist || {}, DN = ['dim', 'lun', 'mar', 'mer', 'jeu', 'ven', 'sam'];
    for (var i = 6; i >= 0; i--) { var t = Date.now() - i * 864e5, k = dkey(t), v = H[k] || { n: 0, ok: 0 }; mx = Math.max(mx, v.n); days.push({ l: DN[new Date(t).getDay()], n: v.n, ok: v.ok, today: i === 0 }); }
    var week = days.map(function (d) { return '<div class="pg-d' + (d.today ? ' today' : '') + '"><span class="pg-n">' + (d.n || '') + '</span><div class="pg-col"><i style="height:' + (d.n * 100 / mx) + '%"></i></div><span class="pg-l">' + d.l + '</span></div>'; }).join('');
    var wk = days.reduce(function (a, d) { return a + d.n; }, 0), act = Object.keys(H).filter(function (k) { return H[k].n > 0; }).length;
    var D = dayState(), y = dkey(Date.now() - 864e5), strk = (ST.strk.last === D.d || ST.strk.last === y) ? ST.strk.n : 0;
    // points faibles (kanji + vocabulaire)
    var weak = [];
    Object.keys(ST.kq || {}).forEach(function (k) { var v = ST.kq[k]; if (v.x > 0) weak.push({ x: v.x, n: v.n, t: k, d: (KD.filter(function (z) { return z.k === k; })[0] || {}).s || '' }); });
    Object.keys(ST.vq || {}).forEach(function (k) { var v = ST.vq[k], w = vById[k]; if (v.x > 0 && w) weak.push({ x: v.x, n: v.n, t: w.jp || w.fr, d: w.jp ? w.fr : '' }); });
    weak.sort(missSort);
    var wh = weak.map(function (w) { return '<li><span class="pg-wt">' + esc(w.t) + '</span><span class="pg-wd">' + esc(w.d) + '</span><span class="pg-wx">' + w.x + '/' + w.n + ' ratés</span></li>'; });
    return '<div class="pg"><div class="pg-sum"><div><b>' + tq + '</b><small>réponses</small></div><div><b>' + (tq ? Math.round(tok * 100 / tq) : 0) + ' %</b><small>réussite</small></div><div><b>' + act + '</b><small>jours actifs</small></div><div><b>' + strk + '</b><small>série 🔥</small></div></div>' +
      '<h3 class="pg-t">7 derniers jours <small>' + wk + ' réponses</small></h3><div class="pg-week">' + week + '</div>' +
      '<h3 class="pg-t">Par quiz</h3>' + cards +
      '<div class="pg-leg"><i class="m"></i> maîtrisés (3 bonnes d’affilée) <i class="w"></i> à revoir <i class="o"></i> en cours</div>' +
      '<h3 class="pg-t">Points faibles</h3>' + (wh.length ? missBlock(wh, 'pg-weak', 'ul')  : '<p class="pg-empty">Rien à signaler pour l’instant : les mots ratés apparaîtront ici.</p>') + '</div>';
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
      days.map(function (d) { return '<div class="pg-d' + (d.today ? ' today' : '') + '"><span class="pg-n">' + (d.n || '') + '</span><div class="pg-col"><i style="height:' + (d.n * 100 / mx) + '%"></i></div><span class="pg-l">' + d.l + '</span></div>'; }).join('') + '</div>';
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
