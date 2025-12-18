# 🎯 Sites Spécialisés pour la Data

## Pourquoi ces sites sont importants ?

### 💻 Sites Tech/Data Spécialisés

#### **Free-Work**
- ✅ **Énorme section CDI/Alternance** très active sur la Data
- ✅ À l'origine pour les freelances, mais excellent pour les CDI
- ✅ Communauté tech active
- ✅ Offres souvent plus techniques et spécialisées

#### **WeLoveDevs**
- ✅ Approche bienveillante
- ✅ Les entreprises viennent à vous
- ✅ Focus sur le bien-être au travail
- ✅ Bon pour les profils data/tech

#### **LesJeudis**
- ✅ Historique dans l'IT et le web
- ✅ Bonne couverture des postes tech
- ✅ Interface simple et efficace

#### **DataScientest (Job Board)**
- ✅ Spécialisé Data Science
- ✅ Partenaires de formations certifiantes
- ✅ Offres souvent liées aux certifications
- ✅ Réseau d'entreprises partenaires

### 🎓 Sites pour l'Alternance

#### **La Bonne Alternance (Pôle Emploi)**
- ✅ **LE HACK** : Montre les entreprises qui ont recruté récemment
- ✅ Même sans offre publiée = **candidature spontanée** possible
- ✅ Algorithme intelligent
- ✅ Financé par les OPCO et l'État
- ✅ **Mine d'or pour trouver des entreprises qui recrutent**

#### **1jeune1solution**
- ✅ Agrégateur gouvernemental massif
- ✅ Toutes les offres d'alternance financées
- ✅ Interface officielle
- ✅ Très complet

#### **Walt Community**
- ✅ Site dédié à l'alternance
- ✅ Communauté active
- ✅ Bon pour les échanges et conseils

## 🚀 Utilisation dans l'outil

### Recherche sur tous les sites
```bash
python main_unified.py --search "Data Scientist" --location "Haute-Garonne"
```

### Recherche sur sites spécialisés
```bash
# Free-Work uniquement
python main_unified.py --search "Data" --sites freework

# Sites alternance
python main_unified.py --search "Data" --sites bonnealternance
```

## 💡 Stratégie de recherche

1. **Recherche large** : Tous les sites pour maximiser les résultats
2. **Recherche ciblée alternance** : La Bonne Alternance + 1jeune1solution
3. **Recherche tech/data** : Free-Work + WeLoveDevs + DataScientest
4. **Candidature spontanée** : Utiliser La Bonne Alternance pour trouver les entreprises qui recrutent

## 📊 Avantages

- **Plus de couverture** : 7+ sites au lieu de 5
- **Spécialisation** : Sites dédiés data/tech
- **Alternance** : Sites spécifiques pour l'apprentissage
- **Candidature spontanée** : La Bonne Alternance révèle les entreprises qui recrutent

## ⚠️ Note

Certains sites peuvent nécessiter des ajustements de sélecteurs CSS selon leurs mises à jour. Les scrapers sont conçus pour être robustes et essayer plusieurs approches.


