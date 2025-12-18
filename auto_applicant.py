"""
Module d'envoi automatique de candidatures (semi-automatique)
⚠️ Note: L'envoi 100% automatique n'est pas recommandé pour des raisons éthiques et légales
Ce module aide à préparer et faciliter l'envoi, mais nécessite une validation manuelle
"""
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from utils import print_success, print_error, print_info, print_warning
import os

class AutoApplicant:
    def __init__(self, headless=False):
        self.driver = None
        self.headless = headless
        
    def setup_driver(self):
        """Configure le driver Selenium"""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.maximize_window()
        print_success("Driver Chrome initialisé")
    
    def login_linkedin(self, email, password):
        """Se connecte à LinkedIn"""
        try:
            print_info("Connexion à LinkedIn...")
            self.driver.get("https://www.linkedin.com/login")
            time.sleep(2)
            
            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            email_field.send_keys(email)
            
            password_field = self.driver.find_element(By.ID, "password")
            password_field.send_keys(password)
            password_field.send_keys(Keys.RETURN)
            
            time.sleep(5)
            
            if "feed" in self.driver.current_url or "linkedin.com/in/" in self.driver.current_url:
                print_success("Connexion réussie à LinkedIn")
                return True
            else:
                print_warning("Connexion peut-être échouée")
                return False
                
        except Exception as e:
            print_error(f"Erreur lors de la connexion: {str(e)}")
            return False
    
    def apply_to_linkedin_job(self, job_url, cover_letter_path, cv_path):
        """
        Aide à postuler à une offre LinkedIn
        ⚠️ Nécessite une validation manuelle à la fin
        """
        try:
            print_info(f"Ouverture de l'offre: {job_url}")
            self.driver.get(job_url)
            time.sleep(3)
            
            # Chercher le bouton "Postuler"
            apply_selectors = [
                "button[aria-label*='Postuler']",
                "button[aria-label*='Apply']",
                "button.jobs-s-apply__application-link",
                "a[href*='apply']"
            ]
            
            apply_button = None
            for selector in apply_selectors:
                try:
                    apply_button = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    break
                except:
                    continue
            
            if not apply_button:
                print_warning("Bouton 'Postuler' non trouvé. L'offre peut nécessiter une candidature externe.")
                return False
            
            print_info("Clic sur 'Postuler'...")
            apply_button.click()
            time.sleep(2)
            
            # Remplir le formulaire si nécessaire
            # LinkedIn peut demander différentes informations
            
            # Télécharger le CV si demandé
            if cv_path and os.path.exists(cv_path):
                try:
                    cv_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='file']")
                    cv_input.send_keys(cv_path)
                    print_success("CV téléchargé")
                    time.sleep(2)
                except:
                    print_warning("Champ CV non trouvé ou déjà rempli")
            
            # Remplir la lettre de motivation si demandée
            if cover_letter_path and os.path.exists(cover_letter_path):
                try:
                    with open(cover_letter_path, 'r', encoding='utf-8') as f:
                        cover_letter = f.read()
                    
                    # Chercher le champ de lettre de motivation
                    letter_selectors = [
                        "textarea[name*='coverLetter']",
                        "textarea[aria-label*='lettre']",
                        "textarea[aria-label*='cover']",
                        "div[contenteditable='true'][aria-label*='cover']"
                    ]
                    
                    for selector in letter_selectors:
                        try:
                            letter_field = WebDriverWait(self.driver, 3).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                            )
                            letter_field.clear()
                            letter_field.send_keys(cover_letter)
                            print_success("Lettre de motivation remplie")
                            break
                        except:
                            continue
                except Exception as e:
                    print_warning(f"Impossible de remplir la lettre: {str(e)}")
            
            # ⚠️ IMPORTANT: Ne pas envoyer automatiquement
            print_warning("⚠️  FORMULAIRE PRÉREMPLI - VALIDATION MANUELLE REQUISE")
            print_info("Veuillez vérifier toutes les informations et cliquer sur 'Envoyer' manuellement")
            print_info("Le navigateur reste ouvert pour que vous puissiez finaliser la candidature")
            
            # Attendre que l'utilisateur finalise
            input("Appuyez sur Entrée une fois la candidature envoyée (ou annulée)...")
            
            return True
            
        except Exception as e:
            print_error(f"Erreur lors de la candidature: {str(e)}")
            return False
    
    def prepare_application_links(self, jobs, cover_letters_dir="cover_letters", cv_path=None):
        """
        Prépare une page avec tous les liens de candidature
        Utile pour postuler rapidement manuellement
        """
        html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Candidatures à envoyer</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .job-card { border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }
        .job-title { font-size: 18px; font-weight: bold; color: #0A66C2; }
        .button { background: #0A66C2; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 5px; }
        .button:hover { background: #004182; }
    </style>
</head>
<body>
    <h1>📝 Candidatures à envoyer</h1>
"""
        
        for job in jobs:
            job_url = job.get('url', '')
            job_title = job.get('title', 'N/A')
            company = job.get('company', 'N/A')
            
            # Trouver la lettre correspondante
            letter_path = None
            if os.path.exists(cover_letters_dir):
                for file in os.listdir(cover_letters_dir):
                    if job_title[:30].replace(' ', '_') in file:
                        letter_path = os.path.join(cover_letters_dir, file)
                        break
            
            html_content += f"""
    <div class="job-card">
        <div class="job-title">{job_title}</div>
        <p><strong>Entreprise:</strong> {company}</p>
        <a href="{job_url}" target="_blank" class="button">🔗 Voir l'offre et postuler</a>
"""
            if letter_path:
                html_content += f'        <a href="file://{os.path.abspath(letter_path)}" class="button">📄 Voir la lettre</a>\n'
            if cv_path:
                html_content += f'        <a href="file://{os.path.abspath(cv_path)}" class="button">📎 Voir le CV</a>\n'
            
            html_content += "    </div>\n"
        
        html_content += """
</body>
</html>
"""
        
        output_file = "candidatures_a_envoyer.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print_success(f"Page HTML créée: {output_file}")
        print_info("Ouvrez ce fichier dans votre navigateur pour accéder rapidement à toutes les candidatures")
        
        return output_file
    
    def close(self):
        """Ferme le driver"""
        if self.driver:
            self.driver.quit()


