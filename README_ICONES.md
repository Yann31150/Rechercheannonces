# 🖥️ Guide des Icônes sur le Bureau

## 📋 Icônes disponibles

### 🔍 Recherche d'emploi.command
**Double-cliquez** pour lancer une recherche d'emploi sur plusieurs sites.

**Fonctionnalités :**
- Recherche sur tous les sites (LinkedIn, WTTJ, Indeed, APEC, Helloworks)
- Recherche personnalisée
- Analyse des compétences

**Résultats :** Tous les fichiers sont sauvegardés dans le dossier **Annonces** sur votre bureau.

### 📊 Visualiser les offres.command
**Double-cliquez** pour ouvrir l'application Streamlit et visualiser toutes les offres trouvées.

**Fonctionnalités :**
- Liste interactive des offres
- Filtres par source, entreprise, localisation
- Statistiques et graphiques
- Téléchargement des résultats

## 📁 Dossier Annonces

Tous les fichiers de résultats sont automatiquement sauvegardés dans :
```
~/Desktop/Annonces/
```

**Types de fichiers :**
- `offres_linkedin.json` - Toutes les offres au format JSON
- `jobs_*.csv` - Fichiers CSV par recherche
- `jobs_*.xlsx` - Fichiers Excel par recherche

## 🚀 Utilisation rapide

1. **Lancer une recherche :**
   - Double-cliquez sur `🔍 Recherche d'emploi.command`
   - Choisissez une option dans le menu
   - Les fichiers apparaîtront dans `Annonces/`

2. **Visualiser les résultats :**
   - Double-cliquez sur `📊 Visualiser les offres.command`
   - L'application s'ouvre dans votre navigateur
   - Explorez les offres avec les filtres

## ⚙️ Première utilisation

Si macOS demande une autorisation :
1. Allez dans **Préférences Système** > **Sécurité et confidentialité**
2. Autorisez l'exécution du script

## 🔄 Recréer les icônes

Si les icônes disparaissent :
```bash
cd /Users/yanndanneels-coignard/Projet/Test1
./creer_raccourci.sh
```


