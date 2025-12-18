# Guide d'installation et configuration d'Airflow

Ce guide vous explique comment configurer Apache Airflow pour automatiser le scraping quotidien des offres d'emploi et recevoir des alertes par email.

## 📋 Prérequis

- Python 3.8+ (vous avez déjà Python 3.13)
- Un compte email (Gmail recommandé pour la simplicité)
- Un environnement virtuel Python (déjà créé : `venv`)

## 🚀 Installation d'Airflow

### Option 1 : Installation dans l'environnement virtuel existant (recommandé)

```bash
# Activer l'environnement virtuel
source venv/bin/activate

# Installer Airflow
pip install apache-airflow==2.7.0

# Ou pour une installation plus légère (sans providers supplémentaires)
pip install apache-airflow==2.7.0 --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.7.0/constraints-3.13.txt"
```

### Option 2 : Installation avec Docker (plus simple mais nécessite Docker)

Si vous préférez Docker, vous pouvez utiliser l'image officielle d'Airflow.

## ⚙️ Configuration

### 1. Configuration de l'email

Éditez votre fichier `.env` (ou créez-le s'il n'existe pas) :

```bash
# Configuration Email pour les alertes
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_SMTP_USER=votre.email@gmail.com
EMAIL_SMTP_PASSWORD=votre_mot_de_passe_application
EMAIL_SENDER=votre.email@gmail.com
EMAIL_RECIPIENT=votre.email@gmail.com
```

**Important pour Gmail :**
- Vous devez utiliser un **mot de passe d'application** (pas votre mot de passe Gmail normal)
- Pour créer un mot de passe d'application :
  1. Allez sur https://myaccount.google.com/security
  2. Activez la validation en 2 étapes si ce n'est pas déjà fait
  3. Allez dans "Mots de passe des applications"
  4. Créez un nouveau mot de passe d'application pour "Mail"
  5. Utilisez ce mot de passe dans `EMAIL_SMTP_PASSWORD`

**Pour d'autres fournisseurs email :**
- **Outlook/Hotmail** : `smtp-mail.outlook.com`, port 587
- **Yahoo** : `smtp.mail.yahoo.com`, port 587
- **Autres** : Consultez la documentation de votre fournisseur

### 2. Initialisation d'Airflow

```bash
# Créer le répertoire AIRFLOW_HOME (si pas déjà fait)
export AIRFLOW_HOME=~/airflow

# Initialiser la base de données
airflow db init

# Créer un utilisateur admin
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email votre.email@gmail.com \
    --password admin
```

### 3. Configuration du DAG

Le DAG est déjà créé dans `dags/job_scraper_dag.py`. Assurez-vous que :

1. Le chemin vers votre projet est correct dans le DAG
2. Les variables d'environnement sont chargées (via `.env`)

### 4. Tester le scraping manuellement

Avant de lancer Airflow, testez que tout fonctionne :

```bash
# Activer l'environnement virtuel
source venv/bin/activate

# Tester le scraping
python scrape_jobs_airflow.py

# Tester la comparaison et l'email
python -c "from compare_jobs import get_new_jobs; from email_notifier import send_email; new_jobs, all_jobs = get_new_jobs(); send_email(new_jobs, len(all_jobs))"
```

## 🎯 Lancement d'Airflow

### 1. Démarrer le scheduler et le webserver

Dans un premier terminal :

```bash
source venv/bin/activate
export AIRFLOW_HOME=~/airflow
airflow webserver --port 8080
```

Dans un deuxième terminal :

```bash
source venv/bin/activate
export AIRFLOW_HOME=~/airflow
airflow scheduler
```

### 2. Accéder à l'interface web

Ouvrez votre navigateur et allez sur : http://localhost:8080

- **Username** : admin
- **Password** : admin (ou celui que vous avez défini)

### 3. Activer le DAG

1. Dans l'interface Airflow, cherchez le DAG `daily_job_scraper`
2. Activez-le en cliquant sur le toggle à gauche
3. Le DAG s'exécutera automatiquement tous les jours à 10h00

### 4. Tester manuellement le DAG

Pour tester immédiatement sans attendre 10h :

1. Cliquez sur le DAG `daily_job_scraper`
2. Cliquez sur le bouton "Play" (▶️) en haut à droite
3. Sélectionnez "Trigger DAG"

## 📧 Format des emails

Les emails contiendront :
- Le nombre total d'offres
- Le nombre de nouvelles offres détectées
- La liste détaillée des nouvelles offres avec :
  - Titre du poste
  - Entreprise
  - Localisation
  - Source (LinkedIn, Indeed, etc.)
  - Lien vers l'offre

## 🔧 Personnalisation

### Changer l'heure d'exécution

Éditez `dags/job_scraper_dag.py` et modifiez la ligne :

```python
schedule_interval='0 10 * * *',  # Tous les jours à 10h00
```

Format cron : `minute heure jour mois jour_semaine`
- `0 10 * * *` = 10h00 tous les jours
- `0 8 * * 1-5` = 8h00 du lundi au vendredi
- `0 */6 * * *` = Toutes les 6 heures

### Changer les paramètres de recherche

Éditez `scrape_jobs_airflow.py` et modifiez :

```python
keywords = "Data"  # Vos mots-clés
location = config.DEFAULT_LOCATION  # Votre localisation
pages = 2  # Nombre de pages par site
```

### Désactiver l'envoi d'email si aucune nouvelle offre

Éditez `dags/job_scraper_dag.py` dans la fonction `compare_and_notify_task` :

```python
# Ne pas envoyer d'email s'il n'y a pas de nouvelles offres
if new_jobs_count == 0:
    print_info("Aucune nouvelle offre, pas d'email envoyé")
    return {'status': 'success', 'new_jobs': 0, 'email_sent': False}
```

## 🐛 Dépannage

### Le DAG n'apparaît pas

1. Vérifiez que le fichier `dags/job_scraper_dag.py` existe
2. Vérifiez qu'il n'y a pas d'erreurs de syntaxe : `python -m py_compile dags/job_scraper_dag.py`
3. Redémarrez le scheduler : `airflow scheduler`

### Erreur d'import des modules

Assurez-vous que le chemin dans `dags/job_scraper_dag.py` est correct :

```python
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
```

### Erreur d'envoi d'email

1. Vérifiez vos identifiants dans `.env`
2. Pour Gmail, utilisez un mot de passe d'application
3. Testez manuellement : `python email_notifier.py`

### Le scraping échoue

1. Vérifiez que Selenium fonctionne : `python main_unified.py --search "Data" --location "Haute-Garonne, France" --pages 1`
2. Vérifiez les logs dans l'interface Airflow

## 📝 Logs

Les logs d'exécution sont disponibles dans l'interface Airflow :
1. Cliquez sur le DAG
2. Cliquez sur une exécution
3. Cliquez sur une tâche
4. Cliquez sur "Log"

## 🎉 C'est tout !

Votre système est maintenant configuré pour :
- ✅ Scraper automatiquement tous les jours à 10h
- ✅ Détecter les nouvelles offres
- ✅ Vous envoyer un email avec les nouvelles annonces

Bon courage dans votre recherche d'emploi ! 🚀

