# ✅ Flux Complet : Recherche → Candidatures

## 🔄 Schéma du flux

```
1. RECHERCHE D'EMPLOI
   ↓
   [Double-clic sur 🔍 Recherche d'emploi.command]
   ↓
   [Lancement de main_unified.py]
   ↓
   [Scraping sur LinkedIn, WTTJ, Indeed, APEC, etc.]
   ↓
   [Sauvegarde dans data/jobs.json]
   ↓
   ✅ Offres trouvées et sauvegardées

2. VISUALISATION DES OFFRES
   ↓
   [Double-clic sur 📊 Visualiser les offres.command]
   ↓
   [Lancement de app.py (Streamlit)]
   ↓
   [Chargement depuis data/jobs.json]
   ↓
   ✅ Affichage des offres avec filtres

3. PRÉPARATION DES CANDIDATURES
   ↓
   [Double-clic sur 📝 Candidatures.command]
   ↓
   [Lancement de applications_app.py (Streamlit)]
   ↓
   [Chargement depuis data/jobs.json]
   ↓
   [Sélection d'une offre]
   ↓
   [Clic sur "📝 Préparer candidature"]
   ↓
   [Génération de la lettre avec LLM/Templates]
   ↓
   [Sauvegarde dans data/applications.json]
   ↓
   ✅ Candidature préparée et suivie

4. SUIVI DES CANDIDATURES
   ↓
   [Onglet "📊 Suivi" dans applications_app.py]
   ↓
   [Affichage de toutes les candidatures]
   ↓
   [Mise à jour du statut : préparée → envoyée → acceptée/refusée]
   ↓
   ✅ Suivi complet avec notes
```

## 📁 Fichiers clés

### `data/jobs.json`
- **Contenu** : Toutes les offres d'emploi trouvées
- **Créé par** : `main_unified.py` ou `main.py`
- **Utilisé par** : 
  - `app.py` (visualisation)
  - `applications_app.py` (candidatures)
- **Format** : Liste JSON d'offres avec `title`, `company`, `location`, `url`, `source`, etc.

### `data/applications.json`
- **Contenu** : Toutes les candidatures préparées/envoyées
- **Créé par** : `applications_app.py` (ApplicationManager)
- **Utilisé par** : `applications_app.py` (suivi)
- **Format** : Liste JSON de candidatures avec `job_title`, `company`, `status`, `cover_letter_path`, etc.

### `cover_letters/`
- **Contenu** : Toutes les lettres de motivation générées
- **Créé par** : `CoverLetterGenerator`
- **Format** : Fichiers texte (.txt) avec le nom de l'offre

## ✅ Vérifications

### 1. Recherche fonctionne
- ✅ `main_unified.py` sauvegarde dans `config.JOBS_FILE` (ligne 120)
- ✅ Le fichier est `data/jobs.json`
- ✅ Les offres contiennent : `title`, `company`, `location`, `url`, `source`

### 2. Application de candidatures charge les offres
- ✅ `applications_app.py` charge depuis `config.JOBS_FILE` (ligne 59)
- ✅ Affiche les offres avec filtres
- ✅ Détecte les offres déjà candidatées

### 3. Génération de lettres
- ✅ Utilise Ollama si disponible (détection automatique)
- ✅ Fallback vers templates si Ollama non disponible
- ✅ Lettres sauvegardées dans `cover_letters/`

### 4. Suivi des candidatures
- ✅ Toutes les candidatures dans `data/applications.json`
- ✅ Statuts : `prepared`, `sent`, `accepted`, `rejected`
- ✅ Notes et dates de suivi

## 🎯 Workflow recommandé

1. **Lancer une recherche** : Double-clic sur 🔍 Recherche d'emploi.command
2. **Visualiser les offres** : Double-clic sur 📊 Visualiser les offres.command
3. **Préparer des candidatures** : Double-clic sur 📝 Candidatures.command
4. **Suivre les candidatures** : Onglet "📊 Suivi" dans l'app candidatures

## 🔍 Points de contrôle

- ✅ Les offres sont bien sauvegardées dans `data/jobs.json`
- ✅ L'application de candidatures charge bien depuis `data/jobs.json`
- ✅ Les candidatures sont bien suivies dans `data/applications.json`
- ✅ Les lettres sont bien générées et sauvegardées
- ✅ Le suivi permet de voir toutes les candidatures avec statuts

## ⚠️ Si ça ne fonctionne pas

1. **Vérifier que la recherche a bien créé `data/jobs.json`**
   ```bash
   ls -la data/jobs.json
   ```

2. **Vérifier le contenu du fichier**
   ```bash
   python3 -c "import json; print(len(json.load(open('data/jobs.json'))))"
   ```

3. **Vérifier que l'app charge bien les offres**
   - Lancer l'app candidatures
   - Vérifier qu'il y a des offres affichées
   - Si vide, relancer une recherche

