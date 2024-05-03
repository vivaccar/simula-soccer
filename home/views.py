from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Team

	
# Create your views here.

def	home(request):
	teams_list = Team.objects.order_by('-points')
	context = {'teams_list': teams_list}
	return (render(request, 'home.html', context))
""" 	template = loader.get_template('home.html')
	return HttpResponse(template.render()) """

def	marcelo(request):
	return (render(request, 'marcelo.html'))