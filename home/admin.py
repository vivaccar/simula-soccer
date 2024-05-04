from django.contrib import admin

# Register your models here.

from .models import Team, Game

admin.site.register(Team)
admin.site.register(Game)