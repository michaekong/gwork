# Generated by Django 5.2.1 on 2025-05-24 17:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentification', '0007_competence_offreemploi_postulation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offreemploi',
            name='competences_requises',
        ),
        migrations.RemoveField(
            model_name='offreemploi',
            name='employeur',
        ),
        migrations.RemoveField(
            model_name='postulation',
            name='offre',
        ),
        migrations.RemoveField(
            model_name='postulation',
            name='travailleur',
        ),
        migrations.DeleteModel(
            name='Competence',
        ),
        migrations.DeleteModel(
            name='OffreEmploi',
        ),
        migrations.DeleteModel(
            name='Postulation',
        ),
    ]
