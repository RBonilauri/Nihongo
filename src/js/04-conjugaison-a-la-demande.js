  /* ── conjugaisons à la demande ── */
  var CJ_GO = { 'う': ['わ', 'い', 'え', 'お'], 'く': ['か', 'き', 'け', 'こ'], 'ぐ': ['が', 'ぎ', 'げ', 'ご'], 'す': ['さ', 'し', 'せ', 'そ'], 'つ': ['た', 'ち', 'て', 'と'], 'ぬ': ['な', 'に', 'ね', 'の'], 'ぶ': ['ば', 'び', 'べ', 'ぼ'], 'む': ['ま', 'み', 'め', 'も'], 'る': ['ら', 'り', 'れ', 'ろ'] };
  var CJ_TE = { 'う': ['って', 'った'], 'つ': ['って', 'った'], 'る': ['って', 'った'], 'く': ['いて', 'いた'], 'ぐ': ['いで', 'いだ'], 'す': ['して', 'した'], 'ぬ': ['んで', 'んだ'], 'ぶ': ['んで', 'んだ'], 'む': ['んで', 'んだ'] };
  var CJ_NO = { 'ある': 1, 'できる': 1, '分かる': 1, 'わかる': 1, '見える': 1, 'みえる': 1, '聞こえる': 1, 'きこえる': 1, '要る': 1, 'いる(要)': 1 };
  function cjForms(s, ty, kana) {
    var L = s.slice(-1), st = s.slice(0, -1), pre = s.slice(0, -2), a, i, e, o, te, ta, pot, pas, cau, vol, imp, ba;
    if (ty === 'suru') { a = pre + 'し'; i = pre + 'し'; te = pre + 'して'; ta = pre + 'した'; pot = pre + 'できる'; pas = pre + 'される'; cau = pre + 'させる'; vol = pre + 'しよう'; imp = pre + 'しろ'; ba = pre + 'すれば'; }
    else if (ty === 'irr') { var c = kana ? ['こ', 'き', 'くれ'] : ['来', '来', '来れ']; a = c[0]; i = c[1]; te = i + 'て'; ta = i + 'た'; pot = a + 'られる'; pas = a + 'られる'; cau = a + 'させる'; vol = a + 'よう'; imp = a + 'い'; ba = c[2] + 'ば'; }
    else if (ty === 'ru') { a = i = st; te = st + 'て'; ta = st + 'た'; pot = st + 'られる'; pas = st + 'られる'; cau = st + 'させる'; vol = st + 'よう'; imp = st + 'ろ'; ba = st + 'れば'; }
    else {
      var g = CJ_GO[L]; a = st + g[0]; i = st + g[1]; e = st + g[2]; o = st + g[3];
      var t = CJ_TE[L]; if (/(行く|いく)$/.test(s)) t = ['って', 'った'];
      te = st + t[0]; ta = st + t[1]; pot = e + 'る'; pas = a + 'れる'; cau = a + 'せる'; vol = o + 'う'; imp = e; ba = e + 'ば';
      if (s === 'ある' || s === 'あ' + 'る') { a = ''; }
    }
    var neg = function (v) { return v.slice(0, -1) + 'ない'; };
    var aru = (s === 'ある' || s === '有る');
    var dn = aru ? 'ない' : a + 'ない', dna = aru ? 'なかった' : a + 'なかった';
    var no = CJ_NO[s] || aru, R = [];
    R.push(['Poli', i + 'ます', i + 'ません']);
    R.push(['Poli, passé', i + 'ました', i + 'ませんでした']);
    R.push(['Neutre (dico)', s, dn]);
    R.push(['Neutre, passé', ta, dna]);
    R.push(['Forme て', te, aru ? 'なくて' : a + 'ないで']);
    R.push(['Envie (〜たい)', (aru || s === 'できる') ? '—' : i + 'たい', (aru || s === 'できる') ? '—' : i + 'たくない']);
    R.push(['Potentiel', no ? '—' : pot, no ? '—' : neg(pot)]);
    R.push(['Passif', no ? '—' : pas, no ? '—' : neg(pas)]);
    R.push(['Causatif', no ? '—' : cau, no ? '—' : neg(cau)]);
    R.push(['Volitif (on y va)', no ? '—' : vol, '—']);
    R.push(['Volitif poli', aru ? '—' : i + 'ましょう', '—']);
    R.push(['Impératif', no ? '—' : imp, no ? '—' : s + 'な']);
    R.push(['Conditionnel ば', aru ? 'あれば' : ba, aru ? 'なければ' : a + 'なければ']);
    R.push(['Conditionnel たら', ta + 'ら', dna + 'ら']);
    R.push(['En cours (〜ている)', aru ? '—' : te + 'いる', aru ? '—' : te + 'いない']);
    R.push(['Demande (〜ください)', aru ? '—' : te + 'ください', aru ? '—' : a + 'ないでください']);
    return R;
  }
  function cjFill(d) {
    var b = d.querySelector('.cjb'); if (!b || b.firstChild) return;
    var k = d.dataset.k, ka = d.dataset.ka, ty = d.dataset.t, A = cjForms(k, ty, false), B = k === ka ? null : cjForms(ka, ty, true);
    var h = '<div class="cj"><div class="cj-row cj-h"><span>Forme</span><span>Affirmatif</span><span>Négatif</span></div>';
    A.forEach(function (r, n) {
      var cell = function (j) { var v = r[j]; if (v === '—') return '<span>—</span>'; var kk = B && B[n][j] !== v ? '<span class="cj-r">' + B[n][j] + '</span>' : ''; return '<span><span class="cj-j">' + v + '</span>' + kk + '</span>'; };
      h += '<div class="cj-row"><span class="cj-l">' + r[0] + '</span>' + cell(1) + cell(2) + '</div>';
    });
    b.innerHTML = h + '</div><p class="cj-n">Les formes passif et causatif existent pour tous les verbes mais servent surtout avec des verbes d’action ; « — » = forme non utilisée.</p>';
  }
  document.addEventListener('toggle', function (e) { var d = e.target; if (d.matches && d.matches('details.cjd') && d.open) cjFill(d); }, true);

