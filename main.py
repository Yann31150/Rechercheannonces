"""
Script principal pour l'outil de recherche d'emploi LinkedIn
"""
import argparse
import sys
from scraper import LinkedInJobScraper
from analyzer import SkillsAnalyzer
from networker import LinkedInNetworker
from tracker import JobTracker
from utils import (
    display_jobs_table, display_skills_table, save_to_excel, save_to_csv,
    print_success, print_error, print_info, print_warning, load_json
)
import config

def main():
    parser = argparse.ArgumentParser(
        description="Outil de recherche d'emploi Data sur LinkedIn",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  python main.py --search "Data Scientist" --location "Paris"
  python main.py --analyze-skills
  python main.py --network --keywords "Data Science" --limit 5
  python main.py --track --keywords "Data Analyst"
        """
    )
    
    # Arguments pour la recherche
    parser.add_argument('--search', type=str, help='Mots-clés de recherche')
    parser.add_argument('--location', type=str, default=config.DEFAULT_LOCATION, help='Localisation (ex: "Haute-Garonne, France")')
    parser.add_argument('--experience', type=str, default='', help='Niveau d\'expérience (1, 2, 3, 4)')
    parser.add_argument('--pages', type=int, default=3, help='Nombre de pages à scraper (défaut: 3)')
    
    # Arguments pour l'analyse
    parser.add_argument('--analyze-skills', action='store_true', help='Analyser les compétences demandées')
    parser.add_argument('--skills-gap', action='store_true', help='Identifier les compétences manquantes')
    
    # Arguments pour le networking
    parser.add_argument('--network', action='store_true', help='Lancer le networking automatique')
    parser.add_argument('--keywords', type=str, help='Mots-clés pour rechercher des contacts')
    parser.add_argument('--limit', type=int, default=10, help='Nombre maximum de contacts (défaut: 10)')
    parser.add_argument('--message-type', type=str, default='data_scientist', 
                       choices=['data_scientist', 'data_analyst', 'recruiter'],
                       help='Type de message à envoyer')
    
    # Arguments pour le suivi
    parser.add_argument('--track', action='store_true', help='Suivre les nouvelles offres')
    
    # Arguments généraux
    parser.add_argument('--headless', action='store_true', help='Mode headless (sans interface graphique)')
    parser.add_argument('--export', type=str, choices=['excel', 'csv', 'json'], 
                       help='Format d\'export (excel, csv, json)')
    
    args = parser.parse_args()
    
    # Si aucun argument, afficher l'aide
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    # Mode recherche d'offres
    if args.search:
        print_info("=== MODE RECHERCHE D'OFFRES ===")
        scraper = LinkedInJobScraper(headless=args.headless)
        
        try:
            scraper.setup_driver()
            
            if not scraper.login():
                print_error("Échec de la connexion. Vérifiez vos identifiants dans .env")
                scraper.close()
                return
            
            jobs = scraper.search_jobs(
                keywords=args.search,
                location=args.location,
                experience_level=args.experience,
                max_pages=args.pages
            )
            
            if jobs:
                display_jobs_table(jobs)
                scraper.save_results()
                
                # Export
                if args.export == 'excel':
                    save_to_excel(jobs, f"data/jobs_{args.search.replace(' ', '_')}.xlsx")
                elif args.export == 'csv':
                    save_to_csv(jobs, f"data/jobs_{args.search.replace(' ', '_')}.csv")
                
                # Analyse automatique si demandée
                if args.analyze_skills:
                    analyze_skills(jobs)
            else:
                print_warning("Aucune offre trouvée")
            
        except KeyboardInterrupt:
            print_warning("\nInterruption par l'utilisateur")
        except Exception as e:
            print_error(f"Erreur: {str(e)}")
        finally:
            scraper.close()
    
    # Mode analyse des compétences
    elif args.analyze_skills:
        print_info("=== MODE ANALYSE DES COMPÉTENCES ===")
        jobs = load_json(config.JOBS_FILE)
        
        if not jobs:
            print_error("Aucune donnée d'offres trouvée. Lancez d'abord une recherche avec --search")
            return
        
        analyze_skills(jobs, show_gap=args.skills_gap)
    
    # Mode networking
    elif args.network:
        print_info("=== MODE NETWORKING ===")
        print_warning("⚠️  Utilisez cette fonctionnalité avec modération pour respecter les limites de LinkedIn")
        
        keywords = args.keywords or "Data Science"
        networker = LinkedInNetworker(headless=args.headless)
        
        try:
            networker.setup_driver()
            
            if not networker.login():
                print_error("Échec de la connexion. Vérifiez vos identifiants dans .env")
                networker.close()
                return
            
            confirm = input(f"Êtes-vous sûr de vouloir envoyer des demandes de connexion ? (oui/non): ")
            if confirm.lower() != 'oui':
                print_info("Opération annulée")
                networker.close()
                return
            
            networker.network_with_keywords(
                keywords=keywords,
                limit=args.limit,
                message_template=args.message_type
            )
            
        except KeyboardInterrupt:
            print_warning("\nInterruption par l'utilisateur")
        except Exception as e:
            print_error(f"Erreur: {str(e)}")
        finally:
            networker.close()
    
    # Mode suivi
    elif args.track:
        print_info("=== MODE SUIVI DES OFFRES ===")
        keywords = args.keywords or "Data Scientist"
        
        tracker = JobTracker()
        new_jobs = tracker.track_new_jobs(
            keywords=keywords,
            location=args.location,
            max_pages=args.pages
        )
        
        if new_jobs:
            display_jobs_table(new_jobs)
            
            if args.export == 'excel':
                save_to_excel(new_jobs, f"data/new_jobs_{keywords.replace(' ', '_')}.xlsx")
            elif args.export == 'csv':
                save_to_csv(new_jobs, f"data/new_jobs_{keywords.replace(' ', '_')}.csv")
        else:
            print_info("Aucune nouvelle offre trouvée")
    
    else:
        parser.print_help()

def analyze_skills(jobs, show_gap=False):
    """Analyse les compétences des offres"""
    analyzer = SkillsAnalyzer()
    skills_data = analyzer.analyze_jobs(jobs)
    
    print_info("\n=== TOP COMPÉTENCES DEMANDÉES ===")
    display_skills_table(analyzer.get_top_skills(20))
    
    if show_gap:
        print_info("\n=== COMPÉTENCES À DÉVELOPPER ===")
        gap = analyzer.get_skills_gap(config.YOUR_SKILLS)
        if gap:
            display_skills_table(dict(list(gap.items())[:20]))
        else:
            print_success("Vous avez toutes les compétences principales !")
    
    stats = analyzer.get_statistics()
    print_info(f"\nStatistiques:")
    print_info(f"  - Offres analysées: {stats.get('total_jobs', 0)}")
    print_info(f"  - Compétences identifiées: {stats.get('total_skills', 0)}")
    print_info(f"  - Compétence la plus demandée: {stats.get('most_demanded', ['N/A', 0])[0]}")
    
    analyzer.generate_report()

if __name__ == "__main__":
    main()

