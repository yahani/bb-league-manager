from rest_framework import serializers
from league.models import Team
from league.serializers.users import PlayerSerializer

class TeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = '__all__'


class TeamPlayersSerializer(serializers.ModelSerializer):
    player_set = PlayerSerializer(many=True, read_only=True)
    class Meta:
        model = Team
        fields = (
            'id',
            'name',
            'player_set'
        )