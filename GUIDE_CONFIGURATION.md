# 📋 Guide de Configuration

## Informations nécessaires

### ✅ OBLIGATOIRE pour toutes les fonctionnalités

1. **Email LinkedIn**
   - L'adresse email avec laquelle vous vous connectez à LinkedIn
   - Exemple: `jean.dupont@email.com`

2. **Mot de passe LinkedIn**
   - Votre mot de passe LinkedIn
   - ⚠️ **Sécurité**: Ce fichier `.env` ne doit JAMAIS être partagé ou commité sur Git

### 📝 RECOMMANDÉ pour le networking

3. **Votre nom**
   - Votre prénom et nom (ou juste prénom)
   - Utilisé dans les messages de networking
   - Exemple: `Jean Dupont` ou `Jean`

4. **Vos compétences principales**
   - Liste de vos compétences séparées par des virgules
   - Utilisées dans les messages et l'analyse de gap
   - Exemple: `Python, SQL, Machine Learning, Tableau, AWS`

## 🔧 Configuration étape par étape

### Étape 1: Créer le fichier .env

Créez un fichier nommé `.env` à la racine du projet avec ce contenu :

```env
# Identifiants LinkedIn (OBLIGATOIRE)
LINKEDIN_EMAIL=votre_email@example.com
LINKEDIN_PASSWORD=votre_mot_de_passe

# Informations personnelles (RECOMMANDÉ)
YOUR_NAME=Votre Nom
YOUR_SKILLS=Python, SQL, Machine Learning, Data Analysis
```

### Étape 2: Remplir vos informations

Remplacez les valeurs d'exemple par vos vraies informations :

```env
LINKEDIN_EMAIL=jean.dupont@gmail.com
LINKEDIN_PASSWORD=MonMotDePasse123!
YOUR_NAME=Jean Dupont
YOUR_SKILLS=Python, SQL, Machine Learning, Pandas, Scikit-learn, Tableau
```

### Étape 3: Vérifier la sécurité

- ✅ Le fichier `.env` est déjà dans `.gitignore` (ne sera pas commité)
- ✅ Ne partagez JAMAIS ce fichier
- ✅ Utilisez un mot de passe fort pour LinkedIn

## 🎯 Utilisation minimale

**Pour juste rechercher des offres** (sans networking) :
- Seulement `LINKEDIN_EMAIL` et `LINKEDIN_PASSWORD` sont nécessaires

**Pour le networking automatique** :
- Toutes les informations sont recommandées pour des messages personnalisés

## ❓ Questions fréquentes

**Q: Est-ce que mes identifiants sont sécurisés ?**
R: Oui, ils sont stockés localement dans `.env` qui n'est pas versionné. Mais utilisez toujours un mot de passe fort.

**Q: Puis-je utiliser l'outil sans identifiants ?**
R: Non, LinkedIn nécessite une connexion pour accéder aux offres d'emploi.

**Q: Que faire si j'ai l'authentification à deux facteurs (2FA) ?**
R: L'outil fonctionne avec 2FA si vous êtes déjà connecté dans Chrome. Sinon, vous devrez peut-être désactiver temporairement le 2FA ou utiliser un token d'application.

## 🚀 Prochaines étapes

Une fois le fichier `.env` configuré :

1. Installez les dépendances : `pip install -r requirements.txt`
2. Testez la connexion : `python main.py --search "Data Scientist" --location "Paris"`


