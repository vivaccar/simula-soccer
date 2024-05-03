from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name='home'),
	path('marcelo', views.marcelo, name='marcelo')
]