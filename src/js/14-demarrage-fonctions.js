  function features() {
    var mainEl = document.querySelector('main');
    // étoiles + bouton Réviser dans chaque sous-section
    Object.keys(subMap).forEach(function (id) {
      var r = subMap[id], sm = r.sub.querySelector(':scope > summary');
      var b = document.createElement('button'); b.className = 'fav'; b.type = 'button'; b.dataset.id = id; b.setAttribute('aria-label', 'Favori');
      b.addEventListener('click', function (e) { e.preventDefault(); e.stopPropagation(); var k = ST.fav.indexOf(id); if (k >= 0) ST.fav.splice(k, 1); else ST.fav.unshift(id); save(); syncFavButtons(); renderHome(); });
      sm.appendChild(b);
      var cjIds = CJ_SUBS[splitT(sm.firstChild.textContent.trim()).jp], isV = r.sec.querySelector(':scope > summary .jp').textContent.trim() === '動詞';
      if (cjIds && isV) {
        /* conjugaison : fiches uniformes (sens, contexte, groupes, exemple) */
        var cb = r.sub.querySelector(':scope > .sub-body'), cbtn = document.createElement('button'); cbtn.className = 'deckbtn'; cbtn.type = 'button'; cbtn.textContent = '🃏 Réviser en fiches';
        cbtn.addEventListener('click', function () { startDeckList(cjFor(cjIds), splitT(sm.firstChild.textContent.trim()).fr, true); });
        cb.insertBefore(cbtn, cb.firstChild);
      } else if (cardsFrom(r.sub, id).length >= 3) {
        var body = r.sub.querySelector(':scope > .sub-body');
        var rb = document.createElement('button'); rb.className = 'deckbtn'; rb.type = 'button'; rb.textContent = '🃏 Réviser en fiches';
        rb.addEventListener('click', function () { startDeck(r.sub, id, true); });
        body.insertBefore(rb, body.firstChild);
      }
    });
    var hint = mainEl.querySelector('.hint'); mainEl.insertBefore(home, (hint ? hint.nextSibling : mainEl.querySelector('details.sec')));
    initQuiz(mainEl); initVocab(mainEl); initGrammar(mainEl, 'c'); initGrammar(mainEl, 'p'); initCounters(mainEl); initGeo(mainEl); initMix(mainEl); renderHome(); syncFavButtons(); buildSettings();
    document.body.appendChild(deck);
    applyPrefs();
    // ouverture depuis l'adresse (#s2-3)
    var h = location.hash.replace('#', '');
    if (h) { window.__deep = Object.keys(subMap).map(function (k) { return subMap[k]; }).filter(function (r) { return r.sub.dataset.id === h; })[0]; }
  }

