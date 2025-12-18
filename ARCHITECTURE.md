# 🏗️ Architecture du Système

## 📋 Vue d'ensemble

Le système est composé de **2 parties principales** :

### 1. 🔍 SCRAPING (Recherche d'annonces)
**Fichier :** `main_unified.py` + scrapers individuels  
**Lancement :** `🔍 Recherche d'emploi.command` sur le bureau  
**Fonction :** Scrape les offres d'emploi sur tous les sites

### 2. 📊 APPLICATION STREAMLIT (Visualisation + Candidatures + Suivi)
**Fichier :** `app_unified.py`  
**Lancement :** `🎯 Application Complète.command` sur le bureau  
**Fonction :** Visualiser, préparer candidatures, suivre

---

## 🔍 PARTIE 1 : SCRAPING DES ANNONCES

### Scripts disponibles
- **`main_unified.py`** : Recherche sur TOUS les sites (LinkedIn, WTTJ, Indeed, APEC, etc.)
- **`main.py`** : Recherche LinkedIn uniquement
- **`scraper.py`** : Scraper LinkedIn
- **`scraper_wttj.py`** : Scraper Welcome to the Jungle
- **`scraper_indeed.py`** : Scraper Indeed
- **`scraper_apec.py`** : Scraper APEC
- **`scraper_helloworks.py`** : Scraper Helloworks
- **`scraper_freework.py`** : Scraper Free-Work
- **`scraper_bonne_alternance.py`** : Scraper La Bonne Alternance

### Comment lancer
1. **Depuis le bureau** : Double-clic sur `🔍 Recherche d'emploi.command`
2. **En ligne de commande** :
   ```bash
   python main_unified.py --search "Data Scientist" --location "Haute-Garonne, France"
   ```

### Résultat
- Sauvegarde dans `data/jobs.json`
- Copie automatique dans `~/Desktop/Annonces/`
- Export CSV/Excel optionnel

---

## 📊 PARTIE 2 : APPLICATION STREAMLIT

### Fichier principal
- **`app_unified.py`** : Application complète avec tous les onglets

### Fonctionnalités

#### Onglet 1 : 📋 Offres d'emploi
- Visualiser toutes les offres scrapées
- Filtres : titre, entreprise, source, localisation, statut candidature
- Tri par date (plus récent en premier)
- Bouton "Préparer candidature" directement depuis la liste

#### Onglet 2 : 📝 Préparer candidatures
- Sélection d'offres pour préparer des candidatures
- Génération automatique de lettres avec LLM (Ollama)
- Utilise le contenu du CV pour personnaliser

#### Onglet 3 : 📤 Candidatures préparées
- Liste des candidatures prêtes à envoyer
- Visualisation des lettres générées
- Marquer comme envoyée

#### Onglet 4 : 📊 Suivi complet
- Toutes vos candidatures avec statuts
- Filtres par statut et entreprise
- Notes personnalisées pour chaque candidature
- Mise à jour du statut (préparée → envoyée → acceptée/refusée)
- Téléchargement des lettres

#### Onglet 5 : 📈 Statistiques
- Graphiques des offres par source
- Top entreprises
- Statistiques de candidatures

#### Onglet 6 : ⚙️ Configuration
- Modifier informations personnelles
- Chemin vers CV
- Vérification Ollama

### Comment lancer
1. **Depuis le bureau** : Double-clic sur `🎯 Application Complète.command`
2. **En ligne de commande** :
   ```bash
   streamlit run app_unified.py
   ```

---

## 🔄 Flux de travail recommandé

```
1. SCRAPING
   ↓
   [Double-clic sur 🔍 Recherche d'emploi.command]
   ↓
   [Scraping sur tous les sites]
   ↓
   [Sauvegarde dans data/jobs.json]
   ↓
   ✅ Offres disponibles

2. VISUALISATION & CANDIDATURES
   ↓
   [Double-clic sur 🎯 Application Complète.command]
   ↓
   [Onglet "Offres d'emploi" : Voir les offres]
   ↓
   [Onglet "Préparer candidatures" : Générer lettres]
   ↓
   [Onglet "Suivi complet" : Suivre les candidatures]
   ↓
   ✅ Candidatures préparées et suivies
```

---

## 📁 Fichiers clés

### Données
- **`data/jobs.json`** : Toutes les offres scrapées (utilisé par les deux parties)
- **`data/applications.json`** : Toutes les candidatures (utilisé par l'app Streamlit)
- **`cover_letters/`** : Lettres de motivation générées
- **`personal_info.json`** : Vos informations personnelles

### Scripts
- **`main_unified.py`** : Script de scraping principal
- **`app_unified.py`** : Application Streamlit complète
- **`application_manager.py`** : Gestion des candidatures
- **`cover_letter_generator.py`** : Génération de lettres
- **`llm_generator.py`** : Interface avec les LLM (Ollama, etc.)

---

## ✅ Résumé

**2 parties distinctes :**

1. **🔍 SCRAPING** → `🔍 Recherche d'emploi.command`
   - Scrape les annonces
   - Sauvegarde dans `data/jobs.json`

2. **📊 APPLICATION** → `🎯 Application Complète.command`
   - Visualise les annonces
   - Prépare les candidatures
   - Assure le suivi

**Tout est connecté via `data/jobs.json` !**

