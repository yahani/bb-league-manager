# bb-league-manager

You were hired by a basketball league to develop a management system to monitor games statistics and rankings of a recent tournament.

A total of 16 teams played in the first qualifying round, 8 moved to the next round, and so forth until one team was crowned as champion.

Each team consists of a coach and 10 players. not all players participate in every 
game.

There are 3 types of users in the system - the league admin, a coach, and a player.

•	All 3 types of users can login to the site and logout. Upon login they will view the scoreboard, which will display all games and final scores, and will reflect how the competition progressed and who won.

•	A coach may select his team in order to view a list of the players on it, and the average score of the team. When one of the players in the list is selected, his personal details will be presented, including - player’s name, height, average score, and the number of games he participated in. 

•	A coach can filter players to see only the ones whose average score is in the 90 percentile across the team.

•	The league admin may view all teams details - their average scores, their list of players, and players details.

•	The admin can also view the statistics of the site’s usage - number of times each user logged into the system, the total amount of time each user spent on the site, and who is currently online. (i.e. logged into the site)


## Project Info

•	python version: 3.7.6

## Set up

1. cd bb-league-manager && python manage.py migrate
2. python manage.py seed

## Run tests

cd bb-league-manager && python manage.py test

## Start server

cd bb-league-manager && python manage.py runserver

## API

#### login and obtain token

###### Requset:  POST /login/ 

Body for admin:

{ 

    "username": "admin",
     "password":"admin"

}

for coach:

{ 
    
    "username": "coach1",
     "password":"coach2"

}

for player:

{ 
    
    "username": "player1", 
    "password":"player1"
}

###### Response:

{ 
    
    "username": "coach1", 
    "token":"<token>"
}

For all subsequent requests, add following header

Authorization : Bearer {token}

#### Scoreboard

Request: POST /scoreboard/

Body:  

{
    
     "sort":"asc"  //default "desc"
} 

#### Team Players

Request: GET /team-players/id

Request: POST /team-players/

#### Team Average

Request: GET /team-average/id

#### Player details including average and number of games

Request: GET /player-average/id

#### Team percentile

Request POST /team-percentile/id

Body: 

{ 

"percentile" : 0.7  //default 0.9

} 

#### Admin site stats

Request: GET /site-stats/<id>

Request: POST /site-stats/
