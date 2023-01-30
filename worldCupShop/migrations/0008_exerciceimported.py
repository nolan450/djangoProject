# Generated by Django 4.1.3 on 2023-01-29 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worldCupShop', '0007_exerciceline'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExerciceImported',
            fields=[
                ('partieCorps', models.CharField(max_length=100)),
                ('equipement', models.CharField(max_length=100)),
                ('gifUrl', models.CharField(max_length=200)),
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('zoneMuscleEnglish', models.CharField(max_length=100)),
                ('nom', models.CharField(max_length=100)),
                ('zoneMuscle', models.CharField(max_length=100)),
            ],
        ),
    ]
