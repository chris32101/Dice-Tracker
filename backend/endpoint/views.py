from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import *
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .models import *
from .serializers import *
from rest_framework import status

# Generate user objects when user registers for an account
class GenerateUserObject(APIView):
    def post(self, request, format=None):
        # serializer checks if the passed in data (json object) meets the desired requirements
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            #checks to see if user already exisits
            if (len(User.objects.filter(username=str(request.data['username']))) == 1):
                return Response(data={"response": False, "error": "There was already a saved User object for this user"})
            #otherwise creates a new user
            elif (len(User.objects.filter(username=str(request.data['username']))) == 0):
                user = User(username=str(request.data['username']), email=str(request.data['email']), stat1=0, stat2=0, stat3=0, stat4=0, stat5=0, stat6=0, stat7=0, stat8=0, stat9=0, stat10=0, stat11=0)
                user.save()
                return Response(data={"response": True, "error": "Created a User object for this user"})
            else:
                return Response(data={"response": True, "error": "THIS SHOULDN'T APPEAR"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# GenerateUserStats sends all stats of a user to the API endpoint under the URL getUserStats/ in JSON format
# Inputs:
#   User
# Outputs:
#   stats of the user
class GenerateUserStats(APIView):
    def post(self, request, format=None):
        # serializer checks if the passed in data (json object) meets the desired requirements
        serializer = StatSerializer(data = request.data)
        tmpName = str(request.data['username'])
        if serializer.is_valid():
            if (len(User.objects.filter(username = tmpName)) == 1):
                tmpUser = User.objects.get(username = tmpName)
                #returns the stats of the user (shots, table hits, points, clinks, dunks, potential points, catches, drops, table hit percentage, potential point percentage)
                return Response(data={  "stat1" : tmpUser.stat1,
                                        "stat2" : tmpUser.stat2,
                                        "stat3" : tmpUser.stat3,
                                        "stat4" : tmpUser.stat4,
                                        "stat5" : tmpUser.stat5,
                                        "stat6" : tmpUser.stat6,
                                        "stat7" : tmpUser.stat7,
                                        "stat8" : tmpUser.stat8,
                                        "stat9" : tmpUser.stat9,
                                        "stat10" : tmpUser.stat10,
                                        "stat11" : tmpUser.stat11})

            else:
                return Response(data={"response": True, "error": "This user does not exist"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Creating a league object based off passed in JSON key information
class LeagueCreate(APIView):
    def post(self, request, format=None):
        # serializer checks if the passed in data (json object) meets the desired requirements
        serializer = LeagueCreateSerializer(data=request.data)
        if serializer.is_valid():
            #check if league has already been started
            if (len(League.objects.filter(ownerUsername=str(request.data['ownerUsername']))) >= 1):
                return Response(data={"response": False, "error": "User already started a league"})
            #Checks to see if a unique league name was used
            elif (len(League.objects.filter(leagueName=str(request.data['leagueName']))) >= 1):
                return Response(data={"response": False, "error": "League name has been used previously"})
            #creates league
            else:
                league = League(ownerUsername=str(request.data['ownerUsername']), leagueName=str(request.data['leagueName']), started=0, teamLength=int(request.data['teamLength']))
                league.save()
                return Response(data={"response": True, "error": "Created league for user", "leagueName": str(request.data['leagueName'])})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Create a team and add to league
class addTeamToLeague(APIView):
    def post(self, request, format=None):
        serializer = addTeamToLeagueSerializer(data=request.data)
        if serializer.is_valid():
            if (len(League.objects.filter(ownerUsername=request.data['ownerUsername'])) == 0):
                return Response(data={"response": False, "error": "This league doesn't exist"})
            if (len(Team.objects.filter(name=request.data['name'])) != 0):
                return Response(data={"response": False, "error": "This team name is taken"})
            gameScoreboard = GameScoreboard(totalPoints=0)
            gameScoreboard.save()
            currentTeam = Team(name = str(request.data['name']), user1 = User.objects.get(username=str(request.data['user1'])), user2 = User.objects.get(username=str(request.data['user2'])))
            currentTeam.save()
            currentTeam.team1Scoreboard.add(gameScoreboard)
            currentTeam.save()
            league = League.objects.get(ownerUsername=request.data['ownerUsername'])    
            league.allTeams.add(currentTeam)
            #print(league.allTeams.all())
            return Response(data={"response": True, "error": "Successfully added the team"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Get all active teams (all teams that have joined the league)
class GetActiveTeamsInLeague(APIView):
    def post(self, request, format=None):
        if serializer.is_valid():
            #checks for valid league name
            if (len(League.objects.filter(leagueName=request.data['leagueName'])) == 0):
                return Response(data={"response": False, "error": "The data for the requested league doesn't exist"})
            else:
                #returns all teams of the league
                teamsInLeague = []
                teamsInLeague = League.objects.get(leagueName=request.data['leagueName']).allTeams.all()
                teamsInLeague.values() -> <QuerySet [{'id': 1, 'name': 'TEAMONE', 'user1_id': UUID('4b7235cf-12da-49b0-8b75-497b47b66116'), 'user2_id': UUID('8d4e9ec9-484f-455e-998d-8112c5248b73')}]>
                
                currLeague = League.objects.get(leagueName=request.data['leagueName'])
                challongeID = currLeague.challongeID
                challongeURL = currLeague.challongeURL
                leagueOwnerUsername = currLeague.ownerUsername
                
                return Response(data={"response": True, "leagueOwnerUsername": leagueOwnerUsername, "leagueTeams": teamsInLeague, "challongeID": challongeID, "challongeURL": challongeURL})    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)