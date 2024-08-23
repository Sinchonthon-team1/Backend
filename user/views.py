import os
from rest_framework.views import APIView
from .serializers import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from jwt import ExpiredSignatureError, InvalidTokenError
import logging
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.permissions import IsAuthenticated
from dotenv import load_dotenv

load_dotenv()

import json
from django.conf import settings

file_path = os.path.join(settings.BASE_DIR, 'user', 'universities.json')



# 이메일 주소에서 도메인 부분을 추출하는 함수
def extract_domain(email):
    try:
        return email.split('@')[1]
    except IndexError:
        return None

# 이메일 주소를 확인하는 함수
def find_universities_by_email(email):
    domain_to_check = extract_domain(email)
    matched_universities = []
    if domain_to_check:
        try:
            with open(file_path, 'r') as file:
                universities = json.load(file)
                for university, domain in universities.items():
                    if domain_to_check.endswith(domain):  # 뒷부분 일치 확인
                        matched_universities.append(university)
        except FileNotFoundError:
            print(f"File not found: {file_path}")
    return matched_universities


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            nickname = serializer.validated_data.get('nickname')

            # 이메일 주소와 일치하는 학교 찾기
            matched_universities = find_universities_by_email(email)
            if not matched_universities:
                return Response({"message": "학교 메일이 아닙니다."}, status=status.HTTP_400_BAD_REQUEST)

            user = serializer.save(
                # email = email,
                # nickname=nickname,  # 닉네임을 저장
                # school=matched_universities[0],  # 학교를 저장
                
            )
            user.save()


            return Response({"message": "성공적으로 등록되었습니다."}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class LoginAPIView(APIView):
    def post(self, request):
        user = authenticate(
            email=request.data['email'],
            password=request.data['password']
        )
        if user is not None:
            serializer = UserSerializer(user)
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "User logged in successfully.",
                    "token": {
                        "refresh": refresh_token,
                        "access": access_token
                    },
                },
                status=status.HTTP_200_OK
            )
            res.set_cookie("access_token", access_token, httponly=True) #httponly js로부터 방어
            res.set_cookie("refresh_token", refresh_token, httponly=True)
            return res
        else:
            return Response({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
            

class LogoutAPIView(APIView):
    def post(self, request):
        res = Response({"message": "User logged out successfully."}, status=status.HTTP_200_OK)
        res.delete_cookie("access_token")
        res.delete_cookie("refresh_token")
        return res
    
class tokenAPIView(APIView):
    def get(self, request):
        token = request.COOKIES.get('access_token')
        if token is None:
            return Response({"message": "No token"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            access_token = AccessToken(token)
            access_token.check_exp()
            user = User.objects.get(id=access_token['user_id'])
            serializer = UserSerializer(user)
            return Response({"user": serializer.data}, status=status.HTTP_200_OK)
        except TokenError:
            refresh_token = request.COOKIES.get('refresh_token')
            if refresh_token is None:
                return Response({"message": "No refresh token"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                refresh_token_obj = RefreshToken(refresh_token)
                refresh_token_obj.check_exp()  # 리프레시 토큰 만료 확인
                
                # 리프레시 토큰이 유효하면 새로운 액세스 토큰 발급
                new_access_token = refresh_token_obj.access_token
                
                # 새로운 액세스 토큰을 응답에 포함시킴
                response = Response({"message": "New access token issued", "access_token": str(new_access_token)}, status=status.HTTP_200_OK)
                response.set_cookie('access_token', str(new_access_token), httponly=True)
                return response
            
            except TokenError:
                # 리프레시 토큰도 유효하지 않은 경우 로그아웃 처리
                response = Response({"message": "Invalid refresh token. Please log in again."}, status=status.HTTP_401_UNAUTHORIZED)
                response.delete_cookie('access_token')
                response.delete_cookie('refresh_token')
                return response

        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            return Response({"message": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
