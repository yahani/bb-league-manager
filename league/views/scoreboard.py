from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.generics import get_object_or_404, ListAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from league.models import Team,Game,Player,GamePlayer
from league.serializers import GameSerializer,PlayerAvgSerializer
from django.db.models import Avg,Count,F,Q
from django.db.models.expressions import RawSQL
import math

class GamesViewSet(ModelViewSet):

    def get_queryset(self):
        queryset = Game.objects.all()
        return queryset

    def list(self, request, *args, **kwargs):

        data = request.data

        sort_date_asc = data['sort_type'] if 'sort_type' in data else 'desc'
        sort_type = 'date' if sort_date_asc == 'asc' else '-date'
        queryset =self.get_queryset()
        queryset = queryset.order_by(sort_type)

        serializer = GameSerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class TeamAverageEndPoint(APIView):
    def get(self, request, team_id):
        db_team = get_object_or_404(Team.objects.all(), pk=team_id)
        avg1 = db_team.game_team1.aggregate(Avg('team1_score'))
        avg2 = db_team.game_team2.aggregate(Avg('team2_score'))
        if avg1['team1_score__avg'] is None and avg2['team2_score__avg'] is None:
            avg = 0
        if avg1['team1_score__avg'] is None or avg2['team2_score__avg'] is None :
            avg = avg1['team1_score__avg'] if avg2['team2_score__avg'] is None else avg2['team2_score__avg']
        else:
            avg = (avg1['team1_score__avg']+avg2['team2_score__avg'])/2

        return Response(avg, status=status.HTTP_200_OK)

class PlayerAverageEndPoint(APIView):
    def get(self, request, player_id):
        db_player = get_object_or_404(Player.objects.all(), pk=player_id)
        records = db_player.game_players.all()
        avg = records.aggregate(Avg('score'))
        count = records.count()
        response = {'name':db_player.user.username, 'height':db_player.height,'weight':db_player.weight,'average':avg,'num_of_games':count}

        return Response(response, status=status.HTTP_200_OK)

class RawAnnotation(RawSQL):
    """
    RawSQL also aggregates the SQL to the `group by` clause which defeats the purpose of adding it to an Annotation.
    """
    def get_group_by_cols(self):
        return []

class PlayerPercentileEndPoint(APIView):
    def get(self, request, team_id):
        db_team = get_object_or_404(Team.objects.all(), pk=team_id)
        players = db_team.players.all().annotate(
            avg_score=Avg(('game_players__score')),
            )
        total_count = players.count()
        percentile_index = math.floor(total_count*0.9)
        print(percentile_index)
        #players = players.annotate(
        #    percentile=Count(('user'), filter=Q(avge_score__gt=F('avge_score')))/total_count,
        #    )
        top_scores = (players
                     .order_by('-avg_score')
                     .values_list('avg_score', flat=True)
                     .distinct())
        top_records = (players
                      .order_by('-avg_score')
                      .filter(avg_score__in=top_scores[:percentile_index]))

        serializer = PlayerAvgSerializer(top_records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)