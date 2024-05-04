from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Team, Game

	
# Create your views here.

def	home(request):
	games_list = Game.objects.all()
	teams_list = Team.objects.order_by('-points')
	context = {'teams_list': teams_list, 'games_list': games_list}
	return (render(request, 'home.html', context))
""" 	template = loader.get_template('home.html')
	return HttpResponse(template.render()) """

def	marcelo(request):
	return (render(request, 'marcelo.html'))