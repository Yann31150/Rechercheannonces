# 📋 Informations Nécessaires pour les Candidatures

## ✅ Informations OBLIGATOIRES

### 1. **Nom complet**
- Votre prénom et nom
- Utilisé dans la signature des lettres
- Exemple: `Yann Coignard`

### 2. **Email**
- Votre adresse email professionnelle
- Utilisé dans les lettres de motivation
- Exemple: `coignard.yann@hotmail.fr`

## 📝 Informations RECOMMANDÉES (pour personnaliser les lettres)

### 3. **Introduction personnelle**
- Une phrase ou deux sur votre profil
- Sera utilisée dans chaque lettre
- Exemple: `"Passionné par la data et l'analyse, je suis convaincu que mon profil correspond à vos attentes. Mon parcours m'a permis de développer des compétences solides en Python, SQL et Machine Learning."`

### 4. **Expérience pertinente**
- Description de votre expérience en data
- Mentionnez vos projets, réalisations
- Exemple: `"J'ai travaillé sur des projets variés en data science, notamment en machine learning et analyse de données. J'ai une bonne maîtrise des outils Python (Pandas, Scikit-learn) et de l'analyse de données."`

### 5. **Chemin vers votre CV (PDF)**
- Chemin complet vers votre fichier CV
- Sera joint aux candidatures (si fonctionnalité d'envoi ajoutée)
- Exemple: `/Users/yanndanneels-coignard/Desktop/CV_Yann_Coignard.pdf`

## 🔧 Informations OPTIONNELLES

### 6. **Téléphone**
- Numéro de téléphone
- Pour les lettres si vous voulez l'inclure

### 7. **Adresse**
- Adresse postale
- Rarement nécessaire pour les candidatures en ligne

### 8. **LinkedIn**
- URL de votre profil LinkedIn
- Peut être mentionné dans les lettres

### 9. **GitHub**
- URL de votre profil GitHub
- Utile pour les postes tech/data

## 🎯 Comment remplir ces informations

### Méthode 1 : Via l'application Streamlit (recommandé)
1. Double-cliquez sur `📝 Candidatures.command`
2. Allez dans l'onglet "⚙️ Configuration"
3. Remplissez le formulaire
4. Cliquez sur "💾 Sauvegarder"

### Méthode 2 : Modifier directement le fichier
Éditez le fichier `personal_info.json` :
```json
{
  "name": "Votre Nom",
  "email": "votre.email@example.com",
  "intro": "Votre introduction...",
  "experience": "Votre expérience...",
  "cv_path": "/chemin/vers/votre/CV.pdf"
}
```

## 💡 Conseils pour rédiger

### Introduction personnelle
- **Court** : 1-2 phrases maximum
- **Impactant** : Montrez votre passion
- **Spécifique** : Mentionnez vos compétences clés
- **Exemple bon** : "Passionné par la data et l'analyse, je suis convaincu que mon profil correspond à vos attentes."
- **Exemple moins bon** : "Je cherche un emploi." (trop générique)

### Expérience pertinente
- **Concret** : Mentionnez des projets, outils, résultats
- **Pertinent** : Focus sur la data
- **Exemple bon** : "J'ai travaillé sur des projets de machine learning avec Python, notamment en utilisant Pandas et Scikit-learn pour l'analyse prédictive."
- **Exemple moins bon** : "J'ai de l'expérience." (trop vague)

## ✅ État actuel de vos informations

Vos informations sont déjà pré-remplies dans `personal_info.json` :
- ✅ Nom : Yann Coignard
- ✅ Email : coignard.yann@hotmail.fr
- ✅ Introduction : Déjà remplie
- ✅ Expérience : Déjà remplie
- ⚠️ CV : À ajouter (chemin vers votre fichier PDF)

## 🚀 Prochaines étapes

1. **Ajoutez le chemin de votre CV** dans la configuration
2. **Personnalisez** l'introduction et l'expérience si besoin
3. **Testez** en générant une lettre pour une offre
4. **Ajustez** selon vos préférences


