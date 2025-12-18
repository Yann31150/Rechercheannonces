"""
Générateur de lettres de motivation adaptées aux offres d'emploi
Supporte les LLM (Ollama, OpenAI, Mistral, Claude) et les templates de secours
"""
import re
import os
from utils import print_success, print_info, print_warning, load_json
import config

class CoverLetterGenerator:
    def __init__(self, use_llm: bool = None, llm_provider: str = "ollama", llm_model: str = None):
        """
        Initialise le générateur
        
        Args:
            use_llm: Si True, utilise un LLM. Si None, détecte automatiquement Ollama.
            llm_provider: "ollama", "openai", "mistral", "claude"
            llm_model: Modèle spécifique (optionnel)
        """
        self.templates = self._load_templates()
        
        # Détection automatique d'Ollama si use_llm n'est pas spécifié
        if use_llm is None:
            use_llm = self._check_ollama_available()
        
        self.use_llm = use_llm
        
        # Initialiser le LLM si demandé
        self.llm_generator = None
        if use_llm:
            try:
                from llm_generator import LLMGenerator
                # Charger la config depuis .env ou config.py
                provider = os.getenv('LLM_PROVIDER', llm_provider)
                model = os.getenv('LLM_MODEL', llm_model)
                self.llm_generator = LLMGenerator(provider=provider, model=model)
                print_info(f"✅ Mode LLM activé avec {provider} (modèle: {self.llm_generator.model})")
            except ImportError:
                print_warning("Module llm_generator non trouvé. Utilisation des templates.")
                self.use_llm = False
            except Exception as e:
                print_warning(f"Erreur avec le LLM: {str(e)}. Utilisation des templates.")
                self.use_llm = False
        else:
            print_info("Mode templates activé (pour utiliser Ollama, lancez: ollama serve)")
    
    def _check_ollama_available(self):
        """Vérifie si Ollama est disponible localement"""
        try:
            import requests
            response = requests.get("http://localhost:11434/api/tags", timeout=1)
            if response.status_code == 200:
                # Vérifier qu'un modèle est disponible
                models = response.json().get('models', [])
                if models:
                    print_info(f"✅ Ollama détecté avec {len(models)} modèle(s). Activation du mode LLM.")
                    return True
        except:
            pass
        return False
        
    def _load_templates(self):
        """Charge les templates de lettres de motivation"""
        return {
            "data_scientist": """Bonjour,

Je me permets de vous adresser ma candidature pour le poste de {job_title} que vous proposez.

{personal_intro}

Mon parcours en Data Science m'a permis de développer des compétences solides en {key_skills}, ce qui correspond parfaitement aux exigences de votre offre. J'ai notamment travaillé sur {relevant_experience}.

{why_company}

Je serais ravi de pouvoir discuter avec vous de la manière dont mon profil pourrait contribuer à vos projets.

Dans l'attente de votre retour, je vous prie d'agréer mes salutations distinguées.

{your_name}
{contact_info}""",

            "data_analyst": """Bonjour,

Par la présente, je souhaite vous faire part de mon intérêt pour le poste de {job_title} au sein de votre entreprise.

{personal_intro}

Mes compétences en analyse de données, notamment en {key_skills}, me permettent de répondre aux besoins exprimés dans votre offre. J'ai une expérience significative dans {relevant_experience}.

{why_company}

Je serais enchanté de vous rencontrer pour échanger sur cette opportunité.

Cordialement,
{your_name}
{contact_info}""",

            "data_engineer": """Bonjour,

Je vous adresse ma candidature pour le poste de {job_title}.

{personal_intro}

Mon expertise en ingénierie des données, particulièrement en {key_skills}, correspond aux compétences recherchées. J'ai notamment contribué à {relevant_experience}.

{why_company}

Je reste à votre disposition pour un entretien.

Bien cordialement,
{your_name}
{contact_info}""",

            "alternance": """Bonjour,

Je me permets de vous adresser ma candidature pour le poste en alternance de {job_title}.

Actuellement en formation, je recherche une alternance qui me permettrait d'appliquer mes connaissances théoriques en {key_skills} dans un contexte professionnel concret.

{personal_intro}

Votre entreprise m'attire particulièrement car {why_company}

Je suis motivé(e) et prêt(e) à m'investir pleinement dans cette alternance.

Dans l'attente de votre retour,
{your_name}
{contact_info}"""
        }
    
    def extract_keywords_from_job(self, job):
        """Extrait les mots-clés importants d'une offre"""
        text = " ".join([
            job.get('title', ''),
            job.get('description', '')
        ]).lower()
        
        # Compétences techniques mentionnées
        skills_found = []
        for skill in config.TECHNICAL_SKILLS:
            if skill.lower() in text:
                skills_found.append(skill)
        
        # Mots-clés métier
        keywords = []
        if 'data scientist' in text or 'data science' in text:
            keywords.append('Data Science')
        if 'machine learning' in text or 'ml' in text:
            keywords.append('Machine Learning')
        if 'analyst' in text:
            keywords.append('Analyse de données')
        if 'engineer' in text:
            keywords.append('Ingénierie des données')
        
        return skills_found[:5], keywords
    
    def generate_cover_letter(self, job, personal_info, cv_path=None):
        """
        Génère une lettre de motivation adaptée à l'offre
        
        Utilise un LLM si disponible, sinon utilise les templates
        """
        # Essayer d'abord avec le LLM si activé
        if self.use_llm and self.llm_generator:
            try:
                print_info("Génération de la lettre avec LLM...")
                # Utiliser le cv_path passé en paramètre ou celui de personal_info
                cv_path_to_use = cv_path or personal_info.get('cv_path')
                cover_letter = self.llm_generator.generate_cover_letter(job, personal_info, cv_path_to_use)
                
                # Vérifier que la lettre contient bien les informations de contact
                if not personal_info.get('email', '') in cover_letter:
                    # Ajouter les informations de contact si manquantes
                    contact_info = self._build_contact_info(personal_info)
                    if contact_info not in cover_letter:
                        cover_letter += f"\n\n{personal_info.get('name', config.YOUR_NAME)}\n{contact_info}"
                
                return cover_letter
            except Exception as e:
                print_warning(f"Erreur avec le LLM: {str(e)}. Utilisation des templates de secours.")
                # Continuer avec les templates
        
        # Fallback vers les templates
        return self._generate_with_templates(job, personal_info)
    
    def _generate_with_templates(self, job, personal_info):
        """Génère une lettre avec les templates (méthode originale)"""
        # Déterminer le type de poste
        title_lower = job.get('title', '').lower()
        job_type = "data_scientist"
        
        if 'analyst' in title_lower:
            job_type = "data_analyst"
        elif 'engineer' in title_lower or 'ingénieur' in title_lower:
            job_type = "data_engineer"
        elif 'alternance' in title_lower or 'apprentissage' in title_lower or 'stage' in title_lower:
            job_type = "alternance"
        
        # Extraire les compétences clés
        skills_found, keywords = self.extract_keywords_from_job(job)
        key_skills = ", ".join(skills_found[:3]) if skills_found else ", ".join(config.YOUR_SKILLS[:3])
        
        # Construire les informations de contact
        contact_info = self._build_contact_info(personal_info)
        
        variables = {
            'job_title': job.get('title', 'ce poste'),
            'company': job.get('company', 'votre entreprise'),
            'location': job.get('location', ''),
            'key_skills': key_skills,
            'your_name': personal_info.get('name', config.YOUR_NAME),
            'contact_info': contact_info,
            'personal_intro': personal_info.get('intro', self._generate_default_intro(keywords)),
            'relevant_experience': personal_info.get('experience', 'des projets variés en data'),
            'why_company': self._generate_why_company(job, personal_info)
        }
        
        # Générer la lettre
        template = self.templates.get(job_type, self.templates['data_scientist'])
        cover_letter = template.format(**variables)
        
        return cover_letter
    
    def _build_contact_info(self, personal_info):
        """Construit les informations de contact"""
        contact_parts = [personal_info.get('email', '')]
        if personal_info.get('phone'):
            contact_parts.append(f"Tél: {personal_info.get('phone')}")
        if personal_info.get('address'):
            contact_parts.append(personal_info.get('address'))
        return "\n".join(contact_parts)
    
    def _generate_default_intro(self, keywords):
        """Génère une introduction par défaut plus variée"""
        intros = [
            "Passionné(e) par la data et l'analyse, je suis convaincu(e) que mon profil correspond parfaitement à vos attentes.",
            "Avec une solide expérience en data science, je suis enthousiaste à l'idée de rejoindre votre équipe.",
            "Mon parcours en data science m'a permis de développer des compétences qui correspondent aux exigences de votre poste.",
            "Je suis très intéressé(e) par cette opportunité qui me permettrait de mettre à profit mes compétences en data."
        ]
        
        if keywords:
            # Personnaliser avec les mots-clés
            keyword_text = ', '.join(keywords[:2])
            return f"Passionné(e) par {keyword_text}, je suis convaincu(e) que mon profil correspond parfaitement à vos attentes."
        
        # Varier les introductions
        intro_index = abs(hash(str(keywords))) % len(intros)
        return intros[intro_index]
    
    def _generate_why_company(self, job, personal_info):
        """Génère une phrase sur pourquoi cette entreprise"""
        company = job.get('company', 'votre entreprise')
        location = job.get('location', '')
        
        # Phrases plus variées et personnalisées
        reasons = [
            f"votre entreprise {company} représente une opportunité passionnante pour mettre en pratique mes compétences en data.",
            f"je suis particulièrement attiré(e) par {company} et ses projets innovants dans le domaine de la data.",
            f"votre entreprise {company} correspond parfaitement à mes aspirations professionnelles et à mes valeurs.",
            f"je serais ravi(e) de contribuer aux projets de {company} et d'apporter ma vision de la data science."
        ]
        
        # Utiliser une raison basée sur l'index pour varier
        reason_index = abs(hash(company)) % len(reasons)
        
        if company != 'N/A' and company:
            return reasons[reason_index]
        return "votre entreprise représente une opportunité intéressante pour mon développement professionnel dans le domaine de la data."
    
    def save_cover_letter(self, cover_letter, job, output_dir="cover_letters"):
        """Sauvegarde une lettre de motivation"""
        import os
        from datetime import datetime
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Nom de fichier basé sur le titre de l'offre
        safe_title = re.sub(r'[^\w\s-]', '', job.get('title', 'offre'))[:50]
        safe_title = safe_title.replace(' ', '_')
        filename = f"{output_dir}/{safe_title}_{datetime.now().strftime('%Y%m%d')}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(cover_letter)
        
        print_success(f"Lettre sauvegardée: {filename}")
        return filename

