# authentification/api.py
from datetime import datetime, timedelta
from django.contrib.auth.hashers import check_password, make_password
from django.utils import timezone
from ninja import NinjaAPI, errors
from django.core.signing import SignatureExpired, BadSignature
from django.shortcuts import get_object_or_404
from django.conf import settings
import uuid 
import jwt
# Import des modèles
from .models import Utilisateur, Travailleur, Employeur, BlacklistedToken
# Import des schémas
from .schemas import (
    EstablishmentAuthPayload,
    TravailleurRegisterPayload,
    EmployeurRegisterPayload,
    TokenResponse,
    UserProfileResponse,
    MessageResponse,
    UserListResponse
)
# Import de la sécurité (JWTAuth)
from .security import JWTAuth
# Import des utilitaires, y compris l'instance 'signer'
from .utils import create_jwt_token, generate_verification_token, send_verification_email, signer

# --- Initialisation de l'API Ninja ---
api = NinjaAPI(
    title="API d'Authentification G-work",
    version="1.0.0",
    description="API pour la gestion des utilisateurs et l'authentification de G-work."
)

# --- Endpoints d'Authentification ---

@api.get("/auth/verify-email/", response=MessageResponse)
def verify_email(request, token: str):
    """
    Vérifie l'adresse email de l'utilisateur à l'aide d'un token.
    """
    try:
        # L'instance 'signer' est importée de utils.py, pas besoin de la recréer ici.
        email = signer.unsign(token) # TimestampSigner gère l'expiration automatiquement
        user = Utilisateur.objects.get(email=email)
        if not user.est_email_verifie:
            user.est_email_verifie = True
            user.save()
            return {"message": "Votre adresse email a été vérifiée avec succès."}
        else:
            raise errors.HttpError(400, "Votre email est déjà vérifié.")
    except Utilisateur.DoesNotExist:
        raise errors.HttpError(404, "Utilisateur non trouvé pour cette adresse email.")
    except SignatureExpired: # Cette exception est levée par TimestampSigner si le token est expiré
        raise errors.HttpError(400, "Le lien de vérification a expiré. Veuillez demander un nouveau lien.")
    except BadSignature: # Cette exception est levée par TimestampSigner si le token est invalide
        raise errors.HttpError(400, "Le lien de vérification est invalide.")
    except Exception as e:
        print(f"Erreur lors de la vérification de l'email: {e}")
        raise errors.HttpError(500, "Une erreur inattendue est survenue lors de la vérification de l'email.")


from ninja import File, Form
from ninja.files import UploadedFile
import json
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

@api.post("/auth/register/travailleur", response=UserProfileResponse)
def register_travailleur(
    request,
    email: str = Form(...),
    mot_de_passe: str = Form(...),
    nom: str = Form(...),
    prenom: str = Form(...),
    coordonnees_contact: str = Form(None),
    disponibilite: str = Form(None),
    type_contrat_souhaite: list[str] = Form(...),
    description_profil: str = Form(None),
    latitude: float = Form(None),
    longitude: float = Form(None),
    zone_preference: str = Form("[]"),  # JSON string
    photo_profil: UploadedFile = File(None),
    cv: UploadedFile = File(None),
):
    # Vérifie l'email
    if Utilisateur.objects.filter(email=email).exists():
        raise errors.HttpError(400, "Cet email est déjà utilisé.")

    # Hash du mot de passe
    hashed_password = make_password(mot_de_passe)

    # Crée l'utilisateur
    user = Utilisateur.objects.create_user(
        username=email,
        email=email,
        password=mot_de_passe,
        is_active=True,
        longitude=longitude,
        latitude=latitude
    )

    # Gérer les fichiers : stockage et génération des URL
    photo_url, cv_url = None, None
    if photo_profil:
        path = default_storage.save(f"photos_profil/{photo_profil.name}", ContentFile(photo_profil.read()))
        photo_url = default_storage.url(path)
    if cv:
        path = default_storage.save(f"cv/{cv.name}", ContentFile(cv.read()))
        cv_url = default_storage.url(path)

    # Traiter zone_preference JSON
    try:
        zone_preference_parsed = json.loads(zone_preference)
    except json.JSONDecodeError:
        zone_preference_parsed = []

    # Création du profil travailleur
    travailleur_profile = Travailleur.objects.create(
        id_travailleur=user,
        nom=nom,
        prenom=prenom,
        coordonnees_contact=coordonnees_contact,
        disponibilite=disponibilite,
        type_contrat_souhaite=type_contrat_souhaite,
        cv=cv_url,
        photo_profil=photo_url,
        description_profil=description_profil,
        zone_preference=zone_preference_parsed,
    )

    # Envoie l’email de vérification
    verification_token = generate_verification_token(user.email)
    send_verification_email(user.email, verification_token)

    return user

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib.auth.hashers import make_password
from .models import Utilisateur, Employeur

 # Assurez-vous d'avoir une gestion des erreurs comme dans votre code précédent

