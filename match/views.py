from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Match
from user.models import User
from .serializers import MatchSerializer
from team.models import Team



#경기 등록 데이터

@api_view(['POST','GET'])
# @permission_classes([IsAuthenticated])
def MatchRegistData(request):
    # if request.method == 'GET':
    #     user = request.user
    #     school = user.school
    #     team = Team.objects.filter(user=user)
    #     teamScore = Team.score

    #     response_data = {
    #         "school" : school,
    #         "teamScore" : teamScore
    #     }
    #     return Response(response_data, status = status.HTTP_200_OK)
    
    if request.method == "POST":
        # user = request.user
        serializer = MatchSerializer(data = request.data)

        if not serializer.is_valid():
            return Response({"status": "error", "message": "유효하지 않은 데이터입니다", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        
        # try:
        #     MatchGroup = Match.objects.filter(user=user, teamName = serializer.get("teamName"))
        # except MatchGroup.Exist:
        #     return Response({"message : 해당 팀으로 등록할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)


        match_exists = Match.objects.filter(
        teamName=validated_data.get("teamName"),
        matchDate=validated_data.get("matchDate")
    ).exists()

    if match_exists:
        return Response(
            {"message": "해당 팀으로 등록할 수 없습니다."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Match 객체를 생성합니다.
    match = Match.objects.create(
        teamName=validated_data.get("teamName"),
        school=validated_data.get("school"),
        matchDate=validated_data.get("matchDate"),
        teamScore=validated_data.get("teamScore"),
        openChatUrl=validated_data.get("openChatUrl")
    )

    # 직렬화된 데이터를 반환합니다.
    match_serialized = MatchSerializer(match)
    return Response(match_serialized.data, status=status.HTTP_201_CREATED)


#경기 리스트 데이터
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def MatchList(request):
    if request.method == 'GET':
        # user = request.user
        matches = Match.objects.all()

        # Prepare the list of formatted memos
        formatted_matches = []
        for match in matches:
            formatted_match = {
            "id": match.id,
            "teamName": match.teamName,
            "school": match.school,  # Adjust according to your actual model field names
            "matchDate": match.matchDate,  # Adjust according to your actual model field names
            "teamScore": match.teamScore,  # Adjust according to your actual model field names
            "openChatUrl": match.openChatUrl,  # Adjust according to your actual model field names
            }
            formatted_matches.append(formatted_match)

        response_data = {
        "detail": "경기가 성공적으로 조회되었습니다.",
        "data":
            {
                "memo": formatted_matches
            }
        }

    return Response(response_data, status=status.HTTP_200_OK)

