# 📝 Système de Candidatures Automatiques

## 🎯 Fonctionnalités

### ✨ Génération automatique de lettres de motivation
- **Adaptation intelligente** : La lettre s'adapte à chaque offre
- **Extraction des compétences** : Détecte automatiquement les compétences mentionnées dans l'offre
- **Templates personnalisables** : Différents templates selon le type de poste (Data Scientist, Analyst, Engineer, Alternance)
- **Personnalisation** : Utilise vos informations personnelles et votre expérience

### 📋 Gestion des candidatures
- **Suivi complet** : Préparées, envoyées, acceptées, refusées
- **Évite les doublons** : Détecte si vous avez déjà candidaté
- **Historique** : Toutes vos candidatures en un seul endroit
- **Statistiques** : Suivez votre taux de réponse

### 📤 Préparation automatique
- **Génération instantanée** : Crée la lettre en quelques secondes
- **Sauvegarde automatique** : Les lettres sont sauvegardées dans `cover_letters/`
- **Prêt à envoyer** : Lettres formatées et prêtes à être jointes

## 🚀 Utilisation

### 1. Configuration initiale

1. **Lancez l'application** : Double-cliquez sur `📝 Candidatures.command` sur votre bureau
2. **Allez dans l'onglet "Configuration"**
3. **Remplissez vos informations** :
   - Nom complet
   - Email
   - Introduction personnelle
   - Expérience pertinente
   - Chemin vers votre CV (PDF)

### 2. Préparer une candidature

1. **Onglet "Préparer candidatures"**
2. **Filtrez les offres** (recherche, statut)
3. **Cliquez sur "📝 Préparer candidature"** pour une offre
4. La lettre de motivation est générée automatiquement

### 3. Consulter les candidatures préparées

1. **Onglet "Candidatures préparées"**
2. **Consultez la lettre générée**
3. **Téléchargez** si besoin
4. **Marquez comme envoyée** une fois que vous avez postulé

### 4. Suivi

- **Onglet "Suivi"** : Voir toutes vos candidatures et statistiques

## 📁 Structure des fichiers

```
cover_letters/          # Dossier avec toutes les lettres générées
personal_info.json      # Vos informations personnelles
data/applications.json  # Historique des candidatures
```

## ⚙️ Personnalisation

### Modifier les templates de lettres

Les templates sont dans `cover_letter_generator.py`. Vous pouvez les modifier pour :
- Changer le style
- Ajouter des sections
- Personnaliser le ton

### Variables disponibles dans les templates

- `{job_title}` : Titre du poste
- `{company}` : Nom de l'entreprise
- `{key_skills}` : Compétences clés extraites
- `{your_name}` : Votre nom
- `{contact_info}` : Vos coordonnées
- `{personal_intro}` : Votre introduction
- `{relevant_experience}` : Votre expérience
- `{why_company}` : Pourquoi cette entreprise

## 💡 Conseils

1. **Personnalisez votre introduction** : Adaptez-la selon votre profil
2. **Vérifiez les lettres** : Lisez-les avant d'envoyer
3. **Mettez à jour votre CV** : Assurez-vous qu'il est à jour
4. **Suivez vos candidatures** : Marquez-les comme envoyées pour le suivi

## 🔄 Workflow recommandé

1. **Rechercher** : Utilisez `🔍 Recherche d'emploi.command` pour trouver des offres
2. **Visualiser** : Utilisez `📊 Visualiser les offres.command` pour voir les offres
3. **Préparer** : Utilisez `📝 Candidatures.command` pour générer les lettres
4. **Envoyer** : Postulez manuellement sur les sites (LinkedIn, etc.)
5. **Suivre** : Marquez comme envoyée dans l'application

## ⚠️ Note importante

**L'envoi automatique n'est pas implémenté** pour des raisons éthiques et légales. Vous devez :
- Postuler manuellement sur les sites d'emploi
- Vérifier chaque lettre avant envoi
- Adapter si nécessaire selon l'offre

L'outil vous **prépare** les candidatures, mais vous gardez le contrôle sur l'envoi.


