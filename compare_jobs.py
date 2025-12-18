"""
Module pour comparer les nouvelles annonces avec les anciennes
"""
import json
import os
from datetime import datetime
from utils import load_json, save_json, print_info, print_success
import config


def get_job_signature(job):
    """Crée une signature unique pour une offre d'emploi"""
    # Utilise l'URL comme identifiant principal, sinon titre + entreprise + source
    if job.get('url'):
        return job.get('url')
    return f"{job.get('title', '')}_{job.get('company', '')}_{job.get('source', '')}"


def compare_jobs(old_jobs, new_jobs):
    """
    Compare deux listes d'offres et retourne les nouvelles
    
    Args:
        old_jobs: Liste des anciennes offres
        new_jobs: Liste des nouvelles offres
    
    Returns:
        Tuple (nouvelles_offres, offres_supprimees)
    """
    # Créer des dictionnaires avec les signatures comme clés
    old_signatures = {get_job_signature(job): job for job in old_jobs}
    new_signatures = {get_job_signature(job): job for job in new_jobs}
    
    # Nouvelles offres : dans new_jobs mais pas dans old_jobs
    new_job_signatures = set(new_signatures.keys()) - set(old_signatures.keys())
    new_jobs_list = [new_signatures[sig] for sig in new_job_signatures]
    
    # Offres supprimées : dans old_jobs mais pas dans new_jobs
    removed_job_signatures = set(old_signatures.keys()) - set(new_signatures.keys())
    removed_jobs_list = [old_signatures[sig] for sig in removed_job_signatures]
    
    return new_jobs_list, removed_jobs_list


def save_jobs_history(jobs, filename=None):
    """Sauvegarde l'historique des offres avec timestamp"""
    if filename is None:
        filename = config.JOBS_FILE.replace('.json', '_history.json')
    
    history_file = os.path.join(config.DATA_DIR, 'jobs_history.json')
    
    # Charger l'historique existant
    if os.path.exists(history_file):
        with open(history_file, 'r', encoding='utf-8') as f:
            history = json.load(f)
    else:
        history = []
    
    # Ajouter la nouvelle entrée
    history_entry = {
        'timestamp': datetime.now().isoformat(),
        'total_jobs': len(jobs),
        'jobs': jobs
    }
    history.append(history_entry)
    
    # Garder seulement les 30 derniers jours
    if len(history) > 30:
        history = history[-30:]
    
    # Sauvegarder
    save_json(history, history_file)
    return history_file


def get_new_jobs():
    """
    Compare les offres actuelles avec les précédentes et retourne les nouvelles
    
    Returns:
        Tuple (nouvelles_offres, total_offres)
    """
    current_jobs_file = config.JOBS_FILE
    previous_jobs_file = os.path.join(config.DATA_DIR, 'jobs_previous.json')
    
    # Charger les offres actuelles
    if not os.path.exists(current_jobs_file):
        print_info("Aucune offre actuelle trouvée")
        return [], []
    
    current_jobs = load_json(current_jobs_file)
    
    # Charger les offres précédentes
    if not os.path.exists(previous_jobs_file):
        print_info("Première exécution : toutes les offres sont considérées comme nouvelles")
        # Sauvegarder les offres actuelles comme précédentes
        save_json(current_jobs, previous_jobs_file)
        return current_jobs, current_jobs
    
    previous_jobs = load_json(previous_jobs_file)
    
    # Comparer
    new_jobs, removed_jobs = compare_jobs(previous_jobs, current_jobs)
    
    print_info(f"Total offres actuelles: {len(current_jobs)}")
    print_info(f"Nouvelles offres: {len(new_jobs)}")
    print_info(f"Offres supprimées: {len(removed_jobs)}")
    
    # Sauvegarder les offres actuelles comme précédentes pour la prochaine fois
    save_json(current_jobs, previous_jobs_file)
    
    # Sauvegarder l'historique
    save_jobs_history(current_jobs)
    
    return new_jobs, current_jobs


if __name__ == "__main__":
    # Test du module
    new_jobs, all_jobs = get_new_jobs()
    print_success(f"✅ {len(new_jobs)} nouvelles offres détectées sur {len(all_jobs)} total")

