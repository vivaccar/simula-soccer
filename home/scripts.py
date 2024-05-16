from .models import Team, Game, League
from math import modf
from django.utils import timezone
import requests

def	create_teams(l_id, season):
	url = "https://api-football-v1.p.rapidapi.com/v3/teams"

	querystring = {"league": l_id,"season": season}

	headers = {
		"X-RapidAPI-Key": "1b8ffa34e2mshb6c3096387b53eep1345dcjsn899e6d7dd07c",
		"X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
	}

	response = requests.get(url, headers=headers, params=querystring)
	data = response.json()
	for team_data in data['response']:
		team_infos = team_data['team']
		venue_infos = team_data['venue']
		team = Team.objects.create(
			id_name = team_infos['name'],
			name = team_infos['name'],
			stadium = venue_infos['name'],
			logo = team_infos['logo'],
			league_id = l_id,

		)

def create_games(l_id, season, games_per_round):
	url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"

	querystring = {"league": l_id,"season":season}

	headers = {
		"X-RapidAPI-Key": "1b8ffa34e2mshb6c3096387b53eep1345dcjsn899e6d7dd07c",
		"X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
	}

	response = requests.get(url, headers=headers, params=querystring)
	data = response.json()
	rd = 1
	i = 1
	for game_data in data['response']:
		game = Game.objects.create(
			home_team = Team.objects.get(id_name = game_data['teams']['home']['name']),
			away_team = Team.objects.get(id_name = game_data['teams']['away']['name']),
			timestamp = game_data['fixture']['timestamp'],
			round = rd,
			league_id = l_id
		)
		i += 1
		if i > games_per_round:
			rd += 1
			i = 1

def	update_table(game, home_team, away_team):
		home_team.games_played += 1
		away_team.games_played += 1
		home_team.goals_pro += game.home_goals
		away_team.goals_pro += game.away_goals
		home_team.goals_con += game.away_goals
		away_team.goals_con += game.home_goals
		home_team.sg += game.home_goals - game.away_goals
		away_team.sg += game.away_goals - game.home_goals
		if game.home_goals > game.away_goals:
			home_team.wins += 1
			away_team.loss += 1
			home_team.points += 3
		elif game.home_goals == game.away_goals:
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
		home_team.save()
		away_team.save()


def	get_updated_games():
	url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
	querystring = {"league":"39", "season":"2023"}
	headers = {
		"X-RapidAPI-Key": "a915c948a2mshd5daae6b916daabp1b5891jsn54b9950682d1",
		"X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
	}
	response = requests.get(url, headers=headers, params=querystring)
	data = response.json()
	game_list = Game.objects.filter(league_id = 39)
	for game_data, game in zip(data['response'], game_list):
		timestamp = game_data['fixture']['timestamp']
		game.timestamp = timestamp
		time_utc = timezone.datetime.utcfromtimestamp(timestamp)
		local_utc = time_utc.astimezone(timezone.get_current_timezone())
		game.local_time = str(local_utc)[:16]
		game.league_id = game_data['league']['id']
		game.home_goals = game_data['goals']['home']
		game.away_goals = game_data['goals']['away']
		if (game_data['fixture']['status']['long'] == 'Match Finished'):
			update_table(game, game.home_team, game.away_team)
			game.real_played = True
			print(game_data['fixture']['status']['long'])
		game.save()



def	create_league(league_id, season):
		url = "https://api-football-v1.p.rapidapi.com/v3/leagues"
		querystring = {"id": league_id, "season": season}
		headers = {
		"X-RapidAPI-Key": "1b8ffa34e2mshb6c3096387b53eep1345dcjsn899e6d7dd07c",
		"X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
		}
		response = requests.get(url, headers=headers, params=querystring)
		data = response.json()
		league = League.objects.create(
			league_id = data['response'][0]['league']['id'],
			league_name = data['response'][0]['league']['name'],
			logo = data['response'][0]['league']['logo'],
			country = data['response'][0]['country']['name'],
		)

def	update_teams():
	teams_list = Team.objects.filter(id__range=(61, 79))
	for item in teams_list:
		item.league_id = 72
		item.save()

def	update_games():	
	games_list = Game.objects.filter(id__range=(381, 760))
	for item in games_list:
		item.league_id = 72
		item.save()

def aproveitamento(team):
	disputed = team.games_played * 3
	gained = team.points
	if gained == 0:
		return 0
	return round((gained/disputed) * 100, 1)

def	game_time():
	game_list = Game.objects.all()
	for game in game_list:
		time_str = str(game.local_time)
		game_time = time_str[:16]
		game.local_time = game_time
		game.save()

