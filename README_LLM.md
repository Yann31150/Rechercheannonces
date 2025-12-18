# 🤖 Génération de Lettres de Motivation avec LLM

Ce système permet de générer des lettres de motivation personnalisées et cohérentes en utilisant des modèles de langage (LLM).

## 🎯 Options disponibles

### 1. **Ollama (Recommandé - Gratuit et Local)** ⭐

**Avantages :**
- ✅ Gratuit
- ✅ Fonctionne localement (pas de clé API)
- ✅ Données privées (rien n'est envoyé sur internet)
- ✅ Plusieurs modèles disponibles

**Installation :**

1. **Installer Ollama :**
   ```bash
   # macOS
   brew install ollama
   # ou téléchargez depuis https://ollama.ai
   ```

2. **Lancer Ollama :**
   ```bash
   ollama serve
   ```

3. **Télécharger un modèle :**
   ```bash
   # Modèles recommandés (choisissez-en un) :
   ollama pull llama3.2        # Léger et rapide (2GB)
   ollama pull mistral         # Bon compromis (4GB)
   ollama pull qwen2.5         # Excellent pour le français (7GB)
   ollama pull llama3.1        # Plus performant (4.7GB)
   ```

4. **Configuration :**
   Créez un fichier `.env` à la racine du projet :
   ```env
   LLM_PROVIDER=ollama
   LLM_MODEL=llama3.2  # ou le modèle que vous avez téléchargé
   ```

### 2. **OpenAI API (Payant mais très performant)**

**Avantages :**
- ✅ Excellent pour le français
- ✅ Très rapide
- ✅ Modèles GPT-4 disponibles

**Installation :**

1. **Installer le package :**
   ```bash
   pip install openai
   ```

2. **Obtenir une clé API :**
   - Allez sur https://platform.openai.com
   - Créez un compte
   - Générez une clé API

3. **Configuration :**
   Dans votre fichier `.env` :
   ```env
   LLM_PROVIDER=openai
   LLM_MODEL=gpt-4o-mini  # ou gpt-4, gpt-3.5-turbo
   OPENAI_API_KEY=votre_cle_api_ici
   ```

**Coûts approximatifs :**
- GPT-4o-mini : ~$0.15 / 1M tokens (très économique)
- GPT-4 : ~$30 / 1M tokens (plus cher mais meilleur)

### 3. **Mistral AI (Bon compromis prix/performance)**

**Avantages :**
- ✅ Bon rapport qualité/prix
- ✅ Excellent pour le français
- ✅ API européenne

**Installation :**

1. **Installer le package :**
   ```bash
   pip install mistralai
   ```

2. **Obtenir une clé API :**
   - Allez sur https://console.mistral.ai
   - Créez un compte
   - Générez une clé API

3. **Configuration :**
   Dans votre fichier `.env` :
   ```env
   LLM_PROVIDER=mistral
   LLM_MODEL=mistral-medium  # ou mistral-small, mistral-large
   MISTRAL_API_KEY=votre_cle_api_ici
   ```

**Coûts approximatifs :**
- Mistral-small : ~$0.20 / 1M tokens
- Mistral-medium : ~$2.70 / 1M tokens

### 4. **Anthropic Claude (Excellent pour le français)**

**Avantages :**
- ✅ Excellent pour le français
- ✅ Très bon contexte
- ✅ Modèles très performants

**Installation :**

1. **Installer le package :**
   ```bash
   pip install anthropic
   ```

2. **Obtenir une clé API :**
   - Allez sur https://console.anthropic.com
   - Créez un compte
   - Générez une clé API

3. **Configuration :**
   Dans votre fichier `.env` :
   ```env
   LLM_PROVIDER=claude
   LLM_MODEL=claude-3-5-sonnet-20241022  # ou claude-3-opus, claude-3-haiku
   ANTHROPIC_API_KEY=votre_cle_api_ici
   ```

**Coûts approximatifs :**
- Claude-3 Haiku : ~$0.25 / 1M tokens
- Claude-3 Sonnet : ~$3 / 1M tokens
- Claude-3 Opus : ~$15 / 1M tokens

## 🚀 Utilisation

### Configuration automatique

Le système détecte automatiquement votre configuration depuis le fichier `.env` ou utilise Ollama par défaut.

### Dans le code

```python
from cover_letter_generator import CoverLetterGenerator

# Utiliser le LLM (recommandé)
generator = CoverLetterGenerator(use_llm=True)

# Ou spécifier un provider
generator = CoverLetterGenerator(
    use_llm=True,
    llm_provider="ollama",  # ou "openai", "mistral", "claude"
    llm_model="llama3.2"
)

# Générer une lettre
letter = generator.generate_cover_letter(job, personal_info)
```

### Dans l'application Streamlit

L'application utilise automatiquement le LLM si configuré. Sinon, elle utilise les templates de secours.

## 📝 Exemple de fichier .env

```env
# Choix du provider LLM
LLM_PROVIDER=ollama
LLM_MODEL=llama3.2

# Si vous utilisez OpenAI
# LLM_PROVIDER=openai
# LLM_MODEL=gpt-4o-mini
# OPENAI_API_KEY=sk-...

# Si vous utilisez Mistral
# LLM_PROVIDER=mistral
# LLM_MODEL=mistral-medium
# MISTRAL_API_KEY=...

# Si vous utilisez Claude
# LLM_PROVIDER=claude
# LLM_MODEL=claude-3-5-sonnet-20241022
# ANTHROPIC_API_KEY=sk-ant-...
```

## 🔧 Dépannage

### Ollama ne répond pas

1. Vérifiez que Ollama est lancé : `ollama serve`
2. Vérifiez que le modèle est téléchargé : `ollama list`
3. Testez manuellement : `ollama run llama3.2`

### Erreur de clé API

- Vérifiez que votre clé API est correcte dans `.env`
- Vérifiez que le package correspondant est installé (`pip install openai`, etc.)

### Lettre générée incomplète

- Le système utilise automatiquement les templates de secours si le LLM échoue
- Vérifiez les logs pour voir l'erreur exacte

## 💡 Recommandations

1. **Pour commencer :** Utilisez **Ollama** (gratuit, local, pas de clé API)
2. **Pour la qualité maximale :** Utilisez **OpenAI GPT-4** ou **Claude Opus**
3. **Pour un bon compromis :** Utilisez **Mistral Medium** ou **Claude Sonnet**

## 📊 Comparaison rapide

| Provider | Coût | Qualité | Vitesse | Confidentialité |
|----------|------|---------|---------|-----------------|
| Ollama | Gratuit | Bonne | Moyenne | ⭐⭐⭐⭐⭐ (local) |
| OpenAI | Payant | Excellente | Rapide | ⭐⭐⭐ (API) |
| Mistral | Payant | Très bonne | Rapide | ⭐⭐⭐ (API) |
| Claude | Payant | Excellente | Rapide | ⭐⭐⭐ (API) |

## 🎯 Modèles recommandés par provider

- **Ollama :** `llama3.2`, `mistral`, `qwen2.5`
- **OpenAI :** `gpt-4o-mini` (économique), `gpt-4` (meilleur)
- **Mistral :** `mistral-small` (économique), `mistral-medium` (équilibré)
- **Claude :** `claude-3-haiku` (économique), `claude-3-5-sonnet` (équilibré)


