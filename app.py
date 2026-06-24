import streamlit as st
import os

# --- IMPORTATION DES VUES (ONGLETS) ---
from tabs.qualif_chantier import afficher_onglet_qualification
from tabs.prospection import afficher_onglet_email, afficher_onglet_gmass
from tabs.reseau_experts import afficher_onglet_experts

# Configuration globale de la page (Doit toujours rester au sommet de app.py)
st.set_page_config(page_title="Assistant IA - Rénovation", page_icon="🏗️", layout="wide")

# =====================================================================
# CŒUR DE L'APPLICATION (Le Routeur)
# =====================================================================
def main():
    # Barre latérale pour naviguer entre tes agents
    st.sidebar.title("🏗️ Mon Assistant IA")
    st.sidebar.markdown("---")
    
    choix_agent = st.sidebar.radio(
        "Sélectionne un outil :",
        [
            "📋 Qualification de Chantier", 
            "📧 Analyse d'Email Entrant", 
            "🚀 Prospection Agences (Gmass)", 
            "📊 Assistant Comptable (Bientôt)", 
            "👷‍♂️ Réseau d'Experts de Chantier"
        ]
    )

    # =====================================================================
    # AIGUILLAGE VERS LES FICHIERS
    # =====================================================================
    if choix_agent == "📋 Qualification de Chantier":
        afficher_onglet_qualification()
        
    elif choix_agent == "📧 Analyse d'Email Entrant":
        afficher_onglet_email()
        
    elif choix_agent == "🚀 Prospection Agences (Gmass)":
        afficher_onglet_gmass()
        
    elif choix_agent == "📊 Assistant Comptable (Bientôt)":
        st.title("📊 Assistant Comptable")
        st.info("Cet outil est en cours de développement...")
        
    elif choix_agent == "👷‍♂️ Réseau d'Experts de Chantier":
        afficher_onglet_experts()

# =====================================================================
# LANCEMENT SÉCURISÉ DE L'APPLICATION
# =====================================================================
if __name__ == "__main__":
    if "GEMINI_API_KEY" in st.secrets:
        os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]
        main()  # <--- On lance l'application ici !
    elif "GEMINI_API_KEY" in os.environ:
        main()  # <--- Ou ici !
    else:
        st.error("⚠️ Clé API Gemini introuvable. Configurez les secrets Streamlit ou une variable locale.")
        st.warning("L'interface est en pause jusqu'à l'ajout d'une clé valide.")