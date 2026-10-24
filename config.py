"""Paramètres du projet : on les change ici, jamais dans le code."""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

AMAZON_URL = "https://www.amazon.fr"

# Menu de la catégorie Technologie : nom affiché -> recherche Amazon
CATEGORIES_TECH = {
    "Ordinateurs": "ordinateur portable",
    "Téléphones et tablettes": "smartphone tablette",
    "Imprimantes et scanners": "imprimante scanner",
    "Objets connectés": "montre connectée objet connecté",
}

HEADLESS = False              # False pour voir le navigateur travailler
PAGES_MAX = 2                 # limite volontaire : projet pédagogique
DELAI_ENTRE_PAGES = (3, 6)    # pause aléatoire en secondes entre deux pages
TIMEOUT = 15                  # attente maximale d'un élément, en secondes
TELECHARGER_IMAGES = True     # False pour ne pas enregistrer les images
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36 ProjetPedagogiqueIIT/1.0"
)

DB_PATH = BASE_DIR / "data" / "produits.db"
EXPORT_DIR = BASE_DIR / "exports"
IMAGES_DIR = BASE_DIR / "images"
