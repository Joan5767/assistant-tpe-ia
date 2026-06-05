import streamlit as st
import os
from crewai import Agent, Task, Crew
from generer_fiche import completer_fiche_word

# Configuration de la page de l'application
st.set_page_config(page_title="Assistant IA - Rénovation", page_icon="🏗️", layout="wide")

if "GEMINI_API_KEY" in st.secrets:
    os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]
else:
    # Si on est en local sur ton PC, il va chercher ta clé classique
    # Tu peux laisser ta vraie clé ici entre les guillemets pour tes tests sur ton PC
    os.environ["GEMINI_API_KEY"] = "AIzaSyDqAiBUf2k9Py4VqHu1coC5zXIe4M0fL-s"

# Barre latérale pour naviguer entre tes agents
st.sidebar.title("🏗️ Mon Assistant IA")
st.sidebar.markdown("---")
choix_agent = st.sidebar.radio(
    "Sélectionne un outil :",
    ["📋 Qualification de Chantier", "🚀 Prospection Agences (Gmass)", "📊 Assistant Comptable (Bientôt)"]
)

# =====================================================================
# ONGLET 1 : QUALIFICATION DE CHANTIER
# =====================================================================
if choix_agent == "📋 Qualification de Chantier":
    st.title("📋 Assistant de Qualification de Chantier")
    st.subheader("Transforme tes notes d'appel brutes en une fiche client Word professionnelle")
    
    # Zone de texte pour coller les notes
    notes_brutes = st.text_area(
        "Colle ici tes notes prises au téléphone (Nom, adresse, détails des travaux...) :",
        height=200,
        placeholder="Exemple :\nMme Wagner, 20 rue du cerf...\nAchat récent, travaux élec..."
    )
    
    # Bouton pour lancer l'IA
    if st.button("🧠 Structurer les notes et générer le fichier Word"):
        if not notes_brutes.strip():
            st.warning("⚠️ S'il te plaît, écris ou colle des notes avant de lancer l'IA.")
        else:
            with st.spinner("L'IA analyse tes notes et prépare le document Word..."):
                
                # Configuration de l'agent CrewAI (le même que dans ton script précédent)
                expert_batiment = Agent(
                    role='Conducteur de Travaux / Métreur TCE',
                    goal='Analyser des notes brutes d\'appels clients pour structurer un dossier technique de qualification de chantier.',
                    backstory="Tu es un professionnel expérimenté du bâtiment. Tu orthographies correctement les termes techniques et organises les infos par lot.",
                    verbose=False,
                    llm='gemini/gemini-2.5-flash'
                )
                
                analyse_notes = Task(
                    description=f"""Analyse ces notes d'appel et crée une fiche client structurée :
                    {notes_brutes}
                    Consignes : Sépare par lots (Électricité, Plâtrerie, Démolition...), indique l'adresse, le nom, et ajoute des points de vigilance pour la visite.""",
                    expected_output="Une fiche de qualification claire et professionnelle.",
                    agent=expert_batiment
                )
                
                crew = Crew(agents=[expert_batiment], tasks=[analyse_notes], verbose=False)
                compte_rendu = crew.kickoff()
                
                # Génération du fichier Word physique
                nom_fichier_word = "Fiche_Chantier_Generée.docx"
                completer_fiche_word(str(compte_rendu), nom_fichier=nom_fichier_word)
                
                # Affichage du résultat à l'écran
                st.success("🎉 Analyse terminée avec succès !")
                
                # Bouton de téléchargement direct depuis ton navigateur
                with open(nom_fichier_word, "rb") as file:
                    st.download_button(
                        label="📥 Télécharger la Fiche Client au format Word (.docx)",
                        data=file,
                        file_name=nom_fichier_word,
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
                
                st.markdown("### 👁️ Aperçu du compte-rendu textuel :")
                st.write(str(compte_rendu))

# =====================================================================
# ONGLET 2 : PROSPECTION (Rappel ou message d'attente)
# =====================================================================
elif choix_agent == "🚀 Prospection Agences (Gmass)":
    st.title("🚀 Campagne de Prospection Automatique")
    st.info("Cet outil te permettra bientôt de déposer ton fichier 'cibles.csv' directement ici pour générer le fichier de campagne Gmass.")