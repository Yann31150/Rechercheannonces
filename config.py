"""
Configuration pour l'outil de recherche d'emploi LinkedIn
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Credentials LinkedIn
LINKEDIN_EMAIL = os.getenv('LINKEDIN_EMAIL', '')
LINKEDIN_PASSWORD = os.getenv('LINKEDIN_PASSWORD', '')

# Paramètres de recherche par défaut
DEFAULT_KEYWORDS = [
    "Data Scientist",
    "Data Analyst",
    "Data Engineer",
    "Machine Learning Engineer",
    "Business Intelligence",
    "Data Science"
]

DEFAULT_LOCATIONS = [
    "Haute-Garonne, France",
    "Toulouse, France",
    "Remote"
]

# Localisation par défaut pour les recherches
DEFAULT_LOCATION = "Haute-Garonne, France"

# Compétences techniques à rechercher
TECHNICAL_SKILLS = [
    "Python", "R", "SQL", "Java", "Scala",
    "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch",
    "Pandas", "NumPy", "Scikit-learn",
    "Tableau", "Power BI", "Qlik",
    "Hadoop", "Spark", "Kafka",
    "AWS", "Azure", "GCP",
    "Docker", "Kubernetes",
    "Git", "CI/CD"
]

# Templates de messages de networking
NETWORKING_MESSAGES = {
    "data_scientist": """Bonjour {name},

Je suis actuellement à la recherche d'opportunités en Data Science et j'ai remarqué votre profil qui m'inspire beaucoup.

J'aimerais en savoir plus sur votre parcours et vos expériences dans le domaine. Seriez-vous disponible pour un échange rapide ?

Merci d'avance !
{your_name}""",

    "data_analyst": """Bonjour {name},

En tant que professionnel passionné par la data, je suis impressionné par votre parcours en Data Analysis.

Je serais ravi d'échanger avec vous sur les tendances du secteur et vos conseils pour quelqu'un qui cherche à évoluer dans ce domaine.

Cordialement,
{your_name}""",

    "recruiter": """Bonjour {name},

Je suis actuellement à la recherche d'opportunités en Data Science/Analysis et je pense que mon profil pourrait correspondre à certaines de vos missions.

Voici mes compétences principales :
- {skills}

Seriez-vous disponible pour discuter d'éventuelles opportunités ?

Merci !
{your_name}"""
}

# Paramètres de scraping
SCRAPING_CONFIG = {
    "delay_between_requests": 2,  # secondes
    "max_pages": 5,  # nombre maximum de pages à scraper
    "headless": False,  # mode headless du navigateur
    "timeout": 30  # timeout en secondes
}

# Fichiers de stockage
DATA_DIR = "data"
JOBS_FILE = f"{DATA_DIR}/jobs.json"
SKILLS_FILE = f"{DATA_DIR}/skills_analysis.json"
TRACKED_JOBS_FILE = f"{DATA_DIR}/tracked_jobs.json"

# Votre profil
YOUR_NAME = os.getenv('YOUR_NAME', 'Votre Nom')
YOUR_SKILLS = os.getenv('YOUR_SKILLS', 'Python, SQL, Machine Learning').split(', ')

# Configuration Email pour les alertes
EMAIL_SMTP_SERVER = os.getenv('EMAIL_SMTP_SERVER', 'smtp.gmail.com')
EMAIL_SMTP_PORT = int(os.getenv('EMAIL_SMTP_PORT', '587'))
EMAIL_SMTP_USER = os.getenv('EMAIL_SMTP_USER', '')
EMAIL_SMTP_PASSWORD = os.getenv('EMAIL_SMTP_PASSWORD', '')  # Mot de passe d'application pour Gmail
EMAIL_SENDER = os.getenv('EMAIL_SENDER', EMAIL_SMTP_USER)
EMAIL_RECIPIENT = os.getenv('EMAIL_RECIPIENT', '')  # Votre email pour recevoir les alertes

