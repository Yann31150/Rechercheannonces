"""
Gestionnaire de candidatures automatiques
"""
import json
import os
from datetime import datetime
from cover_letter_generator import CoverLetterGenerator
from utils import load_json, save_json, print_success, print_info, print_warning, print_error
import config

class ApplicationManager:
    def __init__(self):
        self.applications_file = "data/applications.json"
        self.generator = CoverLetterGenerator()
        self.applications = self._load_applications()
        
    def _load_applications(self):
        """Charge les candidatures déjà envoyées"""
        if os.path.exists(self.applications_file):
            return load_json(self.applications_file)
        return []
    
    def _save_applications(self):
        """Sauvegarde les candidatures"""
        save_json(self.applications, self.applications_file)
    
    def prepare_application(self, job, personal_info, cv_path=None):
        """Prépare une candidature (génère la lettre)"""
        try:
            # Vérifier si déjà candidaté
            job_url = job.get('url', '')
            if self.has_applied(job_url):
                print_warning(f"Déjà candidaté pour: {job.get('title', 'N/A')}")
                return None
            
            # Générer la lettre de motivation
            print_info(f"Génération de la lettre pour: {job.get('title', 'N/A')}")
            cover_letter = self.generator.generate_cover_letter(job, personal_info, cv_path)
            
            # Sauvegarder la lettre
            letter_path = self.generator.save_cover_letter(cover_letter, job)
            
            # Enregistrer la candidature
            application = {
                'job_title': job.get('title'),
                'company': job.get('company'),
                'location': job.get('location'),
                'job_url': job_url,
                'source': job.get('source', 'LinkedIn'),
                'cover_letter_path': letter_path,
                'cv_path': cv_path,
                'status': 'prepared',  # prepared, sent, rejected, accepted
                'prepared_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'sent_at': None,
                'notes': ''
            }
            
            self.applications.append(application)
            self._save_applications()
            
            print_success(f"Candidature préparée pour: {job.get('title', 'N/A')}")
            return application
            
        except Exception as e:
            print_error(f"Erreur lors de la préparation: {str(e)}")
            return None
    
    def has_applied(self, job_url):
        """Vérifie si on a déjà candidaté pour cette offre"""
        if not job_url:
            return False
        return any(app.get('job_url') == job_url for app in self.applications)
    
    def mark_as_sent(self, job_url, sent_at=None):
        """Marque une candidature comme envoyée"""
        for app in self.applications:
            if app.get('job_url') == job_url:
                app['status'] = 'sent'
                app['sent_at'] = sent_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self._save_applications()
                return True
        return False
    
    def update_application_status(self, job_url, new_status, notes=None):
        """Met à jour le statut d'une candidature"""
        for app in self.applications:
            if app.get('job_url') == job_url:
                app['status'] = new_status
                if new_status == 'sent' and not app.get('sent_at'):
                    app['sent_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if notes is not None:
                    app['notes'] = notes
                self._save_applications()
                return True
        return False
    
    def update_notes(self, job_url, notes):
        """Met à jour les notes d'une candidature"""
        for app in self.applications:
            if app.get('job_url') == job_url:
                app['notes'] = notes
                self._save_applications()
                return True
        return False
    
    def delete_application(self, job_url):
        """Supprime une candidature"""
        initial_count = len(self.applications)
        self.applications = [app for app in self.applications if app.get('job_url') != job_url]
        
        if len(self.applications) < initial_count:
            self._save_applications()
            return True
        return False
    
    def get_applications_by_status(self, status=None):
        """Récupère les candidatures par statut"""
        if status:
            return [app for app in self.applications if app.get('status') == status]
        return self.applications
    
    def get_statistics(self):
        """Retourne des statistiques sur les candidatures"""
        total = len(self.applications)
        by_status = {}
        for app in self.applications:
            status = app.get('status', 'prepared')
            by_status[status] = by_status.get(status, 0) + 1
        
        return {
            'total': total,
            'by_status': by_status,
            'prepared': by_status.get('prepared', 0),
            'sent': by_status.get('sent', 0),
            'accepted': by_status.get('accepted', 0),
            'rejected': by_status.get('rejected', 0)
        }

