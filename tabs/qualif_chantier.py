import streamlit as st
import os
import uuid
from crewai import Agent, Task, Crew
from generer_fiche import completer_fiche_word
from outils_calendrier import creer_evenement_calendar
from config_agents import AGENTS_CONFIG  # <--- IMPORTATION DU CERVEAU

def afficher_onglet_qualification():
    st.title("📋 Assistant de Qualification de Chantier")
    st.subheader("Transforme tes notes d'appel brutes en une fiche client Word professionnelle")
    
    # --- AJOUT : Initialisation de la mémoire (Session State) ---
    if "fiche_text" not in st.session_state:
        st.session_state.fiche_text = None
        st.session_state.fiche_bytes = None
        st.session_state.fiche_name = None

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
                
                # Configuration de l'agent CrewAI (Allégée grâce à config_agents.py)
                expert_batiment = Agent(
                    role=AGENTS_CONFIG["expert_batiment"]["role"],
                    goal=AGENTS_CONFIG["expert_batiment"]["goal"],
                    backstory=AGENTS_CONFIG["expert_batiment"]["backstory"],
                    verbose=False,
                    llm='gemini/gemini-2.5-flash',
                    tools=[creer_evenement_calendar]
                )
                
                analyse_notes = Task(
                    description=f"""Analyse ces notes d'appel et crée une fiche client structurée :
                    {notes_brutes}
                    Consignes : Sépare par lots (Électricité, Plâtrerie, Démolition...), indique l'adresse, le nom, et ajoute des points de vigilance pour la visite.
                    
                    IMPORTANT : Si tu détectes une date et une heure de rendez-vous (visite de chantier, rappel...) dans les notes, utilise IMPÉRATIVEMENT ton outil pour créer automatiquement le rendez-vous dans l'agenda.""",
                    expected_output="Une fiche de qualification claire et professionnelle, ainsi qu'un message confirmant si le rendez-vous a bien été ajouté à l'agenda.",
                    agent=expert_batiment
                )
                
                crew = Crew(agents=[expert_batiment], tasks=[analyse_notes], verbose=False)
                compte_rendu = crew.kickoff()
                
                # Génération du fichier Word avec un nom unique pour éviter les collisions
                id_unique = uuid.uuid4().hex[:6]
                nom_fichier_word = f"Fiche_Chantier_{id_unique}.docx"
                completer_fiche_word(str(compte_rendu), nom_fichier=nom_fichier_word)
                
                # Lecture du fichier en mémoire vive
                with open(nom_fichier_word, "rb") as file:
                    docx_bytes = file.read()
                    
                # --- AJOUT : Enregistrement dans le Session State ---
                st.session_state.fiche_text = str(compte_rendu)
                st.session_state.fiche_bytes = docx_bytes
                st.session_state.fiche_name = nom_fichier_word
                
                # Nettoyage immédiat : suppression du fichier physique du serveur
                os.remove(nom_fichier_word)

    # =====================================================================
    # 👉 AFFICHAGE PERSISTANT (Onglet 1 - Qualification)
    # =====================================================================
    if st.session_state.fiche_text:
        st.success("🎉 Analyse terminée avec succès !")
        st.download_button(
            label="📥 Télécharger la Fiche Client au format Word (.docx)",
            data=st.session_state.fiche_bytes,
            file_name=st.session_state.fiche_name,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        st.markdown("### 👁️ Aperçu du compte-rendu textuel :")
        st.write(st.session_state.fiche_text)