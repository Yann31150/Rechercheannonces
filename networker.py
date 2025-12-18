"""
Module d'automatisation des messages de networking LinkedIn
"""
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import config
from utils import print_success, print_error, print_warning, print_info

class LinkedInNetworker:
    def __init__(self, headless=False):
        self.driver = None
        self.headless = headless
        self.messages_sent = 0
        
    def setup_driver(self):
        """Configure le driver Selenium"""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.maximize_window()
        print_success("Driver Chrome initialisé")
    
    def login(self, email=None, password=None):
        """Se connecte à LinkedIn"""
        email = email or config.LINKEDIN_EMAIL
        password = password or config.LINKEDIN_PASSWORD
        
        if not email or not password:
            print_error("Email ou mot de passe manquant. Vérifiez votre fichier .env")
            return False
        
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
                print_warning("Connexion peut-être échouée. Vérifiez vos identifiants.")
                return False
                
        except Exception as e:
            print_error(f"Erreur lors de la connexion: {str(e)}")
            return False
    
    def search_people(self, keywords, limit=10):
        """Recherche des personnes sur LinkedIn"""
        try:
            print_info(f"Recherche de personnes: {keywords}")
            
            # URL de recherche de personnes
            url = f"https://www.linkedin.com/search/results/people/?keywords={keywords.replace(' ', '%20')}"
            self.driver.get(url)
            time.sleep(3)
            
            profiles = []
            profile_elements = self.driver.find_elements(
                By.CSS_SELECTOR,
                "div.entity-result__item"
            )[:limit]
            
            for elem in profile_elements:
                try:
                    name_elem = elem.find_element(By.CSS_SELECTOR, "span.entity-result__title-text a")
                    name = name_elem.text.strip()
                    profile_url = name_elem.get_attribute('href')
                    
                    try:
                        title_elem = elem.find_element(By.CSS_SELECTOR, "div.entity-result__primary-subtitle")
                        title = title_elem.text.strip()
                    except:
                        title = "N/A"
                    
                    profiles.append({
                        'name': name,
                        'title': title,
                        'url': profile_url
                    })
                except:
                    continue
            
            print_success(f"{len(profiles)} profils trouvés")
            return profiles
            
        except Exception as e:
            print_error(f"Erreur lors de la recherche: {str(e)}")
            return []
    
    def send_connection_request(self, profile_url, message_template="data_scientist", add_note=True):
        """Envoie une demande de connexion avec un message personnalisé"""
        try:
            self.driver.get(profile_url)
            time.sleep(2)
            
            # Cliquer sur le bouton "Se connecter"
            try:
                connect_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label*='Se connecter'], button[aria-label*='Connect']"))
                )
                connect_button.click()
                time.sleep(1)
            except:
                print_warning("Bouton de connexion non trouvé ou déjà connecté")
                return False
            
            # Ajouter une note personnalisée
            if add_note:
                try:
                    add_note_button = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label*='Ajouter une note'], button[aria-label*='Add a note']"))
                    )
                    add_note_button.click()
                    time.sleep(1)
                    
                    # Récupérer le nom
                    try:
                        name_elem = self.driver.find_element(By.CSS_SELECTOR, "h1.text-heading-xlarge")
                        name = name_elem.text.strip().split()[0]  # Prénom seulement
                    except:
                        name = "Bonjour"
                    
                    # Générer le message
                    message = self._generate_message(name, message_template)
                    
                    # Entrer le message
                    message_box = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[name='message']"))
                    )
                    message_box.clear()
                    message_box.send_keys(message)
                    time.sleep(1)
                    
                except:
                    print_warning("Impossible d'ajouter une note personnalisée")
            
            # Envoyer la demande
            try:
                send_button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label*='Envoyer'], button[aria-label*='Send']"))
                )
                send_button.click()
                time.sleep(2)
                
                self.messages_sent += 1
                print_success(f"Demande de connexion envoyée ({self.messages_sent} au total)")
                
                # Délai aléatoire pour éviter la détection
                time.sleep(random.uniform(3, 6))
                
                return True
                
            except Exception as e:
                print_error(f"Erreur lors de l'envoi: {str(e)}")
                return False
                
        except Exception as e:
            print_error(f"Erreur lors de l'envoi de la demande: {str(e)}")
            return False
    
    def send_message(self, profile_url, message_template="data_scientist"):
        """Envoie un message à une personne déjà connectée"""
        try:
            self.driver.get(profile_url)
            time.sleep(2)
            
            # Cliquer sur "Message"
            try:
                message_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label*='Message'], a[href*='/messaging']"))
                )
                message_button.click()
                time.sleep(2)
            except:
                print_warning("Bouton de message non trouvé")
                return False
            
            # Récupérer le nom
            try:
                name_elem = self.driver.find_element(By.CSS_SELECTOR, "h1.text-heading-xlarge")
                name = name_elem.text.strip().split()[0]
            except:
                name = "Bonjour"
            
            # Générer et envoyer le message
            message = self._generate_message(name, message_template)
            
            try:
                message_box = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div[contenteditable='true'][aria-label*='message'], div[data-placeholder*='message']"))
                )
                message_box.click()
                message_box.send_keys(message)
                time.sleep(1)
                
                send_button = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label*='Envoyer'], button[aria-label*='Send']")
                send_button.click()
                time.sleep(2)
                
                self.messages_sent += 1
                print_success(f"Message envoyé ({self.messages_sent} au total)")
                
                time.sleep(random.uniform(3, 6))
                return True
                
            except Exception as e:
                print_error(f"Erreur lors de l'envoi du message: {str(e)}")
                return False
                
        except Exception as e:
            print_error(f"Erreur lors de l'envoi du message: {str(e)}")
            return False
    
    def _generate_message(self, name, template_type="data_scientist"):
        """Génère un message personnalisé"""
        template = config.NETWORKING_MESSAGES.get(template_type, config.NETWORKING_MESSAGES["data_scientist"])
        
        message = template.format(
            name=name,
            your_name=config.YOUR_NAME,
            skills=", ".join(config.YOUR_SKILLS)
        )
        
        return message
    
    def network_with_keywords(self, keywords, limit=10, message_template="data_scientist"):
        """Networking automatique basé sur des mots-clés"""
        profiles = self.search_people(keywords, limit)
        
        success_count = 0
        for profile in profiles:
            print_info(f"Tentative de connexion avec {profile['name']} ({profile['title']})...")
            if self.send_connection_request(profile['url'], message_template):
                success_count += 1
        
        print_success(f"Réseautage terminé: {success_count}/{len(profiles)} demandes envoyées")
        return success_count
    
    def close(self):
        """Ferme le driver"""
        if self.driver:
            self.driver.quit()
            print_info("Driver fermé")


