from django.contrib import admin
from authentification.models import *
# Register your models here.
admin.site.register(Utilisateur)
admin.site.register(Employeur)
admin.site.register(Travailleur)