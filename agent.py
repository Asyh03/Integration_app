from groq import Groq
import os
from dotenv import load_dotenv
from database import supabase

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ── OUTILS QUE L'AGENT PEUT UTILISER ──
def lire_nouveaux():
    data = supabase.table("nouveaux").select("*").execute().data
    return data

def compter_par_statut():
    data = supabase.table("nouveaux").select("*").execute().data
    compteurs = {}
    for n in data:
        statut = n["statut"]
        compteurs[statut] = compteurs.get(statut, 0) + 1
    return compteurs

def lire_suivis(nouveau_id):
    data = supabase.table("suivis").select("*").eq("nouveau_id", nouveau_id).execute().data
    return data

# ── FONCTION PRINCIPALE DE L'AGENT ──
def poser_question(question, historique=[]):
    nouveaux = lire_nouveaux()
    statistiques = compter_par_statut()

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