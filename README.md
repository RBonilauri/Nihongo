<div align="center">

# 日本語 · Nihongo

**Référence de japonais en français, pour apprendre, réviser et s'entraîner, à l'écrit comme à l'oral.**

Application web installable (PWA), sans framework, sans compte, sans serveur : un seul fichier `index.html`.

![PWA](https://img.shields.io/badge/PWA-installable-5a0fc8)
![Vanilla JS](https://img.shields.io/badge/JavaScript-vanilla-f7df1e)
![Build](https://img.shields.io/badge/build-Python%203-3776ab)
![Tests](https://img.shields.io/badge/tests-Playwright-2ead33)
![Langue](https://img.shields.io/badge/interface-fran%C3%A7ais-blue)

</div>

---

## Sommaire

- [À propos](#à-propos)
- [Fonctionnalités](#fonctionnalités)
- [Contenu pédagogique](#contenu-pédagogique)
- [Démarrage rapide](#démarrage-rapide)
- [Installer l'application sur un téléphone](#installer-lapplication-sur-un-téléphone)
- [Architecture du projet](#architecture-du-projet)
- [Chaîne de génération](#chaîne-de-génération)
- [Tests](#tests)
- [Données et confidentialité](#données-et-confidentialité)
- [Contribuer et signaler une erreur](#contribuer-et-signaler-une-erreur)
- [Crédits et licences](#crédits-et-licences)

---

## À propos

**Nihongo** (nom installé : *Japonais Référence*, abrégé **日本語**) est une application de référence et d'entraînement pour francophones qui apprennent le japonais. Elle réunit au même endroit :

- une **référence** structurée (kana, kanji, grammaire N4/N3, conjugaison, particules, compteurs, keigo, vocabulaire thématique) ;
- des **outils de révision** (fiches à retourner, quiz variés, suivi de progression) ;
- un volet **oral et voyage** (synthèse vocale japonaise, phrases utiles, carte du Japon, compte à rebours du départ).

Elle est conçue **mobile d'abord** : navigation par onglets, lecture confortable, thèmes clair/sombre, et usage possible dans le métro grâce au mode silencieux.

> **À savoir** : le contenu pédagogique est rédigé avec l'aide de Claude. Des erreurs sont possibles : merci de les signaler pour correction.

---

## Fonctionnalités

### Apprendre

| | |
|---|---|
| **4 pôles thématiques** | *Bases* (kana, prononciation, kanji) · *Grammaire* (particules, conjugaison, N4, N3, adjectifs, compteurs, expressions, outils) · *Vocabulaire* (général, usuel, temps et dates, géographie) · *Parler* (conversation, voyage, keigo) |
| **Plus de 100 sous-rubriques** | Sections repliables, navigation par pages, bouton « retour » du téléphone géré |
| **Conjugaison à la demande** | Conjugue un verbe à la demande, avec les traductions françaises de chaque forme |
| **Exemples de verbes** | Plus de 300 verbes, chacun avec au moins deux phrases dans des contextes différents |
| **Kanji détaillés** | Chaque mot à plusieurs kanji dispose d'un menu décomposant ses kanji, avec leur sens |
| **Aides à la lecture** | Option pour masquer romaji et traductions (flou, touche pour révéler) |

### Rechercher

- Recherche en **français, romaji ou japonais**, sur tout le contenu.
- Tolérante : accents ignorés (`eau` / `éau`), singulier/pluriel, élisions (`l'eau`), fautes de frappe (`conjugasion`), romaji (`toukyou`).
- Filtre par rubrique, historique des recherches récentes, bouton « Afficher plus » pour les requêtes larges.

### S'entraîner

- **Sept quiz** : kanji, vocabulaire, particules, conjugaison, compteurs, géographie et quiz général.
- **Paramétrage fin** : rubriques, sous-rubriques, régions, types de questions, formes de conjugaison, avec « Tout sélectionner / Tout désélectionner ».
- **Mémoire des erreurs** : les ratés sont conservés et ressortent en priorité dans les statistiques.
- **Indices** : lecture en kana (💡), traduction révélable dans le quiz de grammaire.
- **Questions d'écoute** avec option « Voir le texte ».
- **Écran de victoire** à 100 % avec feux d'artifice minimalistes (désactivés si le système demande de réduire les animations).
- **Fiches de révision** générées automatiquement à partir des tableaux : on retourne la carte, puis « Su » ou « À revoir » ; on peut ne rejouer que les cartes à revoir.

### Suivre sa progression

- Page **« Ma progression »** : une carte par quiz avec taux de réussite et répartition *maîtrisés / à revoir / en cours*.
- **Objectif du jour** (20 réponses) affiché sur l'accueil.
- Accès rapide aux **trois dernières sections ouvertes** (désactivable).
- **Favoris**.

### Oral et voyage

- **Mode écoute** : synthèse vocale japonaise (voix `ja-JP`, débit ralenti). Un appui lit une conjugaison ou une phrase d'exemple, une seule fois.
- **Mode silencieux** : supprime les questions d'écoute des quiz (transports, bureau).
- **Carte interactive du Japon** : 47 préfectures dessinées en SVG, fiche par préfecture (région, etc.), utilisée aussi par le quiz de géographie.
- **Compte à rebours du voyage** (J-xx) avec petit avion sur l'accueil : date de départ réglable, masquable.
- **Phrases de voyage et de conversation** : aéroport et douane, situations courantes, politesse et keigo.

### Réglages et données

- Thème **clair**, **sombre** ou **auto**.
- Taille du texte réglable (A− / A+).
- **Export / import JSON** de la sauvegarde (favoris, fiches sues, réglages) et réinitialisation des fiches.

---

## Contenu pédagogique

D'après les tests automatisés, l'application embarque au minimum :

| Élément | Volume |
|---|---|
| Kanji | plus de 600 |
| Vocabulaire et phrases | plus de 2 000 entrées |
| Verbes | plus de 300 (2 phrases d'exemple chacun) |
| Préfectures | 47, avec régions |
| Pages de grammaire | N4 et N3 |
| Quiz | 7 |

Les sources du contenu sont des modules Python lisibles dans [`src/content/`](src/content) : `vocab_core.py`, `vocab_themes.py`, `kanji_n3.py`, `grammaire_n4_n3.py`, `verbes_exemples*.py`, `adjectifs_keigo.py`, `voyage_conversation.py`, `compteurs.py`, `parts_bank.py`, etc. Les listes `src/data/have_vocab.txt` et `have_kanji.txt` recensent ce qui est déjà connu afin d'éviter les doublons.

---

## Démarrage rapide

### Utiliser l'application

Le fichier `index.html` à la racine est **autonome** :

```bash
# Option 1 : l'ouvrir directement dans un navigateur
open index.html

# Option 2 : le servir en local (nécessaire pour la PWA / service worker)
python3 -m http.server 8000
# puis http://localhost:8000
```

Le service worker n'est enregistré que sur `http(s)`, pas en `file://`.

### Développer

Prérequis : **Python 3** et, pour les tests, **Playwright**.

```bash
pip install -r src/requirements.txt

make build     # régénère index.html
make test      # build + tests de non-régression
make release   # tests, puis incrémente la version du cache
```

---

## Installer l'application sur un téléphone

Une fois l'application servie en HTTPS (par exemple via GitHub Pages) :

- **Android (Chrome)** : menu ⋮ → *Installer l'application* / *Ajouter à l'écran d'accueil*.
- **iOS (Safari)** : bouton Partager → *Sur l'écran d'accueil*.

Le manifeste (`manifest.webmanifest`) fournit le nom, les couleurs (`#1c1510`), le mode `standalone` et les icônes (192, 512, *maskable* 512, `apple-touch-icon`).

---

## Architecture du projet

```
Nihongo/
├── index.html               # ⚠ GÉNÉRÉ : ne pas éditer à la main
├── manifest.webmanifest     # Manifeste PWA
├── icon-*.png, apple-touch-icon.png
├── Makefile                 # build / test / release
├── tests/
│   └── test_app.py          # Tests de non-régression (Playwright)
└── src/
    ├── build.py             # Point d'entrée de la génération
    ├── assemble.py          # Assemblage final de index.html
    ├── release.py           # Incrément de version du cache
    ├── requirements.txt
    ├── pipeline/            # Étapes de génération (01 → 06)
    │   ├── 01_html_transformations.py
    │   ├── 02_kanji.py
    │   ├── 03_vocabulaire.py
    │   ├── 04_grammaire_verbes.py
    │   ├── 05_particules_compteurs.py
    │   └── 06_assemblage.py
    ├── content/             # Contenu pédagogique (modules Python)
    ├── data/                # japanmap.json, listes « déjà connu »
    ├── base/                # Gabarit HTML de départ
    ├── html/shell.html      # Coquille : barre du haut, onglets, tiroir, recherche
    ├── css/                 # app.css, nav.css, map.css, quiz.css
    ├── js/                  # Code applicatif numéroté (01 → 19)
    └── tools/mapgen.py      # Régénération de la carte du Japon
```

### Organisation du JavaScript

Le code applicatif est découpé en fichiers numérotés, concaténés dans l'ordre :

| Plage | Rôle |
|---|---|
| `01`–`03` | Cœur, recherche, thème, romaji, état et favoris |
| `04` | Traduction des formes, kanji un par un, conjugaison à la demande, exemples de verbes |
| `05`–`07` | Fiches de révision, écoute (synthèse vocale), lecture et réglages |
| `08`–`15` | Hub des quiz et chaque quiz (vocabulaire, kanji, grammaire, compteurs, général, géographie), sélection « tout / aucun » |
| `16`–`17` | Carte du Japon et quiz de géographie |
| `18` | Navigation par pages, progression, célébration |
| `19` | Démarrage (boot) |

---

## Chaîne de génération

1. `src/build.py` lance les étapes du dossier `src/pipeline/` : transformation du gabarit HTML, injection des kanji, du vocabulaire, de la grammaire et des verbes, des particules et compteurs.
2. `src/assemble.py` assemble CSS, JavaScript, données JSON embarquées et contenu dans un **unique `index.html`**.
3. Les données (kanji, vocabulaire, grammaire, carte, compteurs) sont embarquées sous forme de blocs JSON dans la page, lus au démarrage.

La carte du Japon se régénère avec `src/tools/mapgen.py`, qui télécharge le geojson *dataofjapan/land* (licence ouverte).

---

## Tests

`make test` reconstruit l'application puis exécute `tests/test_app.py` avec Playwright. Les vérifications couvrent notamment :

- le chargement sans erreur JavaScript, 4 onglets, 4 pôles, plus de 100 sous-rubriques non vides ;
- la **recherche** : accents, pluriels, élisions, fautes de frappe, romaji, filtres, historique ;
- les **quiz** : lancement, comptage des réponses, ordre des statistiques, conservation après rechargement, mode silencieux, sous-rubriques ;
- l'**objectif du jour**, le **compte à rebours** et la page **Ma progression** ;
- la **carte** (47 préfectures, fiche de préfecture) ;
- l'**intégrité du contenu** : aucune traduction française vide, chaque verbe a deux exemples, chaque mot à plusieurs kanji a son menu, volumes minimaux de données.

---

## Données et confidentialité

- **Aucun compte, aucun serveur, aucun suivi.**
- La progression, les favoris et les réglages sont enregistrés **dans le navigateur** (`localStorage`, clé `jp-state`).
- La sauvegarde est **manuelle** : utilise *Exporter* / *Importer* dans le menu ⚙ pour changer d'appareil ou conserver une copie.
- Vider les données du navigateur efface la progression.

---

## Contribuer et signaler une erreur

Les corrections de contenu sont particulièrement bienvenues (traduction, lecture d'un kanji, exemple peu naturel, faute de grammaire).

1. Ouvre une *issue* en indiquant la rubrique, l'entrée concernée et la correction proposée.
2. Pour proposer une modification directe, **édite les sources dans `src/`** (jamais `index.html`), puis lance `make test`.
3. Vérifie que les tests passent avant de proposer ta contribution.

---

## Crédits et licences

- Contenu pédagogique rédigé avec l'aide de **Claude** (Anthropic), à relire et corriger.
- Données cartographiques : **dataofjapan/land** (licence ouverte), via `src/tools/mapgen.py`.
- Aucune licence n'est encore déclarée pour ce dépôt : sans fichier `LICENSE`, tous droits sont réservés par défaut. Ajoutes-en une (MIT, par exemple) si tu souhaites autoriser la réutilisation.
