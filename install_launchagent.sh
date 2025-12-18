#!/bin/bash
# Script pour installer le LaunchAgent Airflow

echo "🚀 Installation du LaunchAgent pour Airflow"
echo ""

# Créer le dossier des logs si nécessaire
mkdir -p ~/airflow/logs

# Copier le fichier plist dans le dossier LaunchAgents
LAUNCH_AGENTS_DIR="$HOME/Library/LaunchAgents"
mkdir -p "$LAUNCH_AGENTS_DIR"

PLIST_FILE="com.airflow.jobscraper.plist"
PLIST_PATH="$LAUNCH_AGENTS_DIR/$PLIST_FILE"

# Copier le fichier
cp "$PLIST_FILE" "$PLIST_PATH"
echo "✅ Fichier plist copié dans $PLIST_PATH"

# Charger le LaunchAgent
echo ""
echo "📋 Chargement du LaunchAgent..."
launchctl load "$PLIST_PATH" 2>/dev/null || launchctl load -w "$PLIST_PATH"

if [ $? -eq 0 ]; then
    echo "✅ LaunchAgent chargé avec succès"
else
    echo "⚠️  Le LaunchAgent pourrait déjà être chargé"
fi

echo ""
echo "🎉 Installation terminée !"
echo ""
echo "📝 Commandes utiles :"
echo "   Démarrer maintenant : launchctl start com.airflow.jobscraper"
echo "   Arrêter : launchctl stop com.airflow.jobscraper"
echo "   Vérifier le statut : launchctl list | grep airflow"
echo "   Voir les logs : tail -f ~/airflow/logs/airflow_stdout.log"
echo ""
echo "💡 Airflow démarrera automatiquement au prochain démarrage du Mac"
echo "   et restera en cours d'exécution en permanence."

