"""
Module d'analyse des compétences demandées dans les offres d'emploi
"""
import re
from collections import Counter
import config
from utils import save_json, print_success, print_info

class SkillsAnalyzer:
    def __init__(self):
        self.skills_counter = Counter()
        self.jobs_analyzed = 0
        
    def analyze_jobs(self, jobs):
        """Analyse les compétences demandées dans une liste d'offres"""
        print_info(f"Analyse de {len(jobs)} offres d'emploi...")
        
        self.skills_counter = Counter()
        self.jobs_analyzed = len(jobs)
        
        for job in jobs:
            self._extract_skills_from_job(job)
        
        print_success(f"Analyse terminée : {len(self.skills_counter)} compétences identifiées")
        return dict(self.skills_counter)
    
    def _extract_skills_from_job(self, job):
        """Extrait les compétences d'une offre d'emploi"""
        # Combiner titre, description et critères
        text = " ".join([
            job.get('title', ''),
            job.get('description', ''),
            job.get('full_description', ''),
            " ".join(job.get('criteria', []))
        ]).lower()
        
        # Rechercher les compétences techniques
        for skill in config.TECHNICAL_SKILLS:
            # Recherche insensible à la casse avec variations
            patterns = [
                rf'\b{re.escape(skill.lower())}\b',
                rf'\b{re.escape(skill.lower().replace(" ", "-"))}\b',
                rf'\b{re.escape(skill.lower().replace(" ", "_"))}\b'
            ]
            
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    self.skills_counter[skill] += 1
                    break
        
        # Rechercher des compétences additionnelles communes
        additional_skills = {
            'statistics': ['statistique', 'statistiques', 'statistical'],
            'data visualization': ['visualisation', 'visualization', 'dashboard'],
            'etl': ['etl', 'extract transform load'],
            'nlp': ['nlp', 'natural language processing', 'traitement du langage'],
            'computer vision': ['computer vision', 'vision par ordinateur', 'opencv'],
            'time series': ['time series', 'séries temporelles', 'forecasting'],
            'a/b testing': ['a/b testing', 'ab testing', 'test ab'],
            'agile': ['agile', 'scrum', 'kanban'],
            'jupyter': ['jupyter', 'notebook'],
            'matplotlib': ['matplotlib', 'seaborn', 'plotly'],
            'excel': ['excel', 'vba', 'pivot table'],
            'nosql': ['nosql', 'mongodb', 'cassandra', 'redis'],
            'postgresql': ['postgresql', 'postgres'],
            'mysql': ['mysql', 'mariadb'],
            'elasticsearch': ['elasticsearch', 'elastic search'],
            'airflow': ['airflow', 'apache airflow'],
            'dbt': ['dbt', 'data build tool'],
            'snowflake': ['snowflake'],
            'databricks': ['databricks'],
            'mlflow': ['mlflow', 'ml flow'],
            'kubernetes': ['kubernetes', 'k8s'],
            'terraform': ['terraform'],
            'jenkins': ['jenkins', 'ci/cd'],
            'github': ['github', 'gitlab', 'bitbucket']
        }
        
        for skill_name, keywords in additional_skills.items():
            for keyword in keywords:
                if keyword.lower() in text:
                    self.skills_counter[skill_name.title()] += 1
                    break
    
    def get_top_skills(self, n=20):
        """Retourne les N compétences les plus demandées"""
        return dict(self.skills_counter.most_common(n))
    
    def get_skills_gap(self, your_skills):
        """Identifie les compétences manquantes par rapport à vos compétences"""
        top_skills = self.get_top_skills(30)
        your_skills_lower = [s.lower() for s in your_skills]
        
        missing_skills = {}
        for skill, count in top_skills.items():
            if skill.lower() not in your_skills_lower:
                missing_skills[skill] = count
        
        return missing_skills
    
    def generate_report(self, output_file=None):
        """Génère un rapport d'analyse"""
        output_file = output_file or config.SKILLS_FILE
        
        report = {
            'jobs_analyzed': self.jobs_analyzed,
            'total_skills_found': len(self.skills_counter),
            'top_skills': self.get_top_skills(30),
            'skills_gap': self.get_skills_gap(config.YOUR_SKILLS),
            'all_skills': dict(self.skills_counter)
        }
        
        save_json(report, output_file)
        print_success(f"Rapport sauvegardé dans {output_file}")
        
        return report
    
    def get_statistics(self):
        """Retourne des statistiques sur l'analyse"""
        if not self.skills_counter:
            return {}
        
        total_mentions = sum(self.skills_counter.values())
        avg_mentions_per_job = total_mentions / self.jobs_analyzed if self.jobs_analyzed > 0 else 0
        
        return {
            'total_jobs': self.jobs_analyzed,
            'total_skills': len(self.skills_counter),
            'total_mentions': total_mentions,
            'avg_mentions_per_job': round(avg_mentions_per_job, 2),
            'most_demanded': self.skills_counter.most_common(1)[0] if self.skills_counter else None
        }


