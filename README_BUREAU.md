# 🖥️ Utilisation depuis le Bureau

## 🚀 Lancer la recherche

1. **Double-cliquez** sur l'icône `🔍 Recherche LinkedIn.command` sur votre bureau
2. Un terminal s'ouvrira avec un menu
3. Choisissez une option (1-6)
4. La recherche se lancera automatiquement

## 📋 Options du menu

- **Option 1** : Recherche "Data Scientist" à Toulouse
- **Option 2** : Recherche "Data Analyst" à Toulouse  
- **Option 3** : Recherche "Data Engineer" à Toulouse
- **Option 4** : Recherche personnalisée (vous entrez les mots-clés)
- **Option 5** : Analyser les compétences des offres déjà trouvées
- **Option 6** : Quitter

## 📁 Fichiers de résultats

Les résultats sont automatiquement copiés sur votre bureau :
- `jobs_Data_Scientist.csv` (ou autre selon la recherche)
- `offres_linkedin.json`

Les fichiers sont aussi sauvegardés dans le dossier `data/` du projet.

## ⚠️ Première utilisation

Si macOS vous demande une autorisation :
1. Allez dans **Préférences Système** > **Sécurité et confidentialité**
2. Autorisez l'exécution du script

## 🎨 Personnaliser l'icône (optionnel)

Pour changer l'icône du fichier :
1. Trouvez une image (PNG, JPG, etc.)
2. Ouvrez l'image dans **Aperçu**
3. Sélectionnez tout (Cmd+A) et copiez (Cmd+C)
4. Cliquez sur le fichier `.command` sur le bureau
5. Cmd+I pour ouvrir les informations
6. Cliquez sur la petite icône en haut à gauche
7. Collez (Cmd+V)

## 🔄 Recréer le raccourci

Si le raccourci disparaît, exécutez :
```bash
cd /Users/yanndanneels-coignard/Projet/Test1
./creer_raccourci.sh
```


