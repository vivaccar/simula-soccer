from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import Team, Game, League
from .forms import Game_forms
from .scripts import create_games, create_teams, get_updated_games, aproveitamento, create_league, update_positions
from itertools import combinations
import requests, time
from django.http import JsonResponse
import json
import json

# Create your views here.

def	home(request):
	leagues_list = League.objects.all()
	context = {"leagues_list": leagues_list}
	return render(request, 'home.html', context)

def	get_data(request):
	id_liga = int(request.POST.get('league_id'))
	league = League.objects.get(league_id=id_liga)
	teamslist = Team.objects.filter(league_id=id_liga)
	gameslist = Game.objects.filter(league_id=id_liga)
	if (id_liga == 71  or id_liga == 72):
		teams_list = teamslist.order_by('-points', '-wins', '-sg', '-goals_pro')
	else:
		teams_list = teamslist.order_by('-points', '-sg', '-goals_pro')
	data = {
		'league_data': {
			'league_id': league.league_id,
			'name': league.league_name,
			'logo': league.logo,
			'country': league.country,
			'url': league.url,
			'zone_1': league.zone_1,
			'zone_1_txt': league.zone_1_txt,
			'zone_2': league.zone_2,
			'zone_2_txt': league.zone_2_txt,
			'zone_3': league.zone_3,
			'zone_3_txt': league.zone_3_txt,
			'zone_4': league.zone_4_txt,
			'zone_4_txt': league.zone_4_txt,
			'zone_5': league.zone_5,
			'zone_5_txt': league.zone_5_txt,
			'zone_reb': league.zone_reb,
			'zone_reb_txt': league.zone_reb_txt,
		},
		'teams': [],
		'games': []
	}
	for team in teams_list:
		data['teams'].append({
			'id_name': team.id_name,
			'name': team.name,
			'points': team.points,
			'wins': team.wins,
			'draws': team.draws,
			'loss': team.loss,
			'goals_pro': team.goals_pro,
			'goals_con': team.goals_con,
			'aproveitamento': team.aproveitamento,
			'sg': team.sg,
			'logo': team.logo,
			'stadium': team.stadium,
			'games_played': team.games_played,
	})
	for game in gameslist:
		data['games'].append({
			'league_id' : game.league_id,
			'game_id': game.id,
			'stadium': game.stadium,
			'home_team': game.home_team.name,
			'away_team': game.away_team.name,
			'home_goals': game.home_goals,
			'away_goals': game.away_goals,
			'simulated': game.simulated,
			'real_played': game.real_played,
			'round': game.round,
			'timestamp': game.timestamp,
			'local_time': game.local_time,
	})
	return (JsonResponse(data, safe=False))

def	premier_league(request):
	league = League.objects.get(league_id = 39)
	teams_list = update_positions(39)
	context = {'league': league, 'teams_list': teams_list}
	return render(request, 'league.html', context)

def	la_liga(request):
	league = League.objects.get(league_id = 140)
	teams_list = update_positions(140)
	new_teams_list = desempate(teams_list)
	context = {'league': league, 'teams_list': new_teams_list}
	return render(request, 'league.html', context)

def	serie_a(request):
	league = League.objects.get(league_id = 135)
	teams_list = update_positions(135)
	new_teams_list = desempate(teams_list)
	context = {'league': league, 'teams_list': new_teams_list}
	return render(request, 'league.html', context)

def	bundesliga(request):
	league = League.objects.get(league_id = 78)
	teams_list = update_positions(78)
	context = {'league': league, 'teams_list': teams_list}
	return render(request, 'league.html', context)

def brasil_serie_a(request):
	league = League.objects.get(league_id = 71)
	teams_list = update_positions(71)
	leagues_list = League.objects.all()
	context = {'ĺeagues_list': leagues_list, 'league': league, 'teams_list': teams_list}
	return render(request, 'league.html', context)

def brasil_serie_b(request):
	league = League.objects.get(league_id = 72)
	teams_list = update_positions(72)
	context = {'league': league, 'teams_list': teams_list}
	return render(request, 'league.html', context)

def primeira_liga(request):
	league = League.objects.get(league_id = 94)
	teams_list = update_positions(94)
	context = {'league': league, 'teams_list': teams_list}
	return render(request, 'league.html', context)

def find_index(array, item):
	for index, element in enumerate(array):
		if element == item:
			return index

def desempate(teams_list):
	team_pairs = combinations(teams_list, 2)
	print("ENTROU NO DESEMPATE")

	for team1, team2 in team_pairs:
		if team1.points == team2.points:
			game_1 = Game.objects.get(home_team_id = team1.id, away_team_id = team2.id)
			game_2 = Game.objects.get(home_team_id = team2.id, away_team_id = team1.id)
			team1_goals = game_1.home_goals + game_2.away_goals
			team2_goals = game_1.away_goals + game_2.home_goals
			if team2_goals > team1_goals:
				item1 = teams_list.get(id = team1.id)
				item2 = teams_list.get(id = team2.id)
				print (item1, item1.position, team1_goals)
				print (item2, item2.position, team2_goals)
				temp = item1.position
				item1.position = item2.position
				item2.position = temp
				print (item1, item1.position)
				print (item2, item2.position)
				item1.save()
				item2.save()
			teams_list = teams_list.order_by('position')
	return(teams_list)
