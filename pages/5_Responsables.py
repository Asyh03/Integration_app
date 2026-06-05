import streamlit as st
from database import supabase

st.title("Gestion des responsables")

#Récuperation des données
responsables = supabase.table("responsables").select("*").execute().data

#afficher la liste

if responsables :
    for r in responsables :
        #compter les personnes suivies
        suivis = supabase.table("nouveaux").select("id").eq("responsable_id", r["id"]).execute().data
        nb_suivis = len(suivis)

        col1,col2,col3 = st.columns([3, 2, 1])
        col1.write(f"**{r['nom']}**")
        col2.write(f" {r['telephone']}")
        col3.write(f"{nb_suivis} personnes(s)")
        st.divider()
else:
    st.info("Aucun responsable enregistré")

#Formulaire d'ajout
st.subheader("Ajouter un responsable") 

with st.form("ajouter_responsable") :
    nom = st.text_input("Nom *")
    telephone = st.text_input("Téléphone")
    soumettre = st.form_submit_button("Ajouter")

    if soumettre :
        if not nom :
            st.error("Le nom est obligatoire !")
        else :
            supabase.table("responsables").insert({
                "nom": nom,
                "telephone": telephone
            }).execute()
            st.success(f"{nom} a été ajouté comme responsable !")
            st.rerun()
