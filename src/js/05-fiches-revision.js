  /* ── fiches de révision (à partir des tableaux) ── */
  var deck = document.createElement('div'); deck.className = 'deck'; deck.hidden = true;
  deck.innerHTML = '<div class="deck-top"><button class="x" aria-label="Fermer">×</button><div class="ttl"></div><div class="prog"></div></div><div class="card" id="card" tabindex="0"></div><div class="deck-btns"><button class="again">À revoir</button><button class="ok">Su</button></div>';
  var D = { cards: [], i: 0, flipped: false, title: '' };
  function cellText(c) {
    if (!c.querySelector('ruby, .kmore')) return c.textContent.replace(/\s+/g, ' ').trim();
    var k = c.cloneNode(true);
    k.querySelectorAll('ruby').forEach(function (r) { var rt = r.querySelector('rt'), t = rt ? rt.textContent : ''; if (rt) rt.remove(); r.replaceWith(r.textContent + (t ? '（' + t + '）' : '')); });
    k.querySelectorAll('summary').forEach(function (x) { x.replaceWith(' ＋ '); });
    return k.textContent.replace(/\s+/g, ' ').trim();
  }
  function cardsFrom(sub, title) {
    var out = [];
    sub.querySelectorAll('table').forEach(function (t) {
      var heads = Array.prototype.map.call(t.querySelectorAll('thead th, tr:first-child th'), function (h) { return h.textContent.replace(/\s+/g, ' ').trim(); });
      t.querySelectorAll('tr').forEach(function (tr) {
        var tds = tr.querySelectorAll('td'); if (tds.length < 2) return;
        var cells = Array.prototype.map.call(tds, cellText);
        if (!cells[0]) return;
        var back = []; for (var k = 1; k < cells.length; k++) if (cells[k]) back.push({ l: heads[k] || '', v: cells[k] });
        if (!back.length) return;
        out.push({ id: title, key: title + '|' + cells[0], fl: heads[0] || '', front: cells[0], back: back });
      });
    });
    return out;
  }
  function shuffle(a) { for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
  function showCard() {
    var card = deck.querySelector('#card'), c = D.cards[D.i], total = D.cards.length;
    deck.querySelector('.prog').textContent = Math.min(D.i + 1, total) + ' / ' + total;
    if (!c) {
      var known = D.cards.filter(function (x) { return ST.su[x.key]; }).length;
      card.innerHTML = '<div class="front">Terminé</div><div class="tap">' + known + ' sur ' + total + ' connues</div>';
      deck.querySelector('.deck-btns').innerHTML = '<button class="restart">Revoir les cartes à revoir</button><button class="ok close">Fermer</button>'; return;
    }
    D.flipped = false;
    card.innerHTML = (c.fl ? '<div class="flab">' + esc(c.fl) + '</div>' : '') + '<div class="front">' + esc(c.front) + '</div><div class="tap">Touche pour voir la réponse</div>';
    deck.querySelector('.deck-btns').innerHTML = '<button class="again">À revoir</button><button class="ok">Je sais</button>';
  }
  function flip() {
    var c = D.cards[D.i]; if (!c) return; D.flipped = !D.flipped;
    var card = deck.querySelector('#card');
    card.innerHTML = (c.fl ? '<div class="flab">' + esc(c.fl) + '</div>' : '') + '<div class="front">' + esc(c.front) + '</div>' +
      (D.flipped ? '<div class="back">' + c.back.map(function (b) { return '<div>' + (b.l ? '<b>' + esc(b.l) + '</b>' : '') + esc(b.v) + '</div>'; }).join('') + '</div>' : '<div class="tap">Touche pour voir la réponse</div>');
  }
  function hideDeck() { deck.hidden = true; document.body.style.overflow = ''; if (window.__navHomeRefresh) window.__navHomeRefresh(); }
  function startDeck(sub, title, onlyTodo) {
    D.rv = false; var all = cardsFrom(sub, title);
    var list = onlyTodo ? all.filter(function (c) { return !ST.su[c.key]; }) : all;
    if (!list.length) { list = all; }
    D.cards = shuffle(list.slice()); D.i = 0; D.title = title; D.sub = sub; D.all = all;
    deck.querySelector('.ttl').textContent = title; if (deck.hidden) bkPush(hideDeck); deck.hidden = false; document.body.style.overflow = 'hidden'; showCard();
  }
  function startRv(id) {
    var list = Object.keys(ST.rv).map(function (k) { var c = ST.rv[k]; return { id: c.id, key: k, fl: c.fl, front: c.front, back: c.back }; }).filter(function (c) { return !id || c.id === id; });
    if (!list.length) return;
    D.cards = shuffle(list); D.i = 0; D.title = id && subMap[id] ? subMap[id].title + ' · à revoir' : 'Fiches à revoir'; D.sub = null; D.all = list; D.rv = id || true;
    deck.querySelector('.ttl').textContent = D.title; if (deck.hidden) bkPush(hideDeck); deck.hidden = false; document.body.style.overflow = 'hidden'; showCard();
  }
  function answer(ok) { var c = D.cards[D.i]; if (!c) return; if (ok) { ST.su[c.key] = 1; delete ST.rv[c.key]; } else { delete ST.su[c.key]; ST.rv[c.key] = { id: c.id, fl: c.fl, front: c.front, back: c.back }; } save(); D.i++; showCard(); }
  deck.addEventListener('click', function (e) {
    var b = e.target.closest('button');
    if (b) {
      if (b.classList.contains('x') || b.classList.contains('close')) bkClose(hideDeck);
      else if (b.classList.contains('again')) answer(false);
      else if (b.classList.contains('ok')) answer(true);
      else if (b.classList.contains('restart')) { if (D.rv) startRv(D.rv === true ? '' : D.rv); else startDeck(D.sub, D.title, true); }
      return;
    }
    if (e.target.closest('#card')) flip();
  });

