from django.contrib import admin

# Register your models here.
from league.models import User,Player,Coach,Team,Game,GamePlayer,LoginEntry

admin.site.register(User)
admin.site.register(Player)
admin.site.register(Coach)
admin.site.register(Team)
admin.site.register(Game)
admin.site.register(GamePlayer)
admin.site.register(LoginEntry)