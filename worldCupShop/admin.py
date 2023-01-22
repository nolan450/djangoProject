from django.contrib import admin

from worldCupShop.models import Question, Choice, Exercice, Programme

# Register your models here.
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Exercice)
admin.site.register(Programme)
