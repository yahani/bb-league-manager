from rest_framework import serializers
from league.models import Team, Game
from league.serializers.teams import TeamSerializer

class GameSerializer(serializers.ModelSerializer):
    team1 = TeamSerializer(many=False, read_only=True)
    team2 = TeamSerializer(many=False, read_only=True)
    
    class Meta:
        model = Game
        fields = (
            'id',
            'team1',
            'team2',
            'team1_score',
            'team2_score',
            'date'
        )

