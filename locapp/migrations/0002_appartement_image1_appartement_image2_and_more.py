# Generated by Django 5.0.6 on 2024-06-11 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appartement',
            name='image1',
            field=models.ImageField(blank=True, null=True, upload_to='appartements/'),
        ),
        migrations.AddField(
            model_name='appartement',
            name='image2',
            field=models.ImageField(blank=True, null=True, upload_to='appartements/'),
        ),
        migrations.AddField(
            model_name='appartement',
            name='image3',
            field=models.ImageField(blank=True, null=True, upload_to='appartements/'),
        ),
    ]
