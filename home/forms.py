from django import forms
from django.forms import ModelForm
from .models import Team

class Game_forms(ModelForm):
	home_goals = forms.IntegerField(label='home_goals')
	away_goals = forms.IntegerField(label='away_goals')