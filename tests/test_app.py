"""Tests de non-régression de l'application (navigateur mobile simulé).
Lancer :  python3 tests/test_app.py   (ou  make test)   — sort avec un code ≠ 0 en cas d'échec."""
import os, sys
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP = os.environ.get('APP') or 'file://' + os.path.join(ROOT, 'index.html')
fails, errs = [], []

def check(cond, msg):
    print(('  ok   ' if cond else '  ÉCHEC ') + msg)
    if not cond: fails.append(msg)

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True)
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.add_init_script("window.speechSynthesis.speak=function(){};")
    pg.add_init_script("document.addEventListener('DOMContentLoaded',function(){window.__v=getComputedStyle(document.querySelector('main')).visibility})")
    pg.goto(APP); pg.wait_for_timeout(900)
    print('Démarrage')
    check(pg.evaluate('window.__v') == 'hidden', 'contenu masqué pendant le chargement (%s)' % pg.evaluate('window.__v'))
    check(pg.evaluate("getComputedStyle(document.querySelector('main')).visibility") == 'visible' and not pg.evaluate("document.documentElement.classList.contains('boot')"), 'contenu visible une fois prêt')
    title = lambda: pg.evaluate("document.querySelector('.tb-title').textContent")

    print('Navigation')
    check(pg.evaluate("document.querySelectorAll('#tabbar button').length") == 4, 'barre de 4 onglets')
    check(pg.is_hidden('#tb-back'), 'pas de bouton retour sur l’accueil')
    pg.click('#tabbar [data-tab=learn]')
    poles = pg.evaluate("[...document.querySelectorAll('.npole[data-p]')].map(e=>e.dataset.p)")
    check(len(poles) == 4, '4 pôles : %s' % poles)
    n_sub = n_empty = 0
    for pole in poles:
        pg.click('#tabbar [data-tab=learn]'); pg.click('.npole[data-p=%s]' % pole)
        secs = pg.evaluate("[...document.querySelectorAll('.nsec')].map(e=>e.dataset.sj)")
        for sj in secs:
            pg.click('.nsec[data-sj="%s"]' % sj)
            if pg.evaluate("!!document.querySelector('.sec.cur details.sub.cur')"):
                if pg.evaluate("document.querySelector('.sec.cur details.sub.cur').innerText.length") < 30: n_empty += 1
                n_sub += 1; pg.click('#tb-back'); continue
            ids = pg.evaluate("[...document.querySelectorAll('.sec.cur .nsub')].map(e=>e.dataset.id)")
            if not ids and pg.evaluate("document.querySelector('.sec.cur').innerText.length") < 50: n_empty += 1
            for i in ids:
                pg.click('.sec.cur .nsub[data-id="%s"]' % i)
                if pg.evaluate("document.querySelector('.sec.cur details.sub.cur').innerText.length") < 30: n_empty += 1; print('   page vide :', i, title())
                n_sub += 1
                pg.click('#tb-back')
            pg.click('#tb-back')
    check(n_sub > 100 and n_empty == 0, '%d sous-rubriques ouvertes, %d vide(s)' % (n_sub, n_empty))

    print('Retour après un long défilement')
    pg.click('#tabbar [data-tab=learn]'); pg.click('.npole[data-p=voc]'); pg.click('.nsec[data-sj=常用]')
    pg.evaluate("window.scrollTo(0, 60000)"); pg.wait_for_timeout(200)
    pg.go_back(); pg.wait_for_timeout(600)
    check(pg.evaluate("window.scrollY") == 0 and 'Vocabulaire' in title(), 'retour du téléphone : page en haut')

    print('Carte')
    pg.click('.npole[data-p=voc]') if False else None
    pg.click('#tabbar [data-tab=learn]'); pg.click('.npole[data-p=voc]'); pg.click('.nsec[data-sj=地理]'); pg.click('.sec.cur .nsub >> nth=0'); pg.wait_for_timeout(300)
    check(pg.evaluate("document.querySelectorAll('.jm-svg .jm-p').length") == 47, '47 préfectures dessinées')
    pg.evaluate("document.querySelector('.jm-p[data-n=\"京都\"]').dispatchEvent(new MouseEvent('click',{bubbles:true}))")
    check('Kyōto' in pg.evaluate("document.querySelector('#jm-card').innerText"), 'fiche de préfecture affichée')

    print('Recherche')
    pg.click('#tabbar [data-tab=search]'); pg.wait_for_timeout(300); pg.fill('#q', 'mamoru'); pg.wait_for_timeout(400)
    check(pg.evaluate("document.querySelectorAll('.res').length") > 0, 'la recherche trouve « mamoru »')
    pg.click('.res >> nth=0'); pg.wait_for_timeout(800)
    check('Verbes' in title() or '語彙' in title(), 'un résultat ouvre la bonne page')

    print('Recherche avancée')
    def hits(txt):
        pg.fill('#q', ''); pg.fill('#q', txt); pg.wait_for_timeout(450)
        return pg.evaluate("document.querySelectorAll('.res').length")
    pg.click('#tabbar [data-tab=search]'); pg.wait_for_timeout(300)
    check(hits('eau') > 0 and hits('éau') > 0, 'accents indifférents')
    check(hits('toukyou') > 0, 'romaji « toukyou » trouve')
    check(hits('particules') > 0 and hits('particule') > 0, 'singulier / pluriel')
    check(hits('conjugasion') > 0, 'faute de frappe corrigée (« conjugasion »)')
    check(hits("l'eau") > 0, 'élision « l\'eau »')
    pg.click('.res >> nth=0'); pg.wait_for_timeout(700)
    pg.click('#tabbar [data-tab=search]'); pg.wait_for_timeout(300); pg.fill('#q', ''); pg.wait_for_timeout(200)
    check(pg.evaluate("!document.getElementById('shist').hidden && document.querySelectorAll('#shist .chip').length") >= 1, 'recherches récentes affichées')
    # filtre par rubrique
    pg.fill('#q', 'eau'); pg.wait_for_timeout(450)
    tot = pg.evaluate("document.querySelectorAll('#results .res:not(.more)').length")
    chips = pg.evaluate("[...document.querySelectorAll('#scopes .chip')].map(c=>[c.dataset.sc, c.textContent])")
    check(len(chips) >= 10, 'filtre : %d rubriques proposées' % len(chips))
    target = pg.evaluate("(()=>{const c=[...document.querySelectorAll('#scopes .chip')].find(c=>c.dataset.sc&&!c.classList.contains('zero'));return c&&c.dataset.sc})()")
    pg.click('#scopes .chip[data-sc="%s"]' % target); pg.wait_for_timeout(300)
    sub = pg.evaluate("document.querySelectorAll('#results .res:not(.more)').length")
    check(0 < sub <= tot and pg.evaluate("document.querySelector('#scopes .chip.on').dataset.sc") == target, 'filtre « %s » : %d résultat(s) sur %d' % (target, sub, tot))
    pg.click('#scopes .chip[data-sc=""]'); pg.wait_for_timeout(300)
    check(pg.evaluate("document.querySelectorAll('#results .res:not(.more)').length") == tot, 'filtre « Tout » rétabli')
    pg.fill('#q', 'a'); pg.wait_for_timeout(450)
    check(pg.evaluate("!!document.querySelector('#results .more')"), 'bouton « Afficher plus » sur une recherche large')
    pg.fill('#q', ''); pg.wait_for_timeout(200)
    check(pg.is_hidden('#tb-back'), 'page Recherche : pas de flèche retour')
    pg.click('.nstats') if False else pg.click('#tabbar [data-tab=home]'); pg.wait_for_timeout(300)

    print('Quiz')
    pg.click('#tabbar [data-tab=quiz]'); pg.wait_for_timeout(200)
    cards = pg.evaluate("[...document.querySelectorAll('.quizlist .quizcard')].map(e=>e.querySelector('.qc-t').firstChild.textContent)")
    check(len(cards) >= 7, '%d quiz : %s' % (len(cards), cards))
    for k, name in enumerate(cards):
        pg.evaluate("document.querySelectorAll('.quizlist .quizcard')[%d].click()" % k); pg.wait_for_timeout(250)
        Q = '.quiz:not([hidden])'
        go = pg.query_selector(Q + ' .qgo')
        ok = go is not None and not go.is_disabled()
        if ok:
            go.click(); pg.wait_for_timeout(200)
            for _ in range(6):
                if not pg.query_selector(Q + ' .qopt'): break
                pg.evaluate("document.querySelector('%s .qopt').click()" % Q); pg.wait_for_timeout(80)
                pg.evaluate("(document.querySelector('%s .q-fb .qgo')||{click(){}}).click()" % Q); pg.wait_for_timeout(80)
        check(ok, 'quiz « %s » : lancement et questions' % name)
        pg.evaluate("document.querySelector('.quiz:not([hidden]) .x').click()"); pg.wait_for_timeout(150)

    print('Statistiques des quiz')
    dayn = lambda: pg.evaluate("(JSON.parse(localStorage.getItem('jp-state')).day||{}).n||0")
    pg.click('#tabbar [data-tab=quiz]'); pg.wait_for_timeout(200)
    names = pg.evaluate("[...document.querySelectorAll('.quizlist .quizcard')].map(e=>e.querySelector('.qc-t').firstChild.textContent)")
    for k, name in enumerate(names):
        if 'général' in name: continue
        pg.evaluate("document.querySelectorAll('.quizlist .quizcard')[%d].click()" % k); pg.wait_for_timeout(250)
        Q = '.quiz:not([hidden])'
        pg.evaluate("document.querySelector('%s .q-body').scrollTop = 400" % Q)
        pg.evaluate("document.querySelector('%s .qstat-btn').click()" % Q); pg.wait_for_timeout(200)
        top = pg.evaluate("document.querySelector('%s .q-body').scrollTop" % Q)
        extra = pg.evaluate("document.querySelectorAll('%s .q-stats .pg-card').length" % Q)
        check(top == 0 and extra >= 1, '« %s » : stats en haut de page, avec avancement (scroll=%s)' % (name, top))
        pg.evaluate("document.querySelector('%s .x').click()" % Q); pg.wait_for_timeout(150)
    n0 = dayn()
    pg.evaluate("[...document.querySelectorAll('.quizlist .quizcard')].filter(e=>e.textContent.includes('général'))[0].click()"); pg.wait_for_timeout(300)
    pg.evaluate("document.querySelector('.quiz:not([hidden]) .qgo').click()"); pg.wait_for_timeout(300)
    for _ in range(3):
        pg.evaluate("document.querySelector('.quiz:not([hidden]) .qopt').click()"); pg.wait_for_timeout(80)
        pg.evaluate("(document.querySelector('.quiz:not([hidden]) .q-fb .qgo')||{click(){}}).click()"); pg.wait_for_timeout(80)
    check(dayn() - n0 == 3, 'quiz général : 3 réponses = +3 au compteur du jour (%d)' % (dayn() - n0))
    pg.evaluate("document.querySelector('.quiz:not([hidden]) .x').click()"); pg.wait_for_timeout(150)
    # la géographie est bien sauvegardée après rechargement
    pg.reload(); pg.wait_for_timeout(800)
    gq = pg.evaluate("Object.keys(JSON.parse(localStorage.getItem('jp-state')).gq||{}).length")
    check(gq > 0, 'progression géographie conservée après rechargement (%d)' % gq)

    print('Tri des plus ratés')
    import json as _j
    kq = {k: {'n': n, 'st': 0, 'w': True, 'x': x} for k, (x, n) in zip('一二三四五六七八', [(2, 2), (1, 5), (2, 4), (1, 1), (2, 3), (1, 2), (3, 3), (1, 3)])}
    st0 = pg.evaluate("localStorage.getItem('jp-state')")
    pg.evaluate("s=>localStorage.setItem('jp-state',s)", _j.dumps(dict(_j.loads(st0), kq=kq))); pg.reload(); pg.wait_for_timeout(800)
    pg.click('#tabbar [data-tab=quiz]'); pg.evaluate("document.querySelectorAll('.quizlist .quizcard')[0].click()"); pg.wait_for_timeout(300)
    pg.evaluate("document.querySelector('.quiz:not([hidden]) .qstat-btn').click()"); pg.wait_for_timeout(300)
    order = pg.evaluate("[...document.querySelectorAll('.quiz:not([hidden]) .q-miss .qs-cnt')].map(e=>e.textContent)")
    check(order == ['3 / 3', '2 / 2', '2 / 3', '2 / 4', '1 / 1', '1 / 2', '1 / 3', '1 / 5'], 'ordre erreurs puis taux : %s' % order)
    check(pg.evaluate("document.querySelectorAll('.quiz:not([hidden]) .q-stats > .q-miss-list .q-miss').length") == 5 and pg.evaluate("!!document.querySelector('.quiz:not([hidden]) details.q-more')"), '5 visibles + menu déroulant pour le reste')
    pg.evaluate("document.querySelector('.quiz:not([hidden]) .x').click()"); pg.wait_for_timeout(150)
    pg.evaluate("s=>localStorage.setItem('jp-state',s)", st0); pg.reload(); pg.wait_for_timeout(800)

    print('Traduction des formes verbales')
    pg.click('#tabbar [data-tab=quiz]'); pg.wait_for_timeout(200)
    pg.evaluate("[...document.querySelectorAll('.quizlist .quizcard')].filter(e=>e.textContent.includes('conjugaison'))[0].click()"); pg.wait_for_timeout(300)
    pg.evaluate("document.querySelector('.quiz:not([hidden]) .qgo').click()"); pg.wait_for_timeout(300)
    pg.evaluate("document.querySelector('.quiz:not([hidden]) .qopt').click()"); pg.wait_for_timeout(200)
    check(pg.evaluate("!!document.querySelector('.quiz:not([hidden]) #g-tr') && document.querySelector('.quiz:not([hidden]) #g-trb').hidden"), 'bouton « Traduction » présent, traduction masquée')
    pg.evaluate("document.querySelector('.quiz:not([hidden]) #g-tr').click()"); pg.wait_for_timeout(150)
    trt = pg.evaluate("document.querySelector('.quiz:not([hidden]) #g-trb').innerText")
    check(not pg.evaluate("document.querySelector('.quiz:not([hidden]) #g-trb').hidden") and '«' in trt, 'traduction révélée : %s' % trt.replace('\n', ' | ')[:80])
    check(not pg.is_visible('.quiz:not([hidden]) #g-tr'), 'le bouton « Traduction » disparaît une fois la traduction affichée')
    pg.evaluate("document.querySelector('.quiz:not([hidden]) .x').click()"); pg.wait_for_timeout(150)
    # fiche « Conjuguer »
    pg.evaluate("document.querySelector('details.cjd[data-k=食べる]').open = true"); pg.wait_for_timeout(300)
    n_fr = pg.evaluate("document.querySelectorAll('details.cjd[data-k=食べる] .cj-fr').length")
    check(n_fr >= 15, 'fiche « Conjuguer » : %d traductions pour 食べる' % n_fr)
    ex = pg.evaluate("[...document.querySelectorAll('details.cjd[data-k=食べる] .cj-fr')].slice(0,3).map(e=>e.textContent)")
    check(any('mange' in e for e in ex), 'exemple : %s' % ex)

    print('Objectif du jour')
    st = pg.evaluate("JSON.parse(localStorage.getItem('jp-state')).day")
    check(st and st['n'] >= 6, 'les réponses de quiz sont comptées (%s)' % st)
    pg.click('#tabbar [data-tab=home]'); pg.wait_for_timeout(200)
    check(pg.evaluate("!!document.querySelector('.nday .nd-bar i')"), 'carte objectif du jour sur l’accueil')
    check(pg.evaluate("(document.querySelector('.nday .nd-h span')||{}).textContent") .startswith('%d / 20' % min(st['n'], 20)), 'compteur affiché cohérent')

    print('Quiz vocabulaire : sous-rubriques')
    pg.click('#tabbar [data-tab=quiz]'); pg.wait_for_timeout(300)
    pg.evaluate("[...document.querySelectorAll('.quizlist .quizcard')].find(c=>/Quiz vocabulaire/.test(c.textContent)).click()"); pg.wait_for_timeout(400)
    check(pg.evaluate("!!document.querySelector('#v-sub')"), 'menu « Sous-rubriques » visible quand Vocabulaire est coché')
    pg.click('.quiz:not([hidden]) [data-n="0"]'); pg.wait_for_timeout(150)
    nAll = pg.evaluate("+document.querySelector('#v-go').textContent.match(/Lancer · (\\d+)/)[1]")
    pg.click('#v-sub summary'); pg.click('#v-sub [data-vsnone]'); pg.wait_for_timeout(200)
    n0 = pg.evaluate("+document.querySelector('#v-go').textContent.match(/Lancer · (\\d+)/)[1]")
    pg.click('#v-sub [data-vs="Vocabulaire:家族"]'); pg.click('.quiz:not([hidden]) [data-n="0"]'); pg.wait_for_timeout(200)
    n1 = pg.evaluate("+document.querySelector('#v-go').textContent.match(/Lancer · (\\d+)/)[1]")
    pg.click('#v-sub [data-vsall]'); pg.wait_for_timeout(200)
    check(pg.evaluate("document.querySelector('#v-sub').open") and n0 < n1 < nAll, 'sous-rubriques : aucune %d < Famille %d < toutes %d questions' % (n0, n1, nAll))
    pg.click('.quiz:not([hidden]) .x'); pg.wait_for_timeout(300)

    print('Compte à rebours')
    pg.click('#tabbar [data-tab=home]'); pg.wait_for_timeout(200)
    check(pg.evaluate("!!document.querySelector('.ntrip [data-act=trip-set]')"), 'sans date : invitation à choisir la date')
    pg.click('#menu'); pg.wait_for_timeout(400)
    pg.fill('#trip-date', '2099-01-01'); pg.dispatch_event('#trip-date', 'change'); pg.wait_for_timeout(300)
    pg.click('#dr-close'); pg.wait_for_timeout(400)
    check(pg.evaluate("(document.querySelector('.ntrip .tr-n b')||{}).textContent||''").startswith('J-') and pg.evaluate("!!document.querySelector('.ntrip .tr-plane')"), 'date choisie : J-xxx et avion affichés')
    pg.click('#menu'); pg.wait_for_timeout(400); pg.click('#sw-trip'); pg.click('#dr-close'); pg.wait_for_timeout(400)
    check(pg.evaluate("!document.querySelector('.ntrip')"), 'option « masquer » : la carte disparaît')
    pg.click('#menu'); pg.wait_for_timeout(400); pg.click('#sw-trip'); pg.click('#trip-clear'); pg.click('#dr-close'); pg.wait_for_timeout(300)

    print('Ma progression')
    pg.click('#tabbar [data-tab=home]'); pg.wait_for_timeout(200)
    pg.click('.nstats'); pg.wait_for_timeout(300)
    check('progression' in title().lower(), 'page « Ma progression » ouverte')
    check(pg.evaluate("document.querySelectorAll('.pg-card').length") == 6 and pg.evaluate("document.querySelectorAll('.pg-week:not(.pg-mini) .pg-d').length") == 7, '6 quiz et 7 jours affichés')
    check(pg.evaluate("document.querySelectorAll('.pg-det .pg-sub').length") == 6 and pg.evaluate("!document.querySelector('.pg-det').open"), 'volet « Détails par quiz » : 6 graphiques, replié par défaut')
    check(pg.evaluate("document.querySelector('.pg-sum b').textContent") != '0', 'réponses totales comptées')
    pg.click('#tb-back'); pg.wait_for_timeout(300)
    check('Référence' in title() or 'REF' in title().upper(), 'retour à l’accueil')

    print('Réponses non évidentes')
    leak = pg.evaluate("""() => { const v = JSON.parse(document.getElementById('vocab-data').textContent);
        const strip = s => String(s).replace(/\\s*[（(][^）)]*[぀-ヿ㐀-鿿][^）)]*[）)]/g, '').trim();
        const all = []; (function w(o){ if (Array.isArray(o)) o.forEach(w); else if (o && typeof o === 'object') { if (typeof o.fr === 'string') all.push(o.fr); Object.values(o).forEach(w); } })(v);
        return all.filter(f => !strip(f)).length; }""")
    check(leak == 0, 'aucune traduction française vide une fois les indices japonais retirés (%s)' % leak)

    print('Grammaire N4 / N3')
    gn = pg.evaluate("""() => ['N4','N3'].map(j => { const s = [...document.querySelectorAll('main > details.sec')].find(d => d.querySelector(':scope > summary .jp').textContent.trim() === j); return s ? [s.querySelectorAll(':scope > .sec-body > details.sub').length, s.querySelectorAll('tbody tr').length] : null; })""")
    check(gn[0] and gn[1] and gn[0][0] >= 8 and gn[1][0] >= 8 and gn[0][1] >= 60 and gn[1][1] >= 70, 'pages Grammaire N4 et N3 présentes %s' % gn)
    check(pg.evaluate("[...document.querySelectorAll('.quizcard')].length") >= 6, 'quiz inchangés')

    print('Exemples de verbes')
    ex = pg.evaluate("""() => { let n = 0, bad = 0; document.querySelectorAll('details.exd').forEach(d => { d.open = true; d.dispatchEvent(new Event('toggle')); n++; if (d.querySelectorAll('.ex-s').length < 2) bad++; });
        return [n, bad, document.querySelectorAll('details.vgrp').length]; }""")
    check(ex[0] >= 300 and ex[1] == 0 and ex[2] >= 10, 'exemples (>=2 phrases par verbe) et rubriques repliables %s' % ex)
    ex2 = pg.evaluate("""() => { let n = 0, same = 0; document.querySelectorAll('details.exd').forEach(d => { if (!d.dataset.ex2) return; n++; const a = JSON.parse(d.dataset.ex), b = JSON.parse(d.dataset.ex2); if (a[0] === b[0] && a[3] === b[3]) same++; }); return [n, same]; }""")
    check(ex2[0] >= 380 and ex2[1] == 0, 'chaque verbe a une 2e phrase au contexte différent %s' % ex2)

    print('Écoute ciblée')
    pg.evaluate("""() => { window.__said = []; window.SpeechSynthesisUtterance = function (t) { window.__said.push(t); }; speechSynthesis.speak = () => {}; speechSynthesis.cancel = () => {};
        document.querySelector('.fab').click();
        const d = document.querySelector('details.cjd'); d.open = true; d.dispatchEvent(new Event('toggle')); const e = document.querySelector('details.exd'); e.open = true; e.dispatchEvent(new Event('toggle'));
        window.__a = d.querySelector('.cj-row:not(.cj-h) > span:not(.cj-l) .cj-j'); window.__b = e.querySelector('.ex-s'); window.__a.dispatchEvent(new MouseEvent('click', { bubbles: true })); }""")
    pg.wait_for_timeout(300)
    pg.evaluate("() => window.__b.querySelector('.ex-fr').dispatchEvent(new MouseEvent('click', { bubbles: true }))"); pg.wait_for_timeout(300)
    said = pg.evaluate("() => [window.__said, window.__a.textContent, window.__b.querySelector('.ex-jp').textContent.replace('。', '')]")
    pg.evaluate("document.querySelector('.fab').click()")
    check(said[0] == [said[1], said[2]], 'écoute : une conjugaison / un exemple = une seule lecture %s' % said)

    print('Menu Kanji un par un')
    kj = pg.evaluate("""() => { let n = 0, miss = [], wrong = 0; document.querySelectorAll('details.kjd').forEach(d => { d.open = true; d.dispatchEvent(new Event('toggle')); n++;
        const cs = [...new Set(d.dataset.w.match(/[一-鿿]/g))]; const rs = [...d.querySelectorAll('.kj-r')];
        if (rs.length !== cs.length) wrong++; rs.forEach(r => { if (r.querySelector('.kj-m').textContent.trim() === '—') miss.push(r.querySelector('.kj-c').textContent); }); });
        return [n, wrong, miss.slice(0, 10)]; }""")
    check(kj[0] >= 700 and kj[1] == 0 and not kj[2], 'chaque mot à plusieurs kanji a son menu, chaque kanji a un sens %s' % kj)

    print('Écoute : alternative')
    def ear_run(silent, name):
        pg.evaluate("s=>{const o=JSON.parse(localStorage.getItem('jp-state')||'{}'); o.silent=s; localStorage.setItem('jp-state',JSON.stringify(o));}", silent); pg.reload(); pg.wait_for_timeout(600)
        pg.click('#tabbar [data-tab=quiz]')
        pg.evaluate("n=>[...document.querySelectorAll('.quizlist .quizcard')].filter(e=>e.textContent.includes(n))[0].click()", name); pg.wait_for_timeout(250)
        Q = '.quiz:not([hidden])'; go = pg.query_selector(Q + ' .qgo'); e = a = 0
        if go and not go.is_disabled():
            go.click(); pg.wait_for_timeout(200)
            for _ in range(12):
                if not pg.query_selector(Q + ' .qopt'): break
                if pg.query_selector(Q + ' .vq-ear'):
                    e += 1; a += 1 if pg.query_selector(Q + ' .ear-alt .ear-show') else 0
                pg.evaluate("document.querySelector('%s .qopt').click()" % Q); pg.wait_for_timeout(30)
                pg.evaluate("(document.querySelector('%s .fbb .qgo')||{click(){}}).click()" % Q); pg.wait_for_timeout(30)
        return e, a
    r_s = [ear_run(True, n) for n in ('vocabulaire', 'compteurs', 'géographie')]
    r_n = [ear_run(False, n) for n in ('vocabulaire', 'compteurs', 'géographie')]
    check(all(x[0] == 0 for x in r_s), 'mode silencieux : aucune question d’écoute %s' % r_s)
    check(sum(x[0] for x in r_n) > 0 and all(x[0] == x[1] for x in r_n), 'écoute normale : « Voir le texte » toujours proposé %s' % r_n)
    pg.evaluate("s=>{const o=JSON.parse(localStorage.getItem('jp-state')||'{}'); o.silent=false; localStorage.setItem('jp-state',JSON.stringify(o));}", False)

    print('Données')
    counts = pg.evaluate("""() => ({ kanji: JSON.parse(document.getElementById('kanji-data').textContent).length,
        vocab: JSON.parse(document.getElementById('vocab-data').textContent).length,
        verbes: JSON.parse(document.getElementById('grammar-data').textContent).verbs.length })""")
    check(counts['kanji'] > 600 and counts['vocab'] > 2000 and counts['verbes'] > 300, 'données présentes : %s' % counts)

    check(not errs, 'aucune erreur JavaScript %s' % errs[:2])
    b.close()
print('\n%s' % ('TOUT PASSE' if not fails else '%d ÉCHEC(S)' % len(fails)))
sys.exit(1 if fails else 0)
