from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from .models import Team
from .serializers import TeamSerializer, TeamRequestSerializer, TeamNameSerializer
from user.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_team(request):
    data = request.data
    user = request.user
    serializer = TeamRequestSerializer(data=data)

    if serializer.is_valid():
        #teamTier = 0
        members = [
            serializer.validated_data.get('leader'),
            serializer.validated_data.get('member2'),
            serializer.validated_data.get('member3'),
            serializer.validated_data.get('member4'),
            serializer.validated_data.get('member5')
        ]

    # 학교, 회원가입 여부 일치 확인
        school = serializer.validated_data.get('school')
        for member in members:
            try:
                checked_member = User.objects.get(gamename = member) #pk가 nickname이 아니면 닉네임 겹칠수도.. 
                #teamTier += checked_member.tier #변수 변경 필요
            
                if school != checked_member.school:
                    return Response({
                        "message": "학교가 일치하지 않습니다."
                    }, status=status.HTTP_409_CONFLICT)

            except ObjectDoesNotExist:
                return Response({
                    "message": "가입하지 않은 사용자입니다."
                }, status=status.HTTP_400_BAD_REQUEST)
        
        if user.gamename not in members:
            return Response({
                "message": "본인이 포함된 팀만 등록 가능합니다."
            }, status=status.HTTP_409_CONFLICT)

        #team = serializer.save(teamTier=teamTier) ##티어 부분이 확정되지 않아 ..
        response_serializer = TeamRequestSerializer(request)

        #return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        team = Team.objects.create(
            teamName=serializer.validated_data['teamName'],
            school=school,
            leader=User.objects.get(gamename=serializer.validated_data['leader']),
            member2=User.objects.get(gamename=serializer.validated_data['member2']),
            member3=User.objects.get(gamename=serializer.validated_data['member3']),
            member4=User.objects.get(gamename=serializer.validated_data['member4']),
            member5=User.objects.get(gamename=serializer.validated_data.get('member5'))
        )

        return Response({
            "message": "팀이 성공적으로 생성되었습니다.",
            "team": TeamRequestSerializer(team).data
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def check_name(request):
    serializer = TeamNameSerializer(data=request.data)
    if serializer.is_valid():
        if Team.objects.filter(teamName=serializer.validated_data['teamName']).exists():
            return Response({
                "message": "중복된 팀 이름입니다."
            }, status=status.HTTP_409_CONFLICT)
        
        return Response({
            "message": "사용 가능한 팀 이름입니다."
        }, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def get_team(request, id):
    try:
        team = Team.objects.get(pk=id)
        serializer = TeamSerializer(team)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Team.DoesNotExist:
        return Response({
            "message": "해당 팀이 존재하지 않습니다."
        }, status=status.HTTP_404_NOT_FOUND)