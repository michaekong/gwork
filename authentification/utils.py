# authentification/utils.py
import jwt
from datetime import datetime, timedelta
from django.conf import settings
# CHANGEMENT: Utiliser TimestampSigner au lieu de Signer
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from django.core.mail import send_mail
import logging

logger = logging.getLogger(__name__)

# --- Fonctions utilitaires JWT ---
def create_jwt_token(user) -> str:
    payload = {
        'user_id': str(user.id_utilisateur),
        'exp': datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRATION_TIME_HOURS),
        'iat': datetime.utcnow()
    }
    jwt_token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return jwt_token

# --- Fonctions de vérification d'email ---
# CHANGEMENT: Initialisation de TimestampSigner
# La durée de vie (max_age) est implicitement gérée par TimestampSigner lors de l'unsign
signer = TimestampSigner(key=settings.SECRET_KEY, salt=settings.EMAIL_VERIFICATION_SALT)

def generate_verification_token(user_email: str) -> str:
    """
    Génère un token signé pour la vérification d'email.
    """
    return signer.sign(user_email)

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_verification_email(user_email: str, token: str):
    """
    Envoie un email de vérification à l'utilisateur.
    """
    verification_link = f"{settings.FRONTEND_URL}/verify-email/?token={token}"
    
    # Création du contenu HTML de l'email
    subject = 'Vérifiez votre adresse email pour G-work'
    html_message = render_to_string('email_verification_template.html', {
        'verification_link': verification_link,
        'user_email': user_email,
    })
    plain_message = f"Pour {user_email}, veuillez vérifier votre email en cliquant sur ce lien : {verification_link}"
    
    # Affichage dans la console pour le débogage (facultatif)
    print(f"--- EMAIL DE VÉRIFICATION ---")
    print(f"Pour {user_email}, veuillez vérifier votre email en cliquant sur ce lien :")
    print(verification_link)
    print(f"---------------------------")

    try:
        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [user_email],
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"Email de vérification envoyé à {user_email}")
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi de l'email de vérification à {user_email}: {e}")
