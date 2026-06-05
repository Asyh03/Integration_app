import streamlit as st
from agent import poser_question

st.title("🤖 Assistant IA")
st.caption("Pose une question en français sur les nouveaux membres")

# Initialiser l'historique de conversation
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
    # Afficher la question
    with st.chat_message("user"):
        st.write(question)

    # Obtenir la réponse
    with st.chat_message("assistant"):
        with st.spinner("Réflexion en cours..."):
            reponse = poser_question(question, st.session_state.historique)
            st.write(reponse)

    # Sauvegarder dans l'historique
    st.session_state.historique.append({"role": "user", "content": question})
    st.session_state.historique.append({"role": "assistant", "content": reponse})