from django.contrib import admin

# Register your models here.

from .models import Team, Game, League

admin.site.register(Team)
admin.site.register(Game)
admin.site.register(League)