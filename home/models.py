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

	def __str__(self):
		return self.name