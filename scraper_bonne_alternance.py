"""
Module de scraping pour La Bonne Alternance (Pôle Emploi)
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
from utils import print_success, print_error, print_info, print_warning, get_timestamp

class BonneAlternanceScraper:
    def __init__(self, headless=False):
        self.driver = None
        self.headless = headless
        self.jobs = []
        
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
        print_success("Driver Chrome initialisé pour La Bonne Alternance")
        
    def search_jobs(self, keywords, location="Haute-Garonne", max_pages=3):
        """Recherche des offres d'emploi"""
        try:
            print_info(f"Recherche La Bonne Alternance: {keywords} - {location}")
            
            # URL de recherche La Bonne Alternance
            base_url = "https://labonnealternance.apprentissage.beta.gouv.fr"
            # Format: /recherche-apprentissage?romes=M1805&location=31000
            
            # Essayer avec le code postal de Toulouse (31000) ou le nom
            location_code = "31000" if "toulouse" in location.lower() or "haute-garonne" in location.lower() else location
            
            url = f"{base_url}/recherche-apprentissage?romes=M1805&location={location_code}"
            
            self.driver.get(url)
            time.sleep(4)
            
            jobs = []
            for page in range(max_pages):
                print_info(f"Page {page + 1}/{max_pages}...")
                
                time.sleep(2)
                
                # Trouver les offres
                job_cards = self.driver.find_elements(
                    By.CSS_SELECTOR,
                    "article[class*='offer'], div[class*='offer'], li[class*='offer']"
                )
                
                if not job_cards:
                    job_cards = self.driver.find_elements(By.CSS_SELECTOR, "div[class*='result'], div[class*='job']")
                
                print_info(f"Trouvé {len(job_cards)} offres sur la page {page + 1}")
                
                for card in job_cards:
                    try:
                        job_data = self._extract_job_details(card)
                        if job_data:
                            jobs.append(job_data)
                    except Exception as e:
                        continue
                
                # Passer à la page suivante
                if page < max_pages - 1:
                    try:
                        next_button = self.driver.find_element(
                            By.CSS_SELECTOR,
                            "a[aria-label='Suivant'], a[class*='next']"
                        )
                        next_button.click()
                        time.sleep(3)
                    except:
                        break
            
            self.jobs.extend(jobs)
            print_success(f"{len(jobs)} offres trouvées sur La Bonne Alternance")
            return jobs
            
        except Exception as e:
            print_error(f"Erreur lors de la recherche: {str(e)}")
            return []
    
    def _extract_job_details(self, card):
        """Extrait les détails d'une offre"""
        try:
            job_data = {'source': 'La Bonne Alternance'}
            
            # Titre
            title_selectors = ["h2", "h3", "a[class*='title']", "span[class*='title']"]
            for selector in title_selectors:
                try:
                    title_elem = card.find_element(By.CSS_SELECTOR, selector)
                    job_data['title'] = title_elem.text.strip()
                    break
                except:
                    continue
            
            if 'title' not in job_data:
                return None
            
            # URL
            try:
                link_elem = card.find_element(By.CSS_SELECTOR, "a")
                job_data['url'] = link_elem.get_attribute('href')
            except:
                job_data['url'] = ""
            
            # Entreprise - sélecteurs améliorés pour La Bonne Alternance avec fallback
            company_selectors = [
                "span[class*='company']",
                "div[class*='company']",
                "a[class*='company']",
                "span[data-company]",
                "div[data-company]",
                "span.entreprise",
                "div.entreprise",
                "p[class*='company']",
                "p[data-testid='company-name']"
            ]
            company_found = False
            for selector in company_selectors:
                try:
                    company_elems = card.find_elements(By.CSS_SELECTOR, selector)
                    for company_elem in company_elems:
                        company_text = company_elem.text.strip()
                        if company_text and company_text != "" and len(company_text) > 1 and len(company_text) < 100:
                            if company_text != job_data.get('title', ''):
                                job_data['company'] = company_text
                                company_found = True
                                break
                    if company_found:
                        break
                except:
                    continue
            
            # Fallback : chercher dans tous les éléments texte
            if not company_found:
                try:
                    all_elements = card.find_elements(By.CSS_SELECTOR, "span, div, p, a")
                    for elem in all_elements:
                        text = elem.text.strip()
                        if text and 2 < len(text) < 50:
                            if not any(word in text.lower() for word in ['il y a', 'ago', 'jour', 'day', '€', 'k€', 'france', 'toulouse', 'paris']):
                                if text != job_data.get('title', '') and text != job_data.get('location', ''):
                                    job_data['company'] = text
                                    company_found = True
                                    break
                except:
                    pass
            
            if not company_found:
                job_data['company'] = "N/A"
            
            # Localisation - sélecteurs améliorés pour La Bonne Alternance
            location_selectors = [
                "span[class*='location']",
                "div[class*='location']",
                "span[data-location]",
                "div[data-location]",
                "span.localisation",
                "div.localisation",
                "span[aria-label*='localisation']"
            ]
            location_found = False
            for selector in location_selectors:
                try:
                    location_elems = card.find_elements(By.CSS_SELECTOR, selector)
                    for loc_elem in location_elems:
                        loc_text = loc_elem.text.strip()
                        # Filtrer les éléments vides et les dates
                        if loc_text and len(loc_text) > 1 and "il y a" not in loc_text.lower() and "ago" not in loc_text.lower():
                            job_data['location'] = loc_text
                            location_found = True
                            break
                    if location_found:
                        break
                except:
                    continue
            if not location_found:
                job_data['location'] = "N/A"
            
            job_data['date'] = "N/A"
            job_data['description'] = ""
            job_data['scraped_at'] = get_timestamp()
            
            return job_data
            
        except Exception as e:
            return None
    
    def close(self):
        """Ferme le driver"""
        if self.driver:
            self.driver.quit()


