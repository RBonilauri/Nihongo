"""Assemble l'application : lit le contenu (src/content), les feuilles de style (src/css),
le JavaScript (src/js) et écrit ../index.html. Lancer :  python3 src/build.py"""
import os, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(HERE, 'content'))
subprocess.check_call([sys.executable, os.path.join(HERE, 'assemble.py')])
def _read(*p): return open(os.path.join(HERE, *p), encoding='utf-8').read()
def _cat_files(d, names): return ''.join(_read(d, n) for n in names)
src = _read('build', 'nojs-plus.html')
css = src[src.index('<style>')+7 : src.index('</style>')]
main = src[src.index('<main>'):]

quiz_css = _cat_files('css', ['nav.css', 'map.css', 'quiz.css'])
extra_css = _cat_files('css', ['app.css'])

search_html = _read('html', 'shell.html')

# Les étapes s'exécutent dans l'ordre, dans un espace de noms commun (src/pipeline/).
_PIPE = os.path.join(HERE, 'pipeline')
for _f in sorted(os.listdir(_PIPE)):
    if _f.endswith('.py'):
        exec(compile(open(os.path.join(_PIPE, _f), encoding='utf-8').read(), _f, 'exec'), globals())
