import streamlit as st
from database import supabase

# Vérifier si connecté
if "eglise" not in st.session_state:
    st.switch_page("pages/0_Connexion.py")

eglise_id = st.session_state.eglise["id"]

st.title("📋 Fiche d'un nouveau")

data = supabase.table("nouveaux").select("*").eq("eglise_id", eglise_id).execute().data

if not data:
    st.info("Aucune personne enregistrée.")
else:
    noms = {f"{n['prenom']} {n['nom']}": n for n in data}
    choix = st.selectbox("Choisir une personne", list(noms.keys()))
    personne = noms[choix]

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Informations personnelles")
        st.write(f"**Nom :** {personne['nom']}")
        st.write(f"**Prénom :** {personne['prenom']}")
        st.write(f"**Téléphone :** {personne['telephone']}")
        st.write(f"**Tranche d'âge :** {personne['tranche_age']}")
        st.write(f"**Invité par :** {personne['invite_par']}")
        st.write(f"**Date de visite :** {personne['date_visite']}")

    with col2:
        st.subheader("Suivi")
        st.write(f"**Statut :** {personne['statut']}")

        statuts = ["Nouveau", "Contacté", "Revient régulièrement", "Intégré", "Inactif"]
        nouveau_statut = st.selectbox("Changer le statut", statuts, index=statuts.index(personne['statut']))

        if st.button("Mettre à jour le statut"):
            supabase.table("nouveaux").update({"statut": nouveau_statut}).eq("id", personne["id"]).execute()
            st.success("Statut mis à jour ! ✅")
            st.rerun()

    st.divider()

    if "confirmer_suppression" not in st.session_state:
        st.session_state.confirmer_suppression = False

    if st.button("🗑️ Supprimer cette personne"):
        st.session_state.confirmer_suppression = True

    if st.session_state.confirmer_suppression:
        st.warning(f"Es-tu sûr de vouloir supprimer {personne['prenom']} {personne['nom']} ?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Oui, supprimer"):
                supabase.table("suivis").delete().eq("nouveau_id", personne["id"]).execute()
                supabase.table("nouveaux").delete().eq("id", personne["id"]).execute()
                st.session_state.confirmer_suppression = False
                st.success("Personne supprimée ! ✅")
                st.rerun()
        with col2:
            if st.button("❌ Annuler"):
                st.session_state.confirmer_suppression = False
                st.rerun()

    st.divider()

    st.subheader("📅 Historique des suivis")
    suivis = supabase.table("suivis").select("*").eq("nouveau_id", personne["id"]).order("date_action", desc=True).execute().data

    if suivis:
        for s in suivis:
            col1, col2 = st.columns([1, 3])
            col1.write(f"**{s['type_action']}**")
            col1.caption(s['date_action'][:10])
            col2.write(s['commentaire'])
            st.divider()
    else:
        st.info("Aucun suivi enregistré pour cette personne.")

    st.subheader("➕ Ajouter un suivi")
    with st.form("ajouter_suivi"):
        type_action = st.selectbox("Type d'action", ["Appel", "Message", "Invitation", "Présence"])
        commentaire = st.text_area("Commentaire")
        soumettre = st.form_submit_button("Enregistrer")

        if soumettre:
            if not commentaire:
                st.error("Le commentaire est obligatoire !")
            else:
                supabase.table("suivis").insert({
                    "nouveau_id": personne["id"],
                    "type_action": type_action,
                    "commentaire": commentaire
                }).execute()
                st.success("Suivi enregistré ! ✅")
                st.rerun()