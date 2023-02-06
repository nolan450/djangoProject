from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.auth import views as auth_views

from worldCupShop import views
from manageSport import settings

app_name = 'worldCupShop'
urlpatterns = [
                  path('', views.index, name='index'),
                  path("select2/", include("django_select2.urls")),
                  path('<int:pk>/', views.AddProgrammeView.as_view(), name='detail'),
                  path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
                  path('<int:question_id>/vote/', views.vote, name='vote'),
                  path('accounts/login', views.MyLoginView.as_view(), name='login'),
                  path('accounts/logout', views.MyLogoutView.as_view(), name='logout'),
                  path('accounts/register', views.register, name='register'),
                  path('programmes/', views.programmes, name='programmes'),
                  path('programmes/exercices/get_exercices_by_zone_muscles', views.get_exercices_by_zone_muscles, name='get_exercices_by_zone_muscles'),
                  path('programmes/exercices/add_exercice_line', views.add_exercice_line, name='add_exercice_line'),
                  path('programmes/add', views.add_programme, name='programmes_add'),
                  path('programmes/delete_exercice_line', views.delete_exercice_line, name='delete_exercice_line'),
                  path('programmes/all_exercices', views.get_all_exercices, name='get_all_exercices'),
                  path('programmes/suggerer_nom', views.add_suggestion_exercice, name='add_suggestion_exercice'),
                  path('programmes/<int:pk>/', views.ProgrammeView.as_view(), name='programmes_detail'),
                  path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
                  path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
                  path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
                       name='password_reset_confirm'),
                  path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
