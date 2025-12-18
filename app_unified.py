"""
Application Streamlit unifiée : Recherche d'emploi + Candidatures
Tout en un seul endroit !
"""
import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from utils import load_json, print_info
from application_manager import ApplicationManager
from cover_letter_generator import CoverLetterGenerator
import config

# Configuration de la page
st.set_page_config(
    page_title="🔍 Recherche d'emploi & Candidatures",
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
        margin-bottom: 2rem;
    }
    .job-card {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        background-color: #f9f9f9;
    }
    .stButton>button {
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

def load_jobs_data():
    """Charge les données des offres d'emploi"""
    jobs_file = config.JOBS_FILE
    if os.path.exists(jobs_file):
        jobs = load_json(jobs_file)
        for job in jobs:
            if 'source' not in job:
                job['source'] = 'LinkedIn'
        return jobs
    return []

def load_personal_info():
    """Charge les informations personnelles"""
    if os.path.exists("personal_info.json"):
        return load_json("personal_info.json")
    return {
        "name": config.YOUR_NAME,
        "email": "",
        "intro": "",
        "experience": "",
        "skills": config.YOUR_SKILLS
    }

def parse_date(date_str):
    """Parse une chaîne de date pour le tri"""
    if not date_str or date_str == "N/A" or date_str == "":
        return datetime.min
    
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
            import re
            numbers = re.findall(r'\d+', date_str_clean)
            if numbers:
                days_ago = int(numbers[0])
                return datetime.now() - timedelta(days=days_ago)
        
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
        date_str_clean = date_str.strip()
        
        if 'T' in date_str_clean:
            date_obj = datetime.fromisoformat(date_str_clean.replace('Z', '+00:00').split('T')[0])
            return f"📅 {date_obj.strftime('%d/%m/%Y')}"
        
        if len(date_str_clean) == 10 and date_str_clean.count('-') == 2:
            date_obj = datetime.strptime(date_str_clean, '%Y-%m-%d')
            return f"📅 {date_obj.strftime('%d/%m/%Y')}"
        
        if any(word in date_str_clean.lower() for word in ['il y a', 'ago', 'jour', 'day', 'semaine', 'week']):
            return f"📅 {date_str_clean}"
        
        return f"📅 {date_str_clean}"
    except:
        return f"📅 {date_str}"

def main():
    # En-tête
    st.markdown('<div class="main-header">🔍 Recherche d\'emploi & Candidatures</div>', unsafe_allow_html=True)
    
    # Initialiser le gestionnaire de candidatures
    manager = ApplicationManager()
    personal_info = load_personal_info()
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Navigation")
        
        # Statistiques globales
        st.subheader("📊 Vue d'ensemble")
        jobs = load_jobs_data()
        stats = manager.get_statistics()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("📋 Offres", len(jobs))
        with col2:
            st.metric("📝 Candidatures", stats['total'])
        
        if jobs:
            companies = [j.get('company', 'N/A') for j in jobs if j.get('company') != 'N/A']
            if companies:
                st.metric("🏢 Entreprises", len(set(companies)))
        
        st.divider()
        
        # Actions rapides
        st.subheader("🚀 Actions rapides")
        if st.button("🔄 Actualiser les données"):
            st.rerun()
        
        st.info("💡 Pour lancer une nouvelle recherche, utilisez l'icône 🔍 sur le bureau")
        
        st.divider()
        
        # Statistiques candidatures
        st.subheader("📊 Mes candidatures")
        st.metric("Préparées", stats['prepared'])
        st.metric("Envoyées", stats['sent'])
        st.metric("Acceptées", stats.get('accepted', 0))
    
    # Onglets principaux
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📋 Offres d'emploi", 
        "📝 Préparer candidatures", 
        "📤 Candidatures préparées",
        "📊 Suivi complet",
        "📈 Statistiques",
        "⚙️ Configuration"
    ])
    
    # ========== ONGLET 1: LISTE DES OFFRES ==========
    with tab1:
        st.header("📋 Liste des offres d'emploi")
        
        jobs = load_jobs_data()
        
        if not jobs:
            st.warning("⚠️ Aucune offre d'emploi trouvée. Lancez d'abord une recherche avec le script.")
            st.info("💡 Utilisez le script `🔍 Recherche d'emploi.command` sur le bureau")
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
                sources = [j.get('source', 'LinkedIn') for j in jobs]
                unique_sources = ['Toutes'] + sorted(list(set(sources)))
                selected_source = st.selectbox("🌐 Source", unique_sources)
            
            col4, col5 = st.columns(2)
            with col4:
                locations = [j.get('location', 'N/A') for j in jobs if j.get('location') != 'N/A']
                unique_locations = ['Toutes'] + sorted(list(set(locations)))
                selected_location = st.selectbox("📍 Localisation", unique_locations)
            
            with col5:
                status_filter = st.selectbox("📝 Statut candidature", ["Toutes", "Non candidatées", "Déjà candidatées"])
            
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
            
            # Filtrer par statut de candidature
            if status_filter == "Non candidatées":
                filtered_jobs = [j for j in filtered_jobs if not manager.has_applied(j.get('url', ''))]
            elif status_filter == "Déjà candidatées":
                filtered_jobs = [j for j in filtered_jobs if manager.has_applied(j.get('url', ''))]
            
            # Trier par date (plus récent en premier)
            filtered_jobs.sort(key=lambda x: parse_date(x.get('date', 'N/A')), reverse=True)
            
            st.info(f"📊 {len(filtered_jobs)} offre(s) trouvée(s) sur {len(jobs)} total (triées par date)")
            
            # Afficher les offres
            for idx, job in enumerate(filtered_jobs[:50]):  # Limiter à 50 pour les performances
                title = job.get('title', 'N/A')
                company = job.get('company', 'Non spécifiée')
                location = job.get('location', 'Non spécifiée')
                date_display = format_date(job.get('date', 'N/A'))
                source = job.get('source', 'LinkedIn')
                source_emoji = {
                    'LinkedIn': '💼', 'Welcome to the Jungle': '🌴', 'Indeed': '🔍',
                    'APEC': '📋', 'Helloworks': '👋', 'Free-Work': '💻',
                    'La Bonne Alternance': '🎓'
                }.get(source, '🌐')
                
                # Vérifier si déjà candidaté
                has_applied = manager.has_applied(job.get('url', ''))
                status_badge = "✅ Déjà candidaté" if has_applied else "📝 Non candidaté"
                
                expander_title = f"{source_emoji} {title} | 🏢 {company} | 📍 {location} | {date_display} | {status_badge}"
                
                with st.expander(expander_title, expanded=False):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"**Source:** {source}")
                        st.markdown(f"**Entreprise:** {company}")
                        st.markdown(f"**Localisation:** {location}")
                        st.markdown(f"**Date de publication:** {date_display}")
                        
                        if job.get('description'):
                            st.markdown("**📝 Description:**")
                            st.text(job.get('description', '')[:500] + "...")
                    
                    with col2:
                        if job.get('url'):
                            st.link_button("🔗 Voir l'offre", job.get('url'))
                        
                        if not has_applied:
                            if st.button("📝 Préparer candidature", key=f"quick_apply_{idx}"):
                                with st.spinner("Génération de la lettre de motivation..."):
                                    application = manager.prepare_application(job, personal_info)
                                    if application:
                                        st.success("✅ Candidature préparée !")
                                        st.rerun()
                        
                        st.caption(f"Scrapé le: {job.get('scraped_at', 'N/A')}")
            
            # Boutons de téléchargement
            st.divider()
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📥 Télécharger CSV"):
                    df = pd.DataFrame(filtered_jobs)
                    csv = df.to_csv(index=False)
                    st.download_button("Télécharger", csv, "offres_emploi.csv", "text/csv")
            with col2:
                if st.button("📥 Télécharger Excel"):
                    df = pd.DataFrame(filtered_jobs)
                    excel = df.to_excel(index=False, engine='openpyxl')
                    st.download_button("Télécharger", excel, "offres_emploi.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    
    # ========== ONGLET 2: PRÉPARER CANDIDATURES ==========
    with tab2:
        st.header("📝 Préparer des candidatures")
        
        jobs = load_jobs_data()
        
        if not jobs:
            st.warning("⚠️ Aucune offre disponible. Lancez d'abord une recherche.")
        else:
            # Filtres
            col1, col2 = st.columns(2)
            with col1:
                search_term = st.text_input("🔍 Rechercher dans les titres", key="prep_search")
            with col2:
                status_filter = st.selectbox("Filtrer par statut", ["Toutes", "Non candidatées", "Déjà candidatées"], key="prep_status")
            
            # Filtrer les offres
            filtered_jobs = jobs
            if search_term:
                filtered_jobs = [j for j in filtered_jobs if search_term.lower() in j.get('title', '').lower()]
            
            if status_filter == "Non candidatées":
                filtered_jobs = [j for j in filtered_jobs if not manager.has_applied(j.get('url', ''))]
            elif status_filter == "Déjà candidatées":
                filtered_jobs = [j for j in filtered_jobs if manager.has_applied(j.get('url', ''))]
            
            st.info(f"📊 {len(filtered_jobs)} offre(s) trouvée(s)")
            
            # Afficher les offres avec bouton de candidature
            for idx, job in enumerate(filtered_jobs[:20]):
                title = job.get('title', 'N/A')
                company = job.get('company', 'N/A')
                location = job.get('location', 'N/A')
                source = job.get('source', 'LinkedIn')
                
                # Afficher l'entreprise de manière plus visible
                if company != 'N/A' and company:
                    st.markdown(f"### 🏢 {company}")
                else:
                    st.markdown(f"### 🏢 Entreprise non spécifiée")
                
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    st.markdown(f"**💼 Poste:** {title}")
                    if location != 'N/A' and location:
                        st.caption(f"📍 {location} | 🌐 {source}")
                    
                    # Afficher le statut de candidature
                    if manager.has_applied(job.get('url', '')):
                        applications = manager.get_applications_by_status()
                        app = next((a for a in applications if a.get('job_url') == job.get('url')), None)
                        if app:
                            status = app.get('status', 'prepared')
                            status_emoji = {'prepared': '📝', 'sent': '📤', 'accepted': '✅', 'rejected': '❌'}.get(status, '📋')
                            st.success(f"{status_emoji} **Candidature {status}**")
                            if app.get('sent_at'):
                                st.caption(f"Envoyée le: {app.get('sent_at')}")
                
                with col2:
                    if not manager.has_applied(job.get('url', '')):
                        unique_key = f"apply_{idx}_{hash(job.get('url', str(idx)))}"
                        if st.button("📝 Préparer candidature", key=unique_key):
                            with st.spinner("Génération de la lettre de motivation avec LLM..."):
                                application = manager.prepare_application(job, personal_info)
                                if application:
                                    st.success("✅ Candidature préparée !")
                                    st.rerun()
                    else:
                        if job.get('url'):
                            st.link_button("🔗 Voir l'offre", job.get('url'))
                
                st.divider()
    
    # ========== ONGLET 3: CANDIDATURES PRÉPARÉES ==========
    with tab3:
        st.header("📤 Candidatures préparées")
        
        applications = manager.get_applications_by_status('prepared')
        
        if not applications:
            st.info("Aucune candidature préparée pour le moment.")
        else:
            st.info(f"📊 {len(applications)} candidature(s) prête(s) à être envoyée(s)")
            
            for idx, app in enumerate(applications):
                app_key = f"app_{idx}_{hash(app.get('job_url', str(idx)))}"
                
                with st.expander(f"📝 {app.get('job_title', 'N/A')} - {app.get('company', 'N/A')}", expanded=False):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"**Entreprise:** {app.get('company', 'N/A')}")
                        st.markdown(f"**Localisation:** {app.get('location', 'N/A')}")
                        st.markdown(f"**Source:** {app.get('source', 'N/A')}")
                        st.markdown(f"**Préparée le:** {app.get('prepared_at', 'N/A')}")
                        
                        # Afficher la lettre
                        if os.path.exists(app.get('cover_letter_path', '')):
                            with open(app.get('cover_letter_path', ''), 'r', encoding='utf-8') as f:
                                letter = f.read()
                            st.text_area("Lettre de motivation", letter, height=200, key=f"letter_{app_key}")
                    
                    with col2:
                        if app.get('job_url'):
                            st.link_button("🔗 Voir l'offre et postuler", app.get('job_url'))
                        
                        if st.button("✅ Marquer comme envoyée", key=f"sent_{app_key}"):
                            manager.mark_as_sent(app.get('job_url'))
                            st.success("✅ Marquée comme envoyée")
                            st.rerun()
                        
                        if st.button("📥 Télécharger lettre", key=f"dl_{app_key}"):
                            if os.path.exists(app.get('cover_letter_path', '')):
                                with open(app.get('cover_letter_path', ''), 'r', encoding='utf-8') as f:
                                    letter_content = f.read()
                                    st.download_button(
                                        "Télécharger",
                                        letter_content,
                                        file_name=f"lettre_{app.get('job_title', 'offre')[:30].replace(' ', '_')}.txt",
                                        mime="text/plain",
                                        key=f"download_{app_key}"
                                    )
                        
                        # Bouton pour supprimer/annuler la candidature
                        if st.button("🗑️ Supprimer cette candidature", key=f"delete_{app_key}", type="secondary"):
                            if manager.delete_application(app.get('job_url')):
                                st.success("✅ Candidature supprimée")
                                st.rerun()
                            else:
                                st.error("❌ Erreur lors de la suppression")
    
    # ========== ONGLET 4: SUIVI COMPLET ==========
    with tab4:
        st.header("📊 Suivi complet de vos candidatures")
        
        stats = manager.get_statistics()
        
        # Statistiques
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📋 Total", stats['total'])
        with col2:
            st.metric("📝 Préparées", stats['prepared'])
        with col3:
            st.metric("📤 Envoyées", stats['sent'])
        with col4:
            st.metric("✅ Acceptées", stats.get('accepted', 0))
        
        # Filtres
        st.subheader("🔍 Filtres")
        col1, col2 = st.columns(2)
        with col1:
            status_filter = st.selectbox("Filtrer par statut", ["Toutes", "Préparées", "Envoyées", "Acceptées", "Refusées"], key="status_filter")
        with col2:
            company_filter = st.text_input("🔍 Rechercher par entreprise", key="company_filter")
        
        # Liste complète
        all_apps = manager.get_applications_by_status()
        
        # Appliquer les filtres
        filtered_apps = all_apps
        if status_filter != "Toutes":
            status_map = {"Préparées": "prepared", "Envoyées": "sent", "Acceptées": "accepted", "Refusées": "rejected"}
            filtered_apps = [a for a in filtered_apps if a.get('status') == status_map.get(status_filter)]
        
        if company_filter:
            filtered_apps = [a for a in filtered_apps if company_filter.lower() in a.get('company', '').lower()]
        
        if filtered_apps:
            st.subheader(f"📋 Liste des candidatures ({len(filtered_apps)}/{len(all_apps)})")
            
            for idx, app in enumerate(filtered_apps):
                status = app.get('status', 'prepared')
                status_emoji = {'prepared': '📝', 'sent': '📤', 'accepted': '✅', 'rejected': '❌'}.get(status, '📋')
                status_names = {'prepared': 'Préparée', 'sent': 'Envoyée', 'accepted': 'Acceptée', 'rejected': 'Refusée'}
                
                with st.expander(f"{status_emoji} **{app.get('company', 'N/A')}** - {app.get('job_title', 'N/A')} ({status_names.get(status, status)})", expanded=(status == 'sent' or status == 'accepted')):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"**🏢 Entreprise:** {app.get('company', 'N/A')}")
                        st.markdown(f"**💼 Poste:** {app.get('job_title', 'N/A')}")
                        st.markdown(f"**📍 Localisation:** {app.get('location', 'N/A')}")
                        st.markdown(f"**🌐 Source:** {app.get('source', 'N/A')}")
                        st.markdown(f"**📅 Préparée le:** {app.get('prepared_at', 'N/A')}")
                        
                        if app.get('sent_at'):
                            st.markdown(f"**📤 Envoyée le:** {app.get('sent_at')}")
                        
                        # Notes
                        notes_key = f"notes_{idx}"
                        if notes_key not in st.session_state:
                            st.session_state[notes_key] = app.get('notes', '')
                        
                        notes = st.text_area("📝 Notes (suivi, entretien, etc.)", value=st.session_state[notes_key], key=notes_key, height=100)
                        
                        if st.button("💾 Sauvegarder notes", key=f"save_notes_{idx}"):
                            manager.update_notes(app.get('job_url'), notes)
                            st.session_state[notes_key] = notes
                            st.success("✅ Notes sauvegardées")
                            st.rerun()
                    
                    with col2:
                        if app.get('job_url'):
                            st.link_button("🔗 Voir l'offre", app.get('job_url'))
                        
                        # Changer le statut
                        new_status = st.selectbox("Changer le statut", ["prepared", "sent", "accepted", "rejected"], index=["prepared", "sent", "accepted", "rejected"].index(status) if status in ["prepared", "sent", "accepted", "rejected"] else 0, key=f"status_{idx}")
                        
                        if new_status != status:
                            if st.button("💾 Mettre à jour", key=f"update_{idx}"):
                                manager.update_application_status(app.get('job_url'), new_status)
                                st.success("✅ Statut mis à jour")
                                st.rerun()
                        
                        # Voir la lettre
                        if os.path.exists(app.get('cover_letter_path', '')):
                            with open(app.get('cover_letter_path', ''), 'r', encoding='utf-8') as f:
                                letter_content = f.read()
                                st.download_button("📥 Télécharger lettre", letter_content, file_name=f"lettre_{app.get('company', 'entreprise')}_{app.get('job_title', 'offre')[:20].replace(' ', '_')}.txt", mime="text/plain", key=f"download_{idx}")
                        
                        # Bouton pour supprimer/annuler la candidature
                        st.divider()
                        if st.button("🗑️ Supprimer cette candidature", key=f"delete_tracking_{idx}", type="secondary"):
                            if manager.delete_application(app.get('job_url')):
                                st.success("✅ Candidature supprimée")
                                st.rerun()
                            else:
                                st.error("❌ Erreur lors de la suppression")
        else:
            st.info("Aucune candidature trouvée avec ces filtres.")
    
    # ========== ONGLET 5: STATISTIQUES ==========
    with tab5:
        st.header("📈 Statistiques et analyses")
        
        jobs = load_jobs_data()
        
        if not jobs:
            st.warning("Aucune donnée disponible")
        else:
            # Statistiques générales
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total offres", len(jobs))
            with col2:
                companies = [j.get('company', 'N/A') for j in jobs if j.get('company') != 'N/A']
                st.metric("Entreprises", len(set(companies)))
            with col3:
                sources = [j.get('source', 'LinkedIn') for j in jobs]
                st.metric("Sources", len(set(sources)))
            with col4:
                locations = [j.get('location', 'N/A') for j in jobs if j.get('location') != 'N/A']
                st.metric("Localisations", len(set(locations)))
            
            st.divider()
            
            # Graphiques
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📊 Répartition par source")
                source_counts = pd.Series([j.get('source', 'LinkedIn') for j in jobs]).value_counts()
                fig = px.pie(values=source_counts.values, names=source_counts.index, title="Offres par site")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("🏢 Top entreprises")
                company_counts = pd.Series([j.get('company', 'N/A') for j in jobs if j.get('company') != 'N/A']).value_counts().head(10)
                fig = px.bar(x=company_counts.values, y=company_counts.index, orientation='h', title="Top 10 entreprises")
                st.plotly_chart(fig, use_container_width=True)
            
            # Statistiques candidatures
            st.divider()
            st.subheader("📝 Statistiques candidatures")
            stats = manager.get_statistics()
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total", stats['total'])
            with col2:
                st.metric("Préparées", stats['prepared'])
            with col3:
                st.metric("Envoyées", stats['sent'])
            with col4:
                st.metric("Acceptées", stats.get('accepted', 0))
            
            if stats['total'] > 0:
                # Graphique de suivi
                status_counts = pd.Series([app.get('status', 'prepared') for app in manager.get_applications_by_status()]).value_counts()
                fig = px.pie(values=status_counts.values, names=status_counts.index, title="Répartition des candidatures")
                st.plotly_chart(fig, use_container_width=True)
    
    # ========== ONGLET 6: CONFIGURATION ==========
    with tab6:
        st.header("⚙️ Configuration")
        
        st.subheader("📋 Informations personnelles")
        
        with st.form("personal_info_form"):
            name = st.text_input("Nom complet", value=personal_info.get('name', ''))
            email = st.text_input("Email", value=personal_info.get('email', ''))
            phone = st.text_input("Téléphone", value=personal_info.get('phone', ''))
            address = st.text_area("Adresse", value=personal_info.get('address', ''), height=60)
            intro = st.text_area("Introduction personnelle", value=personal_info.get('intro', ''), height=100)
            experience = st.text_area("Expérience pertinente", value=personal_info.get('experience', ''), height=100)
            cv_path = st.text_input("Chemin vers votre CV (PDF)", value=personal_info.get('cv_path', ''))
            
            if st.form_submit_button("💾 Sauvegarder"):
                personal_info = {
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "address": address,
                    "intro": intro,
                    "experience": experience,
                    "cv_path": cv_path,
                    "skills": personal_info.get('skills', config.YOUR_SKILLS)
                }
                
                with open("personal_info.json", 'w', encoding='utf-8') as f:
                    json.dump(personal_info, f, ensure_ascii=False, indent=2)
                
                st.success("✅ Informations sauvegardées !")
                st.rerun()
        
        st.divider()
        
        st.subheader("🔧 Paramètres")
        
        # Vérifier Ollama
        try:
            import requests
            response = requests.get("http://localhost:11434/api/tags", timeout=1)
            if response.status_code == 200:
                st.success("✅ Ollama est actif et prêt")
                models = response.json().get('models', [])
                if models:
                    st.info(f"Modèles disponibles: {', '.join([m.get('name', 'N/A') for m in models])}")
            else:
                st.warning("⚠️ Ollama ne répond pas")
        except:
            st.info("💡 Ollama n'est pas lancé. Les lettres utiliseront les templates.")
            st.info("Pour utiliser Ollama: `brew services start ollama`")

if __name__ == "__main__":
    main()

