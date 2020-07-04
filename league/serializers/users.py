from rest_framework import serializers
from league.models import User, Coach, Player,Team

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
    user = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Coach
        fields = (
            'user',
        )
    def update(self, instance, validated_data):
        print(validated_data)
        user_data = validated_data.pop('user')
        user = instance.user

        user.username = user_data.get('username', user.username)
        user.email = user_data.get('email', user.email)
        user.password = user_data.get('password', user.password)
        instance.save()
        return instance

class CoachTeamSerializer(serializers.ModelSerializer):
    team = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    user = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Coach
        fields = (
            'user',
            'team'
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


