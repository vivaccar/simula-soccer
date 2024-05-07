from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import Team, Game
from .forms import Game_forms

	
# Create your views here.

def	home(request):
	teams_list = Team.objects.order_by('-points', '-wins')
	context = {'teams_list': teams_list}
	games_list = Game.objects.all()
	teams_list = Team.objects.order_by('-points')
	context = {'teams_list': teams_list, 'games_list': games_list}
	return (render(request, 'home.html', context))

def reset_result(game):
    game.home_team.goals_pro -= game.home_goals
    game.home_team.goals_con -= game.away_goals
    game.away_team.goals_pro -= game.away_goals
    game.away_team.goals_con -= game.home_goals
    if game.home_goals > game.away_goals:
          game.home_team.wins -= 1
          game.away_team.loss -= 1
          game.home_team.points -= 3
    elif game.home_goals == game.away_goals:
          game.home_team.draws = 1
          game.away_team.draws -= 1
          game.home_team.points -= 1
          game.away_team.points -= 1
    else:
          game.away_team.wins -= 1
          game.home_team.loss -= 1
          game.away_team.points -= 3
    game.home_goals = 0
    game.away_goals = 0
    game.save()

def game(request):
    if request.method == 'POST':
        home_team_name = request.POST.get('home_team')
        home_goals = int(request.POST.get('home_goals'))
        away_team_name = request.POST.get('away_team')
        away_goals = int(request.POST.get('away_goals'))
        game_id = int(request.POST.get('game_id'))
        home_team = Team.objects.get(name=home_team_name)
        away_team = Team.objects.get(name=away_team_name)
        game_class = Game.objects.get(id = game_id)
        if game_class.played == True:
            reset_result(game_class)
        home_team.goals_pro += home_goals
        game_class.home_goals = home_goals
        home_team.goals_con += away_goals
        game_class.away_goals = away_goals
        away_team.goals_pro += away_goals
        away_team.goals_con += home_goals
        if home_goals > away_goals:
            home_team.wins += 1
            away_team.loss += 1
            home_team.points += 3
        elif home_goals == away_goals:
            home_team.draws += 1
            away_team.draws += 1
            home_team.points += 1
            away_team.points += 1
        else:
            away_team.wins += 1
            home_team.loss += 1
            away_team.points += 3
        game_class.played = True
        game_class.save()
        home_team.save()
        away_team.save()
        return home(request)
    return home(request)


def	marcelo(request):
	return (render(request, 'marcelo.html'))