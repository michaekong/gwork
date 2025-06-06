# Generated by Django 5.2.1 on 2025-05-24 17:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentification', '0008_remove_offreemploi_competences_requises_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Competence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='OffreEmploi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('type_contrat', models.CharField(choices=[('CDI', 'CDI'), ('CDD', 'CDD'), ('Stage', 'Stage'), ('Freelance', 'Freelance')], max_length=50)),
                ('date_limite', models.DateField()),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('secteur_activite', models.CharField(max_length=255)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('competences_requises', models.ManyToManyField(related_name='offres', to='postulation_offre.competence')),
                ('employeur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offres', to='authentification.employeur')),
            ],
        ),
        migrations.CreateModel(
            name='Postulation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statut', models.CharField(default='En attente', max_length=50)),
                ('date_postulation', models.DateTimeField(auto_now_add=True)),
                ('offre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='postulations', to='postulation_offre.offreemploi')),
                ('travailleur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='postulations', to='authentification.travailleur')),
            ],
        ),
    ]
