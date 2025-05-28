# authentification/schemas.py
import uuid
from typing import List # Importation de List pour les listes de schémas
from ninja import Schema
from typing import Optional, List
from pydantic import BaseModel, EmailStr, constr

class EstablishmentAuthPayload(Schema):
    email: str
    mot_de_passe: str



from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field

class Point(BaseModel):
    latitude: float
    longitude: float
class TravailleurRegisterPayload(Schema):
    email: EmailStr
    mot_de_passe: str
    nom: str
    prenom: str
    coordonnees_contact: Optional[str] = None
    photo_profil: Optional[str] = None
    disponibilite: Optional[str] = None
    type_contrat_souhaite: Optional[List[str]] = Field(default_factory=list)
    cv: Optional[str] = None
    description_profil: Optional[str] = None
    zone_preference: Optional[List[Point]] = Field(default_factory=list)
    longitude: float| None = None
    latitude: float| None = None
    class Config:
        schema_extra = {
            "example": {
                "email": "exemple@domaine.com",
                "mot_de_passe": "motdepassefort",
                "nom": "Dupont",
                "prenom": "Jean",
                "coordonnees_contact": "+33 1 23 45 67 89",
                "photo_profil": "http://example.com/photo.jpg",
                "disponibilite": "IMMEDIATE",
                "type_contrat_souhaite": ["CDI", "CDD"],
                "cv": "http://example.com/cv.pdf",
                "description_profil": "Développeur avec 5 ans d'expérience.",
                "zone_preference": [
                    {"longitude": 2.3522, "latitude": 48.8566},
                    {"longitude": 2.2945, "latitude": 48.8584}
                ]
            }
        }


from pydantic import BaseModel, Field
from typing import Optional

class EmployeurRegisterPayload(BaseModel):
    email: str
    mot_de_passe: str
    nom_entreprise: str
    secteur_activite: Optional[str] = None
    adresse_physique_entreprise: Optional[str] = None
    site_web: Optional[str] = None
    logo_file: Optional[str] = None  # Champ pour le fichier logo de l'entreprise
    presentation_entreprise: Optional[str] = None
    culture_entreprise: Optional[str] = None
    besoins_main_oeuvre_specifiques: Optional[str] = None
    informations_contact_recrutement: Optional[str] = None
    lat3: Optional[float] = None  # Latitude de l'employeur
    lng3: Optional[float] = None  # Longitude de l'employeur
     # Champ pour indiquer si l'entreprise est vérifiée
    
    class Config:
        min_anystr_length = 1
        anystr_strip_whitespace = True

class TokenResponse(Schema):
    access_token: str
    token_type: str = "Bearer"

class UserProfileResponse(Schema):
    id_utilisateur: uuid.UUID
    email: str
    est_email_verifie: bool
    est_administrateur: bool
    longitude: float| None = None
    latitude: float| None = None
    
    # Vous pouvez ajouter ici des champs pour Travailleur/Employeur si l'utilisateur en a un
    # Ex: travailleur_id: uuid.UUID | None = None
    # Ex: employeur_nom_entreprise: str | None = None
class Userprofile(Schema):
    id_utilisateur: uuid.UUID
    nom: str
    prenom: str
    coordonnees_contact: Optional[str]
    disponibilite: str
    zone_preference: List[List[float]]
    type_contrat_souhaite: List[str]
    description_profil: Optional[str]
    cv: Optional[str]
    photo_profil: Optional[str]
    email: str
    est_email_verifie: bool
    est_administrateur: bool
    longitude: float| None = None
    latitude: float| None = None
class TokenResponseUrl(Schema):
    access_token: str
    token_type: str
    redirect_url: Optional[str]
class UserListResponse(Schema):
    """
    Schéma pour la réponse d'une liste d'utilisateurs.
    """
    users: List[UserProfileResponse] # Une liste d'objets UserProfileResponse

class MessageResponse(Schema):
    message: str

from datetime import date, datetime


# --- Schéma de compétence ---
class CompetenceOut(Schema):
    id: int
    nom: str

class CompetenceIn(Schema):
    nom: str


# --- Schéma Offre Emploi ---
class OffreEmploiIn(Schema):
    titre: str
    description: str
    type_contrat: str
    competences_ids: List[int]
    date_limite: date
    latitude: float
    longitude: float
    secteur_activite: str

class OffreEmploiOut(Schema):
    id: int
    titre: str
    description: str
    type_contrat: str
    date_limite: date
    latitude: float
    longitude: float
    secteur_activite: str
    date_creation: datetime
    employeur_id: int
    competences_requises: List[CompetenceOut]


# --- Schéma Postulation ---
class PostulationIn(Schema):
    offre_id: int

class PostulationOut(Schema):
    id: int
    offre_id: int
    travailleur_id: int
    statut: str
    date_postulation: datetime
