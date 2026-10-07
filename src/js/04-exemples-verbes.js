  /* ── phrases d’exemple des verbes courants : présent + un temps tiré au hasard ── */
  var EX_LB = { pres: 'Présent', neg: 'Négatif', pc: 'Passé', pcneg: 'Passé négatif', imp: 'Passé', impneg: 'Passé négatif', en: 'En cours', des: 'Souhait' };
  function exRow(rows, name) { for (var i = 0; i < rows.length; i++) if (rows[i][0] === name) return rows[i]; return null; }
  function exJp(rows, tense, opt) {
    var po = exRow(rows, 'Poli'), pp = exRow(rows, 'Poli, passé'), en = exRow(rows, 'En cours (〜ている)'), de = exRow(rows, 'Envie (〜たい)');
    var teI = en && en[1] !== '—' ? en[1].slice(0, -1) : null;           // forme en て + い (ている sans る)
    if (tense === 'pres') return /T|U/.test(opt) && teI ? teI + 'ます' : po[1];
    if (tense === 'neg') return /U/.test(opt) && teI ? teI + 'ません' : po[2];
    if (tense === 'pc' || tense === 'imp') return pp[1];
    if (tense === 'pcneg' || tense === 'impneg') return pp[2];
    if (tense === 'en') return teI ? teI + 'ます' : null;
    if (tense === 'des') return de && de[1] !== '—' ? de[1] + 'です' : null;
    return null;
  }
  function exTenses(d, ex, rows) {
    var opt = ex[6] || '', je = !ex[4], P = /P/.test(opt), out = ['neg', P ? 'imp' : 'pc', P ? 'impneg' : 'pcneg'];
    if (!/[ETU]/.test(opt) && exJp(rows, 'en', opt)) out.push('en');
    if (!/D/.test(opt) && je && exJp(rows, 'des', opt)) out.push('des');
    return out.filter(function (t) { return FRV.sent(ex[2], ex[3], ex[5], ex[4], t) && exJp(rows, t, opt); });
  }
  function exLine(ex, rowsK, rowsR, tense) {
    var opt = ex[6] || '', jp = ex[0] + exJp(rowsK, tense, opt), fr = FRV.sent(ex[2], ex[3], ex[5], ex[4], tense);
    var kana = rowsR ? ex[1] + exJp(rowsR, tense, opt) : ex[1] + exJp(rowsK, tense, opt);
    var sk = /[一-鿿]/.test(jp) && kana !== jp ? '<span class="ex-k">' + esc(kana) + '。</span>' : '';
    return '<div class="ex-s"><b class="ex-t">' + EX_LB[tense] + '</b><span class="ex-jp">' + esc(jp) + '。</span>' + sk + '<span class="ex-fr">' + esc(fr) + '</span></div>';
  }
  function exFill(d) {
    var b = d.querySelector('.exb'); if (!b) return;
    var ex, ex2 = null; try { ex = JSON.parse(d.dataset.ex); if (d.dataset.ex2) ex2 = JSON.parse(d.dataset.ex2); } catch (e) { return; }
    var k = d.dataset.k, ka = d.dataset.ka, ty = d.dataset.t, rows = cjForms(k, ty, false), rowsR = k === ka ? null : cjForms(ka, ty, true);
    var f2 = ex2 || ex;                                         // 2e phrase : autre sens si disponible
    var pool = exTenses(d, f2, rows), last = d._last, pick = pool.filter(function (t) { return t !== last; });
    if (!pick.length) pick = pool;
    var t = pick.length ? pick[Math.floor(Math.random() * pick.length)] : null; d._last = t;
    var h = exLine(ex, rows, rowsR, 'pres') + (t ? exLine(f2, rows, rowsR, t) : '');
    if (pool.length > 1) h += '<button type="button" class="mini ex-more">↻ Autre temps</button>';
    b.innerHTML = h;
  }
  document.addEventListener('toggle', function (e) { var d = e.target; if (d.matches && d.matches('details.exd') && d.open) exFill(d); }, true);
  document.addEventListener('click', function (e) { var b = e.target.closest && e.target.closest('.ex-more'); if (b) { e.preventDefault(); exFill(b.closest('details.exd')); } });
