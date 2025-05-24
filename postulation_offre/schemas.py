from ninja import Schema
from datetime import date, datetime
from typing import List, Optional

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
