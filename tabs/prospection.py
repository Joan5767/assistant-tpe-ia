import streamlit as st
from crewai import Agent, Task, Crew
from config_agents import AGENTS_CONFIG  # <--- IMPORTATION DU CERVEAU

def afficher_onglet_email():
    st.title("📧 Traitement des Emails Prospects")
    st.subheader("L'équipe IA analyse la demande et prépare ton intervention.")
    
    email_recu = st.text_area(
        "Colle l'email complet du client ici :",
        height=200,
        placeholder="Exemple : Bonjour, je viens d'acheter une maison de 120m2 et je voudrais refaire l'isolation..."
    )
    
    if st.button("🧠 Lancer l'analyse Commerciale et Technique"):
        if not email_recu.strip():
            st.warning("⚠️ Merci de coller un email avant de lancer l'analyse.")
        else:
            with st.spinner("L'équipe commerciale et technique décortique le dossier..."):
                
                # Agent 1 : Le Commercial (Allégé grâce à config_agents.py)
                assistant_commercial = Agent(
                    role=AGENTS_CONFIG["assistant_commercial"]["role"],
                    goal=AGENTS_CONFIG["assistant_commercial"]["goal"],
                    backstory=AGENTS_CONFIG["assistant_commercial"]["backstory"],
                    verbose=False,
                    llm='gemini/gemini-2.5-flash',
                    allow_delegation=False
                )

                # Agent 2 : L'Expert Technique (Allégé grâce à config_agents.py)
                expert_technique = Agent(
                    role=AGENTS_CONFIG["expert_technique"]["role"],
                    goal=AGENTS_CONFIG["expert_technique"]["goal"],
                    backstory=AGENTS_CONFIG["expert_technique"]["backstory"],
                    verbose=False,
                    llm='gemini/gemini-2.5-flash',
                    allow_delegation=False
                )

                # Tâche 1
                tache_commerciale = Task(
                    description=f"Analyse cet email client : '{email_recu}'.\n1. Liste les travaux.\n2. Note la surface.\n3. Rédige le brouillon de réponse pour demander photos/plans.",
                    expected_output="Un compte-rendu commercial et un brouillon d'email.",
                    agent=assistant_commercial
                )

                # Tâche 2
                tache_technique = Task(
                    description="Lis le compte-rendu commercial. Rédige une note interne technique pour le Chargé d'Affaires. Alerte sur les points de vigilance et liste 3 questions techniques à poser. \nIMPORTANT : Ton rendu final doit obligatoirement inclure DEUX parties claires : \nPARTIE 1 : Le brouillon de réponse client généré par le commercial.\nPARTIE 2 : Ta note technique interne de vigilance.",
                    expected_output="Le brouillon de réponse client suivi de la note technique interne complète.",
                    agent=expert_technique
                )

                ma_tpe_virtuelle = Crew(
                    agents=[assistant_commercial, expert_technique],
                    tasks=[tache_commerciale, tache_technique],
                    verbose=False
                )
                
                resultat_final = ma_tpe_virtuelle.kickoff()
                
                st.success("✅ Dossier traité avec succès !")
                st.markdown("### 📋 Rendu Final de l'Équipe :")
                st.write(str(resultat_final))

def afficher_onglet_gmass():
    st.title("🚀 Campagne de Prospection Automatique")
    st.info("Cet outil te permettra bientôt de déposer ton fichier 'cibles.csv' directement ici pour générer le fichier de campagne Gmass.")