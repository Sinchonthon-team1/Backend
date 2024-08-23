from rest_framework import serializers
from .models import Team


class TeamNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['teamName']

class TeamSerializer(serializers.ModelSerializer):
    leader = serializers.CharField(source='leader.nickname')
    leaderTier = serializers.CharField(source='leader.tier')
    
    member2 = serializers.CharField(source='member2.nickname', allow_null=True)
    member2Tier = serializers.CharField(source='member2.tier', allow_null=True)

    member3 = serializers.CharField(source='member3.nickname', allow_null=True)
    member3Tier = serializers.CharField(source='member3.tier', allow_null=True)

    member4 = serializers.CharField(source='member4.nickname', allow_null=True)
    member4Tier = serializers.CharField(source='member4.tier', allow_null=True)

    member5 = serializers.CharField(source='member5.nickname', allow_null=True)
    member5Tier = serializers.CharField(source='member5.tier', allow_null=True)
    

    class Meta:
        model = Team
        fields = [
            'teamName', 
            'school', 
            'teamTier',
            'leader', 
            'leaderTier', 
            'member2', 
            'member2Tier', 
            'member3', 
            'member3Tier', 
            'member4', 
            'member4Tier', 
            'member5', 
            'member5Tier'
        ]

class TeamRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = [
            'teamName', 
            'school', 
            'leader', 
            'member2', 
            'member3', 
            'member4', 
            'member5'
        ]
    
    def create(self, validated_data):
        team = Team.objects.create(**validated_data)
        return team
            

