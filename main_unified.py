"""
Script unifié pour rechercher sur tous les sites d'emploi
"""
import argparse
import sys
import os
from scraper import LinkedInJobScraper
from scraper_wttj import WelcomeToTheJungleScraper
from scraper_indeed import IndeedScraper
from scraper_apec import ApecScraper
from scraper_helloworks import HelloworksScraper
from utils import (
    display_jobs_table, save_to_excel, save_to_csv,
    print_success, print_error, print_info, print_warning, save_json, load_json
)
import config

def search_all_sites(keywords, location, pages=2, sites=None):
    """Recherche sur tous les sites ou sites spécifiés"""
    all_jobs = []
    
    # Sites disponibles
    available_sites = {
        'linkedin': LinkedInJobScraper,
        'wttj': WelcomeToTheJungleScraper,
        'indeed': IndeedScraper,
        'apec': ApecScraper,
        'helloworks': HelloworksScraper,
        'freework': None,  # À implémenter
        'bonnealternance': None  # À implémenter
    }
    
    # Importer les nouveaux scrapers si disponibles
    try:
        from scraper_freework import FreeWorkScraper
        available_sites['freework'] = FreeWorkScraper
    except:
        pass
    
    try:
        from scraper_bonne_alternance import BonneAlternanceScraper
        available_sites['bonnealternance'] = BonneAlternanceScraper
    except:
        pass
    
    # Si aucun site spécifié, utiliser tous
    if not sites:
        sites = list(available_sites.keys())
    
    print_info(f"Recherche sur {len(sites)} site(s): {', '.join(sites)}")
    print_info(f"Mots-clés: {keywords} | Localisation: {location}")
    print("")
    
    for site_name in sites:
        if site_name not in available_sites:
            print_warning(f"Site '{site_name}' non reconnu, ignoré")
            continue
        
        print_info(f"=== Recherche sur {site_name.upper()} ===")
        scraper_class = available_sites[site_name]
        # Mode headless automatique si dans GitHub Actions ou variable d'environnement
        is_headless = os.getenv('GITHUB_ACTIONS') == 'true' or os.getenv('HEADLESS', '').lower() == 'true'
        scraper = scraper_class(headless=is_headless)
        
        try:
            scraper.setup_driver()
            
            # LinkedIn nécessite une connexion
            if site_name == 'linkedin':
                if not scraper.login():
                    print_warning(f"Échec de la connexion {site_name}, passage au site suivant")
                    scraper.close()
                    continue
            
            # Recherche
            jobs = scraper.search_jobs(keywords, location, max_pages=pages)
            all_jobs.extend(jobs)
            
            scraper.close()
            print("")
            
        except Exception as e:
            print_error(f"Erreur sur {site_name}: {str(e)}")
            try:
                scraper.close()
            except:
                pass
            continue
    
    return all_jobs

def main():
    parser = argparse.ArgumentParser(
        description="Recherche d'emploi sur plusieurs sites",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--search', type=str, required=True, help='Mots-clés de recherche')
    parser.add_argument('--location', type=str, default=config.DEFAULT_LOCATION, help='Localisation')
    parser.add_argument('--pages', type=int, default=2, help='Nombre de pages par site')
    parser.add_argument('--sites', type=str, nargs='+', 
                       choices=['linkedin', 'wttj', 'indeed', 'apec', 'helloworks', 'freework', 'bonnealternance'],
                       help='Sites à utiliser (par défaut: tous)')
    parser.add_argument('--export', type=str, choices=['excel', 'csv', 'json'], default='csv',
                       help='Format d\'export')
    parser.add_argument('--headless', action='store_true', help='Mode headless')
    
    args = parser.parse_args()
    
    # Recherche
    jobs = search_all_sites(
        keywords=args.search,
        location=args.location,
        pages=args.pages,
        sites=args.sites
    )
    
    if jobs:
        print_success(f"\n✅ Total: {len(jobs)} offres trouvées sur tous les sites")
        display_jobs_table(jobs)
        
        # Sauvegarder
        save_json(jobs, config.JOBS_FILE)
        
        # Export
        if args.export == 'csv':
            save_to_csv(jobs, f"data/jobs_all_sites_{args.search.replace(' ', '_')}.csv")
        elif args.export == 'excel':
            save_to_excel(jobs, f"data/jobs_all_sites_{args.search.replace(' ', '_')}.xlsx")
        else:
            save_json(jobs, f"data/jobs_all_sites_{args.search.replace(' ', '_')}.json")
    else:
        print_warning("Aucune offre trouvée")

if __name__ == "__main__":
    main()

