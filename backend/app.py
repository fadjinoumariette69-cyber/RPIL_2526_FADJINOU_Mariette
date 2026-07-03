import os
import re
from datetime import time

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

# 1. Calcul des chemins absolus vers vos dossiers frontend standard
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'frontend'))

# 2. Initialisation UNIQUE de Flask avec la bonne configuration de dossiers
app = Flask(__name__, 
            template_folder=os.path.join(FRONTEND_DIR, 'templates'), 
            static_folder=os.path.join(FRONTEND_DIR, 'static'))

CORS(app)  # Autorise les appels fetch() depuis le frontend

# 3. Connexion à la base de données MySQL (Configuration XAMPP)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost:3306/mentorlink"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# ------------------------------------------------------------------
# Modèle
# ------------------------------------------------------------------

class Mentor(db.Model):
    __tablename__ = "mentors"

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(120), nullable=False)
    matieres = db.Column(db.String(255), nullable=False)          # ex: "Algorithmique,Bases de données"
    disponibilites = db.Column(db.String(255), nullable=False)    # ex: "14:00,16:00,18:30"
    filiere = db.Column(db.String(120), nullable=True)
    format = db.Column(db.String(50), nullable=False)             # "présentiel" | "en ligne" | "les deux"

    def liste_matieres(self):
        return [m.strip() for m in self.matieres.split(",") if m.strip()]

    def liste_horaires(self):
        return [h.strip() for h in self.disponibilites.split(",") if h.strip()]


# ------------------------------------------------------------------
# Utilitaires de matching
# ------------------------------------------------------------------

def parser_heure(valeur):
    """Convertit '14:00', '14h30', '14h' ou '14' en objet time. Retourne None si invalide."""
    valeur = valeur.strip().lower().replace("h", ":")
    if valeur.endswith(":"):
        valeur += "00"
    match = re.match(r"^(\d{1,2})(:(\d{1,2}))?$", valeur)
    if not match:
        return None
    heure = int(match.group(1))
    minute = int(match.group(3)) if match.group(3) else 0
    if not (0 <= heure <= 23 and 0 <= minute <= 59):
        return None
    return time(hour=heure, minute=minute)


def difference_minutes(t1, t2):
    return abs((t1.hour * 60 + t1.minute) - (t2.hour * 60 + t2.minute))


def calculer_score(nb_communes, nb_demandees, meilleur_ecart_minutes, filiere_ok):
    """Score simple sur 100 : 60 pts matières + 30 pts proximité horaire + 10 pts filière."""
    score_matieres = (nb_communes / nb_demandees) * 60 if nb_demandees else 0
    score_horaire = max(0, (60 - meilleur_ecart_minutes) / 60) * 30
    score_filiere = 10 if filiere_ok else 0
    return round(min(100, score_matieres + score_horaire + score_filiere))


def matcher_mentors(matiere_texte, horaire_texte, filiere_texte):
    """
    Règles imposées par le sujet :
    - au moins une matière en commun
    - tolérance horaire de ± 1 heure
    """
    matieres_demandees = [m.strip().lower() for m in matiere_texte.split(",") if m.strip()]
    heure_demandee = parser_heure(horaire_texte)

    if heure_demandee is None:
        raise ValueError("Format d'horaire invalide. Utilisez par exemple 14:00.")

    resultats = []

    for mentor in Mentor.query.all():
        matieres_mentor = mentor.liste_matieres()
        communes = [m for m in matieres_mentor if m.lower() in matieres_demandees]

        if not communes:
            continue

        horaires_mentor = [h for h in (parser_heure(h) for h in mentor.liste_horaires()) if h]
        if not horaires_mentor:
            continue

        meilleur_ecart = min(difference_minutes(heure_demandee, h) for h in horaires_mentor)

        if meilleur_ecart > 60:  # tolérance ± 1 heure stricte
            continue

        filiere_ok = bool(
            filiere_texte and mentor.filiere and
            filiere_texte.strip().lower() == mentor.filiere.strip().lower()
        )

        score = calculer_score(
            nb_communes=len(communes),
            nb_demandees=len(matieres_demandees),
            meilleur_ecart_minutes=meilleur_ecart,
            filiere_ok=filiere_ok,
        )

        resultats.append({
            "nom": mentor.nom,
            "matieres_communes": communes,
            "disponibilites": mentor.disponibilites,
            "format": mentor.format,
            "score": score,
        })

    resultats.sort(key=lambda m: m["score"], reverse=True)
    return resultats


# ------------------------------------------------------------------
# Routes
# ------------------------------------------------------------------

# AJOUT DE LA ROUTE PRINCIPALE : Permet d'ouvrir le fichier index.html
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/match", methods=["POST"])
def api_match():
    donnees = request.get_json(silent=True) or {}

    matiere = (donnees.get("matiere") or "").strip()
    horaire = (donnees.get("horaire") or "").strip()
    filiere = (donnees.get("filiere") or "").strip()

    if not matiere or not horaire:
        return jsonify({"erreur": "La matière et l'horaire sont obligatoires."}), 400

    try:
        mentors = matcher_mentors(matiere, horaire, filiere)
    except ValueError as e:
        return jsonify({"erreur": str(e)}), 400

    return jsonify({"mentors": mentors})


# ------------------------------------------------------------------
# Commande CLI pour initialiser et peupler la base
# ------------------------------------------------------------------

@app.cli.command("init-db")
def init_db():
    db.create_all()

    if Mentor.query.count() == 0:
        db.session.add_all([
            Mentor(
                nom="Awa Chabi",
                matieres="Algorithmique,Structures de données,Python",
                disponibilites="14:00,16:00",
                filiere="Licence IA",
                format="en ligne",
            ),
            Mentor(
                nom="Kévin Dossou",
                matieres="Bases de données,SQL,Modélisation",
                disponibilites="09:00,10:30,18:00",
                filiere="Licence GL",
                format="présentiel",
            ),
            Mentor(
                nom="Sandrine Houngbo",
                matieres="Réseaux,Sécurité,Linux",
                disponibilites="13:00,15:30",
                filiere="Licence SE&IoT",
                format="les deux",
            ),
            Mentor(
                nom="Marc Agbodjan",
                matieres="Python,Intelligence artificielle,Machine Learning",
                disponibilites="17:00,19:00",
                filiere="Licence IA",
                format="en ligne",
            ),
        ])
        db.session.commit()
        print("Base initialisée avec 4 mentors.")
    else:
        print("Des mentors existent déjà, aucune donnée ajoutée.")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
