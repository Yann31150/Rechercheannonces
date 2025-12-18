# 🌐 Guide des Sites d'Emploi

L'outil supporte maintenant **5 sites d'emploi** différents !

## 📋 Sites disponibles

1. **💼 LinkedIn** - Le réseau professionnel
2. **🌴 Welcome to the Jungle (WTTJ)** - Plateforme moderne d'emploi
3. **🔍 Indeed** - Moteur de recherche d'emploi
4. **📋 APEC** - Association pour l'emploi des cadres
5. **👋 Helloworks** - Plateforme d'emploi

## 🚀 Utilisation

### Recherche sur TOUS les sites

```bash
python main_unified.py --search "Data Scientist" --location "Toulouse"
```

### Recherche sur sites spécifiques

```bash
# LinkedIn et Indeed uniquement
python main_unified.py --search "Data Analyst" --sites linkedin indeed

# Welcome to the Jungle et APEC
python main_unified.py --search "Data Engineer" --sites wttj apec
```

### Recherche LinkedIn uniquement (avec connexion)

```bash
python main.py --search "Data Scientist" --location "Toulouse, France"
```

## 🎯 Depuis le bureau

Double-cliquez sur **🔍 Recherche LinkedIn.command** et choisissez :
- **Option 1** : Recherche sur TOUS les sites
- **Option 4** : Recherche personnalisée (tous sites)

## 📊 Visualisation

L'application Streamlit affiche maintenant :
- ✅ Filtre par **source** (LinkedIn, WTTJ, Indeed, etc.)
- ✅ Graphique de répartition par source
- ✅ Toutes les offres dans une seule interface

## ⚙️ Notes importantes

### LinkedIn
- ✅ Nécessite une connexion (identifiants dans `.env`)
- ✅ Plus de fonctionnalités (networking, suivi)

### Autres sites
- ✅ Pas de connexion nécessaire
- ✅ Accès public aux offres
- ⚠️ Les sélecteurs CSS peuvent changer (sites mis à jour régulièrement)

## 🔧 Dépannage

Si un site ne fonctionne pas :
1. Le site a peut-être changé sa structure HTML
2. Vérifiez votre connexion internet
3. Certains sites peuvent bloquer les scrapers automatiques
4. Essayez avec un seul site à la fois pour identifier le problème

## 📈 Statistiques

L'application Streamlit affiche :
- Nombre d'offres par source
- Top entreprises
- Répartition géographique
- Compétences demandées (si analyse effectuée)


