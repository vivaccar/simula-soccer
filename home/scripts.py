from .models import Team, Game, League
from math import modf
from django.utils import timezone
import requests

def update_positions(l_id):
	if (l_id == 71 or l_id == 72):
		teams_list = Team.objects.filter(league_id = l_id).order_by('-points', '-wins', '-sg', 'goals_pro')
	else:
		teams_list = Team.objects.filter(league_id = l_id).order_by('-points', '-sg', '-goals_pro')
	i = 1
	for team in teams_list:
		team.position = i
		i = i + 1
		print(f'time: {team}, posicao: {team.position}')
		team.save()
	return(teams_list)

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


def	get_updated_games(l_id, season):

	url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
	querystring = {"league":l_id, "season":season}
	headers = {
		"X-RapidAPI-Key": "a915c948a2mshd5daae6b916daabp1b5891jsn54b9950682d1",
		"X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
	}
	response = requests.get(url, headers=headers, params=querystring)
	data = response.json()
	print ("Updating league: " + str(l_id))
	game_list = Game.objects.filter(league_id = l_id)
	restart_teams(Team.objects.filter(league_id = l_id))
	restart_games(game_list)
	for game_data, game in zip(data['response'], game_list):
		timestamp = game_data['fixture']['timestamp']
		game.timestamp = timestamp
		time_utc = timezone.datetime.utcfromtimestamp(timestamp)
		local_utc = time_utc.astimezone(timezone.get_current_timezone())
		game.local_time = str(local_utc)[:16]
		game.league_id = game_data['league']['id']
		game.home_goals = game_data['goals']['home']
		game.away_goals = game_data['goals']['away']
		game.stadium = game_data['fixture']['venue']['name']
		if (game_data['fixture']['status']['long'] == 'Match Finished'):
			update_table(game, game.home_team, game.away_team)
			game.real_played = True
		game.save()
	convert_date(game_list)

def	check_stadiums(games):
	for game in games:
		if game.stadium == 'Estádio Major Antônio Couto Pereira':
			game.stadium = 'Couto Pereira'
			game.save()
		elif game.stadium == 'Estádio Governador Magalhães Pinto':
			game.stadium = 'Mineirão'
			game.save()
		elif game.stadium == 'Estádio José Pinheiro Borda':
			game.stadium = 'Beira-Rio'
			game.save()
		elif game.stadium == 'Estadio Jornalista Mário Filho':
			game.stadium = 'Maracanã'
			game.save()
		elif game.stadium == 'Estádio Urbano Caldeira':
			game.stadium = 'Vila Belmiro'
			game.save()
		elif game.stadium == 'Estádio Governador Plácido Aderaldo Castelo':
			game.stadium = 'Castelão'
			game.save()
		elif game.stadium == 'Estádio Raimundo Sampaio':
			game.stadium = 'Independência'
			game.save()
		

def	request_data_from_api():
	get_updated_games(71, 2024)
	get_updated_games(72, 2024)
	get_updated_games(39, 2023)
	get_updated_games(140, 2023)
	get_updated_games(78, 2023)
	get_updated_games(135, 2023)
	games = Game.objects.all()
	check_stadiums(games)
	
def	create_league(league_id, season, l_url):
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
			url = l_url
		)


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

def update_zones():
	serie = League.objects.get(league_id = 135)
	
	serie.zone_1 = 4
	serie.zone_1_txt = 'Classificados à fase de grupos da UEFA Champions League'
	serie.zone_2 = 5
	serie.zone_2_txt = 'Classificado à UEFA Europa League'
	serie.zone_3 = 6
	serie.zone_3_txt = 'Classificado à fase preliminar da UEFA Europa Conference League'
	serie.zone_reb = 18
	serie.zone_reb_txt = 'Rebaixados à Serie B'

	serie.save()
	

def convert_date(game_list):
	for game in game_list:
		year = game.local_time[2:4]
		month = game.local_time[5:7]
		day = game.local_time[8:10]
		hour = game.local_time[11:16]
		game.local_time = day + '/' + month + '/' + year + ' - '  + hour
		game.save()

def create_and_update_league(l_id, season, games_per_round, l_url):
	create_league(l_id, season, l_url)
	create_teams(l_id, season)
	create_games(l_id, season, games_per_round)
	get_updated_games(l_id, season)
