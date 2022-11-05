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

# Add a user to a league
class LeagueAddUser(APIView):
    def post(self, request, format=None):
        # serializer checks if the passed in data (json object) meets the desired requirements
        serializer = LeagueAddUserSerializer(data=request.data)
        if serializer.is_valid():
            #checks for invalid username
            if (len(League.objects.filter(ownerUsername=request.data['ownerUsername'])) == 0):
                return Response(data={"response": False, "error": "League owner username is invalid"})
            else:
                #adds user to the league league
                currentLeague = League.objects.get(ownerUsername=request.data['ownerUsername'])
                newUser = User.objects.get(username=request.data['username'])
                # we're just going to assume user wasn't added previously
                currentLeague.allUsers.add(newUser)
                currentLeague.save()
                return Response(data={"response": True, "error": "Added user to league object", "leagueName": currentLeague.leagueName})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)