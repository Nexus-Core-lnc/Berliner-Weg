import os
from datetime import datetime, timedelta

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__,template_folder="../templates", static_folder="../static")
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")

# --- Config email (Gmail SMTP) ---
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")  # mot de passe d'application Gmail
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_USERNAME")

# Adresse qui reçoit les demandes de rendez-vous (peut être différente de l'expéditeur)
CENTRE_EMAIL = os.environ.get("CENTRE_EMAIL", app.config["MAIL_USERNAME"])

mail = Mail(app)

NIVEAUX = [
    {"code": "A1-A2", "label": "A1 – A2", "desc": "Initiation et communication de base", "prix": "100 000 FCFA"},
    {"code": "B1-B2", "label": "B1 – B2", "desc": "Expression fluide, compréhension avancée", "prix": "120 000 FCFA"},
    {"code": "C1-C2", "label": "C1 – C2", "desc": "Perfectionnement et préparation universitaire", "prix": "130 000 FCFA"},
    {"code": "VORB", "label": "Vorbereitungskurs", "desc": "Révisions intensives avant examen", "prix": "20 000 FCFA"},
]

SERVICES = [
    {"titre": "Accompagnement Visa", "desc": "Constitution du dossier, préparation aux entretiens, suivi de A à Z."},
    {"titre": "Cours Intensifs", "desc": "Programmes accélérés pour atteindre rapidement le niveau requis."},
    {"titre": "Formation en Ligne", "desc": "Cours à distance avec supports vidéo, audio et tutoriels."},
    {"titre": "Traduction / Interprétation", "desc": "Traduction de documents officiels et interprétariat."},
    {"titre": "Orientation Emploi", "desc": "Aide à l'orientation vers le marché du travail allemand."},
    {"titre": "Formation Soins Infirmiers", "desc": "Préparation aux filières infirmières très demandées en Allemagne."},
]


@app.context_processor
def inject_globals():
    return {"niveaux": NIVEAUX, "now": datetime.now()}


@app.route("/")
def accueil():
    return render_template("index.html")


@app.route("/a-propos")
def apropos():
    return render_template("apropos.html")


@app.route("/cours")
def cours():
    return render_template("cours.html")


@app.route("/services")
def services():
    return render_template("services.html", services=SERVICES)


@app.route("/rendez-vous", methods=["GET", "POST"])
def rendez_vous():
    if request.method == "POST":
        nom = request.form.get("nom", "").strip()
        email = request.form.get("email", "").strip()
        telephone = request.form.get("telephone", "").strip()
        niveau = request.form.get("niveau", "").strip()
        date_rdv = request.form.get("date_rdv", "").strip()
        message_client = request.form.get("message", "").strip()

        # Validation simple
        if not nom or not email or not date_rdv:
            flash("Merci de renseigner au moins votre nom, votre email et une date souhaitée.", "error")
            return redirect(url_for("rendez_vous"))

        try:
            # Email au centre
            msg_centre = Message(
                subject=f"Nouvelle demande de rendez-vous - {nom}",
                recipients=[CENTRE_EMAIL],
            )
            msg_centre.body = (
                f"Nouvelle demande de rendez-vous reçue via le site :\n\n"
                f"Nom : {nom}\n"
                f"Email : {email}\n"
                f"Téléphone : {telephone or 'non renseigné'}\n"
                f"Niveau souhaité : {niveau or 'non précisé'}\n"
                f"Date/heure souhaitée : {date_rdv}\n"
                f"Message : {message_client or 'aucun'}\n"
            )
            mail.send(msg_centre)

            # Email de confirmation au client
            msg_client = Message(
                subject="Confirmation de votre demande de rendez-vous - Berliner Weg",
                recipients=[email],
            )
            msg_client.body = (
                f"Bonjour {nom},\n\n"
                f"Nous avons bien reçu votre demande de rendez-vous pour le {date_rdv}.\n"
                f"Notre équipe vous contactera très prochainement pour confirmer.\n\n"
                f"À bientôt,\nL'équipe Berliner Weg\n"
                f"En face BICEC Biyem-Assi, Yaoundé\n"
                f"WhatsApp : +237 686 17 03 74"
            )
            mail.send(msg_client)

            flash("Votre demande a bien été envoyée ! Vous recevrez une confirmation par email.", "success")
        except Exception as e:
            app.logger.error(f"Erreur envoi email: {e}")
            flash(
                "Votre demande n'a pas pu être envoyée automatiquement. "
                "Contactez-nous directement au WhatsApp +237 686 17 03 74.",
                "error",
            )

        return redirect(url_for("rendez_vous"))

    return render_template("rdv.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
