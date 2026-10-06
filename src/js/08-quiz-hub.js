  /* ═══════════ RUBRIQUE QUIZ (regroupe tous les quiz) ═══════════ */
  var HK = /[一-鿿々]/;
  var MIXREG = {};
  function hintBtn(k) { return k ? '<button type="button" class="qhint" aria-label="Voir en kana" title="Voir en kana" data-k="' + esc(k) + '">💡</button>' : ''; }
  function toggleHint(b) {
    var o = b.parentNode.querySelector('.qhint-out');
    if (o) { o.remove(); b.classList.remove('on'); return; }
    o = document.createElement('div'); o.className = 'qhint-out'; o.textContent = b.dataset.k; b.parentNode.insertBefore(o, b.nextSibling); b.classList.add('on');
  }
  function quizHost(mainEl) {
    var host = mainEl.querySelector('#quiz-sec .quizlist'); if (host) return host;
    var sec = document.createElement('details'); sec.className = 'sec'; sec.id = 'quiz-sec'; sec.setAttribute('name', 'sec');
    sec.innerHTML = '<summary><span class="jp">クイズ</span><span class="lbl">Quiz</span></summary><div class="sec-body"><p class="jp-sub">クイズ — Kuizu</p><p>Teste-toi sur les kanji, le vocabulaire, la grammaire et les compteurs. Les ratés sont mémorisés et chaque quiz a sa page de statistiques.</p><div class="quizlist"></div></div>';
    var first = mainEl.querySelector('details.sec'); mainEl.insertBefore(sec, first);
    return sec.querySelector('.quizlist');
  }

