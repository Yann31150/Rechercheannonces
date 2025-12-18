"""
Application Streamlit pour gérer les candidatures automatiques
"""
import streamlit as st
import json
import os
from datetime import datetime
from application_manager import ApplicationManager
from cover_letter_generator import CoverLetterGenerator
from utils import load_json
import config

st.set_page_config(
    page_title="📝 Candidatures Automatiques",
    page_icon="📝",
    layout="wide"
)

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

def main():
    st.markdown('<div class="main-header">📝 Gestion des Candidatures Automatiques</div>', unsafe_allow_html=True)
    
    manager = ApplicationManager()
    personal_info = load_personal_info()
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        st.subheader("📋 Informations personnelles")
        if st.button("✏️ Modifier mes infos"):
            st.session_state['edit_personal'] = True
        
        st.subheader("📊 Statistiques")
        stats = manager.get_statistics()
        st.metric("Total candidatures", stats['total'])
        st.metric("Préparées", stats['prepared'])
        st.metric("Envoyées", stats['sent'])
        st.metric("Acceptées", stats.get('accepted', 0))
    
    # Onglets
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Préparer candidatures", "📤 Candidatures préparées", "📊 Suivi", "⚙️ Configuration"])
    
    with tab1:
        st.header("📋 Préparer des candidatures")
        
        # Charger les offres
        jobs = load_json(config.JOBS_FILE) if os.path.exists(config.JOBS_FILE) else []
        
        if not jobs:
            st.warning("⚠️ Aucune offre disponible. Lancez d'abord une recherche.")
        else:
            # Filtres
            col1, col2 = st.columns(2)
            with col1:
                search_term = st.text_input("🔍 Rechercher dans les titres", "")
            with col2:
                status_filter = st.selectbox("Filtrer par statut", ["Toutes", "Non candidatées", "Déjà candidatées"])
            
            # Filtrer les offres
            filtered_jobs = jobs
            if search_term:
                filtered_jobs = [j for j in filtered_jobs if search_term.lower() in j.get('title', '').lower()]
            
            # Filtrer par statut de candidature
            if status_filter == "Non candidatées":
                filtered_jobs = [j for j in filtered_jobs if not manager.has_applied(j.get('url', ''))]
            elif status_filter == "Déjà candidatées":
                filtered_jobs = [j for j in filtered_jobs if manager.has_applied(j.get('url', ''))]
            
            st.info(f"📊 {len(filtered_jobs)} offre(s) trouvée(s)")
            
            # Afficher les offres avec bouton de candidature
            for idx, job in enumerate(filtered_jobs[:20]):  # Limiter à 20 pour l'affichage
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
                        # Récupérer les détails de la candidature
                        applications = manager.get_applications_by_status()
                        app = next((a for a in applications if a.get('job_url') == job.get('url')), None)
                        if app:
                            status = app.get('status', 'prepared')
                            status_emoji = {
                                'prepared': '📝',
                                'sent': '📤',
                                'accepted': '✅',
                                'rejected': '❌'
                            }.get(status, '📋')
                            st.success(f"{status_emoji} **Candidature {status}**")
                            if app.get('sent_at'):
                                st.caption(f"Envoyée le: {app.get('sent_at')}")
                
                with col2:
                    if not manager.has_applied(job.get('url', '')):
                        # Utiliser l'index pour rendre la clé unique
                        unique_key = f"apply_{idx}_{hash(job.get('url', str(idx)))}"
                        if st.button("📝 Préparer candidature", key=unique_key):
                            with st.spinner("Génération de la lettre de motivation..."):
                                application = manager.prepare_application(job, personal_info)
                                if application:
                                    st.success("✅ Candidature préparée !")
                                    st.rerun()
                    else:
                        # Afficher le lien vers l'offre même si déjà candidaté
                        if job.get('url'):
                            st.link_button("🔗 Voir l'offre", job.get('url'))
                
                st.divider()
    
    with tab2:
        st.header("📤 Candidatures préparées")
        
        applications = manager.get_applications_by_status('prepared')
        
        if not applications:
            st.info("Aucune candidature préparée pour le moment.")
        else:
            st.info(f"📊 {len(applications)} candidature(s) prête(s) à être envoyée(s)")
            
            for idx, app in enumerate(applications):
                # Créer une clé unique basée sur l'index et l'URL
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
                            
                            # Bouton pour mode assisté (LinkedIn uniquement)
                            if 'linkedin' in app.get('job_url', '').lower():
                                if st.button("🤖 Mode assisté (prérempli)", key=f"assist_{app_key}"):
                                    st.info("⚠️ Le mode assisté ouvrira le navigateur et préremplira le formulaire. Vous devrez valider manuellement.")
                                    st.code(f"python send_applications.py --mode assist --job-url '{app.get('job_url')}'")
                        
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
                        st.divider()
                        if st.button("🗑️ Supprimer cette candidature", key=f"delete_{app_key}", type="secondary"):
                            if manager.delete_application(app.get('job_url')):
                                st.success("✅ Candidature supprimée")
                                st.rerun()
                            else:
                                st.error("❌ Erreur lors de la suppression")
            
            # Bouton pour créer une page HTML avec tous les liens
            st.divider()
            if st.button("🌐 Créer page HTML avec tous les liens"):
                from auto_applicant import AutoApplicant
                import json
                
                personal_info = {}
                if os.path.exists("personal_info.json"):
                    personal_info = json.load(open("personal_info.json"))
                
                jobs = load_json(config.JOBS_FILE) if os.path.exists(config.JOBS_FILE) else []
                prepared_apps = manager.get_applications_by_status('prepared')
                prepared_urls = {app.get('job_url') for app in prepared_apps}
                jobs_to_apply = [j for j in jobs if j.get('url') in prepared_urls]
                
                if jobs_to_apply:
                    applicant = AutoApplicant()
                    html_file = applicant.prepare_application_links(
                        jobs_to_apply,
                        cv_path=personal_info.get('cv_path')
                    )
                    st.success(f"✅ Page HTML créée: {html_file}")
                    st.info("Ouvrez ce fichier dans votre navigateur pour accéder rapidement à toutes les candidatures")
                else:
                    st.warning("Aucune candidature préparée")
    
    with tab3:
        st.header("📊 Suivi complet de vos candidatures")
        
        stats = manager.get_statistics()
        
        # Statistiques en haut
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📋 Total", stats['total'])
        with col2:
            st.metric("📝 Préparées", stats['prepared'])
        with col3:
            st.metric("📤 Envoyées", stats['sent'])
        with col4:
            st.metric("✅ Acceptées", stats.get('accepted', 0))
        
        # Filtres pour le suivi
        st.subheader("🔍 Filtres")
        col1, col2 = st.columns(2)
        with col1:
            status_filter = st.selectbox(
                "Filtrer par statut",
                ["Toutes", "Préparées", "Envoyées", "Acceptées", "Refusées"],
                key="status_filter"
            )
        with col2:
            company_filter = st.text_input("🔍 Rechercher par entreprise", key="company_filter")
        
        # Liste complète de toutes les candidatures
        all_apps = manager.get_applications_by_status()
        
        # Appliquer les filtres
        filtered_apps = all_apps
        if status_filter != "Toutes":
            status_map = {
                "Préparées": "prepared",
                "Envoyées": "sent",
                "Acceptées": "accepted",
                "Refusées": "rejected"
            }
            filtered_apps = [a for a in filtered_apps if a.get('status') == status_map.get(status_filter)]
        
        if company_filter:
            filtered_apps = [a for a in filtered_apps if company_filter.lower() in a.get('company', '').lower()]
        
        if filtered_apps:
            st.subheader(f"📋 Liste des candidatures ({len(filtered_apps)}/{len(all_apps)})")
            
            for idx, app in enumerate(filtered_apps):
                status = app.get('status', 'prepared')
                status_emoji = {
                    'prepared': '📝',
                    'sent': '📤',
                    'accepted': '✅',
                    'rejected': '❌'
                }.get(status, '📋')
                
                status_names = {
                    'prepared': 'Préparée',
                    'sent': 'Envoyée',
                    'accepted': 'Acceptée',
                    'rejected': 'Refusée'
                }
                
                with st.expander(
                    f"{status_emoji} **{app.get('company', 'N/A')}** - {app.get('job_title', 'N/A')} ({status_names.get(status, status)})",
                    expanded=(status == 'sent' or status == 'accepted')
                ):
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
                        
                        notes = st.text_area(
                            "📝 Notes (suivi, entretien, etc.)",
                            value=st.session_state[notes_key],
                            key=notes_key,
                            height=100
                        )
                        
                        # Bouton pour sauvegarder les notes
                        if st.button("💾 Sauvegarder notes", key=f"save_notes_{idx}"):
                            manager.update_notes(app.get('job_url'), notes)
                            st.session_state[notes_key] = notes
                            st.success("✅ Notes sauvegardées")
                            st.rerun()
                    
                    with col2:
                        if app.get('job_url'):
                            st.link_button("🔗 Voir l'offre", app.get('job_url'))
                        
                        # Changer le statut
                        new_status = st.selectbox(
                            "Changer le statut",
                            ["prepared", "sent", "accepted", "rejected"],
                            index=["prepared", "sent", "accepted", "rejected"].index(status) if status in ["prepared", "sent", "accepted", "rejected"] else 0,
                            key=f"status_{idx}"
                        )
                        
                        if new_status != status:
                            if st.button("💾 Mettre à jour", key=f"update_{idx}"):
                                for a in manager.applications:
                                    if a.get('job_url') == app.get('job_url'):
                                        a['status'] = new_status
                                        if new_status == 'sent' and not a.get('sent_at'):
                                            from datetime import datetime
                                            a['sent_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                        manager._save_applications()
                                        st.success("✅ Statut mis à jour")
                                        st.rerun()
                        
                        # Voir la lettre
                        if os.path.exists(app.get('cover_letter_path', '')):
                            with open(app.get('cover_letter_path', ''), 'r', encoding='utf-8') as f:
                                letter_content = f.read()
                                st.download_button(
                                    "📥 Télécharger lettre",
                                    letter_content,
                                    file_name=f"lettre_{app.get('company', 'entreprise')}_{app.get('job_title', 'offre')[:20].replace(' ', '_')}.txt",
                                    mime="text/plain",
                                    key=f"download_{idx}"
                                )
        else:
            st.info("Aucune candidature trouvée avec ces filtres.")
    
    with tab4:
        st.header("⚙️ Configuration")
        
        st.subheader("📋 Informations personnelles")
        
        # Formulaire pour modifier les infos
        with st.form("personal_info_form"):
            name = st.text_input("Nom complet", value=personal_info.get('name', ''))
            email = st.text_input("Email", value=personal_info.get('email', ''))
            intro = st.text_area("Introduction personnelle", value=personal_info.get('intro', ''), height=100)
            experience = st.text_area("Expérience pertinente", value=personal_info.get('experience', ''), height=100)
            cv_path = st.text_input("Chemin vers votre CV (PDF)", value=personal_info.get('cv_path', ''))
            
            if st.form_submit_button("💾 Sauvegarder"):
                personal_info = {
                    "name": name,
                    "email": email,
                    "intro": intro,
                    "experience": experience,
                    "cv_path": cv_path,
                    "skills": personal_info.get('skills', config.YOUR_SKILLS)
                }
                
                with open("personal_info.json", 'w', encoding='utf-8') as f:
                    json.dump(personal_info, f, ensure_ascii=False, indent=2)
                
                st.success("✅ Informations sauvegardées !")

if __name__ == "__main__":
    main()

