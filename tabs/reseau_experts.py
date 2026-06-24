import streamlit as st
import os
import uuid
from pydantic import BaseModel, Field
from typing import List
from crewai import Agent, Task, Crew, Process
from generer_fiche import completer_fiche_word
from config_agents import AGENTS_CONFIG  # <--- IMPORTATION DU CERVEAU

# =====================================================================
# MODÈLES DE DONNÉES STRICTS (PYDANTIC)
# =====================================================================
class ListeLots(BaseModel):
    lots: List[str] = Field(description="Liste stricte des mots-clés des corps d'état sélectionnés (ex: ['ELEC', 'PLACO'])")

def afficher_onglet_experts():
    st.title("👷‍♂️ Réunion de Chantier Virtuelle")
    st.subheader("Les 7 experts métiers analysent ton projet pour le devis.")
    
    # --- AJOUT : Initialisation de la mémoire (Session State) ---
    if "devis_text" not in st.session_state:
        st.session_state.devis_text = None
        st.session_state.devis_bytes = None
        st.session_state.devis_name = None
    
    # --- NOUVELLES OPTIONS DE PERSONNALISATION ---
    col1, col2 = st.columns(2)
    with col1:
        nom_client = st.text_input("👤 Nom du Client (Optionnel) :", placeholder="Ex: M. et Mme Dupont")
    with col2:
        adresse_chantier = st.text_input("📍 Adresse du Chantier (Optionnel) :", placeholder="Ex: 12 rue des Lilas, Strasbourg")
    
    gamme_travaux = st.selectbox(
        "💎 Gamme, finitions et spécificités du bâtiment :", 
        [
            "Standard (Bon rapport qualité/prix, respect strict des normes)", 
            "Premium (Haut de gamme, finitions parfaites Q4, équipements encastrés, matériaux nobles)", 
            "Éco-responsable (Matériaux biosourcés, économie d'énergie, faible empreinte carbone)",
            "Bâti Ancien / Maison Alsacienne (Colombages, torchis, matériaux perspirants type chaux/chanvre obligatoires, interdiction stricte des enduits ciment et isolants étanches bloquant l'humidité)"
        ]
    )
    
    # La zone de texte pour entrer la demande
    projet_expert = st.text_area("📝 Notes de chantier (à analyser par les experts) :", height=150, placeholder="Ex: Rénovation salle de bain...")
    
    # Le bouton pour lancer la machine
    if st.button("🚀 Lancer l'analyse des experts"):
        if not projet_expert.strip():
            st.warning("⚠️ Veuillez décrire le projet avant de lancer l'équipe.")
        else:
            # --- INJECTION INVISIBLE DE LA GAMME DANS LE CERVEAU DES AGENTS ---
            projet_expert = f"{projet_expert}\n\n[CONSIGNE GLOBALE : La gamme de prestation exigée par le client est : {gamme_travaux}. Adaptez scrupuleusement vos choix de matériaux, techniques et finitions en conséquence.]"
            
            # La roue de chargement
            with st.spinner("⏳ La réunion de chantier est en cours... Cela prend environ 1 à 2 minutes."):
                
                # --- 1. CRÉATION DES AGENTS (Allégés grâce à config_agents.py) ---
                chef_de_chantier = Agent(
                    role=AGENTS_CONFIG["chef_de_chantier"]["role"],
                    goal=AGENTS_CONFIG["chef_de_chantier"]["goal"],
                    backstory=AGENTS_CONFIG["chef_de_chantier"]["backstory"],
                    verbose=False,
                    llm='gemini/gemini-2.5-flash'
                )

                expert_electricien = Agent(
                    role=AGENTS_CONFIG["expert_electricien"]["role"],
                    goal=AGENTS_CONFIG["expert_electricien"]["goal"],
                    backstory=AGENTS_CONFIG["expert_electricien"]["backstory"],
                    verbose=False,
                    llm='gemini/gemini-2.5-flash'
                )

                expert_plombier = Agent(
                    role=AGENTS_CONFIG["expert_plombier"]["role"],
                    goal=AGENTS_CONFIG["expert_plombier"]["goal"],
                    backstory=AGENTS_CONFIG["expert_plombier"]["backstory"],
                    verbose=False,
                    llm='gemini/gemini-2.5-flash'
                )

                expert_plaquiste = Agent(
                    role=AGENTS_CONFIG["expert_plaquiste"]["role"],
                    goal=AGENTS_CONFIG["expert_plaquiste"]["goal"],
                    backstory=AGENTS_CONFIG["expert_plaquiste"]["backstory"],
                    verbose=False,
                    llm='gemini/gemini-2.5-flash'
                )

                expert_carreleur = Agent(
                    role=AGENTS_CONFIG["expert_carreleur"]["role"],
                    goal=AGENTS_CONFIG["expert_carreleur"]["goal"],
                    backstory=AGENTS_CONFIG["expert_carreleur"]["backstory"],
                    verbose=False,
                    llm='gemini/gemini-2.5-flash'
                )

                expert_peintre = Agent(
                    role=AGENTS_CONFIG["expert_peintre"]["role"],
                    goal=AGENTS_CONFIG["expert_peintre"]["goal"],
                    backstory=AGENTS_CONFIG["expert_peintre"]["backstory"],
                    verbose=False,
                    llm='gemini/gemini-2.5-flash'
                )

                expert_solier = Agent(
                    role=AGENTS_CONFIG["expert_solier"]["role"],
                    goal=AGENTS_CONFIG["expert_solier"]["goal"],
                    backstory=AGENTS_CONFIG["expert_solier"]["backstory"],
                    verbose=False,
                    llm='gemini/gemini-2.5-flash'
                )

                expert_menuisier = Agent(
                    role=AGENTS_CONFIG["expert_menuisier"]["role"],
                    goal=AGENTS_CONFIG["expert_menuisier"]["goal"],
                    backstory=AGENTS_CONFIG["expert_menuisier"]["backstory"],
                    verbose=False,
                    llm='gemini/gemini-2.5-flash'
                )

                expert_cvc = Agent(
                    role=AGENTS_CONFIG["expert_cvc"]["role"],
                    goal=AGENTS_CONFIG["expert_cvc"]["goal"],
                    backstory=AGENTS_CONFIG["expert_cvc"]["backstory"],
                    verbose=False,
                    llm='gemini/gemini-2.5-flash'
                )

                expert_isolation = Agent(
                    role=AGENTS_CONFIG["expert_isolation"]["role"],
                    goal=AGENTS_CONFIG["expert_isolation"]["goal"],
                    backstory=AGENTS_CONFIG["expert_isolation"]["backstory"],
                    verbose=False,
                    llm='gemini/gemini-2.5-flash'
                )

                expert_ouvertures = Agent(
                    role=AGENTS_CONFIG["expert_ouvertures"]["role"],
                    goal=AGENTS_CONFIG["expert_ouvertures"]["goal"],
                    backstory=AGENTS_CONFIG["expert_ouvertures"]["backstory"],
                    verbose=False,
                    llm='gemini/gemini-2.5-flash'
                )

                expert_domotique = Agent(
                    role=AGENTS_CONFIG["expert_domotique"]["role"],
                    goal=AGENTS_CONFIG["expert_domotique"]["goal"],
                    backstory=AGENTS_CONFIG["expert_domotique"]["backstory"],
                    verbose=False,
                    llm='gemini/gemini-2.5-flash'
                )

                expert_humidite = Agent(
                    role=AGENTS_CONFIG["expert_humidite"]["role"],
                    goal=AGENTS_CONFIG["expert_humidite"]["goal"],
                    backstory=AGENTS_CONFIG["expert_humidite"]["backstory"],
                    verbose=False,
                    llm='gemini/gemini-2.5-flash'
                )

                # --- 2. CRÉATION DES TÂCHES ---
                # =================================================================
                # ÉTAPE 1 : LE TRI PRÉALABLE PAR LE CHEF DE CHANTIER (Structured Output Pydantic)
                # =================================================================
                tache_tri = Task(
                    description=f"Analyse ce projet de chantier : '{projet_expert}'. Identifie les corps d'état nécessaires parmi cette liste stricte : ELEC, PLOMBERIE, PLACO, CARRELAGE, PEINTURE, SOL, MENUISERIE, CVC, ISOLATION, OUVERTURES, DOMOTIQUE, HUMIDITE.",
                    expected_output="Un objet contenant la liste des mots-clés.",
                    agent=chef_de_chantier,
                    output_pydantic=ListeLots  # <--- LA MAGIE OPÈRE ICI
                )

                # On lance le chef de chantier tout seul
                equipe_tri = Crew(agents=[chef_de_chantier], tasks=[tache_tri], verbose=False)
                resultat_tri = equipe_tri.kickoff()
                
                # Extraction garantie à 100% au format Python (plus besoin de parser le texte)
                if resultat_tri.pydantic:
                    liste_lots = [lot.upper() for lot in resultat_tri.pydantic.lots]
                else:
                    liste_lots = []

                # On affiche discrètement ce que le chef a détecté
                st.info(f"🔍 Le Chef de Chantier a convoqué les lots suivants : {', '.join(liste_lots)}")

                # =================================================================
                # ÉTAPE 2 : CONSTITUTION DE L'ÉQUIPE SUR-MESURE
                # =================================================================
                agents_actifs = [chef_de_chantier]
                taches_actives = []

                if "ELEC" in liste_lots:
                    agents_actifs.append(expert_electricien)
                    taches_actives.append(Task(
                        description=f"Projet : '{projet_expert}'. Rédige le descriptif détaillé du lot Électricité. Ajoute la section 'NORMES ET VIGILANCE' (NF C 15-100).",
                        expected_output="Descriptif détaillé du lot Électricité.",
                        agent=expert_electricien,
                        async_execution=True
                    ))

                if "PLOMBERIE" in liste_lots:
                    agents_actifs.append(expert_plombier)
                    taches_actives.append(Task(
                        description=f"Projet : '{projet_expert}'. Rédige le descriptif détaillé du lot Plomberie. Ajoute la section 'NORMES ET VIGILANCE' (DTU 60.1).",
                        expected_output="Descriptif détaillé du lot Plomberie.",
                        agent=expert_plombier,
                        async_execution=True
                    ))

                if "PLACO" in liste_lots:
                    agents_actifs.append(expert_plaquiste)
                    taches_actives.append(Task(
                        description=f"Projet : '{projet_expert}'. Rédige le descriptif détaillé du lot Plâtrerie/Faux-plafond/Enduisage. Ajoute la section 'NORMES ET VIGILANCE' (DTU 25.41).",
                        expected_output="Descriptif détaillé du lot Plâtrerie.",
                        agent=expert_plaquiste,
                        async_execution=True
                    ))

                if "CARRELAGE" in liste_lots:
                    agents_actifs.append(expert_carreleur)
                    taches_actives.append(Task(
                        description=f"Projet : '{projet_expert}'. Rédige le descriptif détaillé du lot Carrelage/Faïence. Ajoute la section 'NORMES ET VIGILANCE' (DTU 52.2).",
                        expected_output="Descriptif détaillé du lot Carrelage.",
                        agent=expert_carreleur,
                        async_execution=True
                    ))

                if "PEINTURE" in liste_lots:
                    agents_actifs.append(expert_peintre)
                    taches_actives.append(Task(
                        description=f"Projet : '{projet_expert}'. Rédige le descriptif détaillé du lot Peinture. Ajoute la section 'NORMES ET VIGILANCE' (DTU 59.1).",
                        expected_output="Descriptif détaillé du lot Peinture.",
                        agent=expert_peintre,
                        async_execution=True
                    ))

                if "SOL" in liste_lots:
                    agents_actifs.append(expert_solier)
                    taches_actives.append(Task(
                        description=f"Projet : '{projet_expert}'. Rédige le descriptif détaillé du lot Sols (hors carrelage). Ajoute la section 'NORMES ET VIGILANCE'.",
                        expected_output="Descriptif détaillé du lot Sols.",
                        agent=expert_solier,
                        async_execution=True
                    ))

                if "MENUISERIE" in liste_lots:
                    agents_actifs.append(expert_menuisier)
                    taches_actives.append(Task(
                        description=f"Projet : '{projet_expert}'. Rédige le descriptif détaillé du lot Menuiserie / Agencement intérieur (pose des meubles, ajustements, quincaillerie).",
                        expected_output="Descriptif détaillé du lot Menuiserie.",
                        agent=expert_menuisier,
                        async_execution=True
                    ))

                if "CVC" in liste_lots:
                    agents_actifs.append(expert_cvc)
                    taches_actives.append(Task(
                        description=f"Projet : '{projet_expert}'. Rédige le descriptif détaillé du lot Chauffage, Ventilation et Climatisation (extraction, VMC, raccordements thermiques).",
                        expected_output="Descriptif détaillé du lot CVC.",
                        agent=expert_cvc,
                        async_execution=True
                    ))

                if "ISOLATION" in liste_lots:
                    agents_actifs.append(expert_isolation)
                    taches_actives.append(Task(
                        description=f"Projet : '{projet_expert}'. Rédige le descriptif détaillé du lot Isolation Thermique (murs, combles, planchers). Mentionne les exigences de résistance thermique (R) et les points de vigilance liés aux ponts thermiques.",
                        expected_output="Descriptif détaillé du lot Isolation.",
                        agent=expert_isolation,
                        async_execution=True
                    ))

                if "OUVERTURES" in liste_lots:
                    agents_actifs.append(expert_ouvertures)
                    taches_actives.append(Task(
                        description=f"Projet : '{projet_expert}'. Rédige le descriptif détaillé du lot Menuiseries Extérieures (fenêtres, baies, portes d'entrée, volets). Précise le type de pose et l'étanchéité.",
                        expected_output="Descriptif détaillé du lot Menuiseries Extérieures.",
                        agent=expert_ouvertures,
                        async_execution=True
                    ))

                if "DOMOTIQUE" in liste_lots:
                    agents_actifs.append(expert_domotique)
                    taches_actives.append(Task(
                        description=f"Projet : '{projet_expert}'. Rédige le descriptif détaillé du lot Domotique / Courants faibles (Réseau VDI, alarme, automatismes, pilotage chauffage).",
                        expected_output="Descriptif détaillé du lot Domotique.",
                        agent=expert_domotique,
                        async_execution=True
                    ))

                if "HUMIDITE" in liste_lots:
                    agents_actifs.append(expert_humidite)
                    taches_actives.append(Task(
                        description=f"Projet : '{projet_expert}'. Rédige le descriptif détaillé du lot Traitement de l'Humidité (remontées capillaires, cuvelage, assèchement). Précise le mode opératoire curatif.",
                        expected_output="Descriptif détaillé du lot Traitement Humidité.",
                        agent=expert_humidite,
                        async_execution=True
                    ))

                # Le chef de chantier reprend la main à la fin pour assembler le document
                synthese_devis = Task(
                    description=f"Prends les rendus de tous les artisans qui viennent d'intervenir. Synthétise-les dans un document final propre, structuré par lots.\n\n"
                                f"CONSIGNES OBLIGATOIRES :\n"
                                f"1. Ajoute un bel en-tête au début du document avec : 'Client : {nom_client if nom_client else 'Non renseigné'} | Adresse du chantier : {adresse_chantier if adresse_chantier else 'Non renseignée'}'.\n"
                                f"2. Rédige de manière très professionnelle, prêt à être joint à un devis.\n"
                                f"3. À la toute fin du document, ajoute une section '📅 PLANNING PRÉVISIONNEL' où tu proposes un ordre chronologique d'intervention logique (Semaine 1, Semaine 2...) avec les lots retenus.",
                    expected_output="Un document de synthèse ultra-structuré avec en-tête client, descriptifs par lots, et un planning estimatif final.",
                    agent=chef_de_chantier,
                    context=taches_actives.copy()  # <--- LE CHEF RÉCUPÈRE LE TRAVAIL DE TOUS LES ARTISANS ICI
                )
                taches_actives.append(synthese_devis)

                # =================================================================
                # ÉTAPE 3 : LANCEMENT DE L'ÉQUIPE (Économique et ciblée)
                # =================================================================
                if len(agents_actifs) > 1: 
                    reseau_experts = Crew(
                        agents=agents_actifs,
                        tasks=taches_actives,
                        process=Process.sequential,
                        verbose=False
                    )

                    try:
                        resultat_experts = reseau_experts.kickoff()
                        
                        # Génération du fichier Word avec un nom unique pour éviter les collisions
                        id_unique = uuid.uuid4().hex[:6]
                        nom_fichier_devis = f"Synthese_Experts_{id_unique}.docx"
                        completer_fiche_word(str(resultat_experts), nom_fichier=nom_fichier_devis)
                        
                        # Lecture du fichier en mémoire vive
                        with open(nom_fichier_devis, "rb") as file:
                            docx_bytes = file.read()
                            
                        # --- AJOUT : Enregistrement dans le Session State ---
                        st.session_state.devis_text = str(resultat_experts)
                        st.session_state.devis_bytes = docx_bytes
                        st.session_state.devis_name = nom_fichier_devis
                        
                        # Nettoyage immédiat : suppression du fichier physique du serveur
                        os.remove(nom_fichier_devis)
                        
                    except Exception as e:
                        # Message générique pour l'utilisateur
                        st.error("❌ Une erreur inattendue s'est produite lors de la réunion de chantier.")
                        
                        # Boîte déroulante cachée avec la vraie erreur pour toi (le développeur)
                        with st.expander("🛠️ Afficher les détails techniques (Pour le débogage)"):
                            st.error(f"Type d'erreur : {type(e).__name__}")
                            st.code(str(e), language="python")
                            
                else:
                    st.warning("⚠️ Le Chef de Chantier n'a détecté aucun lot correspondant à ta demande. Essaie de détailler davantage les travaux.")

    # ==========================================
    # 👉 AFFICHAGE PERSISTANT (Onglet 3 - Réseau d'experts)
    # ==========================================
    if st.session_state.devis_text:
        st.success("✅ Document généré avec succès (et à moindre coût) !")
        st.download_button(
            label="📥 Télécharger la Synthèse Experts au format Word (.docx)",
            data=st.session_state.devis_bytes,
            file_name=st.session_state.devis_name,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        st.markdown("---")
        st.markdown("### 📋 Aperçu de la Synthèse Technique")
        st.markdown(st.session_state.devis_text)