"""
Application Streamlit pour visualiser les offres d'emploi LinkedIn
"""
import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from utils import load_json, print_info
import config

# Configuration de la page
st.set_page_config(
    page_title="🔍 Recherche d'emploi Data LinkedIn",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #0A66C2;
        text-align: center;
        padding: 1rem 0;
    }
    .job-card {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        background-color: #f9f9f9;
    }
    .job-title {
        font-size: 1.3rem;
        font-weight: bold;
        color: #0A66C2;
    }
    .job-company {
        color: #666;
        font-size: 1.1rem;
    }
    .job-location {
        color: #888;
    }
    </style>
""", unsafe_allow_html=True)

def load_jobs_data():
    """Charge les données des offres d'emploi"""
    jobs_file = config.JOBS_FILE
    if os.path.exists(jobs_file):
        jobs = load_json(jobs_file)
        # S'assurer que toutes les offres ont un champ 'source'
        for job in jobs:
            if 'source' not in job:
                job['source'] = 'LinkedIn'
        return jobs
    return []

def load_skills_data():
    """Charge les données d'analyse des compétences"""
    skills_file = config.SKILLS_FILE
    if os.path.exists(skills_file):
        return load_json(skills_file)
    return None

def parse_date(date_str):
    """Parse une date et retourne un objet datetime pour le tri"""
    if not date_str or date_str == "N/A" or date_str == "":
        return datetime.min  # Date très ancienne pour trier en dernier
    
    try:
        date_str_clean = date_str.strip()
        
        # Format ISO avec T
        if 'T' in date_str_clean:
            return datetime.fromisoformat(date_str_clean.replace('Z', '+00:00').split('T')[0])
        
        # Format YYYY-MM-DD
        if len(date_str_clean) == 10 and date_str_clean.count('-') == 2:
            return datetime.strptime(date_str_clean, '%Y-%m-%d')
        
        # Format relatif (ex: "Il y a 2 jours")
        if any(word in date_str_clean.lower() for word in ['il y a', 'ago', 'jour', 'day']):
            # Essayer d'extraire le nombre de jours
            import re
            numbers = re.findall(r'\d+', date_str_clean)
            if numbers:
                days_ago = int(numbers[0])
                return datetime.now() - timedelta(days=days_ago)
        
        # Si c'est "Aujourd'hui" ou "Today"
        if any(word in date_str_clean.lower() for word in ['aujourd', 'today', 'maintenant']):
            return datetime.now()
        
        return datetime.min
    except:
        return datetime.min

def format_date(date_str):
    """Formate une date pour l'affichage"""
    if not date_str or date_str == "N/A" or date_str == "":
        return "📅 Date non disponible"
    try:
        # Essayer différents formats
        date_str_clean = date_str.strip()
        
        # Format ISO avec T
        if 'T' in date_str_clean:
            date_obj = datetime.fromisoformat(date_str_clean.replace('Z', '+00:00').split('T')[0])
            return f"📅 {date_obj.strftime('%d/%m/%Y')}"
        
        # Format YYYY-MM-DD
        if len(date_str_clean) == 10 and date_str_clean.count('-') == 2:
            date_obj = datetime.strptime(date_str_clean, '%Y-%m-%d')
            return f"📅 {date_obj.strftime('%d/%m/%Y')}"
        
        # Si c'est déjà formaté (ex: "Il y a 2 jours")
        if any(word in date_str_clean.lower() for word in ['il y a', 'ago', 'jour', 'day', 'semaine', 'week']):
            return f"📅 {date_str_clean}"
        
        return f"📅 {date_str_clean}"
    except:
        return f"📅 {date_str}"

