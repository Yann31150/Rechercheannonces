# 🚀 Guide Simple : Ollama pour les Lettres de Motivation

## Pourquoi Ollama ?

✅ **Gratuit** - Aucun coût  
✅ **Local** - Vos données restent sur votre ordinateur  
✅ **Simple** - Installation en 2 minutes  
✅ **Meilleures lettres** - Génération intelligente et personnalisée  

## Installation en 3 étapes

### Étape 1 : Installer Ollama

**Sur macOS :**
```bash
# Option 1 : Via Homebrew (recommandé)
brew install ollama

# Option 2 : Télécharger depuis le site
# Allez sur https://ollama.ai et téléchargez l'application
```

### Étape 2 : Lancer Ollama

```bash
ollama serve
```

Laissez cette fenêtre ouverte. Ollama doit tourner en arrière-plan.

### Étape 3 : Télécharger un modèle

Dans un **nouveau terminal**, tapez :

```bash
# Modèle recommandé (léger et rapide, ~2GB)
ollama pull llama3.2

# OU un modèle plus performant (plus gros, ~4GB)
ollama pull mistral
```

## ✅ C'est tout !

Une fois Ollama lancé et le modèle téléchargé, le système l'utilisera **automatiquement** pour générer vos lettres de motivation.

## 🎯 Utilisation

1. **Lancez Ollama** (une seule fois) :
   ```bash
   ollama serve
   ```

2. **Utilisez l'application normalement** :
   - Lancez votre application Streamlit
   - Préparez une candidature
   - La lettre sera générée avec Ollama automatiquement !

## 🔍 Vérifier que ça marche

```bash
# Vérifier qu'Ollama fonctionne
curl http://localhost:11434/api/tags

# Vérifier les modèles installés
ollama list
```

## 💡 Astuces

- **Lancez Ollama au démarrage** : Ajoutez `ollama serve &` dans votre `.zshrc` ou `.bashrc`
- **Modèles disponibles** : `llama3.2` (recommandé), `mistral`, `qwen2.5`, `llama3.1`
- **Si Ollama n'est pas disponible** : Le système utilisera automatiquement les templates (ça fonctionne quand même !)

## 🆘 Problèmes ?

**Ollama ne démarre pas ?**
- Vérifiez que le port 11434 n'est pas utilisé
- Réinstallez Ollama

**Le modèle n'est pas trouvé ?**
- Vérifiez avec `ollama list`
- Téléchargez-le avec `ollama pull llama3.2`

**Le système utilise toujours les templates ?**
- Vérifiez qu'Ollama est lancé : `ollama serve`
- Vérifiez qu'un modèle est installé : `ollama list`

## 📊 Comparaison

| Mode | Qualité | Vitesse | Configuration |
|------|---------|---------|--------------|
| Templates | ✅ Bonne | ⚡ Instantané | Aucune |
| Ollama | ⭐⭐⭐ Excellente | 🐢 5-10 sec | 2 minutes |

**Recommandation** : Utilisez Ollama pour des lettres vraiment personnalisées et professionnelles !

