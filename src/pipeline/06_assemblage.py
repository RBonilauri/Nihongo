# Assemblage final : romaji, JS, en-tête, écriture de index.html
# Exécuté par build.py dans un espace de noms partagé.
print('grammar verbs', len(_GV), 'forms', sum(len(v['f']) for v in _GV.values()), 'parts', len(_PARTS))

main = add_romaji(main)
main = search_html + main
# searchbar must sit after the header so it sticks at the very top of main: keep as first child

js = _cat_files('js', sorted(f for f in os.listdir(os.path.join(HERE, 'js')) if f.endswith('.js')))

head = '''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Japonais Référence</title>
<meta name="theme-color" content="#1c1510">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="日本語">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<script>try{var t=localStorage.getItem("jp-theme");document.documentElement.setAttribute("data-theme",t==="dark"||t==="light"?t:(t==="auto"?"":"light"));if(!document.documentElement.getAttribute("data-theme"))document.documentElement.removeAttribute("data-theme")}catch(e){document.documentElement.setAttribute("data-theme","light")}</script>
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="icon" type="image/png" href="icon-192.png">
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@400;700&family=DM+Mono:wght@300;400;500&display=swap" rel="stylesheet">
<style>
html { -webkit-text-size-adjust: 100%; }
body { margin: 0; padding-top: env(safe-area-inset-top, 0px); padding-bottom: env(safe-area-inset-bottom, 0px); }
''' + css + extra_css + quiz_css + '''</style>
</head>
<body>
''' 
html = head + main + '\n<script type="application/json" id="kanji-data">' + _KJ.replace('</', '<\\/') + '</script>\n<script type="application/json" id="vocab-data">' + _VJ.replace('</', '<\\/') + '</script>\n<script type="application/json" id="grammar-data">' + _GJ.replace('</', '<\\/') + '</script>\n<script type="application/json" id="map-data">' + open(os.path.join(HERE, 'data', 'japanmap.json'), encoding='utf-8').read().replace('</', '<\\/') + '</script>\n<script type="application/json" id="counter-data">' + _CJ.replace('</', '<\\/') + '</script>\n<script>' + js + '</script>\n</body>\n</html>\n'
open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(html)
print(len(html))

