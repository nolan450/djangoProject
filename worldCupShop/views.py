import datetime
import json

from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.template.context_processors import request
from django.urls import reverse
from django.utils import timezone
from django.views import generic, View

from worldCupShop.forms import AddProgrammeForm, AddExerciceLineForm, UserPersonalizeForm
from worldCupShop.models import Question, Choice, Programme, ExerciceImported, ExerciceLine, SuggestionNom, \
    ExerciceLineRepetition, Entrainement

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User


def index(request):
    if request.user.is_authenticated:
        return ProgrammeListView.as_view()(request)
    else:
        return redirect('worldCupShop:login')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('worldCupShop:index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


class ProfilEditView(View):
    form_class = UserPersonalizeForm()

    def get(self, request):
        return render(request, 'worldCupShop/mon_profil.html', context={"form": self.form_class})

    def post(self, request):
        form = UserPersonalizeForm(request.POST)
        if form.is_valid():
            user = request.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.username = form.cleaned_data['username']
            user.email = form.cleaned_data['email']
            user.save()
            return redirect('worldCupShop:index')
        else:
            return render(request, 'worldCupShop/mon_profil.html', context={"form": self.form_class})


class IndexView(generic.ListView):
    template_name = 'worldCupShop/index.html'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class ProgrammeDeleteView(View):

    def post(self, request):
        programme_id = request.POST.get('programme_id')
        programme = Programme.objects.get(id=programme_id)
        programme.delete()
        return JsonResponse({'status': 'ok'})

    def get(self, request):
        return JsonResponse({'status': 'ok'})


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    next_page = 'worldCupShop:index'


class MyLogoutView(LogoutView):
    next_page = 'worldCupShop:index'


class ProgrammeListView(View):
    def get(self, request):
        programmes = Programme.objects.filter(user=request.user)
        return render(request, 'worldCupShop/dashboard_sport.html', context={"programmes": programmes})


class ProgrammeAddView(View):
    form_class = AddProgrammeForm
    template_name = 'worldCupShop/add_programme.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            # creer un programme
            programme = Programme()
            programme.label = form.cleaned_data['label']
            programme.description = form.cleaned_data['description']
            programme.thumbnail = form.cleaned_data['thumbnail']
            programme.user = request.user
            programme.save()
            return redirect('worldCupShop:programmes')
        return render(request, self.template_name, {'form': form})


class ProgrammeView(generic.DetailView):
    model = Programme
    form = AddExerciceLineForm()
    template_name = 'worldCupShop/programme/programme_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        zoneMuscle = ExerciceImported.objects.values('zoneMuscle').distinct()
        for zone in zoneMuscle:
            zone['zoneMuscle'] = zone['zoneMuscle'].capitalize()
        zoneMuscle = sorted(zoneMuscle, key=lambda k: k['zoneMuscle'])

        context['zoneMuscles'] = zoneMuscle
        context['exercices'] = ExerciceImported.objects.all()

        exercice_line = ExerciceLine.objects.filter(programme=self.object).order_by('order')
        # pour chaque exercice line, on récupère les repetitions triées par serieNumber
        for exercice in exercice_line:
            exercice.repetitions = ExerciceLineRepetition.objects.filter(exerciceLine=exercice).order_by('serieNumber')

        context['exerciceLines'] = exercice_line

        return context


class GetExercicesByZoneMusclesView(View):
    def get(self, request):
        zoneMuscle = request.GET.get('zoneMuscle', None)
        exercices = ExerciceImported.objects.filter(zoneMuscle=zoneMuscle).values()
        for exercice in exercices:
            exercice['nom'] = exercice['nom'].capitalize()

        exercices = sorted(exercices, key=lambda k: k['nom'])
        return JsonResponse(list(exercices), safe=False)

    def post(self, request):
        return JsonResponse({"error": "error"}, status=400)


# fonction qui enregiste une ligne d'exercice envoyé en ajax dans data et qui enregistre dans la base de données
class AddExerciceLineView(View):
    def post(self, request):
        data = request.POST
        exerciceLine = ExerciceLine()
        exerciceLine.exercice = ExerciceImported.objects.get(id=data['exercice_id'])
        exerciceLine.label = data['label']

        repetitions = json.loads(data['nb_repetitions'])
        exerciceLine.nbSerie = data['nb_series']
        exerciceLine.save()

        if repetitions:
            for key, repetition in repetitions.items():
                exerciceLineRepetition = ExerciceLineRepetition()
                exerciceLineRepetition.nbRepetition = int(repetition)
                exerciceLineRepetition.serieNumber = int(key)
                exerciceLineRepetition.exerciceLine = exerciceLine
                exerciceLineRepetition.save()

        if data['programme_id']:
            exerciceLine.programme_id = data['programme_id']

        exerciceLine.order = ExerciceLine.objects.filter(programme=exerciceLine.programme).count() + 1

        exerciceLine.save()
        return JsonResponse({"success": "success"}, status=200)

    def get(self, request):
        return JsonResponse({"error": "error"}, status=400)


class ExerciceLineDelete(View):
    def post(self, request):
        data = request.POST
        exerciceLine = ExerciceLine.objects.get(id=data['exercice_line_id'])
        exerciceLine.delete()
        return JsonResponse({"success": "success"}, status=200)

    def get(self, request):
        return JsonResponse({"error": "error"}, status=400)


class ExerciceRetrieval(View):
    def get(self, request):
        exercices = ExerciceImported.objects.all().values()
        for exercice in exercices:
            exercice['nom'] = exercice['nom'].capitalize()

        zoneMuscles = ExerciceImported.objects.values('zoneMuscle').distinct()

        exercices = sorted(exercices, key=lambda k: k['nom'])
        return render(request, 'worldCupShop/exercice/exercices.html',
                      {'exercices': exercices, 'zoneMuscles': zoneMuscles})

    def post(self, request):
        return JsonResponse({"error": "error"}, status=400)


class SuggestionExerciceAdd(View):
    def post(self, request):
        data = request.POST
        suggestion = SuggestionNom()
        suggestion.nom_suggere = data['nom_suggere']
        suggestion.exercice = ExerciceImported.objects.get(id=data['exercice_id'])
        suggestion.user = request.user
        suggestion.save()
        return JsonResponse({"success": "success"}, status=200)

    def get(self, request):
        return JsonResponse({"error": "error"}, status=400)


class PlanningGet(View):
    def get(self, request):
        programmes = Programme.objects.filter(user=request.user)
        entrainements = Entrainement.objects.filter(user=request.user)

        return render(request, 'worldCupShop/programme/programme_calendar.html',
                      {'programmes': programmes, 'entrainements': entrainements})

    def post(self, request):
        return JsonResponse({"error": "error"}, status=400)


class ProgrammeCalendarAdd(View):
    def post(self, request):
        data = request.POST
        entrainement = Entrainement()
        entrainement.label = data['title']
        entrainement.programme = Programme.objects.get(id=data['programme_id'])
        entrainement.date = data['date_debut']
        current_date = datetime.datetime.now()
        entrainement.user = request.user
        entrainement.save()
        # retourner l'id de l'entrainement
        return JsonResponse({"success": "success", "id": entrainement.id}, status=200)

    def get(self, request):
        return JsonResponse({"error": "error"}, status=400)


def get_entrainements_par_mois(entrainements):
    entrainements_par_mois = {}
    for entrainement in entrainements:
        mois = entrainement.date.strftime("%m")
        if mois in entrainements_par_mois:
            entrainements_par_mois[mois] += 1
        else:
            entrainements_par_mois[mois] = 1
    return entrainements_par_mois


class MyStatsView(View):
    def get(self, request):
        programmes = Programme.objects.filter(user=request.user)
        entrainements = Entrainement.objects.filter(user=request.user)
        # retourne le nombre d'entrainements par mois sous forme de dictionnaire
        entrainements_par_mois = get_entrainements_par_mois(entrainements)

        return render(request, 'worldCupShop/programme/programme_chart.html', {'programmes': programmes,
                                                                               'entrainements': entrainements_par_mois})

    def post(self, request):
        return JsonResponse({"error": "error"}, status=400)


class EntrainementDelete(View):
    def post(self, request):
        data = request.POST
        entrainement = Entrainement.objects.get(id=data['entrainement_id'])
        entrainement.delete()
        return JsonResponse({"success": "success"}, status=200)

    def get(self, request):
        return JsonResponse({"error": "error"}, status=400)
