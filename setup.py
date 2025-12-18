"""
Script interactif pour configurer l'outil
"""
import os
from getpass import getpass

def setup_config():
    """Configure interactivement le fichier .env"""
    print("=" * 60)
    print("🔧 Configuration de l'outil LinkedIn")
    print("=" * 60)
    print()
    
    # Vérifier si .env existe déjà
    if os.path.exists('.env'):
        response = input("⚠️  Le fichier .env existe déjà. Voulez-vous le remplacer ? (o/n): ")
        if response.lower() != 'o':
            print("Configuration annulée.")
            return
    
    print("Veuillez remplir les informations suivantes :")
    print()
    
    # Identifiants LinkedIn (obligatoires)
    print("📧 IDENTIFIANTS LINKEDIN (obligatoires)")
    email = input("Email LinkedIn: ").strip()
    password = getpass("Mot de passe LinkedIn: ").strip()
    
    if not email or not password:
        print("❌ Email et mot de passe sont obligatoires !")
        return
    
    print()
    print("👤 INFORMATIONS PERSONNELLES (optionnel mais recommandé)")
    name = input("Votre nom (pour les messages): ").strip() or "Votre Nom"
    skills = input("Vos compétences (séparées par des virgules): ").strip() or "Python, SQL, Machine Learning"
    
    # Créer le contenu du fichier .env
    env_content = f"""# Identifiants LinkedIn
LINKEDIN_EMAIL={email}
LINKEDIN_PASSWORD={password}

# Informations personnelles
YOUR_NAME={name}
YOUR_SKILLS={skills}
"""
    
    # Écrire le fichier
    try:
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        print()
        print("✅ Configuration sauvegardée dans .env")
        print()
        print("⚠️  IMPORTANT:")
        print("   - Ne partagez JAMAIS le fichier .env")
        print("   - Il est déjà dans .gitignore (ne sera pas commité)")
        print()
        print("🚀 Vous pouvez maintenant utiliser l'outil !")
        print("   Exemple: python main.py --search 'Data Scientist' --location 'Paris'")
        
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde: {str(e)}")

if __name__ == "__main__":
    setup_config()


