#!/usr/bin/env python3
"""Script rapide pour vérifier l'extraction des entreprises"""
import json
import os

jobs_file = "data/jobs.json"
if os.path.exists(jobs_file):
    with open(jobs_file, 'r', encoding='utf-8') as f:
        jobs = json.load(f)
    
    total = len(jobs)
    companies_ok = [j for j in jobs if j.get('company') and j.get('company') != 'N/A']
    companies_na = total - len(companies_ok)
    
    print(f"\n📊 Statistiques d'extraction des entreprises :")
    print(f"   Total d'offres : {total}")
    print(f"   ✅ Entreprises trouvées : {len(companies_ok)} ({len(companies_ok)*100//total if total > 0 else 0}%)")
    print(f"   ❌ Entreprises non trouvées : {companies_na} ({companies_na*100//total if total > 0 else 0}%)")
    
    if companies_ok:
        print(f"\n📋 Exemples d'entreprises trouvées :")
        for i, job in enumerate(companies_ok[:10], 1):
            print(f"   {i}. {job.get('company', 'N/A')} - {job.get('title', 'N/A')[:50]}")
    
    if companies_na > 0:
        print(f"\n⚠️  Offres sans entreprise :")
        for i, job in enumerate([j for j in jobs if not j.get('company') or j.get('company') == 'N/A'][:5], 1):
            print(f"   {i}. {job.get('title', 'N/A')[:50]} - Source: {job.get('source', 'N/A')}")
else:
    print("❌ Fichier jobs.json non trouvé. Lancez d'abord une recherche.")
