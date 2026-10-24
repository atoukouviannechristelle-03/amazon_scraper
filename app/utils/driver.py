"""Création du navigateur Chrome piloté par Selenium."""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import config


def creer_driver() -> webdriver.Chrome:
    options = Options()
    if config.HEADLESS:
        options.add_argument("--headless=new")
    options.add_argument(f"--user-agent={config.USER_AGENT}")
    options.add_argument("--lang=fr-FR")
    options.add_argument("--window-size=1366,900")
    # Selenium Manager (inclus dans Selenium 4.6+) télécharge le bon chromedriver.
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(config.TIMEOUT * 2)
    return driver
