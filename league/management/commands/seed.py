from django.core.management.base import BaseCommand, CommandError
from league.models import User,Team,Player,Coach,Game,GamePlayer
import random

class Command(BaseCommand):

    def handle(self, *args, **options):
        User.objects.create_superuser(username = "admin",password = "admin",email = "admin@bbleague.com")
        for i in range(16):
            Team.objects.create(name="team{}".format(i+1))

        teams_db =  Team.objects.all()

        for i in range(16):
            User.objects.create_user(username = "coach{}".format(i+1),password = "coach{}".format(i+1),email = "coach{}@bbleague.com".format(i+1),is_coach=True)

        users_db =  User.objects.filter(is_coach=True) 
 
        for i in range(16):
            Coach.objects.create(user=users_db[i], team = teams_db[i])

        for i in range(160):
            User.objects.create_user(username = "player{}".format(i+1),password = "player{}".format(i+1),email = "player{}@bbleague.com".format(i+1),is_player=True)

        users_db =  User.objects.filter(is_player=True) 

        for i in range(16):
            for j in range(10):
                Player.objects.create(user=users_db[10*i+j], team = teams_db[i], weight=random.randint(55, 80), height=random.randint(165, 200), birth_date = '1990-9-9')

        for i in range(8):
            team1 = teams_db[i*2]
            team2 = teams_db[i*2+1]
            score1 = random.randint(5,10)
            score2 = random.randint(0,5)
            date = '2020-03-14'
            Game.objects.create(team1=team1, team2=team2, team1_score = score1, team2_score=score2,date=date)

        for i in range (4):
            team1 = teams_db[i*4]
            team2 = teams_db[i*4+2]
            score1 = random.randint(5,10)
            score2 = random.randint(0,5)
            date = '2020-03-16'
            Game.objects.create(team1=team1, team2=team2, team1_score = score1, team2_score=score2,date=date)

        for i in range (2):
            team1 = teams_db[i*8]
            team2 = teams_db[i*8+4]
            score1 = random.randint(5,10)
            score2 = random.randint(0,5)
            date = '2020-03-18'
            Game.objects.create(team1=team1, team2=team2, team1_score = score1, team2_score=score2,date=date)
        
        Game.objects.create(team1=teams_db[0], team2=teams_db[8], team1_score = 6, team2_score=5,date='2020-03-20')

        games_db = Game.objects.all()

        for i in range (14):
            players1 = games_db[i].team1.players.all()
            for j in range (8):
                score = random.randint(0,5)
                GamePlayer.objects.create(game=games_db[i],player=players1[j], score=score)

            players2 = games_db[i].team2.players.all()
            for j in range (8):
                score = random.randint(0,3)
                GamePlayer.objects.create(game=games_db[i],player=players2[j], score=score)
