# Generated by Django 5.0.6 on 2024-06-28 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locapp', '0007_alter_appartement_categorie_reservationmoi'),
    ]

    operations = [
        migrations.AddField(
            model_name='gerant',
            name='signature',
            field=models.ImageField(blank=True, null=True, upload_to='signatures/'),
        ),
    ]
