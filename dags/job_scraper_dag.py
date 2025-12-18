"""
DAG Airflow pour le scraping quotidien des offres d'emploi
Exécute le scraping tous les jours à 10h00 et envoie un email avec les nouvelles annonces
"""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
import sys
import os

# Ajouter le répertoire parent au path pour importer les modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scrape_jobs_airflow import run_daily_scraping
from compare_jobs import get_new_jobs
from email_notifier import send_email
from utils import print_info, print_success, print_error


def scrape_jobs_task(**context):
    """Tâche de scraping"""
    print_info("🚀 Démarrage de la tâche de scraping...")
    success, message, count = run_daily_scraping()
    
    if success:
        print_success(f"✅ Scraping terminé: {message}")
        # Passer le nombre d'offres au contexte pour la tâche suivante
        context['ti'].xcom_push(key='jobs_count', value=count)
        return {'status': 'success', 'jobs_count': count, 'message': message}
    else:
        print_error(f"❌ Scraping échoué: {message}")
        raise Exception(f"Scraping échoué: {message}")


def compare_and_notify_task(**context):
    """Tâche de comparaison et envoi d'email"""
    print_info("📊 Comparaison des nouvelles offres...")
    
    try:
        # Récupérer les nouvelles offres
        new_jobs, all_jobs = get_new_jobs()
        
        jobs_count = len(all_jobs)
        new_jobs_count = len(new_jobs)
        
        print_info(f"📈 Total: {jobs_count} offres")
        print_info(f"🆕 Nouvelles: {new_jobs_count} offres")
        
        # Toujours envoyer un email, même s'il n'y a pas de nouvelles offres
        # (pour confirmer que le scraping a fonctionné)
        print_info("📧 Envoi de l'email de notification...")
        email_sent = send_email(new_jobs, jobs_count)
        
        if email_sent:
            print_success(f"✅ Email envoyé avec {new_jobs_count} nouvelles offres")
            return {
                'status': 'success',
                'total_jobs': jobs_count,
                'new_jobs': new_jobs_count,
                'email_sent': True
            }
        else:
            print_error("❌ Échec de l'envoi de l'email")
            return {
                'status': 'warning',
                'total_jobs': jobs_count,
                'new_jobs': new_jobs_count,
                'email_sent': False
            }
            
    except Exception as e:
        error_msg = f"Erreur lors de la comparaison/notification: {str(e)}"
        print_error(error_msg)
        raise Exception(error_msg)


# Définition du DAG
default_args = {
    'owner': 'job_scraper',
    'depends_on_past': False,
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2024, 1, 1),
}

dag = DAG(
    'daily_job_scraper',
    default_args=default_args,
    description='Scraping quotidien des offres d\'emploi Data et envoi d\'alertes par email',
    schedule_interval='0 10 * * *',  # Tous les jours à 10h00
    catchup=False,
    tags=['scraping', 'jobs', 'data', 'email'],
)

# Tâche 1: Scraping
scrape_task = PythonOperator(
    task_id='scrape_all_sites',
    python_callable=scrape_jobs_task,
    dag=dag,
)

# Tâche 2: Comparaison et notification
notify_task = PythonOperator(
    task_id='compare_and_notify',
    python_callable=compare_and_notify_task,
    dag=dag,
)

# Définir l'ordre d'exécution
scrape_task >> notify_task

