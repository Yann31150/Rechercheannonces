#!/bin/bash
# Script pour désinstaller le LaunchAgent Airflow

echo "🛑 Désinstallation du LaunchAgent Airflow"
echo ""

LAUNCH_AGENTS_DIR="$HOME/Library/LaunchAgents"
PLIST_FILE="com.airflow.jobscraper.plist"
PLIST_PATH="$LAUNCH_AGENTS_DIR/$PLIST_FILE"

# Arrêter le service
echo "📋 Arrêt du service..."
launchctl stop com.airflow.jobscraper 2>/dev/null
launchctl unload "$PLIST_PATH" 2>/dev/null || launchctl unload -w "$PLIST_PATH" 2>/dev/null

# Supprimer le fichier
if [ -f "$PLIST_PATH" ]; then
    rm "$PLIST_PATH"
    echo "✅ Fichier plist supprimé"
else
    echo "⚠️  Fichier plist non trouvé"
fi

echo ""
echo "✅ Désinstallation terminée"
echo ""
echo "💡 Airflow ne démarrera plus automatiquement au démarrage du Mac"

