"""
Fonctions utilitaires
"""
import json
import os
import pandas as pd
from datetime import datetime
from colorama import Fore, Style, init
from tabulate import tabulate

init(autoreset=True)

def ensure_data_dir():
    """Crée le dossier data s'il n'existe pas"""
    if not os.path.exists("data"):
        os.makedirs("data")

def save_json(data, filename):
    """Sauvegarde des données en JSON"""
    ensure_data_dir()
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    # Copier aussi dans Annonces sur le bureau si c'est le fichier jobs.json principal
    import os
    if 'jobs.json' in filename or 'offres' in filename.lower():
        annonces_dir = ensure_desktop_annonces()
        desktop_path = os.path.join(annonces_dir, "offres_linkedin.json")
        try:
            with open(desktop_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"{Fore.GREEN}✓ Fichier JSON copié dans Annonces: offres_linkedin.json")
        except Exception as e:
            pass  # Ne pas afficher d'erreur si ça échoue

def load_json(filename):
    """Charge des données depuis un fichier JSON"""
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def ensure_desktop_annonces():
    """Crée le dossier Annonces sur le bureau s'il n'existe pas"""
    import os
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "Annonces")
    if not os.path.exists(desktop_path):
        os.makedirs(desktop_path)
    return desktop_path

def save_to_excel(data, filename):
    """Sauvegarde des données en Excel"""
    ensure_data_dir()
    if isinstance(data, list) and len(data) > 0:
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)
        print(f"{Fore.GREEN}✓ Données sauvegardées dans {filename}")
        
        # Copier aussi dans Annonces sur le bureau
        import os
        annonces_dir = ensure_desktop_annonces()
        desktop_path = os.path.join(annonces_dir, os.path.basename(filename))
        try:
            df.to_excel(desktop_path, index=False)
            print(f"{Fore.GREEN}✓ Fichier copié dans Annonces: {os.path.basename(filename)}")
        except Exception as e:
            print(f"{Fore.YELLOW}⚠ Impossible de copier dans Annonces: {str(e)}")
    else:
        print(f"{Fore.YELLOW}⚠ Aucune donnée à sauvegarder")

def save_to_csv(data, filename):
    """Sauvegarde des données en CSV"""
    ensure_data_dir()
    if isinstance(data, list) and len(data) > 0:
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"{Fore.GREEN}✓ Données sauvegardées dans {filename}")
        
        # Copier aussi dans Annonces sur le bureau
        import os
        annonces_dir = ensure_desktop_annonces()
        desktop_path = os.path.join(annonces_dir, os.path.basename(filename))
        try:
            df.to_csv(desktop_path, index=False, encoding='utf-8')
            print(f"{Fore.GREEN}✓ Fichier copié dans Annonces: {os.path.basename(filename)}")
        except Exception as e:
            print(f"{Fore.YELLOW}⚠ Impossible de copier dans Annonces: {str(e)}")
    else:
        print(f"{Fore.YELLOW}⚠ Aucune donnée à sauvegarder")

def print_success(message):
    """Affiche un message de succès"""
    print(f"{Fore.GREEN}✓ {message}")

def print_error(message):
    """Affiche un message d'erreur"""
    print(f"{Fore.RED}✗ {message}")

def print_warning(message):
    """Affiche un message d'avertissement"""
    print(f"{Fore.YELLOW}⚠ {message}")

def print_info(message):
    """Affiche un message d'information"""
    print(f"{Fore.CYAN}ℹ {message}")

def display_jobs_table(jobs):
    """Affiche un tableau formaté des offres d'emploi"""
    if not jobs:
        print_warning("Aucune offre trouvée")
        return
    
    table_data = []
    for i, job in enumerate(jobs[:20], 1):  # Limite à 20 pour l'affichage
        table_data.append([
            i,
            job.get('title', 'N/A')[:50],
            job.get('company', 'N/A')[:30],
            job.get('location', 'N/A')[:25],
            job.get('date', 'N/A')
        ])
    
    headers = ["#", "Titre", "Entreprise", "Localisation", "Date"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

def display_skills_table(skills_data):
    """Affiche un tableau formaté des compétences"""
    if not skills_data:
        print_warning("Aucune donnée de compétences")
        return
    
    table_data = []
    for skill, count in sorted(skills_data.items(), key=lambda x: x[1], reverse=True)[:20]:
        table_data.append([skill, count])
    
    headers = ["Compétence", "Nombre d'occurrences"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

def get_timestamp():
    """Retourne un timestamp formaté"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

