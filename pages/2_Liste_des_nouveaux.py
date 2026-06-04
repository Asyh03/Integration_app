import streamlit as st
from database import supabase

st.title("👥 Liste des nouveaux")

# Récupérer les données
data = supabase.table("nouveaux").select("*").execute().data

#filtre par défaut
statuts = ["Tous","Nouveau","Contacté", "Revient régulièrement", "Intégré","Inactif"]
filtre = st.selectbox("Filtrer par defaut", statuts)

#Appliquer le filtre
if filtre != "Tous":
    data = [n for n in data if n["statut"] == filtre]

#Afficher le tableau 
if data :
    st.dataframe(
        data,
        column_config={
            "id": None,
            "responsable_id" : None,
            "created_at": None,
            "nom": "Nom",
            "prenom" : "Prénom", 
            "telephone": "Téléphone",
            "tranche_age" :"Tranche d'Age",
            "date_de_visite": "Date de visite",
            "invite_par" : "Comment as-tu connu ICC",

        },

        use_container_width = True
    )
    st.caption(f"{len(data)} personne(s) trouvée(s)")
else :
    st.info("Aucune personne trouvée pour cet statut.")