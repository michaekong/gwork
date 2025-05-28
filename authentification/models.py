import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser # Utilisé pour la gestion des utilisateurs de base
from django.utils import timezone

# --- Modèle Utilisateur Personnalisé ---
# Ce modèle est la base de tous les utilisateurs de l'application.
# Il gère les informations d'authentification principales.
class Utilisateur(AbstractUser):
    # 'email' est déjà géré par AbstractUser comme champ unique et est souvent utilisé comme USERNAME_FIELD
    id_utilisateur = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID Utilisateur")
    # 'mot_de_passe_hache' est géré par AbstractUser
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    derniere_connexion = models.DateTimeField(null=True, blank=True, verbose_name="Dernière connexion")
    est_email_verifie = models.BooleanField(default=False, verbose_name="Email vérifié")
    est_administrateur = models.BooleanField(default=False, verbose_name="Est administrateur")
      # Nouveaux champs pour les coordonnées
    longitude = models.DecimalField(
        max_digits=9, # Ex: 180.000000
        decimal_places=6,
        null=True,
        blank=True,
        verbose_name="Longitude"
    )
    latitude = models.DecimalField(
        max_digits=9, # Ex: 90.000000
        decimal_places=6,
        null=True,
        blank=True,
        verbose_name="Latitude"
    )
    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

    def __str__(self):
        return self.email

# --- Modèle Travailleur ---
# Ce modèle représente le profil spécifique d'un demandeur d'emploi.
# Il est lié en OneToOne à l'Utilisateur, ce qui signifie qu'un Utilisateur peut avoir
# un profil Travailleur (ou non).
from django.db import models

from django.db import models
from django.core.validators import RegexValidator, FileExtensionValidator

from django.contrib.postgres.fields import ArrayField
from django.db import models

class Travailleur(models.Model):
    id_travailleur = models.OneToOneField(
        'Utilisateur',
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name="ID Travailleur (lié à l'utilisateur)"
    )
    nom = models.CharField(
        max_length=100,
        verbose_name="Nom",
        validators=[RegexValidator(regex='^[a-zA-ZÀ-ÿ\s-]+$', message="Nom invalide.")]
    )
    prenom = models.CharField(
        max_length=100,
        verbose_name="Prénom",
        validators=[RegexValidator(regex='^[a-zA-ZÀ-ÿ\s-]+$', message="Prénom invalide.")]
    )
    coordonnees_contact = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Coordonnées de contact",
        validators=[RegexValidator(regex='^[0-9\s\+\-]+$', message="Coordonnées invalides.")]
    )
    photo_profil = models.ImageField(
        upload_to='media/photos_profil/',
        blank=True,
        null=True,
        verbose_name="Photo de profil",
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )

    DISPONIBILITE_CHOICES = [
        ('IMMEDIATE', 'Immédiate'),
        ('SOUS_1_MOIS', 'Sous 1 mois'),
        ('SOUS_3_MOIS', 'Sous 3 mois'),
        ('NON_DISPONIBLE', 'Non disponible'),
    ]
    disponibilite = models.CharField(
        max_length=20,
        choices=DISPONIBILITE_CHOICES,
        default='NON_DISPONIBLE',
        verbose_name="Disponibilité"
    )

    # ✅ Remplace latitude/longitude par une liste de coordonnées
    zone_preference = models.JSONField(
    default=list,
    blank=True,
    verbose_name="Zone de préférence (liste de points [latitude, longitude])"
)


    TYPE_CONTRAT_CHOICES = [
        ('CDI', 'CDI'),
        ('CDD', 'CDD'),
        ('INTERIM', 'Intérim'),
        ('FREELANCE', 'Freelance'),
    ]
    type_contrat_souhaite = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Types de contrat souhaités (liste)"
    )

    cv = models.FileField(
        upload_to='media/cv/',
        blank=True,
        null=True,
        verbose_name="CV (PDF)",
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )

    description_profil = models.TextField(
        blank=True,
        null=True,
        verbose_name="Description du profil"
    )

    class Meta:
        verbose_name = "Travailleur"
        verbose_name_plural = "Travailleurs"

    def __str__(self):
        return f"{self.prenom} {self.nom}"


# --- Modèle Employeur ---
# Ce modèle représente le profil spécifique d'un employeur (entreprise).
# Il est également lié en OneToOne à l'Utilisateur, permettant à un Utilisateur d'avoir
# un profil Employeur (ou non).
from django.db import models
from django.conf import settings
import os

class Employeur(models.Model):
    id_employeur = models.OneToOneField(
        Utilisateur,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name="ID Employeur (lié à l'utilisateur)"
    )
    nom_entreprise = models.CharField(max_length=255, unique=True, verbose_name="Nom de l'entreprise")
    secteur_activite = models.CharField(max_length=255, blank=True, null=True, verbose_name="Secteur d'activité")
    adresse_physique_entreprise = models.CharField(max_length=500, blank=True, null=True, verbose_name="Adresse physique de l'entreprise")
    site_web = models.URLField(max_length=500, blank=True, null=True, verbose_name="Site web")
    
    # Change logo_url to logo_file for file upload
    logo_file = models.FileField(upload_to='logos/', blank=True, null=True, verbose_name="Logo de l'entreprise")

    presentation_entreprise = models.TextField(blank=True, null=True, verbose_name="Présentation de l'entreprise")
    culture_entreprise = models.TextField(blank=True, null=True, verbose_name="Culture de l'entreprise")
    besoins_main_oeuvre_specifiques = models.TextField(blank=True, null=True, verbose_name="Besoins spécifiques en main-d'œuvre")
    informations_contact_recrutement = models.TextField(blank=True, null=True, verbose_name="Informations de contact pour le recrutement")
    est_entreprise_verifiee = models.BooleanField(default=False, verbose_name="Entreprise vérifiée")

    class Meta:
        verbose_name = "Employeur"
        verbose_name_plural = "Employeurs"

    def __str__(self):
        return self.nom_entreprise

# --- Modèle BlacklistedToken (pour la déconnexion JWT) ---
# Ce modèle est utilisé pour stocker les tokens JWT qui ont été révoqués (déconnectés)
# afin d'empêcher leur réutilisation avant leur expiration naturelle.
class BlacklistedToken(models.Model):
    token = models.CharField(max_length=500, unique=True, verbose_name="Token mis en liste noire")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Date de mise en liste noire")

    class Meta:
        verbose_name = "Token en liste noire"
        verbose_name_plural = "Tokens en liste noire"
        ordering = ['-timestamp']

    def __str__(self):
        return self.token[:50] + "..." if len(self.token) > 50 else self.token

