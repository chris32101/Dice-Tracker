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

# class enterStats(APIView):
#     def post(self, request, format=None):
#         serializer = enterStatsSerializer(data=request.data)
#         if serializer.is_valid():
#             if (len(Team.objects.filter(name = request.data['team'])) == 0):
#                 return Response(data={"response": False})

#             tmpTeam = Team.objects.get(name = request.data['team'])
#             if (tmpTeam.user1 == request.data['player']): 
#                 tmpTeam.user1.stat2 += request.data['shot']
#                 tmpTeam.user1.stat3 += request.data['tablehit']
#                 tmpTeam.user1.stat4 += request.data['point']
#                 tmpTeam.user1.stat5 += request.data['clink']
#                 tmpTeam.user1.stat6 += request.data['dunk']

#             else:
#                 tmpTeam.user2.stat2 += request.data['shot']
#                 tmpTeam.user2.stat3 += request.data['tablehit']
#                 tmpTeam.user2.stat4 += request.data['point']
#                 tmpTeam.user2.stat5 += request.data['clink']
#                 tmpTeam.user2.stat6 += request.data['dunk']
            
#             tmpTeam.team1Scoreboard += request.data['point']

#             return Response(data={"response": True})
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class saveChallongeData(APIView):
    def post(self, request, format=None):
        serializer = challongeDataSaverSerializer(data=request.data)
        if serializer.is_valid():
            currentLeague = League.objects.get(leagueName=request.data['leagueName'])
            print("Challonge ID --> ")
            print(request.data['challongeID'])
            currentLeague.challongeID = request.data['challongeID']
            currentLeague.challongeURL = request.data['challongeURL']
            currentLeague.save()
            return Response(data={"response": True})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class saveMatchIDs(APIView):
    def post(self, request, format=None):
        serializer = matchIDSaverSerializer(data=request.data)
        if serializer.is_valid():
            currentLeague = League.objects.get(leagueName=request.data['leagueName'])
            matchIDs = request.data['matchIDs']
            teamObjects = []
            print(matchIDs)
            for y in currentLeague.allTeams.all():
                teamObjects.append(y)
            for x in matchIDs:
                newGame = Game(gameID=int(x), team1=teamObjects[0], team2=teamObjects[1], winnerTeam="N/A")
                newGame.save()
                currentLeague.allGames.add(newGame)
                currentLeague.save()
            return Response(data={"response": True})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)