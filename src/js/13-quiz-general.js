  function initMix(mainEl) {
    var keys = ['kanji5', 'kanji4', 'kanji3', 'kanji2', 'kanji1', 'vocab', 'conj', 'part', 'compt', 'geo'].filter(function (k) { return MIXREG[k]; });
    if (keys.length < 2) return;
    var NS = [10, 25, 50, 100, 150, 200];
    var cfg = ST.mqc || { themes: keys.slice(), n: 25 };
    if (cfg.themes.indexOf('kanji') >= 0) cfg.themes = cfg.themes.filter(function (k) { return k !== 'kanji'; }).concat(['kanji5', 'kanji4', 'kanji3', 'kanji2', 'kanji1']);
    cfg.themes = cfg.themes.filter(function (k) { return keys.indexOf(k) >= 0; }); if (!cfg.themes.length) cfg.themes = keys.slice();
    var S = null;
    var el = document.createElement('div'); el.className = 'quiz'; el.hidden = true;
    el.innerHTML = '<div class="q-top"><button class="x" type="button" aria-label="Fermer">×</button><div class="ttl">Quiz général</div><div class="prog"></div></div><div class="q-bar"><i></i></div><div class="q-body"></div>';
    document.body.appendChild(el);
    var body = el.querySelector('.q-body'), prog = el.querySelector('.prog'), barI = el.querySelector('.q-bar i');
    var card = document.createElement('button'); card.type = 'button'; card.className = 'quizcard';
    card.innerHTML = '<span class="qc-jp">総合</span><span class="qc-t">Quiz général<small>Tous les thèmes mélangés · à la carte</small></span><span class="qc-go">›</span>';
    quizHost(mainEl).appendChild(card);
    function shuffle(a) { for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
    function hideMix() { if (S && S.cur) { S.cur.hide(); S.cur = null; } el.hidden = true; document.body.style.overflow = ''; }
    function open(v) { if (v) { if (el.hidden) bkPush(hideMix); el.hidden = false; document.body.style.overflow = 'hidden'; } else bkClose(hideMix); }
    card.addEventListener('click', function () { open(true); showSetup(); });
    el.querySelector('.x').addEventListener('click', function () { open(false); });
    function counts() { var c = {}, t = 0; cfg.themes.forEach(function (k) { c[k] = MIXREG[k].count(); t += c[k]; }); return { c: c, t: t }; }
    function chip(label, on, data, dis) { return '<button type="button" class="qchip' + (on ? ' on' : '') + '"' + (dis ? ' disabled' : '') + ' ' + data + '>' + label + '</button>'; }
    function showSetup() {
      S = null; el.querySelector('.ttl').textContent = 'Quiz général'; prog.textContent = ''; barI.style.width = '0';
      var all = {}; keys.forEach(function (k) { all[k] = MIXREG[k].count(); });
      var ct = counts(); if (cfg.n !== 0 && cfg.n > ct.t) cfg.n = 0;
      var h = '<div class="q-sec"><h4>Thèmes</h4><div class="qchips">' + keys.map(function (k) { return chip(MIXREG[k].label + ' · ' + all[k], cfg.themes.indexOf(k) >= 0, 'data-th="' + k + '"'); }).join('') + '</div></div>';
      h += '<div class="q-sec"><h4>Nombre de questions</h4><div class="qchips">' + NS.filter(function (n) { return n <= ct.t; }).map(function (n) { return chip(n, cfg.n === n, 'data-n="' + n + '"'); }).join('') + chip('Tout · ' + ct.t, cfg.n === 0, 'data-n="0"', ct.t === 0) + '</div></div>';
      h += '<p class="conj-note">Les questions sont tirées au hasard dans chaque thème, avec les réglages par défaut (tous les types, tous les niveaux). Chaque réponse compte dans les statistiques du quiz d’origine.</p>';
      h += '<button type="button" class="qgo" id="m-go"' + (ct.t ? '' : ' disabled') + '>Lancer · ' + (cfg.n === 0 ? ct.t : Math.min(cfg.n, ct.t)) + ' questions</button>';
      body.innerHTML = h;
    }
    function persist() { ST.mqc = cfg; save(); }
    function plan() {
      var ct = counts(), N = cfg.n === 0 ? ct.t : Math.min(cfg.n, ct.t), left = {}, quota = {}, act = cfg.themes.slice(), rem = N;
      cfg.themes.forEach(function (k) { left[k] = ct.c[k]; quota[k] = 0; });
      while (rem > 0 && act.length) {
        var per = Math.max(1, Math.floor(rem / act.length)), next = [];
        act.forEach(function (k) { var g = Math.min(per, left[k], rem); quota[k] += g; left[k] -= g; rem -= g; if (left[k] > 0) next.push(k); });
        act = next;
      }
      var items = [];
      cfg.themes.forEach(function (k) { if (quota[k] > 0) MIXREG[k].make(quota[k]).forEach(function (it) { items.push({ k: k, it: it }); }); });
      return shuffle(items);
    }
    function start() {
      var items = plan(); if (!items.length) return;
      S = { items: items, i: 0, ok: 0, res: {}, cur: null, t0: Date.now() };
      cfg.themes.forEach(function (k) { S.res[k] = { n: 0, ok: 0 }; });
      step();
    }
    var hooks = {
      next: function (ok) { var q = S.items[S.i], r = S.res[q.k]; r.n++; if (ok) { r.ok++; S.ok++; } S.i++; step(); },
      quit: function () { open(false); }
    };
    function step() {
      if (S.i >= S.items.length) return finish();
      var q = S.items[S.i], prev = S.cur, m = MIXREG[q.k]; S.cur = m;
      m.show(q.it, hooks, S.i + 1, S.items.length);
      if (prev && prev !== m && !(prev.grp && prev.grp === m.grp)) prev.hide();
    }
    function finish() {
      if (S.cur) { S.cur.hide(); S.cur = null; }
      var n = S.items.length, secs = Math.round((Date.now() - S.t0) / 1000), pct = Math.round(S.ok / n * 100);
      prog.textContent = ''; barI.style.width = '100%';
      var rows = Object.keys(S.res).filter(function (k) { return S.res[k].n; }).map(function (k) { var r = S.res[k], p = Math.round(r.ok / r.n * 100); return '<div class="qs-row"><div class="qs-l"><span>' + MIXREG[k].label + '</span><span><b>' + r.ok + ' / ' + r.n + '</b> · ' + p + ' %</span></div><div class="qs-bar"><i style="width:' + p + '%"></i></div></div>'; }).join('');
      body.innerHTML = '<div class="q-score"><div class="n">' + S.ok + '<small> / ' + n + '</small></div><div class="p">' + pct + ' % · ' + Math.floor(secs / 60) + ' min ' + (secs % 60) + ' s</div></div><h4 class="q-h">Par thème</h4><div class="qs-types">' + rows + '</div>' +
        '<div class="q-end"><button type="button" class="qgo" id="m-again">Rejouer</button><button type="button" class="mini" id="m-new">Nouveau quiz</button><button type="button" class="mini" id="m-close">Fermer</button></div>';
      body.scrollTop = 0;
    }
    body.addEventListener('click', function (e) {
      var b = e.target.closest('button'); if (!b || b.disabled) return;
      if (b.dataset.th) { var i = cfg.themes.indexOf(b.dataset.th); if (i >= 0) { if (cfg.themes.length > 1) cfg.themes.splice(i, 1); } else cfg.themes.push(b.dataset.th); persist(); showSetup(); }
      else if (b.dataset.n !== undefined) { cfg.n = +b.dataset.n; persist(); showSetup(); }
      else if (b.id === 'm-go' || b.id === 'm-again') start();
      else if (b.id === 'm-new') showSetup();
      else if (b.id === 'm-close') open(false);
    });
  }
