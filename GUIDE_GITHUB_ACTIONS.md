# Guide de configuration GitHub Actions

Ce guide vous explique comment configurer GitHub Actions pour automatiser le scraping quotidien des offres d'emploi.

## 🎯 Avantages

- ✅ **Gratuit** : 2000 minutes/mois pour les repos privés
- ✅ **Fonctionne même si votre Mac est éteint**
- ✅ **Pas besoin de maintenir un serveur**
- ✅ **Simple à configurer**

## 📋 Prérequis

- Un compte GitHub
- Un repository GitHub (public ou privé)
- Les credentials nécessaires (LinkedIn, email)

## 🚀 Configuration

### 1. Créer les secrets GitHub

Allez dans votre repository GitHub :
1. **Settings** → **Secrets and variables** → **Actions**
2. Cliquez sur **New repository secret**
3. Ajoutez les secrets suivants :

```
LINKEDIN_EMAIL = votre_email_linkedin
LINKEDIN_PASSWORD = votre_mot_de_passe_linkedin
EMAIL_SMTP_SERVER = smtp.gmail.com
EMAIL_SMTP_PORT = 587
EMAIL_SMTP_USER = yanncoignard31@gmail.com
EMAIL_SMTP_PASSWORD = votre_mot_de_passe_application
EMAIL_SENDER = yanncoignard31@gmail.com
EMAIL_RECIPIENT = yanncoignard31@gmail.com
```

### 2. Pousser le code sur GitHub

```bash
# Initialiser Git si pas déjà fait
git init

# Ajouter tous les fichiers
git add .

# Commit
git commit -m "Add job scraper with GitHub Actions"

# Ajouter votre remote GitHub
git remote add origin https://github.com/VOTRE_USERNAME/VOTRE_REPO.git

# Pousser
git push -u origin main
```

### 3. Vérifier le workflow

1. Allez dans l'onglet **Actions** de votre repository
2. Le workflow `Daily Job Scraping` devrait apparaître
3. Vous pouvez le déclencher manuellement avec "Run workflow"

## ⚙️ Fonctionnement

- **Schedule** : Tous les jours à 10h00 UTC (11h00 heure française en hiver)
- **Actions** :
  1. Scrape tous les sites d'emploi
  2. Compare avec les offres précédentes
  3. Envoie un email avec les nouvelles offres
  4. Sauvegarde les résultats

## 🕐 Ajuster l'heure d'exécution

Pour changer l'heure, modifiez le cron dans `.github/workflows/daily_job_scraping.yml` :

```yaml
- cron: '0 10 * * *'  # 10h00 UTC
```

**Heures UTC correspondantes :**
- 10h00 UTC = 11h00 heure française (hiver) / 12h00 (été)
- 9h00 UTC = 10h00 heure française (hiver) / 11h00 (été)
- 8h00 UTC = 9h00 heure française (hiver) / 10h00 (été)

## 📧 Tester manuellement

Vous pouvez déclencher le workflow manuellement :
1. Allez dans **Actions**
2. Sélectionnez "Daily Job Scraping"
3. Cliquez sur "Run workflow"
4. Sélectionnez la branche et cliquez sur "Run"

## 🔍 Voir les logs

1. Allez dans **Actions**
2. Cliquez sur l'exécution que vous voulez voir
3. Cliquez sur le job "scrape-and-notify"
4. Vous verrez les logs de chaque étape

## 📊 Télécharger les résultats

Les résultats sont sauvegardés comme artifacts :
1. Allez dans **Actions**
2. Cliquez sur une exécution
3. Dans "Artifacts", téléchargez "job-results"

## ⚠️ Notes importantes

- Les secrets sont sécurisés et ne sont jamais visibles dans les logs
- Le workflow utilise Ubuntu (Linux), donc certains ajustements peuvent être nécessaires
- Chrome/Chromium est installé automatiquement pour Selenium
- Les fichiers sont sauvegardés localement dans le runner, puis uploadés comme artifacts

## 🆚 Comparaison avec Airflow local

| Aspect | Airflow Local | GitHub Actions |
|--------|---------------|----------------|
| Coût | Gratuit | Gratuit (2000 min/mois) |
| Maintenance | Vous gérez | Géré par GitHub |
| Fiabilité | Dépend de votre Mac | Très fiable |
| Complexité | Moyenne | Simple |
| Logs | Locaux | Accessibles partout |

## 💡 Recommandation

**Utilisez GitHub Actions** si :
- Vous voulez une solution simple et gratuite
- Vous n'avez pas besoin de garder votre Mac allumé
- Vous voulez accéder aux logs depuis n'importe où

**Gardez Airflow local** si :
- Vous voulez plus de contrôle
- Vous avez besoin de plus de 2000 minutes/mois
- Vous voulez des fonctionnalités avancées d'Airflow

