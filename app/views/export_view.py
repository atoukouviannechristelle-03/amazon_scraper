"""Vue : export des données dans un fichier CSV."""
import csv
import re
import unicodedata
from datetime import datetime
from pathlib import Path

from app.models.catalogue import CHAMPS


def _slug(texte):
    """'Téléphones et tablettes' -> 'telephones_et_tablettes'"""
    ascii_ = unicodedata.normalize("NFKD", texte).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "_", ascii_.lower()).strip("_")


class ExportView:
    def __init__(self, dossier):
        self.dossier = Path(dossier)

    def exporter_csv(self, produits, categorie):
        self.dossier.mkdir(parents=True, exist_ok=True)
        nom = f"tech_{_slug(categorie)}_{datetime.now():%Y%m%d_%H%M%S}.csv"
        chemin = self.dossier / nom
        with open(chemin, "w", newline="", encoding="utf-8-sig") as f:  # utf-8-sig : accents OK dans Excel
            writer = csv.DictWriter(f, fieldnames=CHAMPS, delimiter=";")
            writer.writeheader()
            for p in produits:
                writer.writerow(p.en_dict())
        return chemin
