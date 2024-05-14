from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import Team, Game
from .forms import Game_forms
from .scripts import create_games, create_teams, get_updated_games, aproveitamento
import requests, time
	
# Create your views here.

def	home(request):
	return render(request, 'index.html')

def reset_result(game, home_team, away_team):
	home_team.games_played -= 1
	away_team.games_played -= 1
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
	game.home_goals = None
	game.away_goals = None
	game.played = False
	game.save()
	home_team.save()
	away_team.save()

def current_timestamp():
    return int(time.time())

def	get_current_round():
	cur_timestamp = current_timestamp()
	game_list = Game.objects.all()
	for game in game_list:
		game_time = int(game.timestamp)
		if game_time > cur_timestamp:
			return game.round


def brasil_serie_a(request, round=1):
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
			reset_result(game_class, home_team, away_team)
		round = game_class.round
		home_team.games_played += 1
		away_team.games_played += 1
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
		home_team.aproveitamento = aproveitamento(home_team)
		away_team.aproveitamento = aproveitamento(away_team)
		game_class.played = True
		game_class.save()
		home_team.save()
		away_team.save()
		games_list = Game.objects.filter(round = round)
		teams_list = Team.objects.order_by('-points', '-wins', '-sg')
		context = {'teams_list': teams_list, 'games_list': games_list, 'current_round' : round}
		return render(request, 'home.html', context)
	round = get_current_round()
	games_list = Game.objects.filter(round = round)
	teams_list = Team.objects.order_by('-points', '-wins', '-sg')
	context = {'teams_list': teams_list, 'games_list': games_list, 'current_round' : round}
	return render(request, 'home.html', context)

def	restart_teams(teams_list):
	for team in teams_list:
		team.points = 0
		team.goals_pro = 0
		team.goals_con = 0
		team.wins = 0
		team.loss = 0
		team.draws = 0
		team.sg = 0
		team.games_played = 0
		team.save()
	
def	restart_games(game_list):
	for game in game_list:
		game.home_goals = None
		game.away_goals = None
		game.played = False
		game.save()

def	restart(request):
	restart_teams(Team.objects.all())
	restart_games(Game.objects.all())

def reset_simulation(request):
	game_list = Game.objects.all()
	if (request.method == 'POST'):
		for game in game_list:
			if (game.played == True and game.real_played == False):
				reset_result(game, game.home_team, game.away_team)
	round = get_current_round()
	games_list = Game.objects.filter(round = round)
	teams_list = Team.objects.order_by('-points', '-wins', '-sg')
	context = {'teams_list': teams_list, 'games_list': games_list, 'current_round' : round}
	return render(request, 'home.html', context)


def next_round(request):
	round = int(request.POST.get('current_round'))
	games_list = Game.objects.filter(round = round + 1)
	teams_list = Team.objects.order_by('-points', '-wins', '-sg')
	context = {'teams_list': teams_list, 'games_list': games_list, 'current_round' : round + 1}
	return render(request, 'home.html', context)

def prev_round(request):
	round = int(request.POST.get('current_round'))
	games_list = Game.objects.filter(round = round - 1)
	teams_list = Team.objects.order_by('-points', '-wins', '-sg')
	context = {'teams_list': teams_list, 'games_list': games_list, 'current_round' : round - 1}
	return render(request, 'home.html', context)

def api_football(request):
	if (request.method == 'POST'):
		url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
		querystring = {"league":"71", "season":"2024"}
		headers = {
			"X-RapidAPI-Key": "1b8ffa34e2mshb6c3096387b53eep1345dcjsn899e6d7dd07c",
			"X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
		}
		response = requests.get(url, headers=headers, params=querystring)
		data = response.json()
		restart(request)
		get_updated_games(data)
	return(home(request))