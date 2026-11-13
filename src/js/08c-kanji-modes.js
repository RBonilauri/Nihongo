  /* ═══ Listes de kanji (N5…N1) : menu « Affichage » sous le texte d'introduction ═══
     thème (liste d'origine) · lecture on · lecture kun · homophones on / kun · nombre de traits · radical · fréquence · à revoir.
     Le choix est mémorisé par niveau (ST.km). La vue alternative est construite au moment du choix, avec des copies des lignes d'origine. */
  var KMODES = [
    { id: 'theme', l: 'Par thème (actuel)', h: 'Les kanji sont rangés par thème, comme à l’origine.' },
    { id: 'on', l: 'Lecture on — ordre des kana', h: 'Regroupés par lecture on (あ → ん) : les kanji d’un même groupe sont homophones. Un kanji à plusieurs lectures apparaît sous chacune ; la lecture du groupe est surlignée.' },
    { id: 'kun', l: 'Lecture kun — ordre des kana', h: 'Regroupés par racine de la lecture kun, sans okurigana (あ(う), あ(げる) → あ). Les kanji sans lecture kun sont à la fin.' },
    { id: 'hon', l: 'Homophones on (2 kanji ou plus)', h: 'Seulement les lectures on partagées par au moins 2 kanji de cette liste — ce sont les pièges à ne pas confondre.' },
    { id: 'hkun', l: 'Homophones kun (2 kanji ou plus)', h: 'Seulement les racines kun partagées par au moins 2 kanji de cette liste.' },
    { id: 'traits', l: 'Nombre de traits', h: 'Du plus simple au plus complexe ; dans un groupe, les plus fréquents d’abord (KANJIDIC).' },
    { id: 'rad', l: 'Radical (1 à 214)', h: 'Regroupés par radical classique, dans l’ordre des 214 radicaux (rubrique Radicaux).' },
    { id: 'freq', l: 'Fréquence d’usage', h: 'Rang de fréquence dans la presse (KANJIDIC, 2 500 premiers kanji) : les plus courants d’abord.' },
    { id: 'rev', l: 'À revoir d’abord (mes erreurs)', h: 'D’après tes réponses au quiz kanji : ratés en premier, puis jamais vus, en cours, acquis.' }
  ];
  function kmHira(s) { return String(s).replace(/[ァ-ヶ]/g, function (c) { return String.fromCharCode(c.charCodeAt(0) - 96); }); }
  /* lectures d'un kanji : on = ['コウ', …] ; kun = racines sans okurigana ['あ', …] (une racine une seule fois) */
  function kmReads(y, kind) {
    var raw = kind === 'on' ? y.on : y.kun, out = [];
    String(raw || '').split(/[・･、,，\/]|\s+/).forEach(function (p) {
      var r = kind === 'on' ? p.replace(/[()（）]/g, '') : p.replace(/[(（][^)）]*[)）]/g, '');
      r = r.replace(/[-－—]/g, '').trim(); if (r && out.indexOf(r) < 0) out.push(r);
    });
    return out;
  }
  function kmPiece(p, kind) { return kind === 'on' ? p.replace(/[()（）]/g, '').trim() : p.replace(/[(（][^)）]*[)）]/g, '').trim(); }
  /* surligne dans la cellule On / Kun la lecture du groupe */
  function kmMark(cell, kind, target) {
    var parts = cell.textContent.split(/([・･、,，\/])/);
    cell.innerHTML = '<span>' + parts.map(function (p) { return kmPiece(p, kind) === target && target ? '<mark class="kmk">' + esc(p) + '</mark>' : esc(p); }).join('') + '</span>';
  }
  function kmByQ(a, b) { return (a.y.q || 9999) - (b.y.q || 9999); }
  /* groupes du mode : [{ key, title (html), rows: [{ tr, y, mark: { kind, target }, alt }] }] */
  function kmGroups(rows, mode) {
    var g = {}, order = [];
    function put(key, title, row, srt) { if (!g[key]) { g[key] = { key: key, srt: srt, title: title, rows: [] }; order.push(key); } g[key].rows.push(row); }
    var kind = mode === 'on' || mode === 'hon' ? 'on' : mode === 'kun' || mode === 'hkun' ? 'kun' : '';
    if (kind) {
      rows.forEach(function (r) {
        var rd = kmReads(r.y, kind);
        if (!rd.length) { if (kind === 'kun') put('~', 'Sans lecture kun', { tr: r.tr, y: r.y }, '￿'); return; }
        rd.forEach(function (x, i) { put(x, esc(x), { tr: r.tr, y: r.y, mark: { kind: kind, target: x }, alt: i > 0 }, kmHira(x)); });
      });
      var l = order.map(function (k) { return g[k]; });
      if (mode === 'hon' || mode === 'hkun') l = l.filter(function (z) { return z.rows.length >= 2; });
      l.forEach(function (z) { z.rows.sort(function (a, b) { return a.alt - b.alt || kmByQ(a, b); }); });
      return l.sort(function (a, b) { return a.srt < b.srt ? -1 : a.srt > b.srt ? 1 : 0; });
    }
    if (mode === 'traits') {
      rows.forEach(function (r) { var n = r.y.n || 0; put(n, n ? n + ' trait' + (n > 1 ? 's' : '') : 'Traits inconnus', { tr: r.tr, y: r.y }, n || 99); });
    } else if (mode === 'rad') {
      rows.forEach(function (r) {
        var n = r.y.r || 0, ri = n ? radInfo(r.y.rg, '') : null;
        put(n, n ? '<span class="kmrg">' + esc(r.y.rg) + '</span> ' + (ri && ri.m ? esc(ri.m) : 'radical') + ' <small>(n° ' + n + ')</small>' : 'Radical inconnu', { tr: r.tr, y: r.y }, n || 999);
      });
    } else if (mode === 'freq') {
      var B = [[100, 'Top 100'], [300, '101 – 300'], [600, '301 – 600'], [1000, '601 – 1 000'], [1500, '1 001 – 1 500'], [2500, '1 501 – 2 500'], [1e9, 'Hors des 2 500 plus fréquents']];
      rows.forEach(function (r) { var q = r.y.q || 1e9, i = 0; while (q > B[i][0]) i++; put(i, B[i][1], { tr: r.tr, y: r.y }, i); });
    } else if (mode === 'rev') {
      var T = ['À revoir (ratés au quiz)', 'Jamais vus au quiz', 'En cours', 'Acquis (3 bonnes réponses de suite)'];
      rows.forEach(function (r) { var s = ST.kq && ST.kq[r.y.k], b = !s ? 1 : s.w ? 0 : s.st >= 3 ? 3 : 2; r.x = s ? (s.x || 0) : 0; put(b, T[b], { tr: r.tr, y: r.y, x: r.x }, b); });
    }
    var out = order.map(function (k) { return g[k]; }).sort(function (a, b) { return a.srt - b.srt; });
    out.forEach(function (z) { z.rows.sort(function (a, b) { return mode === 'rev' ? (b.x - a.x) || kmByQ(a, b) : mode === 'rad' ? (a.y.n - b.y.n) || kmByQ(a, b) : kmByQ(a, b); }); });
    return out;
  }
  function kmThead(tbl) { var h = tbl.querySelector('thead'); return h ? h.outerHTML : '<thead><tr><th>Kanji</th><th>On</th><th>Kun</th><th>Sens</th><th>Mots clés</th></tr></thead>'; }
  function kmBuild(sub, mode) {
    var M = kdetMap(), rows = [], head = '';
    sub.querySelectorAll('.kview-theme table.stack-kanji').forEach(function (t) {
      head = head || kmThead(t);
      t.querySelectorAll('tbody tr').forEach(function (tr) { var y = M[tr.cells[0].textContent.trim()]; if (y) rows.push({ tr: tr, y: y }); });
    });
    var groups = kmGroups(rows, mode), frag = document.createDocumentFragment(), n = 0;
    groups.forEach(function (z) {
      var multi = z.rows.length >= 2, wrap = document.createElement('div');
      wrap.innerHTML = '<div class="section-title kmh' + (multi && (mode === 'on' || mode === 'kun') ? ' kmulti' : '') + '"><span>' + z.title + '</span><small class="kmc">' + z.rows.length + ' kanji</small></div><div class="scroll-x"><table class="particle-grid stack stack-kanji">' + head + '<tbody></tbody></table></div>';
      var tb = wrap.querySelector('tbody');
      z.rows.forEach(function (r) {
        var tr = r.tr.cloneNode(true); n++;
        if (r.mark) { var c = tr.cells[r.mark.kind === 'on' ? 1 : 2]; if (c) kmMark(c, r.mark.kind, r.mark.target); }
        if (r.alt) { tr.classList.add('kalt'); tr.cells[0].insertAdjacentHTML('beforeend', '<small class="kaltt">autre lecture</small>'); }
        tb.appendChild(tr);
      });
      while (wrap.firstChild) frag.appendChild(wrap.firstChild);
    });
    return { frag: frag, groups: groups.length, rows: n };
  }
  function kmApply(sub, mode) {
    var lv = sub.dataset.kmLv, th = sub.querySelector('.kview-theme'), alt = sub.querySelector('.kview-alt'), hint = sub.querySelector('.kmhint');
    if (alt) alt.remove();
    var m = KMODES.filter(function (x) { return x.id === mode; })[0] || KMODES[0];
    if (m.id === 'theme') { th.hidden = false; hint.textContent = m.h; }
    else {
      var b = kmBuild(sub, m.id); th.hidden = true;
      alt = document.createElement('div'); alt.className = 'kview kview-alt'; alt.appendChild(b.frag); th.after(alt);
      hint.textContent = m.h + ' · ' + b.groups + ' groupe' + (b.groups > 1 ? 's' : '') + (b.rows ? ', ' + b.rows + ' ligne' + (b.rows > 1 ? 's' : '') : '');
      if (!b.rows) alt.innerHTML = '<p class="conj-intro">Aucun kanji à afficher dans ce mode.</p>';
    }
    sub.querySelector('.kmsel').value = m.id;
    ST.km = ST.km || {}; if (m.id === 'theme') delete ST.km[lv]; else ST.km[lv] = m.id; save();
  }
  function kmodesInit() {
    document.querySelectorAll('details.sub').forEach(function (sub) {
      var sm = sub.querySelector(':scope > summary'), body = sub.querySelector(':scope > .sub-body'), intro = body && body.querySelector(':scope > .conj-intro');
      var mm = sm && /^(N[1-5]) — Liste complète/.exec(sm.textContent.trim());
      if (!mm || !intro || !body.querySelector('table.stack-kanji') || sub.dataset.kmLv) return;
      sub.dataset.kmLv = mm[1];
      var th = document.createElement('div'); th.className = 'kview kview-theme';
      while (intro.nextSibling) th.appendChild(intro.nextSibling);
      intro.after(th);
      var bar = document.createElement('div'); bar.className = 'kmode';
      bar.innerHTML = '<label class="kmlab">Affichage <select class="kmsel" aria-label="Mode d’affichage de la liste ' + mm[1] + '">' + KMODES.map(function (x) { return '<option value="' + x.id + '">' + esc(x.l) + '</option>'; }).join('') + '</select></label><div class="kmhint"></div>';
      intro.after(bar);
      bar.querySelector('.kmsel').addEventListener('change', function (e) { kmApply(sub, e.target.value); });
      bar.querySelector('.kmhint').textContent = KMODES[0].h;
      var saved = ST.km && ST.km[mm[1]]; if (saved && saved !== 'theme') kmApply(sub, saved);
    });
  }
