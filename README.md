# 🔍 Outil de Recherche d'Emploi Data sur LinkedIn

Un outil Python complet pour automatiser votre recherche d'emploi dans le domaine de la data sur LinkedIn.

## ✨ Fonctionnalités

- **Scraping des offres d'emploi** : Recherche et extraction automatique des offres selon vos critères
- **Analyse des compétences** : Identification des compétences les plus demandées
- **Messages de networking** : Génération et envoi automatique de messages personnalisés
- **Suivi des offres** : Détection des nouvelles offres correspondant à vos critères
- **Rapports Excel** : Export des résultats pour analyse approfondie

## 🚀 Installation

1. Clonez ce repository ou téléchargez les fichiers
2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

3. Installez ChromeDriver (ou utilisez webdriver-manager qui le fait automatiquement)

4. Créez un fichier `.env` à la racine du projet :
```
LINKEDIN_EMAIL=votre_email@example.com
LINKEDIN_PASSWORD=votre_mot_de_passe
```

## ⚠️ Avertissements Importants

- **Respect des conditions d'utilisation LinkedIn** : Cet outil est à utiliser de manière responsable et éthique
- **Limites de taux** : LinkedIn peut limiter ou bloquer les comptes avec une activité automatisée excessive
- **Utilisation à vos risques** : Utilisez cet outil avec modération et respectez les limites raisonnables

## 📖 Utilisation

### Mode basique
```bash
python main.py
```

### Recherche d'offres spécifiques
```bash
python main.py --search "Data Scientist" --location "Paris" --experience "2-5"
```

### Analyse des compétences
```bash
python main.py --analyze-skills
```

### Envoi de messages de networking
```bash
python main.py --network --limit 10
```

## 📁 Structure du projet

```
.
├── main.py                 # Script principal
├── config.py              # Configuration
├── scraper.py             # Module de scraping LinkedIn
├── analyzer.py            # Module d'analyse des compétences
├── networker.py           # Module de networking
├── tracker.py             # Module de suivi des offres
├── utils.py               # Fonctions utilitaires
├── requirements.txt       # Dépendances Python
├── .env                   # Variables d'environnement (à créer)
└── README.md             # Ce fichier
```

## 🔧 Configuration

Modifiez `config.py` pour personnaliser :
- Mots-clés de recherche
- Localisations préférées
- Compétences à mettre en avant
- Templates de messages

## 📊 Format des données

Les résultats sont exportés en :
- **CSV** : Pour analyse dans Excel/Python
- **JSON** : Pour traitement programmatique
- **Console** : Affichage formaté en temps réel

## 🤝 Contribution

N'hésitez pas à améliorer cet outil et à partager vos suggestions !

## 📝 Licence

Ce projet est fourni à des fins éducatives. Utilisez-le de manière responsable.