def main():
    # En-tête
    st.markdown('<div class="main-header">🔍 Recherche d\'emploi Data LinkedIn</div>', unsafe_allow_html=True)
    
    # Sidebar pour les actions
    with st.sidebar:
        st.header("⚙️ Actions")
        
        st.subheader("📊 Données")
        if st.button("🔄 Actualiser les données"):
            st.rerun()
        
        st.subheader("🔍 Nouvelle recherche")
        st.info("Utilisez le script de recherche pour ajouter de nouvelles offres")
        
        st.subheader("📈 Statistiques")
        jobs = load_jobs_data()
        if jobs:
            st.metric("Nombre d'offres", len(jobs))
            companies = [j.get('company', 'N/A') for j in jobs if j.get('company') != 'N/A']
            if companies:
                st.metric("Entreprises", len(set(companies)))
        else:
            st.warning("Aucune donnée chargée")
    
    # Onglets principaux
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Liste des offres", "📊 Statistiques", "💼 Compétences", "🔍 Recherche"])
    
    with tab1:
        st.header("📋 Liste des offres d'emploi")
        
        jobs = load_jobs_data()
        
        if not jobs:
            st.warning("⚠️ Aucune offre d'emploi trouvée. Lancez d'abord une recherche avec le script.")
            st.info("💡 Utilisez le script `lancer_recherche.command` ou `python main.py --search ...`")
        else:
            # Filtres
            col1, col2, col3 = st.columns(3)
            
            with col1:
                search_term = st.text_input("🔍 Rechercher dans les titres", "")
            
            with col2:
                companies = [j.get('company', 'N/A') for j in jobs if j.get('company') != 'N/A']
                unique_companies = ['Toutes'] + sorted(list(set(companies)))
                selected_company = st.selectbox("🏢 Entreprise", unique_companies)
            
            with col3:
                # Filtre par source
                sources = [j.get('source', 'LinkedIn') for j in jobs]
                unique_sources = ['Toutes'] + sorted(list(set(sources)))
                selected_source = st.selectbox("🌐 Source", unique_sources)
            
            # Filtre localisation (nouvelle ligne)
            col4, col5 = st.columns(2)
            with col4:
                locations = [j.get('location', 'N/A') for j in jobs if j.get('location') != 'N/A']
                unique_locations = ['Toutes'] + sorted(list(set(locations)))
                selected_location = st.selectbox("📍 Localisation", unique_locations)
            
            # Filtrer les offres
            filtered_jobs = jobs
            if search_term:
                filtered_jobs = [j for j in filtered_jobs if search_term.lower() in j.get('title', '').lower()]
            if selected_company != 'Toutes':
                filtered_jobs = [j for j in filtered_jobs if j.get('company') == selected_company]
            if selected_source != 'Toutes':
                filtered_jobs = [j for j in filtered_jobs if j.get('source', 'LinkedIn') == selected_source]
            if selected_location != 'Toutes':
                filtered_jobs = [j for j in filtered_jobs if j.get('location') == selected_location]
            
            # Trier par date (plus récent en premier)
            filtered_jobs.sort(key=lambda x: parse_date(x.get('date', 'N/A')), reverse=True)
            
            st.info(f"📊 {len(filtered_jobs)} offre(s) trouvée(s) sur {len(jobs)} total (triées par date, plus récentes en premier)")
            
            # Afficher les offres
            for idx, job in enumerate(filtered_jobs, 1):
                # Construire le titre avec entreprise et localisation visibles
                title = job.get('title', 'N/A')
                company = job.get('company', 'N/A')
                location = job.get('location', 'N/A')
                
                # Créer un titre enrichi avec les infos principales
                title_display = f"💼 **{title[:60]}**"
                if company != 'N/A' and company and company.strip():
                    title_display += f" | 🏢 {company}"
                if location != 'N/A' and location and location.strip():
                    title_display += f" | 📍 {location}"
                
                with st.expander(title_display, expanded=False):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        source = job.get('source', 'LinkedIn')
                        source_emoji = {
                            'LinkedIn': '💼',
                            'Welcome to the Jungle': '🌴',
                            'Indeed': '🔍',
                            'APEC': '📋',
                            'Helloworks': '👋',
                            'Free-Work': '💻',
                            'La Bonne Alternance': '🎓',
                            'WeLoveDevs': '❤️',
                            'LesJeudis': '📅',
                            'DataScientest': '📊'
                        }.get(source, '🌐')
                        st.markdown(f"**{source_emoji} Source:** {source}")
                        st.markdown(f"**🏢 Entreprise:** {job.get('company', 'Non spécifiée')}")
                        st.markdown(f"**📍 Localisation:** {job.get('location', 'Non spécifiée')}")
                        # Date de publication mise en avant
                        date_display = format_date(job.get('date', 'N/A'))
                        st.markdown(f"**{date_display}**")
                        if job.get('date') and job.get('date') != 'N/A':
                            st.caption(f"Publiée le: {job.get('date')}")
                        
                        if job.get('description'):
                            st.markdown("**📝 Description:**")
                            st.text(job.get('description', '')[:500] + "...")
                    
                    with col2:
                        if job.get('url'):
                            # Adapter le texte du bouton selon la source
                            button_text = "🔗 Voir l'offre"
                            url_lower = job.get('url', '').lower()
                            if 'linkedin' in url_lower:
                                button_text = "🔗 Voir sur LinkedIn"
                            elif 'welcometothejungle' in url_lower or 'wttj' in url_lower:
                                button_text = "🔗 Voir sur WTTJ"
                            elif 'indeed' in url_lower:
                                button_text = "🔗 Voir sur Indeed"
                            elif 'apec' in url_lower:
                                button_text = "🔗 Voir sur APEC"
                            elif 'free-work' in url_lower or 'freework' in url_lower:
                                button_text = "🔗 Voir sur Free-Work"
                            st.link_button(button_text, job.get('url'))
                        st.caption(f"Scrapé le: {job.get('scraped_at', 'N/A')}")
            
            # Télécharger les données
            st.divider()
            col1, col2, col3 = st.columns(3)
            
            with col1:
                df = pd.DataFrame(filtered_jobs)
                csv = df.to_csv(index=False, encoding='utf-8')
                st.download_button(
                    label="📥 Télécharger CSV",
                    data=csv,
                    file_name=f"offres_linkedin_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            
            with col2:
                json_str = json.dumps(filtered_jobs, ensure_ascii=False, indent=2)
                st.download_button(
                    label="📥 Télécharger JSON",
                    data=json_str,
                    file_name=f"offres_linkedin_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json"
                )
            
            with col3:
                if not df.empty:
                    from io import BytesIO
                    output = BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        df.to_excel(writer, index=False, sheet_name='Offres')
                    excel_data = output.getvalue()
                    st.download_button(
                        label="📥 Télécharger Excel",
                        data=excel_data,
                        file_name=f"offres_linkedin_{datetime.now().strftime('%Y%m%d')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
    
    with tab2:
        st.header("📊 Statistiques")
        
        jobs = load_jobs_data()
        
        if not jobs:
            st.warning("Aucune donnée disponible")
        else:
            df = pd.DataFrame(jobs)
            
            # Graphiques
            col1, col2 = st.columns(2)
            
            with col1:
                # Répartition par source
                sources = df['source'].value_counts() if 'source' in df.columns else pd.Series()
                if not sources.empty:
                    fig = px.pie(
                        values=sources.values,
                        names=sources.index,
                        title="🌐 Répartition par source"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    # Top entreprises si pas de source
                    companies = df[df['company'] != 'N/A']['company'].value_counts().head(10)
                    if not companies.empty:
                        fig = px.bar(
                            x=companies.values,
                            y=companies.index,
                            orientation='h',
                            title="🏢 Top 10 des entreprises",
                            labels={'x': 'Nombre d\'offres', 'y': 'Entreprise'}
                        )
                        fig.update_layout(height=400)
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("Pas de données disponibles")
            
            with col2:
                # Répartition par localisation
                locations = df[df['location'] != 'N/A']['location'].value_counts().head(10)
                if not locations.empty:
                    fig = px.pie(
                        values=locations.values,
                        names=locations.index,
                        title="📍 Répartition par localisation"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Pas de données de localisation disponibles")
            
            # Statistiques générales
            st.subheader("📈 Statistiques générales")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total d'offres", len(jobs))
            
            with col2:
                unique_companies = df[df['company'] != 'N/A']['company'].nunique()
                st.metric("Entreprises", unique_companies)
            
            with col3:
                unique_locations = df[df['location'] != 'N/A']['location'].nunique()
                st.metric("Localisations", unique_locations)
            
            with col4:
                recent_jobs = len([j for j in jobs if j.get('date') != 'N/A'])
                st.metric("Offres datées", recent_jobs)
    
    with tab3:
        st.header("💼 Analyse des compétences")
        
        skills_data = load_skills_data()
        
        if not skills_data:
            st.warning("⚠️ Aucune analyse de compétences disponible.")
            st.info("💡 Lancez d'abord une analyse avec: `python main.py --analyze-skills`")
        else:
            st.subheader("🔥 Top compétences demandées")
            
            top_skills = skills_data.get('top_skills', {})
            if top_skills:
                # Créer un graphique
                skills_df = pd.DataFrame(
                    list(top_skills.items()),
                    columns=['Compétence', 'Occurrences']
                ).sort_values('Occurrences', ascending=False).head(20)
                
                fig = px.bar(
                    skills_df,
                    x='Occurrences',
                    y='Compétence',
                    orientation='h',
                    title="Top 20 des compétences les plus demandées",
                    labels={'Occurrences': 'Nombre d\'occurrences', 'Compétence': 'Compétence'}
                )
                fig.update_layout(height=600)
                st.plotly_chart(fig, use_container_width=True)
                
                # Afficher le tableau
                st.dataframe(skills_df, use_container_width=True)
            else:
                st.info("Pas de données de compétences disponibles")
            
            # Compétences à développer
            st.subheader("📚 Compétences à développer")
            skills_gap = skills_data.get('skills_gap', {})
            if skills_gap:
                gap_df = pd.DataFrame(
                    list(skills_gap.items()),
                    columns=['Compétence', 'Occurrences']
                ).sort_values('Occurrences', ascending=False)
                
                st.dataframe(gap_df, use_container_width=True)
            else:
                st.success("✅ Vous avez toutes les compétences principales !")
            
            # Statistiques
            st.subheader("📊 Statistiques de l'analyse")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Offres analysées", skills_data.get('jobs_analyzed', 0))
            
            with col2:
                st.metric("Compétences identifiées", skills_data.get('total_skills_found', 0))
            
            with col3:
                most_demanded = skills_data.get('top_skills', {})
                if most_demanded:
                    top_skill = max(most_demanded.items(), key=lambda x: x[1])
                    st.metric("Plus demandée", f"{top_skill[0]} ({top_skill[1]}x)")
    
    with tab4:
        st.header("🔍 Lancer une nouvelle recherche")
        
        st.info("💡 Pour lancer une recherche, utilisez le script de ligne de commande ou l'icône sur le bureau.")
        
        st.subheader("📝 Commandes utiles")
        
        st.code("""
# Recherche sur TOUS les sites
python main_unified.py --search "Data Scientist" --location "Toulouse"

# Recherche sur sites spécifiques
python main_unified.py --search "Data Analyst" --sites linkedin indeed wttj

# Recherche LinkedIn uniquement
python main.py --search "Data Scientist" --location "Toulouse"

# Avec export CSV
python main_unified.py --search "Data" --location "Toulouse" --export csv

# Analyser les compétences
python main.py --analyze-skills --skills-gap
        """, language="bash")
        
        st.subheader("🎯 Ou utilisez l'icône sur le bureau")
        st.info("Double-cliquez sur '🔍 Recherche LinkedIn.command' sur votre bureau pour un menu interactif")

if __name__ == "__main__":
    main()

