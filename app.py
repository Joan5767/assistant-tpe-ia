import streamlit as st
import os
from crewai import Agent, Task, Crew
from generer_fiche import completer_fiche_word

# Configuration de la page de l'application
st.set_page_config(page_title="Assistant IA - Rénovation", page_icon="🏗️", layout="wide")

# Gestion sécurisée de la clé API
if "GEMINI_API_KEY" in st.secrets:
    os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]
elif "GEMINI_API_KEY" in os.environ:
    # Si tu as configuré la clé dans les variables d'environnement de ton PC
    pass
else:
    st.error("⚠️ Clé API Gemini introuvable. Configurez les secrets Streamlit ou une variable d'environnement locale.")

# Barre latérale pour naviguer entre tes agents
st.sidebar.title("🏗️ Mon Assistant IA")
st.sidebar.markdown("---")
choix_agent = st.sidebar.radio(
    "Sélectionne un outil :",
    ["📋 Qualification de Chantier", "📧 Analyse d'Email Entrant", "🚀 Prospection Agences (Gmass)", "📊 Assistant Comptable (Bientôt)"]
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
elif choix_agent == "📧 Analyse d'Email Entrant":
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
                
                # Agent 1 : Le Commercial
                assistant_commercial = Agent(
                    role='Assistant Commercial Rénovation',
                    goal='Qualifier les demandes de travaux et préparer la relation client',
                    backstory="Tu es le premier filtre de l'entreprise. Tu extrais les données clés et tu rédiges une réponse polie pour demander les pièces manquantes.",
                    verbose=False,
                    llm='gemini/gemini-2.5-flash',
                    allow_delegation=False
                )

                # Agent 2 : L'Expert Technique
                expert_technique = Agent(
                    role='Directeur Technique Rénovation TCE',
                    goal='Identifier les risques techniques, réglementaires et les opportunités d\'aides d\'un projet',
                    backstory="Tu as 20 ans de bouteille dans le bâtiment et la rénovation tous corps d'état. Tu connais les pièges des chantiers (porteurs, amiante) et les réglementations (passoires thermiques, aides de l'État).",
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

elif choix_agent == "🚀 Prospection Agences (Gmass)":
    st.title("🚀 Campagne de Prospection Automatique")
    st.info("Cet outil te permettra bientôt de déposer ton fichier 'cibles.csv' directement ici pour générer le fichier de campagne Gmass.")
