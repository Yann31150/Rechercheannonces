#!/bin/bash
# Script pour activer l'environnement virtuel et lancer l'outil

# Activer l'environnement virtuel
source venv/bin/activate

# Lancer le script principal avec tous les arguments passés
python main.py "$@"


