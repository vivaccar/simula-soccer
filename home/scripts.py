from .models import Team, Game
from django.utils import timezone

def	create_teams(data):
	for team_data in data['response']:
		team_infos = team_data['team']
		venue_infos = team_data['venue']
		team = Team.objects.create(
			id_name = team_infos['name'],
			name = team_infos['name'],
			stadium = venue_infos['name'],
			logo = team_infos['logo']
		)

def create_games(data):
	rd = 1
	i = 1
	for game_data in data['response']:
		game = Game.objects.create(
			home_team = Team.objects.get(id_name = game_data['teams']['home']['name']),
			away_team = Team.objects.get(id_name = game_data['teams']['away']['name']),
			home_logo = game_data['teams']['home']['logo'],
			away_logo = game_data['teams']['away']['logo'],
			round = rd
		)
		i += 1
		if i == 11:
			rd += 1
			i = 1

def	update_points(game, home_team, away_team):
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
		home_team.save()
		away_team.save()

def	get_updated_games(data):
	game_list = Game.objects.all()
	for game_data, game in zip(data['response'], game_list):
		timestamp = game_data['fixture']['timestamp']
		time_utc = timezone.datetime.utcfromtimestamp(timestamp)
		local_utc = time_utc.astimezone(timezone.get_current_timezone())
		game.timestamp = local_utc
		game.home_goals = game_data['goals']['home']
		game.away_goals = game_data['goals']['away']
		if (game_data['fixture']['status']['long'] == 'Match Finished'):
			update_points(game, game.home_team, game.away_team)
			game.played = True
			print(game_data['fixture']['status']['long'])
		game.save()
