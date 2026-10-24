"""Modèle : catalogue des produits technologie (base SQLite)."""
import sqlite3
from pathlib import Path

from app.models.produit_tech import ProduitTech

CHAMPS = [
    "asin", "nom", "categorie", "prix", "note", "nb_avis",
    "url", "image_url", "image_fichier", "date_scraping",
]


class Catalogue:
    def __init__(self, chemin_db: Path):
        self.chemin_db = Path(chemin_db)
        self.chemin_db.parent.mkdir(parents=True, exist_ok=True)
        self._creer_table()

    def _connexion(self):
        return sqlite3.connect(self.chemin_db)

    def _creer_table(self):
        with self._connexion() as conn:
            conn.execute(
                """CREATE TABLE IF NOT EXISTS produits (
                    asin TEXT PRIMARY KEY,
                    nom TEXT NOT NULL,
                    categorie TEXT,
                    prix REAL,
                    note REAL,
                    nb_avis INTEGER,
                    url TEXT,
                    image_url TEXT,
                    image_fichier TEXT,
                    date_scraping TEXT)"""
            )

    def enregistrer(self, produits: list[ProduitTech]) -> int:
        """Insère ou met à jour (clé = ASIN) : jamais de doublon."""
        lignes = [tuple(p.en_dict()[c] for c in CHAMPS) for p in produits]
        with self._connexion() as conn:
            conn.executemany(
                f"INSERT OR REPLACE INTO produits ({', '.join(CHAMPS)}) "
                f"VALUES ({', '.join('?' * len(CHAMPS))})",
                lignes,
            )
        return len(lignes)

    def lister(self, categorie: str | None = None) -> list[ProduitTech]:
        requete = f"SELECT {', '.join(CHAMPS)} FROM produits"
        params = ()
        if categorie:
            requete += " WHERE categorie = ?"
            params = (categorie,)
        requete += " ORDER BY categorie, nom"
        with self._connexion() as conn:
            lignes = conn.execute(requete, params).fetchall()
        return [ProduitTech(**dict(zip(CHAMPS, l))) for l in lignes]

    def compter(self, categorie: str | None = None) -> int:
        requete = "SELECT COUNT(*) FROM produits"
        params = ()
        if categorie:
            requete += " WHERE categorie = ?"
            params = (categorie,)
        with self._connexion() as conn:
            return conn.execute(requete, params).fetchone()[0]
