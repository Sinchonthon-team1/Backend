from django.urls import path
from team.views import create_team, check_name, view_team, delete_team

urlpatterns = [
    path('/team/', create_team, name='create_team'),
    path('/team/checkname/', check_name, name='check_name'),
    path('/team/{str:id}/', view_team, name='view_team')
]