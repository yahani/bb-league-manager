from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.generics import get_object_or_404, ListAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from league.serializers import GameSerializer,GamePlayerSerializer
from league.models import Team,Game,Player, GamePlayer


class GameEndPoint(APIView):
    def put(self, request):
        if 'team1' not in request.data or 'team2' not in request.data or 'team1_score' not in request.data or 'team2_score' not in request.data or 'date' not in request.data:
            raise ParseError("Empty content")
        
        team1_id = request.data.pop('team1')
        team1 = get_object_or_404(Team.objects.all(), pk=team1_id)
        team2_id= request.data.pop('team2')
        team2 = get_object_or_404(Team.objects.all(), pk=team2_id)
        team1_score =request.data.pop('team1_score')
        team2_score =request.data.pop('team2_score')
        date =request.data.pop('date')

        game = Game.objects.create(team1=team1, team2=team2, team1_score=team1_score, team2_score=team2_score,date=date)

        gameSerializer = GameSerializer(game, many=False)
        return Response(gameSerializer.data, status=status.HTTP_200_OK)

    def post(self, request, game_id):
        db_game = get_object_or_404(Game.objects.all(), pk=game_id)

        data = request.data
        serializer = GameSerializer(instance=db_game, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, game_id):
        db_game = get_object_or_404(Game.objects.all(), pk=game_id)

        serializer = GameSerializer(db_game, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, game_id):
        db_game = get_object_or_404(Game.objects.all(), pk=game_id)
        db_game.delete()
        return Response({"message": "Game ID `{}` has been deleted.".format(game_id)}, status=status.HTTP_200_OK)

class GamePlayerEndPoint(APIView):
    def put(self, request):
        if 'game' not in request.data or 'player' not in request.data or 'score' not in request.data:
            raise ParseError("Empty content")
        
        game_id = request.data.pop('game')
        game = get_object_or_404(Game.objects.all(), pk=game_id)
        player_id= request.data.pop('player')
        player = get_object_or_404(Player.objects.all(), pk=player_id)
        score =request.data.pop('score')

        game_player = GamePlayer.objects.create(game=game, player=player, score=score)

        gamePlayerSerializer = GamePlayerSerializer(game_player, many=False)
        return Response(gamePlayerSerializer.data, status=status.HTTP_200_OK)

    def post(self, request, record_id):
        db_gameplayer = get_object_or_404(GamePlayer.objects.all(), pk=record_id)

        data = request.data
        serializer = GamePlayerSerializer(instance=db_gameplayer, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, record_id):
        db_gameplayer = get_object_or_404(GamePlayer.objects.all(), pk=record_id)

        serializer = GamePlayerSerializer(db_gameplayer, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, record_id):
        db_gameplayer = get_object_or_404(GamePlayer.objects.all(), pk=record_id)
        db_gameplayer.delete()
        return Response({"message": "Record ID `{}` has been deleted.".format(record_id)}, status=status.HTTP_200_OK)