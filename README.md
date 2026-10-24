# Amazon Scraper — Catégorie Technologie

Projet pédagogique de l'**Institut Ivoirien de Technologie** (Séance 2 : *Le web scraping, principe et règles du jeu*).

Application **console** qui récupère, sur **amazon.fr**, les produits de la catégorie **Technologie** avec **Selenium** (uniquement, sans BeautifulSoup). Les données sont enregistrées dans une base **SQLite**, exportées dans un fichier **CSV**, et les images des produits sont téléchargées dans le dossier `images/`.

> **Point d'entrée : `main.py`.** Tous les paramètres se changent dans `config.py`, jamais dans le code.

---

## 1. Ce que fait le programme

1. Affiche un message de **bienvenue**.
2. Demande **« Quel est votre choix ? »** et affiche le menu :

   ```
   1. Ordinateurs
   2. Téléphones et tablettes
   3. Imprimantes et scanners
   4. Objets connectés
   0. Quitter
   ```
3. Ouvre **Chrome** avec Selenium et charge la page de résultats Amazon de la catégorie choisie.
4. Fait défiler la page, puis lit chaque produit avec des **sélecteurs CSS** (Selenium).
5. Passe aux pages suivantes (jusqu'à `PAGES_MAX`), avec une **pause aléatoire** entre deux pages.
6. Télécharge l'**image** de chaque produit dans `images/`.
7. Enregistre les produits dans la base **SQLite** `data/produits.db` (sans doublon).
8. Exporte les produits de la catégorie dans un fichier **CSV** du dossier `exports/`.
9. Affiche un tableau et un résumé dans la console, puis **revient au menu**. Tapez `0` pour quitter.

## 2. Données récupérées

| Donnée | Description |
|---|---|
| `nom` | nom du produit |
| `prix` | prix en euros |
| `note` | note moyenne sur 5 (avis) |
| `nb_avis` | nombre d'avis |
| `asin`, `url` | identifiant Amazon et lien du produit |
| `categorie` | catégorie choisie dans le menu |
| `image_url`, `image_fichier` | adresse de l'image et fichier enregistré (`images/ASIN.jpg`) |
| `date_scraping` | date et heure de la récupération |

Si Amazon n'affiche pas un prix ou des avis pour un produit, la valeur reste vide.

## 3. Arborescence

```
amazon_scraper/
├── README.md
├── main.py                       # point d'entrée
├── config.py                     # tous les paramètres
├── requirements.txt
├── app/
│   ├── controllers/
│   │   └── scraping_controller.py   # menu + enchaînement des étapes
│   ├── models/
│   │   ├── produit_tech.py          # un produit technologie
│   │   └── catalogue.py             # base SQLite
│   ├── utils/
│   │   ├── amazon_scraper.py        # navigation, pages, images
│   │   ├── driver.py                # navigateur Chrome
│   │   └── parsing.py               # sélecteurs CSS + nettoyage
│   └── views/
│       ├── console_view.py          # affichage console et menu
│       └── export_view.py           # export CSV
├── data/                         # base produits.db (créée automatiquement)
├── exports/                      # fichiers CSV
├── images/                       # images des produits scrapés
└── tests/
```

## 4. Prérequis

- **Python 3.10 ou plus récent**
- **Google Chrome** installé (Selenium télécharge tout seul le pilote correspondant)
- Une connexion Internet
- Git (pour GitHub)

## 5. Installation

```bash
git clone https://github.com/atoukouviannechristelle-03/amazon_scraper.git
cd amazon_scraper
```

**Windows (PowerShell)**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
Si l'activation est bloquée : `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, puis recommencez.

**Mac / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Dans PyCharm, l'environnement `.venv` est créé et activé automatiquement : il suffit de lancer `pip install -r requirements.txt` dans le terminal.

## 6. Exécution

À la racine du projet (là où se trouve `main.py`) :

```bash
python main.py
```

Exemple :

```
============================================================
   BIENVENUE - Scraper Amazon : catégorie Technologie
============================================================

Quel est votre choix ?
  1. Ordinateurs
  2. Téléphones et tablettes
  3. Imprimantes et scanners
  4. Objets connectés
  0. Quitter
Votre choix : 1
```

Chrome s'ouvre : **ne le fermez pas** pendant le scraping. À la fin, le programme affiche les produits, le résumé, le chemin du CSV, puis le menu réapparaît.

## 7. Configuration (`config.py`)

| Paramètre | Rôle | Défaut |
|---|---|---|
| `AMAZON_URL` | site cible | `https://www.amazon.fr` |
| `CATEGORIES_TECH` | menu : nom affiché → recherche Amazon | 4 catégories |
| `HEADLESS` | `True` : navigateur invisible | `False` |
| `PAGES_MAX` | nombre de pages par catégorie | `2` |
| `DELAI_ENTRE_PAGES` | pause aléatoire (secondes) | `(3, 6)` |
| `TIMEOUT` | attente maximale d'un élément (s) | `15` |
| `TELECHARGER_IMAGES` | télécharger les images | `True` |
| `DB_PATH` | base SQLite | `data/produits.db` |
| `EXPORT_DIR` | dossier des CSV | `exports/` |
| `IMAGES_DIR` | dossier des images | `images/` |

## 8. Résultats

**Base SQLite** : `data/produits.db`, table `produits` (clé primaire : `asin`, donc aucun doublon : relancer le programme met à jour les produits existants). On peut l'ouvrir avec l'outil *Database* de PyCharm ou *DB Browser for SQLite*.

**CSV** : `exports/tech_<categorie>_<date>_<heure>.csv`, séparateur `;`, encodage UTF-8, ouvrable directement dans Excel. Il contient tous les produits de la catégorie présents en base.

**Images** : `images/<asin>.jpg`, une image par produit (une image déjà présente n'est pas téléchargée deux fois).

## 9. Tests

```bash
python -m unittest discover -s tests -v
```
Ils vérifient le nettoyage des prix, notes et avis, la base SQLite (pas de doublon) et l'export CSV.

## 10. Règles du jeu (cours)

- **robots.txt et CGU** : à lire avant de commencer. Amazon restreint le scraping automatisé : ce projet est **strictement pédagogique**, à faible volume, sans revente ni usage commercial.
- **Politesse** : pause aléatoire entre deux pages, User-Agent identifiable (`config.py`), 2 pages par défaut.
- **Données personnelles** : aucune collecte de noms, téléphones ou e-mails. Seuls des produits sont récupérés.
- **API d'abord** : pour un usage réel, utiliser l'API officielle d'Amazon.
- Si Amazon affiche un **CAPTCHA**, le programme **s'arrête** et ne le contourne pas.

## 11. Publier sur GitHub

```bash
git add .
git commit -m "Projet amazon_scraper : catégorie Technologie"
git branch -M main
git remote add origin https://github.com/atoukouviannechristelle-03/amazon_scraper.git
git push -u origin main
```
Le dépôt doit d'abord être créé (vide) sur github.com. Le `.gitignore` empêche d'envoyer `.venv`, la base, les CSV et les images.

## 12. Dépannage

| Problème | Solution |
|---|---|
| `ModuleNotFoundError: app` | lancer `python main.py` depuis la racine du projet |
| `ModuleNotFoundError: selenium` | activer `.venv` puis `pip install -r requirements.txt` |
| Chrome ne s'ouvre pas | installer Google Chrome, puis `pip install -U selenium` |
| « Aucun produit récupéré » | Amazon a changé son HTML : corriger les sélecteurs en haut de `app/utils/parsing.py` (F12 dans Chrome pour les trouver) |
| Message CAPTCHA | attendre quelques minutes, réduire `PAGES_MAX` |
| Accents illisibles | `$env:PYTHONUTF8 = "1"` (PowerShell) puis relancer |

## 13. Auteur

À compléter : nom, classe, date.
