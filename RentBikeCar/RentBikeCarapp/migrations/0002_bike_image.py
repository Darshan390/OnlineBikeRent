# Generated by Django 4.2.13 on 2024-07-08 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RentBikeCarapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bike',
            name='image',
            field=models.ImageField(default=1, upload_to='image'),
            preserve_default=False,
        ),
    ]
