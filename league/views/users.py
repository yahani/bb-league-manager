from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.generics import get_object_or_404, ListAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from league.serializers import CoachTeamSerializer,UserSerializer,CoachSerializer,PlayerTeamSerializer,PlayerSerializer
from league.models import User,Coach,Team,Player
# Create your views here.

class CoachEndPoint(APIView):
    def put(self, request):
        if 'username' not in request.data or 'password' not in request.data or 'email' not in request.data or 'team_id' not in request.data:
            raise ParseError("Empty content")

        coachSerializer = CoachSerializer(data=request.data)
        if coachSerializer.is_valid():
            coachSerializer.save()
            return Response(coachSerializer.data, status=status.HTTP_200_OK)
        else:
            return Response(coachSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, user_id):
        db_user = get_object_or_404(Coach.objects.all(), pk=user_id)

        data = request.data
        serializer = CoachSerializer(instance=db_user, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, user_id):
        db_coach = get_object_or_404(Coach.objects.all(), pk=user_id)

        serializer = CoachTeamSerializer(db_coach, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, user_id):
        user = get_object_or_404(Coach.objects.all(), pk=user_id)
        user.delete()
        return Response({"message": "Coach ID `{}` has been deleted.".format(user_id)}, status=status.HTTP_200_OK)


class PlayerEndPoint(APIView):
    def put(self, request):
        if 'username' not in request.data or 'password' not in request.data or 'email' not in request.data or 'team_id' not in request.data:
            raise ParseError("Empty content")

        playerSerializer = PlayerSerializer(data=request.data)
        if playerSerializer.is_valid():
            playerSerializer.save()
            return Response(playerSerializer.data, status=status.HTTP_200_OK)
        else:
            return Response(playerSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, user_id):
        db_user = get_object_or_404(Player.objects.all(), pk=user_id)

        data = request.data
        serializer = PlayerSerializer(instance=db_user, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, user_id):
        db_player = get_object_or_404(Player.objects.all(), pk=user_id)

        serializer = PlayerTeamSerializer(db_player, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, user_id):
        user = get_object_or_404(Player.objects.all(), pk=user_id)
        user.delete()
        return Response({"message": "Coach ID `{}` has been deleted.".format(user_id)}, status=status.HTTP_200_OK)


