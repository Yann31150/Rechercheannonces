"""
Module de scraping pour l'APEC
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

class ApecScraper:
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
        print_success("Driver Chrome initialisé pour l'APEC")
        
    def search_jobs(self, keywords, location="Toulouse", max_pages=3):
        """Recherche des offres d'emploi"""
        try:
            print_info(f"Recherche APEC: {keywords} - {location}")
            
            # URL de recherche APEC - format direct
            # L'APEC utilise un format d'URL spécifique
            base_url = "https://www.apec.fr/candidat/recherche-emploi.html/emploi.html"
            
            # Construire l'URL avec les paramètres
            params = {
                "motsCles": keywords.replace(' ', '+'),
                "lieux": location.replace(' ', '+'),
                "page": 1
            }
            
            query_string = "&".join([f"{k}={v}" for k, v in params.items()])
            url = f"{base_url}?{query_string}"
            
            print_info(f"URL APEC: {url}")
            self.driver.get(url)
            time.sleep(5)
            
            # Accepter les cookies si nécessaire
            try:
                accept_selectors = [
                    "button[id*='accept']",
                    "button[class*='accept']",
                    "button[class*='cookie']",
                    "#onetrust-accept-btn-handler",
                    "button[aria-label*='Accepter']"
                ]
                for selector in accept_selectors:
                    try:
                        accept_button = WebDriverWait(self.driver, 3).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                        accept_button.click()
                        time.sleep(1)
                        break
                    except:
                        continue
            except:
                pass
            
            # Attendre que les résultats se chargent
            time.sleep(3)
            
            jobs = []
            for page in range(max_pages):
                print_info(f"Page {page + 1}/{max_pages}...")
                
                time.sleep(3)
                
                # Essayer plusieurs sélecteurs pour trouver les offres APEC
                job_cards = []
                selectors = [
                    "article[class*='offer']",
                    "div[class*='offer']",
                    "li[class*='offer']",
                    "a[href*='/offres-emploi/']",
                    "div[class*='result']",
                    "div[class*='job']",
                    "div[data-offre-id]",
                    "article[data-offre-id]",
                    "div[class*='card']",
                    "li[class*='result']",
                    "div[class*='listing'] > div",
                    "ul[class*='results'] > li"
                ]
                
                for selector in selectors:
                    try:
                        job_cards = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        if job_cards:
                            print_info(f"Trouvé {len(job_cards)} éléments avec le sélecteur: {selector}")
                            # Filtrer pour ne garder que ceux qui ressemblent à des offres
                            job_cards = [c for c in job_cards if c.text.strip() and len(c.text.strip()) > 20]
                            if job_cards:
                                print_info(f"Après filtrage: {len(job_cards)} offres valides")
                                break
                    except:
                        continue
                
                if not job_cards:
                    print_warning("Aucune offre trouvée. Vérification de la page...")
                    # Prendre une capture de la structure de la page pour debug
                    try:
                        page_text = self.driver.find_element(By.TAG_NAME, "body").text[:500]
                        if "offre" in page_text.lower() or "emploi" in page_text.lower():
                            print_info("La page contient du contenu lié aux emplois")
                        else:
                            print_warning("La page ne semble pas contenir d'offres")
                    except:
                        pass
                    break
                
                print_info(f"Extraction de {len(job_cards)} offres sur la page {page + 1}")
                
                for i, card in enumerate(job_cards[:30]):  # Limiter à 30 par page
                    try:
                        job_data = self._extract_job_details(card, i)
                        if job_data and job_data.get('title') and job_data.get('title') != 'N/A':
                            jobs.append(job_data)
                            print_info(f"  ✓ {job_data.get('title', 'N/A')[:50]}...")
                    except Exception as e:
                        continue
                
                # Passer à la page suivante
                if page < max_pages - 1:
                    try:
                        next_selectors = [
                            "a[aria-label='Suivant']",
                            "a[class*='next']",
                            "button[class*='next']",
                            "a[href*='page=']",
                            "li[class*='next'] a"
                        ]
                        next_button = None
                        for selector in next_selectors:
                            try:
                                next_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                                if next_button and next_button.is_enabled():
                                    next_button.click()
                                    time.sleep(3)
                                    break
                            except:
                                continue
                        if not next_button:
                            print_info("Pas de page suivante disponible")
                            break
                    except:
                        break
            
            self.jobs.extend(jobs)
            print_success(f"{len(jobs)} offres trouvées sur l'APEC")
            return jobs
            
        except Exception as e:
            print_error(f"Erreur lors de la recherche: {str(e)}")
            return []
    
    def _extract_job_details(self, card, index=0):
        """Extrait les détails d'une offre"""
        try:
            job_data = {'source': 'APEC'}
            
            # Titre - plusieurs sélecteurs possibles
            title_selectors = [
                "h2 a", "h3 a", "h4 a",
                "a[class*='title']",
                "span[class*='title']",
                "div[class*='title']",
                "h2", "h3", "h4",
                "a[href*='/offres-emploi/']",
                "a[href*='/offre']"
            ]
            
            for selector in title_selectors:
                try:
                    title_elem = card.find_element(By.CSS_SELECTOR, selector)
                    title_text = title_elem.text.strip()
                    if title_text and len(title_text) > 5:  # Vérifier que c'est un vrai titre
                        job_data['title'] = title_text
                        if title_elem.tag_name == 'a':
                            job_data['url'] = title_elem.get_attribute('href')
                        break
                except:
                    continue
            
            # Si pas de titre trouvé, essayer de prendre le texte principal
            if 'title' not in job_data:
                try:
                    # Prendre le premier lien ou le texte principal
                    all_links = card.find_elements(By.CSS_SELECTOR, "a")
                    for link in all_links:
                        link_text = link.text.strip()
                        if link_text and len(link_text) > 10 and len(link_text) < 200:
                            job_data['title'] = link_text
                            job_data['url'] = link.get_attribute('href')
                            break
                except:
                    pass
            
            if 'title' not in job_data or not job_data.get('title'):
                return None
            
            # URL si pas déjà trouvée
            if 'url' not in job_data or not job_data['url']:
                try:
                    link_elem = card.find_element(By.CSS_SELECTOR, "a")
                    job_data['url'] = link_elem.get_attribute('href')
                    if job_data['url'] and not job_data['url'].startswith('http'):
                        job_data['url'] = f"https://www.apec.fr{job_data['url']}"
                except:
                    job_data['url'] = ""
            
            # Entreprise - sélecteurs améliorés pour APEC avec fallback
            company_selectors = [
                "span.card-offer__company",
                "div.card-offer__company",
                "a.card-offer__company",
                "span[class*='company']",
                "div[class*='company']",
                "a[class*='company']",
                "span[data-cy='company-name']",
                "div[data-cy='company-name']",
                "h3.card-offer__company-name",
                "span.offre-emploi__company",
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
            
            # Localisation - sélecteurs améliorés pour APEC
            location_selectors = [
                "span.card-offer__location",
                "div.card-offer__location",
                "span[class*='location']",
                "div[class*='location']",
                "span[data-cy='location']",
                "div[data-cy='location']",
                "span.offre-emploi__location",
                "div.offre-emploi__location",
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

