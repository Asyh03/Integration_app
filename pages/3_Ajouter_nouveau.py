import streamlit as st
from database import supabase

# Vérifier si connecté
if "eglise" not in st.session_state:
    st.switch_page("pages/0_Connexion.py")

eglise_id = st.session_state.eglise["id"]

st.title("➕ Ajouter un nouveau")

# Récupérer la liste des responsables filtrés par église
responsables = supabase.table("responsables").select("*").eq("eglise_id", eglise_id).execute().data

# Créer un dictionnaire nom -> id
responsables_dict = {r["nom"]: r["id"] for r in responsables}

# Formulaire
with st.form("ajouter_nouveau"):
    nom = st.text_input("Nom *")
    prenom = st.text_input("Prénom")
    telephone = st.text_input("Téléphone")
    tranche_age = st.selectbox("Tranche d'âge", ["", "moins de 15", "16-20", "21-30", "31-40", "41-50", "50+"])
    date_visite = st.date_input("Date de première visite")
    invite_par = st.text_input("Invité par")
    responsable = st.selectbox("Responsable de suivi", [""] + list(responsables_dict.keys()))

    soumettre = st.form_submit_button("Ajouter")

    if soumettre:
        if not nom:
            st.error("Le nom est obligatoire !")
        else:
            nouveau = {
                "nom": nom,
                "prenom": prenom,
                "telephone": telephone,
                "tranche_age": tranche_age,
                "date_visite": str(date_visite),
                "invite_par": invite_par,
                "statut": "Nouveau",
                "eglise_id": eglise_id,
            }

            if responsable:
                nouveau["responsable_id"] = responsables_dict[responsable]

            supabase.table("nouveaux").insert(nouveau).execute()
            st.success(f"{prenom} {nom} a été ajouté avec succès ! ✅")