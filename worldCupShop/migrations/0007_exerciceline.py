# Generated by Django 4.1.3 on 2023-01-29 15:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('worldCupShop', '0006_programme_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExerciceLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=100)),
                ('nbRepetition', models.IntegerField(default=0)),
                ('nbSerie', models.IntegerField(default=0)),
                ('exercice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='worldCupShop.exercice')),
            ],
        ),
    ]