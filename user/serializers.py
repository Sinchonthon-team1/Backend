from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__' 

    
    
    def create(self, validated_data):
        # User 객체 생성
        user = User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            game_name=validated_data['game_name'],
            age=validated_data['age'],
            password=validated_data['password'],
            tag_line=validated_data['tag_line'],
        )
        
        # school 필드를 포함하여 저장
        school = validated_data.get('school')
        if school:
            user.school = school
            user.save()
        puuid = validated_data.get('puuid')
        if puuid:
            user.puuid = puuid
            user.save()
        
        return user
    