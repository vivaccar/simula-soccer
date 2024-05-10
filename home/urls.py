from django.urls import path
from . import views

urlpatterns = [
	path('', views.game, name='game'),
	path('', views.home, name='home'),
	path('restart', views.restart, name='restart'),
	path('next_round', views.next_round, name='next_round'),
	path('prev_round', views.prev_round, name='prev_round'),
	path('api', views.api_football, name='api')
]