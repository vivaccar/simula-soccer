from django.db import models

# Create your models here.

class	Team(models.Model):
	id_name = models.CharField(max_length=30, default=None)
	name = models.CharField(max_length = 20, default=None)
	league_id = models.IntegerField(default=None, null=True, blank=True)
	stadium = models.CharField(max_length=50, default=None)
	logo = models.CharField(max_length=150, default=None)
	points = models.IntegerField(default = 0)
	goals_pro = models.IntegerField(default = 0)
	goals_con = models.IntegerField(default = 0)
	wins = models.IntegerField(default = 0)
	draws = models.IntegerField(default = 0)
	loss = models.IntegerField(default = 0)
	sg = models.IntegerField(default=0)
	aproveitamento = models.FloatField(default=0)
	games_played = models.IntegerField(default=0)

	def __str__(self):
		return self.name
	

class	Game(models.Model):
	league_id = models.IntegerField(default=None, null=True, blank=True)
	home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_team')
	away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_team')
	home_goals = models.IntegerField(default = None, null=True, blank=True)
	away_goals = models.IntegerField(default = None, null=True, blank=True)
	played = models.BooleanField(default=False)
	real_played= models.BooleanField(default=False)
	round = models.IntegerField(default = 1)
	timestamp = models.CharField(max_length=150, null=True, default=None)
	local_time = models.CharField(max_length=150, default=None, null=True, blank=True)

	def __str__(self):
		return self.home_team.name + ' X ' + self.away_team.name

class	League(models.Model):
	league_id = models.IntegerField(default=None, null=True, blank=True)
	league_name = models.CharField(max_length=30, default=None)
	logo = logo = models.CharField(max_length=150, default=None)
	country = models.CharField(max_length = 30, default=None)
	url = models.CharField(max_length=150, null=True, blank=True, default = '')

	def	get_games_from_league(cls):
		games = Game.objects.filter(league_id=cls.league_id)
		return games
	
	def	get_teams_from_league(cls):
		teams = Game.objects.filter(league_id=cls.league_id)
		return teams

	def __str__(self):
		return self.league_name