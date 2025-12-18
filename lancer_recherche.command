#!/bin/bash
# Script pour lancer la recherche d'emploi LinkedIn depuis le bureau

# Aller dans le répertoire du projet
cd "$(dirname "$0")"

# Activer l'environnement virtuel
source venv/bin/activate

# Afficher un menu
echo "=================================="
echo "🔍 Recherche d'emploi Data - Multi-sites"
echo "=================================="
echo ""
echo "Sites disponibles: LinkedIn, WTTJ, Indeed, APEC, Helloworks, Free-Work, La Bonne Alternance"
echo ""
echo "1. 🔄 Recherche rapide - TOUS les sites - Haute-Garonne (recommandé)"
echo "2. 🔄 Recherche rapide 'Data Scientist' - Haute-Garonne (tous sites)"
echo "3. 🔄 Recherche rapide 'Data Analyst' - Haute-Garonne (tous sites)"
echo "4. 🔄 Recherche rapide 'Data Engineer' - Haute-Garonne (tous sites)"
echo "5. 📝 Recherche personnalisée (tous sites)"
echo "6. 💼 Recherche personnalisée (LinkedIn uniquement)"
echo "7. 🎓 Recherche sites spécialisés (Free-Work + La Bonne Alternance)"
echo "8. 📊 Analyser les compétences des offres trouvées"
echo "9. ❌ Quitter"
echo ""
read -p "Choisissez une option (1-9): " choice

# Localisation par défaut : Haute-Garonne
DEFAULT_LOCATION="Haute-Garonne, France"

case $choice in
    1)
        read -p "Mots-clés de recherche (laissez vide pour 'Data'): " keywords
        if [ -z "$keywords" ]; then
            keywords="Data"
        fi
        echo ""
        echo "🔄 Lancement de la recherche sur TOUS les sites..."
        python main_unified.py --search "$keywords" --location "$DEFAULT_LOCATION" --pages 2 --export csv
        ;;
    2)
        echo ""
        echo "🔄 Lancement de la recherche 'Data Scientist' sur TOUS les sites..."
        python main_unified.py --search "Data Scientist" --location "$DEFAULT_LOCATION" --pages 2 --export csv
        ;;
    3)
        echo ""
        echo "🔄 Lancement de la recherche 'Data Analyst' sur TOUS les sites..."
        python main_unified.py --search "Data Analyst" --location "$DEFAULT_LOCATION" --pages 2 --export csv
        ;;
    4)
        echo ""
        echo "🔄 Lancement de la recherche 'Data Engineer' sur TOUS les sites..."
        python main_unified.py --search "Data Engineer" --location "$DEFAULT_LOCATION" --pages 2 --export csv
        ;;
    5)
        read -p "Mots-clés de recherche: " keywords
        read -p "Localisation (défaut: $DEFAULT_LOCATION): " location
        if [ -z "$location" ]; then
            location="$DEFAULT_LOCATION"
        fi
        echo ""
        echo "Sites disponibles: linkedin, wttj, indeed, apec, helloworks, freework, bonnealternance"
        read -p "Sites (laissez vide pour tous): " sites_input
        echo ""
        echo "🔄 Lancement de la recherche personnalisée..."
        if [ -z "$sites_input" ]; then
            python main_unified.py --search "$keywords" --location "$location" --pages 2 --export csv
        else
            python main_unified.py --search "$keywords" --location "$location" --sites $sites_input --pages 2 --export csv
        fi
        ;;
    6)
        read -p "Mots-clés de recherche: " keywords
        read -p "Localisation (défaut: $DEFAULT_LOCATION): " location
        if [ -z "$location" ]; then
            location="$DEFAULT_LOCATION"
        fi
        echo ""
        echo "🔄 Lancement de la recherche LinkedIn..."
        python main.py --search "$keywords" --location "$location" --pages 2 --export csv
        ;;
    7)
        read -p "Mots-clés de recherche: " keywords
        echo ""
        echo "🔄 Lancement de la recherche sur Free-Work et La Bonne Alternance..."
        python main_unified.py --search "$keywords" --location "$DEFAULT_LOCATION" --sites freework bonnealternance --pages 2 --export csv
        ;;
    8)
        echo ""
        echo "📊 Analyse des compétences..."
        python main.py --analyze-skills --skills-gap
        ;;
    9)
        exit 0
        ;;
    *)
        echo "❌ Option invalide"
        exit 1
        ;;
esac

# Créer le dossier Annonces sur le bureau s'il n'existe pas
ANNONCES_DIR="$HOME/Desktop/Annonces"
mkdir -p "$ANNONCES_DIR"

# Copier les résultats dans Annonces
if [ -f "data/jobs.json" ]; then
    cp data/jobs.json "$ANNONCES_DIR/offres_linkedin.json" 2>/dev/null
    echo "✅ Fichier JSON copié dans Annonces: offres_linkedin.json"
fi

# Copier les fichiers CSV
for csv_file in data/*.csv; do
    if [ -f "$csv_file" ]; then
        filename=$(basename "$csv_file")
        cp "$csv_file" "$ANNONCES_DIR/$filename" 2>/dev/null
        echo "✅ Fichier CSV copié dans Annonces: $filename"
    fi
done

# Copier les fichiers Excel
for xlsx_file in data/*.xlsx; do
    if [ -f "$xlsx_file" ]; then
        filename=$(basename "$xlsx_file")
        cp "$xlsx_file" "$ANNONCES_DIR/$filename" 2>/dev/null
        echo "✅ Fichier Excel copié dans Annonces: $filename"
    fi
done

echo ""
echo "✅ Recherche terminée ! Les fichiers sont dans le dossier 'Annonces' sur votre bureau."
echo ""
read -p "Appuyez sur Entrée pour fermer..."

