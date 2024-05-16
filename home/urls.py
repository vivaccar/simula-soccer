from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
	path('', views.home, name='home'),
	path('brasil_serie_a', views.brasil_serie_a, name='brasil_serie_a'),
	path('brasil_serie_b', views.brasil_serie_b, name='brasil_serie_b'),
	path('premier_league', views.premier_league, name='premier_league'),
	path('restart', views.reset_simulation, name='restart'),
	path('next_round', views.next_round, name='next_round'),
	path('prev_round', views.prev_round, name='prev_round'),
	path('api', views.api_football, name='api'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)