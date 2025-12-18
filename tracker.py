"""
Module de suivi des nouvelles offres d'emploi
"""
import json
from datetime import datetime
from scraper import LinkedInJobScraper
from utils import load_json, save_json, print_success, print_info, print_warning
import config

class JobTracker:
    def __init__(self):
        self.tracked_jobs_file = config.TRACKED_JOBS_FILE
        self.tracked_jobs = load_json(self.tracked_jobs_file)
        
    def track_new_jobs(self, keywords, location="", max_pages=3):
        """Suit les nouvelles offres correspondant aux critères"""
        print_info("Recherche de nouvelles offres...")
        
        scraper = LinkedInJobScraper(headless=True)
        scraper.setup_driver()
        
        if not scraper.login():
            scraper.close()
            return []
        
        new_jobs = scraper.search_jobs(keywords, location, max_pages=max_pages)
        scraper.close()
        
        # Identifier les nouvelles offres
        tracked_urls = {job.get('url', '') for job in self.tracked_jobs}
        truly_new_jobs = [
            job for job in new_jobs 
            if job.get('url', '') not in tracked_urls
        ]
        
        if truly_new_jobs:
            print_success(f"{len(truly_new_jobs)} nouvelles offres trouvées !")
            self.tracked_jobs.extend(truly_new_jobs)
            self._save_tracked_jobs()
        else:
            print_info("Aucune nouvelle offre trouvée")
        
        return truly_new_jobs
    
    def get_tracked_jobs(self):
        """Retourne toutes les offres suivies"""
        return self.tracked_jobs
    
    def get_jobs_by_keyword(self, keyword):
        """Retourne les offres contenant un mot-clé"""
        keyword_lower = keyword.lower()
        return [
            job for job in self.tracked_jobs
            if keyword_lower in job.get('title', '').lower() or 
               keyword_lower in job.get('description', '').lower()
        ]
    
    def get_recent_jobs(self, days=7):
        """Retourne les offres des N derniers jours"""
        from datetime import timedelta
        cutoff_date = datetime.now() - timedelta(days=days)
        
        recent_jobs = []
        for job in self.tracked_jobs:
            job_date_str = job.get('date', '')
            if job_date_str:
                try:
                    # Essayer de parser différentes formats de date
                    job_date = datetime.fromisoformat(job_date_str.replace('Z', '+00:00'))
                    if job_date >= cutoff_date:
                        recent_jobs.append(job)
                except:
                    # Si la date ne peut pas être parsée, inclure quand même
                    recent_jobs.append(job)
        
        return recent_jobs
    
    def _save_tracked_jobs(self):
        """Sauvegarde les offres suivies"""
        save_json(self.tracked_jobs, self.tracked_jobs_file)
    
    def clear_old_jobs(self, days=30):
        """Supprime les offres de plus de N jours"""
        from datetime import timedelta
        cutoff_date = datetime.now() - timedelta(days=days)
        
        initial_count = len(self.tracked_jobs)
        self.tracked_jobs = [
            job for job in self.tracked_jobs
            if self._is_job_recent(job, cutoff_date)
        ]
        
        removed = initial_count - len(self.tracked_jobs)
        if removed > 0:
            self._save_tracked_jobs()
            print_success(f"{removed} offres anciennes supprimées")
        
        return removed
    
    def _is_job_recent(self, job, cutoff_date):
        """Vérifie si une offre est récente"""
        job_date_str = job.get('date', '')
        if not job_date_str:
            return True  # Garder si pas de date
        
        try:
            job_date = datetime.fromisoformat(job_date_str.replace('Z', '+00:00'))
            return job_date >= cutoff_date
        except:
            return True  # Garder si date invalide


