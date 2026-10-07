  /* ── écoute (synthèse vocale japonaise) ── */
  var JP = /[぀-ヿ㐀-鿿々〜ー]+/g, listening = false, voice = null;
  var fab = document.createElement('button'); fab.className = 'fab'; fab.setAttribute('aria-label', 'Mode écoute'); fab.textContent = '🔊';
  function pickVoice() { var vs = window.speechSynthesis ? speechSynthesis.getVoices() : []; voice = vs.filter(function (v) { return /^ja/i.test(v.lang); })[0] || null; }
  var speakTok = 0;
  function speak(parts) {
    if (!window.speechSynthesis) return;
    var tok = ++speakTok, i = 0;
    try { speechSynthesis.cancel(); } catch (e) {}
    function next() {
      if (tok !== speakTok || i >= parts.length) return;
      var text = parts[i++], done = false;
      function advance() { if (done || tok !== speakTok) return; done = true; setTimeout(next, 500); }
      var u = new SpeechSynthesisUtterance(text); u.lang = 'ja-JP'; if (voice) u.voice = voice; u.rate = 0.85;
      u.onend = advance; u.onerror = advance;
      setTimeout(advance, 3000 + text.length * 450); // sécurité si onend n'arrive jamais
      try { speechSynthesis.resume(); } catch (e) {}
      speechSynthesis.speak(u);
    }
    setTimeout(next, 80); // laisse cancel() se terminer avant de relancer (bug Chrome Android)
  }
  if (window.speechSynthesis) { pickVoice(); speechSynthesis.onvoiceschanged = pickVoice; }
  document.body.appendChild(fab);
  fab.addEventListener('click', function () {
    listening = !listening; fab.classList.toggle('on', listening); document.documentElement.classList.toggle('listen', listening);
    toast(listening ? 'Mode écoute : touche un texte japonais pour l\'entendre.' : 'Mode écoute désactivé.');
    if (listening && window.speechSynthesis && !voice) { pickVoice(); if (!voice) toast('Aucune voix japonaise détectée : installe-la dans les réglages de synthèse vocale du téléphone.'); }
  });
  document.addEventListener('click', function (e) {
    if (!listening) return;
    if (e.target.closest('button, a, summary, .kjd, input, label, .fab, .res, .deck, .toast, .searchbar')) return;
    var one = e.target.closest('.cj-row:not(.cj-h) > span:not(.cj-l), .ex-s');
    if (one) { /* conjugaison / exemple : on lit uniquement la forme cliquée (pas la lecture en kana) */
      var jpEl = one.classList.contains('ex-s') ? one.querySelector('.ex-jp') : one.querySelector('.cj-j');
      if (!jpEl) return;
      var tx = jpEl.textContent.replace(/[。]/g, '').trim(); if (!tx) return;
      one.classList.add('speaking'); setTimeout(function () { one.classList.remove('speaking'); }, 1400);
      speak([tx]); return;
    }
    var el = e.target.closest('td, th, li, .example, .cec-sentence, .tc-ex, .dc-example, .kana, .cec-verb, .sd-cell, .gc-pill, .fs-arrow, p, .ex-answer .ex-body');
    if (!el) return;
    var clean = el.textContent.replace(/[(（]([\u3040-\u30ff\u3400-\u9fff々ー]+)[)）]/g, '$1');
    var m = clean.match(JP); if (!m) return;
    var parts = []; m.forEach(function (x) { x.split(/[・･]/).forEach(function (y) { y = y.replace(/^[、。]+|[、。]+$/g, ''); if (y) parts.push(y); }); }); parts = parts.slice(0, 8);
    el.classList.add('speaking'); setTimeout(function () { el.classList.remove('speaking'); }, 1400);
    speak(parts);
  });


  /* ── alternative à l’écoute (métro, bureau…) : texte à la demande + mode silencieux ── */
  function ctypes(a) { return ST.silent ? a.filter(function (t) { return t !== 'ear'; }) : a; }
  function earAlt(txt) { return '<div class="ear-alt"><button type="button" class="mini ear-show">👁 Voir le texte</button><button type="button" class="mini ear-off">🔇 Plus d’écoute</button><div class="ear-txt" hidden>' + esc(txt) + '</div></div>'; }
  document.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('.ear-show, .ear-off'); if (!b) return;
    var al = b.closest('.ear-alt'), t = al && al.querySelector('.ear-txt');
    if (b.classList.contains('ear-off')) { ST.silent = true; save(); toast('Mode silencieux activé : plus de questions d’écoute (réglable dans ⚙).'); if (t) t.hidden = false; b.disabled = true; try { speechSynthesis.cancel(); } catch (x) {} }
    else if (t) t.hidden = !t.hidden;
  });
