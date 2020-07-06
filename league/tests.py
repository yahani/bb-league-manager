from django.test import TestCase
from rest_framework.test import APIRequestFactory,APITestCase
# Create your tests here.
from league.models import Team, User, Game,Coach,Player,GamePlayer
from league.serializers import GameSerializer,TeamPlayersSerializer,PlayerAvgSerializer
from datetime import date
from django.urls import reverse
from rest_framework import status
import random


# models test
class TeamTest(TestCase):

    def create_team(self, name="only a test"):
        Team.objects.create(name=name)

    def test_team_creation(self):
        self.create_team()
        t = Team.objects.get(name="only a test")
        self.assertTrue(isinstance(t, Team))
        self.assertEqual(t.__str__(), t.name)

class CoachTest(TestCase):

    def create_team(self, name="only a test"):
        return Team.objects.create(name=name)
    
    def create_coach(self, team,username="only a test", email="abc@cdf.com",password="123@3Ad"):
        user = User.objects.create_user(username, email, password=None, is_coach = True)
        coach = Coach.objects.create(user=user,team=team)
        return coach

    def test_coach_creation(self):
        t = self.create_team()
        c = self.create_coach(team=t)
        self.assertTrue(isinstance(c, Coach))
        self.assertTrue(isinstance(c.team, Team))

class PlayerTest(TestCase):

    def create_team(self, name="only a test"):
        return Team.objects.create(name=name)
    
    def create_player(self, team,username="only a test", email="abc@cdf.com",password="123@3Ad"):
        user = User.objects.create_user(username, email, password=None, is_player = True)
        player = Player.objects.create(user=user,team=team,height=190.0,weight=60.0)
        return player

    def test_player_creation(self):
        t = self.create_team()
        p = self.create_player(team=t)
        self.assertTrue(isinstance(p, Player))
        self.assertTrue(isinstance(p.team, Team))
        self.assertEqual(p.height, 190.0)
        self.assertEqual(p.weight, 60.0)
        self.assertEqual(p.team.__str__(), t.name)

class GameTest(TestCase):

    def create_team(self, name="only a test"):
        return Team.objects.create(name=name)
    
    def create_game(self, team1,team2, team1_score=2,team2_score=3,date =date(2019, 7, 27)):
        return Game.objects.create(team1=team1, team2=team2, team1_score=team1_score, team2_score=team2_score,date=date)

    def test_game_creation(self):
        t1 = self.create_team("team1")
        t2 = self.create_team("team2")
        g = self.create_game(t1,t2)
        self.assertTrue(isinstance(g, Game))
        self.assertTrue(isinstance(g.team1, Team))
        self.assertTrue(isinstance(g.team2, Team))
        self.assertEqual(g.team1.name, "team1")
        self.assertEqual(g.team2.name, "team2")

class AdminLoginApiTestCase(APITestCase):
    def test_login(self):
        admin = User.objects.create_superuser(username='testadmin', email='admin@bbleague.com', password='testadmin')
        url = reverse('login')
        data = {'username': 'testadmin', 'password':'testadmin'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testadmin')

class CoachLoginApiTestCase(APITestCase):
    def setUp(self):
        t=Team.objects.create(name="team")
        u = User.objects.create_user(username='coach', email='coach@bbleague.com', password='coach')
        Coach.objects.create(user=u,team=t)

    def test_login(self):
        data = {'username': 'coach', 'password':'coach'}
        url = reverse('login')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)
        self.assertEqual(response.data['username'], 'coach')

    def test_login_invalid(self):
        data = {'username': 'coach', 'password':'coach1'}
        url = reverse('login')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class PlayerLoginApiTestCase(APITestCase):
    def setUp(self):
        t=Team.objects.create(name="team")
        u = User.objects.create_user(username='player', email='player@bbleague.com', password='player')
        Player.objects.create(user=u,team=t,weight=65,height=189)

    def test_login(self):
        data = {'username': 'player', 'password':'player'}
        url = reverse('login')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)
        self.assertEqual(response.data['username'], 'player')

