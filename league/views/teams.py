from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.generics import get_object_or_404, ListAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from league.serializers import TeamSerializer,TeamPlayersSerializer
from league.models import Team
# Create your views here.

class TeamEndPoint(APIView):
    def put(self, request):
        if 'name' not in request.data:
            raise ParseError("Empty content")

        data = request.data
        serializer = TeamSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, team_id):
        db_team = get_object_or_404(Team.objects.all(), pk=team_id)

        data = request.data
        serializer = TeamSerializer(instance=db_team, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, team_id):
        db_team = get_object_or_404(Team.objects.all(), pk=team_id)

        serializer = TeamPlayersSerializer(db_team, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, team_id):
        team = get_object_or_404(Team.objects.all(), pk=team_id)
        team.delete()
        return Response({"message": "Team ID `{}` has been deleted.".format(team_id)}, status=status.HTTP_200_OK)
