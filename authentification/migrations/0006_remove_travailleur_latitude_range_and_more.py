# Generated by Django 5.2.1 on 2025-05-23 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentification', '0005_alter_travailleur_coordonnees_contact_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='travailleur',
            name='latitude_range',
        ),
        migrations.RemoveConstraint(
            model_name='travailleur',
            name='longitude_range',
        ),
        migrations.RemoveField(
            model_name='travailleur',
            name='latitude_pref',
        ),
        migrations.RemoveField(
            model_name='travailleur',
            name='longitude_pref',
        ),
        migrations.AddField(
            model_name='travailleur',
            name='zone_preference',
            field=models.JSONField(blank=True, default=list, verbose_name='Zone de préférence (liste de points [latitude, longitude])'),
        ),
    ]
