from rest_framework import serializers
from league.models import User, Coach, Player,Team, GamePlayer, Game,LoginEntry
from rest_framework.generics import get_object_or_404

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'password',
            'is_active',
            'is_staff',
            'is_coach',
            'is_player'
        )

    def create(self, validated_data):
        instance = User.objects.create_user(**validated_data)
        instance.save()
        return instance

class CoachSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    class Meta:
        model = Coach
        fields = (
            'user',
        )

    def to_internal_value(self, data):
        user = {}
        if 'username' in data:
            user['username'] = data.pop('username')
        if 'email' in data:
            user['email'] = data.pop('email')
        if 'password' in data:
            user['password'] = data.pop('password')
        if 'team_id' in data:
            data['team_id'] = data.pop('team_id')
        data['user'] = user
        return data

    def update(self, instance, validated_data):
        print(validated_data)
        user_data = validated_data.pop('user')
        user = instance.user

        user.username = user_data.get('username', user.username)
        user.email = user_data.get('email', user.email)
        user.password = user_data.get('password', user.password)
        instance.save()
        return instance

    def create(self, validated_data):
        print(validated_data)
        user_data = validated_data.pop('user')
        user = User.objects.create_user(username=user_data['username'], email=user_data['email'], password=user_data['password'], is_coach = True)
        team_id = validated_data.pop('team_id')
        team = get_object_or_404(Team.objects.all(), pk=team_id)
        instance = Coach.objects.create(user=user,team=team)
        instance.save()
        return instance

class TeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = '__all__'

class CoachTeamSerializer(serializers.ModelSerializer):
    team = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    user = UserSerializer(many=False)
    class Meta:
        model = Coach
        fields = (
            'user',
            'team'
        )

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

class PlayerSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Player
        fields = (
            'user',
            'height',
            'weight',
            'birth_date'
        )
    def to_internal_value(self, data):
        user = {}
        if 'username' in data:
            user['username'] = data.pop('username')
        if 'email' in data:
            user['email'] = data.pop('email')
        if 'password' in data:
            user['password'] = data.pop('password')
        if 'team_id' in data:
            data['team_id'] = data.pop('team_id')
        data['user'] = user
        return data

    def update(self, instance, validated_data):
        user = instance.user
        user_data = validated_data.pop('user')
        user.username = user_data.get('username', user.username)
        user.email = user_data.get('email', user.email)
        user.password = user_data.get('password', user.password)
        instance.save()
        return instance

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(username=user_data['username'], email=user_data['email'], password=user_data['password'], is_player = True)
        team_id = validated_data.pop('team_id')
        team = get_object_or_404(Team.objects.all(), pk=team_id)
        instance = Player.objects.create(user=user,team=team,height=validated_data.get('height', None) ,weight=validated_data.get('weight', None),birth_date=validated_data.get('birth_date', None)  )
        instance.save()
        return instance

class PlayerAvgSerializer(serializers.ModelSerializer):
    avg_score = serializers.SerializerMethodField()

    def get_avg_score(self, obj):
        try:
            return obj.avg_score
        except:
            return None

    class Meta:
        model = Player
        fields = '__all__'

class PlayerTeamSerializer(serializers.ModelSerializer):
    team = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    user = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Player
        fields = (
            'user',
            'team',
            'height',
            'weight',
            'birth_date'
        )

class TeamPlayersSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True, read_only=True)
    class Meta:
        model = Team
        fields = (
            'id',
            'name',
            'players'
        )

class GamePlayersSerializer(serializers.ModelSerializer):
    team1 = TeamSerializer(many=False, read_only=True)
    team2 = TeamSerializer(many=False, read_only=True)
    players = PlayerSerializer(many=True, read_only=True)
    
    class Meta:
        model = Game
        fields = (
            'id',
            'team1',
            'team2',
            'team1_score',
            'team2_score',
            'date',
            'players'
        )

class GamePlayerSerializer(serializers.ModelSerializer):
    game = GameSerializer(many=False,read_only=True)
    player = PlayerSerializer(many=False,read_only=True)

    class Meta:
        model = GamePlayer
        fields = (
            'id',
            'game',
            'player',
            'score'
        )

class PlayerGamesSerializer(serializers.ModelSerializer):
    games = GameSerializer(many=True, read_only=True)
    class Meta:
        model = Player
        fields = (
            'user',
            'height',
            'weight',
            'birth_date',
            'games'
        )

class LoginEntrySerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    class Meta:
        model = LoginEntry
        fields = (
            'user',
            'login_time',
            'logout_time'
        )