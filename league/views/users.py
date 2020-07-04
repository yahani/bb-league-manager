from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.generics import get_object_or_404, ListAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from league.serializers.users import CoachTeamSerializer,UserSerializer,CoachSerializer,PlayerTeamSerializer,PlayerSerializer
from league.models import User,Coach,Team,Player
# Create your views here.

class CoachEndPoint(APIView):
    def put(self, request):
        if 'username' not in request.data or 'password' not in request.data or 'email' not in request.data or 'team_id' not in request.data:
            raise ParseError("Empty content")
        
        team_id = request.data.pop('team_id')

        userSerializer = UserSerializer(data=request.data)
        if userSerializer.is_valid():
            userSerializer.save()
            user = get_object_or_404(User.objects.all(), pk=userSerializer.data['id'])
            team = get_object_or_404(Team.objects.all(), pk=team_id)
            coach = Coach.objects.create(user=user,team=team)
            return Response(userSerializer.data, status=status.HTTP_200_OK)
        else:
            return Response(userSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, user_id):
        db_user = get_object_or_404(User.objects.all(), pk=user_id)

        data = request.data
        serializer = UserSerializer(instance=db_user, data=data, partial=True)

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
        
        team_id = request.data.pop('team_id')
        height=request.data.pop('height')
        weight =request.data.pop('weight')
        birth_date =request.data.pop('birth_date')

        userSerializer = UserSerializer(data=request.data)
        if userSerializer.is_valid():
            userSerializer.save()
            user = get_object_or_404(User.objects.all(), pk=userSerializer.data['id'])
            team = get_object_or_404(Team.objects.all(), pk=team_id)
            coach = Player.objects.create(user=user,team=team, height=height,weight=weight,birth_date=birth_date)
            return Response(userSerializer.data, status=status.HTTP_200_OK)
        else:
            return Response(userSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

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


