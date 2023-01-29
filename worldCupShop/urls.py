from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.auth import views as auth_views

from worldCupShop import views
from manageSport import settings

app_name = 'worldCupShop'
urlpatterns = [
                  path('', views.index, name='index'),
                  path('<int:pk>/', views.AddProgrammeView.as_view(), name='detail'),
                  path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
                  path('<int:question_id>/vote/', views.vote, name='vote'),
                  path('accounts/login', views.MyLoginView.as_view(), name='login'),
                  path('accounts/logout', views.MyLogoutView.as_view(), name='logout'),
                  path('accounts/register', views.register, name='register'),
                  path('programmes/', views.programmes, name='programmes'),
                  path('programmes/add', views.add_programme, name='programmes_add'),
                  path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
                  path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
                  path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
                       name='password_reset_confirm'),
                  path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
