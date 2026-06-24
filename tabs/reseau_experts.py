import streamlit as st
import tempfile
from pydantic import BaseModel, Field
from typing import List
from crewai import Agent, Task, Crew, Process
from generer_fiche import completer_fiche_word
from config_agents import AGENTS_CONFIG

class ListeLots(BaseModel):
    lots: List[str] = Field(description="Liste stricte des mots-clés des corps d'état sélectionnés")

def afficher_onglet_experts():
    st.title("👷‍♂️ Réunion de Chantier Virtuelle")
    st.subheader("Les experts métiers analysent ton projet sur-mesure.")
    
    if "devis_text" not in st.session_state:
        st.session_state.devis_text = None
        st.session_state.devis_bytes = None
        st.session_state.devis_name = None
    
    col1, col2 = st.columns(2)
    with col1: nom_client = st.text_input("👤 Nom du Client :", placeholder="Ex: M. Dupont")
    with col2: adresse_chantier = st.text_input("📍 Adresse du Chantier :", placeholder="Ex: Strasbourg")
    
    gamme_travaux = st.selectbox("💎 Gamme :", [
        "Standard (Normes strictes)", "Premium (Finitions Q4, encastré)", 
        "Éco-responsable (Biosourcé)", "Bâti Ancien (Matériaux perspirants obligatoires)"
    ])
    
    projet_expert = st.text_area("📝 Notes de chantier :", height=150)
    
    if st.button("🚀 Lancer l'analyse des experts"):
        if not projet_expert.strip():
            st.warning("⚠️ Veuillez décrire le projet.")
        else:
            projet_text = f"{projet_expert}\n\n[CONSIGNE : Gamme exigée : {gamme_travaux}]"
            
            with st.status("🚀 Démarrage de la réunion...", expanded=True) as status:
                # 1. Chef de Chantier pour le Tri
                st.write("🔍 Chef de Chantier : Analyse des lots nécessaires...")
                chef = Agent(role=AGENTS_CONFIG["chef_de_chantier"]["role"], goal=AGENTS_CONFIG["chef_de_chantier"]["goal"], backstory=AGENTS_CONFIG["chef_de_chantier"]["backstory"], llm='gemini/gemini-2.5-flash')
                tache_tri = Task(description=f"Analyse ce projet : '{projet_text}'. Identifie les lots parmi : ELEC, PLOMBERIE, PLACO, CARRELAGE, PEINTURE, SOL, MENUISERIE, CVC, ISOLATION, OUVERTURES, DOMOTIQUE, HUMIDITE.", expected_output="Liste de lots", agent=chef, output_pydantic=ListeLots)
                
                resultat_tri = Crew(agents=[chef], tasks=[tache_tri]).kickoff()
                liste_lots = [lot.upper() for lot in resultat_tri.pydantic.lots] if resultat_tri.pydantic else []
                st.write(f"👷‍♂️ Lots identifiés : {', '.join(liste_lots)}")

                # 2. Instanciation Lazy des agents
                agents_actifs = [chef]
                taches_actives = []
                
                mapping_lots = {
                    "ELEC": "expert_electricien", "PLOMBERIE": "expert_plombier", "PLACO": "expert_plaquiste",
                    "CARRELAGE": "expert_carreleur", "PEINTURE": "expert_peintre", "SOL": "expert_solier",
                    "MENUISERIE": "expert_menuisier", "CVC": "expert_cvc", "ISOLATION": "expert_isolation",
                    "OUVERTURES": "expert_ouvertures", "DOMOTIQUE": "expert_domotique", "HUMIDITE": "expert_humidite"
                }

                for lot in liste_lots:
                    if lot in mapping_lots:
                        cfg = AGENTS_CONFIG[mapping_lots[lot]]
                        ag = Agent(role=cfg["role"], goal=cfg["goal"], backstory=cfg["backstory"], llm='gemini/gemini-2.5-flash')
                        agents_actifs.append(ag)
                        taches_actives.append(Task(description=f"Rédige le descriptif technique pour le lot {lot} en respectant la gamme {gamme_travaux}.", expected_output=f"Descriptif {lot}", agent=ag, async_execution=True))

                # 3. Finalisation par le Chef
                st.write("📝 Chef de Chantier : Assemblage final du devis...")
                synthese = Task(description="Synthétise les rendus par lots en un document pro avec en-tête client.", expected_output="Synthèse finale", agent=chef, context=taches_actives)
                taches_actives.append(synthese)

                # 4. Lancement de l'équipe
                try:
                    res = Crew(agents=agents_actifs, tasks=taches_actives, process=Process.sequential).kickoff()
                    with tempfile.NamedTemporaryFile(delete=True, suffix=".docx") as tmp:
                        completer_fiche_word(str(res), tmp.name)
                        tmp.seek(0)
                        st.session_state.devis_text = str(res)
                        st.session_state.devis_bytes = tmp.read()
                        st.session_state.devis_name = "Synthese_Experts.docx"
                    status.update(label="✅ Réunion terminée !", state="complete", expanded=False)
                except Exception as e:
                    st.error("❌ Erreur lors de la réunion.")
                    with st.expander("Détails"): st.code(str(e))

    if st.session_state.devis_text:
        st.download_button("📥 Télécharger Word", st.session_state.devis_bytes, st.session_state.devis_name)
        st.markdown(st.session_state.devis_text)