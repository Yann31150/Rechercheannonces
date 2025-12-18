#!/bin/bash
# Script pour créer le raccourci sur le bureau

PROJECT_DIR="/Users/yanndanneels-coignard/Projet/Test1"
DESKTOP="$HOME/Desktop"

# Créer le raccourci sur le bureau
ln -sf "$PROJECT_DIR/lancer_recherche.command" "$DESKTOP/🔍 Recherche LinkedIn.command"
chmod +x "$DESKTOP/🔍 Recherche LinkedIn.command"

echo "✅ Raccourci créé sur le bureau : 🔍 Recherche LinkedIn.command"
echo ""
echo "Vous pouvez maintenant double-cliquer sur l'icône pour lancer la recherche !"


