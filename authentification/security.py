# authentification/security.py
import jwt
from datetime import datetime
from django.conf import settings
from ninja.security import HttpBearer
from .models import Utilisateur, BlacklistedToken

class JWTAuth(HttpBearer):
    def authenticate(self, request, token: str):
        try:
            # Vérifier si le token est en liste noire
            if BlacklistedToken.objects.filter(token=token).exists():
                return None # Token révoqué

            # Décoder le token
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            user_id = payload.get('user_id')
            exp_timestamp = payload.get('exp')

            if not user_id or not exp_timestamp:
                return None # Payload invalide

            # Vérifier l'expiration
            if datetime.fromtimestamp(exp_timestamp) < datetime.utcnow():
                return None # Token expiré

            # Récupérer l'utilisateur
            user = Utilisateur.objects.get(id_utilisateur=user_id)
            return user # Retourne l'objet utilisateur si valide

        except jwt.ExpiredSignatureError:
            return None # Token expiré
        except jwt.InvalidTokenError:
            return None # Token invalide
        except Utilisateur.DoesNotExist:
            return None # Utilisateur non trouvé
        except Exception as e:
            # Log l'erreur pour le débogage
            print(f"Erreur d'authentification JWT: {e}")
            return None
