#!/bin/bash
# Script pour lancer l'application de gestion des candidatures

cd "$(dirname "$0")"
source venv/bin/activate

echo "🚀 Lancement de l'application de candidatures..."
echo "📝 L'application va s'ouvrir dans votre navigateur"
echo ""

streamlit run applications_app.py


