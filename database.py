from supabase import create_client
from dotenv import load_dotenv
import os

#Charger les variables du fichier .env avec le chemin absolu
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

#Récupérer les clés 
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


# Vérification
print("URL:", SUPABASE_URL)
print("KEY:", SUPABASE_KEY)

#Creer la connexion
supabase = create_client(SUPABASE_URL,SUPABASE_KEY)