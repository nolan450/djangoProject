import datetime

from django.db import models
from django.utils import timezone


# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Programme(models.Model):
    label = models.CharField(max_length=100)
    description = models.CharField(max_length=400)
    thumbnail = models.ImageField(upload_to="exercises", blank=True, null=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, default=1)
    status = models.CharField(max_length=50, default="private")
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.label


class Exercice(models.Model):
    label = models.CharField(max_length=100)
    description = models.CharField(max_length=400)
    programme = models.ManyToManyField(Programme)
    thumbnail = models.ImageField(upload_to="exercises", blank=True, null=True)

    def __str__(self):
        return self.label


class ExerciceImported(models.Model):
    partieCorps = models.CharField(max_length=100)
    equipement = models.CharField(max_length=100)
    gifUrl = models.CharField(max_length=200)
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    zoneMuscleEnglish = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    zoneMuscle = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ExerciceLine(models.Model):
    label = models.CharField(max_length=100)
    nbRepetition = models.IntegerField(default=0)
    nbSerie = models.IntegerField(default=0)
    exercice = models.ForeignKey(ExerciceImported, on_delete=models.CASCADE)
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE, null=True)
    order = models.IntegerField(default=1000)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.label


class Fiche(models.Model):
    label = models.CharField(max_length=100)
    description = models.CharField(max_length=400)
    filename = models.CharField(max_length=200)

    def __str__(self):
        return self.label


class SuggestionNom(models.Model):
    nom_suggere = models.CharField(max_length=100)
    exercice = models.ForeignKey(ExerciceImported, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, default=1)


class ExerciceLineRepetition(models.Model):
    exerciceLine = models.ForeignKey(ExerciceLine, on_delete=models.CASCADE)
    serieNumber = models.IntegerField(default=0)
    nbRepetition = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)


class Entrainement(models.Model):
    label = models.CharField(max_length=100)
    description = models.CharField(max_length=400)
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE)
    date = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.label


# class User(models.Model):
