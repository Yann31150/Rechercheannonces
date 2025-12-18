"""
Module de scraping pour Helloworks
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
from utils import print_success, print_error, print_info, get_timestamp

class HelloworksScraper:
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
        print_success("Driver Chrome initialisé pour Helloworks")
        
    def search_jobs(self, keywords, location="Toulouse", max_pages=3):
        """Recherche des offres d'emploi"""
        try:
            print_info(f"Recherche Helloworks: {keywords} - {location}")
            
            # URL de recherche Helloworks
            base_url = "https://www.hellowork.com/fr-fr/emploi/recherche.html"
            params = {
                "k": keywords,
                "l": location,
                "p": 1
            }
            
            query_string = "&".join([f"{k}={v}" for k, v in params.items() if v])
            url = f"{base_url}?{query_string}"
            
            self.driver.get(url)
            time.sleep(3)
            
            # Accepter les cookies si nécessaire
            try:
                accept_button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[id*='accept'], button[class*='accept-cookie']"))
                )
                accept_button.click()
                time.sleep(1)
            except:
                pass
            
            jobs = []
            for page in range(max_pages):
                print_info(f"Page {page + 1}/{max_pages}...")
                
                time.sleep(2)
                
                # Trouver les offres
                job_cards = self.driver.find_elements(
                    By.CSS_SELECTOR,
                    "article[class*='job'], div[class*='job-card'], a[href*='/offres-emploi/']"
                )
                
                if not job_cards:
                    job_cards = self.driver.find_elements(By.CSS_SELECTOR, "div[class*='result'], li[class*='job']")
                
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
                            "a[aria-label='Suivant'], a[class*='next'], button[class*='next']"
                        )
                        next_button.click()
                        time.sleep(3)
                    except:
                        break
            
            self.jobs.extend(jobs)
            print_success(f"{len(jobs)} offres trouvées sur Helloworks")
            return jobs
            
        except Exception as e:
            print_error(f"Erreur lors de la recherche: {str(e)}")
            return []
    
    def _extract_job_details(self, card):
        """Extrait les détails d'une offre"""
        try:
            job_data = {'source': 'Helloworks'}
            
            # Titre
            title_selectors = [
                "h2 a", "h3 a", "a[class*='title']", "span[class*='title']", "h2", "h3"
            ]
            for selector in title_selectors:
                try:
                    title_elem = card.find_element(By.CSS_SELECTOR, selector)
                    job_data['title'] = title_elem.text.strip()
                    if title_elem.tag_name == 'a':
                        job_data['url'] = title_elem.get_attribute('href')
                    break
                except:
                    continue
            
            if 'title' not in job_data:
                return None
            
            # URL si pas déjà trouvée
            if 'url' not in job_data or not job_data['url']:
                try:
                    link_elem = card.find_element(By.CSS_SELECTOR, "a")
                    job_data['url'] = link_elem.get_attribute('href')
                    if job_data['url'] and not job_data['url'].startswith('http'):
                        job_data['url'] = f"https://www.hellowork.com{job_data['url']}"
                except:
                    job_data['url'] = ""
            
            # Entreprise - sélecteurs améliorés pour Helloworks avec fallback
            company_selectors = [
                "span[class*='company']",
                "div[class*='company']",
                "a[class*='company']",
                "span.offre-emploi__company",
                "div.offre-emploi__company",
                "span[data-company]",
                "div[data-company]",
                "span.tw-text-body-base-medium",
                "div.tw-text-body-base-medium",
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
            
            # Localisation - sélecteurs améliorés pour Helloworks
            location_selectors = [
                "span[class*='location']",
                "div[class*='location']",
                "span.offre-emploi__location",
                "div.offre-emploi__location",
                "span[data-location]",
                "div[data-location]"
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

