# Generated by Django 4.1.3 on 2023-02-02 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worldCupShop', '0008_exerciceimported'),
    ]

    operations = [
        migrations.AddField(
            model_name='programme',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]