from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import Team, Game
from .forms import Game_forms

	
# Create your views here.

def	home(request, current_round):
	games_list = Game.objects.filter(round = current_round)
	teams_list = Team.objects.order_by('-points', '-wins', '-sg')
	context = {'teams_list': teams_list, 'games_list': games_list, 'current_round' : current_round}
	return (render(request, 'home.html', context))

def reset_result(game, home_team, away_team):
	home_team.goals_pro -= game.home_goals
	home_team.goals_con -= game.away_goals
	away_team.goals_pro -= game.away_goals
	away_team.goals_con -= game.home_goals
	home_team.sg -= game.home_goals - game.away_goals
	away_team.sg -= game.away_goals - game.home_goals
	if game.home_goals > game.away_goals:
		home_team.wins -= 1
		away_team.loss -= 1
		home_team.points -= 3
	elif game.home_goals == game.away_goals:
		home_team.draws -= 1
		away_team.draws -= 1
		home_team.points -= 1
		away_team.points -= 1
	else:
		away_team.wins -= 1
		home_team.loss -= 1
		away_team.points -= 3
	home_team.save()
	away_team.save()

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
		round = game_class.round
		if game_class.played == True:
			reset_result(game_class, home_team, away_team)
		home_team.goals_pro += home_goals
		game_class.home_goals = home_goals
		home_team.goals_con += away_goals
		game_class.away_goals = away_goals
		away_team.goals_pro += away_goals
		away_team.goals_con += home_goals
		home_team.sg += home_goals - away_goals
		away_team.sg += away_goals - home_goals
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
		return home(request, round)
	return home(request, 1)

def	restart_teams():
	teams_list = Team.objects.all()
	for team in teams_list:
		team.points = 0
		team.goals_pro = 0
		team.goals_con = 0
		team.wins = 0
		team.loss = 0
		team.draws = 0
		team.sg = 0
		print ('oi')
		team.save()
	
def	restart_games():
	game_list = Game.objects.all()
	for game in game_list:
		game.home_goals = None
		game.away_goals = None
		game.played = False
		game.save()

def	restart(request):
	restart_teams()
	restart_games()
	return home(request, 1)

def next_round(request):
	round = int(request.POST.get('current_round'))
	return home(request, round + 1)

def prev_round(request):
	round = int(request.POST.get('current_round'))
	return home(request, round - 1)
