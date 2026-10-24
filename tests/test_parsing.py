import csv
import tempfile
import unittest
from pathlib import Path

from app.models.catalogue import Catalogue
from app.models.produit_tech import ProduitTech
from app.utils import parsing
from app.views.export_view import ExportView


class TestNettoyage(unittest.TestCase):
    def test_prix(self):
        self.assertEqual(parsing.nettoyer_prix("1 299,99\xa0€"), 1299.99)
        self.assertEqual(parsing.nettoyer_prix("49,90 €"), 49.9)
        self.assertIsNone(parsing.nettoyer_prix(None))

    def test_note(self):
        self.assertEqual(parsing.nettoyer_note("4,5 sur 5 étoiles"), 4.5)

    def test_avis(self):
        self.assertEqual(parsing.nettoyer_avis("1 234"), 1234)
        self.assertEqual(parsing.nettoyer_avis("(2,3 k)"), 2300)
        self.assertIsNone(parsing.nettoyer_avis(""))


class TestBaseEtCsv(unittest.TestCase):
    def setUp(self):
        self.dossier = tempfile.TemporaryDirectory()
        self.base = Path(self.dossier.name)
        self.produits = [
            ProduitTech("A1", "PC portable", "Ordinateurs", 599.0, 4.4, 120),
            ProduitTech("A2", "Imprimante", "Imprimantes et scanners", 89.9, 4.0, 35),
        ]

    def tearDown(self):
        self.dossier.cleanup()

    def test_sqlite_sans_doublon(self):
        catalogue = Catalogue(self.base / "t.db")
        catalogue.enregistrer(self.produits)
        catalogue.enregistrer(self.produits)
        self.assertEqual(catalogue.compter(), 2)
        self.assertEqual(len(catalogue.lister("Ordinateurs")), 1)

    def test_export_csv(self):
        chemin = ExportView(self.base / "exports").exporter_csv(self.produits, "Téléphones et tablettes")
        self.assertIn("telephones_et_tablettes", chemin.name)
        with open(chemin, encoding="utf-8-sig") as f:
            lignes = list(csv.DictReader(f, delimiter=";"))
        self.assertEqual(len(lignes), 2)
        self.assertEqual(lignes[0]["nom"], "PC portable")


if __name__ == "__main__":
    unittest.main()
