from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Match
from user.models import User
from serializers import MatchSerializer


#경기 등록 초기 데이터
@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
def TeamData(request):
    if request.method == 'GET':
        user = request.user
        school = user.school
        team = team.objects.filter(user=user)
        teamScore = team.score

        response_data = {
            "school" : school,
            "teamScore" : teamScore
        }
        return Response(response_data, status = status.HTTP_200_OK)
    
    if request.method == "POST":
        user = request.user
        serializer = MatchSerializer(data = request.data)

        if not serializer.is_valid():
            return Response({"status": "error", "message": "유효하지 않은 데이터입니다", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        serializer = serializer.validated_data()
        try:
            MatchGroup = Match.objects.filter(user=user, matchDate = serializer.get("matchDate"))
        except MatchGroup.Exist:
            return Response({"message : 등록에 실패하였습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        match = Match.objects.create(
            user=user,
            teamName = serializer.get("temaName"),
            school = serializer.get("school"),
            matchDate = serializer.get("matchDate"),
            teamScore = serializer.get("teamScore"),
        )
        return Response(match, status = status.HTTP_201_CREATED)

        



        


        
        