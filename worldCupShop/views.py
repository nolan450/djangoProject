from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.template.context_processors import request
from django.urls import reverse
from django.views import generic

from worldCupShop.forms import AddProgrammeForm, AddExerciceLineForm
from worldCupShop.models import Question, Choice, Programme, ExerciceImported, ExerciceLine

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect


# faire une fonction qui vérifie si l'utilisateur est connecté
# si oui, on affiche la page d'accueil
# si non, on affiche la page de login
def index(request):
    if request.user.is_authenticated:
        return IndexView.as_view()(request)
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


class IndexView(generic.ListView):
    template_name = 'worldCupShop/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'worldCupShop/detail.html'


class AddProgrammeView(generic.CreateView):
    model = Programme
    template_name = 'worldCupShop/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'worldCupShop/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'worldCupShop/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('worldCupShop:results', args=(question.id,)))


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    next_page = 'worldCupShop:index'


class MyLogoutView(LogoutView):
    next_page = 'worldCupShop:index'


def programmes(request):
    programmes = Programme.objects.filter(user=request.user)

    return render(request, 'worldCupShop/dashboard_sport.html', context={"programmes": programmes})


def add_programme(request):
    if request.method == 'POST':
        form = AddProgrammeForm(request.POST, request.FILES)
        if form.is_valid():
            # creer un programme
            programme = Programme()
            programme.label = form.cleaned_data['label']
            programme.description = form.cleaned_data['description']
            programme.thumbnail = form.cleaned_data['thumbnail']
            programme.user = request.user
            programme.save()
            return redirect('worldCupShop:programmes')
    else:
        form = AddProgrammeForm()
    return render(request, 'worldCupShop/add_programme.html', {'form': form})


class ProgrammeView(generic.DetailView):
    model = Programme
    form = AddExerciceLineForm()
    template_name = 'worldcupshop/programme/programme_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        zoneMuscle = ExerciceImported.objects.values('zoneMuscle').distinct()
        for zone in zoneMuscle:
            zone['zoneMuscle'] = zone['zoneMuscle'].capitalize()
        zoneMuscle = sorted(zoneMuscle, key=lambda k: k['zoneMuscle'])

        context['zoneMuscles'] = zoneMuscle
        context['exercices'] = ExerciceImported.objects.all()

        return context


#fonction qui retourne tous les exercices sous forme de tableau en fonction de la zoneMuscle
def get_exercices_by_zone_muscles(request):
    if request.method == 'GET':
        zoneMuscle = request.GET.get('zoneMuscle', None)
        exercices = ExerciceImported.objects.filter(zoneMuscle=zoneMuscle).values()
        for exercice in exercices:
            exercice['nom'] = exercice['nom'].capitalize()

        exercices = sorted(exercices, key=lambda k: k['nom'])
        return JsonResponse(list(exercices), safe=False)
    else:
        return JsonResponse({"error": "error"}, status=400)


#fonction qui enregiste une ligne d'exercice envoyé en ajax dans data et qui enregistre dans la base de données
def add_exercice_line(request):
    if request.method == 'POST':
        data = request.POST
        exerciceLine = ExerciceLine()
        exerciceLine.exercice = ExerciceImported.objects.get(id=data['exercice_id'])
        exerciceLine.label = data['label']
        exerciceLine.nbSerie = data['nb_series']
        exerciceLine.nbRepetition = data['nb_repetitions']
        exerciceLine.programme = Programme.objects.get(id=data['programme_id'])
        exerciceLine.save()
        return JsonResponse({"success": "success"}, status=200)
    else:
        return JsonResponse({"error": "error"}, status=400)
