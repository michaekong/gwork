# Generated by Django 5.2.1 on 2025-05-23 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentification', '0002_utilisateur_latitude_utilisateur_longitude'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employeur',
            name='logo_url',
        ),
        migrations.AddField(
            model_name='employeur',
            name='logo_file',
            field=models.FileField(blank=True, null=True, upload_to='logos/', verbose_name="Logo de l'entreprise"),
        ),
    ]
