from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.generics import get_object_or_404, ListAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import authenticate
from league.models import Team,Game,Player,GamePlayer,LoginEntry,User,Coach
from league.serializers import GameSerializer,PlayerAvgSerializer,TeamPlayersSerializer,LoginEntrySerializer
from django.db.models import Avg,Count,F,Q,Sum
from django.db.models.expressions import RawSQL
import math
from datetime import datetime,timezone
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from league.permissions import IsCoach,IsCoachOrAdmin

class LoginEndPoint(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        if 'username' not in request.data or 'password' not in request.data:
            raise ParseError("Empty content")

        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            #end previous session
            login_entries_db = LoginEntry.objects.filter(user=user).order_by('-login_time').filter(logout_time=None)
            if login_entries_db.count()>0:
                login_entry_db = login_entries_db[0]
                now = datetime.now(timezone.utc)
                login_entry_db.logout_time = now
                login_entry_db.session_time = (now-login_entry_db.login_time).total_seconds() / 60
                login_entry_db.save()
            #new session
            LoginEntry.objects.create(user=user)
            refresh = RefreshToken.for_user(user)
            token = str(refresh.access_token)
            return Response({'username':username,'token':token}, status=status.HTTP_200_OK)
        else:
            return Response({'message':'invalid username or password'}, status=status.HTTP_403_FORBIDDEN)

class LogoutEndPoint(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        login_entry_db = LoginEntry.objects.filter(user=request.user).order_by('-login_time').filter(logout_time=None)[0]
        now = datetime.now(timezone.utc)
        login_entry_db.logout_time = now
        login_entry_db.session_time = (now-login_entry_db.login_time).total_seconds() / 60
        return Response({'message':'successfully logged out'}, status=status.HTTP_200_OK)

class GamesViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)

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

class TeamPlayersEndPoint(APIView):
    permission_classes = (IsAuthenticated, IsCoachOrAdmin,)
    def get(self, request, team_id):
        db_team = get_object_or_404(Team.objects.all(), pk=team_id)
        if request.user.is_coach:
            coach = Coach.objects.filter(user=request.user)[0]
            if coach.team == db_team:
                serializer = TeamPlayersSerializer(db_team, many=False)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'message':'you dont have permission to view this details'}, status=status.HTTP_403_FORBIDDEN)
        else:
            serializer = TeamPlayersSerializer(db_team, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if request.user.is_coach:
            coach = Coach.objects.filter(user=request.user)[0]
            serializer = TeamPlayersSerializer(coach.team, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message':'This action is not allowed'}, status=status.HTTP_400_BAD_REQUEST)
        
    
class TeamAverageEndPoint(APIView):
    permission_classes = (IsAuthenticated, IsCoachOrAdmin,)
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
        if request.user.is_coach:
            coach = Coach.objects.filter(user=request.user)[0]
            if coach.team == db_team:
                return Response(avg, status=status.HTTP_200_OK)
            else:
                return Response({'message':'you dont have permission to view this details'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(avg, status=status.HTTP_200_OK)

class PlayerAverageEndPoint(APIView):
    permission_classes = (IsAuthenticated, IsCoachOrAdmin,)

    def get(self, request, player_id):
        db_player = get_object_or_404(Player.objects.all(), pk=player_id)
        records = db_player.game_players.all()
        avg = records.aggregate(Avg('score'))
        count = records.count()
        response = {'name':db_player.user.username, 'height':db_player.height,'weight':db_player.weight,'average':avg['score__avg'],'num_of_games':count}
        if request.user.is_coach:
            coach = Coach.objects.filter(user=request.user)[0]
            if coach.team.players.filter(pk=player_id).count()>0:
                return Response(response, status=status.HTTP_200_OK)
            else:
                return Response({'message':'you dont have permission to view this details'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(response, status=status.HTTP_200_OK)

class PlayerPercentileEndPoint(APIView):
    permission_classes = (IsAuthenticated, IsCoach,)
    def post(self, request, team_id):
        db_team = get_object_or_404(Team.objects.all(), pk=team_id)
        coach = Coach.objects.filter(user=request.user)[0]
        if coach.team == db_team:
            if 'percentile' in request.data:
                percentile = request.data['percentile']
            else:
                percentile = 0.9

            players = db_team.players.all().annotate(
                avg_score=Avg(('game_players__score')),
                )
            total_count = players.count()
            percentile_index = math.floor(total_count*percentile)
            percentile_index = total_count-percentile_index
            top_scores = (players
                        .order_by('-avg_score')
                        .values_list('avg_score', flat=True))
            top_records = (players
                        .order_by('-avg_score')
                        .filter(avg_score__in=top_scores[:percentile_index]))

            serializer = PlayerAvgSerializer(top_records, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message':'you dont have permission to view this details'}, status=status.HTTP_403_FORBIDDEN)

class SiteStatEndPoint(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)
    def post(self,request):
        login_entries_db = LoginEntry.objects.filter(logout_time=None)
        serializer = LoginEntrySerializer(login_entries_db, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self,request,user_id):
        user = get_object_or_404(User.objects.all(),pk=user_id)
        time = LoginEntry.objects.filter(user=user).filter(session_time__isnull=False).aggregate(Sum('session_time'))
        visits = LoginEntry.objects.filter(user=user).count()
        return Response({'username':user.username, 'total time':time, 'visits':visits}, status=status.HTTP_200_OK)


