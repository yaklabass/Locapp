# Generated by Django 5.0.6 on 2024-06-29 23:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locapp', '0008_gerant_signature'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paiement',
            name='Reservation',
        ),
        migrations.RemoveField(
            model_name='paiement',
            name='montant',
        ),
        migrations.AddField(
            model_name='paiement',
            name='capture_ecran',
            field=models.ImageField(blank=True, null=True, upload_to='payement_captures/'),
        ),
        migrations.AddField(
            model_name='paiement',
            name='numero_de_transfert',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='paiement',
            name='numero_telephone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='paiement',
            name='reservation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='locapp.reservation'),
        ),
    ]
