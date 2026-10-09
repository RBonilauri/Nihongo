  /* ═══════════ QUIZ KANJI ═══════════ */
  var QT = [
    { id: 'k2s', label: 'Kanji → sens', short: 'Sens' },
    { id: 's2k', label: 'Sens → kanji', short: 'Kanji' },
    { id: 'k2on', label: 'Kanji → lecture On', short: 'On' },
    { id: 'k2kun', label: 'Kanji → lecture Kun', short: 'Kun' },
    { id: 'w2r', label: 'Mot → lecture', short: 'Mot' }
  ];
  var WT = ['w2r'], WMAX = 8;
  var QPRESETS = [
    { label: 'Tout', types: ['k2s', 's2k', 'k2on', 'k2kun', 'w2r'] },
    { label: 'Mots', types: ['w2r'] },
    { label: 'Sans les mots', types: ['k2s', 's2k', 'k2on', 'k2kun'] },
    { label: 'Lectures', types: ['k2on', 'k2kun', 'w2r'] },
    { label: 'Sens', types: ['k2s', 's2k'] }
  ];
  var QN = [10, 25, 50, 100, 150, 200];
  function initQuiz(mainEl) {
    var KD = []; try { KD = JSON.parse(document.getElementById('kanji-data').textContent); } catch (e) {}
    KD.forEach(function (x) { x.s = (x.s || "").replace(/\s*[(（][^)）]*[\u3040-\u9fff][^)）]*[)）]/g, "").trim(); });// le mot japonais entre parenthèses trahirait la réponse
    if (!KD.length) return;
    var byK = {}; KD.forEach(function (x) { byK[x.k] = x; });
    /* mots utiles : on complète les mots de chaque kanji avec ceux du vocabulaire (lecture + traduction) */
    try {
      var VD = JSON.parse(document.getElementById('vocab-data').textContent), HKJ = /[一-鿿々]/;
      VD.forEach(function (v) {
        if (!HKJ.test(v.jp) || v.jp.length > 6 || v.jp.length < 2 || /[。？！、 ・\/]/.test(v.jp) || !v.kk || v.kk === v.jp) return;
        var w = [v.jp, v.kk.split('・')[0], noJpHint(v.fr)];
        if (!w[2]) return;
        v.jp.split('').filter(function (ch, i, a) { return a.indexOf(ch) === i && byK[ch]; }).forEach(function (ch) {
          var kw = byK[ch].kw; if (kw.length < 8 && !kw.some(function (z) { return z[0] === w[0]; })) kw.push(w);
        });
      });
    } catch (e) {}
    var cfg = ST.kqc || { lv: 'N5', types: QT.map(function (t) { return t.id; }), n: 25, wrong: false };
    cfg.types = cfg.types.filter(function (t) { return QT.some(function (z) { return z.id === t; }); });
    if (!cfg.types.length) cfg.types = QT.map(function (t) { return t.id; });
    if (!Array.isArray(cfg.lv)) cfg.lv = (cfg.lv === 'ALL' || !cfg.lv) ? ['N5', 'N4', 'N3', 'N2', 'N1'] : [cfg.lv];
    cfg.lv = cfg.lv.filter(function (l) { return ['N5', 'N4', 'N3', 'N2', 'N1'].indexOf(l) >= 0; }); if (!cfg.lv.length) cfg.lv = ['N5'];
    var Q = null;
    [['N5', 'kanji5'], ['N4', 'kanji4'], ['N3', 'kanji3'], ['N2', 'kanji2'], ['N1', 'kanji1']].forEach(function (pr) {
      var LV = pr[0];
      MIXREG[pr[1]] = {
        label: 'Kanji ' + LV,
        grp: 'kanji',
        count: function () { return poolSize(LV, QT.map(function (t) { return t.id; }), false).q; },
        make: function (n) { var sv = cfg; cfg = { lv: LV, types: QT.map(function (t) { return t.id; }), n: n, wrong: false }; var r = buildQuiz(); cfg = sv; return r; },
        show: function (it, hooks, idx, total) {
          Q = { items: idx < total ? [it, it] : [it], i: 0, ok: 0, wrongs: [], wrongList: [], t0: Date.now(), mix: hooks, mixLv: LV, mixTag: '<div class="q-tag q-tag-mix">' + '<b>Kanji ' + LV + '</b></div>' };
          el.style.zIndex = 95; el.hidden = false; document.body.style.overflow = 'hidden';
          showQ(); ttl.textContent = 'Quiz général'; prog.textContent = idx + ' / ' + total; barI.style.width = ((idx - 1) / total * 100) + '%'; body.scrollTop = 0;
        },
        hide: function () { el.hidden = true; el.style.zIndex = ''; Q = null; paintCard(); }
      };
    });
    function curLv() { return Q && Q.mixLv ? Q.mixLv : cfg.lv; }

    var el = document.createElement('div'); el.className = 'quiz'; el.hidden = true;
    el.innerHTML = '<div class="q-top"><button class="x" type="button" aria-label="Fermer">×</button><div class="ttl">Quiz kanji</div><div class="prog"></div></div><div class="q-bar"><i></i></div><div class="q-body" id="q-body"></div>';
    document.body.appendChild(el);
    var body = el.querySelector('#q-body'), prog = el.querySelector('.prog'), barI = el.querySelector('.q-bar i'), ttl = el.querySelector('.ttl');

    /* — carte d'accès sur l'accueil — */
    var card = document.createElement('button'); card.type = 'button'; card.className = 'quizcard';
    function wrongCount() { return Object.keys(ST.kq).filter(function (k) { return ST.kq[k].w; }).length; }
    function paintCard() {
      var seen = Object.keys(ST.kq).length, w = wrongCount();
      card.innerHTML = '<span class="qc-jp">漢字</span><span class="qc-t">Quiz kanji<small>' + KD.length + ' kanji N5 à N1 · ' + (seen ? seen + ' vus' + (w ? ', ' + w + ' à revoir' : '') : 'jamais lancé') + '</small></span><span class="qc-go">›</span>';
    }
    paintCard();
    card.addEventListener('click', function () { openQuiz(); });
    quizHost(mainEl).appendChild(card);

    function hideQuiz() { el.hidden = true; document.body.style.overflow = ''; paintCard(); }
    function open(v) { if (v) { if (el.hidden) bkPush(hideQuiz); el.hidden = false; document.body.style.overflow = 'hidden'; } else bkClose(hideQuiz); }
    function openQuiz() { open(true); showSetup(); }
    el.querySelector('.x').addEventListener('click', function () { if (Q && Q.mix) { Q.mix.quit(); return; } open(false); paintCard(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !el.hidden && !(Q && Q.mix)) { open(false); paintCard(); } });

    /* — utilitaires — */
    function shuffle(a) { for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
    function levelPool(lv) { return KD.filter(function (x) { return lv === 'ALL' || (Array.isArray(lv) ? lv.indexOf(x.l) >= 0 : x.l === lv); }); }
    function elig(x, t) {
      return t === 'k2s' || t === 's2k' || (t === 'k2on' && x.on) || (t === 'k2kun' && x.kun) || (WT.indexOf(t) >= 0 && x.kw.length);
    }
    function parts(cell) { return cell.split(/[・･]/).map(function (p) { return p.replace(/[()（）]/g, '').trim(); }).filter(Boolean); }
    function senseToks(sn) { return sn.toLowerCase().split(/\s*[\/,;]\s*/).map(function (t) { return t.replace(/\(.*?\)/g, '').trim(); }).filter(Boolean); }
    function disjoint(a, b) { return !a.some(function (x) { return b.indexOf(x) >= 0; }); }
    function poolSize(lv, types, onlyWrong) {
      var n = 0, kanji = 0, ts = onlyWrong ? missSet(cfg, ST.kq, function (k) { return !!byK[k]; }) : null;
      levelPool(lv).forEach(function (x) {
        if (onlyWrong && !missPass(cfg, ST.kq, x.k, ts)) return;
        var c = types.filter(function (t) { return elig(x, t); }).length; if (c && types.indexOf('w2r') >= 0 && x.kw.length) c += Math.min(x.kw.length, WMAX) - 1; if (c) { n += c; kanji++; }
      });
      return { q: n, k: kanji };
    }

    /* — sélection des questions — */
    function bucket(k) { var s = ST.kq[k]; if (!s) return 1; if (s.w) return 0; if (s.st >= 3) return 3; return 2; }
    function buildQuiz() {
      var ts = missSet(cfg, ST.kq, function (k) { return !!byK[k]; }), pool = levelPool(cfg.lv).filter(function (x) { return missPass(cfg, ST.kq, x.k, ts); });
      var order = shuffle(pool.slice()).sort(function (a, b) { return bucket(a.k) - bucket(b.k); });
      var left = {}, wl = {}; order.forEach(function (x) { left[x.k] = shuffle(cfg.types.filter(function (t) { return elig(x, t); })); var nw = left[x.k].indexOf('w2r') >= 0 ? Math.min(x.kw.length, WMAX) : 0; for (var z = 1; z < nw; z++) left[x.k].push('w2r'); left[x.k] = shuffle(left[x.k]); wl[x.k] = shuffle(x.kw.slice()); });
      var tot = 0; order.forEach(function (x) { tot += left[x.k].length; });
      var items = [], target = cfg.n === 0 ? tot : Math.min(cfg.n, tot), guard = 0;
      while (items.length < target && guard++ < 50) {
        var round = [];
        order.forEach(function (x) { if (items.length + round.length < target && left[x.k].length) round.push({ x: x, t: left[x.k].pop() }); });
        if (!round.length) break;
        items = items.concat(shuffle(round));
      }
      return items.map(function (q) { return { k: q.x.k, t: q.t, w: WT.indexOf(q.t) >= 0 ? wl[q.x.k].pop() : null }; });
    }

    /* — options (distracteurs plausibles) — */
    function sameFirst(x, cands) {
      var same = shuffle(cands.filter(function (c) { return c.g === x.g; })), other = shuffle(cands.filter(function (c) { return c.g !== x.g; }));
      return same.slice(0, 2).concat(other).concat(same.slice(2));
    }
    function options(q) {
      var x = byK[q.k], pool = levelPool(curLv()).filter(function (c) { return c.k !== x.k; }), out = [], seen = {};
      function add(v, ok, k) { if (!v || seen[v]) return false; seen[v] = 1; out.push({ v: v, ok: ok, k: k }); return true; }
      if (q.t === 'k2s') {
        add(x.s, true); var tx = senseToks(x.s);
        sameFirst(x, pool.filter(function (c) { return disjoint(tx, senseToks(c.s)); })).some(function (c) { add(c.s, false); return out.length >= 4; });
      } else if (q.t === 's2k') {
        add(x.k, true); var ty = senseToks(x.s);
        sameFirst(x, pool.filter(function (c) { return disjoint(ty, senseToks(c.s)); })).some(function (c) { add(c.k, false); return out.length >= 4; });
      } else if (q.t === 'k2on' || q.t === 'k2kun') {
        var f = q.t === 'k2on' ? 'on' : 'kun', px = parts(x[f]);
        add(x[f], true);
        sameFirst(x, pool.filter(function (c) { return c[f] && disjoint(px, parts(c[f])); })).some(function (c) { add(c[f], false); return out.length >= 4; });
      } else {
        var r = q.w[1], tail = (q.w[0].match(/[ぁ-ゟ゠-ヿ]+$/) || [''])[0], words = [], wseen = {}, wt = q.t;
        var fk = function (w) { return wt === 'w2r' ? w[1] : wt === 'w2s' ? w[2] : w[0]; };
        var okv = fk(q.w); add(okv, true, q.w[1]);
        var ft = function (t) { return t.toLowerCase().split(/[^a-zàâçéèêëîïôûùüÿœ]+/).filter(function (z) { return z.length > 3; }).map(function (z) { return z.slice(0, 3); }); };
        var tk = ft(q.w[2]);
        var addWords = function (list) { list.forEach(function (c) { c.kw.forEach(function (w) {
          if (fk(w) === okv || w[0] === q.w[0] || wseen[w[0]] || wseen[fk(w)]) return;
          if (wt === 'w2s' && !disjoint(tk, ft(w[2]))) return;
          wseen[w[0]] = 1;
          words.push({ w: w, ov: wt === 'r2w' && w[0].split('').some(function (ch, i) { return i < w[0].length - 1 && r.indexOf(w[0].slice(i, i + 2)) >= 0; }) ? 1 : 0, tl: tail && (wt === 'w2r' ? w[1] : w[0]).slice(-tail.length) === tail ? 1 : 0, share: q.w[0].split('').some(function (ch) { return w[0].indexOf(ch) >= 0; }) ? 1 : 0, d: Math.abs(w[1].length - r.length) });
        }); }); };
        addWords(levelPool(curLv()));
        var tn = function () { return words.filter(function (z) { return z.tl; }).length; };
        if ((tail && tn() < 3) || words.length < 6) addWords(KD);
        var kana = wt === 'w2r' || wt === 'r2w';
        shuffle(words).sort(function (a, b) {
          if (kana) return (b.ov - a.ov) || (b.tl - a.tl) || (a.d > 1) - (b.d > 1) || (b.share - a.share);
          return (a.d > 2) - (b.d > 2) || (b.share - a.share);
        }).some(function (c) { add(fk(c.w), false, c.w[1]); return out.length >= 4; });
      }
      return shuffle(out);
    }

    /* — affichage — */
    function chipBtn(label, on, data, dis) { return '<button type="button" class="qchip' + (on ? ' on' : '') + '"' + (dis ? ' disabled' : '') + ' ' + data + '>' + label + '</button>'; }
    function showSetup() {
      var hc = missFix(cfg, ST.kq, wrongCount(), function (k) { return !!byK[k]; }); persist();
      Q = null; ttl.textContent = 'Quiz kanji'; prog.textContent = ''; barI.style.width = '0';
      var ps = poolSize(cfg.lv, cfg.types, cfg.wrong);
      if (cfg.n !== 0 && cfg.n > ps.q) cfg.n = 0;
      var wc = wrongCount(), h = '';
      h += '<div class="q-sec"><h4>Niveau <small>(un ou plusieurs)</small></h4><div class="qchips" id="q-lv">' + ['N5', 'N4', 'N3', 'N2', 'N1'].map(function (l) { return chipBtn(l + ' · ' + levelPool(l).length, cfg.lv.indexOf(l) >= 0, 'data-lv="' + l + '"'); }).join('') + chipBtn('Tous · ' + KD.length, cfg.lv.length === 5, 'data-lv="ALL"') + '</div></div>';
      h += '<div class="q-sec"><h4>Types de questions</h4><div class="qchips">' + QT.map(function (t) { return chipBtn(t.label, cfg.types.indexOf(t.id) >= 0, 'data-t="' + t.id + '"'); }).join('') + '</div><div class="qpre">' + QPRESETS.map(function (p, i) { return '<button type="button" class="mini" data-p="' + i + '">' + p.label + '</button>'; }).join('') + '</div></div>';
      h += '<div class="q-sec"><h4>Nombre de questions</h4><div class="qchips">' + QN.filter(function (n) { return n <= ps.q; }).map(function (n) { return chipBtn(n, cfg.n === n, 'data-n="' + n + '"', n > ps.q); }).join('') + chipBtn('Tout · ' + ps.q, cfg.n === 0, 'data-n="0"', ps.q === 0) + '</div></div>';
      h += '<div class="q-sec"><div class="row"><span class="lab">Seulement mes ratés<small>' + (hc ? wc + ' à revoir · ' + hc + ' déjà ratés' : 'Aucun raté pour l’instant') + '</small></span><button class="sw" type="button" id="q-wrong" role="switch" aria-checked="' + !!cfg.wrong + '"' + (hc ? '' : ' disabled') + '><i></i></button></div>' + (cfg.wrong ? missUi(cfg, ST.kq, wc, function (k) { return !!byK[k]; }) : '') + '</div>';
      var can = cfg.types.length && ps.q > 0;
      h += '<button type="button" class="mini qstat-btn" id="q-stats">📊 Statistiques</button>';
      h += '<button type="button" class="qgo" id="q-go"' + (can ? '' : ' disabled') + '>Lancer · ' + (cfg.n === 0 ? ps.q : Math.min(cfg.n, ps.q)) + ' questions</button>';
      body.innerHTML = h; body.scrollTop = 0;
    }
    function showStats() {
      Q = null; ttl.textContent = 'Statistiques'; prog.textContent = ''; barI.style.width = '0';
      var S = ST.kqs || { sess: 0, q: 0, ok: 0, ty: {} }, pc = function (a, b) { return b ? Math.round(a / b * 100) + ' %' : '—'; };
      var h = '<div class="q-stats"><div class="qs-tiles"><div><b>' + S.sess + '</b><span>quiz terminés</span></div><div><b>' + S.q + '</b><span>questions</span></div><div><b>' + pc(S.ok, S.q) + '</b><span>de réussite</span></div></div>';
      h += qsExtra('k', ST.kq, KD.length);
      h += '<h4 class="q-h">Par type de question</h4><div class="qs-types">' + QT.map(function (t) { var T = (S.ty || {})[t.id] || { n: 0, ok: 0 }; var p = T.n ? Math.round(T.ok / T.n * 100) : 0;
        return '<div class="qs-row"><div class="qs-l"><span>' + t.label + '</span><span><b>' + T.n + '</b> · ' + pc(T.ok, T.n) + '</span></div><div class="qs-bar"><i style="width:' + p + '%"></i></div></div>'; }).join('') + '</div>';
      var worst = Object.keys(ST.kq).map(function (k) { var v = ST.kq[k]; return { k: k, x: v.x || (v.w ? 1 : 0), n: v.n }; }).filter(function (v) { return v.x > 0 && byK[v.k]; }).sort(missSort);
      h += '<h4 class="q-h">Kanji les plus ratés</h4>';
      h += worst.length ? missBlock(worst.map(function (v) { var x = byK[v.k]; return '<div class="q-miss"><span class="kj">' + esc(v.k) + '</span><span>' + esc(x.s) + '<small>' + esc((x.on || '—') + ' · ' + (x.kun || '—')) + '</small></span><span class="qs-cnt">' + v.x + ' / ' + v.n + '</span></div>'; })) : '<p class="conj-note">Aucun raté enregistré pour l’instant.</p>';
      h += '<div class="q-end"><button type="button" class="qgo" id="q-back">Retour</button><button type="button" class="mini" id="q-reset">Effacer les statistiques</button></div></div>';
      body.innerHTML = h; body.scrollTop = 0;
    }
    function persist() { ST.kqc = cfg; save(); }
    body.addEventListener('click', function (e) {
      var b = e.target.closest('button'); if (!b || b.disabled) return;
      if (b.classList.contains('qhint')) { toggleHint(b); return; }
      if (b.dataset.lv) { var lv = b.dataset.lv; if (lv === 'ALL') cfg.lv = ['N5', 'N4', 'N3', 'N2', 'N1']; else { var i = cfg.lv.indexOf(lv); if (i >= 0) { if (cfg.lv.length > 1) cfg.lv.splice(i, 1); } else cfg.lv.push(lv); cfg.lv = ['N5', 'N4', 'N3', 'N2', 'N1'].filter(function (l) { return cfg.lv.indexOf(l) >= 0; }); } persist(); showSetup(); }
      else if (b.dataset.t) { var i = cfg.types.indexOf(b.dataset.t); if (i >= 0) cfg.types.splice(i, 1); else cfg.types.push(b.dataset.t); persist(); showSetup(); }
      else if (b.dataset.p) { cfg.types = QPRESETS[+b.dataset.p].types.slice(); persist(); showSetup(); }
      else if (b.dataset.n !== undefined) { cfg.n = +b.dataset.n; persist(); showSetup(); }
      else if (b.dataset.top !== undefined) { missTop(cfg, b.dataset.top); persist(); showSetup(); }
      else if (b.id === 'q-wrong') { cfg.wrong = !cfg.wrong; persist(); showSetup(); }
      else if (b.id === 'q-go') { start(buildQuiz()); }
      else if (b.classList.contains('qopt')) answer(b);
      else if (b.id === 'q-next') { if (Q.mix) { Q.mix.next(Q.ok > 0); return; } Q.i++; showQ(); }
      else if (b.id === 'q-say') { speak(JSON.parse(b.dataset.say)); }
      else if (b.id === 'q-again') { if (Q.wrongList.length) start(Q.wrongList.slice()); }
      else if (b.id === 'q-new' || b.id === 'q-back') { showSetup(); }
      else if (b.id === 'q-stats') { showStats(); }
      else if (b.id === 'q-reset') { if (confirm('Effacer toutes les statistiques et les kanji ratés ?')) { ST.kq = {}; ST.kqs = { sess: 0, q: 0, ok: 0, ty: {} }; save(); showStats(); } }
      else if (b.id === 'q-close') { open(false); paintCard(); }
    });

    function start(items) {
      if (!items.length) { toast('Aucune question disponible avec ces réglages.'); return; }
      Q = { items: items, i: 0, ok: 0, wrongs: [], wrongList: [], t0: Date.now(), done: false };
      showQ();
    }
    function bigKanji(t, cls) { return '<div class="q-big ' + (cls || '') + '">' + esc(t) + '</div>'; }
    function showQ() {
      if (Q.i >= Q.items.length) return showResult();
      var q = Q.items[Q.i], x = byK[q.k], opts = options(q); Q.cur = { q: q, opts: opts, done: false };
      ttl.textContent = 'Quiz kanji · ' + cfg.lv.join(' + ');
      prog.textContent = (Q.i + 1) + ' / ' + Q.items.length; barI.style.width = (Q.i / Q.items.length * 100) + '%';
      var ask = '', big = '', hint = '';
      if (q.t === 'k2s') { ask = 'Que signifie ce kanji ?'; big = bigKanji(x.k); }
      else if (q.t === 's2k') { ask = 'Quel kanji correspond à ce sens ?'; big = '<div class="q-big sens">' + esc(x.s) + '</div>'; }
      else if (q.t === 'k2on') { ask = 'Quelle est la lecture On de ce kanji ?'; big = bigKanji(x.k); }
      else if (q.t === 'k2kun') { ask = 'Quelle est la lecture Kun de ce kanji ?'; big = bigKanji(x.k); }
      else if (q.t === 'r2w') { ask = 'Quel est ce mot ?'; big = '<div class="q-big word">' + esc(q.w[1]) + '</div>'; }
      else if (q.t === 's2w') { ask = 'Comment s’écrit ce mot ?'; big = '<div class="q-big sens">' + esc(q.w[2]) + '</div>'; if (opts.length > 1) hint = hintBtn(opts.map(function (o) { return o.k; }).join('\n')); }
      else { ask = q.t === 'w2s' ? 'Que signifie ce mot ?' : 'Comment se lit ce mot ?'; big = '<div class="q-big word">' + q.w[0].split('').map(function (ch) { return ch === x.k ? '<b>' + esc(ch) + '</b>' : esc(ch); }).join('') + '</div>'; }
      var gl = (opts.length < 2) ? '<p class="conj-note">Pas assez de choix pour ce kanji.</p>' : '';
      body.innerHTML = '<div class="q-card">' + (Q.mixTag || '') + '<div class="q-ask">' + ask + '</div>' + big + hint + '</div>' + gl +
        '<div class="q-opts">' + opts.map(function (o, i) { return '<button type="button" class="qopt' + (q.t === 's2k' ? ' kj' : '') + '" data-i="' + i + '">' + esc(o.v) + '</button>'; }).join('') + '</div><div id="q-fb"></div>';
    }
    function answer(b) {
      var cur = Q.cur; if (cur.done) return; cur.done = true;
      var o = cur.opts[+b.dataset.i], q = cur.q, x = byK[q.k], good = !!o.ok;
      body.querySelectorAll('.qopt').forEach(function (n) { var oo = cur.opts[+n.dataset.i]; n.disabled = true; if (oo.ok) n.classList.add('good'); else if (n === b) n.classList.add('bad'); });
      var st = ST.kq[x.k] || { n: 0, st: 0, w: false }; st.n++; if (!good) st.x = (st.x || 0) + 1;
      var S = ST.kqs = ST.kqs || { sess: 0, q: 0, ok: 0, ty: {} }; S.q++; if (good) S.ok++; dayHit(good, 'k'); var T = S.ty[q.t] = S.ty[q.t] || { n: 0, ok: 0 }; T.n++; if (good) T.ok++;
      if (good) { Q.ok++; st.st++; st.w = false; } else { st.st = 0; st.w = true; if (Q.wrongs.indexOf(x.k) < 0) { Q.wrongs.push(x.k); Q.wrongList.push({ k: x.k, t: q.t, w: q.w }); } }
      ST.kq[x.k] = st; save();
      var say = [];
      if (WT.indexOf(q.t) >= 0) say = [q.w[1]]; else { if (x.on) say = say.concat(parts(x.on)); if (x.kun) say = say.concat(parts(x.kun)); }
      var kw = x.kw.slice(0, 4).map(function (w) { return esc(w[0]) + ' (' + esc(w[1]) + ') ' + esc(w[2]); }).join(' · ');
      var last = Q.i + 1 >= Q.items.length;
      document.getElementById('q-fb').innerHTML = '<div class="q-fb ' + (good ? 'good' : 'bad') + '"><div class="fbh">' + (good ? '✓ Bonne réponse' : '✗ Raté') + '</div>' +
        (WT.indexOf(q.t) >= 0 ? '<div class="fbw"><b>' + esc(q.w[0]) + '</b><span>' + esc(q.w[1]) + '</span><em>' + esc(q.w[2]) + '</em></div>' : '') +
        '<div class="fbk">' + esc(x.k) + '</div><div class="fbi"><div><b>On</b> ' + esc(x.on || '—') + '</div><div><b>Kun</b> ' + esc(x.kun || '—') + '</div><div><b>Sens</b> ' + esc(x.s) + '</div>' +
                (kw ? '<div><b>Mots</b> ' + kw + '</div>' : '') + '</div>' +
        '<div class="fbb"><button type="button" class="mini" id="q-say" data-say=\'' + esc(JSON.stringify(say)) + '\'>🔊 Écouter</button><button type="button" class="qgo" id="q-next">' + (last ? 'Voir le score' : 'Suivant') + '</button></div></div>';
      document.getElementById('q-fb').scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    }
    function showResult() {
      if (!Q.done) { Q.done = true; var S0 = ST.kqs = ST.kqs || { sess: 0, q: 0, ok: 0, ty: {} }; S0.sess++; save(); }
      var n = Q.items.length, pct = Math.round(Q.ok / n * 100), secs = Math.round((Date.now() - Q.t0) / 1000);
      ttl.textContent = 'Résultat'; prog.textContent = ''; barI.style.width = '100%';
      var wl = {}; Q.wrongs.forEach(function (k) { wl[k] = 1; });
      var list = Object.keys(wl).map(function (k) { var x = byK[k]; return '<div class="q-miss"><span class="kj">' + esc(k) + '</span><span>' + esc(x.s) + '<small>' + esc((x.on || '—') + ' · ' + (x.kun || '—')) + '</small></span></div>'; }).join('');
      body.scrollTop = 0; body.innerHTML = '<div class="q-score"><div class="n">' + Q.ok + '<small> / ' + n + '</small></div><div class="p">' + pct + ' % · ' + Math.floor(secs / 60) + ' min ' + (secs % 60) + ' s</div></div>' +
        (list ? '<h4 class="q-h">À revoir (' + Object.keys(wl).length + ')</h4><div class="q-miss-list">' + list + '</div>' : '<p class="conj-note">Sans faute. Bravo.</p>') +
        '<div class="q-end">' + (list ? '<button type="button" class="qgo" id="q-again">Refaire les ratés</button>' : '') + '<button type="button" class="mini" id="q-new">Nouveau quiz</button><button type="button" class="mini" id="q-close">Fermer</button></div>';
      paintCard();
    }
  }

