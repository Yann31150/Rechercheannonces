"""
Module de scraping des offres d'emploi LinkedIn
"""
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import config
from utils import print_success, print_error, print_warning, print_info, save_json, get_timestamp

class LinkedInJobScraper:
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
            
            # Attendre plus longtemps pour la connexion et les vérifications
            time.sleep(10)
            
            # Vérifier si la connexion a réussi
            current_url = self.driver.current_url
            if "feed" in current_url or "linkedin.com/in/" in current_url or "linkedin.com/jobs" in current_url:
                print_success("Connexion réussie à LinkedIn")
                return True
            elif "challenge" in current_url or "checkpoint" in current_url:
                print_warning("LinkedIn demande une vérification (captcha/2FA).")
                print_info("Veuillez compléter la vérification dans le navigateur qui s'est ouvert.")
                print_info("Attente de 30 secondes pour que vous puissiez vous connecter manuellement...")
                time.sleep(30)
                # Vérifier à nouveau après l'attente
                current_url = self.driver.current_url
                if "feed" in current_url or "linkedin.com/in/" in current_url or "linkedin.com/jobs" in current_url:
                    print_success("Connexion réussie après vérification manuelle")
                    return True
                else:
                    print_warning("Continuer quand même...")
                    return True
            else:
                print_warning(f"Connexion peut-être échouée. URL actuelle: {current_url}")
                print_info("Tentative de continuation malgré tout...")
                return True  # Continuer quand même pour voir
                
        except Exception as e:
            print_error(f"Erreur lors de la connexion: {str(e)}")
            return False
    
    def search_jobs(self, keywords, location="", experience_level="", max_pages=5):
        """Recherche des offres d'emploi"""
        try:
            print_info(f"Recherche d'offres: {keywords} - {location}")
            
            # Construire l'URL de recherche
            base_url = "https://www.linkedin.com/jobs/search/"
            params = {
                "keywords": keywords,
                "location": location,
                "f_E": experience_level,  # Niveau d'expérience
                "start": 0
            }
            
            # Filtrer les paramètres vides
            query_string = "&".join([f"{k}={v}" for k, v in params.items() if v])
            url = f"{base_url}?{query_string}"
            
            self.driver.get(url)
            time.sleep(3)
            
            # Scroller pour charger plus de résultats
            self._scroll_page()
            
            # Extraire les offres
            jobs = self._extract_jobs(max_pages)
            self.jobs.extend(jobs)
            
            print_success(f"{len(jobs)} offres trouvées")
            return jobs
            
        except Exception as e:
            print_error(f"Erreur lors de la recherche: {str(e)}")
            return []
    
    def _scroll_page(self):
        """Fait défiler la page pour charger plus de résultats"""
        try:
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            scrolls = 0
            max_scrolls = 3
            
            while scrolls < max_scrolls:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                
                if new_height == last_height:
                    break
                last_height = new_height
                scrolls += 1
        except Exception as e:
            print_warning(f"Erreur lors du scroll: {str(e)}")
    
    def _extract_jobs(self, max_pages=5):
        """Extrait les informations des offres d'emploi"""
        jobs = []
        page = 0
        
        try:
            # Attendre que la page se charge
            time.sleep(5)
            
            while page < max_pages:
                # Attendre que les résultats se chargent
                time.sleep(3)
                
                # Essayer plusieurs sélecteurs CSS possibles pour LinkedIn
                job_cards = []
                selectors = [
                    "ul.jobs-search__results-list > li",
                    "div.jobs-search-results-list > ul > li",
                    "li.jobs-search-results__list-item",
                    "div[data-job-id]",
                    "li[data-occludable-job-id]",
                    "div.job-card-container",
                    "li.job-card-list__entity-lockup"
                ]
                
                for selector in selectors:
                    try:
                        job_cards = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        if job_cards:
                            print_info(f"Trouvé {len(job_cards)} offres avec le sélecteur: {selector}")
                            break
                    except:
                        continue
                
                if not job_cards:
                    print_warning("Aucune offre trouvée. Vérification de la page...")
                    # Prendre une capture d'écran pour debug
                    try:
                        page_source = self.driver.page_source
                        if "job" in page_source.lower() or "emploi" in page_source.lower():
                            print_info("La page contient du contenu lié aux emplois")
                        else:
                            print_warning("La page ne semble pas contenir d'offres d'emploi")
                    except:
                        pass
                    break
                
                print_info(f"Extraction des offres de la page {page + 1}...")
                
                for i, card in enumerate(job_cards[:25]):  # Limiter à 25 par page
                    try:
                        # Extraire les données directement depuis la carte sans clic si possible
                        job_data = self._extract_job_details_from_card(card, i)
                        if not job_data or job_data.get('title') == "N/A":
                            # Si l'extraction directe échoue, essayer avec clic
                            job_data = self._extract_job_details(card, i)
                        
                        if job_data and job_data.get('title') != "N/A":
                            jobs.append(job_data)
                            print_info(f"  ✓ {job_data.get('title', 'N/A')[:50]}...")
                    except Exception as e:
                        print_warning(f"  ✗ Erreur sur l'offre {i+1}: {str(e)[:50]}")
                        continue
                
                # Essayer de passer à la page suivante
                try:
                    next_selectors = [
                        "button[aria-label='Page suivante']",
                        "button[aria-label='Next']",
                        "button.artdeco-pagination__button--next",
                        "li[data-test-pagination-page-btn].selected + li button"
                    ]
                    next_button = None
                    for selector in next_selectors:
                        try:
                            next_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                            if next_button and next_button.is_enabled():
                                break
                        except:
                            continue
                    
                    if next_button and next_button.is_enabled():
                        next_button.click()
                        time.sleep(3)
                        page += 1
                    else:
                        print_info("Pas de page suivante disponible")
                        break
                except NoSuchElementException:
                    print_info("Bouton suivant non trouvé, fin de la recherche")
                    break
                
        except Exception as e:
            print_error(f"Erreur lors de l'extraction: {str(e)}")
        
        return jobs
    
    def _extract_job_details_from_card(self, card, index=0):
        """Extrait les détails directement depuis la carte sans clic"""
        try:
            job_data = {}
            
            # Titre - plusieurs sélecteurs possibles
            title_selectors = [
                "a.job-card-list__title",
                "a.base-card__full-link",
                "h3.base-search-card__title a",
                "span.job-search-card__title",
                "a[data-control-name='job_card_title']",
                "a[href*='/jobs/view/']",
                "h3 a"
            ]
            for selector in title_selectors:
                try:
                    title_elem = card.find_element(By.CSS_SELECTOR, selector)
                    job_data['title'] = title_elem.text.strip()
                    job_data['url'] = title_elem.get_attribute('href')
                    if job_data['title']:
                        break
                except:
                    continue
            if 'title' not in job_data or not job_data.get('title'):
                return None
            
            # Entreprise - sélecteurs améliorés avec fallback
            company_selectors = [
                "h4.base-search-card__subtitle",
                "h4.job-card-container__company-name",
                "span.job-card-container__primary-description",
                "a.job-card-container__company-name",
                "h4 a",
                "a.base-card__full-link",
                "span.job-card-container__company-name",
                "div.job-card-container__company-name",
                "h4[class*='company']",
                "span[class*='company']",
                "a[class*='company']",
                # Sélecteurs génériques
                "h4",
                "span[aria-label*='company']",
                "div[aria-label*='company']"
            ]
            company_found = False
            for selector in company_selectors:
                try:
                    company_elems = card.find_elements(By.CSS_SELECTOR, selector)
                    for company_elem in company_elems:
                        company_text = company_elem.text.strip()
                        # Filtrer les éléments qui sont probablement des titres ou des dates
                        if company_text and len(company_text) > 1 and len(company_text) < 100:
                            # Exclure les dates et autres éléments
                            if not any(word in company_text.lower() for word in ['il y a', 'ago', 'jour', 'day', 'semaine', 'week']):
                                if company_text != job_data.get('title', ''):
                                    job_data['company'] = company_text
                                    company_found = True
                                    break
                    if company_found:
                        break
                except:
                    continue
            
            # Fallback : chercher dans tous les éléments de la carte
            if not company_found:
                try:
                    # Chercher tous les liens qui pourraient être des entreprises
                    all_links = card.find_elements(By.CSS_SELECTOR, "a")
                    for link in all_links:
                        href = link.get_attribute('href') or ''
                        text = link.text.strip()
                        # Si le lien pointe vers une page entreprise
                        if ('/company/' in href or '/companies/' in href) and text and len(text) < 100:
                            job_data['company'] = text
                            company_found = True
                            break
                except:
                    pass
            
            if not company_found:
                job_data['company'] = "N/A"
            
            # Localisation
            location_selectors = [
                "span.job-card-container__metadata-item",
                "span.job-search-card__location",
                "li.job-search-card__location",
                "span[class*='location']"
            ]
            for selector in location_selectors:
                try:
                    location_elems = card.find_elements(By.CSS_SELECTOR, selector)
                    if location_elems:
                        job_data['location'] = location_elems[0].text.strip()
                        break
                except:
                    continue
            if 'location' not in job_data:
                job_data['location'] = "N/A"
            
            # Date
            date_selectors = [
                "time.job-card-container__metadata-item",
                "time.job-search-card__listdate",
                "span.job-card-container__listed-time",
                "time"
            ]
            for selector in date_selectors:
                try:
                    date_elem = card.find_element(By.CSS_SELECTOR, selector)
                    job_data['date'] = date_elem.get_attribute('datetime') or date_elem.text.strip()
                    if job_data['date']:
                        break
                except:
                    continue
            if 'date' not in job_data:
                job_data['date'] = "N/A"
            
            job_data['description'] = ""  # Description vide pour extraction directe
            job_data['scraped_at'] = get_timestamp()
            
            return job_data
            
        except Exception as e:
            return None
    
    def _extract_job_details(self, card, index=0):
        """Extrait les détails d'une offre d'emploi"""
        try:
            job_data = {}
            
            # Essayer de cliquer sur la carte pour charger les détails
            try:
                # Scroller pour rendre l'élément visible
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", card)
                time.sleep(1)
                # Essayer de cliquer avec JavaScript si le clic normal échoue
                try:
                    card.click()
                except:
                    # Si le clic normal échoue, utiliser JavaScript
                    self.driver.execute_script("arguments[0].click();", card)
                time.sleep(2)
            except Exception as e:
                # Si même le clic JS échoue, continuer sans clic
                pass
            
            # Titre - plusieurs sélecteurs possibles
            title_selectors = [
                "a.job-card-list__title",
                "a.base-card__full-link",
                "h3.base-search-card__title a",
                "span.job-search-card__title",
                "a[data-control-name='job_card_title']"
            ]
            for selector in title_selectors:
                try:
                    title_elem = card.find_element(By.CSS_SELECTOR, selector)
                    job_data['title'] = title_elem.text.strip()
                    job_data['url'] = title_elem.get_attribute('href')
                    break
                except:
                    continue
            if 'title' not in job_data:
                job_data['title'] = "N/A"
                job_data['url'] = ""
            
            # Entreprise - plusieurs sélecteurs (carte + panneau de détails) avec améliorations
            company_selectors = [
                "h4.base-search-card__subtitle",
                "h4.job-card-container__company-name",
                "span.job-card-container__primary-description",
                "a.job-card-container__company-name",
                "a.base-card__full-link",
                "span.job-card-container__company-name",
                "div.job-card-container__company-name",
                "h4[class*='company']",
                "span[class*='company']",
                "a[class*='company']",
                "h4",
                "span[aria-label*='company']"
            ]
            company_found = False
            for selector in company_selectors:
                try:
                    company_elems = card.find_elements(By.CSS_SELECTOR, selector)
                    for company_elem in company_elems:
                        company_text = company_elem.text.strip()
                        # Filtrer les éléments qui sont probablement des titres ou des dates
                        if company_text and len(company_text) > 1 and len(company_text) < 100:
                            # Exclure les dates et le titre
                            if not any(word in company_text.lower() for word in ['il y a', 'ago', 'jour', 'day', 'semaine', 'week']):
                                if company_text != job_data.get('title', ''):
                                    job_data['company'] = company_text
                                    company_found = True
                                    break
                    if company_found:
                        break
                except:
                    continue
            
            # Fallback : chercher dans les liens de la carte
            if not company_found:
                try:
                    all_links = card.find_elements(By.CSS_SELECTOR, "a")
                    for link in all_links:
                        href = link.get_attribute('href') or ''
                        text = link.text.strip()
                        # Si le lien pointe vers une page entreprise
                        if ('/company/' in href or '/companies/' in href or '/in/company/' in href) and text and len(text) < 100:
                            if text != job_data.get('title', ''):
                                job_data['company'] = text
                                company_found = True
                                break
                except:
                    pass
            
            # Si pas trouvé dans la carte, essayer dans le panneau de détails
            if not company_found:
                try:
                    detail_panel_selectors = [
                        "div.jobs-details-top-card__company-name a",
                        "a.jobs-details-top-card__company-name",
                        "span.jobs-details-top-card__company-name",
                        "h3.topcard__org-name",
                        "a.topcard__org-name-link",
                        "a[href*='/company/']",
                        "a[href*='/companies/']"
                    ]
                    for selector in detail_panel_selectors:
                        try:
                            company_elems = self.driver.find_elements(By.CSS_SELECTOR, selector)
                            for company_elem in company_elems:
                                company_text = company_elem.text.strip()
                                if company_text and company_text != "" and len(company_text) < 100:
                                    if company_text != job_data.get('title', ''):
                                        job_data['company'] = company_text
                                        company_found = True
                                        break
                            if company_found:
                                break
                        except:
                            continue
                except:
                    pass
            
            if not company_found:
                job_data['company'] = "N/A"
            
            # Localisation - plusieurs sélecteurs (carte + panneau de détails)
            location_selectors = [
                "span.job-card-container__metadata-item",
                "span.job-search-card__location",
                "li.job-search-card__location",
                "span.job-card-container__metadata-wrapper",
                "div.job-card-container__metadata-item"
            ]
            location_found = False
            for selector in location_selectors:
                try:
                    location_elems = card.find_elements(By.CSS_SELECTOR, selector)
                    for loc_elem in location_elems:
                        loc_text = loc_elem.text.strip()
                        # Filtrer les éléments qui contiennent "il y a" (dates) ou sont vides
                        if loc_text and "il y a" not in loc_text.lower() and "ago" not in loc_text.lower() and len(loc_text) > 2:
                            job_data['location'] = loc_text
                            location_found = True
                            break
                    if location_found:
                        break
                except:
                    continue
            
            # Si pas trouvé dans la carte, essayer dans le panneau de détails
            if not location_found:
                try:
                    detail_location_selectors = [
                        "span.jobs-details-top-card__bullet",
                        "div.jobs-details-top-card__primary-description-without-tagline",
                        "span.topcard__flavor--black-link",
                        "div.topcard__flavor"
                    ]
                    for selector in detail_location_selectors:
                        try:
                            location_elems = self.driver.find_elements(By.CSS_SELECTOR, selector)
                            for loc_elem in location_elems:
                                loc_text = loc_elem.text.strip()
                                # Filtrer les dates et éléments vides
                                if loc_text and "il y a" not in loc_text.lower() and "ago" not in loc_text.lower() and len(loc_text) > 2:
                                    # Vérifier que ce n'est pas une date
                                    if not any(char.isdigit() for char in loc_text[:3]):
                                        job_data['location'] = loc_text
                                        location_found = True
                                        break
                            if location_found:
                                break
                        except:
                            continue
                except:
                    pass
            
            if not location_found:
                job_data['location'] = "N/A"
            
            # Date de publication - améliorée
            date_selectors = [
                "time.job-card-container__metadata-item",
                "time.job-search-card__listdate",
                "span.job-card-container__listed-time",
                "time[datetime]",
                "span[class*='date']",
                "time"
            ]
            for selector in date_selectors:
                try:
                    date_elem = card.find_element(By.CSS_SELECTOR, selector)
                    # Essayer d'abord l'attribut datetime
                    date_text = date_elem.get_attribute('datetime')
                    if not date_text:
                        date_text = date_elem.text.strip()
                    if date_text and date_text != "N/A":
                        job_data['date'] = date_text
                        break
                except:
                    continue
            if 'date' not in job_data:
                job_data['date'] = "N/A"
            
            # Description (depuis le panneau de droite après clic)
            desc_selectors = [
                "div.show-more-less-html__markup",
                "div.description__text",
                "div.jobs-description__text"
            ]
            for selector in desc_selectors:
                try:
                    description_elem = WebDriverWait(self.driver, 3).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    job_data['description'] = description_elem.text.strip()[:500]
                    break
                except:
                    continue
            if 'description' not in job_data:
                job_data['description'] = ""
            
            job_data['scraped_at'] = get_timestamp()
            
            return job_data
            
        except Exception as e:
            print_warning(f"Erreur extraction détails offre {index}: {str(e)[:100]}")
            return None
    
    def get_job_details(self, job_url):
        """Récupère les détails complets d'une offre"""
        try:
            self.driver.get(job_url)
            time.sleep(2)
            
            details = {}
            
            # Description complète
            try:
                desc_elem = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.show-more-less-html__markup"))
                )
                details['full_description'] = desc_elem.text.strip()
            except:
                details['full_description'] = ""
            
            # Critères (expérience, type de contrat, etc.)
            try:
                criteria = self.driver.find_elements(By.CSS_SELECTOR, "span.description__job-criteria-text")
                details['criteria'] = [c.text for c in criteria]
            except:
                details['criteria'] = []
            
            return details
            
        except Exception as e:
            print_error(f"Erreur lors de la récupération des détails: {str(e)}")
            return {}
    
    def save_results(self, filename=None):
        """Sauvegarde les résultats"""
        filename = filename or config.JOBS_FILE
        save_json(self.jobs, filename)
        print_success(f"Résultats sauvegardés dans {filename}")
    
    def close(self):
        """Ferme le driver"""
        if self.driver:
            self.driver.quit()
            print_info("Driver fermé")

