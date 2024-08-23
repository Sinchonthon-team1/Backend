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
            nickname=validated_data['nickname'],
            password=validated_data['password'],
        )
        
        # school 필드를 포함하여 저장
        school = validated_data.get('school')
        if school:
            user.school = school
            user.save()
        
        return user
    