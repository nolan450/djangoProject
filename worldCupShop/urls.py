from django.conf.urls.static import static
from django.urls import path, include

from worldCupShop import views
from manageSport import settings

app_name = 'worldCupShop'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('accounts/login', views.MyLoginView.as_view(), name='login'),
    path('accounts/logout', views.MyLogoutView.as_view(), name='logout'),
    path('accounts/register', views.register, name='register'),
    path('programmes/', views.programmes, name='programmes')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
