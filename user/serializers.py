from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__' 

    
    
    def create(self, validated_data):
        school = validated_data.pop('school', None)
        
        user = User.objects.create_user(
            email = validated_data['email'],
            nickname = validated_data['nickname'],
            password = validated_data['password'],
        )

        # school 데이터가 있을 경우 추가로 저장
        if school:
            user.school = school
            user.save()
        
        return user
    