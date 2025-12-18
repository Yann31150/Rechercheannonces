#!/bin/bash
# Script d'installation et configuration d'Ollama

echo "🚀 Installation d'Ollama pour générer des lettres de motivation"

# Vérifier si Ollama est déjà installé
if command -v ollama &> /dev/null; then
    echo "✅ Ollama est déjà installé"
else
    echo "📥 Installation d'Ollama..."
    
    # macOS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "Installation via Homebrew..."
        if command -v brew &> /dev/null; then
            brew install ollama
        else
            echo "⚠️  Homebrew n'est pas installé. Téléchargez Ollama depuis: https://ollama.ai"
            echo "Ou installez Homebrew: /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
            exit 1
        fi
    else
        echo "Téléchargez Ollama depuis: https://ollama.ai"
        exit 1
    fi
fi

# Démarrer Ollama en arrière-plan
echo "🔄 Démarrage d'Ollama..."
ollama serve &
OLLAMA_PID=$!
sleep 3

# Vérifier que Ollama fonctionne
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "✅ Ollama est démarré"
else
    echo "⚠️  Ollama ne répond pas. Vérifiez l'installation."
    exit 1
fi

# Télécharger un modèle léger et performant
echo "📦 Téléchargement du modèle llama3.2 (recommandé, ~2GB)..."
ollama pull llama3.2

echo ""
echo "✅ Installation terminée !"
echo ""
echo "📝 Configuration:"
echo "   - Ollama est démarré (PID: $OLLAMA_PID)"
echo "   - Modèle llama3.2 est prêt"
echo ""
echo "💡 Pour utiliser Ollama avec le générateur de lettres:"
echo "   1. Assurez-vous qu'Ollama est lancé: ollama serve"
echo "   2. Le système l'utilisera automatiquement"
echo ""
echo "🛑 Pour arrêter Ollama: kill $OLLAMA_PID"

