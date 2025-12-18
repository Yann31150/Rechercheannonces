"""
Générateur de lettres de motivation utilisant des LLM
Supporte : Ollama (local), OpenAI, Mistral, Anthropic Claude
"""
import os
import json
from typing import Optional, Dict, Any
from utils import print_info, print_error, print_success, print_warning

def extract_cv_text(cv_path: Optional[str]) -> str:
    """Extrait le texte d'un CV PDF"""
    if not cv_path or not os.path.exists(cv_path):
        return ""
    
    try:
        import PyPDF2
        
        cv_text = ""
        with open(cv_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                cv_text += page.extract_text() + "\n"
        
        # Nettoyer le texte
        cv_text = cv_text.strip()
        # Limiter à 3000 caractères pour ne pas surcharger le prompt
        if len(cv_text) > 3000:
            cv_text = cv_text[:3000] + "..."
        
        return cv_text
    except ImportError:
        print_warning("PyPDF2 non installé. Installez-le avec: pip install PyPDF2")
        return ""
    except Exception as e:
        print_warning(f"Erreur lors de l'extraction du CV: {str(e)}")
        return ""

class LLMGenerator:
    """Générateur utilisant différents LLM pour créer des lettres de motivation"""
    
    def __init__(self, provider: str = "ollama", model: Optional[str] = None):
        """
        Initialise le générateur LLM
        
        Args:
            provider: "ollama", "openai", "mistral", "claude"
            model: Nom du modèle à utiliser (optionnel, utilise les valeurs par défaut)
        """
        self.provider = provider.lower()
        self.model = model or self._get_default_model()
        self.api_key = self._load_api_key()
        
    def _get_default_model(self) -> str:
        """Retourne le modèle par défaut selon le provider"""
        defaults = {
            "ollama": "llama3.2",  # ou "mistral", "qwen2.5", etc.
            "openai": "gpt-4o-mini",  # ou "gpt-4", "gpt-3.5-turbo"
            "mistral": "mistral-medium",  # ou "mistral-small", "mistral-large"
            "claude": "claude-3-5-sonnet-20241022"  # ou "claude-3-opus", "claude-3-haiku"
        }
        return defaults.get(self.provider, "llama3.2")
    
    def _load_api_key(self) -> Optional[str]:
        """Charge la clé API depuis les variables d'environnement ou .env"""
        key_names = {
            "openai": "OPENAI_API_KEY",
            "mistral": "MISTRAL_API_KEY",
            "claude": "ANTHROPIC_API_KEY"
        }
        
        if self.provider in key_names:
            # Essayer depuis les variables d'environnement
            api_key = os.getenv(key_names[self.provider])
            if api_key:
                return api_key
            
            # Essayer depuis .env
            try:
                from dotenv import load_dotenv
                load_dotenv()
                return os.getenv(key_names[self.provider])
            except:
                pass
        
        return None
    
    def generate_cover_letter(self, job: Dict[str, Any], personal_info: Dict[str, Any], cv_path: Optional[str] = None) -> str:
        """
        Génère une lettre de motivation personnalisée avec un LLM
        
        Args:
            job: Dictionnaire avec les informations de l'offre (title, company, description, etc.)
            personal_info: Dictionnaire avec les informations personnelles (name, email, intro, experience, skills)
            cv_path: Chemin vers le CV PDF (optionnel, pour extraire le contenu)
        
        Returns:
            Lettre de motivation générée
        """
        prompt = self._build_prompt(job, personal_info, cv_path)
        
        try:
            if self.provider == "ollama":
                return self._generate_with_ollama(prompt)
            elif self.provider == "openai":
                return self._generate_with_openai(prompt)
            elif self.provider == "mistral":
                return self._generate_with_mistral(prompt)
            elif self.provider == "claude":
                return self._generate_with_claude(prompt)
            else:
                raise ValueError(f"Provider non supporté: {self.provider}")
        except Exception as e:
            print_error(f"Erreur lors de la génération avec {self.provider}: {str(e)}")
            # Fallback vers template simple si le LLM échoue
            return self._generate_fallback_letter(job, personal_info)
    
    def _build_prompt(self, job: Dict[str, Any], personal_info: Dict[str, Any], cv_path: Optional[str] = None) -> str:
        """Construit le prompt pour le LLM avec le contenu du CV"""
        job_title = job.get('title', 'ce poste')
        company = job.get('company', 'cette entreprise')
        location = job.get('location', '')
        description = job.get('description', '')[:2000]  # Augmenté pour plus de contexte
        
        name = personal_info.get('name', 'le candidat')
        email = personal_info.get('email', '')
        phone = personal_info.get('phone', '')
        address = personal_info.get('address', '')
        intro = personal_info.get('intro', '')
        experience = personal_info.get('experience', '')
        skills = ", ".join(personal_info.get('skills', []))
        
        # Extraire le contenu du CV si disponible
        cv_content = ""
        if cv_path:
            cv_content = extract_cv_text(cv_path)
            if cv_content:
                print_info("✅ Contenu du CV extrait et inclus dans la génération")
        
        # Construire le prompt avec le CV
        cv_section = ""
        if cv_content:
            cv_section = f"""
CONTENU DU CV DU CANDIDAT :
{cv_content}

IMPORTANT : Utilise les informations précises du CV ci-dessus pour personnaliser la lettre. Mentionne des expériences, projets ou compétences spécifiques du CV qui correspondent au poste.
"""
        
        prompt = f"""Tu es un expert en rédaction de lettres de motivation professionnelles en français.

Tâche : Rédige une lettre de motivation convaincante, professionnelle et HIGHLY PERSONNALISÉE pour le poste suivant.

═══════════════════════════════════════════════════════════════
INFORMATIONS SUR LE POSTE :
═══════════════════════════════════════════════════════════════
- Titre du poste : {job_title}
- Entreprise : {company}
- Localisation : {location}
- Description complète de l'offre :
{description}

═══════════════════════════════════════════════════════════════
INFORMATIONS SUR LE CANDIDAT :
═══════════════════════════════════════════════════════════════
- Nom : {name}
- Email : {email}
- Téléphone : {phone}
- Adresse : {address}
- Introduction personnelle : {intro}
- Expérience mentionnée : {experience}
- Compétences listées : {skills}
{cv_section}
═══════════════════════════════════════════════════════════════
INSTRUCTIONS DÉTAILLÉES :
═══════════════════════════════════════════════════════════════
1. La lettre doit être en français, professionnelle mais chaleureuse et authentique
2. Longueur : environ 300-400 mots (pas trop courte, pas trop longue)
3. PERSONNALISATION MAXIMALE :
   - Adapte-toi spécifiquement à cette offre et cette entreprise
   - Utilise des détails précis de l'offre (compétences mentionnées, missions, etc.)
   - Si le CV est fourni, cite des expériences, projets ou réalisations CONCRÈTES du CV
   - Montre que tu as vraiment lu et compris l'offre
4. Structure de la lettre :
   - Salutation personnalisée (si le nom du recruteur n'est pas disponible, utilise "Madame, Monsieur")
   - Paragraphe 1 : Accroche + pourquoi ce poste t'intéresse spécifiquement
   - Paragraphe 2 : Tes compétences et expériences qui correspondent EXACTEMENT au poste (cite des exemples du CV si disponible)
   - Paragraphe 3 : Pourquoi cette entreprise t'attire + ce que tu peux apporter
   - Paragraphe 4 : Conclusion + disponibilité pour un entretien
   - Formule de politesse
   - Signature avec coordonnées complètes
5. Points importants :
   - Ne pas utiliser de placeholders ou de texte générique
   - Tout doit être concret, spécifique et personnalisé
   - Mentionne des compétences techniques précises de l'offre
   - Si le CV contient des projets pertinents, mentionne-les brièvement
   - Le ton doit être professionnel mais authentique et enthousiaste
   - Évite les phrases toutes faites, sois original tout en restant professionnel

Génère UNIQUEMENT la lettre de motivation complète, sans commentaires, sans explications, sans métadonnées. Commence directement par la salutation."""

        return prompt
    
    def _generate_with_ollama(self, prompt: str) -> str:
        """Génère avec Ollama (local, gratuit)"""
        try:
            import requests
            
            print_info(f"Génération avec Ollama (modèle: {self.model})...")
            
            # Vérifier que Ollama est disponible
            try:
                response = requests.get("http://localhost:11434/api/tags", timeout=2)
                if response.status_code != 200:
                    raise Exception("Ollama n'est pas accessible")
            except:
                raise Exception(
                    "Ollama n'est pas accessible. "
                    "Installez Ollama depuis https://ollama.ai et lancez-le, "
                    f"puis téléchargez un modèle avec: ollama pull {self.model}"
                )
            
            # Générer la lettre
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.9,
                        "max_tokens": 1000
                    }
                },
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                letter = result.get('response', '').strip()
                
                # Nettoyer la réponse (enlever les markdown si présent)
                letter = letter.replace('```', '').strip()
                if letter.startswith('Lettre'):
                    # Enlever les préfixes possibles
                    lines = letter.split('\n')
                    letter = '\n'.join(lines[1:]) if len(lines) > 1 else letter
                
                print_success("Lettre générée avec Ollama")
                return letter
            else:
                raise Exception(f"Erreur Ollama: {response.status_code}")
                
        except ImportError:
            raise Exception("Le package 'requests' est requis pour Ollama. Installez-le avec: pip install requests")
        except Exception as e:
            raise Exception(f"Erreur avec Ollama: {str(e)}")
    
    def _generate_with_openai(self, prompt: str) -> str:
        """Génère avec OpenAI API"""
        try:
            from openai import OpenAI
            
            if not self.api_key:
                raise Exception(
                    "Clé API OpenAI manquante. "
                    "Ajoutez OPENAI_API_KEY dans votre fichier .env ou variables d'environnement"
                )
            
            print_info(f"Génération avec OpenAI (modèle: {self.model})...")
            
            client = OpenAI(api_key=self.api_key)
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Tu es un expert en rédaction de lettres de motivation professionnelles en français."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            letter = response.choices[0].message.content.strip()
            print_success("Lettre générée avec OpenAI")
            return letter
            
        except ImportError:
            raise Exception("Le package 'openai' est requis. Installez-le avec: pip install openai")
        except Exception as e:
            raise Exception(f"Erreur avec OpenAI: {str(e)}")
    
    def _generate_with_mistral(self, prompt: str) -> str:
        """Génère avec Mistral AI API"""
        try:
            from mistralai import Mistral
            
            if not self.api_key:
                raise Exception(
                    "Clé API Mistral manquante. "
                    "Ajoutez MISTRAL_API_KEY dans votre fichier .env ou variables d'environnement"
                )
            
            print_info(f"Génération avec Mistral (modèle: {self.model})...")
            
            client = Mistral(api_key=self.api_key)
            
            response = client.chat.complete(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Tu es un expert en rédaction de lettres de motivation professionnelles en français."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            letter = response.choices[0].message.content.strip()
            print_success("Lettre générée avec Mistral")
            return letter
            
        except ImportError:
            raise Exception("Le package 'mistralai' est requis. Installez-le avec: pip install mistralai")
        except Exception as e:
            raise Exception(f"Erreur avec Mistral: {str(e)}")
    
    def _generate_with_claude(self, prompt: str) -> str:
        """Génère avec Anthropic Claude API"""
        try:
            from anthropic import Anthropic
            
            if not self.api_key:
                raise Exception(
                    "Clé API Anthropic manquante. "
                    "Ajoutez ANTHROPIC_API_KEY dans votre fichier .env ou variables d'environnement"
                )
            
            print_info(f"Génération avec Claude (modèle: {self.model})...")
            
            client = Anthropic(api_key=self.api_key)
            
            response = client.messages.create(
                model=self.model,
                max_tokens=1000,
                temperature=0.7,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            letter = response.content[0].text.strip()
            print_success("Lettre générée avec Claude")
            return letter
            
        except ImportError:
            raise Exception("Le package 'anthropic' est requis. Installez-le avec: pip install anthropic")
        except Exception as e:
            raise Exception(f"Erreur avec Claude: {str(e)}")
    
    def _generate_fallback_letter(self, job: Dict[str, Any], personal_info: Dict[str, Any]) -> str:
        """Génère une lettre basique en cas d'échec du LLM"""
        print_warning("Utilisation d'un template de secours")
        
        name = personal_info.get('name', '')
        email = personal_info.get('email', '')
        phone = personal_info.get('phone', '')
        address = personal_info.get('address', '')
        
        contact_info = f"{email}\n"
        if phone:
            contact_info += f"Tél: {phone}\n"
        if address:
            contact_info += address
        
        return f"""Bonjour,

Je me permets de vous adresser ma candidature pour le poste de {job.get('title', 'ce poste')} au sein de {job.get('company', 'votre entreprise')}.

{personal_info.get('intro', 'Passionné par la data et l\'analyse, je suis convaincu que mon profil correspond à vos attentes.')}

Mon parcours m'a permis de développer des compétences solides en {', '.join(personal_info.get('skills', [])[:3])}, ce qui correspond aux exigences de votre offre.

{personal_info.get('experience', 'J\'ai une expérience significative dans le domaine de la data.')}

Je serais ravi de pouvoir discuter avec vous de la manière dont mon profil pourrait contribuer à vos projets.

Dans l'attente de votre retour, je vous prie d'agréer mes salutations distinguées.

{name}
{contact_info}"""


