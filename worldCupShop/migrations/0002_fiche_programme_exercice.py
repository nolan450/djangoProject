# Generated by Django 4.1.3 on 2023-01-04 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worldCupShop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fiche',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=400)),
                ('filename', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Programme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=400)),
                ('filename', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Exercice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=400)),
                ('filename', models.CharField(max_length=200)),
                ('programme', models.ManyToManyField(to='worldCupShop.programme')),
            ],
        ),
    ]