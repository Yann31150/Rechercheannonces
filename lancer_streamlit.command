#!/bin/bash
# Script pour lancer l'application Streamlit unifiée

cd "$(dirname "$0")"
source venv/bin/activate

echo "🚀 Lancement de l'application Streamlit unifiée..."
echo "📊 L'application va s'ouvrir dans votre navigateur"
echo "💡 Toutes les fonctionnalités sont maintenant dans une seule application !"
echo ""

streamlit run app_unified.py


