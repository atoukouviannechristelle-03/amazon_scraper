"""Modèle : un produit de la catégorie Technologie."""
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class ProduitTech:
    asin: str                      # identifiant Amazon (clé unique)
    nom: str
    categorie: str = ""            # ex. "Ordinateurs"
    prix: float | None = None      # en euros
    note: float | None = None      # ex. 4.5 (sur 5)
    nb_avis: int | None = None     # nombre d'avis
    url: str = ""
    image_url: str = ""
    image_fichier: str = ""        # ex. images/B0XXXX.jpg
    date_scraping: str = ""

    def __post_init__(self):
        if not self.date_scraping:
            self.date_scraping = datetime.now().isoformat(timespec="seconds")

    def en_dict(self) -> dict:
        return asdict(self)
