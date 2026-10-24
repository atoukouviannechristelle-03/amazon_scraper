"""Contrôleur : relie le menu, le scraper, la base SQLite et les vues."""
import config
from app.utils.amazon_scraper import AmazonScraper, CaptchaDetecte


class ScrapingController:
    def __init__(self, catalogue, console_view, export_view):
        self.catalogue = catalogue
        self.console = console_view
        self.export = export_view
        self.scraper = AmazonScraper(log=console_view.message)

    def demarrer(self):
        """Boucle principale : Bienvenue -> menu -> scraping -> retour au menu."""
        self.console.bienvenue()
        noms = list(config.CATEGORIES_TECH)
        while True:
            index = self.console.demander_choix(noms)
            if index is None:
                self.console.message("\nMerci d'avoir utilisé le programme. Au revoir !")
                return
            nom = noms[index]
            self.traiter_categorie(nom, config.CATEGORIES_TECH[nom])

    def traiter_categorie(self, nom, recherche):
        self.console.message(f"\n=== {nom} : scraping en cours ===")
        try:
            produits = self.scraper.scraper(nom, recherche)
        except CaptchaDetecte:
            self.console.erreur(
                "Amazon a affiché un CAPTCHA : arrêt volontaire. "
                "Attendez quelques minutes puis réessayez."
            )
            return
        except Exception as e:
            self.console.erreur(f"Échec du scraping : {str(e).splitlines()[0] if str(e) else e!r}")
            return

        if not produits:
            self.console.message("Aucun produit récupéré (voir le README, section Dépannage).")
            return

        self.catalogue.enregistrer(produits)
        self.console.afficher_produits(produits)
        self.console.afficher_resume(produits, self.catalogue.compter())
        chemin = self.export.exporter_csv(self.catalogue.lister(nom), nom)
        self.console.message(f"\nFichier CSV : {chemin}")
        self.console.message(f"Base SQLite : {config.DB_PATH}")
