# Berliner Weg — Site vitrine

Site vitrine Flask pour le centre de langue allemande Berliner Weg (Yaoundé), avec prise de rendez-vous par email.

## Pages

- `/` — Accueil
- `/a-propos` — À propos
- `/cours` — Nos cours (niveaux et tarifs)
- `/services` — Nos services
- `/rendez-vous` — Formulaire de prise de rendez-vous (envoie un email au centre + confirmation au client)
- `/contact` — Coordonnées et carte

## Installation

```bash
python3 -m venv venv
source venv/bin/activate        # Windows : venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration de l'email (Gmail)

1. Copiez `.env.example` en `.env` :
   ```bash
   cp .env.example .env
   ```
2. Activez la validation en 2 étapes sur le compte Gmail qui enverra les emails.
3. Générez un **mot de passe d'application** :
   - Allez sur https://myaccount.google.com/apppasswords
   - Créez un mot de passe pour "Mail" / "Autre (nom personnalisé)"
   - Copiez le mot de passe généré (16 caractères)
4. Remplissez `.env` :
   ```
   MAIL_USERNAME=votre-adresse@gmail.com
   MAIL_PASSWORD=le-mot-de-passe-application-genere
   CENTRE_EMAIL=adresse-qui-recoit-les-rdv@gmail.com
   ```

⚠️ Ne jamais utiliser votre mot de passe Gmail habituel : Google le bloque pour les connexions SMTP externes. Le mot de passe d'application est obligatoire.

## Lancer le site

```bash
python app.py
```

Le site est accessible sur http://127.0.0.1:5000

## Déploiement

Pour la mise en production, utilisez un serveur WSGI (ex: `gunicorn app:app`) derrière Nginx, et définissez les variables d'environnement sur le serveur (ne pas committer `.env`).
