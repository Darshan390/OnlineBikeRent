# Generated by Django 4.2.13 on 2024-07-18 06:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('RentBikeCarapp', '0008_bike_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('adhar', models.FileField(upload_to='documents/adhar')),
                ('driving_licence', models.FileField(upload_to='documents/licence')),
                ('bike', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='RentBikeCarapp.bike')),
            ],
        ),
    ]
