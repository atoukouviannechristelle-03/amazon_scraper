"""Extraction des données avec Selenium uniquement (sélecteurs CSS)."""
import re

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By

import config
from app.models.produit_tech import ProduitTech

# --- Sélecteurs CSS (à corriger ici si Amazon change son HTML) ---
SEL_RESULTAT = 'div[data-component-type="s-search-result"]'
SEL_NOM = ["h2 span"]
SEL_PRIX = ["span.a-price > span.a-offscreen"]
SEL_NOTE = ["span.a-icon-alt"]
SEL_AVIS = [
    "span.a-size-base.s-underline-text",
    "a[href*='customerReviews'] span.a-size-base",
]
SEL_IMAGE = "img.s-image"
SEL_SUIVANT = "a.s-pagination-next"
SEL_CAPTCHA = 'form[action*="validateCaptcha"]'


# --- Nettoyage des textes ---
def nettoyer_prix(texte):
    """'1 299,99 €' -> 1299.99"""
    if not texte:
        return None
    t = texte.replace("\u202f", "").replace("\xa0", "")
    t = re.sub(r"[^\d,\.]", "", t)
    if "," in t:
        t = t.replace(".", "").replace(",", ".")
    try:
        return float(t)
    except ValueError:
        return None


def nettoyer_note(texte):
    """'4,5 sur 5 étoiles' -> 4.5"""
    if not texte:
        return None
    m = re.search(r"(\d+(?:[,\.]\d+)?)", texte)
    return float(m.group(1).replace(",", ".")) if m else None


def nettoyer_avis(texte):
    """'1 234' -> 1234 ; '(2,3 k)' -> 2300"""
    if not texte:
        return None
    t = texte.lower().replace("\u202f", "").replace("\xa0", "").replace(" ", "")
    m = re.search(r"(\d+(?:[.,]\d+)?)([km])", t)
    if m:
        valeur = float(m.group(1).replace(",", "."))
        return int(valeur * (1000 if m.group(2) == "k" else 1_000_000))
    chiffres = re.sub(r"\D", "", t)
    return int(chiffres) if chiffres else None


# --- Lecture des éléments avec Selenium ---
def _texte(bloc, selecteurs):
    """Premier texte non vide trouvé. textContent lit aussi le texte masqué (prix, note)."""
    for sel in selecteurs:
        for el in bloc.find_elements(By.CSS_SELECTOR, sel):
            texte = (el.get_attribute("textContent") or "").strip()
            if texte:
                return texte
    return None


def extraire_produits(driver, categorie=""):
    produits = []
    for bloc in driver.find_elements(By.CSS_SELECTOR, SEL_RESULTAT):
        try:
            asin = (bloc.get_attribute("data-asin") or "").strip()
            nom = _texte(bloc, SEL_NOM)
            if not asin or not nom:
                continue  # bloc publicitaire ou incomplet
            images = bloc.find_elements(By.CSS_SELECTOR, SEL_IMAGE)
            image_url = (images[0].get_attribute("src") or "") if images else ""
            produits.append(ProduitTech(
                asin=asin,
                nom=nom,
                categorie=categorie,
                prix=nettoyer_prix(_texte(bloc, SEL_PRIX)),
                note=nettoyer_note(_texte(bloc, SEL_NOTE)),
                nb_avis=nettoyer_avis(_texte(bloc, SEL_AVIS)),
                url=f"{config.AMAZON_URL}/dp/{asin}",
                image_url=image_url,
            ))
        except StaleElementReferenceException:
            continue
    return produits


def trouver_page_suivante(driver):
    liens = driver.find_elements(By.CSS_SELECTOR, SEL_SUIVANT)
    return liens[0].get_attribute("href") if liens else None


def est_captcha(driver):
    return bool(driver.find_elements(By.CSS_SELECTOR, SEL_CAPTCHA)) or \
        "captcha" in driver.current_url.lower()
