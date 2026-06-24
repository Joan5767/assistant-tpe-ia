<<<<<<< HEAD
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
=======
import streamlit as st
import os
from crewai import Agent, Task, Crew, Process
from generer_fiche import completer_fiche_word
from outils_calendrier import creer_evenement_calendar

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
    ["📋 Qualification de Chantier", "📧 Analyse d'Email Entrant", "🚀 Prospection Agences (Gmass)", "📊 Assistant Comptable (Bientôt)", "👷‍♂️ Réseau d'Experts de Chantier"]
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
                    goal='Analyser des notes brutes d\'appels clients pour structurer un dossier technique et planifier les rendez-vous.',
                    backstory="Tu es un professionnel expérimenté du bâtiment. Tu orthographies correctement les termes techniques, organises les infos par lot et gères l'agenda des chantiers.",
                    verbose=False,
                    llm='gemini/gemini-2.5-flash',
                    tools=[creer_evenement_calendar]  # <--- AJOUTE CETTE LIGNE
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

# =====================================================================
# ONGLET : LE RÉSEAU D'EXPERTS (Le super-outil)
# =====================================================================
elif choix_agent == "👷‍♂️ Réseau d'Experts de Chantier":
    st.title("👷‍♂️ Réunion de Chantier Virtuelle")
    st.subheader("Les 7 experts métiers analysent ton projet pour le devis.")
    
    # La zone de texte pour entrer la demande
    projet_expert = st.text_area("Notes de chantier (à analyser par les experts) :", height=150, placeholder="Ex: Rénovation salle de bain, dépose carrelage, remplacement baignoire par douche...")
    
    # Le bouton pour lancer la machine
    if st.button("🚀 Lancer l'analyse des experts"):
        if not projet_expert.strip():
            st.warning("⚠️ Veuillez décrire le projet avant de lancer l'équipe.")
        else:
            # La roue de chargement
            with st.spinner("⏳ La réunion de chantier est en cours... Les 7 experts se concertent. Cela prend environ 1 à 2 minutes."):
                
                # --- 1. CRÉATION DES AGENTS ---
                chef_de_chantier = Agent(
                    role='Chef de Chantier TCE',
                    goal='Analyser la demande brute, identifier tous les corps d\'état nécessaires et lister les grandes étapes du projet.',
                    backstory="Tu as 30 ans d'expérience en coordination de travaux. Ton rôle est de lire la demande du client et de distribuer le travail aux spécialistes dans le bon ordre.",
                    verbose=False,
                    llm='gemini/gemini-2.5-flash'
                )

                expert_electricien = Agent(
                    role='Expert Électricien',
                    goal='Rédiger le descriptif technique électrique, lister les normes (NF C 15-100) et les points de vigilance liés à l\'eau.',
                    backstory="Tu es un maître artisan électricien pointilleux. Tu es intraitable sur les volumes de protection et les liaisons équipotentielles.",
                    verbose=False,
                    llm='gemini/gemini-2.5-flash'
                )

                expert_plombier = Agent(
                    role='Expert Plombier-Chauffagiste',
                    goal='Rédiger le descriptif technique plomberie et sanitaire, incluant les raccordements et les DTU.',
                    backstory="Tu es un spécialiste des réseaux d'eau. Tu connais par cœur les pentes d'évacuation nécessaires et les normes de raccordement (DTU 60.1, 60.11).",
                    verbose=False,
                    llm='gemini/gemini-2.5-flash'
                )

                expert_plaquiste = Agent(
                    role='Artisan Plaquiste Jointeur',
                    goal='Rédiger le descriptif précis des travaux de plâtrerie, doublage et jointoiement selon le DTU 25.41.',
                    backstory="Tu es un plaquiste d'expérience. Tu respectes strictement les demandes de traitement de surface (enduit, pose de trame, ou doublage). Si un doublage ou une cloison est explicitement demandé dans une pièce humide, tu appliques du placo hydrofuge. Tu es intransigeant sur la qualité du ratissage.",
                    verbose=False,
                    llm='gemini/gemini-2.5-flash'
                )

                expert_carreleur = Agent(
                    role='Artisan Carreleur Mosaïste',
                    goal='Rédiger le descriptif technique pour la pose de carrelage au sol et faïence murale selon le DTU 52.2.',
                    backstory="Tu connais les sinistres liés aux infiltrations d'eau. Ton cheval de bataille est l'application obligatoire d'un SPEC/SEL sous le carrelage de douche.",
                    verbose=False,
                    llm='gemini/gemini-2.5-flash'
                )

                expert_peintre = Agent(
                    role='Artisan Peintre Décorateur',
                    goal='Rédiger le descriptif de préparation des supports et de mise en peinture selon le DTU 59.1.',
                    backstory="Tu refuses de peindre sur un support mal préparé. Tu listes toujours les phases d'impression et les peintures adaptées aux pièces humides.",
                    verbose=False,
                    llm='gemini/gemini-2.5-flash'
                )

                expert_solier = Agent(
                    role='Artisan Solier / Parqueteur',
                    goal='Rédiger le descriptif de préparation des sols et pose de revêtements selon les DTU 51.2 et 51.11.',
                    backstory="Tu sais qu'un beau sol dépend d'un sol droit. Tu exiges toujours un ragréage parfait avant de poser un revêtement.",
                    verbose=False,
                    llm='gemini/gemini-2.5-flash'
                )

                expert_menuisier = Agent(
                    role='Artisan Menuisier Agenceur',
                    goal='Rédiger le descriptif technique de pose des menuiseries intérieures, escaliers et mobiliers d\'agencement.',
                    backstory="Tu es un menuisier ébéniste minutieux. Tu crées les fiches de pose pour le mobilier (cuisines, dressings) et les blocs-portes. Tu gères les alignements et les fixations lourdes.",
                    verbose=False,
                    llm='gemini/gemini-2.5-flash'
                )

                expert_cvc = Agent(
                    role='Expert CVC (Chauffage, Ventilation, Climatisation)',
                    goal='Rédiger le descriptif technique pour les systèmes de chauffage, de climatisation et de ventilation (VMC) selon les DTU 68.3.',
                    backstory="Tu es le garant du confort thermique et de la qualité de l'air. Tu maîtrises le dimensionnement des réseaux de renouvellement d'air, les pompes à chaleur et l'extraction en cuisine.",
                    verbose=False,
                    llm='gemini/gemini-2.5-flash'
                )

                expert_isolation = Agent(
                    role='Expert en Rénovation Énergétique et Isolation',
                    goal='Rédiger le descriptif technique de l\'isolation thermique (ITI, combles, planchers) pour garantir l\'éligibilité aux aides.',
                    backstory="Tu es un thermicien intransigeant. Tu maîtrises les résistances thermiques (R) requises par MaPrimeRénov' et le traitement des ponts thermiques. Tu exiges toujours une continuité parfaite du pare-vapeur.",
                    verbose=False,
                    llm='gemini/gemini-2.5-flash'
                )

                expert_ouvertures = Agent(
                    role='Menuisier Extérieur / Façadier',
                    goal='Rédiger le descriptif technique pour le remplacement des menuiseries extérieures (fenêtres, baies, portes, volets).',
                    backstory="Tu es un spécialiste de l'enveloppe du bâtiment. Tu précises toujours le type de pose (feuillure, tunnel, applique ou rénovation), le type de vitrage, et tu garantis l'étanchéité à l'air et à l'eau grâce aux compribandes.",
                    verbose=False,
                    llm='gemini/gemini-2.5-flash'
                )

                expert_domotique = Agent(
                    role='Intégrateur Domotique et Courants Faibles',
                    goal='Rédiger le descriptif technique pour les réseaux informatiques, les alarmes, et la maison connectée.',
                    backstory="Tu es le geek du chantier. Tu penses toujours au câblage RJ45 de grade 3, à la centralisation des volets roulants, à la vidéosurveillance et au pilotage du chauffage à distance.",
                    verbose=False,
                    llm='gemini/gemini-2.5-flash'
                )

                expert_humidite = Agent(
                    role='Expert en Traitement de l\'Humidité',
                    goal='Rédiger les protocoles curatifs pour assainir les murs et fondations (remontées capillaires, infiltrations).',
                    backstory="Tu es le docteur des murs malades. Tu prescris des injections de résine hydrophobe, des cuvelages ou des systèmes d'assèchement muraux pour garantir un support pérenne avant toute finition.",
                    verbose=False,
                    llm='gemini/gemini-2.5-flash'
                )

                # --- 2. CRÉATION DES TÂCHES ---
                # =================================================================
                # ÉTAPE 1 : LE TRI PRÉALABLE PAR LE CHEF DE CHANTIER
                # =================================================================
                tache_tri = Task(
                    description=f"Analyse ce projet de chantier : '{projet_expert}'. Ton unique but est de lister les corps d'état qui vont devoir intervenir. Réponds UNIQUEMENT par une liste de mots-clés séparés par des virgules. Choisis tes mots-clés STRICTEMENT parmi cette liste : ELEC, PLOMBERIE, PLACO, CARRELAGE, PEINTURE, SOL, MENUISERIE, CVC, ISOLATION, OUVERTURES, DOMOTIQUE, HUMIDITE. N'écris aucune autre phrase, juste les mots-clés.",
                    expected_output="Une liste de mots-clés en majuscules séparés par des virgules.",
                    agent=chef_de_chantier
                )

                # On lance le chef de chantier tout seul pour faire le tri
                equipe_tri = Crew(agents=[chef_de_chantier], tasks=[tache_tri], verbose=False)
                resultat_tri = str(equipe_tri.kickoff()).upper()
                
                # On affiche discrètement ce que le chef a détecté
                st.info(f"🔍 Le Chef de Chantier a convoqué les lots suivants : {resultat_tri}")

                # =================================================================
                # ÉTAPE 2 : CONSTITUTION DE L'ÉQUIPE SUR-MESURE
                # =================================================================
                agents_actifs = [chef_de_chantier]
                taches_actives = []

                if "ELEC" in resultat_tri:
                    agents_actifs.append(expert_electricien)
                    taches_actives.append(Task(
                        description=f"Projet : '{projet_expert}'. Rédige le descriptif détaillé du lot Électricité. Ajoute la section 'NORMES ET VIGILANCE' (NF C 15-100).",
                        expected_output="Descriptif détaillé du lot Électricité.",
                        agent=expert_electricien
                    ))

                if "PLOMBERIE" in resultat_tri:
                    agents_actifs.append(expert_plombier)
                    taches_actives.append(Task(
                        description=f"Projet : '{projet_expert}'. Rédige le descriptif détaillé du lot Plomberie. Ajoute la section 'NORMES ET VIGILANCE' (DTU 60.1).",
                        expected_output="Descriptif détaillé du lot Plomberie.",
                        agent=expert_plombier
                    ))

                if "PLACO" in resultat_tri:
                    agents_actifs.append(expert_plaquiste)
                    taches_actives.append(Task(
                        description=f"Projet : '{projet_expert}'. Rédige le descriptif détaillé du lot Plâtrerie/Faux-plafond/Enduisage. Ajoute la section 'NORMES ET VIGILANCE' (DTU 25.41).",
                        expected_output="Descriptif détaillé du lot Plâtrerie.",
                        agent=expert_plaquiste
                    ))

                if "CARRELAGE" in resultat_tri:
                    agents_actifs.append(expert_carreleur)
                    taches_actives.append(Task(
                        description=f"Projet : '{projet_expert}'. Rédige le descriptif détaillé du lot Carrelage/Faïence. Ajoute la section 'NORMES ET VIGILANCE' (DTU 52.2).",
                        expected_output="Descriptif détaillé du lot Carrelage.",
                        agent=expert_carreleur
                    ))

                if "PEINTURE" in resultat_tri:
                    agents_actifs.append(expert_peintre)
                    taches_actives.append(Task(
                        description=f"Projet : '{projet_expert}'. Rédige le descriptif détaillé du lot Peinture. Ajoute la section 'NORMES ET VIGILANCE' (DTU 59.1).",
                        expected_output="Descriptif détaillé du lot Peinture.",
                        agent=expert_peintre
                    ))

                if "SOL" in resultat_tri:
                    agents_actifs.append(expert_solier)
                    taches_actives.append(Task(
                        description=f"Projet : '{projet_expert}'. Rédige le descriptif détaillé du lot Sols (hors carrelage). Ajoute la section 'NORMES ET VIGILANCE'.",
                        expected_output="Descriptif détaillé du lot Sols.",
                        agent=expert_solier
                    ))

                if "MENUISERIE" in resultat_tri:
                    agents_actifs.append(expert_menuisier)
                    taches_actives.append(Task(
                        description=f"Projet : '{projet_expert}'. Rédige le descriptif détaillé du lot Menuiserie / Agencement intérieur (pose des meubles, ajustements, quincaillerie).",
                        expected_output="Descriptif détaillé du lot Menuiserie.",
                        agent=expert_menuisier
                    ))

                if "CVC" in resultat_tri:
                    agents_actifs.append(expert_cvc)
                    taches_actives.append(Task(
                        description=f"Projet : '{projet_expert}'. Rédige le descriptif détaillé du lot Chauffage, Ventilation et Climatisation (extraction, VMC, raccordements thermiques).",
                        expected_output="Descriptif détaillé du lot CVC.",
                        agent=expert_cvc
                    ))

                if "ISOLATION" in resultat_tri:
                    agents_actifs.append(expert_isolation)
                    taches_actives.append(Task(
                        description=f"Projet : '{projet_expert}'. Rédige le descriptif détaillé du lot Isolation Thermique (murs, combles, planchers). Mentionne les exigences de résistance thermique (R) et les points de vigilance liés aux ponts thermiques.",
                        expected_output="Descriptif détaillé du lot Isolation.",
                        agent=expert_isolation
                    ))

                if "OUVERTURES" in resultat_tri:
                    agents_actifs.append(expert_ouvertures)
                    taches_actives.append(Task(
                        description=f"Projet : '{projet_expert}'. Rédige le descriptif détaillé du lot Menuiseries Extérieures (fenêtres, baies, portes d'entrée, volets). Précise le type de pose et l'étanchéité.",
                        expected_output="Descriptif détaillé du lot Menuiseries Extérieures.",
                        agent=expert_ouvertures
                    ))

                if "DOMOTIQUE" in resultat_tri:
                    agents_actifs.append(expert_domotique)
                    taches_actives.append(Task(
                        description=f"Projet : '{projet_expert}'. Rédige le descriptif détaillé du lot Domotique / Courants faibles (Réseau VDI, alarme, automatismes, pilotage chauffage).",
                        expected_output="Descriptif détaillé du lot Domotique.",
                        agent=expert_domotique
                    ))

                if "HUMIDITE" in resultat_tri:
                    agents_actifs.append(expert_humidite)
                    taches_actives.append(Task(
                        description=f"Projet : '{projet_expert}'. Rédige le descriptif détaillé du lot Traitement de l'Humidité (remontées capillaires, cuvelage, assèchement). Précise le mode opératoire curatif.",
                        expected_output="Descriptif détaillé du lot Traitement Humidité.",
                        agent=expert_humidite
                    ))

                # Le chef de chantier reprend la main à la fin pour assembler le document
                synthese_devis = Task(
                    description="Prends les rendus de tous les artisans qui viennent d'intervenir. Synthétise-les dans un document final propre, structuré par lots. Ce document doit être rédigé de manière très professionnelle, prêt à être joint à un devis.",
                    expected_output="Un document de synthèse ultra-structuré par lots avec descriptifs, normes et points de vigilance.",
                    agent=chef_de_chantier
                )
                taches_actives.append(synthese_devis)

                # =================================================================
                # ÉTAPE 3 : LANCEMENT DE L'ÉQUIPE (Économique et ciblée)
                # =================================================================
                if len(agents_actifs) > 1: # On vérifie qu'il y a au moins un artisan convoqué
                    reseau_experts = Crew(
                        agents=agents_actifs,
                        tasks=taches_actives,
                        process=Process.sequential,
                        verbose=False
                    )

                    try:
                        resultat_experts = reseau_experts.kickoff()
                        st.success("✅ Document généré avec succès (et à moindre coût) !")
                        
                        # Génération du fichier Word physique
                        nom_fichier_devis = "Synthese_Experts_Devis.docx"
                        completer_fiche_word(str(resultat_experts), nom_fichier=nom_fichier_devis)
                        
                        # Bouton de téléchargement direct
                        with open(nom_fichier_devis, "rb") as file:
                            st.download_button(
                                label="📥 Télécharger la Synthèse Experts au format Word (.docx)",
                                data=file,
                                file_name=nom_fichier_devis,
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                            )
                        st.markdown("---")
                        
                        # Affichage du résultat
                        st.markdown("### 📋 Aperçu de la Synthèse Technique")
                        st.markdown(str(resultat_experts))
                        
                    except Exception as e:
                        st.error("❌ Les serveurs de Google ont saturé. Veuillez patienter quelques minutes et réessayer.")
                else:
                    st.warning("⚠️ Le Chef de Chantier n'a détecté aucun lot correspondant à ta demande. Essaie de détailler davantage les travaux.")
>>>>>>> 9c27fc9fd288468608231c0fe5aa74101f4c21d7
