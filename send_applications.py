"""
Script pour faciliter l'envoi de candidatures
⚠️ Mode semi-automatique : prépare tout mais nécessite validation manuelle
"""
import argparse
import json
import os
from application_manager import ApplicationManager
from auto_applicant import AutoApplicant
from utils import load_json, print_success, print_info, print_warning
import config

def main():
    parser = argparse.ArgumentParser(description="Facilite l'envoi de candidatures")
    
    parser.add_argument('--mode', choices=['prepare', 'assist', 'links'], default='links',
                       help='Mode: prepare (prépare), assist (assiste), links (crée page HTML)')
    parser.add_argument('--job-url', type=str, help='URL de l\'offre spécifique')
    parser.add_argument('--all-prepared', action='store_true', help='Traiter toutes les candidatures préparées')
    
    args = parser.parse_args()
    
    manager = ApplicationManager()
    
    if args.mode == 'links':
        # Créer une page HTML avec tous les liens
        print_info("Création d'une page HTML avec tous les liens de candidature...")
        
        # Charger les offres
        jobs = load_json(config.JOBS_FILE) if os.path.exists(config.JOBS_FILE) else []
        
        # Filtrer celles qui ont des candidatures préparées
        prepared_apps = manager.get_applications_by_status('prepared')
        prepared_urls = {app.get('job_url') for app in prepared_apps}
        
        jobs_to_apply = [j for j in jobs if j.get('url') in prepared_urls]
        
        if not jobs_to_apply:
            print_warning("Aucune candidature préparée trouvée")
            return
        
        # Charger les infos personnelles pour le CV
        personal_info = {}
        if os.path.exists("personal_info.json"):
            personal_info = json.load(open("personal_info.json"))
        
        applicant = AutoApplicant()
        html_file = applicant.prepare_application_links(
            jobs_to_apply,
            cv_path=personal_info.get('cv_path')
        )
        
        print_success(f"✅ Page créée: {html_file}")
        print_info("Ouvrez ce fichier dans votre navigateur pour accéder à toutes les candidatures")
        
    elif args.mode == 'assist':
        # Mode assisté : ouvre le navigateur et préremplit
        if not args.job_url:
            print_error("--job-url requis en mode assist")
            return
        
        # Charger les infos
        personal_info = {}
        if os.path.exists("personal_info.json"):
            personal_info = json.load(open("personal_info.json"))
        
        # Trouver la candidature préparée
        prepared_apps = manager.get_applications_by_status('prepared')
        app = next((a for a in prepared_apps if a.get('job_url') == args.job_url), None)
        
        if not app:
            print_warning("Aucune candidature préparée pour cette offre")
            return
        
        applicant = AutoApplicant()
        applicant.setup_driver()
        
        # Se connecter à LinkedIn
        if 'linkedin' in args.job_url.lower():
            email = personal_info.get('email') or config.LINKEDIN_EMAIL
            password = config.LINKEDIN_PASSWORD
            if not applicant.login_linkedin(email, password):
                applicant.close()
                return
        
        # Aider à postuler
        applicant.apply_to_linkedin_job(
            args.job_url,
            app.get('cover_letter_path'),
            personal_info.get('cv_path')
        )
        
        applicant.close()
    
    elif args.mode == 'prepare':
        print_info("Utilisez l'application Streamlit pour préparer les candidatures")
        print_info("Double-cliquez sur '📝 Candidatures.command'")

if __name__ == "__main__":
    main()


