"""Orchestration du scraping : charger -> défiler -> extraire -> images."""
import random
import time
from urllib.parse import quote_plus
from urllib.request import Request, urlopen

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import config
from app.models.produit_tech import ProduitTech
from app.utils import parsing
from app.utils.driver import creer_driver


class CaptchaDetecte(Exception):
    """Amazon demande une vérification : on s'arrête, on ne la contourne pas."""


class AmazonScraper:
    def __init__(self, log=print):
        self.log = log
        self.driver = None

    # --- Navigation ---
    def _accepter_cookies(self):
        try:
            WebDriverWait(self.driver, 4).until(
                EC.element_to_be_clickable((By.ID, "sp-cc-accept"))
            ).click()
        except TimeoutException:
            pass  # pas de bannière

    def _charger(self, url, premiere):
        self.driver.get(url)
        if parsing.est_captcha(self.driver):
            raise CaptchaDetecte("CAPTCHA détecté")
        if premiere:
            self._accepter_cookies()
        try:
            WebDriverWait(self.driver, config.TIMEOUT).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, parsing.SEL_RESULTAT))
            )
        except TimeoutException:
            self.log("  Aucun résultat détecté sur cette page.")

    def _defiler(self, etapes=4):
        """Fait défiler la page pour charger les images différées."""
        hauteur = self.driver.execute_script("return document.body.scrollHeight")
        for i in range(1, etapes + 1):
            self.driver.execute_script(f"window.scrollTo(0, {hauteur * i // etapes});")
            time.sleep(0.4)

    # --- Scraping d'une catégorie ---
    def scraper(self, categorie, recherche, pages_max=None):
        pages_max = pages_max or config.PAGES_MAX
        url = f"{config.AMAZON_URL}/s?k={quote_plus(recherche)}"
        uniques: dict[str, ProduitTech] = {}
        self.driver = creer_driver()
        try:
            for numero in range(1, pages_max + 1):
                self.log(f"Page {numero}/{pages_max} en cours...")
                self._charger(url, premiere=(numero == 1))
                self._defiler()
                trouves = parsing.extraire_produits(self.driver, categorie)
                self.log(f"  -> {len(trouves)} produits lus")
                for p in trouves:
                    uniques.setdefault(p.asin, p)
                url = parsing.trouver_page_suivante(self.driver)
                if not url or numero == pages_max:
                    break
                pause = random.uniform(*config.DELAI_ENTRE_PAGES)
                self.log(f"  pause de {pause:.1f}s (politesse)")
                time.sleep(pause)
        finally:
            self.driver.quit()

        produits = list(uniques.values())
        if config.TELECHARGER_IMAGES:
            self._telecharger_images(produits)
        return produits

    # --- Images ---
    def _telecharger_images(self, produits):
        config.IMAGES_DIR.mkdir(parents=True, exist_ok=True)
        total = 0
        for p in produits:
            if not p.image_url:
                continue
            fichier = config.IMAGES_DIR / f"{p.asin}.jpg"
            if not fichier.exists():
                try:
                    requete = Request(p.image_url, headers={"User-Agent": config.USER_AGENT})
                    with urlopen(requete, timeout=config.TIMEOUT) as reponse:
                        fichier.write_bytes(reponse.read())
                except (OSError, ValueError):
                    continue
                time.sleep(0.2)
            p.image_fichier = f"images/{p.asin}.jpg"
            total += 1
        self.log(f"  {total} images enregistrées dans le dossier images/")