@api.post("/auth/register/employeur", response=UserProfileResponse)
def register_employeur(request, payload: EmployeurRegisterPayload):
    """
    Enregistre un nouvel utilisateur en tant qu'Employeur.
    """
    if Utilisateur.objects.filter(email=payload.email).exists():
        raise errors.HttpError(400, "Cet email est déjà utilisé.")

    # Hachage du mot de passe
    hashed_password = make_password(payload.mot_de_passe)

    # Création de l'utilisateur
    user = Utilisateur.objects.create_user(
        username=payload.email,
        email=payload.email,
        password=payload.mot_de_passe,
        is_active=True,
        longitude=payload.lng3,
        latitude=payload.lat3
    )

    # Gestion du logo
    logo_file_instance = None
    if payload.logo_file:
        # Enregistrer le fichier logo dans le système de fichiers
        logo_name = f'logos/{payload.logo_file.name}'  # Définir un nom de fichier unique
        logo_file_instance = ContentFile(payload.logo_file.read(), name=logo_name)
        # Utilisation du stockage par défaut de Django pour stocker le fichier
        path = default_storage.save(logo_name, logo_file_instance)
        logo_url = default_storage.url(path)  # L'URL du fichier

    # Création du profil employeur
    employeur_profile = Employeur.objects.create(
        id_employeur=user,
        nom_entreprise=payload.nom_entreprise,
        secteur_activite=payload.secteur_activite,
        adresse_physique_entreprise=payload.adresse_physique_entreprise,
        site_web=payload.site_web,
        logo_file=logo_file_instance,  # Lien vers le fichier logo téléchargé
        presentation_entreprise=payload.presentation_entreprise,
        culture_entreprise=payload.culture_entreprise,
        besoins_main_oeuvre_specifiques=payload.besoins_main_oeuvre_specifiques,
        informations_contact_recrutement=payload.informations_contact_recrutement,
        est_entreprise_verifiee=payload.est_entreprise_verifiee,
    )

    return user  # Retourne l'objet utilisateur créé (ou vous pouvez retourner un profil utilisateur détaillé)


@api.post("/auth/login", response=TokenResponse)
def login(request, payload: EstablishmentAuthPayload):
    """
    Connecte un utilisateur et retourne un token JWT.
    """
    user = Utilisateur.objects.filter(email=payload.email).first()

    # --- DÉBOGAGE : Ajout de prints pour inspecter les valeurs ---
    print(f"Tentative de connexion pour l'email: {payload.email}")
    if user:
        print(f"Utilisateur trouvé. Hachage BD: {user.password}")
        print(f"Mot de passe fourni: {payload.mot_de_passe}")
        print(f"Vérification du mot de passe: {check_password(payload.mot_de_passe, user.password)}")
    else:
        print("Utilisateur non trouvé.")
    # --- FIN DÉBOGAGE ---

    if not user or not check_password(payload.mot_de_passe, user.password):
        raise errors.HttpError(401, "Identifiants invalides.")
    
    if not user.is_active:
        raise errors.HttpError(401, "Votre compte est inactif. Veuillez contacter l'administrateur.")

    if not user.est_email_verifie:
        # Optionnel: renvoyer un nouveau lien de vérification ici
        # verification_token = generate_verification_token(user.email)
        # send_verification_email(user.email, verification_token)
        raise errors.HttpError(403, "Veuillez vérifier votre adresse email avant de vous connecter.")

    # Mettre à jour la dernière connexion
    user.derniere_connexion = timezone.now()
    user.save()

    access_token = create_jwt_token(user)
    return {"access_token": access_token, "token_type": "Bearer"}


@api.post("/auth/logout", response=MessageResponse, auth=JWTAuth())
def logout(request):
    """
    Déconnecte l'utilisateur en mettant son token JWT en liste noire.
    """
    # Le token est déjà validé par JWTAuth et accessible via request.auth
    auth_header = request.headers.get('Authorization', '')
    token_to_blacklist = auth_header.split(' ')[-1]

    if token_to_blacklist and not BlacklistedToken.objects.filter(token=token_to_blacklist).exists():
        BlacklistedToken.objects.create(token=token_to_blacklist)
        return {"message": "Déconnexion réussie. Token mis en liste noire."}
    else:
        # Si le token n'est pas trouvé ou déjà blacklisté (ce qui est peu probable avec JWTAuth)
        raise errors.HttpError(400, "Token déjà invalide ou non fourni.")


@api.get("/auth/me", response=UserProfileResponse, auth=JWTAuth())
def get_current_user_profile(request):
    """
    Récupère les informations du profil de l'utilisateur actuellement authentifié.
    """
    user = request.auth # L'objet Utilisateur est fourni par JWTAuth
    if not user:
        raise errors.HttpError(401, "Non authentifié.")
    
    return user # Retourne l'objet Utilisateur, Ninja le sérialisera via UserProfileResponse

# --- Endpoints de Gestion des Utilisateurs (Admin seulement) ---

@api.get("/users/", response=UserListResponse, auth=JWTAuth())
def list_users(request):
    """
    Affiche la liste de tous les utilisateurs. Requiert des privilèges d'administrateur.
    """
    
    users = Utilisateur.objects.all()
    # Django Ninja va automatiquement sérialiser la queryset en utilisant UserProfileResponse
    # et l'encapsuler dans le schéma UserListResponse.
    return {"users": users}

@api.delete("/users/{user_id}", response=MessageResponse, auth=JWTAuth())
def delete_user(request, user_id: uuid.UUID):
    """
    Supprime un utilisateur par son ID. Requiert des privilèges d'administrateur.
    """
    if not request.auth.est_administrateur:
        raise errors.HttpError(403, "Accès refusé. Vous devez être administrateur.")
    
    # Ne pas permettre à un administrateur de se supprimer lui-même (optionnel mais recommandé)
    if request.auth.id_utilisateur == user_id:
        raise errors.HttpError(400, "Un administrateur ne peut pas supprimer son propre compte via cette API.")

    user_to_delete = get_object_or_404(Utilisateur, id_utilisateur=user_id)
    user_to_delete.delete()
    
    return {"message": f"Utilisateur avec ID {user_id} supprimé avec succès."}
