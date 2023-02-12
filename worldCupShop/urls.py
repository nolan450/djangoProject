from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.auth import views as auth_views

from worldCupShop import views
from manageSport import settings

app_name = 'worldCupShop'
urlpatterns = [
                  path('', views.index, name='index'),
                  path('<int:pk>/', views.ProgrammeAddView.as_view(), name='detail'),
                  path('accounts/login', views.MyLoginView.as_view(), name='login'),
                  path('accounts/logout', views.MyLogoutView.as_view(), name='logout'),
                  path('accounts/register', views.register, name='register'),
                  path('accounts/profil_edit', views.ProfilEditView.as_view(), name='profil_edit'),
                  path('programmes/', views.ProgrammeListView.as_view(), name='programmes'),
                  path('programmes/exercices/get_exercices_by_zone_muscles', views.GetExercicesByZoneMusclesView.as_view(), name='get_exercices_by_zone_muscles'),
                  path('programmes/exercices/add_exercice_line', views.AddExerciceLineView.as_view(), name='add_exercice_line'),
                  path('programmes/add', views.ProgrammeAddView.as_view(), name='programmes_add'),
                  path('programmes/planning', views.PlanningGet.as_view(), name='programme_planning'),
                  path('programmes/add_programme_to_calendar', views.ProgrammeCalendarAdd.as_view(), name='add_programme_to_calendar'),
                  path('programmes/delete_exercice_line', views.ExerciceLineDelete.as_view(), name='delete_exercice_line'),
                  path('programmes/all_exercices', views.ExerciceRetrieval.as_view(), name='get_all_exercices'),
                  path('programmes/delete_entrainement', views.EntrainementDelete.as_view(), name='delete_entrainement_from_calendar'),
                  path('programmes/mes_statistiques', views.MyStatsView.as_view(), name='my_stats'),
                  path('programmes/suggerer_nom', views.SuggestionExerciceAdd.as_view(), name='add_suggestion_exercice'),
                  path('programmes/<int:pk>/', views.ProgrammeView.as_view(), name='programmes_detail'),
                  path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
                  path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
                  path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
                       name='password_reset_confirm'),
                  path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
