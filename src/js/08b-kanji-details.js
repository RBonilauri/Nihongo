  /* ═══ « Détails » des kanji d'une réponse (commun à tous les quiz) ═══ */
  var KDMAP = null;
  function kdetBind(m) { KDMAP = m; }
  function kdetMap() {
    if (!KDMAP) {
      KDMAP = {};
      try { JSON.parse(document.getElementById('kanji-data').textContent).forEach(function (x) { x.s = (x.s || '').replace(/\s*[(（][^)）]*[぀-鿿][^)）]*[)）]/g, '').trim(); KDMAP[x.k] = x; }); } catch (e) {}
    }
    return KDMAP;
  }
  function kdetParts(cell) { return String(cell || '').split(/[・･]/).map(function (p) { return p.replace(/[()（）]/g, '').trim(); }).filter(Boolean); }
  function kdetSay(y) { return kdetParts(y.on).concat(kdetParts(y.kun)); }
  function kdetSpk(y) { return '<button type="button" class="qsay2 kspk" aria-label="Écouter les lectures on et kun" title="Écouter" data-say=\'' + esc(JSON.stringify(kdetSay(y))) + '\'>🔊</button>'; }
  /* « Mots » : liste rangée (mot · lecture · sens) */
  function kdetWords(y) {
    var l = (y.kw || []).slice(0, 4); if (!l.length) return '';
    return '<div class="fbwl"><b>Mots</b>' + l.map(function (w) { return '<div class="fbwr"><span class="fbwj">' + esc(w[0]) + '</span><span class="fbwy">' + esc(w[1]) + '</span><span class="fbwm">' + esc(w[2]) + '</span></div>'; }).join('') + '</div>';
  }
  /* « Composants » : menu déroulant radical + éléments (source CJKVI-IDS / KANJIDIC2), '' s'il n'y a rien */
  function kdetComp(y) {
    var cp = y.cp; if (!cp || (!cp[0] && !cp[1])) return '';
    var M = kdetMap();
    function one(c, r) { var m = M[c] && M[c].s ? M[c].s.split(/[,;，、]/)[0].trim() : ''; return '<span class="fbcc' + (r ? ' fbcrad' : '') + '"' + (r ? ' title="Radical"' : '') + '><b>' + esc(c) + '</b>' + (m ? '<i>' + esc(m) + '</i>' : '') + '</span>'; }
    return '<details class="fbc"><summary>Composants</summary>' + (cp[0] && cp[1].indexOf(cp[0]) < 0 ? '<div class="fbcr"><span class="fbcl">Radical</span>' + one(cp[0]) + '</div>' : '') + (cp[1] ? '<div class="fbcr"><span class="fbcl">' + 'Éléments' + '</span>' + cp[1].split('').map(function (c) { return one(c, c === cp[0]); }).join('<span class="fbcp">+</span>') + '</div>' : '') + '</details>';
  }
  /* HTML de la rubrique déroulante pour les kanji de `text` (hors `skip`), '' s'il n'y en a aucun */
  function kdetHtml(text, skip) {
    var M = kdetMap(), seen = {}, oth = String(text || '').split('').filter(function (c) { if (c === skip || seen[c] || !M[c]) return false; return (seen[c] = 1); }).slice(0, 12);
    if (!oth.length) return '';
    return '<details class="fbd"><summary>Détails · ' + (skip ? (oth.length > 1 ? 'les autres kanji' : 'l’autre kanji') : (oth.length > 1 ? 'les kanji' : 'le kanji')) + ' (' + esc(oth.join(' ')) + ')</summary>' + oth.map(function (c) {
      var y = M[c];
      return '<div class="fbd-k"><div class="fbkr"><div class="fbk">' + esc(y.k) + '</div><span class="lvp lv-' + esc(y.l) + '">' + esc(y.l) + '</span>' + kdetSpk(y) + '</div><div class="fbi"><div><b>On</b> ' + esc(y.on || '—') + '</div><div><b>Kun</b> ' + esc(y.kun || '—') + '</div><div><b>Sens</b> ' + esc(y.s) + '</div>' + '</div>' + kdetComp(y) + kdetWords(y) + '</div>';
    }).join('') + '</details>';
  }
  /* ajoute la rubrique à un encadré de correction (.q-fb) des quiz hors kanji, d'après les kanji de la réponse affichée */
  function kdetAdd(host) {
    var fb = host && host.querySelector('.q-fb'); if (!fb || fb.querySelector('.fbd')) return;
    var c = fb.cloneNode(true); c.querySelectorAll('.fbh,.fbb,.vq-ex,.jm-mini,.vq-tr,.cq-row,.cq-det,.fbd').forEach(function (n) { n.remove(); });
    var h = kdetHtml(c.textContent, ''), bar = fb.querySelector('.fbb');
    if (h && bar) bar.insertAdjacentHTML('beforebegin', h);
  }
  document.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('.qsay2'); if (!b) return;
    try { speak(JSON.parse(b.dataset.say)); } catch (x) {}
  });
