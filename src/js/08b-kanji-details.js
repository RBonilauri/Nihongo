  /* ═══ « Détails » des kanji d'une réponse (commun à tous les quiz) ═══ */
  var KDMAP = null;
  function kdetBind(m) { KDMAP = m; }
  function kdetMap() {
    if (!KDMAP) {
      KDMAP = {};
      try { JSON.parse(document.getElementById('kanji-data').textContent).forEach(function (x) { x.s = (x.s || '').replace(/\s*[(（][^)）]*[぀-鿿][^)）]*[)）]/g, '').trim(); KDMAP[x.k] = x; }); } catch (e) {}
    }
    return KDMAP;
  }
  function kdetParts(cell) { return String(cell || '').split(/[・･]/).map(function (p) { return p.replace(/[()（）]/g, '').trim(); }).filter(Boolean); }
  function kdetSay(y) { return kdetParts(y.on).concat(kdetParts(y.kun)); }
  function kdetSpk(y) { return '<button type="button" class="qsay2 kspk" aria-label="Écouter les lectures on et kun" title="Écouter" data-say=\'' + esc(JSON.stringify(kdetSay(y))) + '\'>🔊</button>'; }
  /* noms français des radicaux / éléments qui ne sont pas eux-mêmes des kanji de l'appli (noms usuels des radicaux) */
  var KRN = { '氵': 'eau', '亻': 'personne', '扌': 'main', '艹': 'herbe', '辶': 'chemin, marcher', '阝': 'colline / village', '宀': 'toit', '隹': 'oiseau (à courte queue)', '厶': 'privé', '冖': 'couvercle', '勹': 'envelopper', '尸': 'corps, cadavre', '夂': 'marcher lentement', '忄': 'cœur', '攵': 'frapper', '攴': 'frapper', '禾': 'céréale', '刂': 'couteau', '頁': 'tête, page', '冂': 'enceinte', '广': 'abri, bâtiment', '灬': 'feu', '彳': 'marcher', '犭': 'animal, chien', '罒': 'filet', '网': 'filet', '彡': 'poils, ornement', '几': 'table', '疒': 'maladie', '冫': 'glace', '卩': 'sceau', '厂': 'falaise', '囗': 'enclos', '礻': 'autel, esprit', '衤': 'vêtement', '彐': 'museau de porc', '儿': 'jambes', '凵': 'récipient ouvert', '艮': 'limite', '亠': 'couvercle', '匚': 'boîte', '戈': 'lance', '殳': 'arme', '戶': 'porte', '曰': 'dire', '歹': 'mort', '疋': 'pied', '虍': 'tigre', '幺': 'petit fil', '襾': 'couvrir', '豸': 'félin', '巛': 'rivière', '廴': 'allonger le pas', '廾': 'deux mains', '毋': 'ne pas', '豕': 'cochon', '靑': 'bleu', '麥': 'blé', '黑': 'noir', '匕': 'cuillère', '耒': 'charrue', '舛': 'opposés', '釆': 'discerner', '髟': 'cheveux', '韋': 'cuir', '黃': 'jaune', '黍': 'millet', '齒': 'dent', '鹵': 'sel', '气': 'vapeur', '爿': 'planche', '而': 'barbe', '尢': 'boiteux', '屮': 'pousse', '耂': 'vieillard', '聿': 'pinceau', '卜': 'divination', '匸': 'boîte cachée', '夊': 'marcher lentement', '弋': 'flèche à fil', '无': 'sans, ne pas', '爻': 'croiser', '癶': 'pieds écartés', '隶': 'atteindre', '鬯': 'vin sacrificiel' };
  /* « Mots » : liste rangée (mot · lecture · sens) */
  function kdetWords(y) {
    var l = (y.kw || []).slice(0, 4); if (!l.length) return '';
    return '<div class="fbwl"><b>Mots</b>' + l.map(function (w) { return '<div class="fbwr"><span class="fbwj">' + esc(w[0]) + '</span><span class="fbwy">' + esc(w[1]) + '</span><span class="fbwm">' + esc(w[2]) + '</span></div>'; }).join('') + '</div>';
  }
  /* « Composants » : menu déroulant radical + éléments (source CJKVI-IDS / KANJIDIC2), '' s'il n'y a rien */
  function kdetComp(y) {
    var cp = y.cp; if (!cp || (!cp[0] && !cp[1])) return '';
    var M = kdetMap();
    function one(c, r) { var m = M[c] && M[c].s ? M[c].s.split(/[,;，、]/)[0].trim() : (KRN[c] || ''); return '<span class="fbcc' + (r ? ' fbcrad' : '') + '"' + (r ? ' title="Radical"' : '') + '><b>' + esc(c) + '</b>' + (m ? '<i>' + esc(m) + '</i>' : '') + '</span>'; }
    return '<details class="fbc"><summary>Composants</summary>' + (cp[0] ? '<div class="fbcr"><span class="fbcl">Radical</span>' + one(cp[0], 1) + (cp[2] ? '<span class="fbcv">forme réduite de ' + esc(cp[2]) + '</span>' : '') + '</div>' : '') + (cp[1] ? '<div class="fbcr"><span class="fbcl">Kanji</span>' + cp[1].split('').map(function (c) { return one(c); }).join('<span class="fbcp">+</span>') + '</div>' : '') + '</details>';
  }
  /* HTML de la rubrique déroulante pour les kanji de `text` (hors `skip`), '' s'il n'y en a aucun */
  function kdetHtml(text, skip) {
    var M = kdetMap(), seen = {}, oth = String(text || '').split('').filter(function (c) { if (c === skip || seen[c] || !M[c]) return false; return (seen[c] = 1); }).slice(0, 12);
    if (!oth.length) return '';
    return '<details class="fbd"><summary>Détails · ' + (skip ? (oth.length > 1 ? 'les autres kanji' : 'l’autre kanji') : (oth.length > 1 ? 'les kanji' : 'le kanji')) + ' (' + esc(oth.join(' ')) + ')</summary>' + oth.map(function (c) {
      var y = M[c];
      return '<div class="fbd-k"><div class="fbkr"><div class="fbk">' + esc(y.k) + '</div><span class="lvp lv-' + esc(y.l) + '">' + esc(y.l) + '</span>' + kdetSpk(y) + '</div><div class="fbi"><div><b>On</b> ' + esc(y.on || '—') + '</div><div><b>Kun</b> ' + esc(y.kun || '—') + '</div><div><b>Sens</b> ' + esc(y.s) + '</div>' + '</div>' + kdetComp(y) + kdetWords(y) + '</div>';
    }).join('') + '</details>';
  }
  /* ajoute la rubrique à un encadré de correction (.q-fb) des quiz hors kanji, d'après les kanji de la réponse affichée */
  function kdetAdd(host) {
    var fb = host && host.querySelector('.q-fb'); if (!fb || fb.querySelector('.fbd')) return;
    var c = fb.cloneNode(true); c.querySelectorAll('.fbh,.fbb,.vq-ex,.jm-mini,.vq-tr,.cq-row,.cq-det,.fbd').forEach(function (n) { n.remove(); });
    var h = kdetHtml(c.textContent, ''), bar = fb.querySelector('.fbb');
    if (h && bar) bar.insertAdjacentHTML('beforebegin', h);
  }
  document.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('.qsay2'); if (!b) return;
    try { speak(JSON.parse(b.dataset.say)); } catch (x) {}
  });
