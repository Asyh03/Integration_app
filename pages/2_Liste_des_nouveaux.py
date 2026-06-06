import streamlit as st
from database import supabase

# Vérifier si connecté
if "eglise" not in st.session_state:
    st.switch_page("pages/0_Connexion.py")

eglise_id = st.session_state.eglise["id"]

st.title("👥 Liste des nouveaux")

# Récupérer les données filtrées par église
data = supabase.table("nouveaux").select("*").eq("eglise_id", eglise_id).execute().data

# Filtre par statut
statuts = ["Tous", "Nouveau", "Contacté", "Revient régulièrement", "Intégré", "Inactif"]
filtre = st.selectbox("Filtrer par statut", statuts)

# Appliquer le filtre
if filtre != "Tous":
    data = [n for n in data if n["statut"] == filtre]

# Afficher le tableau
if data:
    st.dataframe(
        data,
        column_config={
            "id": None,
            "responsable_id": None,
            "created_at": None,
            "eglise_id": None,
            "nom": "Nom",
            "prenom": "Prénom",
            "telephone": "Téléphone",
            "tranche_age": "Tranche d'âge",
            "date_visite": "Date de visite",
            "statut": "Statut",
            "invite_par": "Invité par",
        },
        use_container_width=True
    )
    st.caption(f"{len(data)} personne(s) trouvée(s)")
else:
    st.info("Aucune personne trouvée pour ce statut.")