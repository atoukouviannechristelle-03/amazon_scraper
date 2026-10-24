"""Vue : tout ce qui s'affiche dans la console."""
from app.models.produit_tech import ProduitTech


class ConsoleView:
    def message(self, texte=""):
        print(texte)

    def erreur(self, texte):
        print(f"[ERREUR] {texte}")

    def bienvenue(self):
        print("=" * 60)
        print("   BIENVENUE - Scraper Amazon : catégorie Technologie")
        print("=" * 60)

    def demander_choix(self, categories):
        """Affiche le menu. Retourne l'index choisi, ou None pour quitter."""
        while True:
            print("\nQuel est votre choix ?")
            for numero, nom in enumerate(categories, start=1):
                print(f"  {numero}. {nom}")
            print("  0. Quitter")
            saisie = input("Votre choix : ").strip()
            if saisie == "0":
                return None
            if saisie.isdigit() and 1 <= int(saisie) <= len(categories):
                return int(saisie) - 1
            print("Choix invalide : tapez un numéro de la liste.")

    def afficher_produits(self, produits: list[ProduitTech], limite=15):
        if not produits:
            print("Aucun produit à afficher.")
            return
        print(f"\n{'PRIX (€)':>10}{'NOTE':>6}{'AVIS':>8}  NOM")
        print("-" * 85)
        for p in produits[:limite]:
            prix = f"{p.prix:.2f}" if p.prix is not None else "-"
            note = f"{p.note:.1f}" if p.note is not None else "-"
            avis = str(p.nb_avis) if p.nb_avis is not None else "-"
            print(f"{prix:>10}{note:>6}{avis:>8}  {p.nom[:60]}")
        if len(produits) > limite:
            print(f"... et {len(produits) - limite} autres (voir le CSV).")

    def afficher_resume(self, produits: list[ProduitTech], total_base: int):
        prix = [p.prix for p in produits if p.prix is not None]
        moyen = f"{sum(prix) / len(prix):.2f} €" if prix else "-"
        images = sum(1 for p in produits if p.image_fichier)
        print("\nRésumé :")
        print(f"  Produits récupérés : {len(produits)}")
        print(f"  Prix moyen         : {moyen}")
        print(f"  Images enregistrées: {images}")
        print(f"  Total en base      : {total_base}")
