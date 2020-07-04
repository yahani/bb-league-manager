from django.conf.urls import url
from django.urls import include
from league.views.teams import TeamEndPoint
from league.views.users import CoachEndPoint, PlayerEndPoint
from league.views.games import GameEndPoint
from rest_framework import routers

urlpatterns = [
    url(r'^teams/$', TeamEndPoint.as_view()),
    url(r'^teams/(?P<team_id>[0-9]+)', TeamEndPoint.as_view()),
    url(r'^users/coach/$', CoachEndPoint.as_view()),
    url(r'^users/coach/(?P<user_id>[0-9]+)', CoachEndPoint.as_view()),
    url(r'^users/player/$', PlayerEndPoint.as_view()),
    url(r'^users/player/(?P<user_id>[0-9]+)', PlayerEndPoint.as_view()),
    url(r'^games/$', GameEndPoint.as_view()),
    url(r'^games/(?P<game_id>[0-9]+)', GameEndPoint.as_view()),
]
