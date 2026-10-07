  /* ── mode lecture (flou romaji / traductions) ── */
  document.addEventListener('click', function (e) {
    if (!document.documentElement.classList.contains('aid-hide')) return;
    var el = e.target.closest('.romaji, .cec-trans, .tc-trans, .dc-translation, .sd-translation, .cec-meaning'); if (el) el.classList.toggle('rv');
  });

  /* ── réglages ── */
  function applyPrefs() {
    document.documentElement.style.setProperty('--fs', ST.fs);
    document.documentElement.classList.toggle('aid-hide', !!ST.aid);
  }
  function buildSettings() {
    var aidB = document.getElementById('sw-aid'), recB = document.getElementById('sw-rec'), silB = document.getElementById('sw-silent'), fsv = document.getElementById('fs-val');
    function paint() {
      aidB.setAttribute('aria-checked', ST.aid ? 'true' : 'false');
      recB.setAttribute('aria-checked', ST.showRec ? 'true' : 'false');
      silB.setAttribute('aria-checked', ST.silent ? 'true' : 'false');
      fsv.textContent = Math.round(ST.fs * 100) + ' %';
    }
    paint();
    document.getElementById('fs-').addEventListener('click', function () { ST.fs = Math.max(0.8, Math.round((ST.fs - 0.1) * 100) / 100); save(); applyPrefs(); paint(); });
    document.getElementById('fs-val').addEventListener('click', function () { ST.fs = 1; save(); applyPrefs(); paint(); });
    document.getElementById('fs+').addEventListener('click', function () { ST.fs = Math.min(1.4, Math.round((ST.fs + 0.1) * 100) / 100); save(); applyPrefs(); paint(); });
    aidB.addEventListener('click', function () { ST.aid = !ST.aid; save(); applyPrefs(); paint(); });
    silB.addEventListener('click', function () { ST.silent = !ST.silent; save(); paint(); toast(ST.silent ? 'Mode silencieux : les quiz n’auront plus de questions d’écoute.' : 'Questions d’écoute réactivées.'); });
    recB.addEventListener('click', function () { ST.showRec = !ST.showRec; save(); renderHome(); paint(); });
    document.getElementById('rec-clear').addEventListener('click', function () { ST.rec = []; save(); renderHome(); toast('Historique vidé.'); });
    document.getElementById('exp').addEventListener('click', function () {
      var blob = new Blob([JSON.stringify(ST, null, 1)], { type: 'application/json' }), a = document.createElement('a');
      a.href = URL.createObjectURL(blob); a.download = 'japonais-progression.json'; document.body.appendChild(a); a.click(); a.remove();
    });
    document.getElementById('imp').addEventListener('change', function (e) {
      var f = e.target.files[0]; if (!f) return; var rd = new FileReader();
      rd.onload = function () { try { var o = JSON.parse(rd.result); Object.keys(ST).forEach(function (k) { if (o[k] !== undefined) ST[k] = o[k]; }); save(); applyPrefs(); renderHome(); syncFavButtons(); paint(); toast('Sauvegarde importée.'); } catch (err) { toast('Fichier invalide.'); } };
      rd.readAsText(f);
    });
    document.getElementById('rst').addEventListener('click', function () { ST.su = {}; save(); toast('Fiches remises à zéro.'); });
  }


