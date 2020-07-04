from django.conf.urls import url
from django.urls import include
from league.views.teams import TeamEndPoint
from league.views.users import CoachEndPoint, PlayerEndPoint
from league.views.games import GameEndPoint, GamePlayerEndPoint
from league.views.scoreboard import GamesViewSet,TeamAverageEndPoint,PlayerAverageEndPoint,PlayerPercentileEndPoint
from rest_framework import routers

urlpatterns = [
    #basic CRUD
    url(r'^teams/$', TeamEndPoint.as_view()),
    url(r'^teams/(?P<team_id>[0-9]+)', TeamEndPoint.as_view()),
    url(r'^users/coach/$', CoachEndPoint.as_view()),
    url(r'^users/coach/(?P<user_id>[0-9]+)', CoachEndPoint.as_view()),
    url(r'^users/player/$', PlayerEndPoint.as_view()),
    url(r'^users/player/(?P<user_id>[0-9]+)', PlayerEndPoint.as_view()),
    url(r'^games/$', GameEndPoint.as_view()),
    url(r'^games/(?P<game_id>[0-9]+)', GameEndPoint.as_view()),
    url(r'^game-player/$', GamePlayerEndPoint.as_view()),
    url(r'^game-player/(?P<record_id>[0-9]+)', GamePlayerEndPoint.as_view()),

    #special API calls
    url(r'^scoreboard/games/$', GamesViewSet.as_view({'post': 'list'})),
    url(r'^scoreboard/team-average/(?P<team_id>[0-9]+)', TeamAverageEndPoint.as_view()),
    url(r'^scoreboard/player-average/(?P<player_id>[0-9]+)', PlayerAverageEndPoint.as_view()),
    url(r'^scoreboard/team-percentile/(?P<team_id>[0-9]+)', PlayerPercentileEndPoint.as_view()),
    
]
