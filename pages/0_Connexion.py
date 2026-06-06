import streamlit as st
from database import supabase

# Si déjà connecté, rediriger
if "eglise" in st.session_state:
    st.switch_page("main.py")

st.title("⛪ Connexion")
st.subheader("Connectez-vous à votre espace")

with st.form("connexion"):
    email = st.text_input("Email")
    mot_de_passe = st.text_input("Mot de passe", type="password")
    soumettre = st.form_submit_button("Se connecter")

    if soumettre:
        if not email or not mot_de_passe:
            st.error("Veuillez remplir tous les champs !")
        else:
            # Vérifier les credentials
            result = supabase.table("eglises").select("*").eq("email", email).eq("mot_de_passe", mot_de_passe).execute().data

            if result:
                eglise = result[0]
                st.session_state.eglise = eglise
                st.success(f"Bienvenue {eglise['nom']} ! ✅")
                st.switch_page("main.py")
            else:
                st.error("Email ou mot de passe incorrect !")