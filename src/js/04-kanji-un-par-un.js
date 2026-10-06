  /* ── menu « Kanji » : sens de chaque kanji d’un mot, un par un ── */
  var KJR = {}, KJM = null;
  function kjMap() {
    if (KJM) return KJM; KJM = {};
    try { JSON.parse(document.getElementById('kanji-gloss').textContent, function (k, v) { if (k && typeof v === 'string') KJM[k] = v; return v; }); } catch (e) {}
    try { JSON.parse(document.getElementById('kanji-data').textContent).forEach(function (x) { KJM[x.k] = x.s; if (x.on || x.kun) KJR[x.k] = [x.on, x.kun].filter(Boolean).join('  ·  '); }); } catch (e) {}
    return KJM;
  }
  function kjFill(d) {
    var b = d.querySelector('.kjb'); if (!b || b.firstChild) return;
    var M = kjMap(), seen = {}, h = '';
    (d.dataset.w.match(/[一-鿿]/g) || []).forEach(function (c) { if (seen[c]) return; seen[c] = 1; h += '<div class="kj-r"><b class="kj-c">' + c + '</b><span class="kj-t"><span class="kj-m">' + esc(M[c] || '—') + '</span>' + (KJR[c] ? '<span class="kj-y">' + esc(KJR[c]) + '</span>' : '') + '</span></div>'; });
    b.innerHTML = h;
  }
  document.addEventListener('toggle', function (e) { var d = e.target; if (d.matches && d.matches('details.kjd') && d.open) kjFill(d); }, true);
