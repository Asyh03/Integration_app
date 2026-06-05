import streamlit as st
from database import supabase

st.title("Fiche d'un nouveau")

#Récupérer tous les nouveaux
data = supabase.table("nouveaux").select("*").execute().data

if not data :
    st.info("Aucune personne enregistrée;")
else :
    #Menu de selection
    noms = {f"{n['prenom']} {n['nom']}": n for n in data}
    choix = st.selectbox("Choisir une personne", list(noms.keys()))
    personne = noms[choix]

    #Afficher la fiche
    col1, col2 = st.columns(2)

    with col1 :
        st.subheader("Informations personnelles")
        st.write(f"**Nom:** {personne['nom']}")
        st.write(f"**Prénom :** {personne['prenom']}")
        st.write(f"**Téléphone :** {personne['telephone']}")
        st.write(f"**Tranche d'âge :** {personne['tranche_age']}")
        st.write(f"**Invité par :** {personne['invite_par']}")
        st.write(f"**Date de visite :** {personne['date_visite']}")
    with col2 :
        st.subheader("Suivi")
        st.write(f"**Statut :** {personne['statut']}")

        #Changer le statut
        statuts = ["Tous","Nouveau","Contacté", "Revient régulièrement", "Intégré","Inactif"]
        nouveau_statut = st.selectbox("Changer el statut", statuts, index = statuts.index(personne['statut']))

        if st.button("Mettre à jour le statut"):
            supabase.table("nouveaux").update({"statut": nouveau_statut}).eq("id", personne["id"]).execute()
            st.success("Statut mis à jour ! ✅")
            st.rerun()
    st.divider()

    #Historique des suivis
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Ajouter une action")

        with st.form("ajouter_suivi") :
            type_action = st.selectbox("Type d'action",["appel","message","invitation","presence"])
            commentaire = st.text_area("Commentaire")
            soumettre = st.form_submit_button("Enregistrer")

            if soumettre :
                supabase.table("suivis").insert({
                    "nouveau_id": personne["id"],
                    "type_action": type_action,
                    "commentaire": commentaire
                }).execute()
                st.success("Action enregistrée")
                st.rerun()
    with col2 :
        st.subheader("Historique")

        suivis = supabase.table("suivis").select("*").eq("nouveau_id", personne["id"]).order("date_action",desc=True).execute().data

        if suivis :
            for s in suivis :
                st.write(f"**{s['type_action'].upper()}** - {s['date_action'][:10]}")
                st.caption(s['commentaire'])
                st.divider()

        else :
            st.info("Aucune action enregistrée.")