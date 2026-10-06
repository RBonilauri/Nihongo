  /* ── romaji → hiragana (pour la recherche) ── */
  var R = { a:'あ', i:'い', u:'う', e:'え', o:'お', ya:'や', yu:'ゆ', yo:'よ', wa:'わ', wo:'を', shi:'し', chi:'ち', tsu:'つ', fu:'ふ', ji:'じ', sha:'しゃ', shu:'しゅ', sho:'しょ', cha:'ちゃ', chu:'ちゅ', cho:'ちょ', ja:'じゃ', ju:'じゅ', jo:'じょ' };
  (function () {
    var rows = { k:'かきくけこ', g:'がぎぐげご', s:'さしすせそ', z:'ざじずぜぞ', t:'たちつてと', d:'だぢづでど', n:'なにぬねの', h:'はひふへほ', b:'ばびぶべぼ', p:'ぱぴぷぺぽ', m:'まみむめも', r:'らりるれろ' };
    var v = 'aiueo';
    Object.keys(rows).forEach(function (c) { for (var i = 0; i < 5; i++) { var key = c + v[i]; if (!R[key]) R[key] = rows[c][i]; } });
    R.si = 'し'; R.ti = 'ち'; R.tu = 'つ'; R.hu = 'ふ'; R.zi = 'じ';
    var sm = { a:'ゃ', u:'ゅ', o:'ょ' };
    'kgnhbpmr'.split('').forEach(function (c) { ['a', 'u', 'o'].forEach(function (x) { R[c + 'y' + x] = rows[c][1] + sm[x]; }); });
  })();
  function r2k(s) {
    if (!/^[a-z'-]+$/.test(s)) return null;
    var o = '', i = 0;
    while (i < s.length) {
      var c = s[i], n = s[i + 1];
      if (c === '-') { o += 'ー'; i++; continue; }
      if (c === 'n' && (n === undefined || n === "'" || (!/[aiueoy]/.test(n)))) { o += 'ん'; i += (n === "'" || n === 'n') ? 2 : 1; continue; }
      if (c === n && /[kgszjtdhbpmrwcf]/.test(c)) { o += 'っ'; i++; continue; }
      var hit = null;
      for (var L = 3; L >= 1 && !hit; L--) { var seg = s.substr(i, L); if (R[seg]) { hit = seg; } }
      if (!hit) return null;
      o += R[hit]; i += hit.length;
    }
    return o;
  }

