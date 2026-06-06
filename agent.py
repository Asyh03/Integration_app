from groq import Groq
import os
from dotenv import load_dotenv
from database import supabase

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def lire_nouveaux(eglise_id):
    return supabase.table("nouveaux").select("*").eq("eglise_id", eglise_id).execute().data

def compter_par_statut(eglise_id):
    data = lire_nouveaux(eglise_id)
    compteurs = {}
    for n in data:
        statut = n["statut"]
        compteurs[statut] = compteurs.get(statut, 0) + 1
    return compteurs

def poser_question(question, historique=[], eglise_id=None):
    nouveaux = lire_nouveaux(eglise_id)
    statistiques = compter_par_statut(eglise_id)

    system_prompt = f"""Tu es un assistant intelligent qui aide les responsables d'une église
à suivre l'intégration des nouveaux membres.

Voici les données actuelles :
- Liste des nouveaux : {nouveaux}
- Statistiques par statut : {statistiques}

Réponds toujours en français, de manière claire et concise.
Si on te demande de générer un message, génère un message chaleureux et personnalisé."""

    messages = [{"role": "system", "content": system_prompt}] + historique + [{"role": "user", "content": question}]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=1000
    )

    return response.choices[0].message.content