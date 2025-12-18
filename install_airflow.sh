#!/bin/bash
# Script d'installation rapide d'Airflow

echo "🚀 Installation d'Apache Airflow pour l'automatisation du scraping"
echo ""

# Activer l'environnement virtuel
if [ ! -d "venv" ]; then
    echo "❌ Environnement virtuel non trouvé. Créez-le d'abord avec: python3 -m venv venv"
    exit 1
fi

source venv/bin/activate

echo "📦 Installation d'Airflow..."
pip install apache-airflow==2.7.0

echo ""
echo "✅ Airflow installé !"
echo ""
echo "📝 Prochaines étapes :"
echo "1. Configurez votre email dans le fichier .env (voir GUIDE_AIRFLOW.md)"
echo "2. Initialisez Airflow :"
echo "   export AIRFLOW_HOME=~/airflow"
echo "   airflow db init"
echo "   airflow users create --username admin --firstname Admin --lastname User --role Admin --email votre.email@gmail.com --password admin"
echo "3. Démarrez Airflow :"
echo "   Terminal 1: airflow webserver --port 8080"
echo "   Terminal 2: airflow scheduler"
echo ""
echo "📖 Consultez GUIDE_AIRFLOW.md pour plus de détails"

