from ninja import Router
from django.shortcuts import get_object_or_404
from .models import OffreEmploi, Competence, Postulation
from authentification.models import Employeur, Travailleur
from .schemas import (
    OffreEmploiIn, OffreEmploiOut,
    CompetenceIn, CompetenceOut,
    PostulationIn, PostulationOut,
)
from ninja.errors import HttpError

router = Router()

# 🔹 1. Ajouter une compétence
@router.post("/competences", response=CompetenceOut)
def create_competence(request, payload: CompetenceIn):
    competence = Competence.objects.create(**payload.dict())
    return competence

# 🔹 2. Lister toutes les compétences
@router.get("/competences", response=list[CompetenceOut])
def list_competences(request):
    return Competence.objects.all()

# 🔹 3. Créer une offre d'emploi
@router.post("/offres", response=OffreEmploiOut)
def create_offre(request, payload: OffreEmploiIn, employeur_id: int):
    employeur = get_object_or_404(Employeur, id=employeur_id)
    offre = OffreEmploi.objects.create(
        employeur=employeur,
        titre=payload.titre,
        description=payload.description,
        type_contrat=payload.type_contrat,
        date_limite=payload.date_limite,
        latitude=payload.latitude,
        longitude=payload.longitude,
        secteur_activite=payload.secteur_activite
    )
    offre.competences_requises.set(payload.competences_ids)
    return offre

# 🔹 4. Lister toutes les offres
@router.get("/offres", response=list[OffreEmploiOut])
def list_offres(request):
    return OffreEmploi.objects.select_related("employeur").prefetch_related("competences_requises").all()

# 🔹 5. Modifier une offre (optionnel)
@router.put("/offres/{offre_id}", response=OffreEmploiOut)
def update_offre(request, offre_id: int, payload: OffreEmploiIn):
    offre = get_object_or_404(OffreEmploi, id=offre_id)
    for attr, value in payload.dict(exclude={"competences_ids"}).items():
        setattr(offre, attr, value)
    offre.save()
    offre.competences_requises.set(payload.competences_ids)
    return offre

# 🔹 6. Supprimer une offre
@router.delete("/offres/{offre_id}")
def delete_offre(request, offre_id: int):
    offre = get_object_or_404(OffreEmploi, id=offre_id)
    offre.delete()
    return {"success": True}

# 🔹 7. Postuler à une offre
@router.post("/postuler", response=PostulationOut)
def postuler(request, payload: PostulationIn, travailleur_id: int):
    travailleur = get_object_or_404(Travailleur, id=travailleur_id)
    offre = get_object_or_404(OffreEmploi, id=payload.offre_id)

    if Postulation.objects.filter(travailleur=travailleur, offre=offre).exists():
        raise HttpError(400, "Vous avez déjà postulé à cette offre.")

    postulation = Postulation.objects.create(travailleur=travailleur, offre=offre)
    return postulation

# 🔹 8. Historique des candidatures d’un travailleur
@router.get("/travailleurs/{travailleur_id}/postulations", response=list[PostulationOut])
def historique_postulations(request, travailleur_id: int):
    travailleur = get_object_or_404(Travailleur, id=travailleur_id)
    return Postulation.objects.filter(travailleur=travailleur)

