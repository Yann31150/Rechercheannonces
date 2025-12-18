"""
Module de scraping pour Welcome to the Jungle
"""
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from utils import print_success, print_error, print_info, get_timestamp

class WelcomeToTheJungleScraper:
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
        print_success("Driver Chrome initialisé pour Welcome to the Jungle")
        
    def search_jobs(self, keywords, location="Toulouse", max_pages=3):
        """Recherche des offres d'emploi"""
        try:
            print_info(f"Recherche Welcome to the Jungle: {keywords} - {location}")
            
            # URL de recherche WTTJ
            base_url = "https://www.welcometothejungle.com/fr/jobs"
            params = {
                "query": keywords,
                "aroundQuery": location,
                "page": 1
            }
            
            query_string = "&".join([f"{k}={v}" for k, v in params.items() if v])
            url = f"{base_url}?{query_string}"
            
            self.driver.get(url)
            time.sleep(3)
            
            jobs = []
            for page in range(1, max_pages + 1):
                print_info(f"Page {page}/{max_pages}...")
                
                # Attendre le chargement
                time.sleep(2)
                
                # Trouver les offres
                job_cards = self.driver.find_elements(
                    By.CSS_SELECTOR,
                    "div[data-testid='job-card'], article[class*='job-card'], div[class*='job-card']"
                )
                
                if not job_cards:
                    # Essayer d'autres sélecteurs
                    job_cards = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='/jobs/']")
                
                print_info(f"Trouvé {len(job_cards)} offres sur la page {page}")
                
                for card in job_cards:
                    try:
                        job_data = self._extract_job_details(card)
                        if job_data:
                            jobs.append(job_data)
                    except Exception as e:
                        continue
                
                # Passer à la page suivante
                if page < max_pages:
                    try:
                        next_button = self.driver.find_element(
                            By.CSS_SELECTOR,
                            "a[aria-label='Page suivante'], button[aria-label='Next'], a[href*='page=']"
                        )
                        next_button.click()
                        time.sleep(2)
                    except:
                        break
            
            self.jobs.extend(jobs)
            print_success(f"{len(jobs)} offres trouvées sur Welcome to the Jungle")
            return jobs
            
        except Exception as e:
            print_error(f"Erreur lors de la recherche: {str(e)}")
            return []
    
    def _extract_job_details(self, card):
        """Extrait les détails d'une offre"""
        try:
            job_data = {'source': 'Welcome to the Jungle'}
            
            # Titre
            title_selectors = [
                "h3", "h2", "a[class*='title']", "span[class*='title']"
            ]
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
                if not job_data['url'].startswith('http'):
                    job_data['url'] = f"https://www.welcometothejungle.com{job_data['url']}"
            except:
                job_data['url'] = ""
            
            # Entreprise - sélecteurs améliorés avec fallback
            company_selectors = [
                "span[class*='company']",
                "div[class*='company']",
                "a[class*='company']",
                "[data-testid='company-name']",
                "span[data-testid='company']",
                "div[data-testid='company']",
                "a[href*='/companies/']",
                "a[href*='/c/']",  # WTTJ utilise /c/ pour les companies
                "span.ais-Highlight",
                "div.sc-1pe7b5t-0",
                "p[class*='company']"
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
            
            # Fallback : chercher dans les liens
            if not company_found:
                try:
                    all_links = card.find_elements(By.CSS_SELECTOR, "a")
                    for link in all_links:
                        href = link.get_attribute('href') or ''
                        text = link.text.strip()
                        if ('/companies/' in href or '/c/' in href) and text and 2 < len(text) < 100:
                            if text != job_data.get('title', ''):
                                job_data['company'] = text
                                company_found = True
                                break
                except:
                    pass
            
            if not company_found:
                job_data['company'] = "N/A"
            
            # Localisation - sélecteurs améliorés
            location_selectors = [
                "span[class*='location']",
                "div[class*='location']",
                "[data-testid='location']",
                "span[data-testid='location']",
                "div[data-testid='location']",
                "span.sc-1pe7b5t-0",
                "div.sc-1pe7b5t-0",
                "span[aria-label*='location']",
                "div[aria-label*='location']"
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
            
            # Date de publication
            date_selectors = [
                "time", "span[class*='date'], div[class*='date'], span[class*='published']"
            ]
            for selector in date_selectors:
                try:
                    date_elem = card.find_element(By.CSS_SELECTOR, selector)
                    date_text = date_elem.get_attribute('datetime') or date_elem.text.strip()
                    if date_text:
                        job_data['date'] = date_text
                        break
                except:
                    continue
            if 'date' not in job_data:
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

