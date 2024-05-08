from django.db import models

# Create your models here.

class	Team(models.Model):
	name = models.CharField(max_length = 20)
	points = models.IntegerField(default = 0)
	goals_pro = models.IntegerField(default = 0)
	goals_con = models.IntegerField(default = 0)
	wins = models.IntegerField(default = 0)
	draws = models.IntegerField(default = 0)
	loss = models.IntegerField(default = 0)
	sg = models.IntegerField(default=0)

	def __str__(self):
		return self.name

class	Game(models.Model):
	home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_team')
	away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_team')
	home_goals = models.IntegerField(default = None, null=True, blank=True)
	away_goals = models.IntegerField(default = None, null=True, blank=True)
	played = models.BooleanField(default=False)
	round = models.IntegerField(default = 1)

	def __str__(self):
		return self.home_team.name + ' X ' + self.away_team.name
