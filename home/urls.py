from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name='home'),
	path('game', views.game, name='game'),
	path('restart', views.reset_simulation, name='restart'),
	path('next_round', views.next_round, name='next_round'),
	path('prev_round', views.prev_round, name='prev_round'),
	path('api', views.api_football, name='api'),
]