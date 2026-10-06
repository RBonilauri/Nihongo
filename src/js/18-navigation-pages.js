  /* ═══════════ NAVIGATION PAR PAGES ═══════════ */
  var POLES = [
    { id: 'bases', jp: '仮', label: 'Bases', secs: ['仮名', '発音', '漢字'] },
    { id: 'gram', jp: '文', label: 'Grammaire', secs: ['助詞', '動詞', '形容詞', '助数詞', '表現', '道具'] },
    { id: 'voc', jp: '語', label: 'Vocabulaire', secs: ['語彙', '時間', '地理'] },
    { id: 'parl', jp: '話', label: 'Parler', secs: ['会話', '旅行', '敬語'] }
  ];
  var QMAP = { '助詞': ['Quiz particules'], '動詞': ['Quiz conjugaison'], '漢字': ['Quiz kanji'], '助数詞': ['Quiz compteurs'], '地理': ['Quiz géographie'],
    '語彙': ['Quiz vocabulaire', ['Vocabulaire', 'Verbes']], '時間': ['Quiz vocabulaire', ['Temps']], '形容詞': ['Quiz vocabulaire', ['Adjectifs']], '表現': ['Quiz vocabulaire', ['Expressions']],
    '旅行': ['Quiz vocabulaire', ['Voyage']], '会話': ['Quiz vocabulaire', ['Conversation']], '敬語': ['Quiz vocabulaire', ['Keigo']], '道具': ['Quiz vocabulaire', ['Outils']] };
  var NAV = [{ v: 'home' }], TAB = 'home', pushed = 0, secBy = {}, subById = {}, navMain = null, navPage = null;
  function secJp(s) { return s.querySelector(':scope > summary .jp').textContent.trim(); }
  function secLb(s) { return s.querySelector(':scope > summary .lbl').textContent.trim(); }
  function subsOf(s) { return [].slice.call(s.querySelectorAll(':scope > .sec-body > details.sub')); }
  function splitT(t) { var p = t.split(' — '); return p.length > 1 ? { jp: p[0], fr: p.slice(1).join(' — ') } : { jp: '', fr: t }; }
  function poleOf(jp) { for (var i = 0; i < POLES.length; i++) if (POLES[i].secs.indexOf(jp) >= 0) return POLES[i]; return null; }
  function launchQuiz(name, cats) {
    if (cats) window.QPRE = { cats: cats };
    var card = [].slice.call(document.querySelectorAll('.quizlist .quizcard')).filter(function (c) { return c.textContent.indexOf(name) >= 0; })[0];
    if (card) card.click(); else window.QPRE = null;
  }
  function navPush(st) { NAV.push(st); try { history.pushState({ nv: 1 }, ''); } catch (e) {} pushed++; navRender(); }
  function navReset(tab) {
    if (pushed > 0) { bkSkip++; try { history.go(-pushed); } catch (e) { bkSkip--; } pushed = 0; }
    TAB = tab; NAV = [tab === 'quiz' ? { v: 'sec', s: secBy['クイズ'] } : { v: tab }]; navRender();
  }
  function navOpen(sec, sub) { navPush(sub ? { v: 'sub', s: sec, d: sub } : { v: 'sec', s: sec }); }
  function navRender() {
    var st = NAV[NAV.length - 1], v = st.v, h = '', title = ['日本語', 'Référence'];
    navMain.className = navMain.className.replace(/\bv-\w+\b/g, '').trim() + ' nv v-' + v;
    Object.keys(secBy).forEach(function (k) { secBy[k].classList.remove('cur'); });
    Object.keys(subById).forEach(function (k) { subById[k].classList.remove('cur'); });
    if (st.s) { st.s.open = true; st.s.classList.add('cur'); }
    if (st.d) { st.d.open = true; st.d.classList.add('cur'); var rid = Object.keys(subMap).filter(function (k) { return subMap[k].sub === st.d; })[0]; if (rid) { ST.rec = [rid].concat(ST.rec.filter(function (x) { return x !== rid; })).slice(0, 3); save(); renderHome(); } }
    if (v === 'home') {
      h = dayCard() + '<div class="nhero"><div class="nh-t">DÉMARRER</div><div class="nh-b">Quiz général</div><p>Un mélange de tous les thèmes, à ton rythme.</p><button type="button" class="ngo" data-act="mix">Lancer un quiz</button></div>' +
        '<div class="nrow"><button type="button" data-act="learn"><i>📚</i>Apprendre</button><button type="button" data-act="quiz"><i>❓</i>Tous les quiz</button></div>' +
        '<button type="button" class="nstats" data-act="stats"><i>📈</i>Ma progression<small>Réussite, jours actifs, points faibles</small></button>';
    } else if (v === 'search') { title = ['日本語', 'Recherche'];
    } else if (v === 'stats') { title = ['日本語', 'Ma progression']; h = statsHtml();
    } else if (v === 'learn') {
      title = ['日本語', 'Apprendre'];
      h = POLES.map(function (p) { var ss = p.secs.map(function (j) { return secBy[j]; }).filter(Boolean); return '<button type="button" class="npole" data-p="' + p.id + '"><span class="ni">' + p.jp + '</span><span class="nt">' + esc(p.label) + '<small>' + ss.map(secLb).map(esc).join(' · ') + '</small></span><span class="ch">›</span></button>'; }).join('') ;
    } else if (v === 'pole') {
      var P = POLES.filter(function (p) { return p.id === st.p; })[0]; title = [P.jp, P.label];
      h = P.secs.map(function (j) { return secBy[j]; }).filter(Boolean).map(function (s) { var n = subsOf(s).length; return '<button type="button" class="nsec" data-sj="' + esc(secJp(s)) + '"><span class="nj">' + esc(secJp(s)) + '</span><span class="nt">' + esc(secLb(s)) + '<small>' + (n ? n + ' sous-rubrique' + (n > 1 ? 's' : '') : 'contenu direct') + '</small></span><span class="ch">›</span></button>'; }).join('');
    } else if (v === 'sec') { title = [secJp(st.s), secLb(st.s)]; }
    else if (v === 'sub') { title = [secJp(st.s), splitT(st.d.querySelector(':scope > summary').firstChild.textContent.trim()).fr]; }
    navPage.innerHTML = h;
    var tb = document.querySelector('.tb-title'); tb.innerHTML = '<span>' + esc(title[0]) + '</span><small>' + esc(title[1]) + '</small>';
    document.getElementById('tb-back').hidden = NAV.length < 2;
    if (v === 'search') { renderScopes(cur && q.value.trim() ? cur.counts : null); renderHist(); if (!q.value.trim()) setTimeout(function () { try { q.focus(); } catch (e) {} }, 120); }
    [].slice.call(document.querySelectorAll('#tabbar button[data-tab]')).forEach(function (b) { b.classList.toggle('on', b.dataset.tab === TAB); });
    navTop();
  }
  function navTop() { window.scrollTo(0, 0); requestAnimationFrame(function () { window.scrollTo(0, 0); setTimeout(function () { if (!NAV[NAV.length - 1].keep) window.scrollTo(0, 0); }, 60); }); }
  function navInit() {
    try { history.scrollRestoration = 'manual'; } catch (e) {}
    navMain = document.querySelector('main');
    var sp = document.getElementById('spage'); navMain.insertBefore(sp, navMain.firstChild);
    navPage = document.createElement('div'); navPage.id = 'navpage'; navMain.insertBefore(navPage, navMain.querySelector('.home') || navMain.querySelector('details.sec'));
    [].slice.call(navMain.querySelectorAll(':scope > details.sec')).forEach(function (s) { secBy[secJp(s)] = s; });
    Object.keys(subMap).forEach(function (k) { subById[subMap[k].sub.dataset.id] = subMap[k].sub; });
    // listes de sous-rubriques + bouton quiz, dans chaque rubrique
    Object.keys(secBy).forEach(function (j) {
      var s = secBy[j], subs = subsOf(s), body = s.querySelector(':scope > .sec-body'), ns = document.createElement('div'); ns.className = 'navsubs';
      var q = QMAP[j], h = q ? '<button type="button" class="nquiz" data-qj="' + esc(j) + '">❓ Quiz de cette rubrique</button>' : '';
      h += subs.map(function (d) { var t = splitT(d.querySelector(':scope > summary').firstChild.textContent.trim()); return '<button type="button" class="nsub" data-id="' + esc(d.dataset.id) + '"><span class="nj">' + esc(t.jp) + '</span><span class="nt">' + esc(t.fr) + '</span><span class="ch">›</span></button>'; }).join('');
      ns.innerHTML = h; if (!h) return;
      body.insertBefore(ns, subs[0] || body.firstChild);
    });
    navMain.addEventListener('click', function (e) {
      var b = e.target.closest('button'); if (!b) return;
      if (b.classList.contains('nsub')) { var d = subById[b.dataset.id], cur = NAV[NAV.length - 1]; navPush({ v: 'sub', s: cur.s, d: d }); }
      else if (b.classList.contains('nquiz')) { var q = QMAP[b.dataset.qj]; launchQuiz(q[0], q[1]); }
      else if (b.classList.contains('npole') && b.dataset.p) navPush({ v: 'pole', p: b.dataset.p });
      else if (b.classList.contains('nsec')) navPush({ v: 'sec', s: secBy[b.dataset.sj] });
      else if (b.dataset.act === 'learn') navReset('learn');
      else if (b.dataset.act === 'quiz') navReset('quiz');
      else if (b.dataset.act === 'stats') navPush({ v: 'stats' });
      else if (b.dataset.act === 'mix') launchQuiz('Quiz général');
    });
    // une sous-rubrique affichée comme page reste ouverte
    navMain.addEventListener('click', function (e) { var sm = e.target.closest('details.sub.cur > summary'); if (sm && !e.target.closest('button')) e.preventDefault(); }, true);
    document.getElementById('tabbar').addEventListener('click', function (e) {
      var b = e.target.closest('button'); if (!b) return;
      if (b.dataset.tab) { if (TAB === b.dataset.tab && NAV.length === 1) { window.scrollTo(0, 0); return; } navReset(b.dataset.tab); }
    });
    document.getElementById('tb-back').addEventListener('click', function () { if (pushed > 0) history.back(); else { NAV = [NAV[0]]; navRender(); } });
    navRender();
    if (window.__deep) { var dp = window.__deep; window.__deep = null; openTo(dp); }
  }