class GetAllGamesTest(APITestCase):
    """ Test module for GET all puppies API """

    def setUp(self):
        for i in range(4):
            Team.objects.create(name="team{}".format(i+1))
        teams_db =  Team.objects.all()
        for i in range(4):
            User.objects.create_user(username = "coach{}".format(i+1),password = "coach{}".format(i+1),email = "coach{}@bbleague.com".format(i+1),is_coach=True)
        users_db =  User.objects.filter(is_coach=True) 
        for i in range(4):
            Coach.objects.create(user=users_db[i], team = teams_db[i])
        for i in range(16):
            User.objects.create_user(username = "player{}".format(i+1),password = "player{}".format(i+1),email = "player{}@bbleague.com".format(i+1),is_player=True)
        users_db =  User.objects.filter(is_player=True) 
        for i in range(4):
            for j in range(4):
                Player.objects.create(user=users_db[4*i+j], team = teams_db[i], weight=random.randint(55, 80), height=random.randint(165, 200), birth_date = '1990-9-9')

        for i in range(2):
            team1 = teams_db[i*2]
            team2 = teams_db[i*2+1]
            score1 = random.randint(5,10)
            score2 = random.randint(0,5)
            date = '2020-03-14'
            Game.objects.create(team1=teams_db[i*2], team2=teams_db[i*2+1], team1_score = score1, team2_score=score2,date=date)

    def test_get_all_games(self):
        user = User.objects.get(username='player1')
        self.client.force_authenticate(user=user)
        # get API response
        self.client.login(username='player1', password='player1')
        response = self.client.post(reverse('scoreboard'))
        # get data from db
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_games_not_auth(self):
        # get API response
        response = self.client.post(reverse('scoreboard'))
        # get data from db
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class TeamPlayersTest(APITestCase):
    """ Test module for GET all puppies API """

    def setUp(self):
        User.objects.create_superuser(username='admin', email='admin@bbleague.com', password='admin')
        t1 = Team.objects.create(name="team1")
        u = User.objects.create_user(username = "coach1",password = "coach1",email = "dd",is_coach=True)
        Coach.objects.create(user=u, team = t1)
        u = User.objects.create_user(username = "player1",password = "player1",email = "dd",is_player=True)
        Player.objects.create(user=u, team = t1, weight=random.randint(55, 80), height=random.randint(165, 200), birth_date = '1990-9-9')
        u = User.objects.create_user(username = "player2",password = "player2",email = "dd",is_player=True)
        Player.objects.create(user=u, team = t1, weight=random.randint(55, 80), height=random.randint(165, 200), birth_date = '1990-9-9')        
        t2 = Team.objects.create(name="team2")
        u = User.objects.create_user(username = "player3",password = "player3",email = "dd",is_player=True)
        Player.objects.create(user=u, team = t2, weight=random.randint(55, 80), height=random.randint(165, 200), birth_date = '1990-9-9')
        date = '2020-03-14'

    def test_team_players_coach(self):
        user = User.objects.get(username='coach1')
        self.client.force_authenticate(user=user)
        # get API response
        self.client.login(username='coach1', password='coach1')
        response = self.client.get(reverse('team-players', kwargs={'team_id': 1}) )
        # get data from db
        team = Team.objects.get(pk=1)
        serializer = TeamPlayersSerializer(team, many=False)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_team_players_coach_my_team(self):
        user = User.objects.get(username='coach1')
        self.client.force_authenticate(user=user)
        # get API response
        self.client.login(username='coach1', password='coach1')
        response = self.client.post(reverse('my-team') )
        # get data from db
        team = Team.objects.get(pk=1)
        serializer = TeamPlayersSerializer(team, many=False)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_team_players_admin(self):
        user = User.objects.get(username='admin')
        self.client.force_authenticate(user=user)
        # get API response
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('team-players', kwargs={'team_id': 1}) )
        # get data from db
        team = Team.objects.get(pk=1)
        serializer = TeamPlayersSerializer(team, many=False)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_team_players_admin_my_team_fail(self):
        user = User.objects.get(username='admin')
        self.client.force_authenticate(user=user)
        # get API response
        self.client.login(username='admin', password='admin')
        response = self.client.post(reverse('my-team') )
        # get data from db
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_team_players_coach_auth_fail(self):
        user = User.objects.get(username='coach1')
        self.client.force_authenticate(user=user)
        # get API response
        self.client.login(username='coach1', password='coach1')
        response = self.client.get(reverse('team-players', kwargs={'team_id': 2}) )
        # get data from db
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_team_players_player_auth_fail(self):
        user = User.objects.get(username='player1')
        self.client.force_authenticate(user=user)
        # get API response
        self.client.login(username='player1', password='player1')
        response = self.client.get(reverse('team-players', kwargs={'team_id': 1}) )
        # get data from db
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class TeamAverageTest(APITestCase):
    """ Test module for GET all puppies API """

    def setUp(self):
        User.objects.create_superuser(username='admin', email='admin@bbleague.com', password='admin')
        t1 = Team.objects.create(name="team1")
        u = User.objects.create_user(username = "coach1",password = "coach1",email = "dd",is_coach=True)
        Coach.objects.create(user=u, team = t1)
        u = User.objects.create_user(username = "player1",password = "player1",email = "dd",is_player=True)
        Player.objects.create(user=u, team = t1, weight=random.randint(55, 80), height=random.randint(165, 200), birth_date = '1990-9-9')
        t2 = Team.objects.create(name="team2")
        date = '2020-03-14'
        Game.objects.create(team1=t1, team2=t2, team1_score = 2, team2_score=3,date=date)
        Game.objects.create(team1=t1, team2=t2, team1_score = 4, team2_score=7,date=date)
        Game.objects.create(team1=t2, team2=t1, team1_score = 4, team2_score=3,date=date)

    def test_team_average_coach(self):
        user = User.objects.get(username='coach1')
        self.client.force_authenticate(user=user)
        # get API response
        self.client.login(username='coach1', password='coach1')
        response = self.client.get(reverse('team-average', kwargs={'team_id': 1}) )
        self.assertTrue(isinstance(response.data, float))
        self.assertEqual(response.data, 3.0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_team_average_admin(self):
        user = User.objects.get(username='admin')
        self.client.force_authenticate(user=user)
        # get API response
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('team-average', kwargs={'team_id': 1}) )
        self.assertTrue(isinstance(response.data, float))
        self.assertEqual(response.data, 3.0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_tteam_average_player_auth_fail(self):
        user = User.objects.get(username='player1')
        self.client.force_authenticate(user=user)
        # get API response
        self.client.login(username='player1', password='player1')
        response = self.client.get(reverse('team-average', kwargs={'team_id': 1}) )
        # get data from db
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_team_average_coach_auth_fail(self):
        user = User.objects.get(username='coach1')
        self.client.force_authenticate(user=user)
        # get API response
        self.client.login(username='coach1', password='coach1')
        response = self.client.get(reverse('team-average', kwargs={'team_id': 2}) )
        # get data from db
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class PlayerAverageTest(APITestCase):
    """ Test module for GET all puppies API """

    def setUp(self):
        t1 = Team.objects.create(name="team1")
        u = User.objects.create_user(username = "coach1",password = "coach1",email = "dd",is_coach=True)
        Coach.objects.create(user=u, team = t1)
        u = User.objects.create_user(username = "player1",password = "player1",email = "dd",is_player=True)
        p1 = Player.objects.create(user=u, team = t1, weight=random.randint(55, 80), height=random.randint(165, 200), birth_date = '1990-9-9')
        t2 = Team.objects.create(name="team2")
        u = User.objects.create_user(username = "player2",password = "player2",email = "dd",is_player=True)
        p2 = Player.objects.create(user=u, team = t2, weight=random.randint(55, 80), height=random.randint(165, 200), birth_date = '1990-9-9')
        
        g1 = Game.objects.create(team1=t1, team2=t2, team1_score = 4, team2_score=7,date='2020-3-3')
        g2= Game.objects.create(team1=t1, team2=t2, team1_score = 4, team2_score=7,date='2020-3-3')
        GamePlayer.objects.create(game=g1, player=p1, score = 2)
        GamePlayer.objects.create(game=g2, player=p1, score = 4)
        User.objects.create_superuser(username='admin', email='admin@bbleague.com', password='admin')

    def test_player_average_coach(self):
        user = User.objects.get(username='coach1')
        self.client.force_authenticate(user=user)
        # get API response
        self.client.login(username='coach1', password='coach1')
        response = self.client.get(reverse('player-average', kwargs={'player_id': 2}) )
        self.assertEqual(response.data['average'], 3)
        self.assertEqual(response.data['num_of_games'], 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_player_average_admin(self):
        user = User.objects.get(username='admin')
        self.client.force_authenticate(user=user)
        # get API response
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('player-average', kwargs={'player_id': 2}) )
        self.assertEqual(response.data['average'], 3)
        self.assertEqual(response.data['num_of_games'], 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_player_average_player_auth_fail(self):
        user = User.objects.get(username='player1')
        self.client.force_authenticate(user=user)
        # get API response
        self.client.login(username='player1', password='player1')
        response = self.client.get(reverse('player-average', kwargs={'player_id': 1}) )
        # get data from db
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_player_average_coach_auth_fail(self):
        user = User.objects.get(username='coach1')
        self.client.force_authenticate(user=user)
        # get API response
        self.client.login(username='coach1', password='coach1')
        response = self.client.get(reverse('player-average', kwargs={'player_id': 3}) )
        # get data from db
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PlayerPercentileTest(APITestCase):
    """ Test module for GET all puppies API """

    def setUp(self):
        t1 = Team.objects.create(name="team1")
        u = User.objects.create_user(username = "coach1",password = "coach1",email = "dd",is_coach=True)
        Coach.objects.create(user=u, team = t1)
        u = User.objects.create_user(username = "player1",password = "player1",email = "dd",is_player=True)
        p1 = Player.objects.create(user=u, team = t1, weight=random.randint(55, 80), height=random.randint(165, 200), birth_date = '1990-9-9')
        u = User.objects.create_user(username = "player2",password = "player1",email = "dd",is_player=True)
        p2 = Player.objects.create(user=u, team = t1, weight=random.randint(55, 80), height=random.randint(165, 200), birth_date = '1990-9-9')
        u = User.objects.create_user(username = "player3",password = "player1",email = "dd",is_player=True)
        p3 = Player.objects.create(user=u, team = t1, weight=random.randint(55, 80), height=random.randint(165, 200), birth_date = '1990-9-9')
        u = User.objects.create_user(username = "player4",password = "player1",email = "dd",is_player=True)
        p4 = Player.objects.create(user=u, team = t1, weight=random.randint(55, 80), height=random.randint(165, 200), birth_date = '1990-9-9')
                             
        
        t2 = Team.objects.create(name="team2")
        u = User.objects.create_user(username = "player5",password = "player2",email = "dd",is_player=True)
        p2 = Player.objects.create(user=u, team = t2, weight=random.randint(55, 80), height=random.randint(165, 200), birth_date = '1990-9-9')
        
        g1 = Game.objects.create(team1=t1, team2=t2, team1_score = 4, team2_score=7,date='2020-3-3')
        g2= Game.objects.create(team1=t1, team2=t2, team1_score = 4, team2_score=7,date='2020-3-3')
    
        GamePlayer.objects.create(game=g1, player=p1, score = 3)#p1->avg=4
        GamePlayer.objects.create(game=g2, player=p1, score = 5)
        GamePlayer.objects.create(game=g1, player=p2, score = 1)#p1->avg=1
        GamePlayer.objects.create(game=g2, player=p2, score = 1)
        GamePlayer.objects.create(game=g1, player=p3, score = 2)#p1->avg=3
        GamePlayer.objects.create(game=g2, player=p3, score = 4)
        GamePlayer.objects.create(game=g1, player=p4, score = 0)#p1->avg=2
        GamePlayer.objects.create(game=g2, player=p4, score = 4)

        User.objects.create_superuser(username='admin', email='admin@bbleague.com', password='admin')

    def test_player_percentile(self):
        user = User.objects.get(username='coach1')
        self.client.force_authenticate(user=user)
        self.client.login(username='coach1', password='coach1')
        response = self.client.post(reverse('team-percentile', kwargs={'team_id': 1}) )
        p = Player.objects.get(pk=2)
        p.avg_score = 4
        serializer = PlayerAvgSerializer((p,), many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_player_percentile_admin_fail(self):
        user = User.objects.get(username='admin')
        self.client.force_authenticate(user=user)
        self.client.login(username='admin', password='admin')
        response = self.client.post(reverse('team-percentile', kwargs={'team_id': 1}) )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_player_percentile_player_auth_fail(self):
        user = User.objects.get(username='player1')
        self.client.force_authenticate(user=user)
        self.client.login(username='player1', password='player1')
        response = self.client.post(reverse('team-percentile', kwargs={'team_id': 1}) )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_player_Percentile_coach_auth_fail(self):
        user = User.objects.get(username='coach1')
        self.client.force_authenticate(user=user)
        self.client.login(username='coach1', password='coach1')
        response = self.client.post(reverse('team-percentile', kwargs={'team_id': 2}) )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)