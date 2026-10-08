  /* ═══════════ QUIZ VOCABULAIRE & PHRASES ═══════════ */
  var VT = [
    { id: 'j2f', label: 'Japonais → français' },
    { id: 'f2j', label: 'Français → japonais' },
    { id: 'ear', label: '🔊 Écoute → français' }
  ];
  var VSUB = { '家族': 'Famille', '指示詞': 'Démonstratifs', '人称': 'Pronoms', '島と海': 'Îles et mers', 'Modalités': 'Modalités (il faut, peut-être…)', 'Conjugaison': 'Conjugaison des adjectifs', 'つなぎ言葉': 'Mots de liaison', '会話を続ける': 'Relancer la conversation', '同意・断り': 'Accord et refus', '接続詞': 'Connecteurs', '文型': 'Structures de phrase', '相づち': 'Réactions',
    'サービスの言葉': 'Vocabulaire du service', '旅行者のための敬語': 'Keigo pour voyageurs', '位置': 'Positions', '副詞': 'Adverbes', '疑問詞': 'Mots interrogatifs',
    '時刻': 'Heures', '曜日': 'Jours de la semaine', '月': 'Mois', '表現': 'Expressions de temps', '体': 'Corps', '動物': 'Animaux', '職業': 'Métiers', '色': 'Couleurs', '食べ物': 'Nourriture',
    'ハイキング': 'Randonnée', 'ホテル': 'Hôtel', 'レストラン': 'Restaurant', '困ったとき': 'En difficulté', '温泉': 'Onsen', '緊急': 'Urgences', '自己紹介': 'Se présenter', '買い物': 'Shopping', '鉄道': 'Train', '動詞': 'Verbes courants', '場所': 'Lieux en ville', '家': 'Maison et objets', '服': 'Vêtements', '天気': 'Météo et saisons', '気持ち': 'Émotions et états', '症状': 'Symptômes', '国': 'Pays et langues', '趣味': 'Loisirs', '擬音語': 'Onomatopées', '標識': 'Panneaux', '大きな数': 'Grands nombres', 'お金': 'Prix et argent', 'メッセージ': 'Messages', 'い形容詞': 'Adjectifs en い', 'な形容詞': 'Adjectifs en な', '学校': 'École et bureau', '自然': 'Nature et paysages', 'スポーツ': 'Sports', '芸術': 'Musique et arts', 'IT': 'Téléphone et internet', '料理': 'Cuisine', '量': 'Quantités', '人間関係': 'Relations', '店': 'Magasins', '旅行用語': 'Billets et bagages', '文化': 'Culture et traditions', '都道府県': 'Préfectures', '地方': 'Régions du Japon', '日付': 'Jours du mois', '期間': 'Durées', '年齢': 'Âge', '祝日': 'Jours fériés', '空港': 'Aéroport', 'タクシー': 'Taxi', 'コンビニ': 'Konbini', '銀行・郵便': 'Banque et poste', '携帯・ネット': 'Téléphone et Wi‑Fi', '病院・薬局': 'Médecin et pharmacie', '観光': 'Visites', '居酒屋・カラオケ': 'Izakaya et karaoké', '道案内': 'Chemin', '予約': 'Réservations', '洗濯・生活': 'Vie pratique', '祭り・行事': 'Fêtes', '世間話': 'Petite conversation', '意見': 'Opinions', '聞き返す': 'Faire répéter', '褒める・感謝': 'Compliments et remerciements', '誘う': 'Inviter', '自分のこと': 'Parler de soi', '電話': 'Téléphone', '尊敬語・謙譲語': 'Verbes de keigo', 'サービス・接客': 'Service client', 'ビジネス・電話': 'Affaires et téléphone', '文型・続き': 'Structures de phrase (suite)', '日常': 'Expressions du quotidien', 'ことわざ': 'Proverbes', 'その他': 'Autres particules' };
  function vtag2(x) {
    var p = x.g.split(':'), sub = p[1] === 'Listes' ? '' : (p[1] === '交通' ? 'Transports' : (VSUB[p[1]] || p[1] || ''));
    return esc(x.c === 'Vocabulaire' ? sub : x.c === 'Verbes' ? 'Verbes du quotidien · ' + (p[1] || '') : x.c + (sub ? ' · ' + sub : ''));
  }
  function vtag(x) {
    var p = x.g.split(':'), sub = p[1] === 'Listes' ? '' : (p[1] === '交通' ? 'Transports' : (VSUB[p[1]] || p[1] || ''));
    return '<div class="q-tag">' + esc(x.c) + (sub ? ' · ' + esc(sub) : '') + '</div>';
  }
  var VCATS = ['Voyage', 'Conversation', 'Keigo', 'Vocabulaire', 'Verbes', 'Temps', 'Adjectifs', 'Outils', 'Expressions', 'Particules'];
  var VN = [10, 25, 50, 100];
  function initVocab(mainEl) {
    var VD = []; try { VD = JSON.parse(document.getElementById('vocab-data').textContent); } catch (e) {}
    if (!VD.length) return;
    var canSpeak = !!window.speechSynthesis;
    var types = VT.filter(function (t) { return canSpeak || t.id !== 'ear'; });
    var byI = {}; VD.forEach(function (x) { byI[x.i] = x; });
    var cfg = ST.vqc || { cats: VCATS.slice(), types: types.map(function (t) { return t.id; }), n: 25, wrong: false };
    cfg.ka = false;
    if (!cfg.v2) { cfg.v2 = 1; if (cfg.cats.indexOf('Verbes') < 0) cfg.cats.push('Verbes'); }
    cfg.types = cfg.types.filter(function (t) { return types.some(function (u) { return u.id === t; }); }); if (!cfg.types.length) cfg.types = types.map(function (t) { return t.id; });
    if (!cfg.vx) cfg.vx = [];
    var vsOpen = false, VG = [], vgN = {};
    VD.forEach(function (x) { if (x.c === 'Vocabulaire') { if (!vgN[x.g]) { vgN[x.g] = 0; VG.push(x.g); } vgN[x.g]++; } });
    function vgLab(g) { var k = g.split(':')[1]; return k === '交通' ? 'Transports' : (VSUB[k] || k); }
    var Q = null;
    MIXREG['vocab'] = {
      label: 'Vocabulaire',
      count: function () { var sv = cfg; cfg = { cats: VCATS.slice(), types: types.map(function (t) { return t.id; }), n: 0, wrong: false, ka: false }; var r = countAvail().q; cfg = sv; return r; },
      make: function (n) { var sv = cfg; cfg = { cats: VCATS.slice(), types: types.map(function (t) { return t.id; }), n: n, wrong: false, ka: false }; var r = build(); cfg = sv; return r; },
      show: function (it, hooks, idx, total) {
        Q = { items: idx < total ? [it, it] : [it], i: 0, ok: 0, wrongList: [], t0: Date.now(), mix: hooks, mixTag: '<div class="q-tag q-tag-mix">' + '<b>Vocabulaire</b> › ' + vtag2(byI[it.i]) + '</div>' };
        el.style.zIndex = 95; el.hidden = false; document.body.style.overflow = 'hidden';
        showQ(); ttl.textContent = 'Quiz général'; prog.textContent = idx + ' / ' + total; barI.style.width = ((idx - 1) / total * 100) + '%'; body.scrollTop = 0;
      },
      hide: function () { el.hidden = true; el.style.zIndex = ''; Q = null; paintCard(); }
    };
    if (!ST.vq) ST.vq = {}; if (!ST.vqs) ST.vqs = { sess: 0, q: 0, ok: 0, ty: {}, cat: {} };

    var el = document.createElement('div'); el.className = 'quiz'; el.hidden = true;
    el.innerHTML = '<div class="q-top"><button class="x" type="button" aria-label="Fermer">×</button><div class="ttl">Quiz vocabulaire</div><div class="prog"></div></div><div class="q-bar"><i></i></div><div class="q-body"></div>';
    document.body.appendChild(el);
    var body = el.querySelector('.q-body'), prog = el.querySelector('.prog'), barI = el.querySelector('.q-bar i'), ttl = el.querySelector('.ttl');
    function $(id) { return el.querySelector('#' + id); }

    var card = document.createElement('button'); card.type = 'button'; card.className = 'quizcard';
    function wrongCount() { return Object.keys(ST.vq).filter(function (k) { return ST.vq[k].w && byI[k]; }).length; }
    function paintCard() {
      var seen = Object.keys(ST.vq).length, w = wrongCount();
      card.innerHTML = '<span class="qc-jp">言葉</span><span class="qc-t">Quiz vocabulaire &amp; phrases<small>' + VD.length + ' mots et phrases · ' + (seen ? seen + ' vus' + (w ? ', ' + w + ' à revoir' : '') : 'jamais lancé') + '</small></span><span class="qc-go">›</span>';
    }
    paintCard();
    card.addEventListener('click', function () { if (window.QPRE && window.QPRE.cats) { cfg.cats = window.QPRE.cats.slice(); window.QPRE = null; persist(); } open(true); showSetup(); });
    quizHost(mainEl).appendChild(card);
    function hideV() { el.hidden = true; document.body.style.overflow = ''; paintCard(); }
    function open(v) { if (v) { if (el.hidden) bkPush(hideV); el.hidden = false; document.body.style.overflow = 'hidden'; } else bkClose(hideV); }
    el.querySelector('.x').addEventListener('click', function () { if (Q && Q.mix) { Q.mix.quit(); return; } open(false); });

    function shuffle(a) { for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
    function pool() { return VD.filter(function (x) { return cfg.cats.indexOf(x.c) >= 0 && !(x.c === 'Vocabulaire' && cfg.vx && cfg.vx.indexOf(x.g) >= 0) && (!cfg.wrong || (ST.vq[x.i] && ST.vq[x.i].w)); }); }
    function earOK(x) { return /[぀-ヿ㐀-鿿]/.test(x.jp) && x.jp.indexOf('…') < 0; }
    function elig(x, t) { return cands(x).length >= 2 && (t !== 'ear' || earOK(x)); }
    function bucket(x) { var s = ST.vq[x.i]; if (!s) return 1; if (s.w) return 0; if (s.st >= 3) return 3; return 2; }
    function say(x) { var t = (x.ka || x.jp).split(/\s*[\/・]\s*/)[0].replace(/[…〜∅]/g, '').trim(); return [t]; }
    function sayJp(x) { if (canSpeak) speak(say(x)); }

    function build() {
      var p = pool(), order = shuffle(p.slice()).sort(function (a, b) { return bucket(a) - bucket(b); });
      var av0 = countAvail().q, target = cfg.n === 0 ? av0 : Math.min(cfg.n, av0), items = [], used = {}, guard = 0;
      while (items.length < target && guard++ < 20) {
        var round = [];
        order.forEach(function (x) {
          if (items.length + round.length >= target) return;
          var ok = ctypes(cfg.types).filter(function (t) { return elig(x, t) && !(used[x.i] && used[x.i][t]); });
          if (!ok.length) return;
          var t = ok[Math.floor(Math.random() * ok.length)]; (used[x.i] = used[x.i] || {})[t] = 1; round.push({ i: x.i, t: t });
        });
        if (!round.length) break; items = items.concat(shuffle(round));
      }
      return items;
    }
    function countAvail() { var p = pool(), q = 0; p.forEach(function (x) { q += ctypes(cfg.types).filter(function (t) { return elig(x, t); }).length; }); return { q: q, k: p.length }; }

    var STOPW = /^(dans|pour|avec|vous|votre|vos|pouvez|pourriez|pourrais|est-ce|tout|sans|plus|cette|elle|nous|faire|c’est|j’ai|puis-je|avoir|quel|quelle)$/;
    function toks(f) { return f.toLowerCase().replace(/[()（）\/,.?!«»…]/g, ' ').split(/\s+/).filter(function (w) { return w.length >= 5 && !STOPW.test(w); }); }
    function qty(f) { return /¥/.test(f) ? 'p' : /\bmin\b/.test(f) ? 'm' : /\d/.test(f) ? 'd' : ''; }
    function isPhrase(c) { return /[。？！…]/.test(c.jp) || c.fr.split(/\s+/).length >= 4; }
    var CAND = {};
    function cands(x) {
      if (CAND[x.i]) return CAND[x.i];
      var tx = toks(x.fr), rx = x.ka || x.jp;
      return (CAND[x.i] = VD.filter(function (c) {
        if (c.i === x.i || c.fr === x.fr || c.jp === x.jp) return false;
        if (qty(c.fr) !== qty(x.fr) || isPhrase(c) !== isPhrase(x)) return false;
        if ((c.ka || c.jp) === rx) return false;
        var tc = toks(c.fr); if (tx.some(function (w) { return tc.indexOf(w) >= 0; })) return false;
        return true;
      }));
    }
    function options(it) {
      var x = byI[it.i], key = it.t === 'f2j' ? 'jp' : 'fr', out = [x], seen = {}, kv = function (c) { return key === 'fr' ? noJpHint(c.fr) : c.jp; }; seen[kv(x)] = 1;
      var rest = cands(x).filter(function (c) { return !seen[kv(c)]; });
      var score = function (c) { return (c.g === x.g ? 0 : c.c === x.c ? 100 : 200) + Math.abs(c[key].length - x[key].length) + Math.random() * 12; };
      rest.sort(function (a, b) { return score(a) - score(b); });
      rest.some(function (c) { if (seen[kv(c)]) return false; seen[kv(c)] = 1; out.push(c); return out.length >= 4; });
      return shuffle(out.map(function (c) { return { v: kv(c), ok: c === x, k: c.kk || c.jp }; }));
    }

    function chip(label, on, data, dis) { return '<button type="button" class="qchip' + (on ? ' on' : '') + '"' + (dis ? ' disabled' : '') + ' ' + data + '>' + label + '</button>'; }
    function showSetup() {
      if (cfg.wrong && !wrongCount()) { cfg.wrong = false; persist(); } /* plus aucun raté : le mode « seulement mes ratés » ne doit pas rester bloqué */
      Q = null; ttl.textContent = 'Quiz vocabulaire'; prog.textContent = ''; barI.style.width = '0';
      var av = countAvail(); if (cfg.n !== 0 && cfg.n > av.q) cfg.n = 0;
      var cnt = {}; VD.forEach(function (x) { cnt[x.c] = (cnt[x.c] || 0) + 1; });
      var wc = wrongCount(), h = '';
      h += '<div class="q-sec"><h4>Rubriques</h4><div class="qchips">' + VCATS.map(function (c) { return chip((c === 'Verbes' ? 'Verbes du quotidien' : c) + ' · ' + (cnt[c] || 0), cfg.cats.indexOf(c) >= 0, 'data-c="' + c + '"'); }).join('') + '</div><div class="qpre"><button type="button" class="mini" data-call="1">Tout</button><button type="button" class="mini" data-cmin="1">Phrases (voyage)</button><button type="button" class="mini" data-cw="1">Mots</button></div></div>';
      if (cfg.cats.indexOf('Vocabulaire') >= 0 && VG.length) {
        var vOn = VG.filter(function (g) { return cfg.vx.indexOf(g) < 0; }).length;
        h += '<div class="q-sec"><details class="qsubd" id="v-sub"' + (vsOpen ? ' open' : '') + '><summary><span>Sous-rubriques de Vocabulaire</span><b>' + vOn + ' / ' + VG.length + '</b></summary><div class="qchips">' +
          VG.map(function (g) { return chip(esc(vgLab(g)) + ' · ' + vgN[g], cfg.vx.indexOf(g) < 0, 'data-vs="' + esc(g) + '"'); }).join('') +
          '</div><div class="qpre"><button type="button" class="mini" data-vsall="1">Tout</button><button type="button" class="mini" data-vsnone="1">Aucune</button></div></details></div>';
      }
      h += '<div class="q-sec"><h4>Types de questions</h4><div class="qchips">' + types.filter(function (t) { return !(ST.silent && t.id === 'ear'); }).map(function (t) { return chip(t.label, cfg.types.indexOf(t.id) >= 0, 'data-t="' + t.id + '"'); }).join('') + '</div></div>';
      h += '<div class="q-sec"><h4>Nombre de questions</h4><div class="qchips">' + VN.filter(function (n) { return n <= av.q; }).map(function (n) { return chip(n, cfg.n === n, 'data-n="' + n + '"', n > av.q); }).join('') + chip('Tout · ' + av.q, cfg.n === 0, 'data-n="0"', av.q === 0) + '</div></div>';
      h += '<div class="q-sec"><div class="row"><span class="lab">Seulement mes ratés<small>' + (wc ? wc + ' à revoir' : 'Aucun raté pour l’instant') + '</small></span><button class="sw" type="button" id="v-wrong" role="switch" aria-checked="' + !!cfg.wrong + '"' + (wc ? '' : ' disabled') + '><i></i></button></div></div>';
      h += '<button type="button" class="mini qstat-btn" id="v-stats">📊 Statistiques</button>';
      h += '<button type="button" class="qgo" id="v-go"' + (cfg.cats.length && cfg.types.length && av.q ? '' : ' disabled') + '>Lancer · ' + (cfg.n === 0 ? av.q : Math.min(cfg.n, av.q)) + ' questions</button>';
      body.innerHTML = h; body.scrollTop = 0;
    }
    function persist() { ST.vqc = cfg; save(); }
    function toggle(arr, v) { var i = arr.indexOf(v); if (i >= 0) arr.splice(i, 1); else arr.push(v); }

    body.addEventListener('toggle', function (e) { if (e.target.id === 'v-sub') vsOpen = e.target.open; }, true);
    body.addEventListener('click', function (e) {
      var b = e.target.closest('button'); if (!b || b.disabled) return;
      var d = b.dataset;
      if (b.classList.contains('qhint')) { toggleHint(b); return; }
      if (d.vs) { toggle(cfg.vx, d.vs); persist(); showSetup(); }
      else if (d.vsall) { cfg.vx = []; persist(); showSetup(); }
      else if (d.vsnone) { cfg.vx = VG.slice(); persist(); showSetup(); }
      else if (d.c) { toggle(cfg.cats, d.c); persist(); showSetup(); }
      else if (d.call) { cfg.cats = VCATS.slice(); persist(); showSetup(); }
      else if (d.cmin) { cfg.cats = ['Voyage', 'Conversation', 'Keigo']; persist(); showSetup(); }
      else if (d.cw) { cfg.cats = ['Vocabulaire', 'Temps', 'Adjectifs', 'Outils']; persist(); showSetup(); }
      else if (d.t) { toggle(cfg.types, d.t); persist(); showSetup(); }
      else if (d.n !== undefined) { cfg.n = +d.n; persist(); showSetup(); }
      else if (b.id === 'v-wrong') { cfg.wrong = !cfg.wrong; persist(); showSetup(); }
      else if (b.id === 'v-go') { start(build()); }
      else if (b.classList.contains('qopt')) answer(b);
      else if (b.id === 'v-next') { if (Q.mix) { Q.mix.next(Q.ok > 0); return; } Q.i++; showQ(); }
      else if (b.id === 'v-say') { sayJp(byI[b.dataset.id]); }
      else if (b.id === 'v-replay') { sayJp(byI[Q.cur.it.i]); }
      else if (b.id === 'v-again') { if (Q.wrongList.length) start(Q.wrongList.slice()); }
      else if (b.id === 'v-new' || b.id === 'v-back') { showSetup(); }
      else if (b.id === 'v-stats') { showStats(); }
      else if (b.id === 'v-close') { open(false); }
      else if (b.id === 'v-reset') { if (confirm('Effacer toutes les statistiques du quiz vocabulaire et les ratés ?')) { ST.vq = {}; ST.vqs = { sess: 0, q: 0, ok: 0, ty: {}, cat: {} }; save(); showStats(); } }
    });

    function start(items) {
      if (!items.length) { toast('Aucune question disponible avec ces réglages.'); return; }
      Q = { items: items, i: 0, ok: 0, wrongList: [], t0: Date.now(), done: false }; showQ();
    }
    function showQ() {
      if (Q.i >= Q.items.length) return showResult();
      var it = Q.items[Q.i], x = byI[it.i], opts = options(it); Q.cur = { it: it, opts: opts, done: false };
      prog.textContent = (Q.i + 1) + ' / ' + Q.items.length; barI.style.width = (Q.i / Q.items.length * 100) + '%';
      var ask, big, hint = '';
      if (it.t === 'j2f') { ask = 'Que signifie ?'; big = '<div class="q-big word vq">' + esc(x.jp) + '</div>'; hint = hintBtn(x.kk && x.kk !== x.jp ? x.kk : ''); }
      else if (it.t === 'f2j') { ask = 'Comment dit-on en japonais ?'; big = '<div class="q-big sens">' + esc(noJpHint(x.fr)) + '</div>'; hint = hintBtn(opts.some(function (o) { return HK.test(o.v); }) ? opts.map(function (o) { return o.k; }).join('\n') : ''); }
      else if (ST.silent) { ask = 'Que signifie ?'; big = '<div class="q-big word vq">' + esc(x.jp) + '</div>'; hint = hintBtn(x.kk && x.kk !== x.jp ? x.kk : ''); }
      else { ask = 'Écoute, puis choisis le sens'; big = '<button type="button" class="qgo vq-ear" id="v-replay">🔊 Réécouter</button>' + earAlt(x.jp + (x.kk && x.kk !== x.jp ? '  (' + x.kk + ')' : '')); }
      body.innerHTML = '<div class="q-card">' + (Q.mixTag || vtag(x)) + '<div class="q-ask">' + ask + '</div>' + big + hint + '</div><div class="q-opts">' +
        opts.map(function (o, i) { return '<button type="button" class="qopt vq-opt" data-i="' + i + '">' + esc(o.v) + '</button>'; }).join('') + '</div><div id="v-fb"></div>';
      if (it.t === 'ear' && !ST.silent) setTimeout(function () { sayJp(x); }, 150);
    }
    function answer(b) {
      var cur = Q.cur; if (cur.done) return; cur.done = true;
      var o = cur.opts[+b.dataset.i], it = cur.it, x = byI[it.i], good = !!o.ok;
      body.querySelectorAll('.qopt').forEach(function (n) { var oo = cur.opts[+n.dataset.i]; n.disabled = true; if (oo.ok) n.classList.add('good'); else if (n === b) n.classList.add('bad'); });
      var st = ST.vq[x.i] || { n: 0, st: 0, w: false }; st.n++;
      if (good) { Q.ok++; st.st++; st.w = false; } else { st.st = 0; st.w = true; st.x = (st.x || 0) + 1; if (!Q.wrongList.some(function (w) { return w.i === x.i; })) Q.wrongList.push({ i: x.i, t: it.t }); }
      ST.vq[x.i] = st;
      var S = ST.vqs; S.q++; if (good) S.ok++; dayHit(good, 'v');
      var T = S.ty[it.t] = S.ty[it.t] || { n: 0, ok: 0 }; T.n++; if (good) T.ok++;
      var C = S.cat[x.c] = S.cat[x.c] || { n: 0, ok: 0 }; C.n++; if (good) C.ok++;
      save();
      var last = Q.i + 1 >= Q.items.length;
      $('v-fb').innerHTML = '<div class="q-fb ' + (good ? 'good' : 'bad') + '"><div class="fbh">' + (good ? '✓ Bonne réponse' : '✗ Raté') + '</div>' +
        '<div class="vq-ans"><div class="vq-jp">' + esc(x.jp) + '</div>' + (x.ka ? '<div>' + esc(x.ka) + '</div>' : '') + (x.ro ? '<div class="vq-ro">' + esc(x.ro) + '</div>' : '') + '<div><b>' + esc(x.fr) + '</b></div></div>' + jpMini(x) +
        '<div class="fbb">' + (canSpeak && earOK(x) ? '<button type="button" class="mini" id="v-say" data-id="' + x.i + '">🔊 Écouter</button>' : '') + '<button type="button" class="qgo" id="v-next">' + (last ? 'Voir le score' : 'Suivant') + '</button></div></div>';
      $('v-fb').scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    }
    function showResult() {
      if (!Q.done) { Q.done = true; ST.vqs.sess++; save(); }
      barI.style.width = '100%'; prog.textContent = '';
      var n = Q.items.length, pct = Math.round(Q.ok / n * 100), secs = Math.round((Date.now() - Q.t0) / 1000);
      var list = Q.wrongList.map(function (w) { var x = byI[w.i]; return '<div class="q-miss"><span class="vq-mj">' + esc(x.jp) + '</span><span>' + esc(x.fr) + '<small>' + esc(x.ka || x.ro) + '</small></span></div>'; }).join('');
      body.scrollTop = 0; body.innerHTML = '<div class="q-score"><div class="n">' + Q.ok + '<small> / ' + n + '</small></div><div class="p">' + pct + ' % · ' + Math.floor(secs / 60) + ' min ' + (secs % 60) + ' s</div></div>' +
        (list ? '<h4 class="q-h">À revoir (' + Q.wrongList.length + ')</h4><div class="q-miss-list">' + list + '</div>' : '<p class="conj-note">Sans faute. Bravo.</p>') +
        '<div class="q-end">' + (list ? '<button type="button" class="qgo" id="v-again">Refaire les ratés</button>' : '') + '<button type="button" class="mini" id="v-new">Nouveau quiz</button><button type="button" class="mini" id="v-close">Fermer</button></div>';
    }
    function showStats() {
      Q = null; ttl.textContent = 'Statistiques'; prog.textContent = ''; barI.style.width = '0';
      var S = ST.vqs, pc = function (a, b) { return b ? Math.round(a / b * 100) + ' %' : '—'; };
      function rows(list, get) { return list.map(function (t) { var T = get(t[0]) || { n: 0, ok: 0 }; var p = T.n ? Math.round(T.ok / T.n * 100) : 0; return '<div class="qs-row"><div class="qs-l"><span>' + t[1] + '</span><span><b>' + T.n + '</b> · ' + pc(T.ok, T.n) + '</span></div><div class="qs-bar"><i style="width:' + p + '%"></i></div></div>'; }).join(''); }
      var h = '<div class="q-stats"><div class="qs-tiles"><div><b>' + S.sess + '</b><span>quiz terminés</span></div><div><b>' + S.q + '</b><span>questions</span></div><div><b>' + pc(S.ok, S.q) + '</b><span>de réussite</span></div></div>';
      h += qsExtra('v', ST.vq, VD.length);
      h += '<h4 class="q-h">Par type de question</h4><div class="qs-types">' + rows(VT.map(function (t) { return [t.id, t.label]; }), function (k) { return S.ty[k]; }) + '</div>';
      h += '<h4 class="q-h">Par rubrique</h4><div class="qs-types">' + rows(VCATS.map(function (c) { return [c, c]; }), function (k) { return S.cat[k]; }) + '</div>';
      var worst = Object.keys(ST.vq).map(function (k) { var v = ST.vq[k]; return { i: k, x: v.x || (v.w ? 1 : 0), n: v.n }; }).filter(function (v) { return v.x > 0 && byI[v.i]; }).sort(missSort);
      h += '<h4 class="q-h">Les plus ratés</h4>' + (worst.length ? missBlock(worst.map(function (v) { var x = byI[v.i]; return '<div class="q-miss"><span class="vq-mj">' + esc(x.jp) + '</span><span>' + esc(x.fr) + '<small>' + esc(x.ka || x.ro) + '</small></span><span class="qs-cnt">' + v.x + ' / ' + v.n + '</span></div>'; })) : '<p class="conj-note">Aucun raté enregistré pour l’instant.</p>');
      h += '<div class="q-end"><button type="button" class="qgo" id="v-back">Retour</button><button type="button" class="mini" id="v-reset">Effacer les statistiques</button></div></div>';
      body.innerHTML = h; body.scrollTop = 0;
    }
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !el.hidden && !(Q && Q.mix)) open(false); });
  }

