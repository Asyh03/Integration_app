import streamlit as st 
from database import supabase

#Vérifier si connecté
if "eglise" not in st.session_state :
    st.switch_page("pages/0_connexion.py")

eglise_id = st.session_state.eglise["id"]

st.title("Tableau de bord")

#Recuperation de toutes les données
data = supabase.table("nouveaux").select("*").execute().data

#filtre le nombre par statut
total = len(data)
nouveau = len([n for n in data if n["statut"] == "Nouveau"])
contacte = len([n for n in data if n["statut"] == "Contacté"])
integre = len([n for n in data if n["statut"] == "Integre"])
inactif = len([n for n in data if n["statut"] == "inactif"])

#Afficher les compteurs
col1,col2,col3,col4,col5 = st.columns(5)

col1.metric("Total",total)
col2.metric("Nouveau",nouveau)
col3.metric("Contacté",contacte)
col4.metric("Integré", integre)
col5.metric("Inactif",inactif)
