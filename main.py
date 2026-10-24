"""Point d'entrée du projet : python main.py"""
import sys

import config
from app.controllers.scraping_controller import ScrapingController
from app.models.catalogue import Catalogue
from app.views.console_view import ConsoleView
from app.views.export_view import ExportView


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")  # accents et € corrects dans la console

    controleur = ScrapingController(
        catalogue=Catalogue(config.DB_PATH),
        console_view=ConsoleView(),
        export_view=ExportView(config.EXPORT_DIR),
    )
    try:
        controleur.demarrer()
    except KeyboardInterrupt:
        print("\nArrêt demandé. Au revoir !")


if __name__ == "__main__":
    main()
