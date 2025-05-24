from django.db import models

# Create your models here.
from django.db import models
from authentification.models import Employeur, Travailleur

class Competence(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class OffreEmploi(models.Model):
    TYPE_CONTRAT_CHOICES = [
        ('CDI', 'CDI'),
        ('CDD', 'CDD'),
        ('Stage', 'Stage'),
        ('Freelance', 'Freelance'),
    ]

    employeur = models.ForeignKey(Employeur, on_delete=models.CASCADE, related_name="offres")
    titre = models.CharField(max_length=255)
    description = models.TextField()
    type_contrat = models.CharField(max_length=50, choices=TYPE_CONTRAT_CHOICES)
    competences_requises = models.ManyToManyField(Competence, related_name="offres")
    date_limite = models.DateField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    secteur_activite = models.CharField(max_length=255)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre


class Postulation(models.Model):
    travailleur = models.ForeignKey(Travailleur, on_delete=models.CASCADE, related_name="postulations")
    offre = models.ForeignKey(OffreEmploi, on_delete=models.CASCADE, related_name="postulations")
    statut = models.CharField(max_length=50, default="En attente")  # ou "Acceptée", "Rejetée", etc.
    date_postulation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.travailleur} postule à {self.offre}"
