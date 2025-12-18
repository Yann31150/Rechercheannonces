"""
Module pour envoyer des emails avec les nouvelles annonces
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from datetime import datetime
from utils import print_info, print_success, print_error, print_warning
import config


def format_job_for_email(job, index=1):
    """Formate une offre d'emploi pour l'email"""
    company = job.get('company', 'Entreprise non spécifiée')
    title = job.get('title', 'Titre non spécifié')
    location = job.get('location', 'Localisation non spécifiée')
    source = job.get('source', 'Source inconnue')
    date = job.get('date', 'Date non spécifiée')
    url = job.get('url', '#')
    
    return f"""
    <div style="margin-bottom: 20px; padding: 15px; border-left: 4px solid #0077b5; background-color: #f8f9fa;">
        <h3 style="margin-top: 0; color: #0077b5;">{index}. {title}</h3>
        <p><strong>🏢 Entreprise:</strong> {company}</p>
        <p><strong>📍 Localisation:</strong> {location}</p>
        <p><strong>🌐 Source:</strong> {source}</p>
        <p><strong>📅 Date:</strong> {date}</p>
        <p><a href="{url}" style="color: #0077b5; text-decoration: none;">🔗 Voir l'offre →</a></p>
    </div>
    """


def create_email_html(new_jobs, total_jobs):
    """Crée le contenu HTML de l'email"""
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 800px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #0077b5; color: white; padding: 20px; border-radius: 5px 5px 0 0; }}
            .content {{ background-color: #ffffff; padding: 20px; border: 1px solid #ddd; }}
            .footer {{ background-color: #f8f9fa; padding: 15px; text-align: center; color: #666; font-size: 12px; border-radius: 0 0 5px 5px; }}
            .stats {{ background-color: #e3f2fd; padding: 15px; margin: 20px 0; border-radius: 5px; }}
            a {{ color: #0077b5; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔔 Nouvelles offres d'emploi Data</h1>
                <p>Rapport quotidien - {datetime.now().strftime('%d/%m/%Y à %H:%M')}</p>
            </div>
            <div class="content">
                <div class="stats">
                    <h2>📊 Statistiques</h2>
                    <p><strong>{len(new_jobs)}</strong> nouvelle(s) offre(s) détectée(s)</p>
                    <p><strong>{total_jobs}</strong> offre(s) au total</p>
                </div>
                
                <h2>🆕 Nouvelles offres</h2>
    """
    
    if new_jobs:
        for idx, job in enumerate(new_jobs, 1):
            html_content += format_job_for_email(job, idx)
    else:
        html_content += """
                <p style="padding: 20px; background-color: #fff3cd; border-left: 4px solid #ffc107;">
                    Aucune nouvelle offre détectée aujourd'hui.
                </p>
        """
    
    html_content += """
            </div>
            <div class="footer">
                <p>Cet email a été généré automatiquement par votre système de recherche d'emploi.</p>
                <p>Vous recevez cet email car vous avez configuré des alertes quotidiennes.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html_content


def create_email_text(new_jobs, total_jobs):
    """Crée le contenu texte de l'email (fallback)"""
    text_content = f"""
🔔 NOUVELLES OFFRES D'EMPLOI DATA
Rapport quotidien - {datetime.now().strftime('%d/%m/%Y à %H:%M')}

📊 STATISTIQUES
{len(new_jobs)} nouvelle(s) offre(s) détectée(s)
{total_jobs} offre(s) au total

🆕 NOUVELLES OFFRES
"""
    
    if new_jobs:
        for idx, job in enumerate(new_jobs, 1):
            company = job.get('company', 'Entreprise non spécifiée')
            title = job.get('title', 'Titre non spécifié')
            location = job.get('location', 'Localisation non spécifiée')
            source = job.get('source', 'Source inconnue')
            url = job.get('url', '#')
            
            text_content += f"""
{idx}. {title}
   🏢 Entreprise: {company}
   📍 Localisation: {location}
   🌐 Source: {source}
   🔗 URL: {url}
"""
    else:
        text_content += "\nAucune nouvelle offre détectée aujourd'hui.\n"
    
    text_content += f"""
---
Cet email a été généré automatiquement par votre système de recherche d'emploi.
"""
    
    return text_content


def send_email(new_jobs, total_jobs, recipient_email=None):
    """
    Envoie un email avec les nouvelles annonces
    
    Args:
        new_jobs: Liste des nouvelles offres
        total_jobs: Nombre total d'offres
        recipient_email: Email du destinataire (si None, utilise config.EMAIL_RECIPIENT)
    """
    # Configuration email depuis config
    smtp_server = config.EMAIL_SMTP_SERVER
    smtp_port = config.EMAIL_SMTP_PORT
    smtp_user = config.EMAIL_SMTP_USER
    smtp_password = config.EMAIL_SMTP_PASSWORD
    sender_email = config.EMAIL_SENDER
    recipient = recipient_email or config.EMAIL_RECIPIENT
    
    if not all([smtp_server, smtp_user, smtp_password, recipient]):
        print_error("Configuration email incomplète. Vérifiez config.py et .env")
        return False
    
    try:
        # Créer le message
        msg = MIMEMultipart('alternative')
        msg['From'] = sender_email
        msg['To'] = recipient
        msg['Subject'] = f"🔔 {len(new_jobs)} nouvelle(s) offre(s) Data - {datetime.now().strftime('%d/%m/%Y')}"
        
        # Créer les versions texte et HTML
        text_content = create_email_text(new_jobs, total_jobs)
        html_content = create_email_html(new_jobs, total_jobs)
        
        # Attacher les deux versions
        part1 = MIMEText(text_content, 'plain', 'utf-8')
        part2 = MIMEText(html_content, 'html', 'utf-8')
        
        msg.attach(part1)
        msg.attach(part2)
        
        # Envoyer l'email
        print_info(f"Connexion au serveur SMTP {smtp_server}:{smtp_port}...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        
        print_info(f"Envoi de l'email à {recipient}...")
        server.send_message(msg)
        server.quit()
        
        print_success(f"✅ Email envoyé avec succès à {recipient}")
        return True
        
    except Exception as e:
        print_error(f"❌ Erreur lors de l'envoi de l'email: {str(e)}")
        return False


if __name__ == "__main__":
    # Test du module
    from compare_jobs import get_new_jobs
    
    print_info("Test du module d'envoi d'email...")
    new_jobs, all_jobs = get_new_jobs()
    
    if new_jobs:
        print_info(f"Envoi d'un email de test avec {len(new_jobs)} nouvelles offres...")
        send_email(new_jobs, len(all_jobs))
    else:
        print_info("Aucune nouvelle offre, pas d'email envoyé")

