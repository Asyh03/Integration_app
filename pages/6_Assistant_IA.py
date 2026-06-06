import streamlit as st
from agent import poser_question

# Vérifier si connecté
if "eglise" not in st.session_state:
    st.switch_page("pages/0_Connexion.py")

eglise_id = st.session_state.eglise["id"]
eglise_nom = st.session_state.eglise["nom"]

st.title("🤖 Assistant IA")
st.caption(f"Assistant de {eglise_nom}")

# Initialiser l'historique
if "historique" not in st.session_state:
    st.session_state.historique = []

# Afficher l'historique
for message in st.session_state.historique:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.write(message["content"])
    else:
        with st.chat_message("assistant"):
            st.write(message["content"])

# Champ de saisie
question = st.chat_input("Ex: Qui n'a pas été contacté ? Génère un message pour Kofi...")

if question:
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Réflexion en cours..."):
            reponse = poser_question(question, st.session_state.historique, eglise_id)
            st.write(reponse)

    st.session_state.historique.append({"role": "user", "content": question})
    st.session_state.historique.append({"role": "assistant", "content": reponse})