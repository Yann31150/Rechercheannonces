#!/bin/bash
# Script pour démarrer Airflow facilement

echo "🚀 Démarrage d'Airflow..."
echo ""

# Aller dans le répertoire du projet
cd "$(dirname "$0")"

# Activer l'environnement virtuel
source venv/bin/activate

# Configurer AIRFLOW_HOME
export AIRFLOW_HOME=~/airflow

# S'assurer que le DAG est dans le bon dossier
if [ ! -f ~/airflow/dags/job_scraper_dag.py ]; then
    echo "📋 Copie du DAG dans ~/airflow/dags/..."
    mkdir -p ~/airflow/dags
    cp dags/job_scraper_dag.py ~/airflow/dags/
    echo "✅ DAG copié"
    echo ""
fi

# Démarrer Airflow en mode standalone
echo "🌐 Démarrage d'Airflow standalone..."
echo "   Interface web: http://localhost:8080"
echo "   (Le mot de passe admin sera affiché ci-dessous)"
echo ""
echo "⚠️  Pour arrêter: Ctrl+C"
echo ""

airflow standalone

