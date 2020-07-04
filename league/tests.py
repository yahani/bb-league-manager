from django.test import TestCase

# Create your tests here.
from league.models import Team, User, Game
from datetime import date

# models test
class TeamTest(TestCase):

    def create_team(self, name="only a test"):
        return Team.objects.create(name=name)

    def test_team_creation(self):
        t = self.create_team()
        self.assertTrue(isinstance(t, Team))
        self.assertEqual(t.__str__(), t.name)

class CoachTest(TestCase):

    def create_team(self, name="only a test"):
        return Team.objects.create(name=name)
    
    def create_coach(self, team,username="only a test", email="abc@cdf.com",password="123@3Ad"):
        coach = User.objects.create_user(username, email, password=None, is_coach = True)
        coach.team = team
        return coach

    def test_coach_creation(self):
        t = self.create_team()
        c = self.create_coach(team=t)
        self.assertTrue(isinstance(t, Team))
        self.assertTrue(isinstance(c, User))
        self.assertTrue(isinstance(c.team, Team))
        self.assertEqual(c.is_coach, True)


class PlayerTest(TestCase):

    def create_team(self, name="only a test"):
        return Team.objects.create(name=name)
    
    def create_player(self, team,username="only a test", email="abc@cdf.com",password="123@3Ad"):
        player = User.objects.create_user(username, email, password=None, is_player = True)
        player.team = team
        player.height = 190.0
        player.weight = 60.0
        return player

    def test_player_creation(self):
        t = self.create_team()
        p = self.create_player(team=t)
        self.assertTrue(isinstance(t, Team))
        self.assertTrue(isinstance(p, User))
        self.assertTrue(isinstance(p.team, Team))
        self.assertEqual(p.is_player, True)
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