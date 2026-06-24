from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from crewai.tools import tool
import os
import json
import streamlit as st

def obtenir_service_calendar():
    # Sur Streamlit Web, on stockera le JSON dans les secrets. Sur PC, on lit le fichier.
    if "GOOGLE_CALENDAR_JSON" in st.secrets:
        info_cles = json.loads(st.secrets["GOOGLE_CALENDAR_JSON"])
    else:
        # Chemin vers ton fichier téléchargé sur ton PC
        with open("ta_cle_google.json", "r") as f:
            info_cles = json.load(f)
            
    scopes = ['https://www.googleapis.com/auth/calendar']
    creds = Credentials.from_service_account_info(info_cles, scopes=scopes)
    return build('calendar', 'v3', credentials=creds)

@tool("Créer un rendez-vous dans Google Calendar")
def creer_evenement_calendar(titre: str, date_debut_iso: str, date_fin_iso: str, description: str) -> str:
    """Utile pour créer un événement dans l'agenda Google. 
    Les dates doivent être au format ISO (Ex: '2026-06-15T14:00:00')."""
    try:
        service = obtenir_service_calendar()
        
        evenement = {
            'summary': titre,
            'description': description,
            'start': {'dateTime': date_debut_iso, 'timeZone': 'Europe/Paris'},
            'end': {'dateTime': date_fin_iso, 'timeZone': 'Europe/Paris'},
            # colorId '11' correspond généralement au Rouge Foncé dans Google Calendar
            'colorId': '11', 
            'reminders': {
                'useDefault': False,
                'overrides': [
                    # Rappel 90 minutes avant (90)
                    {'method': 'popup', 'minutes': 90}
                ]
            }
        }
        
        # 'primary' désigne l'agenda principal partagé avec le compte de service
        evenement_cree = service.events().insert(calendarId='primary', body=evenement).execute()
        return f"✅ Rendez-vous créé avec succès ! Lien : {evenement_cree.get('htmlLink')}"
    except Exception as e:
        return f"❌ Erreur lors de la création du rendez-vous : {str(e)}"