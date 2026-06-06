import streamlit as st

# Vérifier si connecté
if "eglise" not in st.session_state:
    st.switch_page("pages/0_Connexion.py")

st.set_page_config(
    page_title="Intégration Église",
    page_icon="⛪",
    layout="wide"
)

eglise = st.session_state.eglise

st.title(f"⛪ {eglise['nom']}")
st.write(f"Bienvenue sur votre espace de suivi des nouveaux membres.")

# Bouton déconnexion
if st.sidebar.button("🚪 Se déconnecter"):
    del st.session_state.eglise
    st.switch_page("pages/0_Connexion.py")