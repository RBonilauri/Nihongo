  /* ── bouton « tout / aucun » sur les choix multiples des quiz ── */
  function selAllInit() {
    var MULTI = ['Rubriques', 'Régions', 'Types de questions', 'Contrastes', 'Formes de conjugaison', 'Catégories', 'Thèmes'];
    function secs(root) { return [].slice.call(root.querySelectorAll('.q-sec')).filter(function (sc) { var h = sc.querySelector('h4'); return h && MULTI.indexOf(h.firstChild.textContent.trim()) >= 0 && sc.querySelectorAll('.qchips .qchip').length > 1; }); }
    function chips(sc) { return [].slice.call(sc.querySelectorAll('.qchips .qchip')).filter(function (c) { return !c.disabled; }); }
    function decorate(body) {
      secs(body).forEach(function (sc, idx) {
        if (sc.querySelector('.qall')) return;
        var h = sc.querySelector('h4'), cs = chips(sc), all = cs.every(function (c) { return c.classList.contains('on'); });
        h.classList.add('q-h4all');
        var b = document.createElement('button'); b.type = 'button'; b.className = 'qall'; b.textContent = all ? 'Tout désélectionner' : 'Tout sélectionner';
        b.addEventListener('click', function () {
          var title = h.firstChild.textContent.trim(), target = !all, guard = 0;
          for (;;) {
            var cur = secs(body).filter(function (x) { return x.querySelector('h4').firstChild.textContent.trim() === title; })[0]; if (!cur) break;
            var next = chips(cur).filter(function (c) { return c.classList.contains('on') !== target; })[0];
            if (!next || guard++ > 60) break; next.click();
          }
        });
        h.appendChild(b);
      });
    }
    [].slice.call(document.querySelectorAll('.quiz .q-body')).forEach(function (body) {
      var busy = false, mo = new MutationObserver(function () { if (busy) return; busy = true; try { decorate(body); } finally { busy = false; } });
      mo.observe(body, { childList: true }); decorate(body);
    });
  }
