# Generated by Django 4.2.13 on 2024-07-12 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RentBikeCarapp', '0003_gallery'),
    ]

    operations = [
        migrations.AddField(
            model_name='bike',
            name='category',
            field=models.CharField(choices=[('standard', 'standard'), ('cruiser', 'cruiser'), ('touring', 'touring'), ('Sports', 'Sports'), ('scooters ', 'scooters ')], default=1, max_length=200),
            preserve_default=False,
        ),
    ]
