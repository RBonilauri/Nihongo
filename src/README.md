# Nihongo — sources

Le fichier `../index.html` est **généré** : ne pas l'éditer à la main.

## Commandes (depuis la racine du dépôt)
- `make build` : régénère `index.html` (`python3 src/build.py`)
- `make test` : build + tests de non-régression (Playwright, `tests/test_app.py`)
- `make release` : tests puis incrémente la version du cache dans `sw.js`
- Dépendances : `pip install -r src/requirements.txt`

## Structure
- `content/` : contenu en modules Python (vocabulaire, kanji N3, adjectifs/keigo, voyage/conversation, thèmes, compteurs, banque de particules…)
- `js/` : code de l'app découpé et numéroté (01 recherche … 19 boot)
- `css/` : styles (app, nav, map, quiz) ; `html/shell.html` : coquille ; `base/` : gabarit de départ
- `data/` : `japanmap.json` (carte), listes de kanji/vocab déjà connus
- `tools/mapgen.py` : régénère la carte (télécharge le geojson dataofjapan/land, sous licence ouverte)
- `build.py`, `assemble.py` : assemblage → `index.html`

## À savoir
Le contenu pédagogique est rédigé par Claude : des erreurs sont possibles, à signaler pour correction.
