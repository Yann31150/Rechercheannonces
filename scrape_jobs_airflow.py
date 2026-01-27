"""
Script de scraping pour Airflow
Peut être exécuté indépendamment ou via Airflow
"""
import sys
import os
from datetime import datetime
from utils import print_info, print_success, print_error, save_json
from main_unified import search_all_sites
import config


def run_daily_scraping():
    """
    Lance le scraping quotidien sur tous les sites
    
    Returns:
        Tuple (success: bool, message: str, jobs_count: int)
    """
    try:
        print_info("=" * 60)
        print_info("🔍 DÉMARRAGE DU SCRAPING QUOTIDIEN")
        print_info(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print_info("=" * 60)
        
        # Paramètres de recherche
        keywords = "Data"
        location = config.DEFAULT_LOCATION
        pages = 2  # Nombre de pages par site
        
        print_info(f"🔎 Recherche: '{keywords}'")
        print_info(f"📍 Localisation: {location}")
        print_info(f"📄 Pages: {pages}")
        print_info("")
        
        # Lancer la recherche sur tous les sites
        jobs = search_all_sites(
            keywords=keywords,
            location=location,
            pages=pages,
            sites=None  # Tous les sites
        )
        
        if jobs:
            # Sauvegarder les résultats
            save_json(jobs, config.JOBS_FILE)
            print_success(f"✅ {len(jobs)} offres trouvées et sauvegardées")
            
            # Copier aussi dans le dossier Annonces sur le bureau
            from utils import ensure_desktop_annonces
            annonces_dir = ensure_desktop_annonces()
            desktop_path = os.path.join(annonces_dir, "offres_linkedin.json")
            try:
                save_json(jobs, desktop_path)
                print_success(f"✅ Fichier copié dans Annonces: {desktop_path}")
            except Exception as e:
                print_error(f"⚠️  Impossible de copier dans Annonces: {str(e)}")
            
            return True, f"Scraping réussi: {len(jobs)} offres trouvées", len(jobs)
        else:
            # Aucun résultat n'est pas une erreur : on sauvegarde un fichier vide
            save_json([], config.JOBS_FILE)
            print_info("ℹ️  Aucune offre trouvée aujourd'hui")
            return True, "Aucune offre trouvée", 0
            
    except Exception as e:
        error_msg = f"Erreur lors du scraping: {str(e)}"
        print_error(error_msg)
        return False, error_msg, 0


if __name__ == "__main__":
    # Exécution directe (pour tests)
    success, message, count = run_daily_scraping()
    if success:
        print_success(f"✅ {message}")
        sys.exit(0)
    else:
        print_error(f"❌ {message}")
        sys.exit(1)

