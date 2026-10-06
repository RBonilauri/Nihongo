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
    pg.goto(APP); pg.wait_for_timeout(900)
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
    pg.click('#tabbar [data-tab=learn]'); pg.click('.npole[data-p=voc]'); pg.click('.nsec[data-sj=語彙]')
    idx = pg.evaluate("[...document.querySelectorAll('.sec.cur .nsub')].findIndex(e=>e.textContent.includes('動詞'))")
    pg.click('.sec.cur .nsub >> nth=%d' % idx); pg.evaluate("window.scrollTo(0, 60000)"); pg.wait_for_timeout(200)
    pg.go_back(); pg.wait_for_timeout(600)
    check(pg.evaluate("window.scrollY") == 0 and 'Vocabulaire' in title(), 'retour du téléphone : page en haut')

    print('Carte')
    pg.click('.npole[data-p=voc]') if False else None
    pg.click('#tabbar [data-tab=learn]'); pg.click('.npole[data-p=voc]'); pg.click('.nsec[data-sj=地理]'); pg.click('.sec.cur .nsub >> nth=0'); pg.wait_for_timeout(300)
    check(pg.evaluate("document.querySelectorAll('.jm-svg .jm-p').length") == 47, '47 préfectures dessinées')
    pg.evaluate("document.querySelector('.jm-p[data-n=\"京都\"]').dispatchEvent(new MouseEvent('click',{bubbles:true}))")
    check('Kyōto' in pg.evaluate("document.querySelector('#jm-card').innerText"), 'fiche de préfecture affichée')

    print('Recherche')
    pg.click('#tabbar [data-srch]'); pg.wait_for_timeout(300); pg.fill('#q', 'mamoru'); pg.wait_for_timeout(400)
    check(pg.evaluate("document.querySelectorAll('.res').length") > 0, 'la recherche trouve « mamoru »')
    pg.click('.res >> nth=0'); pg.wait_for_timeout(800)
    check('Verbes' in title() or '語彙' in title(), 'un résultat ouvre la bonne page')

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

    print('Données')
    counts = pg.evaluate("""() => ({ kanji: JSON.parse(document.getElementById('kanji-data').textContent).length,
        vocab: JSON.parse(document.getElementById('vocab-data').textContent).length,
        verbes: JSON.parse(document.getElementById('grammar-data').textContent).verbs.length })""")
    check(counts['kanji'] > 600 and counts['vocab'] > 2000 and counts['verbes'] > 300, 'données présentes : %s' % counts)

    check(not errs, 'aucune erreur JavaScript %s' % errs[:2])
    b.close()
print('\n%s' % ('TOUT PASSE' if not fails else '%d ÉCHEC(S)' % len(fails)))
sys.exit(1 if fails else 0)
