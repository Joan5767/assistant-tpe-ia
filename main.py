import os
from crewai import Agent, Task, Crew

# Configuration du modèle (N'oublie pas de remettre ta clé)
os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

# 1. Entrée dynamique de l'email
print("\n--- ARRIVÉE D'UN NOUVEL EMAIL CLIENT ---")
email_recu = input("Colle l'email du prospect ici puis appuie sur Entrée : \n")

# =====================================================================
# ÉTAPE 2 : DÉFINITION DES AGENTS (L'ÉQUIPE)
# =====================================================================

# Agent 1 : Le Commercial
assistant_commercial = Agent(
    role='Assistant Commercial Rénovation',
    goal='Qualifier les demandes de travaux et préparer la relation client',
    backstory="""Tu es le premier filtre de l'entreprise. Tu extrais les données clés 
    et tu rédiges une réponse polie pour demander les pièces manquantes.""",
    verbose=True,
    llm='gemini/gemini-2.5-flash',
    allow_delegation=False
)

# Agent 2 : Le Directeur Technique (LE NOUVEAU)
expert_technique = Agent(
    role='Directeur Technique Rénovation TCE',
    goal='Identifier les risques techniques, réglementaires et les opportunités d\'aides d\'un projet',
    backstory="""Tu as 20 ans de bouteille dans le bâtiment et la rénovation tous corps d'état. 
    Tu connais les pièges des chantiers (porteurs, amiante, isolations ratées) et les réglementations 
    sur les passoires thermiques (DPE G, F) ainsi que les aides de l'État.""",
    verbose=True,
    llm='gemini/gemini-2.5-flash',
    allow_delegation=False
)

# =====================================================================
# ÉTAPE 3 : DÉFINITION DES TÂCHES (LE FLUX DE TRAVAIL)
# =====================================================================

# Tâche 1 pour le Commercial
tache_commerciale = Task(
    description=f"""Analyse cet email client : '{email_recu}'.
    1. Liste les travaux.
    2. Note la surface.
    3. Rédige le brouillon de réponse pour demander photos/plans.""",
    expected_output="Un compte-rendu commercial clair et un brouillon d'email.",
    agent=assistant_commercial
)

# Tâche 2 pour l'Expert Technique (Elle va utiliser le travail de la tâche 1)
tache_technique = Task(
    description="""Lis le compte-rendu commercial qui vient d'être généré pour ce projet. Rédige une note interne technique ultra-précise destinée au Chargé d'Affaires (le boss).
    Cette note doit :
    1. Alerter sur les points de vigilance techniques obligatoires liés aux travaux demandés (ex: si cloison -> vérifier si porteur, si isolation + DPE G -> parler de l'audit obligatoire ou des aides).
    2. Lister les 3 questions techniques cruciales à poser au client lors du premier rendez-vous téléphonique pour verrouiller le dossier.""",
    expected_output="Une note technique interne de vigilance avec les alertes et les questions clés à poser.",
    agent=expert_technique
)

# =====================================================================
# ÉTAPE 4 : LE CHEF D'ORCHESTRE (LE CREW)
# =====================================================================
# L'ordre dans la liste "tasks" est CRUCIAL. CrewAI va les exécuter l'une après l'autre.
ma_tpe_virtuelle = Crew(
    agents=[assistant_commercial, expert_technique],
    tasks=[tache_commerciale, tache_technique],
    verbose=True
)

# Lancement
print("\nLancement de l'équipe... Les agents collaborent.\n")
resultat_final = ma_tpe_virtuelle.kickoff()

print("\n================ LIVRABLE FINAL ENVOYÉ PAR L'ÉQUIPE ================\n")
print(resultat_final)