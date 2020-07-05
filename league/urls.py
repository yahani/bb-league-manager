from django.conf.urls import url
from django.urls import include
from league.views.teams import TeamEndPoint
from league.views.users import CoachEndPoint, PlayerEndPoint
from league.views.games import GameEndPoint, GamePlayerEndPoint
from league.views.scoreboard import *
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    #basic CRUD, admin only
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

    #Login
    url(r'^login/', LoginEndPoint.as_view(), name='login'),
    url(r'^logout/', LogoutEndPoint.as_view(), name='logout'),

    #special API calls
    url(r'^scoreboard/$', GamesViewSet.as_view({'post': 'list'}),name='scoreboard'),
    url(r'^team-average/(?P<team_id>[0-9]+)', TeamAverageEndPoint.as_view(),name='team-average'),
    url(r'^team-players/(?P<team_id>[0-9]+)', TeamPlayersEndPoint.as_view(),name='team-players'),
    url(r'^team-players/$', TeamPlayersEndPoint.as_view(),name='my-team'),
    url(r'^player-average/(?P<player_id>[0-9]+)', PlayerAverageEndPoint.as_view(),name='player-average'),
    url(r'^team-percentile/(?P<team_id>[0-9]+)', PlayerPercentileEndPoint.as_view(),name='team-percentile'),
    
    #admin site stat API calls
    url(r'^site-stats/$', SiteStatEndPoint.as_view()),
    url(r'^site-stats/(?P<user_id>[0-9]+)', SiteStatEndPoint.as_view()),
    
]
