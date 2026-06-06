import streamlit as st
from database import supabase

# Si déjà connecté, rediriger
if "eglise" in st.session_state:
    st.switch_page("main.py")

st.title("⛪ Bienvenue")

# Onglets Connexion / Inscription
onglet1, onglet2 = st.tabs(["Se connecter", "Créer un compte"])

# ── CONNEXION ──
with onglet1:
    st.subheader("Connexion")
    with st.form("connexion"):
        email = st.text_input("Email")
        mot_de_passe = st.text_input("Mot de passe", type="password")
        soumettre = st.form_submit_button("Se connecter")

        if soumettre:
            if not email or not mot_de_passe:
                st.error("Veuillez remplir tous les champs !")
            else:
                result = supabase.table("eglises").select("*").eq("email", email).eq("mot_de_passe", mot_de_passe).execute().data

                if result:
                    eglise = result[0]
                    st.session_state.eglise = eglise
                    st.success(f"Bienvenue {eglise['nom']} ! ✅")
                    st.switch_page("main.py")
                else:
                    st.error("Email ou mot de passe incorrect !")

# ── INSCRIPTION ──
with onglet2:
    st.subheader("Créer un compte")
    with st.form("inscription"):
        nom = st.text_input("Nom de l'église *")
        email = st.text_input("Email *")
        mot_de_passe = st.text_input("Mot de passe *", type="password")
        confirmer = st.text_input("Confirmer le mot de passe *", type="password")
        soumettre = st.form_submit_button("Créer le compte")

        if soumettre:
            if not nom or not email or not mot_de_passe or not confirmer:
                st.error("Veuillez remplir tous les champs !")
            elif mot_de_passe != confirmer:
                st.error("Les mots de passe ne correspondent pas !")
            else:
                # Vérifier si l'email existe déjà
                existant = supabase.table("eglises").select("id").eq("email", email).execute().data

                if existant:
                    st.error("Cet email est déjà utilisé !")
                else:
                    supabase.table("eglises").insert({
                        "nom": nom,
                        "email": email,
                        "mot_de_passe": mot_de_passe
                    }).execute()
                    st.success("Compte créé avec succès ! Connectez-vous maintenant ✅")
