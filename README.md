# ⛪ Système d'Intégration des Nouveaux Membres

Application web full-stack avec agent IA pour aider les églises ou entreprises à suivre et accompagner l'intégration de leurs nouveaux membres.

---

## 🚀 Fonctionnalités

- **Multi-église** — chaque structure a son propre espace sécurisé avec ses données isolées
- **Tableau de bord** — compteurs en temps réel par statut (Nouveau, Contacté, Intégré...)
- **Gestion des nouveaux** — ajout, fiche individuelle, changement de statut, suppression
- **Gestion des responsables** — attribution d'un responsable à chaque nouveau membre
- **Historique des suivis** — enregistrement de chaque action (appel, message, invitation, présence)
- **Agent IA** — assistant intelligent qui répond en langage naturel et génère des messages personnalisés

---

## 🛠️ Stack technique

| Composant | Technologie |
|---|---|
| Interface web | Python + Streamlit |
| Base de données | Supabase (PostgreSQL) |
| Authentification | Système custom avec session Streamlit |
| Agent IA | Groq API (Llama 3.3 70B) |
| Hébergement | Streamlit Cloud |
| Versioning | GitHub |

---

## 📁 Structure du projet

```
integration_app/
├── main.py                    # Point d'entrée
├── database.py                # Connexion Supabase
├── agent.py                   # Agent IA avec Groq
├── requirements.txt           # Dépendances Python
├── .env                       # Variables d'environnement (non versionné)
└── pages/
    ├── 0_Connexion.py         # Page de connexion
    ├── 1_Tableau_de_bord.py   # Dashboard
    ├── 2_Liste_des_nouveaux.py
    ├── 3_Ajouter_nouveau.py
    ├── 4_Fiche_nouveau.py     # Fiche + historique + suivi
    ├── 5_Responsables.py
    └── 6_Assistant_IA.py      # Chat avec l'agent IA
```

---

## ⚙️ Installation locale

### Prérequis
- Python 3.11
- Un compte [Supabase](https://supabase.com)
- Un compte [Groq](https://console.groq.com)

### Étapes

**1. Cloner le dépôt**
```bash
git clone https://github.com/Asyh03/Integration_app.git
cd Integration_app
```

**2. Créer un environnement virtuel**
```bash
python -m venv venv
source venv/Scripts/activate  # Windows
# source venv/bin/activate    # Mac/Linux
```

**3. Installer les dépendances**
```bash
pip install -r requirements.txt
```

**4. Configurer les variables d'environnement**

Crée un fichier `.env` à la racine :
```
SUPABASE_URL=https://xxxxxxxx.supabase.co
SUPABASE_KEY=ta_cle_anon
GROQ_API_KEY=ta_cle_groq
```

**5. Créer les tables Supabase**

Exécute ce script dans le SQL Editor de Supabase :
```sql
CREATE TABLE eglises (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  nom TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  mot_de_passe TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE responsables (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  nom TEXT NOT NULL,
  telephone TEXT,
  eglise_id UUID REFERENCES eglises(id),
  created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE nouveaux (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  nom TEXT NOT NULL,
  prenom TEXT,
  telephone TEXT,
  tranche_age TEXT,
  date_visite DATE,
  statut TEXT DEFAULT 'Nouveau',
  responsable_id UUID REFERENCES responsables(id),
  eglise_id UUID REFERENCES eglises(id),
  invite_par TEXT,
  created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE suivis (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  nouveau_id UUID REFERENCES nouveaux(id),
  date_action TIMESTAMP DEFAULT now(),
  type_action TEXT,
  commentaire TEXT
);
```

**6. Lancer l'application**
```bash
streamlit run main.py
```

---

## 🌍 Déploiement sur Streamlit Cloud

1. Pousse ton code sur GitHub
2. Va sur [share.streamlit.io](https://share.streamlit.io)
3. Connecte ton dépôt GitHub
4. Dans **Advanced settings → Secrets**, ajoute :
```toml
SUPABASE_URL = "https://xxxxxxxx.supabase.co"
SUPABASE_KEY = "ta_cle_anon"
GROQ_API_KEY = "ta_cle_groq"
```
5. Clique sur **Deploy**

---

## 🤖 Utilisation de l'agent IA

L'agent peut répondre à des questions en langage naturel comme :

- *"Qui n'a pas été contacté cette semaine ?"*
- *"Combien de personnes sont intégrées ?"*
- *"Génère un message de suivi pour Kofi Mensah"*
- *"Donne-moi un résumé de l'intégration ce mois-ci"*

---

## 👨‍💻 Auteur

Projet réalisé par **Samuel AHETO** — Étudiant L2 Informatique  
Projet personnel

---

## 📄 Licence

Ce projet est open source et libre d'utilisation.
